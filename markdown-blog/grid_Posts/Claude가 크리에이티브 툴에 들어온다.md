---
date: 2026-04-29
tags:
  - 정보
description: "Anthropic이 Blender, Adobe, Ableton 등 크리에이티브 툴과의 공식 커넥터를 출시하며 전문 창작 환경으로 Claude를 확장합니다."
---

2026년 4월 28일, Anthropic이 크리에이티브 전문가를 위한 Claude 활용 방안을 발표했습니다. 단순한 대화 AI가 아니라 Blender, Adobe, Ableton 같은 전문 툴 안에서 직접 동작하는 파트너로 자리매김하겠다는 선언입니다.

## 커넥터란 무엇인가

커넥터는 Claude가 외부 플랫폼과 툴에 직접 접근할 수 있게 해주는 연동 도구입니다. [[MCP(Model Context Protocol)]] 기반으로 만들어져 Claude 외 다른 LLM도 사용할 수 있습니다. Anthropic이 이날 공개한 커넥터 목록은 다음과 같습니다.

- **Ableton** — Live와 Push의 공식 제품 문서를 기반으로 답변
- **Adobe for creativity** — Photoshop, Premiere, Express 등 50개 이상의 Creative Cloud 앱에서 이미지·영상·디자인 작업
- **Affinity by Canva** — 배치 이미지 조정, 레이어 이름 변경, 파일 내보내기 등 반복 작업 자동화
- **Autodesk Fusion** — 대화로 3D 모델 생성 및 수정 (Fusion 구독자 대상)
- **Blender** — Python API에 자연어 인터페이스 제공, 복잡한 씬 분석 및 스크립트 생성
- **Resolume Arena / Wire** — VJ와 라이브 비주얼 아티스트가 실시간으로 자연어로 Arena·Wire 제어
- **SketchUp** — 대화로 시작하는 3D 모델링 (공간, 가구, 부지 개념을 기술하면 SketchUp으로 가져와 다듬기)
- **Splice** — 로열티 프리 샘플 카탈로그를 Claude 안에서 직접 검색

## Claude를 크리에이티브 작업에 쓰는 방법

Anthropic은 몇 가지 구체적인 활용 패턴을 제시했습니다.

**툴 학습과 마스터링.** Claude를 온디맨드 튜터로 씁니다. 모디파이어 스택, 신디사이저 기법, 낯선 기능을 설명해달라고 하면 사용법을 직접 보여줍니다.

**코드로 툴 확장.** [[Claude Code]]가 이미 쓰고 있는 소프트웨어용 스크립트, 플러그인, 생성형 시스템을 작성합니다. 커스텀 셰이더, 절차적 애니메이션 스크립트, 파라메트릭 모델 생성 등이 가능합니다.

**파이프라인 연결.** 포맷 변환, 데이터 재구조화, 여러 앱에 걸친 에셋 동기화를 Claude가 처리해 수동 핸드오프 없이 디자인·3D·오디오 툴 사이를 오갑니다.

**빠른 아이디어 탐색.** 새로 공개된 **Claude Design**은 소프트웨어 UX 아이디어를 시각화하고 반복할 수 있는 Anthropic Labs의 신규 제품입니다. 현재 Canva로의 내보내기를 지원합니다.

**반복 생산 작업 처리.** 에셋 배치 처리, 프로젝트 스캐폴딩, 씬 전반의 절차적 변경 등 시간을 잡아먹는 단순 반복 작업을 Claude에게 넘길 수 있습니다.

## Blender와의 파트너십

Blender 개발팀이 MCP 커넥터를 직접 만들었고 이것이 Claude 공식 커넥터로 등록됐습니다. 3D 아티스트가 전체 Blender 씬을 분석·디버깅하거나, 씬 내 오브젝트에 배치 변경을 적용하는 커스텀 스크립트를 만들 수 있습니다.

Anthropic은 Blender 개발 펀드에 후원자로 참여해 Python API 개발을 지원하기로 했습니다. MCP 기반이라 Claude 외 다른 LLM도 이 커넥터를 쓸 수 있다는 점은 오픈소스 정신을 지키는 Blender다운 결정입니다.

## 교육 파트너십

Anthropic은 크리에이티브 컴퓨테이션 커리큘럼을 운영하는 예술·디자인 학교 세 곳과도 협력합니다.

- Rhode Island School of Design — Art and Computation
- Ringling College of Art and Design — Fundamentals of AI for Creatives
- Goldsmiths, University of London — MA/MFA Computational Arts

학생과 교수진이 Claude와 커넥터에 접근할 수 있게 되고, 이들의 피드백이 크리에이티브 실무자에게 필요한 기능 개발로 이어질 예정입니다.

## 의미

프롬프트 하나로 뭔가를 만들어내는 "AI가 그림 그린다" 식의 접근과는 다릅니다. 크리에이티브 전문가가 이미 쓰고 있는 툴의 안에 Claude를 넣어, 반복 작업을 줄이고 더 야심찬 프로젝트를 가능하게 하는 방향입니다. 상상력과 취향은 여전히 사람의 몫이고, Claude는 그 상상이 실제로 구현되는 마찰을 줄이는 역할입니다.

Blender의 Python API, Adobe의 50+ 앱 생태계, Ableton의 Live 환경이 Claude와 연결된다는 건 — 적어도 이 생태계에서 일하는 사람에게는 — 꽤 실질적인 변화입니다.
