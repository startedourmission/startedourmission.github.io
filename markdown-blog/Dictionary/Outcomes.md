---
date: 2026-06-10
tags:
  - 도구
  - 에이전트
description: "[[Claude Managed Agents]]의 자동 평가 기능. 별도 verifier 서브에이전트가 독립 컨텍스트에서 목표 달성 여부를 검증"
---

[[Claude Managed Agents|CMA]]에서 제공하는 기능으로, 에이전트가 자기 자신의 결과를 판단하는 대신 별도의 검증 서브에이전트(verifier)가 독립적인 컨텍스트 창에서 평가합니다.

## 필요성

모델이 자신의 결과물을 스스로 평가할 때는 편향(self-critique bias)이 발생하기 쉽습니다. Outcomes는 이를 해결하기 위해:

1. 사용자가 정의한 루브릭(체크리스트)을 제공
2. 이를 독립적 컨텍스트의 grader가 검증
3. 모든 기준이 충족되어야만 에이전트 작업 종료

## 성능 효과

[[Parameter Golf]] 벤치마크에서 Outcomes를 통한 검증이 활성화되면 [[Claude Fable 5|Fable 5]]의 루프 효율이 크게 향상됩니다.
