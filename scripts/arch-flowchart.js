/**
 * arch-flowchart.js v3
 * 모델 아키텍처 인터랙티브 플로차트 + 데이터 흐름 애니메이션
 *
 * 마크다운: %%arch:alexnet%%
 */
(function () {
  "use strict";

  /* ── 스타일 (검정 + 회색 + 강조색) ── */
  var S = {
    stroke: "#333", fill: "#fff", fillAlt: "#f7f7f7",
    text: "#333", textSub: "#888", accent: "#2563EB",
    font: "-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif",
  };

  var COL_W = 220, ROW_H = 72, PAD = 30, R = 6;
  var BOX_W = 190, BOX_H = 54;

  /* ── vis 타입별 데이터 시각화 그리기 ──
     vis 종류:
       "img"    — 작은 픽셀 그리드 (이미지)
       "maps"   — 여러 작은 사각형 (피처맵)
       "maps_s" — 더 작은 피처맵
       "vec"    — 수평 막대 (벡터)
       "bar"    — 수직 막대차트 (확률)
       "dots"   — 점 클러스터 (임베딩/잠재공간)
       "narrow" — 아주 좁은 바 (병목)
  */
  function drawVis(g, cx, cy, vis, accent) {
    var a = accent || S.accent;
    switch (vis) {
      case "img": /* 5×5 픽셀 그리드 */
        var colors = ["#e74c3c","#3498db","#2ecc71","#f1c40f","#9b59b6","#e67e22","#1abc9c","#34495e"];
        for (var r=0;r<5;r++) for (var c=0;c<5;c++) {
          g.appendChild(sv("rect",{
            x:cx-10+c*4, y:cy-10+r*4, width:3.5, height:3.5, rx:"0.5",
            fill: colors[(r*5+c+r)%colors.length], opacity:"0.8",
          }));
        }
        break;
      case "maps": /* 4개 피처맵 */
        for (var i=0;i<4;i++) {
          var mx = cx - 12 + i * 7;
          g.appendChild(sv("rect",{ x:mx, y:cy-6, width:5, height:12, rx:"1",
            fill:a, opacity: (0.3 + i*0.2)+"",
          }));
        }
        break;
      case "maps_s": /* 더 작은 피처맵 3개 */
        for (var i=0;i<3;i++) {
          g.appendChild(sv("rect",{
            x:cx-8+i*6, y:cy-4, width:4, height:8, rx:"1",
            fill:a, opacity:(0.3+i*0.25)+"",
          }));
        }
        break;
      case "vec": /* 수평 벡터 바 */
        g.appendChild(sv("rect",{ x:cx-14, y:cy-3, width:28, height:6, rx:"2",
          fill:a, opacity:"0.25" }));
        for (var i=0;i<7;i++) {
          var h = 2 + Math.abs(Math.sin(i*1.8))*4;
          g.appendChild(sv("rect",{
            x:cx-13+i*4, y:cy-h/2, width:3, height:h, rx:"0.5",
            fill:a, opacity:"0.7",
          }));
        }
        break;
      case "bar": /* 확률 막대차트 */
        var vals = [0.05,0.87,0.03,0.02,0.03];
        for (var i=0;i<5;i++) {
          var bh = vals[i] * 14;
          g.appendChild(sv("rect",{
            x:cx-12+i*5, y:cy+6-bh, width:4, height:bh, rx:"0.5",
            fill: i===1 ? a : "#ccc",
          }));
        }
        break;
      case "dots": /* 점 클러스터 */
        var pts = [[-6,-4],[2,-6],[6,-2],[-3,2],[4,4],[-7,1],[1,-1],[5,6]];
        pts.forEach(function(p){
          g.appendChild(sv("circle",{
            cx:cx+p[0], cy:cy+p[1], r:"1.8",
            fill:a, opacity:(0.4+Math.random()*0.5)+"",
          }));
        });
        break;
      case "narrow": /* 좁은 병목 바 */
        g.appendChild(sv("rect",{ x:cx-3, y:cy-6, width:6, height:12, rx:"2",
          fill:a, opacity:"0.6" }));
        break;
    }
  }

  function sv(tag, a) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (var k in a) if (a.hasOwnProperty(k)) el.setAttribute(k, a[k]);
    return el;
  }
  function tx(x, y, str, o) {
    o = o || {};
    var t = sv("text", {
      x:x, y:y, "text-anchor":o.anchor||"middle",
      "font-size":o.size||"11", "font-weight":o.bold?"600":"400",
      "font-family":S.font, fill:o.fill||S.text, "pointer-events":"none",
    });
    t.textContent = str;
    return t;
  }

  function drawFilter(parent, cx, cy, fw, fh) {
    var s = 3;
    var gx = cx - (Math.min(fw,5)*s)/2, gy = cy - (Math.min(fh,5)*s)/2;
    for (var r=0; r<Math.min(fh,5); r++) {
      for (var c=0; c<Math.min(fw,5); c++) {
        parent.appendChild(sv("rect", {
          x: gx+c*s, y: gy+r*s, width: s-0.5, height: s-0.5,
          fill: (r+c)%2===0 ? S.accent : "#ddd", opacity:"0.5", rx:"0.5",
        }));
      }
    }
  }

  /* ── 프리셋 ── */
  var P = {};

  P.alexnet = {
    title: "AlexNet (2012)",
    /* path: 애니메이션이 따라갈 노드 순서 */
    path: ["in","c1","p1","c2","p2","c3","c4","c5","p3","f6","f7","out"],
    nodes: [
      { id:"in",  name:"Input",          sub:"227×227×3",     col:0, row:0,  vis:"img" },
      { id:"c1",  name:"Conv1 + ReLU",   sub:"55×55×96",      col:0, row:1,  vis:"maps", detail:"11×11 필터, stride 4", filter:[11,11] },
      { id:"p1",  name:"MaxPool → LRN",  sub:"27×27×96",      col:0, row:2,  vis:"maps", detail:"3×3 pool, stride 2" },
      { id:"c2",  name:"Conv2 + ReLU",   sub:"27×27×256",     col:0, row:3,  vis:"maps", detail:"5×5 필터, pad 2", filter:[5,5] },
      { id:"p2",  name:"MaxPool → LRN",  sub:"13×13×256",     col:0, row:4,  vis:"maps_s", detail:"3×3 pool, stride 2" },
      { id:"c3",  name:"Conv3 + ReLU",   sub:"13×13×384",     col:0, row:5,  vis:"maps_s", detail:"3×3 필터, pad 1", filter:[3,3] },
      { id:"c4",  name:"Conv4 + ReLU",   sub:"13×13×384",     col:0, row:6,  vis:"maps_s", detail:"3×3 필터", filter:[3,3] },
      { id:"c5",  name:"Conv5 + ReLU",   sub:"13×13×256",     col:0, row:7,  vis:"maps_s", detail:"3×3 필터", filter:[3,3] },
      { id:"p3",  name:"MaxPool+Flatten", sub:"6×6×256→9216", col:0, row:8,  vis:"vec",  detail:"3×3 pool → Flatten" },
      { id:"f6",  name:"FC6 + Dropout",  sub:"4096",          col:0, row:9,  vis:"vec",  detail:"ReLU, Dropout p=0.5" },
      { id:"f7",  name:"FC7 + Dropout",  sub:"4096",          col:0, row:10, vis:"vec",  detail:"ReLU, Dropout p=0.5" },
      { id:"out", name:"Softmax",        sub:"1000 classes",  col:0, row:11, vis:"bar" },
    ],
    edges: [
      {from:"in",to:"c1",label:"11×11 conv"},{from:"c1",to:"p1"},{from:"p1",to:"c2",label:"5×5 conv"},
      {from:"c2",to:"p2"},{from:"p2",to:"c3",label:"3×3 conv"},{from:"c3",to:"c4"},{from:"c4",to:"c5"},
      {from:"c5",to:"p3"},{from:"p3",to:"f6",label:"flatten"},{from:"f6",to:"f7"},{from:"f7",to:"out"},
    ],
  };

  P.dbn = {
    title: "Deep Belief Net (2006)",
    path: ["in","r1","r2","r3","ft","out"],
    nodes: [
      { id:"in",  name:"Input",      sub:"784 (28×28)", col:0, row:0, vis:"img" },
      { id:"r1",  name:"RBM 1",      sub:"500 units",   col:0, row:1, vis:"maps",  detail:"비지도 사전훈련: CD-1" },
      { id:"r2",  name:"RBM 2",      sub:"500 units",   col:0, row:2, vis:"maps_s",detail:"비지도 사전훈련: CD-1" },
      { id:"r3",  name:"RBM 3",      sub:"2000 units",  col:0, row:3, vis:"vec",   detail:"비지도 사전훈련: CD-1" },
      { id:"ft",  name:"Fine-tune",  sub:"전체 가중치",   col:0, row:4, vis:"vec",   detail:"Wake-sleep 변형" },
      { id:"out", name:"Output",     sub:"10 classes",  col:0, row:5, vis:"bar" },
    ],
    edges: [
      {from:"in",to:"r1",label:"학습 ①"},{from:"r1",to:"r2",label:"학습 ②"},
      {from:"r2",to:"r3",label:"학습 ③"},{from:"r3",to:"ft",label:"미세조정"},
      {from:"ft",to:"out"},
    ],
  };

  P.autoencoder = {
    title: "Autoencoder (2006)",
    path: ["in","e1","e2","e3","bn","d1","d2","d3","out"],
    nodes: [
      { id:"in", name:"Input",     sub:"784",  col:0,  row:0, vis:"img" },
      { id:"e1", name:"Encoder 1", sub:"1000", col:-1, row:1, vis:"maps" },
      { id:"e2", name:"Encoder 2", sub:"500",  col:-1, row:2, vis:"maps_s" },
      { id:"e3", name:"Encoder 3", sub:"250",  col:-1, row:3, vis:"dots" },
      { id:"bn", name:"Bottleneck",sub:"30",   col:0,  row:4, vis:"narrow", detail:"핵심 표현 30차원" },
      { id:"d1", name:"Decoder 1", sub:"250",  col:1,  row:3, vis:"dots" },
      { id:"d2", name:"Decoder 2", sub:"500",  col:1,  row:2, vis:"maps_s" },
      { id:"d3", name:"Decoder 3", sub:"1000", col:1,  row:1, vis:"maps" },
      { id:"out",name:"Output",    sub:"784",  col:0,  row:5, vis:"img" },
    ],
    edges: [
      {from:"in",to:"e1"},{from:"e1",to:"e2"},{from:"e2",to:"e3"},{from:"e3",to:"bn",label:"encode"},
      {from:"bn",to:"d1",label:"decode"},{from:"d1",to:"d2"},{from:"d2",to:"d3"},{from:"d3",to:"out"},
    ],
  };

  P.distillation = {
    title: "Knowledge Distillation (2015)",
    path: ["in","tea","soft","loss","out"],
    nodes: [
      { id:"in",   name:"Input",          sub:"학습 데이터",       col:0,  row:0, vis:"img" },
      { id:"tea",  name:"Teacher (대형)", sub:"앙상블/대형 모델",   col:-1, row:1, vis:"vec", detail:"이미 훈련 완료" },
      { id:"stu",  name:"Student (소형)", sub:"경량 모델",         col:1,  row:1, vis:"vec", detail:"학습 중" },
      { id:"soft", name:"Soft Targets",   sub:"softmax(z/T)",     col:-1, row:2, vis:"bar", detail:"T=20으로 소프트닝" },
      { id:"hard", name:"Hard Labels",    sub:"정답",             col:1,  row:2, vis:"bar" },
      { id:"loss", name:"Combined Loss",  sub:"αL_soft + βL_hard",col:0,  row:3, vis:"dots" },
      { id:"out",  name:"Distilled Model",sub:"소형 + 높은 성능",  col:0,  row:4, vis:"bar" },
    ],
    edges: [
      {from:"in",to:"tea"},{from:"in",to:"stu"},{from:"tea",to:"soft",label:"T=20"},
      {from:"stu",to:"hard"},{from:"soft",to:"loss"},{from:"hard",to:"loss"},
      {from:"loss",to:"out"},
    ],
  };

  P.dropout = {
    title: "Dropout (2014)",
    path: ["in","h1","h1d","h2","h2d","out"],
    nodes: [
      { id:"in",  name:"Input",         sub:"입력 벡터",   col:0,  row:0, vis:"vec" },
      { id:"h1",  name:"Hidden 1",      sub:"N units",    col:-1, row:1, vis:"vec" },
      { id:"d1",  name:"× Dropout Mask",sub:"p=0.5",      col:1,  row:1, vis:"dots", detail:"Bernoulli(0.5)" },
      { id:"h1d", name:"Thinned Layer", sub:"~N/2 활성",  col:0,  row:2, vis:"maps_s" },
      { id:"h2",  name:"Hidden 2",      sub:"N units",    col:-1, row:3, vis:"vec" },
      { id:"d2",  name:"× Dropout Mask",sub:"p=0.5",      col:1,  row:3, vis:"dots", detail:"Bernoulli(0.5)" },
      { id:"h2d", name:"Thinned Layer", sub:"~N/2 활성",  col:0,  row:4, vis:"maps_s" },
      { id:"out", name:"Output",        sub:"추론: W×p",   col:0,  row:5, vis:"bar", detail:"테스트 시 전체 가중치×p" },
    ],
    edges: [
      {from:"in",to:"h1"},{from:"h1",to:"h1d"},{from:"d1",to:"h1d",label:"mask"},
      {from:"h1d",to:"h2"},{from:"h2",to:"h2d"},{from:"d2",to:"h2d",label:"mask"},
      {from:"h2d",to:"out"},
    ],
  };

  P.boltzmann = {
    title: "Boltzmann Machine (1985)",
    path: ["v","e","gs","upd"],
    nodes: [
      { id:"v",   name:"Visible Units",  sub:"관측 데이터",          col:-1, row:0, vis:"img" },
      { id:"h",   name:"Hidden Units",   sub:"잠재 표현",           col:1,  row:0, vis:"dots" },
      { id:"e",   name:"Energy E(v,h)",  sub:"-Σ wᵢⱼvᵢhⱼ",        col:0,  row:1, vis:"narrow", detail:"낮은 에너지=높은 확률" },
      { id:"gs",  name:"Gibbs Sampling", sub:"교대 샘플링",          col:0,  row:2, vis:"dots",   detail:"v→h→v→h 반복" },
      { id:"upd", name:"ΔW 업데이트",    sub:"⟨vh⟩data−⟨vh⟩model", col:0,  row:3, vis:"vec" },
    ],
    edges: [
      {from:"v",to:"e",label:"wᵢⱼ"},{from:"h",to:"e",label:"wᵢⱼ"},
      {from:"e",to:"gs"},{from:"gs",to:"upd"},
    ],
  };

  P.helmholtz = {
    title: "Helmholtz Machine (1995)",
    path: ["data","rec","z","gen"],
    nodes: [
      { id:"data", name:"Data (x)",      sub:"관측 데이터",      col:0,  row:0, vis:"img" },
      { id:"rec",  name:"Recognition ↑", sub:"q(z|x)",          col:-1, row:1, vis:"maps",  detail:"데이터→잠재변수" },
      { id:"z",    name:"Latent z",      sub:"잠재 변수",        col:0,  row:2, vis:"narrow" },
      { id:"gen",  name:"Generative ↓",  sub:"p(x|z)",          col:1,  row:1, vis:"maps",  detail:"잠재변수→데이터" },
      { id:"wake", name:"Wake Phase",    sub:"생성 가중치 학습",  col:-1, row:3, vis:"vec",   detail:"인식 고정, 생성 학습" },
      { id:"sleep",name:"Sleep Phase",   sub:"인식 가중치 학습",  col:1,  row:3, vis:"vec",   detail:"생성 고정, 인식 학습" },
    ],
    edges: [
      {from:"data",to:"rec"},{from:"rec",to:"z",label:"encode"},{from:"z",to:"gen",label:"decode"},
      {from:"gen",to:"data"},{from:"rec",to:"wake"},{from:"gen",to:"sleep"},
    ],
  };
  P.wakesleep = P.helmholtz;

  P.capsule = {
    title: "Capsule Network (2017)",
    path: ["in","c1","pc","rt","dc","out"],
    nodes: [
      { id:"in",  name:"Input",          sub:"28×28×1",    col:0, row:0, vis:"img" },
      { id:"c1",  name:"Conv1",          sub:"20×20×256",  col:0, row:1, vis:"maps",  detail:"9×9, stride 1, ReLU", filter:[9,9] },
      { id:"pc",  name:"PrimaryCaps",    sub:"6×6×32×8D",  col:0, row:2, vis:"dots",  detail:"32채널, 각 8D 캡슐", filter:[9,9] },
      { id:"rt",  name:"Dynamic Routing",sub:"3회 반복",    col:0, row:3, vis:"dots",  detail:"routing-by-agreement" },
      { id:"dc",  name:"DigitCaps",      sub:"10×16D",     col:0, row:4, vis:"vec",   detail:"벡터 길이=존재 확률" },
      { id:"out", name:"Classification", sub:"10 classes",  col:0, row:5, vis:"bar" },
    ],
    edges: [
      {from:"in",to:"c1",label:"9×9 conv"},{from:"c1",to:"pc",label:"캡슐화"},
      {from:"pc",to:"rt",label:"ûⱼ|ᵢ"},{from:"rt",to:"dc"},{from:"dc",to:"out",label:"‖v‖"},
    ],
  };

  P.simclr = {
    title: "SimCLR (2020)",
    path: ["in","a1","e1","p1","loss","out"],
    nodes: [
      { id:"in",  name:"Input Image",     sub:"원본 이미지",   col:0,  row:0, vis:"img" },
      { id:"a1",  name:"Augment → x̃ᵢ",   sub:"crop+color",   col:-1, row:1, vis:"img",  detail:"랜덤 crop, 색상" },
      { id:"a2",  name:"Augment → x̃ⱼ",   sub:"crop+blur",    col:1,  row:1, vis:"img",  detail:"랜덤 crop, blur" },
      { id:"e1",  name:"Encoder f(·)",    sub:"ResNet-50",    col:-1, row:2, vis:"vec",  detail:"공유 가중치" },
      { id:"e2",  name:"Encoder f(·)",    sub:"ResNet-50",    col:1,  row:2, vis:"vec",  detail:"동일 인코더" },
      { id:"p1",  name:"Projection g(·)", sub:"→ 128D",       col:-1, row:3, vis:"dots" },
      { id:"p2",  name:"Projection g(·)", sub:"→ 128D",       col:1,  row:3, vis:"dots" },
      { id:"loss",name:"NT-Xent Loss",    sub:"대조 손실",     col:0,  row:4, vis:"narrow", detail:"sim(zᵢ,zⱼ)/τ" },
      { id:"out", name:"Representation",  sub:"2048-dim h",   col:0,  row:5, vis:"vec",    detail:"프로젝션 헤드 버림" },
    ],
    edges: [
      {from:"in",to:"a1"},{from:"in",to:"a2"},{from:"a1",to:"e1"},{from:"a2",to:"e2"},
      {from:"e1",to:"p1"},{from:"e2",to:"p2"},{from:"p1",to:"loss"},{from:"p2",to:"loss"},
      {from:"e1",to:"out"},{from:"e2",to:"out"},
    ],
  };

  P.byol = {
    title: "BYOL (2020)",
    path: ["in","on_e","on_p","pred","loss"],
    nodes: [
      { id:"in",   name:"Input Image",      sub:"원본 이미지",     col:0,  row:0, vis:"img" },
      { id:"on_e", name:"Online Encoder",    sub:"f_θ",           col:-1, row:1, vis:"maps", detail:"학습됨" },
      { id:"tg_e", name:"Target Encoder",    sub:"f_ξ (EMA)",     col:1,  row:1, vis:"maps", detail:"ξ←τξ+(1-τ)θ" },
      { id:"on_p", name:"Online Projector",  sub:"g_θ → z",      col:-1, row:2, vis:"vec" },
      { id:"tg_p", name:"Target Projector",  sub:"g_ξ → z'",     col:1,  row:2, vis:"vec" },
      { id:"pred", name:"Predictor q_θ",     sub:"q(z) → p",     col:-1, row:3, vis:"dots", detail:"비대칭 핵심" },
      { id:"sg",   name:"Stop-Gradient",     sub:"sg(z')",        col:1,  row:3, vis:"dots" },
      { id:"loss", name:"MSE Loss",          sub:"‖p−sg(z')‖²",  col:0,  row:4, vis:"narrow" },
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
    path: ["pos","l1p","l2p","pred"],
    nodes: [
      { id:"pos", name:"Positive Input", sub:"데이터+정답",    col:-1, row:0, vis:"img" },
      { id:"neg", name:"Negative Input", sub:"데이터+오답",    col:1,  row:0, vis:"img" },
      { id:"l1p", name:"Layer 1",        sub:"goodness ↑",    col:-1, row:1, vis:"vec", detail:"Σ(aᵢ²)>θ" },
      { id:"l1n", name:"Layer 1",        sub:"goodness ↓",    col:1,  row:1, vis:"vec", detail:"Σ(aᵢ²)<θ" },
      { id:"l2p", name:"Layer 2",        sub:"goodness ↑",    col:-1, row:2, vis:"maps_s" },
      { id:"l2n", name:"Layer 2",        sub:"goodness ↓",    col:1,  row:2, vis:"maps_s" },
      { id:"pred",name:"Prediction",     sub:"argmax",        col:0,  row:3, vis:"bar" },
    ],
    edges: [
      {from:"pos",to:"l1p"},{from:"neg",to:"l1n"},{from:"l1p",to:"l2p"},{from:"l1n",to:"l2n"},
      {from:"l2p",to:"pred"},{from:"l2n",to:"pred"},
    ],
  };

  P.contrastive_divergence = {
    title: "Contrastive Divergence (2002)",
    path: ["v0","h0","v1","upd"],
    nodes: [
      { id:"v0",  name:"Data v⁰",         sub:"관측 데이터",    col:0,  row:0, vis:"img" },
      { id:"h0",  name:"Sample h⁰",       sub:"p(h|v⁰)",      col:0,  row:1, vis:"dots", detail:"v⁰에서 h⁰ 샘플링" },
      { id:"v1",  name:"Reconstruct v¹",   sub:"p(v|h⁰)",      col:0,  row:2, vis:"img",  detail:"깁스 1스텝" },
      { id:"pos", name:"Positive ⟨vh⟩⁰",   sub:"데이터 통계",   col:-1, row:3, vis:"vec" },
      { id:"neg", name:"Negative ⟨vh⟩¹",   sub:"모델 통계",     col:1,  row:3, vis:"vec" },
      { id:"upd", name:"ΔW ∝ pos − neg",   sub:"가중치 갱신",   col:0,  row:4, vis:"narrow" },
    ],
    edges: [
      {from:"v0",to:"h0",label:"p(h|v)"},{from:"h0",to:"v1",label:"p(v|h)"},
      {from:"v0",to:"pos"},{from:"h0",to:"pos"},{from:"v1",to:"neg"},
      {from:"pos",to:"upd",label:"+"},{from:"neg",to:"upd",label:"−"},
    ],
  };

  P.tsne = {
    title: "t-SNE (2008)",
    path: ["in","ph","lo","ql","kl","out"],
    nodes: [
      { id:"in",  name:"High-D Data",     sub:"n×D",           col:0, row:0, vis:"vec" },
      { id:"ph",  name:"Pairwise p_ij",   sub:"가우시안 커널",   col:0, row:1, vis:"maps",  detail:"가까운 점→높은 pᵢⱼ" },
      { id:"lo",  name:"Init Embedding",   sub:"n×2 랜덤",      col:0, row:2, vis:"dots" },
      { id:"ql",  name:"Student-t q_ij",   sub:"t분포 (df=1)",  col:0, row:3, vis:"dots",  detail:"긴 꼬리→crowding 해결" },
      { id:"kl",  name:"Minimize KL(P‖Q)", sub:"경사하강법",     col:0, row:4, vis:"dots" },
      { id:"out", name:"2D Visualization", sub:"n×2",           col:0, row:5, vis:"dots" },
    ],
    edges: [
      {from:"in",to:"ph",label:"가우시안"},{from:"ph",to:"lo"},
      {from:"lo",to:"ql",label:"t분포"},{from:"ql",to:"kl"},{from:"kl",to:"out",label:"반복"},
    ],
  };

  P.layernorm = {
    title: "Layer Normalization (2016)",
    path: ["in","st","nm","sc","out"],
    nodes: [
      { id:"in",  name:"Input Activation", sub:"H-dim vector", col:0, row:0, vis:"vec" },
      { id:"st",  name:"Compute μ, σ",     sub:"층 통계량",     col:0, row:1, vis:"narrow", detail:"배치가 아닌 층 단위" },
      { id:"nm",  name:"Normalize",        sub:"(a−μ)/σ",      col:0, row:2, vis:"vec" },
      { id:"sc",  name:"Scale & Shift",    sub:"γ·â + β",      col:0, row:3, vis:"vec",    detail:"학습 가능 γ, β" },
      { id:"out", name:"Output",           sub:"정규화 완료",    col:0, row:4, vis:"vec" },
    ],
    edges: [
      {from:"in",to:"st"},{from:"st",to:"nm"},{from:"nm",to:"sc"},{from:"sc",to:"out"},
    ],
  };

  P.rbm_relu = {
    title: "ReLU Improves RBM (2010)",
    path: ["in","new","cd","out"],
    nodes: [
      { id:"in",  name:"Visible (Input)",  sub:"실수값 입력",   col:0,  row:0, vis:"vec" },
      { id:"old", name:"Sigmoid RBM",      sub:"σ(Wx+b)",      col:-1, row:1, vis:"maps_s", detail:"포화 문제" },
      { id:"new", name:"NReLU",            sub:"max(0,x+ε)",   col:1,  row:1, vis:"maps",   detail:"무한 이진 유닛 근사" },
      { id:"cd",  name:"Contrastive Div.", sub:"CD-1",          col:0,  row:2, vis:"dots" },
      { id:"out", name:"Learned Features", sub:"개선된 표현",    col:0,  row:3, vis:"vec" },
    ],
    edges: [
      {from:"in",to:"old"},{from:"in",to:"new"},{from:"old",to:"cd"},{from:"new",to:"cd"},
      {from:"cd",to:"out"},
    ],
  };

  P.transformer_ae = {
    title: "Transforming Auto-encoders (2011)",
    path: ["in","rec","pos","gen","sum","out"],
    nodes: [
      { id:"in",  name:"Input Image",      sub:"이미지 패치",    col:0,  row:0, vis:"img" },
      { id:"rec", name:"Recognition",      sub:"pᵢ=σ(Wᵢx)",   col:-1, row:1, vis:"dots",  detail:"캡슐별 확률" },
      { id:"pos", name:"Pose+Transform",   sub:"Tᵢ(Δ)",        col:0,  row:2, vis:"dots",  detail:"이동/회전 적용" },
      { id:"gen", name:"Generation",       sub:"yᵢ=pᵢ·g(Tᵢ)", col:1,  row:1, vis:"maps",  detail:"변환된 포즈로 생성" },
      { id:"sum", name:"Sum Outputs",      sub:"Σ yᵢ",         col:0,  row:3, vis:"maps" },
      { id:"out", name:"Reconstruction",   sub:"변환된 이미지",   col:0,  row:4, vis:"img" },
    ],
    edges: [
      {from:"in",to:"rec"},{from:"rec",to:"pos"},{from:"pos",to:"gen"},
      {from:"gen",to:"sum"},{from:"sum",to:"out"},
    ],
  };

  /* ── 메인 렌더러 ── */
  function render(container) {
    var key = container.dataset.arch;
    if (!key || !P[key]) {
      container.innerHTML = "<p style='color:#999'>arch-flowchart: '"+key+"' 미지원</p>";
      return;
    }
    var arch = P[key], nodes = arch.nodes, edges = arch.edges;

    var minC=0, maxC=0, maxR=0;
    nodes.forEach(function(n) {
      if (n.col<minC) minC=n.col;
      if (n.col>maxC) maxC=n.col;
      if (n.row>maxR) maxR=n.row;
    });
    var cols = maxC-minC+1;
    var svgW = cols*COL_W+PAD*2;
    var svgH = (maxR+1)*ROW_H+PAD*2+28;

    var svg = sv("svg", {
      width:"100%", viewBox:"0 0 "+svgW+" "+svgH,
      style:"max-width:"+Math.min(svgW,600)+"px;display:block;margin:1.5em auto;",
    });

    svg.appendChild(tx(svgW/2, 20, arch.title, { size:"14", bold:true }));

    var posMap = {};
    function ncx(n) { return PAD+(n.col-minC)*COL_W+COL_W/2; }
    function ncy(n) { return 38+n.row*ROW_H+BOX_H/2; }
    nodes.forEach(function(n) { posMap[n.id]={cx:ncx(n),cy:ncy(n)}; });

    /* defs */
    var defs = sv("defs",{});
    var mk = sv("marker",{id:"ah-"+key,markerWidth:"7",markerHeight:"5",refX:"7",refY:"2.5",orient:"auto"});
    mk.appendChild(sv("path",{d:"M0,0 L7,2.5 L0,5 Z",fill:S.stroke}));
    defs.appendChild(mk);
    svg.appendChild(defs);

    /* 엣지 */
    edges.forEach(function(e) {
      var f=posMap[e.from], t=posMap[e.to];
      if (!f||!t) return;
      var dy=t.cy-f.cy, dx=t.cx-f.cx;
      var fy=f.cy+BOX_H/2, ty=t.cy-BOX_H/2, fx=f.cx, tx2=t.cx;
      if (Math.abs(dy)<ROW_H*0.3) {
        fx=dx>0?f.cx+BOX_W/2:f.cx-BOX_W/2;
        tx2=dx>0?t.cx-BOX_W/2:t.cx+BOX_W/2;
        fy=f.cy; ty=t.cy;
      }
      if (fx===tx2) {
        svg.appendChild(sv("line",{x1:fx,y1:fy,x2:tx2,y2:ty,
          stroke:S.stroke,"stroke-width":"1.2","marker-end":"url(#ah-"+key+")"}));
      } else {
        var midY=(fy+ty)/2;
        svg.appendChild(sv("path",{
          d:"M"+fx+","+fy+" C"+fx+","+midY+" "+tx2+","+midY+" "+tx2+","+ty,
          fill:"none",stroke:S.stroke,"stroke-width":"1.2","marker-end":"url(#ah-"+key+")"}));
      }
      if (e.label) {
        var lx=(fx+tx2)/2, ly=(fy+ty)/2;
        svg.appendChild(sv("rect",{x:lx-e.label.length*3.5-3,y:ly-7,
          width:e.label.length*7+6,height:14,fill:"#fff",rx:"3"}));
        svg.appendChild(tx(lx,ly+3.5,e.label,{size:"9",fill:S.textSub}));
      }
    });

    /* 툴팁 */
    var tooltip = document.createElement("div");
    Object.assign(tooltip.style, {
      position:"absolute",padding:"8px 14px",background:"#222",color:"#fff",
      borderRadius:"6px",fontSize:"13px",lineHeight:"1.5",
      pointerEvents:"none",opacity:"0",transition:"opacity 0.15s",
      zIndex:"9999",maxWidth:"260px",whiteSpace:"pre-wrap",
      fontFamily:S.font,left:"50%",transform:"translateX(-50%)",
    });
    container.style.position = "relative";
    container.appendChild(tooltip);
    document.addEventListener("click",function(ev){
      if (!container.contains(ev.target)) tooltip.style.opacity="0";
    });

    /* 노드 */
    nodes.forEach(function(n) {
      var cx=posMap[n.id].cx, cy=posMap[n.id].cy;
      var x=cx-BOX_W/2, y=cy-BOX_H/2;
      var g=sv("g",{style:"cursor:pointer"});

      g.appendChild(sv("rect",{
        x:x,y:y,width:BOX_W,height:BOX_H,rx:R,ry:R,
        fill:n.filter?S.fillAlt:S.fill,stroke:S.stroke,"stroke-width":"1.2",
      }));
      g.appendChild(tx(cx,cy-8,n.name,{size:"12",bold:true}));
      g.appendChild(tx(cx,cy+6,n.sub,{size:"10",fill:S.textSub}));

      if (n.filter) drawFilter(g,x+BOX_W-18,y+14,n.filter[0],n.filter[1]);

      /* 인터랙션 */
      var rect=g.querySelector("rect");
      function showTip(){
        if(!n.detail)return;
        tooltip.textContent=n.name+"\n"+n.detail;
        var sr=svg.getBoundingClientRect(),cr=container.getBoundingClientRect();
        tooltip.style.top=(sr.top-cr.top+(cy+BOX_H/2)*(sr.height/svgH)+6)+"px";
        tooltip.style.opacity="1"; rect.setAttribute("stroke-width","2");
      }
      function hideTip(){
        tooltip.style.opacity="0"; rect.setAttribute("stroke-width","1.2");
      }
      g.addEventListener("mouseenter",showTip);
      g.addEventListener("mouseleave",hideTip);
      g.addEventListener("click",function(ev){
        ev.stopPropagation();
        if(!n.detail)return;
        tooltip.style.opacity==="1"?hideTip():showTip();
      });

      svg.appendChild(g);
    });

    /* ── 데이터 흐름 애니메이션 ── */
    if (arch.path && arch.path.length > 1) {
      var nodeMap = {};
      nodes.forEach(function(n){ nodeMap[n.id]=n; });

      var tokenG = sv("g",{"pointer-events":"none"});
      svg.appendChild(tokenG);

      var pathNodes = arch.path.map(function(id){ return nodeMap[id]; }).filter(Boolean);
      var step = 0, t = 0;
      var SPEED = 0.012; /* 프레임당 진행률 */
      var PAUSE = 40;    /* 노드 도착 후 대기 프레임 */
      var pauseCount = 0;

      function animateStep() {
        if (step >= pathNodes.length - 1) { step = 0; t = 0; pauseCount = PAUSE; }

        var from = pathNodes[step], to = pathNodes[step + 1];
        var fp = posMap[from.id], tp = posMap[to.id];
        var cx = fp.cx + (tp.cx - fp.cx) * t;
        var cy = fp.cy + (tp.cy - fp.cy) * t;

        /* 현재 vis 타입: 출발점에서 시작, 50% 넘으면 도착점 vis */
        var currentNode = t < 0.5 ? from : to;

        /* 토큰 그리기 */
        while (tokenG.firstChild) tokenG.removeChild(tokenG.firstChild);

        /* 배경 원 */
        tokenG.appendChild(sv("circle",{
          cx:cx, cy:cy, r:"16", fill:S.accent, opacity:"0.12",
        }));

        if (currentNode.vis) {
          drawVis(tokenG, cx, cy, currentNode.vis, S.accent);
        }

        if (pauseCount > 0) {
          pauseCount--;
        } else {
          t += SPEED;
          if (t >= 1) { t = 0; step++; pauseCount = PAUSE; }
        }

        requestAnimationFrame(animateStep);
      }

      /* Intersection Observer: 뷰포트에 있을 때만 애니메이션 */
      var animRunning = false;
      function startAnim() {
        if (!animRunning) { animRunning = true; requestAnimationFrame(animateStep); }
      }

      if (typeof IntersectionObserver !== "undefined") {
        var obs = new IntersectionObserver(function(entries) {
          if (entries[0].isIntersecting) startAnim();
          else animRunning = false;
        }, { threshold: 0.1 });
        /* container가 아직 DOM에 안 붙어있을 수 있으므로 svg 관찰 */
        setTimeout(function(){ obs.observe(container); }, 100);
      } else {
        startAnim();
      }
    }

    container.innerHTML = "";
    container.appendChild(svg);
  }

  /* ── 초기화 ── */
  function init() { document.querySelectorAll(".arch-flow").forEach(render); }
  if (document.readyState==="loading") document.addEventListener("DOMContentLoaded",init);
  else init();
})();
