---
date: 2026-09-04
ready: true
tags:
  - 논문
  - LLM
  - 트랜스포머
description: 긴 컨텍스트 디코드에서 매 스텝 전체 KV를 읽는 비용을, 모델이 CoT 안에 어텐션 범위를 선언하게 해서 줄입니다. KAIST·DeepMind 자문 팀이 제안한 Declarative Attention은 제로샷으로 attended tokens를 최대 52% 줄이고, 정확도 손실은 1~3pp 수준입니다.
image: "![[da-overview.png]]"
buzz: 46
---

> N. Ho, H. Ahmad, W. Koh, S.-Y. Yun, T. Schuster, and C. Nogueira dos Santos, "Language Models Can Control Their Own Attention," arXiv:2609.02737, 2026.

긴 대화를 이어가다가 앞쪽 한 줄을 다시 물을 때를 생각해 봅니다. 사람은 그 한 줄이 있는 구간만 다시 펼칩니다. 트랜스포머 디코드는 대개 그렇지 않습니다. 답이 한 토큰씩 나올 때마다 글로벌 어텐션 레이어가 지금까지의 KV 캐시를 통째로 읽습니다. 컨텍스트가 백만 토큰이면, 실제로 쓰는 토큰은 소수인데도 매 스텝 읽기 비용은 $O(N)$으로 남습니다.

기존 해법은 대체로 이렇습니다. 가벼운 프록시 점수로 "중요해 보이는" 토큰·페이지를 고른 뒤 나머지를 마스크합니다. [Quest](https://arxiv.org/abs/2406.10774)처럼 쿼리 인식 페이지 선택이 대표적이고, 상수는 줄여도 스텝마다 전체(또는 그 대리 표현)를 한 번 훑는 구조는 남습니다. 이 논문은 질문을 뒤집습니다. 모델이 이미 어디가 필요한지 알고 있다면, 그 계획을 텍스트로 말하게 하면 되지 않느냐는 것입니다.

![[da-overview.png]]

## 저자

공동 1저자 셋은 모두 [[카이스트|KAIST]] AI OSI LAB입니다. [[허남규]]은 NeurIPS 2024 Block Transformer의 공동 1저자이고, LG AI Research와 [[Google DeepMind]] 인턴을 거쳤습니다. [[후자마 아흐마드]]는 SpotAttention처럼 사전학습 장문맥 모델에 꽂는 블록-스파스 라우팅을 따로 밀어 온 사람입니다. [[고우성|Woosung (Reiss) Koh]]까지 합치면, 같은 랩에서 어텐션 비용을 "아키텍처로 줄이기"와 "선택기로 줄이기"를 동시에 다루던 사람들이 세 번째 축을 연 셈입니다.

교신저자는 [[윤세영]](OSI LAB 리더), [[탈 슈스터]], [[시세로 노게이라]]입니다. 슈스터는 Block Transformer에도 이름을 올렸고, DeepMind에서 LLM adaptive compute를 다룹니다. 다만 논문이 첫 페이지에 밝힌 대로 Google 공저는 advisory 역할입니다. 실질 설계·실험의 무게는 KAIST 쪽에 있습니다.

합류 동기는 직전 작업에서 읽힙니다. Block Transformer는 글로벌-로컬 계층으로 KV 병목을 구조적으로 줄였습니다. SpotAttention은 이미 학습된 모델에 외재적 라우터를 붙입니다. Declarative Attention은 파라미터를 건드리지 않고, 모델이 CoT 안에서 자신의 어텐션 span을 선언하게 합니다. 같은 비용 문제를 세 층위에서 본 결과입니다.

## 배경

어텐션이 소수 토큰에 몰린다는 관찰 자체는 오래됐습니다. 문제는 그 소수를 **미리** 알 수 없다는 점입니다. 진짜 attention score는 full matrix를 계산한 뒤에야 나옵니다. 그래서 정적 휴리스틱(최근성, 과거 크기)은 미래 쿼리를 못 따라가고, 쿼리 인식 경량 스캔은 정확도를 지키더라도 스텝당 $O(N)$ 선택을 남깁니다.

다른 갈래는 컨텍스트를 밖에서 줄입니다. 검색으로 무엇을 넣을지 고르거나, 에이전트 루프에서 히스토리를 요약·삭제합니다. Anthropic이 정리한 컨텍스트 엔지니어링도 같은 예산 문제입니다. 다만 검색·압축은 "무엇이 컨텍스트에 들어오는가"이고, 이 논문이 겨냥하는 것은 "이미 들어온 것 중 매 스텝 무엇을 읽는가"입니다. 저자들도 에이전트 설정에서 tool 결과가 누적될수록 DA가 다루는 비용이 커진다고 적습니다.

선행으로 Self-Selected Attention Span(Jin et al., 2024)은 태스크별 파티션과 주석 문법으로 span 선택을 **학습**시켰고, 컨텍스트는 2K 규모였습니다. DA는 한 장의 태스크 무관 프롬프트로 기성 모델에서 제로샷으로 같은 행동을 끌어내고, 평가 컨텍스트는 대략 $10^5$ 토큰 규모까지 올라갑니다. 마스크를 활성화 근사가 아니라 생성된 텍스트에서 직접 읽으므로, 선언된 글로벌 구간을 제외하면 스텝마다의 선택 스캔 비용이 사라집니다.

## 어떻게 만들었나

DA는 생성 구간을 세 모드로 나눕니다. 모드 전환은 CoT 안의 태그로 이뤄지고, 옆에서 돌아가는 상태 머신이 디코드 스텝마다 어텐션 마스크를 갱신합니다.

```text
<global> … 전체 세그먼트를 훑어 다음 focus 후보를 고름 … </global>
<focus magic_chunks="2"> … 해당 청크에서 값을 추출 … </focus>
<local> … 이미 뽑아 둔 값만으로 계산·합성 … </local>
<answer>…</answer>
```

프롬프트는 항상 보이는 scaffold와, 가시성이 바뀌는 context로 나뉩니다. scaffold는 시스템 지시, 질문, DA 사용법입니다. context는 긴 입력을 목표 약 2048토큰 단위로 나눈 뒤, 모델이 이미 익숙한 tool-turn 경계에 실어 "Magic Chunk N"으로 보여 줍니다. 실제 tool은 실행되지 않습니다. 세그먼트는 생성 전에 모두 들어가 있고, focus가 이름을 부를 수 있게 주소만 붙인 것입니다.

마스크는 토큰 단위가 아니라 vLLM 블록(보통 16~32토큰) 단위입니다. 커널이 블록 통째로 읽기 때문에, 흩어진 토큰 몇 개를 빼도 메모리 트래픽이 안 줄어듭니다. 상태 머신은 선언된 span을 바깥으로 블록 정렬해 보존하고, 요청의 KV 블록 테이블만 다시 써서 FlashAttention 경로는 그대로 둡니다. SWA·Gated DeltaNet처럼 이미 비용이 윈도/상태로 묶인 효율 레이어에는 손을 대지 않습니다.

평가 팔은 셋입니다. Vanilla, DA, 그리고 같은 청크·모드 프롬프트만 쓰고 마스크는 끈 $DA^{nm}$입니다. $DA^{nm}$이 있어야 "절약이 프롬프트 형식 때문인지, 마스크 때문인지"가 갈립니다.

## 결과

15개 장문맥 소스(RULER NIAH, LongBench, LooGLE, ZeroSCROLLS 등)에서 헤드라인 모델 두 개의 총평균은 다음과 같습니다.

| 모델 | Vanilla acc | DA acc | $\Delta$ acc | Vanilla tokens | DA tokens | 감소율 |
| --- | --- | --- | --- | --- | --- | --- |
| Gemma-4-31B | 87.01% | **85.74%** | $-1.27$pp | 13.43M | **6.45M** | **52.0%** |
| Qwen-3.6-27B | 85.31% | **82.56%** | $-2.75$pp | 22.54M | **15.52M** | **31.1%** |

절대 절약은 긴 소스에서 큽니다. `code_repo`에서 Gemma 41.8M, Qwen 52.0M 토큰이 줄고, `dialogue_history`에서도 각각 22.1M·39.1M이 빠집니다. 멀티스팬 추론 쪽 정확도 하락이 싱글스팬보다 큽니다(Gemma 카테고리 평균 $-2.28$pp vs $-0.78$pp).

![[da-fig2-mask.png]]

$DA^{nm}$은 정확도는 vanilla에 가깝습니다(Gemma 동률, Qwen $-0.69$pp). 그런데 attended tokens는 vanilla보다 각각 66.2%, 28.8% **많습니다**. DA 프로토콜이 디코드 스텝을 약 15~35% 늘리기 때문입니다. 마스크를 켜면 그 오버헤드가 뒤집혀, $DA^{nm}$ 대비 attended tokens가 Gemma 71.1%, Qwen 46.5% 줄어듭니다. 효율의 출처는 짧은 생성이 아니라 마스크입니다.

스케일 축도 같은 방향을 가리킵니다. vanilla 대비 상대 정확도는 Gemma-4-E4B 29%에서 31B 99%로, Qwen-3.5-4B 64%에서 3.6-27B 97%로 올라갑니다. 작은 모델은 태그·청크 참조를 못 지키는 비율이 높고, Gemma-4-E4B의 focus 성공률은 58%에 그칩니다(대형 모델은 약 99%). 토큰 절약 비율 자체는 규모에 덜 민감하고, 대체로 vanilla의 절반 전후입니다.

![[da-fig3-scale.png]]

Roofline으로 잡은 디코드 wall-clock(단일 B200, bf16, MFU 40% / MBU 70%)에서는 Gemma가 vanilla 대비 $0.71\times$, Qwen이 $0.77\times$입니다. 절감은 글로벌 KV 읽기에서만 나옵니다. matmul과 로컬(효율 레이어) 비용은 스텝 수 증가 때문에 오히려 조금 커집니다. Gemma는 SWA 바닥이 커서 글로벌 절감이 희석되고, Qwen의 GDN 상태는 작아 절감이 더 잘 남습니다. 수치는 실측이 아니라 이용률 가정하의 천장입니다.

## 회고

저자들이 한계로 적는 지점은 대부분 제로샷 elicitation의 속성입니다. 디코드 스텝이 늘어나고, 태스크 모양에 안 맞는 모드 분해가 남으며, thinking trace 안에서는 프로토콜이 깨져 non-thinking만 평가했습니다. 벤치마크용으로 만든 magic chunk는 실제 문서 구조가 아니라 휴리스틱 분할입니다. 에이전트의 tool·유저 턴처럼 원래 주소 가능한 경계가 있으면 더 자연스럽다고 봅니다.

글로벌 모드가 전체 attended tokens의 대부분(저자 분석상 80% 이상)을 차지한다는 점도 남습니다. 내비게이션에 full fidelity가 필요 없다면 세그먼트 인덱스만 보게 하는 쪽이 다음 레버입니다. 반대로 글로벌 구간에 Quest류 경량 스캔을 붙이고, focus/local은 선언 마스크에 맡기면 두 축이 겹칩니다. 스펙큘레이티브 디코딩과도 보완적입니다. DA는 스텝 비용을 낮추고, speculation은 늘어난 스텝 수를 묶습니다.

해석 가능성 주장도 메커니즘에 붙어 있습니다. 마스크를 만드는 토큰이 곧 사람이 읽는 계획입니다. 저자들은 이를 system-2 sparse attention이라 부르고, 정확도와 어텐션 효율을 같이 보상하는 RL을 후속으로 적습니다. KV 오프로딩 관점에서는 모드가 span 단위로만 바뀌고 선언이 읽기보다 앞서므로, out-of-focus 세그먼트를 호스트로 내렸다가 prefetch할 손잡이가 생깁니다. 요약으로 원문을 지우는 compaction과는 달리 시퀀스를 편집하지 않으므로 캐시가 유효하게 남습니다.

## 정리

- Declarative Attention은 기성 LLM이 CoT에서 `<global>` / `<focus>` / `<local>`을 선언하게 해, 추론 엔진이 KV 블록 읽기를 줄이는 제로샷 프로토콜입니다.
- 15개 장문맥 과제에서 Gemma-4-31B는 attended tokens 52.0% 감소·정확도 $-1.27$pp, Qwen-3.6-27B는 31.1% 감소·$-2.75$pp입니다. 절약은 마스크에서 오고, 같은 프롬프트만 쓴 $DA^{nm}$은 오히려 더 비쌉니다.
- 백본이 커질수록 프로토콜 준수와 제한된 정보 하의 답변 품질이 같이 올라 vanilla 격차가 닫히며, 컨텍스트가 길수록 절대 토큰 절약이 커집니다. 남은 과제는 thinking 연동, 자연 세그먼트, 글로벌 모드 비용입니다.

---
참고: [arXiv:2609.02737](https://arxiv.org/abs/2609.02737) · [Quest (Tang et al., 2024)](https://arxiv.org/abs/2406.10774) · [Block Transformer (Ho et al., NeurIPS 2024)](https://arxiv.org/abs/2406.02657) · [SpotAttention (Ahmad & Yun, 2026)](https://arxiv.org/abs/2606.22874) · [Anthropic - Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [HF Papers](https://huggingface.co/papers/2609.02737)
