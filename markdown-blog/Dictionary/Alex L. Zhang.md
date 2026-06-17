---
type: person
description: Recursive Language Models 1저자, MIT CSAIL 박사과정, 언어모델이 비효율적으로 쓰이는 지점을 파고드는 연구자
tags:
  - 인물
  - LLM
  - 머신러닝
aliases:
  - Alex L. Zhang
  - Alex Zhang
---

알렉스 장(Alex L. Zhang)은 MIT CSAIL 박사과정 학생으로, [[Omar Khattab]]과 [[Tim Kraska]]의 공동 지도를 받습니다. 프린스턴 컴퓨터과학과를 수석으로 졸업했고, 학부 시절 Karthik Narasimhan, Khanh Nguyen, Ofir Press, Kai Li의 지도를 받았습니다. 본인 소개에 따르면 "언어모델이 충분히 활용되지 못하거나 비효율적으로 쓰이는 영역"을 주로 파고듭니다.

[[Recursive Language Models]]의 1저자입니다. RLM 아이디어는 정식 논문 이전에 본인 블로그(alexzhang13.github.io)에 올린 글에서 출발했습니다. 긴 프롬프트를 신경망에 통째로 밀어넣는 대신, REPL 환경의 변수로 두고 모델이 코드를 써서 들여다보고 자기 자신을 재귀 호출하게 만든다는 발상입니다. 블로그에서 받은 반응이 좋아 GPT-5·Qwen3-Coder 같은 프런티어 모델로 본격 평가하고 8B 모델을 직접 파인튜닝하는 정식 연구로 키웠습니다.

논문 구현체와 학습 레시피, 트라젝토리까지 GitHub에 공개했습니다(github.com/alexzhang13/rlm). 작은 규모에서 1,000개 샘플만으로 8B 모델을 RLM으로 학습시켜 평균 $28.3\%$ 끌어올린 RLM-Qwen3-8B 실험은 본인이 직접 주도한 것으로 보입니다.
