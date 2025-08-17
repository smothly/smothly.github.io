"""포트폴리오 데이터 관리 모듈"""

import frontmatter
import markdown
from pathlib import Path
from typing import Dict, List, Optional

# 상수 정의
PERSONAL_INFO = {
    "name": "SeungHo, Choi",
    "title": "Data Engineer",
    "company": "Neowiz",
    "email": "seungho546@naver.com",
    "github": "https://github.com/smothly",
    "linkedin": "https://www.linkedin.com/in/csh0911/",
    "location": "Seoul, Korea"
}

ABOUT_TEXT = """
<p class="mb-6 text-lg leading-relaxed">
데이터가 잘 흐르고 다양하게 활용 될 수 있도록 꿈꾸고 실현하는 <b>5년차 데이터 엔지니어 최승호</b>입니다.
</p>

<p class="mb-6 text-lg leading-relaxed">
어떻게 하면 <b>안정적인 데이터 파이프라인</b>을 구축할 지,<br>
어떻게 하면 <b>비용효율적으로 데이터 플랫폼</b>을 구성할 지,<br>
어떻게 하면 <b>데이터 분석에 집중할 수 있는 환경</b>을 제공할 지<br>
지속적으로 고민하고 테스트하고 도입하는 데이터 엔지니어입니다.
</p>

<p class="mb-6 text-lg leading-relaxed">
데이터를 통해 인사이트를 낼 수 있다고 생각하며 그 가치가 무궁무진하다고 믿습니다.<br>
조직이 공통된 목표를 향해 나아갈 수 있도록 중간에서 커뮤니케이션하며 업무를 진행하여 인사이트를 내는데 도움이 되기를 희망합니다.
</p>
"""

EXPERIENCE_DATA = [
    {
        "company": "Neowiz",
        "position": "Data Engineer",
        "period": "2020.07 - Present",
        "description": "실시간(CDC) 데이터 파이프라인 구축 및 데이터 웨어하우스 운영",
        "achievements": [
            "🔄 15개 이상 다양한 데이터 소스 통합 및 일 10억건+ CDC ETL 구축",
            "📊 Redshift 멀티클러스터 아키텍처 설계로 성능 병목 해결 및 데이터 매쉬 구조 초석 마련",
            "🏗️ 멀티클라우드(AWS ↔ GCP)간 일 4000만건+ 실시간 데이터 파이프라인 구축",
            "⚡ 자동화 및 모니터링 시스템으로 운영 리소스 90% 절감",
            "💰 인프라 비용 최적화로 고정비용 20%($3,000+) 절감",
            "🤖 LLM 기반 Text-to-SQL 시스템으로 데이터 추출 요청 40% 감소",
        ]
    }
]

SKILLS_DATA = {
    "specialties": ["Real-time(CDC) Data Pipeline", "Multi-cloud Architecture", "Cost Optimization", "Data Governance"],
    "cloud_platforms": ["AWS ", "GCP"],
    "data_engineering": ["Prefect", "Apache Kafka", "Trino"],
    "data warehouse": ["Redshift", "BigQuery", "Snowflake"],
    "databases": ["MySQL", "PostgreSQL", "DynamoDB", "ElasticSearch", "Redis"],
    "programming": ["Python", "SQL", "Java"],
    "infrastructure": ["Terraform", "Docker", "ECS", "Grafana"],
    "ai_ml": ["LangChain", "Langfuse", "RedshiftML", "SageMaker", "OpenAI GPT"]
}

PROJECTS_DATA = [
    {
        "id": "aws-multi-cluster-architecture",
        "title": "AWS 멀티 클러스터 아키텍처 도입 (GAMES ON AWS 2024 발표)",
        "period": "2024.01 - 2024.06",
        "description": "단일 Redshift 클러스터의 성능 병목을 해결하기 위한 멀티클러스터 아키텍처 설계 및 구축. Redshift Serverless 및 Concurrency Scaling 도입으로 비용 최적화와 성능 향상을 동시에 달성",
        "tech_stack": ["Amazon Redshift", "Redshift Serverless", "WLM", "Concurrency Scaling"],
        "image": "/static/images/projects/aws-multi-cluster-architecture/multi-example.png",
        "highlights": ["AWS 크레딧 $34K 확보", "GAMES ON AWS 2024 발표"]
    },
    {
        "id": "multicloud-realtime-pipeline",
        "title": "Multi-Cloud Real-time Data Pipeline (AWS ↔ GCP)",
        "period": "2022.12 - 2023.05",
        "description": "AWS DMS CDC, Lambda, SQS를 활용하여 RDS Aurora의 데이터를 Google BigQuery로 준실시간 이동하는 멀티클라우드 파이프라인 구축. 일 4,000만 건 데이터 처리로 실시간 분석 및 FDS 지원",
        "tech_stack": ["AWS DMS", "AWS Lambda", "SQS", "Google BigQuery", "Python", "Serverless Framework"],
        "image": "/static/images/projects/multicloud-realtime-pipeline/architecture.png",
        "highlights": ["일 4,000만 건 데이터 처리", "99.9% 데이터 정합성", "평균 지연시간 1-2분", "실시간 FDS 지원"]
    },
    {
        "id": "trino-ecs-platform",
        "title": "Trino on ECS 기반 DataLake 플랫폼",
        "period": "2023.08 - 2024.01",
        "description": "Trino를 AWS ECS에 배포하여 다양한 데이터 소스를 통합 쿼리할 수 있는 DataLake 환경 구축. Apache Iceberg 테이블 포맷을 활용한 원본 데이터 확인 및 Federated Query 플랫폼 제공",
        "tech_stack": ["Trino", "AWS ECS", "Apache Iceberg", "S3 Lifecycle", "Glue Catalog", "Terraform"],
        "image": "/static/images/projects/trino-ecs-platform/trino.png",
        "highlights": ["ECS 기반 Federated Query Engine", "Iceberg 테이블 포맷",]
    },
    {
        "id": "streaming-data-collection",
        "title": "스트리밍 데이터 수집",
        "period": "2025.01 - 2025.05",
        "description": "Amazon MSK와 DynamoDB에서 생성되는 스트리밍 데이터 수집 및 처리 플랫폼 구축. 실시간 이벤트 스트림 처리와 반정형 데이터 처리",
        "tech_stack": ["Amazon MSK", "DynamoDB Streams", "MSK Connect", "AWS Lambda", "Python"],
        "image": "/static/images/projects/streaming-data-collection/msk_sample.png",
    },
    {
        "id": "text-to-sql-system",
        "title": "LLM 기반 Text-to-SQL 시스템",
        "period": "2024.01 - 2024.04",
        "description": "LangChain과 OpenAI GPT를 활용한 자연어 기반 SQL 생성 시스템 구축. 비개발자도 쉽게 데이터 조회가 가능하도록 하여 데이터 추출 요청을 감소시킨 솔루션",
        "tech_stack": ["OpenAI GPT", "LangChain", "Chainlit", "FastAPI", "Langfuse", "PostgreSQL"],
        "image": "/static/images/projects/text-to-sql-system/sample.png",
        "highlights": ["데이터 추출 요청 30% 감소", "자연어 → SQL 변환", "대화형 인터페이스", "프롬프트 엔지니어링"]
    },
    {
        "id": "infrastructure-management-and-monitoring",
        "title": "인프라 운영 및 모니터링 시스템",
        "period": "2021.01 - ",
        "description": "IaC 기반 인프라 관리와 종합적인 모니터링 시스템 구축. Terraform과 Serverless Framework를 통한 인프라 코드화 및 비용 최적화 자동화 시스템 도입",
        "tech_stack": ["Terraform", "Serverless Framework", "Grafana", "CloudWatch", "AWS Cost Explorer"],
        "image": "/static/images/projects/infrastructure-management-and-monitoring/sample.png",
        "highlights": ["IaC 기반 인프라 관리", "비용 최적화 대시보드", "쿼리 알람", "유휴 리소스 자동 관리"]
    },
    {
        "id": "diverse-data-sources",
        "title": "다양한 데이터 소스 통합",
        "period": "2021.01 - ",
        "description": "ElasticSearch, Google/Apple 마켓, Prometheus, Redis, SensorTower 등 15개 이상의 다양한 외부 데이터 소스를 안정적으로 수집하는 ETL 구축",
        "tech_stack": ["Prefect", "ElasticSearch", "Redis", "Prometheus", "RDS Snapshot", "API Integration"],
        "image": "/static/images/projects/diverse-data-sources/sample.png",
        "highlights": ["15개 이상 데이터 소스", "마켓 데이터 수집", "시계열 데이터 처리", "외부 공통 데이터(환율/GeoIP)"]
    },
    {
        "id": "other-projects",
        "title": "기타 프로젝트",
        "period": "2020.07 - ",
        "description": "Snowflake PoC, 마케팅 비용 관리 사이트 개발, 외부 API 구축, 공용 라이브러리 개발, ML(첫 구매자 예측, 이탈자 예측) 관련 배포 다양한 프로젝트 수행 및 조직 내 데이터 문화 확산",
        "tech_stack": ["Snowflake", "AI/ML", "Python", "FastAPI", "Docker"],
        "image": "/static/images/projects/other-projects/snowflake.png",
        "highlights": ["Snowflake PoC 수행", "마케팅 비용 관리 사이트 개발", "공용 라이브러리 구축", "AI 기반 고객 이탈 분석"]
    }
]

# 함수 정의
def get_portfolio_data() -> Dict:
    """포트폴리오 전체 데이터 반환"""
    return {
        "personal_info": PERSONAL_INFO,
        "about": ABOUT_TEXT,
        "experience": EXPERIENCE_DATA,
        "projects": PROJECTS_DATA,
        "skills": SKILLS_DATA
    }

def get_project_by_id(project_id: str) -> Optional[Dict]:
    """특정 프로젝트 상세 정보 반환"""
    project = next((p for p in PROJECTS_DATA if p["id"] == project_id), None)
    
    if not project:
        return None
    
    # 프로젝트 복사본 생성 (원본 데이터 보호)
    project_copy = project.copy()
    
    # 마크다운 파일에서 상세 내용 로드
    content_path = Path(f"content/projects/{project_id}.md")
    if content_path.exists():
        try:
            with open(content_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                project_copy["content"] = markdown.markdown(
                    post.content, 
                    extensions=['codehilite', 'fenced_code']
                )
        except Exception:
            project_copy["content"] = "<p>프로젝트 상세 내용을 불러올 수 없습니다.</p>"
    else:
        project_copy["content"] = "<p>프로젝트 상세 내용을 준비 중입니다.</p>"
    
    return project_copy
