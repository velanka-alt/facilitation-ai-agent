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


def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def score_tools(query: str) -> List[MatchResult]:
    results: List[MatchResult] = []
    query_normalized = normalize_text(query)

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
        card = REFERENCE_CARDS.get(tool_name)
        results.append(
            MatchResult(
                name=tool_name,
                score=score,
                matched_keywords=sorted(set(matched)),
                card=card,
            )
        )

    results.sort(key=lambda r: (-r.score, r.name))
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

    if request.method == "POST":
        submitted = True
        for key in form:
            form[key] = request.form.get(key, "").strip()
        query = "\n".join([form[k] for k in form if form[k]])
        results = score_tools(query)
        results = [r for r in results if r.score > 0]

    return render_template(
        "index.html",
        form=form,
        results=results,
        submitted=submitted,
        total_tools=len(KEYWORDS_MAP),
    )


if __name__ == "__main__":
    app.run(debug=True)
