---
date: 2026-04-23
tags:
  - 정보
  - LLM
description: "Anthropic이 출시하지 않은 모델로 보안을 고치는 프로그램을 시작했습니다. Project Glasswing. 가장 위험한 AI를 가장 방어적인 목적에만 씁니다. 이 역설이 어떻게 작동하는지 들여다봤습니다."
---

Anthropic은 Claude Mythos Preview를 일반에 공개하지 않았습니다. 이유는 하나입니다. 사이버 공격 능력이 너무 강합니다.

그런데 그 모델로 뭔가를 하고 있습니다.

**Project Glasswing.** Mythos Preview를 방어적 사이버보안 목적으로만, 선별된 파트너에게만 제공하는 프로그램입니다. 4월 7일 Mythos 시스템 카드와 함께 공개됐습니다.

---

## 참여 파트너

출시 파트너만 나열해도 규모가 보입니다.

Amazon Web Services, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks.

여기에 40개 이상의 추가 기관이 참여합니다. 주요 운영체제, 웹 브라우저, 클라우드 인프라, 오픈소스 프로젝트를 유지하는 조직들입니다. 수십억 명이 사용하는 소프트웨어의 관리자들입니다.

Anthropic은 이 프로그램에 **최대 $1억의 사용 크레딧**을 약정했습니다. 오픈소스 보안 단체에 별도로 $400만을 직접 기부합니다.

---

## 모델이 실제로 한 일

시스템 카드에 구체적인 사례가 나옵니다.

Claude Mythos Preview는 주요 운영체제와 웹 브라우저에서 **제로데이 취약점을 자율적으로 발견**했습니다. 발견에서 끝나지 않습니다. **작동하는 개념 증명 익스플로잇(PoC)까지 개발**했습니다.

그 중 하나: **17년 묵은 FreeBSD NFS 원격 코드 실행(RCE) 취약점.** 이 취약점은 NFS를 실행하는 머신에서 누구나 root 권한을 획득할 수 있게 합니다. 17년 동안 아무도 발견하지 못했거나, 발견하고도 보고하지 않은 취약점입니다.

이미 수천 개의 고위험 취약점을 발견했다고 합니다. 수치가 과장됐을 가능성을 염두에 두더라도, 방어 측에 이런 도구가 생겼다는 건 의미 있는 변화입니다.

---

## 역설: 가장 위험한 도구를 가장 조심스럽게 쓴다

이 프로그램의 구조가 흥미롭습니다.

공격자는 Mythos Preview 없이도 공격합니다. 이미 있는 도구로, 이미 알려진 취약점으로. 반면 방어자는 아직 모르는 취약점을 먼저 발견해야 합니다. 정보 비대칭이 공격자 쪽에 기울어져 있습니다.

Project Glasswing의 논리는 이 비대칭을 AI로 뒤집자는 것입니다. Mythos Preview를 방어자에게만 먼저 주면, 공격자가 발견하기 전에 취약점을 패치할 수 있다는 것.

Bruce Schneier는 이 구조에 대해 조심스럽게 긍정합니다. "공격 AI가 방어 AI보다 앞서면 이 논리가 무너진다. 지금은 Anthropic이 가장 강한 AI를 가지고 있어서 작동한다."

---

## Vercel 사고와 연결되는 지점

지난주 Vercel 보안 사고를 다뤘습니다. 서드파티 AI 도구의 OAuth 앱이 뚫렸고, 그 경로로 Vercel 내부까지 침해됐습니다.

그 사고는 사람이 한 겁니다. 그나마 기존 방식의 공격이었습니다.

Mythos Preview 수준의 능력을 가진 AI가 공격 도구로 쓰인다면, Vercel 사고보다 훨씬 정교한 공급망 공격이 가능합니다. AI가 코드베이스를 읽고, 제로데이를 발견하고, 익스플로잇을 작성하고, 공격 경로를 계획하는 루프. 자동화된 취약점 발굴과 공격.

Project Glasswing이 방어하려는 게 바로 그 미래입니다.

---

## API 접근과 가격

Mythos Preview는 아래 경로로 접근 가능합니다.

- Claude API 직접
- Amazon Bedrock
- Google Cloud Vertex AI
- Microsoft Foundry (Azure)

가격은 입력 $25/MTok, 출력 $125/MTok입니다. 일반 모델보다 훨씬 비쌉니다. Glasswing 파트너는 Anthropic의 크레딧을 활용합니다.

---

## 전망

Project Glasswing이 성공적이라면, 앞으로 두 가지 질문이 중요해질 것입니다.

하나, 다른 AI 회사들도 비슷한 구조를 채택할 것인가. 가장 강한 모델을 공개하지 않고, 방어 목적에만 제한적으로 쓰는 선례가 생겼습니다.

둘, 이 모델에 접근하지 못한 공격자들은 얼마나 뒤처지는가. 앤트로픽의 $100M 크레딧이 소진되고 Glasswing이 끝난 이후에도 취약점은 계속 생깁니다.

좋은 시작이지만, 끝은 아닙니다.

---

**참고:**
- [Project Glasswing: Securing critical software for the AI era | Anthropic](https://www.anthropic.com/glasswing)
- [On Anthropic's Mythos Preview and Project Glasswing | Bruce Schneier](https://www.schneier.com/blog/archives/2026/04/on-anthropics-mythos-preview-and-project-glasswing.html)
- [The Glasswing Paradox | Picus Security](https://www.picussecurity.com/resource/blog/anthropics-project-glasswing-paradox)
- [Fortune: Anthropic is giving firms early access to Mythos](https://fortune.com/2026/04/07/anthropic-claude-mythos-model-project-glasswing-cybersecurity/)
