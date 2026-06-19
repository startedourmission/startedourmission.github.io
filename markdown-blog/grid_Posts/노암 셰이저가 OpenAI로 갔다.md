---
date: 2026-06-19
tags:
  - 정보
  - LLM
description: "Transformer 공동 발명자이자 Gemini 공동 리드였던 Noam Shazeer가 2026년 6월 OpenAI로 이동했습니다. Google이 2년 전 27억 달러를 들여 데려온 인물입니다."
image: "![[noam-shazeer-to-openai.png]]"
---
[[노암 셰이저]]가 [[OpenAI]]로 갔습니다. 2026년 6월 18일, 본인이 X에 직접 올린 발표입니다. 직함은 Lead of Architecture Research. 모델을 어떻게 설계할 것인가를 연구하는 자리입니다.

이름이 낯설 수 있지만, 셰이저는 2017년 "Attention Is All You Need" 논문의 공동 저자입니다. [[Transformer]]를 만든 여덟 명 중 한 명이고, 그 구조 위에 [[Gemini]]도 [[ChatGPT]]도 서 있습니다. 지금 LLM 판에서 셰이저급 인물의 이동은 칩이나 데이터센터 발표만큼 무게가 있습니다.

## 왜 이게 큰일인가

Google이 셰이저를 다시 데려온 게 불과 2년 전입니다. 2024년 8월, 약 27억 달러 규모의 [[Character.AI]] 기술 라이선스 딜로 셰이저와 공동 창업자 Daniel De Freitas, 그리고 핵심 연구진을 [[Google DeepMind]]로 흡수했습니다. 회사를 통째로 산 게 아니라 사람과 기술을 가져오는, 사실상의 애크하이어였습니다.

그 비싼 영입의 핵심 인물이 2년도 안 돼 경쟁사로 넘어갔습니다. 27억 달러를 들여 데려온 사람이 Gemini의 공동 리드까지 맡았다가 OpenAI로 간 겁니다. Google 입장에서 이건 단순한 인력 이탈이 아니라 모델 로드맵을 함께 그리던 사람이 빠진 자리입니다.

## 셰이저가 뭘 했길래

Transformer 하나로 끝나는 사람이 아닙니다. 대규모 모델을 실제로 굴리게 만든 기반 기술 상당수가 그의 손을 거쳤습니다.

- 희소 게이팅 Mixture-of-Experts(MoE) — 파라미터를 키우되 토큰마다 일부 전문가만 켜서 연산을 아끼는 방식. 지금 거의 모든 프런티어 모델이 씁니다.
- Mesh-TensorFlow — 모델을 여러 칩에 쪼개 학습하는 모델 병렬화 프레임워크.
- Adafactor — 메모리를 크게 줄인 옵티마이저.
- T5, LaMDA — 초기 대화형·텍스트 생성 모델 연구.

즉 아키텍처를 설계하고 그걸 대규모로 학습 가능하게 만드는 양쪽을 다 아는 사람입니다. OpenAI가 그에게 붙인 직함이 "Architecture Research"인 건 우연이 아닙니다.

## 양쪽의 셈법

[[샘 올트먼]]은 그를 "OpenAI 초창기부터 가장 함께 일하고 싶었던 사람"이라며 "10년이 걸렸다"고 했습니다. 립서비스로 들리지만, OpenAI의 의도는 분명합니다. 모델 성능 곡선이 단순히 데이터와 컴퓨트를 더 붓는 것만으로는 예전만큼 가파르게 오르지 않는 국면에서, 다음 도약은 아키텍처 자체에서 나올 가능성이 큽니다. 그 영역을 처음부터 설계해본 사람을 데려온 겁니다.

Google 입장에서는 아픈 손실입니다. 다만 Gemini는 이미 셰이저 한 사람에 의존하는 단계는 지났고, DeepMind에는 [[데미스 하사비스]] 아래 두꺼운 연구 인력이 있습니다. 그래도 상징성은 큽니다. 27억 달러를 써서 데려온 사람을 2년 만에 라이벌에 내준 건, 지금 AI 인재 시장에서 돈만으로는 사람을 묶어둘 수 없다는 신호입니다.

## 앞으로

제 생각에는 이 이동의 의미는 "스타 한 명이 옮겼다"보다 한 단계 위에 있습니다. 컴퓨트와 데이터의 스케일링이 비싸지면서, 경쟁의 무게추가 다시 아키텍처 연구 쪽으로 돌아오고 있다는 신호로 봅니다. 트랜스포머 다음 구조를 누가 먼저 찾느냐의 싸움이라면, OpenAI는 그 구조를 처음 만든 사람 중 하나를 손에 넣은 셈입니다.

Google이 이 자리를 어떻게 메우는지, 그리고 셰이저가 OpenAI에서 트랜스포머 이후를 들고 나오는지가 다음 관전 포인트입니다.

---

출처: [CNBC](https://www.cnbc.com/2026/06/18/google-gemini-co-lead-noam-shazeer-leaves-for-openai.html), [Calcalist](https://www.calcalistech.com/ctechnews/article/r1je3bzzze), [Silicon Republic](https://www.siliconrepublic.com/business/googles-noam-shazeer-leaving-organisation-join-rival-openai)
