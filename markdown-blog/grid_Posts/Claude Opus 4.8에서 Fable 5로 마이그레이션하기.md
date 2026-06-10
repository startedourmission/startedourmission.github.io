---
date: 2026-06-10
tags:
  - 정보
  - LLM
description: "모델 ID 한 줄 바꾸면 끝일 것 같지만, Fable 5로 넘어올 때 실제로 바꿔야 하는 것들이 있습니다. 적응형 사고 강제 활성화, 안전 분류기 폴백 처리, 30일 트래픽 보관 정책까지 실무 관점으로 체크리스트 형식으로 정리합니다."
---
[[Claude Fable 5]]가 나왔습니다. 성능은 올라갔고, 가격은 두 배입니다. Opus 4.8에서 넘어오는 마이그레이션은 "거의 드롭인"이라고 공식 문서가 말하는데, 그 "거의"가 어디에 있는지를 짚는 게 이 글의 목적입니다.

공식 마이그레이션 가이드는 [platform.claude.com/docs/en/about-claude/models/migration-guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide)에 있습니다. 이 글은 그 내용을 개발자 실무 관점으로 다시 읽습니다.

## 모델 ID 변경

가장 먼저 바꿀 것입니다.

```python
# 변경 전
model = "claude-opus-4-8"

# 변경 후
model = "claude-fable-5"
```

코드베이스 전체에서 모델 ID를 찾아 바꾸는 작업은 Claude Code가 있다면 자동화할 수 있습니다.

```text
/claude-api migrate this project to claude-fable-5
```

이 명령은 모델 ID 교체와 함께 필요한 파라미터 변경, 플랫폼별 ID 포맷(Bedrock, Vertex AI, Microsoft Foundry) 처리까지 묶어서 처리하고 수동 확인이 필요한 항목을 체크리스트로 뽑아줍니다.

## 가격

| | Opus 4.8 | Fable 5 |
|---|---|---|
| 입력 토큰 | $5 / 1M | $10 / 1M |
| 출력 토큰 | $25 / 1M | $50 / 1M |

정확히 두 배입니다. 토크나이저는 동일하니 같은 프롬프트에서 토큰 수는 거의 그대로입니다. 비용 재산정은 "토큰 수 x 2"로 시작점을 잡으면 됩니다.

## 적응형 사고가 항상 켜진다

Opus 4.8에서는 `thinking` 파라미터 없이 요청하면 사고 없이 응답했습니다. Fable 5는 다릅니다. `thinking` 필드가 없어도 적응형 사고가 자동으로 켜집니다.

사고 토큰이 `max_tokens` 한도 안에서 함께 소비됩니다. Opus 4.8에서 사고 없이 돌리던 워크로드를 Fable 5로 옮기면 같은 `max_tokens` 설정에서 사고 토큰이 추가로 사용되면서 비용이 더 올라갈 수 있습니다. 사고를 끄는 것도 불가능합니다.

```python
# 이렇게 하면 400 에러
client.messages.create(
    model="claude-fable-5",
    thinking={"type": "disabled"},  # 에러 반환
    ...
)
```

Opus 4.8에서 사고를 명시적으로 켰던 코드는 단순해집니다.

```python
# Opus 4.8
client.messages.create(
    model="claude-opus-4-8",
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...],
)

# Fable 5 — thinking 필드 제거 가능
client.messages.create(
    model="claude-fable-5",
    output_config={"effort": "high"},
    messages=[...],
)
```

적응형 사고가 항상 켜진다는 건 `max_tokens`를 다시 봐야 한다는 뜻입니다. 사고 토큰과 응답 텍스트가 합산되어 이 한도를 씁니다. Opus 4.8에서 사고 없이 돌리던 워크로드가 있다면 `max_tokens`에 여유를 더 줘야 할 수 있습니다.

## effort 기본값: high면 충분

Opus 4.8에서 코딩이나 고자율 에이전트 작업에 `xhigh`를 명시적으로 쓰던 팀이 많습니다. Fable 5에서는 대부분의 작업에 `high`가 적절합니다.

```python
output_config={"effort": "high"}   # 대부분의 작업
output_config={"effort": "xhigh"}  # 정말 능력이 중요한 경우에만
```

`xhigh`를 항상 쓰는 습관이 있다면 비용 측면에서 재검토할 여지가 있습니다. Fable 5의 `high`는 이전 모델의 `xhigh`보다 나을 때가 많습니다.

## 안전 분류기 폴백: 새로운 stop_reason

Fable 5에서 가장 새로운 API 동작입니다. 사이버보안, 생물학/화학, 증류 쿼리가 분류기에 걸리면 응답이 차단됩니다. 이때 반환되는 `stop_reason`이 `"refusal"`입니다.

```python
response = client.messages.create(
    model="claude-fable-5",
    messages=[{"role": "user", "content": "..."}],
)

if response.stop_reason == "refusal":
    category = response.stop_details.get("category")
    # "cyber" | "bio" | "reasoning_extraction" | None
    # 카테고리에 따라 처리
```

중요한 점 두 가지입니다.

첫째, 거부 응답은 HTTP 200입니다. 에러 코드가 아닙니다. `stop_reason`을 명시적으로 체크하지 않으면 빈 응답을 정상으로 처리할 수 있습니다.

둘째, 응답 생성 시작 전에 거부되면 입력 토큰은 청구되지 않습니다. 스트리밍 중간에 분류기가 작동하면 그때까지 생성된 출력은 청구됩니다.

전체 세션의 95% 이상은 폴백 없이 Fable가 그대로 응답합니다. 하지만 5%가 어디서 나오는지를 알아야 합니다. 사이버보안 연구, 생물학 관련 업무, 또는 다른 모델의 응답을 수집하는 워크로드라면 이 분류기에 걸릴 가능성이 있습니다.

자동 폴백이 필요하면 베타 파라미터를 쓸 수 있습니다.

```python
# 거부된 요청을 다른 모델로 자동 재시도 (베타, Claude API에서만)
client.messages.create(
    model="claude-fable-5",
    fallbacks=["claude-opus-4-8"],  # 베타 기능
    messages=[...],
)
```

다만 이 기능은 Claude API와 Claude Platform on AWS에서만 베타로 제공됩니다. Amazon Bedrock, Vertex AI, Microsoft Foundry에서는 클라이언트 쪽에서 재시도 로직을 직접 구현해야 합니다.

## 30일 트래픽 보관 정책

이건 코드 변경이 아니라 계약/운영 이슈입니다.

Mythos급 모델(Fable 5, Mythos 5)을 사용하는 모든 트래픽은 30일간 보관됩니다. 이전에 제로 보관(zero-retention) 계약을 맺은 기업 고객도 예외가 없습니다. 목적은 안전 모니터링이고, 모델 훈련에는 쓰지 않는다고 [[Anthropic]]은 밝혔습니다.

의료, 금융, 법률 분야처럼 데이터 보관 정책이 규정과 연결된 조직이라면 이 부분을 법무 또는 컴플라이언스 팀과 검토해야 합니다. 트래픽 내용이 30일간 Anthropic 시스템에 남는다는 것을 감수할 수 있는지 판단이 필요합니다.

Opus 4.8은 기존 제로 보관 계약이 유지되므로, 이 정책이 문제라면 당분간 Opus 4.8을 유지하는 것이 하나의 선택입니다.

## 프롬프트 캐싱: 최솟값이 낮아졌다

작지만 유용한 변화입니다. Fable 5의 프롬프트 캐싱 최솟값은 512 토큰입니다. Opus 4.8의 1,024 토큰보다 절반 낮습니다. 이전에는 너무 짧아서 캐시를 못 만들던 프롬프트가 Fable 5에서는 캐시 혜택을 받을 수 있습니다. 코드 변경 없이 자동으로 적용됩니다.

단, Amazon Bedrock에서는 Fable 5도 최솟값이 1,024 토큰으로 유지됩니다.

## 멀티턴 대화에서 사고 블록 처리

Fable 5를 이어지는 대화에서 쓸 때 주의할 점입니다. 사고 블록은 생성한 모델에 묶여 있습니다. 대화 이력을 다른 모델로 넘길 때는 `thinking`과 `redacted_thinking` 블록을 제거해야 합니다.

```python
# 대화 이력을 다른 모델로 전달할 때
messages = [
    msg for msg in conversation_history
    if not any(
        block.get("type") in ("thinking", "redacted_thinking")
        for block in (msg.get("content") if isinstance(msg.get("content"), list) else [])
    )
]
```

같은 Fable 5 세션 안에서 이어지는 대화라면 사고 블록을 그대로 넘겨야 합니다. 제거하면 모델이 이전 추론을 참조할 수 없게 됩니다.

## Claude Code 설정

[[Claude Code]]를 CLI나 IDE 확장으로 쓰고 있다면 바꿔야 할 것들이 있습니다.

**기본 모델 변경.** Claude Code는 세션마다 사용할 모델을 설정할 수 있습니다.

```bash
# 전역 기본 모델 변경
claude config set model claude-fable-5

# 현재 세션에서만
claude --model claude-fable-5
```

프로젝트 단위로 고정하려면 `.claude/settings.json`에 모델을 명시합니다.

```json
{
  "model": "claude-fable-5"
}
```

**환경 변수.** CI/CD 파이프라인이나 스크립트에서 `ANTHROPIC_MODEL` 환경 변수로 모델을 지정했다면 그 값도 바꿔야 합니다.

```bash
export ANTHROPIC_MODEL=claude-fable-5
```

**CLAUDE.md.** 프로젝트의 `CLAUDE.md`나 팀 공유 설정에 모델 이름이 하드코딩돼 있는 경우도 있습니다. 그립으로 찾아봅니다.

```bash
grep -r "opus-4-8" .claude/ CLAUDE.md 2>/dev/null
```

**자동 마이그레이션 명령.** Claude Code 안에서 직접 실행할 수 있는 명령이 있습니다.

```text
/claude-api migrate this project to claude-fable-5
```

모델 ID 교체, 파라미터 변경, 플랫폼별 ID 포맷 처리까지 묶어서 처리하고 수동 확인이 필요한 항목을 체크리스트로 뽑아줍니다. 모델 ID만 바꾸는 게 아니라 위에서 다룬 `thinking`, `stop_reason` 관련 코드 변경까지 한 번에 제안합니다.

**토큰 사용량 모니터링.** 적응형 사고가 항상 켜지므로 Claude Code 세션에서 소비하는 토큰이 늘어납니다. 특히 긴 코드베이스를 다루는 세션이라면 `claude usage` 명령으로 주기적으로 확인하는 습관이 필요합니다.

**코드베이스 내용과 30일 보관.** Claude Code로 코드베이스를 탐색하거나 파일을 읽어 컨텍스트에 넣으면 그 내용도 Fable 5 트래픽의 일부가 됩니다. 사내 미공개 코드나 고객 데이터가 포함된 작업을 Fable 5로 돌릴 때는 조직의 데이터 보관 정책과 맞는지 확인이 필요합니다.

## CLAUDE.md와 스킬 마이그레이션

모델 ID와 API 파라미터만 바꾸면 끝이 아닙니다. Fable 5는 적응형 사고가 항상 켜지기 때문에, Opus 4.8을 기준으로 작성된 지침 파일과 스킬이 의도와 다르게 작동하는 경우가 생깁니다.

**CoT 유도 지시 제거.** "단계별로 생각하세요", "차분히 검토한 뒤 답하세요", "Let's think step by step" 같은 사고 유도 문장이 CLAUDE.md나 SKILL.md에 있다면 제거해도 됩니다. Fable 5는 이미 적응형 사고로 알아서 합니다. 중복 지시가 오히려 사고 흐름을 방해할 수 있습니다.

**검증 지시 단순화.** Opus 4.8 시절에 "출력하기 전에 다음 항목을 하나씩 확인하세요 — 1. ..., 2. ..., 3. ..."처럼 체크리스트를 명시하던 패턴이 있었다면, Fable 5에서는 "결과를 배포 전에 검증하세요" 수준으로 줄여도 충분한 경우가 많습니다. 모델이 스스로 검증 항목을 도출합니다.

**지시 밀도 조정.** Opus 4.8 기준으로 쓴 CLAUDE.md는 예외 상황을 일일이 나열하는 경향이 있습니다. "A면 B하고, C면 D하되, E일 때는 F하세요" 같은 규칙 목록입니다. Fable 5는 원칙과 의도를 이해하고 스스로 적용하는 능력이 더 높습니다. 규칙보다 원칙을 쓰는 방향으로 리팩토링할 수 있습니다. 다만 이 작업은 Fable 5로 전환한 뒤 실제로 지침이 의도대로 작동하는지 테스트하면서 점진적으로 하는 게 안전합니다.

**스킬의 거부 처리.** 루프를 돌거나 반복 호출하는 스킬은 `stop_reason == "refusal"` 케이스를 명시적으로 처리해야 합니다. 처리하지 않으면 거부 응답이 빈 텍스트로 보이고, 루프가 조용히 잘못된 상태로 진행됩니다. SKILL.md 안에 "거부 응답이 왔을 때는 작업을 중단하고 사용자에게 알리세요"처럼 명시하거나, 스킬이 호출하는 코드에 핸들링을 추가합니다.

**안전 분류기를 유발할 수 있는 지시 검토.** 사이버보안 연구, 생물학/화학 실험 데이터, 다른 모델의 출력을 수집하거나 분석하는 워크로드가 있다면 해당 스킬이나 CLAUDE.md 지시문을 검토합니다. 분류기가 지시문의 의도를 오해하는 경우가 있습니다. 재표현하거나 목적을 명확히 적어두면 트리거 빈도를 줄일 수 있습니다.

**effort 설정 재검토.** 스킬 코드나 지침에 `effort: "xhigh"`가 하드코딩된 부분이 있다면 검토합니다. Fable 5에서 대부분의 작업은 `high`로 충분하고, `xhigh`는 비용이 더 높습니다.
## 언제 Opus 4.8을 유지하는 게 나을까

Fable 5가 무조건 낫지는 않습니다.

가격이 두 배인 만큼, 성능 향상이 실제 작업에서 체감되는지를 먼저 측정해야 합니다. 간단한 분류, 요약, 짧은 응답 생성 같은 워크로드는 Opus 4.8로도 충분할 수 있습니다. 비용 대비 효과는 워크로드마다 다릅니다.

30일 트래픽 보관이 컴플라이언스 문제가 되는 조직은 Fable 5를 쓸 수 없습니다. 이 경우 Opus 4.8을 유지해야 합니다.

반대로 Fable 5가 확실히 유리한 경우는 며칠 단위로 실행되는 긴 에이전트 작업, 복잡한 코드 작업, 과학 데이터 분석처럼 깊은 추론이 필요한 작업입니다. 이 경우에는 가격 차이를 정당화할 수 있습니다.
