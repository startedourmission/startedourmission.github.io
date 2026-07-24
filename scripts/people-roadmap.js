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

  // 인물을 flat 배열로 펴고 섹터 메타를 붙인다.
  function flatten(data) {
    var people = [];
    data.sectors.forEach(function (s, si) {
      var color = sectorColor(s.key, si);
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
    });
    return people;
  }

  // 결정론적 원 패킹: 큰 원부터 아르키메데스 나선을 촘촘히 돌며 겹치지 않는
  // 첫 자리에 놓는다. 라이브러리 없이 동작하고 매번 같은 배치를 만든다(랜덤 없음).
  // 나선 위 표본 간 호 길이를 일정하게 유지해(각도 증분을 반경에 반비례) 빈틈을 남기지 않는다.
  function packCircles(nodes, width, height) {
    var placed = [];
    var cx = width / 2, cy = height / 2;
    var sorted = nodes.slice().sort(function (a, b) { return b.r - a.r; });
    var PAD = 3;
    var B = 1.6;        // 나선 촘촘함(작을수록 촘촘)
    var STEP_ARC = 4;   // 표본 간 대략적인 호 길이(px)
    var maxRad = Math.sqrt(width * width + height * height);
    sorted.forEach(function (n) {
      var t = 0, done = false;
      for (var i = 0; i < 200000; i++) {
        var rad = B * t;
        var x = cx + rad * Math.cos(t);
        var y = cy + rad * Math.sin(t);
        var ok = true;
        if (x - n.r < 4 || x + n.r > width - 4 || y - n.r < 4 || y + n.r > height - 4) {
          ok = false;
        } else {
          for (var j = 0; j < placed.length; j++) {
            var p = placed[j];
            var dx = x - p.x, dy = y - p.y, s = n.r + p.r + PAD;
            if (dx * dx + dy * dy < s * s) { ok = false; break; }
          }
        }
        if (ok) { n.x = x; n.y = y; placed.push(n); done = true; break; }
        t += STEP_ARC / Math.max(B * Math.sqrt(1 + t * t), 1);
        if (rad > maxRad) break;
      }
      if (!done) { n.x = cx; n.y = cy; placed.push(n); }
    });
    return sorted;
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

  function renderBubbleMap(data, people, tip) {
    var W = 900, H = 620, PADV = 46;  // viewBox 여백 — 큰 원 라벨이 경계에 붙지 않게.
    var minStar = Math.min.apply(null, people.map(function (p) { return p.star || 1; }));
    var maxStar = Math.max.apply(null, people.map(function (p) { return p.star; }));
    people.forEach(function (p) { p.r = radiusFor(p.star || minStar, minStar, maxStar); });
    packCircles(people, W, H);

    var wrap = el("div", "rm-map-wrap");
    var s = svg("svg", {
      "class": "rm-map",
      viewBox: (-PADV) + " " + (-PADV) + " " + (W + 2 * PADV) + " " + (H + 2 * PADV),
      preserveAspectRatio: "xMidYMid meet",
      role: "img",
      "aria-label": "주목 연구자 버블 맵"
    });

    people.forEach(function (p) {
      var a = svg("a", { href: p.url });
      a.setAttribute("tabindex", "0");
      var g = svg("g", { "class": "rm-bubble" });

      var c = svg("circle", {
        cx: p.x, cy: p.y, r: p.r,
        fill: p.color, "fill-opacity": "0.82",
        stroke: p.color, "stroke-width": "1.5"
      });
      g.appendChild(c);

      g.appendChild(makeLabel(p));

      // 인터랙션
      g.addEventListener("mouseenter", function (e) { showTip(tip, p, e); });
      g.addEventListener("mousemove", function (e) { moveTip(tip, e); });
      g.addEventListener("mouseleave", function () { tip.style.display = "none"; });
      a.addEventListener("focus", function () {
        var box = s.getBoundingClientRect();
        var scale = box.width / W;
        showTip(tip, p, { clientX: box.left + p.x * scale, clientY: box.top + p.y * scale });
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

    var people = flatten(data);
    var tip = buildTooltip();

    // 1) 레전드
    root.appendChild(renderLegend(data));
    // 2) 버블 맵
    root.appendChild(renderBubbleMap(data, people, tip));

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
