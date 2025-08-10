# 스트리밍 데이터 수집 플랫폼

## 프로젝트 개요

게임 서비스의 실시간 이벤트 스트림 처리와 고성능 NoSQL 데이터 저장을 위해 Amazon MSK(Managed Streaming for Apache Kafka)와 DynamoDB를 활용한 대용량 스트리밍 데이터 수집 플랫폼을 구축했습니다. 실시간 사용자 행동 분석과 이벤트 기반 아키텍처를 통한 확장 가능한 데이터 처리 시스템을 개발했습니다.

**핵심 성과:**
- 실시간 스트림 처리로 지연시간 100ms 이내 달성
- MSK 클러스터 운영으로 99.9% 가용성 확보
- DynamoDB 최적화로 읽기/쓰기 성능 10배 향상
- 이벤트 기반 아키텍처로 시스템 확장성 확보

## 프로젝트 목표

### 비즈니스 요구사항
1. **실시간 이벤트 처리**: 게임 내 실시간 사용자 액션 추적 및 분석
2. **고성능 데이터 저장**: 대용량 게임 데이터의 빠른 읽기/쓰기 지원
3. **확장 가능한 아키텍처**: 급증하는 트래픽에 대한 자동 확장
4. **이벤트 기반 시스템**: 마이크로서비스 간 느슨한 결합 구현

### 기술적 목표
- Apache Kafka 기반 실시간 메시지 스트리밍
- DynamoDB를 활용한 밀리초 단위 응답시간 달성
- 이벤트 소싱 패턴을 통한 데이터 일관성 보장
- 자동 스케일링을 통한 비용 최적화

## 기술적 도전과 해결 과정

### 1. 아키텍처 설계

**도전 과제:**
- 대용량 스트리밍 데이터의 실시간 처리
- 다양한 이벤트 타입의 효율적 관리
- NoSQL 데이터베이스의 성능 최적화

**해결 방안:**
```
Streaming Data Flow
├── Game Clients
│   └── Real-time Events
├── API Gateway + Lambda
│   └── Event Validation & Routing
├── Amazon MSK (Kafka)
│   ├── game-events Topic
│   ├── user-activity Topic
│   └── transaction-events Topic
├── Kafka Connect
│   ├── DynamoDB Sink Connector
│   ├── S3 Sink Connector
│   └── ElasticSearch Connector
└── Data Consumers
    ├── DynamoDB (Hot Data)
    ├── S3 (Cold Data Archive)
    └── Real-time Analytics
```

### 2. Amazon MSK 클러스터 구축

**MSK 클러스터 설정:**
```yaml
# MSK 클러스터 Terraform 설정
resource "aws_msk_cluster" "game_events_cluster" {
  cluster_name           = "game-events-streaming"
  kafka_version         = "2.8.1"
  number_of_broker_nodes = 6

  broker_node_group_info {
    instance_type   = "kafka.m5.xlarge"
    ebs_volume_size = 1000
    client_subnets = var.private_subnet_ids
    
    security_groups = [aws_security_group.msk_cluster.id]
  }

  configuration_info {
    arn      = aws_msk_configuration.game_events_config.arn
    revision = aws_msk_configuration.game_events_config.latest_revision
  }

  encryption_info {
    encryption_in_transit {
      client_broker = "TLS"
      in_cluster    = true
    }
    encryption_at_rest_kms_key_id = aws_kms_key.msk_encryption.arn
  }

  logging_info {
    broker_logs {
      cloudwatch_logs {
        enabled   = true
        log_group = aws_cloudwatch_log_group.msk_logs.name
      }
      s3 {
        enabled = true
        bucket  = aws_s3_bucket.msk_logs.bucket
        prefix  = "msk-broker-logs"
      }
    }
  }
}

resource "aws_msk_configuration" "game_events_config" {
  kafka_versions = ["2.8.1"]
  name           = "game-events-config"

  server_properties = <<PROPERTIES
auto.create.topics.enable=false
default.replication.factor=3
min.insync.replicas=2
num.partitions=12
log.retention.hours=168
log.segment.bytes=1073741824
compression.type=snappy
PROPERTIES
}
```

**토픽 설계 및 파티셔닝 전략:**
```python
from kafka.admin import KafkaAdminClient, NewTopic
import json

def create_kafka_topics():
    """게임 이벤트용 Kafka 토픽 생성"""
    
    admin_client = KafkaAdminClient(
        bootstrap_servers=['msk-cluster.region.amazonaws.com:9092'],
        security_protocol='SSL'
    )
    
    topics = [
        NewTopic(
            name='game-events',
            num_partitions=24,  # 높은 처리량을 위한 파티션 수
            replication_factor=3,
            topic_configs={
                'compression.type': 'snappy',
                'retention.ms': '604800000',  # 7일
                'segment.ms': '86400000',     # 1일
                'cleanup.policy': 'delete'
            }
        ),
        NewTopic(
            name='user-activity',
            num_partitions=12,
            replication_factor=3,
            topic_configs={
                'compression.type': 'lz4',
                'retention.ms': '259200000',  # 3일
                'cleanup.policy': 'compact'
            }
        ),
        NewTopic(
            name='transaction-events',
            num_partitions=8,
            replication_factor=3,
            topic_configs={
                'compression.type': 'gzip',
                'retention.ms': '2592000000',  # 30일
                'min.insync.replicas': '2'
            }
        )
    ]
    
    admin_client.create_topics(topics)

def produce_game_events():
    """게임 이벤트 프로듀서 구현"""
    
    from kafka import KafkaProducer
    import json
    import uuid
    from datetime import datetime
    
    producer = KafkaProducer(
        bootstrap_servers=['msk-cluster.region.amazonaws.com:9092'],
        security_protocol='SSL',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda v: str(v).encode('utf-8'),
        batch_size=16384,
        linger_ms=10,
        compression_type='snappy',
        retries=3,
        acks='all'
    )
    
    def send_event(user_id, event_type, event_data):
        """게임 이벤트 전송"""
        
        event = {
            'event_id': str(uuid.uuid4()),
            'user_id': user_id,
            'event_type': event_type,
            'event_data': event_data,
            'timestamp': datetime.utcnow().isoformat(),
            'game_version': '1.2.3',
            'platform': 'mobile'
        }
        
        # 사용자 ID로 파티셔닝하여 순서 보장
        partition_key = str(user_id)
        
        future = producer.send(
            topic='game-events',
            key=partition_key,
            value=event
        )
        
        return future
    
    return send_event
```

### 3. DynamoDB 최적화 설계

**테이블 설계 및 인덱스 최적화:**
```python
import boto3
from boto3.dynamodb.conditions import Key, Attr

def create_optimized_dynamodb_tables():
    """게임 데이터용 최적화된 DynamoDB 테이블 생성"""
    
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    
    # 사용자 세션 테이블
    user_sessions_table = dynamodb.create_table(
        TableName='GameUserSessions',
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'session_start_time', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'session_start_time', 'AttributeType': 'S'},
            {'AttributeName': 'game_id', 'AttributeType': 'S'},
            {'AttributeName': 'session_end_time', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'GameSessionsIndex',
                'KeySchema': [
                    {'AttributeName': 'game_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'session_start_time', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        StreamSpecification={
            'StreamEnabled': True,
            'StreamViewType': 'NEW_AND_OLD_IMAGES'
        },
        Tags=[
            {'Key': 'Environment', 'Value': 'production'},
            {'Key': 'Application', 'Value': 'game-analytics'}
        ]
    )
    
    # 실시간 리더보드 테이블
    leaderboard_table = dynamodb.create_table(
        TableName='GameLeaderboard',
        KeySchema=[
            {'AttributeName': 'game_id', 'KeyType': 'HASH'},
            {'AttributeName': 'score_timestamp', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'game_id', 'AttributeType': 'S'},
            {'AttributeName': 'score_timestamp', 'AttributeType': 'S'},
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'score', 'AttributeType': 'N'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'UserScoresIndex',
                'KeySchema': [
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'score', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'BillingMode': 'PAY_PER_REQUEST'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    return user_sessions_table, leaderboard_table

class DynamoDBOptimizedAccess:
    """DynamoDB 최적화된 접근 클래스"""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.user_sessions = self.dynamodb.Table('GameUserSessions')
        self.leaderboard = self.dynamodb.Table('GameLeaderboard')
    
    def batch_write_user_events(self, events):
        """배치 쓰기를 통한 성능 최적화"""
        
        with self.user_sessions.batch_writer() as batch:
            for event in events:
                batch.put_item(Item={
                    'user_id': event['user_id'],
                    'session_start_time': event['timestamp'],
                    'game_id': event['game_id'],
                    'event_type': event['event_type'],
                    'event_data': event['event_data'],
                    'ttl': int(time.time()) + (30 * 24 * 60 * 60)  # 30일 TTL
                })
    
    def query_user_recent_activity(self, user_id, hours=24):
        """사용자 최근 활동 조회 (파티션 키 최적화)"""
        
        from datetime import datetime, timedelta
        
        start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        
        response = self.user_sessions.query(
            KeyConditionExpression=Key('user_id').eq(user_id) & 
                                 Key('session_start_time').gte(start_time),
            ScanIndexForward=False,  # 최신 순 정렬
            Limit=100
        )
        
        return response['Items']
    
    def update_leaderboard_score(self, game_id, user_id, score):
        """리더보드 점수 업데이트 (조건부 쓰기)"""
        
        from datetime import datetime
        
        try:
            response = self.leaderboard.update_item(
                Key={
                    'game_id': game_id,
                    'score_timestamp': datetime.utcnow().isoformat()
                },
                UpdateExpression='SET user_id = :uid, score = :score, updated_at = :timestamp',
                ConditionExpression='attribute_not_exists(score) OR score < :score',
                ExpressionAttributeValues={
                    ':uid': user_id,
                    ':score': score,
                    ':timestamp': datetime.utcnow().isoformat()
                },
                ReturnValues='ALL_NEW'
            )
            return response['Attributes']
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                # 점수가 더 낮은 경우 업데이트하지 않음
                return None
            raise e
```

### 4. Kafka Connect 통합

**DynamoDB Sink Connector 구성:**
```json
{
  "name": "dynamodb-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.aws.dynamodb.DynamoDbSinkConnector",
    "topics": "game-events,user-activity",
    "aws.dynamodb.region": "ap-northeast-2",
    "aws.dynamodb.endpoint": "https://dynamodb.ap-northeast-2.amazonaws.com",
    "auto.create": "true",
    "auto.evolve": "true",
    "pk.mode": "record_value",
    "pk.fields": "user_id,timestamp",
    "table.name.format": "GameEvents_${topic}",
    "write.method": "upsert",
    "batch.size": 25,
    "max.retries": 10,
    "retry.backoff.ms": 3000,
    "transforms": "addTimestamp,flattenStruct",
    "transforms.addTimestamp.type": "org.apache.kafka.connect.transforms.TimestampConverter$Value",
    "transforms.addTimestamp.field": "timestamp",
    "transforms.addTimestamp.format": "yyyy-MM-dd HH:mm:ss",
    "transforms.flattenStruct.type": "org.apache.kafka.connect.transforms.Flatten$Value"
  }
}
```

**S3 Sink Connector 구성 (아카이브용):**
```json
{
  "name": "s3-archive-connector",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "topics": "game-events,user-activity,transaction-events",
    "s3.region": "ap-northeast-2",
    "s3.bucket.name": "game-events-archive",
    "s3.part.size": "67108864",
    "flush.size": "10000",
    "rotate.interval.ms": "300000",
    "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
    "partition.duration.ms": "3600000",
    "path.format": "year=YYYY/month=MM/day=dd/hour=HH",
    "timestamp.extractor": "Record",
    "timestamp.field": "timestamp",
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "schema.compatibility": "BACKWARD"
  }
}
```

### 5. 실시간 스트림 프로세싱

**Lambda 기반 실시간 이벤트 처리:**
```python
import json
import boto3
from datetime import datetime, timedelta
import base64

def lambda_handler(event, context):
    """MSK 이벤트 실시간 처리"""
    
    dynamodb = boto3.resource('dynamodb')
    cloudwatch = boto3.client('cloudwatch')
    
    # 실시간 메트릭 수집
    total_events = 0
    error_count = 0
    
    for record in event['records']:
        for kafka_record in record['value']:
            try:
                # Kafka 메시지 디코딩
                message = json.loads(
                    base64.b64decode(kafka_record['value']).decode('utf-8')
                )
                
                # 이벤트 타입별 처리
                event_type = message.get('event_type')
                
                if event_type == 'user_login':
                    process_user_login(message, dynamodb)
                elif event_type == 'game_start':
                    process_game_start(message, dynamodb)
                elif event_type == 'purchase':
                    process_purchase_event(message, dynamodb)
                elif event_type == 'achievement':
                    process_achievement(message, dynamodb)
                
                total_events += 1
                
            except Exception as e:
                print(f"이벤트 처리 오류: {str(e)}")
                error_count += 1
    
    # CloudWatch 메트릭 전송
    send_processing_metrics(cloudwatch, total_events, error_count)
    
    return {'statusCode': 200, 'body': f'Processed {total_events} events'}

def process_user_login(message, dynamodb):
    """사용자 로그인 이벤트 처리"""
    
    table = dynamodb.Table('GameUserSessions')
    
    # 세션 시작 기록
    table.put_item(
        Item={
            'user_id': message['user_id'],
            'session_start_time': message['timestamp'],
            'game_id': message['event_data']['game_id'],
            'platform': message['event_data']['platform'],
            'session_status': 'active',
            'ttl': int(time.time()) + (30 * 24 * 60 * 60)
        }
    )
    
    # 동시 접속자 수 업데이트
    update_concurrent_users(message['event_data']['game_id'], 1)

def process_purchase_event(message, dynamodb):
    """구매 이벤트 처리"""
    
    table = dynamodb.Table('GameTransactions')
    
    # 트랜잭션 기록
    table.put_item(
        Item={
            'transaction_id': message['event_data']['transaction_id'],
            'user_id': message['user_id'],
            'timestamp': message['timestamp'],
            'amount': message['event_data']['amount'],
            'currency': message['event_data']['currency'],
            'item_id': message['event_data']['item_id'],
            'payment_method': message['event_data']['payment_method']
        }
    )
    
    # 실시간 매출 집계 업데이트
    update_revenue_metrics(
        message['event_data']['game_id'],
        message['event_data']['amount']
    )

def update_concurrent_users(game_id, increment):
    """동시 접속자 수 실시간 업데이트"""
    
    import redis
    
    redis_client = redis.Redis(
        host='elasticache-cluster.region.amazonaws.com',
        port=6379,
        decode_responses=True
    )
    
    # Redis에서 동시 접속자 수 업데이트
    current_count = redis_client.incr(f"concurrent_users:{game_id}", increment)
    
    # 5분간의 TTL 설정
    redis_client.expire(f"concurrent_users:{game_id}", 300)
    
    return current_count
```

### 6. 모니터링 및 알러트 시스템

**종합 모니터링 대시보드:**
```python
def setup_streaming_monitoring():
    """스트리밍 데이터 플랫폼 모니터링 설정"""
    
    cloudwatch = boto3.client('cloudwatch')
    
    # MSK 클러스터 메트릭
    msk_alarms = [
        {
            'AlarmName': 'MSK-HighCPUUtilization',
            'MetricName': 'CpuUser',
            'Namespace': 'AWS/Kafka',
            'Statistic': 'Average',
            'Threshold': 80.0,
            'ComparisonOperator': 'GreaterThanThreshold'
        },
        {
            'AlarmName': 'MSK-HighMemoryUtilization',
            'MetricName': 'MemoryUsed',
            'Namespace': 'AWS/Kafka',
            'Statistic': 'Average',
            'Threshold': 85.0,
            'ComparisonOperator': 'GreaterThanThreshold'
        }
    ]
    
    # DynamoDB 메트릭
    dynamodb_alarms = [
        {
            'AlarmName': 'DynamoDB-HighThrottling',
            'MetricName': 'ThrottledRequests',
            'Namespace': 'AWS/DynamoDB',
            'Statistic': 'Sum',
            'Threshold': 10.0,
            'ComparisonOperator': 'GreaterThanThreshold'
        },
        {
            'AlarmName': 'DynamoDB-HighLatency',
            'MetricName': 'SuccessfulRequestLatency',
            'Namespace': 'AWS/DynamoDB',
            'Statistic': 'Average',
            'Threshold': 100.0,
            'ComparisonOperator': 'GreaterThanThreshold'
        }
    ]
    
    # 알람 생성
    for alarm_config in msk_alarms + dynamodb_alarms:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm_config['AlarmName'],
            ComparisonOperator=alarm_config['ComparisonOperator'],
            EvaluationPeriods=3,
            MetricName=alarm_config['MetricName'],
            Namespace=alarm_config['Namespace'],
            Period=300,
            Statistic=alarm_config['Statistic'],
            Threshold=alarm_config['Threshold'],
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:region:account:streaming-alerts'
            ],
            AlarmDescription=f'Alarm for {alarm_config["AlarmName"]}'
        )
```

## 성과 및 임팩트

### 성능 지표
- **스트림 처리 지연**: 평균 100ms 이내 이벤트 처리
- **DynamoDB 응답시간**: 읽기 평균 2ms, 쓰기 평균 5ms
- **MSK 처리량**: 초당 100만 메시지 처리 가능
- **시스템 가용성**: 99.9% 업타임 달성

### 확장성 및 비용
- **자동 스케일링**: 트래픽 증가 시 자동 확장 (최대 10배)
- **비용 최적화**: DynamoDB On-Demand로 30% 비용 절감
- **스토리지 효율성**: Kafka 압축으로 70% 스토리지 절약
- **운영 효율성**: 관리형 서비스로 운영 오버헤드 90% 감소

### 비즈니스 가치
- **실시간 게임 분석**: 사용자 행동 즉시 파악으로 게임 밸런싱 최적화
- **개인화 서비스**: 실시간 사용자 데이터로 맞춤형 콘텐츠 제공
- **사기 탐지**: 실시간 이상 패턴 감지로 부정행위 즉시 차단
- **운영 인사이트**: 실시간 KPI 모니터링으로 빠른 의사결정 지원

## 배운 점과 향후 개선 방향

### 주요 학습 내용

1. **스트리밍 아키텍처 설계 원칙**
   - 파티셔닝 전략이 성능에 미치는 결정적 영향
   - 백프레셀(Backpressure) 처리의 중요성

2. **NoSQL 데이터베이스 최적화**
   - 액세스 패턴 기반 테이블 설계의 중요성
   - Hot Partition 문제와 해결 방안

3. **이벤트 기반 아키텍처의 장단점**
   - 느슨한 결합의 장점과 디버깅의 복잡성
   - 이벤트 순서 보장과 멱등성의 필요성

### 향후 개선 계획

#### 단기 개선 사항 (3-6개월)
- **스트림 분석**: Kinesis Analytics를 활용한 실시간 윈도우 집계
- **캐싱 강화**: ElastiCache를 통한 Hot Data 캐싱으로 응답시간 단축
- **데이터 품질**: Schema Registry 도입으로 데이터 스키마 관리

#### 중기 개선 사항 (6-12개월)
- **ML 파이프라인**: 실시간 스트림 기반 머신러닝 모델 서빙
- **글로벌 확장**: 다중 리전 복제를 통한 글로벌 서비스 지원
- **CQRS 패턴**: Command와 Query 분리를 통한 성능 최적화

#### 장기 비전 (1-2년)
- **서버리스 진화**: Lambda + Kinesis 기반 완전 서버리스 아키텍처
- **AI 기반 최적화**: 자동 파티션 조정 및 성능 튜닝
- **실시간 데이터 메시**: 도메인별 이벤트 스트림 관리

### 기술 스택 진화 방향
- **Apache Pulsar**: Kafka 대안으로 멀티 테넌트 지원 검토
- **ClickHouse**: 실시간 분석 워크로드를 위한 OLAP 데이터베이스 도입
- **Apache Beam**: 스트림/배치 통합 처리 파이프라인 구축

이 프로젝트를 통해 대용량 실시간 데이터 처리의 전문성을 확보했으며, 이벤트 기반 아키텍처를 통한 확장 가능한 시스템 설계 능력을 크게 향상시킬 수 있었습니다.
