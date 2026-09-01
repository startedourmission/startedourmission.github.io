---
ready: true
type: concept
description: Joint-Embedding Predictive Architecture. 원 감각 신호를 재구성하는 대신 학습된 잠재 공간에서 예측하는 자기지도 학습 원리
tags:
  - 딥러닝
  - 컴퓨터비전
aliases:
  - Joint-Embedding Predictive Architecture
---

Joint-Embedding Predictive Architecture의 약자입니다. 마스킹된 픽셀을 그대로 복원하는 대신, 학습된 잠재 공간에서 목표 표현을 예측하도록 학습시키는 자기지도 원리입니다.

핵심 논지는 재구성이 잘못된 목표라는 것입니다. 픽셀 단위 복원은 예측 불가능한 세부(질감 노이즈, 정확한 화소값)까지 맞추라고 요구해 용량을 낭비합니다. 잠재 공간에서 예측하면 예측 가능한 구조만 남기고 나머지는 표현이 알아서 버립니다.

계보는 이미지의 I-JEPA에서 시작해 영상의 V-JEPA와 V-JEPA 2로 이어집니다. LeJEPA는 휴리스틱 없이 증명 가능하고 확장 가능한 형태를 다뤘고, LeWorldModel은 이 원리를 픽셀 기반 잠재 월드 모델링에 적용했습니다.

이 원리는 시각 밖으로도 옮겨집니다. [[N0-VTLA - Scaling Vision-Tactile-Language-Action Model with Latent Tactile Tokens]]는 촉각 신호를 재구성하지 않고 다가올 접촉 변화의 잠재 표현을 예측 목표로 삼는데, 논문 본문이 자기 위치를 JEPA 계보 안에서 잡습니다.
