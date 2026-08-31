---
title: "Prompt caching | OpenAI"
source: "https://developers.openai.com/api/docs/guides/prompt-caching"
author: "OpenAI"
clipped: 2026-08-12
tags: [AI, API, cost]
---

# OpenAI Prompt Caching

원문: https://developers.openai.com/api/docs/guides/prompt-caching  
Cookbook: https://developers.openai.com/cookbook/examples/prompt_caching_201 (2026-02-18)

## 핵심
- 정확한 prompt **prefix** 재사용(KV prefill). 보통 ≥1024 토큰.
- 정적 내용(지침·툴·스키마)을 앞에, 가변 유저 입력을 뒤에.
- 캐시된 입력 할인: 신규 모델 최대 **~90%** (예: gpt-5.2 $1.75→$0.175/MTok 쿡북 표). gpt-4o급은 ~50%.
- GPT-5.6+ 계열: cache **write**는 uncached 대비 **1.25×**. 휘발 suffix가 write 되지 않게 explicit breakpoint.
- TTFT 최대 ~80% 단축. Flex Processing은 Batch와 같은 50% 토큰 할인 + 더 나은 캐시 locality.
- 히스토리 compaction/재작성은 캐시를 깨뜨림 → 컨텍스트 엔지니어링과 긴장 관계.
