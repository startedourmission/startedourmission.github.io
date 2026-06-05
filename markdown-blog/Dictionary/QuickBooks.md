---
type: tool
description: "Intuit의 SMB·소규모 사업자용 회계 SaaS, 미국 시장 점유율 1위로 Claude for Small Business의 주력 커넥터 중 하나"
tags:
  - 도구
  - SaaS
aliases:
  - "QuickBooks"
  - "QuickBooks Online"
  - "Intuit QuickBooks"
---

QuickBooks는 [Intuit](https://www.intuit.com)이 만든 회계·재무 관리 SaaS로, 미국 SMB(소상공인·중소기업) 회계 시장에서 압도적인 점유율을 가진 제품이다. 클라우드 기반 *QuickBooks Online* 과 데스크톱 버전 *QuickBooks Desktop* 이 있으며, 현대 SMB는 거의 대부분 Online을 쓴다.

핵심 기능은 거래 분류, 송장 발행, 비용 추적, 은행·결제 계정 연동, P&L·재무제표 자동 생성이다. 결제 처리(PayPal, Stripe, Square 등)와 자동 reconciliation을 지원해 사장님이 직접 엑셀로 장부를 맞추는 시간을 크게 줄여 준다.

[[Anthropic]]의 *Claude for Small Business* 플러그인에서 **주력 커넥터** 로 지정돼 있으며, `/plan-payroll`(급여 계획)과 `/close-month`(월말 결산) 워크플로우의 데이터 소스 역할을 한다. [[Claude]]는 QuickBooks에서 거래 데이터를 읽어 [[PayPal]]·[[Stripe]] 정산과 자동 매칭하고, 안 맞는 항목을 분류해 P&L narrative까지 작성한다.
