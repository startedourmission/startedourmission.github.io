---
type: product
description: "데이터 통합·온톨로지·앱 빌딩·AI 운영을 하나의 거버넌스 평면에 묶은 팔란티어의 엔터프라이즈 운영 OS"
tags:
  - 정보
aliases:
  - Foundry
  - Palantir Foundry
  - 파운드리
---

Foundry는 [[Palantir]]가 2010년대 중반부터 본격적으로 키워온 엔터프라이즈 데이터·AI 운영 플랫폼입니다. 외부 시스템에서 데이터를 끌어오는 통합 레이어, Python·SQL·시각적 도구로 변환을 정의하는 파이프라인 레이어, 데이터를 비즈니스 객체로 끌어올리는 [[온톨로지]] 레이어, 그 위에 운영 앱을 짓는 Workshop/Slate/Quiver/Vertex/Map, AI를 붙이는 [[AIP]]까지를 하나의 거버넌스 모델 안에 묶습니다.

내부적으로는 **Rubix**라는 자체 Kubernetes 런타임 위에서 동작하고, **Apollo**가 그 위에 무중단 CD를 조율합니다. 같은 코드베이스가 AWS·Azure·GCP·온프레미스·에어갭·FedRAMP 환경 모두에 배포된다는 점이 다른 데이터 플랫폼과 갈리는 지점입니다.

다른 데이터 스택과의 차이는 세 가지로 요약됩니다. 데이터·객체·액션·앱·AI가 **같은 권한·감사·릴리스 모델을 공유**한다는 점, 데이터·코드·온톨로지·앱 모두에 **브랜치 기반 변경 관리**가 적용된다는 점, AIP가 별도 챗봇이 아니라 **온톨로지·액션·함수를 통째로 도구로 쓰는 LLM 오케스트레이터**라는 점입니다.

대표 고객은 미국 국방부, NHS, Airbus(A350 Skywise), BP, SOMPO Holdings 등입니다. 한국에서는 HD현대오일뱅크에서 시작해 2026년 그룹 차원 Foundry+AIP Center of Excellence 설립으로 확장된 HD현대 사례가 가장 크고, KT가 Palantir Worldwide Partner Ecosystem의 한국 첫 공식 멤버로 합류해 있습니다.
