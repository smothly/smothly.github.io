#!/usr/bin/env python3
"""정적 HTML 파일 생성 스크립트 (GitHub Pages 배포용)"""

import shutil
import subprocess
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from data.portfolio_data import get_portfolio_data, get_project_by_id, PROJECTS_DATA

OUTPUT_DIR = Path("docs")
TEMPLATES_DIR = "templates"
STATIC_DIR = Path("static")

def check_uv_installed() -> bool:
    """UV 설치 확인"""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ UV가 설치되지 않았습니다. pip로 대체 실행합니다.")
        return False

def install_dependencies() -> bool:
    """의존성 설치"""
    # UV 사용 시도 (간단한 방법)
    if check_uv_installed():
        print("📦 UV로 의존성을 설치합니다...")
        try:
            packages = [
                "fastapi>=0.104.1", "jinja2>=3.1.2", "uvicorn[standard]>=0.24.0",
                "python-multipart>=0.0.6", "markdown>=3.5.1", "pyyaml>=6.0.1", 
                "python-frontmatter>=1.0.0"
            ]
            for package in packages:
                subprocess.run(["uv", "add", package], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ UV 설치 실패, pip로 대체합니다.")
    
    print("📦 pip로 의존성을 설치합니다...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ 의존성 설치에 실패했습니다.")
        return False

def setup_output_directory():
    """출력 디렉토리 설정"""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

def create_main_page(env: Environment, data: dict):
    """메인 페이지 생성"""
    print("📄 메인 페이지 생성 중...")
    template = env.get_template('index.html')
    html_content = template.render(**data)
    
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def create_project_pages(env: Environment):
    """프로젝트 상세 페이지들 생성"""
    print("📁 프로젝트 페이지 생성 중...")
    project_dir = OUTPUT_DIR / "project"
    project_dir.mkdir()
    
    template = env.get_template('project.html')
    
    for project in PROJECTS_DATA:
        project_data = get_project_by_id(project['id'])
        if project_data:
            html_content = template.render(project=project_data)
            with open(project_dir / f"{project['id']}.html", "w", encoding="utf-8") as f:
                f.write(html_content)

def create_404_page(env: Environment):
    """404 페이지 생성"""
    print("❌ 404 페이지 생성 중...")
    template = env.get_template('404.html')
    html_content = template.render()
    
    with open(OUTPUT_DIR / "404.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def copy_static_files():
    """정적 파일 복사"""
    if STATIC_DIR.exists():
        print("📂 정적 파일 복사 중...")
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")

def build_static_site():
    """정적 사이트 빌드"""
    setup_output_directory()
    
    # Jinja2 환경 설정
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    data = get_portfolio_data()
    
    print("🚀 정적 사이트 빌드 시작...")
    
    create_main_page(env, data)
    create_project_pages(env)
    create_404_page(env)
    copy_static_files()
    
    print("✅ 정적 사이트 빌드 완료!")
    print(f"📁 출력 디렉토리: {OUTPUT_DIR.absolute()}")
    print("🌐 GitHub Pages에 배포하려면 docs 폴더를 커밋하고 푸시하세요.")

def main():
    """메인 함수"""
    print("🏗️  Python Portfolio - 정적 사이트 빌드")
    print("=" * 45)
    
    if not install_dependencies():
        sys.exit(1)
    
    try:
        build_static_site()
    except Exception as e:
        print(f"❌ 빌드 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
