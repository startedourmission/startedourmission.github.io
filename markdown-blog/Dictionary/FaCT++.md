---
date: 2026-05-18
tags:
  - 오픈소스
description: "맨체스터 대학교가 개발한 C++ 기반 OWL DL 추론기. C++로 작성되어 자바 기반 추론기보다 빠른 경우가 많습니다."
---

FaCT++는 영국 맨체스터 대학교가 개발한 OWL DL [[Reasoner]]입니다. 이전 세대인 FaCT(Fast Classification of Terminologies)를 C++로 재구현한 것으로, 이름의 `++`이 그 의미입니다.

자바 기반 [[HermiT]]·[[Pellet]]과 달리 C++로 작성되어, 메모리 사용과 분류 속도에서 유리한 경우가 많습니다. JNI(Java Native Interface)를 통해 Protégé에서도 추론기로 선택할 수 있습니다.

태블로 기반 알고리즘을 사용하며, OWL DL 표준의 거의 모든 기능을 지원합니다. 학술 연구에서 추론기 벤치마크에 자주 포함되는 구현체입니다.

다만 개발이 활발하지 않은 시기가 길어, 산업 현장에서는 HermiT나 Pellet의 점유율이 더 높습니다.
