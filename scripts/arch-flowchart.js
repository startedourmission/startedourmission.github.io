/**
 * arch-flowchart.js
 * 모델 아키텍처 인터랙티브 플로차트 렌더러
 *
 * 사용법 (마크다운 내):
 *   <div class="arch-flow" data-arch="alexnet"></div>
 *
 * 또는 인라인 정의:
 *   <div class="arch-flow" data-layers='[{"name":"Input","shape":"224×224×3","type":"input"}, ...]'></div>
 */
(function () {
  "use strict";

  /* ── 색상 팔레트 ── */
  const COLORS = {
    input:   { fill: "#e8f4fd", stroke: "#2196F3", text: "#1565C0" },
    conv:    { fill: "#fff3e0", stroke: "#FF9800", text: "#E65100" },
    pool:    { fill: "#f3e5f5", stroke: "#9C27B0", text: "#6A1B9A" },
    norm:    { fill: "#fce4ec", stroke: "#E91E63", text: "#AD1457" },
    fc:      { fill: "#e8eaf6", stroke: "#3F51B5", text: "#283593" },
    dropout: { fill: "#efebe9", stroke: "#795548", text: "#4E342E" },
    act:     { fill: "#e0f2f1", stroke: "#009688", text: "#00695C" },
    output:  { fill: "#e8f5e9", stroke: "#4CAF50", text: "#2E7D32" },
    softmax: { fill: "#e8f5e9", stroke: "#4CAF50", text: "#2E7D32" },
    embed:   { fill: "#fff8e1", stroke: "#FFC107", text: "#F57F17" },
    attn:    { fill: "#fce4ec", stroke: "#E91E63", text: "#AD1457" },
    add:     { fill: "#f1f8e9", stroke: "#8BC34A", text: "#558B2F" },
    concat:  { fill: "#fff3e0", stroke: "#FF9800", text: "#E65100" },
    bn:      { fill: "#fce4ec", stroke: "#E91E63", text: "#AD1457" },
    flatten: { fill: "#eceff1", stroke: "#607D8B", text: "#37474F" },
    default: { fill: "#f5f5f5", stroke: "#9E9E9E", text: "#424242" },
  };

  /* ── 레이아웃 상수 ── */
  const BOX_W = 200;
  const BOX_H = 52;
  const GAP_Y = 18;
  const PAD_X = 40;
  const PAD_Y = 30;
  const ARROW_LEN = GAP_Y;
  const RADIUS = 8;

  /* ── 사전 정의 아키텍처 ── */
  const PRESETS = {};

  PRESETS.alexnet = {
    title: "AlexNet (2012)",
    layers: [
      { name: "Input Image",       shape: "227×227×3",     type: "input" },
      { name: "Conv1",             shape: "55×55×96",      type: "conv",  detail: "11×11 필터, stride 4, ReLU" },
      { name: "Max Pool 1",        shape: "27×27×96",      type: "pool",  detail: "3×3, stride 2" },
      { name: "LRN 1",             shape: "27×27×96",      type: "norm",  detail: "Local Response Normalization" },
      { name: "Conv2",             shape: "27×27×256",     type: "conv",  detail: "5×5 필터, pad 2, ReLU" },
      { name: "Max Pool 2",        shape: "13×13×256",     type: "pool",  detail: "3×3, stride 2" },
      { name: "LRN 2",             shape: "13×13×256",     type: "norm",  detail: "Local Response Normalization" },
      { name: "Conv3",             shape: "13×13×384",     type: "conv",  detail: "3×3 필터, pad 1, ReLU" },
      { name: "Conv4",             shape: "13×13×384",     type: "conv",  detail: "3×3 필터, pad 1, ReLU" },
      { name: "Conv5",             shape: "13×13×256",     type: "conv",  detail: "3×3 필터, pad 1, ReLU" },
      { name: "Max Pool 3",        shape: "6×6×256",       type: "pool",  detail: "3×3, stride 2" },
      { name: "Flatten",           shape: "9216",          type: "flatten" },
      { name: "FC6 + Dropout",     shape: "4096",          type: "fc",    detail: "ReLU, Dropout 0.5" },
      { name: "FC7 + Dropout",     shape: "4096",          type: "fc",    detail: "ReLU, Dropout 0.5" },
      { name: "FC8 (Output)",      shape: "1000 classes",  type: "output", detail: "Softmax" },
    ],
  };

  PRESETS.dbn = {
    title: "Deep Belief Net (2006)",
    layers: [
      { name: "Input (Visible)",    shape: "784 (28×28)",  type: "input" },
      { name: "RBM 1 → Hidden 1",  shape: "500 units",    type: "fc",    detail: "비지도 사전훈련: CD-1" },
      { name: "RBM 2 → Hidden 2",  shape: "500 units",    type: "fc",    detail: "비지도 사전훈련: CD-1" },
      { name: "RBM 3 → Hidden 3",  shape: "2000 units",   type: "fc",    detail: "비지도 사전훈련: CD-1" },
      { name: "Fine-tuning",       shape: "전체 가중치",    type: "act",   detail: "Wake-sleep 변형으로 미세조정" },
      { name: "Output (Label)",    shape: "10 classes",   type: "output", detail: "1.25% 에러율 (MNIST)" },
    ],
  };

  PRESETS.boltzmann = {
    title: "Boltzmann Machine (1985)",
    layers: [
      { name: "Visible Units",     shape: "입력 데이터",    type: "input",  detail: "관측 가능한 노드" },
      { name: "Hidden Units",      shape: "잠재 표현",     type: "fc",     detail: "관측 불가, 내부 표현 학습" },
      { name: "Energy Function",   shape: "E(v,h)",       type: "act",    detail: "-Σ wᵢⱼvᵢhⱼ - Σ bᵢvᵢ - Σ cⱼhⱼ" },
      { name: "Gibbs Sampling",    shape: "확률 샘플링",    type: "norm",   detail: "시뮬레이티드 어닐링으로 평형 도달" },
      { name: "Weight Update",     shape: "Δw = ε(⟨vᵢhⱼ⟩data - ⟨vᵢhⱼ⟩model)", type: "default", detail: "양의 위상 - 음의 위상" },
    ],
  };

  PRESETS.autoencoder = {
    title: "Autoencoder — Reducing Dimensionality (2006)",
    layers: [
      { name: "Input",             shape: "784 (28×28)",  type: "input" },
      { name: "Encoder Layer 1",   shape: "1000 units",   type: "conv",   detail: "RBM 사전훈련" },
      { name: "Encoder Layer 2",   shape: "500 units",    type: "conv",   detail: "RBM 사전훈련" },
      { name: "Encoder Layer 3",   shape: "250 units",    type: "conv",   detail: "RBM 사전훈련" },
      { name: "Bottleneck (Code)", shape: "30 units",     type: "embed",  detail: "2차원 → 이 코드로 시각화" },
      { name: "Decoder Layer 1",   shape: "250 units",    type: "fc" },
      { name: "Decoder Layer 2",   shape: "500 units",    type: "fc" },
      { name: "Decoder Layer 3",   shape: "1000 units",   type: "fc" },
      { name: "Reconstruction",    shape: "784 (28×28)",  type: "output", detail: "입력 복원" },
    ],
  };

  PRESETS.capsule = {
    title: "Capsule Network — Dynamic Routing (2017)",
    layers: [
      { name: "Input Image",       shape: "28×28×1",      type: "input" },
      { name: "Conv1",             shape: "20×20×256",    type: "conv",   detail: "9×9, stride 1, ReLU" },
      { name: "PrimaryCaps",       shape: "6×6×32×8",     type: "conv",   detail: "9×9, stride 2 → 32채널, 8D 캡슐" },
      { name: "Dynamic Routing",   shape: "라우팅 반복 3회", type: "attn",   detail: "coupling coefficients cᵢⱼ 업데이트" },
      { name: "DigitCaps",         shape: "10×16",        type: "fc",     detail: "10개 클래스, 16D 캡슐" },
      { name: "Length → Class",    shape: "10 classes",   type: "output", detail: "캡슐 벡터 길이 = 존재 확률" },
    ],
  };

  PRESETS.distillation = {
    title: "Knowledge Distillation (2015)",
    layers: [
      { name: "Input",             shape: "학습 데이터",    type: "input" },
      { name: "Teacher Network",   shape: "대형 모델/앙상블", type: "fc",   detail: "높은 정확도, 높은 비용" },
      { name: "Soft Targets (T)",  shape: "softmax(z/T)", type: "act",    detail: "temperature T로 소프트닝" },
      { name: "Student Network",   shape: "소형 모델",     type: "conv",   detail: "경량화된 네트워크" },
      { name: "Loss = αLhard + βLsoft", shape: "혼합 손실", type: "norm",  detail: "hard label + soft target 결합" },
      { name: "Distilled Model",   shape: "압축된 지식",    type: "output", detail: "teacher에 근접한 성능" },
    ],
  };

  PRESETS.dropout = {
    title: "Dropout (2014)",
    layers: [
      { name: "Input",             shape: "입력 벡터",     type: "input" },
      { name: "Hidden Layer 1",    shape: "N units",      type: "fc",     detail: "훈련: p=0.5로 랜덤 비활성화" },
      { name: "Dropout Mask 1",    shape: "Bernoulli(p)",  type: "dropout", detail: "매 미니배치마다 새 마스크" },
      { name: "Hidden Layer 2",    shape: "N units",      type: "fc",     detail: "훈련: p=0.5로 랜덤 비활성화" },
      { name: "Dropout Mask 2",    shape: "Bernoulli(p)",  type: "dropout", detail: "매 미니배치마다 새 마스크" },
      { name: "Output",            shape: "추론 시: 가중치×p", type: "output", detail: "앙상블 평균 근사" },
    ],
  };

  PRESETS.helmholtz = {
    title: "Helmholtz Machine (1995)",
    layers: [
      { name: "Input (Data)",       shape: "관측 데이터",   type: "input" },
      { name: "Recognition ↑",     shape: "상향 가중치",    type: "conv",   detail: "데이터 → 잠재 표현 추론" },
      { name: "Top-Level Latent",   shape: "잠재 변수",     type: "embed",  detail: "사전 분포에서 샘플링" },
      { name: "Generative ↓",      shape: "하향 가중치",    type: "fc",     detail: "잠재 표현 → 데이터 생성" },
      { name: "Wake-Sleep Learning", shape: "두 위상 교대", type: "act",    detail: "Wake: 생성 학습 / Sleep: 인식 학습" },
      { name: "Reconstruction",     shape: "생성된 데이터",  type: "output" },
    ],
  };

  PRESETS.wakesleep = {
    title: "Wake-Sleep Algorithm (1995)",
    layers: [
      { name: "Sensory Input",      shape: "관측 데이터",   type: "input" },
      { name: "Recognition (↑)",    shape: "상향 추론",     type: "conv",   detail: "Wake: 데이터로 잠재 변수 추론" },
      { name: "Latent Variables",   shape: "내부 표현",     type: "embed" },
      { name: "Generative (↓)",     shape: "하향 생성",     type: "fc",     detail: "Sleep: 잠재 변수에서 데이터 생성" },
      { name: "Wake Phase",         shape: "생성 가중치 학습", type: "act",  detail: "실제 데이터 → 생성 가중치 조정" },
      { name: "Sleep Phase",        shape: "인식 가중치 학습", type: "norm", detail: "환각 데이터 → 인식 가중치 조정" },
    ],
  };

  PRESETS.forwardforward = {
    title: "Forward-Forward Algorithm (2022)",
    layers: [
      { name: "Positive Data",     shape: "실제 데이터 + 정답 레이블", type: "input", detail: "goodness ↑" },
      { name: "Layer 1 (FF)",      shape: "활성값 제곱합",  type: "fc",     detail: "목표: 양성 → 임계값 초과" },
      { name: "Layer 2 (FF)",      shape: "활성값 제곱합",  type: "fc",     detail: "목표: 양성 → 임계값 초과" },
      { name: "Negative Data",     shape: "잘못된 레이블 부착", type: "norm", detail: "goodness ↓" },
      { name: "Layer 1 (FF)",      shape: "활성값 제곱합",  type: "fc",     detail: "목표: 음성 → 임계값 미달" },
      { name: "Goodness Threshold", shape: "Σ(aᵢ²) vs θ", type: "act",   detail: "역전파 없이 층별 독립 학습" },
      { name: "Prediction",        shape: "가장 높은 goodness 클래스", type: "output" },
    ],
  };

  PRESETS.simclr = {
    title: "SimCLR — Contrastive Learning (2020)",
    layers: [
      { name: "Input Image x",     shape: "원본 이미지",    type: "input" },
      { name: "Augmentation",      shape: "x̃ᵢ, x̃ⱼ",      type: "act",    detail: "랜덤 crop, 색상 변환, blur" },
      { name: "Encoder f(·)",      shape: "ResNet-50",    type: "conv",   detail: "표현 hᵢ = f(x̃ᵢ)" },
      { name: "Projection g(·)",   shape: "128-dim",      type: "fc",     detail: "zᵢ = g(hᵢ), MLP" },
      { name: "NT-Xent Loss",      shape: "대조 손실",     type: "norm",   detail: "같은 이미지 쌍 ↑, 다른 쌍 ↓" },
      { name: "Learned Repr.",     shape: "2048-dim",     type: "output", detail: "프로젝션 헤드 버리고 h 사용" },
    ],
  };

  PRESETS.byol = {
    title: "BYOL — Bootstrap Your Own Latent (2020)",
    layers: [
      { name: "Input Image",       shape: "원본 이미지",    type: "input" },
      { name: "Online Encoder",    shape: "f_θ → h",      type: "conv",   detail: "학습되는 인코더" },
      { name: "Online Projector",  shape: "g_θ → z",      type: "fc",     detail: "프로젝션" },
      { name: "Predictor",         shape: "q_θ(z)",       type: "attn",   detail: "target 예측 — 비대칭 핵심" },
      { name: "Target Encoder",    shape: "f_ξ (EMA)",    type: "conv",   detail: "θ의 지수이동평균, 학습 안 함" },
      { name: "Stop-Gradient",     shape: "sg(z')",       type: "norm",   detail: "target 쪽 그래디언트 차단" },
      { name: "Loss: MSE(q, sg(z'))", shape: "예측 ↔ target", type: "output", detail: "음성 쌍 없이 학습" },
    ],
  };

  PRESETS.layernorm = {
    title: "Layer Normalization (2016)",
    layers: [
      { name: "Input Activation",   shape: "H-dim vector", type: "input" },
      { name: "Compute μ, σ",      shape: "μ = 1/H Σaᵢ",  type: "act",   detail: "한 층의 모든 뉴런에서 통계량 계산" },
      { name: "Normalize",          shape: "(a - μ) / σ",  type: "norm",  detail: "배치 크기에 무관, RNN에 적합" },
      { name: "Scale & Shift",      shape: "γ·â + β",     type: "fc",    detail: "학습 가능한 파라미터 γ, β" },
      { name: "Output",             shape: "정규화된 활성값", type: "output" },
    ],
  };

  PRESETS.rbm_relu = {
    title: "ReLU Improves RBM (2010)",
    layers: [
      { name: "Visible (Input)",    shape: "실수값 입력",   type: "input" },
      { name: "Traditional RBM",    shape: "sigmoid 활성화", type: "fc",   detail: "기존: σ(Wx + b)" },
      { name: "NReLU Unit",         shape: "max(0, x + N(0,σ))", type: "act", detail: "노이즈 ReLU: 무한 이진 유닛 근사" },
      { name: "Contrastive Div.",   shape: "CD-1 학습",    type: "norm",   detail: "ReLU로 수렴 속도 개선" },
      { name: "Learned Features",   shape: "개선된 표현",   type: "output", detail: "CIFAR-10/NORB에서 성능 향상" },
    ],
  };

  PRESETS.contrastive_divergence = {
    title: "Contrastive Divergence (2002)",
    layers: [
      { name: "Training Data v⁰",  shape: "관측 데이터",   type: "input" },
      { name: "Positive Phase",     shape: "⟨vᵢhⱼ⟩data",  type: "fc",    detail: "v⁰에서 h⁰ 샘플링" },
      { name: "Reconstruction",     shape: "v¹ ← h⁰",     type: "act",   detail: "한 번의 깁스 샘플링" },
      { name: "Negative Phase",     shape: "⟨vᵢhⱼ⟩recon", type: "norm",  detail: "v¹에서 h¹ 샘플링" },
      { name: "Weight Update",      shape: "Δw ∝ ⟨vh⟩⁰ - ⟨vh⟩¹", type: "default", detail: "CD-1: 한 스텝만으로 근사" },
      { name: "Trained RBM",        shape: "학습된 가중치",  type: "output" },
    ],
  };

  PRESETS.tsne = {
    title: "t-SNE (2008)",
    layers: [
      { name: "High-D Data",       shape: "n×D",          type: "input",  detail: "고차원 데이터 포인트들" },
      { name: "Pairwise Affinity",  shape: "pⱼ|ᵢ (가우시안)", type: "fc",  detail: "고차원에서 유사도 계산" },
      { name: "Symmetrize",         shape: "pᵢⱼ = (pⱼ|ᵢ+pᵢ|ⱼ)/2n", type: "act" },
      { name: "Low-D Embedding",    shape: "n×2 or n×3",  type: "embed",  detail: "랜덤 초기화" },
      { name: "Student-t Affinity",  shape: "qᵢⱼ (t분포, df=1)", type: "norm", detail: "저차원에서 유사도: 긴 꼬리" },
      { name: "Minimize KL(P‖Q)",   shape: "경사하강법",    type: "default", detail: "Crowding 문제 해결" },
      { name: "2D/3D Visualization", shape: "시각화 결과",  type: "output" },
    ],
  };

  PRESETS.transformer_ae = {
    title: "Transforming Auto-encoders (2011)",
    layers: [
      { name: "Input Image",        shape: "이미지 패치",   type: "input" },
      { name: "Capsule: Recognition", shape: "pᵢ = σ(Wᵢx)", type: "conv", detail: "각 캡슐이 독립적으로 인식" },
      { name: "Pose Prediction",     shape: "Tᵢ(Δ)",       type: "attn",  detail: "변환 행렬 적용 (이동/회전)" },
      { name: "Capsule: Generation", shape: "yᵢ = pᵢ · g(Tᵢ)", type: "fc", detail: "변환된 포즈로 출력 생성" },
      { name: "Sum Outputs",         shape: "Σ yᵢ",        type: "add",   detail: "모든 캡슐 출력 합산" },
      { name: "Reconstruction",      shape: "변환된 이미지", type: "output", detail: "입력의 변환 버전 복원" },
    ],
  };

  /* ── SVG 유틸리티 ── */
  function svgEl(tag, attrs) {
    const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    return el;
  }

  function textEl(x, y, str, opts = {}) {
    const t = svgEl("text", {
      x, y,
      "text-anchor": opts.anchor || "middle",
      "font-size":   opts.size || "13",
      "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      "font-weight": opts.bold ? "600" : "400",
      fill:          opts.fill || "#333",
      "pointer-events": "none",
    });
    t.textContent = str;
    return t;
  }

  /* ── 메인 렌더러 ── */
  function renderFlowchart(container) {
    const archKey = container.dataset.arch;
    const inlineLayers = container.dataset.layers;

    let title = "";
    let layers = [];

    if (archKey && PRESETS[archKey]) {
      title = PRESETS[archKey].title;
      layers = PRESETS[archKey].layers;
    } else if (inlineLayers) {
      try {
        layers = JSON.parse(inlineLayers);
        title = container.dataset.title || "";
      } catch (e) {
        container.innerHTML = "<p style='color:red'>arch-flowchart: JSON 파싱 오류</p>";
        return;
      }
    } else {
      container.innerHTML = "<p style='color:#999'>arch-flowchart: 알 수 없는 아키텍처 '" + archKey + "'</p>";
      return;
    }

    const n = layers.length;
    const svgW = BOX_W + PAD_X * 2;
    const svgH = PAD_Y + n * (BOX_H + GAP_Y) - GAP_Y + PAD_Y + (title ? 32 : 0);
    const titleOffset = title ? 32 : 0;

    const svg = svgEl("svg", {
      width: "100%",
      viewBox: `0 0 ${svgW} ${svgH}`,
      style: "max-width:360px;display:block;margin:1.5em auto;",
    });

    /* 타이틀 */
    if (title) {
      svg.appendChild(textEl(svgW / 2, 22, title, { size: "15", bold: true, fill: "#222" }));
    }

    /* 툴팁 */
    const tooltip = document.createElement("div");
    Object.assign(tooltip.style, {
      position: "absolute", padding: "8px 14px", background: "#222", color: "#fff",
      borderRadius: "6px", fontSize: "13px", lineHeight: "1.5",
      pointerEvents: "none", opacity: "0", transition: "opacity 0.15s",
      zIndex: "9999", maxWidth: "280px", whiteSpace: "pre-wrap",
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      left: "50%", transform: "translateX(-50%)",
    });
    container.style.position = "relative";
    container.appendChild(tooltip);

    /* 다른 곳 탭하면 툴팁 닫기 (모바일) */
    document.addEventListener("click", function (e) {
      if (!container.contains(e.target)) tooltip.style.opacity = "0";
    });

    /* 데이터 흐름 애니메이션용 라인 경로 */
    const flowPath = svgEl("line", {
      x1: svgW / 2, y1: PAD_Y + titleOffset,
      x2: svgW / 2, y2: svgH - PAD_Y,
      stroke: "#ddd", "stroke-width": "2", "stroke-dasharray": "6 4",
    });
    svg.appendChild(flowPath);

    layers.forEach(function (layer, i) {
      const cx = svgW / 2;
      const topY = PAD_Y + titleOffset + i * (BOX_H + GAP_Y);
      const x = cx - BOX_W / 2;
      const y = topY;
      const color = COLORS[layer.type] || COLORS.default;

      /* 화살표 (첫 번째 제외) */
      if (i > 0) {
        const arrowY = topY - GAP_Y;
        const arrow = svgEl("line", {
          x1: cx, y1: arrowY, x2: cx, y2: topY,
          stroke: "#bbb", "stroke-width": "1.5",
          "marker-end": "url(#arrowhead)",
        });
        svg.appendChild(arrow);
      }

      /* 박스 그룹 */
      const g = svgEl("g", { style: "cursor:pointer" });

      const rect = svgEl("rect", {
        x, y, width: BOX_W, height: BOX_H, rx: RADIUS, ry: RADIUS,
        fill: color.fill, stroke: color.stroke, "stroke-width": "1.5",
      });
      g.appendChild(rect);

      /* 레이어 이름 */
      g.appendChild(textEl(cx, y + 20, layer.name, { size: "13", bold: true, fill: color.text }));

      /* shape */
      g.appendChild(textEl(cx, y + 38, layer.shape, { size: "11", fill: "#666" }));

      /* 툴팁 위치 계산 (박스 아래 중앙) */
      function positionTooltipBelow() {
        var svgRect = svg.getBoundingClientRect();
        var containerRect = container.getBoundingClientRect();
        var scaleY = svgRect.height / parseFloat(svg.getAttribute("viewBox").split(" ")[3]);
        var boxBottom = svgRect.top - containerRect.top + (y + BOX_H) * scaleY + 6;
        tooltip.style.top = boxBottom + "px";
      }

      /* 데스크톱: 호버 */
      g.addEventListener("mouseenter", function () {
        rect.setAttribute("stroke-width", "2.5");
        rect.setAttribute("filter", "url(#shadow)");
        if (layer.detail) {
          tooltip.textContent = layer.name + "\n" + layer.detail;
          positionTooltipBelow();
          tooltip.style.opacity = "1";
        }
      });
      g.addEventListener("mouseleave", function () {
        rect.setAttribute("stroke-width", "1.5");
        rect.removeAttribute("filter");
        tooltip.style.opacity = "0";
      });

      /* 모바일 + 데스크톱: 클릭/탭 토글 */
      g.addEventListener("click", function (e) {
        e.stopPropagation();
        if (!layer.detail) return;
        var isVisible = tooltip.style.opacity === "1" && tooltip.textContent === layer.name + "\n" + layer.detail;
        tooltip.style.opacity = "0";
        if (!isVisible) {
          tooltip.textContent = layer.name + "\n" + layer.detail;
          positionTooltipBelow();
          tooltip.style.opacity = "1";
          rect.setAttribute("stroke-width", "2.5");
          rect.setAttribute("filter", "url(#shadow)");
        } else {
          rect.setAttribute("stroke-width", "1.5");
          rect.removeAttribute("filter");
        }
      });

      svg.appendChild(g);
    });

    /* defs: 화살표 마커 + 그림자 필터 */
    const defs = svgEl("defs", {});

    const marker = svgEl("marker", {
      id: "arrowhead", markerWidth: "8", markerHeight: "6",
      refX: "8", refY: "3", orient: "auto",
    });
    const arrowPath = svgEl("path", { d: "M0,0 L8,3 L0,6 Z", fill: "#bbb" });
    marker.appendChild(arrowPath);
    defs.appendChild(marker);

    const filter = svgEl("filter", { id: "shadow", x: "-5%", y: "-5%", width: "110%", height: "120%" });
    const feDropShadow = svgEl("feDropShadow", {
      dx: "0", dy: "2", stdDeviation: "3", "flood-color": "#00000020",
    });
    filter.appendChild(feDropShadow);
    defs.appendChild(filter);

    svg.insertBefore(defs, svg.firstChild);

    /* 데이터 흐름 애니메이션 (점이 위에서 아래로) */
    const flowDot = svgEl("circle", {
      cx: svgW / 2, r: "4", fill: "#2196F3", opacity: "0.8",
    });
    const animate = svgEl("animate", {
      attributeName: "cy",
      from: PAD_Y + titleOffset,
      to: svgH - PAD_Y,
      dur: (n * 0.6) + "s",
      repeatCount: "indefinite",
    });
    flowDot.appendChild(animate);
    svg.appendChild(flowDot);

    container.innerHTML = "";
    container.appendChild(svg);
  }

  /* ── 초기화 ── */
  function init() {
    document.querySelectorAll(".arch-flow").forEach(renderFlowchart);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
