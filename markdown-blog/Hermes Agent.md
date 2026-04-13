---
date: 2026-04-11
tags:
  - 정보
  - LLM
  - 오픈소스
description: "Nous Research의 Hermes Agent — 스스로 배우고 성장하는 오픈소스 AI 에이전트. 5단계 메모리, 자동 스킬 생성, 6개 실행 백엔드, 40+ 도구를 갖춘 로컬 퍼스트 에이전트 프레임워크."
---

요즘 AI 에이전트 하면 Claude Code, Cursor, Copilot 같은 IDE 내장형이나, ChatGPT/Claude 같은 API 래퍼를 떠올립니다. Hermes Agent는 둘 다 아닙니다.

[[Nous Research]]가 2026년 2월에 공개한 Hermes Agent는 **"여러분의 서버에 살면서, 배운 것을 기억하고, 오래 쓸수록 더 잘하는"** 에이전트입니다. IDE에 붙어있지 않고, 특정 API에 종속되지 않고, 텔레그램이든 디스코드든 슬랙이든 이메일이든 어디서나 대화할 수 있습니다. GitHub 스타 53.4k, 포크 7k. MIT 라이선스.

> GitHub: [NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent)
> 공식 사이트: [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/)

---

## 다른 에이전트와 뭐가 다른가

가장 큰 차이는 **학습 루프**입니다.

Claude Code나 Cursor는 세션이 끝나면 학습한 것이 사라집니다. 다음 세션에서 같은 문제를 만나면 처음부터 다시 풀어야 합니다. 메모리 기능이 추가되고 있지만, 대부분 사용자의 선호도를 기억하는 수준입니다.

Hermes Agent는 다릅니다. 복잡한 작업을 해결하면 그 과정을 **스킬 문서(SKILL.md)**로 자동 생성합니다. 다음에 비슷한 작업이 오면 스킬을 불러와서 바로 적용합니다. 같은 유형의 작업을 10-20번 처리하면 스킬이 2-3배 개선된다고 합니다. "Observe → Plan → Act → Learn"의 닫힌 학습 루프입니다.

그리고 **모델에 구애받지 않습니다**. Nous Research의 자체 모델(Hermes 3, Hermes 4)뿐만 아니라 OpenRouter(200+ 모델), OpenAI, Anthropic, 커스텀 엔드포인트를 `hermes model` 명령 하나로 바꿀 수 있습니다. $5짜리 VPS에서 8B 모델로 돌려도 되고, 클라우드에서 405B로 돌려도 됩니다.

---

## 5단계 메모리 아키텍처

Hermes Agent의 메모리는 5개 계층으로 구성됩니다.

| 계층 | 역할 | 예시 |
|---|---|---|
| **단기 추론 메모리** | 현재 세션의 트랜스포머 컨텍스트 | 지금 대화 내용 |
| **절차적 스킬 문서** | 작업 완료 후 자동 생성되는 SKILL.md | "프로덕션 배포 + 롤백 절차" |
| **컨텍스트 영속성** | 벡터 스토어에 스킬을 인덱싱, 관련 스킬 검색 | "배포 관련 스킬 3개 로드" |
| **사용자 모델링 (Honcho)** | 비동기적으로 사용자에 대한 사실 추론 | "이 사용자는 TypeScript 선호, Jest 사용" |
| **전문 검색 (FTS5)** | SQLite 기반, 과거 세션 검색 | "지난 화요일에 뭐 했지?" |

8개 외부 메모리 프로바이더 플러그인(Honcho, Mem0, Hindsight, Holographic 등)도 지원합니다. 지식 그래프, 시맨틱 검색, 자동 팩트 추출 같은 고급 기능을 추가할 수 있습니다.

핵심은 이겁니다: **프롬프트에 모든 가능한 도구를 때려넣지 않습니다.** 관련 스킬만 필요할 때 로드합니다. 토큰 사용량과 비용이 대폭 줄어듭니다.

---

## 스킬 시스템과 agentskills.io

스킬 문서는 이런 형태입니다:

```yaml
---
name: deploy-to-production
description: Safely deploy with rollback support
license: Apache-2.0
---

## Steps
1. Run test suite
2. Create tagged release
3. Deploy using script
4. Verify health check
5. Trigger rollback if needed
```

여기서 흥미로운 건 **agentskills.io** 표준입니다. Hermes가 만든 스킬 포맷인데, 이걸 지금 11개 이상의 도구가 채택하고 있습니다. Claude Code, Cursor, GitHub Copilot, Gemini CLI, VS Code, Amp, Goose, Roo Code 등. 에이전트 간에 스킬을 공유할 수 있는 포터블 포맷인 셈입니다.

`/skills` 명령으로 사용 가능한 스킬을 브라우징하고, 커스텀 스킬을 만들 수도 있습니다. 커뮤니티 Skills Hub에서 다른 사람이 만든 스킬을 가져올 수도 있습니다.

---

## 6개 실행 백엔드

| 백엔드 | 용도 | 특징 |
|---|---|---|
| **Local** | 개발 | 시스템 직접 실행 |
| **Docker** | 프로덕션 | 네임스페이스 격리, 권한 축소 |
| **SSH** | 원격 | 세션 간 환경 영속 |
| **Daytona** | 클라우드 개발 | 서버리스 환경 |
| **Singularity** | HPC/연구 | 대규모 연산 워크로드 |
| **Modal** | 서버리스 프로덕션 | 유휴 시 하이버네이트, 세션 간 비용 거의 0 |

설정은 YAML 한 줄(`backend: modal`)입니다. MCP(Model Context Protocol) 서버도 지원하고, 시작 시 자동 탐지합니다.

---

## 멀티 플랫폼 메시징

이게 IDE 에이전트와의 결정적 차이입니다. Hermes Agent는 **게이트웨이**를 통해 어디서든 대화할 수 있습니다.

- 텔레그램
- 디스코드
- 슬랙
- WhatsApp
- Signal
- 이메일
- CLI

자연어로 크론 스케줄링도 가능합니다. "매일 아침 9시에 서버 상태 리포트를 텔레그램으로 보내줘" 같은 걸 설정하면 에이전트가 무인으로 실행합니다.

---

## Hermes 모델: 자체 훈련 파이프라인

Nous Research는 에이전트만 만든 게 아니라 모델도 직접 훈련합니다.

**Hermes 3 (2024년 8월):**
- Llama 3.1 기반 파인튜닝, ~390M 합성 토큰
- SFT + DPO 2단계 훈련
- 함수 호출 정확도 90% (일반 모델 60-70%)
- 8B / 70B / 405B 변형

**Hermes 4 (2025년 8월):**
- `<think>...</think>` 태그로 하이브리드 추론 (최대 16,000 토큰)
- DataForge: 그래프 기반 합성 데이터 생성, 5M 샘플, 60B 토큰 (Hermes 3의 150배)
- AIME'24 벤치마크에서 과도한 추론 78.4% 감소

**Atropos 프레임워크**: 분산 RL 훈련. 비동기 워커 조율, ~1,000개 작업별 검증기로 궤적 필터링. 이것도 오픈소스입니다.

---

## 설치

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
```

Linux, macOS, WSL2, Termux(Android) 지원. 모든 데이터가 로컬에 저장되며, 텔레메트리나 트래킹이 없습니다.

OpenClaw에서 마이그레이션하는 경우:
```bash
hermes claw migrate
```
페르소나, 메모리, API 키, 사용자 생성 스킬이 자동 이전됩니다.

---

## 다른 에이전트와 비교

| | Hermes Agent | Claude Code | OpenClaw |
|---|---|---|---|
| **유형** | 독립 에이전트 | IDE 내장 | 클라우드 게이트웨이 |
| **모델** | 200+ (모델 무관) | Claude만 | 다양 |
| **메모리** | 5계층 영속 | 세션 메모리 + auto memory | 커스텀 |
| **스킬** | 자동 생성 + agentskills.io | CLAUDE.md 수동 | 커스텀 |
| **실행** | 6개 백엔드 | 로컬/클라우드 | 클라우드 |
| **메시징** | 6+ 플랫폼 | CLI/웹 | 다양 |
| **라이선스** | MIT | 상용 | 상용 |
| **GitHub 스타** | 53.4k | - | 247k |

---

## 왜 지금 주목받는가

Hermes Agent가 뜨는 이유는 시기와 맞물려 있습니다.

첫째, **에이전트가 IDE를 벗어나고 있습니다.** 코딩만 하는 에이전트에서 서버를 관리하고, 보고서를 생성하고, 스케줄 작업을 실행하는 에이전트로 확장되고 있습니다. Hermes의 멀티 플랫폼 게이트웨이는 이 확장에 자연스럽게 맞습니다.

둘째, **로컬 퍼스트가 다시 중요해졌습니다.** 클라우드 종속성에 대한 반감, 데이터 주권 이슈, 비용 통제 욕구가 커지면서 "내 서버에서 돌리는 에이전트"의 매력이 커졌습니다. $5 VPS에서도 돌아간다는 건 실질적인 차별화입니다.

셋째, **스킬의 표준화**입니다. agentskills.io가 11개 도구에 채택된 건, 에이전트 생태계가 "하나의 모델/플랫폼에 종속되지 않는 방향"으로 움직이고 있다는 신호입니다. Hermes가 만든 스킬을 Claude Code에서 쓸 수 있다는 건, 개발자 입장에서는 에이전트를 바꿔도 지식이 이전된다는 뜻이니까요.

물론 열린 질문도 있습니다. 자동 생성된 스킬이 쌓이면서 충돌하거나 낡아지지 않을까? Python + Ollama 스택이 로컬 퍼스트의 정답인가? 60B 합성 토큰이 390M 큐레이션된 토큰을 이기는 베팅이 맞을까?

하지만 "스스로 배우고, 기억하고, 어디서든 대화할 수 있는 오픈소스 에이전트"라는 포지셔닝은 지금 시장에서 독보적입니다.
