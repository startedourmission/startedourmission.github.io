#!/usr/bin/env python3
"""Dictionary 인물 노트 → assets/people-roadmap.json 생성.

Maps 페이지(roadmap.html)는 인물을 "조직 단위"로 묶어 보여준다.
- 조직(org)   = 실제 소속 한 곳. OpenAI, MIT, Shanghai AI Lab 처럼 구체적으로.
- 섹터(sector) = 그 조직의 종류. 프론티어 랩 / 빅테크 / 기업 / 반도체 / 연구소 / 대학 / 방법론.
겸직은 org 하나(주 소속)로 정하고 나머지는 also 에 적는다.

사용: 블로그/ 안에서 python3 tools/gen_people_roadmap.py [--threshold 32] [--check]
  --check 를 주면 파일을 쓰지 않고 매핑 누락만 보고한다.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 블로그/
DICT_DIR = os.path.join(ROOT, "markdown-blog", "Dictionary")
OUT_PATH = os.path.join(ROOT, "assets", "people-roadmap.json")

# 섹터 = 조직의 종류. 순서가 곧 지도에 그려지는 순서.
SECTORS = [
    ("frontier", "프론티어 AI 랩"),
    ("bigtech", "빅테크 연구조직"),
    ("company", "AI 기업 · 스타트업"),
    ("hardware", "반도체 · 하드웨어"),
    ("institute", "연구소 · 비영리"),
    ("university", "대학 · 학계"),
    ("method", "애자일 · 방법론"),
]

# 조직 레지스트리: 조직명 → 섹터. 여기 없는 조직이 나오면 스크립트가 에러를 낸다.
ORGS = {
    # 프론티어 랩
    "OpenAI": "frontier",
    "Anthropic": "frontier",
    "Google DeepMind": "frontier",
    "xAI": "frontier",
    "SSI": "frontier",
    "Thinking Machines Lab": "frontier",
    # 빅테크 연구조직
    "Google Research": "bigtech",
    "Meta FAIR": "bigtech",
    "AMAP (Alibaba)": "bigtech",
    # AI 기업 · 스타트업
    "AMI Labs": "company",
    "Sakana AI": "company",
    "Essential AI": "company",
    "Cohere": "company",
    "World Labs": "company",
    "DeepLearning.AI": "company",
    "NEAR Foundation": "company",
    "Inceptive": "company",
    "Moonshot AI": "company",
    "Skywork AI": "company",
    "TwelveLabs": "company",
    "Moloco": "company",
    "Adaption Labs": "company",
    "Macaron AI": "company",
    "Spotify": "company",
    # 반도체 · 하드웨어
    "NVIDIA": "hardware",
    "Tenstorrent": "hardware",
    "FuriosaAI": "hardware",
    "Modular AI": "hardware",
    # 연구소 · 비영리
    "Mila": "institute",
    "CAIS": "institute",
    "LG AI연구원": "institute",
    "Shanghai AI Lab": "institute",
    "Tsinghua AIR": "institute",
    # 대학 · 학계
    "University of Toronto": "university",
    "NYU": "university",
    "UC Berkeley": "university",
    "MIT": "university",
    "Stanford": "university",
    "CMU": "university",
    "KAIST": "university",
    "Northeastern University": "university",
    "인민대 가오링 AI대학": "university",
    "독립 연구자": "university",
    # 애자일 · 방법론
    "Scrum Inc.": "method",
    "Scrum.org": "method",
    "Kanban University": "method",
    "Gusto": "method",
    "애자일 (독립)": "method",
}

# 인물 → (주 소속, 겸직/이력 메모, 한 줄 소개). 주 소속은 ORGS 키여야 한다.
PEOPLE = {
    "제프리 힌턴": ("University of Toronto", "", "딥러닝의 아버지, 노벨 물리학상"),
    "얀 르쿤": ("AMI Labs", "전 Meta 수석 AI 과학자", "CNN의 아버지, AMI Labs 창업"),
    "일리야 수츠케버": ("SSI", "전 OpenAI 수석과학자", "SSI 창업자"),
    "데미스 하사비스": ("Google DeepMind", "", "DeepMind CEO, 노벨 화학상"),
    "조경현": ("NYU", "Genentech", "GRU·어텐션 공동 개발"),
    "앤드류 응": ("DeepLearning.AI", "Stanford, AI Fund", "Coursera 공동창업, Google Brain 출신"),
    "요슈아 벤지오": ("Mila", "U Montréal", "딥러닝 3대 거장"),
    "피터 아베일": ("UC Berkeley", "Covariant 출신", "로봇 강화학습 대가"),
    "페이-페이 리": ("World Labs", "Stanford HAI", "ImageNet 창시자"),
    "존 점퍼": ("Anthropic", "전 Google DeepMind", "AlphaFold2 책임자, 노벨 화학상"),
    "젠슨 황": ("NVIDIA", "", "NVIDIA 창업자 겸 CEO"),
    "샘 올트먼": ("OpenAI", "", "OpenAI CEO"),
    "다리오 아모데이": ("Anthropic", "", "Anthropic CEO"),
    "일리아 폴로수킨": ("NEAR Foundation", "", "트랜스포머 공저, NEAR CEO"),
    "에이단 고메즈": ("Cohere", "", "트랜스포머 최연소 저자, Cohere CEO"),
    "야코프 우스코레이트": ("Inceptive", "", "트랜스포머 공저, RNA 생성 창업"),
    "아시시 바스와니": ("Essential AI", "전 Adept", "트랜스포머 1저자"),
    "마르쿠스 후터": ("Google DeepMind", "ANU", "AIXI 창시자"),
    "루카시 카이저": ("OpenAI", "", "트랜스포머 공저, o1 리드"),
    "노암 셰이저": ("OpenAI", "전 Character.AI·Google", "트랜스포머 공동 발명자"),
    "김종욱": ("OpenAI", "", "CLIP·Whisper 핵심 저자"),
    "크리스 래트너": ("Modular AI", "Qualcomm 인수", "LLVM·Swift·Mojo 창시자"),
    "일론 머스크": ("xAI", "Tesla, SpaceX", "xAI 창업자"),
    "안드레이 카파시": ("Anthropic", "전 Tesla·OpenAI", "바이브 코딩 창안"),
    "앤드루 천": ("Macaron AI", "Mind Lab", "Macaron AI 공동창업, 수석 연구원"),
    "셔빈 아미디": ("Google DeepMind", "Stanford 강의", "CME295 강의, CS229 치트시트"),
    "리온 존스": ("Sakana AI", "전 Google Brain", "트랜스포머 공저, Sakana CTO"),
    "니키 파마르": ("Essential AI", "전 Google Brain", "트랜스포머 공저"),
    "켄트 벡": ("Gusto", "", "XP 창시자, TDD 대중화"),
    "론 제프리스": ("애자일 (독립)", "", "XP 공저, 애자일 선언 17인"),
    "장야친": ("Tsinghua AIR", "전 Baidu 사장", "칭화대 AIR 원장"),
    "황성주": ("KAIST", "DeepAuto CEO", "메타러닝·효율적 딥러닝"),
    "쿠니히코 후쿠시마": ("독립 연구자", "일본", "Neocognitron 발명자"),
    "산야 피들러": ("NVIDIA", "University of Toronto", "NVIDIA AI 연구 VP"),
    "로널드 윌리엄스": ("Northeastern University", "", "역전파 1986 공저, REINFORCE 창안"),
    "댄 헨드릭스": ("CAIS", "", "MMLU·MATH·GELU 저자"),
    "허카이밍": ("MIT", "Google DeepMind", "ResNet·MAE·MoCo 저자"),
    "원지룽": ("인민대 가오링 AI대학", "전 MSRA", "가오링 인공지능대학 학장"),
    "최예진": ("Stanford", "NVIDIA", "상식 추론, 맥아더 펠로우"),
    "이홍락": ("LG AI연구원", "U Michigan", "LG AI연구원 CSO"),
    "옌수이청": ("Skywork AI", "Kunlun 2050 Research", "컴퓨터비전 대가, H-index 140+"),
    "바하브 미로크니": ("Google Research", "", "Gemini 데이터 총괄"),
    "롭 퍼거스": ("Meta FAIR", "NYU", "ZFNet 저자, FAIR 책임자"),
    "그레이엄 뉴비그": ("CMU", "All Hands AI", "다국어 NLP·코드 생성"),
    "짐 켈러": ("Tenstorrent", "", "AMD Zen·Apple A4 설계자"),
    "미라 무라티": ("Thinking Machines Lab", "전 OpenAI CTO", "Thinking Machines CEO"),
    "다니엘 에크": ("Spotify", "Neko Health", "Spotify 공동창업 CEO"),
    "궈닝": ("AMAP (Alibaba)", "", "AMAP CEO, 공간 지능 에이전트"),
    "허충후이": ("Shanghai AI Lab", "OpenDataLab", "비전-언어 데이터 엔지니어링"),
    "켄 슈와버": ("Scrum.org", "", "Scrum 공동 창시자"),
    "제프 서덜랜드": ("Scrum Inc.", "", "Scrum 공동 창시자"),
    "이토 렌": ("Sakana AI", "전 메르카리 유럽 CEO", "Sakana AI COO"),
    "이재성": ("TwelveLabs", "", "TwelveLabs CEO"),
    "양즈린": ("Moonshot AI", "", "Moonshot CEO, Kimi 총괄"),
    "안익진": ("Moloco", "", "Moloco CEO"),
    "사라 후커": ("Adaption Labs", "전 Cohere For AI", "모델 효율성·공정성 연구"),
    "백준호": ("FuriosaAI", "", "FuriosaAI CEO, RNGD 개발"),
    "데이비드 하": ("Sakana AI", "전 Google Brain", "Sakana AI CEO"),
    "데이비드 앤더슨": ("Kanban University", "", "칸반 방법 체계화"),
}


def hash_id(name: str) -> str:
    return hashlib.md5(unicodedata.normalize("NFC", name).encode("utf-8")).hexdigest()[:8]


def read_people():
    """Dictionary 의 type: person 노트에서 (이름, star) 목록을 읽는다."""
    out = []
    for fname in sorted(os.listdir(DICT_DIR)):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(DICT_DIR, fname), encoding="utf-8") as f:
            text = f.read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            continue
        fm = m.group(1)
        if not re.search(r"^type:\s*person\s*$", fm, re.M):
            continue
        star = re.search(r"^star:\s*(\d+)", fm, re.M)
        out.append((unicodedata.normalize("NFC", fname[:-3]), int(star.group(1)) if star else 0))
    return out


def build(threshold: int):
    people = [(n, s) for n, s in read_people() if s >= threshold]
    people.sort(key=lambda r: (-r[1], r[0]))

    unmapped = [n for n, _ in people if n not in PEOPLE]
    bad_org = sorted({PEOPLE[n][0] for n, _ in people if n in PEOPLE and PEOPLE[n][0] not in ORGS})
    stale = [n for n in PEOPLE if n not in {p for p, _ in people}]

    # 조직 → 멤버
    by_org = {}
    for name, star in people:
        if name not in PEOPLE:
            continue
        org, also, tagline = PEOPLE[name]
        member = {"name": name, "url": hash_id(name) + ".html", "tagline": tagline, "star": star}
        if also:
            member["also"] = also
        by_org.setdefault(org, []).append(member)

    # 섹터 → 조직 (멤버 수 → 최고 star 순)
    sectors = []
    for key, label in SECTORS:
        orgs = []
        for org, members in by_org.items():
            if ORGS[org] != key:
                continue
            members.sort(key=lambda m: -m["star"])
            orgs.append({"org": org, "count": len(members), "members": members})
        if not orgs:
            continue
        orgs.sort(key=lambda o: (-o["count"], -o["members"][0]["star"], o["org"]))
        sectors.append({"key": key, "label": label, "orgCount": len(orgs),
                        "count": sum(o["count"] for o in orgs), "orgs": orgs})

    data = {
        "generated": date.today().isoformat(),
        "threshold": threshold,
        "total": sum(s["count"] for s in sectors),
        "orgTotal": sum(s["orgCount"] for s in sectors),
        "sectors": sectors,
    }
    return data, unmapped, bad_org, stale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=32)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    data, unmapped, bad_org, stale = build(args.threshold)

    if bad_org:
        print("ORGS 레지스트리에 없는 조직: " + ", ".join(bad_org), file=sys.stderr)
        return 1
    if unmapped:
        print("PEOPLE 매핑이 없는 인물 (소속을 추가하세요):", file=sys.stderr)
        for n in unmapped:
            print("  - " + n, file=sys.stderr)
        return 1
    if stale:
        print("기준 미달로 지도에서 빠진 인물: " + ", ".join(stale))

    print(f"{data['total']}명 · {data['orgTotal']}개 조직 · {len(data['sectors'])}개 섹터 (★{args.threshold} 이상)")
    for s in data["sectors"]:
        print(f"  {s['label']}: {s['count']}명 / {s['orgCount']}곳")

    if args.check:
        return 0

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote " + OUT_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
