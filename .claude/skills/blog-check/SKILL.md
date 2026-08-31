---
name: blog-check
description: 블로그 일일 점검 스킬. launchd cron이 매일 새벽 자동 실행하며, 사용자가 "블로그 점검", "점검 돌려", "check", "/blog-check" 라고 말할 때도 트리거. 여섯 가지를 순서대로 실행 — (1) Clippings → 포스트 제안, (2) 끊어진 위키 링크 탐지, (3) 링크 추천(Dictionary 항목이 본문에 평문으로 등장하는 경우), (4) 방치된 초안 목록, (5) 중복 노트 후보(같은 대상이 영문/한글 등으로 갈라진 경우), (6) 인물 노트 type/태그 불일치(type:person ↔ 인물 태그). 점검 리포트는 stdout으로만 출력 — cron-runner가 blog-check-cron.md에 timestamp와 함께 누적 캡처한다(별도 리포트 파일 없음). 더해서 Step 1 스크립트가 매일 블로그 Trends 페이지용 HN 트렌드 데이터(assets/trends-data.json)를 재생성한다 — 로컬 갱신만, 자동 푸시 없음.
---

# Blog Check

> `raw/drafts/`는 없어졌습니다 (2026-08-31). 초안은 **목적지 폴더에 직접** `ready: false` 로 만듭니다 — 목적지는 `python3 tools/ready_queue.py --dest <태그…>` 가 알려줍니다.

블로그 유지관리 점검입니다. **헤드리스 자동 실행을 전제로 설계됨** — 사용자 입력 없이 한 흐름으로 끝나야 합니다. 스크립트(`blog-check.sh`)로 먼저 파일 기반 점검을 실행하고, 그 결과를 바탕으로 Clippings 분석까지 수행합니다.

**산출물은 stdout 출력 하나뿐.** 별도 파일에 저장하지 않습니다. cron-runner.sh가 stdout 전체를 `blog-check-cron.md` 에 timestamp 헤딩과 함께 누적 캡처합니다.

## 경로 상수

```
VAULT=$HOME/Vaults/AutoVault
CLIPPINGS=$VAULT/raw/Clippings
POSTS=$VAULT/markdown-blog
POSTS=$VAULT/markdown-blog/grid_Posts
PAPERS=$VAULT/markdown-blog/grid_Papers
BLOG=$VAULT/markdown-blog
```

## 실행 순서

### Step 1 — 스크립트 실행 (끊긴 링크 + 방치 초안 + buzz 업데이트 + 트렌드 데이터 갱신)

```bash
bash "$VAULT/.claude/skills/blog-check/blog-check.sh"
```

스크립트 출력을 읽어 끊어진 위키 링크와 방치된 초안 목록을 확보합니다.

스크립트 마지막 단계에서 블로그 Trends 페이지용 `assets/trends-data.json`을 재생성합니다(Hacker News 언급량을 Algolia API로 연도별 집계, `scripts/gen-trends-data.js`). **로컬 갱신만** — 자동 커밋/푸시는 하지 않으며, 다음 블로그 push 때 라이브에 함께 반영됩니다. 네트워크 실패 등으로 데이터가 비면 기존 파일을 덮어쓰지 않고 점검은 계속 진행됩니다(생성기에 안전장치 내장).

### Step 2 — Clippings 점검

`$CLIPPINGS/` (= `$VAULT/raw/Clippings/`) 안의 .md 파일을 모두 봅니다. `Archive/` 하위 폴더는 제외. 각 파일의 `title`과 본문을 보고 다음을 판정:

- `$POSTS` 또는 `$PAPERS`에 비슷한 글이 이미 있으면 → ✅ 게시 완료
- `$DRAFTS`에 비슷한 초안이 있으면 → 🔧 진행 중 (작성일 N일 표기)
- 어느 쪽에도 없으면 → ⏳ 미처리 (초안화 액션 후보)

### Step 3 — stdout 출력 (표 기반)

아래 형식으로 출력합니다. cron-runner가 그대로 캡처합니다.

```markdown
### 오늘 할 일

| # | 액션 | 대상 | 사유 |
|---|------|------|------|
| 1 | 📤 게시 | `<드래프트 파일명>` | drafts N일 경과 |
| 2 | 📝 초안화 | `<클리핑 제목>` | Clippings 미커버 |
| 3 | 🔗 링크 수정 | `[[<이름>]]` | `<어느 파일>`에서 깨짐 |
| 4 | 🔗 링크 추가 | `[[<이름>]]` | `<어느 파일>`에서 평문 등장 |
| 5 | 🔀 병합 검토 | `<파일A>` ↔ `<파일B>` | 같은 대상 중복 노트 |
| 6 | 🏷️ 태그 정합 | `<인물 노트>` | type:person ↔ 인물 태그 불일치 |

(할 일 없을 땐 한 줄로: **오늘 할 일 없음** ✅)

### 상세

**클리핑** (`raw/Clippings/`)
- ⏳ `<클리핑>` — 미커버, 추천: 초안화
- 🔧 `<클리핑>` → `markdown-blog/<목적지>/<파일>` (작성일 N일 경과)
- ✅ `<클리핑>` → `블로그/.../<파일>` (게시 완료)

**방치된 초안** (목적지 폴더, 7일+)
- N일 — `<파일>` (작성일 YYYY-MM-DD)
- 없으면: 없음

**끊어진 위키 링크**
- 본문(Posts/Papers): `[[<이름>]]` ← `<어느 파일>` (전부 나열)
- Dictionary: 개수 + 참조 많은 상위 25개 (`[[<이름>]]` (N곳))
- 없으면: 없음

**링크 추천 (최근 30일)**
- `[[<이름>]]` ← `<파일>` (본문 평문 등장, 링크 없음)
- 없으면: 없음

**중복 노트 후보**
- `<파일A>` ↔ `<파일B>` (이름 충돌 / 제목 토큰 동일 / 본문 유사)
- 없으면: 없음

**인물 노트 type/태그 불일치**
- `<노트>` (type:person인데 인물 태그 없음 / 인물 태그인데 type 아님)
- 없으면: 없음
```

**우선순위 규칙 (할 일 표 정렬):**
- 1순위 📤 게시 — `blog-check.sh` 의 "방치된 초안 (7일 이상)" 항목, 경과일 내림차순
- 2순위 📝 초안화 — Step 2에서 ⏳ 표기된 클리핑
- 3순위 🔗 링크 수정 — `check_broken_links.py` 의 끊어진 링크. **본문(Posts/Papers) 우선** — 게시글에서 깨진 링크가 독자에게 404로 노출되므로. Dictionary 내부 깨진 링크는 양이 많아(수백 건) 참조 많은 상위 항목부터 항목 생성으로 점진 정리.
- 4순위 🔗 링크 추가 — `blog-check.sh` 의 "링크 추천" 항목 (Dictionary 항목명이 본문 평문으로 등장, 링크 없음)
- 5순위 🔀 병합 검토 — `blog-check.sh` 의 "중복 노트 후보" 항목 (`find_dupes.py` 출력). 자동 병합하지 않고 후보만 보고한다 — 어느 표기를 표준으로 둘지는 사람이 결정.
- 6순위 🏷️ 태그 정합 — `blog-check.sh` 의 "인물 노트 type/태그 불일치" 항목 (`check_person_tags.py` 출력). type:person인데 인물 태그가 없으면 옵시디언 인물 뷰에서 누락된다. 태그 추가는 명확하면 바로, 오분류(인물 태그인데 회사 등)는 사람 확인.

## 자동 실행 원칙

- 사용자에게 확인·재질문하지 않는다. 한 흐름으로 끝낸다.
- 외부 MCP(예: Zotero) 없이 동작해야 한다. 헤드리스에서 로드되지 않을 수 있다.
- **점검 리포트는 stdout 하나뿐.** 별도 리포트 파일을 만들지 않는다(cron-runner.sh 가 캡처). 단 Step 1 스크립트는 유지보수성 쓰기를 한다 — buzz 점수 갱신, 그리고 `assets/trends-data.json` 재생성. 둘 다 working tree에만 남기고 자동 푸시는 하지 않는다.
