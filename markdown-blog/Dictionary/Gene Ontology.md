---
date: 2026-05-18
tags:
  - 정보
description: "생명과학에서 유전자와 단백질의 기능을 표준화된 어휘로 기술하는 온톨로지. 1998년 시작해 분자생물학·생물정보학의 표준 자원이 됐습니다."
---

Gene Ontology(GO)는 생명과학에서 유전자와 단백질의 기능을 표준화된 어휘로 기술하기 위한 [[온톨로지]]입니다. 1998년 SGD, FlyBase, MGI 세 모델 생물 데이터베이스가 공동 시작했습니다.

세 가지 측면(aspect)으로 구성됩니다.

- **Molecular Function** — 분자 수준의 기능 (예: 인산화 효소 활성)
- **Biological Process** — 큰 생물학적 프로세스 (예: 세포 분열)
- **Cellular Component** — 세포 내 위치 (예: 핵, 미토콘드리아)

각 측면은 DAG(Directed Acyclic Graph) 구조로, `is-a`·`part-of`·`regulates` 등 형식 관계로 개념을 연결합니다. OWL 표현으로 공개되며 [[HermiT]] 같은 [[Reasoner]]로 일관성을 검사합니다.

2026년 기준 약 4만 개 개념을 보유하며, 단백질 데이터베이스(UniProt) 등 거의 모든 생물정보학 자원이 GO 주석(annotation)을 표준 메타데이터로 채택합니다. [[SNOMED CT]]와 함께, 형식 [[온톨로지]]가 산업적으로 정착한 손꼽히는 사례입니다.
