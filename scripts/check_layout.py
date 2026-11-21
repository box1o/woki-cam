#!/usr/bin/env python3
"""Report unfinished layouts in draft builds and block manufacturing releases."""

import argparse
import json
import os
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--expected-reports", type=int, default=1)
    args = parser.parse_args()
    reports = sorted(args.root.rglob("checks/drc.json"))
    if len(reports) != args.expected_reports:
        sys.exit(f"Expected {args.expected_reports} DRC reports, found {len(reports)}")

    rows = []
    for path in reports:
        data = json.loads(path.read_text())
        # Missing/malformed reports must fail even when generating draft outputs.
        for field in ("violations", "unconnected_items"):
            if not isinstance(data.get(field), list):
                sys.exit(f"Invalid {field} in {path}")
        rows.append(
            {
                "board": path.parent.parent.name,
                "violations": len(data["violations"]),
                "unrouted": len(data["unconnected_items"]),
            }
        )

    ready = not any(row["violations"] or row["unrouted"] for row in rows)
    status = {"manufacturing_ready": ready, "boards": rows}
    (args.root / "layout-status.json").write_text(json.dumps(status, indent=2) + "\n")
    title = "Layout checks passed" if ready else "Draft PCB — not ready for manufacture"
    lines = [f"## {title}", "", "| Board | DRC issues | Unrouted |", "|---|---:|---:|"]
    for row in rows:
        lines.append(f"| {row['board']} | {row['violations']} | {row['unrouted']} |")
    summary = "\n".join(lines) + "\n"
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as output:
            output.write(summary)
    if not ready:
        print(
            "::warning::Draft outputs only. Resolve all DRC issues and unrouted connections before manufacture."
        )
        if args.strict:
            sys.exit("Manufacturing release blocked by PCB layout checks")


if __name__ == "__main__":
    main()
