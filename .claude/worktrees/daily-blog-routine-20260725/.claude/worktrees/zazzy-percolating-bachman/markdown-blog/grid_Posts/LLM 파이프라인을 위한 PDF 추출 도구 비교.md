---
date: 2026-05-08
tags:
  - 정보
  - 오픈소스
description: "pdftotext, pymupdf4llm, MinerU, marker, docling — LLM 파이프라인에서 PDF를 다루는 대표 도구 5개와 상황별 선택 기준을 정리합니다. 한국어 문서, 표, 스캔본, 속도 — 무엇을 우선시하느냐에 따라 답이 달라집니다."
---

[[LLM]] 파이프라인에 PDF를 넣어야 할 때 선택지가 너무 많습니다. 빠른 게 좋은지, 정확한 게 좋은지, 한국어가 되는지, GPU가 필요한지 — 조건마다 최선의 도구가 다릅니다.

PDF 파싱이 어려운 이유부터 짚고 갑니다. PDF는 인쇄를 위한 포맷입니다. 텍스트 흐름이 아니라 좌표 기반으로 글자를 배치합니다. 다단 컬럼, 표 셀, 수식, 머리글/바닥글이 모두 좌표로만 구분됩니다. 스캔한 PDF는 아예 이미지뿐이라 OCR 없이는 텍스트를 꺼낼 수 없습니다. 한국어는 폰트 인코딩 문제가 추가로 붙습니다. 여기에 RAG 청킹까지 고려하면 도구 선택이 파이프라인 품질 전체를 좌우합니다.

## pdftotext — 가장 빠른 선택

```bash
# Ubuntu/Debian
sudo apt install poppler-utils

# macOS
brew install poppler

pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt  # 레이아웃 보존
```

Poppler 라이브러리의 CLI 도구입니다. PDF 내부 텍스트 스트림을 직접 읽어내기 때문에 GPU도, 무거운 모델도 필요하지 않습니다. 수백 페이지짜리 문서를 초 단위로 처리합니다.

디지털 텍스트가 포함된 논문이나 보고서라면 충분합니다. `-layout` 옵션으로 공백 정렬을 보존하면 다단 컬럼을 어느 정도 살릴 수 있습니다.

한계는 명확합니다. 이미지 기반 스캔 PDF는 전혀 처리하지 못합니다. 표 구조가 무너집니다. 한국어는 `poppler-data` 패키지를 추가로 설치해야 하고, 폰트 인코딩이 잘못된 PDF는 복구가 안 됩니다. 마크다운이나 JSON 출력도 없습니다.

**쓸 때:** 전처리 파이프라인에서 디지털 텍스트 PDF를 빠르게 긁어야 할 때.

## pymupdf4llm — RAG 파이프라인의 기본기

```bash
pip install pymupdf4llm
```

```python
import pymupdf4llm

md_text = pymupdf4llm.to_markdown("input.pdf")
```

PyMuPDF 위에 [[LLM]]/RAG 최적화 레이어를 올린 라이브러리입니다. "No GPU, no Cloud, no Tokens required"를 표방하며, 한 줄 코드로 PDF를 마크다운으로 변환합니다.

속도는 CPU 기준 약 0.12초/페이지입니다. 표는 pipe-table 마크다운으로 자동 변환하고, 다단 컬럼은 읽기 순서를 재구성합니다. LangChain, LlamaIndex 통합도 지원합니다.

한국어는 PyMuPDF 기반이라 DroidSans Fallback 폰트 내장으로 CJK 처리가 됩니다. 스캔 PDF OCR은 Tesseract/RapidOCR를 별도 설치하면 사용 가능하고, 텍스트가 있는 페이지는 OCR을 건너뛰어 속도를 최적화합니다.

주의할 점은 라이선스입니다. **AGPL v3**라 상업용 폐쇄형 소프트웨어에 쓰려면 별도 계약이 필요합니다. 복잡한 중첩 표나 수식은 ML 기반 도구보다 정확도가 낮습니다.

**쓸 때:** 개인/오픈소스 프로젝트의 RAG 파이프라인에서 빠르고 가벼운 마크다운 변환이 필요할 때.

## MinerU (opendatalab) — 한국어 포함 고정확도

```bash
uv pip install -U "mineru[all]"
```

OpenDataLab이 만든 고품질 문서 파싱 엔진입니다. GitHub 스타 62,000개 이상으로 가장 큰 커뮤니티를 갖고 있습니다. VLM + OCR 듀얼 백엔드 아키텍처를 씁니다.

정확도가 강점입니다. Pipeline 백엔드 기준 OmniDocBench 85+, VLM 백엔드는 95+. 표는 HTML로, 수식은 LaTeX로 변환합니다. **109개 언어 OCR을 지원하며 한국어, 중국어, 일본어를 명시적으로 지원합니다.** 출력은 마크다운, JSON, 이미지 포함 멀티모달 마크다운.

트레이드오프는 하드웨어입니다. RAM 최소 16GB(권장 32GB+), VRAM 2~8GB. CPU-only 모드도 지원하지만 속도가 느립니다. Docker, CLI, API, 웹 인터페이스를 모두 제공해서 배포는 유연합니다. 라이선스는 Apache 2.0 기반.

**쓸 때:** 한국어 문서를 고정확도로 처리해야 할 때, 또는 표/수식이 많은 학술 문서를 다룰 때.

## marker — 복잡한 PDF를 마크다운으로

```bash
pip install marker-pdf
```

```bash
marker input.pdf --output_dir output/
```

GitHub 스타 34,000개. 딥러닝(Surya OCR + 자체 레이아웃 모델) 기반 PDF → 마크다운 변환기입니다. PDF 외에도 DOCX, PPTX, XLSX, 이미지, EPUB를 지원합니다.

벤치마크에서 휴리스틱 점수 95.7%, LLM 평가 4.24/5로 LlamaParse와 Mathpix 대비 우수한 수치를 냅니다. 표 구조 보존, 수식 LaTeX 변환, 다단 컬럼 재구성 모두 처리합니다. Surya OCR이 90개 이상 언어를 지원해 한국어 스캔 PDF도 언어 지정(`--langs ko`) 없이 자동 인식됩니다.

속도가 문제입니다. **CPU에서 약 11초/페이지**로 느립니다. H100 GPU에서는 0.18초/페이지까지 올라가지만, GPU 없는 환경에서 대량 처리는 현실적이지 않습니다. 첫 실행 시 1GB 이상의 모델을 다운로드합니다. 라이선스는 GPL-3.0으로 상업용 폐쇄형 소프트웨어 사용에 제한이 있습니다.

**쓸 때:** GPU가 있고, 복잡한 학술 논문이나 다단 컬럼 문서를 정확하게 마크다운으로 변환해야 할 때.

## docling (IBM) — 테이블 정확도 최고

```bash
pip install docling  # Python 3.10+ 필요
```

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("input.pdf")
print(result.document.export_to_markdown())
```

IBM Research Zurich가 개발하고 MIT 라이선스로 공개한 도구입니다. GitHub 스타 59,000개. DocLayNet(레이아웃 분석)과 TableFormer(표 구조 인식) 두 모델을 씁니다.

**테이블 정확도 97.9%**가 핵심 강점입니다. 처리 속도는 CPU 기준 약 0.79초/페이지, M3 Max에서 0.32초/페이지, NVIDIA L4 GPU에서 114ms/페이지입니다. PDF 외에 DOCX, PPTX, XLSX, HTML, LaTeX, 이미지, 오디오(WAV/MP3), 비디오(MP4)까지 지원합니다.

출력 형식도 풍부합니다. 마크다운, HTML, JSON(lossless), DocTags, WebVTT. 에어갭(인터넷 차단) 환경에서의 완전 오프라인 동작을 공식 문서에서 명시합니다. 최근에는 [[MCP]] 서버 지원도 추가됐습니다.

한국어는 Tesseract OCR 연동으로 지원합니다. 자동 언어 감지 기능과 예제 코드도 공식 문서에 포함되어 있습니다.

**쓸 때:** 표가 많은 문서를 높은 정확도로 처리해야 할 때. 상업용 프로젝트(MIT 라이선스).

## 추가로 알아둘 도구

**pdfplumber** — 좌표 기반의 정밀한 테이블 추출이 필요할 때. MIT 라이선스. 시각적 디버깅 도구가 내장돼 있어 "이 영역의 표만 꺼내겠다" 수준의 세밀한 제어가 가능합니다. 스캔 PDF는 처리 불가.

**pypdf** — 텍스트 추출보다 PDF 분할/병합/암호화 같은 조작이 목적일 때. C 의존성이 없어 AWS Lambda나 가벼운 컨테이너에 올리기 쉽습니다. BSD-3 라이선스.

**LlamaParse** — 설정 없이 바로 쓰고 싶을 때의 클라우드 API. 월 10,000 크레딧 무료. 복잡한 문서는 1페이지당 최대 $0.045까지 올라갑니다. 데이터가 외부로 나가므로 민감 정보 처리에는 적합하지 않습니다.

## 상황별 선택 정리

| 상황 | 추천 도구 |
|------|-----------|
| 빠른 전처리, 디지털 PDF | pdftotext |
| RAG 파이프라인, 오프라인 | pymupdf4llm |
| 한국어 문서, 고정확도 | MinerU 또는 marker |
| 복잡한 표가 핵심 | docling 또는 pdfplumber |
| GPU 있음, 복잡한 학술 논문 | marker |
| 빠르게 프로토타이핑 | LlamaParse |
| PDF 분할/병합 등 조작 | pypdf |

표가 복잡하고 한국어가 포함된 문서라면 docling이나 MinerU. 속도가 최우선이고 스캔이 없는 디지털 PDF라면 pdftotext나 pymupdf4llm. GPU가 있고 정확도를 끝까지 올려야 한다면 marker. 라이선스와 하드웨어 요구사항을 먼저 확인하고 선택하는 게 순서입니다.
