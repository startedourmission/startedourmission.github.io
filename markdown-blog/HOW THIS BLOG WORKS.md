---
date: 2026-04-13
tags:
  - 정보
description: "이 블로그가 어떻게 만들어지고 운영되는지에 대한 기술 문서. 옵시디언에서 마크다운을 쓰고, F# 빌드 시스템이 HTML로 변환하고, GitHub Pages로 배포됩니다. 이 문서는 자동으로 업데이트됩니다."
---

이 글은 이 블로그의 작동 방식을 설명합니다. 블로그가 변경될 때마다 이 문서도 자동으로 업데이트됩니다.

---

## 구조

옵시디언(Obsidian) 볼트에서 마크다운으로 글을 쓰고, F# 빌드 시스템이 HTML로 변환하고, GitHub Pages로 배포됩니다.

```
AutoVault/
  raw/drafts/     ← 초안 작성
  블로그/           ← git repo (startedourmission.github.io)
    markdown-blog/
      Geoffrey Hinton/   ← 힌튼 시리즈 25편
      CS229 Book/        ← CS229 강의 20장
      CME295 Book/       ← CME295 강의 9장
      grid_Papers/       ← 논문 리뷰
      grid_Posts/        ← 일반 게시글
      Dictionary/        ← 벤치마크, 인물, 칩 사전
      Python/            ← 파이썬 가이드
      _assets/           ← 루트 이미지
    css/                 ← 스타일시트
    html/                ← 템플릿
    SkunkHtml.fs         ← 빌드: HTML 생성
    SkunkUtils.fs        ← 빌드: 유틸리티
    Program.fs           ← 빌드: 메인
```

## 글 작성 → 게시 파이프라인

1. `raw/drafts/`에 마크다운 초안을 작성합니다
2. 프론트매터를 검증합니다 (태그 규칙, description, image)
3. `블로그/markdown-blog/`로 이동합니다
4. `git add → commit → push`합니다
5. GitHub Actions가 F# 빌드를 실행하고 GitHub Pages에 배포합니다

## 빌드 시스템

F#으로 작성된 정적 사이트 생성기입니다.

**마크다운 → HTML 변환:**
- YAML 프론트매터에서 메타데이터 추출 (date, tags, description, image)
- 옵시디언 위키 링크 `[[파일명]]` → HTML 링크로 변환
- 이미지 `![[파일.png]]` → `<img>` 태그로 변환
- MathJax 수식 지원

**URL 생성:**
- 게시글: 파일명의 MD5 해시 앞 8자리 (예: `a3f2b1c4.html`)
- 태그 페이지: `tag-태그명.html`
- 카테고리/그리드: 폴더명 기반

**SEO/AIEO:**
- OG 태그, Twitter 카드, JSON-LD(BlogPosting) 자동 생성
- 이미지 없는 글은 기본 아바타(notion_avatar.png)로 fallback
- `og:title`에는 블로그명 suffix 없음 (제목만)
- HTML 이스케이핑 적용 (escHtml, escJson)

**자동 생성 파일:**
- `sitemap.xml` — 모든 페이지 포함
- `robots.txt` — AI 크롤러(GPTBot, ClaudeBot, Google-Extended 등) 명시 허용
- `llms.txt` — AI를 위한 사이트 구조 파일 (메타데이터 + 태그 + 컬렉션)
- `rss.xml` — RSS 피드

## 프론트매터 규칙

```yaml
---
date: 2026-04-13
tags:
  - 정보
  - LLM
  - Headliner
description: "한 줄 설명"
image: "![[이미지.png]]"
---
```

**태그:** 따옴표 금지, `#` 금지, 5개 이하.
- 분류 (필수 1개): 논문, 정보, 잡담
- 주제 (선택): LLM, 머신러닝, 딥러닝, 파이썬, 영상처리, 데이터분석, 벤치마크, 오픈소스, AI평가
- 시리즈: 제프리힌턴, cs229, cme295
- 특수: Headliner, 베스트논문

**이미지:** `_assets/` 폴더에 저장. 다른 폴더의 이미지 참조 금지.

## 도해 생성

[node-pretext](https://github.com/startedourmission/node-pretext) (npm 패키지)로 텍스트 너비/높이를 정확히 측정하여 Excalidraw 도해를 프로그래밍으로 생성합니다.

- `gen_diagram.py`의 `labeled_box()`: 텍스트 크기에 맞춰 박스 자동 사이징
- `@swiftlysingh/excalidraw-cli`로 PNG export
- 스타일: 검은 선 + 흰 배경 + 영문 텍스트만

## 위키 링크

노트 간 `[[링크]]`를 적극적으로 사용합니다.
- Dictionary 항목(인물, 벤치마크, 칩)이 본문에 언급되면 첫 등장에 링크
- `autolink.py` 스크립트로 일괄 링크 (토큰 소모 없음)
- 새 글 작성 시 자연스럽게 링크 삽입

## 네비게이션

2단 구조:
- **nav-main**: Posts, Papers 등 주요 항목 (크고 굵게)
- **nav-sub**: Geoffrey Hinton, CS229 Book 등 서브 폴더 (작고 흐리게, flex-wrap)

## 통계

*이 섹션은 자동으로 업데이트됩니다.*

- 총 게시글: 170
- Dictionary 항목: 153
- 도해 이미지: 234
- 위키 링크: 902
- 마지막 업데이트: 2026-04-13
