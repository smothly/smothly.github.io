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
    "email": "your.email@example.com",
    "github": "https://github.com/smothly",
    "linkedin": "https://www.linkedin.com/in/csh0911/",
    "location": "Seoul, Korea"
}

ABOUT_TEXT = """
<p class="mb-6 text-lg leading-relaxed">
<strong>데이터 생성부터 소비까지 End-to-End를 책임지는</strong> 4년차 데이터 엔지니어입니다.<br>
게임 산업에서 <strong>일 4,000만 건의 데이터를 안정적으로 처리</strong>하며, 실시간 데이터 파이프라인부터 AI/ML 인프라까지 구축해왔습니다.
</p>

<p class="mb-6 text-lg leading-relaxed">
<strong>비용 효율성과 안정성을 동시에 추구</strong>하는 것이 저의 강점입니다.<br>
AWS 크레딧 $34K 확보, 월 $1,000+ 비용 절감, 99.9% 데이터 정합성 달성 등<br>
<strong>기술적 우수성을 비즈니스 가치로 전환</strong>하는 능력을 입증해왔습니다.
</p>

<p class="text-lg leading-relaxed">
단순한 데이터 파이프라인 구축을 넘어, <strong>조직의 데이터 문화를 혁신</strong>하는 것이 목표입니다.<br>
LLM 기반 Text-to-SQL로 데이터 추출 요청 70% 감소, 자동화를 통한 운영 리소스 90% 절감 등<br>
<strong>기술로 사람과 조직의 생산성을 극대화</strong>하는 데이터 엔지니어입니다.
</p>
"""

EXPERIENCE_DATA = [
    {
        "company": "Neowiz",
        "position": "Data Engineer",
        "period": "2022.01 - Present",
        "description": "게임 데이터 플랫폼 설계 및 운영, 실시간 데이터 파이프라인 구축",
        "achievements": [
            "🏗️ 멀티클라우드 실시간 데이터 파이프라인 구축 (AWS ↔ GCP, 일 4,000만 건 처리)",
            "💰 인프라 비용 최적화로 월 $1,000+ 절감 및 AWS 크레딧 $34K 확보",
            "🤖 LLM 기반 Text-to-SQL 시스템으로 데이터 추출 요청 70% 감소",
            "📊 Redshift 멀티클러스터 아키텍처 설계로 성능 병목 해결",
            "⚡ 자동화 및 모니터링 시스템으로 운영 리소스 90% 절감",
            "🔄 15개 이상 다양한 데이터 소스 통합 및 실시간 ETL 구축"
        ]
    }
]

SKILLS_DATA = {
    "cloud_platforms": ["AWS (Expert)", "Google Cloud Platform", "Azure"],
    "data_engineering": ["Apache Spark", "Apache Kafka", "Airflow", "dbt", "Trino", "Prefect"],
    "databases": ["Redshift", "BigQuery", "PostgreSQL", "MySQL", "DynamoDB", "ElasticSearch", "Redis"],
    "programming": ["Python", "SQL", "Scala", "Java", "JavaScript"],
    "infrastructure": ["Terraform", "Docker", "ECS", "Kubernetes", "Grafana", "Prometheus"],
    "ai_ml": ["LangChain", "OpenAI GPT", "MLflow", "Scikit-learn", "TensorFlow"],
    "specialties": ["Real-time Data Pipeline", "Multi-cloud Architecture", "Cost Optimization", "Data Governance"]
}

PROJECTS_DATA = [
    {
        "id": "realtime-multicloud-pipeline",
        "title": "Multi-Cloud Real-time Data Pipeline (AWS ↔ GCP)",
        "period": "2022.12 - 2023.03",
        "description": "AWS DMS CDC, Lambda, SQS를 활용하여 RDS Aurora의 데이터를 Google BigQuery로 준실시간 이동하는 멀티클라우드 파이프라인 구축. 일 4,000만 건 데이터 처리로 실시간 분석 및 FDS 지원",
        "tech_stack": ["AWS DMS", "AWS Lambda", "SQS", "Google BigQuery", "Python", "Terraform"],
        "image": "/static/images/projects/aws-bigquery-pipeline/architecture.png",
        "highlights": ["일 4,000만 건 데이터 처리", "99.9% 데이터 정합성", "평균 지연시간 1-2분", "실시간 FDS 지원"]
    },
    {
        "id": "redshift-modernization",
        "title": "Redshift 인프라 현대화 & 멀티클러스터 아키텍처",
        "period": "2024.01 - 2024.06",
        "description": "단일 클러스터 DW 환경을 멀티클러스터로 전환하여 성능 병목 해결. AWS와 협업하여 Games on AWS 발표 및 $34K 크레딧 확보. Concurrency Scaling, 암호화, 비용 최적화 적용",
        "tech_stack": ["Amazon Redshift", "AWS", "Terraform", "Grafana", "CloudWatch"],
        "image": "/static/images/projects/aws-bigquery-pipeline/table_status.png",
        "highlights": ["AWS 크레딧 $34K 확보", "Games on AWS 발표", "성능 병목 해결", "무중단 암호화 적용"]
    },
    {
        "id": "llm-text-to-sql",
        "title": "LLM 기반 Text-to-SQL 시스템 (MayoBot)",
        "period": "2024.01 - 2024.03",
        "description": "LangChain과 OpenAI GPT를 활용한 챗봇 형태의 Text-to-SQL 시스템 구축. 자연어 질의를 SQL로 변환하여 데이터 추출 요청을 70% 감소시키고 비개발자도 쉽게 데이터 조회 가능",
        "tech_stack": ["OpenAI GPT", "LangChain", "Chainlit", "FastAPI", "Langfuse"],
        "image": "/static/images/projects/aws-bigquery-pipeline/table_status2.png",
        "highlights": ["데이터 추출 요청 70% 감소", "자연어 → SQL 변환", "대화형 인터페이스", "프롬프트 최적화"]
    },
    {
        "id": "data-lake-trino",
        "title": "Trino 기반 DataLake 플랫폼 구축",
        "period": "2023.12 - 2024.01",
        "description": "Trino를 AWS ECS에 배포하여 다양한 데이터 소스(S3, BigQuery, Redshift 등)를 통합 쿼리할 수 있는 DataLake 환경 구축. Federated Query와 Iceberg 테이블 포맷 활용",
        "tech_stack": ["Trino", "AWS ECS", "Apache Iceberg", "S3", "Glue Catalog"],
        "image": "/static/images/projects/aws-bigquery-pipeline/architecture.png",
        "highlights": ["15개 이상 데이터 소스 통합", "Federated Query 지원", "Iceberg 테이블 포맷", "ECS 기반 Auto Scaling"]
    },
    {
        "id": "cost-optimization",
        "title": "AWS 인프라 비용 최적화 프로젝트",
        "period": "2021.01 - 2024.06",
        "description": "S3 Intelligent Tiering, Graviton 인스턴스, Serverless 아키텍처 등을 통한 체계적인 비용 최적화. 월 $1,000+ 절감 달성 및 지속적인 비용 모니터링 체계 구축",
        "tech_stack": ["AWS Cost Explorer", "S3 Lifecycle", "Graviton", "Lambda", "Grafana"],
        "image": "/static/images/projects/aws-bigquery-pipeline/table_status.png",
        "highlights": ["월 $1,000+ 비용 절감", "S3 Intelligent Tiering", "Graviton 적용", "자동 비용 모니터링"]
    },
    {
        "id": "external-data-integration",
        "title": "다양한 외부 데이터 소스 통합 플랫폼",
        "period": "2021.01 - 2024.06",
        "description": "Google/Apple 마켓, Data.ai, ElasticSearch, DynamoDB, Redis 등 15개 이상의 외부 데이터 소스를 안정적으로 수집하는 통합 플랫폼 구축. API 제한 대응 및 자동 복구 시스템 포함",
        "tech_stack": ["Python", "AWS Lambda", "Prefect", "API Integration", "Redis", "DynamoDB"],
        "image": "/static/images/projects/aws-bigquery-pipeline/table_status2.png",
        "highlights": ["15개 이상 데이터 소스", "API Rate Limiting 대응", "자동 복구 시스템", "실시간 모니터링"]
    },
    {
        "id": "automation-monitoring",
        "title": "데이터 파이프라인 자동화 & 모니터링 시스템",
        "period": "2022.01 - 2024.12",
        "description": "Grafana, CloudWatch, Prefect를 활용한 종합적인 모니터링 시스템 구축. 자동화를 통해 운영 리소스 90% 절감 및 장애 대응 시간 최소화",
        "tech_stack": ["Grafana", "CloudWatch", "Prefect", "AWS SNS", "Slack API"],
        "image": "/static/images/projects/aws-bigquery-pipeline/architecture.png",
        "highlights": ["운영 리소스 90% 절감", "실시간 장애 감지", "자동 복구 시스템", "통합 대시보드"]
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
