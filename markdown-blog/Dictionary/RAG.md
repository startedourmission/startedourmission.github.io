---
date: 2026-04-10
tags:
  - 정보
  - LLM
aliases: Retrieval-Augmented Generation, 검색 증강 생성
image: "![[]]"
description: "외부 지식 베이스에서 관련 문서를 검색하여 LLM 프롬프트에 삽입해 응답 품질을 높이는 기법"
---

# RAG

RAG(Retrieval-Augmented Generation, 검색 증강 생성)는 LLM이 응답을 생성할 때 외부 지식 베이스에서 관련 문서를 검색하여 프롬프트에 삽입함으로써, 모델의 지식 컷오프를 극복하고 근거 있는 응답을 생성하는 기법이다.

## 핵심

- 바이 인코더(bi-encoder)로 의미 유사도 기반 후보 문서를 검색한다
- 크로스 인코더(cross-encoder)로 재순위화(reranking)하여 품질을 높인다
- 상위 $K$개 문서를 컨텍스트로 LLM 프롬프트에 삽입한다
- 모델 재훈련 없이 최신 정보를 활용할 수 있다
- 검색 품질, 컨텍스트 길이 제한, 청크 전략이 성능을 좌우한다
