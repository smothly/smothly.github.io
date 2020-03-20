---
layout: post
title: Python Iterator Generator 설명
comments: true
categories : [Programming Language/Python]
tags: [Python, Iterator, Generator, Memory]
---

# Python Iterator Generator 설명

#### Iterator(이터레이터): next()를 호출했을 때 다음값을 생성해내는 상태를 가진 헬퍼 객체(iterable)
#### Generator(제너레이터): 이터레이터의 종류로서 그 값을 그떄그때 생성해냄 yield 키워드를 가지고 있음

결론부터 말하자면, 제너레이터는 메모리/CPU 효율이 더 좋습니다. 제너레이터에 대해 설명해보겠습니다.<br><br>

우리가 loop를 돌릴 때 흔히 쓰는 `range`의 내부 문법을 보면 제너레이터에 대해 알 수 있습니다.
<pre><code class='python'>def range(start, stop, step=1):
    while start < stop:
        yield start
        start += step</code></pre> 
이렇습니다. 여기서 생소해 보이는 것이 `yield`함수를 쓰는 것입니다.<br>
파이썬 2에서는 기존에는 yield 방식이 아니라 그냥 append를 해서 전체 메모리가 잡는 방식을 사용했었습니다.(xrange라는 함수로 제너레이터 방식이 존재는 했었습니다.)<br>
만약에 range를 선언할 때 마다, 크기 만큼의 리스트가 만들어지면 메모리가 엄청나게 낭비 됐을 겁니다.<br><br>
제너레이터는 `yield`를 실행하는 순간 함수는 그 값을 방출하고, 다음 요청에는 이전 상태를 유지했다가 새 값을 방출합니다. 계속 반복하다가 `StopIteration` 예외를 발생시켜 함수를 종료시킵니다.<br>
간단한 제너레이터의 예제로서, 순차적이고 현재값만 필요한 경우 유용합니다.

---

> ## 리스트와 비교

코드는 밑과 같고 이전 포스트에 올렸던 [memory profiling](https://smothly.github.io/programming%20language/python/2020/03/13/Python-Memory-%EC%82%AC%EC%9A%A9%EB%9F%89-%EC%B8%A1%EC%A0%95%ED%95%98%EA%B8%B0.html)을 해보겠습니다.
![image](https://user-images.githubusercontent.com/37397737/77132264-1fdc5100-6aa2-11ea-8041-02cf6cfb0669.png)

파이썬3에서는 기본적으로 loop가 제너레이터 형식으로 되어있어 시간상에는 차이가 없고, 메모리 사용량을 보면 차이남(0.555 mb)을 볼 수 있습니다. 조금 rough한 예제라 큰 차이가 아니여 보이는데 실제로 더 큰 데이터를 사용하게 되면 엄청 큰 차이를 느끼실 수 있습니다.<br><br>
간단한 사용법을 알려드리자면, `list comphrension`을 아시는 분들은
<pre><code class='python'>A = [i for i in range(0, 100000)]</code></pre>
이런식으로 보통 사용하실텐데, 제너레이터를 만드는 간단한 방법은 `[] => ()`로 바꿔주시면 됩니다. (tuple이 아닙니다.)
<pre><code class='python'>A = (i for i in range(0, 100000))</code></pre>
참고로, 이런식으로 만들면 우리가 기존에 쓰던 list 문법(`len()`, `index()`등)들이 안먹힙니다.<br>
그래서 sum(A)이런식으로 길이를 구하기도 합니다만 경우에 따라 제너레이터와 리스트를 적절히 사용하시면 될 것 같습니다.

<br><br><br>

> <subtitle>출처</subtitle>

- 고성능 파이썬 책
- https://github.com/scari/high_performance_python/
- https://mingrammer.com/translation-iterators-vs-generators/

<br><br>