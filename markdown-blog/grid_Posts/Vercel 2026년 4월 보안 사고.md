---
date: 2026-04-20
tags:
  - 정보
description: "서드파티 AI 도구의 OAuth 앱이 뚫리면서 Vercel 내부 시스템까지 번진 사고. 무엇이 노출됐고, 우리는 무엇을 해야 할까요."
---

2026년 4월 19일, Vercel이 공식 Knowledge Base에 조용히 공지를 올렸습니다. 내부 시스템 일부에 무단 접근이 있었고, 일부 고객의 환경변수(environment variables)가 노출됐다는 내용이었습니다. 공지만 보면 담담하지만, 내부 사정은 그렇지 않았습니다. 침해 경로가 "작은 서드파티 AI 도구"였다는 점 때문입니다. 이 사고가 왜 중요한지, 그리고 Vercel 쓰는 우리가 지금 무엇을 해야 하는지 정리해봤습니다.

## 어떤 일이 있었나

Vercel의 설명을 요약하면 이렇습니다. 작은 서드파티 AI 도구의 Google Workspace OAuth 앱이 먼저 침해됐습니다. 공격자는 그 OAuth 앱을 발판으로 해당 AI 도구를 쓰던 조직의 계정에 들어갔고, 그 중 하나가 Vercel 환경에 접근 권한을 가진 계정이었습니다. 결과적으로 공격자는 Vercel 내부 시스템 일부에 닿았고, "sensitive"로 표시되지 않은 환경변수들을 볼 수 있었습니다.

공지에는 피해 고객 수나 구체적인 시스템 이름은 적혀 있지 않습니다. "limited subset of customers"라고만 표현합니다. 다만 해커 포럼에서는 ShinyHunters를 자칭하는 공격자가 "Vercel에서 훔친 접근 키, 소스 코드, 데이터베이스 데이터, 내부 배포 접근 권한"을 판매한다는 글을 올렸다고 BleepingComputer가 보도했습니다. Vercel이 공식적으로 인정하는 범위와 공격자가 주장하는 범위 사이에는 간극이 있습니다.

## 왜 환경변수가 노출됐나

Vercel의 환경변수는 두 종류로 구분됩니다. 일반 환경변수와 sensitive로 표시된 환경변수입니다. sensitive로 표시된 값은 저장 단계에서 암호화되고 대시보드에서도 가려집니다. 반면 그렇게 표시되지 않은 값은 평문에 가깝게 저장됩니다. API 키, DB 커넥션 문자열, 서드파티 서명 토큰이 이 "일반" 쪽에 들어가 있었다면, 이번 사고에서 그대로 노출됐을 가능성이 높습니다.

문제는 많은 팀이 sensitive 옵션의 존재를 모르거나, 알더라도 "나중에 옮겨야지" 하고 미뤘다는 점입니다. Vercel이 이번 공지에서 sensitive 기능 사용을 반복해서 강조하는 것도 그래서입니다. 기본값이 안전하지 않으면 아무리 기능이 있어도 실제 안전은 오지 않는다는 구조적 문제가 드러난 셈입니다.

## 공급망 공격이라는 형태

이번 사고의 진짜 교훈은 침해 경로입니다. 공격자가 Vercel을 직접 뚫은 게 아닙니다. Vercel을 쓰는 조직이 쓰던 서드파티 AI 도구의 OAuth 앱을 뚫었습니다. 그 앱에 부여된 Google Workspace 권한이 계정을 넘나드는 다리가 됐고, 그 다리를 건너 Vercel까지 온 겁니다.

AI 도구가 많아질수록 우리는 OAuth 동의 화면을 더 자주 봅니다. "이 앱이 당신의 Google Drive, Calendar, Gmail에 접근합니다"에 무심하게 Allow를 누릅니다. 그 순간 우리는 그 앱 개발사의 보안 수준을 우리 조직의 보안 수준에 묶습니다. 이번 사고는 그 묶임이 얼마나 길게 이어질 수 있는지를 보여줬습니다. AI 도구 → Google Workspace → 계정 → Vercel → 고객 환경변수.

## 지금 해야 할 체크리스트

Vercel 프로젝트가 있다면 오늘 안에 최소한 아래 네 가지를 확인하시길 권합니다.

첫째, Vercel의 **Activity Log**(vercel.com/activity-log)에서 의심스러운 접근 기록이 없는지 봅니다. 평소와 다른 IP, 평소와 다른 시간대의 배포, 환경변수 읽기 기록이 있는지 훑어봅니다.

둘째, **모든 환경변수를 점검**합니다. API 키, DB 커넥션, JWT 시크릿, OAuth 클라이언트 시크릿이 sensitive로 표시되어 있는지 확인하고, 표시되지 않은 값은 지금 모두 **회전(rotate)**합니다. Vercel은 이번 공지에서 "노출됐을 수 있다고 가정하고 우선순위를 두어 교체하라"고 명시했습니다.

셋째, Vercel이 아니라 **Google Workspace 쪽의 OAuth 앱 목록**을 보셔야 합니다. admin.google.com의 Security → API controls → Third-party apps에서 조직 구성원들이 허용한 OAuth 앱을 전수조사하고, 쓰지 않는 앱, 출처가 불명확한 AI 도구는 모두 철회합니다.

넷째, **서드파티 AI 도구의 권한 범위**를 재검토합니다. "Gmail 읽기 권한"이 정말 필요한지, "Drive 전체 쓰기"가 정말 필요한지, 꼭 필요한 권한만 남기고 나머지는 회수합니다.

## 이 사고가 남긴 질문

Vercel은 "services remain operational"이라고 했습니다. 기술적으로는 맞습니다. 다만 이 사고가 남긴 질문은 기술보다 구조에 가깝습니다. 우리 조직이 쓰는 수십 개의 SaaS·AI 도구 중, 침해됐을 때 이런 연쇄 반응을 일으킬 만한 권한을 가진 앱이 몇 개나 되는지 답할 수 있을까요. 답이 "모르겠다"에 가깝다면, 이번 공지는 남의 이야기가 아닙니다.

Vercel의 대응 자체는 빠르고 투명한 편이었습니다. OAuth 앱 ID까지 IOC로 공개했고, 법 집행기관에 통보했으며, 조사를 계속 진행 중이라고 밝혔습니다. 그러나 개별 고객 입장에서는 Vercel의 투명성과 무관하게 해야 할 일이 남습니다. 노출 여부와 관계없이 회전을 전제로 움직이는 것이 지금으로선 가장 안전한 기본값입니다.

## 참고 자료

- [Vercel April 2026 security incident (Vercel KB)](https://vercel.com/kb/bulletin/vercel-april-2026-security-incident)
- [Vercel confirms breach as hackers claim to be selling stolen data (BleepingComputer)](https://www.bleepingcomputer.com/news/security/vercel-confirms-breach-as-hackers-claim-to-be-selling-stolen-data/)
- [Vercel Confirms Internal System Breach Linked to Third-Party AI Tool (Techweez)](https://techweez.com/2026/04/19/vercel-data-breach-third-party-ai-tool/)
- [Vercel Security Breach Raises Concerns for Crypto Projects (BeInCrypto)](https://beincrypto.com/vercel-security-breach-internal-systems/)
- [Vercel Breach Exposes AI Tool Supply Chain Risk Ahead of IPO (Startup Fortune)](https://startupfortune.com/vercel-breach-exposes-ai-tool-supply-chain-risk-ahead-of-ipo/)
