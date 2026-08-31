#!/usr/bin/env python3
"""Star score calculator for Dictionary person entries.

점수 = 태그 점수 합 + 인용 보너스(citations 기반)
LLM 판단 없이 순수 파싱 기반.

## 점수 태그 (frontmatter tags에 추가)
  노벨상       +65
  프론티어CEO  +60
  튜링상       +50
  필즈상       +45
  CEO          +32
  분야창시자   +32
  수석과학자   +24
  Nature논문   +16
  오픈소스거장 +16
  교수         +12

  프론티어CEO: 프론티어 AI 랩·빅테크를 이끄는 최상위 CEO 전용.
  CEO와 함께 붙이면 65점(노벨/튜링급). 일반 CEO는 CEO 태그만.
  오픈소스거장: 영향력 큰 오픈소스 프레임워크·코드·교재의 저자(카파시, 켄트 벡 등).
  NeurIPS논문 태그는 완전 폐지(2026-06). 단순 학회 통과는 무점, 임팩트는 buzz
  보너스가 이미 반영하므로 중복. 점수 미부여 + 노트에서 태그도 전부 제거함.

## 인용 보너스 (papers: 리스트로 논문 연결)
  논문별 보너스 = CITE_COEF * citations^CITE_POW (편당 상한 50) → 합산 → 총상한 100.
  거듭제곱(p=0.4)이라 고인용의 우위가 보존된다: 어텐션(18만)≈50, AlphaFold(3.7만)≈25,
  Neural Prob LM(7.6천)≈14, 평범 최신(수백)≈4, 저인용(수십)≈2.
  → 저인용 논문은 30편을 써도 어텐션 1편을 못 넘는다(로그가 아니라 거듭제곱이라 격차 보존).
  논문 frontmatter `citations:` 필드 필요. tools/cite_collect.py가 S2 API로 채움.
  buzz(blog Headliner용 화제도)와 분리 — star는 역사적 임팩트=인용수가 핵심.
  거장은 반드시 대표 논문을 papers로 연결해야 공정(연결 누락 시 과소평가).

비활동 패널티는 폐지(은퇴/last_active 기반 감점 없음). last_active는 참고용으로만 유지.

## person frontmatter 예시
  type: person
  tags:
    - 인물
    - 딥러닝
    - 노벨상
    - 튜링상
    - 분야창시자
    - 교수
  last_active: 2024
  papers:
    - Attention Is All You Need
    - ImageNet Classification with Deep Convolutional Neural Networks

Usage:
    python3 tools/calc_star.py <person.md>       # 단일 파일
    python3 tools/calc_star.py --all              # Dictionary 전체 person 재계산
    python3 tools/calc_star.py --dry-run --all    # 점수만 출력, 파일 수정 없음
"""
import sys
sys.dont_write_bytecode = True

import re
import math
import json
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
DICT_DIR = VAULT / "markdown-blog/Dictionary"
PAPERS_DIR = VAULT / "markdown-blog/grid_Papers"
# 간이 논문 노트(stub). 블로그 repo 밖이라 배포·RSS 대상이 아님.
# buzz·점수 계산용으로만 쓰다가 완성되면 grid_Papers로 옮긴다.
STUBS_DIR = VAULT / "paper-stubs"
CURRENT_YEAR = 2026

# 논문 보너스는 인용수(citations) 기반. 로그가 아니라 거듭제곱이라 고인용의 우위가 보존된다.
# (blog Headliner용 buzz는 화제도라 로그가 맞지만, star는 역사적 임팩트=인용수가 핵심)
CITE_COEF = 0.40          # bonus = CITE_COEF * citations^CITE_POW
CITE_POW = 0.40           # 어텐션(18.1만)≈50, AlphaFold(3.7만)≈25, 평범(수백)≈4, 저인용(수십)≈2
CITE_PER_PAPER_CAP = 50   # 논문 1편당 보너스 상한. 어텐션급 단일 논문도 +50까지
CITE_TOTAL_CAP = 100      # 전체 합산 상한. 정상급 대표작 2편 이상이면 50 초과 가능
# 논문별 개별 보너스(각 CAP)를 합산 → 총 CAP로 클램프.
# "거장은 대표작이 여러 편"을 반영하되, 저인용 논문은 30편 써도 어텐션 1편을 못 넘는다.

TAG_SCORES = {
    "노벨상":      65,
    "프론티어CEO": 60,
    "튜링상":      50,
    "필즈상":      45,
    "CEO":         32,
    "분야창시자":  32,
    "수석과학자":  24,
    "Nature논문":  16,
    "오픈소스거장": 16,
    "교수":        12,
}

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def inactivity_penalty(last_active: int | None) -> int:
    # 비활동 패널티 폐지. last_active는 참고용으로만 보존한다.
    return 0


def load_paper_citations() -> dict[str, int]:
    """{파일명(확장자 제외): citations} 매핑 반환.

    grid_Papers를 먼저 읽고, paper-stubs를 나중에 읽어 보강한다.
    같은 제목이 양쪽에 있으면 grid_Papers(게시본) 값을 우선한다.
    citations 필드가 없으면 제외(buzz는 star 계산에 더 이상 안 씀).
    """
    cite_map: dict[str, int] = {}
    for src in (STUBS_DIR, PAPERS_DIR):
        if not src.is_dir():
            continue
        for p in src.glob("*.md"):
            text = p.read_text(encoding="utf-8")
            m = FRONT_RE.match(text)
            if not m:
                continue
            cm = re.search(r"^citations:\s*(\d+)", m.group(1), re.MULTILINE)
            if cm:
                cite_map[p.stem] = int(cm.group(1))
    return cite_map


def _single_paper_bonus(citations: int) -> float:
    """논문 1편의 보너스. 인용수 거듭제곱, 편당 상한(CITE_PER_PAPER_CAP)."""
    if citations <= 0:
        return 0.0
    return min(CITE_COEF * (citations ** CITE_POW), CITE_PER_PAPER_CAP)


def citation_bonus(cite_values: list[int]) -> int:
    """연결된 논문 각각의 보너스(편당 상한)를 합산 후 총 상한으로 클램프."""
    total = sum(_single_paper_bonus(c) for c in cite_values if c > 0)
    return round(min(total, CITE_TOTAL_CAP))


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    yaml_raw = m.group(1)
    body = text[m.end():]
    fm: dict = {"_yaml_raw": yaml_raw}

    tm = re.search(r"^type:\s*(.+)$", yaml_raw, re.MULTILINE)
    if tm:
        fm["type"] = tm.group(1).strip()

    tags_m = re.search(r"^tags:\s*\n((?:[ \t]+-[^\n]+\n?)*)", yaml_raw, re.MULTILINE)
    fm["tags"] = re.findall(r"-\s*(.+)", tags_m.group(1)) if tags_m else []

    lam = re.search(r"^last_active:\s*(\d{4})", yaml_raw, re.MULTILINE)
    if lam:
        fm["last_active"] = int(lam.group(1))

    sm = re.search(r"^star:\s*(\d+)", yaml_raw, re.MULTILINE)
    if sm:
        fm["star"] = int(sm.group(1))

    # papers: 리스트
    papers_m = re.search(r"^papers:\s*\n((?:[ \t]+-[^\n]+\n?)*)", yaml_raw, re.MULTILINE)
    fm["papers"] = [p.strip().lstrip("- ").strip() for p in
                    re.findall(r"-\s*(.+)", papers_m.group(1))] if papers_m else []

    return fm, body


def calc_score(fm: dict, paper_cite: dict[str, int]) -> tuple[int, int, int]:
    """(총점, citation_bonus, penalty) 반환."""
    tags = fm.get("tags", [])
    tag_score = sum(TAG_SCORES.get(t, 0) for t in tags)

    cite_values = [paper_cite.get(title, 0) for title in fm.get("papers", [])]
    bonus = citation_bonus(cite_values)

    penalty = inactivity_penalty(fm.get("last_active"))

    total = max(0, tag_score + bonus + penalty)
    return total, bonus, penalty


def update_file(path: Path, paper_cite: dict[str, int], dry_run: bool = False) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if fm.get("type") != "person":
        return None

    new_score, bonus, penalty = calc_score(fm, paper_cite)
    old_score = fm.get("star")

    changed = old_score != new_score

    cite_sum = sum(paper_cite.get(t, 0) for t in fm.get("papers", []))
    result = {
        "file": path.name,
        "old_score": old_score,
        "new_score": new_score,
        "tag_score": sum(TAG_SCORES.get(t, 0) for t in fm.get("tags", []) if t in TAG_SCORES),
        "cite_sum": cite_sum,
        "cite_bonus": bonus,
        "penalty": penalty,
        "tags_used": [t for t in fm.get("tags", []) if t in TAG_SCORES],
        "papers": fm.get("papers", []),
        "last_active": fm.get("last_active"),
        "changed": changed,
    }

    if dry_run or not changed:
        return result

    yaml_raw = fm["_yaml_raw"]

    # star 값 갱신
    if re.search(r"^star:\s*\d+", yaml_raw, re.MULTILINE):
        yaml_raw = re.sub(r"^star:\s*\d+", f"star: {new_score}", yaml_raw, flags=re.MULTILINE)
    else:
        yaml_raw = yaml_raw.rstrip() + f"\nstar: {new_score}"

    path.write_text(f"---\n{yaml_raw}\n---\n{body}", encoding="utf-8")
    return result


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    paper_cite = load_paper_citations()

    if "--all" in args:
        results = []
        for p in sorted(DICT_DIR.glob("*.md")):
            r = update_file(p, paper_cite, dry_run=dry_run)
            if r:
                results.append(r)

        changed = [r for r in results if r["changed"]]
        print(f"{'[DRY RUN] ' if dry_run else ''}Processed {len(results)} person files, {len(changed)} changed.\n")
        for r in sorted(results, key=lambda x: -x["new_score"]):
            if r["new_score"] == 0:
                continue
            flag = "*" if r["changed"] else " "
            parts = [f"tags={r['tags_used']}"] if r["tags_used"] else []
            if r["cite_bonus"]:
                parts.append(f"cite={r['cite_sum']}→+{r['cite_bonus']}")
            if r["penalty"]:
                parts.append(f"penalty={r['penalty']}")
            detail = "  " + "  ".join(parts) if parts else ""
            print(f"  {flag} {r['new_score']:3d}  {r['file']}{detail}")

        print(f"\n{'[DRY RUN] ' if dry_run else ''}{json.dumps({'processed': len(results), 'changed': len(changed)})}")

    elif args:
        path = Path(args[0])
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            sys.exit(1)
        r = update_file(path, paper_cite, dry_run=dry_run)
        if r is None:
            print("Not a person entry (type: person required).")
        else:
            print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
