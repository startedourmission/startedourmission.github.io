---
type: benchmark
description: "미국 수학 올림피아드 수학 추론 벤치마크"
tags:
  - 벤치마크
  - AI평가
  - 정보
aliases:
  - United States of America Mathematical Olympiad
---

# USAMO

USAMO(United States of America Mathematical Olympiad)는 미국 수학 올림피아드 문제를 활용한 수학 추론 벤치마크다. 고등학교 및 대학 수준의 수학 경시대회 문제 중에서도 최고 난도에 해당하며, 증명 기반의 심층적 수학 추론 능력을 평가한다.

## 구성

USAMO 문제는 대수, 조합론, 기하, 정수론 등 다양한 수학 분야에서 출제된다. 단답형이 아닌 서술형 증명을 요구하는 것이 특징이다.

## 평가 방식

MathArena 방법론을 사용하여 평가한다. 각 문제당 10회 시도를 허용하며, 모델이 생성한 풀이의 정확성을 판정하는 구조다. MathArena는 수학 경시대회 문제에 특화된 자동 평가 프레임워크로, 인간 채점 기준과 높은 일치도를 보인다.

## Mythos 시스템 카드 주요 수치

| 모델 | 정확도 |
| --- | --- |
| **Mythos** | **97.6%** |
| GPT-5.4 | 95.2% |
| Gemini 3.1 Pro | 74.4% |
| Opus 4.6 | 42.3% |

USAMO에서 모델 간 성능 차이가 극명하게 드러난다. Mythos는 97.6%로 거의 완벽에 가까운 점수를 기록한 반면, Opus 4.6은 42.3%에 그쳤다. 이는 수학 추론 능력에서 세대 간 격차가 매우 크다는 것을 의미한다. GPT-5.4도 95.2%로 높은 성능을 보였지만, Gemini 3.1 Pro는 74.4%로 상대적으로 낮은 편이다.
