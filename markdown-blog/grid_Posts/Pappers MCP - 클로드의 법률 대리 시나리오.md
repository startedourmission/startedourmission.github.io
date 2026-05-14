---
date: 2026-05-14
tags:
  - 정보
  - LLM
description: Pappers MCP를 통해 클로드가 프랑스 상법 사건 페이지 분석 그리드를 그대로 출력하는 시연. 회사 데이터와 판례를 동시에 조회해, pin-cite·gap 분석·결정트리까지 변호사가 받아 쓸 수 있는 출력을 만듭니다. 자체 플러그인이 아닌 오픈 MCP 서버로 법률 버티컬을 묶은 사례입니다.
---
[[Anthropic]]이 [[Claude]]와 [[Pappers]]의 협업 데모를 공개했습니다. 프랑스 변호사가 받아 보면 *그대로 사용 가능* 한 수준의 9페이지짜리 사전 분석 문서를, [[Claude]]가 [[Pappers]] [[MCP]] 서버 한 번의 호출로 만들어 내는 시연입니다.

데모의 가상 케이스는 *Google France SARL을 피고로 한 "rupture brutale de relations commerciales établies"* — 한국으로 치면 "지속적 거래관계의 갑작스러운 해지" 분쟁입니다. 프랑스 상법 *Art. L.442-1, II C. com.* 의 5개 요건 분해, 증거·반대증거 매핑, 우선 수집해야 할 자료 10건, 양측 논리 정리, 다음 단계 결정트리까지 한 호흡에 출력됩니다.

이 글은 그 *데모 출력물의 구조* 를 풀어 보면서, [[Pappers]] [[MCP]]가 어떻게 법률 버티컬 AI 에이전트의 한 모델이 되는지를 짚습니다.

## Pappers

[[Pappers]]는 프랑스의 *기업 데이터 + 판례 검색* 통합 SaaS입니다.

- *pappers.fr* — 프랑스 기업 등기부등본(Kbis), 재무제표, BO(실소유자), 임원 변동 정보. 영국 Companies House와 미국 EDGAR의 중간 위치
- *justice.pappers.fr* — 프랑스 판례(*Cour de cassation*, *Cour d'appel*), 법률 텍스트, 행정 결정

기존에는 변호사·회계사·M&A 실사 담당자가 두 사이트를 오가며 손으로 자료를 모았습니다. [[Pappers]]는 2026년 **자체 [[MCP]] 서버** 를 열어, [[Claude]] 같은 에이전트가 기업 데이터와 판례를 **한 호흡에** 쿼리할 수 있게 했습니다.

핵심은 *어느 한 쪽이 아니라 양쪽* 입니다. 회사 정보만 있으면 분석이 사무적이 되고, 판례만 있으면 사실 관계가 빠집니다. 둘이 묶이면 *"이 회사를 상대로 이 사건을 어떻게 짤 것인가"* 라는 변호사의 실제 작업 단위에 닿습니다.

## 데모 출력의 구조

데모 PDF의 본문은 7개 섹션 + 부록으로 구성됩니다. 변호사가 만든 분석 양식과 거의 동일한 구조입니다.

### 1. 신원 확인 (Identification)

피고 [[Pappers]] 데이터로부터 직접 가져온 식별 정보입니다.

> GOOGLE FRANCE SARL — SIREN 443 061 841 · RCS Paris · 8 rue de Londres 75009 Paris · capital 1 000 000 € · NAF 62.02A · effectif 1 000–1 999 salariés (2022) · gérants Paul Manicle (03/05/2019) et Kenneth H. Yi (30/06/2017) · TVA FR64443061841

또한 *공동 피고 잠재성* 으로 *Google Ireland Limited*(유럽 Google Ads/AdSense 실제 계약자) 가능성을 짚어 둡니다. 이 정도 디테일은 단순 RAG로는 안 나옵니다 — 회사 변동 이력·계약 구조에 대한 영역 지식이 결합돼 있습니다.

### 2. 적용 법조문

*Art. L.442-1, II C. com.* — 2019년 4월 24일 ord. n°2019-359로 개정된 현행 조문 전문을 직접 인용합니다. 핵심은 *"브뤼탈한 거래 해지"* 와 *18개월 법정 상한 préavis* 입니다.

### 3. 요건 분해 (Décomposition en éléments)

법조 5요건 + 면책 사유 1개로 분해합니다.

| # | 요건 | 출처 |
| --- | --- | --- |
| 1 | 거래 관계 (relation commerciale) | Cass. com., 28 juin 2023, n° 21-16.940 |
| 2 | 관계가 established 상태 | Cass. com., 15 sept. 2009, n° 08-19.200 |
| 3 | 갑작스러운 해지 (totale ou partielle) | Cass. com., 18 oct. 2023, n° 22-20.438 |
| 4 | 손해 (préavis manquant 기간의 marge brute) | 법정 상한 18개월 |
| 5 | 인과관계 | Art. 1240 C. civ. |
| Exc. | 면책 (중대한 불이행 / force majeure) | L.442-1, II al. 3 |

각 요건마다 *최근 5년 이내 Cour de cassation 결정* 으로 pin-cite가 박혀 있습니다. 변호사가 인용하려면 그대로 가져다 쓰면 됩니다.

### 4. 요건별 상세 분석

각 요건을 다시 sub-element로 쪼개, 4컬럼 표(*소요건 / 입증 증거 / 반대 증거 / 상태*)로 매핑합니다. 상태 컬럼은 색 코드로 가시화됩니다.

- *blanc* — 입증 완료
- *jaune* — 부분 / 다툼 중
- *orange* — 추가 자료 수집 필요 (discovery)
- *rouge* — gap (현재 입증 불가)
- *bleu Pappers* — [[Pappers]] 데이터 참조

이 색 코드 자체가 흥미롭습니다. [[Claude]]가 *어디까지 입증됐고 어디서부터 추가 수집이 필요한지* 를 명시적으로 분류하고, 변호사가 한눈에 액션 아이템을 잡을 수 있게 합니다.

예를 들어 *"관계가 established"* 요건의 한 sub-element는 이렇게 처리됩니다.

> **2.3 합리적인 계속성 예측** — 입증 증거: [PROVISIONNEL — emails, prévisionnels, account manager dédié] · 반대 증거: [PROVISIONNEL — CGU Google Ads contiennent clause de résiliation à tout moment] *Clause CGU ≠ neutralisation L.442-1 II* · 상태: **disputé**

CGU(이용약관)에 "언제든 해지 가능" 조항이 있어도 L.442-1 II는 *공공질서* 성격이라 무력화되지 않는다는 프랑스 법원 판례의 입장까지 한 셀에 압축돼 있습니다.

### 5. Gaps — 사전 통고 전 우선 수집 자료 10건

현재 분석에서 *비어 있는 자료* 를 우선순위로 정렬한 액션 리스트입니다. 한 줄로 압축하면 이렇습니다.

1. 해지 통고 자체의 증빙(이메일·서신·계정 폐쇄 캡처)
2. 원고 회사 3~5개년 재무제표 (Infogreffe 또는 [[Pappers]])
3. 클라이언트별 매출 분석 (60% Google 의존 입증용)
4. 거래 시작일 입증 (첫 BC·첫 인보이스·최초 Google Ads 계정 캡처)
5. 계약 또는 CGU 확보
6. 해지 관련 모든 서면 커뮤니케이션
7. 해지 효과 분석 (인력 감축·투자 손실)
8. 진짜 피고가 누구인지 확정 (Google France vs Google Ireland)
9. *mandat civil* 항변 사전 대응
10. 관할 확인 (TC Paris 전속 — L.442-4, D.442-3)

이 리스트가 데모 출력의 *현실성* 을 결정합니다. 형식만 갖춘 분석은 누구나 할 수 있지만, *지금 변호사가 무엇을 더 모아야 하는가* 까지 짚는 것은 영역 지식 + 케이스 패턴 인식이 필요합니다.

### 6. 양측 논리 정리 + 7. 결정 트리

원고가 강한 부분, 피고(Google)가 안 끼울 항변, 그리고 변호사가 다음으로 취할 수 있는 6가지 옵션 — 사전 통고 발송, 자료 수집, 소장 제출, *référé* (긴급 가처분), CEPC 조정, 기타 — 까지 한 페이지로 정리됩니다.

## 어떻게 가능한가

[[Pappers]] [[MCP]] 서버가 [[Claude]]에게 제공하는 도구는 (공개된 정보상으로) 크게 두 갈래입니다.

- *기업 검색 도구* — SIREN/RCS 기반 조회, 임원 변동 이력, 재무제표 시계열, BO 확인
- *판례 검색 도구* — 키워드·법조문·판결 번호·연도 기반 *Cour de cassation* 결정 검색, 풀텍스트 인용

[[Claude]]는 사건 입력을 받으면 (1) 적용 법조문을 식별하고, (2) 그 법조문의 *요건 결정* 을 검색해 최근 *Cass. com.* 라인업을 끌어오고, (3) 회사 정보로 사실관계를 매핑하고, (4) 색 코드로 입증 상태를 분류한 뒤, (5) 액션 리스트를 결정트리 형태로 출력합니다.

이 5단계가 한 호흡에 도는 이유는 *[[Pappers]] 데이터에 대한 도메인 특화 도구가 [[MCP]]로 노출* 돼 있기 때문입니다. 만약 [[Claude]]가 [[Pappers]] 페이지를 직접 스크레이핑하거나 일반 검색으로 접근했다면, 9페이지짜리 *진짜 변호사 work product* 까지는 못 나옵니다.

## 마무리

이 데모가 변호사 일을 *대체* 한다는 의미는 아닙니다. PDF 본문 끝에 [[Pappers]]도 명시적으로 적어 둡니다.

> *Rappel — ce document est un projet pour analyse et vérification par l'avocat ; il n'est ni une assignation, ni des conclusions, ni un avis juridique.* (이 문서는 변호사의 검토를 위한 초안이며, 소장도 결론서도 법률 의견서도 아니다.)

다만 변호사가 *처음 한 시간에 만들던 사전 분석* 이 *한 호흡* 으로 줄어드는 변화는 분명합니다. 변호사의 시간이 *분석* 에서 *검증* 으로 이동합니다.

지켜볼 포인트는 두 가지입니다.

- *동일 모델이 다른 사법권역으로 확장될 수 있는가* — 미국이라면 [PACER](https://pacer.uscourts.gov)와 EDGAR가, 영국이라면 [BAILII](https://www.bailii.org)와 Companies House가 같은 역할을 할 수 있습니다. 누가 자기 영역의 *MCP 서버* 를 먼저 여느냐가 변수입니다.
- *답변의 안전성* — 색 코드의 *gap / discovery* 분류가 *"여기까지는 알고, 여기부터는 모른다"* 를 명시적으로 드러내는 점이 핵심입니다. 환각이 생기더라도 *"이 셀은 PROVISIONNEL"* 로 표시돼 있어, 변호사가 어디를 검증해야 하는지 자동으로 알 수 있습니다. 이 형식 자체가 안전장치로 기능합니다.
