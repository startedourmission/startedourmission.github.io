---
date: 2026-04-08
tags:
  - 논문
  - 제프리힌턴
aliases:
  - "ReLU (2010)"
image: "![[1-relu.png]]"
description: "ReLU 활성화 함수를 RBM에 도입. 이후 거의 모든 딥러닝의 표준 활성화 함수가 되어 신경망 실무를 크게 단순화한 논문."
---

# Rectified Linear Units Improve Restricted Boltzmann Machines

신경망에서 활성화 함수는 신경원의 출력을 결정합니다. 이 논문은 ReLU의 확률적 정당화(stepped sigmoid → ReLU 수렴)를 제시하고 RBM에서의 효과를 입증했습니다.

> [1] V. Nair and G. E. Hinton, "Rectified linear units improve restricted boltzmann machines," in Proceedings of the 27th International Conference on Machine Learning, Haifa, Israel, June 2010, pp. 807–814.

## 배경

2010년, 활성화 함수는 여전히 시그모이드와 tanh가 주류였습니다. ICML 2010에서 발표된 이 논문은 생물학적 뉴런의 발화 패턴에서 영감을 받은 max(0, x)가 기존보다 월등히 효과적임을 보였습니다.

## 저자 소개

Vinod Nair는 토론토대 Hinton 연구실의 박사과정 학생으로, 이후 Google DeepMind에서 활동했습니다. Geoffrey Hinton은 토론토대 교수로 RBM과 딥러닝 실용화에 집중하고 있었습니다.

![[1-relu.png]]

## 요약

ReLU는 입력이 0 이상이면 그대로, 0 미만이면 0을 출력합니다. 수식: f(x) = max(0, x). 이 단순한 함수가 두 가지 큰 이점을 가집니다: (1) 계산이 매우 빠르고, (2) 다층 신경망에서 정보 손실이 적습니다.

**기술 스펙:**
- RBM의 이진 은닉층을 ReLU로 대체
- NORB 데이터셋(3D 객체 인식): 성능 향상 (이진 유닛 대비)
- 얼굴 인증(LFW): ReLU가 상대 강도 정보 보존
- 다층 특성 추출: ReLU가 정보를 더 잘 전파

## 논문 상세

### 배경
전통적 RBM은 이진 확률 단위를 사용합니다. 입력 x에 대해, 숨겨진 단위 j의 활성화 확률은 sigmoid(b_j + Σ w_ij x_i) 형태입니다. 문제점은 다음과 같습니다:
- 시그모이드는 포화되는 경향이 있어 그래디언트 소실 위험이 있습니다
- 다층에서 정보가 압축되는 경향이 있습니다
- 상대적 강도(relative magnitude) 정보가 손실됩니다

### 방법론

**무한 복사 모델(Infinite Copies Model):**
논문의 핵심 아이디어는 이진 단위의 무한 복사를 생각하는 것입니다. 각각 같은 가중치를 가지지만 점점 더 음의 편향을 가진다면, 그들의 합은 어떻게 될까요?

실제로는 이를 근사할 수 있는데, 이것이 바로 stepped sigmoid에서 ReLU로 수렴하는 과정입니다.

**구체적 형태:**
- 이진 단위: h_j = Bernoulli(sigmoid(b_j + Σ w_ij x_i))
- Stepped Sigmoid: 여러 복사본의 합
- ReLU 근사: h_j = max(0, b_j + Σ w_ij x_i) + Gaussian noise

노이즈는 훈련 중에만 있고, 추론(테스트)에서는 결정론적입니다.

### 결과

**NORB 데이터셋 (3D 물체 인식):**
- ReLU RBM: 더 우수한 특성 학습
- 이진 유닛 대비: 객체 분류 성능 향상

**얼굴 인증 (LFW):**
- ReLU: 상대 강도 정보 보존 (표정, 조명 변화 더 잘 포착)
- 이진 유닛: 이 정보가 손실되는 경향

**특성의 시각화:**
- 이진 유닛: 패턴의 유무만 정보로 삼음
- ReLU: 강도 차이(subtle variations)도 특성으로 표현

## 생각

**잘한 점:**
이 논문은 활성화 함수를 이론적으로 정당화했습니다. Stepped Sigmoid에서 ReLU로의 유도가 우아하고, 실험이 명확합니다. 무엇보다 이 아이디어는 즉시 실무에 채택되어 딥러닝 혁명을 가능하게 했습니다.

이진 활성화의 한계(상대 강도 정보 손실)를 명확히 지적하고, ReLU가 이를 해결함을 보인 것도 중요합니다.

**한계:**
- Stepped Sigmoid 해석은 흥미롭지만, ReLU가 정말 무한 복사의 근사인지 엄밀하게 증명하지 않았습니다.
- Gaussian 노이즈의 크기를 어떻게 설정하는지 명확하지 않습니다.
- RBM만 실험했습니다. 일반적 신경망에서도 작동하는지는 이 논문에서 직접 보이지 않았습니다 (하지만 이후에 증명되었습니다).
- ReLU의 "죽은 뉴런" 문제(음수 입력에서 영구히 0이 되는 문제)는 언급하지 않았습니다.

**의의:**
이것이 현대 딥러닝을 가능하게 한 논문입니다. ReLU의 단순성, 효율성, 효과성은 GPU 기반 대규모 학습을 가능하게 했습니다. 이 논문 이후 AlexNet(2012)이 ImageNet을 제패했고, 그 핵심 요소 중 하나가 ReLU였습니다.

개념상으로는 작은 논문이지만, 실무적 임팩트는 지난 15년간의 딥러닝 발전에서 가장 핵심적입니다.

## 후속 연구 링크

이 논문의 한계는 Hinton의 이후 연구에서 다루어졌습니다:
- **RBM에서만 검증** → [[ImageNet Classification with Deep Convolutional Neural Networks]]: AlexNet에서 일반 CNN에 ReLU를 적용하여 ImageNet을 제패했습니다

