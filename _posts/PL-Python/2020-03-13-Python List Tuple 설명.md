---
layout: post
title: Python List Tuple 설명
comments: true
categories : [Programming Language/Python]
tags: [Python, List, Tuple]
---

# Python List Tuple 설명

Python에서 흔히 쓰는 `리스트[ ]`, `튜플( )` 자료형에 대해 알아보겠습니다.<br>
보통은 혼용해서 쓰기 마련인데, 차이점들을 설명해드리겠습니다.

---

> ## List 리스트

- 동적배열
  - 변경이 가능한 배열로 `append`명령어를 통해 리스트를 변경할 수 있음
- 초기할당은 정해진 양만큼 하지만, `append`를 쓰는 순간 초과할당을 합니다.
  - resize연산이 가능하여 길이가 N짜리 배열을 만드는 것이 아니라 N + M(M > N)인 여유분이 있는 배열을 만듭니다.
  - memory할당과 복사 요청 횟수를 줄이기 위함입니다.
  - 리스트 크기 할당 방정식: (N >> 3) + (N < 9 ? 3 : 6) ex) 10,000,000짜리 배열이 약 16,000,000개 배열만큼 메모리를 사용함

> ## Tuple 튜플

- 정적배열
  - 튜플은 한 번 생성되면 내용을 바꾸거나 크기를 변경할 수 없다.
  - 합치는건 가능 ex) tuple1 + tuple2
- 여유 공간 할당 x
- 리소스 캐싱
  - 크기가 20이하인 튜플은 GC를 통해 메모리를 반환하지 않는다.
  - 같은 크기의 튜플이 필요해지면 메모리에 새로 할당받지 않고, 기존에 있던걸 사용함

---

> ## 언제 써야 할까?

앞서 말한 리소스 캐싱 기능 덕분에 튜플을 중복할당할 일이 생기면 속도차이가 생깁니다.
![image](https://user-images.githubusercontent.com/37397737/76627397-4a984800-657e-11ea-8a4d-50fb5c824103.png)

보통은 `list`를 쓰는게 더 편하겠지만, 정적데이터에 한해서는 `tuple`을 쓰는 버릇을 들이는 게 좋아보입니다.<br>
list와 tuple 타입만으로 동적, 정적데이터가 구분될 수 있습니다.

<br><br><br>

> <subtitle>출처</subtitle>

- 고성능 파이썬 책
- https://github.com/scari/high_performance_python/

<br><br>