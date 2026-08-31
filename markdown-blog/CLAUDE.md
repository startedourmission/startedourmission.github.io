## 글 종류별 저장 위치

- **일반 정보성 글**은 `markdown-blog/grid_Posts/`에 작성한다. 프론트매터 tags에 `정보` 태그를 삽입한다.
- **논문 리뷰 글**은 `markdown-blog/grid_Papers/`에 작성한다. 프론트매터 tags에 `논문` 태그를 삽입한다.
- **사전·용어·인물 항목**은 `markdown-blog/Dictionary/`에 작성한다.
- **시리즈 강의·책**은 해당 시리즈 폴더(`CS229 Lectures/`, `Geoffrey Hinton/` 등)에 작성한다.
- **지식 관리·구축 방법론(KMS 시리즈)**은 `markdown-blog/Knowledge Management System/KMS 시리즈/`에 작성한다(leaf 하위 폴더, moc.md가 상위 목차). 프론트매터 tags에 `정보`, `KMS`를 포함한다.

## 저장 금지 위치

- `markdown-blog/` 루트에 새 글을 작성하지 않는다. 루트에는 시스템 파일(`index.md`, `links.md`, `HOW THIS BLOG WORKS.md`, `node-pretext.md`, `CLAUDE.md`)만 유지한다.

## 초안 흐름

- 초안은 `raw/drafts/`에 먼저 저장한 뒤, 검토 후 해당 목적 폴더로 이동한다.
- 사용자가 "옮겨"라고 지시하면 drafts → 목적 폴더로 이동한다.

## 공통 규칙

- 모든 글은 마크다운이며, 프론트매터 `date`에 작성 당일 날짜를 쓴다.
- 본문에 H1(`# 제목`)을 넣지 않는다. 빌드가 자동 생성한다.
- 이미지는 해당 폴더의 `_assets/`에 저장하고 `![[파일명.png]]` 형식으로 참조한다. 크로스 폴더 이미지 참조 금지.
- 태그는 한 글에 5개 이하, 따옴표·`#` 금지.
