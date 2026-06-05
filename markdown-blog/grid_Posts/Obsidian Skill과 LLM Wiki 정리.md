---
date: 2026-05-14
tags:
  - 정보
  - Obsidian
  - LLM
image: "![[obsidian-skill-llm-wiki.png]]"
description: "Obsidian CEO kepano가 만든 공식 Obsidian Skills와 Andrej Karpathy가 제안한 LLM Wiki 패턴. 둘은 별개 프로젝트지만 합치면 'Claude가 내 옵시디언 볼트를 직접 운영하는 지식 위키'가 됩니다."
---

> Obsidian CEO Steph Ango(kepano)가 만든 **공식 Obsidian Skills**와, Andrej Karpathy가 제안한 **LLM Wiki** 패턴. 둘은 별개 프로젝트지만, 합치면 "Claude가 내 옵시디언 볼트를 직접 운영하는 지식 위키"가 된다.

---

## 1. Obsidian Skills (kepano/obsidian-skills)

### 한 줄 정의
**Steph Ango(Obsidian CEO, GitHub: kepano)가 직접 만든 공식 Agent Skills 묶음.** Claude Code, Codex CLI, OpenCode 등 "Agent Skills 스펙"을 지원하는 모든 에이전트가 옵시디언 파일 형식을 정확히 다루도록 가르치는 규칙서다.

### 왜 필요한가
Claude Code는 기본적으로 옵시디언의 "비표준" 파일 형식을 모른다. 그대로 시키면:
- `.md`를 만들 때 위키링크(`[[페이지]]`) 문법을 깨먹는다
- `.base` 파일을 편집하면 잘못된 JSON을 뱉는다
- `.canvas` 파일을 쓰면 옵시디언에서 안 열린다

이 다섯 개 스킬은 그 갭을 메운다.

### 다섯 스킬

| 스킬 | 역할 |
|------|------|
| **obsidian-markdown** | Obsidian Flavored Markdown(위키링크, 임베드, 콜아웃, 프로퍼티) 작성·편집 규칙 |
| **obsidian-bases** | `.base` 파일(옵시디언 DB 레이어) — 뷰·필터·수식·요약 |
| **json-canvas** | `.canvas` 파일 — 노드·엣지·그룹·연결 |
| **obsidian-cli** | 옵시디언 CLI 연동 (플러그인·테마 개발용) |
| **defuddle** | 웹페이지에서 광고·내비·페이지 chrome을 걷어내고 깔끔한 마크다운으로 추출 → **토큰 절약** |

### 설치

```bash
# 옵시디언 플러그인 마켓플레이스
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills

# 또는 skills.sh CLI로 (Claude Code용)
npx skills add kepano/obsidian-skills@obsidian-markdown -g -y
npx skills add kepano/obsidian-skills@obsidian-bases -g -y
npx skills add kepano/obsidian-skills@json-canvas -g -y
npx skills add kepano/obsidian-skills@obsidian-cli -g -y
```

### 의의·맥락
- repo 생성: **2026-01-02**, MIT 라이선스
- 별 30,897개, 포크 2,115개 (2026-05-13 기준) — Agent Skills 생태계 중 최상위 인기
- "툴 벤더가 직접 공식 스킬을 만들기 시작한 신호탄" — Obsidian 외에 다른 제품들도 이 흐름을 따라갈 가능성
- skills.sh 통계: obsidian-bases 3.9K, obsidian-markdown 3.4K, json-canvas 2.2K, obsidian-cli 1.3K 설치

### 1차 출처
- GitHub: <https://github.com/kepano/obsidian-skills>
- kepano 프로필: <https://github.com/kepano>

---

## 2. LLM Wiki (Karpathy 패턴)

### 한 줄 정의
**Andrej Karpathy가 2026-04-04 gist로 제안한 패턴.** RAG처럼 매번 원본을 검색하지 말고, **LLM이 마크다운 위키를 직접 짓고 유지·갱신**하게 만들자는 접근.

### 핵심 통찰 (직접 인용)

> "지식 베이스 유지에서 지루한 부분은 읽기나 생각이 아니라 **bookkeeping**이다."
> — Karpathy, llm-wiki gist

사람이 손으로는 한 달도 못 버티는 교차참조·일관성 관리를 LLM은 잘한다. 그래서 사람은 소스를 던지고, LLM이 위키를 키운다.

### 3-layer 아키텍처

```
raw/        ← 원본 (불변): 기사·논문·이미지·데이터
wiki/       ← LLM이 만든 마크다운 페이지들 (요약·엔티티·개념)
CLAUDE.md   ← 스키마: 규칙·워크플로 정의
```

### 3가지 operation

| 작업 | 동작 |
|------|------|
| **Ingest** | 새 소스를 읽고 요약 작성 → index.md 갱신 → 관련 엔티티·개념 페이지 수정 |
| **Query** | 위키 페이지를 먼저 검색해 답변 → 가치 있는 답변은 **새 페이지로 저장** |
| **Lint** | 주기적 점검: 모순, 낡은 주장, 고아 페이지, 끊긴 교차참조 |

추가로 `index.md`(카테고리별 카탈로그), `log.md`(시간순 작업 기록)를 유지한다.

### RAG와의 차이

| | 전통 RAG | LLM Wiki |
|---|---|---|
| 저장 | 벡터 DB | 평문 마크다운 |
| 매 쿼리마다 | 원본 chunk 재검색·재해석 | 위키에서 합성된 답을 바로 인용 |
| 누적 | 안 됨 (매번 0에서 시작) | 됨 (질문할수록 위키가 풍부해짐) |
| 효율 | 기준선 | 70배 효율 주장 (출처: VentureBeat 기사) |
| 적합 규모 | 수만~수백만 문서 | **수백~수천 페이지의 큐레이션된 지식** |

### 1차 출처
- Karpathy 원본 gist: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

---

## 3. 두 개를 합치면

**Obsidian Skills + LLM Wiki = "Claude가 내 옵시디언 볼트를 운영하는 지식 위키"**

- LLM Wiki 패턴이 *왜·무엇을* 정의한다면
- Obsidian Skills는 *어떻게 옵시디언 안에서* 정확히 해낼지를 정의한다
- 합치면 Claude Code가 볼트 안에서 raw/ → wiki/ 사이클을 옵시디언 표준 파일(.md/.canvas/.base)로 정확하게 돌릴 수 있다

골든래빗 자료 중 이미 이 결합을 구현한 사례:
- **바로 72 — LLM 위키 구축하기** (바로바로 클로드 7장 4절 초고, 2026-04-14)
  - 위치: `HubVault/_Inbox/Archive/바로바로_클로드/바로72 초고 - LLM 위키 구축하기.md`
  - 패턴: Ingest → Update → Review → Query
  - 서브에이전트로 수집과 검증 분리
  - CLAUDE.md 하나로 하네스 정의

### 활용 시나리오

1. **편집자 개인 지식 위키** — 도서별 회고·저자 노트·시리즈 가이드·표지 분석을 raw로 던지면 LLM이 교차 정리
2. **신간 기획 리서치 위키** — 시장 자료·경쟁서·인터뷰를 raw에 쌓고, 기획 단계에서 wiki를 reference로 사용
3. **사내 노하우 위키** — 거래처·인쇄소·외주 정보 (지금은 `goldendb/data/context/업무정보.md`에 평문으로 누적 중인 것을 위키 패턴으로 진화 가능)

---

## 4. 참고 자료

### 1차 소스
- [kepano/obsidian-skills (GitHub)](https://github.com/kepano/obsidian-skills)
- [Karpathy llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

### 해설·튜토리얼
- [Obsidian Skills — Let Your Agent Manage Your Second Brain (DEV)](https://dev.to/stevengonsalvez/obsidian-skills-let-your-agent-manage-your-second-brain-4fel)
- [Claude Skills for Obsidian: Steph Ango's Official Agent Integration](https://claudeskills.info/blog/obsidian-claude-skills-guide/)
- [Obsidian Skills — Empowering AI Agents to Master Obsidian Knowledge Management (Medium)](https://addozhang.medium.com/obsidian-skills-empowering-ai-agents-to-master-obsidian-knowledge-management-8b4f6d844b34)
- [Andrej Karpathy's LLM Wiki — Create your own knowledge base (Medium)](https://medium.com/@urvvil08/andrej-karpathys-llm-wiki-create-your-own-knowledge-base-8779014accd5)
- [What Is Karpathy's LLM Wiki? Build a Personal KB with Claude Code (MindStudio)](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code)
- [Karpathy LLM Knowledge Base — bypasses RAG (VentureBeat)](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
- [Beyond RAG: LLM Wiki Pattern that Compounds (Level Up Coding)](https://levelup.gitconnected.com/beyond-rag-how-andrej-karpathys-llm-wiki-pattern-builds-knowledge-that-actually-compounds-31a08528665e)
- [LLM Knowledge Bases (DAIR.AI Academy)](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)
- [How to Build Karpathy's LLM Wiki (Starmorph blog)](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide)

### vault 내부 관련 자료
- `HubVault/_Inbox/Archive/바로바로_클로드/바로72 초고 - LLM 위키 구축하기.md` — 책 챕터 초고
- `HubVault/Claude/기획편집 유용 스킬 정리.md` — skills.sh 에코시스템 분류
- `AutoVault/블로그/markdown-blog/grid_Posts/Claude와 옵시디언으로 만드는 자동 지식 볼트.md` — 이미 게시된 글
