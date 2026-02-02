from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Dict, List, Tuple

from flask import Flask, render_template, request

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
KEYWORDS_PATH = DOCS_DIR / "tool_frame_keywords.md"
REFERENCE_PATH = DOCS_DIR / "tool_frame_reference.md"

app = Flask(__name__)


@dataclass
class ToolCard:
    name: str
    purpose: str
    usage: str
    steps: List[str]
    notes: str
    outputs: str
    raw: str


@dataclass
class MatchResult:
    name: str
    score: int
    matched_keywords: List[str]
    reason: str
    card: ToolCard | None


def load_keywords() -> Dict[str, List[str]]:
    keywords_map: Dict[str, List[str]] = {}
    if not KEYWORDS_PATH.exists():
        return keywords_map

    for line in KEYWORDS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        if ":" not in line:
            continue
        tool_name, raw_keywords = line[2:].split(":", 1)
        tool_name = tool_name.strip()
        keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]
        # Ensure tool name is also a keyword
        if tool_name not in keywords:
            keywords.append(tool_name)
        # De-duplicate while preserving order
        seen = set()
        cleaned: List[str] = []
        for kw in keywords:
            if kw in seen:
                continue
            seen.add(kw)
            cleaned.append(kw)
        keywords_map[tool_name] = cleaned
    return keywords_map


def parse_card(lines: List[str], tool_name: str) -> ToolCard:
    purpose = ""
    usage = ""
    steps: List[str] = []
    notes = ""
    outputs = ""

    current_section = ""
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("- 목적:"):
            purpose = line.split(":", 1)[1].strip()
            current_section = ""
            continue
        if line.startswith("- 사용 상황:"):
            usage = line.split(":", 1)[1].strip()
            current_section = ""
            continue
        if line.startswith("- 진행 방법:"):
            current_section = "steps"
            continue
        if line.startswith("- 유의점:"):
            notes = line.split(":", 1)[1].strip()
            current_section = ""
            continue
        if line.startswith("- 기대 산출물:"):
            outputs = line.split(":", 1)[1].strip()
            current_section = ""
            continue

        if current_section == "steps":
            step_match = re.match(r"\s*\d+\)\s*(.+)", line)
            if step_match:
                steps.append(step_match.group(1).strip())
            elif line.strip() and not line.strip().startswith("-"):
                steps.append(line.strip())

    raw_block = "\n".join([l.rstrip() for l in lines]).strip()
    return ToolCard(
        name=tool_name,
        purpose=purpose,
        usage=usage,
        steps=steps,
        notes=notes,
        outputs=outputs,
        raw=raw_block,
    )


def load_reference_cards() -> Dict[str, ToolCard]:
    cards: Dict[str, ToolCard] = {}
    if not REFERENCE_PATH.exists():
        return cards

    lines = REFERENCE_PATH.read_text(encoding="utf-8").splitlines()
    current_name = ""
    buffer: List[str] = []

    for line in lines:
        if line.startswith("### "):
            if current_name:
                cards[current_name] = parse_card(buffer, current_name)
            current_name = line.replace("### ", "").strip()
            buffer = []
        elif current_name:
            buffer.append(line)

    if current_name:
        cards[current_name] = parse_card(buffer, current_name)

    return cards


KEYWORDS_MAP = load_keywords()
REFERENCE_CARDS = load_reference_cards()
INTENT_BOOST = 2
INTENT_RULES = [
    {
        "triggers": [
            "아이스브레이크",
            "아이스브레이커",
            "라포",
            "첫만남",
            "체크인",
            "분위기",
            "친밀",
            "소개",
        ],
        "tools": [
            "명함만들기",
            "진진가",
            "이미지카드",
            "제비뽑기 토크",
            "릴레이 초상화",
            "Life Line",
            "Pie 한 조각",
            "One less chair",
            "Last Man Standing",
        ],
    },
    {
        "triggers": [
            "아이디어",
            "발산",
            "브레인스토밍",
            "아이디어도출",
            "아이디어 도출",
            "발상",
            "창의",
        ],
        "tools": [
            "Brain writing(브레인라이팅)",
            "Random Word Brainstorming",
            "Reverse Brainstorming",
            "침묵의 마인드맵",
            "NGT(Nominal Group Technique)",
        ],
    },
    {
        "triggers": [
            "정리",
            "구조화",
            "정렬",
            "분류",
            "체계화",
            "클러스터",
            "묶기",
        ],
        "tools": [
            "Cluster",
            "Grid",
            "Diagram",
            "List",
            "Illustration",
            "Gallery walk",
        ],
    },
    {
        "triggers": [
            "의사결정",
            "결정",
            "합의",
            "우선순위",
            "투표",
            "선택",
            "평가",
        ],
        "tools": [
            "우선순위화",
            "Payoff Matrix(Pay off matrix)",
            "Multi Voting",
            "Fist to five",
            "Minority Review",
            "Point Sharing Method",
            "Top Consensus Workshop Method",
        ],
    },
    {
        "triggers": [
            "회고",
            "피드백",
            "마무리",
            "클로징",
            "소감",
            "리뷰",
        ],
        "tools": [
            "3F",
            "PMI(Plus/Minus/Interesting)",
            "MDFP",
            "Exit Survey",
        ],
    },
    {
        "triggers": [
            "갈등",
            "복합",
            "이슈",
            "복잡",
            "조정",
        ],
        "tools": [
            "Dynamic Facilitation",
            "MDFP",
        ],
    },
    {
        "triggers": [
            "목적",
            "범위",
            "스코프",
            "정의",
            "요구사항",
            "니즈",
            "진단",
        ],
        "tools": [
            "Sensing(센싱)",
            "3P Define(목적/산출물/참여자)",
            "In&Out Frame(Scope In/Out)",
        ],
    },
]

SIZE_BOOST = 2
SIZE_RULES = [
    {
        "min": 30,
        "label": "대규모 인원 기준",
        "tools": [
            "Gallery walk",
            "Multi Voting",
            "NGT(Nominal Group Technique)",
        ],
    },
    {
        "min": 12,
        "label": "중간 규모 기준",
        "tools": [
            "Brain writing(브레인라이팅)",
            "Cluster",
            "Fist to five",
        ],
    },
    {
        "min": 0,
        "label": "소규모 기준",
        "tools": [
            "List",
            "3F",
            "Brain writing(브레인라이팅)",
        ],
    },
]


def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def extract_participant_count(raw: str) -> int | None:
    if not raw:
        return None
    match = re.search(r"(\\d+)", raw)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def apply_intent_rules(query_normalized: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    boosts: Dict[str, int] = {}
    matched: Dict[str, List[str]] = {}

    for rule in INTENT_RULES:
        hits = [t for t in rule["triggers"] if t in query_normalized]
        if not hits:
            continue
        for tool in rule["tools"]:
            if tool not in KEYWORDS_MAP:
                continue
            boosts[tool] = boosts.get(tool, 0) + INTENT_BOOST
            matched.setdefault(tool, [])
            matched[tool].extend(hits)

    return boosts, matched


def apply_size_rules(count: int | None) -> Tuple[Dict[str, int], Dict[str, str]]:
    if count is None:
        return {}, {}
    boosts: Dict[str, int] = {}
    labels: Dict[str, str] = {}
    for rule in SIZE_RULES:
        if count >= rule["min"]:
            for tool in rule["tools"]:
                if tool not in KEYWORDS_MAP:
                    continue
                boosts[tool] = boosts.get(tool, 0) + SIZE_BOOST
                labels[tool] = rule["label"]
            break
    return boosts, labels


def build_reason(matched_keywords: List[str], size_label: str | None, fallback: bool = False) -> str:
    if fallback:
        return "키워드 매칭이 없어 기본 추천으로 표시했습니다."
    parts: List[str] = []
    if matched_keywords:
        preview = ", ".join(matched_keywords[:2])
        parts.append(f"키워드 매칭({preview})")
    if size_label:
        parts.append(size_label)
    return " / ".join(parts) if parts else "입력 정보 기반 추천"


def score_tools(query: str, participants: str) -> List[MatchResult]:
    results: List[MatchResult] = []
    query_normalized = normalize_text(query)
    intent_boosts, intent_hits = apply_intent_rules(query_normalized)
    participant_count = extract_participant_count(participants)
    size_boosts, size_labels = apply_size_rules(participant_count)

    for tool_name, keywords in KEYWORDS_MAP.items():
        score = 0
        matched: List[str] = []
        for kw in keywords:
            kw_norm = normalize_text(kw)
            if not kw_norm:
                continue
            if kw_norm in query_normalized:
                score += 1
                matched.append(kw)
        if tool_name in intent_boosts:
            score += intent_boosts[tool_name]
            matched.extend(intent_hits.get(tool_name, []))
        if tool_name in size_boosts:
            score += size_boosts[tool_name]
        card = REFERENCE_CARDS.get(tool_name)
        reason = build_reason(sorted(set(matched)), size_labels.get(tool_name))
        results.append(
            MatchResult(
                name=tool_name,
                score=score,
                matched_keywords=sorted(set(matched)),
                reason=reason,
                card=card,
            )
        )

    results.sort(key=lambda r: (-r.score, r.name))
    return results


def fallback_results(participants: str) -> List[MatchResult]:
    participant_count = extract_participant_count(participants)
    if participant_count is not None and participant_count >= 30:
        tools = ["Gallery walk", "Multi Voting", "NGT(Nominal Group Technique)"]
    elif participant_count is not None and participant_count >= 12:
        tools = ["Brain writing(브레인라이팅)", "Cluster", "Fist to five"]
    else:
        tools = ["List", "3F", "Brain writing(브레인라이팅)"]

    results: List[MatchResult] = []
    for tool in tools:
        card = REFERENCE_CARDS.get(tool)
        results.append(
            MatchResult(
                name=tool,
                score=1,
                matched_keywords=[],
                reason=build_reason([], None, fallback=True),
                card=card,
            )
        )
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    form = {
        "purpose": "",
        "situation": "",
        "participants": "",
    }
    results: List[MatchResult] = []
    submitted = False
    fallback_notice = False

    if request.method == "POST":
        submitted = True
        for key in form:
            form[key] = request.form.get(key, "").strip()
        query = "\n".join([form[k] for k in form if form[k]])
        results = score_tools(query, form["participants"])
        results = [r for r in results if r.score > 0]
        if submitted and not results:
            fallback_notice = True
            results = fallback_results(form["participants"])

    return render_template(
        "index.html",
        form=form,
        results=results,
        submitted=submitted,
        fallback_notice=fallback_notice,
        total_tools=len(KEYWORDS_MAP),
    )


if __name__ == "__main__":
    app.run(debug=True)
