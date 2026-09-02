---
name: arxiv-to-zotero
description: Add an arXiv paper to Zotero (with PDF attached) using the Zotero Web API. Use this skill whenever the user wants to save an arXiv link to their Zotero library — phrases like "이 논문 조테로에 넣어줘", "arxiv 링크 조테로", "이거 zotero에 저장", "조테로에 추가해줘", or just pasting an arxiv.org URL with intent to archive it. Pulls metadata from arXiv, creates a `preprint` item, downloads the PDF, and attaches it inside the `Inbox` collection.
---

# arXiv → Zotero

arXiv 링크 하나를 받아서 Zotero `Inbox` 컬렉션에 PDF까지 첨부해 저장합니다. 브라우저 확장 거치지 않고 Zotero Web API로 바로 꽂습니다.

## 자격증명

볼트 루트 `.env`에서 읽습니다:

- `ZOTERO_USERID` — 숫자 user ID
- `ZOTERO_PRIVATE_KEY` — Zotero API 키 (library write 권한 필요)

`.env`는 절대 출력/커밋하지 말 것. 값은 `set -a; source .env; set +a` 식으로 로컬 셸에만 노출합니다.

## 사전 캐시: 컬렉션 ID

`Inbox` 컬렉션의 key를 한 번만 조회해서 `.claude/skills/arxiv-to-zotero/.collection_key` 에 캐시합니다. 파일이 있으면 그 값을 신뢰하고, 없거나 빈 값이면 다시 조회합니다.

조회:
```bash
curl -s -H "Zotero-API-Key: $ZOTERO_PRIVATE_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USERID/collections?format=json" \
  | jq -r '.[] | select(.data.name=="Inbox") | .key'
```

비어 있으면 컬렉션을 생성합니다:
```bash
curl -s -X POST \
  -H "Zotero-API-Key: $ZOTERO_PRIVATE_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"name":"Inbox","parentCollection":false}]' \
  "https://api.zotero.org/users/$ZOTERO_USERID/collections" \
  | jq -r '.successful["0"].key'
```

받아낸 key를 `.collection_key`에 저장.

## 워크플로우

### 1단계 — arXiv ID 추출

사용자 입력에서 URL 또는 ID를 잡아냅니다. 지원 패턴:

- `https://arxiv.org/abs/2401.12345`
- `https://arxiv.org/abs/2401.12345v2`
- `https://arxiv.org/pdf/2401.12345.pdf`
- `arxiv.org/abs/cs.CL/0301001` (구형)
- `2401.12345` 단독

정규화: 버전 접미사(`v\d+`)는 제거, 정규 ID만 보관.

### 2단계 — 메타데이터 조회

arXiv API (`http://export.arxiv.org/api/query?id_list=<ID>`)를 호출해 Atom XML을 받습니다.

```bash
curl -s "http://export.arxiv.org/api/query?id_list=$ARXIV_ID"
```

추출 항목:
- `title` (개행/연속 공백 정리)
- `summary` → abstract
- 모든 `<author><name>` → 저자 목록
- `published` → 발행일 (YYYY-MM-DD)
- `<arxiv:doi>` 또는 `<link title="doi">` (있으면)
- `<arxiv:primary_category term="...">` → 카테고리
- `<link title="pdf" href="...">` → PDF URL

XML 파싱은 Python `xml.etree.ElementTree` 권장. namespace는 `atom: http://www.w3.org/2005/Atom`, `arxiv: http://arxiv.org/schemas/atom`.

### 3단계 — Zotero 아이템 생성

`itemType`은 **`preprint`** 사용 (publication 정보가 명확해지면 사용자가 나중에 바꾸도록).

```json
[{
  "itemType": "preprint",
  "title": "<제목>",
  "creators": [
    {"creatorType": "author", "firstName": "<이름>", "lastName": "<성>"}
  ],
  "abstractNote": "<abstract>",
  "repository": "arXiv",
  "archiveID": "arXiv:<ID>",
  "date": "<YYYY-MM-DD>",
  "DOI": "<doi 있으면, 없으면 빈 문자열>",
  "url": "https://arxiv.org/abs/<ID>",
  "libraryCatalog": "arXiv.org",
  "collections": ["<INBOX_KEY>"],
  "tags": [{"tag": "<primary_category>"}]
}]
```

저자 이름 분리: `"Firstname Middlename Lastname"` → `lastName = 마지막 토큰`, `firstName = 나머지`. 단일 토큰이면 `name` 필드 하나로 (`{"creatorType":"author","name":"..."}`).

POST:
```bash
curl -s -X POST \
  -H "Zotero-API-Key: $ZOTERO_PRIVATE_KEY" \
  -H "Content-Type: application/json" \
  -d @item.json \
  "https://api.zotero.org/users/$ZOTERO_USERID/items"
```

응답의 `successful["0"].key`가 새 아이템의 key. 실패 시 `failed`를 보여주고 중단.

### 4단계 — PDF 첨부

PDF는 두 단계: (a) attachment 메타 생성, (b) 파일 업로드 인증 + 업로드.

**(a) attachment 아이템 생성** (parentItem = 3단계에서 만든 key):

```bash
ARXIV_PDF_URL="https://arxiv.org/pdf/${ARXIV_ID}.pdf"
TMP_PDF="/tmp/arxiv_${ARXIV_ID}.pdf"
curl -sL "$ARXIV_PDF_URL" -o "$TMP_PDF"
FILESIZE=$(stat -f%z "$TMP_PDF")
MD5=$(md5 -q "$TMP_PDF")
MTIME=$(($(date +%s) * 1000))
FILENAME="${ARXIV_ID}.pdf"
```

```json
[{
  "itemType": "attachment",
  "parentItem": "<PARENT_KEY>",
  "linkMode": "imported_file",
  "title": "arXiv Fulltext PDF",
  "filename": "<FILENAME>",
  "contentType": "application/pdf",
  "charset": "",
  "tags": [],
  "relations": {}
}]
```

POST 동일 엔드포인트, 응답의 `successful["0"].key` = `ATTACH_KEY`.

**(b) 업로드 인증 요청**:

```bash
curl -s -X POST \
  -H "Zotero-API-Key: $ZOTERO_PRIVATE_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "If-None-Match: *" \
  --data-urlencode "md5=$MD5" \
  --data-urlencode "filename=$FILENAME" \
  --data-urlencode "filesize=$FILESIZE" \
  --data-urlencode "mtime=$MTIME" \
  "https://api.zotero.org/users/$ZOTERO_USERID/items/$ATTACH_KEY/file"
```

응답 케이스:
- `{"exists": 1}` → 이미 같은 파일이 서버에 있음, 끝.
- 그 외에는 `url`, `contentType`, `prefix`, `suffix`, `uploadKey` 가 옴.

**업로드 본문 합성 + S3 PUT**:

```bash
# body = prefix + 파일 바이트 + suffix
cat <(printf '%s' "$PREFIX") "$TMP_PDF" <(printf '%s' "$SUFFIX") > /tmp/upload_body.bin

curl -s -X POST \
  -H "Content-Type: $UPLOAD_CONTENT_TYPE" \
  --data-binary @/tmp/upload_body.bin \
  "$UPLOAD_URL"
```

**업로드 등록**:
```bash
curl -s -X POST \
  -H "Zotero-API-Key: $ZOTERO_PRIVATE_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "If-None-Match: *" \
  --data-urlencode "upload=$UPLOAD_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USERID/items/$ATTACH_KEY/file"
```

이 단계가 까다로워서 **Python 스크립트로 한 방에 처리**하는 걸 권장합니다 (아래 참조 구현).

### 5단계 — 사용자에게 보고

성공 시 한 줄:
```
✅ {title} → Zotero Inbox (key: ABC123, PDF 첨부됨)
열기: zotero://select/library/items/ABC123
```

여러 링크가 한 번에 왔으면 각각 처리하고 줄별로 보고.

## 참조 구현 (Python)

복잡한 PDF 업로드 부분 때문에 셸만으로는 너저분합니다. 같은 폴더 `add.py` 사용:

```bash
set -a; source "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/.env"; set +a
python3 "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/AutoVault/.claude/skills/arxiv-to-zotero/add.py" <ARXIV_URL_OR_ID> [<ARXIV_URL_OR_ID> ...]
```

스크립트는 `ZOTERO_USERID`, `ZOTERO_PRIVATE_KEY` 환경변수와 `.collection_key` 캐시 파일을 사용합니다. `--no-pdf` 플래그로 PDF 첨부를 건너뛸 수 있습니다.

## 에러 처리

- arXiv API 응답에 `<entry>`가 없거나 `<title>Error</title>`이면 ID가 잘못된 것 → 사용자에게 알리고 다음 항목으로.
- Zotero POST가 429를 주면 `Retry-After` 헤더만큼 대기 후 1회 재시도.
- PDF 다운로드 실패는 메타데이터만 저장하고 PDF 첨부 단계만 건너뜀 (보고에 "PDF 실패" 표시).
- `403 Forbidden`이면 API 키 권한 부족 — 사용자에게 키를 library write 권한으로 재발급하라고 안내.

## 하지 말 것

- `.env` 값을 채팅/로그에 그대로 출력하지 말 것.
- `itemType: "journalArticle"`로 저장하지 말 것 — preprint가 정확함.
- 이미 같은 `archiveID`를 가진 아이템이 있는지 검사하는 단계는 **생략**한다. 사용자가 의도적으로 다시 넣으려고 호출했을 수 있고, 중복 검사 자체가 1회 추가 요청이라 가성비가 떨어진다. 사용자가 "중복 막아줘"라고 명시하면 그때 `q={ID}&qmode=everything` 검색으로 확인.
