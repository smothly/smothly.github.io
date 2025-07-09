#!/usr/bin/env python3
"""환경 독립적인 빠른 실행 스크립트"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """필요한 모듈 확인"""
    required_modules = [
        'fastapi', 'jinja2', 'uvicorn', 'markdown', 'frontmatter'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    return missing

def install_missing(missing_modules):
    """누락된 모듈 설치 시도"""
    if not missing_modules:
        return True
    
    print(f"📦 누락된 모듈 설치 시도: {', '.join(missing_modules)}")
    
    # 여러 방법으로 설치 시도
    install_commands = [
        [sys.executable, "-m", "pip", "install"] + missing_modules,
        ["pip3", "install"] + missing_modules,
        ["pip", "install"] + missing_modules,
    ]
    
    for cmd in install_commands:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ 모듈 설치 성공!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    print("❌ 자동 설치 실패. 수동으로 설치해주세요:")
    print(f"pip install {' '.join(missing_modules)}")
    return False

def run_server():
    """서버 실행"""
    print("🚀 개발 서버를 시작합니다...")
    print("🌐 http://localhost:8000 에서 확인하세요")
    print("⏹️  종료: Ctrl+C")
    print("-" * 40)
    
    # 현재 디렉토리를 Python 경로에 추가
    current_dir = str(Path.cwd())
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        # uvicorn 직접 실행
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("❌ uvicorn을 찾을 수 없습니다.")
        print("💡 수동 설치: pip install uvicorn")
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
    except Exception as e:
        print(f"❌ 서버 실행 오류: {e}")

def main():
    print("🐍 Python Portfolio - 빠른 시작")
    print("=" * 35)
    
    # 의존성 확인
    missing = check_dependencies()
    
    if missing:
        if not install_missing(missing):
            print("\n💡 수동 설치 후 다시 실행해주세요:")
            print("pip install fastapi jinja2 uvicorn markdown python-frontmatter")
            sys.exit(1)
        
        # 설치 후 다시 확인
        missing = check_dependencies()
        if missing:
            print(f"❌ 여전히 누락된 모듈: {missing}")
            sys.exit(1)
    
    print("✅ 모든 의존성이 준비되었습니다!")
    run_server()

if __name__ == "__main__":
    main()
