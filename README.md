# Python Portfolio Website

**SeungHo Choi**의 데이터 엔지니어 포트폴리오 웹사이트입니다. Python FastAPI 기반으로 구축되었으며, 깔끔하고 현대적인 디자인을 제공합니다.

## ✨ 특징

- **🐍 Python 기반**: FastAPI + Jinja2로 구축
- **🎨 현대적 디자인**: TailwindCSS 기반 반응형 UI
- **📱 모바일 친화적**: 모든 디바이스에서 완벽한 표시
- **⚡ 빠른 성능**: 정적 사이트 생성으로 빠른 로딩
- **🚀 GitHub Pages 배포**: 자동 배포 지원
- **✏️ 쉬운 수정**: Python 코드로 간단한 내용 관리

## 🚀 빠른 시작

### 가장 간단한 방법 (추천)

```bash
python quick_start.py
```

이 명령어 하나로 모든 의존성을 자동 설치하고 서버를 실행합니다.

### 다른 실행 방법들

```bash
# UV 사용 (UV가 설치된 경우)
python run_dev.py

# 수동 설치 후 실행
pip install fastapi jinja2 uvicorn markdown python-frontmatter
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

브라우저에서 `http://localhost:8000`으로 접속하여 확인할 수 있습니다.

## 📁 프로젝트 구조

```
python-portfolio/
├── main.py                    # FastAPI 애플리케이션
├── data/
│   └── portfolio_data.py      # 포트폴리오 데이터 (여기만 수정하면 됩니다!)
├── templates/
│   ├── index.html            # 메인 페이지
│   ├── project.html          # 프로젝트 상세 페이지
│   └── 404.html              # 404 페이지
├── content/projects/          # 프로젝트 마크다운 파일들
├── static/images/            # 이미지 파일들
├── quick_start.py            # 간단한 실행 스크립트
├── run_dev.py               # 개발 서버 실행 (UV 지원)
├── build_static.py          # 정적 사이트 빌드
└── requirements.txt         # Python 의존성
```

## ✏️ 내용 수정하기

### 1. 개인 정보 수정

`data/portfolio_data.py` 파일의 `PERSONAL_INFO` 상수를 수정하세요:

```python
PERSONAL_INFO = {
    "name": "Your Name",
    "title": "Your Title", 
    "company": "Your Company",
    "email": "your.email@example.com",
    "github": "https://github.com/yourusername",
    "linkedin": "https://www.linkedin.com/in/yourprofile/",
}
```

### 2. 자기소개 수정

`data/portfolio_data.py` 파일의 `ABOUT_TEXT` 상수를 수정하세요:

```python
ABOUT_TEXT = """
<p class="mb-6 text-lg leading-relaxed">
여기에 자기소개를 작성하세요.
</p>
"""
```

### 3. 프로젝트 추가/수정

`data/portfolio_data.py` 파일의 `PROJECTS_DATA` 리스트에 프로젝트를 추가하세요:

```python
{
    "id": "new-project",
    "title": "새로운 프로젝트",
    "period": "2024.01 - 2024.03",
    "description": "프로젝트 설명",
    "tech_stack": ["Python", "FastAPI", "PostgreSQL"],
    "image": "/static/images/your-image.png",  # 대표 이미지 경로
    "github": "https://github.com/username/project"
}
```

**대표 이미지 설정 방법:**
- 이미지를 `static/images/` 폴더에 업로드
- `"image"` 필드에 이미지 경로 지정
- 각 프로젝트마다 다른 이미지 사용 가능
- 예시: 
  - `"/static/images/projects/aws-bigquery-pipeline/architecture.png"` (아키텍처 다이어그램)
  - `"/static/images/projects/aws-bigquery-pipeline/table_status.png"` (모니터링 화면)
  - `"/static/images/projects/aws-bigquery-pipeline/table_status2.png"` (대시보드 화면)

그리고 `content/projects/new-project.md` 파일을 생성하여 상세 내용을 작성하세요.

### 4. 기술 스택 수정

`data/portfolio_data.py` 파일의 `SKILLS_DATA` 딕셔너리를 수정하세요:

```python
SKILLS_DATA = {
    "languages": ["Python", "JavaScript", "Java"],
    "frameworks": ["FastAPI", "React", "Django"],
    # ...
}
```

## 🌐 GitHub Pages 배포

### 1. 정적 사이트 빌드

```bash
python build_static.py
```

### 2. GitHub에 배포

```bash
git add .
git commit -m "Update portfolio"
git push origin main
```

GitHub Actions가 자동으로 사이트를 빌드하고 배포합니다.

### 3. GitHub Pages 설정

1. GitHub 저장소 → Settings → Pages
2. Source: "Deploy from a branch" 선택
3. Branch: "gh-pages" 선택
4. 저장

## 🛠️ 기술 스택

- **Backend**: FastAPI
- **Template Engine**: Jinja2
- **Styling**: TailwindCSS
- **Markdown**: Python-Markdown
- **Deployment**: GitHub Pages
- **Package Management**: UV (선택적)

## 📝 마크다운 작성 가이드

프로젝트 상세 페이지는 마크다운으로 작성됩니다:

```markdown
# 프로젝트 제목

## 개요
프로젝트에 대한 설명...

## 기술 스택
- Python
- FastAPI
- PostgreSQL

## 주요 기능
1. 기능 1
2. 기능 2

## 성과
- 성과 1
- 성과 2
```

## 🎨 디자인 커스터마이징

### 색상 변경

`templates/index.html`에서 CSS 클래스를 수정:

```css
.gradient-bg { 
    background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%); 
}
```

### 레이아웃 수정

- `templates/index.html`: 메인 페이지 레이아웃
- `templates/project.html`: 프로젝트 상세 페이지 레이아웃
- `templates/404.html`: 404 페이지

## 🔧 개발 도구

```bash
# 코드 포맷팅 (선택적)
pip install black isort
black .
isort .

# 개발 서버 (자동 재시작)
python quick_start.py
```

## 📞 문의

질문이나 제안사항이 있으시면 언제든 연락주세요!

- **Email**: your.email@example.com
- **GitHub**: [Your GitHub](https://github.com/yourusername)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

**💡 Tip**: `data/portfolio_data.py` 파일만 수정하면 대부분의 내용을 변경할 수 있습니다!
