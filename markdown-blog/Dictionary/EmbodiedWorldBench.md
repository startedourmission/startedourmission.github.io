---
type: benchmark
description: Alibaba AMAP CV Lab이 제안한 실행 가능 구현체 AI 벤치마크. UnrealZoo(Unreal Engine 5) 기반 16개 씬, 4단계 난이도, 200개 이상 태스크로 장기 멀티태스크 에이전트를 평가합니다.
tags:
  - 에이전트
  - AI평가
  - 벤치마크
aliases:
  - EWB
---

Alibaba AMAP CV Lab이 [[ABot-AgentOS - A General Robotic Agent OS with Lifelong Multi-modal Memory|ABot-AgentOS]] 논문과 함께 공개한 구현체 에이전트 평가 벤치마크입니다. Unreal Engine 5 기반 UnrealZoo로 실내·실외·하이브리드 16개 실행 가능 씬을 구성하고, 4단계 난이도와 200개 이상 태스크를 제공합니다.

태스크는 형식적으로 $\text{Scenario} = \langle \mathcal{M}, \mathcal{S}_0, \mathcal{O}, \mathcal{N}, \mathcal{C} \rangle$로 정의됩니다. $\mathcal{M}$은 공간 맵, $\mathcal{S}_0$는 초기 상태, $\mathcal{O}$는 관찰 규칙, $\mathcal{N}$은 NPC 행동, $\mathcal{C}$는 성공 기준입니다.

주요 지표:
- **TSR(Task Success Rate)**: 모든 서브태스크와 종료 조건 동시 만족 여부 (엄격)
- **GCR(Goal Completion Rate)**: 달성된 서브태스크 비율 (부분 완료 인정)

에이전트는 필터링된 시멘틱 맵과 자연어 명령만 받으며, NPC 위치나 평가 신호는 노출되지 않습니다. 채점은 실행 트레이스에서 결정론적으로 이뤄져 인간 주관 평가 없이 재현 가능합니다.
