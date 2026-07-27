---
date: 2026-06-21
tags:
  - 정보
  - 반도체
  - AI평가
description: "Qualcomm이 스타트업 Tenstorrent를 80억~100억 달러에 인수 협상 중. Jim Keller가 이끄는 RISC-V 기반 AI 가속기 스타트업으로, 성사 시 Qualcomm의 엣지·데이터센터 AI 가속기 전략에 중대한 전환점."
image: "![[qualcomm-tenstorrent.png]]"
---

> 이 글은 Reuters·The Information(2026-06-15), Tom's Hardware, TechTimes 보도를 바탕으로 작성했습니다.

[[Jim Keller]]가 이끄는 RISC-V 기반 AI 칩 스타트업 Tenstorrent를 Qualcomm이 80억~100억 달러에 인수 협상 중이라는 보도가 나왔습니다. The Information이 2026년 6월 15일 먼저 터뜨렸고 Reuters가 이를 받아 보도했습니다. 양사 모두 공식 코멘트를 거부한 상태입니다.

## Tenstorrent가 만드는 것

Tenstorrent는 캐나다에 본사를 둔 AI 가속기 스타트업입니다. 핵심은 RISC-V 기반 Tensix 코어와 이를 묶어 분산 추론을 구현하는 소프트웨어 스택입니다.

NVIDIA GPU가 단일 가속기 안에서 병렬 연산을 처리하는 방식과 달리, Tenstorrent는 작은 가속기를 네트워크로 이어 추론을 분산합니다. 이 구조의 장점은 규모 조정(scaling)입니다. 추론 부하가 늘면 가속기 수를 더하면 됩니다. 전용 인터커넥트로 묶는 NVIDIA의 NVLink 방식보다 구성 자유도가 높고, 단위 전력당 효율이 유리한 워크로드가 있습니다.

2026년 초 공개한 Galaxy Blackhole 플랫폼은 6U 랙 인클로저에 Tensix 가속기 32개를 탑재하며, 가속기 하나당 RISC-V 코어 768개가 들어갑니다. 엣지 추론부터 소규모 데이터센터까지 커버하는 제품군입니다.

아키텍처 못지않게 주목받는 건 컴파일러 스택입니다. Tenstorrent는 하드웨어와 함께 오픈소스 컴파일러 생태계를 키워왔습니다. CUDA 의존성을 탈피하고 싶지만 대안 소프트웨어 스택이 없어 고민하던 기업들에게 이 부분이 설득력 있습니다.

## Qualcomm이 왜 원하는가

Qualcomm의 전략적 딜레마는 명확합니다. 스냅드래곤 브랜드로 대표되는 모바일 SoC 사업은 성숙했고, 스마트폰 시장 성장세가 꺾였습니다. 데이터센터로 가야 한다는 방향성에는 수년간 이견이 없었지만, 실행은 계속 삐거덕거렸습니다.

Qualcomm의 데이터센터 도전은 실패 이력이 있습니다. 2017년 내놓은 서버 CPU Centriq 2400은 2018년 조용히 사라졌습니다. 2021년에는 서버용 Arm 코어 설계사 Nuvia를 14억 달러에 인수해 재진입을 노렸지만, Arm과 라이선스 소송에 발목이 잡히며 수년을 허비했습니다. 2025년에는 다시 NVIDIA 칩과 연동되는 AI 인퍼런스 가속기 라인업을 발표했습니다.

Tenstorrent는 이 맥락에서 다른 선택지입니다. 자체 아키텍처(RISC-V), 자체 컴파일러 스택, 실제로 팔리는 제품(Galaxy Blackhole), 그리고 [[Jim Keller]]라는 이름이 묶음으로 딸려옵니다. 인수에 성공하면 Qualcomm은 Arm 생태계 의존 없이 AI 가속기 시장에서 독자적인 기술 스택을 보유하게 됩니다.

또 하나의 동기는 타이밍입니다. Intel도 같은 매물에 관심이 있다는 보도가 동시에 나왔습니다. 경쟁 입찰이 붙으면 가격이 올라갑니다. Qualcomm으로서는 지금이 제일 싸게 살 수 있는 시점일 수 있습니다.

## Tenstorrent 입장

Tenstorrent의 밸류에이션 궤적을 보면 이 딜의 맥락이 보입니다. 2024년 12월 시리즈 D에서 20억 달러로 평가받았고, 2025년 말에는 32억 달러로 오른 밸류에이션에 추가 자금 조달을 타진 중이었습니다. 그 수개월 뒤 80억~100억 달러 인수 협상 테이블에 앉아 있는 것입니다.

파는 쪽이 흔쾌히 손 내밀 이유는 있습니다. AI 가속기 시장에서 NVIDIA를 넘어 의미 있는 시장 점유율을 확보하려면 영업·유통·고객 지원에 막대한 투자가 필요합니다. Tenstorrent의 기술 경쟁력은 인정받고 있지만, 독자적으로 그 판을 키울 자본이 충분한지는 별개 문제입니다. 80억 달러라는 숫자는 창업자와 시리즈 D 투자자 모두에게 매력적인 엑시트입니다.

안 파는 이유도 있습니다. Keller가 Tenstorrent에서 쌓아온 것은 단순한 칩 설계가 아닙니다. RISC-V 기반의 오픈 아키텍처로 AI 컴퓨팅의 CUDA 독점 구도를 깨겠다는 비전입니다. Qualcomm 산하로 들어가면 그 방향성이 얼마나 살아남을지 보장하기 어렵습니다. Qualcomm은 Arm 생태계 회사이고 RISC-V 전략이 따로 없습니다.

## 업계 지형 변화

인수가 성사될 경우 파장은 여러 방향으로 뻗습니다.

NVIDIA는 단기 위협을 크게 느끼지 않을 것입니다. Tenstorrent의 제품은 훈련(training) 워크로드보다 추론(inference)에 특화돼 있고, NVIDIA의 핵심 매출인 대형 훈련 클러스터 시장과 직접 겹치지 않습니다. 그러나 Qualcomm의 유통망과 결합하면 엣지 추론 시장에서의 압력은 커집니다.

AMD와 Intel에게는 달갑지 않은 소식입니다. 두 회사 모두 AI 가속기 시장에서 NVIDIA를 추격 중인데, Qualcomm이 Tenstorrent의 RISC-V 스택을 가져가면 Arm/x86 진영의 경쟁이 아닌 새로운 축이 형성됩니다. Intel이 같은 매물에 관심을 뒀다는 보도도 이 위기감의 반영입니다.

Arm 입장에서는 아이러니합니다. Qualcomm의 핵심 파트너이면서 최대 고객인 Qualcomm이 RISC-V 기반 AI 가속기 회사를 사면, Arm 생태계 밖에서 독자 기술 자산을 키우는 행보가 됩니다. 지금도 진행 중인 Qualcomm-Arm 라이선스 긴장과 맞물려 복잡한 신호를 줍니다.

## 가격이 적정한가

80억~100억 달러는 Tenstorrent의 직전 밸류에이션(32억 달러) 대비 2.5~3.1배 프리미엄입니다. 인수 프리미엄 치고는 높지 않습니다. 반도체 인수합병 역사에서 전략적 자산에 3~5배 프리미엄이 붙는 경우는 흔합니다.

다만 Tenstorrent는 아직 증명 단계에 있습니다. Galaxy Blackhole은 출시됐지만 대규모 상업 배포 실적이 공개되지 않았습니다. 기술과 인재(특히 [[Jim Keller]])에 베팅하는 측면이 큽니다. 켈러가 인수 이후에도 남아서 제품을 계속 이끌어줄지가 딜의 실질 가치를 결정합니다. 대규모 인수 직후 핵심 인재가 이탈하는 사례는 반도체 업계에서 드물지 않습니다.

제 생각에는, Qualcomm이 이 딜을 성사시키는 것보다 어려운 문제가 딜 이후에 기다리고 있을 것 같습니다. Centriq 실패, Nuvia 표류를 거친 Qualcomm이 세 번째 데이터센터 도전에서 실행력을 보여줄 수 있을지가 진짜 질문입니다.

> 출처: [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/qualcomm-mulls-taking-over-jim-kellers-tenstorrent-report-claims-deal-for-ai-chipmaker-would-value-the-company-at-between-usd8-billion-and-usd10-billion), [TechTimes](https://www.techtimes.com/articles/318559/20260617/qualcomm-pursues-tenstorrent-10-billion-risc-v-bet-nvidias-blind-spot.htm), The Next Web (2026-06-16)
