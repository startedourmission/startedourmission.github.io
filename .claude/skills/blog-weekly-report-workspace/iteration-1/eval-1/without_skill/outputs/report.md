---
date: 2026-06-09
tags:
  - 주간리포트
description: 2026년 6월 2일부터 9일까지 startedourmission 블로그에 게시된 글 20편을 한눈에 정리한 주간 결산
---

# 이번 주 블로그 결산 (2026-06-02 ~ 06-09)

## 한눈에 보기

- **게시 글 20편** + 섹션 인덱스(MOC) 3개 신설
- **논문 리뷰 14편**, 정보·모델 릴리스 글 2편, 인물 사전 4편
- 이번 주를 관통한 큰 줄기 둘
  - **NVIDIA Physical AI 패키지**: Cosmos 3 옴니모달 월드 모델 리뷰 + 그 뒤를 만든 핵심 인물 4명 사전 등록
  - **추론(reasoning)의 한계 정밀 해부**: 더 길게 생각한다고 더 잘하는 게 아니라는 논문이 한 주에만 4편
- Headliner 글 4편: Cosmos 3, MiniMax M3, OpenAI Dreaming V3, The Self-Correction Illusion (사용자 지정)

| 분류 | 편수 |
|------|------|
| 논문 리뷰 (grid_Papers) | 14 |
| 정보·릴리스 (grid_Posts) | 2 |
| 인물 사전 (Dictionary) | 4 |
| **합계** | **20** |
| 신설 섹션 인덱스(MOC) | 3 |

## 요일별 타임라인

### 6/4 (목) — 자기진화 에이전트 3종 + 오픈웨이트 릴리스
- **HLL - Can Agents Cross Humanity's Last Line of Verification** (논문) — CAPTCHA를 "정답 인식"이 아니라 실제 상호작용으로 푸는지로 측정하는 벤치마크. 8개 프런티어 에이전트가 방해·궤적 검증이 들어오면 무너진다.
- **MMG2Skill - Can Agents Distill In-the-Wild Guides into Self-Evolving Skills** (논문) — 위키하우 같은 사람용 가이드를 에이전트용 SKILL.md 절차로 증류하고, 실행 궤적 진단으로 스스로 고치는 폐루프.
- **MetaForge - A Self-Evolving Multimodal Agent that Retrieves, Adapts, and Forges Tools On Demand** (논문) — Decide·Retrieve·Adapt·Forge 4단계로 도구를 언제·어떻게 늘릴지 강화학습으로 함께 학습.
- **MiniMax M3 - 오픈웨이트 프런티어 모델** (정보, Headliner) — 프런티어 코딩 + 1M 컨텍스트 + 네이티브 멀티모달을 한 모델에 담은 첫 오픈웨이트 모델, MSA 희소 어텐션 중심 해부.

### 6/6 (토) — NVIDIA Physical AI 패키지
- **Cosmos 3 - Omnimodal World Models for Physical AI** (논문, Headliner) — 언어·이미지·비디오·오디오·행동을 하나의 Mixture-of-Transformers로 처리. 자기회귀 추론 타워 + 확산 생성 타워로 VLM·비디오 생성기·월드 시뮬레이터·월드 액션 모델을 한 백본에 흡수.
- 인물 사전 4명 (모두 NVIDIA, Cosmos/Physical AI 라인):
  - **Ming-Yu Liu** — NVIDIA Research 부사장, Cosmos Lab 리더
  - **Jim Fan** — AI 디렉터, GEAR Lab 공동 리더, GR00T 공동 책임
  - **Sanja Fidler** — AI 연구 부사장, 토론토 Spatial Intelligence Lab, 3D 비전·월드 모델
  - **Jan Kautz** — Learning and Perception Research 부사장, 컴퓨터비전·생성·효율 딥러닝

### 6/7 (일) — 추론의 한계 + 음성 + 메모리 릴리스
- **Audio Interaction Model** (논문) — 오프라인 오디오 LLM과 스트리밍 모델을 하나의 always-on 모델로. perceive-decide-respond 루프 + SoundFlow 프레임워크.
- **Quantized Reasoning Models Think They Need to Think Longer, but They Do Not** (논문) — 양자화하면 정확도는 떨어지고 CoT는 길어진다. 원인은 사고력이 아니라 "멈추지 못함". 학습 없이 로짓 페널티로 처방 (메타 FAIR).
- **The Deterministic Horizon - When Extended Reasoning Fails and Tool Delegation Becomes Necessary** (논문, ICML 2026) — 긴 CoT가 어느 지점부터 정확도를 무너뜨리는지 정보이론적 용량 한계로 증명. 19~31스텝의 임계점을 넘으면 신경 추론 대신 도구에 위임하라.
- **OpenAI Dreaming V3 - ChatGPT 메모리를 백그라운드에서 합성하는 새 아키텍처** (정보, Headliner) — 저장 메모리 목록을 비동기 백그라운드 합성으로 대체한 OpenAI의 새 메모리 아키텍처.

### 6/8 (월) — 에이전트 평가·메모리·자기교정
- **Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents** (논문) — 새 에이전트를 실제로 굴리지 않고 과거 로그만으로 성능 가늠하는 오프폴리시 평가 ADWM. 월드 모델을 디퓨전으로 세워 네 벤치마크 전 셀에서 양의 순위 상관.
- **Holo3.1 - Fast and Local Computer Use Agents** (논문) — 화면 보고 클릭하는 컴퓨터 유즈 에이전트를 내 기기에서. 0.8B~35B-A3B 확장 + FP8·NVFP4·Q4 GGUF 양자화로 온디바이스 GUI 자동화 첫 본격 출하 (H Company).
- **MARDoc - A Memory-Aware Refinement Agent Framework for Multimodal Long Document QA** (논문) — 수백 페이지 멀티모달 문서 QA. 탐색·정제·반성 세 에이전트가 구조화된 메모리로 소통. 오픈 Qwen3-30B만으로 DocAgent+Claude 3.5 Sonnet과 맞먹고 DocBench 사람 기준선 돌파.
- **ReasoningFlow - Discourse Structures for Understanding LLM Reasoning Traces** (논문) — 추론 트레이스를 8종 노드·14종 엣지 DAG로 파싱. 충격: 오류 스텝의 14.4%만 실제 오답에 인과 기여, 79.6%는 최종 답과 연결조차 안 됨.
- **The Self-Correction Illusion - LLMs Correct Others but Not Themselves** (논문, Headliner) — 자기 추론 오류는 못 고치면서 같은 주장이 외부 출처로 붙으면 잘 고친다. 능력 결함이 아니라 채팅 템플릿 역할 라벨 아티팩트. 라벨만 self→external로 바꾸면 교정률 23~93%p 상승.
- 신설 섹션 인덱스 3개: **Language**(프로그래밍 언어), **Lectures Translate**(대학 강의 번역), **Mastermind**(AI 인물 강연 번역)

### 6/9 (화) — 시스템 비용 + 통계물리
- **Agent Memory - Characterization and System Implications of Stateful Long-Horizon Workloads** (논문) — 에이전트 기억을 정확도가 아니라 시스템 비용으로 처음 해부. 정답 하나 만드는 에너지가 시스템 간 수십 배 차이, 그 비용 대부분이 안 보이는 "기억 구축" 단계에 숨어 있다.
- **Generative Criticality in Large Language Model Temperature Scaling** (논문) — 물리학자들이 LLM temperature를 통계물리 상전이로 해석. 토큰 임베딩을 스핀으로 놓으면 임계온도 근처에서 질서·무질서가 물 끓는점처럼 급변. susceptibility 급첨두·order parameter 붕괴·내재 차원 최소가 같은 지점을 가리킴.

## 이번 주 테마 묶음

### 1. 추론은 길수록 좋은 게 아니다 (4편)
한 주에 같은 메시지가 네 각도로 모였다.
- **Quantized Reasoning** — 양자화 모델은 "멈추지 못해서" 길어진다
- **Deterministic Horizon** — 19~31스텝 넘으면 신경 추론이 무너진다, 도구에 위임하라
- **ReasoningFlow** — 긴 트레이스 안 오류의 대부분은 최종 답과 무관하다
- **Self-Correction Illusion** — 자기 추론 교정 실패는 능력이 아니라 역할 라벨 아티팩트

### 2. NVIDIA Physical AI / 월드 모델 (5편)
- **Cosmos 3** 리뷰 + 그 라인을 만든 **Ming-Yu Liu·Jim Fan·Sanja Fidler·Jan Kautz** 사전 등록. 한 논문 리뷰를 인물 컨텍스트까지 통째로 엮은 패키지 게시.

### 3. 에이전트: 자기진화·평가·메모리 (다수)
- 자기진화/도구 합성: MMG2Skill, MetaForge
- 평가: HLL(능력 벤치마크), ADWM(오프폴리시 평가)
- 메모리·문서: MARDoc, Agent Memory(시스템 비용)
- 온디바이스 실행: Holo3.1

### 4. 모델·제품 릴리스 (2편)
- **MiniMax M3** (오픈웨이트 프런티어), **OpenAI Dreaming V3** (ChatGPT 메모리 새 아키텍처)

## 분류 통계

- **태그 분포(논문 외)**: 에이전트 9, 멀티모달 8, LLM/추론 다수, 강화학습 3, 확산모델·음성·머신러닝 등
- **출처 다양성**: 메타 FAIR, NVIDIA, ICML 2026, UIUC, 톈진대, 에모리·상하이교통대, 국립성공대 등
- **블로그 구조 변화**: 강의·언어·인물 번역 섹션(Lectures Translate, Language, Mastermind) 인덱스가 6/8 신설되어 앞으로의 연재 기반이 마련됨

## 한 줄 회고

이번 주는 "에이전트를 어떻게 더 똑똑하게"보다 **"에이전트의 한계와 비용을 어떻게 정직하게 잴 것인가"**에 무게가 쏠린 한 주였다. 추론 길이의 함정, 자기교정의 착시, 메모리의 숨은 에너지 비용, 오프폴리시 평가까지 — 측정과 진단을 다룬 논문이 많았다. 동시에 NVIDIA Cosmos 3와 인물 패키지로 Physical AI / 월드 모델이라는 큰 흐름을 본격적으로 다루기 시작했다.
