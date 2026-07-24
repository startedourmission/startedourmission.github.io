// 인물 지도(Maps) 렌더러 — assets/people-roadmap.json 을 읽어 버블 맵으로 그린다.
// 원 하나 = 인물, 원 크기 = 주목도(★), 색 = 섹터, 클릭 → 인물 노트.
// 라이브러리 없이 순수 SVG + vanilla JS. 데이터는 수작업 큐레이션된 정적 파일.
(function () {
  "use strict";
  var DATA_URL = "assets/people-roadmap.json";
  var SVGNS = "http://www.w3.org/2000/svg";

  // 섹터별 색 — 노트 링크(--color-link)와 충돌하지 않는 구분 팔레트.
  var SECTOR_COLORS = {
    frontier: "#4f8cff",
    company: "#22b8a6",
    hardware: "#f2a13d",
    academia: "#a970ff",
    agile: "#e0607e"
  };
  var FALLBACK_COLORS = ["#4f8cff", "#22b8a6", "#f2a13d", "#a970ff", "#e0607e", "#d98a3d"];

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function svg(tag, attrs) {
    var e = document.createElementNS(SVGNS, tag);
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }

  function sectorColor(key, idx) {
    return SECTOR_COLORS[key] || FALLBACK_COLORS[idx % FALLBACK_COLORS.length];
  }

  // ★ → 반지름. 면적 대신 sqrt 스케일 + 클램프로 큰 값(226)이 화면을 잡아먹지 않게.
  function radiusFor(star, minStar, maxStar) {
    var R_MIN = 15, R_MAX = 46;
    if (maxStar <= minStar) return (R_MIN + R_MAX) / 2;
    var t = (Math.sqrt(star) - Math.sqrt(minStar)) / (Math.sqrt(maxStar) - Math.sqrt(minStar));
    return R_MIN + t * (R_MAX - R_MIN);
  }

  // 섹터별로 인물을 묶어 반환한다: [{key,label,color,people:[...]}].
  function groupBySector(data) {
    return data.sectors.map(function (s, si) {
      var color = sectorColor(s.key, si);
      var people = [];
      s.orgs.forEach(function (o) {
        o.members.forEach(function (m) {
          people.push({
            name: m.name,
            url: m.url,
            org: o.org,
            star: typeof m.star === "number" ? m.star : 0,
            tagline: m.tagline || "",
            sectorKey: s.key,
            sectorLabel: s.label,
            color: color
          });
        });
      });
      return { key: s.key, label: s.label, color: color, people: people };
    });
  }

  // 결정론적 원 패킹: 큰 원(items[i].r)부터 (cx,cy) 중심 아르키메데스 나선을 촘촘히 돌며
  // 겹치지 않는 첫 자리에 놓고 n.x/n.y를 채운다. 라이브러리 없이 동작하고 매번 같은 배치(랜덤 없음).
  // 나선 표본 간 호 길이를 일정하게 유지(각도 증분을 반경에 반비례)해 빈틈을 남기지 않는다.
  // opts: {pad, b, stepArc, bound:{w,h,inset}} — bound가 있으면 그 사각형 안에만 배치.
  function spiralPack(items, cx, cy, opts) {
    opts = opts || {};
    var PAD = opts.pad != null ? opts.pad : 3;
    var B = opts.b != null ? opts.b : 1.6;
    var STEP_ARC = opts.stepArc != null ? opts.stepArc : 4;
    var bound = opts.bound || null;
    var placed = [];
    var sorted = items.slice().sort(function (a, b) { return b.r - a.r; });
    sorted.forEach(function (n) {
      var t = 0, done = false;
      for (var i = 0; i < 400000; i++) {
        var rad = B * t;
        var x = cx + rad * Math.cos(t);
        var y = cy + rad * Math.sin(t);
        var ok = true;
        if (bound) {
          var ins = bound.inset || 0;
          if (x - n.r < ins || x + n.r > bound.w - ins || y - n.r < ins || y + n.r > bound.h - ins) ok = false;
        }
        if (ok) {
          for (var j = 0; j < placed.length; j++) {
            var p = placed[j];
            var dx = x - p.x, dy = y - p.y, s = n.r + p.r + PAD;
            if (dx * dx + dy * dy < s * s) { ok = false; break; }
          }
        }
        if (ok) { n.x = x; n.y = y; placed.push(n); done = true; break; }
        t += STEP_ARC / Math.max(B * Math.sqrt(1 + t * t), 1);
      }
      if (!done) { n.x = cx; n.y = cy; placed.push(n); }
    });
    return sorted;
  }

  // 섹터별 클러스터 레이아웃: (1) 각 섹터 인물을 로컬 중심(0,0) 기준 패킹해 클러스터 반경 R을
  // 구하고, (2) 그 클러스터들을 다시 나선 패킹해 서로 안 겹치는 중심을 잡은 뒤, (3) 인물 좌표에
  // 클러스터 중심 오프셋을 더한다. 같은 알고리즘을 두 레벨에 재사용 → 섹터가 공간적으로 뭉친다.
  // 반환: {people, clusters, bbox:{minX,minY,maxX,maxY}}
  function layoutClusters(sectorsData) {
    var LABEL_GAP = 26;  // 섹터 라벨(위쪽 바깥)이 이웃 클러스터와 겹치지 않도록 확보할 세로 여백.
    var clusters = sectorsData.map(function (s) {
      var nodes = s.people.map(function (p) { return { ref: p, r: p.r }; });
      spiralPack(nodes, 0, 0, { pad: 3, b: 1.5, stepArc: 3.5 });
      var R = 0;
      nodes.forEach(function (n) {
        var d = Math.hypot(n.x, n.y) + n.r;
        if (d > R) R = d;
      });
      // 패킹용 반경 r 은 라벨 여백을 포함(클러스터 간 간격 확보). 실제 헤일로 반경 R 은 그대로.
      return { key: s.key, label: s.label, color: s.color, R: R, r: R + LABEL_GAP, nodes: nodes };
    });

    // 클러스터 원들을 나선 패킹(라벨 여백 포함 반경 기준).
    spiralPack(clusters, 0, 0, { pad: 14, b: 3, stepArc: 4 });

    // 인물 절대좌표 = 로컬 + 클러스터 중심.
    var people = [];
    var bbox = { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity };
    clusters.forEach(function (c) {
      c.nodes.forEach(function (n) {
        n.ref.x = n.x + c.x;
        n.ref.y = n.y + c.y;
        people.push(n.ref);
      });
      bbox.minX = Math.min(bbox.minX, c.x - c.R);
      bbox.minY = Math.min(bbox.minY, c.y - c.R - 24);  // 위쪽 섹터 라벨 공간.
      bbox.maxX = Math.max(bbox.maxX, c.x + c.R);
      bbox.maxY = Math.max(bbox.maxY, c.y + c.R);
    });
    return { people: people, clusters: clusters, bbox: bbox };
  }

  function buildTooltip() {
    var tip = el("div", "rm-tip");
    tip.style.display = "none";
    document.body.appendChild(tip);
    return tip;
  }

  function showTip(tip, node, evt) {
    tip.innerHTML = "";
    var name = el("div", "rm-tip-name", node.name);
    tip.appendChild(name);
    var meta = el("div", "rm-tip-org");
    meta.appendChild(el("span", "rm-tip-dot"));
    meta.lastChild.style.background = node.color;
    meta.appendChild(document.createTextNode(" " + node.org));
    tip.appendChild(meta);
    if (node.tagline) tip.appendChild(el("div", "rm-tip-tag", node.tagline));
    tip.appendChild(el("div", "rm-tip-star", "★ " + node.star + " · " + node.sectorLabel));
    tip.style.display = "block";
    moveTip(tip, evt);
  }
  function moveTip(tip, evt) {
    var pad = 14;
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var x = evt.clientX + pad, y = evt.clientY + pad;
    if (x + w > window.innerWidth - 8) x = evt.clientX - w - pad;
    if (y + h > window.innerHeight - 8) y = evt.clientY - h - pad;
    tip.style.left = x + "px";
    tip.style.top = y + "px";
  }

  function renderLegend(data) {
    var wrap = el("div", "rm-legend");
    data.sectors.forEach(function (s, si) {
      var n = s.orgs.reduce(function (a, o) { return a + o.members.length; }, 0);
      var item = el("span", "rm-legend-item");
      var dot = el("span", "rm-legend-dot");
      dot.style.background = sectorColor(s.key, si);
      item.appendChild(dot);
      item.appendChild(document.createTextNode(s.label + " (" + n + ")"));
      wrap.appendChild(item);
    });
    return wrap;
  }

  // 원 안 이름 라벨. 반지름에 맞춰 한 줄/두 줄/성만/폰트축소를 결정해 원 밖으로 새지 않게 한다.
  // 한글 글자폭 ≈ fontSize, 원 안 가용 폭 ≈ 2r*0.86 (여유), 두 줄이면 세로도 확인.
  function makeLabel(p) {
    var label = svg("text", {
      x: p.x, y: p.y, "class": "rm-bubble-label",
      "text-anchor": "middle", "dominant-baseline": "central"
    });
    var parts = p.name.split(" ");
    var maxFont = Math.max(8, Math.min(15, p.r * 0.5));
    var avail = 2 * p.r * 0.86;          // 한 줄 가용 폭
    var CW = 0.98;                        // 글자당 폭 계수(한글)

    function widthOf(str, f) { return str.length * f * CW; }

    // 후보 1: 이름 전체 한 줄
    var oneLineFont = Math.min(maxFont, avail / (widthOf(p.name, 1) || 1));
    if (oneLineFont >= 8.5) {
      label.setAttribute("font-size", Math.min(maxFont, oneLineFont));
      label.textContent = p.name;
      return label;
    }
    // 후보 2: 공백 기준 두 줄 (각 줄이 avail 안에 들어오고 세로 2줄이 원 높이 안이면)
    if (parts.length > 1) {
      var longest = parts.reduce(function (a, b) { return b.length > a.length ? b : a; });
      var line2 = parts.slice(1).join(" ");
      var widest = Math.max(parts[0].length, line2.length);
      var twoLineFont = Math.min(maxFont, avail / (widest * CW));
      // 두 줄 세로 = 2*font*1.05 이 2r*0.9 안에 들어와야
      if (twoLineFont >= 8 && twoLineFont * 2 * 1.05 <= 2 * p.r * 0.92) {
        label.setAttribute("font-size", twoLineFont);
        var t1 = svg("tspan", { x: p.x, dy: "-0.55em" }); t1.textContent = parts[0];
        var t2 = svg("tspan", { x: p.x, dy: "1.1em" }); t2.textContent = line2;
        label.appendChild(t1); label.appendChild(t2);
        return label;
      }
      // 후보 3: 가장 긴 파트(성 등)만 한 줄
      var partFont = Math.min(maxFont, avail / (longest.length * CW));
      label.setAttribute("font-size", Math.max(8, partFont));
      label.textContent = longest;
      return label;
    }
    // 후보 4: 외자 이름인데 좁음 — 폰트를 최소로 축소해서라도 원 안에.
    label.setAttribute("font-size", Math.max(7.5, avail / (widthOf(p.name, 1) || 1)));
    label.textContent = p.name;
    return label;
  }

  function renderBubbleMap(sectors, people, tip) {
    var minStar = Math.min.apply(null, people.map(function (p) { return p.star || 1; }));
    var maxStar = Math.max.apply(null, people.map(function (p) { return p.star; }));
    people.forEach(function (p) { p.r = radiusFor(p.star || minStar, minStar, maxStar); });

    // 섹터별 클러스터 레이아웃(2단계 나선 패킹).
    var layout = layoutClusters(sectors);
    var clusters = layout.clusters;
    var bb = layout.bbox;

    // viewBox: bbox(섹터 라벨 공간 포함) + 여백.
    var PAD = 24;
    var vbX = bb.minX - PAD, vbY = bb.minY - PAD;
    var vbW = (bb.maxX - bb.minX) + 2 * PAD;
    var vbH = (bb.maxY - bb.minY) + 2 * PAD;

    var wrap = el("div", "rm-map-wrap");
    var s = svg("svg", {
      "class": "rm-map",
      viewBox: vbX + " " + vbY + " " + vbW + " " + vbH,
      preserveAspectRatio: "xMidYMid meet",
      role: "img",
      "aria-label": "주목 연구자 섹터별 버블 맵"
    });

    // 1) 클러스터 배경 헤일로(옅은 섹터 색 원)와 섹터 라벨.
    var haloLayer = svg("g", { "class": "rm-halo-layer" });
    clusters.forEach(function (c) {
      haloLayer.appendChild(svg("circle", {
        cx: c.x, cy: c.y, r: c.R + 10,
        fill: c.color, "fill-opacity": "0.07",
        stroke: c.color, "stroke-opacity": "0.28", "stroke-width": "1"
      }));
      // 섹터 라벨 — 클러스터 위쪽 가장자리 바깥.
      var lab = svg("text", {
        x: c.x, y: c.y - c.R - 12,
        "class": "rm-cluster-label",
        "text-anchor": "middle", fill: c.color
      });
      lab.textContent = c.label;
      haloLayer.appendChild(lab);
    });
    s.appendChild(haloLayer);

    // 2) 인물 원.
    people.forEach(function (p) {
      var a = svg("a", { href: p.url });
      a.setAttribute("tabindex", "0");
      var g = svg("g", { "class": "rm-bubble" });

      g.appendChild(svg("circle", {
        cx: p.x, cy: p.y, r: p.r,
        fill: p.color, "fill-opacity": "0.85",
        stroke: p.color, "stroke-width": "1.5"
      }));
      g.appendChild(makeLabel(p));

      g.addEventListener("mouseenter", function (e) { showTip(tip, p, e); });
      g.addEventListener("mousemove", function (e) { moveTip(tip, e); });
      g.addEventListener("mouseleave", function () { tip.style.display = "none"; });
      a.addEventListener("focus", function () {
        var box = s.getBoundingClientRect();
        var scale = box.width / vbW;
        showTip(tip, p, {
          clientX: box.left + (p.x - vbX) * scale,
          clientY: box.top + (p.y - vbY) * scale
        });
      });
      a.addEventListener("blur", function () { tip.style.display = "none"; });

      a.appendChild(g);
      s.appendChild(a);
    });

    wrap.appendChild(s);
    return wrap;
  }

  // 접근성·SEO·폴백용 카드 목록 (기존 레이아웃 유지, 지도 아래 접힘).
  function renderMember(m) {
    var li = el("li", "rm-member");
    var a = el("a", null, m.name);
    a.href = m.url;
    li.appendChild(a);
    if (typeof m.star === "number" && m.star > 0) li.appendChild(el("span", "rm-star", "★ " + m.star));
    if (m.tagline) li.appendChild(el("span", "rm-tag", m.tagline));
    return li;
  }
  function renderOrg(o) {
    var card = el("div", "rm-card");
    var head = el("div", "rm-card-head");
    head.appendChild(el("span", "rm-org", o.org));
    head.appendChild(el("span", "rm-badge", o.count + "명"));
    card.appendChild(head);
    var ul = el("ul", "rm-members");
    o.members.forEach(function (m) { ul.appendChild(renderMember(m)); });
    card.appendChild(ul);
    return card;
  }
  function renderSector(s, si) {
    var wrap = el("div", "rm-sector");
    var head = el("div", "rm-sector-head");
    var dot = el("span", "rm-sector-dot");
    dot.style.background = sectorColor(s.key, si);
    head.appendChild(dot);
    head.appendChild(el("h2", null, s.label));
    var n = s.orgs.reduce(function (acc, o) { return acc + o.count; }, 0);
    head.appendChild(el("span", "rm-sector-count", n + "명 · " + s.orgs.length + "곳"));
    wrap.appendChild(head);
    var grid = el("div", "rm-grid");
    s.orgs.forEach(function (o) { grid.appendChild(renderOrg(o)); });
    wrap.appendChild(grid);
    return wrap;
  }

  function render(data) {
    var root = document.getElementById("rm-root");
    if (!root) return;
    root.innerHTML = "";

    var asof = document.getElementById("rm-asof");
    if (asof) {
      asof.textContent = "기준 " + (data.generated || "") +
        " · 주목도(★) " + data.threshold + " 이상 " + data.total + "명";
    }

    var sectors = groupBySector(data);
    var people = sectors.reduce(function (acc, s) { return acc.concat(s.people); }, []);
    var tip = buildTooltip();

    // 1) 레전드
    root.appendChild(renderLegend(data));
    // 2) 섹터별 클러스터 버블 맵
    root.appendChild(renderBubbleMap(sectors, people, tip));

    // 3) 폴백 카드 목록 — 기본 접힘, 토글로 펼침.
    var details = el("details", "rm-list-toggle");
    var summary = el("summary", null, "소속별 목록으로 보기");
    details.appendChild(summary);
    var listWrap = el("div", "rm-list");
    data.sectors.forEach(function (s, si) { listWrap.appendChild(renderSector(s, si)); });
    details.appendChild(listWrap);
    root.appendChild(details);
  }

  fetch(DATA_URL)
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(render)
    .catch(function (err) {
      var root = document.getElementById("rm-root");
      if (root) {
        root.innerHTML = "";
        root.appendChild(el("p", "rm-status", "데이터를 불러오지 못했습니다: " + err.message));
      }
    });
})();
