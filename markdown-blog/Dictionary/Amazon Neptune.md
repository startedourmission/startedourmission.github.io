---
date: 2026-05-18
tags:
  - 오픈소스
description: "AWS가 제공하는 완전 관리형 그래프 데이터베이스. Property Graph와 RDF를 모두 지원해 Cypher·Gremlin·SPARQL을 모두 쓸 수 있습니다."
---
Amazon Neptune은 AWS가 2018년 GA한 완전 관리형 그래프 데이터베이스입니다.

특징은 두 가지 그래프 모델을 동시에 지원한다는 점입니다.

- **Property Graph** 모델 — [[Gremlin]]과 [[Cypher]] 쿼리
- **RDF** 모델 — [[SPARQL]] 쿼리

같은 클러스터에서 두 모델을 함께 다룰 수 있어, 기존 시맨틱 웹 자산을 가진 조직이 새로 [[Knowledge Graph]]를 도입할 때 마이그레이션 부담이 적습니다.

읽기 복제본 최대 15개, 페타바이트급 스토리지, 자동 백업 등 AWS 관리형 서비스 특성이 그대로 들어갑니다. 사기 탐지, 추천, 지식 그래프, 소셜 네트워킹 워크로드에 주로 사용됩니다.
