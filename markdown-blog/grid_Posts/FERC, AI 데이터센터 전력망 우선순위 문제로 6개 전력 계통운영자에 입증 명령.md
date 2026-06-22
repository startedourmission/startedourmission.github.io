---
date: 2026-06-22
tags:
  - 정보
  - Headliner
description: "미국 연방에너지규제위원회(FERC)가 2026년 6월 18일 6개 전력 계통운영자에 Section 206 입증 명령을 발령했습니다. AI 데이터센터의 대규모 전력 연계 요청이 기존 대기열을 뒤흔들고 있기 때문입니다."
image: "![[ferc-datacenter-grid.png]]"
---
> 이 글은 [FERC 공식 보도자료](https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration), [Data Center Dynamics](https://www.datacenterdynamics.com/en/news/ferc-orders-us-grid-operators-to-justify-or-reform-how-data-centers-connect-to-the-grid/), [American Action Forum](https://www.americanactionforum.org/insight/ferc-data-center-orders-accelerate-grid-connection/) 등을 참고했습니다.

2026년 6월 18일, 미국 연방에너지규제위원회(FERC)가 전국 6개 지역 계통운영자에 "입증 명령(show cause order)"을 내렸습니다. AI 데이터센터를 포함한 대형 부하(large load)가 전력망에 연계되는 방식을 현행 규정으로 계속 운영할 수 있는지 스스로 입증하거나, 60일 이내에 요금 체계(tariff)를 개정하라는 명령입니다.

## AI 데이터센터가 전력을 얼마나 쓰는가

AI 열풍의 핵심 인프라는 GPU 훈련 클러스터입니다. Nvidia H100 기준으로 GPU 1만 개 클러스터가 소비하는 전력은 약 30~40MW에 달하며, 100만 GPU를 목표로 하는 초대형 데이터센터 단지는 기가와트 규모로 향합니다. Microsoft, Google, Meta, Amazon이 선언한 각사의 데이터센터 투자 계획을 합산하면 향후 5년간 수백 기가와트의 신규 전력 수요가 집중될 것이라는 전망이 나옵니다.

전력망 연계 대기열(interconnection queue)은 이미 한계에 달한 상태입니다. 미국 내 발전·부하 연계 신청 잔고는 2024~2025년 기준으로 2,600GW를 넘는데, 실제로 연계 완료되는 용량은 연간 30GW 수준에 불과합니다. 신청에서 상업 운전까지 최소 5년이 걸리는 것이 표준입니다. AI 데이터센터는 이 대기열을 건너뛰거나 앞당기는 연계 우선권을 요청하고 있고, 이것이 기존 신청자들과의 충돌을 만들었습니다.

## 대상 ISOs와 빠진 ERCOT

이번 명령의 대상은 FERC 관할 아래 있는 6개 독립 계통운영자(ISO/RTO)입니다.

| 계통운영자 | 관할 지역 |
|-----------|----------|
| PJM Interconnection | 미드-애틀랜틱, 오하이오, 일리노이 등 13개 주 + DC |
| MISO | 중부 평원 ~ 걸프 연안 15개 주 |
| SPP | 오클라호마, 캔자스 등 중남부 |
| CAISO | 캘리포니아 대부분 |
| ISO-NE | 뉴잉글랜드 6개 주 |
| NYISO | 뉴욕 주 |

합산하면 약 2억 명, 30개 이상의 주가 해당합니다.

ERCOT(텍사스 대부분)은 명단에 없습니다. ERCOT은 연방간(interstate) 전력 계통에 연결되지 않고 텍사스 내부에서 독립적으로 운영되는 계통입니다. FPA(Federal Power Act)는 주간 도매 전력 거래에만 적용되므로 FERC의 관할권 자체가 미치지 않습니다. 텍사스가 미국 최대의 AI 데이터센터 허브로 급부상하는 배경에는 이 규제 공백도 있습니다.

## Section 206 입증 명령이란

FERC는 연방전력법(Federal Power Act) Section 206에 근거해 이번 명령을 발령했습니다. Section 206의 구조는 단순합니다. FERC가 특정 요금 체계 또는 관행이 "부당하거나 불합리하다"고 판단할 이유가 있다고 보면, 해당 유틸리티에 현재 관행이 왜 적절한지 스스로 입증하도록 요구합니다. 입증에 실패하거나 입증 대신 자발적 개정안을 제출하면, FERC가 청문회를 열어 강제적 요금 변경을 명령할 수 있습니다.

이번 명령에서 FERC가 각 ISO에 요청한 개정 범주는 다섯 가지입니다.

1. **효율적인 전송 서비스 개발** — 대형 부하가 기존 소형 연계 신청 프로세스에 묶이지 않도록 별도 트랙 또는 패스트트랙을 만들 것.
2. **비용 투명성 및 비용 전가 방지** — 대형 부하 연계에 수반되는 망 보강 비용이 다른 고객에게 전가되지 않도록 명확한 비용 분담 원칙을 마련할 것.
3. **코로케이션 및 자체 발전 수용** — 데이터센터가 인접한 발전소를 직접 짓고 운영하는 방식(behind-the-meter 발전, co-location)을 허용하는 규정을 만들 것.
4. **유연 부하 서비스** — 피크 시간대에 부하를 자발적으로 줄이는 조건으로 전력망 연계를 앞당길 수 있는 옵션을 제공할 것.
5. **발전원 검토 프로세스** — 대형 부하에 전력을 공급할 신규 발전소가 계통에 미치는 영향을 별도로 검토하는 프로세스를 만들 것.

## 코로케이션이 핵심 이슈

이번 명령에서 가장 기술적으로 복잡한 개념은 코로케이션(co-location)입니다. 데이터센터가 발전소 옆에 시설을 짓거나, 부지 안에 자체 발전 설비를 두고, 공중 전력망 의존을 최소화하는 방식입니다. 이는 사실상 대형 부하가 계통 연계 대기열을 우회하는 수단이 됩니다.

Microsoft가 Three Mile Island 원자력 발전소를 직접 구매해 데이터센터에 연계하는 계약을 맺은 사례가 대표적입니다. Google이 소형 모듈 원자로(SMR)와 직접 전력 구매 계약을 체결하고, Amazon이 수력발전소 인근에 대규모 데이터센터 단지를 구축하는 것도 같은 전략입니다.

코로케이션의 문제는 공중 전력망에 연결된 나머지 사용자들입니다. 대형 부하가 망을 우회해 자체 발전으로 간다면, 망 보강 비용과 고정 운영비는 그대로인데 그 비용을 분담할 고객이 줄어듭니다. 일반 가정과 중소기업의 전기요금이 오르는 구조적 원인이 됩니다. FERC가 비용 투명성과 비용 전가 방지를 별도 항목으로 명시한 이유입니다.

## 재생에너지 대기열 문제

현재 전력망 연계 대기열의 대부분은 태양광, 풍력, 배터리 저장장치 프로젝트들로 채워져 있습니다. 2024년 기준 대기열 내 신재생에너지 비율은 70%를 넘습니다. AI 데이터센터에 연계 우선권이 주어지면, 이 재생에너지 프로젝트들이 밀릴 수 있습니다.

이것은 미국 전력 정책 내부의 두 가지 국가 목표가 충돌하는 지점입니다. 하나는 AI 인프라 구축을 통한 기술 경쟁력 확보고, 다른 하나는 탈탄소화를 위한 재생에너지 보급입니다. FERC는 이번 명령에서 이 충돌을 직접 해소하지는 않았습니다. "지역 유연성"을 허용한다는 표현에서 알 수 있듯이, 구체적 우선순위 결정은 각 ISO와 해당 주 규제기관에 맡겼습니다.

에너지부(DOE)는 2025년 10월 크리스 라이트 장관 주도로 이미 FERC에 대형 부하 연계 가속화를 촉구하는 사전 규칙 제안(ANOPR)을 제출한 바 있습니다. 이번 FERC 명령은 그 연장선에서 나온 것으로, 행정부 전체가 AI 인프라를 국가 우선 과제로 보고 있음을 보여줍니다.

## 빅테크의 전략적 맥락

AI 데이터센터에 전력을 공급하는 것은 단순한 인프라 문제가 아닙니다. 훈련 클러스터 규모와 위치는 AI 개발 속도를 좌우하고, 전력 확보 여부가 경쟁 우위 자체가 됩니다. Meta가 루이지애나 주에 2GW급 데이터센터 단지를 발표했고, Microsoft는 2028년까지 500억 달러의 데이터센터 투자를 계획했습니다. 이 규모의 전력을 표준 대기열로 기다리면 2030년대가 됩니다.

FERC 명령은 결과적으로 이 빅테크의 속도 압박에 규제 당국이 응한 것으로 볼 수 있습니다. 동시에 비용 전가 방지와 소비자 보호 조항을 명시함으로써 "AI를 위해 일반 소비자가 전기요금을 부담한다"는 정치적 반발을 의식한 구성이기도 합니다.

60일 후 각 ISO의 응답이 나오면 그 내용이 실제 업계 지형을 바꿉니다. 각 ISO마다 시장 설계와 이해관계자 구성이 달라서 결과가 동일하지 않을 것입니다. 버지니아가 이미 대형 고객에게 수요의 85%를 별도 요금으로 부과하는 모델을 운영하고 있다는 점은 하나의 참고 사례가 됩니다.

---

> 참고: [FERC 공식 보도자료](https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration), [Data Center Dynamics](https://www.datacenterdynamics.com/en/news/ferc-orders-us-grid-operators-to-justify-or-reform-how-data-centers-connect-to-the-grid/), [American Action Forum](https://www.americanactionforum.org/insight/ferc-data-center-orders-accelerate-grid-connection/), [Latitude Media](https://www.latitudemedia.com/news/ferc-to-grid-operators-connect-large-loads-to-transmission-faster/)
