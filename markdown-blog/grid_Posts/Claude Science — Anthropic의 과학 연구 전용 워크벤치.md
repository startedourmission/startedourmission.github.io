---
date: 2026-07-06
tags:
  - 정보
  - LLM
  - 도구
  - 에이전트
description: "Anthropic이 출시한 과학 연구 전용 Claude 플랫폼. 유전체학·단백질체학·화학정보학 등 60개 이상 과학 데이터베이스를 단일 에이전트 워크벤치로 연결하고, 직접 소외 질환 신약 개발 프로그램도 운영합니다."
---

Anthropic이 2026년 6월 30일 샌프란시스코 행사에서 Claude Science를 공개했습니다. 과학 연구자를 위한 AI 워크벤치로, Claude Code가 소프트웨어 엔지니어링을 위한 것이라면 Claude Science는 과학 연구를 위한 것입니다.

## 무엇인가

Claude Science는 독립적인 새 모델이 아닙니다. Anthropic의 기존 Claude 모델 위에 60개 이상의 과학 도구와 데이터베이스를 연결한 워크벤치입니다. PubMed, Jupyter를 비롯해 유전체학, 단백질체학, 화학정보학, 단세포 분석 도구가 단일 환경 안에 사전 연결되어 있습니다.

연구자가 자연어로 지시하면 Claude Science가 멀티스텝 파이프라인을 자율적으로 실행합니다. 단세포 RNA 시퀀싱, CRISPR 설계, 펩타이드 구조 예측 같은 작업을 전문가 팀이 몇 주에 걸쳐 할 일을 시스템이 대신합니다. 재현성에도 집중해서 어떤 그림이나 결과가 어떤 데이터에서 나왔는지 역추적이 가능합니다.

## 신약 개발 직접 참여

Claude Science 출시와 함께 Anthropic은 자체 신약 개발 프로그램을 시작한다고 발표했습니다. AI 도구를 팔기만 하는 게 아니라 직접 후보 물질을 찾겠다는 뜻입니다. 대상은 소외 질환(neglected disease), 즉 기존 제약사가 수익성이 없다고 포기한 분야입니다.

행사에서 Alexander Tarashansky(Claude Science 개발 총괄)가 실시간으로 시연했습니다. 페닐케톤뇨증(phenylketonuria)이라는 희귀 대사 질환을 치료할 후보 물질을, 자연어 명령 몇 줄로 몇 분 만에 찾아냈습니다. 펩타이드를 설계하고, 효능을 예측하고, 실험에서 가장 성공 가능성이 높은 후보 목록을 추렸습니다.

이 움직임을 만든 것은 Eric Kauderer-Abrams(생명과학 부문 총괄)입니다. Anthropic이 Coefficient Bio를 인수한 것도 이 방향의 일부입니다.

## 경쟁 구도

AI 신약 개발 시장은 세 방향에서 동시에 달아오르고 있습니다.

| 플랫폼 | 출시 | 접근 방식 | 접근 제한 |
| --- | --- | --- | --- |
| Claude Science | 2026-06-30 | 범용 워크플로 + 60개 데이터베이스 | 유료 구독자 전체 베타 |
| Gemini for Science | 진행 중 | AlphaFold·AlphaGenome + 30개 DB | 제한 없음 |
| GPT-Rosalind | 2026-04 | 전문 생물학 추론 모델 | 미국 기업 고객 한정 |

OpenAI의 GPT-Rosalind는 특화된 생물학 추론 모델로 접근이 제한적입니다. Google은 AlphaFold, AlphaGenome 같은 자체 기초 모델에 30개 이상 생명과학 데이터베이스를 묶었습니다. Anthropic은 특화 모델 대신 워크플로 설계로 차별화를 노렸습니다. 연구자에게 더 똑똑한 모델이 아니라 더 나은 작업 환경을 주겠다는 판단입니다.

## 지금 AI 회사가 신약 개발에 들어오는 이유

전통 제약사가 소외 질환을 포기하는 이유는 단순합니다. 환자 수가 적어서 임상 시험 비용을 회수하기 어렵습니다. AI는 이 방정식을 바꿉니다. 후보 물질 탐색 비용이 급격히 낮아지면 수익성이 없던 영역도 진입 가능해집니다.

여기에 파운데이션 모델 연구소들이 이미 필요한 인프라를 갖고 있다는 점이 더해집니다. 대규모 연산, 대용량 데이터 처리, 멀티스텝 추론, 코드 실행. 신약 개발 파이프라인과 AI 연구 인프라 사이의 거리가 생각보다 짧습니다.

## 지금 쓸 수 있는 것

Claude Science 베타는 지금 macOS와 Linux에서 유료 구독자(Pro, Max, Team, Enterprise)에게 열려 있습니다. 연구자라면 Anthropic의 AI for Science 프로그램을 통해 최대 $30,000 상당의 Claude 크레딧을 신청할 수 있습니다. 최대 50개 프로젝트를 지원하며, 신청 마감은 2026년 7월 15일입니다.

Claude Science가 실험실 현장의 반복적인 분석 작업을 얼마나 실질적으로 줄여줄지는 좀 더 지켜볼 필요가 있습니다. 자연어로 파이프라인을 구성한다는 약속은 매력적이지만, 실제로 연구자의 분석 흐름에 맞게 통합되는지가 관건입니다.

---

출처: [Anthropic Claude Science 공식 발표](https://www.anthropic.com/news/claude-science-ai-workbench), [CNBC](https://www.cnbc.com/2026/06/30/anthropic-launches-ai-drug-discovery-program-claude-science.html), [MIT Technology Review](https://www.technologyreview.com/2026/06/30/1139987/claude-science-is-anthropics-newest-flagship-product/), [STAT News](https://www.statnews.com/2026/06/30/anthropic-ai-drug-development/)
