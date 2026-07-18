---
date: 2026-07-02
tags:
  - 정보
  - LLM
  - 에이전트
description: "Anthropic이 Sonnet 5를 전면 출시 — SWE-bench Pro 63.2%, OSWorld 83.4% 등 Opus 4.8에 근접하는 에이전틱 성능을 Sonnet 가격에 제공하지만 에이전틱 작업 시 토큰 소모가 기존 대비 더 많아 '저렴한 에이전트'라는 말을 액면 그대로 받아들이기 어렵습니다."
---

> 이 글은 [Anthropic 공식 발표](https://www.anthropic.com/news/claude-sonnet-5), [TechCrunch](https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/), [MarkTechPost](https://www.marktechpost.com/2026/06/30/anthropic-claude-sonnet-5-vs-sonnet-4-6-vs-opus-4-8-agentic-coding-benchmarks-api-pricing-and-cost-performance-tradeoffs-compared/) 를 참고하여 작성했습니다.

Anthropic이 2026년 6월 30일 Claude Sonnet 5를 출시했습니다. Free와 Pro 플랜의 기본 모델로 즉시 전환됐고, Max·Team·Enterprise에서도 이용할 수 있습니다. 홍보 메시지는 명확합니다. "Opus 4.8에 근접한 에이전틱 성능을, Sonnet 가격에." 그런데 이 문장을 해석하려면 숫자를 하나씩 들여다봐야 합니다.

## 벤치마크

Sonnet 5는 Sonnet 4.6 대비 모든 공개 벤치마크에서 앞섭니다.

| 벤치마크 | Sonnet 5 | Opus 4.8 | Sonnet 4.6 |
|---------|---------|---------|----------|
| SWE-bench Pro (에이전틱 코딩) | 63.2% | **69.2%** | 58.1% |
| OSWorld-Verified (컴퓨터 사용) | 81.2% | **83.4%** | -- |
| GDPval-AA v2 Elo (지식 작업) | **1,618** | 1,615 | -- |

에이전틱 코딩(SWE-bench Pro)에서 Opus 4.8과의 격차는 6%p입니다. 지식 작업 Elo에서는 Sonnet 5(1,618)가 Opus 4.8(1,615)을 오히려 소폭 앞섭니다. Anthropic이 내세운 "근접"은 수치 기준으로는 사실입니다.

한 가지 더 있습니다. Sonnet 5에는 다섯 가지 effort 레벨이 있습니다(low / medium / high / max / x-high). x-high 설정에서 Sonnet 5는 Opus 4.8의 medium~high effort와 OSWorld·BrowseComp 결과가 거의 같아집니다. effort 레벨이 높을수록 모델이 더 많은 thinking budget을 할당하고, 그만큼 출력 토큰이 늘어납니다.

## 가격과 실제 비용

표시 단가를 먼저 봅니다.

| 모델 | 입력 ($/M) | 출력 ($/M) | 기간 |
|-----|-----------|-----------|------|
| Sonnet 5 (프로모션) | $2 | $10 | ~2026-08-31 |
| Sonnet 5 (표준) | $3 | $15 | 2026-09~ |
| Opus 4.8 | $5 | $25 | -- |

표준 단가 기준으로 Sonnet 5는 Opus 4.8보다 입력 40%, 출력 40% 저렴합니다. 여기까지는 마케팅 설명과 일치합니다.

**문제는 토크나이저입니다.** Sonnet 5는 새 토크나이저를 탑재했고, 동일한 텍스트가 콘텐츠 유형에 따라 기존 대비 최대 1.35배 더 많은 토큰으로 변환됩니다. Anthropic은 "Sonnet 4.6에서 Sonnet 5로의 전환이 '대략 비용 중립'이 되도록 프로모션 가격을 설정했다"고 밝혔습니다. 즉, $2/$10 프로모션 기간에는 같은 작업을 Sonnet 4.6과 비슷한 비용으로 처리할 수 있지만, 9월부터 $3/$15로 전환되면 이야기가 달라집니다.

에이전틱 작업에서는 추가 변수가 있습니다. 에이전트가 도구를 반복 호출하고 결과를 맥락에 쌓아가는 방식으로 동작하면, 출력 토큰이 단순 채팅보다 훨씬 많이 발생합니다. effort 레벨을 높일수록 thinking 과정의 토큰도 늘어납니다. 표시 단가만으로 비용을 추정하면 실제 청구서와 차이가 납니다.

요약하면, "Opus 4.8의 성능을 훨씬 저렴하게" 쓰려면:

1. **벤치마크 기준 성능 차이(6%p)를 감수해야 하거나, effort를 x-high로 올려야 합니다.** x-high는 medium보다 토큰이 많이 나옵니다.
2. **프로모션 가격($2/$10)이 8월에 끝나면** 새 토크나이저 영향과 합산해 Sonnet 4.6 대비 비용이 올라갈 수 있습니다.
3. **Opus 4.8과 직접 비교할 때** 단가 격차는 실제로 상당합니다. 단가만으로는 Sonnet 5가 명백히 저렴합니다. 다만 같은 태스크에서 Opus 4.8이 더 적은 턴에 끝낸다면, 실효 비용 차이는 좁혀집니다.

## 모델 계층 재편

Anthropic의 모델 라인업은 Haiku(경량) - Sonnet(중간) - Opus(최고) 구조입니다. 이번 출시로 Sonnet이 Free/Pro 기본값이 됐습니다. 수천만 명의 사용자가 이전 Sonnet 4.6 대신 Sonnet 5를 쓰게 됩니다.

이는 Opus를 어떤 위치에 두려는 전략인지를 보여줍니다. Sonnet 5가 대부분의 작업을 충분히 처리하게 되면, Opus는 진짜 고난이도 작업(장기 연구, 복잡한 추론 체인)에만 쓰이는 구조가 됩니다. Anthropic 입장에서는 API 매출과 사용자 만족도를 동시에 관리하면서 Opus의 고부가가치 포지션을 유지할 수 있습니다.

## Fable 5와의 비교

동시에 Anthropic의 최신 모델인 [[Fable 5]]는 6월 23일부터 구독 무료 범위에서 제외됐습니다(입력 $10/M, 출력 $50/M). Sonnet 5가 기본값으로 올라선 것과 Fable 5가 유료로 전환된 것은 같은 논리의 두 면입니다. 용량 제약 속에서 프런티어 모델을 고가격·저접근 구조로 유지하고, 중간 모델로 대량 수요를 흡수하는 방식입니다.

## 결론

Sonnet 5는 기존 Sonnet 4.6보다 분명히 능력이 높고, Opus 4.8에 상당히 근접했습니다. 단순 채팅이나 짧은 작업에서는 실제로 Opus 4.8 없이도 충분할 수 있습니다.

에이전틱 파이프라인을 운영하는 경우는 달리 봐야 합니다. 새 토크나이저의 팽창, effort 레벨별 토큰 소비, 9월 가격 인상을 고려한 실측 비용 계산이 필요합니다. "저렴하게 Opus 수준으로"라는 메시지는 특정 조건에서만 성립합니다.

---

이 글은 [Anthropic 공식 발표](https://www.anthropic.com/news/claude-sonnet-5)와 [TechCrunch](https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/) 의 관점에서 작성되었습니다. 핵심 긴장 -- 단가 인하 vs 토크나이저 팽창 + effort 레벨 비용 -- 은 9월 이후 실측 데이터가 나오면 더 명확하게 판단할 수 있을 것입니다.
