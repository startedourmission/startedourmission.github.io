---
type: concept
date: 2026-05-18
tags:
  - 오픈소스
description: "RDF 데이터를 위한 W3C 표준 쿼리 언어. SQL과 비슷한 문법으로 트리플 패턴을 매칭해 시맨틱 웹·온톨로지 생태계의 사실상 표준입니다."
---

SPARQL은 SPARQL Protocol and RDF Query Language의 약어로, RDF 데이터를 쿼리하기 위한 W3C 표준입니다. 2008년 1.0, 2013년 1.1이 권고안으로 확정됐습니다.

SQL과 유사한 SELECT/WHERE 구조를 갖되, 매칭 대상이 트리플 패턴이라는 점이 다릅니다.

```sparql
SELECT ?person ?name WHERE {
  ?person rdf:type :Researcher .
  ?person :name ?name .
  ?person :affiliatedWith :Stanford .
}
```

[[Wikidata]], [[DBpedia]], [[Gene Ontology]], 유럽 도서관 데이터 등 [[시맨틱 웹]] 기반 공개 데이터셋의 표준 인터페이스입니다. [[온톨로지]] 시스템에서 [[Reasoner]]가 추론한 결과를 조회할 때도 SPARQL을 씁니다.

엔드포인트는 보통 HTTP로 노출되며, Wikidata Query Service 같은 공개 SPARQL 엔드포인트가 대표적입니다.
