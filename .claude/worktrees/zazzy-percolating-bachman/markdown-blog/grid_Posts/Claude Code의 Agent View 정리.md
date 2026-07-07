---
date: 2026-05-13
tags:
  - 정보
  - 오픈소스
description: "Anthropic이 2026-05-11에 Research Preview로 공개한 Claude Code의 Agent View 기능을 처음부터 끝까지 정리합니다. 다중 세션 대시보드, 백그라운드 실행, 상태 아이콘, 단축키, worktree 격리, supervisor 프로세스, 한계까지 모두 다룹니다."
---

Claude Code를 여러 개 띄워서 일을 시켜본 분이라면 한 번쯤 겪어봤을 겁니다. 탭이 7개쯤 열려 있는데 어느 탭이 입력을 기다리고 있고, 어느 탭이 아직 도구를 돌리고 있고, 어느 탭이 PR을 이미 올렸는지 도무지 모르겠는 상황. tmux 그리드를 짜보기도 하고, 화면을 4분할 해보기도 하지만 결국엔 마우스를 들고 일일이 확인하게 됩니다.

[[Anthropic]]이 2026년 5월 11일에 공개한 **Agent View**는 정확히 이 문제를 푸는 기능입니다. 모든 Claude Code 세션을 한 화면에서 관리하고, 백그라운드로 돌리고, 필요할 때만 들어가게 해주는 대시보드죠. 출시 당시 Research Preview 단계이며 v2.1.139 이상에서만 작동합니다.

이 글에서는 Agent View가 정확히 어떤 기능인지, 어떻게 쓰는지, 그리고 백그라운드에서 어떻게 동작하는지까지 공식 문서를 토대로 자세히 정리해봅니다.

## Agent View가 해결하려는 문제

지금까지 Claude Code 사용 패턴은 대체로 이랬습니다. 터미널 탭을 열고 `claude`를 실행하고, 한 가지 일을 시키고, 끝날 때까지 기다리거나 다른 탭으로 가서 또 다른 일을 시킵니다. 병렬로 일을 시키는 건 가능하지만 **상태를 한눈에 보는 수단이 없었습니다.**

- 이 탭은 입력을 기다리고 있나, 아니면 도구를 돌리는 중인가
- 저 탭은 PR을 올렸나, 아직 코드만 짜고 있나
- 30분 전에 시켰던 그 작업은 어떻게 됐지

Agent View는 이걸 표(table) UI 하나로 묶습니다. 각 행은 세션 하나이고, 상태 아이콘이 즉시 무슨 상황인지 알려줍니다. 그리고 결정적으로 — **세션이 터미널에 붙어있지 않아도 백그라운드에서 계속 돕니다.** 터미널을 닫아도, 다른 작업을 하고 있어도 세션은 살아있습니다.

> 공식 문서 표현 그대로 옮기면 *"Dispatch new sessions, watch their state at a glance instead of scrolling through transcripts, and step in only when one needs you."*

## 빠른 시작

먼저 버전을 확인합니다.

```bash
claude --version
```

`2.1.139` 이상이어야 합니다. 그다음 셸에서:

```bash
claude agents
```

이게 Agent View의 진입점입니다. 처음 열면 아래쪽에 입력창이 있고 위쪽 표는 비어 있습니다. 입력창에 프롬프트를 치고 Enter를 누르면 백그라운드 세션이 시작되고 표에 한 줄이 추가됩니다. 여러 개를 차례로 입력하면 그만큼 병렬로 돕니다.

표에서 행을 골라 `Space`를 누르면 그 세션이 지금 뭘 하고 있는지 보여주는 **peek 패널**이 열립니다. 거기서 바로 답글을 쓰고 Enter를 칠 수 있죠. 전체 대화가 보고 싶으면 `Enter` 또는 `→`로 **attach** 하면 됩니다. 그러면 평소 `claude`를 실행한 것과 똑같은 인터랙티브 세션이 됩니다. 빈 프롬프트에서 `←`를 누르면 다시 표로 돌아옵니다.

세션을 끝낼 일이 없으면 Agent View를 그냥 `Esc`로 닫아도 세션은 계속 돕니다. 이게 핵심입니다.

## 세션 표 읽는 법

Agent View 표는 상태별로 그룹핑됩니다. 입력을 기다리는 세션이 위로, 작업 중이거나 완료된 세션이 아래로 정렬됩니다. 공식 문서가 보여주는 예시는 이렇게 생겼습니다.

```text
Pinned
  ✽ clawd walk cycle          Write assets/sprites/clawd-walk.png           3m

Ready for review
  ∙ jump physics              github.com/anthropics/example/pull/2048       2h

Needs input
  ✻ power-up design           needs input: double jump or wall climb?       1m

Working
  ✽ collision detection       Edit src/physics/CollisionSystem.ts           2m
  ✢ playtest level 3          run 12 · all checkpoints cleared           in 4m

Completed
  ✻ title screen              result: menu, options, and credits done       9m
  ∙ sound effects             result: 14 SFX exported to assets/audio       4h
  … 6 more
```

게임 개발 예시인데, 한눈에 무슨 일이 벌어지고 있는지 보입니다. PR이 올라간 세션은 `github.com/...` 링크와 CI 체크 상태까지 행에 표시됩니다. 대부분의 경우 결과를 확인하는 자리는 바로 이 행입니다 — 굳이 attach 할 필요 없이 PR 머지 화면으로 가면 됩니다.

### 상태 아이콘과 색깔

각 행 앞의 아이콘은 두 가지 정보를 담고 있습니다. **색깔(또는 애니메이션)은 세션의 상태**, **모양은 프로세스가 살아있는지 여부**입니다.

상태 표는 공식 문서 그대로 정리하면:

| 표시 | 상태 | 의미 |
|------|------|------|
| 애니메이션 | Working | Claude가 도구를 돌리거나 응답을 생성 중 |
| 노랑 | Needs input | 권한 결정이나 답변을 기다리는 중 |
| 흐림(dimmed) | Idle | 특정 질문에 막힌 건 아니지만 입력 대기 |
| 초록 | Completed | 작업 성공적으로 완료 |
| 빨강 | Failed | 에러로 종료 |
| 회색 | Stopped | `Ctrl+X` 또는 `claude stop`으로 중단됨 |

모양은 세 가지입니다.

- `✻` 또는 작업 중인 애니메이션 `✽` — 프로세스가 살아있는 상태. 바로 답글 가능.
- `∙` — 프로세스는 종료됐지만 transcript는 남아있는 상태. peek·reply·attach 모두 가능하며, 그 순간 Claude가 새 프로세스를 띄워서 이어갑니다.
- `✢` — `/loop` 세션이 다음 반복을 기다리며 자고 있는 상태. 행에 run 카운트와 다음 실행까지 남은 시간이 함께 표시됩니다.

### Peek 패널의 진짜 가치

`Space`를 눌러 여는 peek 패널이 Agent View의 진짜 가치라고 봐도 됩니다. **transcript 전체를 열지 않고도 세션의 최근 출력, PR 링크, 막혀있는 질문까지 확인할 수 있습니다.**

세션이 객관식 질문을 던져두고 막혀있을 때는 peek 패널에 선택지가 그대로 표시되고, 숫자 키 하나로 답할 수 있습니다. 다른 종류로 막혀있다면 `Tab`을 눌러 추천 답변을 채워넣을 수도 있고, `!` 접두어로 Bash 명령을 보낼 수도 있습니다. `↑`·`↓`로 인접 세션을 빠르게 훑어볼 수도 있죠.

대부분의 일은 여기서 끝납니다. transcript를 열어볼 필요가 거의 없습니다.

### 행의 한 줄 요약은 어떻게 만들어지나

각 행에 보이는 한 줄 요약(`Write assets/...`, `needs input: double jump or wall climb?` 같은 문구)은 사용자가 설정한 **Haiku 클래스 모델이 자동 생성**합니다. 작업 중일 때는 최대 15초에 한 번, 그리고 매 턴이 끝날 때 한 번 갱신됩니다.

이 갱신은 사용자의 일반 provider를 거쳐 짧은 Haiku 요청 한 번으로 처리되며, 청구도 데이터 정책도 본 세션과 동일하게 적용됩니다. 그러니까 *행 요약 한 줄에도 토큰이 소진된다*는 점은 알아두는 게 좋습니다.

## 세션을 띄우는 세 가지 방법

세션 시작 경로는 셋입니다. 각각 쓰임이 다릅니다.

### 1. Agent View 안에서 — `Enter`

표 아래 입력창에 프롬프트를 쓰고 Enter. 가장 일반적인 경로입니다. 입력에는 몇 가지 prefix·mention 문법이 작동합니다.

| 입력 | 효과 |
|------|------|
| `<agent-name> <prompt>` | 첫 단어가 서브에이전트 이름이면 그 서브에이전트가 메인 에이전트로 실행 |
| `@<agent-name>` | 위와 같지만 명시적 |
| `@<repo>` | Agent View를 연 디렉토리 아래의 리포지토리 이름을 mention하면 거기서 세션 실행 |
| `/<skill>` | 스킬을 dispatch |
| `#<번호>` 또는 PR URL | 이미 그 PR을 작업 중인 세션이 있으면 새로 띄우지 않고 선택 |
| `Shift+Enter` | dispatch 하면서 즉시 attach |

입력창에서 `Tab`을 누르면 사용 가능한 서브에이전트 목록을 훑어볼 수 있습니다. 같은 이름이 서브에이전트와 형제 리포지토리에 둘 다 있으면 **서브에이전트가 우선**입니다. 명시적으로 리포지토리를 지목하려면 `@` 형식을 쓰면 됩니다.

스크린샷이나 다이어그램이 필요하면 입력창에 이미지를 붙여넣을 수도 있습니다.

### 2. 인터랙티브 세션 안에서 — `/bg`

이미 `claude`를 켜놓고 작업하다가, 이건 시간이 좀 걸릴 것 같으니 백그라운드로 던지고 다른 일을 하고 싶을 때가 있습니다. 그럴 땐 세션 안에서:

```
/background
```

또는 짧은 별칭으로:

```
/bg
```

추가로 한 마디 시킬 게 있으면 `/bg run the test suite and fix any failures` 같이 프롬프트를 함께 넘기면 그 메시지를 마지막으로 보내고 백그라운드로 빠집니다.

빈 프롬프트에서 `←`를 누르는 것도 같은 효과를 냅니다. 현재 세션이 백그라운드로 가고 Agent View가 그 세션을 선택한 상태로 열립니다. 이 단축키가 마음에 안 들면 `/config`에서 끌 수 있습니다.

### 3. 셸에서 직접 — `claude --bg`

터미널에서 처음부터 백그라운드로 시작하고 싶을 때:

```bash
claude --bg "investigate the flaky SettingsChangeDetector test"
```

특정 서브에이전트를 메인으로 띄우려면 `--agent`를 함께:

```bash
claude --agent code-reviewer --bg "address review comments on PR 1234"
```

백그라운드로 들어가면 짧은 ID와 함께 관리 명령이 출력됩니다.

```text
backgrounded · 7c5dcf5d
  claude agents             list sessions
  claude attach 7c5dcf5d    open in this terminal
  claude logs 7c5dcf5d      show recent output
  claude stop 7c5dcf5d      stop this session
```

이 ID로 다른 터미널·스크립트에서도 같은 세션을 다룰 수 있습니다.

## 파일 편집 격리 — worktree로 자동 분리

여러 세션이 같은 리포지토리에서 동시에 일하면 충돌이 나는 게 정상입니다. 두 세션이 같은 파일을 동시에 고치면 한쪽 변경이 묻혀버리겠죠. Agent View는 이걸 worktree로 자동으로 풉니다.

**모든 백그라운드 세션은 시작은 사용자의 working directory에서 하지만, 거기에 쓰기는 막혀있습니다.** Claude가 파일 편집이 필요한 순간이 오면, 자동으로 `.claude/worktrees/` 아래 격리된 git worktree로 세션을 옮깁니다. 그래서 병렬 세션들은 같은 체크아웃을 읽지만 각자 자기 worktree에만 씁니다.

다만 이 격리에는 예외가 있습니다.

- 세션이 이미 worktree 안에서 시작된 경우
- working directory가 git 저장소가 아닌 경우
- working directory 바깥으로의 쓰기

**중요한 함정**: worktree는 세션을 지우면 함께 사라집니다. 살리고 싶은 변경이 있다면 **세션을 삭제하기 전에 머지하거나 푸시해야** 합니다. 세션의 worktree 경로는 peek 패널에서 보거나, attach 해서 working directory를 확인하면 알 수 있습니다.

서브에이전트별로 항상 worktree에서 돌게 만들고 싶다면, 서브에이전트 frontmatter에 `isolation: worktree`를 추가하면 됩니다.

## 백그라운드 세션은 어떻게 살아남는가 — supervisor 프로세스

Agent View의 마법은 supervisor 프로세스가 깔립니다. 이 부분이 기술적으로 가장 흥미로운데, 동작 원리를 알고 있으면 디버깅도 쉬워집니다.

작동 방식을 정리하면 이렇습니다.

**1. supervisor는 사용자당 하나, 자동으로 뜬다.** 백그라운드 세션을 처음 만들거나 Agent View를 처음 열 때 supervisor가 시작됩니다. 직접 관리할 필요는 없습니다. 인터랙티브 세션과 동일한 자격 증명을 쓰고, 모델 API 외에 추가 네트워크 연결은 만들지 않습니다.

**2. 세션은 각자의 프로세스다.** 백그라운드 세션 각각은 별도의 Claude Code 프로세스이고, 사용자 터미널이 아니라 supervisor의 자식 프로세스입니다. 그래서 터미널을 닫아도 세션이 죽지 않습니다.

**3. 1시간 유휴 시 프로세스만 잠재운다.** 작업이 끝난 세션이 한 시간 정도 누구도 들여다보지 않으면 supervisor는 프로세스를 정리해서 리소스를 회수합니다. 단 transcript와 state는 디스크에 남아있고, peek·reply·attach 하는 순간 supervisor가 새 프로세스를 띄워서 이어갑니다. 사용자 입장에서는 끊김이 없습니다.

**4. 자동 업데이트도 자연스럽게.** supervisor는 디스크의 Claude Code 바이너리를 감시해서, auto-updater가 새 버전으로 교체하면 supervisor 자체도 새 버전으로 재시작합니다. 백그라운드 세션은 detached 프로세스라 그 와중에도 계속 돌고, 새 supervisor가 다시 잡아갑니다.

**5. state는 config 디렉토리에 저장된다.**

| 경로 | 내용 |
|------|------|
| `~/.claude/daemon.log` | supervisor 로그 |
| `~/.claude/daemon/roster.json` | 재시작 후 재연결용 세션 목록 |
| `~/.claude/jobs/<id>/state.json` | 세션별 state, Agent View가 표시하는 데이터 |

`CLAUDE_CONFIG_DIR` 환경변수를 설정하면 supervisor도 그 디렉토리를 쓰고, 사실상 별도 인스턴스로 분리됩니다.

**6. 머신이 자거나 꺼지면 멈춘다.** 백그라운드 세션은 사용자 머신에서 도는 로컬 프로세스라 sleep·shutdown은 못 버팁니다. 다음에 깨어났을 때 그 세션들은 stopped 상태로 표시되며, peek·attach·reply 하는 순간 어디서 멈췄든 그 지점부터 재개됩니다. 전부 한 번에 재시작하려면:

```bash
claude respawn --all
```

## 단축키 정리

자주 쓰는 것들만 추리면.

| 단축키 | 동작 |
|--------|------|
| `↑` `↓` | 행 이동 |
| `Enter` | 선택 행에 attach (입력창에 텍스트가 있으면 dispatch) |
| `Space` | peek 패널 열기·닫기 |
| `Shift+Enter` | dispatch 후 즉시 attach |
| `→` | 선택 행에 attach |
| `Alt+1`~`Alt+9` | 포커스된 그룹의 N번째 세션에 attach |
| `Tab` | 서브에이전트 둘러보기 또는 추천 적용 |
| `Ctrl+S` | 그룹핑을 state ↔ directory로 토글 |
| `Ctrl+T` | 선택 세션 pin/unpin |
| `Ctrl+R` | 선택 세션 이름 변경 |
| `Ctrl+G` | dispatch 프롬프트를 `$EDITOR`로 열기 |
| `Ctrl+X` | 세션 stop (2초 안에 또 누르면 delete) |
| `Shift+↑` `Shift+↓` | 선택 세션 순서 바꾸기 |
| `Esc` | peek 닫기 / 입력 비우기 / 종료 |
| `Ctrl+C` | 입력 비우기 (두 번 누르면 종료) |
| `?` | 전체 단축키 보기 |

표가 길어지면 입력창에 필터를 칠 수도 있습니다. `a:code-reviewer` 같이 특정 서브에이전트만, `s:blocked` 같이 막힌 세션만, `#2048`이나 PR URL로 그 PR을 작업하는 세션만 추릴 수 있습니다.

## 셸에서 직접 다루기 — 스크립트용

Agent View를 안 열고도 셸에서 짧은 ID로 세션을 다룰 수 있습니다. 스크립트로 묶거나, GUI 안 열고 빠르게 한 줄 처리할 때 유용합니다.

| 명령 | 용도 |
|------|------|
| `claude agents` | Agent View 열기 |
| `claude attach <id>` | 그 세션에 attach |
| `claude logs <id>` | 최근 출력 출력 |
| `claude stop <id>` | 세션 중단 (별칭 `claude kill`) |
| `claude respawn <id>` | 중단된 세션을 대화 그대로 재시작 |
| `claude respawn --all` | 모든 중단된 세션 재시작 |
| `claude rm <id>` | 목록에서 세션 제거 |

## 권한 모드는 어떻게 적용되나

조금 미묘한 부분입니다. dispatch 된 세션의 [settings](https://code.claude.com/docs/en/settings)와 [권한 모드](https://code.claude.com/docs/en/permissions)는 **세션이 실행되는 디렉토리** 기준으로 읽힙니다. 즉 그 디렉토리에서 그냥 `claude`를 친 것과 같습니다.

Agent View의 입력창에서 dispatch 할 때는 권한 모드를 따로 전달하지 않습니다. 그래서 해당 디렉토리 settings의 `defaultMode` 또는 dispatch 된 서브에이전트 frontmatter의 `permissionMode`가 적용됩니다.

셸에서 모드를 명시하려면 `--permission-mode` 플래그를 `claude --bg`와 함께 쓰면 되는데, 여기서 한 가지 안전장치가 있습니다. **`bypassPermissions`나 `auto` 모드는 인터랙티브 세션에서 한 번이라도 그 모드를 수락한 적이 있어야** `--bg`로 쓸 수 있습니다. 사용자가 지켜보지 않는 세션이 승인 없이 행동하는 걸 막기 위한 장치입니다.

이건 합리적인 선택이라고 봅니다. 백그라운드 + 무제한 권한 조합은 사고가 나기 딱 좋은 조건이라 한 번이라도 명시적 수락을 강제하는 게 맞습니다.

## 한계와 주의점

공식 문서가 명시한 한계는 셋입니다.

**Rate limit는 그대로 적용됩니다.** 백그라운드 세션도 인터랙티브 세션과 똑같이 구독 quota를 씁니다. 10개를 병렬로 돌리면 1개를 돌릴 때의 10배 속도로 quota가 줄어듭니다. 게다가 각 행의 한 줄 요약도 Haiku 호출이라 별도로 토큰이 들죠.

**세션은 로컬입니다.** 사용자 머신에서 도는 프로세스라, 머신이 자거나 꺼지면 멈춥니다. 클라우드 환경에서 도는 게 아닙니다. 24시간 도는 게 필요하다면 [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)을 봐야 합니다.

**worktree는 세션과 함께 사라집니다.** 다시 강조하는데, 세션을 삭제하기 전에 worktree의 변경을 머지하거나 푸시해야 합니다. 안 그러면 그냥 사라집니다.

추가로 알아두면 좋은 것들.

- Research Preview 단계라 인터페이스와 단축키는 바뀔 수 있습니다.
- 관리자는 organization 차원에서 `disableAgentView` managed setting으로 끌 수 있습니다.
- 개인이 끄려면 `disableAgentView: true`를 settings에 넣거나 `CLAUDE_CODE_DISABLE_AGENT_VIEW` 환경변수를 설정합니다.
- 같은 세션 안에서 도는 [서브에이전트](https://code.claude.com/docs/en/sub-agents)는 별도의 행으로 나오지 않습니다. 부모 세션 행 하나로 묶입니다.

## 어떤 워크플로에 가장 잘 맞을까

문서를 읽고 나서 든 생각인데, Agent View가 진가를 발휘하는 상황은 대략 이런 패턴 같습니다.

**서로 독립적인 작업 여러 개를 동시에 던지는 패턴.** 버그 수정 1개, PR 리뷰 1개, 로그 조사 1개 — 서로 코드 충돌이 안 나고 결과가 독립적인 작업들. 이건 Agent View가 가장 잘 푸는 케이스입니다. worktree 격리 덕에 충돌 걱정 없이 병렬화할 수 있죠.

**오래 걸리는 작업을 백그라운드로 빼두는 패턴.** 큰 테스트 스위트를 돌려서 실패를 고치는 일이라거나, 전체 의존성 업데이트라거나. `/bg`로 던져두고 다른 일을 하다가, peek로 잠깐 상황만 확인하고, 끝나면 PR 머지하면 됩니다.

**`/loop` 세션을 깔아두는 패턴.** 5분마다 CI 상태를 확인하거나, 새로 올라온 PR을 검토하는 루프를 깔아두고 결과만 받아보는 식. `✢` 아이콘으로 표시되는 그 카운트다운이 바로 이런 용도죠.

반대로 **하나의 문제를 깊게 같이 풀어가는 패턴**이라면 굳이 Agent View를 쓸 이유가 없습니다. 그냥 `claude`로 인터랙티브 세션을 띄워서 같이 작업하는 게 낫습니다. 공식 문서도 그렇게 명시합니다 — *"When you want to work through a problem together, attach to a session and use Claude Code interactively as usual."*

## 정리

Agent View를 한 줄로 요약하면, **"Claude Code를 병렬로 부리는 사람을 위한 컨트롤 타워"** 입니다. 핵심은 세 가지죠.

1. 세션이 터미널에 묶여있지 않다 — supervisor 프로세스 덕에 백그라운드로 살아남음
2. 모든 세션을 한 표에서 본다 — 상태 아이콘과 peek 패널로 transcript 안 열고도 파악
3. 동시 편집 충돌을 worktree로 자동 격리한다 — 사용자가 손댈 일 거의 없음

Research Preview라 단축키나 UI는 계속 바뀔 가능성이 있으니, 익숙해진 단축키를 너무 의존하지는 마시고요. 그래도 핵심 모델 — 백그라운드 세션 + supervisor + worktree 격리 — 은 꽤 잘 짜여 있어서 큰 골격은 유지될 것 같습니다.

직접 써보려면 `claude --version`으로 v2.1.139 이상인지 확인하고, 그냥 `claude agents`를 치면 됩니다. 첫 화면이 비어 있어도 놀라지 마세요 — 첫 세션을 dispatch 하기 전엔 그게 정상입니다.

## 참고

- [Manage multiple agents with agent view (공식 문서)](https://code.claude.com/docs/en/agent-view)
- [Agent view in Claude Code (Anthropic 블로그)](https://claude.com/blog/agent-view-in-claude-code)
- [Run agents in parallel](https://code.claude.com/docs/en/agents)
- [Subagents 문서](https://code.claude.com/docs/en/sub-agents)
- [Worktrees 문서](https://code.claude.com/docs/en/worktrees)
