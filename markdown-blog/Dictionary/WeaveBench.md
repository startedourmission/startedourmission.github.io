---
ready: true
type: benchmark
description: "GUI와 CLI를 같은 워크플로 안에서 오가야 풀리는 114개 장기 실행 과제. 하이브리드 인터페이스 컴퓨터 유즈 에이전트를 재는 벤치마크"
tags:
  - 벤치마크
  - AI평가
  - 에이전트
aliases:
  - WeaveBench
---

WeaveBench는 컴퓨터를 쓰는 에이전트를 대상으로 하는 장기 실행 벤치마크입니다. 114개 과제로 구성되며, 하나의 워크플로 안에서 GUI 조작과 CLI 실행을 함께 요구한다는 점이 다른 벤치마크와 갈리는 지점입니다. 2026년 Wanli Li 등이 공개했습니다(arXiv:2606.09426).

## 구성

과제는 여덟 개 도메인으로 나뉩니다. Desktop(DSK), Document(DOC), Games(GAM), Web(WEB), Data Analysis & Visualization(DAV), DevOps(OPS), Spatial/3D(SPA), Design(DES)입니다. 게임 도메인은 시각 조작, 심볼릭 상태, 탐색, 환경별 제약이 한꺼번에 걸려 있어 스트레스 테스트 역할을 합니다.

## 지표

PassRate는 전 과제를 완전히 통과한 비율이고, Overall은 114개 과제 전체의 평균 점수입니다. 부분 점수가 있으므로 두 지표가 크게 벌어질 수 있습니다.

## 성적

공식 리포트 기준 최고 성적은 [[Claude Code]] 하네스에 Claude Opus 4.7을 얹은 41.2%였습니다. [[LongHorizon-Harness - Advancing Long-Horizon Agents for Real-World Tasks|LongHorizon-Harness]]가 Qwen 3.7-Plus로 80.7%를 보고했으나, 공식 결과가 일반 사용자 계정에서 측정된 반면 이쪽은 태스크 VM 안에서 root 권한을 쓴 조건이라 저자들도 직접 비교가 아닌 참고치로 두고 있습니다. 같은 Claude Code 조건끼리 맞춘 비교는 51.8% 대 80.7%입니다.

## 관련 항목

- [[OSWorld]] — 데스크톱 워크플로 중심, GUI 위주
- [[Terminal-Bench]] — 순수 명령줄 과제
