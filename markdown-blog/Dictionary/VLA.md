---
type: concept
description: Vision-Language-Action. 카메라 뷰와 자연어 지시를 받아 로봇 액션을 직접 출력하는 정책 모델 계열
tags:
  - 멀티모달
  - 에이전트
aliases:
  - Vision-Language-Action
  - Vision Language Action
---

Vision-Language-Action의 약자입니다. 사전학습된 비전-언어 백본에서 파인튜닝해 카메라 뷰와 자연어 지시를 받고 로봇 액션 청크를 출력하는 정책 모델 계열을 가리킵니다.

계보는 액션 청크와 생성형 시각운동 아키텍처에서 출발합니다. ACT가 시간적으로 일관된 액션 청크를 예측했고, Diffusion Policy가 반복 디노이징으로 다봉 액션 시퀀스를 모델링했습니다. RT-1이 실세계 제어용 트랜스포머 정책을 규모 있게 세웠고, RT-2가 인터넷 사전학습 비전-언어 표현을 로봇 제어에 연결했습니다.

액션 생성 방식으로 두 갈래가 갈립니다. OpenVLA처럼 자기회귀 액션 토큰을 쓰면 언어모델 인터페이스를 재사용하고 사전학습 백본과 함께 자연스럽게 확장됩니다. $\pi_0$와 $\pi_{0.5}$처럼 플로우 매칭으로 연속 액션 청크를 생성하면 저수준 명령을 연속 공간에서 직접 모델링하고 서로 다른 유효 액션 시퀀스를 여러 개 담을 수 있습니다.

관측 공간이 카메라·언어·로봇 상태에 머물러 접촉과 미끄러짐이 간접적으로만 관측된다는 것이 이 계열의 공통 약점입니다. [[N0-VTLA - Scaling Vision-Tactile-Language-Action Model with Latent Tactile Tokens]]가 여기에 촉각 경로를 더한 사례입니다.
