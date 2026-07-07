---
type: benchmark
description: "Cursor 엔지니어링 팀의 실제 코딩 세션에서 만든 사내 코딩 에이전트 벤치마크"
tags:
  - 벤치마크
  - AI평가
aliases:
  - CursorBench v3.1
---

# CursorBench

CursorBench는 [[Cursor]] 엔지니어링 팀이 자체 코딩 세션에서 추출한 과제들로 만든 사내 벤치마크입니다. Cursor가 자체 학습시키는 Composer 시리즈 모델을 평가하기 위해 쓰며, 공개된 [[SWE-bench]]·[[Terminal-Bench]]와 함께 모델 발표에 같이 실리는 세 번째 축입니다.

## 만들어진 배경

Composer 2 기술 보고서에 따르면 CursorBench는 *"real coding sessions by our engineering team"* 에서 유래합니다. Cursor 사용자가 실제로 마주치는 상황을 그대로 옮긴 과제입니다.

- 프롬프트가 짧고 모호합니다 (terse and ambiguous)
- 해결에 여러 파일에 걸친 수백 줄의 코드 변경이 필요합니다

이 두 가지 특성이 공개 벤치마크와 결이 다릅니다. SWE-bench는 GitHub 이슈가 출처라 비교적 잘 정제된 문제 설명이 붙고, Terminal-Bench는 환경 검증이 명확한 단일 과제입니다. CursorBench는 *"한두 줄짜리 요구사항으로 큰 변경을 만들어내는"* 실제 IDE 사용 시나리오에 가깝습니다.

## 버전 변천

| 버전 | 등장 시점 | 메모 |
|---|---|---|
| 초기 | Composer 1.5 발표 시 | 구체 수치 비공개 |
| v? | Composer 2 발표 시 | Composer 2가 61.3점 |
| v3.1 (harder tasks) | Composer 2.5 발표 시 | 더 어려운 과제로 재편, Composer 2.5가 63.2% |

v3.1은 명시적으로 *harder tasks* 라벨이 붙어 있습니다. 모델 성능이 빠르게 올라가자 천장을 다시 밀어올린 갱신으로 보입니다. Terminal-Bench가 1.0 → 2.0으로 가면서 89개 과제로 재구성한 것과 비슷한 동기입니다.

## Composer 2.5 발표 시점 수치

| 모델 | CursorBench v3.1 |
|---|---|
| Composer 2.5 | 63.2% |
| Opus 4.7 (max effort) | 64.8% |
| Opus 4.7 (xhigh default) | 61.6% |
| GPT-5.5 (xhigh) | 64.3% |
| GPT-5.5 (medium default) | 59.2% |
| Composer 2 | 52.2% |

Composer 2.5의 default 동작이 Opus 4.7의 max effort 근처에 자리합니다. Composer 2 대비 11%p 향상으로, 같이 공개된 세 벤치 중 가장 큰 폭의 진전입니다.

## 한계와 주의점

- **사내 벤치입니다.** Cursor가 만들고 Cursor가 점수를 보고합니다. 자기 모델에 유리하게 설계됐을 가능성을 완전히 배제할 수 없습니다.
- **재현 어려움.** 과제 자체가 공개되지 않아 외부 연구자가 동일 조건에서 다른 모델을 돌려볼 수 없습니다.
- **상대 비교는 같은 표 안에서만.** 같은 표에 함께 실린 Opus·GPT 수치는 자체 보고치(self-reported)라는 점이 표 각주에 명시되어 있습니다.

다만 Cursor가 Opus 4.7의 default와 max를 같이 보여주고, GPT-5.5의 medium·xhigh를 같이 표시한 점은 비교적 정직한 표시 방식입니다. *"effort에 따라 점수가 갈리니 default끼리 비교하라"* 는 정보를 의도적으로 노출한 것입니다.

## 같이 보면 좋은 항목

- [[SWE-bench]] (Verified / Multilingual / Pro / Multimodal)
- [[Terminal-Bench]]
- [[Cursor]]
