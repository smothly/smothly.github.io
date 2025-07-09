#!/usr/bin/env python3
"""의존성 없이 정적 HTML 생성"""

import os
import shutil
from pathlib import Path

def create_simple_index():
    """간단한 index.html 생성"""
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SeungHo Choi - Senior Data Engineer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .hover-lift { transition: transform 0.3s ease, box-shadow 0.3s ease; }
        .hover-lift:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center py-4">
                <div class="text-2xl font-bold text-gray-800">SeungHo Choi</div>
                <div class="hidden md:flex space-x-8">
                    <a href="#about" class="text-gray-600 hover:text-gray-800 transition-colors">About</a>
                    <a href="#experience" class="text-gray-600 hover:text-gray-800 transition-colors">Experience</a>
                    <a href="#projects" class="text-gray-600 hover:text-gray-800 transition-colors">Projects</a>
                    <a href="#skills" class="text-gray-600 hover:text-gray-800 transition-colors">Skills</a>
                    <a href="#contact" class="text-gray-600 hover:text-gray-800 transition-colors">Contact</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="gradient-bg text-white py-20">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="mb-8">
                <img src="static/images/profile.jpg" alt="SeungHo Choi" class="w-32 h-32 rounded-full mx-auto mb-6 border-4 border-white shadow-lg">
            </div>
            <h1 class="text-5xl md:text-6xl font-bold mb-6">Senior Data Engineer</h1>
            <p class="text-xl md:text-2xl text-white/90 mb-8">데이터 생성부터 소비까지 End-to-End를 책임지는 4년차 시니어 데이터 엔지니어</p>
            <div class="flex justify-center space-x-6">
                <a href="https://github.com/smothly" class="text-white/80 hover:text-white text-2xl transition-colors">
                    <i class="fab fa-github"></i>
                </a>
                <a href="https://www.linkedin.com/in/csh0911/" class="text-white/80 hover:text-white text-2xl transition-colors">
                    <i class="fab fa-linkedin"></i>
                </a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-20 bg-white">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-bold text-center mb-16 text-gray-800">About Me</h2>
            <div class="max-w-3xl mx-auto">
                <p class="mb-6 text-lg leading-relaxed">
                <strong>데이터 생성부터 소비까지 End-to-End를 책임지는</strong> 4년차 시니어 데이터 엔지니어입니다.<br>
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
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section id="experience" class="py-20 bg-gray-50">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-bold text-center mb-16 text-gray-800">Experience</h2>
            <div class="bg-white rounded-2xl p-8 shadow-lg">
                <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0">
                        <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                            <i class="fas fa-building text-white"></i>
                        </div>
                    </div>
                    <div class="flex-1">
                        <h3 class="text-2xl font-bold text-gray-800">Senior Data Engineer</h3>
                        <p class="text-blue-600 font-semibold mb-2">Neowiz • 2022.01 - Present</p>
                        <p class="text-gray-600 mb-4">게임 데이터 플랫폼 설계 및 운영, 실시간 데이터 파이프라인 구축</p>
                        <ul class="space-y-2">
                            <li class="flex items-start">
                                <i class="fas fa-check-circle text-green-500 mt-1 mr-3"></i>
                                <span>🏗️ 멀티클라우드 실시간 데이터 파이프라인 구축 (AWS ↔ GCP, 일 4,000만 건 처리)</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-check-circle text-green-500 mt-1 mr-3"></i>
                                <span>💰 인프라 비용 최적화로 월 $1,000+ 절감 및 AWS 크레딧 $34K 확보</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-check-circle text-green-500 mt-1 mr-3"></i>
                                <span>🤖 LLM 기반 Text-to-SQL 시스템으로 데이터 추출 요청 70% 감소</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-check-circle text-green-500 mt-1 mr-3"></i>
                                <span>📊 Redshift 멀티클러스터 아키텍처 설계로 성능 병목 해결</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-check-circle text-green-500 mt-1 mr-3"></i>
                                <span>⚡ 자동화 및 모니터링 시스템으로 운영 리소스 90% 절감</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="py-20 bg-white">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-bold text-center mb-16 text-gray-800">Featured Projects</h2>
            <div class="grid md:grid-cols-2 gap-8">
                <!-- Project 1 -->
                <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl overflow-hidden shadow-lg hover-lift">
                    <div class="h-48 bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                        <i class="fas fa-project-diagram text-4xl text-white"></i>
                    </div>
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">Multi-Cloud Real-time Pipeline</h3>
                        <p class="text-gray-600 mb-4">AWS DMS CDC, Lambda, SQS를 활용한 멀티클라우드 실시간 데이터 파이프라인. 일 4,000만 건 데이터 처리</p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ 일 4,000만 건 처리</span>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ 99.9% 정합성</span>
                        </div>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">AWS DMS</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Lambda</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">BigQuery</span>
                        </div>
                    </div>
                </div>

                <!-- Project 2 -->
                <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl overflow-hidden shadow-lg hover-lift">
                    <div class="h-48 bg-gradient-to-r from-green-500 to-teal-600 flex items-center justify-center">
                        <i class="fas fa-database text-4xl text-white"></i>
                    </div>
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">Redshift 인프라 현대화</h3>
                        <p class="text-gray-600 mb-4">멀티클러스터 아키텍처로 전환하여 성능 병목 해결. AWS와 협업하여 $34K 크레딧 확보</p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ AWS 크레딧 $34K</span>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ Games on AWS 발표</span>
                        </div>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Redshift</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Terraform</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Grafana</span>
                        </div>
                    </div>
                </div>

                <!-- Project 3 -->
                <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl overflow-hidden shadow-lg hover-lift">
                    <div class="h-48 bg-gradient-to-r from-purple-500 to-pink-600 flex items-center justify-center">
                        <i class="fas fa-brain text-4xl text-white"></i>
                    </div>
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">LLM Text-to-SQL 시스템</h3>
                        <p class="text-gray-600 mb-4">LangChain과 OpenAI GPT를 활용한 자연어 쿼리 시스템. 데이터 추출 요청 70% 감소</p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ 요청 70% 감소</span>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ 자연어 → SQL</span>
                        </div>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">OpenAI GPT</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">LangChain</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Chainlit</span>
                        </div>
                    </div>
                </div>

                <!-- Project 4 -->
                <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl overflow-hidden shadow-lg hover-lift">
                    <div class="h-48 bg-gradient-to-r from-orange-500 to-red-600 flex items-center justify-center">
                        <i class="fas fa-chart-line text-4xl text-white"></i>
                    </div>
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">비용 최적화 프로젝트</h3>
                        <p class="text-gray-600 mb-4">S3 Intelligent Tiering, Graviton 등을 통한 체계적인 비용 최적화. 월 $1,000+ 절감</p>
                        <div class="flex flex-wrap gap-2 mb-4">
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ 월 $1,000+ 절감</span>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-xs rounded-full">✨ 자동 모니터링</span>
                        </div>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">S3 Lifecycle</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Graviton</span>
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">Lambda</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="py-20 bg-gray-50">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-4xl font-bold text-center mb-16 text-gray-800">Technical Expertise</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div class="bg-white rounded-2xl p-6 shadow-lg">
                    <h3 class="text-xl font-bold mb-4 text-gray-800 flex items-center">
                        <i class="fas fa-cloud mr-3 text-blue-600"></i>Cloud Platforms
                    </h3>
                    <div class="flex flex-wrap gap-2">
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">AWS (Expert)</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">Google Cloud</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">Azure</span>
                    </div>
                </div>
                <div class="bg-white rounded-2xl p-6 shadow-lg">
                    <h3 class="text-xl font-bold mb-4 text-gray-800 flex items-center">
                        <i class="fas fa-database mr-3 text-green-600"></i>Data Engineering
                    </h3>
                    <div class="flex flex-wrap gap-2">
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">Apache Spark</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">Kafka</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">Airflow</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">Trino</span>
                    </div>
                </div>
                <div class="bg-white rounded-2xl p-6 shadow-lg">
                    <h3 class="text-xl font-bold mb-4 text-gray-800 flex items-center">
                        <i class="fas fa-brain mr-3 text-pink-600"></i>AI/ML
                    </h3>
                    <div class="flex flex-wrap gap-2">
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">LangChain</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">OpenAI GPT</span>
                        <span class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm">MLflow</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20 bg-white">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-4xl font-bold mb-8 text-gray-800">Get In Touch</h2>
            <p class="text-xl text-gray-600 mb-8">데이터 엔지니어링에 대한 이야기를 나누고 싶으시다면 언제든 연락주세요!</p>
            <div class="flex justify-center space-x-8">
                <a href="https://github.com/smothly" class="flex items-center text-gray-600 hover:text-gray-800 transition-colors">
                    <i class="fab fa-github text-2xl mr-3"></i>
                    <span class="text-lg">GitHub</span>
                </a>
                <a href="https://www.linkedin.com/in/csh0911/" class="flex items-center text-gray-600 hover:text-gray-800 transition-colors">
                    <i class="fab fa-linkedin text-2xl mr-3"></i>
                    <span class="text-lg">LinkedIn</span>
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-12">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <p class="text-gray-300">&copy; 2024 SeungHo Choi. All rights reserved.</p>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """정적 사이트 생성"""
    print("🏗️  정적 HTML 생성 중...")
    
    # docs 디렉토리 생성
    docs_dir = Path("docs")
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir()
    
    # index.html 생성
    html_content = create_simple_index()
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # static 폴더 복사
    static_dir = Path("static")
    if static_dir.exists():
        shutil.copytree(static_dir, docs_dir / "static")
    
    print("✅ 정적 사이트 생성 완료!")
    print(f"📁 출력 디렉토리: {docs_dir.absolute()}")

if __name__ == "__main__":
    main()
