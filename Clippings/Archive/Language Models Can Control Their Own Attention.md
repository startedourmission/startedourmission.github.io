---
title: "Language Models Can Control Their Own Attention"
source: "https://arxiv.org/abs/2609.02737"
author: "Namgyu Ho, Huzama Ahmad, Woosung Koh, Se-Young Yun, Tal Schuster, Cicero Nogueira dos Santos"
clipped: 2026-09-04
tags: [arxiv, LLM, sparse-attention, KV-cache, long-context]
arxiv: "2609.02737"
pdf: "https://arxiv.org/pdf/2609.02737"
---

# Language Models Can Control Their Own Attention

원문: https://arxiv.org/abs/2609.02737 (arXiv:2609.02737, 2026-09-02)  
PDF: https://arxiv.org/pdf/2609.02737  
기관: KAIST AI + Google DeepMind (Google 공저는 advisory only)

## Abstract gist
긴 컨텍스트에서 디코드 매 스텝이 전체 KV 캐시를 읽는 $O(N)$ 비용을 줄이려는 기존 방법은 프록시 스코어로 토큰을 고르는 **외재적(extrinsic)** 스파스 어텐션이다. 이 논문은 모델이 이미 어디를 봐야 아는지에서 출발해, CoT 안에 어텐션 범위를 **선언**하게 하는 **내재적(intrinsic)** 프로토콜 Declarative Attention(DA)을 제안한다.

모드 세 가지:
- `<global>`: 전체 컨텍스트 탐색(내비게이션)
- `<focus magic_chunks="K">`: 지정 세그먼트만
- `<local>`: 최근 응답만 (컨텍스트 세그먼트 없음)

추론 엔진이 태그 전이를 파싱해 블록 단위 마스크를 만들고, vLLM 블록 테이블 rewrite로 FlashAttention 커널은 그대로 둔 채 읽기만 줄인다.

## 핵심 수치 (zero-shot, 15 long-context tasks)
| 모델 | attended tokens 감소 | accuracy drop |
| --- | --- | --- |
| Gemma-4-31B | 52.0% (13.43M → 6.45M) | 1.27pp (87.01 → 85.74) |
| Qwen-3.6-27B | 31.1% (22.54M → 15.52M) | 2.75pp (85.31 → 82.56) |

- DA-nm(같은 프롬프트, 마스크 없음): accuracy는 vanilla에 가깝지만 attended tokens는 **증가** → 절약은 마스크에서 옴
- 스케일: 백본이 커질수록 vanilla 대비 상대 accuracy↑ (Gemma E4B 29% → 31B 99%)
- Roofline decode wall-clock (B200 bf16 추정): Gemma 0.71×, Qwen 0.77× of vanilla
- HF Papers buzz: 55 (2026-09-04 기준)

## 메모
- Block Transformer(NeurIPS 2024, 같은 랩+Schuster)의 후속 축: 아키텍처가 아니라 **프로토콜**로 어텐션 span 제어
- Huzama의 SpotAttention(외재적 블록 라우팅)과 orthogonal
- thinking mode에서는 프로토콜 실패 → non-thinking만 평가
- agentic tool-turn 세그먼트에 더 자연스러울 가능성 저자 스스로 강조
- 블로그 초안: `markdown-blog/grid_Papers/Language Models Can Control Their Own Attention.md`
