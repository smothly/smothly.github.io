# AWS RDS Aurora → Google Bigquery Multi-Cloud Near-Realtime(CDC) Data Pipeline

## 목표

- PnE도입으로 인해 글로벌 카지노 게임 3종의 일배치를 **준실시간 배치**로 전환
  - DB Cluster 6개
  - 테이블 70여개
  - 하루 데이터 4000만 row
- RDB에 저장된 데이터를 실시간으로 옮겨야 하는 미션

---

## 아키텍처

![architecture](/static/images/projects/aws-bigquery-pipeline/architecture.png)

- RDS(MySQL) → DMS(CDC) → S3 → SQS → Lambda → Bigquery

---

## 이슈 & 해결

### 데이터 누락

**이슈**
- 빅쿼리 API - 빅쿼리 로드가 API 기반이다 보니 간헐적으로 로드 오류가 발생
- 휴먼 에러 - 테이블 명이나 코드의 문법오류가 발생시 로드 실패

**해결**
- S3와 Lambda사이에 **SQS큐를 추가**함으로써 실패한 이벤트들은 다시 큐로 돌아가도록 함

### 데이터 중복

**이슈**
- S3 event가 at least once여서 중복이벤트가 발생함
- 빅쿼리에 append형태로 적재를 하는데 실패 시 재처리

**해결**
- 빅쿼리의 **Job id를 unique id처럼 활용하여 중복된 job일 경우 패스**하도록 함
  - ex) 로드할 때 yyyymmddhhmmss_{테이블}.parquet을 Job id로 올리고 중복된 Job인지 체크

### 테이블 관리

**이슈**
- 테이블의 변동이 잦음
- 테이블 매핑 코드를 매번 수동으로 배포했어야함

**해결**
- 테이블 매핑 파일을 따로 두어 관리
- **CD(자동 배포)를 구축하여 테이블 파일 수정하면 자동으로 배포**되도록 변경

### 자동 스키마 추론

**이슈**
- Bit, Boolean등 MySQL의 특정타입들을 지원하지 않아 인코딩이 깨짐
- 테이블 추가시 매번 빅쿼리에서 테이블 정의했어야 함

**해결**
- 1차적으로 **DMS에게 공통변환을 맡겨 mysql라이브러리의 이슈들은 해결**
- 2차적으로는 **parquet파일로 변환 및 빅쿼리의 autodetect 스키마 추론 기능을 활용**하여 테이블을 자동으로 생성함
  - parquet + gz압축으로 비용절감 효과는 덤!

---

## 성과

- 평균 Latency 1~2분정도의 **준실시간 배치로의 안정적인 파이프라인** 구축
  - 실시간 대시보드, 실시간 FDS가 가능하도록 함
- DW/BI엔지니어 분들이 ETL 파이프라인을 관리하는데 리소스 낭비가 없도록 함
  - 테이블 관리를 분석가 분들이 직접 함으로써 데이터 엔지니어와 dependency를 줄임
  - 데이터 현황 모니터링 대시보드를 통해 데이터가 안정적으로 수집되고 있음을 확인하도록 함

![table_status](/static/images/projects/aws-bigquery-pipeline/table_status.png)

![table_status2](/static/images/projects/aws-bigquery-pipeline/table_status2.png)

- 장애가 발생할 경우 재처리를 할 수 있도록 백필하는 시스템(Prefect Flow) 제공

---

## 아쉬운 점

- CD를 구축하긴 하였지만, DMS와 코드를 각각 수정해야하는 문제점이 있음. 한꺼번에 수정하도록 wrapping하는 작업이 필요했음
- 준실시간 말고 로그성 데이터는 실시간성으로 받고싶었던 아쉬움. 데이터를 Produce하는 곳이 리소스가 없었음
