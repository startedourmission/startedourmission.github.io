#!/usr/bin/env python3
"""
buzz-update.py — grid_Papers 게시글의 buzz 점수를 갱신하고 Headliner 태그를 관리한다.

buzz 공식:
  hf_term   = log2(hf_upvotes + 1) * 20
  hf_term  *= 0.5 ** (age_days / HF_HALF_LIFE)    # HF 항만 게시 경과로 시간 감쇠
  cite_term = log10(citations + 1) * 100
  cite_factor = 1 - 0.6 / (1 + citations / 5)   # 0인용 → 0.4, 20인용 → 0.9, 100+ → ~1.0
  buzz = round((hf_term + cite_term) * cite_factor)

  - HF upvotes : huggingface.co/api/papers/<arXiv_ID>
  - citations  : api.semanticscholar.org/graph/v1/paper/arXiv:<arXiv_ID>
  - 두 소스 모두 로그 스케일로 합산하되, 인용 수 낮을수록 전체 buzz를 곱셈 페널티로 감산
    → 인용 0인 최신 커뮤니티 버즈 논문이 인용 많은 학술 영향작을 과도하게 앞지르지 않도록 조정
  - HF 추천수는 게시 직후 며칠 동안만 쌓이고 그 뒤로 박제되는 값이라, 게시일 경과에 따라
    HF '항'(로그 변환 후)에 반감기 HF_HALF_LIFE(90일) 감쇠를 직접 곱한다. 로그 안에서
    감쇠시키면 log이 흡수해 거의 안 깎이므로 반드시 로그 바깥에서 항 단위로 깎아야 한다.
    초반 붐업은 인정하되 시간이 지나면 buzz가 인용 항 중심으로 수렴 → "현재 화제도"에 가까워진다.
    age를 모르면 감쇠 없음(아직 게시 전인 stub 등 게시일 미상 케이스).

갱신 대상:
  1. buzz 필드 없는 글  (신규 게시)
  2. date 기준 30일 이내 글  (buzz 변동 구간)
  3. 주 1회 전체 갱신  (.last-buzz-full-update 타임스탬프)

Headliner 관리:
  buzz 갱신 완료 후, grid_Papers 전체를 buzz 내림차순 정렬하여
  상위 20편 → Headliner 태그 추가 (없으면)
  21위 이하  → Headliner 태그 제거 (있으면)
  * Headliner 태그는 사용자 권한이 원칙이지만,
    buzz 기반 자동 관리를 blog-check에서 명시적으로 위임받음.
"""
import os, re, json, subprocess, time, math
from datetime import date, timedelta

VAULT  = os.path.expanduser(
    "~/Vaults/AutoVault"
)
PAPERS = os.path.join(VAULT, "markdown-blog/grid_Papers")
POSTS  = os.path.join(VAULT, "markdown-blog/grid_Posts")
STAMP  = os.path.join(VAULT, ".claude/skills/blog-check/.last-buzz-full-update")

# Semantic Scholar API 키 (선택). 있으면 레이트 리밋 크게 완화.
# 우선순위: 환경변수 S2_API_KEY → 파일 ~/.../AutoVault/.s2_api_key
def _load_s2_key() -> str:
    k = os.environ.get("S2_API_KEY", "").strip()
    if k:
        return k
    try:
        return open(os.path.join(VAULT, ".s2_api_key"), encoding="utf-8").read().strip()
    except Exception:
        return ""

S2_API_KEY = _load_s2_key()

TODAY     = date.today()
CUTOFF_30 = TODAY - timedelta(days=30)
HEADLINER_PAPERS_N = 10   # grid_Papers: buzz 상위 N편
HEADLINER_POSTS_N  = 10   # grid_Posts:  최신 N편
HF_HALF_LIFE       = 90   # HF upvotes 시간 감쇠 반감기(일)


# ── 공식 ──────────────────────────────────────────────────────────────────────

def calc_buzz(hf: int, citations: int, age_days: int | None = None) -> int:
    hf_term   = math.log2(hf + 1) * 20
    # HF 추천수는 게시 직후 박제되는 값 → 로그 변환 후 항 단위로 반감기 감쇠.
    # (로그 안에서 hf를 깎으면 log이 흡수해 거의 안 줄어듦. 반드시 바깥에서 곱한다.)
    # age_days=None이면 감쇠 없음(아직 게시 전인 stub 등 게시일 미상 케이스).
    if age_days is not None and age_days > 0:
        hf_term *= 0.5 ** (age_days / HF_HALF_LIFE)
    cite_term = math.log10(citations + 1) * 100
    cite_factor = 1 - 0.6 / (1 + citations / 5)
    return round((hf_term + cite_term) * cite_factor)


# ── 타임스탬프 ────────────────────────────────────────────────────────────────

def last_full_update() -> date:
    try:
        return date.fromisoformat(open(STAMP).read().strip())
    except Exception:
        return date(2000, 1, 1)


def needs_full_update() -> bool:
    return (TODAY - last_full_update()).days >= 7


# ── API ───────────────────────────────────────────────────────────────────────

def get_hf_upvotes(arxiv_id: str) -> int:
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "8",
             f"https://huggingface.co/api/papers/{arxiv_id}"],
            capture_output=True, text=True,
        )
        return json.loads(r.stdout).get("upvotes", 0)
    except Exception:
        return 0


def get_citations(arxiv_id: str) -> int | None:
    """None = API 실패 (0 인용과 구분)."""
    try:
        cmd = ["curl", "-sk", "--max-time", "10"]
        if S2_API_KEY:
            cmd += ["-H", f"x-api-key: {S2_API_KEY}"]
        cmd += [f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"
                f"?fields=citationCount"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(r.stdout)
        count = data.get("citationCount")
        return int(count) if count is not None else None
    except Exception:
        return None


# ── frontmatter 파싱 ──────────────────────────────────────────────────────────

def extract_arxiv_id(content: str) -> str | None:
    # arXiv:1706.03762 / arxiv.org/abs/1706.03762 / frontmatter `arxiv: 1706.03762`
    m = re.search(r"arXiv:([0-9]{4}\.[0-9]{4,5})", content)
    if not m:
        m = re.search(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})", content)
    if not m:
        m = re.search(r"(?im)^arxiv:\s*([0-9]{4}\.[0-9]{4,5})", content)
    return m.group(1) if m else None


def extract_date(content: str) -> date | None:
    m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", content, re.MULTILINE)
    try:
        return date.fromisoformat(m.group(1)) if m else None
    except ValueError:
        return None


def get_buzz_value(content: str) -> int | None:
    m = re.search(r"^buzz:\s*(\d+)", content, re.MULTILINE)
    return int(m.group(1)) if m else None


def get_citations_fm(content: str) -> int | None:
    """frontmatter의 citations 값 (S2 조회 실패 시 fallback)."""
    m = re.search(r"^citations:\s*(\d+)", content, re.MULTILINE)
    return int(m.group(1)) if m else None


# ── frontmatter 수정 ──────────────────────────────────────────────────────────

def _split_frontmatter(content: str):
    """(fm_lines, body) 또는 (None, content)."""
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm_lines = content[: end + 4].split("\n")
    body = content[end + 4 :]
    return fm_lines, body


def set_buzz(content: str, value: int) -> str:
    fm_lines, body = _split_frontmatter(content)
    if fm_lines is None:
        return content
    # 기존 buzz 줄 제거 (단, 멀티라인 description 안의 들여쓴 텍스트는 건드리지 않도록
    # 들여쓰기 없는 'buzz:'만 매칭)
    fm_lines = [l for l in fm_lines if not re.match(r"^buzz:\s*\d+\s*$", l)]
    # buzz는 frontmatter 맨 끝(닫는 '---' 직전)에 넣는다.
    # description: |- 같은 멀티라인 값 한가운데 끼어들어 YAML을 깨뜨리지 않게.
    # fm_lines의 마지막 원소는 닫는 '---' 이므로 그 앞에 삽입.
    insert_at = len(fm_lines) - 1
    fm_lines.insert(insert_at, f"buzz: {value}")
    return "\n".join(fm_lines) + body


def set_headliner(content: str, add: bool) -> tuple[str, bool]:
    """Headliner 태그를 추가/제거. (new_content, changed) 반환."""
    fm_lines, body = _split_frontmatter(content)
    if fm_lines is None:
        return content, False

    has_tag = any("Headliner" in l for l in fm_lines)
    if add == has_tag:
        return content, False  # 변경 불필요

    if add:
        # tags: 블록 안에 삽입
        for i, line in enumerate(fm_lines):
            if line.strip().startswith("- ") and i > 0 and "tags" in fm_lines[i - 1]:
                fm_lines.insert(i + 1, "  - Headliner")
                break
            # tags: 바로 아래 첫 번째 항목 위치 찾기
        else:
            # tags 블록에서 마지막 - 항목 뒤에 삽입
            last_tag_idx = None
            in_tags = False
            for i, line in enumerate(fm_lines):
                if re.match(r"^tags\s*:", line):
                    in_tags = True
                elif in_tags and line.startswith("  - "):
                    last_tag_idx = i
                elif in_tags and not line.startswith("  "):
                    in_tags = False
            if last_tag_idx is not None:
                fm_lines.insert(last_tag_idx + 1, "  - Headliner")
    else:
        fm_lines = [l for l in fm_lines if "Headliner" not in l]

    return "\n".join(fm_lines) + body, True


# ── 메인 ─────────────────────────────────────────────────────────────────────

def main():
    full_refresh = needs_full_update()

    all_files = sorted(f for f in os.listdir(PAPERS) if f.endswith(".md"))

    # 모든 파일 로드
    posts = []  # (fname, path, arxiv_id, content)
    for fname in all_files:
        path = os.path.join(PAPERS, fname)
        try:
            content = open(path, encoding="utf-8").read()
        except Exception:
            continue
        arxiv_id = extract_arxiv_id(content)
        posts.append((fname, path, arxiv_id, content))

    # 갱신 대상 선별
    candidates = []
    for fname, path, arxiv_id, content in posts:
        if not arxiv_id:
            continue
        post_date = extract_date(content)
        missing   = get_buzz_value(content) is None
        recent    = post_date and post_date >= CUTOFF_30
        if missing or recent or full_refresh:
            candidates.append((fname, path, arxiv_id, content))

    # ── buzz 갱신 ────────────────────────────────────────────────────────────
    updated_buzz, failed, unchanged = [], [], []

    for fname, path, arxiv_id, content in candidates:
        hf   = get_hf_upvotes(arxiv_id)
        time.sleep(0.05)
        cite = get_citations(arxiv_id)
        time.sleep(0.3)   # Semantic Scholar 레이트 리밋 (1 req/s 권장)

        # S2 조회 실패 시 frontmatter의 citations로 fallback.
        # (S2가 특정 arXiv ID를 영구히 못 찾는 경우가 있어, 박제된 buzz가
        #  영영 갱신 안 되는 걸 막는다. 둘 다 없을 때만 fail 처리.)
        if cite is None:
            cite = get_citations_fm(content)
        if cite is None:
            failed.append(fname)
            continue

        post_date = extract_date(content)
        age_days  = (TODAY - post_date).days if post_date else None
        new_buzz = calc_buzz(hf, cite, age_days)
        old_buzz = get_buzz_value(content)

        if old_buzz == new_buzz:
            unchanged.append(fname)
            continue

        new_content = set_buzz(content, new_buzz)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        diff = f"{new_buzz - old_buzz:+d}" if old_buzz is not None else "new"
        updated_buzz.append((fname[:55], arxiv_id, new_buzz, diff, hf, cite))

        # 메모리 내 content도 갱신 (Headliner 단계에서 재사용)
        for i, (fn, p, aid, c) in enumerate(posts):
            if fn == fname:
                posts[i] = (fn, p, aid, new_content)
                break

    if full_refresh:
        with open(STAMP, "w") as f:
            f.write(str(TODAY))

    # ── Headliner 관리 — grid_Papers (buzz 상위 10) ──────────────────────────
    ranked_papers = []
    for fname, path, arxiv_id, content in posts:
        bv = get_buzz_value(content)
        if bv is not None:
            ranked_papers.append((bv, fname, path, content))
    ranked_papers.sort(reverse=True)

    headliner_added, headliner_removed = [], []
    for rank, (bv, fname, path, content) in enumerate(ranked_papers, start=1):
        should_have = rank <= HEADLINER_PAPERS_N
        new_content, changed = set_headliner(content, should_have)
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            if should_have:
                headliner_added.append(("논문", rank, bv, fname[:55]))
            else:
                headliner_removed.append(("논문", rank, bv, fname[:55]))

    # ── Headliner 관리 — grid_Posts (최신 10) ────────────────────────────────
    posts_all = []
    if os.path.isdir(POSTS):
        for fname in os.listdir(POSTS):
            if not fname.endswith(".md"):
                continue
            path = os.path.join(POSTS, fname)
            try:
                content = open(path, encoding="utf-8").read()
            except Exception:
                continue
            post_date = extract_date(content)
            posts_all.append((post_date or date(2000, 1, 1), fname, path, content))
    posts_all.sort(reverse=True)  # 최신순

    for rank, (post_date, fname, path, content) in enumerate(posts_all, start=1):
        should_have = rank <= HEADLINER_POSTS_N
        new_content, changed = set_headliner(content, should_have)
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            label = str(post_date)
            if should_have:
                headliner_added.append(("포스트", rank, 0, fname[:55]))
            else:
                headliner_removed.append(("포스트", rank, 0, fname[:55]))

    # ── stdout 출력 ──────────────────────────────────────────────────────────
    mode = "전체 갱신" if full_refresh else "부분 갱신(30일 이내 + buzz 미설정)"
    print(f"====== buzz 업데이트 [{mode}] ======")
    print(f"대상: {len(candidates)}편  |  갱신: {len(updated_buzz)}편  |  "
          f"변동 없음: {len(unchanged)}편  |  API 실패: {len(failed)}편")

    if updated_buzz:
        print("\n변경된 글:")
        for fname, aid, val, diff, hf, cite in sorted(updated_buzz, key=lambda x: -x[2]):
            print(f"  buzz:{val:4d} ({diff:>5})  HF:{hf} cite:{cite}  {fname}")

    if headliner_added or headliner_removed:
        print(f"\nHeadliner 변동 (논문 상위 {HEADLINER_PAPERS_N} / 포스트 최신 {HEADLINER_POSTS_N}):")
        for kind, rank, bv, fname in headliner_added:
            suffix = f"buzz:{bv}" if kind == "논문" else "최신순"
            print(f"  ✚ [{kind}] #{rank:2d}  {suffix}  {fname}")
        for kind, rank, bv, fname in headliner_removed:
            suffix = f"buzz:{bv}" if kind == "논문" else "최신순"
            print(f"  ✖ [{kind}] #{rank:2d}  {suffix}  {fname}")
    else:
        print("\nHeadliner 변동 없음")

    if failed:
        print(f"\nAPI 실패 (다음 실행에 재시도): {len(failed)}편")

    # 현재 Headliner 목록 출력
    print(f"\n현재 Headliner — 논문 (buzz 상위 {HEADLINER_PAPERS_N}):")
    for rank, (bv, fname, _, _) in enumerate(ranked_papers[:HEADLINER_PAPERS_N], 1):
        print(f"  #{rank:2d}  buzz:{bv:4d}  {fname[:55]}")
    print(f"\n현재 Headliner — 포스트 (최신 {HEADLINER_POSTS_N}):")
    for rank, (post_date, fname, _, _) in enumerate(posts_all[:HEADLINER_POSTS_N], 1):
        print(f"  #{rank:2d}  {post_date}  {fname[:55]}")
    print()


if __name__ == "__main__":
    main()
