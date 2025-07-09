# Infra Management

## 목표

AWS Cloud상에서 IaC(Terraform), DW(Redshift/Bigquery) Monitoring, Grafana를 통한 인프라 모니터링 및 알람, Cost Optimization, 공용라이브러리 등 다양한 인프라 관리 경험을 쌓음

---

## 주요 영역

### Infrastructure as Code (IaC)
- **Terraform**을 활용한 인프라 자동화
- 버전 관리를 통한 인프라 변경 추적
- 환경별 인프라 구성 관리 (Dev/Staging/Prod)

### 데이터 웨어하우스 모니터링
- **Redshift** 성능 모니터링 및 최적화
- **BigQuery** 쿼리 비용 및 성능 분석
- 슬롯 사용량 및 대기열 모니터링

### 통합 모니터링 시스템
- **Grafana** 대시보드를 통한 시각화
- **CloudWatch** 메트릭 수집 및 알람
- **Slack** 연동을 통한 실시간 알림

### 비용 최적화
- AWS Cost Explorer를 활용한 비용 분석
- 리소스 사용량 기반 Right-sizing
- Reserved Instance 및 Spot Instance 활용

---

## 아키텍처

### IaC 파이프라인
```
GitHub → Terraform Cloud → AWS Resources
```

### 모니터링 스택
```
CloudWatch → Grafana → Slack Alerts
```

### 비용 관리
```
Cost Explorer → Budget Alerts → Optimization Reports
```

---

## 이슈 & 해결

### 인프라 드리프트
**이슈**
- 수동 변경으로 인한 Terraform 상태와 실제 인프라 불일치

**해결**
- Terraform Plan을 통한 정기적 드리프트 감지
- 변경 승인 프로세스 도입
- 자동화된 상태 동기화

### 모니터링 알람 피로도
**이슈**
- 과도한 알람으로 인한 중요 알람 무시

**해결**
- 알람 우선순위 분류 체계 구축
- 임계값 조정 및 알람 그룹핑
- 에스컬레이션 정책 수립

### 비용 급증
**이슈**
- 예상치 못한 리소스 사용량 증가로 인한 비용 급증

**해결**
- 실시간 비용 모니터링 대시보드 구축
- 예산 기반 자동 알림 설정
- 리소스 태깅을 통한 비용 추적

---

## 성과

### 인프라 자동화
- **95% 이상**의 인프라를 코드로 관리
- 배포 시간 **80% 단축**
- 인프라 변경 오류 **90% 감소**

### 모니터링 개선
- 장애 감지 시간 **평균 5분 이내**
- 시스템 가용성 **99.9% 달성**
- 운영 효율성 대폭 향상

### 비용 최적화
- 월 AWS 비용 **30% 절감**
- 불필요한 리소스 **정기적 정리**
- 비용 예측 정확도 향상

---

## 구축한 공용 라이브러리

### Terraform 모듈
- VPC, RDS, ECS 등 재사용 가능한 모듈
- 보안 정책이 적용된 표준 모듈
- 환경별 설정 템플릿

### 모니터링 템플릿
- Grafana 대시보드 템플릿
- CloudWatch 알람 템플릿
- 로그 분석 쿼리 모음

### 비용 관리 도구
- 비용 분석 스크립트
- 리소스 사용량 리포트 자동화
- 최적화 권장사항 생성기

---

## 아쉬운 점

- 초기 IaC 도입 시 학습 곡선으로 인한 시간 소요
- 레거시 인프라의 코드화 작업 복잡성
- 다양한 모니터링 도구 간의 통합 부족
