---
type: person
description: 전 Alibaba Qwen 팀 테크 리드, OFA(ICML 2022) 및 Qwen 시리즈 주도, 멀티모달 사전학습 연구자
tags:
  - LLM
  - NLP
  - 오픈소스
aliases:
  - Junyang Lin
  - 林俊扬
---

Junyang Lin(林俊扬)은 중국의 AI 연구자로, 베이징 대학교에서 컴퓨터 과학과 언어학을 공부한 뒤 2019년 Alibaba에 입사했습니다. Alibaba Cloud 역사상 가장 젊은 P10급 테크니컬 엑스퍼트 중 한 명으로 알려져 있으며, 2023년부터 2026년 초까지 Qwen 팀의 공식 테크 리드를 역임했습니다. 2026년 3월 Alibaba를 떠났습니다.

대표적인 초기 연구로는 초대형 혼합 전문가 모델 M6와 멀티모달 멀티태스크 모델 OFA(Unifying Architectures, Tasks, and Modalities)가 있습니다. OFA는 ICML 2022에 발표됐으며 단일 모델이 이미지 캡셔닝, 시각 질문 응답, 텍스트 요약 등 다양한 태스크를 통합 아키텍처 하나로 처리할 수 있음을 보였습니다. 700회 이상 인용됐습니다. Chinese-CLIP 역시 그의 주요 기여물로, 중국어 비전-언어 표현 학습의 실용적 기준점을 마련했습니다.

Qwen 테크 리드로서 [[Qwen]] 시리즈 전 세대의 기술 방향을 이끌었습니다. 2026년 1월 기준 Qwen 모델군은 Hugging Face에서 누적 7억 회 이상 다운로드됐고, 오픈소스 커뮤니티에서 약 18만 개의 파인튜닝 파생 모델이 생성됐습니다. NeurIPS 2025에서는 Qwen 팀이 제출한 "Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free"(arXiv:2505.06708)가 Best Paper Award와 Oral 발표(상위 1.5%)를 동시에 수상했으며, Lin은 시니어 저자로 이름을 올렸습니다.

Gated Attention 논문의 핵심 기여는 소프트맥스 어텐션 뒤에 헤드별 시그모이드 게이트를 붙이는 단순한 수정 하나가 30개 이상의 변형 실험에서 일관되게 성능을 끌어올린다는 사실을 3.5조 토큰 규모의 실험으로 증명한 것입니다. 이 발견은 이후 Qwen3-Next 모델에 Gated DeltaNet과 Gated Attention의 조합으로 실제 반영됐습니다.
