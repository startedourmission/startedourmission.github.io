---
date: 2025-10-21
tags:
  - 논문
  - LLM
aliases:
  - "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain"
image: "![[1-DragonHatchling.png]]"
description: Dragon Hatchling(BDH)은 트랜스포머와 뇌 모델 사이의 연결고리를 찾습니다. 생물학적으로 그럴듯한 그래프 기반 뉴런 네트워크로 설계되어, 헤비안 학습과 스파이킹 뉴런을 사용하면서도 GPT-2 수준의 성능을 달성했습니다. 핵심은 attention을 시냅스 가소성으로, feed-forward를 국소적 그래프 동역학으로 재해석한 것입니다.
---
"트랜스포머는 어떻게 작동하는가?"와 "뇌는 어떻게 사고하는가?"는 각각 AI와 신경과학의 핵심 질문입니다. 하지만 이 둘을 동시에 답하려는 시도는 많지 않았습니다. 트랜스포머는 밀집 텐서 연산에 기반한 중앙집중식 시스템이고, 뇌는 국소적으로 상호작용하는 분산 그래프 시스템이기 때문입니다.

> A. Kosowski, P. Uznański, J. Chorowski, Z. Stamirowska, and M. Bartoszkiewicz, "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain", arXiv preprint arXiv:2509.26507, September 2025, DOI: 10.48550/arXiv.2509.26507.

>**코드**: https://github.com/pathwaycom/bdh  
  **논문**: https://arxiv.org/abs/2509.26507 

이번에 소개할 Dragon Hatchling(BDH)은 이 두 세계를 잇는 다리를 제공합니다. BDH는 $n$개의 뉴런이 국소적으로 상호작용하는 그래프 기반 시스템으로 설계되었지만, GPU에서 효율적으로 학습 가능하며, 놀랍게도 GPT-2와 동등한 성능을 보입니다. 더 흥미로운 점은 BDH가 생물학적으로 그럴듯하다는 것입니다. 헤비안 학습(Hebbian learning)을 사용하고, 스파이킹 뉴런으로 구현 가능하며, attention 메커니즘이 시냅스 가소성으로 자연스럽게 설명됩니다.
![[1-DragonHatchling.png|454x479]]

## 요약

**아키텍처**: $n$개의 뉴런이 국소적으로 상호작용하는 그래프 기반 시스템. GPU 친화적 변형인 BDH-GPU도 제공

**핵심 방법론**:

- Edge-reweighting kernel: 시냅스 상태를 동적으로 조정하는 국소 그래프 동역학
- Linear attention in high dimension: $n$ 차원에서의 선형 어텐션
- ReLU-lowrank feed-forward: 모듈성과 스케일-프리 구조를 유도하는 비선형성

**데이터셋**: MNIST, WikiText, WMT14 번역 등

**평가 메트릭**: Cross-entropy loss, Test error rate

**주요 성과**:

- GPT-2와 동등한 스케일링 법칙 (10M~1B 파라미터)
- 생물학적으로 그럴듯한 뇌 모델로 표현 가능
- Monosemantic 뉴런과 희소 활성화 자연 발생
- 고modularity 및 heavy-tailed degree distribution의 emergent network

## 논문 상세

### 1. 연구 배경: 두 가지 미스터리

**첫 번째 미스터리: 뇌는 어떻게 추론하는가?**

뇌는 약 $10^{11}$개의 뉴런과 $10^{14}$개 이상의 시냅스를 가진 거대한 분산 시스템입니다. 하지만 우리는 뉴런의 국소적 동역학이 어떻게 언어나 추론 같은 고차원적 인지 기능으로 이어지는지 명확히 이해하지 못합니다.

**두 번째 미스터리: 트랜스포머와 뇌의 관계는?**

트랜스포머는 언어 모델링에서 엄청난 성공을 거두었지만, 밀집 텐서 기반의 중앙집중식 구조입니다. 반면 뇌는 sparse하고 국소적인 그래프 구조를 가집니다. 이 둘이 어떻게 연결될 수 있을까요?

**핵심 질문**: 언어 모델이 인간처럼 추론을 일반화하려면, 인간의 뇌가 사용하는 추론 함수를 효율적으로 에뮬레이션해야 합니다. 하지만 트랜스포머가 뇌를 튜링 머신 시뮬레이션으로 에뮬레이션하려면 단일 추론 단계에 수십억 개의 토큰이 필요할 것입니다. 그렇다면 트랜스포머가 실제로 뇌 기능과 관련이 있을까요?

### 2. BDH: 국소 그래프 동역학으로서의 언어 모델

#### 2.1 Edge-Reweighting Kernel

BDH의 핵심은 **edge-reweighting kernel**입니다. 이는 다음 두 가지 규칙을 결합합니다:

**규칙 1 - Modus Ponens 추론**:

$$X(i), \sigma(i, j) \rightarrow A(j)$$

"만약 사실 $i$가 믿을만하고($X(i)$), 규칙집합 $\sigma$에서 $i \rightarrow j$의 강도가 $\sigma(i, j)$라면, 사실 $j$에 대한 믿음 $A(j)$는 $X(i)\sigma(i, j)$만큼 증가한다"

**규칙 2 - 헤비안 학습**:

$$Y(i), X(j) \rightarrow \sigma(i, j)$$

"뉴런 $Y(i)$가 발화하고 이어서 $X(j)$가 발화하면, 시냅스 $\sigma(i, j)$의 강도가 $Y(i)X(j)$만큼 증가한다"

이 두 규칙은 $n$개의 사실(뉴런)에 대한 approximate reasoning system을 형성합니다. 시스템은 초기 연결에서 시작해 규칙을 적용하며 새로운 사실을 발견하고, 동시에 규칙집합을 재가중하여 초기 사실과 유도된 사실 간의 연결을 강화합니다.

#### 2.2 BDH의 상태 공간 방정식

BDH는 다음과 같은 국소 그래프 동역학으로 표현됩니다:

$$\begin{aligned} \sigma_{t,l} &:= \left(\sigma_{t-1,l} + \left(\left(y_{t,l-1}x_{t,l}^T\right) \odot G_s\right)\right) U \ x_{t,l} &:= x_{t,l-1} + \left(\left(G_e^x - G_i^x\right) y_{t,l-1}\right)_+ \ y_{t,l} &:= \left(\left(G_e^y - G_i^y\right)(\sigma_{t-1,l}x_{t,l})\right)_+ \odot x_{t,l} \end{aligned}$$

여기서:

- $x_{t,l}, y_{t,l} \in \mathbb{R}_+^n$: 뉴런 활성화 벡터
- $\sigma_{t,l} \in \mathbb{R}^{n \times n}$: 시냅스 상태 행렬
- $G_s, G_e^x, G_i^x, G_e^y, G_i^y$: 뉴런 상호작용 그래프의 파라미터
- $U$: 상태 감쇠/회전 행렬 (ALiBi 또는 RoPE)

**핵심 특징**:

- 모든 파라미터는 그래프의 topology와 weights로 표현됨
- 추론 중 상태는 이 그래프 topology의 edge-reweighting으로 표현됨
- 각 뉴런은 $O(d)$개의 파라미터로 특징지어짐 (여기서 $d \ll n$)

#### 2.3 생물학적 해석

BDH는 다음과 같이 뇌 모델로 표현 가능합니다:

**흥분성 및 억제성 회로**: $G_e^x - G_i^x$와 $G_e^y - G_i^y$는 흥분성과 억제성 연결을 나타냅니다.

**Integrate-and-Fire 뉴런**: ReLU 연산 $(·)_+$는 뉴런의 thresholding과 대응됩니다.

**헤비안 학습**: 시냅스 업데이트 규칙 $\sigma_{t,l} := \sigma_{t-1,l} + y_{t,l-1}x_{t,l}^T$는 고전적인 헤비안 학습 규칙입니다.

**스파이킹 동역학**: 국소 규칙들은 확률적 스파이킹 신호로 구현 가능합니다.

### 3. BDH-GPU: 텐서 친화적 구현

BDH를 GPU에서 효율적으로 학습하기 위해, 저자들은 **BDH-GPU**라는 변형을 제안합니다.

#### 3.1 핵심 아이디어

**문제**: BDH는 $\sigma \in \mathbb{R}^{n \times n}$ 상태 행렬을 사용하므로 메모리가 $O(n^2)$입니다.

**해결책**:

1. $\sigma$를 직접 구체화하지 않고, linear attention으로 접근
2. 그래프 $G_e^x, G_e^y$를 low-rank 분해: $G_e^x = D_xE$, $G_e^y = D_yE$
3. 압축된 상태 사용: $\rho_{t,l} = E\sigma_{t,l} \in \mathbb{R}^{d \times n}$

#### 3.2 BDH-GPU 방정식

$$\begin{aligned} \rho_{t,l} &:= \left(\rho_{t-1,l} + \text{LN}(Ey_{t,l-1}) x_{t,l}^T\right) U \ x_{t,l} &:= x_{t,l-1} + (D_x\text{LN}(Ey_{t,l-1}))_+ \ y_{t,l} &:= \left(D_y\text{LN}\left(\rho_{t-1,l}x_{t,l}\right)\right)_+ \odot x_{t,l} \end{aligned}$$

**파라미터 수**: BDH-GPU($n, d$)는 정확히 $(3 + o(1))nd$ 개의 파라미터를 가집니다.

- $E \in \mathbb{R}^{d \times n}$: encoder
- $D_x, D_y \in \mathbb{R}^{n \times d}$: decoders

**상태 크기**: 레이어당 $nd$ (BDH의 $n^2$보다 훨씬 작음)

#### 3.3 트랜스포머와의 비교

|특징|트랜스포머|BDH-GPU|
|---|---|---|
|Attention|Softmax (저차원 $d$)|Linear (고차원 $n$)|
|Activation|밀집|희소 ($\sim$5%)|
|FFN|MLP with ReLU|ReLU-lowrank|
|해석성|어려움|Monosemantic 뉴런|
|생물학적 타당성|낮음|높음|

### 4. 실험 결과

#### 4.1 스케일링 법칙

저자들은 10M~1B 파라미터 범위에서 BDH-GPU를 학습시켰습니다.

**WikiText Language Modeling**:

BDH-GPU는 GPT-2와 거의 동일한 스케일링 법칙을 보여줍니다. 동일한 파라미터 수와 동일한 훈련 데이터에서 유사한 perplexity를 달성했습니다.

**WMT14 영-독 번역**:

BDH-GPU는 트랜스포머 기반 모델과 비슷한 BLEU 점수를 기록했습니다.

#### 4.2 Emergent Properties

**1. Monosemantic 시냅스**

특정 시냅스 $\sigma(i, j)$가 특정 개념에 일관되게 반응합니다. 예를 들어, "Paris"와 "France"를 연결하는 시냅스는 지리적 관계를 나타내는 프롬프트에서 일관되게 강화됩니다.

**2. 희소 활성화**

활성화 벡터 $y$는 약 5% 정도의 희소성을 보입니다. 이는 L1 정규화 없이도 자연스럽게 발생합니다.

**3. 모듈성 및 스케일-프리 네트워크**

학습된 파라미터 행렬에서 읽어낸 뉴런 상호작용 그래프는:

- 높은 Newman modularity (커뮤니티 구조)
- Heavy-tailed degree distribution (허브 뉴런 존재)

를 보입니다. 이는 뇌의 connectome과 유사한 특성입니다.

#### 4.3 생물학적 타당성 검증

**working memory는 시냅스 가소성에만 의존**:

BDH의 추론 중 작업 기억은 오직 시냅스 상태 $\sigma$에만 저장됩니다. 이는 분(minutes) 단위의 시간 스케일에서 헤비안 학습을 사용하는 스파이킹 뉴런으로 구현 가능합니다.

**스파이킹 뉴런으로 구현 가능**:

저자들은 BDH의 국소 규칙들이 integrate-and-fire 뉴런과 헤비안 학습을 사용하는 스파이킹 신경망으로 표현 가능함을 formal하게 보였습니다.

### 5. 이론적 기여

#### 5.1 Macro-to-Micro Correspondence

BDH는 언어 모델의 거시적 attention 메커니즘과 뇌의 미시적 attention 메커니즘 사이의 formal한 대응을 제공합니다:

**거시적 (Transformer level)**: $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d}}\right)V$$

**미시적 (BDH level)**: $$\sigma(i, j) \text{ encodes connection strength from neuron } i \text{ to } j$$

이 두 개념이 $n \to \infty$ 극한에서 수렴합니다!

#### 5.2 Axiomatic AI

BDH는 **Axiomatic AI**의 예시입니다. 즉, 미시적 기초(뉴런 동역학)와 거시적 행동(언어 모델링)이 일관되고 잘 이해됩니다.

이는 다음을 가능하게 합니다:

- **길이 일반화**: 학습 시보다 긴 추론 chain에 대한 이론적 보장
- **모델 스케일링**: 여러 BDH 모델을 조합할 때의 행동 예측
- **Thermodynamic limit**: 큰 모델의 확률적으로 예측 가능한 행동

### 6. 추가 실험

#### 6.1 모델 병합

두 개의 독립적으로 학습된 BDH 모델을 단순히 concatenate하여 더 큰 모델을 만들 수 있습니다. 이 merged model은 여전히 BDH 아키텍처를 따르며, 두 원본 모델의 기능을 모두 보존합니다.

#### 6.2 Backpropagation Through Time 없이 학습

BDH는 각 레이어를 독립적으로 학습할 수 있어, BPTT 없이도 reasonable한 성능을 달성합니다.

## 한계점

1. **복잡한 태스크에서는 여전히 트랜스포머보다 약간 성능이 떨어짐**
2. **초기 학습률 조정이 까다로움**
3. **긴 컨텍스트 처리에서의 효율성은 추가 연구 필요**

## 의의 및 영향

### AI 엔지니어링 관점

**해석 가능성**: BDH의 뉴런은 monosemantic하고 희소 활성화를 보여, 모델의 내부 작동을 이해하기 쉽습니다.

**모델 병합**: 독립적으로 학습된 모델들을 쉽게 조합 가능합니다.

**Foreseeable AI**: 스케일-프리 구조로 인해 큰 모델의 행동을 작은 테스트로 예측 가능합니다.

### 뇌과학 관점

**언어 기능의 메커니즘**: BDH는 헤비안 학습이 어떻게 언어와 추론 기능을 지원할 수 있는지 구체적 메커니즘을 제공합니다.

**분(minutes) 스케일의 추론**: BDH는 "순간"에서 "분" 단위의 추론 동역학을 설명합니다. 더 긴 시간 스케일(시간~일)의 학습은 시냅스 상태에서 가중치로의 전이로 설명 가능합니다.

**실험 가능한 예측**: BDH는 특정 시냅스가 특정 개념에 반응한다는 testable prediction을 제공합니다.

## 결론

Dragon Hatchling은 트랜스포머와 뇌 모델 사이의 잃어버린 고리를 제공합니다. 국소 그래프 동역학으로 설계되어 생물학적으로 타당하면서도, GPU에서 효율적으로 학습 가능하고, GPT-2 수준의 성능을 달성했습니다.

이 연구는 두 가지 중요한 메시지를 전달합니다:

1. **AI 연구자들에게**: 언어 모델은 입자 기반 해석과 논리 프로그래밍 행동이 융합될 수 있습니다. Axiomatic AI로 가는 길이 열렸습니다.
    
2. **뇌과학자들에게**: 헤비안 학습과 스파이킹 뉴런만으로도 언어와 추론 기능을 설명할 수 있는 구체적 메커니즘이 존재합니다.
    

앞으로 BDH가 더 큰 스케일로 확장되고, 더 복잡한 태스크에 적용되면서, 우리는 언어와 추론의 "equations of reasoning"을 더 깊이 이해하게 될 것입니다.