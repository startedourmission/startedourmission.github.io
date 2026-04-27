---
date: 2026-04-17
tags:
  - 정보
  - LLM
description: "Anthropic, OpenAI, Google 세 회사의 AI 인프라를 숫자로 정리합니다. Stargate 10GW, TPU Ironwood 9,216칩 포드, Project Rainier 100만 칩 — 누가 어디서 어떤 칩으로 얼마를 쓰는지 한눈에 보는 비교."
---

AI 모델 품질 전쟁의 이면에는 **인프라 전쟁**이 있습니다. GPT, Claude, Gemini 세 회사가 쓰는 컴퓨트 인프라가 점점 갈라지고 있습니다. 같은 NVIDIA GPU를 나눠 쓰던 시절은 끝났고, 이제 각자 고유의 칩·클라우드·데이터센터 전략을 굳히는 단계입니다.

어제(2026-04-16) Opus 4.7 공개를 계기로 Anthropic 인프라를 정리하다 보니, 세 회사를 한자리에 놓고 비교하고 싶어졌습니다. 공식 발표와 1차 보도를 교차 확인해서 숫자를 맞췄습니다.

> 주요 출처: Anthropic·OpenAI·Google 공식 블로그, Data Center Frontier, TechCrunch, Reuters·CNBC 보도 (아래 본문 링크 참조)

---

## 한눈에 비교

| 항목 | **Anthropic** | **OpenAI** | **Google** |
|---|---|---|---|
| **주 클라우드** | AWS (주력) + Google Cloud | Microsoft Azure + Oracle/Stargate | 자사 Google Cloud |
| **핵심 학습 칩** | AWS Trainium2, Google TPU | NVIDIA GB200, 향후 자체 칩 | TPU v7 (Ironwood), Trillium |
| **자체 설계 칩** | ❌ (파트너 칩 사용) | ✅ 설계 중 (Broadcom 제조, 10GW) | ✅ 자체 설계 (Broadcom 협업) |
| **대표 클러스터** | Project Rainier (인디애나) | Abilene (텍사스) + Stargate 6곳 | 전 세계 Google 데이터센터 |
| **공표된 용량** | 2026년 1GW+ 신규 | 7GW 계획, 최종 10GW | Ironwood만 수백만 칩/2026 |
| **공표된 투자** | AWS $80억 + Google 수백억 달러 | Stargate $500B (2029년까지) | Ironwood·데이터센터 $1,850억 |
| **추론 서빙** | Bedrock, Vertex AI, MS Foundry | Azure + ChatGPT 자체 | Vertex AI, Gemini 앱 |

숫자 단위가 다릅니다. Anthropic이 "기가와트"를 말할 때, OpenAI는 "10기가와트"를 말합니다.

---

## Anthropic — 3-클라우드 헤지 전략

가장 **분산**된 구조입니다.

- **AWS Trainium2** (주력 학습): 인디애나의 **Project Rainier** 클러스터가 중심입니다. 약 50만 칩에서 시작해 2025년 말 100만 칩+로 확장 예정. AWS는 $80억을 투자했습니다.
- **Google TPU**: 2025년 10월 수백억 달러 규모의 확장 계약. 최대 **100만 TPU**, 2026년 1GW+ 용량을 받습니다. Broadcom이 TPU 커스텀 설계에 참여합니다.
- **NVIDIA GPU**: 학습·추론 보조 용도로 계속 사용.
- **CoreWeave**: 2026년 하반기부터 GPU 인프라를 단계적으로 임대. 추론 스케일링 용도.

전략이 명확합니다. **한 칩, 한 클라우드에 묶이지 않는다.** Trainium은 비용 효율, TPU는 대규모 학습, GPU는 범용성 — 칩마다 강점이 다르니 워크로드를 골라서 돌립니다. 공급망 리스크도 분산됩니다.

[Anthropic × Google TPU 확장](https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services) · [Google·Broadcom 파트너십](https://www.anthropic.com/news/google-broadcom-partnership-compute)

---

## OpenAI — Stargate라는 국가급 프로젝트

세 회사 중 단연 **규모가 큽니다**. 그리고 가장 복잡합니다.

**Stargate 프로젝트**가 중심축입니다. OpenAI, SoftBank, Oracle, MGX가 공동 출자한 합작법인으로, 2029년까지 미국 내 **AI 인프라에 최대 $5,000억**을 투자합니다. 총 **10GW** 목표.

현황:
- **플래그십 사이트**: 텍사스 애빌린(Abilene). Oracle이 15년 리스로 **GB200 GPU 45만 개 이상**을 배치.
- **Oracle 확장 계약**: $3,000억+, 추가 4.5GW. "OpenAI-Oracle 단독 거래"로는 역대 최대.
- **현재 계획 용량**: 7GW, 6개 사이트에서 건설 중.
- **2026년 하반기 첫 1GW**가 NVIDIA **Vera Rubin 플랫폼**으로 온라인 예정.
- **Microsoft Azure**도 계속 병행. 추론·API 서빙의 상당 부분이 Azure에서 돌아갑니다.

여기에 2025년 10월 공개된 **OpenAI-Broadcom 자체 칩 계약**이 얹힙니다. OpenAI가 직접 설계한 AI 가속기를 Broadcom이 제조해 **10GW 규모**로 배치합니다. 2026년 하반기부터 출하 시작, 2029년 완료. OpenAI가 NVIDIA 의존도를 낮추려는 첫 번째 큰 발걸음입니다.

달러 단위의 무게감이 다릅니다. Stargate 혼자서 Anthropic 전체 계약 규모보다 큽니다.

[Stargate 프로젝트 발표](https://openai.com/index/announcing-the-stargate-project/) · [Stargate Oracle 확장](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) · [OpenAI × Broadcom 10GW](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)

---

## Google — 수직 통합의 끝판왕

Google은 유일하게 **처음부터 끝까지 자기 집**에서 해결합니다.

**TPU v7 (코드명 Ironwood)**가 2026년 초 GA. 숫자가 흉악합니다:
- **9,216칩 / 포드 (pod)**, 액체 냉각
- 포드당 **42.5 엑사플롭스** — 단일 포드가 세계 최강 슈퍼컴퓨터급
- 포드당 **10MW** 전력
- TPU v5p 대비 **10배**, Trillium(v6e) 대비 **4배+** 성능
- 첫 **native FP8** 지원 Google TPU

TSMC에서 2026년 생산 시작, **수백만 개 양산 계획**. 설계는 Google이, 물리 구현은 Broadcom이 돕습니다.

인프라도 자사 데이터센터입니다. 별도 합작법인이나 장기 리스가 없습니다. Google Cloud 전 리전에 TPU가 분산 배치되고, Ironwood·Trillium·Axion ARM CPU가 함께 돌아갑니다. 데이터센터와 칩에 **$1,850억**을 투자한다고 공표했습니다.

재미있는 반전은 **고객들**입니다:
- **Anthropic**: 최대 100만 TPU 계약
- **Meta**: 2026년부터 TPU 리스, 수십억 달러 규모 (최종 논의 중)

Google은 경쟁사의 경쟁 모델을 자사 칩에서 돌립니다. "TPU는 GPU보다 싸고 빠르다"는 메시지를 적극 팔고 있습니다.

[Ironwood 공식 소개](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/) · [TPU v7 기술 상세 (SemiAnalysis)](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)

---

## 세 회사의 전략 차이

같은 "컴퓨트 확보"를 서로 다른 철학으로 풀고 있습니다.

| 전략 축 | Anthropic | OpenAI | Google |
|---|---|---|---|
| 칩 자체 설계 | ❌ (파트너) | 🟡 (설계 시작) | ✅ (7세대째) |
| 클라우드 자사 소유 | ❌ | ❌ (Stargate 공동출자) | ✅ |
| 공급사 헤지 | ✅ 매우 강함 | 🟡 중간 | ❌ (자사 중심) |
| 투자 스케일 | $100억대 | $5,000억대 | $1,000억대 |
| 리스크 프로파일 | 분산·유연 | 집중·메가딜 | 수직 통합 |

**Anthropic**은 "작지만 빠르게, 어디에도 안 묶이게"를 택했습니다. Opus 4.7처럼 자주 내놓으면서 비용·공급 리스크를 분산합니다.

**OpenAI**는 "국가급 인프라"를 짓고 있습니다. Stargate는 이미 사기업 규모를 넘어섰고, 미국 내 반도체 공급망·에너지 정책과 얽힙니다. 스케일은 최강이지만 파트너 간 이해관계가 복잡합니다.

**Google**은 "수직 통합"의 모범답안을 계속 가다듬습니다. 7세대 TPU는 이제 성능·가격·전력에서 NVIDIA와 동급 혹은 우위를 주장할 만한 수준이 됐고, 경쟁사들이 고객으로 들어옵니다.

---

## 숨은 공통분모: Broadcom

세 회사 이름 옆에 **Broadcom**이 계속 등장합니다.

- Google TPU 커스텀 설계 파트너
- OpenAI 자체 칩 제조 파트너 (10GW)
- Anthropic이 계약한 Google TPU 자체도 Broadcom 참여

2025년 기준 **Broadcom의 AI 커스텀 칩 매출이 전년 대비 100% 이상 성장**했다는 발표가 있었습니다. NVIDIA가 "AI 칩 = GPU"를 독점하는 동안, Broadcom은 조용히 "AI 칩 = 맞춤 설계" 시장을 쓸어 담고 있습니다. 이 게임의 **진짜 승자**일 수 있다는 분석이 늘어나고 있는 이유입니다.

---

## 인프라 안정성 — 누가 가장 덜 무너지나

스펙과 달러 규모는 인상적이지만, **실제로 안 끊기는 게 제일 중요**합니다. 2026년 1~4월의 인시던트 기록을 비교해봤습니다.

### 클로드 — 가장 불안정

2026년 들어 **가장 자주 무너졌습니다**.

- **4월 15일**: Claude.ai·API·Claude Code 전방위 장애 (약 3시간, DownDetector 신고 5,100건+)
- **4월 13일**: 48분 장애 (Claude.ai + Claude Code)
- **최근 90일 기준**: **128건의 인시던트** — 메이저 41건, 마이너 87건, 중앙값 지속시간 **1시간 7분**
- 3월 말~4월 초에도 유사한 elevated-error 이슈 반복

원인은 **수요 폭증**입니다. 2월 Opus 4.6 출시로 에이전틱 코딩 수요가 폭발했고, 3-클라우드 분산에도 불구하고 피크 트래픽을 소화하지 못하는 상황이 반복되고 있습니다. 앞 글에서 다룬 [[Claude 토큰 소모와 성능 저하]] 이슈도 같은 맥락입니다 — 용량이 부족하니 throttling과 설정 변경이 빈번해집니다.

### Gemini — 부분 불안정 (이미지·멀티모달)

텍스트 API는 **상대적으로 안정**, 그러나 일부 특수 워크로드는 **눈에 띄게 불안**합니다.

- **2월 27일**: Vertex Gemini API 약 2시간 장애. 안전 필터 서비스 **설정 변경**이 전체 모델로 번짐.
- **3월 27일**: AI Studio의 `gemini-3-pro-image-preview`(Nano Banana Pro)와 Nano Banana 2 이미지 API 대규모 장애.
- **근본 원인**: **TPU v7 (Ironwood) 양산 램프가 아직 완료되지 않았습니다.** 2026년 내내 확대 중이라 이미지 생성 같은 고비용 diffusion 워크로드가 GPU·TPU 자원을 두고 경합합니다. Gemini 3.0 학습 세션이 같은 풀을 쓰는 것도 원인으로 지목됩니다.

핵심 Gemini 텍스트 API는 잘 버팁니다. 문제는 **Ironwood 의존 워크로드가 늘수록 변동성이 커질 수 있다**는 점입니다. 수직 통합의 장점은 통제력이지만, **병목이 생기면 혼자 다 감당**해야 한다는 단점도 있습니다.

### ChatGPT — 가장 안정

수치상 가장 좋습니다.

- **1~4월 12개 컴포넌트 평균 가동률 99.99%** (OpenAI 공표)
- 큰 장애는 있지만 **빈도가 낮습니다**:
    - 2월 3~4일: 대규모 장애 (신고 28,000건+, 드물게 큰 사고)
    - 4월 14일: 계정 생성 이슈 (부분적)
- 장애 간 간격이 길고, 서비스 전반 대신 특정 컴포넌트만 영향받는 경우가 많습니다.

이유는 역설적이게도 **Stargate가 아직 가동 전**이라서입니다. 현재 ChatGPT 추론은 Microsoft Azure의 검증된 GPU 풀에서 돌아갑니다. Azure는 엔터프라이즈급 SLA 이력을 쌓아온 인프라입니다. Stargate 1GW가 하반기부터 온라인되면 **변수가 늘어날 수 있습니다**.

### 정리 — 안정성 순위

| 순위 | 서비스 | 체감 안정성 | 주 원인 |
|---|---|---|---|
| 🥇 | **ChatGPT** | 최상 | 검증된 Azure 인프라, 99.99% 가동률 |
| 🥈 | **Gemini (텍스트)** | 양호 | 자사 TPU 통제, 단 이미지 API는 불안 |
| 🥉 | **Claude** | 취약 | 수요 > 용량, 최근 90일 128건 인시던트 |

단 **이 순위는 오래 가지 않을 수 있습니다**.

- OpenAI는 2026년 하반기 Stargate Vera Rubin 전환 시 **새로운 소프트웨어 스택의 안정화 기간**을 거칩니다. 과거 어떤 대규모 마이그레이션도 무흔적이 아니었습니다.
- Google은 Ironwood가 2026년 내내 **수백만 칩 규모로 램프업**합니다. 신규 칩 대량 배치 과정에서 예기치 못한 이슈가 나올 수 있습니다.
- Anthropic은 Project Rainier 100만 칩+CoreWeave 온라인이 들어오면 **2026년 하반기 여유 생길 가능성**이 있습니다. 지금이 바닥일 수도 있습니다.

**"지금 가장 안정적인" 순위와 "앞으로 가장 안정적일" 순위는 다를 수 있다**는 뜻입니다. 운영 환경에 중요한 서비스를 붙인다면, 한 공급사에 묶지 말고 **멀티 프로바이더 폴백**을 설계하는 게 현실적입니다.

---

## 사용자 관점에서 뭐가 달라지나

인프라 차이는 결국 **세 가지**로 번역됩니다.

1. **가격** — Google TPU 자체 조달이 제일 쌉니다. OpenAI는 NVIDIA+Oracle 프리미엄을 얹을 수밖에 없습니다. Anthropic은 중간.
2. **가용성·지역** — Google이 글로벌 리전 수 최다. OpenAI는 Azure+Stargate 거점 중심. Anthropic은 3-클라우드라 선택지가 넓습니다.
3. **장기 로드맵 예측 가능성** — Google이 가장 단순합니다(자사 컨트롤). OpenAI는 Stargate·Broadcom 일정 변수가 많습니다. Anthropic은 파트너 의존이 분산돼 변동이 적습니다.

결국 모델 품질만큼이나 **어느 클라우드에서 어떤 칩으로 서빙되는가**가 비용과 지연시간을 결정합니다. 모델 벤치마크 옆에 인프라 지도를 같이 봐야 하는 시대입니다.

---

## 업데이트 — 4월 20·24 Anthropic 메가딜

이 글을 올린 직후, Anthropic 쪽 숫자가 또 한 단계 올라갔습니다.

**4월 20일 — Amazon $250억 추가 투자**

기존 $80억 위에 Amazon이 **추가로 최대 $250억**을 투입한다고 발표했습니다. 대가는 명확합니다. Anthropic이 향후 10년간 **AWS에 $1,000억+ 지출**을 약정했고, **최대 5GW 신규 컴퓨트**를 추가로 받습니다. 본문의 Project Rainier 위에 또 한 층이 얹히는 구조입니다.

**4월 24일 — Google 최대 $400억**

며칠 뒤 Google이 **즉시 $100억 + 추가 최대 $300억** 투자를 공개했습니다. 동시에 Google Cloud가 **향후 5년 5GW TPU 용량**을 공급합니다. 본문에서 본 100만 TPU 계약 위에 5GW가 또 올라가는 셈입니다.

두 발표를 합치면 Anthropic이 일주일 만에 컴퓨트 측에서만 **10GW에 가까운 신규 용량**을 확보했습니다. OpenAI Stargate 10GW와 같은 자릿수입니다. "분산 헤지"를 택했던 Anthropic이 결과적으로 OpenAI에 견줄 만한 절대 규모로 올라섰다는 게 이번 발표들의 의미입니다.

칩 다변화도 더 굳어졌습니다. Anthropic은 이제 **Trainium(Amazon) + TPU(Google) + GPU(Nvidia)** 세 축을 모두 기가와트급으로 깔게 됩니다. 본문 표의 "공표된 용량"과 "공표된 투자" 행은 이 시점부터 한 단계씩 위로 올려 읽어주시면 됩니다.

[Amazon 추가 $25B (CNBC)](https://www.cnbc.com/2026/04/20/amazon-invest-up-to-25-billion-in-anthropic-part-of-ai-infrastructure.html) · [Google 최대 $40B (TechCrunch)](https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/) · [Anthropic·Amazon 5GW 발표](https://www.anthropic.com/news/anthropic-amazon-compute)
