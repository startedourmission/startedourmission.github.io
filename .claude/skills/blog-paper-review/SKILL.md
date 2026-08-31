---
name: blog-paper-review
description: Write a research-paper review post for the startedourmission blog, end-to-end. Use this skill whenever the user is reviewing/blogging about a research paper (arXiv preprint, conference paper, journal article) and wants a finished post, not just a stub. Triggers include "이 논문 다듬어줘", "논문 리뷰 써줘", "이 페이퍼 블로그로", "조테로 논문으로 글", and any phrase where the deliverable is a paper review post with depth (multiple sections, author background, results table, limitations). For just creating a draft skeleton with frontmatter, use blog-draft instead.
---

# Blog Paper Review

이 스킬은 startedourmission 블로그의 **논문 리뷰 글 한 편 전체**를 책임집니다. 프론트매터 채우기에서 끝나는 `blog-draft`와 다릅니다. 조테로 PDF 읽기 → 저자 조사 → Dictionary 항목 분리 → 논문 구조 기반 본문 작성 → startedourmission 톤으로 다듬기까지를 묶어둔 워크플로우입니다.

## 언제 이 스킬을 쓰는가

- 사용자가 *논문 리뷰 글 다듬어줘 / 보강해줘 / 새로 써줘*라고 할 때
- 조테로에 있는 논문을 블로그 글로 만들어달라고 할 때
- 이미 grid_Papers에 있는 글을 *전면 재작성*해달라고 할 때
- 사용자가 "ㅈ같애 / 별로다 / 다시 써"라고 글 품질을 부정할 때 (요청은 단순해도 결과물은 본격적인 리뷰여야 함)

`blog-draft`로 충분한 경우 (단순 프론트매터·짧은 초안 생성)는 거기로 갑니다. 이 스킬은 **전체 글을 책임지는 경우**에만 발동합니다.

---

## 워크플로우 (이 순서를 지킬 것)

### 1단계. 논문 전문 확보 — 3패스 독법 (S. Keshav 방식)

요약본·초록·뉴스 기사로 글을 쓰지 않습니다. **반드시 PDF 전문**을 봅니다.

**PDF 위치 확인 (패스 시작 전)**
1. 사용자가 조테로에 논문을 넣어뒀는지 먼저 확인합니다. `find "$HOME/Zotero" -type f -iname "*<키워드>*"` 또는 `mcp__zotero__zotero_search_items` 사용.
2. 못 찾으면 사용자에게 알립니다: "Zotero에 해당 논문이 없는 것 같습니다. 추가해주시면 전문으로 작성하겠습니다."
3. PDF 페이지 수를 먼저 확인합니다 (`mdls -name kMDItemNumberOfPages`). 10페이지 초과면 `pages` 파라미터로 나눠 읽습니다.

#### 1차 패스 — 조감도 (5~10분)

빠른 스캔으로 전체 그림을 잡습니다. 이 단계에서 더 읽을지 여부도 결정합니다.

- 제목·초록·도입 꼼꼼히 읽기
- 섹션과 서브섹션 제목만 훑기 (내용 건너뜀)
- 결론 읽기
- 참조 목록 훑으며 이미 아는 논문 체크

완료 후 **5C 자문** — 이 다섯 가지에 답할 수 있어야 다음 패스로 넘어갑니다:
- **Category**: 측정/분석/시스템/프로토타입 중 어디인가? (측정=실험 중심, 분석=기존 시스템 해부, 시스템=새 인프라 구축, 프로토타입=연구 개념 증명)
- **Context**: 어떤 선행 연구에 기대는가? 이론적 배경은?
- **Correctness**: 핵심 가정이 타당한가?
- **Contributions**: 주요 기여 1~3가지는?
- **Clarity**: 논문이 잘 쓰였는가? 가정 없이 따라갈 수 있는가?

산출물: §배경 초안 · 글 구조 결정

#### 2차 패스 — 정독 (증명 건너뜀)

본문을 꼼꼼히 읽되 수식 증명의 세부 전개는 건너뜁니다.

- **Figure·그래프 집중 점검**: 축 레이블, 오차 막대, 통계적 유의성. 급하게 쓴 논문과 엄밀한 논문을 가르는 기준.
- **핵심 숫자 기록**: abstract·본문·표에서 같은 지표를 비교해 불일치 탐지.
- **저자가 솔직히 쓴 한계**: Discussion·Limitation·Appendix의 인정 부분 표시.
- **더 읽을 참조 표시**: 배경 이해에 필요한 미독 논문 체크.

산출물: §어떻게 만들었나 · §결과 초안

#### 3차 패스 — 재구현 관점

"내가 이 연구를 처음부터 설계한다면"이라는 관점으로 전체를 다시 읽습니다. 각 주장의 암묵적 전제를 밝히는 것이 핵심입니다.

- 모든 주장마다: "이 결론이 성립하려면 어떤 전제가 필요한가?" 질문
- 암묵적 가정, 누락된 인용, 실험 기법의 잠재적 약점 찾기
- **Appendix까지 탐색** (회고·한계·실험 세부가 부록에 자주 있음)
- abstract ↔ 본문 숫자 불일치 최종 확인
- 미래 연구 아이디어 메모

산출물: §회고 (숨겨진 가정, 누락 인용, 실험 약점)

### 2단계. 저자 조사 (이게 빠지면 다시 함)

논문 리뷰 글은 *어떤 사람들이 왜 이 논문을 썼는가*가 거의 항상 중요합니다. 무조건 합니다.

1. 조직 팀(Organizing Team) / 1·시니어 저자 명단을 본문에서 추출합니다.
2. 핵심 인물 4~6명을 추리는 기준:
   - **1저자**는 무조건 포함
   - **시니어 저자**(보통 마지막) 무조건 포함
   - **분야별 대표 연구자**가 끼어 있으면 포함 (LLM-as-a-Judge면 Prometheus 저자, RAG면 Self-RAG 저자처럼)
   - 나머지는 본문 흐름상 언급할 가치가 있는 사람만
3. 각 인물에 대해 `WebSearch`로 병렬 검색 (소속·대표 연구·최근 활동). 6명이면 6개 검색을 한 메시지에 묶어 보냅니다.
4. **각 인물별로 Dictionary 항목을 만듭니다.** 인물 신상은 본문에 풀어쓰지 않고 사전으로 뺍니다.

#### Dictionary 항목 형식 (`markdown-blog/Dictionary/<한글 이름>.md`)

**파일명은 한글 이름으로 짓습니다** (2026-07 규칙 — 이전엔 영문 파일명이었으나 볼트 관례에 맞춰 한글로 통일). 표기 원칙:
- 중국계: 만다린 병음을 한글로 음차하고 **성을 먼저** 붙여씁니다 (예: 王立民 Wang Limin → `왕리민`, 张俊林 Zhang Junlin → `장쥔린`, 何恺明 He Kaiming → `허카이밍`). 단 `페이-페이 리`(Fei-Fei Li)처럼 서양권에 given-first로 굳어진 경우는 그 순서를 따릅니다.
- 서양·기타: 표준 한글 음차, 이름과 성 사이 띄어쓰기 (예: Chris Lattner → `크리스 래트너`).
- 한국계: 실제 한글 이름 (예: `이병관`).
- **새 인물 노트를 만들기 전에, 같은 사람이 다른 표기(영문·한자)로 이미 있는지 파일명과 aliases를 훑어 확인합니다.** 있으면 새로 만들지 말고 기존 노트를 재사용해 EN/KR 중복 노트를 막습니다.

```yaml
---
type: person
description: <한 줄로 정의되는 정체성. 소속·대표 연구·역할>
tags:
  - 인물
  - <LLM | 머신러닝 | 딥러닝 | AI평가 | 오픈소스 | ...>
  - <해당하는 점수 태그들 — 아래 목록 참고>
aliases:
  - <영문 이름>
  - <한자 이름 (있으면)>
last_active: <YYYY — 마지막으로 논문·발표·직책 활동한 연도>
papers:
  - <이 논문 파일명 (.md 제외) — 저자인 논문만>
---
```

**점수 태그 목록** (해당하는 것만 추가):
- `노벨상` — 노벨상 수상자
- `튜링상` — ACM 튜링상 수상자
- `필즈상` — 필즈상 수상자
- `분야창시자` — 해당 분야를 개척했다고 명시적으로 언급되는 인물
- `CEO` — 현재 또는 최근 회사 CEO·공동창업자
- `수석과학자` — Chief Scientist, VP of Research 등 연구 수장급
- `교수` — 현직 대학 교수 (은퇴 포함)
- `Nature논문` — Nature·Science 게재 논문 보유
- `NeurIPS논문` — NeurIPS·ICML·ICLR 등 주요 ML 학회 논문 보유
- `은퇴` — 은퇴·퇴직·비활동 상태

**star 점수는 직접 쓰지 않는다.** 노트 저장 후 아래 스크립트가 자동 계산해서 채운다:

```bash
python3 "$VAULT/tools/calc_star.py" "<person.md 절대경로>"
```

`$VAULT`는 `/Users/chajinwoo/Vaults/AutoVault`.

파일명은 한글 이름이고, aliases에 영문 이름과 (있으면) 한자를 넣어 검색·중복탐지가 되게 합니다. 본문 위키링크는 한글 파일명 기준으로 걸되, 영어 문맥에서 영문 표기를 보이려면 pipe를 씁니다 (`[[손귀진|Guijin Son]]`).

### 3단계. 본문 글의 골격

논문 리뷰 글은 다음 5~6 섹션을 따릅니다. 섹션 제목은 짧은 단어로.

```
## 저자          (누가 왜 모였나. 신상 말고 *합류 동기*. 인물 위키링크.)
## 배경          (왜 이 논문이 지금 나왔나. 분야 흐름과 빈자리.)
## 어떻게 만들었나 (데이터셋/방법론 논문이면 가장 두꺼운 섹션. 파이프라인·게이트·인센티브.)
## 무엇으로 구성돼 있나 (데이터셋이면 서브셋·통계. 모델 논문이면 아키텍처.)
## 결과          (표 + 핵심 발견 3~4개. 컴퓨트 스케일링, 인간 베이스라인 등.)
## 회고          (저자 본인의 한계·실패 인정 부분. 부록에 있어도 본문에 끌어올림.)
## 정리          (1~3 항목 압축.)
```

이 골격을 무조건 따르지는 않습니다. 논문 성격에 따라 §어떻게/§무엇으로를 합치거나 §회고를 §결과에 녹일 수 있습니다. 다만 **§저자와 §배경은 거의 항상 분리**합니다.

### 4단계. 톤 가이드 (startedourmission 블로그 전용)

`blog-draft`의 라이팅 스타일을 따르되, 논문 리뷰는 특히 다음을 지킵니다.

#### 어미

- 기본: **`~입니다 / ~합니다`** 존댓말 어미. 예외 없음.
- **`~다 / ~한다 / ~이다 / ~된다 / ~있다 / ~없다`** 같은 반말체는 **절대 쓰지 않습니다.** 기존 글이 반말로 작성되어 있어도 따라 쓰지 말고 해당 글 전체를 존댓말로 교정합니다.
- `~예요 / 이에요 / ~죠 / ~대요 / ~거예요` 같은 **구어체·전언 어미도 쓰지 않습니다.**
- 마지막 패스에서 반드시 `~다 / ~한다 / ~이다` grep해서 0건 확인.

#### 섹션 제목

- 짧은 단어 한두 개. `## 어떻게 만들었나` (O), `## 2. 어떻게 만들었나: 5단계 파이프라인과 3개의 게이트` (X).
- 섹션 번호 안 붙입니다. 사용자가 글을 옮겨다닐 때 번호 헷갈림.

#### 강조

- **굵게**는 무거운 핵심에만. 자기 강조(*진짜 가치는*, *여기가 핵심이에요*, *진짜 본진이에요*)는 제거.
- 너무 많이 굵게 하면 강조 의미가 사라집니다.

#### 문장

- 한 문단을 짧게 끊어 호흡 분명히. 2~4문장이 한 단위.
- "~한대요 / ~했대요"식 전언체 금지. 사실은 사실대로 단정합니다.

#### 위키링크

- Dictionary 항목이 있는 모든 인물·모델·벤치마크·기관을 첫 등장 시 `[[위키링크]]`로 연결합니다.
- 인물 위키링크는 한글 파일명 기준 (`[[손귀진]]`), 영어 문맥에서 영문 표기가 필요하면 pipe 사용 (`[[손귀진|Guijin Son]]`).

#### 결과 숫자는 표로 (필수. 줄글로 나열하지 말 것)

§결과 섹션이 다음 모양이면 자동 실패: *모델 A는 85.5점, B는 75.8점, C는 GSM8K 89.2 MATH-500 84.2 HotpotQA 88.4 ... 평균 12.7배 빠르고 ...*. 사용자가 가장 자주 잡아내는 패턴입니다. 세 개 이상의 시스템 × 두 개 이상의 컬럼이면 무조건 마크다운 표로 옮깁니다.

**판단 기준:**
- *시스템 ≥ 3개, 컬럼 ≥ 2개* → 표 거의 무조건. 메인 결과 표 한 장은 §결과 가장 위에.
- *벤치마크별 점수 줄줄이* (`GSM8K X.X, MATH-500 Y.Y, HotpotQA Z.Z, LiveCodeBench W.W`) → 행=시스템, 열=벤치마크.
- *카테고리별 정확도* (`static 82.0%, dynamic 72.4%, workflow 72.6%, gotchas 51.7%`) → 행=시스템 한 줄, 열=카테고리. 또는 행=카테고리 한 컬럼.
- *공격/방어/필터링 등 세 가지 victim model* → 행=시스템, 열=victim. 평균은 마지막 열.
- *라운드별 / 에폭별 곡선* → 표보다 줄글이나 그림이 나음. 표는 횡단면(snapshot) 결과에.
- 한두 숫자만 비교한다면(`A는 92.8, B는 75.8`) 표 불필요. 줄글로.

**형식:**
- 최고 성적은 **굵게**. tie면 둘 다 굵게.
- 단위는 헤더에 ((%), (s), (점)). 표 안에는 숫자만.
- 시스템 이름이 길면 줄여 쓰고 표 아래 한 줄로 풀이.
- 본문에서 표를 *해석*하는 1~2문단을 표 직후에 둡니다. 표만 던지면 독자가 다시 찾아야 함. *AgentRunbook-C가 RAG 베이스라인보다 24~32점 앞서고, 무너지는 곳은 gotcha입니다.* 식으로.

**예시 (간단형):**
```
| 시스템             | LME-V2-Small | LME-V2-Medium | 평균 |
| ----------------- | ------------ | ------------- | ---- |
| AgentRunbook-C    | **74.9**     | **70.1**      | **72.5** |
| Codex (vanilla)   | 69.9         | 68.7          | 69.3 |
| AgentRunbook-R    | 59.6         | 57.0          | 58.3 |
| Simple RAG        | 42.8         | 38.1          | 48.5 |
```

**예시 (카테고리별):**
```
| 카테고리 | AgentRunbook-C | Codex |
| ------- | -------------- | ----- |
| static   | **82.0**       | 78.4  |
| dynamic  | **72.4**       | 70.1  |
| ...      |                |       |
```

#### 수식 (필수. 줄글로 풀지 말 것)

블로그 빌드가 **MathJax**를 띄워줍니다. 논문에서 수식이나 수식적 표현이 등장하면 **LaTeX로 적습니다.** 한국어 줄글로 "곱하기 / 나누기 / 제곱 / 로그 / 시그마 / 1에서 빼고 다시 곱한 값" 같은 식으로 풀어쓰지 않습니다. 사용자가 가장 자주 잡아내는 패턴입니다.

- 인라인 수식 `$ ... $`: 본문 문장 안에 섞이는 짧은 식, 변수, 복잡도 표기, 작은 산술.
- 디스플레이 수식 `$$ ... $$`: 독립된 줄에 놓이는 정의식, 손실 함수, 합성 규칙, 합/곱 표기.
- 변수/기호 1개도 가능하면 `$N$`, `$k$`처럼 감싸 줍니다.

**한국어 → LaTeX 치환 예시 (반드시 이렇게 고친다):**

| 줄글 (X)                                  | LaTeX (O)                                            |
| -------------------------------------- | --------------------------------------------------- |
| `(5 곱하기 4) 5승 = 3,200,000개`            | `$(5 \times 4)^5 = 3{,}200{,}000$`                  |
| `O(N log N)` / `O(N 로그 N)`              | `$O(N \log N)$`                                     |
| `1에서 (1 빼기 각 정확도)의 곱을 뺀 값`             | `$1 - \prod_i (1 - p_i)$`                           |
| `모두의 곱`                                 | `$\prod_i p_i$`                                     |
| `가중 합`                                  | `$\sum_i w_i p_i$`                                  |
| `평균 expected utility`                   | `$\mathbb{E}[U]$` 또는 `평균 $\mathbb{E}[U]$`           |
| `정확도 p, 지연 t`                           | `정확도 $p$, 지연 $t$`                                   |
| `3.4배 빠르다` / `12.7배`                    | `$3.4\times$ 빠르다` (배수 표기는 `$N\times$` 권장, 줄글도 허용)   |
| `평균 Spearman correlation 0.92`         | `평균 Spearman $\rho = 0.92$` (논문에 기호가 있으면 그대로 가져오기) |
| `손실은 cross entropy + KL의 가중합`          | `$\mathcal{L} = \mathcal{L}_{\text{CE}} + \lambda \, \mathcal{L}_{\text{KL}}$` |

**판단 기준:**
- 논문 본문에 *식 번호 (eq. 3)* 또는 *그리스 문자·아래첨자·기댓값·시그마*가 붙어 있으면 → 거의 항상 `$$ ... $$` 디스플레이.
- 합성 규칙·loss·objective처럼 *재현·인용 대상이 되는 식*은 무조건 LaTeX. 풀어쓰면 독자가 손으로 다시 적어야 합니다.
- 본문 흐름상 *순서·구조만 설명*하는 거라면 (`먼저 X, 그다음 Y`) LaTeX 안 써도 됨. 수식이 아니라 절차이기 때문.
- 단순 숫자(`85.5점`, `약 104만 개`, `32개 H100`)는 LaTeX 대상 아님.

**자주 빠지는 함정:**
- `5승` / `제곱` / `곱하기` / `로그` 같이 *한국어로 연산자 이름을 적는 순간* 자동 실패. 무조건 기호로.
- 본문에서 변수 정의(`정확도를 p, 지연을 t로 두면`) 없이 식만 던지지 말기. 한 줄로라도 정의하고 식 띄우기.
- MathJax는 `\\` 줄바꿈, `\text{...}` 한글, `\mathbb{E}`, `\mathcal{L}` 다 됩니다. Obsidian 미리보기에서 깨지는 표기는 빌드에서도 깨지니 한 번 보고 확정.

### 5단계. Figure 추출과 삽입 (필수)

블로그 논문 글은 **frontmatter `image` 필드와 본문 figure 1~2장**을 반드시 포함합니다. 빌드된 카드/OG 이미지가 figure로 뜨도록 하기 위함이고, 본문도 그림 없으면 모델 논문 흐름을 못 따라갑니다.

#### 5-1. 어떤 figure를 고르는가

- **frontmatter image (1장)**: 논문 전체를 한 장으로 보여주는 figure. 보통 Figure 1·2·3 중 하나(architecture overview, teaser, main pipeline). 카드·OG에 쓰이므로 텍스트 잔글씨가 너무 빽빽한 건 피하기.
- **본문 figure (1~2장)**: 글이 다루는 핵심 기여를 시각적으로 보강하는 것. 비교 구조도, 결과 정성 예시, 데이터 파이프라인 등. 결과 표만 잔뜩인 figure는 본문에 안 넣음 (어차피 본문에서 수치로 다시 인용).

총 2~3장이 적당. 5장 이상이면 글이 figure 갤러리가 되니 자제.

#### 5-2. 추출 절차

PDF는 보통 Zotero local storage에 `$HOME/Zotero/storage/<ATTACH_KEY>/<filename>.pdf` 로 있습니다.

```bash
# 1. figure가 어느 페이지에 있는지 찾기
pdftotext -layout "<PDF_PATH>" /tmp/paper.txt
grep -nE "Figure [0-9]+ " /tmp/paper.txt | head

# 2. 해당 페이지를 PNG로 렌더 (150dpi 권장)
pdftoppm -png -r 150 -f <PAGE> -l <PAGE> "<PDF_PATH>" /tmp/<prefix>_page

# 3. PIL로 figure 영역만 crop (페이지 통째로는 본문 텍스트가 같이 잡힘)
python3 -c "
from PIL import Image
img = Image.open('/tmp/<prefix>_page-<NN>.png')
w, h = img.size
# 예: figure가 페이지 상단 ~38% 영역에 있으면
fig = img.crop((0, 0, w, int(h*0.38)))
fig.save('/tmp/<prefix>_figN.png')
"
```

자른 결과를 **Read 툴로 시각 확인**하는 단계를 반드시 거치기. crop 비율이 안 맞으면 캡션이 잘리거나 figure 절반만 들어와서 못 씀. 잘렸으면 비율 조정해서 다시 crop.

#### 5-3. 파일 저장과 frontmatter

논문 글의 이미지는 `markdown-blog/grid_Papers/_assets/` 에 저장. **다른 폴더 참조 금지** (크로스 폴더 시 404).

파일명은 슬러그-기반 + 용도 접미사 (kebab-case):
- `sensenova-u1-overview.png` (frontmatter image)
- `sensenova-u1-neo-unify.png` (본문 figure)
- `sensenova-u1-results.png` (본문 figure)

frontmatter (예시):
```yaml
image: "![[sensenova-u1-overview.png]]"
```

본문에는 `![[sensenova-u1-neo-unify.png]]` 형태로 그냥 위키 이미지 링크. 캡션은 직전·직후 문단에서 본문 흐름으로 풀어 쓰고, 별도 `*Figure N: ...*` 라인은 안 적음 (이미 본문이 설명함).

#### 5-4. 가장 흔한 실수

- 페이지 통째로 frontmatter image에 넣기 → 카드에서 figure가 아니라 본문 텍스트 페이지가 보임. 항상 figure만 crop.
- `_assets/` 아닌 위치 (raw 경로, /tmp, 다른 폴더 `_assets`)를 참조 → 빌드 404.
- 잔글씨가 빽빽한 figure를 OG 이미지로 → 썸네일에서 무슨 그림인지 안 보임. 이런 건 본문에만.
- 캡션 잘린 채로 저장 → crop 비율 조정 후 재추출.

### 6단계. 숫자 검수 (preprint면 특히)

arXiv preprint는 abstract와 본문 숫자가 자주 안 맞습니다 (저널 review 전이기 때문). 작업 중 다음을 검수합니다.

- Abstract의 *N문제 / N명*과 §1·§3.x의 같은 항목 수치 비교.
- 표(Table)의 합계와 본문 서술의 합계 비교.
- 그림(Figure) 캡션과 본문 수치 비교.
- 불일치를 발견하면 **본문에 명시**합니다. *abstract는 X라고 적었지만 §3.x 기준으로는 Y가 맞다*는 식으로 독자에게 알립니다.

### 7단계. 메모리 저장 (해당 시)

논문 리뷰 작업 중 사용자가 **톤·구조·형식에 대한 피드백**을 주면 즉시 메모리 저장 후보입니다. 예:

- *섹션 번호 빼고 짧은 제목으로* → feedback memory
- *저자 신상은 Dictionary로 분리* → feedback memory (이미 저장됨)
- *어미는 ~합니다체로* → feedback memory

본인이 *반항하는 거야*라고 지적할 때, 그건 보통 이 스킬이 미흡했다는 신호입니다. 그 패턴을 메모리로 남깁니다.

---

## 파일명·frontmatter 규칙

**파일명은 논문 제목을 그대로 사용합니다.** 임의로 줄인 슬러그(`SenseNova-U1.md`)는 안 됨. `:` 같은 파일시스템 금지문자는 `-`로 치환:

- `SenseNova-U1: Unifying Multimodal Understanding ...` → `SenseNova-U1 - Unifying Multimodal Understanding and Generation with NEO-unify Architecture.md`

**frontmatter `aliases`는 논문 글에서 비웁니다** (필드 자체를 빼거나 빈 리스트). 인물·일반 글에서는 alias를 쓰지만 논문은 제목 한 가지로만 참조하므로 불필요하고, 잘못 채우면 빌드 단계에서 오류가 납니다.

필수 frontmatter 필드:
- `date`: 작성 당일
- `tags`: `논문`(필수 분류) + 주제 태그 1~3개 (5개 이하)
- `description`: 한 문단
- `image`: `"![[<slug>-overview.png>]]"` 형식, `_assets/`에 실제 파일 존재해야 함
- `buzz`: HF Papers API 업보트 수 (정수). arXiv ID가 있는 논문은 **반드시** 포함:

```bash
curl -s "https://huggingface.co/api/papers/<arXiv_ID>" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('upvotes',0))" 2>/dev/null || echo 0
```

HF에 없는 논문(404·오류)은 `buzz: 0`. arXiv ID가 없으면 필드 생략.

예시 frontmatter:
```yaml
date: 2026-06-16
tags:
  - 논문
  - LLM
description: "..."
image: "![[paper-overview.png]]"
buzz: 142
```

`aliases` 안 씀. `image` 누락 시 OG/카드가 기본 아바타로 폴백되니 무조건 채움.

## 본문 최상단 citation (필수)

frontmatter 종료 `---` 바로 다음 줄에 인용 한 줄을 **반드시** 넣습니다. 빌드가 H1을 자동 생성하므로 본문은 곧장 citation으로 시작합니다.

형식 (IEEE-style 약식, blockquote `>`로 시작):

```
> <Initials. LastName>, <Initials. LastName>, ..., and <Initials. LastName>, "<논문 제목 전체>," arXiv:<ID>, <연도>.
```

- 저자가 2명이면 `A and B`.
- 저자가 3~7명이면 `A, B, ..., and Z`.
- 저자가 8명 이상이면 다 적기 부담스럽지만 가능하면 다 나열. 정 길면 처음 4명 + `et al.` 허용.
- 제목은 줄임 없이 전체. 부제(`:`)도 포함.
- arXiv ID는 `arXiv:2605.12500` 형식. 연도는 발행 연도.

예시:
```
> H. Diao, P. Wu, H. Deng, J. Wang, et al., "SenseNova-U1: Unifying Multimodal Understanding and Generation with NEO-unify Architecture," arXiv:2605.12500, 2026.
```

```
> E. D. J. Park and D. Alharthi, "Predictive Maps of Multi-Agent Reasoning: A Successor-Representation Spectrum for LLM Communication Topologies," arXiv:2605.11453, 2026.
```

citation 라인 다음에 빈 줄 한 줄, 그 다음에 본문 시작. citation 자체는 `>` 한 줄로 끝.

저자 명단은 Zotero의 `zotero_get_item_metadata` 또는 `zotero_search_items` 결과의 `Authors:` 필드에서 그대로 가져옴 (이미 `LastName, FirstName` 순으로 정렬돼 있음).

---

## 자주 빠지는 함정

1. **요약본으로 글쓰기**. 절대 금지. arXiv abstract와 트위터 스레드만으로 글을 쓰면 숫자가 틀립니다.
2. **저자 조사 누락**. *논문 다듬어줘*라는 짧은 요청이 와도 저자 섹션은 무조건 들어갑니다.
3. **저자 신상을 본문에 풀어쓰기**. Dictionary로 분리. 본문에서는 *왜 합류했나*만.
4. **모든 숫자를 abstract에서 가져오기**. preprint면 본문이 정본.
5. **친근체 잔재**. `~예요 / ~대요`가 한 군데라도 남으면 톤이 깨집니다. 마지막 패스에서 grep.
6. **Appendix 안 읽기**. 회고·한계·실험 디테일이 부록에 자주 있습니다.
7. **figure 누락**. frontmatter image 또는 본문 figure 안 넣으면 다시 작업. OG·카드가 깨집니다.
8. **파일명 슬러그화**. 논문 제목 그대로 가야 함. 짧게 줄이지 말기.
9. **citation 누락**. frontmatter 직후 `>` 인용 한 줄 안 넣으면 글이 출처 없이 시작합니다. 필수.
12. **buzz 필드 누락**. arXiv 논문이면 HF API 호출해서 반드시 frontmatter에 `buzz: <숫자>` 를 넣는다. 나중에 Obsidian Bases에서 인기순 정렬할 때 이 필드를 쓴다.
10. **수식을 한국어 줄글로 풀기**. `5 곱하기 4 5승`, `O(N 로그 N)`, `1에서 (1 빼기 각 정확도)의 곱을 뺀 값` 같은 표현이 한 군데라도 남으면 다시 작업. MathJax 빌드가 깔려 있으니 `$...$` / `$$...$$`로 적습니다.
11. **결과 숫자를 줄글로 나열하기**. *A는 92.8, B는 75.8, C는 GSM8K 89.2 MATH-500 84.2 ...* 같은 문단은 무조건 표로 옮깁니다. 시스템 3개 이상 × 컬럼 2개 이상이면 표.

---

## 산출물 체크리스트

- [ ] 1차 패스 완료: 조감도 확보, 5C 자문(Category·Context·Correctness·Contributions·Clarity) 통과
- [ ] 2차 패스 완료: figure·숫자 점검, 저자 한계 표시, 더 읽을 참조 메모
- [ ] 3차 패스 완료: Appendix까지 읽고, 숨겨진 가정 추출, 불일치 확인
- [ ] 핵심 저자 4~6명에 대한 Dictionary 항목을 만들었다
- [ ] 본문 §저자에는 신상이 아닌 *합류 동기*만 적었다
- [ ] 인물·모델·벤치마크·기관에 위키링크가 걸려 있다
- [ ] preprint면 숫자 불일치를 점검했고, 본문에 어떤 숫자가 정본인지 적었다
- [ ] 어미가 일관되게 존댓말(`~입니다 / ~합니다`)이다. `~다 / ~한다 / ~이다 / ~예요` grep해서 0건
- [ ] 섹션 제목이 짧다 (긴 부제·번호 없음)
- [ ] 굵게 강조가 핵심에만 걸려 있다
- [ ] Appendix의 회고/한계가 본문 §회고로 끌어올려져 있다
- [ ] 정리 섹션이 1~3 항목으로 압축돼 있다
- [ ] 파일명이 논문 제목 그대로다 (`:`만 `-`로 치환, 슬러그화 금지)
- [ ] frontmatter에 `image` 필드가 있고, `_assets/`에 실제 파일이 있다
- [ ] 본문에 figure 1~2장이 적절한 섹션에 배치돼 있다
- [ ] `aliases` 필드가 없거나 비어 있다
- [ ] frontmatter 직후 `>` citation 한 줄이 들어 있다 (저자·제목·arXiv ID·연도)
- [ ] 수식이 LaTeX로 적혀 있다 (`곱하기`, `5승`, `로그`, `시그마`, `1에서 ... 빼기`, `Big-O 안의 log/N` 같은 줄글 표기 grep해서 0건)
- [ ] 시스템 3개 × 컬럼 2개 이상의 성능 비교는 표로 옮겼다 (메인 결과 표 한 장 + 카테고리·victim별 표 1~2장)
