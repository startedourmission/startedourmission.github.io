---
date: 2026-05-18
tags:
  - LLM
description: "온톨로지의 형식 정의로부터 새로운 사실을 자동 도출하는 추론 엔진. HermiT·Pellet·FaCT++가 대표적입니다."
---

Reasoner(추론기)는 [[온톨로지]]의 형식 정의를 입력받아 논리적으로 따라오는 사실을 자동으로 도출하는 도구입니다.

크게 두 역할을 합니다.

- **일관성 검사(consistency checking)** — 정의된 공리들이 서로 모순되지 않는지 검사
- **분류(classification)와 인스턴스 체크(instance check)** — 정의된 규칙으로부터 새 사실 도출

가장 단순한 예 — 하위 클래스 추이성:

```
:Mammal rdfs:subClassOf :Animal .
:Human rdfs:subClassOf :Mammal .
# Reasoner의 결론: :Human rdfs:subClassOf :Animal
```

대표 구현체는 다음 세 가지입니다.

- **[[HermiT]]** — 옥스퍼드 대학교, 자바, OWL 2 DL
- **[[Pellet]]** — Clark & Parsia, 자바, 오픈소스
- **[[FaCT++]]** — 맨체스터 대학교, C++

[[Description Logic]]이 결정가능하기 때문에 Reasoner의 결과는 항상 같은 입력에 같은 출력을 보장합니다. [[LLM]]의 자연어 추론과 결정적으로 다른 지점입니다.

[[Knowledge Graph]]는 Reasoner를 돌리지 않습니다. 이게 KG와 온톨로지를 가르는 진짜 선입니다.
