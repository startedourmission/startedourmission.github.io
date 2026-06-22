---
date: 2026-06-21
tags:
  - 정보
  - Headliner
  - 에이전트
  - 오픈소스
  - AI평가
description: "AI 에이전트 스킬(MCP 확장 포함) 보안 취약점 64개 패턴·16개 카테고리를 탐지하는 오픈소스 스캐너. 야생 스킬 26.1%에서 취약점 발견, 5.2%는 악의적 의도 의심."
image: "![[nvidia-skillspector.png]]"
---

> 이 글은 [NVIDIA/SkillSpector GitHub 저장소](https://github.com/nvidia/skillspector) 및 관련 자료를 바탕으로 작성했습니다.

[[Claude Code]]·Codex CLI·Gemini CLI 같은 에이전트 도구가 스킬이나 MCP 확장을 실행하는 방식은 생각보다 취약합니다. 에이전트는 스킬이 시키는 대로 파일을 읽고 외부 API를 호출하고 코드를 실행합니다. 스킬 하나가 오염되면 에이전트 전체 실행 컨텍스트가 공격자 손에 들어올 수 있습니다.

NVIDIA가 공개한 SkillSpector는 이 위협에 직접 대응하는 오픈소스 정적·시맨틱 보안 스캐너입니다. 2026년 6월 16일 v2.0.0으로 출시됐고, 이틀 만에 GitHub 스타 5,500개를 넘겼습니다.

## 왜 스킬이 공격 표면이 됐나

에이전트 스킬과 MCP 확장은 사실상 코드입니다. 사용자가 "Jira 티켓을 열어줘"라고 하면 에이전트는 설치된 Jira 스킬을 호출하고, 그 스킬은 로컬 파일 시스템이나 네트워크에 접근하는 코드를 실행합니다. 이 과정에 악성 코드가 끼어든다면 어떻게 될까요.

Liu et al. (2026)의 "Agent Skills in the Wild" 연구는 42,447개 야생 스킬을 스캔한 결과를 공개했습니다. **26.1%에서 취약점이 발견됐고, 5.2%는 악의적 의도가 의심**됩니다. 네 개 중 하나는 사용하기 전에 검토가 필요하다는 결론입니다.

공격 벡터는 여러 종류입니다.

- **프롬프트 인젝션**: 스킬 메타데이터에 숨긴 지시문이 에이전트를 조종합니다. 도구 설명에 유니코드 동형 문자(homoglyph)나 HTML 주석으로 감춰진 명령이 들어갈 수 있습니다.
- **공급망 공격**: 의존성 패키지가 오염되거나, 스킬이 신뢰할 수 없는 외부 저장소에서 코드를 가져옵니다.
- **과도한 권한(Excessive Agency)**: 스킬이 실행에 필요한 수준을 넘는 파일 접근·외부 통신 권한을 요청합니다.
- **데이터 탈취**: 에이전트가 처리한 민감 정보를 외부 엔드포인트로 조용히 전송합니다.
- **메모리 포이즈닝**: 에이전트의 장기 기억 저장소에 악성 정보를 심어 이후 행동을 유도합니다.

## SkillSpector가 탐지하는 것

SkillSpector는 64개 취약점 패턴을 16개 카테고리로 분류해 탐지합니다.

| 카테고리 | 탐지 내용 |
|---------|---------|
| prompt_injection | 스킬 설명·메타데이터 내 인젝션 패턴 |
| data_exfiltration | 외부 전송 코드·비인가 API 호출 |
| privilege_escalation | 불필요한 권한 상승 시도 |
| supply_chain | 오염된 의존성·비신뢰 레지스트리 참조 |
| excessive_agency | 실행에 불필요한 파일/네트워크 접근 |
| output_handling | 출력물의 안전하지 않은 처리 |
| system_prompt_leakage | 시스템 프롬프트 유출 시도 |
| memory_poisoning | 에이전트 메모리 오염 시도 |
| tool_misuse | 도구 호출의 의도 외 사용 |
| rogue_agent | 무허가 에이전트 스폰 |
| trigger_abuse | 숨겨진 트리거·조건부 활성화 |
| dangerous_code | AST 기반 위험 코드 패턴 탐지 |
| taint_tracking | 오염된 데이터 흐름 추적 |
| yara_signatures | YARA 규칙 기반 알려진 악성 패턴 |
| mcp_least_privilege | MCP 확장의 과도한 권한 선언 |
| mcp_tool_poisoning | MCP 도구 메타데이터 내 인젝션 |

## 2단계 분석 파이프라인

SkillSpector의 탐지는 두 단계로 이루어집니다.

**1단계 — 빠른 정적 분석**: 64개 정규식 패턴 매칭, AST(추상 구문 트리) 행동 분석, 테인트 추적, YARA 시그니처 검사, OSV.dev를 통한 실시간 CVE 조회(오프라인 폴백 자동 지원). 대부분의 스캔이 이 단계에서 몇 초 안에 완료됩니다.

**2단계 — 선택적 LLM 시맨틱 분석**: 1단계만으로는 의도 파악이 어려운 패턴에 LLM을 투입합니다. 코드가 실제로 악의적 의도를 가지는지 자연어 수준에서 판단합니다. 추가 비용이 들지만 정밀도가 올라갑니다.

MCP 카테고리의 경우 유니코드 동형 문자나 HTML 주석으로 도구 메타데이터에 숨긴 인젝션을 탐지합니다. 육안 코드 리뷰로는 놓치기 쉬운 공격입니다.

## 사용 방법

설치는 pip 한 줄입니다.

```bash
pip install skillspector
```

스캔 대상은 Git 저장소·URL·zip 파일·디렉토리·단일 파일을 모두 지원합니다.

```bash
# GitHub 저장소 스캔
skillspector scan https://github.com/some-org/some-skill

# 로컬 디렉토리 스캔
skillspector scan ./my-skill-directory

# LLM 시맨틱 분석 포함
skillspector scan ./my-skill --semantic

# SARIF 형식 출력 (CI 통합용)
skillspector scan ./my-skill --format sarif -o results.sarif
```

출력은 JSON·Markdown·SARIF 세 가지 형식을 지원합니다. SARIF는 GitHub Actions·GitLab CI 등 CI/CD 파이프라인과 바로 연동할 수 있습니다. 스킬 설치 전 자동 검사를 파이프라인에 넣으면 됩니다.

## 야생 스킬 26.1%가 취약하다는 것의 의미

수치 자체보다 맥락이 중요합니다. 26.1%는 스킬이 악성이라는 뜻이 아닙니다. 취약점 패턴이 발견됐다는 것으로, 의도적 악용보다는 개발자 실수나 설계 결함이 많습니다. 그러나 5.2%의 "악의적 의도 의심" 수치는 다릅니다. 이미 에이전트 스킬이 사이버 공격의 진지한 표적이 됐다는 뜻입니다.

에이전트 환경에서 스킬은 코드보다 느슨하게 취급되는 경향이 있습니다. npm 패키지를 설치할 때는 그래도 package.json을 훑어보는 사람이 있지만, "유용해 보이는 MCP 서버"를 설치할 때 동일한 주의를 기울이는 사람은 드뭅니다. SkillSpector는 이 간극을 메우는 도구입니다.

> 프로젝트: [GitHub — NVIDIA/SkillSpector](https://github.com/nvidia/skillspector)
