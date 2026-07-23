---
date: 2026-07-16
tags:
  - 정보
  - 도구
  - LLM
description: "GitHub Copilot이 코드 보안 리뷰와 에이전틱 자동수정을 퍼블릭 프리뷰로 공개했습니다. CodeQL 2.26.0은 AI 프롬프트 인젝션을 최초로 SAST 탐지 대상으로 지정했습니다."
image: "![[github-copilot-security-thumb.png]]"
---

2026년 7월 14일 GitHub Changelog가 연달아 세 가지 발표를 냈습니다. Copilot 앱 내 보안 리뷰, code scanning 취약점의 에이전틱 자동수정, 그리고 CodeQL 2.26.0의 AI 프롬프트 인젝션 탐지입니다.

## 보안 리뷰

`/security-review` 명령어를 Copilot 앱에서 실행하면 PR 단위로 보안 분석을 수행합니다. Copilot이 변경된 코드를 훑고 잠재적인 취약점을 코멘트로 남깁니다. 코드 리뷰를 보안 관점에서 한 층 더 거치는 구조입니다.

이 기능은 Copilot 앱(IDE 통합 아님, 웹 기반 Copilot chat)에서 퍼블릭 프리뷰로 열렸습니다.

## 에이전틱 자동수정

code scanning(GitHub Advanced Security)이 발견한 취약점에 대해 Copilot이 직접 수정을 제안하는 기능입니다. 기존 Copilot Autofix가 패턴 매칭 기반의 단순 수정이었다면, 이번 에이전틱 autofix는 다단계로 작동합니다.

1. 취약점 경고를 받으면 Copilot이 관련 파일을 탐색합니다.
2. 수정 코드를 작성합니다.
3. CodeQL을 재실행해 수정이 경고를 닫는지 확인합니다.
4. 검증이 통과하면 Draft PR을 엽니다.

"코드를 열고, 고치고, 테스트하고, PR을 올린다"는 워크플로를 자동화한 것입니다. 현재 퍼블릭 프리뷰 단계입니다.

## 프롬프트 인젝션 탐지

CodeQL 2.26.0이 JavaScript와 TypeScript 코드에서 **AI 시스템 프롬프트 인젝션**을 탐지하는 쿼리를 추가했습니다. 세 발표 중 파급이 가장 큰 항목입니다.

SAST(정적 분석 보안 테스트) 도구가 프롬프트 인젝션을 탐지 대상으로 공식 지정한 건 이번이 처음입니다. XSS와 SQL 인젝션이 오랫동안 SAST 도구의 핵심 탐지 대상이었던 것처럼, AI 에이전트 시대의 새 취약점 클래스가 같은 위치를 차지하기 시작했습니다.

프롬프트 인젝션은 외부 입력(사용자 메시지, 웹 콘텐츠, 파일 내용)이 LLM의 시스템 프롬프트를 오염시키는 공격입니다. AI 에이전트가 코드베이스에 합류하면서 이 공격 벡터가 실질적인 위협이 됐습니다. SecurityWeek 보도에 따르면 Claude Code, Gemini CLI, GitHub Copilot Agents 모두 코드 주석을 통한 프롬프트 인젝션에 취약하다는 연구가 나와 있습니다.

## 스캐너 자신의 취약점

Copilot 자체도 보안 이슈로부터 자유롭지 않습니다. 2025년 CamoLeak(CVE-2025-59145, CVSS 9.6)는 프롬프트 인젝션을 이용해 비공개 소스 코드를 유출하는 취약점이었고, 2026년 2월에는 Orca Security가 GitHub Codespaces의 패시브 프롬프트 인젝션 결함 RoguePilot을 공개했습니다.

보안 스캔을 수행하는 LLM이 동일 범주의 취약점에 노출돼 있다는 점은 짚어둘 필요가 있습니다. 에이전틱 autofix가 실제로 배포되면 코드베이스 접근 권한을 가진 에이전트가 추가로 생긴다는 의미이기도 합니다.

CodeQL의 프롬프트 인젝션 탐지가 실제로 얼마나 정밀하게 작동하는지는 아직 실사용 데이터가 없습니다. "JavaScript에서 외부 입력이 LLM 프롬프트로 흘러들어가는 경로"를 정적 분석으로 잡아내는 건 taint analysis의 전형적인 문제이고, 실제 에이전트 코드베이스에서 얼마나 false positive를 줄이는지가 관건입니다.

세 기능 모두 퍼블릭 프리뷰 단계로, 프로덕션 적용 전에 검증할 시간이 있습니다.

---

참고: [GitHub Changelog - Security reviews in Copilot app (2026-07-14)](https://github.blog/changelog/2026-07-14-security-reviews-now-available-in-the-github-copilot-app/) / [CodeQL 2.26.0 AI prompt injection detection (2026-07-10)](https://github.blog/changelog/2026-07-10-codeql-2-26-0-adds-kotlin-2-4-0-support-and-ai-prompt-injection-detection/)
