---
type: tool
description: "프랑스 기업 정보·판례 데이터베이스 SaaS, 자체 MCP 서버를 통해 Claude를 법률 AI 에이전트로 확장하는 버티컬 통합의 대표 사례"
tags:
  - 도구
  - 법률
  - SaaS
aliases:
  - "Pappers"
  - "Pappers MCP"
---

Pappers는 프랑스의 기업 정보·법률 데이터베이스 SaaS다. *pappers.fr* 도메인에서 프랑스 기업 등기부등본(Kbis), 재무제표, BO(beneficial owner), 임원 정보를 제공하며, *justice.pappers.fr* 도메인에서는 프랑스 판례(특히 *Cour de cassation* 결정)와 법률 텍스트를 색인·제공한다. 영국의 [Companies House](https://www.gov.uk/government/organisations/companies-house)나 미국의 [EDGAR](https://www.sec.gov/edgar)에 해당하는 위치이지만, 판례 검색까지 한 회사가 묶어 둔 것이 특징이다.

기존에는 변호사·회계사·M&A 실사 팀이 직접 두 사이트를 오가며 자료를 모았다. Pappers는 2026년 자체 **MCP 서버** 를 공개해, [[Claude]] 같은 AI 에이전트가 기업 데이터와 판례를 동시에 쿼리할 수 있게 했다. [[Anthropic]]과 공동으로 공개한 데모에서, Claude가 *Art. L.442-1 II C. com.* (거래관계의 brusque 해지) 사건의 9페이지짜리 분석 그리드 — pin-citation, gap 분석, 결정트리 포함 — 를 생성하는 모습이 시연됐다.

법률 영역에서 [[MCP]] 기반 버티컬 통합이 본격적으로 동작하는 첫 사례 중 하나로, [[Anthropic]]의 *Claude for Small Business* 가 자체 플러그인 포맷으로 SMB를 묶었다면, Pappers는 *오픈 MCP 서버* 로 자기 도메인 데이터를 외부 에이전트에게 노출하는 다른 모델을 택했다.
