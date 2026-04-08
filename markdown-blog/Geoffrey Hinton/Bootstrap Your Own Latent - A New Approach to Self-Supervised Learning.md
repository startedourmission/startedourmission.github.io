---
date: 2026-04-20
tags:
  - 논문
  - 제프리힌턴
aliases:
  - "BYOL (2020)"
description: 부정 샘플 없이 자기지도 학습하는 방법. SimCLR과 달리 음의 예가 필요 없으며, 온라인-타겟 네트워크 구조로 표현 학습 수행
image: "![[1-byol.png]]"
---

# Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning (BYOL, 2020)

> Grill, J.-B., Strub, F., Altché, F., Tallec, C., Richemond, P. H., Buchatskaya, E., ..., & Hinton, G. E. (2020). Bootstrap your own latent: A new approach to self-supervised learning. In *Advances in Neural Information Processing Systems* (NeurIPS 2020).

![[1-byol.png]]

## 배경

2020년은 자기지도 학습의 결정적 해였습니다. "음의 예 없이는 표현이 붕괴한다"는 정설을 DeepMind 팀이 NeurIPS 2020에서 정면으로 뒤집었습니다.

## 저자 소개

Jean-Bastien Grill이 제1저자로 실험을 주도했습니다. Koray Kavukcuoglu는 DeepMind 부사장으로 LeCun 연구실 출신입니다. Rémi Munos는 강화학습 이론의 권위자입니다. Hinton은 직접 저자는 아니지만 BYOL은 Hinton의 SimCLR에 대한 직접적 응답입니다.

## 요약

SimCLR이 자기지도 학습의 새로운 지평을 열었지만, 한 가지 문제가 있었습니다. 큰 배치와 많은 "음의 예(negative examples)"를 필요로 한다는 점입니다. 메모리가 많이 필요합니다.

BYOL은 근본적으로 다른 접근을 시도합니다. **음의 예가 없어도 됩니다.** 대신 온라인 네트워크와 타겟 네트워크라는 두 개의 네트워크가 서로를 부스트합니다(bootstrap).

온라인 네트워크는 이미지 하나의 증강본을 처리하고, 타겟 네트워크의 다른 증강본 표현을 예측하려 합니다. 타겟 네트워크의 가중치는 온라인 네트워크의 지수 이동 평균(EMA)으로 업데이트됩니다. 이는 일종의 "자가-감독 신호"를 만듭니다.

결과는 놀랍습니다. BYOL은 선형 평가(linear evaluation)에서 74.3%를 달성하며 SimCLR의 69.3%(ResNet-50 기준)를 능가하면서도 메모리를 적게 사용합니다. 그리고 더 중요한 것은 "왜 음의 예 없이 작동하는가"라는 물음을 던진다는 점입니다.

## 논문 상세

### 배경: 대조 학습의 문제

SimCLR의 핵심은 대조 손실입니다. 같은 샘플 쌍은 가깝게, 다른 샘플은 멀게 배치합니다.

$$\ell_{i,j} = -\log \frac{\exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_j) / \tau)}{\sum_{k=1}^{N} \exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_k) / \tau)}$$

문제는 분모에 있습니다. 모든 다른 샘플들($k \neq i$)이 "음의 예"로 기여해야 합니다. 이는:
- 큰 배치 필요 (배치 크기 4096)
- 높은 메모리 요구
- GPU 간 동기화 복잡

### 방법론: 온라인-타겟 네트워크

BYOL의 구조는 다음과 같습니다.

**온라인 네트워크 $\theta$:**
$$\mathbf{q}_\theta = \text{proj}_q(\text{pred}(f_\theta(\tilde{x})))$$

**타겟 네트워크 $\xi$ (EMA 업데이트):**
$$\mathbf{z}_\xi = \text{proj}(\text{enc}_\xi(\tilde{x}')), \quad \xi \leftarrow \tau \xi + (1 - \tau) \theta$$

손실:
$$\ell = 2 - 2 \cdot \frac{\mathbf{q}_\theta \cdot \mathbf{z}_\xi}{\|\mathbf{q}_\theta\| \|\mathbf{z}_\xi\|}$$

(코사인 유사도를 최대화합니다)

**핵심 차이:**
- 음의 예 없음. 같은 이미지의 두 증강본 쌍만 필요합니다
- 타겟 네트워크는 이동 평균으로 업데이트됩니다 (학습되지 않음)
- 기본 배치 크기 4096 (논문에서 더 작은 배치에서도 강건함을 검증)

### 왜 작동하는가?

이것은 논문의 가장 미스터리한 부분입니다. 대조 학습 이론에 따르면, 음의 예가 없으면 모든 벡터를 동일한 값으로 붕괴시켜야 합니다(collapse). 그런데 왜 작동할까요?

가설:
1. **이동 평균의 역할**: 타겟 네트워크가 온라인 네트워크보다 천천히 변합니다. 이는 안정적인 목표(stable target)를 제공해 붕괴를 방지합니다.
2. **중지 경사(stop gradient)**: 타겟 네트워크의 가중치 업데이트가 온라인 네트워크에 영향을 주지 않습니다. 이것이 비대칭성을 만들어 붕괴를 방지합니다.
3. **확률론적 효과**: 각 배치가 다른 증강을 만들므로, 매번 다른 목표를 추적하게 됩니다.

완전한 이론적 설명은 여전히 미해결입니다. (이후 연구에서 "바람직한 하이퍼파라미터가 암묵적으로 정규화를 제공한다"는 설명이 제시되었습니다.)

### 결과

ImageNet 선형 평가(linear evaluation, ResNet-50 기준):
- BYOL: 74.3% Top-1 정확도
- SimCLR: 69.3% Top-1 정확도

또한:
- 배치 크기 축소에 강건: 기본 배치 크기 4096이지만, SimCLR 대비 작은 배치에서도 성능 하락이 적습니다
- 데이터 증강 선택에 더 강건합니다 (SimCLR처럼 특정 augmentation에 민감하지 않습니다)
- 장시간 훈련에 안정적입니다

## 생각

**잘한 점:**
- 음의 예 없는 자기지도 학습을 실현했습니다. 개념적으로 도발적입니다
- 메모리 효율성이 높습니다. 실제 GPU 자원 제약이 있는 상황에서 실용적입니다
- 성능이 더 높습니다. SimCLR을 뛰어넘었습니다
- 구현이 간단합니다. EMA 업데이트만 필요합니다

**한계:**
- 이론적 설명이 부족합니다. "왜" 작동하는지 명확하지 않으며, 이는 이후 연구 과제가 되었습니다
- 붕괴 방지 메커니즘이 완전히 이해되지 않았습니다
- 온라인-타겟 구조가 사전훈련-미세조정 패러다임과의 상호작용이 명확하지 않습니다
- 추론 시 온라인 네트워크를 사용하는지 타겟 네트워크를 사용하는지 논문에서 명확하지 않은 부분이 존재합니다

**의의:**
BYOL은 자기지도 학습의 "왜"에 대한 기본 가정을 도전했습니다. "음의 예가 필수인가?"라는 질문에 "아니다"라고 답했습니다.

이후 여러 연구가 이 질문을 깊이 있게 탐구했습니다:
- SimCSE: 대조 학습의 최소 요구사항 분석
- VICReg: 분산-불변성-공변성 정규화

또한 BYOL은 음의 예 없는 학습의 실용성을 입증했습니다. 메모리 제약이 있는 환경에서 더 나은 선택지를 제공하며, 비자명한 표현을 학습할 수 있음을 보여주었습니다.

현재 자기지도 학습 커뮤니티는 두 패러다임(대조 vs 비대조)이 공존하고 있으며, BYOL은 그 대표 연구 중 하나입니다.

## 후속 연구 링크

BYOL은 DeepMind 팀의 연구로, Hinton이 직접 저자는 아닙니다. 다만 BYOL이 제기한 "왜 붕괴가 일어나지 않는가?"라는 질문은 자기지도 학습 이론의 핵심 과제로 남아 있습니다. Hinton의 [[A Simple Framework for Contrastive Learning of Visual Representations]]와 [[Big Self-Supervised Models are Strong Semi-Supervised Learners]]가 대조적 접근으로 비교됩니다.

