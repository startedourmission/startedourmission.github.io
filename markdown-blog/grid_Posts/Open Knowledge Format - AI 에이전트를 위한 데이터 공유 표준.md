---
date: 2026-06-14
tags:
  - 정보
  - Headliner
  - 데이터분석
  - 오픈소스
description: "Google Cloud가 제안한 OKF는 AI 에이전트가 데이터를 이해할 수 있도록 마크다운과 YAML 프론트매터로 지식을 표현하는 개방형 표준입니다. CLAUDE.md와 Obsidian vault 같은 패턴의 데이터 카탈로그 버전입니다"
---
테이블 스키마는 BigQuery에, 그 테이블이 무슨 의미인지는 Confluence에, 조인 관계는 시니어 엔지니어의 머릿속에. 데이터를 깔끔하게 정리하고 AI 에이전트 검색의 효율을 높이기 위한 노력은 어느 때보다 활발한 상황입니다. 

| 위치                   | 담긴 것             |
| -------------------- | ---------------- |
| 메타데이터 카탈로그           | 스키마, 타입 정보       |
| Confluence / Notion  | 비즈니스 정의, 운용 문서   |
| GitHub / Jupyter 노트북 | 분석 로직, 주석        |
| 코드 댓글                | 특수 케이스, 예외 처리 이유 |
| 시니어 엔지니어 머릿속         | 조인 함정, 히스토리      |

에이전트가 이 모든 곳에서 컨텍스트를 모아 조립하는 일을 매번 새로 해야 합니다. 지식이 생성된 시스템에 갇혀 있고, 다른 시스템으로 옮기기 어렵습니다. [[LLM]]이 아무리 좋아도, 컨텍스트가 없으면 제대로 된 답을 낼 수 없습니다.


Google Cloud가 2026년 6월 공개한 Open Knowledge Format(OKF)도 이 문제를 해결하기 위해 나섰습니다. 마크다운 파일과 YAML 프론트매터만으로 데이터에 대한 지식을 표현하는 개방형 표준입니다. 특정 클라우드 SDK도, 독점 API도 필요하지 않습니다.
## OKF가 제안하는 해법

OKF는 사실 새로운 아이디어가 아닙니다. 코드 저장소에 `CLAUDE.md`나 `AGENTS.md`를 두는 관행, Obsidian 볼트에 마크다운으로 지식을 쌓는 방식, 데이터팀이 "메타데이터 as 코드" 저장소를 운영하는 것 — 이런 패턴들이 이미 자연스럽게 등장하고 있었습니다. [[Andrej Karpathy]]는 이 흐름을 "LLM wiki 패턴"이라 부르며 이렇게 말했습니다.

> "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."

OKF는 이 패턴을 데이터 카탈로그 영역에서 공식화합니다. 각 데이터 개념(테이블, 뷰, 메트릭, 데이터셋)을 마크다운 파일 하나로 표현하고, 파일 상단에 YAML 프론트매터로 구조화된 메타데이터를 붙입니다.

```
sales/
├── index.md
├── datasets/
│   └── orders_db.md
├── tables/
│   ├── orders.md
│   └── customers.md
└── metrics/
    └── weekly_active_users.md
```

각 파일은 이런 모습입니다.

```markdown
---
type: BigQuery Table
title: Orders
description: One row per completed customer order.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---

## Schema

| Column      | Type   | Description                         |
|-------------|--------|-------------------------------------|
| order_id    | STRING | 글로벌 고유 주문 식별자               |
| customer_id | STRING | FK to [customers](/tables/customers.md) |

## Joins

`customer_id`로 [customers](/tables/customers.md)와 조인합니다.
```

YAML 프론트매터가 에이전트를 위한 구조화된 진입점이고, 마크다운 본문이 사람이 읽을 수 있는 설명입니다. 같은 파일 하나가 둘 다를 충족합니다.

## 설계 원칙 세 가지

OKF 사양 문서는 의도적으로 짧습니다. 세 가지 원칙을 중심에 두기 때문입니다.

**최소한의 의견(Minimally Opinionated)**. 필수 필드는 `type` 하나뿐입니다. 나머지 필드, 타입 이름, 본문 구조는 전부 작성자 재량입니다. "틀린 OKF 파일"은 없고, 상호운용성을 위한 최소 표면만 정의합니다. 덕분에 도입 장벽이 낮습니다.

**프로듀서와 컨슈머의 독립성**. 지식을 만드는 쪽과 소비하는 쪽이 서로를 알 필요가 없습니다. 인간이 작성한 번들을 AI 에이전트가 소비할 수 있고, 메타데이터 파이프라인이 생성한 번들을 시각화 도구가 읽을 수 있습니다. 한 [[LLM]]이 만든 번들을 다른 LLM이 쿼리하는 것도 됩니다. 포맷이 공통어 역할을 합니다.

**포맷이지 플랫폼이 아님(Format, not Platform)**. 특정 클라우드, 특정 데이터베이스, 특정 모델 제공자에 종속되지 않습니다. tarball로 배포하거나, git 저장소에 올리거나, 어떤 파일시스템에도 마운트할 수 있습니다. SDK 없이 vim으로도 쓸 수 있고, GitHub에서 바로 렌더링됩니다.

## v0.1과 함께 나온 것들

Google Cloud는 OKF 사양만 공개한 게 아닙니다. 참조 구현도 같이 냈습니다.

**Enrichment Agent**는 프로듀서 역할입니다. BigQuery 데이터셋을 자동으로 순회하면서 각 테이블과 뷰에 대해 OKF 문서를 작성합니다. 그냥 스키마를 덤프하는 게 아니라, 두 번째 LLM 패스로 권위 있는 문서를 크롤해서 인용까지 추가합니다. 조인 경로와 스키마도 자동 추출합니다.

**Static HTML Visualizer**는 컨슈머 역할입니다. OKF 번들을 대화형 그래프 뷰로 변환해주는 단일 HTML 파일입니다. 백엔드가 필요 없고, 설치도 없습니다. 파일을 브라우저에 드래그하면 됩니다. 데이터가 페이지 밖으로 나가지 않는다는 점도 강점입니다.

샘플 번들로 GA4 e-commerce 데이터셋, Stack Overflow 공개 데이터, Bitcoin 블록체인 데이터 세 가지를 같이 공개했습니다. [GitHub 저장소](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)에서 받아서 Visualizer에 올려보면 어떤 형태인지 바로 확인할 수 있습니다.

## CLAUDE.md의 데이터 카탈로그 버전

이 맥락에서 OKF를 보면 흥미롭습니다. `CLAUDE.md`나 `AGENTS.md`는 코드 저장소에 에이전트를 위한 컨텍스트를 두는 관행이고, OKF는 데이터 저장소에 에이전트를 위한 컨텍스트를 두는 관행입니다. 둘 다 "마크다운 + 사람이 읽을 수 있는 구조"라는 철학을 공유합니다. 이미 하고 있던 일의 공식화라는 점이 OKF의 장점이기도 하고 약점이기도 합니다.

진입 장벽이 낮다는 건 좋습니다. 그런데 필수 필드가 `type` 하나뿐이다 보니, 서로 다른 팀이 만든 OKF 번들 간에 실제 상호운용이 잘 될지는 지켜봐야 합니다. 팀마다 다른 타입 이름을 쓰고, 다른 필드를 정의하면 결국 각자의 사일로가 마크다운으로 바뀌는 것에 불과할 수 있습니다.

Google이 "개방형 표준"이라고 내놓으면서 동시에 BigQuery Knowledge Catalog를 통해 OKF를 수집하고 서빙한다는 점도 생각해볼 부분입니다. 포맷은 열려 있지만, 가장 잘 통합된 구현은 Google Cloud 위에 있을 가능성이 높습니다. 표준이 생태계를 만드는지, 아니면 Google의 데이터 플랫폼 락인을 위한 온보딩 도구가 되는지는 프로듀서와 컨슈머가 얼마나 다양하게 등장하느냐에 달려 있습니다.

## 직접 써보려면

표준이 자리를 잡으려면 프로듀서와 컨슈머가 함께 늘어야 합니다. 지금 v0.1 단계에서는 직접 만들어보고 피드백을 주는 게 가장 실질적인 참여입니다. 사양은 명시적으로 역방향 호환성을 설계하고 있으므로, 지금 올라탄다고 해서 나중에 다 뒤집어야 할 가능성은 낮습니다.

순서는 이렇습니다.

1. [사양 문서](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)를 읽습니다. 짧습니다.
2. 샘플 번들 중 하나를 받아서 Visualizer에 올려봅니다.
3. 자신의 데이터셋에 맞는 OKF 파일을 직접 작성해봅니다.
4. BigQuery를 쓴다면 Enrichment Agent를 실제 데이터셋에 돌려봅니다.
5. 부족한 부분은 이슈나 PR로 올립니다.

데이터 카탈로그가 AI 에이전트 시대에 어떻게 바뀌어야 하는지 고민하고 있다면, OKF는 한 번 들여다볼 만한 시도입니다. 기술적으로 새로운 게 없다는 게 오히려 설득력입니다. 마크다운을 쓸 수 있으면 시작할 수 있습니다.
