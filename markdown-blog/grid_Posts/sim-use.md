---
date: 2026-07-10
tags:
  - 정보
  - 오픈소스
  - 도구
  - 에이전트
description: "sim-use가 iOS 시뮬레이터와 Android 에뮬레이터의 접근성 트리를 에이전트용 화면 표현으로 바꾸고, 관찰·조작·검증 루프를 하나의 CLI로 묶는 방식을 정리합니다."
image: "![[sim-use.png]]"
---

> 이 글은 [LY Corporation의 sim-use 공식 README](https://github.com/lycorp-jp/sim-use)를 참고하여 작성했습니다.

모바일 앱을 만드는 코딩 에이전트는 소스 코드를 수정하고 빌드할 수 있어도, 결과 화면을 직접 확인하는 단계에서 자주 멈춥니다. `sim-use`는 iOS Simulator와 Android 에뮬레이터 또는 기기의 화면을 읽고 조작하는 과정을 하나의 CLI로 제공합니다.

핵심은 스크린샷을 매번 모델에 보내는 대신 접근성 트리를 짧은 텍스트 윤곽으로 바꾸는 것입니다. 에이전트는 화면을 읽고, 요소 별칭으로 누르고, 다시 읽어 결과를 검증합니다.

## 관찰과 조작

기본 루프는 세 명령으로 구성됩니다.

```bash
sim-use ui
sim-use tap @9
sim-use ui
```

첫 `ui`는 앱 이름과 화면 크기, 상단·본문·하단 영역, 각 접근성 요소를 출력합니다. 각 요소에는 `@9` 같은 임시 별칭이 붙습니다. 다음 명령은 좌표를 계산하지 않고 해당 요소를 누르며, 마지막 명령은 화면이 예상대로 바뀌었는지 확인합니다.

README가 제시하는 화면 윤곽은 원시 JSON 접근성 트리보다 약 16배 작습니다. 접근성 역할과 라벨, 프레임처럼 작업에 필요한 정보만 남기므로 한 화면을 수백 토큰 안에서 다룰 수 있습니다.

## 선택자

`sim-use`는 작업 성격에 따라 네 종류의 선택자를 제공합니다.

| 선택자 | 예시 | 용도 |
| --- | --- | --- |
| 임시 별칭 | `tap @9` | 직전 `ui` 결과를 빠르게 재사용 |
| 접근성 ID | `tap "#settingsButton"` | 레이아웃 변경에도 안정적인 자동화 |
| 라벨 | `tap --label "General"` | 사람이 읽는 이름을 사용하는 흐름 |
| 좌표 | `tap --point 100,200` | 접근성 정보가 없는 요소의 최후 수단 |

`@N`은 직전 화면 스냅샷의 캐시에 의존하므로 화면이 바뀌면 다시 `ui`를 호출하는 편이 안전합니다. 반복 테스트에는 앱 코드에 안정적인 접근성 ID를 부여하고 `#<id>` 선택자를 쓰는 편이 낫습니다.

iOS에서는 명령마다 현재 회전을 보정해 접근성 좌표를 프레임버퍼 좌표로 옮깁니다. 반면 명시한 좌표는 기기의 세로 방향 원점 기준으로 해석되므로, 회전 화면에서는 접근성 기반 선택자가 더 안전합니다.

## 설치

권장 설치 방식은 Homebrew입니다.

```bash
brew tap lycorp-jp/tap
brew install lycorp-jp/tap/sim-use
```

소스 빌드는 macOS 14 이상과 최신 Xcode 도구 체인이 필요합니다. iOS 백엔드는 Meta의 `idb`에서 만든 XCFramework와 Apple Accessibility API, Simulator HID 파이프라인을 사용합니다.

```bash
git clone https://github.com/lycorp-jp/sim-use.git
cd sim-use
./scripts/build.sh dev
make build
.build/debug/sim-use --help
```

Android는 기기나 에뮬레이터에 브리지 APK를 한 번 설치해야 합니다.

```bash
sim-use android init --device emulator-5554
sim-use ui --device emulator-5554
```

기기 ID가 UUID면 iOS Simulator, `emulator-5554`나 ADB 일련번호 또는 네트워크 주소면 Android 백엔드를 선택합니다.

## 명령 표면

두 플랫폼에서 공통으로 사용할 수 있는 상위 명령은 `ui`, `tap`, `swipe`, `type`, `paste`, `button`, `gesture`, `keyboard-state`, `screenshot`, `record-video`, `app-state`입니다. 모든 명령은 `--json` 출력을 지원해 셸 스크립트나 에이전트가 성공 여부와 오류 힌트를 구조적으로 읽을 수 있습니다.

```bash
UDID="B34FF305-5EA8-412B-943F-1D0371CA17FF"

sim-use ui --json --device "$UDID"
sim-use tap "#loginButton" --wait-timeout 5 --device "$UDID"
sim-use paste '테스트 사용자' --device "$UDID"
sim-use screenshot --output ./result.png --device "$UDID"
```

일본어와 한국어처럼 HID 키 코드로 직접 입력하기 어려운 문자열은 `paste`가 유용합니다. iOS Simulator의 클립보드에 문자열을 넣고 Cmd+V를 보내므로 호스트의 입력기 조합을 우회합니다. 다만 iOS 16 이상에서는 앱 세션의 첫 붙여넣기에 사용자 허용이 필요할 수 있습니다.

## 에이전트 연결

저장소에는 AI 클라이언트가 명령 체계를 배우도록 하는 에이전트 스킬이 포함되어 있습니다.

```bash
sim-use init
sim-use init --client claude
sim-use init --print
```

에이전트에게 모바일 앱 수정 작업을 맡기면 빌드 뒤에 `ui`로 현재 화면을 읽고, 필요한 요소를 누르고, 다시 `ui` 또는 `screenshot`으로 확인하는 검증 단계를 붙일 수 있습니다. 화면 전환을 기다려야 하는 탭에는 `--wait-timeout`을 사용합니다.

iOS 전용 `batch`는 여러 동작에서 HID 세션과 접근성 스냅샷을 재사용합니다. 화면이 매 단계 바뀌면 `--ax-cache perStep`, 같은 화면 안에서 여러 요소를 다루면 기본값 `perBatch`가 맞습니다.

```bash
sim-use ios batch --device "$UDID" \
  --wait-timeout 5 \
  --ax-cache perStep \
  --step "tap --id LoginButton" \
  --step "tap --id WelcomeMessage"
```

## 구조

iOS 경로는 호스트에서 Simulator의 접근성 트리와 HID 입력을 직접 다룹니다. Android 경로는 기기 안의 AccessibilityService가 트리와 입력 주입 기능을 HTTP로 제공하고, 호스트가 `adb forward`로 연결합니다. 상위 CLI가 두 구현의 출력과 플래그를 같은 형태로 맞춥니다.

기기별 백그라운드 데몬은 초기화 비용을 여러 명령에 나눕니다. 첫 명령 뒤 관찰·조작 왕복이 공식 README 기준 약 300ms이며, 데몬은 600초 동안 사용하지 않으면 종료됩니다. 사용자가 별도 서버를 관리할 필요는 없습니다.

## 범위와 한계

`sim-use`는 Appium이나 XCUITest의 테스트 선언 언어를 대체하는 프레임워크가 아닙니다. 에이전트가 현재 화면을 관찰하고 다음 행동을 결정하는 대화형 루프에 맞춘 도구입니다. 결정적인 회귀 테스트는 안정적인 접근성 ID와 명시적 단언을 사용하는 기존 테스트 스위트가 계속 필요합니다.

접근성 정보가 부실한 커스텀 캔버스와 게임 화면은 텍스트 윤곽만으로 충분하지 않을 수 있습니다. 좌표, 스크린샷, 녹화를 함께 써야 하며, Android의 비디오 스트리밍과 iOS의 일부 저수준 키보드·배치 기능처럼 플랫폼별 차이도 남아 있습니다.

라이선스는 Apache 2.0입니다. 프로젝트는 AXe v1.6.0에서 포크한 뒤 크게 수정됐고, iOS 연결에 Meta의 `idb` 구성 요소를 사용합니다.

이 글은 [sim-use 공식 README](https://github.com/lycorp-jp/sim-use)의 명령과 아키텍처를 검증해 작성했습니다.

