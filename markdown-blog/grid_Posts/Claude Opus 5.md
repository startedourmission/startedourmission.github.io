---
date: 2026-07-28
tags:
  - 정보
  - LLM
  - AI평가
description: "Anthropic이 두 달 새 네 번째 Claude 5 계열 모델을 내놓았습니다. 단가는 Opus 4.8과 같게 두고, low/medium/high 노력 토글로 요청마다 계산량을 사용자가 정하게 했습니다."
image: "![[Claude Opus 5 - 노력 토글과 요청 단위 가격표-thumb.png]]"
---

[[Anthropic]]이 2026년 7월 24일 Claude Opus 5를 출시했습니다. API 모델명은 `claude-opus-5`이고, Claude Max의 새 기본 모델이자 Claude Pro에서 쓸 수 있는 최상위 모델입니다.

숫자부터 정리합니다. 가격은 입력 100만 토큰당 5달러, 출력 100만 토큰당 25달러입니다. [[Opus 4.7]]의 후속인 Opus 4.8과 같은 단가이고, 상위 모델인 [[Claude Fable 5]]의 절반입니다. Fable 5는 입력 10달러, 출력 50달러입니다.

Anthropic이 공개한 13개 벤치마크 비교에서 Opus 5가 Fable 5보다 높은 점수를 낸 항목이 8개입니다. 절반 가격 모델이 상위 모델을 대부분의 항목에서 이겼다는 뜻입니다.

## 노력 토글

이번 출시의 실질적 변화는 벤치마크 숫자가 아니라 effort 파라미터입니다. low, medium, high, xhigh, max 중에서 모델이 한 요청에 얼마나 계산을 쓸지 사용자가 고릅니다. API 기본값은 high입니다.

지금까지 추론 예산은 모델 티어를 고르는 것으로만 조절됐습니다. 가벼운 작업은 Haiku, 무거운 작업은 Opus, 이런 식입니다. 그런데 같은 모델 안에서 계산량을 다이얼로 돌린다는 것은 가격표가 모델 단위에서 요청 단위로 내려왔다는 뜻입니다.

그러면 "어떤 요청에 high를 쓸 것인가"가 애플리케이션 설계 문제가 됩니다. 토큰 단가만 보고 비용을 예측할 수 없게 됩니다. 트래픽의 80%를 low나 medium으로 흘리고 어려운 20%만 high로 올리는 팀은 표에 적힌 단가보다 훨씬 적게 씁니다.

실무에서 이 결정을 하려면 라우팅 기준이 필요합니다. 요청 길이나 도구 호출 횟수 같은 정적 신호로 나눌 수도 있고, low로 먼저 시도한 뒤 검증에 실패하면 high로 재시도하는 에스컬레이션 구조를 짤 수도 있습니다. 후자는 지연이 두 배가 될 수 있으니 실패율이 낮은 도메인에서만 쓸 만합니다.

fast mode도 함께 제공됩니다. 비용은 두 배이고 속도는 약 2.5배입니다. effort와 fast mode를 조합하면 비용, 지연, 품질 세 축에서 요청마다 다른 지점을 고를 수 있습니다.

## 벤치마크

공개된 수치 몇 가지입니다.

| 항목 | Opus 5 | 비교 |
| --- | --- | --- |
| Frontier-Bench v0.1 | 43.3% (최대 노력) | Fable 5 33.7% |
| 13개 벤치마크 승패 | 8승 | Fable 5 대비 |
| ARC-AGI 3 | 차순위 모델의 3배 | |
| Zapier AutomationBench | 최고 경쟁자 대비 1.5배 통과율 | 최저 노력에서도 전 모델 상회 |

Zapier AutomationBench 결과에서 최저 노력 설정으로도 다른 모든 모델을 앞섰다는 대목이 눈에 띕니다. 노력 토글이 마케팅용 옵션이 아니라 실제 성능 곡선을 만든다는 근거입니다. 다만 이 수치들은 Anthropic이 선택한 벤치마크 조합이라는 점은 감안해야 합니다.

## 티어 구분의 축이 바뀌었습니다

Fable 5는 Anthropic의 프런티어 모델입니다. 그 아래 티어인 Opus 5가 절반 가격에 13개 중 8개를 이겼다면, 티어를 나누는 기준이 더 이상 순수 성능이 아니라는 이야기가 됩니다.

그럼 무엇이 남을까요. 컨텍스트 길이, 안전 프로파일, 특정 도메인 최적화, 그리고 가장 현실적으로는 최고 난이도 구간에서의 신뢰도입니다. 평균 성능은 뒤집혔어도 어려운 꼬리에서는 상위 모델이 여전히 앞설 수 있습니다. Frontier-Bench에서 Opus 5가 43.3%로 Fable 5의 33.7%를 앞선 것을 보면 그 설명도 완전하지는 않습니다.

Opus 5는 두 달이 채 안 되는 기간에 나온 네 번째 Claude 5 계열 모델입니다. 대형 출시 한 번에 몰아넣던 방식에서 능력과 비용과 속도를 각각 빠르게 개선하는 방식으로 배포 리듬이 옮겨갔다는 신호입니다.

볼트에 있는 [[Claude Opus 4.8에서 Fable 5로 마이그레이션하기]] 글의 전제도 이 출시로 다시 볼 필요가 있습니다. 그 글은 상위 티어로 올라가는 것이 성능 문제의 답이라는 구도를 깔고 있는데, 지금은 같은 티어 안에서 effort를 올리는 선택지가 생겼습니다.

## 정리

가격표가 모델 단위에서 요청 단위로 내려왔습니다. 이제 비용 최적화는 어떤 모델을 쓸지 고르는 문제가 아니라, 어떤 요청에 얼마나 쓸지 라우팅하는 문제입니다. 여기서 나오는 절감폭이 모델을 한 단계 낮추는 것보다 클 수 있습니다.

출처는 Anthropic 공식 발표(2026-07-24)와 [Axios](https://www.axios.com/2026/07/24/anthropic-releases-new-model-opus-5), [TechCrunch](https://techcrunch.com/2026/07/24/anthropic-launches-opus-5/), [Fortune](https://fortune.com/2026/07/24/anthropic-debuts-claude-opus-5-with-feature-that-lets-users-toggle-between-cost-and-capability/), [SiliconANGLE](https://siliconangle.com/2026/07/24/anthropic-launches-claude-opus-5-efficiency-safety-improvements/) 보도입니다.
