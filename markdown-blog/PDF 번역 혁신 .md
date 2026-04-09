---
date: 2025-09-29
tags:
  - 정보
aliases:
image: "![[1-PDFMathTranslate.png]]"
description: 여러분이 굉장히 놀랄만한 PDF 번역 도구입니다. PDF로 작업을 자주 하거나 저처럼 외국 자료를 볼 일이 많은 분께 강력 추천합니다. PDF의 복잡한 구조를 어떻게 처리하는지 내부 코드도 뜯어보고 싶네요. Zotero와 연동할 수 있어 더욱 편리합니다.
---
PDF 번역이 쉬운 문제는 아닙니다. 파일 구조가 복잡해서 단순한 텍스트 복사-붙여넣기도 매끄럽게 잘 안 된다는 사실 다들 아실겁니다. 그리고 영어는 그나마 괜찮은데 요새 뛰어난 중국어 논문이 많아서 번역기가 절실합니다. 저는 외국어에 약해서 이런게 너무 필요했습니다. **PDFMathTranslate**는 PDF 형태 그대로 번역을 수행하는 도구입니다. 

![[1-PDFMathTranslate.png|714x488]]

처음 봤을 때 너무 놀라서 뒤집어졌습니다. 언어의 장벽이 지식을 습득하는 데 정말 크게 작용하지 않나요? 이게 있으면 걱정이 없겠습니다. 더 마음에 들었던 것은 Zotero 플러그인으로 연동할 수 있다는 겁니다. 저는 Zotero를 정말 많이 씁니다. 이젠 다른 서지 프로그램으로 넘어가기도 힘들죠. MCP에 이어 번역까지 완벽한 저의 Zotero 생태계가 만들어진 것 같습니다. 

- 깃허브 링크 : https://github.com/Byaidu/PDFMathTranslate
- Zotero 플러그인 : https://github.com/guaguastandup/zotero-pdf2zh

설치는 간단합니다. 압축파일 하나 받아서 의존성 깔고 실행만 하면 됩니다. 의존성이 많아서 가상 환경 사용을 추천합니다. 저는 uv를 사용했습니다. 사족으로, uv는 이제 최고의 패키지 관리 도구가 된 것 같습니다. 관리도 편하고 속도가 너무 빨라요. 

```bash
curl -L https://raw.githubusercontent.com/guaguastandup/zotero-pdf2zh/refs/heads/main/server.zip -o server.zip

unzip server.zip

cd server

uv venv
uv pip install -r requirements.txt
uv run server.py
```

그리고 Zotero 플러그인을 설치합니다. 위 플러그인 깃허브에서 Zotero 플러그인 설치 파일을 내려받을 수 있습니다.

![[1-zoteroplugin3.png|590x235]]


Zotero에서 플러그인을 추가하기 위해 Zotero-도구-Plugins에 들어갑니다.

![[1-zoteroplugin.png]]

플러그인 관리 화면에서 톱니바퀴 아이콘을 눌러 내려받은 설치 파일로 플러그인을 설치합니다.


![[1-zoteroplugin2.png]]

이렇게 논문을 선택했을 때 PDF2zh 플러그인이 보이면 성공입니다. 

![[1-PDF2zh.png|653x498]]

네 가지 번역 옵션이 있습니다. 결과 화면을 어떻게 표시할 지 선택하는 겁니다. 깃허브에 각 옵션에 대한 설명이 나와있습니다.

![[1-zoteroplugin4.png|588x572]]

저는 보통 Billungual PDF 옵션으로 번역합니다. 양 쪽으로 나란히 보여주니 제일 보기가 편하더라구요. 1번 옵션도 좋습니다. 이렇게 번역한 PDF 파일은 server/translated에 저장됩니다. 아직 불안정한 건지 번역 중 오류도 발생하긴 하네요. 분량 문제인지 인식하지 못하는 형식이 있는건지는 좀 더 사용해봐야겠습니다. 


