#!/usr/bin/env python3
"""개발 서버 실행 스크립트"""

import subprocess
import sys
from pathlib import Path

def check_uv_available() -> bool:
    """UV 사용 가능 여부 확인"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, check=True)
        print(f"✅ UV 사용 가능: {result.stdout.decode().strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  UV를 찾을 수 없습니다. pip를 사용합니다.")
        return False

def install_with_uv() -> bool:
    """UV로 의존성 설치 (간단한 방법)"""
    print("📦 UV로 의존성 설치 중...")
    try:
        # 직접 패키지 설치 (빌드 문제 우회)
        packages = [
            "fastapi>=0.104.1",
            "jinja2>=3.1.2", 
            "uvicorn[standard]>=0.24.0",
            "python-multipart>=0.0.6",
            "markdown>=3.5.1",
            "pyyaml>=6.0.1",
            "python-frontmatter>=1.0.0"
        ]
        
        for package in packages:
            subprocess.run(["uv", "add", package], check=True, capture_output=True)
        
        print("✅ UV 의존성 설치 완료!")
        return True
    except subprocess.CalledProcessError:
        print("❌ UV 설치 실패")
        return False

def install_with_pip() -> bool:
    """pip로 의존성 설치"""
    print("📦 pip로 의존성 설치 중...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ pip 의존성 설치 완료!")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip 설치 실패")
        return False

def run_server(use_uv: bool):
    """개발 서버 실행"""
    print("🚀 개발 서버 시작...")
    print("🌐 http://localhost:8000 에서 확인하세요")
    print("⏹️  종료: Ctrl+C")
    print("-" * 40)
    
    if use_uv:
        cmd = ["uv", "run", "--", sys.executable, "-m", "uvicorn"]
    else:
        cmd = [sys.executable, "-m", "uvicorn"]
    
    cmd.extend(["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
    except Exception as e:
        print(f"❌ 서버 실행 오류: {e}")

def main():
    """메인 함수"""
    print("🐍 Python Portfolio - 개발 서버")
    print("=" * 35)
    
    use_uv = check_uv_available()
    
    # 의존성 설치
    success = False
    if use_uv:
        success = install_with_uv()
        if not success:
            print("🔄 pip로 대체합니다...")
            success = install_with_pip()
            use_uv = False
    else:
        success = install_with_pip()
    
    if not success:
        print("❌ 의존성 설치에 실패했습니다.")
        print("💡 start.py를 사용해보세요: python start.py")
        sys.exit(1)
    
    run_server(use_uv)

if __name__ == "__main__":
    main()
