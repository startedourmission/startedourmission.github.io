---
date: 2026-05-22
tags:
  - 정보
description: 구글이 안티그래비티를 쪼갠 이유, 개발자들의 입장, 구글의 생각을 정리했습니다.
---
I/O 2026에서 Antigravity 2.0이 공개됐고, 개발자 커뮤니티가 불타올랐습니다. 다만 욕이 나오는 표면적 이유와 구글이 정말로 노린 것은 다른 층위입니다. 분할은 UX 실수가 아니라 의도된 베팅이고, 베팅 자체보다 타이밍이 문제였다고 보는 게 정확합니다.

Antigravity 2.0을 실행하면 더 이상 IDE가 열리지 않습니다. Agent Manager가 먼저 뜨고, Editor View는 여전히 존재하지만 공식 권장은 "dual-wield" 입니다. 기존 IDE 아무거나 쓰고 그 위에 Antigravity를 오케스트레이션 레이어로 얹으라는 것이죠. Manager View는 에이전트 다섯 개를 동시에 돌리는 Linear 보드처럼 작동합니다. 사람의 기본 작업 단위를 "타이핑" 에서 "에이전트 디스패치 후 리뷰" 로 옮기겠다는 선언으로 읽힙니다.

코드와 터미널을 볼 필요가 없다고 본 게 아니라, 기본값이 더 이상 그곳이 아니라고 본 것에 가깝습니다. 보고 싶으면 옆에 따로 열어두라는 거죠.

## 방향

이 의사결정은 따로 보면 우연이고, 같이 보면 같은 베팅의 세 면입니다. 흥미로운 점은 셋 중 두 개가 구글 바깥에서 동시에 같은 방향을 가리켰다는 것입니다.

첫째, 4월 21일 공개된 [[Google DeepMind]]의 Deep Research Max는 비동기 다중 소스 리서치 에이전트입니다. 던져두고 결과를 받으러 가는 모델이죠. 둘째, 1월에 올라온 [[Self-Manager - Parallel Agent Loop for Long-form Deep Research|Self-Manager (Parallel Agent Loop for Long-form Deep Research)]]는 메인 스레드가 격리 컨텍스트의 서브스레드들을 Thread Control Block으로 관리하는 구조를 제안합니다. Antigravity Manager View가 거의 이 논문의 UI 구현체에 가깝습니다. 셋째, Microsoft Research에서 나온 [[The Era of Agentic Organization - Learning to Organize with Language Models|The Era of Agentic Organization (Learning to Organize with Language Models)]]은 LLM이 스스로 워크플로를 조직화하는 학습을 다룹니다. 오거나이저가 동적으로 서브쿼리를 분배하고 중간 결과를 머지하는 AsyncThink 프로토콜로, 병렬 사고 대비 추론 지연이 28% 낮아졌다고 보고합니다. 사람이 단계를 짜주는 시대가 끝난다는 전제죠.

세 개를 한 줄로 묶으면 "비동기 병렬 에이전트가 디폴트 인터페이스다" 입니다. 구글만 외롭게 가는 게 아니라 학계와 다른 빅테크가 같은 방향을 보고 있다는 거죠. 구글은 그 흐름을 가장 공격적으로 제품에 박았을 뿐입니다.

## 어쩔 수가 없다

2023년 DeepMind와 Brain이 합쳐진 뒤 [[Demis Hassabis]]는 본인 인터뷰에서 "스타트업 페이스" 로 굴리고 있다고 했습니다. 알파벳 CEO와 매일 통화하는 구도라고도 알려져 있죠. [[Gemini]] 3가 12월에 잠깐 프론티어를 잡았다가 봄에 [[Anthropic]]의 [[Claude Code]]와 [[OpenAI]]의 Codex에게 개발자 도구 내러티브를 다시 빼앗긴 상황이고, 한 방에 패러다임으로 뒤집겠다는 압박이 컸을 겁니다. IDE 점진 개선이 아니라 IDE 자체를 부차적으로 만든다는 도박이 가능했던 배경입니다.

문제는 베팅이 지금 받쳐지지 않는다는 점입니다.

첫째, 모델이 안 따라옵니다. Gemini 3.5 Flash가 업데이트 후 "작은 버그도 못 고치고 사실상 useless" 라는 리포트가 4월 구글 AI 포럼에 쌓였습니다. fire-and-forget의 전제는 에이전트가 봐도 되는 수준의 안정성인데, 오히려 회귀한 상태죠.

둘째, 마이그레이션이 엉망이었습니다. 자동 업데이트 후 terminal, source control, sidebar가 사라지고, AppData가 `Roaming\Antigravity` 와 `Roaming\Antigravity IDE` 로 갈라지고, CDN 404가 떴습니다. 후속 CLI인 agy는 패키지 매니저에 아직 올라오지도 않았습니다. "에이전트 시대 왔다" 보다 "내 IDE 망가졌다" 가 먼저 도착하면 메시지가 죽습니다.

기존 VS Code 익스텐션 호환성도 같이 무너졌습니다. Antigravity는 처음부터 Microsoft가 운영하는 VS Code Marketplace가 아닌 OpenVSX 레지스트리를 쓰기 때문에 인기 익스텐션 상당수가 검색조차 안 됐는데, 2.0에서는 그 위에 IDE와 Agent를 함께 설치하면 작동을 멈추고, IDE만 설치하면 기존 설정과 익스텐션이 사라지는 사고까지 겹쳤습니다. VS Code Marketplace URL을 직접 끼워 넣으면 "Failed to fetch" 가 뜨고, C# Dev Kit처럼 라이선스로 막힌 익스텐션은 아예 못 씁니다. VS Code 포크라는 익숙함을 마케팅하면서 정작 익숙한 환경은 못 가져오게 만든 셈이죠.

셋째, 가격으로 비전을 강제했습니다. 200달러 Ultra 티어로 Manager View를 풀로 굴리게 만들어놓고 Gemini CLI는 6월 18일에 셧다운합니다. 선택권 없이 비전을 받아들이게 만드는 형태죠.

## 마무리

구글이 방향을 잘못 본 건 아닙니다. 비동기 에이전트가 디폴트 인터페이스가 되는 미래는 아마 옵니다. 다만 그 미래가 준비됐다고 지금 선언한 것이 문제였습니다. 모델 안정성, 마이그레이션 엔지니어링, 가격 정책 셋 다 베팅을 뒷받침 못 하는데 베팅만 6개월에서 12개월 먼저 던진 상태에 가깝습니다.

내러티브를 한 방에 회수하려는 조직적 절박함이 제품 준비도보다 앞섰다는 게, 지금 구글이 "이상하다" 고 느껴지는 이유의 핵심일 겁니다.
