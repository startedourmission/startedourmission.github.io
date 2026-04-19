---
date: 2026-04-05
tags:
  - 정보
  - LLM
description: "2026년 2월, 공개 GitHub 커밋의 4%—하루 약 13만 5천 건—가 Claude Code에 의해 작성됐다. 이게 어떤 의미인지 뜯어봤다."
---

2026년 2월, Anthropic이 공개한 숫자 하나가 눈에 걸렸다.

**공개 GitHub 커밋의 4%. 하루 약 135,000건.**

Claude Code가 실제로 커밋한 수치다. 이걸 어떻게 해석해야 할까. "AI가 코드를 쓴다"는 뉴스는 이제 새롭지 않다. 그런데 이 숫자가 새로운 건, 에이전트가 PR을 열고 리뷰받고 머지되는 전체 흐름을 통과했다는 뜻이기 때문이다. 자동완성이 아니다. 에이전트가 작업 단위를 완수한 것이다.

---

## Sonnet이 Opus를 1.2%p 차이로 쫓아온 의미

Claude Sonnet 4.6의 SWE-bench Verified 점수는 **79.6%**. Opus 4.6은 80.8%. 차이가 1.2%p다.

[[SWE-bench]] Verified는 실제 GitHub 이슈를 AI가 해결하는 능력을 측정한다. 코드 작성, 디버깅, 테스트 통과까지를 포함하는 엔드투엔드 평가다. 여기서 Sonnet이 Opus와 1.2%p 차이라는 건, 코딩 태스크에 한해서 Sonnet과 Opus가 사실상 동급이라는 뜻이다.

그런데 가격은 다르다. Opus 대비 Sonnet의 API 비용은 훨씬 낮다. GitHub이 자사 코딩 에이전트를 Sonnet 4.6으로 구동하기로 한 선택이 이 맥락에서 읽힌다 — Opus급 성능이 필요한 작업을 Sonnet 비용으로 처리할 수 있게 됐다면, 에이전트를 규모 있게 배포하는 경제성이 성립한다.

수학 벤치마크의 변화도 주목할 만하다. 4.5에서 62%였던 수치가 4.6에서 89%로 올랐다. 27%p 점프다. 이건 단순 수학 능력의 향상이 아니라, 복잡한 추론을 요구하는 코드 작성 — 알고리즘, 자료구조, 성능 최적화 — 에서도 신뢰도가 높아졌다는 신호다.

---

## Claude Code가 "어시스턴트"가 아닌 이유

Claude Code는 터미널 기반 에이전트다. IDE 플러그인으로 자동완성해주는 Copilot류와 근본적으로 다르다.

자동완성 도구는 **지금 이 줄 다음에 뭐가 오는가**를 예측한다. Claude Code는 **이 태스크를 완료하려면 어떤 파일을 어떻게 바꿔야 하는가**를 판단한다. 실제로 파일을 열고, 코드를 수정하고, 테스트를 실행하고, 실패하면 원인을 분석해서 다시 시도한다.

이 차이가 135,000 커밋/일이라는 숫자를 만들어낸다. 자동완성은 커밋을 생성하지 않는다. 에이전트는 한다.

**실제로 어떻게 쓰는가**를 보면 더 명확해진다. MCP(Model Context Protocol)로 외부 시스템을 연결하면, Claude Code는 Slack에서 이슈를 읽고, Jira 티켓을 참조하고, 코드를 수정해서 GitHub PR을 올리는 흐름을 자율적으로 처리한다. "PR 올려줘"라는 한 마디가 실제로 PR로 이어진다.

---

## CLAUDE.md와 Skills — 팀 단위로 쓰는 방법

개인 생산성 도구에서 팀 도구로 전환하는 핵심이 두 가지다.

**CLAUDE.md**는 프로젝트 루트에 두는 마크다운 파일이다. 코드베이스의 규칙, 패턴, 금지 사항을 적어두면 Claude Code가 이를 컨텍스트로 읽는다. "테스트 없이 PR 올리지 말 것", "이 디렉토리 구조를 따를 것", "이 라이브러리 쓰지 말 것" 같은 팀 규칙을 자연어로 적으면 에이전트가 지킨다.

**Skills**는 반복되는 작업 패턴을 슬래시 커맨드로 묶는 기능이다. `/deploy`, `/review-pr`, `/run-tests` 같은 커스텀 커맨드를 만들면 복잡한 멀티스텝 작업이 커맨드 하나로 실행된다. 새 팀원도 컨텍스트 없이 동일한 품질의 작업을 수행할 수 있게 된다.

이 두 가지가 팀 전체의 작업 방식을 코드화하는 수단이 된다. "우리 팀이 코드를 이렇게 짠다"는 암묵지가 명시적 규칙으로 변환되고, 에이전트가 그 규칙 안에서 작업한다.

---

## 개발자는 뭘 해야 하나

**지금 당장 써볼 것**: SWE-bench 기준 코딩 태스크에서 Sonnet 4.6이 Opus급이다. 비용 걱정으로 미뤘다면 지금이 시점이다. 실제 버그 수정, 리팩토링, 테스트 작성 — 이 세 가지부터 에이전트에게 맡겨보는 게 가장 빠른 검증이다.

**MCP 연동을 먼저 설계할 것**: 에이전트의 실제 가치는 외부 시스템과 연결될 때 나온다. GitHub, Jira, Slack 중 팀이 가장 많이 쓰는 하나를 골라서 MCP로 연결하는 것부터 시작하면 된다. 연결 자체는 어렵지 않다.

**CLAUDE.md를 팀 온보딩 문서로 쓸 것**: 에이전트를 위해 만드는 컨텍스트 파일이 결국 새 팀원 온보딩 가이드가 된다. 팀 규칙을 자연어로 명시하는 과정이 팀 자체의 암묵지를 정리하는 계기가 된다.

---

하루 135,000 커밋이 AI에 의해 만들어진다는 것은, AI가 코딩의 일부를 한다는 게 아니라 소프트웨어 개발 루프의 일부를 자율적으로 순환하고 있다는 뜻이다. 그 루프에 팀이 어떻게 들어갈지를 설계하는 게 지금 개발 리더가 할 일이다.

---

**Sources**
- [Claude Sonnet 4.6 launches — Help Net Security](https://www.helpnetsecurity.com/2026/02/18/anthropic-claude-sonnet-4-6-release/)
- [Claude Sonnet 4.6 Full Review — LumiChats](https://lumichats.com/blog/claude-sonnet-46-full-review-students-developers-2026)
- [AI Coding Benchmarks 2026 — ByteIota](https://byteiota.com/ai-coding-benchmarks-2026-claude-vs-gpt-vs-gemini/)
- [AI와 함께하는 DevOps: Claude Code로 생산성 10배 높이기 — Medium](https://medium.com/@baramboys0615/ai%EC%99%80-%ED%95%A8%EA%BB%98%ED%95%98%EB%8A%94-devops-claude-code%EB%A1%9C-%EC%83%9D%EC%82%B0%EC%84%B1-10%EB%B0%B0-%EB%86%92%EC%9D%B4%EA%B8%B0-629a2ce68d62)
- [2026년판 AI 프로그래밍: Claude Code + Skills — Velog](https://velog.io/@ken708/claude-code-skills-programming-guide-2026)
