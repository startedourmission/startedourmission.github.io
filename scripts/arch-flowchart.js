/**
 * arch-flowchart.js v2
 * 모델 아키텍처 인터랙티브 플로차트
 *
 * 마크다운: %%arch:alexnet%%
 * HTML:     <div class="arch-flow" data-arch="alexnet"></div>
 */
(function () {
  "use strict";

  /* ── 스타일 (검정 + 회색 + 강조 1색) ── */
  var S = {
    stroke: "#333", fill: "#fff", fillAlt: "#f7f7f7",
    text: "#333", textSub: "#888", accent: "#2563EB",
    font: "-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
  };

  /* ── 레이아웃 ── */
  var COL_W = 220, ROW_H = 72, PAD = 30, R = 6;
  var BOX_W = 190, BOX_H = 54;

  /* ── 프리셋 ── */
  /* 각 노드: { id, name, sub, data, col, row, detail, filter }
     각 엣지: { from, to, label }
     col/row: 그리드 좌표. col=0 중앙, -1 왼쪽, 1 오른쪽 */
  var P = {};

  P.alexnet = {
    title: "AlexNet (2012)",
    nodes: [
      { id:"in",   name:"Input",           sub:"227×227×3", data:"🖼 RGB 이미지",        col:0, row:0 },
      { id:"c1",   name:"Conv1 + ReLU",    sub:"55×55×96",  data:"96개 특징 맵",          col:0, row:1, detail:"11×11 필터, stride 4", filter:[11,11] },
      { id:"p1",   name:"MaxPool → LRN",   sub:"27×27×96",  data:"공간 축소",             col:0, row:2, detail:"3×3 pool, stride 2" },
      { id:"c2",   name:"Conv2 + ReLU",    sub:"27×27×256", data:"256개 특징 맵",          col:0, row:3, detail:"5×5 필터, pad 2", filter:[5,5] },
      { id:"p2",   name:"MaxPool → LRN",   sub:"13×13×256", data:"공간 축소",             col:0, row:4, detail:"3×3 pool, stride 2" },
      { id:"c3",   name:"Conv3 + ReLU",    sub:"13×13×384", data:"GPU 간 통신 시작",       col:0, row:5, detail:"3×3 필터, pad 1", filter:[3,3] },
      { id:"c4",   name:"Conv4 + ReLU",    sub:"13×13×384", data:"",                     col:0, row:6, detail:"3×3 필터, pad 1", filter:[3,3] },
      { id:"c5",   name:"Conv5 + ReLU",    sub:"13×13×256", data:"",                     col:0, row:7, detail:"3×3 필터, pad 1", filter:[3,3] },
      { id:"p3",   name:"MaxPool",          sub:"6×6×256",  data:"9216 벡터로 펼침",       col:0, row:8, detail:"3×3 pool → Flatten" },
      { id:"f6",   name:"FC6 + Dropout",    sub:"4096",     data:"[0.2, -1.1, 0.8, ...]", col:0, row:9, detail:"ReLU, Dropout p=0.5" },
      { id:"f7",   name:"FC7 + Dropout",    sub:"4096",     data:"[0.5, 0.0, -0.3, ...]", col:0, row:10, detail:"ReLU, Dropout p=0.5" },
      { id:"out",  name:"Softmax",          sub:"1000 classes", data:"P(고양이)=0.87",     col:0, row:11 },
    ],
    edges: [
      {from:"in",to:"c1",label:"11×11 conv"},{from:"c1",to:"p1"},{from:"p1",to:"c2",label:"5×5 conv"},
      {from:"c2",to:"p2"},{from:"p2",to:"c3",label:"3×3 conv"},{from:"c3",to:"c4"},{from:"c4",to:"c5"},
      {from:"c5",to:"p3"},{from:"p3",to:"f6",label:"flatten"},{from:"f6",to:"f7"},{from:"f7",to:"out"},
    ],
  };

  P.dbn = {
    title: "Deep Belief Net (2006)",
    nodes: [
      { id:"in",  name:"Input",           sub:"784 (28×28)", data:"손글씨 이미지",  col:0, row:0 },
      { id:"r1",  name:"RBM 1",           sub:"500 units",   data:"저수준 특징",    col:0, row:1, detail:"비지도 사전훈련: CD-1" },
      { id:"r2",  name:"RBM 2",           sub:"500 units",   data:"중간 특징",      col:0, row:2, detail:"비지도 사전훈련: CD-1" },
      { id:"r3",  name:"RBM 3",           sub:"2000 units",  data:"고수준 표현",    col:0, row:3, detail:"비지도 사전훈련: CD-1" },
      { id:"ft",  name:"Fine-tune",       sub:"전체 가중치",   data:"지도 학습 조정", col:0, row:4, detail:"Wake-sleep 변형" },
      { id:"out", name:"Output",          sub:"10 classes",  data:"P(숫자 3)=0.94", col:0, row:5 },
    ],
    edges: [
      {from:"in",to:"r1",label:"학습 ①"},{from:"r1",to:"r2",label:"학습 ②"},
      {from:"r2",to:"r3",label:"학습 ③"},{from:"r3",to:"ft",label:"↕ 미세조정"},
      {from:"ft",to:"out"},
    ],
  };

  P.autoencoder = {
    title: "Autoencoder (2006)",
    nodes: [
      { id:"in",  name:"Input",     sub:"784",  data:"손글씨 이미지",   col:0, row:0 },
      { id:"e1",  name:"Encoder 1", sub:"1000", data:"압축 시작",       col:-1, row:1 },
      { id:"e2",  name:"Encoder 2", sub:"500",  data:"",               col:-1, row:2 },
      { id:"e3",  name:"Encoder 3", sub:"250",  data:"",               col:-1, row:3 },
      { id:"bn",  name:"Bottleneck",sub:"30",   data:"핵심 표현 30차원", col:0, row:4, detail:"이 코드로 시각화/분류" },
      { id:"d1",  name:"Decoder 1", sub:"250",  data:"",               col:1, row:3 },
      { id:"d2",  name:"Decoder 2", sub:"500",  data:"",               col:1, row:2 },
      { id:"d3",  name:"Decoder 3", sub:"1000", data:"복원 시작",       col:1, row:1 },
      { id:"out", name:"Output",    sub:"784",  data:"복원된 이미지",    col:0, row:5 },
    ],
    edges: [
      {from:"in",to:"e1"},{from:"e1",to:"e2"},{from:"e2",to:"e3"},{from:"e3",to:"bn",label:"encode"},
      {from:"bn",to:"d1",label:"decode"},{from:"d1",to:"d2"},{from:"d2",to:"d3"},{from:"d3",to:"out"},
    ],
  };

  P.distillation = {
    title: "Knowledge Distillation (2015)",
    nodes: [
      { id:"in",   name:"Input",           sub:"학습 데이터",     data:"이미지/텍스트",     col:0,  row:0 },
      { id:"tea",  name:"Teacher (대형)",   sub:"앙상블/대형 모델", data:"높은 정확도",      col:-1, row:1, detail:"이미 훈련 완료" },
      { id:"stu",  name:"Student (소형)",   sub:"경량 모델",       data:"학습 중",          col:1,  row:1 },
      { id:"soft", name:"Soft Targets",    sub:"softmax(z/T)",   data:"[.05,.80,.10,.05]", col:-1, row:2, detail:"temperature T로 소프트닝" },
      { id:"hard", name:"Hard Labels",     sub:"정답",            data:"[0, 1, 0, 0]",     col:1,  row:2 },
      { id:"loss", name:"Combined Loss",   sub:"αL_soft + βL_hard", data:"두 손실 결합",   col:0,  row:3 },
      { id:"out",  name:"Distilled Model", sub:"소형 + 높은 성능",  data:"배포용",          col:0,  row:4 },
    ],
    edges: [
      {from:"in",to:"tea"},{from:"in",to:"stu"},{from:"tea",to:"soft",label:"T=20"},
      {from:"stu",to:"hard"},{from:"soft",to:"loss"},{from:"hard",to:"loss"},
      {from:"loss",to:"out"},
    ],
  };

  P.dropout = {
    title: "Dropout (2014)",
    nodes: [
      { id:"in",   name:"Input",          sub:"입력 벡터",    data:"[1.2, 0.5, -0.8, 2.1]", col:0, row:0 },
      { id:"h1",   name:"Hidden 1",       sub:"N units",     data:"전체 뉴런 활성",          col:-1, row:1 },
      { id:"d1",   name:"× Dropout Mask", sub:"p=0.5",       data:"[1,0,1,0,1,...] 랜덤",   col:1, row:1, detail:"Bernoulli(0.5)" },
      { id:"h1d",  name:"Thinned Layer",  sub:"~N/2 활성",   data:"뉴런 절반 꺼짐",          col:0, row:2 },
      { id:"h2",   name:"Hidden 2",       sub:"N units",     data:"전체 뉴런 활성",          col:-1, row:3 },
      { id:"d2",   name:"× Dropout Mask", sub:"p=0.5",       data:"[0,1,1,0,0,...] 랜덤",   col:1, row:3, detail:"Bernoulli(0.5)" },
      { id:"h2d",  name:"Thinned Layer",  sub:"~N/2 활성",   data:"뉴런 절반 꺼짐",          col:0, row:4 },
      { id:"out",  name:"Output",         sub:"추론: W×p",    data:"앙상블 평균 근사",        col:0, row:5, detail:"테스트 시 전체 가중치×p 사용" },
    ],
    edges: [
      {from:"in",to:"h1"},{from:"h1",to:"h1d"},{from:"d1",to:"h1d",label:"mask"},
      {from:"h1d",to:"h2"},{from:"h2",to:"h2d"},{from:"d2",to:"h2d",label:"mask"},
      {from:"h2d",to:"out"},
    ],
  };

  P.boltzmann = {
    title: "Boltzmann Machine (1985)",
    nodes: [
      { id:"v",   name:"Visible Units",  sub:"관측 데이터",     data:"[1,0,1,1,0,...]",  col:-1, row:0 },
      { id:"h",   name:"Hidden Units",   sub:"잠재 표현",       data:"[?,?,?,...]",       col:1,  row:0 },
      { id:"e",   name:"Energy",         sub:"E(v,h)",          data:"-Σ wᵢⱼvᵢhⱼ - Σb",  col:0,  row:1, detail:"낮은 에너지 = 높은 확률" },
      { id:"gs",  name:"Gibbs Sampling", sub:"교대 샘플링",      data:"v→h→v→h... 반복",   col:0,  row:2, detail:"평형 상태에 도달할 때까지" },
      { id:"upd", name:"ΔW 업데이트",    sub:"⟨vh⟩data−⟨vh⟩model", data:"가중치 조정",   col:0,  row:3 },
    ],
    edges: [
      {from:"v",to:"e",label:"wᵢⱼ"},{from:"h",to:"e",label:"wᵢⱼ"},
      {from:"e",to:"gs"},{from:"gs",to:"upd"},
    ],
  };

  P.helmholtz = {
    title: "Helmholtz Machine (1995)",
    nodes: [
      { id:"data", name:"Data (x)",       sub:"관측 데이터",    data:"이미지 입력",         col:0,  row:0 },
      { id:"rec",  name:"Recognition ↑",  sub:"q(z|x)",        data:"상향 추론",           col:-1, row:1, detail:"데이터→잠재변수" },
      { id:"z",    name:"Latent z",       sub:"잠재 변수",      data:"압축된 표현",          col:0,  row:2 },
      { id:"gen",  name:"Generative ↓",   sub:"p(x|z)",        data:"하향 생성",           col:1,  row:1, detail:"잠재변수→데이터" },
      { id:"wake", name:"Wake Phase",     sub:"생성 가중치 학습", data:"실제 데이터 사용",   col:-1, row:3, detail:"인식 네트워크 고정, 생성 학습" },
      { id:"sleep",name:"Sleep Phase",    sub:"인식 가중치 학습", data:"환각 데이터 사용",   col:1,  row:3, detail:"생성 네트워크 고정, 인식 학습" },
    ],
    edges: [
      {from:"data",to:"rec"},{from:"rec",to:"z",label:"encode"},{from:"z",to:"gen",label:"decode"},
      {from:"gen",to:"data"},{from:"rec",to:"wake"},{from:"gen",to:"sleep"},
    ],
  };

  P.capsule = {
    title: "Capsule Network (2017)",
    nodes: [
      { id:"in",  name:"Input",         sub:"28×28×1",      data:"손글씨 이미지",               col:0, row:0 },
      { id:"c1",  name:"Conv1",         sub:"20×20×256",    data:"256개 특징 맵",                col:0, row:1, detail:"9×9, stride 1, ReLU", filter:[9,9] },
      { id:"pc",  name:"PrimaryCaps",   sub:"6×6×32×8D",    data:"32채널, 각 8D 벡터",           col:0, row:2, detail:"9×9, stride 2 → 캡슐 변환", filter:[9,9] },
      { id:"rt",  name:"Dynamic Routing",sub:"3회 반복",     data:"cᵢⱼ 업데이트 → 합의",          col:0, row:3, detail:"routing-by-agreement" },
      { id:"dc",  name:"DigitCaps",     sub:"10×16D",       data:"10개 클래스, 각 16D 벡터",      col:0, row:4, detail:"벡터 길이 = 존재 확률" },
      { id:"out", name:"Classification", sub:"10 classes",  data:"‖v‖ → P(숫자 7)=0.91",        col:0, row:5 },
    ],
    edges: [
      {from:"in",to:"c1",label:"9×9 conv"},{from:"c1",to:"pc",label:"캡슐화"},
      {from:"pc",to:"rt",label:"예측 벡터 ûⱼ|ᵢ"},{from:"rt",to:"dc"},{from:"dc",to:"out",label:"‖v‖"},
    ],
  };

  P.simclr = {
    title: "SimCLR (2020)",
    nodes: [
      { id:"in",  name:"Input Image x",   sub:"원본 이미지",       data:"🖼 고양이 사진",        col:0,  row:0 },
      { id:"a1",  name:"Augment → x̃ᵢ",   sub:"crop+color",       data:"🖼 변형 A",             col:-1, row:1, detail:"랜덤 crop, 색상 변환" },
      { id:"a2",  name:"Augment → x̃ⱼ",   sub:"crop+blur",        data:"🖼 변형 B",             col:1,  row:1, detail:"랜덤 crop, 가우시안 blur" },
      { id:"e1",  name:"Encoder f(·)",    sub:"ResNet-50",        data:"hᵢ ∈ ℝ²⁰⁴⁸",          col:-1, row:2, detail:"공유 가중치" },
      { id:"e2",  name:"Encoder f(·)",    sub:"ResNet-50",        data:"hⱼ ∈ ℝ²⁰⁴⁸",          col:1,  row:2, detail:"동일 인코더" },
      { id:"p1",  name:"Projection g(·)", sub:"MLP → 128D",       data:"zᵢ ∈ ℝ¹²⁸",           col:-1, row:3 },
      { id:"p2",  name:"Projection g(·)", sub:"MLP → 128D",       data:"zⱼ ∈ ℝ¹²⁸",           col:1,  row:3 },
      { id:"loss",name:"NT-Xent Loss",    sub:"대조 손실",         data:"같은 쌍↑ 다른 쌍↓",     col:0,  row:4, detail:"sim(zᵢ,zⱼ)/τ" },
      { id:"out", name:"Representation h", sub:"2048-dim",        data:"프로젝션 헤드 버림",      col:0,  row:5, detail:"downstream task에 h 사용" },
    ],
    edges: [
      {from:"in",to:"a1"},{from:"in",to:"a2"},{from:"a1",to:"e1"},{from:"a2",to:"e2"},
      {from:"e1",to:"p1"},{from:"e2",to:"p2"},{from:"p1",to:"loss"},{from:"p2",to:"loss"},
      {from:"e1",to:"out"},{from:"e2",to:"out"},
    ],
  };

  P.byol = {
    title: "BYOL (2020)",
    nodes: [
      { id:"in",   name:"Input Image",       sub:"원본 이미지",     data:"🖼",                col:0,  row:0 },
      { id:"on_e", name:"Online Encoder",     sub:"f_θ",           data:"학습됨",             col:-1, row:1, detail:"그래디언트 업데이트" },
      { id:"tg_e", name:"Target Encoder",     sub:"f_ξ (EMA)",     data:"θ의 이동평균",       col:1,  row:1, detail:"학습 안 함, ξ←τξ+(1-τ)θ" },
      { id:"on_p", name:"Online Projector",   sub:"g_θ → z",      data:"",                   col:-1, row:2 },
      { id:"tg_p", name:"Target Projector",   sub:"g_ξ → z'",     data:"",                   col:1,  row:2 },
      { id:"pred", name:"Predictor q_θ",      sub:"q(z) → p",     data:"비대칭 핵심",         col:-1, row:3, detail:"target에는 predictor 없음" },
      { id:"sg",   name:"Stop-Gradient",      sub:"sg(z')",        data:"그래디언트 차단",     col:1,  row:3 },
      { id:"loss", name:"MSE Loss",           sub:"‖p - sg(z')‖²", data:"예측 ↔ target",     col:0,  row:4 },
    ],
    edges: [
      {from:"in",to:"on_e"},{from:"in",to:"tg_e"},
      {from:"on_e",to:"on_p"},{from:"tg_e",to:"tg_p"},
      {from:"on_p",to:"pred"},{from:"tg_p",to:"sg"},
      {from:"pred",to:"loss"},{from:"sg",to:"loss"},
    ],
  };

  P.forwardforward = {
    title: "Forward-Forward (2022)",
    nodes: [
      { id:"pos", name:"Positive Input",  sub:"데이터 + 정답 레이블", data:"실제 이미지 + '3'",   col:-1, row:0 },
      { id:"neg", name:"Negative Input",  sub:"데이터 + 오답 레이블", data:"실제 이미지 + '7'",   col:1,  row:0 },
      { id:"l1p", name:"Layer 1",         sub:"goodness ↑",          data:"Σ(aᵢ²) > θ 목표",    col:-1, row:1, detail:"양성: 임계값 초과하도록" },
      { id:"l1n", name:"Layer 1",         sub:"goodness ↓",          data:"Σ(aᵢ²) < θ 목표",    col:1,  row:1, detail:"음성: 임계값 미달하도록" },
      { id:"l2p", name:"Layer 2",         sub:"goodness ↑",          data:"층별 독립 학습",       col:-1, row:2 },
      { id:"l2n", name:"Layer 2",         sub:"goodness ↓",          data:"역전파 불필요",        col:1,  row:2 },
      { id:"pred",name:"Prediction",      sub:"argmax goodness",     data:"가장 높은 클래스 선택", col:0,  row:3 },
    ],
    edges: [
      {from:"pos",to:"l1p"},{from:"neg",to:"l1n"},{from:"l1p",to:"l2p"},{from:"l1n",to:"l2n"},
      {from:"l2p",to:"pred"},{from:"l2n",to:"pred"},
    ],
  };

  P.contrastive_divergence = {
    title: "Contrastive Divergence (2002)",
    nodes: [
      { id:"v0",  name:"Data v⁰",        sub:"관측 데이터",         data:"[1,0,1,1,0,...]",   col:0, row:0 },
      { id:"h0",  name:"Sample h⁰",      sub:"p(h|v⁰)",           data:"은닉 활성화",        col:0, row:1, detail:"v⁰에서 h⁰ 샘플링" },
      { id:"v1",  name:"Reconstruct v¹",  sub:"p(v|h⁰)",           data:"1스텝 재구성",       col:0, row:2, detail:"깁스 샘플링 1회" },
      { id:"pos", name:"Positive ⟨vh⟩⁰",  sub:"데이터 통계량",      data:"v⁰ × h⁰",          col:-1, row:3 },
      { id:"neg", name:"Negative ⟨vh⟩¹",  sub:"모델 통계량",        data:"v¹ × h¹",          col:1,  row:3 },
      { id:"upd", name:"ΔW ∝ pos − neg",  sub:"가중치 업데이트",    data:"1스텝만으로 근사",  col:0,  row:4 },
    ],
    edges: [
      {from:"v0",to:"h0",label:"p(h|v)"},{from:"h0",to:"v1",label:"p(v|h)"},
      {from:"v0",to:"pos"},{from:"h0",to:"pos"},{from:"v1",to:"neg"},
      {from:"pos",to:"upd",label:"+"},{from:"neg",to:"upd",label:"−"},
    ],
  };

  P.tsne = {
    title: "t-SNE (2008)",
    nodes: [
      { id:"in",  name:"High-D Data",     sub:"n×D",              data:"784차원 벡터들",              col:0, row:0 },
      { id:"ph",  name:"Pairwise p_ij",   sub:"가우시안 커널",     data:"고차원 유사도 행렬",          col:0, row:1, detail:"가까운 점 → 높은 pᵢⱼ" },
      { id:"lo",  name:"Init Embedding",   sub:"n×2 랜덤",         data:"2D 좌표 랜덤 배치",          col:0, row:2 },
      { id:"ql",  name:"Student-t q_ij",   sub:"t분포 (df=1)",    data:"저차원 유사도",               col:0, row:3, detail:"긴 꼬리 → crowding 해결" },
      { id:"kl",  name:"Minimize KL(P‖Q)", sub:"경사하강법",       data:"p와 q 차이 줄이기",           col:0, row:4 },
      { id:"out", name:"2D Visualization", sub:"n×2",             data:"클러스터 시각화 완성",         col:0, row:5 },
    ],
    edges: [
      {from:"in",to:"ph",label:"가우시안"},{from:"ph",to:"lo"},
      {from:"lo",to:"ql",label:"t분포"},{from:"ql",to:"kl"},{from:"kl",to:"out",label:"반복 최적화"},
    ],
  };

  P.layernorm = {
    title: "Layer Normalization (2016)",
    nodes: [
      { id:"in",  name:"Input Activation", sub:"H-dim vector",    data:"[2.1, -0.5, 1.3, ...]",   col:0, row:0 },
      { id:"st",  name:"Compute μ, σ",     sub:"한 층의 통계량",    data:"μ=0.97, σ=1.04",          col:0, row:1, detail:"배치가 아닌 층 단위" },
      { id:"nm",  name:"Normalize",        sub:"(a−μ)/σ",         data:"[1.09, -1.41, 0.32, ...]", col:0, row:2 },
      { id:"sc",  name:"Scale & Shift",    sub:"γ·â + β",         data:"학습 가능 파라미터",         col:0, row:3, detail:"γ, β per feature" },
      { id:"out", name:"Output",           sub:"정규화 완료",      data:"안정적 활성값",              col:0, row:4 },
    ],
    edges: [
      {from:"in",to:"st"},{from:"st",to:"nm"},{from:"nm",to:"sc"},{from:"sc",to:"out"},
    ],
  };

  P.wakesleep = P.helmholtz;  /* 동일 구조 */

  P.rbm_relu = {
    title: "ReLU Improves RBM (2010)",
    nodes: [
      { id:"in",  name:"Visible (Input)",  sub:"실수값 입력",     data:"[0.3, 1.2, -0.1, ...]",  col:0,  row:0 },
      { id:"old", name:"Sigmoid RBM",      sub:"σ(Wx+b)",        data:"0~1 사이 출력",           col:-1, row:1, detail:"기존 방식: 포화 문제" },
      { id:"new", name:"NReLU",            sub:"max(0, x+ε)",    data:"0 또는 양수",             col:1,  row:1, detail:"노이즈 ReLU: 무한 이진 유닛 근사" },
      { id:"cd",  name:"Contrastive Div.", sub:"CD-1",            data:"수렴 속도 개선",          col:0,  row:2 },
      { id:"out", name:"Learned Features", sub:"개선된 표현",     data:"CIFAR-10/NORB 향상",      col:0,  row:3 },
    ],
    edges: [
      {from:"in",to:"old"},{from:"in",to:"new"},{from:"old",to:"cd"},{from:"new",to:"cd"},
      {from:"cd",to:"out"},
    ],
  };

  P.transformer_ae = {
    title: "Transforming Auto-encoders (2011)",
    nodes: [
      { id:"in",  name:"Input Image",        sub:"이미지 패치",      data:"원본 이미지",           col:0, row:0 },
      { id:"rec", name:"Recognition",        sub:"pᵢ = σ(Wᵢx)",    data:"캡슐별 확률",           col:-1, row:1, detail:"각 캡슐 독립 인식" },
      { id:"pos", name:"Pose + Transform",   sub:"Tᵢ(Δ)",           data:"이동/회전 적용",        col:0,  row:2, detail:"변환 행렬" },
      { id:"gen", name:"Generation",         sub:"yᵢ = pᵢ·g(Tᵢ)",  data:"캡슐별 출력",           col:1,  row:1, detail:"변환된 포즈로 생성" },
      { id:"sum", name:"Sum Outputs",        sub:"Σ yᵢ",            data:"모든 캡슐 합산",        col:0,  row:3 },
      { id:"out", name:"Reconstruction",     sub:"변환된 이미지",     data:"이동/회전된 복원",      col:0,  row:4 },
    ],
    edges: [
      {from:"in",to:"rec"},{from:"rec",to:"pos"},{from:"pos",to:"gen"},
      {from:"gen",to:"sum"},{from:"sum",to:"out"},
    ],
  };

  /* ── SVG 헬퍼 ── */
  function sv(tag, a) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (var k in a) if (a.hasOwnProperty(k)) el.setAttribute(k, a[k]);
    return el;
  }
  function tx(x, y, str, o) {
    o = o || {};
    var t = sv("text", {
      x:x, y:y, "text-anchor": o.anchor||"middle",
      "font-size": o.size||"11", "font-weight": o.bold?"600":"400",
      "font-family": S.font, fill: o.fill||S.text, "pointer-events":"none",
    });
    t.textContent = str;
    return t;
  }

  /* ── 필터 아이콘 (작은 격자) ── */
  function drawFilter(svg, cx, cy, fw, fh) {
    var s = 3, gx = cx - (fw*s)/2, gy = cy - (fh*s)/2;
    for (var r=0; r<Math.min(fh,5); r++) {
      for (var c=0; c<Math.min(fw,5); c++) {
        svg.appendChild(sv("rect", {
          x: gx+c*s, y: gy+r*s, width: s-0.5, height: s-0.5,
          fill: (r+c)%2===0 ? S.accent : "#ddd", opacity: "0.5", rx:"0.5",
        }));
      }
    }
  }

  /* ── 메인 렌더러 ── */
  function render(container) {
    var key = container.dataset.arch;
    if (!key || !P[key]) {
      container.innerHTML = "<p style='color:#999'>arch-flowchart: '" + key + "' 미지원</p>";
      return;
    }
    var arch = P[key], nodes = arch.nodes, edges = arch.edges;

    /* 그리드 범위 계산 */
    var minC=0, maxC=0, maxR=0;
    nodes.forEach(function(n) {
      if (n.col < minC) minC = n.col;
      if (n.col > maxC) maxC = n.col;
      if (n.row > maxR) maxR = n.row;
    });
    var cols = maxC - minC + 1;
    var svgW = cols * COL_W + PAD * 2;
    var svgH = (maxR + 1) * ROW_H + PAD * 2 + 28; /* +28 타이틀 */

    var svg = sv("svg", {
      width: "100%", viewBox: "0 0 " + svgW + " " + svgH,
      style: "max-width:" + Math.min(svgW, 600) + "px;display:block;margin:1.5em auto;",
    });

    /* 타이틀 */
    svg.appendChild(tx(svgW/2, 20, arch.title, { size:"14", bold:true }));

    /* 노드 ID → 위치 맵 */
    var pos = {};
    function ncx(n) { return PAD + (n.col - minC) * COL_W + COL_W/2; }
    function ncy(n) { return 38 + n.row * ROW_H + BOX_H/2; }
    nodes.forEach(function(n) { pos[n.id] = { cx: ncx(n), cy: ncy(n) }; });

    /* defs */
    var defs = sv("defs", {});
    var mk = sv("marker", { id:"ah", markerWidth:"7", markerHeight:"5", refX:"7", refY:"2.5", orient:"auto" });
    mk.appendChild(sv("path", { d:"M0,0 L7,2.5 L0,5 Z", fill:S.stroke }));
    defs.appendChild(mk);
    svg.appendChild(defs);

    /* 엣지 */
    edges.forEach(function(e) {
      var f = pos[e.from], t = pos[e.to];
      if (!f || !t) return;
      /* 시작/끝을 박스 경계로 조정 */
      var dy = t.cy - f.cy, dx = t.cx - f.cx;
      var fy = f.cy + BOX_H/2, ty = t.cy - BOX_H/2;
      var fx = f.cx, tx2 = t.cx;
      if (Math.abs(dy) < ROW_H * 0.3) { /* 같은 행 → 수평 */
        fx = dx > 0 ? f.cx + BOX_W/2 : f.cx - BOX_W/2;
        tx2 = dx > 0 ? t.cx - BOX_W/2 : t.cx + BOX_W/2;
        fy = f.cy; ty = t.cy;
      }

      if (fx === tx2) {
        /* 수직선 */
        svg.appendChild(sv("line", {
          x1:fx, y1:fy, x2:tx2, y2:ty,
          stroke:S.stroke, "stroke-width":"1.2", "marker-end":"url(#ah)",
        }));
      } else {
        /* 곡선 경로 */
        var midY = (fy + ty) / 2;
        svg.appendChild(sv("path", {
          d: "M"+fx+","+fy+" C"+fx+","+midY+" "+tx2+","+midY+" "+tx2+","+ty,
          fill:"none", stroke:S.stroke, "stroke-width":"1.2", "marker-end":"url(#ah)",
        }));
      }

      /* 엣지 라벨 */
      if (e.label) {
        var lx = (fx + tx2) / 2 + (fx === tx2 ? 0 : 0);
        var ly = (fy + ty) / 2;
        var bg = sv("rect", {
          x: lx - e.label.length * 3.5 - 3, y: ly - 7,
          width: e.label.length * 7 + 6, height: 14,
          fill: "#fff", rx: "3",
        });
        svg.appendChild(bg);
        svg.appendChild(tx(lx, ly + 3.5, e.label, { size:"9", fill:S.textSub }));
      }
    });

    /* 툴팁 */
    var tooltip = document.createElement("div");
    Object.assign(tooltip.style, {
      position:"absolute", padding:"8px 14px", background:"#222", color:"#fff",
      borderRadius:"6px", fontSize:"13px", lineHeight:"1.5",
      pointerEvents:"none", opacity:"0", transition:"opacity 0.15s",
      zIndex:"9999", maxWidth:"260px", whiteSpace:"pre-wrap",
      fontFamily:S.font, left:"50%", transform:"translateX(-50%)",
    });
    container.style.position = "relative";
    container.appendChild(tooltip);
    document.addEventListener("click", function(ev) {
      if (!container.contains(ev.target)) tooltip.style.opacity = "0";
    });

    /* 노드 */
    nodes.forEach(function(n) {
      var cx = pos[n.id].cx, cy = pos[n.id].cy;
      var x = cx - BOX_W/2, y = cy - BOX_H/2;
      var g = sv("g", { style:"cursor:pointer" });

      /* 박스 */
      g.appendChild(sv("rect", {
        x:x, y:y, width:BOX_W, height:BOX_H, rx:R, ry:R,
        fill: n.filter ? S.fillAlt : S.fill, stroke:S.stroke, "stroke-width":"1.2",
      }));

      /* 이름 */
      g.appendChild(tx(cx, cy - 10, n.name, { size:"12", bold:true }));

      /* shape (sub) */
      g.appendChild(tx(cx, cy + 4, n.sub, { size:"10", fill:S.textSub }));

      /* 데이터 흐름 예시 */
      if (n.data) {
        g.appendChild(tx(cx, cy + 18, n.data, { size:"9", fill:S.accent }));
      }

      /* 필터 아이콘 */
      if (n.filter) {
        drawFilter(g, x + BOX_W - 18, y + 14, n.filter[0], n.filter[1]);
      }

      /* 인터랙션 */
      var rect = g.querySelector("rect");
      function showTip() {
        if (!n.detail) return;
        tooltip.textContent = n.name + "\n" + n.detail;
        var svgRect = svg.getBoundingClientRect();
        var cRect = container.getBoundingClientRect();
        var scaleY = svgRect.height / svgH;
        tooltip.style.top = (svgRect.top - cRect.top + (cy + BOX_H/2) * scaleY + 6) + "px";
        tooltip.style.opacity = "1";
        rect.setAttribute("stroke-width", "2");
      }
      function hideTip() {
        tooltip.style.opacity = "0";
        rect.setAttribute("stroke-width", "1.2");
      }
      g.addEventListener("mouseenter", showTip);
      g.addEventListener("mouseleave", hideTip);
      g.addEventListener("click", function(ev) {
        ev.stopPropagation();
        if (!n.detail) return;
        tooltip.style.opacity === "1" ? hideTip() : showTip();
      });

      svg.appendChild(g);
    });

    container.innerHTML = "";
    container.appendChild(svg);
  }

  /* ── 초기화 ── */
  function init() {
    document.querySelectorAll(".arch-flow").forEach(render);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
