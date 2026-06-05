---
type: hardware
description: "SambaNova Reconfigurable Dataflow Unit, 엔터프라이즈 추론"
tags:
  - 벤치마크
  - AI평가
  - 커스텀칩
aliases:
  - "SN40L"
  - "RDU"
---

SambaNova SN40L은 SambaNova Systems가 개발한 Reconfigurable Dataflow Unit(RDU) 기반의 AI 가속기이다. 엔터프라이즈 환경에서의 대규모 모델 추론에 특화되어 있다.

## 주요 사양

- **아키텍처**: Reconfigurable Dataflow Unit (RDU)
- **405B 모델 추론**: 16칩으로 100+ tok/s
- **지원 정밀도**: bf16/fp32 혼합 정밀도
- **최적화 대상**: 엔터프라이즈 추론

## 특징

[[Cerebras WSE-3]], [[Groq LPU]]와 함께 비GPU 추론 아키텍처를 대표한다. SN40L의 RDU 아키텍처는 데이터 흐름(dataflow)을 하드웨어 수준에서 재구성할 수 있는 구조이다. 이는 모델의 연산 그래프에 맞춰 하드웨어 자원을 동적으로 최적화할 수 있다는 의미이며, 고정된 구조의 GPU 대비 특정 워크로드에서 더 높은 효율을 달성한다.

405B 파라미터 규모의 모델을 16개 칩만으로 100 tok/s 이상의 속도로 추론할 수 있다는 점이 주목할 만하다. bf16과 fp32의 혼합 정밀도를 지원하여 정밀도와 성능 사이의 균형을 유연하게 조절할 수 있다. 엔터프라이즈 고객을 대상으로 턴키(turnkey) 솔루션 형태로 제공되며, 금융, 의료, 통신 등 산업별 AI 추론 수요에 대응한다.
