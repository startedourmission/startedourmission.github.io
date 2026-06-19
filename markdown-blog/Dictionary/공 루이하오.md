---
type: person
description: SenseTime Senior Research Manager. LLMC·QDrop 등 LLM·VLM 경량화·양자화 라인을 이끕니다.
tags:
  - 인물
  - LLM
  - 오픈소스
aliases:
  - Ruihao Gong
  - 공 루이하오
---

Ruihao Gong(공 루이하오)은 SenseTime의 Senior Research Manager이자 베이항대학교 SKLSDE 박사과정으로, 거대 모델 경량화와 양자화 라인을 이끌어왔습니다. 2017년부터 SenseTime 인턴으로 컴퓨터비전 시스템과 모델 양자화에 매달려 왔고, 지금은 SenseTime 내부에서 효율 추론과 배포 자동화의 책임자에 가깝습니다.

대표 작업은 두 갈래입니다. 첫째는 QDrop(ICLR 2022)으로 극저비트 PTQ(post-training quantization)의 안정성을 끌어올린 연구, 둘째는 LLMC(EMNLP 2024 Industry Track) — LLM부터 VLM까지, 정수에서 부동소수점까지, 단일 비트에서 mixed precision까지 다양한 양자화·희소화 알고리즘을 한 툴킷으로 묶은 오픈소스입니다. Neural Networks의 "Model Compression in the Era of LLMs" 특집 게스트 에디터도 맡았습니다.

[[SenseNova-U1]]에서는 Senior Project Lead 6인 중 1인입니다. Phased DMD(arXiv:2510.27684) 같은 distribution matching distillation 기법 — 100 NFE를 8 NFE로 줄이는 step distillation — 의 공저자라는 점이 결정적입니다. U1이 32× 압축률 X2I 생성을 5090·L40S 같은 비교적 평범한 GPU에서 step당 0.4초대로 돌릴 수 있는 것은 그의 라인이 만든 인프라 덕분입니다.
