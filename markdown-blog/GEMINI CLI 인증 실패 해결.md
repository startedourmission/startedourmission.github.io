---
date: 2025-08-14
tags:
  - 잡담
aliases:
description: macOS에서 Gemini CLI 로그인 시 'Precondition check failed' 오류가 발생하는 문제 해결 과정을 공유합니다. 원인으로 GOOGLE_CLOUD_PROJECT 환경 변수 충돌을 지목하고, '고스트 변수' 현상에 대응하기 위한 unset 사용법 등 단계별 해결 방법을 안내합니다.
image: "![[1-algorithm.png]]"
---
# 문제 발생

Gemini CLI 공식 깃허브에 이슈가 올라왔습니다. 
- https://github.com/google-gemini/gemini-cli/issues/5331

요지는, **macOS 15.6에서 Workspace 계정**으로 Gemini CLI에 로그인을 시도할 때 다음과 같은 오류가 발생한다는 것입니다. macOS 15.5에서는 정상 작동했다는 단서도 주어졌습니다.

```
Failed to login. Message: Precondition check failed.
```

제가 Gemini CLI를 실행하려고 했을 때도 같은 문제가 발생했습니다. 그런데 저는 macOS 15.5이고, Workspace 계정과 일반 계정 둘 다 같은 문제가 발생했습니다. 

**운영체제도, Workspace 계정 문제도 아니라는겁니다.** 

잘 사용하던 Gemini CLI에서 이런 일이 발생하니 참 머리가 아팠는데요, 저는 잘못한 것도 없는데 말이죠.
# 해결

이 오류의 근본 원인은 `GOOGLE_CLOUD_PROJECT` 환경 변수입니다. 기존에 설정된 Google Cloud 프로젝트 변수가 Gemini CLI의 인증 과정을 방해했답니다. 

저는 Gemini CLI가 제공하는 여러 개의 인증 방식을 모두 시험해보기 위해 환경 변수를 추가하고서는, 지우지 않았습니다. 이것이 문제였습니다. 

개발자들에게는 이런 환경 변수 충돌 문제가 낯설지 않을 것입니다. 하지만 이번 경우는 조금 특별합니다. 단순히 변수를 주석 처리하는 것만으로는 해결되지 않는 "고스트 변수" 현상이 발생하기 때문입니다.

## 단계별 해결 방법

### 1단계: 현재 상태 진단

먼저 터미널에서 다음 명령을 실행하여 문제의 원인인 환경 변수가 실제로 존재하는지 확인합니다.

```bash
echo $GOOGLE_CLOUD_PROJECT
```

이 명령이 `gen-lang-client-xxxxxx`와 같은 값을 출력한다면, 바로 이것이 문제의 원인입니다. 값이 비어 있다면 다른 원인을 찾아봐야 합니다.

### 2단계: 표준 해결 방법 시도

환경 변수는 대부분 셸의 시작 파일에 설정되어 있습니다. 사용하는 셸에 따라 다음 파일을 확인해보세요.

- **Bash 사용자**: `~/.bashrc`
- **Zsh 사용자**: `~/.zshrc`

해당 파일에서 `GOOGLE_CLOUD_PROJECT` 관련 설정을 찾아 주석 처리합니다.

```bash
# 이렇게 변경
#export GOOGLE_CLOUD_PROJECT="some-project-name"
```

변경 후 파일을 다시 로드합니다.

```bash
# Bash의 경우
source ~/.bashrc

# Zsh의 경우
source ~/.zshrc
```

### 3단계: 핵심 검증 단계

이 단계가 가장 중요합니다. 변수가 정말로 제거되었는지 다시 한 번 확인해야 합니다.

```bash
echo $GOOGLE_CLOUD_PROJECT
```

**결과에 따른 분기점:**

- **비어 있다면**: 표준 해결 방법이 성공했습니다. 이제 `gemini auth login`을 시도해보세요.
- **여전히 값이 표시된다면**: "고스트 변수" 상황입니다. 최종 해결 방법으로 진행해야 합니다.

### 4단계: 최종 해결 방법 (고스트 변수 대응)

변수가 사라지지 않더라도 당황하지 마세요. 이는 상위 시스템 프로세스에서 설정된 변수가 지속적으로 로드되고 있기 때문입니다. 이런 경우에는 `unset` 명령을 사용하여 강제로 제거할 수 있습니다.

셸 시작 파일에 unset 명령을 추가합니다.

```bash
# Bash 사용자
echo 'unset GOOGLE_CLOUD_PROJECT' >> ~/.bashrc

# Zsh 사용자
echo 'unset GOOGLE_CLOUD_PROJECT' >> ~/.zshrc
```

마지막으로 파일을 다시 로드합니다.

```bash
source ~/.bashrc  # 또는 source ~/.zshrc
```

## 해결 완료

저는 4단계까지 진행한 뒤에야  Gemini CLI에 정상적으로 로그인할 수 있었습니다. 아무래도 환경 문제는 언제 만나도 지긋지긋합니다. 
이슈에 명확한 해결 방법을 달아준 ZhongKuang에게 감사합니다. 
