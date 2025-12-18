from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

def render_markdown(report: dict) -> str:
    lines = []
    lines.append("# CSV Profile Report")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append(f"- Rows: {report['summary']['rows']}")
    lines.append(f"- Columns: {len(report['columns'])}")
    lines.append("")
    lines.append("| Column | Type | Missing % | Unique |")
    lines.append("|--------|------|-----------|--------|")
    rows = report["summary"]["rows"]
    columns = report["columns"]
    for col, info in columns.items():
        missing = info["stats"].get("missing", 0)
        unique = info["stats"].get("unique", 0)
        missing_pct = (missing / rows * 100) if rows else 0.0
        col_type = info["type"]
        lines.append(f"| {col} | {col_type} | {missing_pct:.1f}% | {unique} |")
    lines.append("")
    for col, info in columns.items():
        col_type = info["type"]
        stats = info["stats"]
        lines.append(f"## Column: {col}")
        lines.append(f"- Type: {col_type}")
        lines.append(f"- Missing: {stats.get('missing', 0)}")
        lines.append(f"- Unique: {stats.get('unique', 0)}")
        if col_type == "number":
            lines.append(f"- Min: {stats.get('min')}")
            lines.append(f"- Max: {stats.get('max')}")
            lines.append(f"- Mean: {stats.get('mean')}")
        else:
            top = stats.get("top", [])
            if top:
                top_str = ", ".join(f"{v} ({c})" for v, c in top)
                lines.append(f"- Top values: {top_str}")
        lines.append("")
    return "\n".join(lines)

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = render_markdown(report)
    with open(path, "w", encoding="utf8") as f:
        f.write(content)
