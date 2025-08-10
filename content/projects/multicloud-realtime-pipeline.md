# Multi-Cloud Real-time Data Pipeline (AWS ↔ GCP)

## 프로젝트 개요

PnE(Probability and Enhancement) 시스템 도입에 따라 글로벌 카지노 게임 3종의 일배치 시스템을 준실시간 배치로 전환하는 멀티클라우드 데이터 파이프라인을 구축했습니다. AWS DMS CDC, Lambda, SQS를 활용하여 RDS Aurora의 데이터를 Google BigQuery로 준실시간으로 이동시키는 고가용성 파이프라인을 설계 및 구현했습니다.

**핵심 성과:**
- 일 4,000만 건 데이터의 준실시간 처리 (평균 지연시간 1-2분)
- 99.9% 데이터 정합성 보장
- 실시간 FDS(Fraud Detection System) 및 대시보드 지원
- 6개 DB 클러스터, 70여 개 테이블의 통합 관리

## 프로젝트 목표

### 비즈니스 요구사항
1. **실시간성 확보**: 기존 일배치에서 준실시간 배치로 전환 (1-2분 지연)
2. **확장성**: 글로벌 카지노 게임 3종, 6개 DB 클러스터 지원
3. **안정성**: 일 4,000만 건 데이터의 무손실 전송 보장
4. **운영 효율성**: DW/BI 엔지니어의 독립적인 테이블 관리 가능

### 기술적 목표
- AWS와 GCP 간 멀티클라우드 아키텍처 구축
- CDC(Change Data Capture) 기반 실시간 데이터 동기화
- 장애 복구 및 백필 시스템 구현
- 자동화된 스키마 관리 및 테이블 생성

## 기술적 도전과 해결 과정

### 1. 멀티클라우드 CDC 파이프라인 아키텍처

**아키텍처 설계:**
```
AWS RDS Aurora (MySQL)
    ↓ (CDC)
AWS DMS (Database Migration Service)
    ↓ (Parquet + GZ)
Amazon S3
    ↓ (Event Trigger)
Amazon SQS
    ↓ (Lambda Trigger)
AWS Lambda (Python)
    ↓ (BigQuery API)
Google BigQuery
```

**파이프라인 핵심 구현:**
```python
import json
import boto3
import logging
from google.cloud import bigquery
from google.cloud.exceptions import Conflict
import pandas as pd
from io import BytesIO
import gzip
from datetime import datetime
import os

# 환경 변수 설정
BIGQUERY_PROJECT = os.environ['BIGQUERY_PROJECT']
BIGQUERY_DATASET = os.environ['BIGQUERY_DATASET']
S3_BUCKET = os.environ['S3_BUCKET']

# 클라이언트 초기화
s3_client = boto3.client('s3')
bq_client = bigquery.Client(project=BIGQUERY_PROJECT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """SQS 이벤트 처리 Lambda 핸들러"""
    
    try:
        # SQS 메시지 처리
        for record in event['Records']:
            # S3 이벤트 정보 파싱
            s3_event = json.loads(record['body'])
            s3_records = s3_event.get('Records', [])
            
            for s3_record in s3_records:
                bucket = s3_record['s3']['bucket']['name']
                key = s3_record['s3']['object']['key']
                
                # CDC 파일 처리
                result = process_cdc_file(bucket, key)
                logger.info(f"처리 완료: {key}, 결과: {result}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('성공적으로 처리되었습니다')
        }
        
    except Exception as e:
        logger.error(f"처리 중 오류 발생: {str(e)}")
        raise e

def process_cdc_file(bucket, key):
    """CDC 파일을 BigQuery로 로드"""
    
    try:
        # 파일명에서 테이블 정보 추출
        table_info = extract_table_info(key)
        table_name = table_info['table_name']
        database_name = table_info['database_name']
        timestamp = table_info['timestamp']
        
        # BigQuery Job ID 생성 (중복 방지용)
        job_id = f"{timestamp}_{database_name}_{table_name}"
        
        # 중복 Job 체크
        if check_duplicate_job(job_id):
            logger.info(f"중복된 Job ID: {job_id}, 건너뜀")
            return {"status": "skipped", "reason": "duplicate_job"}
        
        # S3에서 Parquet 파일 읽기
        parquet_data = read_parquet_from_s3(bucket, key)
        
        if parquet_data.empty:
            logger.info(f"빈 파일: {key}")
            return {"status": "skipped", "reason": "empty_file"}
        
        # BigQuery 테이블 존재 여부 확인 및 생성
        ensure_bigquery_table(database_name, table_name, parquet_data)
        
        # BigQuery로 데이터 로드
        load_result = load_to_bigquery(
            database_name, table_name, parquet_data, job_id
        )
        
        return {
            "status": "success",
            "table": f"{database_name}.{table_name}",
            "rows": len(parquet_data),
            "job_id": job_id
        }
        
    except Exception as e:
        logger.error(f"파일 처리 실패 {key}: {str(e)}")
        raise e

def extract_table_info(s3_key):
    """S3 키에서 테이블 정보 추출"""
    
    # 예시: cdc/database1/table1/2023/03/15/20230315143022_table1.parquet.gz
    path_parts = s3_key.split('/')
    
    if len(path_parts) < 6:
        raise ValueError(f"잘못된 S3 키 형식: {s3_key}")
    
    database_name = path_parts[1]
    table_name = path_parts[2]
    filename = path_parts[-1]
    
    # 타임스탬프 추출 (yyyymmddhhmmss 형식)
    timestamp = filename.split('_')[0]
    
    return {
        'database_name': database_name,
        'table_name': table_name,
        'timestamp': timestamp,
        'filename': filename
    }

def check_duplicate_job(job_id):
    """BigQuery Job ID 중복 체크"""
    
    try:
        # 최근 24시간 내 Job 조회
        query = f"""
        SELECT job_id
        FROM `{BIGQUERY_PROJECT}.region-asia-northeast3.INFORMATION_SCHEMA.JOBS`
        WHERE job_id = '{job_id}'
        AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
        LIMIT 1
        """
        
        results = list(bq_client.query(query))
        return len(results) > 0
        
    except Exception as e:
        logger.warning(f"Job 중복 체크 실패: {str(e)}")
        return False

def read_parquet_from_s3(bucket, key):
    """S3에서 압축된 Parquet 파일 읽기"""
    
    try:
        # S3에서 파일 다운로드
        response = s3_client.get_object(Bucket=bucket, Key=key)
        
        # GZ 압축 해제
        if key.endswith('.gz'):
            compressed_data = response['Body'].read()
            decompressed_data = gzip.decompress(compressed_data)
            parquet_buffer = BytesIO(decompressed_data)
        else:
            parquet_buffer = BytesIO(response['Body'].read())
        
        # Parquet 파일을 DataFrame으로 읽기
        df = pd.read_parquet(parquet_buffer)
        
        # DMS CDC 메타데이터 처리
        df = process_cdc_metadata(df)
        
        return df
        
    except Exception as e:
        logger.error(f"S3 파일 읽기 실패 {key}: {str(e)}")
        raise e

def process_cdc_metadata(df):
    """DMS CDC 메타데이터 처리"""
    
    # CDC 오퍼레이션 컬럼 추가
    if 'Op' in df.columns:
        # I: Insert, U: Update, D: Delete
        df['_cdc_operation'] = df['Op']
        df['_cdc_timestamp'] = datetime.utcnow()
        df = df.drop('Op', axis=1)
    
    # MySQL 특수 타입 처리
    for column in df.columns:
        if df[column].dtype == 'object':
            # BIT 타입 처리
            if column.endswith('_bit'):
                df[column] = df[column].astype(str)
    
    return df

def ensure_bigquery_table(database_name, table_name, sample_data):
    """BigQuery 테이블 존재 여부 확인 및 생성"""
    
    dataset_id = f"{database_name}_{BIGQUERY_DATASET}"
    table_id = f"{BIGQUERY_PROJECT}.{dataset_id}.{table_name}"
    
    try:
        # 데이터셋 존재 여부 확인 및 생성
        try:
            dataset = bq_client.get_dataset(dataset_id)
        except:
            dataset = bigquery.Dataset(f"{BIGQUERY_PROJECT}.{dataset_id}")
            dataset.location = "asia-northeast3"
            dataset = bq_client.create_dataset(dataset)
            logger.info(f"데이터셋 생성: {dataset_id}")
        
        # 테이블 존재 여부 확인
        try:
            table = bq_client.get_table(table_id)
            logger.info(f"기존 테이블 사용: {table_id}")
            return table
        except:
            # 테이블이 없으면 샘플 데이터로 스키마 자동 생성
            logger.info(f"새 테이블 생성: {table_id}")
            return create_table_with_autodetect(table_id, sample_data)
            
    except Exception as e:
        logger.error(f"테이블 확인/생성 실패 {table_id}: {str(e)}")
        raise e

def create_table_with_autodetect(table_id, sample_data):
    """샘플 데이터로 BigQuery 테이블 자동 생성"""
    
    try:
        # 임시 파일로 샘플 데이터 업로드하여 스키마 자동 감지
        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        
        # 샘플 데이터를 Parquet 형태로 변환
        parquet_buffer = BytesIO()
        sample_data.head(1).to_parquet(parquet_buffer, index=False)
        parquet_buffer.seek(0)
        
        # 임시 Job으로 테이블 생성
        job = bq_client.load_table_from_file(
            parquet_buffer, table_id, job_config=job_config
        )
        job.result()  # 완료 대기
        
        table = bq_client.get_table(table_id)
        logger.info(f"자동 스키마 감지로 테이블 생성: {table_id}")
        
        return table
        
    except Exception as e:
        logger.error(f"자동 테이블 생성 실패 {table_id}: {str(e)}")
        raise e

def load_to_bigquery(database_name, table_name, df, job_id):
    """DataFrame을 BigQuery로 로드"""
    
    dataset_id = f"{database_name}_{BIGQUERY_DATASET}"
    table_id = f"{BIGQUERY_PROJECT}.{dataset_id}.{table_name}"
    
    try:
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            autodetect=False  # 기존 스키마 사용
        )
        
        # DataFrame을 Parquet으로 변환
        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer, index=False)
        parquet_buffer.seek(0)
        
        # BigQuery로 로드
        job = bq_client.load_table_from_file(
            parquet_buffer, table_id, 
            job_config=job_config,
            job_id=job_id
        )
        
        job.result()  # 완료 대기
        
        logger.info(f"데이터 로드 완료: {table_id}, 행 수: {len(df)}")
        
        return {
            "job_id": job_id,
            "rows_loaded": len(df),
            "table": table_id
        }
        
    except Conflict as e:
        if "already exists" in str(e):
            logger.info(f"중복 Job ID로 인한 건너뜀: {job_id}")
            return {"status": "skipped", "reason": "duplicate_job_id"}
        else:
            raise e
    except Exception as e:
        logger.error(f"BigQuery 로드 실패 {table_id}: {str(e)}")
        raise e

# 백필 시스템을 위한 Prefect Flow
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
from datetime import datetime, timedelta

@task
def backfill_single_table(database_name, table_name, start_date, end_date):
    """단일 테이블 백필 태스크"""
    
    logger.info(f"백필 시작: {database_name}.{table_name} ({start_date} ~ {end_date})")
    
    # S3에서 해당 기간의 CDC 파일 목록 조회
    s3_prefix = f"cdc/{database_name}/{table_name}/"
    
    current_date = start_date
    processed_files = 0
    
    while current_date <= end_date:
        date_prefix = current_date.strftime("%Y/%m/%d")
        full_prefix = f"{s3_prefix}{date_prefix}/"
        
        # S3에서 해당 날짜의 파일 목록 조회
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET,
            Prefix=full_prefix
        )
        
        for obj in response.get('Contents', []):
            key = obj['Key']
            
            try:
                # 파일 처리
                result = process_cdc_file(S3_BUCKET, key)
                if result['status'] == 'success':
                    processed_files += 1
                    logger.info(f"백필 처리 완료: {key}")
            except Exception as e:
                logger.error(f"백필 처리 실패 {key}: {str(e)}")
        
        current_date += timedelta(days=1)
    
    return {
        "database": database_name,
        "table": table_name,
        "processed_files": processed_files,
        "period": f"{start_date} ~ {end_date}"
    }

@flow(task_runner=ConcurrentTaskRunner())
def backfill_cdc_data(databases, tables, start_date, end_date):
    """CDC 데이터 백필 Flow"""
    
    logger.info(f"전체 백필 시작: {len(databases)} 데이터베이스, {len(tables)} 테이블")
    
    # 병렬로 각 테이블 백필 실행
    futures = []
    for database in databases:
        for table in tables:
            future = backfill_single_table.submit(database, table, start_date, end_date)
            futures.append(future)
    
    # 결과 수집
    results = [future.result() for future in futures]
    
    total_files = sum(result['processed_files'] for result in results)
    
    logger.info(f"전체 백필 완료: {total_files}개 파일 처리")
    
    return {
        "total_processed_files": total_files,
        "results": results
    }

# 모니터링 대시보드용 메트릭 수집
def publish_metrics(table_name, rows_processed, latency_seconds):
    """CloudWatch 메트릭 발행"""
    
    cloudwatch = boto3.client('cloudwatch')
    
    try:
        cloudwatch.put_metric_data(
            Namespace='CDC-Pipeline',
            MetricData=[
                {
                    'MetricName': 'RowsProcessed',
                    'Value': rows_processed,
                    'Unit': 'Count',
                    'Dimensions': [
                        {'Name': 'TableName', 'Value': table_name}
                    ]
                },
                {
                    'MetricName': 'ProcessingLatency',
                    'Value': latency_seconds,
                    'Unit': 'Seconds',
                    'Dimensions': [
                        {'Name': 'TableName', 'Value': table_name}
                    ]
                }
            ]
        )
    except Exception as e:
        logger.error(f"메트릭 발행 실패: {str(e)}")
```

### 2. 데이터 무결성 보장 메커니즘

**중복 데이터 방지:**
```python
class DuplicationHandler:
    """중복 데이터 처리 핸들러"""
    
    def __init__(self, bigquery_client):
        self.bq_client = bigquery_client
        self.processed_jobs = set()
    
    def generate_unique_job_id(self, timestamp, table_name):
        """고유 Job ID 생성"""
        return f"{timestamp}_{table_name}_parquet"
    
    def is_duplicate_job(self, job_id):
        """Job ID 중복 여부 확인"""
        
        if job_id in self.processed_jobs:
            return True
        
        # BigQuery Jobs 테이블에서 중복 확인
        query = f"""
        SELECT job_id
        FROM `{BIGQUERY_PROJECT}.region-asia-northeast3.INFORMATION_SCHEMA.JOBS`
        WHERE job_id = '{job_id}'
        AND state = 'DONE'
        AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
        """
        
        results = list(self.bq_client.query(query))
        
        if results:
            self.processed_jobs.add(job_id)
            return True
        
        return False
    
    def mark_job_processed(self, job_id):
        """처리된 Job 표시"""
        self.processed_jobs.add(job_id)
```

**데이터 검증 시스템:**
```python
class DataValidator:
    """데이터 정합성 검증"""
    
    def __init__(self, source_db_config, bigquery_client):
        self.source_db = pymysql.connect(**source_db_config)
        self.bq_client = bigquery_client
    
    def validate_row_count(self, table_name, date_range):
        """행 수 검증"""
        
        # 소스 DB 행 수 조회
        source_query = f"""
        SELECT COUNT(*) as source_count
        FROM {table_name}
        WHERE DATE(updated_at) BETWEEN '{date_range['start']}' AND '{date_range['end']}'
        """
        
        with self.source_db.cursor() as cursor:
            cursor.execute(source_query)
            source_count = cursor.fetchone()['source_count']
        
        # BigQuery 행 수 조회
        bq_query = f"""
        SELECT COUNT(*) as bq_count
        FROM `{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{table_name}`
        WHERE DATE(_cdc_timestamp) BETWEEN '{date_range['start']}' AND '{date_range['end']}'
        """
        
        bq_result = list(self.bq_client.query(bq_query))
        bq_count = bq_result[0]['bq_count']
        
        # 정합성 확인
        accuracy = (min(source_count, bq_count) / max(source_count, bq_count)) * 100
        
        return {
            'table': table_name,
            'source_count': source_count,
            'bigquery_count': bq_count,
            'accuracy_percent': accuracy,
            'is_valid': accuracy >= 99.9
        }
```

### 3. 자동화된 배포 및 테이블 관리

**테이블 매핑 관리 시스템:**
```yaml
# table_mappings.yaml
databases:
  casino_db1:
    tables:
      - name: user_actions
        schema_override:
          user_id: INTEGER
          action_type: STRING
          timestamp: TIMESTAMP
      - name: game_sessions
        auto_schema: true
      - name: transactions
        auto_schema: true
        
  casino_db2:
    tables:
      - name: player_stats
        auto_schema: true
      - name: game_results
        schema_override:
          game_id: STRING
          result_data: JSON

pipeline_config:
  batch_size: 1000
  retry_attempts: 3
  error_threshold: 0.1
  notification_channels:
    - slack_webhook: "https://hooks.slack.com/..."
    - email: "data-team@company.com"
```

**CI/CD 파이프라인 (GitHub Actions):**
```yaml
# .github/workflows/deploy-cdc-pipeline.yml
name: Deploy CDC Pipeline

on:
  push:
    paths:
      - 'table_mappings.yaml'
      - 'lambda/**'
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install boto3 google-cloud-bigquery pyyaml
      
      - name: Validate table mappings
        run: |
          python scripts/validate_mappings.py
      
      - name: Deploy Lambda functions
        run: |
          cd lambda
          zip -r cdc-processor.zip .
          aws lambda update-function-code \
            --function-name cdc-processor \
            --zip-file fileb://cdc-processor.zip
      
      - name: Update DMS endpoints
        run: |
          python scripts/update_dms_config.py
      
      - name: Run smoke tests
        run: |
          python scripts/smoke_test.py
```

## 성과 및 임팩트

### 성능 및 안정성
- **데이터 처리량**: 일 4,000만 건의 안정적인 실시간 처리
- **지연시간**: 평균 1-2분의 준실시간 데이터 동기화
- **데이터 정합성**: 99.9% 이상의 정확도 보장
- **가용성**: 99.5% 이상의 파이프라인 가용성 달성

### 비즈니스 임팩트
- **실시간 대시보드**: 경영진 대시보드의 실시간 데이터 제공
- **FDS 고도화**: 실시간 사기 탐지 시스템 구축으로 보안 강화
- **운영 효율성**: DW/BI 엔지니어의 독립적인 테이블 관리로 의존성 제거
- **비용 절감**: Parquet + GZ 압축으로 스토리지 비용 30% 절감

### 기술적 성과
- **멀티클라우드 아키텍처**: AWS와 GCP 간 안정적인 데이터 파이프라인 구축
- **자동화**: 테이블 스키마 자동 추론 및 배포 자동화 시스템 구축
- **장애 복구**: SQS 기반 재처리 메커니즘으로 데이터 유실 방지
- **모니터링**: 실시간 데이터 현황 모니터링 대시보드 제공

## 배운 점과 향후 개선 방향

### 주요 학습 내용

1. **멀티클라우드 데이터 파이프라인의 복잡성**
   - 클라우드 간 네트워크 지연 및 API 제한 고려사항
   - 각 플랫폼의 특성을 활용한 최적화 방법

2. **CDC 시스템의 설계 원칙**
   - At-least-once 보장과 중복 처리의 균형
   - 백프레셔 처리 및 버퍼링 전략의 중요성

3. **운영 자동화의 가치**
   - 테이블 매핑 자동화로 인한 생산성 향상
   - 모니터링과 알람의 사전 장애 예방 효과

### 향후 발전 방향

#### 단기 개선 사항 (3-6개월)
- **스키마 진화 대응**: BigQuery Schema Evolution 기능 활용
- **성능 최적화**: 배치 크기 동적 조정 및 병렬 처리 확대
- **모니터링 고도화**: 데이터 드리프트 감지 및 자동 알림

#### 중기 발전 계획 (6-12개월)
- **실시간 스트리밍**: Kafka 기반 완전 실시간 파이프라인 구축
- **데이터 레이크하우스**: Delta Lake/Iceberg 도입으로 ACID 보장
- **ML 파이프라인 통합**: 실시간 피처 스토어 구축

#### 장기 비전 (1-2년)
- **완전 자동화**: Infrastructure as Code와 GitOps 전면 도입
- **글로벌 확장**: 다중 리전 지원 및 글로벌 데이터 거버넌스
- **AI 기반 운영**: 이상 탐지 및 자동 복구 시스템 구축

### 아쉬웠던 점과 개선 방안

**기술적 아쉬움:**
- DMS 설정과 코드 배포의 분리된 관리
- 완전한 실시간성 미확보 (준실시간 1-2분 지연)

**개선 방안:**
- Infrastructure as Code로 DMS와 Lambda 통합 관리
- Apache Kafka 도입으로 완전 실시간 스트리밍 구축
- 컨테이너 기반 마이크로서비스 아키텍처 전환

이 프로젝트를 통해 멀티클라우드 환경에서의 대용량 실시간 데이터 파이프라인 구축 경험을 쌓았으며, 특히 AWS와 GCP 간의 안정적인 데이터 동기화 방법론을 확립할 수 있었습니다. 또한 운영 자동화의 중요성과 모니터링 시스템의 가치를 깊이 이해하게 되었습니다.