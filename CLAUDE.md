# AutoVault

옵시디언 볼트 = 블로그 레포. **하나의 폴더, 하나의 git 레포**(`startedourmission.github.io`, 공개).

> 2026-08-31 통합. 볼트와 블로그 레포를 합쳤다.
> 이전 구조(`블로그/` 하위 레포, `raw/drafts/` 초안 폴더)는 없다.
>
> 2026-09-02 볼트를 iCloud로 되돌렸다. 서버컴·회사컴·폰 사이 동기화는 iCloud가 맡는다.
> **단 `.git`은 iCloud 밖 `~/git/AutoVault.git`에 있다.** 볼트 루트의 `.git`은 그곳을 가리키는
> 한 줄짜리 포인터 파일이다(`git init --separate-git-dir` 방식).
> iCloud가 `.git` 내부를 evict하면 git 명령이 통째로 멎고 레포가 깨진다 — 실제로 겪었다.
> **`.git`을 볼트 안으로 되돌리지 말 것.**
>
> 따라서 git은 기기 간 동기화 수단이 아니라 GitHub Pages 배포 전용이다.
> 레포를 가진 건 서버컴 한 대뿐이고, push도 서버컴만 한다. 회사컴엔 git이 없다.

## 초안 = `ready: false`

**모든 글은 처음부터 최종 목적지에 쓴다.** 초안 폴더는 없다. 프론트매터의 `ready`가 노출을 정한다.

| `ready` | 블로그 | 레포 |
|---|---|---|
| `false` | 안 보임 | 보임 (공개 레포) |
| 없음 | 보임 | 보임 |
| `true` | 보임 | 보임 |

- 빌드(`Obsidian.isUnpublished` → `Program.fs`)가 `ready: false`인 파일을 통째로 뺀다.
  HTML·인덱스·RSS·사이트맵·llms.txt에서 동시에 빠진다.
- **필드가 없으면 게시된다.** 기존 글 1,400여 편이 여기 해당한다.
  실수로 빠뜨렸을 때 "조용히 사라짐"이 아니라 "그냥 올라감"으로 실패하게 한 것이다.
- **`ready`는 `Headliner`처럼 사용자만 켠다.** Claude는 새 글을 항상 `ready: false`로 만들고
  이 값을 `true`로 바꾸지 않는다. "올려줘"라고 하면 체크박스를 켜는 게 아니라 `blog-publish`를 실행한다.
- 초안이라도 레포에는 공개된다. 안 되는 내용은 애초에 쓰지 않는다.

```bash
python3 tools/ready_queue.py            # 게시 대기 (ready:true 인데 아직 push 안 됨)
python3 tools/ready_queue.py --drafts   # ready:false 초안 전부
python3 tools/ready_queue.py --dest 논문 # 태그 → 목적지 폴더
```

## 게시 흐름

1. 글을 **목적지 폴더에 직접** 만든다 (`ready: false`). 목적지는 태그가 정한다(아래 표).
2. 사용자가 옵시디언 속성 패널에서 `ready`를 켠다 = 게시 승인.
3. `blog-publish`가 검증 게이트(`validate.py` · 팩트체크 · RSS)를 통과시킨 뒤 커밋·푸시.
4. GitHub Actions가 F# 빌드 후 Pages 배포.

2~4단계는 매일 04:00 일일 루틴이 자동으로 돌린다. 체크는 "읽어봤다"이지 "검증 건너뛰라"가 아니다 —
막힌 글은 `ready: true`인 채로 두고 다음 날 재시도한다.

### 태그 → 목적지

| 태그 | 폴더 |
|---|---|
| 논문 | `markdown-blog/grid_Papers/` |
| 정보 · 잡담 | `markdown-blog/grid_Posts/` |
| 제프리힌턴 / 얀르쿤 | `markdown-blog/Mastermind/…` |
| cs229 / cs230 / cme295 | `markdown-blog/Lectures Translate/…` |
| KMS | `markdown-blog/Knowledge Management System/` |
| 사전·인물·벤치마크 | `markdown-blog/Dictionary/` |

## 발행량과 밀도

- **하루 상한: 논문 리뷰 1편 + 정보·잡담 1편.** 후보가 몇 개든 넘기지 않는다. 한쪽이 비면 0편이 정상.
- **이 상한은 수집·작성 트랙에만 걸린다.** 사용자가 `ready`를 켠 글은 몇 편이 쌓여 있든 그날 전부 올린다.
- **정보·잡담은 서로 다른 레퍼런스 3개 이상.** 못 채우면 안 쓴다. 같은 보도자료 받아쓴 기사는 1개로 센다.
  논문 리뷰는 원문이 1차 출처라 예외.
- **우라까이 금지.** 출처가 엇갈리는 지점, 겹쳐야 보이는 것, 다들 빠뜨린 것 중 최소 하나를 짚는다.
  본문은 출처가 아니라 주제를 따라 전개한다. 상세는 `STYLE.md`.

## 프론트매터

```yaml
---
date: 2026-04-09
ready: false          # 초안일 때만. 게시본은 true 이거나 필드 없음
tags:
  - 논문
  - LLM
description: "한 줄 설명"
image: "![[이미지.png]]"
---
```

**태그**: 따옴표·`#` 금지, aliases·논문 제목 넣지 않음, 한 글에 5개 이하.

- 분류(필수 1개): 논문 · 정보 · 잡담
- 도메인(선택 1–3): LLM, 멀티모달, 컴퓨터비전, 영상처리, 음성, NLP, 강화학습, 추론, 에이전트, 확산모델, 트랜스포머, 머신러닝, 딥러닝, 데이터분석, 파이썬, 오픈소스, 도구, GPU, TPU, 반도체, 벤치마크, AI평가, SaaS
- 시리즈: 제프리힌턴, 얀르쿤, cs229, cs230, cme295, book, KMS
- 특수: Headliner(메인 노출), 베스트논문, MOC — **Headliner·베스트논문은 사용자만 부여한다.**

표기: 영문 이니셜리즘은 대문자(LLM, NLP, RAG, RL, GPU, TPU), 그 외 개념어는 한국어. 목록에 없는 주제는 신조어 대신 가장 가까운 기존 태그를 쓰거나 추가를 제안한다.

**image**: `![[파일명.png]]` 형식. 이미지는 **해당 폴더의 `_assets/`**에 둔다. 크로스 폴더 참조는 404다.

### Dictionary 전용

`type:` 필수 1개 — person / company / product / ai-model / benchmark / tool / hardware / concept.
`type:`이 항목 종류, `tags:`가 도메인 주제인 2축 분류다.

- **`type: person`에는 `인물` 태그를 반드시 함께.** 옵시디언 인물 뷰가 태그 기준이라 없으면 누락된다.
  `tools/check_person_tags.py`가 점검하고 `blog-check`가 매일 보고한다.
- 인물 노트는 점수 태그를 함께 달아서 **태그 5개 제한을 적용하지 않는다.**
- **파일명은 한글 이름.** 중국계는 병음을 성 먼저 붙여쓰고(`왕리민`), 서양은 한글 음차에 띄어쓰기(`크리스 래트너`),
  한국계는 실제 한글명. 영문·한자는 `aliases`에. **새로 만들기 전에 다른 표기로 이미 있는지 확인**해 중복을 막는다.

## 글쓰기 규칙

존댓말 기반 스토리텔링, 딱딱하면 안 됨 · 문제 → 해결 → 사용법 → 시사점 · H2 5–7개 이내 ·
검증 안 된 수치 금지 · **본문에 H1(`# 제목`) 넣지 않음**(빌드가 자동 생성).

## 빌드

- `dotnet run --project skunk-html.fsproj` (로컬 dotnet: `~/.dotnet/dotnet`)
- URL = 파일명 MD5 앞 8자리(`Url.toHashId`) · `[[파일명]]` → `해시.html` · `![[파일.png]]` → `폴더/_assets/파일.png`
- **로컬 빌드는 평소에 하지 않는다.** 빌드는 Actions 담당이고 `skunk-html-output/`(6.1GB)은 gitignore다.
  게시 전 RSS 게이트는 `python3 tools/rss_check.py --source <파일>` 로 빌드 없이 건다.
  **단 `SkunkHtml.fs`·`SkunkUtils.fs`·`Program.fs`를 고쳤으면 반드시 로컬 빌드로 확인하고, 끝나면 산출물을 지운다.**
- 푸시 뒤 `gh run watch --exit-status` 로 배포 결과를 확인한다. 빌드가 실패해도 사이트는
  이전 버전을 계속 서비스하므로 **갱신이 조용히 멈춘다.**

## 폴더

```
markdown-blog/       글 (= 게시 대상. 초안도 여기 산다)
Clippings/           웹 클리핑 원본
Excalidraw/          도해 원본 + 생성 스크립트
tools/  scripts/     검증·집계 도구
.claude/skills/      스킬 25개
paper-stubs/  주간리포트/  _Templates/
SkunkHtml.fs SkunkUtils.fs Program.fs   F# 빌드
```

## 절대 주의

- **`.env`·`.s2_api_key`는 gitignore돼 있다. 공개 레포이므로 절대 커밋하지 않는다.**
  Zotero 키는 `daily-paper-pipeline`이, S2 키는 `buzz-update.py`가 매일 쓴다. 지우지 말 것.
- **Google Workspace 연동은 `gws` CLI만 쓴다.** 별도 라이브러리를 설치하지 않는다.
- **외부 시스템 갱신 시 스냅샷·기억 기반 덮어쓰기 금지.** 먼저 GET으로 현재 상태를 읽고 필요한 부분만 수정한다.
- cron 로그는 볼트가 아니라 `~/Library/Logs/blog-daily-routine/`에 쌓인다.
