---
type: product
description: "Palantir Foundry 위에 얹는 AI 운영 평면. LLM·에이전트·평가·자동화를 온톨로지·액션과 묶어 운영"
tags:
  - LLM
  - 정보
aliases:
  - AIP
  - Palantir AIP
  - AI Platform
---

AIP(AI Platform)는 [[Palantir]]가 [[Foundry]] 위에 얹어 출시한 AI 운영 평면이다. 단독 챗봇 제품이 아니라 Foundry의 [[온톨로지]]·액션·함수를 통째로 도구로 쓰는 LLM 오케스트레이터에 가깝다. 2023년 봄 발표 이후 미국 상장 소프트웨어 기업의 AI 매출 성장세를 견인하는 핵심 라인이 됐다.

주요 컴포넌트는 노코드 블록 기반 AI 함수 빌더 **AIP Logic**, 대화형 에이전트 빌더 **AIP Chatbot Studio**(구 Agent Studio), 설정 없이 바로 채팅하는 **AIP Threads**, 플랫폼 전역 보조 **AIP Assist**, 회귀 평가 **AIP Evals**, 사전 구축 AI 제품 카탈로그 **AIP Now**, 데이터 분석 특화 **AIP Analyst** 등으로 구성된다.

보안 모델이 특징이다. LLM은 도구를 직접 실행하지 않고 호출만 하고, 실제 실행은 **호출 사용자의 권한으로 AIP가 수행**한다. 모든 호출이 감사 로그에 남고 [[Claude]]·GPT·Llama 등 어떤 모델을 붙여도 같은 거버넌스가 적용된다. 2025년 7월 GA된 Palantir MCP 서버를 통해 Cursor·Claude Desktop 같은 외부 IDE도 같은 안전장치 안에서 Foundry를 다룰 수 있다.
