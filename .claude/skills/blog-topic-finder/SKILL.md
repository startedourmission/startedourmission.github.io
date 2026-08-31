---
name: blog-topic-finder
description: Search for blog-worthy topics focused on recent papers, technical deep-dives, and trending tech for the startedourmission blog. launchd cron이 매일 새벽 자동 실행하며, 사용자가 "블로그 주제 뭐 쓸까", "요즘 논문 중에 좋은 거 있어", "arXiv 최신 뭐 있어", "블로그 아이디어 뽑아줘", "주제 찾아줘", "뭐 써야 할지 모르겠어" 라고 말할 때도 트리거. 결과는 stdout으로만 출력 — cron-runner가 blog-topic-finder-cron.md 에 timestamp와 함께 누적 캡처한다. 별도 산출물 파일 없음.
---

# Blog Topic Finder

> `raw/drafts/`는 없어졌습니다 (2026-08-31). 초안은 **목적지 폴더에 직접** `ready: false` 로 만듭니다 — 목적지는 `python3 tools/ready_queue.py --dest <태그…>` 가 알려줍니다.

startedourmission 블로그 전용 주제 탐색 스킬. **헤드리스 자동 실행을 전제로 설계됨** — 사용자 입력 없이 한 흐름으로 끝나야 합니다. arXiv, Hacker News, Hugging Face, GitHub, Papers with Code, 기술 미디어, **한국 개발 커뮤니티(긱뉴스·velog·커리어리)** 등에서 최신 논문·기술 트렌드를 긁어 블로그 후보 목록을 만들어 **stdout으로 출력**합니다. cron-runner.sh 가 stdout 전체를 `blog-topic-finder-cron.md` 에 timestamp와 함께 캡처합니다. 별도 산출물 파일은 만들지 않습니다.

이 블로그의 정체성: **기술 딥다이브 + 논문 리뷰 중심**. 독자가 메커니즘을 이해하고 실제로 써볼 수 있을 수준의 깊이 있는 글.

## 신선도 + 주목도 규칙 (최우선)

**원본 발행일이 오늘 기준 7일 이내**이면서 **화제성(buzz) 시그널이 붙은 것**을 우선한다. 8일 이상 지난 것은 발견해도 무조건 제외.

- 신선도(7일 창)는 강제 게이트. 그 안에서 **주목도 높은 순으로 정렬**해 상위만 올린다. 갓 나온 논문은 화제가 붙는 데 며칠 걸리므로 3일이 아니라 7일로 본다.
- 매일 새벽 자동 실행되므로, 어제·그제 이미 후보로 올린 주제가 다시 올라오면 안 된다 — 중복 방지가 7일 창보다 우선. 최근 `blog-topic-finder-cron.md` 로그를 확인해 이미 올린 건 뺀다.
- 기준일은 `WebSearch`가 반환한 발행일/제출일/푸시일 — 모르면 후보에서 제외.
- 7일 이내 + 주목도 있는 후보가 5개 미만이면 그대로 5개 미만으로 보고. 억지로 안 채운다.

---

## buzz 점수 — 수치 정의

**base = log2(hf + 1) × 20 + log10(citations + 1) × 100**
**cite_factor = 1 − 0.6 / (1 + citations / 5)**
**buzz = round(base × cite_factor)**

- `hf`: HF Papers API upvote 수 (`https://huggingface.co/api/papers/<arXiv_ID>` → `.upvotes`)
- `citations`: Semantic Scholar 인용 수 (`https://api.semanticscholar.org/graph/v1/paper/arXiv:<ID>?fields=citationCount` → `.citationCount`)
- 두 소스를 로그 스케일로 합산한 뒤, 인용 수가 낮을수록 전체 buzz를 곱셈 페널티로 감산한다.
- cite_factor 기준: 0인용 → 0.40 (60% 감산), 5인용 → 0.70, 20인용 → 0.90, 100+인용 → ~1.0
- 커뮤니티 버즈(HF upvote)만 높고 학술 인용이 없는 신규 논문이 오래된 영향력 있는 논문을 과도하게 앞지르지 않도록 설계됨.

```bash
# HF upvote
HF=$(curl -s "https://huggingface.co/api/papers/<arXiv_ID>" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('upvotes',0))" 2>/dev/null || echo 0)
# Semantic Scholar citations (-k: SSL 만료 우회)
CITE=$(curl -sk "https://api.semanticscholar.org/graph/v1/paper/arXiv:<arXiv_ID>?fields=citationCount" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('citationCount',0) or 0)" 2>/dev/null || echo 0)
# buzz
python3 -c "import math; print(round(math.log2($HF+1)*20 + math.log10($CITE+1)*100))"
```

HF에 없는 논문(404) 또는 arXiv가 없는 정보 후보는 `buzz: 0` 으로 처리한다. 정보·잡담 후보는 buzz 필드를 생략한다.

**blog-paper-review 를 통해 생성되는 논문 드래프트의 프론트매터에 반드시 `buzz: <숫자>` 를 추가한다.** blog-topic-finder 가 후보를 선정할 때, 또는 daily-paper-pipeline 이 드래프트를 생성할 때 API를 호출해서 채운다. (`blog-check`의 `buzz-update.py`가 이후 주기적으로 재산정한다.)

---

## 주목도(buzz) 시그널 — 무엇을 "주목받는"으로 보나

7일 창을 통과한 후보를 아래 시그널로 랭킹한다. **이게 이 스킬의 새 핵심이다** — 메커니즘이 좋아도 아무도 안 보는 논문보다, 지금 화제인 논문을 위로 올린다.

| 시그널 | 어디서 | 강함 기준 (참고) |
|--------|--------|------------------|
| **buzz 점수 (복합)** | HF upvote + Semantic Scholar 인용 합산 | 200+ = 강함, 400+ = 매우 강함 |
| **X(Twitter) 화제** | AK(@_akhaliq) 등 큐레이션, 인용·리트윗 | 여러 계정이 동시에 언급 |
| **Hacker News** | news.ycombinator.com | 100+ points / 댓글 활발 |
| **Reddit** | r/MachineLearning, r/LocalLLaMA | upvote·댓글 많은 토론 스레드 |
| **GitHub star 급증** | 논문 코드 repo | 며칠 새 star 수백+ 급증 |
| **한국 커뮤니티 화제** | 긱뉴스(news.hada.io), velog 트렌딩, 커리어리 | 긱뉴스 포인트·댓글 많음 / 여러 곳 동시 언급 |
| **툴 채택 신호** | Show HN, Product Hunt, GitHub 릴리스·star 속도 | Show HN·PH 상위 / 며칠 새 star 급증 |
| **alphaXiv / PwC trending** | alphaxiv.org, paperswithcode.com | trending 목록 등재 |

**복합 buzz 점수가 가장 신뢰도 높은 단일 수치다.** 커뮤니티 화제(HF upvote)와 학술 영향(인용 수) 양쪽을 로그 스케일로 반영해 어느 한쪽 편향을 줄인다. 나머지 시그널은 buzz 점수 옆에 보조 맥락으로 붙인다.

**비-논문 테마(모델릴리스·툴·산업·잡담)는 arXiv/HF/S2 buzz가 없다.** 이 후보들은 **한국 커뮤니티 화제 + 툴 채택 신호를 1순위 랭킹 근거**로 쓰고, 수치를 `근거` 칼럼에 명시한다 (예: `긱뉴스 320pt/58댓글`, `Show HN 1위`, `GitHub +900★/3d`). 논문은 복합 buzz, 비-논문은 채택·커뮤니티 신호 — 테마별로 랭킹 근거가 다르다.

**랭킹·컷 규칙:**
- **buzz 점수를 1순위 정렬 기준**으로 쓴다. buzz가 높을수록 상위.
- 시그널 수치는 표 `근거` 칼럼에 반드시 명시 (예: `buzz 312 (HF 88 / cite 4312)`, `HN 230 pts`, `GitHub +1.2k★/3d`).
- buzz 있는 후보로 5~8개가 차면 buzz 없는 후보는 올리지 않는다. 자리가 부족할 때만 메커니즘이 특출난 무-buzz 후보로 보충하고, 그 경우 `근거` 칼럼에 `(buzz 미확인, 메커니즘 강함)`이라 표기.

---

## 테마 다양성 (buzz와 함께 이 스킬의 두 번째 핵심 축)

이 블로그는 지금 **논문 리뷰로 심하게 쏠려 있다.** 그대로 두면 매일 buzz 상위가 전부 arXiv 논문이라 후보 목록도 논문 일색이 되고, 결국 블로그도 논문만 쌓인다. 그래서 buzz 정렬과 **별개로**, 후보 목록이 아래 5개 테마에 걸쳐 퍼지도록 뽑는다. 이게 buzz만큼 중요한 두 번째 선정 축이다.

| 테마 | 요일 슬롯 | 무엇을 찾나 | 블로그 분류(종류) |
|------|-----------|-------------|-------------------|
| 논문 | 월 | arXiv 신작 논문 (설명할 메커니즘이 있는 것) | 논문 |
| 모델 릴리스 | 화 | 새 모델·제품 출시 (프런티어·오픈웨이트 LLM, 멀티모달, 새 API) | 정보 |
| 툴·오픈소스 | 수 | 개발자 툴·라이브러리·프레임워크·깃허브 화제 | 정보 |
| 산업·비즈니스 | 목 | 기업 전략·정책·시장 구조 변화·인수합병 (펀딩은 아래 게이트 통과한 것만) | 정보 |
| 잡담·에세이 | 금 | 오피니언·에세이·기술 논쟁·커뮤니티 화제 | 잡담 |

요일 슬롯은 `blog-weekly-report`가 쓰는 편집 캘린더와 같다. 후보에 테마를 달아두면 사용자가 그날 슬롯에 맞는 걸 바로 고를 수 있다.

**다양성 규칙 (위 buzz 규칙과 함께 적용):**
- 목표는 "buzz 상위 8개"가 아니라 **"5개 테마를 최대한 덮기"**다. 테마마다 freshest + buzziest 후보를 1~2개씩 골라 올린다. 그러면 자연히 5~8개가 되고 요일 슬롯에 하나씩 배치된다.
- **한 테마가 목록을 독식하지 못한다.** 특히 논문은 한 번에 최대 2~3개까지만. 논문 후보가 아무리 buzz가 높아도 4개째부터는 다른 테마 자리를 위해 양보한다.
- 각 테마 **안에서는** 기존대로 신선도(≤7일) 게이트 + buzz 순 정렬을 그대로 적용한다. 다양성은 테마 간 배분 규칙이지, 테마 안에서 약한 걸 끌어올리라는 뜻이 아니다.
- 어떤 테마에 7일 이내 + 주목할 후보가 없으면 **그 테마는 비워둔다.** 억지로 오래된 걸 끌어오지 않는다. 하루 5테마를 다 채울 필요는 없다. 그날 공백 테마가 있는 건 정상.
- 사용자가 특정 테마/요일을 지정했으면(예: "오늘은 모델 릴리스 쪽으로") 그 테마만 집중 탐색.

---

## 워크플로우

### 1단계 — 기존 게시글 중복 방지 목록 구축

탐색 전에 아래 두 가지를 먼저 수집해 블랙리스트를 만든다.

**① 이미 게시된 arXiv ID 목록** (논문 중복 방지):
```bash
grep -roh --include="*.md" 'arXiv:[0-9]\{4\}\.[0-9]\{4,5\}' \
  "$VAULT/markdown-blog/grid_Papers/" \
  "$VAULT/markdown-blog/<목적지>/" 2>/dev/null \
  | sed 's/.*arXiv://' | sort -u
```
이 목록에 있는 arXiv ID를 가진 논문은 HF upvote가 아무리 높아도 **후보에서 완전히 제외**.

**② 이미 게시된 비논문 주제 목록** (정보·잡담 중복 방지):
```bash
ls "$VAULT/markdown-blog/grid_Posts/"
ls "$VAULT/markdown-blog/<목적지>/"
```
파일명을 훑어 후보 주제와 키워드가 겹치는지 확인한다. 정확히 같은 파일이 없어도 **핵심 키워드(인물명·제품명·사건명)가 겹치면 중복으로 간주**하고 제외한다. (예: "jqwik"가 파일명에 있으면 jqwik 관련 후보 전부 제외)

**② 최근 cron 로그에서 이미 제안한 주제** (당일 재중복 방지):
```bash
tail -200 "$HOME/Library/Logs/blog-daily-routine/blog-topic-finder-cron.md" 2>/dev/null
```
최근 7일 이내 cron 로그에 올라온 제목·arXiv ID와 겹치는 후보도 제외.

두 블랙리스트를 메모해두고, 이후 모든 후보 검토 시 조회해서 걸러낸다.

---

### 1.5단계 — 탐색 범위 확인

사용자가 특정 테마·분야를 지정했으면 그쪽을 집중 탐색. 지정이 없으면 **위 5개 테마를 모두** 탐색 대상으로 삼고, 각 테마 아래 분야를 훑는다.

- **논문**: LLM / NLP / 멀티모달, 컴퓨터비전, 강화학습·RLHF·에이전트, 추론·코딩 AI, 벤치마크·평가 방법론
- **모델 릴리스**: 프런티어 LLM·오픈웨이트 모델·멀티모달/음성/영상 모델·새 API·새 추론 모델
- **툴·오픈소스**: ML 인프라·프레임워크·라이브러리·개발자 툴·깃허브 트렌딩
- **산업·비즈니스**: AI 펀딩·인수·기업 전략·규제/정책·시장 동향
- **잡담·에세이**: 기술 오피니언·에세이·논쟁·커뮤니티 화제(전망, 회고, "왜 X인가" 류)

### 2단계 — 소스별 웹 서치 (7일 이내 한정)

먼저 Bash `date +%Y-%m-%d`로 오늘 날짜를 확인하고 7일 창(today ~ today-6)을 적어둔다. 모든 검색 쿼리에는 **현재 연·월** 또는 **"this week"·"trending"·"today"** 같이 신선도·화제성을 좁히는 단어를 반드시 넣는다. **주목도 소스(HF Papers, X, HN, Reddit)를 먼저 훑어 화제작을 잡고**, arXiv·미디어로 메커니즘을 보강하는 순서가 효율적이다.

`WebSearch` 툴 사용 (deferred → `ToolSearch select:WebSearch`로 먼저 로드). 아래 소스를 병렬로 검색. 위쪽 4개가 주목도 소스, 아래쪽이 메커니즘·보강 소스.

| 소스 | 검색 쿼리 예시 ({YYYY-MM} = 현재 연·월) |
|------|---------------|
| **HF Papers** (trending) | `huggingface papers trending this week`, `huggingface daily papers {YYYY-MM} top upvoted`, `hugging face papers most upvoted today` |
| **X(Twitter) 화제** | `arxiv paper {YYYY-MM} twitter discussion`, `_akhaliq paper this week`, `most discussed AI paper X this week` |
| **Hacker News** | `site:news.ycombinator.com AI this week`, `hacker news machine learning paper top this week` |
| **Reddit** | `site:reddit.com r/MachineLearning {YYYY-MM} paper`, `site:reddit.com r/LocalLLaMA new model this week` |
| **한국 커뮤니티** | `site:news.hada.io {YYYY-MM}`, `긱뉴스 이번 주 AI`, `site:velog.io AI 트렌딩`, `커리어리 AI 이번 주` |
| arXiv | `arxiv {YYYY-MM} LLM new paper this week`, `arxiv this week reasoning`, `arxiv {YYYY-MM} computer vision` |
| alphaXiv / PwC | `alphaxiv trending this week`, `papers with code {YYYY-MM} trending`, `papers with code new benchmark this week` |
| GitHub 트렌딩 | `github trending machine learning this week`, `github trending AI tools this week` |
| 기술 미디어 | `AI research {YYYY-MM} breakthrough`, `LLM news this week site:techcrunch.com OR site:venturebeat.com` |
| 유튜브 | `site:youtube.com AI {YYYY-MM} explained`, `youtube LLM paper review this week`, `youtube ML new model {YYYY-MM}` |

위 표는 논문·화제 위주라 그대로 두면 또 논문만 잡힌다. **비-논문 테마(모델 릴리스·툴·산업·잡담)는 아래 소스를 따로 챙겨 최소 1개 테마당 1후보는 확보하려 시도한다.**

| 테마 | 검색 쿼리 예시 ({YYYY-MM} = 현재 연·월) |
|------|------------------------------------------|
| 모델 릴리스 | `new AI model release this week`, `huggingface trending models this week`, `open weights LLM released {YYYY-MM}`, `OpenAI OR Anthropic OR Google OR Meta OR Qwen OR Mistral new model {YYYY-MM}` |
| 툴·오픈소스 | `Show HN AI tool this week`, `Product Hunt AI {YYYY-MM}`, `github trending AI {YYYY-MM}`, `new LLM framework OR library released this week`, `site:news.hada.io 툴 OR 라이브러리 {YYYY-MM}` |
| 산업·비즈니스 | `AI funding round this week`, `AI startup raises {YYYY-MM}`, `AI acquisition this week`, `AI regulation OR policy {YYYY-MM} site:techcrunch.com OR site:theinformation.com` |
| 잡담·에세이 | `AI essay this week`, `most discussed AI opinion hacker news this week`, `AI substack {YYYY-MM}`, `긱뉴스 AI 토론 이번 주`, `site:news.hada.io 오피니언 OR 회고` |

각 소스당 2~3 쿼리. 제목·URL·**발행일**·**눈에 띈 buzz 수치(upvote·points·star 등)**·**해당 테마**를 함께 수집. 발행일이 없거나 8일 이상 지난 것은 즉시 버린다.

**유튜브 후보 특별 처리**: 유튜브 영상이 후보로 올라가면 해당 URL을 따로 모아둔다 (5단계에서 트랜스크립트를 Clippings/에 저장).

### 3단계 — 블로그 적합성 필터

수집한 후보 중 발행일 ≤ 7일인 것만 남기고, 아래 기준으로 거른 뒤 **5개 테마에 걸쳐 5~8개**를 선정한다. 테마 안에서는 주목도 순, 테마 사이에서는 골고루 (없으면 미만이라도 OK).

**통과 기준 (모두 충족해야 함):**
- **발행일이 오늘 기준 7일 이내** (강제 게이트)
- **주목도(buzz) 시그널이 붙어 있는가?** — HF upvote·X 화제·HN 포인트·star 급증 중 하나 이상 (위 「주목도 시그널」 표 참조). **이게 정렬 1순위.**
- 설명할 수 있는 **메커니즘**이 있는가? (단순 발표 뉴스 X)
- 기술적 깊이로 **딥다이브** 할 수 있는가? (논문 리뷰 or 기술 분석 가능)
- startedourmission 독자(기술에 관심 있는 일반인 ~ 비전공 개발자)가 "이거 알고 싶다"고 느낄 만한가?

**선정 (테마 다양성 + buzz):** 통과 후보를 먼저 **테마별로 묶고**, 각 테마에서 buzz 강도 순 상위를 1~2개씩 뽑아 5개 테마를 최대한 덮는다. 논문은 buzz가 아무리 높아도 최대 2~3개까지만, 나머지 자리는 모델릴리스·툴·산업·잡담에 양보한다. 7일 이내 + 주목할 후보가 없는 테마는 비워둔다. 최종 목록은 테마가 다양하게 섞이도록 배열한다.

**제외 기준:**
- **발행일 8일 이상 지난 것** (evergreen 가치가 있어도 제외 — 신선도 게이트)
- **buzz 시그널이 전혀 없는 것** — 자리가 부족해 메커니즘 특출난 것으로 보충하는 예외만 허용하고, 이때 `근거`에 `(buzz 미확인, 메커니즘 강함)` 명기
- 기술 내용 없는 단순 기업 PR·발표문
- 이미 한국어 블로그에서 수없이 다뤄진 기초 개념 (Transformer 101, GPT 개요 등)
- 검증되지 않은 주장만 있고 실험 결과나 수치가 없는 것
- **투자·펀딩 뉴스 — 조달 사실 자체로는 통과 불가.** 다음 중 하나를 글로 설명할 수 있어야 선정: (1) 기술·시장 구조에 실질적 변화를 일으키는 전략적 이유, (2) 지정학·규제 맥락이 배경에 있는 경우, (3) 새로운 카테고리나 시장 판도를 만드는 신호. "$XM 조달, 기업가치 $XB, 투자자 A·B" 수준의 보도자료 반복 구조는 제외.

### 4단계 — 후보별 분석

각 후보에 대해 다음을 결정:

**글 종류 판단:**
- `논문`: arXiv 논문이 중심인 경우 → **반드시 arXiv ID(예: 2606.13707)를 확인하고 상세 섹션 `arXiv:` 줄에 명기해야 한다.** arXiv ID를 확인하지 못하면 `정보`로 내리지 말고 **후보에서 완전히 제외**한다. daily-paper-pipeline이 arXiv ID 없이 처리할 수 없고, 논문을 `정보`로 위장해 다양성 슬롯을 채우는 건 허용하지 않는다.
- `정보`: 기술 트렌드·툴·이슈 소개가 중심인 **진짜 비논문 콘텐츠**에만 사용. 모델 릴리스·오픈소스 툴·산업 뉴스·오피니언이 여기에 해당한다. arXiv 논문인데 ID를 못 찾은 것은 절대 `정보`로 분류하지 않는다.

**테마 + 추천 요일 슬롯:** 이 후보가 5개 테마 중 무엇인지(논문/모델릴리스/툴오픈소스/산업비즈니스/잡담에세이)와 어울리는 요일(월~금)을 함께 적는다.

**추천 태그** (분류 1개 + 주제 태그 1~3개):
- 분류: `논문` / `정보`
- 주제: `LLM`, `멀티모달`, `컴퓨터비전`, `영상처리`, `음성`, `NLP`, `강화학습`, `추론`, `에이전트`, `확산모델`, `트랜스포머`, `머신러닝`, `딥러닝`, `데이터분석`, `파이썬`, `오픈소스`, `도구`, `GPU`, `TPU`, `반도체`, `벤치마크`, `AI평가`, `SaaS`
- 표기 규칙: 영문 이니셜리즘은 대문자(LLM, NLP, GPU, TPU), 그 외는 한국어(머신러닝, 강화학습, 에이전트 등). 목록 밖 신조어 금지.

**한줄 설명**: description 필드에 바로 쓸 수 있는 수준으로 작성.

**발굴 근거**: 왜 지금 이 주제인지 한 줄. **발행일 + buzz 수치를 반드시 함께** (예: `arXiv 2026-06-02, HF 142 upvotes`, `GitHub +1.2k★/3d`).

### 4.5단계 — 유튜브 후보 트랜스크립트 → raw/Clippings 저장

후보에 유튜브 영상이 있으면, **각 영상마다** defuddle로 트랜스크립트를 따와서 `raw/Clippings/`에 저장한다. 영상 본 적 없는 사람도 주제를 파악할 수 있게 + `blog-check` 가 클리핑 → 포스트 제안으로 우려먹게 하기 위해서.

```bash
# 영상 1개당 1회. URL은 watch?v=... 형식 그대로.
defuddle parse "<youtube-url>" --md -o "raw/Clippings/<slug>.md"
```

**slug 생성 규칙**: 영상 제목을 한글·영문·숫자·하이픈만 남기고 공백→하이픈으로 변환. 길이 60자 이내. 같은 slug 존재하면 끝에 ` 2`, ` 3` 추가.

**저장 직후 frontmatter 보강**: defuddle은 단순 markdown만 뽑으므로, 파일 맨 위에 직접 frontmatter를 prepend한다 (Read → 본문 앞에 다음 블록 삽입 → Write):

```yaml
---
tags:
  - 클리핑
  - 유튜브
source: <원본 youtube URL>
date: <오늘 날짜 YYYY-MM-DD>
description: <영상 한 줄 요약 — 후보 분석에서 만든 한줄 설명 재사용>
---
```

**실패 시**: defuddle이 트랜스크립트 없는 영상(자막 없음/숏폼)이라 빈 출력을 내면 그 후보 건너뜀. 표·상세에는 그대로 두되 `근거` 칼럼에 `(트랜스크립트 없음)` 표기.

defuddle 미설치(`command not found`)면 이 단계를 통째로 건너뛰고 표에만 영상 후보를 남긴다 — 사용자가 수동으로 보면 됨.

### 5단계 — stdout 출력

결과는 **stdout으로만** 출력합니다. 별도 파일에 저장하지 않습니다. cron-runner.sh 가 stdout 전체를 `blog-topic-finder-cron.md` 에 timestamp 헤딩과 함께 누적 캡처합니다. 의존 스킬(`daily-paper-pipeline`)이 그 로그의 최신 섹션을 읽습니다.

**출력 형식:**

```markdown
| # | 테마(요일) | 제목 | 종류 | 태그 | 한줄 설명 | 근거 |
|---|-----------|------|------|------|-----------|------|
| 1 | 논문(월) | ... | 논문 | LLM, 벤치마크 | ... | arXiv 2026-05-09, HF 142 upvotes |
| 2 | 툴·오픈소스(수) | ... | 정보 | 오픈소스, 파이썬 | ... | GitHub 2026-05-08, +1.2k★/3d |

### 상세

#### 1. {제목}
- arXiv: {URL} *(논문일 경우)*
- 기관: ...
- 주목도: {buzz 시그널·수치 + 발행일} (예: HF 142 upvotes · HN 230 pts · 2026-06-02)
- 핵심: ...
- 글로 풀 포인트: ...
- 참고 출처: *(정보 후보 필수, 3개 이상)*
  - [출처1 제목](URL) — 어떤 관점인지 (예: 공식 발표)
  - [출처2 제목](URL) — (예: 3자 분석)
  - [출처3 제목](URL) — (예: HN 실사용 반응)

#### 2. {제목}
- ...

### Sources
- [출처1](URL)
- [출처2](URL)
```

**필수 사항:**
- **표 + 상세 둘 다 필수.** `daily-paper-pipeline` 이 상세 섹션의 "글로 풀 포인트"를 입력으로 씀.
- **정보 후보에는 `참고 출처` 3개 이상 필수.** `daily-paper-pipeline`이 이걸 자격 심사에 쓴다 — 3개 미만이면 그 후보는 드래프트로 가지 못하고 탈락한다. 같은 보도자료를 받아쓴 기사 여러 개는 1개로 세므로, **관점이 다른 출처**를 찾아 붙일 것(공식 발표 / 3자 분석 / 실사용 반응). 3개를 못 채우겠으면 그 후보는 아예 목록에서 빼는 게 낫다.
- 논문 후보에는 arXiv ID 또는 URL 표기 (예: `arxiv.org/abs/2504.xxxxx`).
- **발행일 + buzz 수치가 표 `근거` 칼럼에 반드시 함께** (예: `arXiv 2026-05-08, HF 142 upvotes`, `HN 230 pts`). buzz가 정렬 근거이므로 빠지면 안 됨.
- **표 `테마(요일)` 칼럼 필수**. 각 후보가 5개 테마(논문/모델릴리스/툴오픈소스/산업비즈니스/잡담에세이) 중 무엇이고 어울리는 요일이 언제인지. `blog-weekly-report`의 요일 캘린더와 맞춘다.
- **표는 테마가 다양하게 섞이도록 배열.** 같은 테마(특히 논문)를 위에 몰아넣지 말 것. 논문 최대 2~3개.
- 5~8개 선호하지만 신선도(≤7일) + buzz 충족하는 후보가 그보다 적으면 적은 채로 보고. 채우려고 오래된 거·무-buzz 끌어오지 말 것.

### 6단계 — 대화 출력 (인터랙티브 모드만)

사용자가 직접 호출한 경우(헤드리스가 아니면) 같은 표를 대화에도 보여주고, 마지막에 한 줄: "원하시는 번호 말씀해 주시면 `blog-draft`로 바로 초안 생성해 드립니다."

헤드리스 자동 실행이면 stdout 출력으로 끝.

## 자동 실행 원칙

- 사용자에게 확인·재질문하지 않는다. 한 흐름으로 끝낸다.
- 외부 MCP 없이 동작해야 한다. WebSearch 만으로 충분.
- **파일 쓰기 없음.** 결과는 오로지 stdout. (예외: 4.5단계의 유튜브 트랜스크립트 `raw/Clippings/` 저장 — 이건 의도적 부산물로, 다음 날 `blog-check`가 점검 대상으로 우려먹음.)

---

## 하면 안 되는 것

- **기존 게시글과 중복된 논문을 후보에 올리기** — 1단계에서 구축한 arXiv ID 블랙리스트를 반드시 확인. grid_Papers나 raw/drafts에 이미 있는 논문은 HF upvote가 높아도 무조건 제외.
- **후보 목록을 논문으로만 채우기**. 테마 다양성이 buzz와 동급 기준이다. 논문은 최대 2~3개까지만, 나머지는 모델릴리스·툴오픈소스·산업비즈니스·잡담에세이로 채운다. buzz 상위가 다 논문이어도 그렇다. (이 블로그가 논문 일색이 된 게 바로 이걸 안 지켜서임)
- **발행일 8일 이상 지난 주제 넣기** — 신선도가 분량보다 우선
- **buzz 시그널 없는 논문을 상위에 올리기** — 주목도가 정렬 1순위. 무-buzz는 자리 부족 시 보충용으로만, `근거`에 명기
- 발행일·buzz 수치가 표 `근거` 칼럼에 없거나 모호하게 표기 ("최근", "this week"·"화제"만 쓰지 말고 `2026-05-08`, `HF 142 upvotes` 형식 명시)
- 기술 내용 없는 뉴스성 주제 넣기
- 논문 후보에 arXiv 확인 없이 ID 표기하기
- **arXiv ID 미확인 논문을 `정보`로 위장해 후보에 넣기** — arXiv ID를 확인하지 못한 논문은 후보에서 완전히 제외한다. `정보`로 재분류해서 다양성 슬롯을 채우는 것은 금지. `정보` 슬롯은 진짜 비논문 콘텐츠로만 채워야 한다.
- 출처 없는 수치 활용
- 중간에 사용자에게 분야·범위 재확인 요청하기 — 탐색·선정을 한 흐름으로 완료
- 신선한 후보 부족하다고 오래된 거 끌어와서 5개 채우기 — 그냥 적게 보고
- 유튜브 후보 트랜스크립트 없이 표에만 올려서 끝내기 — defuddle 있고 자막 있으면 반드시 `raw/Clippings/`에 저장
- `raw/Clippings/`에 저장한 파일에 frontmatter 빠뜨리기 — `blog-check`가 frontmatter 기준으로 클리핑을 인식함
