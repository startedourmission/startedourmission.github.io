---
date: 2026-05-18
tags:
  - 오픈소스
description: "Apache TinkerPop 프로젝트의 그래프 순회 언어. 함수형 체이닝 스타일로 그래프를 단계별로 탐색합니다."
---

Gremlin은 Apache TinkerPop 프로젝트의 그래프 순회(traversal) 언어입니다. 2009년 Marko Rodriguez가 처음 설계했습니다.

[[Cypher]]가 패턴 매칭 기반 선언형이라면, Gremlin은 함수형 체이닝 기반 명령형입니다.

```groovy
g.V().has('name', 'Alice').out('friend').out('friend').dedup()
```

`V()`로 노드를 얻고, `out('friend')`로 친구 노드로 이동하고, 다시 한 번 친구의 친구로 이동하는 식입니다. 단계별 순회를 명시적으로 통제할 수 있어 복잡한 분석에 유리합니다.

[[Amazon Neptune]], JanusGraph, OrientDB 등 TinkerPop 호환 그래프 DB에서 모두 지원됩니다.
