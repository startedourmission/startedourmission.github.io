---
date: 2026-05-19
tags:
  - 정보
description: "OpenAPI 스펙에서 다국어 SDK를 자동 생성해 주는 개발자 도구 회사. 2022년 Alex Rattray가 창업했고 2026년 5월 Anthropic에 인수되었습니다."
---

Stainless는 OpenAPI 스펙을 입력받아 TypeScript, Python, Go, Java, Kotlin 등 여러 언어의 SDK를 자동 생성해 주는 개발자 도구입니다. 2022년 Alex Rattray가 창업했고 2024년 12월 [[a16z]] 리드로 $25M 시리즈 A를 마쳤습니다. 2026년 5월 [[Anthropic]]에 약 $300M 이상으로 인수되었습니다.

## 창업 배경

창업자 Alex Rattray는 [[Stripe]] 개발자 플랫폼 팀에서 Stripe의 API 클라이언트 라이브러리 자동 생성 시스템을 만들었습니다. Stripe의 API 문서와 SDK 품질이 업계 표준이 된 데에는 이 시스템이 기여했고, Rattray는 그 경험을 일반화해 모든 API 회사가 같은 품질의 SDK를 가질 수 있도록 만들겠다는 비전으로 Stainless를 시작했습니다.

## 작동 방식

API 회사가 OpenAPI 스펙을 입력하면, Stainless가 AI 기반 컴파일러로 각 언어의 관용구에 맞는 SDK를 생성합니다. 단순 코드 자동화가 아니라 언어별 네이밍 규칙, 에러 처리 패턴, 페이지네이션 헬퍼 등 "그 언어 개발자라면 이렇게 짰겠다" 싶은 코드를 만듭니다. 이후 MCP 서버, CLI 도구로도 영역을 넓혔습니다.

## 주요 사용처

[[Anthropic]]의 모든 공식 SDK는 처음부터 Stainless가 생성했습니다. [[OpenAI]], Google, Cloudflare, Replicate, Runway 등 경쟁사들도 Stainless를 통해 SDK를 만들었습니다. 수백 개 기업이 유료로 사용했고 매주 수백만 명의 개발자가 Stainless가 만든 SDK를 다운로드하던 사실상의 AI SDK 표준 도구였습니다.

## 인수 후

Anthropic은 인수와 함께 Stainless 호스팅 제품 전체를 단계적으로 종료한다고 발표했습니다. 기존 고객들은 이미 생성된 SDK의 소유권과 수정 권한은 유지하지만, 향후 새 버전 생성이나 자동 업데이트는 받지 못합니다. [[MCP]] 도구 부분은 Claude 플랫폼에 통합됩니다.
