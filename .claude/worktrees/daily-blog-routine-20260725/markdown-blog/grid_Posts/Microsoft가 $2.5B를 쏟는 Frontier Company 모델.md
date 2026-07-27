---
date: 2026-07-05
tags:
  - 정보
  - Headliner
  - LLM
  - 에이전트
  - SaaS
description: "Microsoft가 $2.5B를 투자해 Frontier Company를 출범했습니다. Palantir가 원조인 FDE(Forward Deployed Engineering) 모델로, 6,000명의 엔지니어를 기업 고객 안에 심어 AI 파일럿의 90% 실패율을 정면으로 돌파하려는 시도입니다."
image: "![[microsoft-frontier-company.png]]"
---

> 이 글은 [TechCrunch](https://techcrunch.com/2026/07/02/microsoft-launches-its-own-ai-deployment-company-with-2-5-billion-commitment/), [CNBC](https://www.cnbc.com/2026/07/02/microsoft-commits-2point5-billion-6000-employees-ai-implementation-unit.html), [The Decoder](https://the-decoder.com/microsoft-launches-2-5-billion-frontier-company-to-embed-6000-ai-engineers-inside-enterprise-clients/), [GeekWire](https://www.geekwire.com/2026/microsoft-announces-2-5b-frontier-company-to-embed-ai-engineers-inside-customers/) 보도를 참고해 작성했습니다.

## AI 파일럿의 무덤

MIT Project NANDA 연구에 따르면 기업 생성 AI 파일럿의 95%가 손익에 측정 가능한 영향을 전혀 주지 못합니다. 3년째 Copilot을 팔고 Azure AI를 밀어왔는데, 정작 고객사에서 AI가 돈을 버는 경우는 5%에 불과하다는 뜻입니다.

Microsoft가 7월 2일 Frontier Company를 발표한 것은 이 숫자에 대한 직접적인 답변입니다. 공식 발표문에는 "성과 중심의 새로운 AI 배포 모델"이라고 돼 있지만, 실제로는 AI 도구를 파는 것에서 AI가 일하게 만드는 것으로 사업 모델을 전환하겠다는 선언입니다.

## FDE 모델이란 무엇인가

FDE(Forward Deployed Engineering)는 Palantir가 2005년 처음 만든 개념입니다. 고객사에 소프트웨어만 납품하는 대신, 엔지니어를 60-180일간 고객 환경 안에 상주시킵니다. 고객의 업무 맥락을 직접 파악하면서 시스템을 통합하고, 막연한 기업 문제를 실제로 배포 가능한 솔루션으로 바꿉니다.

Palantir가 CIA, NSA, 미 육군 정보부를 고객으로 성공을 거두면서 이 모델이 알려지기 시작했습니다. 전통적인 컨설팅과 다른 점이 있습니다. 컨설턴트는 권고를 하고 떠나지만, FDE는 직접 코드를 씁니다. 고객 환경이 어디서 막히는지 현장에서 체감하면서 해결합니다.

2026년에 들어서며 이 모델을 따라가는 곳이 급증했습니다. Anthropic과 OpenAI도 FDE 벤처에 $4B 이상을 투입했고, Google DeepMind, Databricks, Cohere도 같은 방향으로 움직이고 있습니다. FDE가 12개월 만에 $5.5B 이상 규모의 카테고리가 됐습니다.

## Microsoft가 이 판에서 노리는 것

Microsoft Frontier Company(이하 Frontier Co.)는 별도 법인은 아닙니다. Microsoft 대변인은 "자체 리더십과 재무 책임을 가진 목적 설계 회사"라고 설명했습니다. 실질적으로는 Azure Engineering, Microsoft Consulting Services, 고객 성공 조직에서 내부 이동한 인력이 40%, 외부 채용이 60%로 구성된 6,000명 규모의 전담 조직입니다.

외부 채용 목표는 구체적입니다. 산업별 솔루션 아키텍트, 도메인 특화 데이터 과학자, 변화 관리 전문가입니다. 일반 소프트웨어 엔지니어가 아니라 금융, 의료, 에너지, 제조 같은 특정 산업을 깊이 아는 사람들입니다.

초기 고객으로 Unilever와 Novo Nordisk가 공개됐습니다. 고객 서비스, 구매·조달, 소프트웨어 개발, 금융 프로세스, 에너지 시스템 운영 같은 영역에 에이전트를 심는 것이 목표입니다.

Judson Althoff(Microsoft EVP)는 Frontier Co.가 단순한 FDE 모델을 넘어선다고 밝혔습니다만, 구조 자체는 FDE 원형과 거의 같습니다.

## 왜 지금인가

Microsoft는 그동안 AI를 "도구로서" 팔았습니다. GitHub Copilot, Microsoft 365 Copilot, Azure OpenAI Service가 모두 이 라인입니다. 도구를 팔면 라이선스 수익이 나지만, 도구가 실제로 성과를 내지 못하면 갱신율이 떨어집니다.

기업 AI 채택에서 실제 병목은 모델 품질이 아닙니다. 기업 내 데이터 사일로, 레거시 시스템 통합, 조직 프로세스 변경, 보안과 규정 준수 등 소프트웨어 바깥의 문제들입니다. 이 문제를 API 문서로 해결할 수 없습니다. 사람이 현장에 있어야 합니다.

Frontier Co.의 $2.5B는 이 판단에 대한 베팅입니다. 규모를 보면 단순한 컨설팅 부서 신설이 아닙니다. 6,000명은 많은 IT 서비스 회사 전체 규모입니다.

## SaaS를 대체한다는 말의 실제 의미

FDE 모델에서 자주 나오는 "AI 에이전트가 SaaS를 대체한다"는 표현은 주의가 필요합니다. Salesforce나 SAP 같은 소프트웨어 자체가 없어진다는 뜻이 아닙니다.

지금까지 SaaS는 표준화된 도구를 만들고, 기업이 그 도구에 프로세스를 맞추는 구조였습니다. FDE 모델이 목표하는 것은 반대 방향입니다. 기업의 특정 프로세스를 분석하고, 그 프로세스에 맞게 에이전트를 구성합니다. 소프트웨어가 조직에 맞춰 오는 것입니다.

현실적으로는 두 가지가 공존할 것입니다. 인사, 회계, CRM 같은 범용 영역은 SaaS가 유지됩니다. 기업마다 달라지는 운영 방식, 의사결정 프로세스, 도메인 특화 판단이 들어가는 영역에 에이전트가 들어옵니다.

## 앞으로

Frontier Co.의 성패는 규모가 아니라 반복 가능성에 달려 있습니다. 6,000명이 각기 다른 고객사에 들어가서 처음부터 다 만들면 이건 비싼 컨설팅입니다. 한 산업에서 배운 것이 다른 고객사에 재사용될 수 있어야 사업이 됩니다.

Palantir가 20년에 걸쳐 구축한 것이 바로 이 재사용 레이어입니다. 고객마다 다른 것처럼 보이는 문제들을 Foundry라는 플랫폼 위에서 처리할 수 있게 만든 것입니다. Microsoft가 $2.5B로 얼마나 빨리 비슷한 재사용 레이어를 만들 수 있는지가 관건입니다.

---

> 이 글은 [TechCrunch](https://techcrunch.com/2026/07/02/microsoft-launches-its-own-ai-deployment-company-with-2-5-billion-commitment/), [CNBC](https://www.cnbc.com/2026/07/02/microsoft-commits-2point5-billion-6000-employees-ai-implementation-unit.html), [The Decoder](https://the-decoder.com/microsoft-launches-2-5-billion-frontier-company-to-embed-6000-ai-engineers-inside-enterprise-clients/), [GeekWire](https://www.geekwire.com/2026/microsoft-announces-2-5b-frontier-company-to-embed-ai-engineers-inside-customers/) 보도를 참고해 작성했습니다.
