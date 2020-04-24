---
layout: post
title: Python 소리 데이터 (Audio Data)Augmentation
comments: true
categories : [Programming Language/Python]
tags: [Python, Audio, Augmentation, Deeplearning]
---

# Python 소리 데이터 (Audio Data)Augmentation

`소리 데이터 augmentation`에 다양한 방법에 대해 알아보겠습니다.<br>
먼저 말씀드리자면, 이 코드는 올해 1월에 했던 빅데이터분석연합동아리 투빅스 컨퍼런스에 했던 코드들입니다.<br>
이때 했던 프로젝트는 [Singing Voice Conversion](https://github.com/sora-12/Singing-Voice-Conversion)으로 기회가 되면 `Cycle GAN`내용과 함께 나중에 포스팅 하겠습니다.<br><br>

이미지 같은 경우는 noise, 회전, 압축 등 다양한 `augmentation` 방법이 있고 설명도 많은데, 소리 같은 경우는 코드나 방법에 관한 내용이 별로 없습니다. 그래서 제가 알고 있고 사용했던 총 5가지 방법을 포스팅하겠습니다.(참고로 이 augmentation 방법이 정확하고 항상 설명력이 있다고는 못함을 전제합니다.)

---

> ## Augmentation Code

### 라이브러리 설치
다 설치 되어있으시면 넘어가셔도 됩니다.
<pre><code>pip install librosa
pip install numpy
pip install matplotlib</code></pre>
<br>

전체 코드는 [여기](https://github.com/smothly/High_Perfomance_Python/blob/master/Untitled.ipynb) 올려놓겠습니다. 블로그에서는 함수 별로 설명하겠습니다.

### 원본 데이터 Plot
![image](https://user-images.githubusercontent.com/37397737/77171823-58ab1300-6b00-11ea-8126-b0c8dd5037aa.png)

원본 데이터를 plot 한 것으로 다른 함수들과 비교하며 설명하겠습니다.

> ## 1. White Noise

<pre><code class='python'>def adding_white_noise(data, sr=22050, noise_rate=0.005):
    # noise 방식으로 일반적으로 쓰는 잡음 끼게 하는 겁니다.
    wn = np.random.randn(len(data))
    data_wn = data + noise_rate*wn
    plot_time_series(data_wn)
    librosa.output.write_wav('./white_noise.wav', data, sr=sr) # 저장
    print('White Noise 저장 성공')
    
    return data</code></pre> 
![image](https://user-images.githubusercontent.com/37397737/77171603-0ff35a00-6b00-11ea-8ce6-15915642ad2a.png)

이미지와 비슷하게 잡음 끼게 하였습니다. 그림에서 보다시피 원본데이터에 비해 그래프가 두꺼워진 것을 볼 수 있습니다. 흔히 쓰는 방법으로 모델의 일반화를 하는데 많은 도움을 줍니다.

---

> ## 2. Shifting

<pre><code class='python'>def shifting_sound(data, sr=22050, roll_rate=0.1):
    # 그냥 [1, 2, 3, 4] 를 [4, 1, 2, 3]으로 만들어주는겁니다.
    data_roll = np.roll(data, int(len(data) * roll_rate))
    plot_time_series(data_roll)
    librosa.output.write_wav('./rolling_sound.wav', data, sr=sr)
    print('rolling_sound 저장 성공')
    
    return data</code></pre>
![image](https://user-images.githubusercontent.com/37397737/77172171-e4bd3a80-6b00-11ea-9afe-1db2f1abb02a.png)

주석에서 쓰여있다 싶이 말 그대로 데이터를 `roll`하는 것이다. 원래 빨간선 쯤에서 끝났던 데이터가 새로운 지점에서 시작합니다. classfication할 때 추가 데이터로 도움이 됩니다.

---

> ## 3. Stretching

<pre><code class='python'>def stretch_sound(data, sr=22050, rate=0.8):
    # stretch 해주는 것 테이프 늘어진 것처럼 들린다.
    stretch_data = librosa.effects.time_stretch(data, rate)
    plot_time_series(stretch_data)
    librosa.output.write_wav('./stretch_data.wav', stretch_data, sr=sr)
    print('stretch_data 저장 성공')
    
    return data</code></pre>
![image](https://user-images.githubusercontent.com/37397737/77172511-6dd47180-6b01-11ea-819f-cb7f100a41a0.png)

우리 귀에는 테이프처럼 늘어지게 하는것이다. 자세한 설명은 [librosa 공식홈페이지](https://librosa.github.io/librosa/generated/librosa.effects.time_stretch.html)를 참고해주세요. 그림으로 보면 빈공간들이 채워진 느낌이 듭니다. 위에 예제들과 비슷한 상황에 쓰입니다.

--- 

> ## 4. Reverse

<pre><code class='python'>def reverse_sound(data, sr=22050):
    # 거꾸로 재생
    data_len = len(data)
    data = np.array([data[len(data)-1-i] for i in range(len(data))])
    plot_time_series(data)
    librosa.output.write_wav('./reverse_data.wav', data, sr=sr)
    
    return data</code></pre>
![image](https://user-images.githubusercontent.com/37397737/77172856-ffdc7a00-6b01-11ea-9802-0ff1b85ad86c.png)

소리를 거꾸로 재생하는 겁니다. 원본데이터 세로축 기준으로 뒤집어 졌다고 보시면 됩니다. 위에 3가지 방법과 다른 점은 원본데이터의 변형을 가하지 않았다는 점입니다. 그래서 제가 했던 voice conversion project에서 사용했던 방법입니다.

--- 

> ## 5. Minus

<pre><code class='python'>def minus_sound(data, sr=22050):
    # 위상을 뒤집는 것으로서 원래 소리와 똑같이 들린다.
    temp_numpy = (-1)*data
    plot_time_series(temp_numpy)
    librosa.output.write_wav('./minus_data.wav', temp_numpy, sr=sr)
    
    return data</code></pre>
![image](https://user-images.githubusercontent.com/37397737/77173384-c5271180-6b02-11ea-97c3-a5f77dccc2af.png)

그림에서도 보다시피 x축 기준으로 뒤집는 것인데, 이게 사람귀에는 똑같이 들립니다. 실제로 확인해 보셔도 됩니다. 이것도 원본에 변형을 가하지 않고 단순한 대칭이므로 프로젝트에 사용했었습니다.

---

이상으로 python으로 간편하게  할수 있는 `5가지 augmentation 방법`에 대해 보았습니다. 음성전문가가 아니라 설명이 잘못 되어있을 수도 있습니다.(태클 환영합니다) 음성 관련 ML/DL 프로젝트하실 때 유용하게 사용하십시오! 

<br><br><br>

> <subtitle>출처</subtitle>

- https://github.com/sora-12/Singing-Voice-Conversion/blob/master/Preprocessing/data_augmentation.ipynb
- https://www.kaggle.com/CVxTz/audio-data-augmentation
- https://librosa.github.io/librosa/generated/librosa.effects.time_stretch.html

<br><br>