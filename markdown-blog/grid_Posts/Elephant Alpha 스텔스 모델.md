---
date: 2026-04-18
tags:
  - 정보
  - LLM
  - 벤치마크
description: "OpenRouter에 등장한 100B 파라미터 스텔스 모델 Elephant Alpha. 환각 억제 벤치 1위, 코딩 82%, 무료 공급. '유명한 오픈 모델 랩'의 정체를 공개하지 않은 채 강력한 성능을 내놓았습니다."
---

지난주 OpenRouter에 **코드명 "Elephant Alpha"**라는 모델이 조용히 올라왔습니다. 제작사 미공개, 모델 카드 없음, 무료 공급. 그런데 **환각 억제 벤치마크에서 1위**를 찍었습니다.

개발자 커뮤니티가 술렁이고 있습니다. DeepSeek일까, Qwen일까, 새로운 Llama 계열일까. 확인된 건 **"유명한 오픈 모델 랩의 스텔스 릴리즈"**라는 한 줄뿐입니다.

> 모델 접속: [openrouter.ai/openrouter/elephant-alpha](https://openrouter.ai/openrouter/elephant-alpha)
> OpenRouter 공식 트윗: [@OpenRouter](https://x.com/OpenRouter/status/2043714975756390844)

---

## 기본 스펙

| 항목 | 내용 |
|---|---|
| 출시일 | **2026년 4월 13일** |
| 파라미터 | **100B** |
| 컨텍스트 | **256K 토큰** |
| 출력 최대 | 32K 토큰 |
| 지원 기능 | Function calling, Structured output, Prompt caching |
| 입력 양식 | **텍스트 전용** (이미지·오디오·비디오 미지원) |
| 가격 | **입력·출력 모두 $0** (알파 기간) |
| 공급자 | **비공개** ("a prominent open model lab") |

256K 컨텍스트는 100B급 모델에서 상위권입니다. 다만 멀티모달이 빠진 점은 요즘 모델들 흐름과 다릅니다. **텍스트·코드 워크로드에만 집중**한 설계로 보입니다.

---

## 벤치 수치 — 환각 억제 1위

[benchable.ai](https://benchable.ai/models/openrouter/elephant-alpha) 독립 벤치 기준입니다.

| 카테고리 | 점수 | 평가 |
|---|---|---|
| **Hallucination Prevention** | **100%** | **🥇 전체 1위** (정확도·비용효율 모두) |
| General Knowledge | 98.0% | 최상위권 |
| Ethics | 96.0% | — |
| Email Classification | 96.0% | — |
| **Coding** | **82.0%** | 강점 영역 |
| Reasoning | 78.0% | 평균 |
| **Instruction Following** | **54.0%** | **⚠️ 약점** |
| 전체 성공률 | 99% | — |
| 속도 | 67 백분위 | 상위권 |

**해석**:
- **환각 100%는 드문 수치**입니다. 상위 프론티어 모델들도 대부분 95% 전후에서 맴돕니다. 학습·RLHF 파이프라인이 "모르면 모른다고 말한다"는 축에 상당한 자원을 투입한 흔적입니다.
- **코딩 82%는 100B급 평균 이상**. 공식 공급자가 강조한 "code completion, debugging" 포지셔닝과 일치합니다.
- **지시 이행 54%는 명백한 약점**입니다. 복잡한 다단계 지시를 처리해야 하는 에이전트 워크로드에 쓰려면 주의가 필요합니다.

---

## 포지셔닝: "Intelligence Efficiency"

공급자의 핵심 메시지는 **"같은 정확도를 더 적은 토큰으로"**입니다. OpenRouter 공식 설명은 **"100B급 SOTA 매칭하면서 극도로 토큰 효율적"**.

공식 타깃 용도:
- Rapid code completion / debugging
- Long document 단일 패스 처리 (256K 컨텍스트 활용)
- Lightweight agent loops (토큰 예산 중요한 상황)

[[Claude 토큰 소모와 성능 저하]]에서 다뤘듯, 요즘 모델들은 토큰 효율이 점점 중요한 축이 되고 있습니다. Elephant Alpha는 이 흐름을 정면으로 잡겠다는 메시지입니다.

---

## 정체는 누구인가

가장 재밌는 부분입니다. **아무도 모릅니다**.

**커뮤니티 추측**:
- [David Hendrickson (X)](https://x.com/TeksEdge/status/2044041574863040523)은 **DeepSeek V3.3 또는 "V4 Lite"** 가능성을 제기. 100B + 256K + 토큰 효율 강조는 DeepSeek 시리즈의 특성과 맞아떨어집니다.
- "prominent open model lab" 표현은 **오픈 가중치를 공개하는 랩**을 시사합니다. 후보군: **DeepSeek, Qwen(Alibaba), Meta(Llama), Mistral, Kimi**.
- OpenAI나 Anthropic은 오픈 모델 랩이 아니므로 제외됩니다.

**단정할 수 없는 이유**:
- 공식 모델 카드 없음
- 학습 세부정보 없음
- 표준 벤치(SWE-bench, MMLU, HumanEval) 랩 측 공표 없음
- 아키텍처 상세 미공개

흥미로운 단서 하나: Kilo 블로그가 **이전 스텔스 모델 "Giga Potato"**를 언급했습니다. OpenRouter가 **동물·사물 코드명으로 스텔스 모델을 시리즈로 운영**하고 있다는 뜻입니다. Sonoma Dusk, Sonoma Sky(둘 다 나중에 Grok 4 계열로 밝혀짐) 같은 사례도 있었습니다. 알파 기간이 끝나면 정체가 공개되는 패턴이 유력합니다.

---

## 왜 무료로 풀었나

이유는 단순합니다. **학습 데이터 수집**입니다.

공식 고지:
> "Prompts and completions may be logged by the provider and used to improve the model."

100B 모델을 전 세계에 무료로 푸는 랩은 자선 사업이 아닙니다. 이용자의 프롬프트·완성 결과가 **다음 버전 학습 데이터**로 쓰입니다. 그래서:

1. **민감 정보·사내 코드는 절대 입력 금지**
2. **프로덕션 의존 금지** — 알파는 언제든 종료 가능
3. [datanorth.ai](https://datanorth.ai/news/openrouter-launches-elephant-alpha)와 [Kilo 공식 블로그](https://blog.kilo.ai/p/introducing-elephant-a-new-stealth)가 공통으로 권고한 포지셔닝: **"평가 채널"**. 성능 평가용으로만 쓰고, 실제 서비스는 공식 공급자로 돌려야 합니다.

스텔스 모델 생태계는 **"무료 벤치 공유 vs 프롬프트 로깅"**이라는 딜 구조 위에 서 있습니다. 유용하지만, 이해하고 써야 합니다.

---

## 정리 — 써볼 만한가

**써볼 만한 경우:**
- 새 모델 평가 / 벤치마크 실험
- 민감하지 않은 대용량 문서 요약·번역
- 개인 프로젝트의 빠른 코드 자동완성

**쓰면 안 되는 경우:**
- 사내 비공개 코드 입력
- 고객 데이터 처리
- 복잡 다단계 지시 기반 에이전트 (IF 54%가 발목을 잡습니다)
- 서비스 운영 경로 (공급 종료 리스크)

**핵심 요약**: **환각 잘 안 내고, 코딩 적당히 잘하고, 지시는 좀 잘 못 듣는 100B 모델**. 토큰을 아껴주는 게 강점, 복잡한 문맥에서 무너지는 게 약점입니다. 정체가 공개되는 2~3주 후가 진짜 평가의 시작일 겁니다.

---

## 관련 문서

- [[Claude Opus 4.7]]
- [[Claude 토큰 소모와 성능 저하]]
- [[AI 3대장 인프라]]
