---
date: 2026-05-18
tags:
  - LLM
description: "1차 술어 논리의 결정가능한 부분집합. 온톨로지의 형식 기반이자 OWL DL의 수학적 토대입니다."
---

Description Logic(DL)은 1차 술어 논리의 결정가능(decidable)한 부분집합으로, [[온톨로지]]의 형식 기반이 되는 논리 체계입니다.

핵심은 세 종류의 어휘로 세상을 기술한다는 점입니다.

- **개념(concept)** — 클래스에 해당. 예: `Person`, `Animal`
- **역할(role)** — 관계에 해당. 예: `hasParent`, `bornIn`
- **개체(individual)** — 인스턴스에 해당. 예: `Alice`, `Berlin`

DL은 표현력과 추론 복잡도의 트레이드오프에 따라 여러 변종이 있습니다. ALC, SHIQ, SROIQ 등 알파벳 조합으로 표기되며, 표현력이 강할수록 추론 비용이 커집니다.

W3C의 OWL 표준은 DL을 직접 채택한 것입니다. [[OWL DL]] 프로파일은 SHOIN(D), OWL 2 DL 프로파일은 SROIQ(D)에 해당합니다.

DL의 결정가능성 덕분에 [[HermiT]], [[Pellet]], [[FaCT++]] 같은 [[Reasoner]]가 일관성 검사와 추론을 알고리즘적으로 수행할 수 있습니다.
