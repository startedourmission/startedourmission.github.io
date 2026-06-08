---
date: 2026-03-31
tags:
  - 논문
  - 제프리힌턴
  - 딥러닝
description: 다층 신경망을 훈련하는 역전파 알고리즘을 Nature 한 편으로 정리하고, 은닉층이 과제에 맞는 내부 표현을 자동으로 만들 수 있음을 보인 1986년 논문입니다.
image: "![[backprop-symmetry-network.png]]"
---

> D. E. Rumelhart, G. E. Hinton, and R. J. Williams, "Learning representations by back-propagating errors," Nature, vol. 323, pp. 533-536, 1986.

다층 신경망을 어떻게 훈련할 것인가. 1986년에는 답이 없는 질문이었습니다. 단층 퍼셉트론은 XOR도 풀지 못한다는 비판이 17년 동안 신경망 연구를 얼려놓았고, 깊이를 늘리면 학습 신호를 어떻게 흘려야 할지 아무도 정리하지 못한 상태였습니다. [[David Rumelhart]], [[Geoffrey Hinton]], [[Ronald Williams]] 세 사람은 4페이지짜리 Nature 논문 한 편으로 이 문제를 정리해버립니다. 그 알고리즘이 오늘날 우리가 부르는 역전파(back-propagation)입니다.

## 저자

세 저자 모두 1980년대 connectionism 부흥의 한복판에 있던 사람들입니다. [[David Rumelhart]]는 UCSD Institute for Cognitive Science에서 PDP(parallel distributed processing) 그룹을 이끌고 있었고, 같은 해 출간된 3권짜리 PDP 시리즈로 분야의 교과서를 함께 정리하던 중이었습니다. [[Ronald Williams]]는 1983-1986년 사이 UCSD PDP 그룹에서 Rumelhart와 함께 일한 뒤 이 논문이 나온 해에 노스이스턴대로 옮겨갑니다. [[Geoffrey Hinton]]은 당시 카네기멜론대 컴퓨터과학과에서 신경망 연구를 이끌고 있었고, Boltzmann Machine 작업과 PDP 프로젝트에 동시에 발을 걸치고 있었습니다.

세 사람이 손을 잡은 동기는 명확합니다. PDP 시리즈는 "분산 표상이 인지를 설명한다"는 큰 주장을 펼치고 있었는데, 그 주장이 작동하려면 *다층 네트워크가 실제로 학습될 수 있다*는 증거가 필요했습니다. 역전파는 그 자리에 들어갈 알고리즘이었습니다. 논문 자체는 4페이지로 짧지만, 같은 해 PDP Vol. 1의 8장에 더 긴 버전이 실립니다.

## 배경

1969년 Minsky와 Papert의 *Perceptrons*가 단층 퍼셉트론이 XOR을 비롯한 비선형 분리 불가 문제를 풀 수 없음을 증명하면서 신경망 연구는 긴 침체기에 들어갑니다. 다층으로 쌓으면 표현력은 커지지만, 은닉 유닛의 가중치를 어떻게 조정해야 할지 모른다는 것이 결정적인 막힘이었습니다. 이를 *신용 할당 문제(credit assignment problem)*라고 불렀습니다. 출력 유닛의 오차는 직접 측정할 수 있지만, 중간층 유닛 하나가 그 오차에 얼마나 기여했는지를 어떻게 셈할 것인가.

체인 룰을 역방향으로 적용하는 아이디어 자체는 1970년대에 Werbos가 박사학위 논문에서 제안했고, 1985년에는 Yann Le Cun이 비슷한 변형을 독립적으로 발표합니다. 이 Nature 논문이 한 일은 *최초로 제안한 것*이 아니라, *최초로 신경망 학습 절차로서 명확하게 정리하고 작동하는 실험을 붙여 보여준 것*입니다. 그래서 분야 표준이 됩니다.

## 방법

논문이 정의하는 네트워크는 단순합니다. 입력층, 하나 이상의 은닉층, 출력층으로 이루어진 layered net이고, 같은 층 안의 연결과 위층에서 아래층으로 가는 연결은 금지하되 중간층을 건너뛰는 연결은 허용합니다.

유닛 $j$의 총입력 $x_j$는 아래 층 유닛들의 출력 $y_i$의 선형 결합으로 정의됩니다.

$$x_j = \sum_i y_i \, w_{ji}$$

비선형 출력은 시그모이드입니다.

$$y_j = \frac{1}{1 + e^{-x_j}}$$

오차는 출력 유닛의 실제 값 $y_{j,c}$와 목표 값 $d_{j,c}$의 차이를 모든 사례 $c$에 대해 제곱합한 값입니다.

$$E = \tfrac{1}{2} \sum_c \sum_j (y_{j,c} - d_{j,c})^2$$

핵심은 *역방향 패스*입니다. 출력층에서 시작해 $\partial E / \partial y_j = y_j - d_j$로 시작한 뒤, 체인 룰을 적용해 한 층씩 내려갑니다. 시그모이드의 도함수가 $y_j(1 - y_j)$로 깔끔하게 떨어진다는 점이 계산을 간단하게 만듭니다.

$$\partial E / \partial x_j = \partial E / \partial y_j \cdot y_j (1 - y_j)$$

가중치 $w_{ji}$에 대한 그래디언트는 아래 층 활성화 $y_i$와 위 층 오차 신호 $\partial E / \partial x_j$의 곱으로 떨어집니다.

$$\partial E / \partial w_{ji} = \partial E / \partial x_j \cdot y_i$$

업데이트는 모든 입출력 사례에 대한 그래디언트를 누적한 뒤 적용하는 batch SGD이고, 가속을 위해 모멘텀 항을 더합니다.

$$\Delta w(t) = -\varepsilon \, \partial E / \partial w(t) + \alpha \, \Delta w(t - 1)$$

이 모든 계산이 *국소적*이라는 점을 논문은 강조합니다. 각 가중치 업데이트에 필요한 정보는 자신이 연결하는 두 유닛의 활동과 위쪽에서 흘러 내려온 오차 신호뿐입니다. 병렬 하드웨어에서 그대로 구현할 수 있다는 뜻이고, 이 성질이 GPU 시대에 와서 결정적으로 작동합니다.

## 실험

세 가지 과제로 알고리즘을 검증합니다.

**대칭 판별.** 1차원 입력 벡터가 중심점을 기준으로 대칭인지 판별하는 과제입니다. 단순해 보이지만 개별 입력 유닛 하나만 봐서는 풀 수 없습니다. 은닉층이 반드시 필요합니다.

![[backprop-symmetry-network.png]]

논문은 입력 6개에 은닉 유닛 단 2개로 이 과제를 푸는 우아한 해를 학습된 결과로 보여줍니다. 학습된 가중치가 입력 중심을 기준으로 *부호가 반대이고 크기는 1:2:4*로 떨어진다는 점이 핵심입니다. 대칭 패턴이면 두 은닉 유닛으로 들어오는 가중합이 정확히 상쇄되어 둘 다 꺼지고, 비대칭 패턴이면 어느 한쪽이 켜져 출력에 신호가 갑니다. 사람이 설계하지 않았는데 네트워크가 알아서 이 해법을 찾았다는 점이 당시 충격적이었습니다.

- 사용 파라미터: $\varepsilon = 0.1$, $\alpha = 0.9$, 초기 가중치 $[-0.3, 0.3]$ 균등 분포
- 학습 비용: 64개 입력 벡터 전체에 대해 1,425회 sweep

**가족 관계 학습.** 더 흥미로운 과제는 두 개의 isomorphic한 가계도(영국인 가족과 이탈리아인 가족, 그림 참조)를 학습하는 것입니다.

![[backprop-family-trees.png]]

총 24명의 인물과 12개의 관계(father, mother, husband, wife, son, daughter, uncle, aunt, brother, sister, nephew, niece)로 만들어지는 ⟨person1, relationship, person2⟩ 삼중쌍 104개 중 100개로 훈련하고 나머지 4개로 일반화를 봅니다. 입력층은 인물 24개와 관계 12개, 은닉층은 6+12+6 구조, 출력층은 인물 24개입니다.

| 항목 | 값 |
| --- | --- |
| 학습 sweep | 1,500 |
| 초기 학습률 | $\varepsilon = 0.005$ (첫 20 sweep) → $\varepsilon = 0.01$ |
| 모멘텀 | $\alpha = 0.5$ → $\alpha = 0.9$ |
| weight decay | 0.2% per update |
| 학습 사례 | 104개 중 100개 |
| 일반화 평가 | 미학습 4개 모두 정답 |

은닉 유닛이 자동으로 의미 있는 특징을 학습한 점이 결과의 압권입니다. Unit 1은 *영국인 vs 이탈리아인*을 구별했고, Unit 2는 *세대*를 인코딩했으며, Unit 6은 *가족의 어느 가지(branch)*에 속하는지를 표현했습니다. 표상이 사전에 설계되지 않았는데 과제 구조에서 자연스럽게 발현됐다는 점이, 이후 30년 representation learning 패러다임의 출발점이 됩니다.

**Recurrent net 일반화.** 마지막으로 layered net 학습 절차가 그대로 recurrent net에도 적용 가능함을 보입니다. 시간축으로 펼친 동등한 layered net으로 매핑하면 같은 가중치가 여러 층에 등장하는데, 이 경우 *대응되는 가중치들의 그래디언트를 평균낸 뒤 동일하게 업데이트*하면 된다는 절차를 정리합니다. BPTT(backpropagation through time)의 원형입니다.

## 회고

저자들이 직접 한계로 적은 부분이 두 가지 있습니다.

첫째, **로컬 미니마 가능성**입니다. 오차 표면(error surface)에 국소 최소점이 존재할 수 있으므로 경사 하강이 전역 최적해 수렴을 보장하지 않습니다. 다만 본문에서는 *경험적으로 거의 빠지지 않는다*고 보고하고, 빠지는 경우는 연결이 과제를 풀기에 빠듯할 때뿐이며 연결을 조금 더 늘리면 가중치 공간의 추가 차원이 우회 경로를 만들어준다고 정리합니다.

둘째, **생물학적 비현실성**입니다. 논문 마지막 문단에 다음과 같이 솔직하게 적혀 있습니다.

> "The learning procedure, in its current form, is not a plausible model of learning in brains."

다만 흥미로운 내부 표상을 만들어낸다는 사실 자체가 *생물학적으로 더 그럴듯한 형태의 weight-space gradient descent를 찾을 가치가 있음을 시사한다*는 단서를 남깁니다. 이 단서는 30여 년 뒤 [[The Forward-Forward Algorithm - Some Preliminary Investigations]]에서 Hinton이 직접 다시 끌어올리게 됩니다.

논문이 *언급하지 않은* 한계도 짚어둘 만합니다. 깊이를 1-2층 이상으로 늘렸을 때 시그모이드 도함수가 0에 가까워지면서 그래디언트가 사라지는 vanishing gradient 문제는 본 논문에서 다뤄지지 않습니다. 이 문제는 1990년대 후반에야 체계적으로 진단되고, 2010년대에 [[Rectified Linear Units Improve Restricted Boltzmann Machines|ReLU]]와 잘 설계된 초기화, 배치 정규화가 결합되면서 실용적으로 해결됩니다.

## 정리

- 다층 신경망 학습의 신용 할당 문제를 체인 룰 역방향 적용으로 풀고, 작동하는 세 가지 실험으로 증명했습니다.
- 은닉 유닛이 사람 설계 없이 *영국인/이탈리아인*, *세대*, *가족 가지* 같은 의미 있는 특징을 자동으로 학습한다는 사실을 처음 보였습니다. 표상 학습의 출발점입니다.
- 알고리즘이 국소 계산만 요구한다는 성질 덕분에 30년 뒤 GPU 병렬 하드웨어에서 그대로 작동했고, PyTorch와 TensorFlow의 autograd가 지금도 같은 식을 계산합니다.

## 후속 연구 링크

이 논문이 남긴 빈자리는 Hinton의 이후 연구에서 채워집니다.

- 깊은 네트워크 훈련의 어려움 → [[A Fast Learning Algorithm for Deep Belief Nets]]: 층별 사전훈련으로 우회
- 시그모이드 vanishing gradient → [[Rectified Linear Units Improve Restricted Boltzmann Machines]]: ReLU로 완화
- 역전파의 생물학적 비현실성 → [[The Forward-Forward Algorithm - Some Preliminary Investigations]]: 순전파 두 번으로 학습
