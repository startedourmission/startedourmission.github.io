---
type: benchmark
description: "초등 과학 객관식 추론 벤치마크"
tags:
  - 벤치마크
  - AI평가
  - 정보
aliases:
  - AI2 Reasoning Challenge
  - ARC-Easy
  - ARC-Challenge
---

# ARC

ARC(AI2 Reasoning Challenge)는 2018년 Allen Institute for AI가 공개한 초등 과학 추론 벤치마크다. 미국 초등~중학교 과학 시험 문제에서 뽑은 4지선다 문항으로 구성된다. 추상 추론 퍼즐인 [[ARC-AGI-2]]와는 다른 벤치마크다.

## 구성

- **ARC-Easy**: 5,197문항. 문장 검색이나 단순 추론으로 풀 수 있는 쉬운 문제.
- **ARC-Challenge**: 2,590문항. 검색·단어 매칭 기반 모델이 틀렸던 어려운 문제만 선별.

총 약 7,800문항으로 모두 4지선다다.

## 평가 방식

표준 객관식 정확도. 과학 지식과 기본 추론을 함께 요구한다.

## 포화 상태

ARC-Easy는 일찌감치 포화됐고, ARC-Challenge도 2023년 이후 프론티어 모델이 95% 이상으로 상단을 채웠다. 2026년 기준 변별력은 거의 없다.

## 의의

AI2가 "검색만으론 풀 수 없는" 과학 추론 문제를 표준화한 초기 시도로, 이후 [[GPQA Diamond]]처럼 "Google-proof"를 설계 원칙으로 삼는 벤치마크의 계보를 열었다.
