---
name: daily-content-routine
description: "Find timely content topics and create a daily pack of two Korean drafts: one practical information post (3+ cross-referenced sources) and one research-paper-based post. Use when asked for a daily content routine, topic finding, a daily editorial pack, multiple content drafts, or balanced information and paper-based writing."
---

# Daily Content Routine

Create a usable daily editorial pack, not merely a topic list. Default to **two** Korean drafts: **one** information post and **one** paper-based post. Adapt the topic domain, audience, channel, and length when the user specifies them.

**Volume cap is deliberate.** One paper + one post per day, no more. The cap exists to raise per-post density. Never pad to hit the cap with a weak candidate — if no information candidate clears the 3-source bar (below), ship the paper post alone and say so. Zero is a valid result for either lane.

## Workflow

1. Confirm the brief from the request. Infer a sensible audience and channel when omitted. Default to a general Korean professional audience and a concise blog/newsletter draft.
2. Find several candidates per lane before choosing. Use current, credible sources for the information post and original papers, publishers, or official preprints for the research post. Prefer practical relevance, novelty, and a clear reader benefit.
3. Select **one topic per lane**, two total.
   - Information x1: explain a current development, tool, method, policy, or useful trend. **Eligible only if 3+ genuinely distinct sources exist.**
   - Paper x1: translate a recent or durable research finding into plain language without exaggerating its certainty or applicability.
4. Build a source dossier for every selected topic before drafting. Record title, publisher or author, publication date, URL, and the exact claim it supports. For papers, include the study type, sample/data, and material limitations.
5. **Synthesize across sources — never rehash one.** Reading three sources and summarizing them in sequence produces three rehashes, not one article. Organize the draft by **topic**, not by source. Every information draft must land at least one of: where the sources disagree and why, or what becomes visible only when they are read together, or what all of them omit. If a paragraph reads "source A says X, source B says Y", rewrite it.
6. Run a final check: one draft per lane, every material factual claim traceable to a source, the information draft reflects 3+ distinct sources in its substance (not just its link list), and each draft contains one practical takeaway.

## Topic Selection Rules

- Favor topics with a timely hook and enough reliable material to sustain a draft.
- **Three-source bar for information posts.** Fewer than three genuinely distinct sources disqualifies the candidate outright. Articles rewriting the same press release count as **one** source. Prefer a mix of viewpoints: official announcement, independent analysis, hands-on or community reaction.
- Exclude stale, speculative, paywalled-only, or weakly sourced candidates.
- Prefer primary sources. Use reputable reporting only to add context or explain current impact.
- For research posts, cite the original paper directly. Do not rely on press coverage alone.
- Do not use a paper outside its scope. Note small samples, non-peer-reviewed status, observational designs, lab-only findings, or conflicts of interest when relevant.
- When a requested niche cannot support two credible papers that day, state the limitation and ask whether to broaden the date range or substitute another evidence-based post.

## Output Format

Start with a compact editorial table:

| No. | Type | Working title | Reader benefit | Evidence | Sources |
| --- | --- | --- | --- | --- | --- |
| 1 | Information | | | | (count, must be 3+) |
| 2 | Paper | | | | (original paper) |

Then provide two numbered drafts. Use this structure for each:

1. `Type` and working title
2. One-sentence angle
3. Draft body with a clear opening, evidence-led explanation, and practical close
4. `Sources`: direct links — **3 or more for the information post**, original paper included for the paper post
5. `Cross-source insight` (information post only): one or two lines naming what the synthesis produced — the disagreement, the pattern visible only across sources, or the shared blind spot
6. `Fact check`: key caveat or limitation, if applicable

If a lane produced nothing, say so explicitly with the reason instead of substituting a weaker topic.

Unless the user requests another format, write each draft at roughly 2,000-3,500 Korean characters. Depth is the point of the volume cap. Keep the style factual, specific, and free of generic promotional language.

## Delivery

Return the completed pack in the conversation by default. Write files only when the user specifies a destination or explicitly asks to save them. When saving to Obsidian, create one index note plus one note per draft and preserve the source dossier in each note. Do NOT put dates in filenames. This vault names notes with a descriptive title only (e.g. `딥시크 추론 칩.md`, not `2026-07-13 딥시크 추론 칩.md`); keep the date in the frontmatter `date` field.

Stop at the draft handoff. Do not publish, schedule, upload, or send content. The user reviews the drafts and performs publication directly.
