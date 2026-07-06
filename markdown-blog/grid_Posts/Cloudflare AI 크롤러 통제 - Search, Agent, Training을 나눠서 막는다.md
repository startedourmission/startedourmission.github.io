---
date: 2026-07-06
tags:
  - 정보
  - 도구
  - LLM
description: "Cloudflare가 AI 트래픽을 Search·Agent·Training 세 유형으로 분류해 웹사이트 운영자가 목적별로 허용 여부를 설정할 수 있는 체계를 발표했습니다. 2026년 9월 15일부터 광고 페이지에서 Agent와 Training은 기본 차단됩니다."
---

Cloudflare가 7월 2일 AI 크롤러 통제 체계를 전면 개편했습니다. 기존 "모든 AI 봇 허용 또는 전면 차단" 이분법에서 벗어나, 크롤러의 목적에 따라 세 가지 유형으로 분류하고 운영자가 각각을 별도로 제어할 수 있게 합니다.

## 왜 지금인가

검색 엔진과 AI 크롤러는 같은 HTTP 요청을 보내지만 목적이 전혀 다릅니다. Googlebot은 링크를 색인해 검색 결과에 반영하고, OpenAI의 GPTBot은 콘텐츠를 모델 학습에 사용합니다. 기존 robots.txt는 이 구분을 표현할 수 없었습니다.

문제는 여기서 그치지 않습니다. 검색 엔진 자체가 AI 기반으로 바뀌고 있습니다. 기존에 검색 트래픽을 허용하던 사이트가 지금은 검색 봇과 학습 봇을 구분하기 어려운 상황에 놓였습니다. "모든 AI 차단"을 선택하면 검색 노출도 잃고, 허용하면 학습 데이터 제공을 막지 못합니다.

## 세 가지 분류

Cloudflare는 AI 봇 트래픽을 세 유형으로 정의합니다.

**Search**: 콘텐츠를 수집·색인해 나중에 답변에 사용하는 봇. AI 검색 엔진과 기존 검색 엔진이 여기에 해당합니다.

**Agent**: 사람을 대신해 실시간으로 작동하는 자동화 행위자. ChatGPT나 Gemini가 웹 탐색을 수행할 때가 Agent 트래픽에 해당합니다.

**Training**: 콘텐츠를 모델 학습 데이터로 수집하는 크롤러. 수집된 데이터가 모델에 영구적으로 흡수됩니다.

웹사이트 운영자는 이 세 유형에 대해 각각 허용·차단·제한을 설정할 수 있습니다. "Search는 허용, Training은 차단"처럼 세밀한 정책이 가능해졌습니다.

## 기술 구현

콘텐츠 사용 수준은 robots.txt의 `Content-Signal` 확장으로 표시합니다.

- `use=immediate`: 크롤링 후 즉시 폐기. 저장이나 재사용 금지
- `use=reference`: 색인, 발췌, 링크 허용. 기본값
- `use=full`: 요약이나 재현 허용

크롤러 신원 확인에는 RFC 7239 기반 `Forwarded` 헤더를 활용합니다. Cloudflare의 BotBase 데이터베이스가 알려진 봇의 분류, 목적, 검증 상태를 관리합니다. 무료 플랜 사용자는 user agent 문자열 기반으로 AI 크롤러를 식별하고, Enterprise 고객은 Cloudflare의 Bot Management 감지 엔진을 통해 더 정밀한 식별을 이용할 수 있습니다.

## 9월 15일 기본값 변경

2026년 9월 15일부터 새 도메인에 대한 기본 설정이 바뀝니다. 광고가 표시되는 페이지에서 Agent와 Training이 기본 차단됩니다. Search는 허용됩니다.

현재 Cloudflare를 사용하는 사이트는 이 기한 전에 설정을 직접 검토해야 합니다. 기본값이 바뀌어도 기존 사이트에는 자동 적용되지 않습니다.

## 웹 운영자에게 무엇이 달라지는가

이 변화의 핵심은 선택지가 생겼다는 것입니다. 지금까지 콘텐츠를 공개하는 웹사이트 운영자는 AI 학습 데이터 제공 여부를 통제할 수단이 사실상 없었습니다. Cloudflare의 이번 체계는 인프라 수준에서 이 통제를 가능하게 합니다.

광고로 수익을 내는 미디어나 콘텐츠 사이트에게는 특히 의미 있습니다. Agent 봇이 콘텐츠를 실시간으로 요약해 사용자에게 전달하면 광고 노출 없이 정보가 소비됩니다. 이 트래픽을 차단하면서도 검색 색인은 유지하는 것이 이제 가능합니다.

한편 제3자가 이 분류를 정확히 적용할 수 있는지는 별개 문제입니다. 봇이 자신의 목적을 정직하게 신고하지 않으면, user agent 기반 감지의 한계는 여전히 있습니다.

---

출처: [Cloudflare 공식 블로그](https://blog.cloudflare.com/content-independence-day-ai-options/), [Help Net Security](https://www.helpnetsecurity.com/2026/07/02/cloudflare-ai-crawler-controls/), [Cloudflare AI Crawl Control 문서](https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/)
