---
date: 2026-06-29
tags:
  - 정보
  - Headliner
  - LLM
  - 에이전트
description: "OpenAI가 GPT-5.6 계열 세 모델을 발표했습니다. Sol(플래그십), Terra(범용), Luna(경량) 구성으로 가격 전략과 에이전트 기능 모두 이전 세대와 다른 방향을 가리킵니다. 미국 정부 게이팅이라는 전례 없는 출시 방식도 주목됩니다."
image: "![[gpt-5-6-sol-terra-luna.png]]"
---

OpenAI가 2026년 6월 26일 GPT-5.6 계열을 공개했습니다. 단일 모델이 아니라 Sol, Terra, Luna 세 개로 나뉜 라인업이고, 출시 방식도 이례적입니다. 약 20개 기업만 미국 정부의 개별 승인을 거쳐 먼저 접근할 수 있었습니다.

## 세 모델의 역할

세 모델은 용도와 가격대를 명확히 나눕니다.

**GPT-5.6 Sol**은 플래그십입니다. 1M 토큰당 입력 $5, 출력 $30입니다. "max"와 "ultra" 두 가지 추론 모드가 있고, ultra 모드는 복잡한 작업을 병렬 서브에이전트에 분산합니다. 코딩, 생물학, 사이버보안 영역에서 에이전트 성능이 특히 강화됐습니다.

**GPT-5.6 Terra**는 일상적 업무에 쓸 수 있는 중간 모델입니다. 1M 토큰당 입력 $2.50, 출력 $15입니다. GPT-5.5 수준의 성능을 약 절반 가격에 제공한다고 OpenAI는 설명합니다.

**GPT-5.6 Luna**는 가장 빠르고 저렴합니다. 1M 토큰당 입력 $1, 출력 $6입니다. 대량의 반복적 작업에 적합합니다.

| 모델 | 입력 (1M) | 출력 (1M) | 포지션 |
|------|-----------|-----------|--------|
| Sol | $5 | $30 | 플래그십 / 에이전트 |
| Terra | $2.50 | $15 | 범용 / 일상 |
| Luna | $1 | $6 | 경량 / 대량 처리 |

## 에이전트 모드: Ultra와 서브에이전트

GPT-5.6 Sol의 가장 눈에 띄는 기능은 "ultra" 모드입니다. 복잡한 요청이 들어오면 하나의 모델이 처리하는 대신 병렬 서브에이전트를 스폰해서 작업을 쪼갭니다. OpenAI가 공개한 코딩 벤치마크 Terminal-Bench 2.1 기준으로, Sol 일반 모드는 88.8%, Sol Ultra는 91.9%를 기록했습니다.

사이버보안 쪽은 더 주목됩니다. OpenAI 내부 CTF(Capture-The-Flag) 평가에서 Sol이 96.7%를 기록했는데, 이 점수는 OpenAI가 자체적으로 설정한 "high" 사이버 위험 임계선을 넘습니다. OpenAI는 이 때문에 강화된 안전 스택을 Sol에 탑재했다고 밝혔습니다. 고위험 요청에 대한 거부 임계치와 반복 오남용 감지 기능이 이전 세대보다 강화됐습니다.

ChatGPT와 Codex도 이번 GPT-5.6 모델로 업그레이드됩니다.

## 기존 세대와의 포지셔닝

GPT-4o와 o3를 어디 두느냐는 OpenAI가 명시하지 않았습니다. 가격 구조만 보면 GPT-5.6 Terra($2.50/$15)는 GPT-5.5 수준을 훨씬 낮은 가격에 가져왔고, Luna($1/$6)는 4o mini 계열이 채우던 자리를 대체할 가능성이 있습니다.

에이전트 태스크에서의 실질적 차이는 Sol에서 나옵니다. 기존 o3가 단일 추론 체인이었다면, Sol Ultra는 서브에이전트 분산 처리를 지원합니다. 긴 코드베이스 분석, 멀티스텝 보안 테스트, 복합 연구 요청처럼 한 번의 컨텍스트 창에 담기 어려운 작업에서 구조적으로 다릅니다.

## 정부 게이팅: 무슨 일이 있었나

이번 출시는 전례 없는 방식으로 이루어졌습니다. 트럼프 행정부가 2026년 6월 2일 행정명령을 통해 연방 기관들이 새 AI 모델을 벤치마킹·평가하는 프로세스를 수립하도록 했고, 이 기반 위에서 Office of the National Cyber Director와 Office of Science and Technology Policy가 OpenAI에 출시 제한을 요청했습니다.

OpenAI는 요청을 받아들여 약 20개 기업에만 정부 개별 승인을 거쳐 먼저 제공했습니다. Sam Altman은 "이것이 장기적인 선호 모델이 아님을 정부에 분명히 했다"며, "미래 출시를 위한 더 지속 가능한 접근법을 업계와 함께 만들어가겠다"고 밝혔습니다.

미국 정부가 AI 회사의 상업 모델 출시를 사전 심사한 첫 사례입니다. 사이버 능력 임계선이 규제 트리거가 됐다는 점에서, 이후 GPT 계열 출시 방식에도 영향을 줄 수 있습니다.

## API 가격과 활용 전략

가격 체계로만 보면, 에이전트 워크플로우를 구축하는 팀은 역할 분담이 명확해집니다.

- **Sol**: 복잡한 추론, 다단계 에이전트 작업, 보안·생물학 특화 태스크
- **Terra**: 문서 처리, 코드 리뷰, 반복 QA처럼 GPT-5.5가 하던 역할
- **Luna**: 분류, 요약, 라우팅처럼 대량으로 돌려야 하는 간단한 작업

Ultra 모드의 서브에이전트는 Sol 가격 기준으로 과금되므로, 복잡한 작업에서 비용이 빠르게 올라갈 수 있습니다. 단순 작업은 Luna로 처리하고 Sol Ultra는 진짜 복합 태스크에만 쓰는 방식이 비용 면에서 합리적입니다.

OpenAI는 일반 출시 시점을 "수 주 내"라고만 밝혔습니다.

---

출처: [OpenAI 공식 발표](https://openai.com/index/previewing-gpt-5-6-sol/), [VentureBeat](https://venturebeat.com/technology/openai-unveils-gpt-5-6-sol-terra-and-luna-models-but-only-accessible-to-limited-preview-partners-for-now-per-us-gov), [TechCrunch](https://techcrunch.com/2026/06/26/openai-limits-gpt-5-6-rollout-after-government-request-says-restrictions-shouldnt-be-the-norm/), [Axios](https://www.axios.com/2026/06/26/openai-gpt-sol-terra-luna-trump)
