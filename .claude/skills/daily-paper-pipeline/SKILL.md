---
name: daily-paper-pipeline
description: Process today's candidates from `blog-topic-finder-cron.md` end-to-end into drafts. 논문(arXiv)은 Zotero 저장 후 페이퍼리뷰 드래프트, 정보는 blog-draft 풀 본문으로 생성. 대화형(동의 게이트)과 헤드리스 자동 모드(새벽 크론, 동의 스킵) 둘 다 지원. Use whenever the user wants the day's candidates turned into drafts in one shot. Triggers — "오늘 주제후보 다 처리해줘", "주제후보 드래프트로 우려먹어", "오늘 파이프라인 돌려", "어제꺼 다 드래프트", "주제후보 → 드래프트".
---

# Daily Paper Pipeline

> `raw/drafts/`는 없어졌습니다 (2026-08-31). 초안은 **목적지 폴더에 직접** `ready: false` 로 만듭니다 — 목적지는 `python3 tools/ready_queue.py --dest <태그…>` 가 알려줍니다.

`blog-topic-finder-cron.md`의 최신 날짜 섹션을 읽어서 거기 들어 있는 후보들을 **드래프트까지** 한 번에 처리합니다. 후보 종류에 따라 두 갈래로 라우팅:

- **논문**(arXiv ID 있음): Zotero에 저장 → fulltext 읽기 → `blog-paper-review` 호출로 페이퍼리뷰 드래프트 생성.
- **정보**(arXiv 없음): `blog-draft` 호출로 목적지 폴더에 본문 전체 작성.

## 실행 모드

두 가지 모드로 동작합니다. 호출 맥락으로 판별:

- **대화형 모드 (기본).** 사용자가 직접 호출. 2단계 동의 게이트(AskUserQuestion)로 처리 목록을 확인받고 진행.
- **헤드리스 자동 모드.** 호출 프롬프트에 "헤드리스 자동 모드" 또는 arg `auto`가 있으면(새벽 launchd 크론이 그렇게 부름) **2단계 동의 게이트를 건너뛰고** 처리한다. 단 **하루 상한(논문 1편 + 정보 1편)은 헤드리스에서도 그대로 적용** — 게이트를 건너뛰는 것이지 상한을 푸는 게 아니다. AskUserQuestion을 절대 호출하지 않는다(헤드리스에선 멈춰버림). 결과는 stdout 리포트로만 끝낸다.

### 헤드리스 가드 (자동 모드에서만, 중복·오작동 방지)

1. **오늘 날짜만.** 최신 `## ` 섹션 헤딩의 날짜가 오늘(`date +%Y-%m-%d`)이 아니면 처리하지 않고 "최신 섹션이 오늘 것이 아니라 종료"라고 보고 후 종료. topic-finder가 그날 안 돌았는데 어제 후보를 재드래프트하는 사고를 막는다.
2. **중복 skip.** 후보 제목에서 핵심 키워드(첫 의미 단어 1~2개, 예: "MiniMax", "Visa ChatGPT")를 추출하고, 목적지 폴더와 `markdown-blog/` 전체를 `grep -r -l` 로 키워드 검색한다. 정확한 파일명 일치가 아닌 **키워드 포함 여부**로 중복 판단 — 제목이 달라도 같은 주제면 skip. slug 정확 매칭만 쓰면 제목이 조금 다를 때 중복을 놓치므로 이 방법을 반드시 쓸 것.
3. 에러 섹션(`API Error` 한 줄)이면 기존 로직대로 그 섹션 건너뛰고 다음 정상 섹션 사용.

## 입력

- `blog-topic-finder-cron.md` — 볼트 루트. `blog-topic-finder`가 매일 새벽 cron으로 채우는 누적 로그
- 헤딩 형식: `## YYYY-MM-DD HH:MM:SS KST` (cron-runner가 stdout을 코드블록 ` ``` ` 안에 캡처)
- 최신 헤딩 다음의 코드블록 안 내용에서 종류=**논문**이고 근거에 arXiv ID가 있는 항목만 대상

사용자가 명시적으로 "어제꺼"라고 하면 두번째로 최신인 섹션 사용. 특정 날짜 (`2026-05-12`) 지정하면 해당 날짜로 시작하는 헤딩의 섹션 사용.

**에러 섹션 처리:** 코드블록 안이 `API Error: ...` 같은 한 줄짜리 에러만 있으면 그날은 스킬이 실행 실패한 것. 그 섹션은 건너뛰고 다음으로 최신인 정상 섹션을 사용. 사용자에게 "최신 cron 실행이 실패해 그 이전 섹션을 씁니다"라고 알린다.

## 사전 조건

- 이 워크스페이스의 `.env`에 `ZOTERO_USERID`, `ZOTERO_PRIVATE_KEY` 존재 (이미 설정됨)
- `arxiv-to-zotero/add.py` 사용 가능 (메타데이터 저장 전용, PDF 첨부 없음)
- `curl` 사용 가능 (3-B arXiv PDF 직접 다운로드용)

## 워크플로우

### 1단계 — 대상 섹션 파싱

`blog-topic-finder-cron.md`를 Read한 뒤 가장 최신 `## YYYY-MM-DD HH:MM:SS KST` 헤딩부터 다음 `## ` 또는 `---` 또는 EOF까지를 자릅니다. 그 안의 코드블록(` ``` ... ``` `) 내부 텍스트만 추출 (cron-runner가 stdout을 코드블록으로 감싸기 때문).

코드블록 내부에서 상세 섹션(`#### N. 제목`)별로 다음을 뽑습니다:
- 제목
- 종류 (표에서 가져옴)
- arXiv ID — 본문의 `https://arxiv.org/abs/<ID>` 패턴 또는 `arXiv 2605.12500` 같은 표기

**라우팅 기준** (선정된 후보만, 두 갈래로):
- 종류 = `논문` **그리고** arXiv ID 추출 성공 → **논문 브랜치**(3-A → 3-B → 3-C).
- 종류 = `논문`인데 arXiv ID 미추출 → **arXiv 검색 시도**: WebSearch로 `"<논문제목>" arxiv` 검색해 arXiv ID를 직접 찾는다. 찾으면 논문 브랜치로. 못 찾으면 정보 브랜치(3-D)로 fallback하되 분류 태그를 `논문`으로 blog-draft에 전달하고, 결과 리포트에 "논문(arXiv 미확인, 정보 브랜치로 fallback)"로 표시.
- 종류 = `정보` → **정보 브랜치**(3-D, blog-draft).

결과 리포트에 어느 브랜치로 갔는지 반드시 표시.

### 2단계 — 처리 목록 확정

#### 하루 상한 — 논문 1편 + 정보 1편 (절대 규칙)

**후보가 몇 개 올라왔든 하루에 만드는 드래프트는 논문 1편, 정보 1편, 총 2편입니다.** 대화형·헤드리스 모두 동일하게 적용합니다. 이 상한을 넘기지 않습니다.

양을 줄인 이유는 편당 밀도를 올리기 위해서입니다. 상한을 채우려고 약한 후보를 억지로 끌어오지 않습니다. **논문 갈래에 쓸 만한 후보가 없으면 0편으로 두고, 정보 갈래만 처리합니다.** 반대도 같습니다. "오늘은 논문만 1편" 또는 "오늘은 없음"이 정상적인 결과입니다.

#### 선정 기준

각 갈래에서 1편을 고릅니다.

**논문 갈래** — 다음 순서로 비교해 1편:
1. buzz 수치 (HF upvotes · HN points) 가 가장 높은 것
2. 동률이면 발행일이 최신인 것
3. 그래도 동률이면 우리 블로그의 기존 논문 리뷰와 주제가 덜 겹치는 것

**정보 갈래** — **레퍼런스를 3개 이상 확보할 수 있는 후보만 자격이 있습니다.** topic-finder 상세 섹션의 `참고 출처`가 3개 미만이면 그 후보는 탈락입니다. 자격을 갖춘 후보 중에서:
1. 서로 다른 관점의 출처가 많은 것 (같은 보도자료를 받아쓴 기사 여러 개는 1개로 셈)
2. buzz 수치가 높은 것
3. 발행일이 최신인 것

**출처 3개를 못 채우는 후보는 처리하지 않습니다.** 한 곳의 발표나 기사 한 편을 옮겨 쓰는 글은 만들지 않습니다. 자격 미달로 정보 갈래가 비면 그날은 논문만 나갑니다. 이 경우 리포트에 "정보 갈래: 출처 3개 이상 후보 없음 — 생성 안 함"이라고 적습니다.

#### 모드별 동작

**대화형 모드:** 선정된 2편(갈래 표시)과 **탈락 사유**를 함께 보여주고 동의 받습니다 (AskUserQuestion 사용):

```
오늘(2026-05-14) 선정 2편:
1. SenseNova-U1 (논문) — 2605.12500 · HF 142 upvotes
2. Gemini Flash GA 분석 (정보) — 출처 4개 확보

미선정:
- Predictive Maps of Multi-Agent Reasoning (논문) — buzz 낮음
- Cursor 2.0 출시 (정보) — 출처 1개, 자격 미달

[진행] [교체] [중단]
```

사용자가 "교체"면 어느 갈래를 무엇으로 바꿀지 받습니다. 진행 동의 못 받으면 종료.

**헤드리스 자동 모드:** 동의 게이트를 건너뛴다. 헤드리스 가드(오늘 날짜 / 중복 skip)를 통과한 후보 중 **위 선정 기준으로 갈래별 1편씩만** 3단계로 보낸다. AskUserQuestion 호출 금지. 미선정 후보와 사유는 stdout 리포트에 남긴다.

### 3단계 — 항목별 처리 (순차)

각 논문마다 아래 3-A → 3-B → 3-C 순서. 어느 단계든 실패하면 그 논문은 **건너뛰고 다음 항목으로**. 전체 파이프라인은 절대 중단되지 않습니다.

#### 3-A. Zotero 저장 (메타데이터만)

```bash
set -a; source "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/.env"; set +a
python3 "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/.claude/skills/arxiv-to-zotero/add.py" --no-pdf "<ARXIV_ID>"
```

PDF는 첨부하지 않는다 (Zotero 스토리지 절약). stdout에서 `→ Zotero <KEY>` 줄을 파싱해 `item_key` 확보. 실패하면 이 논문을 "Zotero 저장 실패"로 마킹하고 다음으로.

**팁**: `add.py` 출력의 마지막 줄이 `zotero://select/library/items/<KEY>` 형태라 정규식으로 KEY 추출.

#### 3-B. PDF 직접 다운로드

Zotero에 PDF가 없으므로 arXiv에서 직접 받는다:

```bash
curl -L -o "/tmp/arxiv_<ARXIV_ID>.pdf" "https://arxiv.org/pdf/<ARXIV_ID>"
```

다운로드 성공 시 `/tmp/arxiv_<ARXIV_ID>.pdf` 경로를 3-C에 전달. 실패하면 "PDF 다운로드 실패"로 마킹하고 메타데이터만으로 blog-paper-review 진행 (스킬이 자체적으로 PDF를 찾으려 시도).

#### 3-C. blog-paper-review 호출

`blog-paper-review` 스킬을 Skill 툴로 호출. args에 다음 정보를 넘김:

- 논문 제목
- Zotero item key (스킬이 fulltext 가져갈 때 사용)
- topic-finder 섹션의 "글로 풀 포인트" 항목 — 사용자가 미리 정리한 앵글

이 스킬이 알아서 목적지 폴더에 마크다운 파일을 만듭니다. 생성된 파일 경로를 받아서 결과 리포트에 기록.

#### 3-D. blog-draft 호출 (정보 브랜치)

arXiv가 없는 정보 후보는 `blog-draft` 스킬을 Skill 툴로 호출해 목적지 폴더에 완성도 있는 본문을 만든다. 넘기는 정보:

- 제목
- topic-finder 섹션의 추천 태그(분류 1개 + 주제 1~3개)
- 한줄 설명 → description
- "글로 풀 포인트" → 배경 조사와 본문 작성에 활용
- **`참고 출처` 목록 전체 (3개 이상)** — blog-draft가 교차 종합에 쓴다. 이걸 빼고 호출하면 blog-draft가 단일 출처 요약을 쓰게 되므로 반드시 전달한다.

호출 프롬프트에 **"레퍼런스 3개 이상 교차 종합. 우라까이 금지."** 를 명시한다. blog-draft가 출처를 3개 미만으로 확보하면 드래프트를 만들지 않고 사유를 반환하므로, 그 경우 리포트에 "정보 갈래: 출처 부족으로 생성 실패"로 기록하고 넘어간다.

`blog-draft`는 프론트매터 + 본문 전체를 완성해야 한다. 섹션 헤딩만 뽑는 스켈레톤으로 끝내지 않는다. 생성된 파일 경로를 결과 리포트에 기록. Headliner 태그는 절대 넣지 않는다.

### 4단계 — 결과 리포트

처리 끝나면 한 번에 요약 출력:

```
✅ daily-paper-pipeline 결과 (2026-05-14)

논문 (2/3):
- SenseNova-U1 → markdown-blog/<목적지>/SenseNova-U1.md (Zotero ABC123)
- OmniNFT → markdown-blog/<목적지>/OmniNFT.md (Zotero DEF456)

정보 (1/1):
- Gemini Flash GA 분석 → markdown-blog/<목적지>/gemini-flash-ga.md (blog-draft 스켈레톤)

수동 필요 (1/3):
- Predictive Maps of Multi-Agent Reasoning, fulltext 미인덱싱
  (Zotero에는 저장됨: GHI789. 잠시 후 다시 시도하거나 직접 blog-paper-review 호출)

skip:
- (해당 시) 이미 존재하는 초안/게시글

다음 단계: markdown-blog/<목적지>/ 에서 검토 후 /blog-publish
```

### 5단계 — 마무리 안내

- 드래프트가 1편 이상 생성됐으면 사용자에게 "목적지 폴더에서 검토하고 게시 준비되면 알려달라"고 안내.
- `blog-topic-finder-cron.md`는 **건드리지 않습니다** — 그건 cron 로그라 추후 이력으로 남고, 다음 cron 실행이 알아서 새 섹션을 prepend함.

## 하지 말 것

- 정보 후보도 `blog-draft`를 통해 본문 전체를 완성한다. 섹션 헤딩만 뽑는 스켈레톤으로 끝내지 않는다.
- **대화형 모드**에서 사용자 동의 없이 목적지 폴더에 파일을 만들지 말 것(2단계 동의 후에만). **헤드리스 자동 모드**에서는 동의 없이 진행하되, 헤드리스 가드(오늘 날짜·중복 skip)를 반드시 적용.
- 헤드리스 모드에서 AskUserQuestion을 호출하지 말 것(멈춰버림).
- 하나 실패했다고 전체 중단하지 말 것. 항상 다음 후보로.
- 처리 중 Headliner 태그를 임의로 부여하지 말 것 (CLAUDE.md 규칙).
- Zotero에 같은 archiveID가 이미 있는지 사전 검사하지 말 것. `arxiv-to-zotero` 스킬이 이미 정책 정해둠(그쪽 결정 따름).

## 디버깅

- arxiv-to-zotero/add.py가 401/403을 주면 → `.env`의 ZOTERO_PRIVATE_KEY 권한 확인
- arXiv PDF 다운로드 실패(curl 오류) → arXiv가 일시적으로 막은 것. 잠시 후 재시도하거나 직접 blog-paper-review 호출
- topic-finder 섹션 파싱이 빗나가면 → blog-topic-finder의 stdout 포맷이 바뀐 것. 그쪽 SKILL.md의 "5단계 — stdout 출력" 부분을 먼저 확인.

## 관련 스킬

- `blog-topic-finder` — 이 파이프라인의 **입력**을 만드는 스킬. 매일 새벽 cron.
- `arxiv-to-zotero` — 3-A 단계에서 사용하는 저장 도구. Zotero MCP에 쓰기 도구가 추가되면 이 스킬도 그쪽으로 갈아탈 수 있음.
- `blog-paper-review` — 3-C 단계(논문 브랜치)에서 호출. 실제 본문 작성을 담당.
- `blog-draft` — 3-D 단계(정보 브랜치)에서 호출. 프론트매터 + 스켈레톤 생성.
- `blog-publish` — 사용자가 드래프트 검토 후 게시할 때 따로 호출.
