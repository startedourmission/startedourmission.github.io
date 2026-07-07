---
type: concept
date: 2026-04-10
tags:
  - 머신러닝
aliases: Expectation-Maximization
image: "![[]]"
description: "잠재 변수가 있는 모델에서 최대 우도 추정을 반복적으로 수행하는 알고리즘"
---

EM 알고리즘(Expectation-Maximization Algorithm)은 잠재 변수(latent variable)가 있는 확률 모델에서 최대 우도 추정을 수행하기 위해, 기댓값 계산(E-step)과 최대화(M-step)를 반복하는 알고리즘입니다.

## 핵심

- **E-step**: 현재 매개변수로 잠재 변수의 사후 분포를 계산합니다
- **M-step**: E-step에서 계산한 기댓값으로 매개변수를 최대화합니다
- 각 반복에서 우도가 증가하거나 유지됨이 보장됩니다 (수렴 보장)
- 가우시안 혼합 모델, 인자 분석 등의 학습에 사용됩니다
- 지역 최적값에 수렴할 수 있어 초기값에 민감합니다

## 수식

E-step: $Q(\theta, \theta^{(t)}) = \mathbb{E}_{z|x;\theta^{(t)}}[\log p(x,z;\theta)]$

M-step: $\theta^{(t+1)} = \arg\max_\theta Q(\theta, \theta^{(t)})$
