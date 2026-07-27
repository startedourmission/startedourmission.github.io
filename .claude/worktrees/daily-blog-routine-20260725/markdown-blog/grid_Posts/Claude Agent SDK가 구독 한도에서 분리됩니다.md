---
date: 2026-05-14
tags:
  - 정보
  - LLM
description: "2026년 6월 15일부터 Claude Agent SDK와 claude -p 사용량은 구독 플랜 한도에서 빠지고, 별도의 월간 크레딧으로 분리됩니다. Pro 20달러, Max 5x 100달러, Max 20x 200달러가 자동으로 충전됩니다."
---

[[Anthropic]]이 [[Claude]] 구독 플랜에 새로운 빌링 정책을 들고 왔습니다. 2026년 6월 15일부터 **Claude Agent SDK 사용량과 `claude -p` 명령은 구독 한도에서 빠지고**, 별도의 월간 크레딧으로 따로 청구됩니다. ([공식 안내](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan))

핵심만 먼저 정리하면 이렇습니다.

- Pro·Max·Team·Enterprise 플랜은 매달 SDK 전용 크레딧을 자동으로 받습니다.
- Agent SDK·`claude -p`·GitHub Actions·SDK 기반 외부 앱 호출은 이 크레딧에서만 차감됩니다.
- 터미널/IDE에서의 대화형 [[Claude Code]] 사용, 웹·데스크톱·모바일 채팅은 기존 구독 한도 그대로입니다.

## 어떤 플랜이 얼마를 받나요

크레딧은 플랜에 따라 정해진 금액으로 매달 새로 들어옵니다. 누적되지 않고, 매 청구 주기 시작에 리셋됩니다.

| 플랜 | 월간 SDK 크레딧 |
| --- | --- |
| Pro | $20 |
| Max 5x | $100 |
| Max 20x | $200 |
| Team (Standard) | $20 |
| Team (Premium) | $100 |
| Enterprise (usage-based) | $20 |
| Enterprise (seat-based Premium) | $200 |

seat-based Enterprise의 Standard seat는 크레딧 대상이 아닙니다. 그리고 [Claude Developer Platform](https://console.anthropic.com)의 API 키로 SDK를 쓰는 사람은 크레딧을 따로 받지 않습니다 — 기존대로 pay-as-you-go가 유지됩니다.

크레딧을 받으려면 Claude 계정에서 **한 번만** opt-in하면 됩니다. 그 다음부터는 청구 주기마다 자동으로 갱신됩니다.

## 무엇에 적용되나요

크레딧이 빠지는 항목은 정확히 네 가지입니다.

- 본인 프로젝트에서의 [[Claude Agent SDK]] 사용 (Python·TypeScript)
- Claude Code의 `claude -p` 명령 (비대화형 모드)
- Claude Code [GitHub Actions](https://github.com/anthropics/claude-code-action) 연동
- Agent SDK로 사용자의 Claude 구독을 인증해 동작하는 서드파티 앱

반대로 크레딧이 적용되지 않는 항목, 즉 **여전히 구독 한도에서 차감되는** 항목은 다음과 같습니다.

- 터미널·IDE에서의 *대화형* Claude Code
- 웹·데스크톱·모바일 Claude 채팅
- Claude Cowork
- extra usage를 끌어다 쓰는 다른 기능들

핵심은 *대화형(interactive)* 과 *자동화(automation)* 가 이제 별도의 주머니에서 빠진다는 것입니다.

## 크레딧이 떨어지면

월 크레딧을 다 쓰면 Agent SDK 호출은 두 가지 경로 중 하나로 갑니다.

- *extra usage가 켜져 있다면* — 표준 API 요율로 추가 청구가 시작됩니다.
- *extra usage가 꺼져 있다면* — 크레딧이 갱신될 때까지 SDK 요청이 **그냥 멈춥니다**.

자동화 파이프라인을 돌리는 입장에서는 두 번째 경로가 운영 위험입니다. cron으로 매시간 도는 작업이 월 중반부터 조용히 죽어 있을 수 있다는 뜻이니까요. 운영 자동화를 돌릴 거면 extra usage를 켜 두든지, 아예 API 키로 옮기든지 둘 중 하나를 결정해 두는 게 안전합니다.

또 하나 — 크레딧은 **개인 단위**입니다. Team이나 Enterprise라도 팀원끼리 풀로 모아 쓸 수 없습니다. 각자 자기 크레딧을 따로 claim합니다.

## 왜 지금 이렇게 바꾸나요

표면적 메시지는 "더 자유롭게 Agent SDK를 써 보세요"입니다. 그런데 정책 디자인을 보면 Anthropic이 풀려는 문제가 셋으로 보입니다.

**첫째, 대화형 한도와 자동화의 충돌을 끊습니다.** 그동안 `claude -p`를 cron이나 [GitHub Actions](https://docs.claude.com/en/docs/claude-code/github-actions)에 걸어 두면 그게 본인의 5시간 단위 사용량을 갉아먹어, 정작 터미널에서 대화하려 할 때 한도에 막히는 일이 흔했습니다. 자동화와 대화를 분리하면 두 사용 모드가 서로를 죽이지 않게 됩니다.

**둘째, 서드파티 SDK 생태계를 키웁니다.** 외부 앱이 사용자의 Claude 구독을 인증해 동작하는 경로가 크레딧 대상에 포함됐습니다. 즉 [[MCP]] 서버나 Agent SDK 기반 도구들이, 사용자의 구독 한도를 직접 까먹지 않고 별도 크레딧을 통해 호출될 수 있습니다. 일반 사용자가 OS·IDE 곳곳에 Claude 기반 자동화를 깔아 두는 시나리오를 권장하는 그림입니다.

**셋째, 실제 운영 트래픽은 API로 보냅니다.** 안내문이 짚어 두는 부분이 중요합니다.

> "The Agent SDK monthly credit is sized for individual experimentation and automation. Teams running shared production automation should use the Claude Developer Platform with an API key for predictable pay-as-you-go billing."

크레딧 액수는 *개인의 실험과 자동화* 규모로 설계됐다는 명시적 선언입니다. Max 20x의 200달러는 개인 헤비 유저 1인의 자동화 비용으로는 충분하지만, 팀의 공동 프로덕션 파이프라인을 굴리기에는 작습니다. 헤비 트래픽은 API로 가라는 신호입니다. Anthropic 입장에서는 (1) 개인 실험 비용을 흡수해 SDK 채택을 늘리고, (2) 진짜 매출은 API에서 회수하는 깔끔한 두 단계 구조입니다.

## 실제로는 어떻게 바뀌나요

본인의 사용 패턴이 어떤 그룹에 속하느냐에 따라 체감은 다릅니다.

**자동화를 거의 안 쓰는 사람** — 바뀌는 게 거의 없습니다. 구독 한도가 그대로니 그냥 평소처럼 쓰면 됩니다.

**가끔 `claude -p`를 쓰는 사람** — 작은 자동화(저녁마다 블로그 점검 cron, 가벼운 스크립트)는 Pro 20달러 크레딧으로 거의 다 커버됩니다. 그동안 한도가 빠듯하다고 느끼던 사람들은 오히려 여유가 생깁니다.

**Agent SDK로 진지하게 자동화를 돌리는 사람** — Max 20x의 200달러가 한 달치 자동화 비용을 다 커버할지 직접 계산해 봐야 합니다. 200달러는 표준 API 요율로 환산하면 [[Claude]] Sonnet 호출 기준으로는 의외로 빨리 소진될 수 있는 금액이라, extra usage를 켜 두는 게 사실상 필수가 됩니다.

**팀의 프로덕션 파이프라인을 굴리는 사람** — 메시지대로 API 키로 옮기는 게 맞습니다. 멤버 각자에게 200달러 크레딧이 따로 충전된다 해도, 공유 자동화는 풀로 묶을 수 없으니 결국 운영이 복잡해집니다.

## 정리

이 변경은 빌링 구조 개편처럼 보이지만, 본질적으로는 *"대화형 Claude와 자동화 Claude를 다른 제품으로 분리한다"* 는 신호로 읽힙니다. 같은 모델을 호출하지만, 결제 주머니와 운영 모드가 다른 두 가지로 갈라지는 것이죠.

해야 할 일은 단순합니다. 2026년 6월 15일 이전까지는 그대로 두고, 그 시점에 Anthropic에서 오는 안내 이메일을 받으면 한 번 opt-in합니다. 자동화 작업이 많은 사람이라면 extra usage 토글을 같이 점검해 두면 됩니다.
