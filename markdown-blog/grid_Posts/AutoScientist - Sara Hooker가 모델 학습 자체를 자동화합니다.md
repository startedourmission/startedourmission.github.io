---
date: 2026-05-15
tags:
  - 정보
  - 머신러닝
  - AI평가
description: "전 Cohere VP of Research [[사라 후커]]가 공동창업한 Adaption Labs가 첫 제품 AutoScientist를 공개했습니다. 모델 학습·정렬 전체 research loop을 자동화하는 시스템으로, 데이터 큐레이션과 학습 recipe를 동시에 self-improve 합니다. 사내 AI 리서처가 직접 설정한 학습 대비 평균 +35%, win rate는 48%에서 64%로 올랐다고 합니다. 첫 30일 무료, $50M 시드 (Emergence Capital + Mozilla Ventures 리드)."
---
2026년 5월 13일, [Adaption Labs](https://adaptionlabs.ai)가 첫 제품 [AutoScientist](https://www.adaptionlabs.ai/blog/autoscientist)를 공개했습니다. 한 줄 요약: *모델 학습·정렬을 위한 사람의 의사결정 — 데이터 큐레이션, 학습 recipe, 평가 — 을 통째로 자동화하는 시스템*.

이걸 만든 사람이 누구냐가 중요합니다. CEO [[사라 후커]]는 *Cohere For AI* 를 이끌었던 전 Cohere VP of Research이고, 작은 모델로 큰 효율을 내는 *"scaling race에 반대"* 노선의 학계 대표자 중 한 명입니다. 공동창업자 Sudip Roy는 전 Cohere inference director입니다. *프론티어 랩의 학습 노하우를 외부 도구로 옮기는* 작업을 두 사람이 회사로 만든 것이죠.

## 무엇이 새로운가요

AutoScientist의 주장은 단순합니다 — *fine-tuning을 사람이 운영하는 시대를 끝낸다*. 구체적으로 자동화되는 의사결정은 세 갈래입니다.

**1. 적응형 데이터 (adaptive data)** — AI 시스템이 *답을 내는 데 필요한 데이터를 실시간으로 생성·조작* 합니다. 기존 패러다임은 *고정된 데이터셋 → 학습* 이었다면, AutoScientist는 *문제에 필요한 데이터를 모델이 직접 생성·정제* 합니다. 합성 데이터 + 정제가 *학습과 동시에* 굴러갑니다.

**2. 적응형 지능 (adaptive intelligence)** — 문제 난이도에 따라 *compute를 자동으로 조절* 합니다. 쉬운 문제는 적게, 어려운 문제는 많이. *reasoning budget* 을 사람이 정하지 않습니다.

**3. 적응형 인터페이스 (adaptive interfaces)** — *사용자가 시스템과 상호작용하는 방식에서 학습* 합니다. 한 번 답을 주고 끝이 아니라, 사용자가 무엇을 받아들이고 무엇을 거부하는지로 시스템이 본인 행동을 조정합니다.

이 셋이 합쳐져 *데이터 + recipe + 평가 루프* 가 동시에 self-improve 합니다. RAFT, DPO, GRPO 같은 학습 알고리즘과 데이터 큐레이션 전략을 *사람이 골라야 하는* 시대를 마감하겠다는 베팅입니다.

## 숫자 — 사람 vs 시스템

회사가 공개한 핵심 수치는 다음 두 개입니다.

- **+35%** — Adaption 사내 AI 리서처가 *직접 설계한* 학습 대비 AutoScientist의 평균 성능 향상
- **48% → 64%** — 같은 비교에서 win rate

*"사내 AI 리서처"* 라는 표현이 모호하긴 합니다. *전 Cohere VP 출신* 이 모은 사내 인력이라면 일반 회사의 ML 엔지니어보다 강할 가능성이 높지만, *진짜 frontier lab 시니어 리서처* (예: [[Anthropic]]·OpenAI 인력)와 비교한 게 아니라는 점은 짚어야 합니다. 외부 재현이 따라야 합니다.

다만 *48% → 64%* 라는 win rate 점프 폭은 무시하기 어렵습니다. *동등한 인력의 절반 이상이 자동화에 진다* 는 의미라, 만약 사실이라면 *fine-tuning consultant* 라는 업종 자체가 압박을 받습니다.

## 회사 배경

[2026년 2월 Fortune 보도](https://fortune.com/2026/02/04/adaption-labs-50-million-seed-funding-emergence-captial-sara-hooker-sudip-roy-ai-models-that-learn-on-the-fly/)로 본 자금 구조는 다음과 같습니다.

- **시드** — $50M (Emergence Capital + Mozilla Ventures 리드)
- **공동창업** — [[사라 후커]] (CEO) + Sudip Roy (전 Cohere inference director)
- **포지셔닝** — *작고 똑똑한 모델* 노선, *scaling race에 반대* 노선

이 라인업이 보내는 메시지는 명확합니다. *Frontier 랩들이 더 큰 모델 + 더 많은 컴퓨트로 가는 동안, 다음 병목은 학습 expertise 자체* 라는 베팅입니다. [[Anthropic]]이 *Constitutional AI* 로 학습 방법론을 자기 자산화한 것과 같은 결의 베팅을 *외부 도구* 형태로 만드는 시도입니다.

## 누구에게 의미가 있나요

자동 fine-tuning이 모두에게 같은 의미는 아닙니다.

**중소·중견 AI 팀** — 전담 ML 리서처가 1~2명인 회사. 본인들이 골라야 할 RAFT vs DPO vs GRPO를 시스템이 자동 결정한다면, ML 인력 한 명 분이 다른 일로 옮겨갈 수 있습니다. 직접적 이득.

**한국 SI·금융권 AI 팀** — 고객 도메인 데이터로 자체 모델을 만드는 경우. 자체 노하우를 *AutoScientist 같은 도구* 와 *사내 시니어 리서처* 두 채널 중 하나로 흡수시킬 수 있다면, 의사결정 비용이 크게 떨어집니다. 다만 *데이터 외부 유출* 우려는 별도 검토가 필요합니다.

**Frontier lab들** — 직접 이득은 적습니다. [[Anthropic]] 같은 곳은 *학습 노하우* 자체가 경쟁 우위라 외부 도구로 대체할 유인이 없습니다.

**컨설팅·MLOps 업종** — 압박을 받는 자리입니다. *"본인 데이터를 가져오면 우리가 fine-tune 해드립니다"* 라는 모델이 *"AutoScientist를 켜세요"* 로 대체될 가능성.

## Sakana AI The AI Scientist와의 차이

비슷한 이름의 *AI Scientist* 가 이미 있습니다 — [Sakana AI](https://sakana.ai)가 2024년 공개한 *연구 자동화* 시스템. 둘은 자동화 대상이 다릅니다.

| 시스템 | 자동화 대상 |
| --- | --- |
| Sakana AI Scientist | 가설 생성·논문 작성·실험 설계 (연구 자체) |
| Adaption AutoScientist | 데이터·recipe·평가 (학습 운영) |

Sakana는 *논문을 쓰는 AI* 입니다. AutoScientist는 *기업이 자기 데이터로 모델을 fine-tune하는 일* 을 자동화합니다. 같은 *"연구 자동화"* 카테고리로 묶이지만, 실제로 푸는 문제와 고객이 완전히 다릅니다.

## 한계와 의문

- **재현성** — *사내 AI 리서처* 라는 비교 기준이 공개되지 않았습니다. 누가 보더라도 같은 수치가 나오는지는 외부 재현이 따라야 합니다.
- **첫 30일 무료** — *오후 한나절이면 어댑테이션 끝* 이라는 마케팅 표현은 *얼마나 빨리 lock-in되는가* 에 대한 질문이기도 합니다. 본인 학습 파이프라인을 자동화 도구에 의존시킨 뒤 가격이 어떻게 되는지는 별도 관찰이 필요합니다.
- **데이터 위치** — 본인 데이터가 어디서 처리되는지(클라우드 vs on-prem) 명시적 답변이 필요합니다. 한국 금융권·의료 데이터에는 결정적 변수입니다.

## 정리

- *Fine-tuning을 사람이 운영하는 시대* 가 끝나는지 검증할 첫 본격 제품입니다. *[[사라 후커]] + 전 Cohere 인력* 이라는 무게감이 무시할 수 없는 신호입니다.
- *+35% / 48%→64% win rate* 라는 수치는 외부 재현 전에는 마케팅 자료지만, *프론티어 학습 expertise를 외부 도구로 흡수* 한다는 베팅 방향은 명확합니다.
- 한국 중소·중견 AI 팀이 가장 빠르게 이득을 볼 자리지만, *데이터 위치*·*lock-in*·*가격* 세 가지를 직접 확인하지 않고 도입하기는 이릅니다. 첫 30일 무료를 *한 번 돌려 보는* 정도가 가장 합리적 시작입니다.
