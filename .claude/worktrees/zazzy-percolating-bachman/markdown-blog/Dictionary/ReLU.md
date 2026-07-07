---
type: concept
date: 2026-04-10
tags:
  - 딥러닝
aliases: Rectified Linear Unit
image: "![[]]"
description: "음수 입력을 0으로 만들고 양수 입력은 그대로 통과시키는 신경망 활성화 함수"
---

ReLU(Rectified Linear Unit)는 $\text{ReLU}(z) = \max(0, z)$로 정의되는 신경망 활성화 함수입니다. 단순하지만 시그모이드, tanh 대비 기울기 소실 문제를 완화하여 딥러닝의 발전에 핵심 역할을 했습니다.

## 핵심

- 양수 구간에서 기울기가 항상 1이므로 역전파 시 기울기가 소실되지 않습니다
- 계산이 매우 단순합니다 (부호만 확인)
- 음수 입력에 대해 기울기가 0이 되는 "죽은 ReLU(dying ReLU)" 문제가 있습니다
- Leaky ReLU, ELU, GELU 등의 변형이 이 문제를 완화합니다
- LLM에서는 GELU, SiLU 등이 ReLU를 대체하는 추세입니다

## 수식

$$\text{ReLU}(z) = \max(0, z) = \begin{cases} z & z \geq 0 \\ 0 & z < 0 \end{cases}$$
