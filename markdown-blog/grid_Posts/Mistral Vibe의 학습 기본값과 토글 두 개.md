---
date: 2026-09-03
ready: false
tags:
  - 정보
  - LLM
  - SaaS
description: "Mistral이 Vibe 일반 사용자를 학습 기본 대상으로 두고 있습니다. 정작 덜 알려진 건 옵트아웃 토글이 Vibe와 API로 따로 있다는 점입니다."
image: "![[Mistral Vibe의 학습 기본값과 토글 두 개-thumb.png]]"
---

[[Mistral]]의 헬프센터 문서가 9월 2일 갱신되면서 한 줄이 확인됐습니다. Vibe 일반 사용자는 학습에서 **기본으로 제외되지 않습니다.** 끄려면 직접 꺼야 합니다. Enterprise 고객은 반대로 기본 제외입니다.

Hacker News에서 289포인트에 댓글 126개가 붙었는데, 논점은 "학습에 쓴다"는 사실 자체가 아니었습니다. 자기가 옵트인 상태인 줄 몰랐다는 보고가 이어졌습니다. 그 착각이 어디서 생기는지가 이 건의 실질입니다.

## 무엇이 켜져 있나

공식 문서 기준으로 정리하면 이렇습니다.

| 경로 | 학습 기본값 | 끄는 방법 |
|---|---|---|
| Vibe (일반) | 켜짐 | Admin 패널 → Manage → Vibe → "Allow your interactions to be used to train our models" 끄기 |
| Vibe (모바일) | 켜짐 | 설정 → Data & Account Controls → "Enable data sharing" 해제 |
| Vibe (Enterprise) | 꺼짐 | 해당 없음 |
| Mistral Studio · API | 선택 가능 | Admin 패널 → Privacy → "Anonymous improvement data" 끄기 |

API 쪽 보존 정책도 균일하지 않습니다. 기본은 남용 모니터링용 30일 창인데, Agents API는 계정 해지 시점까지, Fine-Tuning API는 삭제하거나 계정을 해지할 때까지 데이터를 보관합니다. Scale 플랜에서는 상태 없는 호출에 한해 Zero Data Retention을 쓸 수 있습니다.

## 토글 두 개

여기가 보도에서 거의 다뤄지지 않은 대목입니다. 공식 문서는 **Vibe 옵트아웃 토글과 API 옵트아웃 토글이 별개**라고 명시합니다. 한쪽을 껐다고 다른 쪽이 꺼지지 않습니다.

실무에서 이게 왜 문제가 되는지는 금방 보입니다. 개발자가 API 키를 발급받으면서 Privacy 메뉴에서 익명 개선 데이터를 껐다고 합시다. 같은 계정으로 Vibe 웹에서 사내 문서를 붙여 넣고 요약을 시켰다면, 그건 여전히 켜져 있습니다. 반대도 마찬가지입니다. 앱에서 데이터 공유를 껐다고 파이프라인에서 도는 API 호출까지 빠지지 않습니다.

"프라이버시 설정을 껐다"는 기억이 계정 단위로 남는데 실제 적용은 제품 단위로 갈리는 구조입니다. HN에서 나온 "나는 껐는데 왜 켜져 있느냐"는 반응 상당수가 이 지점에 걸린 것으로 보입니다.

## 면제의 조건

"프라이버시가 유료 기능이 됐다"는 식의 요약을 자주 봅니다. 여러 회사를 겹쳐 보면 조금 다릅니다.

| 회사 | 소비자 기본값 | 학습에서 빠지는 조건 |
|---|---|---|
| [[OpenAI]] | 학습함 | Business·Enterprise·API (계약으로 제외) |
| [[Google]] | Keep Activity 켜져 있으면 학습함 | Workspace Business·Enterprise·Education (계약으로 제외) |
| [[Anthropic]] | 가입 시 학습 선호를 직접 선택 | 상용 API·Enterprise 플랜 |
| Mistral | Vibe 일반은 학습함 | Enterprise, 유료 API |

면제가 붙는 자리가 전부 같습니다. **돈을 냈는지가 아니라 법인 계약인지**입니다. 개인이 소비자 구독료를 더 낸다고 기본값이 뒤집히지 않습니다. 뒤집히는 건 조직 관리자가 관리 콘솔을 쥐고 계약서에 서명했을 때입니다.

이 구분이 실용적으로 중요한 이유가 있습니다. 프리랜서나 1인 사업자가 유료 요금제를 쓰면서 "돈 냈으니 안 쓰겠지"라고 넘어가는 경우가 흔한데, 위 표에서 그 가정이 성립하는 칸은 없습니다. 개인 유료 사용자는 여전히 직접 꺼야 하는 쪽에 있습니다.

## 이름이 바뀐 자리

착각이 생기는 두 번째 경로는 제품명입니다. Mistral은 2026년 5월 28일에 Le Chat과 코딩 에이전트를 합쳐 Vibe로 개편했습니다. 대화 기록과 설정, 요금제는 그대로 넘어왔습니다.

문제는 이걸 설명하는 문서들의 시차입니다. Mistral 공식 헬프센터는 Vibe로 갱신됐지만, 프라이버시 비교를 정리해 둔 3자 페이지들은 여전히 Le Chat 기준으로 티어를 서술합니다. 자기 계정 상태를 확인하려고 이런 가이드를 찾아본 사용자는 자기 화면에 없는 메뉴 이름을 보게 됩니다.

정책 변경 자체보다 이런 종류의 어긋남이 실제 오해를 더 많이 만듭니다. 사용자는 보통 공식 약관을 읽지 않고 요약 페이지를 읽습니다.

## 유럽 회사라는 것

GDPR은 동의가 자유롭게 주어지고 구체적이며 명확해야 한다고 요구합니다. 사전에 체크된 상자나 기본 켜짐 설정은 유효한 동의로 보지 않는다는 것이 유럽 데이터보호위원회의 오래된 입장입니다.

Mistral은 프랑스 회사이고, 미국 프런티어 랩 대비 강조해 온 차별점 중 하나가 유럽 데이터 규범 친화성이었습니다. 그 회사가 소비자 제품에서 기본 켜짐 + 수동 옵트아웃 구조를 쓰고, 그 옵트아웃마저 제품별로 쪼개 두었습니다.

이게 곧바로 위반이라는 뜻은 아닙니다. 학습 이용의 법적 근거를 동의가 아니라 정당한 이익(legitimate interest)으로 잡았다면 다른 판단이 가능하고, 실제로 여러 회사가 그 경로를 씁니다. 다만 그 경우에도 사용자가 반대할 권리를 쉽게 행사할 수 있어야 한다는 요건이 남습니다. 토글이 두 개로 갈려 있는 구조가 그 "쉽게"에 부합하는지는 다투어질 만합니다.

정리하면, 이번 건에서 새로운 건 정책이 아니라 정책을 확인하기 어렵게 만드는 표면입니다. 토글이 두 개고, 제품 이름이 바뀌었고, 참고할 만한 3자 문서는 옛 이름으로 쓰여 있습니다. 지금 Mistral을 쓰고 계신다면 Vibe 쪽과 Studio·API 쪽을 각각 열어 확인하시는 편이 낫습니다. 한 번 껐다는 기억은 근거가 되지 못합니다.

---

참고:
- [Can I opt out of my input or output data being used for training? (Mistral 헬프센터)](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training)
- [Mistral now trains on user input by default, except on enterprise tier (Hacker News, 289pt/126댓글)](https://news.ycombinator.com/item?id=49535284)
- [Mistral La Plateforme Data Retention Policy 2026 (Meetily)](https://meetily.ai/llm-privacy/mistral)
- [Which AI Companies Train on Your Conversations? (Venice)](https://venice.ai/blog/which-ai-companies-train-on-your-conversations)
- [Mistral's chatbot is now called "Vibe" and gains new capabilities (heise online)](https://www.heise.de/en/news/Mistral-s-chatbot-is-now-called-Vibe-and-gains-new-capabilities-11311685.html)
