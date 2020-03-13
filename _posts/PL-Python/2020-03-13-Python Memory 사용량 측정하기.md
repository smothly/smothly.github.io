---
layout: post
title: Python Memory 사용량 측정하기(memory profiler)
comments: true
categories : [Programming Language/Python]
tags: [Python, Memory, MemoryProfiler]
---

# Python Memory 사용량 측정하기(memory_profiler)

코드 라인별로 CPU를 측정해주는 [line_profiler](https://smothly.github.io/programming%20language/python/2020/03/12/Python-CPU%EC%82%AC%EC%9A%A9%EB%9F%89-%EC%B8%A1%EC%A0%95%ED%95%98%EA%B8%B0(line-profiler).html)에 이어 <br>
메모리 사용량을 측정해주는 `memory profiler`를 사용해보겠습니다.

이전 [line_profiler 포스트](https://smothly.github.io/programming%20language/python/2020/03/12/Python-CPU%EC%82%AC%EC%9A%A9%EB%9F%89-%EC%B8%A1%EC%A0%95%ED%95%98%EA%B8%B0(line-profiler).html)처럼 고성능 파이썬 책을 읽고 따라해보고 고찰한 것입니다. <br>
쥘리아집합 예제를 사용할 것입니다.<br><br>

`memory profiler`는 속도가 느립니다. 그래서 코드의 일부만 떼어내서 시험해보는것을 추천드립니다.<br>
그리고, CPU사용량처럼 정확하지 않습니다. 왜냐하면 파이썬의 Garbage Collector 작동 방식과 메모리 할당 비용이 비싸 메모리에 미리 할당해 놓기 때문입니다.<br><br>

---

> ## 시작

#### 라이브러리 설치
<pre><code>pip install memory_profiler</code></pre>

[코드](https://github.com/smothly/High_Perfomance_Python/blob/master/julia_example.py)
를 다운받으시거나 복사하셔서 `julia_example.py`로 생성해주고,
밑에 명령어로 실행해 줍니다.

<pre><code> python -m memory_profiler julia_example.py</code></pre>
저 같은 경우는 너무 오래걸려서 iteration을 조금 줄여서 실행했습니다. 참고로만 봐주세요

---


> ## 결과

![image](https://user-images.githubusercontent.com/37397737/76629599-e24b6580-6581-11ea-83df-325f603d39a0.png)
`Line Contents`는 원본 코드 입니다.<br>
`Mem Usage`는 현재 메모리 사용량<br>
`Increment`는 해당 줄이 얼마나 memory를 증가시켰는지를 알려주는 것입니다. 12번째 줄에서 약 0.008MB증가한 것을 볼 수 있습니다.<br>
비정상적 종료라 제대로 결과가 안나오는데 제대로 실행하면 increment와 mem usage도 정상적으로 나올 것 입니다.

---

> ## 결과 시각화

matplotlib이 안 깔려 있으면 설치해 주시고요.
<pre><code>pip install matplotlib</code></pre>
밑에 명령어를 실행해주시면
<pre><code> mprof run julia_example.py</code></pre>
하면 `??.dat` 파일이 생길겁니다. 밑에 명령어를 실행해주면 image.png파일이 생성됩니다.
<pre><code> mprof plot -o image.png --backend agg</code></pre>
사진파일을 열어보면 시간별로 memory usage를 보여주는 그래프가 나옵니다!
![image](https://user-images.githubusercontent.com/37397737/76581959-610bb880-6518-11ea-8a2b-60c6ce0ebc8e.png)

<br>

---

> ## 고찰

라이브러리를 이용하여 간단하게 `memory profiling`을 해보았습니다. <br>
이제 어느 부분에서 메모리가 많이 쓰이는지 알 수 있게 되었습니다! <br><br>

여기서는 range를 iterator로 변경해서 메모리를 줄일 수 있다.<br>
다른 방법은 잘 생각나지 않는다..<br><br>

참고로, 주피터 노트북 환경에서는 `%memit`를 셀 코드 맨앞에 추가함으로 측정할 수 있습니다.

<br><br><br>

> <subtitle>출처</subtitle>

- https://pypi.org/project/memory-profiler/
- 고성능 파이썬 책
- https://github.com/scari/high_performance_python/

<br><br>