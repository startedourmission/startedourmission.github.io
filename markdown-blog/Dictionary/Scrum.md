---
date: 2026-04-17
tags:
  - 정보
aliases:
  - 스크럼
description: "경험적 프로세스 제어를 바탕으로 하는 소프트웨어 개발 프레임워크. 역할 3개, 이벤트 5개, 산출물 3개로 구성되며 Scrum Guide 13페이지에 성문화되어 있다."
---

스크럼(Scrum)은 [[Jeff Sutherland]]와 [[Ken Schwaber]]가 1995년 OOPSLA 학회에서 공개한 소프트웨어 개발 프레임워크다. 공식 정의는 [Scrum Guide](https://scrumguides.org/scrum-guide.html)에 담겨 있으며, 2020년 개정판 기준 13페이지로 구성된 짧은 문서다.

## 핵심

- **경험적 프로세스 제어**를 기반으로 한다: 투명성(Transparency) → 검사(Inspection) → 적응(Adaptation)의 반복
- **역할 3개**: Product Owner, Scrum Master, Developers
- **이벤트 5개**: Sprint, Sprint Planning, Daily Scrum(15분), Sprint Review, Sprint Retrospective
- **산출물 3개**: Product Backlog, Sprint Backlog, Increment
- **Sprint**는 1~4주로 타임박스가 고정되어 있다
- **엔지니어링 실천을 규정하지 않는다** — 계획·검토 구조만 정의하므로 별도의 실천(TDD, CI 등)을 결합해야 한다

## 다른 방법론과의 관계

스크럼은 구체적 코딩 방법을 정의하지 않기 때문에, 실제 현장에서는 [[Extreme Programming]]의 실천(TDD, Pair Programming, Refactoring)과 결합해 사용하는 경우가 많다. [[Kanban]]의 WIP 제한을 스크럼에 접목한 Scrumban 방식도 널리 쓰인다.

## 비판

용어와 이벤트는 명확하게 정의되어 있지만, "경험적 제어"라는 철학 자체는 검증이 어렵다. 스크럼 실패 시 "진짜 스크럼이 아니었다"고 해석되는 [[No True Scotsman 오류]]가 자주 지적된다. 단, 스크럼은 애자일과 달리 구체적 규칙(스탠드업 15분, 스프린트 타임박스 등)을 통해 최소한의 반증 가능성을 확보하고 있다.

## 관련 문서

- [[애자일 선언문]]
- [[Extreme Programming]]
- [[Kanban]]
- [[Jeff Sutherland]]
- [[Ken Schwaber]]
