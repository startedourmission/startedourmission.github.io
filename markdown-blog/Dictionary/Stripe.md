---
type: tool
description: "개발자 친화적인 온라인 결제 인프라 SaaS, SaaS·이커머스 스타트업의 표준 결제 처리기이자 Claude for Small Business의 부가 커넥터"
tags:
  - 도구
  - SaaS
aliases:
  - "Stripe"
---

Stripe는 2010년 아일랜드 출신 형제 Patrick·John Collison이 창업한 결제 인프라 SaaS다. API 우선 설계와 개발자 친화적 문서로 명성을 얻으며, 2020년대 들어 SaaS·이커머스 스타트업의 표준 결제 처리기로 자리잡았다. 비공개 상태로 기업 가치 700억 달러대를 평가받는 거대 핀테크다.

핵심 제품은 *Stripe Payments* (카드 결제 처리), *Stripe Billing* (구독·인보이스), *Stripe Connect* (마켓플레이스 결제), *Stripe Atlas* (델라웨어 법인 설립) 등이다. [[PayPal]]·[[Square]]와 함께 SMB 결제 시장의 핵심 플레이어이지만, 특히 개발자가 셋업하는 디지털 비즈니스에서 압도적 선호도를 보인다.

[[Anthropic]]의 *Claude for Small Business* 플러그인에서 **부가 커넥터** 로 연결되며, `/close-month` 월말 결산 워크플로우에서 [[QuickBooks]] 거래 데이터와 Stripe 정산을 reconcile하는 데이터 소스 역할을 한다.
