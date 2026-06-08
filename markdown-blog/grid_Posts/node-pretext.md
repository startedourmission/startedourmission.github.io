---
date: 2026-04-05
tags:
  - 정보
  - 오픈소스
description: "브라우저 없이 텍스트 너비를 정확히 측정하는 Node.js 라이브러리. Excalidraw 도해 자동 생성 과정에서 탄생한 서버사이드 measureText() 구현체."
---
## 한 줄 요약

`npm install node-pretext` — 브라우저 없이 텍스트가 몇 픽셀인지 알 수 있습니다.

> GitHub: [startedourmission/node-pretext](https://github.com/startedourmission/node-pretext)
> npm: [node-pretext](https://www.npmjs.com/package/node-pretext)

---

## 시작은 삐뚤어진 글자였습니다

제프리 힌튼의 논문 24편을 블로그에 정리하는 작업을 하고 있었습니다. 글만 있으면 밋밋하니까, 각 논문의 핵심 아이디어를 한 장의 도해로 만들어서 넣고 싶었습니다. Excalidraw가 손그림 느낌이 나서 좋길래 이걸로 정했는데, 24장을 손으로 그리기는 싫었습니다. 프로그래밍으로 생성하기로 했습니다.

Excalidraw 파일은 JSON입니다. 원(노드), 선(연결), 텍스트(라벨)를 좌표로 찍어주면 됩니다. Python 스크립트로 JSON을 만들고, CLI 도구로 PNG로 변환하는 파이프라인을 짰습니다. 신경망 노드를 배치하고, 층 사이를 연결하고, 라벨을 붙이는 것까지 금방 됐습니다.

그런데 결과물을 보는 순간 한숨이 나왔습니다.

**글자가 다 삐뚤어져 있었습니다.**

"Hidden Units"라는 라벨이 노드 그룹의 중앙에 와야 하는데, 왼쪽으로 밀려 있었습니다. "[[Learning representations by back-propagating errors|Backpropagation]]" 제목은 오른쪽으로 치우쳐 있었습니다. 연결선 위의 "Forward Pass" 캡션은 화살표와 겹쳤습니다.

원인은 단순합니다. 텍스트를 중앙에 놓으려면 `x = 중심 - (글자너비 / 2)`를 계산해야 합니다. 그런데 **"Backpropagation"이 몇 픽셀인지 모릅니다.**

브라우저에서는 한 줄이면 끝나는 일입니다:

```js
ctx.font = '28px Helvetica';
ctx.measureText('Backpropagation').width;  // 210.2
```

하지만 여기는 Node.js CLI 환경입니다. 브라우저가 없습니다. `measureText()`가 없습니다.

그래서 글자 수에 비례해서 대충 너비를 추정해봤습니다. `width = text.length * fontSize * 0.6` 같은 식으로요. 당연히 안 맞습니다. 'W'와 'i'의 너비는 3배 이상 차이나는데, 같은 값으로 치면 짧은 글자는 너무 넓게, 긴 글자는 너무 좁게 잡힙니다. "Title"은 오른쪽으로 밀리고 "Backward Pass (Error Gradients)"는 왼쪽으로 밀립니다.

---

### 찾아봤는데 없더라고요

혹시 누가 이미 만들어놨을까 싶어서 npm을 뒤졌습니다. "server side text width", "node text measurement", "measure text without browser" 같은 키워드로 한참을 찾았습니다.

| 패키지 | 상태 | 문제 |
|---|---|---|
| [measure-text](https://github.com/bezoerb/measure-text) | **DEPRECATED** | 정확히 이거였는데 관리 포기 |
| [server-text-width](https://www.npmjs.com/package/server-text-width) | 살아있음 | 폰트마다 문자별 룩업 테이블을 미리 생성해야 합니다. Helvetica 쓰다가 Arial로 바꾸면 테이블을 다시 만들어야 합니다 |
| [text-metrics](https://www.npmjs.com/package/text-metrics) | 살아있음 | 브라우저 전용. DOM이 필요합니다 |
| [@chenglou/pretext](https://github.com/chenglou/pretext) | 활발함 | 서버사이드 "지원 예정"이지만 아직 구현되지 않았습니다 |

`measure-text`의 README에 "DEPRECATED"가 박혀 있는 걸 보고 좀 허탈했습니다. node-canvas를 감싸서 `measureText()`를 제공하는 패키지인데, 딱 필요한 물건이 더 이상 관리되지 않는 겁니다.

2026년인데 서버에서 텍스트 너비 하나 재는 게 이렇게 어려운 일인가 싶었습니다. 브라우저 안에서는 너무 당연해서 의식조차 못 하는 기능인데, 밖으로 한 발짝만 나오면 아무것도 없습니다.

Pillow(Python)로 대체해볼까도 생각했습니다. PIL의 `ImageFont.getbbox()`로 텍스트 크기를 잴 수 있긴 한데, Excalidraw는 Helvetica를 기본 폰트로 쓰고, Pillow의 폰트 렌더링은 Excalidraw의 렌더링과 미묘하게 다릅니다. 측정값은 나오는데 실제 렌더링 결과와 안 맞으면 의미가 없습니다.

---

### pretext에서 얻은 힌트

그러다 Cheng Lou의 [pretext](https://github.com/chenglou/pretext)를 다시 들여다봤습니다. Midjourney의 시니어 엔지니어가 만든 라이브러리인데, 브라우저에서 DOM reflow 없이 텍스트를 측정합니다. 2026년 3월에 나왔고, 꽤 주목받고 있었습니다.

핵심 원리를 알고 싶어서 `src/measurement.ts`를 열어봤습니다. 복잡한 코드가 있을 줄 알았는데, 측정의 핵심은 의외로 단순했습니다:

```js
const ctx = getMeasureContext();  // Canvas context를 가져오고
metrics = { width: ctx.measureText(seg).width };  // measureText()로 잰다
```

결국 `canvas.measureText()`입니다. DOM이 비싸니까 Canvas API로 우회해서 폰트 엔진에 직접 물어보는 거죠. pretext의 진짜 가치는 여기에 grapheme segmentation, emoji 보정, 캐싱, 멀티라인 레이아웃 같은 것들을 정교하게 쌓아올린 데 있습니다.

하지만 제가 필요한 건 그 정교한 부분이 아니라, 가장 밑바닥의 원리였습니다. "Canvas API로 폰트 엔진에 물어보면 정확한 너비를 알 수 있다"는 것.

그런데 pretext는 브라우저 안에서만 작동합니다. Canvas API가 있으니까요.

잠깐.

[node-canvas](https://github.com/Automattic/node-canvas)가 있습니다. Node.js에서 Canvas API를 네이티브로 구현한 패키지입니다. macOS에서는 Core Text, Linux에서는 FreeType을 직접 호출해서 브라우저의 Canvas와 거의 동일한 결과를 냅니다.

pretext의 원리를 node-canvas 위에서 쓰면?

```
pretext의 원리:    Canvas API → measureText() → 정확한 너비
node-canvas:       Node.js에서 Canvas API 제공
합치면:            Node.js에서 정확한 텍스트 너비 측정
```

해봤습니다:

```js
const { createCanvas } = require('canvas');
const ctx = createCanvas(1, 1).getContext('2d');

ctx.font = '28px Helvetica';
console.log(ctx.measureText('Backpropagation').width);  // 210.2
```

됩니다. 브라우저에서 재는 것과 동일한 값입니다.

---

## 사용법

이 세 줄짜리 코드에 실무에서 필요한 것들을 얹었습니다.

**캐싱.** 같은 폰트+텍스트 조합을 반복 측정하면 node-canvas를 매번 호출하는 게 낭비입니다. font → text → metrics 2단계 Map으로 캐싱합니다. 다이어그램 하나에 같은 폰트로 수십 개 라벨을 배치하는 경우, 폰트별 컨텍스트 전환이 한 번만 발생합니다.

**정렬 헬퍼.** `centerX('Title', '28px Helvetica', 200)`이 `200 - width/2`를 계산해서 왼쪽 x 좌표를 돌려줍니다. 매번 수동으로 빼기하는 건 실수를 부릅니다.

**워드랩.** `wrap(text, font, 300)`이 300px 안에 맞게 줄바꿈 위치를 계산합니다. 각 줄의 실제 너비와 전체 높이도 같이 돌려줍니다. OG 이미지에 제목을 넣을 때, 한 줄에 들어가는지 두 줄로 넘어가는지 이걸로 결정할 수 있습니다.

**배치 처리.** 여러 텍스트를 한꺼번에 측정하는 `measureBatch()`가 있고, CLI의 `--batch` 모드로 JSON 배열을 stdin으로 넘기면 한 번에 처리합니다.

**CLI.** Node.js가 아닌 환경(Python, Go, Ruby 등)에서도 subprocess로 호출할 수 있습니다. 실제로 저는 Python 스크립트에서 이렇게 씁니다:

```python
result = subprocess.run(
    ["node", "node-pretext/src/cli.js", "14px Helvetica", "Hidden Units"],
    capture_output=True, text=True
)
width = float(result.stdout.strip())  # 80.2
```

### 설치

```bash
npm install node-pretext
```

### 코드

```js
const { measure, width, centerX, wrap } = require('node-pretext');

// 너비만 알고 싶을 때
width('Hello World', '14px Helvetica');  // 72.1

// 전체 메트릭이 필요할 때
measure('Hello', '20px Arial');
// { width: 47.1, ascent: 15, descent: 4, height: 19 }

// "이 글자를 x=200에 가운데 놓으려면 왼쪽 끝을 어디에?"
centerX('Backpropagation', '28px Helvetica', 200);  // 94.9

// "이 문장을 300px 안에 넣으려면 어디서 줄바꿈?"
wrap('The quick brown fox jumps over the lazy dog', '14px Helvetica', 300);
// { lines: ['The quick brown fox jumps', 'over the lazy dog'],
//   lineWidths: [165.2, 112.8],
//   totalHeight: 35 }
```

---

## 결과물

처음에 삐뚤어진 라벨에서 시작한 일이었는데, node-pretext를 적용한 뒤로는 이렇게 나옵니다.


볼츠만 머신의 Positive/Negative Phase를 나란히 보여주는 도해입니다. Python 스크립트가 node-pretext CLI를 호출해서 "Positive Phase (Data)", "Hidden Units", "Visible Units" 등 모든 라벨의 픽셀 너비를 측정합니다. 그 값으로 `cx - width/2` 좌표를 계산해서 `.excalidraw` JSON을 생성합니다.

좌우 패널의 대칭이 맞는 이유가 여기 있습니다. "Positive Phase (Data)"와 "Negative Phase (Free)"의 글자 수가 다르지만, 각각의 실제 픽셀 너비를 알고 있으니 둘 다 패널 중앙에 정확히 놓을 수 있습니다. 글자 수로 대충 추정했다면 이 정렬은 불가능합니다.


Wake-Sleep 알고리즘 도해입니다. Wake Phase에서는 위로 올라가는 화살표(Recognition), Sleep Phase에서는 아래로 내려가는 화살표(Generation)가 네트워크 옆에 배치됩니다. "Recognition (bottom-up)" 같은 2줄짜리 라벨도 각 줄의 너비를 따로 측정해서 중앙 정렬합니다.

이런 도해를 24장 만들어야 하는데, 한 장마다 손으로 정렬하는 건 현실적이지 않습니다. node-pretext 덕분에 스크립트 한 번 돌리면 전부 정렬된 상태로 나옵니다.

---

## 다른 곳에서도 쓸 수 있습니다

만들고 보니, Excalidraw에서만 필요한 게 아니었습니다. "서버에서 텍스트가 몇 픽셀인지 모른다"는 문제는 프로그래밍으로 시각적 결과물을 만드는 모든 곳에서 발생합니다.

**OG 이미지를 자동 생성할 때.** 블로그 글을 올리면 제목으로 Open Graph 썸네일을 자동 생성하고 싶습니다. "제프리 힌튼의 역전파 논문"이라는 제목이 카드 안에 한 줄로 들어가는지, 아니면 두 줄로 넘어가는지 미리 알아야 합니다. `wrap(title, '32px Arial', 600)`이면 됩니다. 줄이 넘어가면 카드 높이를 늘리고, 안 넘어가면 그대로 쓰면 됩니다.

**카드뉴스를 찍어낼 때.** 인스타그램 카드뉴스를 프로그래밍으로 만들려면 제목 크기에 맞춰서 배경 박스를 그려야 합니다. 제목이 "AI"면 박스가 작고, "Artificial Intelligence"면 커야 합니다. 글자 수가 아니라 픽셀 너비로 계산해야 자연스럽습니다.

**PDF에서 표를 그릴 때.** 셀 안에 "2026-04-05"가 들어가는지, 아니면 잘려서 "2026-04..."이 되는지 미리 알아야 합니다. 셀 너비를 내용물에 맞춰 자동 조정하려면 각 셀 텍스트의 너비를 알아야 합니다.

**SVG 뱃지를 만들 때.** GitHub README에서 흔히 보는 `![npm](https://img.shields.io/npm/v/node-pretext)` 같은 뱃지. 텍스트 길이에 따라 배경 rect의 width가 달라져야 합니다. shields.io도 내부적으로 이 계산을 하고 있을 겁니다.

**슬라이드를 자동 생성할 때.** Marp나 reveal.js로 발표자료를 프로그래밍으로 만들 때, 제목이 슬라이드를 넘어가는지 미리 확인하려면 너비를 알아야 합니다.

전부 같은 문제입니다. "이 텍스트가 렌더링되면 몇 픽셀을 차지하는가." 브라우저 안에서는 DOM이 알아서 해주니까 아무도 신경 안 쓰는데, 서버에서 좌표를 직접 계산하는 순간 필수가 됩니다.

---

## 설계

### 한 가지만 합니다

node-pretext는 "이 텍스트, 이 폰트에서 몇 픽셀인가"라는 질문에만 답합니다. 레이아웃을 잡아주지 않습니다. 이미지를 렌더링하지 않습니다. 파일을 생성하지 않습니다.

이게 의도적인 설계입니다. 측정과 레이아웃을 같은 라이브러리에 넣으면 Excalidraw 용으로는 좋지만 PDF에서는 못 쓰고, PDF 용으로 만들면 SVG에서는 안 맞습니다. 측정만 분리해두면 어떤 출력 포맷과도 조합할 수 있습니다.

### OS 폰트 엔진을 믿습니다

자체 폰트 파서를 만들지 않았습니다. `server-text-width`처럼 문자별 룩업 테이블을 쓰지도 않습니다. node-canvas가 OS의 폰트 렌더링 엔진을 직접 호출하고, 저는 그 결과를 전달합니다.

이 방식의 장점은 정확도입니다. OS가 실제로 렌더링할 때 사용하는 것과 동일한 엔진이 측정합니다. 룩업 테이블은 커닝(글자 쌍 간격 조정)을 무시하는 경우가 많은데, `measureText()`는 커닝까지 반영합니다.

트레이드오프는 node-canvas의 네이티브 바이너리 의존성입니다. 설치할 때 C++ 빌드가 필요할 수 있습니다(대부분의 플랫폼에서는 prebuilt binary가 있어서 괜찮습니다). 순수 JS만으로는 이 정확도를 낼 수 없기 때문에 감수하는 부분입니다.

### 캐싱은 기본입니다

font → text → metrics 2단계 Map으로 캐싱합니다. 같은 폰트+텍스트 조합은 한 번만 측정합니다. 다이어그램 하나를 만들면서 "Hidden Units"를 왼쪽 패널과 오른쪽 패널에 각각 배치할 때, 두 번째는 캐시에서 바로 꺼냅니다.

---

## API

| 함수                           | 하는 일                            |
| ---------------------------- | ------------------------------- |
| `measure(text, font?)`       | 전체 메트릭 (너비, ascent, descent, 높이) |
| `width(text, font?)`         | 너비만                             |
| `measureBatch(items)`        | 여러 개 한꺼번에                       |
| `centerX(text, font, cx)`    | cx 기준 중앙 정렬 좌표                  |
| `centerY(font, cy)`          | cy 기준 중앙 정렬 좌표                  |
| `wrap(text, font, maxWidth)` | 줄바꿈 (줄별 너비, 총 높이)               |
| `clearCache()`               | 캐시 비우기                          |

font는 Canvas API 형식 그대로 씁니다: `"14px Helvetica"`, `"bold 20px Arial"`, `"italic 16px Georgia"`.

---

## 마치며

삐뚤어진 Excalidraw 라벨에서 시작해서, pretext의 소스를 뜯어보고, node-canvas와 결합하는 아이디어를 얻고, 패키지로 만들어서 npm에 올리기까지. 하루 만에 벌어진 일입니다.

4.4KB짜리 작은 패키지입니다. 하지만 "서버에서 텍스트가 몇 픽셀인지 모른다"는 건 꽤 근본적인 빈자리였고, deprecated된 `measure-text` 이후로 아무도 채우지 않고 있었습니다. 비슷한 상황에서 삽질하고 계신 분이 있다면 꺼내 써보시길 바랍니다.

```bash
npm install node-pretext
```

> GitHub: [startedourmission/node-pretext](https://github.com/startedourmission/node-pretext)
