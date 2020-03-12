---
layout: post
title: Python CPU사용량 측정하기(line profiler)
comments: true
categories : [Programming Language/Python]
tags: [Python, CPU, LineProfiler]
---

# Python CPU사용량 측정하기(line profiler)


CPU 병목원인을 찾아주는 도구로 한줄씩 프로파일링 해주는 `line_profiler`를 사용해 보겠습니다.

- 프로파일링(profiling): 프로그램의 시간 복잡도 및 공간(메모리) 등 분석
- 병목(bottleneck): 전체 시스템의 성능이나 용량이 하나의 구성 요소로 인해 제한을 받는 현상

고성능 파이썬 책을 읽고 따라해보고 고찰한 것입니다. <br>
쥘리아집합 예제를 사용할 것입니다.
- 쥘리아 집합: 복작합 그림을 생성하는 프렉탈

자세한 건 저도 잘 모르고, CPU와 RAM사용량을 측정하기에 좋은 예제라고 합니다. [자세한 설명](https://ko.wikipedia.org/wiki/%EC%A5%98%EB%A6%AC%EC%95%84_%EC%A7%91%ED%95%A9)은 링크를 참조해주세요.
<br><br>

---

> ## 시작

#### 라이브러리 설치
<pre><code>pip install line_profiler</code></pre>

[코드](https://github.com/smothly/High_Perfomance_Python/blob/master/julia_example.py)
를 다운받으시거나 복사하셔서 `julia_example.py`로 생성해주고,
밑에 명령어로 실행해 줍니다.

<pre><code>kernprof -l -v  julia_example.py</code></pre>


- `-l`은 결과를 한줄씩 출력
- `-v`는 lprof파일 반환이 아니라 출력

---

> ## 결과

![image](https://user-images.githubusercontent.com/37397737/76531560-badc9600-64b8-11ea-952d-4d82d45d90e2.png)
Line Contents로 원본코드를 볼 수 있고, 다른 것들을 설명 드리겠습니다.<br>
`Hits`는 각 라인이 실행된 횟수입니다. CPU가 몇번 라인을 실행했는지입니다. 이것은 시간과 비례합니다.<br>
`Time` 항목에서 각 줄에서 시간이 얼마나 소요된지 확인할 수 있습니다.<br>
`%Time` 퍼센트로 약 34퍼센트가 17번째 while문에서 소요됨을 확인할 수 있습니다.<br>

밑에 결과는 바깥에서 함수를 실행한 부분으로 `calculate_z_serial_pureputhon(max_iterations, zs, cs)`가 전체 시간을 거의 차지함을 볼 수 있다.
![image](https://user-images.githubusercontent.com/37397737/76531722-fd9e6e00-64b8-11ea-919b-0502b10d2f11.png)
![image](https://user-images.githubusercontent.com/37397737/76531802-1444c500-64b9-11ea-96b2-fb71c3e909ff.png)

<br>

---

> ## 고찰

라이브러리를 이용하여 간단하게 `line profiling`을 해보았습니다. <br>
이번에는 어느 부분이 많이 실행되고 많은 시간이 소요되었는지를 확인할 수 있는 예제였습니다.<br>

예제 코드에서는 17, 18, 19번째에서 연산의 대부분이 진행되었습니다. 코드의 성능을 개선하기 위해서는 이 부분을 만져야 함을 알 수 있습니다!<br>

책에서는 나중에 이 코드를 어떻게 효율적으로 만들 것인지에 대해 알려줍니다.<br> 방법들을 몇 가지 나열해 보자면,

- numpy를 통한 벡터 연산
- cython/pypy를 통한 속도 향상
- 조건문 변경
- multiprocessing

을 통해 속도를 드라마틱하게 향상시켰습니다.

다음 포스팅에는 memory profiling을 하고, 향후에는 이 예제코드가 최고 효율을 내는 방법을 포스팅 해보겠습니다.
<br><br><br>

> <subtitle>출처</subtitle>

- https://ko.wikipedia.org/wiki/%EC%A5%98%EB%A6%AC%EC%95%84_%EC%A7%91%ED%95%A9
- 고성능 파이썬 책
- https://github.com/scari/high_performance_python/

<br><br>