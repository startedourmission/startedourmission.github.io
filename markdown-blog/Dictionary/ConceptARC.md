---
ready: true
type: benchmark
description: ARC 유사 과제를 16개 개념 계열로 묶은 벤치마크. 총점 하나에 가려지는 능력 프로파일을 개념 단위로 드러냅니다
tags:
  - 벤치마크
  - AI평가
  - 추론
aliases:
  - Concept ARC
---

Moskvichev, Odouard, Melanie Mitchell이 2023년 TMLR에 낸 벤치마크입니다. ARC 스타일 과제를 공간·의미 개념의 설계된 온톨로지에 따라 16개 계열로 묶었습니다.

계열마다 과제 10개와 테스트 입력 30개가 들어 있습니다. 계열 이름은 ExtendToBoundary, FilledNotFilled, TopBottom2D, CleanUp, HorizontalVertical, Copy, Order 같은 식으로 각각 하나의 시각 연산을 지목합니다.

값은 총점이 아니라 프로파일에 있습니다. 세 테스트 입력을 모두 풀어야 정답으로 세는 strict task accuracy와 입력별로 세는 test-pair accuracy를 함께 보면, 규칙을 제대로 배운 것과 몇 입력에서만 맞힌 것이 갈립니다. 계열당 과제가 10개뿐이라 계열 간 순위는 신뢰구간이 크게 겹칩니다. 순위표가 아니라 프로파일로 읽어야 합니다.
