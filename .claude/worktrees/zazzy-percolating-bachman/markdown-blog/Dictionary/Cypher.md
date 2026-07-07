---
type: concept
date: 2026-05-18
tags:
  - 오픈소스
description: "Neo4j가 만든 그래프 쿼리 언어. ASCII 아트 형태로 노드와 관계를 표현해 가독성이 높고, 현재는 openCypher·GQL 표준의 기반이 됩니다."
---

Cypher는 [[Neo4j]]가 2011년 도입한 선언형 그래프 쿼리 언어입니다.

특징은 ASCII 아트로 그래프 패턴을 표현한다는 점입니다. `(a)-[:FRIEND]->(b)` 같은 식으로 노드와 관계를 직관적으로 적습니다. [[SPARQL]]이나 [[Gremlin]]보다 진입 장벽이 낮아 빠르게 확산됐습니다.

```cypher
MATCH (p:Person {name: "Alice"})-[:FRIEND*1..3]-(friend)
RETURN friend
```

2015년 Neo4j가 openCypher 프로젝트로 표준화를 추진했고, 이는 2023년 ISO 표준 그래프 쿼리 언어인 GQL의 기반이 됐습니다. SAP HANA, Memgraph, [[Amazon Neptune]] 등 여러 그래프 DB가 Cypher 또는 그 변형을 지원합니다.
