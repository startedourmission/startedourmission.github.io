#!/usr/bin/env python3
"""blog-weekly-report 결과물을 6개 구조 어서션으로 기계 채점.
각 run 디렉터리(outputs/report.md)를 읽어 grading.json 을 run 디렉터리에 쓴다.
재실행 가능 — iteration 인자로 대상 폴더 지정."""
import json, re, sys, pathlib

ITER = sys.argv[1] if len(sys.argv) > 1 else "iteration-1"
ROOT = pathlib.Path(__file__).parent / ITER

WEEKDAYS = ["## 월요일", "## 화요일", "## 수요일", "## 목요일", "## 금요일"]
LABELS = ["[논문]", "[정보]", "[잡담]", "[사전]", "[시리즈"]

def grade(md: str, fname: str):
    fm = md.split("---", 2)
    fmtext = fm[1] if len(fm) >= 3 else ""
    exps = []

    has_fm = bool(re.search(r"^date:", fmtext, re.M)) and "주간리포트" in fmtext \
        and re.search(r"^week:", fmtext, re.M) and re.search(r"^description:", fmtext, re.M)
    exps.append({"text": "frontmatter에 date·tags(주간리포트)·week·description 모두 포함",
                 "passed": bool(has_fm),
                 "evidence": "frontmatter 키 " + ", ".join(k for k in ["date","tags:주간리포트","week","description"]
                              if (k.split(':')[0] in fmtext and ("주간리포트" in fmtext if "주간리포트" in k else True)))})

    has_callout = "> [!summary]" in md
    exps.append({"text": "상단 > [!summary] 한 주 요약 콜아웃 존재",
                 "passed": has_callout,
                 "evidence": "콜아웃 발견" if has_callout else "[!summary] 콜아웃 없음"})

    found_days = [d for d in WEEKDAYS if d in md]
    exps.append({"text": "월~금 5개 요일·테마 섹션 모두 존재",
                 "passed": len(found_days) == 5,
                 "evidence": f"{len(found_days)}/5 요일 섹션: " + ", ".join(d.replace('## ','') for d in found_days)})

    has_wiki = "[[" in md
    has_label = any(l in md for l in LABELS)
    exps.append({"text": "각 글에 [분류] 라벨 + [[위키링크]] 제목",
                 "passed": has_wiki and has_label,
                 "evidence": f"위키링크 {'있음' if has_wiki else '없음'}, 분류라벨 {'있음' if has_label else '없음'}"})

    dashes = md.count("—") + md.count("–")
    exps.append({"text": "본문에 em/en dash 없음",
                 "passed": dashes == 0,
                 "evidence": "dash 없음" if dashes == 0 else f"— / – {dashes}개 발견"})

    iso = bool(re.search(r"\d{4}-W\d{2}", md)) or bool(re.search(r"\d{4}-W\d{2}", fname))
    exps.append({"text": "파일명/week 필드가 ISO 주차(YYYY-Www)",
                 "passed": iso,
                 "evidence": "ISO 주차 표기 있음" if iso else "ISO 주차 표기 없음"})

    return exps

def main():
    runs = sorted(ROOT.glob("eval-*/*/outputs/report.md"))
    for rep in runs:
        run_dir = rep.parent.parent  # .../with_skill or without_skill
        md = rep.read_text(encoding="utf-8")
        exps = grade(md, rep.name)
        passed = sum(1 for e in exps if e["passed"])
        out = {"expectations": exps, "passed": passed, "total": len(exps)}
        (run_dir / "grading.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        rel = rep.relative_to(ROOT)
        print(f"{passed}/{len(exps)}  {rel}")

if __name__ == "__main__":
    main()
