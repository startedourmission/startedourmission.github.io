---
name: base-audit
description: Audit Obsidian Bases (.base files) — read views and report which notes in scope have empty/missing values for the columns shown by each view. Use when the user wants to know which notes are missing a property in a specific base view, says "베이스 비어있는 거 찾아줘", "이 뷰에서 description 빈 노트", "블로그베이스에서 image 없는 것들", "힌튼시리즈에서 비어있는 속성", "base 뷰 점검", or asks "어디가 비어있어".
---

# Base Audit

Obsidian `.base` 파일을 **읽기 전용**으로 점검하는 스킬. 뷰 정의(필터 + 표시 컬럼)를 파싱해서, 그 뷰가 보여주는 노트들 중 어떤 노트가 어떤 속성에서 비어있는지 표로 보고합니다.

**편집 안 함.** 이 스킬은 base 파일을 수정하지 않습니다. base 자체를 새로 만들거나 뷰를 수정하려면 `obsidian-bases` 스킬을 쓰세요.

## 워크플로우

### 1단계 — 대상 base 파일 확인

사용자가 base 파일 경로나 이름을 지정했으면 그걸 사용. 지정 안 했으면 볼트 루트와 한 단계 아래에서 `*.base` 파일 목록을 보여주고 어느 걸 점검할지 묻기.

```bash
find . -maxdepth 3 -name "*.base" -not -path "./.*"
```

### 2단계 — base 파일 파싱

`Read` 툴로 파일 전체를 읽는다. YAML이므로 다음 구조를 추출:

- `views[].name` — 뷰 이름
- `views[].filters` — `and`/`or`/`not` 트리. 주로 다음 표현식이 들어감:
  - `file.inFolder("경로")` — 해당 폴더 내 노트만
  - `!file.inFolder("경로")` — 해당 폴더 제외
  - `file.hasTag("태그")` / `file.tags.contains("태그")` — 태그 조건
  - `!file.tags.isEmpty()` — 태그 있는 것만
  - `note.property == "값"` 등 — 프로퍼티 조건
- `views[].order` — 그 뷰에 표시되는 컬럼 목록. `file.name`, `date`, `tags`, `description`, `image` 같은 식별자. `file.*` 는 시스템 필드, 그 외는 frontmatter property.
- `formulas` — 계산식 (이번 워크플로우에서는 점검 대상 아님)

각 뷰별로 `{이름, 스코프(폴더 목록), 표시 컬럼(file.* 제외한 frontmatter property)}` 로 정리.

### 3단계 — 스코프에 해당하는 노트 수집

뷰별로:

1. `filters` 안의 `file.inFolder("X")` 를 모은다 → 포함할 폴더
2. `!file.inFolder("X")` 를 모은다 → 제외할 폴더
3. `find` 로 노트 목록 만들기. 절대 경로보다는 볼트 루트 기준 상대 경로 유지.

```bash
# 예: file.inFolder("markdown-blog/grid_Posts") + !file.inFolder("markdown-blog/Geoffrey Hinton/_assets")
find "markdown-blog/grid_Posts" -name "*.md" -not -path "*/_assets/*"
```

`_assets/` 같은 이미지 폴더는 보통 제외 대상. 필터에 명시되지 않았어도 `*.md` 만 본다.

태그 필터(`file.hasTag`, `!file.tags.isEmpty()`)는 노트 frontmatter를 실제로 읽어서 추가 필터링. `grep -l "tags:" file.md` 만으로 부족하므로 frontmatter를 파싱해야 한다.

### 4단계 — 각 노트의 frontmatter 점검

수집한 노트 각각에 대해 `Read`로 첫 50줄 정도 읽어서 frontmatter 파싱. 뷰가 표시하는 컬럼 중 frontmatter property에 해당하는 것만 점검 (`file.name`, `file.tags` 같은 시스템 필드는 건너뜀 — 비어있을 수 없거나 다른 방식으로 채워짐).

**"비어있다"의 정의:**
- 해당 키가 frontmatter에 아예 없음
- 키는 있지만 값이 빈 문자열 `""`, `null`, 빈 배열 `[]`
- 값이 공백 문자만으로 채워져 있음

노트 수가 많으면 `Agent` (Explore) 서브에이전트로 병렬 점검 고려. 30개 이하면 그냥 직접 Read.

### 5단계 — 보고

뷰별로 표를 만든다.

```markdown
## 블로그베이스.base — 뷰: 포스트

스코프: `markdown-blog/grid_Posts` (필터: `!file.tags.isEmpty()`)
점검 컬럼: `date`, `tags`, `description`, `image`
대상 노트: 42개 / 비어있는 노트: 7개

| 노트 | date | tags | description | image |
|------|:----:|:----:|:-----------:|:-----:|
| 어떤글.md | ✅ | ✅ | ❌ | ❌ |
| 다른글.md | ✅ | ✅ | ✅ | ❌ |
| ... |

### 컬럼별 결손 요약
- `description` 비어있음: 3개
- `image` 비어있음: 6개
```

**보고 원칙:**
- 점검 결과는 대화에 직접 출력. 파일로 따로 저장하지 않는다 (사용자가 명시적으로 요청하면 `raw/베이스점검-YYYY-MM-DD.md`에 저장).
- 비어있는 게 하나도 없는 컬럼은 "전부 채워짐" 한 줄로 압축.
- 노트가 너무 많으면 (50개+) "비어있는 노트만" 보여주고 전체 통계는 카운트만.
- frontmatter property 이름이 한글이면 그대로 한글로 표시 (변환 X).

### 6단계 — 후속 제안 (선택)

비어있는 노트가 많으면 마지막에 한 줄:
"이 중 어떤 노트부터 채울까요? 파일명 말씀해 주시면 frontmatter 수정 도와드립니다."

## 알려진 함정

- **`order` ≠ 모든 frontmatter**. base 뷰의 `order`는 그 뷰가 *표시*하는 컬럼이지 노트가 가진 모든 property가 아니다. 점검 대상은 `order`로 한정.
- **`file.name`, `file.tags` 같은 시스템 필드는 점검 대상 아님** — frontmatter property가 아니라 Obsidian이 자동 계산함.
- **YAML 다중 줄/배열 처리**. `tags:` 가 다음 줄에 `- 논문` 형식이면 빈 게 아니다. 파싱할 때 주의.
- **이미지가 첨부 파일 링크인 경우**. `image: "[[블로그/.../_assets/foo.png]]"` 처럼 wikilink면 채워진 것. URL이어도 채워진 것.
- **필터 표현식 못 알아들으면 추측하지 말기.** 모르는 함수가 나오면 사용자에게 "이 필터는 해석 못 했으니 전체 노트로 점검합니다"라고 명시하고 진행.

## 하면 안 되는 것

- base 파일을 수정하기 — 이 스킬은 읽기 전용
- frontmatter를 임의로 채워 넣기 — 사용자가 확인하고 결정
- `_assets/`, `.obsidian/` 같은 비-노트 디렉토리를 점검 대상에 넣기
- 뷰가 표시하지 않는 property까지 점검 결과에 넣기 — 뷰별 점검은 그 뷰의 `order` 컬럼만
