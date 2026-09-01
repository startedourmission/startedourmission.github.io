---
ready: true
type: concept
description: "공장·발전소·정수장의 설비를 제어하는 산업용 컨트롤러. IEC 61131-3 언어로 프로그래밍하며, 텍스트 언어가 Structured Text(ST)입니다"
tags:
  - 로보틱스
aliases:
  - "Programmable Logic Controller"
  - "프로그래머블 로직 컨트롤러"
  - "PLC"
last_active: 2026
---

## 개요

PLC(Programmable Logic Controller)는 공장 라인, 발전소, 정수 처리 시설 같은 산업 설비를 제어하는 컨트롤러입니다. 센서 입력을 읽고 논리를 계산해 밸브·모터·히터 같은 액추에이터를 구동합니다.

일반 소프트웨어와 결정적으로 다른 점은 **스캔 사이클**입니다. PLC 프로그램은 한 번 실행되고 끝나는 것이 아니라, 입력 읽기 → 로직 실행 → 출력 쓰기를 밀리초 단위로 무한 반복합니다. 그래서 어떤 상태가 스캔 사이를 넘어 유지돼야 하는지, 어떤 값이 매 스캔 다시 계산돼야 하는지를 구분하지 못하면 컴파일은 통과해도 설비가 잘못 움직입니다.

## 프로그래밍 언어

IEC 61131-3 표준이 다섯 가지 언어를 규정합니다. 래더 다이어그램(LD), 기능 블록 다이어그램(FBD), 명령어 목록(IL), 순차 기능 차트(SFC), 그리고 텍스트 언어인 **Structured Text(ST)** 입니다. ST는 Pascal 계열 문법이라 LLM이 생성하기에 가장 다루기 쉬운 갈래이고, LLM 기반 PLC 코드 생성 연구는 대체로 ST를 대상으로 합니다.

기본 단위는 POU(Program Organization Unit)이고, 재사용 가능한 상태 보유 단위가 FB(Function Block)입니다. TON 같은 타이머 블록은 스캔 사이클을 가로질러 상태를 유지하기 때문에 형식 검증이 특히 어렵습니다.

## LLM 코드 생성 연구

- **LLM4PLC** (2024) - 컴파일러와 SMV 피드백을 붙인 초기 ST 생성 연구
- **AutoPLC** (2025) - 벤더 IDE 안에서 사례 검색과 API 추천, 컴파일러 기반 디버깅
- **Agents4PLC** (2026) - 5개 에이전트 폐루프와 PLCverif 검증, 117개 태스크 벤치마크
- **[[SemaPLC - A Project-Grounded, Verification-Gated Agent Harness for PLC Code Generation|SemaPLC]]** (2026) - 명세·컴파일·라이브 런타임 세 층 검증을 종료 조건으로 삼는 하네스

검증 도구로는 ST를 모델 체커 입력으로 번역하는 PLCverif가 널리 쓰이고, 백엔드로 nuXmv를 씁니다.
