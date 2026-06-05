---
date: 2026-05-18
tags:
  - LLM
description: "실세계 개체와 관계에 의미를 입힌 그래프 형태의 지식 표현. 구글·위키데이터가 대표 사례이며, LLM 시대에 Graph RAG의 기반으로 다시 주목받고 있습니다."
---

Knowledge Graph(KG)는 실세계의 개체(entity)를 노드로, 의미 있는 관계(relation)를 엣지로 표현한 지식 구조입니다.

용어를 대중화한 것은 [[Google Knowledge Graph]]입니다. 2012년 구글이 "things, not strings"라는 슬로건으로 검색 결과 우측에 등장하는 정보 패널을 선보이면서 KG가 산업적 용어로 자리잡았습니다.

대표 예시:

- **Google Knowledge Graph** — 검색 결과의 정보 박스
- **[[Wikidata]]** — 위키미디어 재단의 공개 KG
- **[[DBpedia]]** — 위키피디아 인포박스에서 추출한 KG
- 기업 내부 KG — 직원·고객·제품 정보 통합

KG와 [[온톨로지]]는 자주 혼동되지만, 엄밀히는 다릅니다. KG는 "사실의 모음"이고, 온톨로지는 "사실 + 사실에서 새로운 사실을 끌어내는 규칙"입니다. KG는 T-Box(스키마)와 A-Box(인스턴스)를 분리하지 않는 경우가 많고, 관계의 domain/range 제약도 느슨하며, [[Reasoner]] 기반 추론을 돌리지 않습니다.

[[LLM]] 시대에 KG는 [[Graph RAG]]의 기반으로 다시 주목받고 있습니다.
