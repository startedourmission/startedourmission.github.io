// 인물 지도(Maps) 렌더러 — assets/people-roadmap.json 을 읽어 버블 맵으로 그린다.
// 원 하나 = 인물, 원 크기 = 주목도(★), 클릭 → 인물 노트.
// 묶음은 3단이다: 인물 → 조직(OpenAI·MIT·Shanghai AI Lab 처럼 구체적으로) → 섹터(조직의 종류).
// 라이브러리 없이 순수 SVG + vanilla JS. 데이터는 tools/gen_people_roadmap.py 가 생성한다.
(function () {
  "use strict";
  var DATA_URL = "assets/people-roadmap.json";
  var SVGNS = "http://www.w3.org/2000/svg";

  // 섹터별 색 — 노트 링크(--color-link)와 충돌하지 않는 구분 팔레트.
  var SECTOR_COLORS = {
    frontier: "#4f8cff",
    bigtech: "#6fb3ff",
    company: "#22b8a6",
    hardware: "#f2a13d",
    institute: "#e0607e",
    university: "#a970ff",
    method: "#9aa4b2"
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

  // 같은 섹터 안에서도 조직끼리 구분되도록 명도를 조금씩 흔든다(-10% ~ +10%).
  function shade(hex, t) {
    var n = parseInt(hex.slice(1), 16);
    var r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    function mix(c) {
      var v = t >= 0 ? c + (255 - c) * t : c * (1 + t);
      return Math.max(0, Math.min(255, Math.round(v)));
    }
    return "#" + ((1 << 24) + (mix(r) << 16) + (mix(g) << 8) + mix(b)).toString(16).slice(1);
  }
  function orgShade(color, idx, total) {
    if (total <= 1) return color;
    var t = -0.1 + 0.2 * (idx / (total - 1));
    return shade(color, t);
  }

  // ★ → 반지름. 면적 대신 sqrt 스케일 + 클램프로 큰 값(226)이 화면을 잡아먹지 않게.
  function radiusFor(star, minStar, maxStar) {
    var R_MIN = 15, R_MAX = 46;
    if (maxStar <= minStar) return (R_MIN + R_MAX) / 2;
    var t = (Math.sqrt(star) - Math.sqrt(minStar)) / (Math.sqrt(maxStar) - Math.sqrt(minStar));
    return R_MIN + t * (R_MAX - R_MIN);
  }

  // JSON → [{key,label,color,orgs:[{org,color,people:[...]}]}]. 인물 객체는 여기서 한 번만 만든다.
  function groupByOrg(data) {
    return data.sectors.map(function (s, si) {
      var base = sectorColor(s.key, si);
      var orgs = s.orgs.map(function (o, oi) {
        var color = orgShade(base, oi, s.orgs.length);
        var people = o.members.map(function (m) {
          return {
            name: m.name,
            url: m.url,
            org: o.org,
            also: m.also || "",
            star: typeof m.star === "number" ? m.star : 0,
            tagline: m.tagline || "",
            sectorKey: s.key,
            sectorLabel: s.label,
            color: color
          };
        });
        return { org: o.org, color: color, people: people };
      });
      return { key: s.key, label: s.label, color: base, orgs: orgs };
    });
  }

  // 결정론적 원 패킹: 큰 원(items[i].r)부터 (cx,cy) 중심 아르키메데스 나선을 촘촘히 돌며
  // 겹치지 않는 첫 자리에 놓고 n.x/n.y를 채운다. 라이브러리 없이 동작하고 매번 같은 배치(랜덤 없음).
  // 나선 표본 간 호 길이를 일정하게 유지(각도 증분을 반경에 반비례)해 빈틈을 남기지 않는다.
  // opts.aspect > 1 이면 나선을 가로로 늘여 결과가 와이드 화면에 맞는 비율로 퍼진다
  // (후보 좌표만 타원으로 뿌릴 뿐 충돌 판정은 그대로 원 기준이라 겹침은 생기지 않는다).
  function spiralPack(items, cx, cy, opts) {
    opts = opts || {};
    var PAD = opts.pad != null ? opts.pad : 3;
    var B = opts.b != null ? opts.b : 1.6;
    var STEP_ARC = opts.stepArc != null ? opts.stepArc : 4;
    var ASPECT = opts.aspect != null ? opts.aspect : 1;
    var placed = [];
    var sorted = items.slice().sort(function (a, b) { return b.r - a.r; });
    sorted.forEach(function (n) {
      var t = 0, done = false;
      for (var i = 0; i < 400000; i++) {
        var rad = B * t;
        var x = cx + ASPECT * rad * Math.cos(t);
        var y = cy + rad * Math.sin(t);
        var ok = true;
        for (var j = 0; j < placed.length; j++) {
          var p = placed[j];
          var dx = x - p.x, dy = y - p.y, s = n.r + p.r + PAD;
          if (dx * dx + dy * dy < s * s) { ok = false; break; }
        }
        if (ok) { n.x = x; n.y = y; placed.push(n); done = true; break; }
        t += STEP_ARC / Math.max(B * Math.sqrt(1 + t * t), 1);
      }
      if (!done) { n.x = cx; n.y = cy; placed.push(n); }
    });
    return sorted;
  }

  // 로컬 (0,0) 기준으로 배치된 노드들을 감싸는 반경.
  function enclosingRadius(nodes, extra) {
    var pad = extra || 0;
    var R = 0;
    nodes.forEach(function (n) {
      var d = Math.hypot(n.x, n.y) + n.r + pad;
      if (d > R) R = d;
    });
    return R;
  }

  // 3단 레이아웃: (1) 조직 안에서 인물 패킹 → 조직 반경, (2) 섹터 안에서 조직 패킹 → 섹터 반경,
  // (3) 섹터들을 캔버스에 패킹. 같은 나선 패커를 세 레벨에 재사용한다.
  // 반환: {people, orgs, sectors, bbox}
  // SVG 텍스트 폭 어림 — 한글은 폰트 크기만큼, 라틴 문자는 그 55% 정도를 차지한다.
  function textWidth(str, fontSize) {
    var w = 0;
    for (var i = 0; i < str.length; i++) {
      w += str.charCodeAt(i) > 0x2000 ? 1 : 0.55;
    }
    return w * fontSize;
  }

  function layoutMap(sectorsData) {
    var ORG_LABEL_GAP = 16;     // 조직 이름표(아래쪽 바깥)를 위한 여백.
    var ORG_LABEL_FONT = 10.5;  // .rm-org-label 과 맞춰둘 것.
    var SECTOR_LABEL_GAP = 30;  // 섹터 이름표(위쪽 바깥)를 위한 여백.

    var sectors = sectorsData.map(function (s) {
      var orgs = s.orgs.map(function (o) {
        var nodes = o.people.map(function (p) { return { ref: p, r: p.r }; });
        spiralPack(nodes, 0, 0, { pad: 3, b: 1.5, stepArc: 3.5 });
        var R = enclosingRadius(nodes);
        // 패킹용 반경 r 은 이름표 여백을 포함, 실제 테두리 반경 R 은 그대로.
        // 이름이 원보다 넓으면(Thinking Machines Lab 등) 글자 폭만큼 자리를 더 잡아둔다.
        var half = textWidth(o.org, ORG_LABEL_FONT) / 2 + 6;
        return {
          org: o.org, color: o.color, R: R,
          r: Math.max(R + ORG_LABEL_GAP, half), nodes: nodes
        };
      });
      spiralPack(orgs, 0, 0, { pad: 8, b: 2.4, stepArc: 4, aspect: 1.3 });
      var R = enclosingRadius(orgs.map(function (o) {
        return { x: o.x, y: o.y, r: o.r };
      }));
      return { key: s.key, label: s.label, color: s.color, R: R, r: R + SECTOR_LABEL_GAP, orgs: orgs };
    });

    spiralPack(sectors, 0, 0, { pad: 18, b: 4, stepArc: 5, aspect: 1.5 });

    var people = [];
    var allOrgs = [];
    var bbox = { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity };
    sectors.forEach(function (s) {
      s.orgs.forEach(function (o) {
        o.absX = o.x + s.x;
        o.absY = o.y + s.y;
        allOrgs.push(o);
        o.nodes.forEach(function (n) {
          n.ref.x = n.x + o.absX;
          n.ref.y = n.y + o.absY;
          people.push(n.ref);
        });
      });
      bbox.minX = Math.min(bbox.minX, s.x - s.R);
      bbox.minY = Math.min(bbox.minY, s.y - s.R - 26);  // 위쪽 섹터 이름표 공간.
      bbox.maxX = Math.max(bbox.maxX, s.x + s.R);
      bbox.maxY = Math.max(bbox.maxY, s.y + s.R);
    });
    return { people: people, orgs: allOrgs, sectors: sectors, bbox: bbox };
  }

  function buildTooltip() {
    var tip = el("div", "rm-tip");
    tip.style.display = "none";
    document.body.appendChild(tip);
    return tip;
  }

  function showTip(tip, node, evt) {
    tip.innerHTML = "";
    tip.appendChild(el("div", "rm-tip-name", node.name));
    var meta = el("div", "rm-tip-org");
    var dot = el("span", "rm-tip-dot");
    dot.style.background = node.color;
    meta.appendChild(dot);
    meta.appendChild(document.createTextNode(" " + node.org));
    tip.appendChild(meta);
    if (node.also) tip.appendChild(el("div", "rm-tip-also", "겸직 · " + node.also));
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
      var n = s.count != null ? s.count
        : s.orgs.reduce(function (a, o) { return a + o.members.length; }, 0);
      var orgs = s.orgCount != null ? s.orgCount : s.orgs.length;
      var item = el("span", "rm-legend-item");
      var dot = el("span", "rm-legend-dot");
      dot.style.background = sectorColor(s.key, si);
      item.appendChild(dot);
      item.appendChild(document.createTextNode(s.label + " " + orgs + "곳 · " + n + "명"));
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

    var layout = layoutMap(sectors);
    var bb = layout.bbox;

    // viewBox: bbox(섹터 이름표 공간 포함) + 여백.
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
      "aria-label": "주목 연구자 조직별 버블 맵"
    });

    // 1) 섹터 영역 — 옅은 점선 바탕과 위쪽 이름표.
    var sectorLayer = svg("g", { "class": "rm-halo-layer" });
    layout.sectors.forEach(function (sec) {
      sectorLayer.appendChild(svg("circle", {
        cx: sec.x, cy: sec.y, r: sec.R + 10,
        fill: sec.color, "fill-opacity": "0.05",
        stroke: sec.color, "stroke-opacity": "0.22", "stroke-width": "1",
        "stroke-dasharray": "6 5"
      }));
      var lab = svg("text", {
        x: sec.x, y: sec.y - sec.R - 14,
        "class": "rm-sector-label", "text-anchor": "middle", fill: sec.color
      });
      lab.textContent = sec.label;
      sectorLayer.appendChild(lab);
    });
    s.appendChild(sectorLayer);

    // 2) 조직 영역 — 실선 테두리와 아래쪽 이름표. 지도의 실제 구분 단위다.
    var orgLayer = svg("g", { "class": "rm-halo-layer" });
    layout.orgs.forEach(function (o) {
      orgLayer.appendChild(svg("circle", {
        cx: o.absX, cy: o.absY, r: o.R + 5,
        fill: o.color, "fill-opacity": "0.09",
        stroke: o.color, "stroke-opacity": "0.5", "stroke-width": "1"
      }));
      var lab = svg("text", {
        x: o.absX, y: o.absY + o.R + 15,
        "class": "rm-org-label", "text-anchor": "middle", fill: o.color
      });
      lab.textContent = o.org;
      orgLayer.appendChild(lab);
    });
    s.appendChild(orgLayer);

    // 3) 인물 원.
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
    if (m.also) li.appendChild(el("span", "rm-also", "겸직 " + m.also));
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
    head.appendChild(el("span", "rm-sector-count", s.orgs.length + "곳 · " + n + "명"));
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
      var orgTotal = data.orgTotal != null ? data.orgTotal
        : data.sectors.reduce(function (a, s) { return a + s.orgs.length; }, 0);
      asof.textContent = "기준 " + (data.generated || "") +
        " · 주목도(★) " + data.threshold + " 이상 " + data.total + "명 · " + orgTotal + "개 조직";
    }

    var sectors = groupByOrg(data);
    var people = sectors.reduce(function (acc, s) {
      return s.orgs.reduce(function (a2, o) { return a2.concat(o.people); }, acc);
    }, []);
    var tip = buildTooltip();

    // 1) 레전드
    root.appendChild(renderLegend(data));
    // 2) 조직 단위 클러스터 버블 맵(3단 나선 패킹)
    root.appendChild(renderBubbleMap(sectors, people, tip));

    // 3) 폴백 카드 목록 — 기본 접힘, 토글로 펼침.
    var details = el("details", "rm-list-toggle");
    details.appendChild(el("summary", null, "소속별 목록으로 보기"));
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
