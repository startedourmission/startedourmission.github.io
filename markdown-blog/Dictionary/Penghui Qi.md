---
type: person
description: 싱가포르국립대(NUS) 연구원. LLM 강화학습의 trust region 문제 전문가. DPPO 제안자.
tags:
  - 인물
  - 강화학습
  - LLM
aliases:
  - Penghui Qi
---

싱가포르국립대(NUS) 소속 연구원. [[Wee Sun Lee]] 교수 그룹에서 LLM 강화학습의 안정성 문제를 연구한다. 2026년 arXiv에 발표한 DPPO 논문("Rethinking the Trust Region in LLM Reinforcement Learning", arXiv:2602.04879)의 제1 저자로, ratio 기반 trust region의 long-tail 어휘 취약성을 이론적으로 분석하고 divergence 기반 마스크(Binary-TV)를 제안했다.

DPPO는 PPO·GRPO의 importance ratio가 저빈도 토큰에서 폭발적으로 커지는 문제를 TV divergence로 대체해 해소했다. 이 연구는 이후 [[Tianyu Pang]] 팀의 DRPO([[Rethinking the Divergence Regularization in LLM RL]])의 직접적 선행 연구가 됐다. DRPO 논문에서 Qi는 프로젝트 리드(Project Lead) 역할을 맡았다.

R1-Zero 류 학습을 비판적으로 분석한 논문("Understanding R1-Zero-Like Training: A Critical Perspective", arXiv:2503.20783)도 [[Tianyu Pang]] 등과 함께 썼다. Training-inference mismatch로 인한 off-policy 문제를 FP16 수치로 극복하는 연구(arXiv:2510.26788)도 공저했다.
