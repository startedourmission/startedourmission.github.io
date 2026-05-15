---
date: 2026-05-14
type: person
description: University of Arizona 소속 연구자. Predictive Maps of Multi-Agent Reasoning의 1저자로 successor representation을 LLM 멀티에이전트 통신 그래프로 옮긴 분석을 주도.
tags:
  - 인물
  - LLM
  - 머신러닝
aliases:
  - Ethan David James Parks
  - Ethan Parks
---

Ethan David James Parks는 University of Arizona 소속 연구자입니다. 공개된 학회·기관 프로필 흔적이 거의 없는 신진 저자로, 대학 이메일 `edparks@arizona.edu`로만 식별됩니다. arXiv 2605.11453이 공개 트랙에서 잡히는 첫 번째 1저자 논문입니다.

이 연구의 분야 조합 — 강화학습의 successor representation, 그래프 신호처리의 스펙트럼 도구, LLM 멀티에이전트 시스템의 실패 모드 — 은 한 분야의 깊이로는 나오지 않습니다. 강화학습에서 Dayan이 제안하고 Gershman·Momennejad가 신경과학으로 확장한 SR을 가져와, AutoGen·MetaGPT·ChatEval 같은 멀티에이전트 LLM 프레임워크의 chain·star·mesh 토폴로지에 그대로 얹은 것이 핵심 기여입니다. 1저자 단독으로 closed-form 스펙트럼 derivation(부록 A.1), affine-noise 모델의 √k 예측(부록 A.3), 그리고 100 trial × Qwen2.5-7B-Instruct 실험까지 한 트랙으로 묶었습니다.

[[Predictive Maps of Multi-Agent Reasoning - A Successor-Representation Spectrum for LLM Communication Topologies]]은 시니어 [[Dalal Alharthi]]와의 2인 협업입니다. Alharthi의 사이버보안 기반 위에 Parks의 SR·스펙트럼 분석이 얹혀, *공격자가 한 leaf agent만 잡았을 때 condition number κ가 얼마나 부풀어 오르는가*를 묻는 Appendix A.6 같은 줄기가 자연스럽게 본문 골격에 들어갔습니다.
