---
date: 2026-04-10
tags:
  - 정보
  - LLM
aliases: Rotary Position Embeddings
image: "![[]]"
description: "토큰 쌍 간의 상대 위치를 회전 행렬로 어텐션에 직접 반영하는 위치 인코딩 방법"
---

# RoPE

RoPE(Rotary Position Embeddings)는 토큰의 위치 정보를 임베딩에 더하는 대신, 쿼리와 키 벡터에 회전 행렬을 적용하여 토큰 쌍 간의 상대 위치 거리가 내적에 자연스럽게 반영되게 하는 위치 인코딩 방법이다.

## 핵심

- 절대 위치가 아닌 상대 위치를 어텐션 계산 내부에서 직접 반영한다
- $\text{dot}(R_m q, R_n k) = \text{dot}(q, R_{n-m}k)$: 두 토큰의 내적이 상대 위치 $(n-m)$에만 의존한다
- 긴 시퀀스 일반화(extrapolation)와 훈련 컨텍스트 이상 확장에 유리하다
- LLaMA, Mistral, Gemma 등 현대 LLM의 표준 위치 인코딩이 되었다
- 이미지 분야에서 2D RoPE로 확장되어 패치 위치 인코딩에도 사용된다

## 수식

$$\text{RoPE}(q, m) = R_m q = \begin{pmatrix}\cos m\theta \\ \sin m\theta\end{pmatrix} \otimes q \text{ (per 2D block)}$$
