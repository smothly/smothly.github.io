# Trino on ECS 기반 DataLake 플랫폼

## 프로젝트 개요

다양한 데이터 소스에 분산되어 있는 데이터를 통합적으로 조회하고 분석하기 위해 Trino(구 PrestoSQL)를 AWS ECS에 배포한 DataLake 플랫폼을 구축했습니다. Apache Iceberg 테이블 포맷을 활용하여 원본 데이터 확인과 Ad-hoc 쿼리를 효율적으로 지원하는 시스템을 개발했습니다.

**핵심 성과:**
- ECS 기반 Auto Scaling으로 탄력적 자원 관리
- Apache Iceberg 테이블 포맷으로 스키마 진화 지원
- 15개 이상 데이터 소스 통합 쿼리 지원
- S3 Lifecycle 정책으로 비용 최적화

## 프로젝트 목표

### 비즈니스 요구사항
1. **통합 데이터 접근**: 분산된 데이터 소스를 단일 SQL 인터페이스로 통합
2. **Ad-hoc 분석 지원**: 데이터 분석가의 자유로운 탐색적 분석 지원
3. **원본 데이터 검증**: ETL 과정에서 발생하는 데이터 변화 추적 및 검증
4. **비용 효율성**: 필요 시에만 리소스를 사용하는 탄력적 플랫폼

### 기술적 목표
- Federated Query를 통한 다양한 데이터 소스 통합
- Iceberg 테이블 포맷을 활용한 ACID 트랜잭션 지원
- ECS 기반 컨테이너 오케스트레이션으로 고가용성 확보
- S3 Lifecycle 정책을 통한 자동 비용 최적화

## 기술적 도전과 해결 과정

### 1. 아키텍처 설계

**도전 과제:**
- 다양한 데이터 소스 간 성능 차이
- 대용량 데이터 처리 시 메모리 관리
- 동적 스케일링과 고가용성 보장

**해결 방안:**
```
ECS Cluster Architecture
├── Trino Coordinator (ECS Service)
│   ├── Auto Scaling Group (1-3 tasks)
│   ├── Application Load Balancer
│   └── Service Discovery
├── Trino Workers (ECS Service)
│   ├── Auto Scaling Group (2-10 tasks)
│   ├── Memory-optimized instances (r5.xlarge)
│   └── Spot Instance 활용
└── Data Sources Integration
    ├── S3 (Iceberg Tables)
    ├── Redshift Connector
    ├── BigQuery Connector
    ├── MySQL Connector
    └── ElasticSearch Connector
```

### 2. ECS 기반 Trino 클러스터 구축

**ECS Task Definition 최적화:**
```json
{
  "family": "trino-coordinator",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["EC2"],
  "cpu": "2048",
  "memory": "8192",
  "taskRoleArn": "arn:aws:iam::account:role/TrinoTaskRole",
  "containerDefinitions": [
    {
      "name": "trino-coordinator",
      "image": "trinodb/trino:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "TRINO_ENVIRONMENT",
          "value": "production"
        }
      ],
      "mountPoints": [
        {
          "sourceVolume": "trino-config",
          "containerPath": "/etc/trino"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/trino-coordinator",
          "awslogs-region": "ap-northeast-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "volumes": [
    {
      "name": "trino-config",
      "efsVolumeConfiguration": {
        "fileSystemId": "fs-xxxxxxxxx",
        "transitEncryption": "ENABLED"
      }
    }
  ]
}
```

**Auto Scaling 정책 구현:**
```python
import boto3

def setup_trino_autoscaling():
    """Trino 워커 노드의 오토스케일링 설정"""
    
    client = boto3.client('application-autoscaling')
    
    # 스케일링 타겟 등록
    client.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId='service/trino-cluster/trino-worker',
        ScalableDimension='ecs:service:DesiredCount',
        MinCapacity=2,
        MaxCapacity=10,
        RoleARN='arn:aws:iam::account:role/ECSAutoScalingRole'
    )
    
    # CPU 기반 스케일링 정책
    client.put_scaling_policy(
        PolicyName='trino-worker-cpu-scaling',
        ServiceNamespace='ecs',
        ResourceId='service/trino-cluster/trino-worker',
        ScalableDimension='ecs:service:DesiredCount',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
            },
            'ScaleOutCooldown': 300,
            'ScaleInCooldown': 300
        }
    )
    
    # 메모리 기반 스케일링 정책
    client.put_scaling_policy(
        PolicyName='trino-worker-memory-scaling',
        ServiceNamespace='ecs',
        ResourceId='service/trino-cluster/trino-worker',
        ScalableDimension='ecs:service:DesiredCount',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 80.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ECSServiceAverageMemoryUtilization'
            }
        }
    )
```

### 3. Apache Iceberg 테이블 포맷 구현

**Iceberg 카탈로그 설정:**
```properties
# catalog.properties
connector.name=iceberg
iceberg.catalog.type=glue
iceberg.glue.region=ap-northeast-2
iceberg.s3.region=ap-northeast-2
iceberg.table-statistics-enabled=true
iceberg.extended-statistics.enabled=true
```

**Iceberg 테이블 생성 및 관리:**
```sql
-- Iceberg 테이블 생성
CREATE TABLE iceberg.game_data.user_events (
    user_id BIGINT,
    event_time TIMESTAMP(6) WITH TIME ZONE,
    event_type VARCHAR,
    game_id VARCHAR,
    session_id VARCHAR,
    properties MAP(VARCHAR, VARCHAR),
    created_date DATE
)
WITH (
    format = 'PARQUET',
    partitioning = ARRAY['created_date'],
    location = 's3://data-lake-bucket/iceberg/user_events/',
    table_type = 'ICEBERG'
);

-- 파티션 기반 데이터 삽입
INSERT INTO iceberg.game_data.user_events
SELECT 
    user_id,
    event_time,
    event_type,
    game_id,
    session_id,
    properties,
    DATE(event_time) as created_date
FROM s3_source.raw_data.events
WHERE DATE(event_time) = DATE '2024-01-01';

-- 스키마 진화 예시
ALTER TABLE iceberg.game_data.user_events 
ADD COLUMN device_info MAP(VARCHAR, VARCHAR);

-- 타임 트래블 쿼리
SELECT * FROM iceberg.game_data.user_events 
FOR TIMESTAMP AS OF TIMESTAMP '2024-01-01 12:00:00';
```

### 4. 다양한 데이터 소스 연동

**커넥터 설정 및 최적화:**
```properties
# redshift.properties
connector.name=redshift
connection-url=jdbc:redshift://cluster.region.redshift.amazonaws.com:5439/dev
connection-user=${ENV:REDSHIFT_USER}
connection-password=${ENV:REDSHIFT_PASSWORD}
redshift.table-description-cache-ttl=1h
redshift.max-connections=50

# bigquery.properties  
connector.name=bigquery
bigquery.project-id=your-gcp-project
bigquery.parent-project-id=your-gcp-project
bigquery.credentials-file=/etc/trino/bigquery-credentials.json
bigquery.parallel-read-max-partitions=100

# mysql.properties
connector.name=mysql
connection-url=jdbc:mysql://mysql-server:3306
connection-user=${ENV:MYSQL_USER}
connection-password=${ENV:MYSQL_PASSWORD}
mysql.connection-timeout=10s
mysql.join-pushdown.enabled=true
```

**Cross-connector 쿼리 최적화:**
```sql
-- 다중 데이터 소스 조인 쿼리
WITH redshift_aggregates AS (
    SELECT 
        user_id,
        SUM(revenue) as total_revenue,
        COUNT(*) as transaction_count
    FROM redshift.analytics.user_transactions
    WHERE date_created >= DATE '2024-01-01'
    GROUP BY user_id
),
bigquery_events AS (
    SELECT 
        user_id,
        COUNT(*) as event_count,
        MAX(event_time) as last_activity
    FROM bigquery.game_analytics.user_events
    WHERE DATE(event_time) >= DATE '2024-01-01'
    GROUP BY user_id
)
SELECT 
    r.user_id,
    r.total_revenue,
    r.transaction_count,
    b.event_count,
    b.last_activity
FROM redshift_aggregates r
LEFT JOIN bigquery_events b ON r.user_id = b.user_id
WHERE r.total_revenue > 100;
```

### 5. S3 Lifecycle 정책 구현

**자동 비용 최적화:**
```python
import boto3
import json

def setup_s3_lifecycle_policies():
    """S3 데이터의 자동 비용 최적화 정책 설정"""
    
    s3_client = boto3.client('s3')
    
    lifecycle_config = {
        'Rules': [
            {
                'ID': 'IcebergDataLifecycle',
                'Status': 'Enabled',
                'Filter': {
                    'Prefix': 'iceberg/'
                },
                'Transitions': [
                    {
                        'Days': 30,
                        'StorageClass': 'STANDARD_IA'
                    },
                    {
                        'Days': 90,
                        'StorageClass': 'GLACIER'
                    },
                    {
                        'Days': 365,
                        'StorageClass': 'DEEP_ARCHIVE'
                    }
                ]
            },
            {
                'ID': 'IcebergMetadataLifecycle',
                'Status': 'Enabled',
                'Filter': {
                    'Prefix': 'iceberg/metadata/'
                },
                'Transitions': [
                    {
                        'Days': 90,
                        'StorageClass': 'STANDARD_IA'
                    }
                ]
            },
            {
                'ID': 'QueryResultsCleanup',
                'Status': 'Enabled',
                'Filter': {
                    'Prefix': 'query-results/'
                },
                'Expiration': {
                    'Days': 7
                }
            }
        ]
    }
    
    s3_client.put_bucket_lifecycle_configuration(
        Bucket='data-lake-bucket',
        LifecycleConfiguration=lifecycle_config
    )

def iceberg_table_maintenance():
    """Iceberg 테이블 메인터넌스 작업"""
    import trino
    
    conn = trino.dbapi.connect(
        host='trino-coordinator.internal',
        port=8080,
        user='admin',
        catalog='iceberg',
        schema='game_data'
    )
    
    cursor = conn.cursor()
    
    # 오래된 스냅샷 정리
    cursor.execute("""
        CALL iceberg.system.expire_snapshots(
            table => 'game_data.user_events',
            older_than => TIMESTAMP '2024-01-01 00:00:00',
            retain_last => 5
        )
    """)
    
    # 작은 파일 통합
    cursor.execute("""
        CALL iceberg.system.rewrite_data_files(
            table => 'game_data.user_events',
            strategy => 'sort',
            sort_order => 'event_time DESC'
        )
    """)
    
    # 테이블 통계 업데이트
    cursor.execute("ANALYZE TABLE game_data.user_events")
    
    conn.close()
```

### 6. 모니터링 및 성능 최적화

**CloudWatch 메트릭 수집:**
```python
def collect_trino_metrics():
    """Trino 클러스터의 성능 메트릭 수집"""
    
    import requests
    import boto3
    
    cloudwatch = boto3.client('cloudwatch')
    
    # Trino 코디네이터에서 메트릭 수집
    response = requests.get('http://trino-coordinator:8080/v1/node')
    nodes = response.json()
    
    active_workers = len([n for n in nodes if n['state'] == 'active'])
    
    # Trino 쿼리 통계 수집
    stats_response = requests.get('http://trino-coordinator:8080/v1/query')
    queries = stats_response.json()
    
    running_queries = len([q for q in queries if q['state'] == 'RUNNING'])
    
    # CloudWatch에 메트릭 전송
    cloudwatch.put_metric_data(
        Namespace='Trino/Cluster',
        MetricData=[
            {
                'MetricName': 'ActiveWorkers',
                'Value': active_workers,
                'Unit': 'Count'
            },
            {
                'MetricName': 'RunningQueries',
                'Value': running_queries,
                'Unit': 'Count'
            }
        ]
    )

def query_optimization_recommendations():
    """쿼리 최적화 권장사항 분석"""
    
    # 느린 쿼리 탐지
    slow_queries = """
        SELECT 
            query_id,
            query,
            state,
            elapsed_time_millis,
            total_bytes_processed,
            total_rows_processed
        FROM system.runtime.queries
        WHERE elapsed_time_millis > 60000
        AND state = 'FINISHED'
        ORDER BY elapsed_time_millis DESC
        LIMIT 10
    """
    
    # 리소스 사용량 분석
    resource_usage = """
        SELECT 
            query_id,
            peak_user_memory_bytes / 1024 / 1024 / 1024 as peak_memory_gb,
            cumulative_memory_bytes / 1024 / 1024 / 1024 as cumulative_memory_gb,
            wall_time_millis / 1000 as wall_time_seconds
        FROM system.runtime.queries
        WHERE peak_user_memory_bytes > 8589934592  -- 8GB 이상
        ORDER BY peak_user_memory_bytes DESC
    """
```

## 성과 및 임팩트

### 성능 지표
- **쿼리 응답시간**: Ad-hoc 쿼리 평균 30초 이내 처리
- **동시 처리**: 최대 50개 동시 쿼리 처리 가능
- **데이터 처리량**: 시간당 10TB 데이터 스캔 가능
- **가용성**: 99.9% 업타임 달성

### 비용 효율성
- **인프라 비용**: Spot Instance 활용으로 40% 비용 절감
- **스토리지 비용**: S3 Lifecycle으로 30% 스토리지 비용 절감
- **운영 비용**: 자동 스케일링으로 유휴 리소스 90% 감소

### 비즈니스 가치
- **분석 민첩성**: 데이터 분석가의 셀프 서비스 분석 환경 제공
- **데이터 검증**: ETL 파이프라인의 데이터 정합성 검증 시간 80% 단축
- **통합 분석**: 15개 이상 데이터 소스의 통합 분석 환경 구축
- **개발 생산성**: SQL 기반 통합 인터페이스로 개발 효율성 50% 향상

## 배운 점과 향후 개선 방향

### 주요 학습 내용

1. **Federated Query의 성능 최적화**
   - 데이터 소스 간 조인 시 네트워크 비용 고려 필요
   - 적절한 필터 푸시다운과 프로젝션 최적화의 중요성

2. **Iceberg 테이블 포맷의 장점**
   - ACID 트랜잭션과 스키마 진화의 강력함
   - 타임 트래블 기능을 통한 데이터 버전 관리

3. **ECS 기반 컨테이너 오케스트레이션**
   - 동적 스케일링과 고가용성의 균형점
   - Spot Instance 활용 시 상태 관리의 중요성

### 향후 개선 계획

#### 단기 개선 사항 (3-6개월)
- **쿼리 캐싱**: Redis 기반 결과 캐싱으로 반복 쿼리 성능 향상
- **보안 강화**: Ranger 통합을 통한 세밀한 권한 관리
- **메타데이터 관리**: Apache Atlas를 통한 데이터 lineage 추적

#### 중기 개선 사항 (6-12개월)
- **실시간 스트리밍**: Kafka 커넥터를 통한 실시간 데이터 조회
- **ML 통합**: SparkML과의 연동을 통한 ML 파이프라인 구축
- **글로벌 확장**: 다중 리전 배포를 통한 글로벌 데이터 레이크

#### 장기 비전 (1-2년)
- **완전 서버리스**: Fargate 기반 완전 관리형 클러스터
- **AI 기반 최적화**: 자동 쿼리 최적화 및 인덱스 추천
- **데이터 메시 통합**: 도메인별 독립적인 데이터 제품 관리

### 기술 스택 진화 방향
- **Delta Lake**: Apache Iceberg 대안으로 Delta Lake 검토
- **Kubernetes**: ECS에서 EKS로의 마이그레이션 고려
- **Starburst**: 엔터프라이즈 Trino 솔루션 도입 검토

이 프로젝트를 통해 현대적인 DataLake 아키텍처의 구축과 운영 노하우를 확보했으며, 조직의 셀프 서비스 분석 역량을 크게 향상시킬 수 있었습니다.
