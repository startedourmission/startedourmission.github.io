---
type: ai-model
date: 2026-06-10
tags:
  - LLM
description: "Anthropic의 Mythos급 AI 모델 시리즈. 고급 사이버보안 능력으로 일반 공개가 제한되며, 일반용 버전은 Claude Fable로 제공된다."
aliases:
  - Claude Mythos
  - Mythos 5
---

# Mythos

Mythos는 [[Anthropic]]이 개발한 최상위 연구급 AI 모델 계열이다. 2026년 4월 처음 공개됐으나, 사이버보안 분야의 능력이 지나치게 강력하다는 판단 아래 일반 공개를 하지 않고 제한된 파트너들(정부 기관, 안보 연구자, 선별된 기업)에게만 접근을 허용했다.

## 성능

[[SWE-bench]] 기준으로 Mythos는 Verified에서 93.9%, Pro에서 77.8%를 기록했다. 이전 세대인 Opus 4.6의 Verified 80.8%, Pro 53.4% 대비 큰 폭의 향상이다. 소프트웨어 엔지니어링 외에도 단백질 설계 과정을 약 10배 가속화하는 등 과학 연구 영역에서도 주목받는다.

## Fable vs Mythos: 두 가지 접근 경로

Anthropic은 Mythos 기술을 두 가지 경로로 제공한다.

**Claude Fable** (일반용): 동일한 기반 모델에 세 가지 분류기를 추가한 버전이다. 사이버보안, 생물학·화학, 증류(distillation) 영역에서 위험 쿼리를 감지하면 [[Claude Opus]] 4.8로 자동 폴백한다. 전체 세션의 95% 이상은 폴백 없이 Fable이 직접 응답한다.

**Mythos 5** (전문가용): 안전장치가 부분적으로 해제된 버전이다. 사이버 방어 기관(Project Glasswing 파트너)과 선정된 생물학 연구자들에게 접근이 제한된다.

## 안전 정책

Mythos급 모델을 사용하는 모든 트래픽에 30일 보관 의무가 적용된다. Anthropic은 이 데이터를 안전 모니터링 목적으로만 사용하며 모델 훈련에는 쓰지 않는다고 밝혔다. 이전에 제로 보관 계약을 맺은 기업 고객에게도 예외 없이 적용된다.

## 가격

Fable 5와 Mythos 5 모두 입력 $10 / 출력 $50 (백만 토큰 기준). Claude Opus 4.8의 두 배, Mythos Preview의 절반 이하다.
