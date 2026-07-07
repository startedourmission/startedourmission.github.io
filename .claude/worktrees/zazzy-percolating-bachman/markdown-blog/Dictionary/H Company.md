---
type: company
description: 파리에 본사를 둔 AI 에이전트 스타트업. Runner H와 Holo 컴퓨터 유즈 VLM 라인업을 만든다
tags:
  - 에이전트
  - 오픈소스
aliases:
  - H Company
  - H (company)
---

H Company는 2023년 파리에서 설립된 AI 에이전트 스타트업입니다. 화면을 보고 클릭하고 입력하는 컴퓨터 유즈 에이전트를 핵심 제품으로 삼고, "에이전트가 일을 대신하고 사람은 차이를 만든다"는 방향을 내세웁니다.

설립진에는 구글 딥마인드 출신 연구자들이 포함됩니다. 창업자는 Laurent Sifre와 Charles Kantor, 그리고 딥마인드 베테랑 Daan Wierstra, Karl Tuyls, Julien Perolat입니다. 2024년 5월 당시 유럽 최대 규모의 AI 시드 라운드였던 2억 2천만 달러를 유치했고, Eric Schmidt, Amazon, Accel, Bpifrance, UiPath, Xavier Niel, Samsung 등이 투자에 참여했습니다.

첫 제품은 2024년 11월 공개한 Runner H입니다. LLM과 소형 비전 언어 모델(VLM)을 결합한 에이전틱 API 플랫폼으로, 브라우저 자동화 작업을 수행합니다. 이후 오픈 웨이트 VLM 라인업인 Holo 시리즈를 내놓았습니다. Holo-1(3B)을 Surfer-H와 묶어 WebVoyager 92.2%를 기록했고, 2026년에는 [[OSWorld]] 기반 데스크톱 컴퓨터 유즈에서 당시 SOTA를 찍은 Holo3을 공개했습니다.

Holo 라인은 웹·데스크톱·모바일을 모두 다루는 GUI 에이전트용 VLM으로, 화면을 좌표 단위로 그라운딩하고 멀티스텝 작업을 실행하도록 학습됩니다. 본 글이 다루는 [[Holo3.1 - Fast and Local Computer Use Agents]]는 이 라인을 0.8B부터 35B-A3B까지 확장하고, 양자화 체크포인트로 온디바이스 실행을 처음 본격 지원한 릴리스입니다. 모델링은 [[피에르루이 스도]]가 이끕니다.
