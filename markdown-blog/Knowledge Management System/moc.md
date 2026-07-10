---
date: 2026-07-08
tags:
  - 정보
  - LLM
  - KMS
  - MOC
description: "LLM Wiki부터 GraphRAG, 온톨로지, Agent Memory까지. KMS 시리즈 13편을 [KMS-01]~[KMS-13]으로 정리한 목차입니다."
---

LLM에게 개인·팀·조직의 맥락을 이해시키는 방법을 다루는 시리즈입니다. 마크다운 파일 몇 개로 시작하는 개인용 LLM Wiki부터, 그래프 기반 검색, 온톨로지, 에이전트 메모리까지 규모가 커질수록 필요한 구조가 달라집니다. 관심 있는 지점부터 읽으면 됩니다.

## Part 1. LLM Wiki의 시작

- **KMS-01** [[Andrej Karpathy의 LLM Knowledge Base 워크플로우\|안드레이 카파시의 LLM 지식 베이스 워크플로우]]: 카파시 원문 스레드 요약. 원본 수집 → 위키 컴파일 → Q&A → 출력 → 린팅까지 6단계 워크플로우
- **KMS-02** [[Karpathy LLM Wiki - 개인 지식을 AI와 공유하는 새로운 방법\|카파시 LLM Wiki - 개인 지식을 AI와 공유하는 새로운 방법]]: LLM Wiki 개념 소개, 외부 기억으로서의 정의, 실제 도입 사례와 한계
- **KMS-03** [[LLM Wiki는 왜 무너지는가 - 4가지 붕괴 모드]]: 인식론적 필터·지식 생애주기·엔트로피 역전·접지 검증, 4가지 구조적 결함과 대응법

## Part 2. 규모별 확장 (GraphRAG·온톨로지·Agent Memory)

- **KMS-04** [[온톨로지, Knowledge Graph, Graph RAG]]: 그래프·그래프 DB·Knowledge Graph·온톨로지·Graph RAG·Second Brain 용어 정리
- **KMS-05** [[HyGRAG - 단순 벡터 검색이 놓치는 것]]: 청크와 엔티티를 함께 다루는 하이브리드 그래프로 멀티홉 추론 정확도 개선
- **KMS-06** [[Databricks Genie Ontology - RAG를 넘어선 엔터프라이즈 지식 레이어]]: 자동 지식 추출과 OntoRank 권위성 결정으로 조직 규모 지식 관리를 자동화
- **KMS-07** [[Open Knowledge Format - AI 에이전트를 위한 데이터 공유 표준]]: Google Cloud가 공개한 마크다운·YAML 기반 데이터 카탈로그 개방형 표준
- **KMS-08** [[Agent Memory - 에이전트가 기억하는 7가지 방법]]: 대화형·의미형·에피소딕 등 7가지 메모리 유형과 LLM Wiki·mem0의 위치
- **KMS-09** [[지식 관리의 방법]]: 규모·도메인 안정성·질문 복잡도·자동화 필요도 기준으로 방법론을 고르는 선택 가이드

HyGRAG 논문 전문 리뷰는 [[HyGRAG - A Unified Framework for Context-Aware and Relation-Aware Graph Retrieval-Augmented Generation]]에 있습니다.

## Part 3. 실전 구축 (Obsidian과 Claude)

- **KMS-10** [[하네스 옵시디언 LLM 위키 - 블로그]]: Claude Code 하네스 개념, 옵시디언이 적합한 이유, 구축 4단계
- **KMS-11** [[옵시디언을 구조화하는 세 가지 방법]]: 온톨로지 구조·자동 흐름 구조·출력 연결 구조, 목적에 따라 갈리는 세 방향 비교
- **KMS-12** [[Claude와 옵시디언으로 만드는 자동 지식 볼트]]: 캡처·파이프라인·옵시디언·Claude 4개 레이어로 매일 아침 브리핑이 도착하는 구조
- **KMS-13** [[Obsidian Skill과 LLM Wiki 정리\|옵시디언 스킬과 LLM Wiki 정리]]: 공식 옵시디언 스킬 5종과 LLM Wiki 패턴을 결합해 Claude가 볼트를 직접 운영하게 만들기
