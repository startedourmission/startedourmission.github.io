// hn-trends.js — Trends page.
// Primary: a gallery of curated mention-trend charts, rendered instantly from a
// pre-computed static file (assets/trends-data.json). No per-visit API calls.
// Secondary: an optional "compare your own keywords" box that queries the Algolia
// HN Search API live in the browser.
(function () {
  "use strict";

  var ALGOLIA = "https://hn.algolia.com/api/v1/search";
  var DATA_URL = "assets/trends-data.json";
  var PALETTE = ["#118bee", "#920de9", "#e8590c", "#2f9e44", "#c2255c", "#1098ad"];
  var YEARS = null;          // filled from the data file; falls back to computed
  var charts = [];

  function yearStart(y) { return Math.floor(Date.UTC(y, 0, 1) / 1000); }
  function nowYear() { return new Date().getFullYear(); }
  function computeYears() { var o = [], e = nowYear(); for (var y = 2007; y <= e; y++) o.push(y); return o; }

  function themeColor(name, fallback) {
    try { var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim(); return v || fallback; }
    catch (_) { return fallback; }
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function hnSearchUrl(k) {
    return "https://hn.algolia.com/?dateRange=all&type=all&query=" + encodeURIComponent('"' + k + '"');
  }
  function linksHtml(keywords) {
    return keywords.map(function (k) {
      return '<a href="' + hnSearchUrl(k) + '" target="_blank" rel="noopener">' + escapeHtml(k) + " ↗</a>";
    }).join("");
  }

  // Build one Chart.js line chart. compact=true tunes it for the small gallery cards.
  function makeChart(canvas, years, series, compact) {
    var textColor = themeColor("--color-text", "#333");
    var gridColor = "rgba(127,127,127,0.16)";
    var datasets = series.map(function (s, i) {
      var color = PALETTE[i % PALETTE.length];
      return {
        label: s.keyword, data: s.counts,
        borderColor: color, backgroundColor: color,
        borderWidth: 2, pointRadius: compact ? 0 : 2, pointHoverRadius: 4,
        tension: 0.25, spanGaps: true
      };
    });
    var ch = new Chart(canvas.getContext("2d"), {
      type: "line",
      data: { labels: years, datasets: datasets },
      options: {
        responsive: true, maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { color: textColor, usePointStyle: true, boxWidth: 8, font: { size: compact ? 11 : 13 } } },
          tooltip: { callbacks: { label: function (c) { return c.dataset.label + ": " + c.parsed.y.toLocaleString(); } } }
        },
        scales: {
          x: { ticks: { color: textColor, maxRotation: 0, autoSkip: true, maxTicksLimit: compact ? 7 : 12, font: { size: 10 } }, grid: { display: false } },
          y: { beginAtZero: true, ticks: { color: textColor, font: { size: 10 }, maxTicksLimit: 6 }, grid: { color: gridColor } }
        }
      }
    });
    charts.push(ch);
    return ch;
  }

  // ---- gallery (static data) ----
  function renderGallery(data) {
    YEARS = data.years;
    var host = document.getElementById("hnt-gallery");
    if (!host) return;
    host.innerHTML = "";
    data.groups.forEach(function (g) {
      var card = document.createElement("div");
      card.className = "hnt-card";

      var h = document.createElement("h3");
      h.textContent = g.title;
      card.appendChild(h);

      var wrap = document.createElement("div");
      wrap.className = "hnt-card-chart";
      var cv = document.createElement("canvas");
      wrap.appendChild(cv);
      card.appendChild(wrap);

      var links = document.createElement("div");
      links.className = "hnt-card-links";
      links.innerHTML = linksHtml(g.series.map(function (s) { return s.keyword; }));
      card.appendChild(links);

      host.appendChild(card);
      makeChart(cv, data.years, g.series, true);
    });
    var asof = document.getElementById("hnt-asof");
    if (asof) asof.textContent = "데이터 기준 " + data.generatedAt + " · 출처 " + data.source;
  }

  // ---- optional live "compare your own" ----
  function buildUrl(k, y) {
    var s = yearStart(y), e = yearStart(y + 1);
    var nf = "created_at_i>=" + s + ",created_at_i<" + e;
    return ALGOLIA + "?query=" + encodeURIComponent('"' + k + '"') +
      "&advancedSyntax=true&numericFilters=" + encodeURIComponent(nf) + "&hitsPerPage=0";
  }
  function cacheGet(k, y) {
    if (y === nowYear()) return null;
    try { var v = sessionStorage.getItem("hntrends:v2:" + k.toLowerCase() + ":" + y); return v === null ? null : parseInt(v, 10); }
    catch (_) { return null; }
  }
  function cacheSet(k, y, n) {
    if (y === nowYear()) return;
    try { sessionStorage.setItem("hntrends:v2:" + k.toLowerCase() + ":" + y, String(n)); } catch (_) {}
  }
  function fetchCount(k, y) {
    var c = cacheGet(k, y);
    if (c !== null) return Promise.resolve(c);
    function attempt(t) {
      return fetch(buildUrl(k, y))
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(function (j) { var n = (j && typeof j.nbHits === "number") ? j.nbHits : 0; cacheSet(k, y, n); return n; })
        .catch(function (err) { if (t > 0) return attempt(t - 1); throw err; });
    }
    return attempt(1);
  }
  function pool(thunks, limit, onTick) {
    return new Promise(function (resolve) {
      var i = 0, active = 0, done = 0, res = new Array(thunks.length);
      function next() {
        if (done === thunks.length) { resolve(res); return; }
        while (active < limit && i < thunks.length) {
          (function (idx) {
            active++;
            thunks[idx]().then(function (v) { res[idx] = v; }).catch(function () { res[idx] = null; })
              .then(function () { active--; done++; if (onTick) onTick(done, thunks.length); next(); });
          })(i++);
        }
      }
      next();
    });
  }

  var cu = {}, runToken = 0, customChart = null;
  function parseKeywords(raw) {
    var seen = {}, out = [];
    (raw || "").split(",").forEach(function (k) {
      var t = k.trim(); if (!t) return;
      var key = t.toLowerCase(); if (seen[key]) return;
      seen[key] = true; out.push(t);
    });
    return out.slice(0, 5);
  }
  function setStatus(m) { if (cu.status) cu.status.textContent = m || ""; }

  function compare(keywords) {
    keywords = (keywords || []).filter(Boolean).slice(0, 5);
    if (!keywords.length) { setStatus("키워드를 한 개 이상 입력하세요."); return; }
    if (typeof window.Chart === "undefined") { setStatus("차트 라이브러리를 불러오지 못했습니다."); return; }
    var ys = YEARS || computeYears();
    var token = ++runToken;
    cu.input.value = keywords.join(", ");
    setStatus("불러오는 중…");
    cu.run.disabled = true;
    cu.wrap.style.display = "";

    var jobs = [];
    keywords.forEach(function (k) { ys.forEach(function (y) { jobs.push(function () { return fetchCount(k, y); }); }); });
    pool(jobs, 6, function (d, t) { if (token === runToken) setStatus("불러오는 중… " + d + "/" + t); }).then(function (flat) {
      if (token !== runToken) return;
      var per = ys.length;
      var series = keywords.map(function (k, ki) { return { keyword: k, counts: flat.slice(ki * per, ki * per + per) }; });
      if (customChart) customChart.destroy();
      customChart = makeChart(cu.canvas, ys, series, false);
      cu.links.innerHTML = linksHtml(keywords);
      setStatus("실시간 조회 완료 · 올해 값은 진행 중");
      cu.run.disabled = false;
    });
  }

  function initCustom() {
    cu.input = document.getElementById("hnt-input");
    cu.run = document.getElementById("hnt-run");
    cu.status = document.getElementById("hnt-status");
    cu.canvas = document.getElementById("hnt-custom-chart");
    cu.links = document.getElementById("hnt-links");
    cu.wrap = document.getElementById("hnt-custom-wrap");
    if (!cu.run) return;
    cu.run.addEventListener("click", function () { compare(parseKeywords(cu.input.value)); });
    cu.input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); compare(parseKeywords(cu.input.value)); }
    });
  }

  function init() {
    initCustom();
    fetch(DATA_URL)
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(renderGallery)
      .catch(function () {
        var host = document.getElementById("hnt-gallery");
        if (host) host.innerHTML = '<p class="hnt-status">트렌드 데이터를 불러오지 못했습니다. 아래에서 직접 키워드를 비교해보세요.</p>';
      });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
