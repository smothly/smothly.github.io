---
layout: post
title: 네이버 영화 리뷰 EDA & Clustering(Kmeans)    
comments: true
categories : [Data Science/NLP]
tags: [NLP, Python, Clustering, EDA, K-means]
---

> ## 데이터 수집(네이버 영화 리뷰)

[크롤링 포스트](https://smothly.github.io/data%20science/nlp/2020/01/13/%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%98%81%ED%99%94-%EB%A6%AC%EB%B7%B0-%ED%81%AC%EB%A1%A4%EB%A7%81(Crawling).html)를 사용하여 네이버 영화 데이터를 약 2만개 모았습니다.
<br><br>

> ## EDA & 시각화 & K-means를 활용한 클러스터링

해본 것들을 설명드리면
- EDA: 평점 분포, 품사 별 긍부정 분포 
- K-means를 활용한 군집화
- 이외에 전처리나 WordCloud
<br><br>
결과와 코드는 [소스 노트북 파일](https://github.com/smothly/ToBigs/blob/master/week8/NLP/nlpProject.ipynb)을 참고하여 봐주시기 바랍니다!
<br><br>

사이드 프로젝트 느낌으로 해본거라 많이 부족합니다. NLP기본적인 것들 배운것을 활용하여 진행했습니다.
<br><br>

이외에도 딥러닝을 활용하여 감성분석을 진행할 수도 있고,

LDA, LSA등 토픽모델링로 군집화를 진행해볼 수 있었는데 제일 간단한 머신러닝 기법인 K-means로 진행하였습니다.


<br><br>

> <subtitle>출처</subtitle>

- https://medium.com/ml2vec/using-word2vec-to-analyze-reddit-comments-28945d8cee57
- https://github.com/smothly/ToBigs/blob/master/week8/NLP/nlpProject.ipynb
- https://github.com/smothly/ai_innovation_NLP/blob/master/6.21%2C%2026%20Sentiment%20Analysis%20%EC%8B%A4%EC%8A%B5.ipynb

<br><br>
