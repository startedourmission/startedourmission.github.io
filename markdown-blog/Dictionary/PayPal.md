---
type: tool
description: "전 세계 SMB·이커머스가 가장 널리 쓰는 온라인 결제 서비스, Claude for Small Business의 주력 커넥터"
tags:
  - 도구
  - SaaS
aliases:
  - "PayPal"
---

PayPal은 1998년 설립된 온라인 결제 회사로, 2002년 eBay에 인수됐다가 2015년 분사해 독립 상장사가 됐습니다. 전 세계 200개국 이상에서 4억 명 이상의 활성 사용자를 보유하며, SMB와 이커머스 사업자의 기본 결제 인프라로 자리잡았습니다.

핵심 기능은 신용카드·은행 계좌·PayPal 잔액 결제 처리, 송금, 분쟁 처리(chargeback·환불), 통화 변환입니다. 사업자 입장에서는 [Stripe](https://stripe.com)·[Square](https://squareup.com)와 함께 가장 흔히 쓰는 결제 처리기 중 하나입니다.

[[Anthropic]]의 *Claude for Small Business* 플러그인에서 **주력 커넥터** 로 지정돼 있으며, [[QuickBooks]] 거래와 PayPal 정산을 자동 reconcile하는 핵심 데이터 소스 역할을 합니다. *중복 환불*, *FX 변동*, *월말 cutoff 타이밍 차이* 같은 anomaly를 [[Claude]]가 자동 분류해 사용자에게 보고합니다.
