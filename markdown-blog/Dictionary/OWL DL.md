---
type: concept
date: 2026-05-18
tags:
  - LLM
  - 추론
description: "W3C OWL 표준의 결정가능한 프로파일. Description Logic을 기반으로 하며 온톨로지 표현력과 추론 효율의 균형점입니다."
---

OWL DL은 W3C의 OWL(Web Ontology Language) 표준에서 정의한 세 프로파일 중 하나입니다.

OWL 1.0은 표현력과 결정가능성의 트레이드오프에 따라 세 단계로 나뉩니다.

- **OWL Lite** — 표현력이 가장 약하나 추론이 가장 단순
- **OWL DL** — [[Description Logic]] 기반, 결정가능, 산업 표준
- **OWL Full** — 표현력 최대, 결정불가능, 자동 추론 어려움

OWL DL은 SHOIN(D) Description Logic에 해당하며, [[HermiT]]·[[Pellet]]·[[FaCT++]] 같은 [[Reasoner]]가 알고리즘적으로 일관성과 추론을 검증할 수 있습니다. 산업 [[온톨로지]]는 거의 모두 OWL DL 또는 그 후속인 OWL 2 DL(SROIQ(D))로 작성됩니다.

DL이라는 이름이 붙은 이유는 결정가능성과 추론 알고리즘이 Description Logic 수학에 직접 대응되기 때문입니다.
