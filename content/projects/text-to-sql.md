# Text To SQL Using LLM

## 목표

Chainlit과 LangChain(LangServe)를 활용하여 챗봇형태의 Text To SQL을 구축하여 데이터 추출 요청을 줄이고 사용자들이 쉽게 데이터를 추출할 수 있게 함

---

## 아키텍처

- **Frontend**: Chainlit을 활용한 챗봇 인터페이스
- **Backend**: LangChain + LangServe를 통한 LLM 파이프라인
- **Database**: 스키마 정보 및 메타데이터 관리
- **LLM**: OpenAI GPT 모델을 활용한 자연어 → SQL 변환

---

## 주요 기능

### 자연어 쿼리 처리
- 사용자의 자연어 질문을 SQL로 자동 변환
- 테이블 스키마 정보를 활용한 정확한 쿼리 생성
- 복잡한 조인 및 집계 쿼리 지원

### 스키마 인식
- 데이터베이스 스키마 자동 분석
- 테이블 관계 및 컬럼 정보 활용
- 동적 스키마 업데이트 지원

---

## 이슈 & 해결

### SQL 정확성
**이슈**
- LLM이 생성한 SQL의 문법 오류 및 논리적 오류

**해결**
- SQL 검증 로직 추가
- 스키마 정보를 프롬프트에 포함하여 정확성 향상
- Few-shot learning을 통한 예제 기반 학습

### 성능 최적화
**이슈**
- 복잡한 쿼리 생성 시 응답 시간 지연

**해결**
- 쿼리 캐싱 메커니즘 도입
- 스키마 정보 사전 로딩
- 비동기 처리를 통한 응답성 개선

---

## 성과

- 데이터 추출 요청 **70% 감소**
- 비개발자도 쉽게 데이터 조회 가능
- 데이터 엔지니어의 반복 작업 부담 경감
- 실시간 데이터 분석 환경 제공

---

## 아쉬운 점

- 복잡한 비즈니스 로직이 포함된 쿼리의 정확도 한계
- LLM 비용 관리 필요
- 보안 및 권한 관리 체계 보완 필요
