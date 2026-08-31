---
title: "New in Air: Claude Subscriptions, Multiproject View, and Improved Markdown"
source: "https://blog.jetbrains.com/air/2026/08/new-in-air-claude-subscriptions-multiproject-view-and-improved-markdown/"
author:
  - "JetBrains"
published: 2026-08-20
created: 2026-08-20
description: "Air가 Claude Pro/Max/Team 구독을 그대로 씀. API 크레딧·콘솔 과금 없음. 데스크톱 무료. 토큰은 로컬 Claude만 보유."
tags:
  - clippings
---

시각: 2026-08-20 16:05 KST 시그널 델타

X: https://x.com/getsome_air/status/2090118343370145882

공식: https://blog.jetbrains.com/air/2026/08/new-in-air-claude-subscriptions-multiproject-view-and-improved-markdown/

각도(메모만): 클로드 구독만으로 다른 에이전트 IDE. 작성자 사례로 빠짐없이. 테마로 묶지 말 것.

## Claude 구독

Air에서 기존 Claude Pro, Max, Team 구독을 쓸 수 있다. 사용량은 구독 쿼터에서 빠진다. API 크레딧을 살 필요 없고, 토큰당 Console 과금이 없다.

Connect Claude.ai Account를 누르면 Air가 자체 OAuth를 돌리지 않는다. 터미널에서 Claude를 켤 때와 같은 네이티브 로그인이다. 브라우저가 열리고 승인하면 토큰은 Anthropic이 설계한 자리, Claude 쪽에 남는다. Claude가 자격 증명을 갖고 갱신한다. Air가 아는 것은 로그인됐다는 사실뿐이다. Air는 토큰을 저장하지 않는다.

Anthropic 문서에 적힌 인증 흐름을 따른다. 계정 위험을 줄이려고 OAuth 우회를 내지 않고 기다렸다고 적혀 있다.

데스크톱 Air는 무료다. JetBrains AI나 유료 Air 플랜은 필요 없다. 외부 AI 제공자 구독을 가져오면 추가 과금이 없다고 FAQ에 적혀 있다.

## Claude Agent

번들 이름은 Claude Agent다. 1차 연동이다.

- 현재 모델 선택, reasoning effort
- 슬래시 커맨드
- MCP 서버
- 스킬
- 권한과 세션 상태
- 사용량·상태 보고

ACP로 Claude를 붙인 사람은 ACP 항목을 빼고 번들 Claude Agent로 로그인하라고 한다. 모델 보고, 슬래시 커맨드, 1차 기능이 맞다고 한다.

macOS, Windows, Linux에서 된다. Claude Team 좌석만 있고 API 예산이 없어도 Team 구독으로 된다고 한다.

## Docker·클라우드·자동화

구독 토큰은 로컬 머신 Claude에만 있고 Air는 사본을 안 가진다. 격리 컨테이너에 넘길 자격 증명이 없다. Docker 환경, 클라우드 에이전트, 자동화는 API 과금 또는 JetBrains AI 크레딧이 필요하다. 구독으로 돌린 작업을 IDE·모바일 같은 다른 면에 아직 공유하지 못한다.

## Multiproject view

다른 저장소를 열려면 창을 하나 더 열어야 했다. 이제 한 창에 여러 프로젝트와 태스크가 있다. 사이드바가 프로젝트별로 태스크를 묶고, 검색은 전체 태스크를 본다. 태스크마다 프로젝트와 브랜치가 보인다. 탐색 단위가 창에서 태스크로 바뀐다. 백엔드에서 에이전트를 켜고 프론트엔드로 옮긴 뒤 세 번째 프로젝트의 끝난 태스크로 갈 수 있다.

## Markdown

`.md`를 문서처럼 렌더한다. 제목 계층, 목록, 코드 블록, 명령·경로·인라인 코드 강조. 파일은 그대로 Markdown이다. 읽을 때 문법이 뒤로 가고 편집할 때 나타난다.

## 다운로드

https://air.dev/download 또는 JetBrains Toolbox.
