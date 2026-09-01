---
ready: true
type: ai-model
description: 구글이 공개한 3B 규모 오픈 비전-언어 모델. 전이(transfer)를 목표로 설계돼 로봇 정책 백본으로 자주 쓰입니다
tags:
  - 멀티모달
  - 오픈소스
---

구글이 공개한 3B 규모의 오픈 비전-언어 모델입니다. 논문 부제가 "A versatile 3B VLM for transfer"인 데서 드러나듯, 그 자체로 최고 성능을 내는 것보다 다양한 다운스트림 과제로 옮겨 붙이기 좋게 만드는 것을 목표로 설계됐습니다.

크기가 적당하고 라이선스가 열려 있어 로봇 정책의 비전-언어 백본으로 널리 채택됐습니다. [[VLA]] 계열에서 $\pi_0$와 $\pi_{0.5}$가 PaliGemma 위에 플로우 매칭 액션 전문가를 붙이는 구조를 씁니다. [[N0-VTLA - Scaling Vision-Tactile-Language-Action Model with Latent Tactile Tokens]]도 이 조합을 그대로 상속합니다.
