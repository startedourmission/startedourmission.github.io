---
type: concept
date: 2026-08-11
ready: true
tags:
  - AI평가
description: "이미지·영상·문서 파일에 출처와 수정 이력을 암호서명으로 실어나르는 개방 표준. Coalition for Content Provenance and Authenticity가 만들었고, 소비자 대상 이름은 Content Credentials입니다."
---

Coalition for Content Provenance and Authenticity의 약자. Adobe, Microsoft, BBC, Intel 등이 참여한 연합이 만든 콘텐츠 출처 표준입니다. 소비자에게 노출될 때는 Content Credentials라는 이름을 씁니다.

## 구조

파일에 매니페스트를 붙입니다. 매니페스트는 언제 어디서 만들어졌는지, 어떤 도구로 무엇이 수정됐는지, AI가 관여했는지를 담은 어서션(assertion)의 묶음입니다. 전체가 암호로 서명되어 있어 파일이 변조되면 서명이 깨집니다. 즉 탬퍼에빈트(tamper-evident) 구조입니다.

AI 생성 여부는 `digitalSourceType` 필드로 표시하고, 어떤 모델이 얼마나 관여했는지는 `c2pa.ai-disclosure` 어서션으로 더 세분화해 담을 수 있습니다. AI 생성/비생성을 이분법으로 나누는 라벨이 아니라, 인간 개입 정도까지 기록하는 쪽으로 확장되고 있습니다.

## 한계

C2PA는 라벨링 시스템이지 방지 시스템이 아닙니다. 정직한 제작자와 플랫폼이 출처를 자발적으로 남기게 해줄 뿐, 매니페스트를 아예 붙이지 않거나 제거하는 악의적 행위자를 막을 방법은 없습니다. 메타데이터 제거 도구도 공개적으로 존재합니다.
