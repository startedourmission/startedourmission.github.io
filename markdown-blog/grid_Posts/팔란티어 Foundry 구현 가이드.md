---
date: 2026-05-14
tags:
  - 정보
image: "![[palantir-foundry-guide.png]]"
description: 팔란티어 Foundry를 실제로 구현한다는 게 무엇인지를 데이터 통합부터 온톨로지·Workshop·AIP·OSDK 배포까지 공식 문서 기반으로 따라갑니다. 단순한 BI 도구가 아니라 데이터·로직·액션을 한 거버넌스 안에 묶는 운영 OS로서 Foundry가 어떻게 짜여 있는지 — 도구 한 줄, 컴포넌트 한 줄까지 정리했습니다.
---
[[온톨로지]] 글에서 [[Palantir]]의 [[Foundry]] 온톨로지가 RDF/OWL과 다른 방향으로 진화했다고 이야기했습니다. 이번에는 그 구체적인 방법을 알아보겠습니다.

Foundry로 무언가를 만든다는 게 실제로 무슨 작업의 연속인지 알아야 합니다. 외부 DB에서 데이터를 끌어오는 첫 줄부터, 온톨로지에 매핑하고, Workshop 앱을 띄우고, AIP 에이전트를 붙이고, OSDK로 외부 모바일 앱에 노출하기까지의 흐름을 공식 문서 기준으로 따라갑니다.

- palantir.com/docs
- learn.palantir.com

> Foundry의 마케팅 문구를 한 줄 요약하면 "데이터를 의사결정으로 바꿉니다"입니다. 이걸 구현 관점으로 다시 쓰면 다음과 같습니다.
> **Data → Logic → Actions가 같은 거버넌스 평면 위에 올라간 운영 OS.**
> 이 글은 그 운영 OS의 부품들을 하나씩 분해해서 봅니다.

## 1. 플랫폼 전체 구조

Foundry를 처음 접하면 가장 헷갈리는 게 "Foundry"와 "AIP", "Apollo"의 관계입니다. 셋은 같은 레이어가 아닙니다.

| 레이어 | 이름 | 역할 |
| --- | --- | --- |
| 인프라/배포 | **Apollo** | 무중단 CD 컨트롤 플레인. Foundry/AIP 서비스를 환경마다 배포·업그레이드 |
| 데이터 운영 | **Foundry** | 데이터 통합·변환·온톨로지·앱 빌딩 |
| AI 운영 | **AIP** (AI Platform) | LLM·에이전트·평가·자동화 |

Foundry는 내부적으로 **Rubix**라는 Palantir 자체 Kubernetes 런타임 위에서 동작하고, Apollo가 이걸 AWS·Azure·GCP·온프레미스·에어갭(인터넷 차단망)·FedRAMP 환경에 무중단으로 굴립니다. 같은 코드가 SaaS, 전용 클러스터, 정부망까지 모두 도는 게 Palantir의 차별점입니다.

플랫폼은 의사결정을 세 가지 기본 요소로 분해합니다.

- **Data** — 세계에 대한 사실
- **Logic** — 모델·룰·예측
- **Actions** — 실제 세계에 반영되는 결정

이 셋이 결합된 결과물이 **Ontology**이고, Foundry의 거의 모든 도구는 이 셋 중 하나를 다듬는 표면입니다.

## 2. 데이터 통합 — 외부에서 Foundry로

### Data Connection

모든 외부 데이터는 **Data Connection**을 통해 들어옵니다. 핵심 개념은 다섯입니다.

| 개념 | 설명 |
| --- | --- |
| **Source** | 외부 시스템에 대한 연결 정의. URL·인증·네트워크 |
| **Agent** | 사내망·DMZ 안에서 도는 worker. 방화벽 안의 DB를 안전하게 중개 |
| **Sync** | 외부 → Foundry 데이터 이동. Standard / Streaming / File-based / Mediaset |
| **Export** | Foundry → 외부 송출 |
| **Webhook / Listener** | 외부 이벤트 수신(HTTPS, WebSocket, Email, Slack, Jira, Pub/Sub) |

연결 방식은 두 가지입니다. **Agent-Based**(자체 인프라에 깐 에이전트가 중개)와 **Direct Connection**(클라우드 직결). 보안 등급이 높은 고객일수록 Agent 비중이 큽니다.

지원 커넥터는 200개가 넘습니다. 대표적인 것만 적으면:

- 클라우드 스토리지: S3, Azure Blob, GCS
- RDBMS/DW: PostgreSQL, MySQL, Oracle, SQL Server, Snowflake, BigQuery, Databricks
- ERP/CRM: SAP(ECC·S/4HANA 전용 소스 별도), Salesforce, NetSuite, Dynamics
- 협업: Slack, Teams, Jira, Confluence
- REST: 표준 **REST APIs** 커넥터 (구버전 `magritte-rest-v2`는 legacy)

**Magritte**는 Foundry의 에이전트 기반 sync 엔진 내부 코드명입니다. 옛 문서에서 자주 보이지만 신규 명칭은 "Data Connection"으로 통합되는 추세입니다.

### Compass — 파일 시스템과 탐색

Foundry의 모든 리소스(데이터셋, 코드 저장소, Workshop 모듈, 온톨로지 객체)는 **Project** 안에 저장됩니다. Project는 단순한 폴더가 아니라 **1차 보안 경계**입니다. **Compass**는 이 파일 시스템 + 탐색 표면이고, 내부적으로 데이터 카탈로그·Sensitive Data Scanner(PII 자동 탐지)도 끼고 있습니다.

### Data Lineage

데이터셋·온톨로지·코드가 어디서 와서 어디로 가는지 시각화하는 인터랙티브 그래프입니다. 단순 다이어그램이 아니라 운영 도구입니다.

- 업스트림/다운스트림 추적
- 빌드 타임라인(Gantt)
- 스케줄 생성·수정·삭제를 같은 화면에서
- 노드 색상으로 건강 상태·소유권 표시
- 컬럼 기반 역검색 (어디서 이 컬럼이 쓰이고 있나)

영향 분석(impact analysis), 즉 "이 데이터셋을 바꾸면 무엇이 깨지는가"를 빠르게 보는 게 핵심 가치입니다.

## 3. 데이터 변환 — Raw에서 Clean으로

Foundry는 변환 도구를 세 갈래로 제공합니다. 사용자 페르소나가 다릅니다.

### Code Repositories — 데이터 엔지니어용

웹 IDE + Git. 프로덕션 파이프라인의 정식 코드 저장소입니다.

- 언어: **Python**, **Java**, **SQL(Spark SQL)**, **R**, **Containers**(임의 환경)
- `@transform`, `@transform_df` 데코레이터로 함수형 변환 정의
- Branches → Propose a change(PR) → 리뷰/머지의 표준 워크플로우
- 단위 테스트(pytest 등) 인프라 내장
- Project references로 타 프로젝트 자원 참조
- Artifact repositories로 패키지 재사용
- **Ontology imports** — 데이터셋이 아닌 온톨로지 객체 자체를 transform 입력으로 사용

### Code Workspaces — 데이터 과학자용

탐색·모델 개발용 IDE 통합. **JupyterLab**, **RStudio Workbench**, **VS Code**를 Foundry 안에서 띄우고, 데이터 권한·마킹·거버넌스는 그대로 유지합니다. **Dash, Streamlit, Shiny** 앱을 직접 호스팅할 수 있고, 결과물을 Pipeline Builder나 Code Repositories로 승격해 운영화합니다. 옛 **Code Workbook**은 legacy로 분류돼 있어 신규 도입에는 Code Workspaces를 씁니다.

### Pipeline Builder — 시각적 ETL/ELT

데이터 엔지니어와 시민 개발자가 같이 쓰는 그래프+폼 기반 환경입니다. 단순 노코드가 아니라, Foundry의 변환 추상화를 가장 풍부하게 갖춘 도구입니다.

- 변환 노드: Join, Union, Aggregate, Filter, Cast, Geospatial, Media, **LLM nodes**, **Trained model nodes**, Unique ID 생성
- 출력: Dataset, Mediaset, Virtual tables, **Ontology output**, Geotemporal series
- Branches + Propose a change(Code Repositories와 동일 거버넌스)
- **Data expectations**(헬스 체크 인라인 정의)
- **Create a schedule with AIP** — 자연어로 스케줄 명세

Code Repos와의 선택은 단순합니다. 복잡 로직·재사용·테스트 비중이 크면 Code Repos, 협업과 빠른 반복이 우선이면 Pipeline Builder입니다.

### Contour — 분석가용 ad-hoc

표 형식 데이터 위의 path-style 분석 도구입니다. 필터 → 파생 컬럼 → 집계 → 차트의 단계형 파이프를 코드 없이 그리고, 결과를 **Contour Dashboards**로 게시하거나 Workshop에 임베드합니다.

### Build / Schedule / Health Checks

- **Build** — 데이터셋 갱신 트랜잭션 단위. 수동 또는 스케줄
- **Schedule** — Cron 또는 이벤트(upstream 빌드 완료)
- **Health Checks** — 데이터 품질 SLA. Schema, Freshness, Row count, Build duration, Build success rate, Time-based SLA. 실패 시 알람·Automate 연계

여기서 Foundry가 단순 ETL 도구와 갈리는 지점이 나옵니다. **변환·스케줄·헬스체크·알람이 같은 객체에 부착됩니다.** 데이터셋 한 줄에 "어떻게 만들어지고, 언제 망가지면 누구에게 알리고, 어떤 다운스트림이 영향받는지"가 메타데이터로 묶입니다.

## 4. 온톨로지 — 데이터를 객체로 끌어올리기

[[온톨로지]] 글에서 다룬 개념을 Foundry의 실제 구현 도구로 옮겨오면 이렇게 됩니다.

### Ontology Manager

모든 **Object Type / Link Type / Action Type / Function / Interface / Shared Property Types**를 한곳에서 정의·수정·게시하는 앱입니다. 변경은 브랜치/제안 흐름을 따릅니다.

### Object Types

현실 세계 엔티티의 스키마(`Employee`, `Order`, `Vessel`). 객체 한 개는 데이터셋의 한 행이고, **Object Set**은 필터된 행 집합입니다.

매핑할 때 결정해야 하는 것들:

- **Backing datasource** — 객체를 채우는 실제 소스. 데이터셋·스트림·가상 테이블·Restricted View 모두 가능
- **Multi-Datasource Objects (MDOs)** — 한 Object Type을 여러 데이터소스로 분할(예: 부서별·지역별 권한 분리)
- **Primary Key** — 객체의 고유 식별자. OSv2에서는 고유성이 **강제**되며 중복 시 빌드 실패. 결정론적이지 않은 PK는 사용자 edit/링크 손실 위험
- **Title key** — UI 표시용 대표 컬럼
- **Display Properties** — 카드/뷰에 노출할 속성 순서
- **Type Classes** — "이름", "주소", "센서값" 같은 메타데이터 라벨(다른 도구가 의미를 해석)
- **Mandatory control properties** — 권한 결정용 필수 필드(예: `care_center`)

### Link Types

객체-객체 관계. 같은 Object Type 자기 참조(예: `Manager ↔ Direct Report`)도 가능합니다. 카디널리티(1:1·1:N·N:N)와 backing(링크 데이터셋 또는 외래키)을 구성합니다. 서로 다른 Ontology 간 링크는 지원하지 않습니다.

### Action Types — 온톨로지의 "쓰기"

여기가 RDF/OWL과 결정적으로 갈리는 지점입니다. Action Type은 **온톨로지에 쓰기를 수행하는 트랜잭션 단위**입니다.

- **Parameters** — 사용자 입력(드롭다운·기본값·객체 picker)
- **Submission criteria / Validation** — 조건 만족 시에만 실행
- **Edits** — `create`, `modify`, `delete object`, `add link`, `remove link`를 트랜잭션으로 묶음
- **Side effects** — Notifications, **Webhooks**(외부 시스템 호출)
- **Function-backed Actions** — 복잡 로직은 TypeScript/Python Function이 실행
- **Staged writes** — 변경을 검토 후 커밋

OSv2 기준 한 액션이 최대 **10,000개 객체**를 한 트랜잭션으로 편집할 수 있습니다.

### Functions

언어는 **TypeScript v2**(권장), TypeScript v1(legacy), **Python**입니다. 종류는 둘로 나뉩니다.

- **Functions on Objects (FoO)** — 객체셋·객체·링크·미디어를 다루는 함수
- 일반 query/compute 함수 — Workshop 변수, Quiver 집계, Slate query, Action 파라미터 매핑

쓰이는 곳이 굉장히 넓습니다. Workshop의 Function-backed variables, Object Table derived properties, Chart Function aggregations, Function-backed Actions, Notification 동적 콘텐츠, Webhook 파라미터 매핑, Slate Foundry Function 호출, Automate의 function-backed automation. **함수가 온톨로지의 거의 모든 표면에 끼어든다고 보면 됩니다.**

### Interfaces & Shared Property Types

- **Interface** — Object Type의 형태/기능 계약. 폴리모피즘 지원(여러 Object Type이 같은 Interface 구현 → 공통 도구로 처리)
- **Shared Property Types** — 여러 Object Type이 공통으로 쓰는 표준 속성(예: 표준화된 `address`)

이게 있으니까 "운송수단" 인터페이스를 정의하면 `Truck`, `Vessel`, `Aircraft` 객체를 같은 Workshop 컴포넌트로 다룰 수 있습니다.

### Object Storage V2 (OSv2)

객체 백엔드의 차세대 아키텍처입니다. 마이크로서비스로 분리돼 있습니다.

- **Ontology Metadata Service** — 메타데이터
- **Object Storage** — 인덱싱·쿼리
- **Object Set Service** — 읽기 API
- **Actions Service** — 쓰기 API
- **Object Data Funnel** — 데이터소스 → 인덱스 동기화

스케일 한계도 명시돼 있습니다. Object Type 하나에 **수십억 객체**, **최대 2,000개 속성**, **액션당 10,000개 객체 편집**. 증분 인덱싱·스트리밍 데이터소스·MDO·행 단위 권한·스키마 변경 후 사용자 edit 마이그레이션을 지원합니다. 옛 OSv1(**Phonograph**)에서 OSv2로 넘어오면서 PK 중복 불가, 일부 데이터 타입 PK 사용 불가, 비결정론적 PK 금지 같은 제약이 강화됐습니다.

### 데이터셋 → 온톨로지 매핑 시퀀스

실무에서는 이 순서로 갑니다.

1. Ontology Manager에서 **Object Type 생성**
2. **Backing datasource** 추가
3. **Primary Key** 매핑(Funnel이 고유성 검사)
4. **Properties** 매핑, Type class·표준화 옵션 설정
5. **Title key**, **Display properties** 지정
6. **Indexing** — Funnel이 데이터셋을 OSv2에 인덱싱(끝나기 전엔 Workshop/Quiver에서 객체 사용 불가)
7. **Link Types**·**Action Types** 추가
8. **Ontology branch**에서 작업 후 **publish**

## 5. 애플리케이션 빌딩 — 사람이 만지는 화면

### Workshop — 1순위 앱 빌더

객체 지향 드래그앤드롭 앱 빌더입니다. 데스크탑·모바일을 같이 만듭니다.

위젯 카테고리만 보면 Foundry가 단순 BI 도구가 아니라는 게 드러납니다.

- **Core**: Object Table, Object List, Object View, Property List, Links
- **Visualization**: Chart XY, Vega Chart, Map, Gantt Chart, Pivot Table, Time Series Analysis, Image Annotation, Video/Audio Display, PDF Viewer
- **Filtering**: Filter List, Object Dropdown, User Select, Exploration Search Bar
- **Event-trigger**: Button Group, Media Uploader, Comments, Tabs, Inline Action, Audio Recorder
- **Embed**: Iframe, Quiver Dashboard, Vertex Graph, Map Application Template

핵심 개념은 React 비슷합니다. **Variables**(상태) · **Events & Actions**(상호작용) · **Layouts**(반응형) · **Routing** · **Permissions** · **Embedded Modules**(재사용) · **State Saving** · **Mobile**. AIP Agent를 Workshop에 임베드하면, 사용자 컨텍스트(현재 열린 객체, 적용된 필터) 위에서 채팅·자동화가 가능합니다.

### Slate — 풀 커스텀

HTML/CSS/JavaScript 풀 커스터마이즈. Palantir의 **Blueprint** 디자인 시스템 위에서 빌드합니다.

- 위젯 카테고리: Text, Visualization, **Platform**(Foundry Function 호출), **Advanced**(Code Sandbox, File Import, Iframe)
- **Code Sandbox**는 postMessage 기반 샌드박스 iframe. 직접 `fetch` 불가, **SlateFunctions**의 Query를 통해서만 네트워크 호출
- 내장 라이브러리: Lodash, Math.js, Moment, Numeral, es6-shim

Workshop이 80%를 커버하면 Slate가 픽셀 단위 커스텀이 필요한 나머지 20%를 담당합니다.

### Quiver — 분석·대시보드

포인트앤클릭 객체·시계열 분석 도구입니다. 온톨로지 링크가 native라 join이 필요 없습니다(`search around`로 링크 탐색). Formula language로 고급 계산, **Function-backed aggregations**으로 사용자 정의 집계, 시계열 라이브러리로 센서·IoT 신호 처리. 결과를 **Quiver Dashboard**로 게시하고 Workshop에 임베드합니다.

### Vertex — 그래프 시각화

객체·링크의 관계망을 노드/엣지로 시각화합니다. 디지털 트윈의 인과 가시화, 중앙화된 risk 알림, 시나리오 시뮬레이션에 씁니다. Workshop에 embed해서 사용자 워크플로우에 통합합니다.

### Map — 지리공간

전용 지리공간·temporal 분석 표면입니다. **Map Layer Editor**가 포인트앤클릭으로 Vector layers(MVT URL)와 Raster layers(타일셋 URL, opacity·sampling 설정)를 구성합니다. 객체를 위성/벡터 레이어와 겹쳐서 본다든가, 시간 축으로 객체 이동 경로를 보는 식입니다.

### 그 외 표면

- **Notepad** — 분석 보고서. 텍스트 + 차트 + 객체 + 코멘트. Quiver 차트 임베드, AIP 보조
- **Reports** — Legacy. Contour Dashboard 또는 Notepad로 변환 권장
- **Applications Portal** — 노출할 앱을 큐레이션해서 카탈로그처럼 배포

## 6. AIP — LLM이 온톨로지를 도구로 쓰는 평면

AIP가 단순 챗봇이 아니라는 점이 중요합니다. **AIP는 온톨로지·액션·함수를 통째로 도구로 쓰는 LLM 오케스트레이터**입니다.

| 컴포넌트 | 역할 |
| --- | --- |
| **AIP Logic** | 노코드 블록 기반 AI 함수 빌더 |
| **AIP Chatbot Studio** (구 Agent Studio) | 대화형 에이전트 빌더 |
| **AIP Threads** | 설정 없이 바로 채팅 |
| **AIP Assist** | 플랫폼 전역 LLM 보조 |
| **AIP Evals** | 프롬프트·함수 회귀 평가 |
| **AIP Now** | 사전 구축된 AI 제품 카탈로그 |
| **AIP Analyst** | 데이터 분석 특화 에이전트 |
| **Model Catalog** | LLM·임베딩 카탈로그 |
| **Document Intelligence** | 문서 추출/이해 |

### AIP Logic — 블록 기반 함수

LLM-driven 워크플로우를 코드 없이 빌드해서 Foundry function으로 배포합니다. 블록은 단순합니다.

- **Use LLM** — 핵심 블록. 프롬프트 + 도구 + 출력 스키마. 플랫폼에 등록된 모든 LLM 선택 가능
- **Apply action** — LLM 우회, 결정론적 액션 실행
- **Execute function** — TypeScript/Python/Logic 함수 호출
- **Conditionals** — if/else 분기
- **Loops** — 리스트 순회
- **Create variable** — 중간 변수

Use LLM 블록이 받을 수 있는 **도구**가 핵심입니다. 세 분류로 갈립니다.

- **Data**: **Query objects** (객체 타입과 노출할 속성을 명시 — 토큰 효율적)
- **Logic**: **Call function**, **Calculator**
- **Action**: **Apply actions** (LLM이 직접 온톨로지 편집)

여기서 보안 모델이 중요합니다. **LLM은 도구를 직접 실행하지 않습니다.** LLM은 도구 호출을 "요청"만 하고, 실제 실행은 **호출 사용자의 권한으로 AIP Logic이 수행**합니다. 모든 호출은 감사 로그에 남습니다. LLM이 권한 없는 객체를 만지려고 해도 호출자가 권한이 없으면 막힙니다. 이게 [[Claude]] 같은 모델을 엔터프라이즈 데이터에 붙일 수 있는 안전장치입니다.

배포 후엔 **Evals**로 회귀 테스트, **Metrics**로 실행 모니터링, **Automate**로 스케줄/이벤트 트리거를 묶습니다.

### AIP Chatbot Studio

대화형 에이전트 빌더입니다(`+ New > AIP Chatbot` 또는 `Cmd/Ctrl + J`로 진입).

- System prompt — 슬래시(`/`)로 도구·앱 상태 참조
- Model + temperature (0–1)
- Retrieval Context / Application State(Workshop 연동) / Tools
- 2025년부터 **무기한 대화 보존**

사용 가능한 Tools:

1. **Action** — 온톨로지 edit (확인/자동 실행)
2. **Object Query** — 필터·집계·검사·링크 순회
3. **Function** — 임의 Foundry function(AIP Logic 함수 포함, 버전 핀 가능)
4. **Update Application Variable** — Workshop 상태 변경
5. **Command** — 다른 Palantir 앱 명령 실행
6. **Request Clarification** — 사용자에게 추가 정보 요청

**Publish** 하면 Workshop view, AIP Threads, OSDK/Developer Console에서 호출 가능합니다. Monitoring·Usage·Feedback 탭에서 활용 추적이 따라옵니다.

### Modeling Objective & Model Catalog

**Modeling Objective**는 특정 ML 문제(예: 이탈 예측)의 mission control입니다. 권한 레이어 + 자동 균일 평가 + CI/CD(다운타임 없는 모델 교체)가 묶여 있습니다. Submit → Review → Release → Deploy → Monitor의 모델 lifecycle을 강제합니다.

모델은 Ontology에 부착돼서 객체 데이터로 직접 추론할 수 있습니다. **Bring your own model**은 세 갈래입니다. 플랫폼 내(scikit-learn, TF, PyTorch, OR-tools), 외부 임포트(notebook 산출, 3rd party DS 제품, 컨테이너), 외부 호스팅 API 등록.

### Palantir MCP

2025년 7월 GA. 외부 AI IDE/에이전트가 Foundry를 자율적으로 다룰 수 있게 하는 [[MCP]] 서버입니다. Cursor·Claude Desktop이 Foundry에 직접 접속해서 온톨로지를 검색·수정하고, Python transform을 preview·실행하고, OSDK 앱을 빌드하고, Developer Console 앱을 업데이트할 수 있습니다.

## 7. 거버넌스 — 보안·운영·릴리스

Foundry가 정부·금융·헬스케어에서 채택되는 이유의 절반은 거버넌스 모델 때문입니다.

### 보안 프리미티브

| 개념 | 역할 |
| --- | --- |
| **Organization** | 사용자·리소스 사일로의 최상위 경계 |
| **Project** | 1차 보안 경계 (DAC) |
| **Role** | Viewer, Editor, Owner, Discoverer |
| **Marking** | MAC. 데이터 type(예: PII)에 대한 접근 자격 |
| **CBAC** | 분류 등급(예: TS/SCI) 기반 접근 |
| **Restricted View** | 행·컬럼 단위 접근 통제 |
| **Granular policy** | 사용자 속성/컬럼/값 기반 정책 |
| **Project template** | 신규 프로젝트의 보안 기본값 강제 |

**Marking은 권한 부여가 아니라 자격 체크**라는 점이 중요합니다. 프로젝트 오너가 공유해도 사용자가 해당 마킹을 못 가지면 접근 불가입니다. **Restricted View**는 row-level filtering을 적용한 데이터셋 위 정책 객체이고, 객체 타입의 backing source로도 쓸 수 있어서 **row-level object security**가 자연스럽게 됩니다.

### Foundry Branching

데이터·온톨로지·코드·Workshop 모두 **브랜치**가 됩니다. 운영 영향 없이 격리 환경에서 작업 후 머지합니다. Git만 익숙해도 멘탈 모델이 그대로 이어집니다.

### Foundry Rules (Taurus)

저코드 비즈니스 룰 엔진. 데이터셋·객체·시계열에 룰을 적용합니다. AML 의심거래 플래그, 데이터 카테고리화, 장비 모니터링, 마케팅 코호트 같은 데에 씁니다. Rule = Condition + Action 구조라 단순 필터부터 복잡 집계·조인까지 커버합니다.

### Foundry DevOps & Marketplace

**Products**는 데이터셋·온톨로지·Workshop·Function·모델을 하나의 **재사용 배포 단위**로 패키징한 것입니다.

- 환경 분리: Development / Test / Production
- **Release channels**: Release / Pre-stable / Stable, 채널별 자동 업그레이드
- **Maintenance windows**: 업그레이드 시간대 제한
- **Foundry Marketplace**: 조직 내부 또는 Palantir 커뮤니티에 제품 게시

Workflow Lineage도 따로 있습니다. Data Lineage가 데이터셋 흐름이면, **Workflow Lineage**는 온톨로지 객체부터 Workshop 모듈까지의 전체 워크플로우를 추적합니다.

## 8. 외부 연동 — Foundry 바깥과 잇기

### Webhooks / External Functions / External Transforms

- **Webhooks** — Action의 side effect 또는 Function 내부에서 외부 시스템 호출
- **External Functions** — Webhook을 import해서 Function 코드에서 직접 호출
- **External Transforms** — Python Code Repository에서 외부 REST API를 호출해 데이터셋 생성(표준 커넥터로 커버 안 되는 시스템 통합)

### Ontology SDK (OSDK) & Developer Console

**OSDK**는 외부 앱에서 Foundry 온톨로지를 타입 안전하게 사용하는 SDK입니다.

- 언어: **TypeScript**(npm), **Python**(pip/conda), **Java**(Maven), 기타(OpenAPI spec)
- 객체·속성·액션·함수가 자동 타입 생성
- 토큰을 특정 엔티티에 범위 제한 → 최소 권한
- 온톨로지 변경 시 SDK 자동 갱신

**Developer Console**은 OSDK 앱·OAuth 클라이언트를 만드는 표면입니다. 앱별 API 문서가 자동 생성되고, 2026년 2월부터 Developer Console 앱은 **Compass-managed permissions**로 일원화됩니다(프로젝트로부터 roles/orgs/markings 상속).

외부 호출 메커니즘을 정리하면 이렇습니다.

- **OSDK** — 외부 앱이 Foundry 조회/쓰기
- **API Gateway** — Foundry function을 외부 REST로 노출
- **Webhooks** — Foundry → 외부
- **Listeners / External Transforms / External Functions** — 외부 → Foundry

### 배포 환경

Apollo가 모든 환경 공통의 배포 엔진입니다. SaaS, 전용 클러스터, 온프레미스, 에어갭, 미국 정부망(FedRAMP)까지 같은 코드가 도는 게 다른 데이터 플랫폼과 갈리는 지점입니다. **Cloud identities**가 사용자의 AWS/Azure/GCP IAM에 위임 액세스해서 외부 자원에 접근합니다.

## 9. End-to-End 시나리오

위 도구들이 실제로 어떤 순서로 엮이는지가 가장 헷갈리는 부분입니다. Palantir Learn의 "Speedrun your first E2E workflow"를 일반화해서 정리하면 이 흐름입니다.

**1) 소스 연결**
Project 생성 → Source 등록 → (필요 시) Agent 설치 → Sync 정의(스케줄·webhook 트리거)

**2) 원시 데이터셋**
Sync 결과로 raw dataset 생성 → 카탈로그 메타데이터·소유자·태그 부여 → Branch에서 작업 시작

**3) 변환 파이프라인**
Pipeline Builder 또는 Code Repositories로 변환 → Join/정제/표준화 → cleaned dataset 출력 → Data Expectations/Health checks 부착 → 스케줄 등록 → Propose a change → 리뷰 → merge

**4) 온톨로지 매핑**
Object Type 생성 → cleaned dataset을 Backing datasource로 → Primary Key 매핑 → Properties 매핑·Title key 지정 → Link Types 정의 → Funnel 인덱싱 완료 대기

**5) 액션·함수**
Action Types 작성(파라미터·검증·side effect) → Function-backed Action으로 복잡 로직 → Functions on Objects로 파생 속성·집계

**6) 분석 표면**
Quiver 대시보드 → Vertex 관계 그래프 → Map 지리공간 레이어

**7) 운영 앱(Workshop)**
Workshop 모듈 → Object Table/Object View/Filter List → Button을 Action에 연결(writeback) → Quiver/Vertex/Map 임베드 → Variables/Events로 상호작용 → Permissions

**8) AIP 연결**
AIP Logic 함수 작성(Use LLM + Query objects/Apply action) → AIP Chatbot을 Workshop에 임베드 → AIP Evals로 회귀 테스트 → Automate로 자동화

**9) 외부 노출 (선택)**
Developer Console에서 OSDK 앱 등록 → 외부 웹/모바일이 OSDK로 객체 조회·Action 실행 → 또는 Function을 API Gateway로 노출

**10) 배포·릴리스**
Foundry DevOps에서 Product 패키징 → Dev → Test → Prod → Release channels + Maintenance windows → Marketplace 게시 → Data Lineage·Workflow Lineage·Health 대시보드로 모니터링

이 흐름이 한 거버넌스 안에서 끝까지 이어지는 게 Foundry의 핵심 가치입니다. Snowflake로 데이터를 쌓고, dbt로 변환하고, Looker로 보고, Retool로 앱 만들고, LangChain으로 LLM을 붙이고, GitHub Actions로 배포하는 식의 7개 도구 스택을 한 플랫폼이 대체한다는 주장이고, 실제로 정부·방산처럼 권한·감사가 엄격한 환경에서 이 통합이 작동합니다.

## 10. 한국 시장 현황

### HD현대 — 한국 최대·최장 파트너십

2021년 **HD현대오일뱅크**에서 Foundry 도입으로 시작했습니다. 정유 운영 최적화·원유 선택·예지보전·센서 분석을 Foundry 온톨로지 위에 올렸습니다. 이후 조선·해양엔지니어링, 건설장비, 전기시스템, 로보틱스, 마린 애프터마켓으로 확대됐고, 2026년 1월에는 그룹 차원 전략적 파트너십이 다시 확장돼 **Foundry+AIP의 Center of Excellence** 설립이 발표됐습니다. Siemens와 함께 조선소 자동화·디지털 트윈(Future of Shipyard)을 만들고, 무인 수상정(USV) 자율 운용 시스템도 공동 개발 중입니다.

### KT — Palantir의 한국 첫 공식 파트너

**Palantir Worldwide Partner Ecosystem**의 한국 첫 공식 멤버입니다. 클라우드 기반 작업 환경 구축 + Foundry/AIP 사내 적용을 진행 중이고, 2025년 **AX Leaders Summit**을 개최해 [[Alex Karp]]가 대한항공·메리츠금융·LS Electric·POSCO Holdings 같은 한국 대기업 CEO들과 회동했습니다. 한국 시장 확장의 게이트웨이 역할입니다.

### 다른 한국 대기업

삼성·KAI·한화의 직접 도입 보도는 공개 자료상 확인되지 않습니다. 다만 KT 파트너십을 통한 간접 도입 가능성과 AX Leaders Summit 회동을 통한 추진 의향은 시사됩니다. 한국 대기업의 일반적인 도입 패턴(PoC → 단위조직 적용 → 그룹 확산)을 따라가는 HD현대 케이스가 향후 표준이 될 가능성이 큽니다.

## 11. 정리하며

Foundry가 다른 데이터 플랫폼과 갈리는 지점은 결국 세 가지입니다.

첫째, **데이터 → 객체 → 액션 → 앱 → AI가 같은 거버넌스 평면 위에 올라갑니다.** 데이터셋을 만든 사람과 액션을 호출할 사람과 AIP 함수를 평가할 사람이 동일한 권한·감사·릴리스 모델을 공유합니다.

둘째, **브랜치가 데이터·코드·온톨로지·앱 모두에 적용됩니다.** 운영을 건드리지 않고 격리 환경에서 변경하고 머지하는 개발자 워크플로우가 데이터 운영 전체에 확장된 모양입니다.

셋째, **AIP는 별도 챗봇이 아니라 온톨로지·액션·함수를 통째로 도구로 쓰는 LLM 오케스트레이터입니다.** LLM이 직접 실행하지 않고 호출 사용자의 권한으로 실행되는 보안 모델 덕분에 [[Claude]]·[[GPT]]·Llama를 엔터프라이즈 데이터에 안전하게 붙일 수 있습니다.

[[온톨로지]] 글의 마지막 문장은 "아리스토텔레스의 분류가 2,500년 뒤 AI에게 세상을 가르치는 핵심 방법이 됐다"였습니다. 이번 글은 거기에 더해서, 그 분류 위에 **읽기·쓰기·자동화·릴리스**를 묶어내는 게 운영 OS로서의 Foundry가 하는 일이라는 이야기입니다. 개념이 인프라가 되는 지점이 여기입니다.
