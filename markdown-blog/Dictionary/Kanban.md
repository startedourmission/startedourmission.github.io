---
date: 2026-04-17
tags:
  - 정보
aliases:
  - 칸반
description: "도요타 생산방식(TPS)에서 파생된 흐름 기반 작업 관리 시스템. 이터레이션 없이 WIP 제한과 리드 타임 측정을 통해 연속적 개선을 추구한다."
---

칸반(Kanban)은 원래 도요타 생산방식(Toyota Production System)에서 개발된 재고 관리 기법으로, 일본어로 "간판(看板)"을 뜻한다. 소프트웨어 개발로의 적용은 [[David J. Anderson]]이 2010년 저서 *Kanban: Successful Evolutionary Change for Your Technology Business*로 체계화했다.

[[Scrum]]이나 [[Extreme Programming]]과 달리 **이터레이션이 없고**, **역할이 없으며**, **미팅 규정이 없다**. 현재 프로세스를 유지하면서 점진적으로 개선하는 것을 원칙으로 한다.

## 6개 핵심 실천

1. **Visualize** — 업무 흐름을 칸반 보드로 시각화
2. **Limit WIP (Work in Progress)** — 동시 진행 작업 수를 명시적으로 제한
3. **Manage Flow** — 리드 타임·사이클 타임 측정을 통한 흐름 관리
4. **Make Policies Explicit** — Done의 정의 등 정책을 명문화
5. **Implement Feedback Loops** — 정기 리뷰(단, 스프린트는 없음)
6. **Improve Collaboratively** — 이론(리틀의 법칙 등) 기반의 협력적 개선

## 핵심 지표

- **Lead Time**: 요청부터 완료까지 전체 시간
- **Cycle Time**: 작업 시작부터 완료까지 시간
- **Throughput**: 단위 시간당 완료 수
- **WIP**: 현재 진행 중인 작업 수

## Scrum과의 차이

| 항목 | Scrum | Kanban |
|---|---|---|
| 단위 | Sprint (시간) | Work Item (작업) |
| 역할 | 3개 고정 | 없음 |
| 이터레이션 | 필수 (1~4주) | 없음 (연속) |
| WIP 제한 | 암묵적 (스프린트 용량) | 명시적 숫자 |
| 변경 접근 | 혁명적 | 점진적 진화 |

## Scrumban

Scrum의 이벤트 구조에 Kanban의 WIP 제한을 결합한 하이브리드로, 실무에서 가장 흔한 방식 중 하나다.

## 관련 문서

- [[애자일 선언문]]
- [[Scrum]]
- [[Extreme Programming]]
- [[David J. Anderson]]
