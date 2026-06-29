#!/usr/bin/env node
// gen-trends-data.js — pre-compute Hacker News mention trends for the Trends gallery.
// Fetches yearly counts from the Algolia HN Search API and writes assets/trends-data.json.
// Run occasionally (data is yearly buckets; it barely moves day to day):
//   node scripts/gen-trends-data.js
"use strict";

const fs = require("fs");
const path = require("path");

const ALGOLIA = "https://hn.algolia.com/api/v1/search";
const START_YEAR = 2007;
const CONCURRENCY = 4; // gentle — Algolia rate-limits (403) on bursts
const OUT = path.join(__dirname, "..", "assets", "trends-data.json");

const sleep = (ms) => new Promise((res) => setTimeout(res, ms));

// Curated comparisons. Keywords are phrase-matched, so multiword names stay exact.
// Single generic words (e.g. "Threads", "Nomad") are avoided — too noisy.
const GROUPS = [
  { title: "AI 코딩 도구", keywords: ["Claude Code", "Cursor", "Copilot", "Codex"] },
  { title: "프런티어 LLM", keywords: ["ChatGPT", "Claude", "Gemini", "DeepSeek"] },
  { title: "LLM 연구소", keywords: ["OpenAI", "Anthropic", "Mistral", "Hugging Face"] },
  { title: "코드 에디터", keywords: ["Vim", "Neovim", "VS Code", "Zed"] },
  { title: "JS 빌드 도구", keywords: ["Webpack", "Vite", "esbuild", "Turbopack"] },
  { title: "CI/CD", keywords: ["Jenkins", "GitHub Actions", "CircleCI", "GitLab"] },
  { title: "컨테이너", keywords: ["Docker", "Kubernetes", "Podman", "containerd"] },
  { title: "데이터베이스", keywords: ["PostgreSQL", "MySQL", "MongoDB", "SQLite"] },
  { title: "라이선스 변경과 포크", keywords: ["Terraform", "OpenTofu", "Redis", "Valkey"] },
  { title: "소셜 플랫폼 대안", keywords: ["Mastodon", "Bluesky", "Lemmy", "Nostr"] },
  { title: "보안 사고", keywords: ["Log4j", "Heartbleed", "XZ Utils", "SolarWinds"] },
  { title: "프론트엔드 프레임워크", keywords: ["React", "Vue", "Svelte", "Angular"] }
];

const yearStart = (y) => Math.floor(Date.UTC(y, 0, 1) / 1000);

function years() {
  const end = new Date().getFullYear();
  const out = [];
  for (let y = START_YEAR; y <= end; y++) out.push(y);
  return out;
}

function buildUrl(keyword, y) {
  const s = yearStart(y), e = yearStart(y + 1);
  const nf = `created_at_i>=${s},created_at_i<${e}`;
  return `${ALGOLIA}?query=${encodeURIComponent('"' + keyword + '"')}` +
    `&advancedSyntax=true&numericFilters=${encodeURIComponent(nf)}&hitsPerPage=0`;
}

// Non-throwing: returns a number, or null after exhausting backoff retries.
async function fetchCount(keyword, y, attempts = 7) {
  const url = buildUrl(keyword, y);
  let delay = 700;
  for (let a = 0; a < attempts; a++) {
    try {
      const r = await fetch(url);
      if (!r.ok) throw new Error("HTTP " + r.status); // 403/429/5xx all retried below
      const j = await r.json();
      return typeof j.nbHits === "number" ? j.nbHits : 0;
    } catch (err) {
      if (a === attempts - 1) return null;
      await sleep(delay + Math.random() * 400);
      delay = Math.min(delay * 2, 9000);
    }
  }
  return null;
}

async function pool(items, limit, worker) {
  const results = new Array(items.length);
  let i = 0, done = 0;
  async function run() {
    while (i < items.length) {
      const idx = i++;
      results[idx] = await worker(items[idx], idx);
      done++;
      if (done % 40 === 0) process.stderr.write(`  ${done}/${items.length}\n`);
    }
  }
  await Promise.all(Array.from({ length: limit }, run));
  return results;
}

(async function main() {
  const ys = years();

  // Dedupe fetches: the same keyword may appear in multiple groups.
  const uniqKeywords = [...new Set(GROUPS.flatMap((g) => g.keywords))];
  const jobs = [];
  uniqKeywords.forEach((k) => ys.forEach((y) => jobs.push([k, y])));
  console.error(`Fetching ${uniqKeywords.length} keywords × ${ys.length} years = ${jobs.length} requests…`);

  const counts = {}; // keyword -> { year: n }
  await pool(jobs, CONCURRENCY, async ([k, y]) => {
    const n = await fetchCount(k, y);
    (counts[k] || (counts[k] = {}))[y] = n;
    return n;
  });

  // Sequentially re-fetch any buckets that failed (null), with generous spacing.
  let failed = jobs.filter(([k, y]) => counts[k][y] === null);
  if (failed.length) {
    console.error(`Retrying ${failed.length} failed buckets sequentially…`);
    for (const [k, y] of failed) {
      await sleep(1200);
      counts[k][y] = await fetchCount(k, y, 8);
    }
  }
  const stillNull = jobs.filter(([k, y]) => counts[k][y] === null).length;
  if (stillNull) console.error(`WARNING: ${stillNull} buckets still null (will serialize as null / line gap)`);

  const groups = GROUPS.map((g) => ({
    title: g.title,
    series: g.keywords.map((k) => ({ keyword: k, counts: ys.map((y) => counts[k][y]) }))
  }));

  const out = {
    generatedAt: new Date().toISOString().slice(0, 10),
    source: "Hacker News via Algolia Search API",
    startYear: START_YEAR,
    endYear: ys[ys.length - 1],
    years: ys,
    groups
  };

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(out));
  console.error(`Wrote ${OUT} (${groups.length} groups, ${(JSON.stringify(out).length / 1024).toFixed(1)} KB)`);
})();
