---
date: 2026-05-08
tags:
  - 정보
  - LLM
  - 오픈소스
description: "Karpathy 연구 자동화 프레임워크부터 Microsoft AI 에이전트 코스까지, 2026년 실제로 써볼 만한 AI 관련 GitHub 저장소 10개를 정리했습니다."
---

X에서 돌아다니는 "세상의 가장 똑똑한 사람들을 증류한 저장소" 목록을 봤습니다. 과장을 걷어내면 실제로 쓸 만한 것들이 있습니다.

## 학습 리소스

**1. andrej-karpathy-skills**
[github.com/forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)

Karpathy가 직접 쓴 게 아니라, 그의 유튜브 강의와 인터뷰에서 코딩·AI 조언을 추출해 단일 마크다운으로 정리한 파일입니다. 109K+ 스타를 받았는데, "역사상 가장 많은 스타를 받은 단일 파일"이라는 주장도 있습니다. 내용 자체는 Karpathy 사상의 요약이지, 공식 문서가 아닙니다.

**2. AI-Agents-for-Beginners**
[github.com/microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)

Microsoft가 만든 무료 12강 AI 에이전트 구축 코스. 실제 코드와 실습이 포함되어 있고, Microsoft가 공식 관리합니다. 에이전트를 처음 만들어보려는 사람에게 가장 검증된 출발점입니다.

## 도구·프레임워크

**3. autoresearch**
[github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch)

Karpathy 본인이 만든 연구 자동화 프레임워크. 논문 검색·요약·비교를 자동화합니다. 공개 직후 3일 만에 23K 스타를 받았습니다. 연구자보다는 AI 에이전트 아키텍처를 공부하는 용도로 보는 게 맞습니다.

**4. awesome-claude-code**
[github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

Claude Code 관련 프롬프트, CLAUDE.md 예시, 워크플로우 모음. 커뮤니티가 관리하는 비공식 가이드이지만, 실무에서 바로 가져다 쓸 수 있는 패턴이 많습니다.

**5. SuperClaude Framework**
[github.com/SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)

Claude Code를 위한 페르소나, 커스텀 명령어, 프롬프트 템플릿을 배포 가능한 형태로 패키징한 프레임워크. awesome-claude-code가 모음집이라면 이건 하나의 완성된 셋업입니다.

**6. hermes-agent**
[github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)

Nous Research가 만든 자기 진화 에이전트. 매 대화에서 기술을 추출해 자체 스킬로 저장하고, 이후 대화에서 꺼내 씁니다. 에이전트 메모리 아키텍처를 공부할 때 참고 코드로 유용합니다.

**7. MemPalace**
[github.com/MemPalace/mempalace](https://github.com/MemPalace/mempalace)

LLM 기반 메모리 시스템. LongMemEval 벤치마크에서 높은 점수를 기록했습니다. "할리우드 여배우가 Claude Code로 만들었다"는 홍보 문구는 마케팅입니다 — 코드 자체로 판단하세요.

## 애플리케이션·컬렉션

**8. awesome-llm-apps**
[github.com/Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

106K+ 스타. 실제로 작동하는 LLM 애플리케이션 예제 컬렉션입니다. RAG 파이프라인, 멀티 에이전트, 음성 앱 등 분야별로 정리되어 있고, 각 예제는 바로 실행 가능한 코드로 제공됩니다. 아이디어를 빠르게 검증할 때 가장 자주 열게 되는 저장소입니다.

**9. mattpocock/skills**
[github.com/mattpocock/skills](https://github.com/mattpocock/skills)

TypeScript 전문가 Matt Pocock의 일상 코딩 워크플로우 공개본. TDD, 아키텍처 결정, git 가드레일 등 AI와 직접 관련은 없지만, AI 코딩 도구와 함께 쓰는 엔지니어링 습관으로 참고할 만합니다.

**10. qlib**
[github.com/microsoft/qlib](https://github.com/microsoft/qlib)

Microsoft Research의 퀀트 투자 플랫폼. 알파 팩터 엔진, 백테스팅, 포트폴리오 최적화가 모두 들어 있습니다. AI 트레이딩에 관심이 있다면 시작점으로 쓸 수 있지만, 실서비스용으로 그대로 갖다 쓰기에는 적합하지 않습니다.

---

이 목록에서 진짜 입문 코스를 원하면 **AI-Agents-for-Beginners**, 실용 예제를 원하면 **awesome-llm-apps**, Claude Code를 더 잘 쓰고 싶다면 **awesome-claude-code**부터 보면 됩니다.
