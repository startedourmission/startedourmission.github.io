// hn-trends.js — Hacker News mention trends, queried live from the Algolia HN Search API.
// No build-time data, no backend: every chart is fetched in the visitor's browser.
// Counts are "how many HN stories+comments mentioned a term", bucketed by year.
(function () {
  "use strict";

  var ALGOLIA = "https://hn.algolia.com/api/v1/search";
  var START_YEAR = 2007;            // Hacker News launched in 2007
  var CONCURRENCY = 6;              // parallel requests in flight
  var MAX_KEYWORDS = 5;
  var PALETTE = ["#118bee", "#920de9", "#e8590c", "#2f9e44", "#e8590c", "#c2255c", "#1098ad"];

  var els = {};
  var chart = null;
  var runToken = 0;                 // bumps on every new comparison to cancel stale renders

  function nowYear() { return new Date().getFullYear(); }

  function yearStart(y) { return Math.floor(Date.UTC(y, 0, 1) / 1000); }

  function years() {
    var out = [], end = nowYear();
    for (var y = START_YEAR; y <= end; y++) out.push(y);
    return out;
  }

  // Algolia URL for one (keyword, year). Phrase-matched via advancedSyntax so that
  // "claude code" matches the phrase, not "claude" AND "code" scattered apart.
  function buildUrl(keyword, y) {
    var s = yearStart(y), e = yearStart(y + 1);
    var nf = "created_at_i>=" + s + ",created_at_i<" + e;
    return ALGOLIA +
      "?query=" + encodeURIComponent('"' + keyword + '"') +
      "&advancedSyntax=true" +
      "&numericFilters=" + encodeURIComponent(nf) +
      "&hitsPerPage=0";
  }

  function cacheKey(keyword, y) {
    return "hntrends:v1:" + keyword.toLowerCase() + ":" + y;
  }

  function cacheGet(keyword, y) {
    // The current year keeps growing, so never serve it from cache.
    if (y === nowYear()) return null;
    try {
      var v = sessionStorage.getItem(cacheKey(keyword, y));
      return v === null ? null : parseInt(v, 10);
    } catch (_) { return null; }
  }

  function cacheSet(keyword, y, n) {
    if (y === nowYear()) return;
    try { sessionStorage.setItem(cacheKey(keyword, y), String(n)); } catch (_) {}
  }

  // Fetch one bucket, with cache + a single retry on transient failure.
  function fetchCount(keyword, y) {
    var cached = cacheGet(keyword, y);
    if (cached !== null) return Promise.resolve(cached);

    function attempt(tries) {
      return fetch(buildUrl(keyword, y))
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(function (j) {
          var n = (j && typeof j.nbHits === "number") ? j.nbHits : 0;
          cacheSet(keyword, y, n);
          return n;
        })
        .catch(function (err) {
          if (tries > 0) return attempt(tries - 1);
          throw err;
        });
    }
    return attempt(1);
  }

  // Run an array of thunks with bounded concurrency. onTick fires after each settles.
  function pool(thunks, limit, onTick) {
    return new Promise(function (resolve) {
      var i = 0, active = 0, done = 0, results = new Array(thunks.length);
      function next() {
        if (done === thunks.length) { resolve(results); return; }
        while (active < limit && i < thunks.length) {
          (function (idx) {
            active++;
            thunks[idx]().then(function (v) { results[idx] = v; })
              .catch(function () { results[idx] = null; })
              .then(function () { active--; done++; if (onTick) onTick(done, thunks.length); next(); });
          })(i++);
        }
      }
      next();
    });
  }

  function setStatus(msg) { if (els.status) els.status.textContent = msg || ""; }

  function parseKeywords(raw) {
    var seen = {}, out = [];
    (raw || "").split(",").forEach(function (k) {
      var t = k.trim();
      if (!t) return;
      var key = t.toLowerCase();
      if (seen[key]) return;
      seen[key] = true;
      out.push(t);
    });
    return out.slice(0, MAX_KEYWORDS);
  }

  function themeColor(name, fallback) {
    try {
      var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      return v || fallback;
    } catch (_) { return fallback; }
  }

  function renderChart(labels, series) {
    var ctx = els.canvas.getContext("2d");
    var textColor = themeColor("--color-text", "#333");
    var gridColor = "rgba(127,127,127,0.18)";

    var datasets = series.map(function (s, idx) {
      var color = PALETTE[idx % PALETTE.length];
      return {
        label: s.keyword,
        data: s.counts,
        borderColor: color,
        backgroundColor: color,
        borderWidth: 2,
        pointRadius: 2,
        pointHoverRadius: 5,
        tension: 0.25,
        spanGaps: true
      };
    });

    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: "line",
      data: { labels: labels, datasets: datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { color: textColor, usePointStyle: true } },
          tooltip: { callbacks: { label: function (c) { return c.dataset.label + ": " + c.parsed.y.toLocaleString() + " mentions"; } } }
        },
        scales: {
          x: { ticks: { color: textColor }, grid: { color: gridColor } },
          y: { beginAtZero: true, ticks: { color: textColor }, grid: { color: gridColor } }
        }
      }
    });
  }

  function renderLinks(keywords) {
    if (!els.links) return;
    els.links.innerHTML = keywords.map(function (k) {
      var href = "https://hn.algolia.com/?dateRange=all&type=all&query=" + encodeURIComponent('"' + k + '"');
      return '<a href="' + href + '" target="_blank" rel="noopener">' + escapeHtml(k) + ' ↗</a>';
    }).join("");
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function compare(keywords) {
    keywords = (keywords || []).filter(Boolean).slice(0, MAX_KEYWORDS);
    if (!keywords.length) { setStatus("키워드를 한 개 이상 입력하세요."); return; }
    if (typeof window.Chart === "undefined") { setStatus("차트 라이브러리를 불러오지 못했습니다."); return; }

    var token = ++runToken;
    if (els.input) els.input.value = keywords.join(", ");
    setStatus("불러오는 중…");
    els.run.disabled = true;

    var ys = years();
    var jobs = [];
    keywords.forEach(function (k) {
      ys.forEach(function (y) { jobs.push(function () { return fetchCount(k, y); }); });
    });

    pool(jobs, CONCURRENCY, function (d, total) {
      if (token === runToken) setStatus("불러오는 중… " + d + "/" + total);
    }).then(function (flat) {
      if (token !== runToken) return; // a newer comparison superseded this one
      var per = ys.length;
      var series = keywords.map(function (k, ki) {
        return { keyword: k, counts: flat.slice(ki * per, ki * per + per) };
      });
      renderChart(ys, series);
      renderLinks(keywords);
      setStatus("출처: Hacker News (Algolia Search API) · 언급 = 글+댓글 본문 매칭 · 올해는 진행 중");
      els.run.disabled = false;
    });
  }

  function init() {
    els.input = document.getElementById("hnt-input");
    els.run = document.getElementById("hnt-run");
    els.status = document.getElementById("hnt-status");
    els.canvas = document.getElementById("hnt-chart");
    els.links = document.getElementById("hnt-links");
    if (!els.canvas) return;

    els.run.addEventListener("click", function () { compare(parseKeywords(els.input.value)); });
    els.input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); compare(parseKeywords(els.input.value)); }
    });

    Array.prototype.forEach.call(document.querySelectorAll(".hnt-preset"), function (btn) {
      btn.addEventListener("click", function () { compare(parseKeywords(btn.getAttribute("data-kw"))); });
    });

    // Render a default comparison so the page is alive on load.
    var first = document.querySelector(".hnt-preset");
    compare(parseKeywords(first ? first.getAttribute("data-kw") : "Claude Code, Cursor, Copilot, Codex"));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
