// 인물 지도 렌더러 — assets/people-roadmap.json 을 읽어 현재 소속별 카드로 그린다.
// 데이터는 빌드와 무관한 정적 파일이며 scripts/gen 없이 수작업 큐레이션된다.
(function () {
  "use strict";
  var DATA_URL = "assets/people-roadmap.json";

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function renderMember(m) {
    var li = el("li", "rm-member");
    var a = el("a", null, m.name);
    a.href = m.url;
    li.appendChild(a);
    if (typeof m.star === "number" && m.star > 0) {
      li.appendChild(el("span", "rm-star", "★ " + m.star));
    }
    if (m.tagline) {
      li.appendChild(el("span", "rm-tag", m.tagline));
    }
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

  function renderSector(s) {
    var wrap = el("div", "rm-sector");
    var head = el("div", "rm-sector-head");
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
    data.sectors.forEach(function (s) { root.appendChild(renderSector(s)); });
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
