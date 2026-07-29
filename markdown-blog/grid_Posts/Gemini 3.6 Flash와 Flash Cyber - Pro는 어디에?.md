---
date: 2026-07-25
tags:
  - 정보
  - LLM
  - 도구
description: "Google이 2026년 7월 21일 Gemini 3.6 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber를 한꺼번에 내놨습니다. 기다리던 3.5 Pro는 없었고, 보안 전용 모델은 공개하지 않았습니다."
---

[[Google]]이 2026년 7월 21일 Gemini 모델 세 개를 동시에 출시했습니다. Gemini 3.6 Flash, Gemini 3.5 Flash-Lite, Gemini 3.5 Flash Cyber입니다.

세 개 다 Flash 계열입니다. 다들 기다리던 3.5 Pro는 이번에도 없었습니다.

## 세 모델

**Gemini 3.6 Flash**는 Google이 워크호스 모델이라 부르는 축입니다. 코딩, 지식 작업, 멀티모달 성능이 올라갔고 출력 토큰 사용량이 최대 17% 줄었습니다. 전작인 3.5 Flash보다 저렴합니다.

**Gemini 3.5 Flash-Lite**는 프런티어급 추론보다 속도와 비용이 중요한 고volume 워크로드를 겨냥합니다. Google은 이 모델을 동급에서 가장 비용 효율적인 모델로 소개했습니다.

**Gemini 3.5 Flash Cyber**는 성격이 다릅니다. 소프트웨어 취약점을 찾고 검증하고 패치하도록 파인튜닝된 모델이며, DeepMind의 코드 보안 에이전트 CodeMender 안에서 동작합니다.

## 토큰 17%가 뜻하는 것

3.6 Flash의 대표 수치가 성능이 아니라 토큰 절감이라는 점이 이번 출시의 성격을 보여 줍니다.

같은 작업에 출력 토큰이 17% 덜 든다면, 출력 단가가 그대로여도 실사용 비용은 그만큼 내려갑니다. 월 1,000만 출력 토큰을 쓰던 워크로드는 830만 토큰이 됩니다. 에이전트처럼 한 요청이 여러 차례 모델을 호출하는 구조에서는 이 차이가 호출마다 누적됩니다.

벤치마크 점수 몇 점이 아니라 단위 작업당 비용을 줄이는 쪽으로 릴리스의 무게중심이 옮겨간 것입니다.

## Cyber를 공개하지 않은 이유

Flash Cyber는 오픈되지 않습니다. 정부와 신뢰할 수 있는 파트너에게만 제한 접근 파일럿으로 제공됩니다.

취약점을 찾고 검증하고 고치도록 훈련된 모델은 같은 능력으로 취약점을 찾아 악용할 수 있습니다. 이중용도가 아니라 사실상 같은 용도이고, 방향만 다릅니다. Google이 이 모델만 접근을 묶은 것은 그 사실을 공개적으로 인정한 결정입니다.

같은 주에 미국 하원에서 [[AI Kill Switch Act - DHS에 모델 종료 권한을 주는 법안|AI Kill Switch Act]]가 발의된 것과 겹쳐 읽으면 맥락이 분명해집니다. 사이버 능력을 갖춘 모델을 누구에게 어디까지 열 것인가가 기업의 자율 판단에서 규제 대상으로 넘어가는 구간입니다.

## Pro는 왜 안 나왔나

Google의 플래그십 Pro 모델은 2026년 2월 이후 갱신되지 않았습니다. Bloomberg 보도에 따르면 내부 성능 목표를 맞추지 못해 3.5 Pro 출시가 지연됐습니다.

Google DeepMind 제품 리드 Logan Kilpatrick은 현재 파트너들과 3.5 Pro를 테스트 중이며 곧 내놓기를 바란다고 밝혔습니다.

같은 발표에서 Google은 Gemini 4를 위한 가장 야심찬 사전학습 런을 이미 시작했다고 했습니다. 3.5 Pro가 아직 안 나온 상태에서 4의 사전학습을 알리는 구성이라, 세대 번호가 실제 출시 순서와 어긋나 있습니다.

## 참고

- [Google releases three new Gemini models, but no 3.5 Pro](https://techcrunch.com/2026/07/21/google-releases-three-new-gemini-models-but-no-3-5-pro/)
- [Google Launches Gemini 3.6 Flash and Cybersecurity Model for Enterprise AI](https://www.eweek.com/news/google-gemini-36-flash-35-flash-lite-cyber-models-2026/)
- [Google Ships Three Gemini Flash Models as Its Flagship Slips](https://www.unite.ai/google-ships-three-gemini-flash-models-as-its-flagship-slips/)
