---
type: tool
date: 2026-08-28
tags:
  - 도구
  - 오픈소스
description: "GraphBLAS 기반 희소 인접 행렬로 그래프를 표현해 순회를 선형대수 연산으로 처리하는 그래프 데이터베이스. RedisGraph의 후속작이며 GraphRAG 전용 설계를 표방합니다."
---

FalkorDB는 [[Redis]]가 2023년 RedisGraph 모듈을 단종하면서 그 뒤를 이어 나온 그래프 데이터베이스입니다. 2026년 C에서 Rust로 재작성됐습니다.

가장 큰 차이는 그래프를 저장하고 순회하는 방식입니다. [[Neo4j]]를 포함한 대부분의 그래프 DB는 노드가 이웃 노드를 가리키는 포인터를 따라가며 순회하는 pointer-chasing 방식을 씁니다. FalkorDB는 그래프를 희소 인접 행렬(sparse adjacency matrix)로 표현하고, GraphBLAS(희소 행렬 연산 표준 API)를 통해 순회를 행렬 곱셈으로 처리합니다. 개별 엣지를 하나씩 따라가는 대신 CPU 코어 전반에 걸쳐 병렬로 행렬 연산을 수행하는 방식입니다.

OpenCypher 쿼리를 지원하며 [[Graph RAG]] 구현을 표방 목적으로 내세웁니다. 라이선스는 Server Side Public License v1(SSPLv1)입니다.
