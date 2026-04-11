---
date: 2026-04-10
tags:
  - 정보
  - 딥러닝
aliases: 장단기 기억 네트워크, Long Short-Term Memory
image: "![[]]"
description: "게이트 메커니즘으로 장거리 의존성 문제를 해결한 RNN의 개선 모델"
---

# LSTM

LSTM(Long Short-Term Memory, 장단기 기억 네트워크)은 망각 게이트(forget gate), 입력 게이트(input gate), 출력 게이트(output gate)를 추가하여 장거리 의존성 문제를 해결한 RNN의 개선 버전이다.

## 핵심

- 셀 상태(cell state) $C_t$가 정보를 장기간 유지하는 "메모리 벨트" 역할을 한다
- 망각 게이트: 이전 셀 상태의 어떤 정보를 지울지 결정
- 입력 게이트: 새로운 정보를 얼마나 저장할지 결정
- 출력 게이트: 셀 상태에서 어떤 정보를 출력할지 결정
- 바닐라 RNN보다 훨씬 긴 시퀀스의 의존성을 포착할 수 있다

## 수식

$f_t = \sigma(W_f[h_{t-1}, x_t] + b_f)$ (망각 게이트)

$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ (셀 상태 업데이트)

## 등장하는 강의

- [[1장 - 트랜스포머]] (CME295)
