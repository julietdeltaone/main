#!/usr/bin/env python3
"""Write skills/skills.json from a private master file.

Usage: python3 scripts/export_public.py /path/to/private/master.json

The master file stays outside this repository. It uses the same shape as
skills/skills.json and may carry extra fields on any skill (rating notes,
private evidence, tier values of "professional" or "private"). Only skills
with tier == "public" are written, and only the fields listed in KEEP.
"""
import json
import sys
from pathlib import Path

KEEP = ["id", "name", "category", "summary", "depth", "verified",
        "first_seen", "last_seen", "audiences", "tier", "evidence"]
EVIDENCE_KEEP = ["title", "note", "link"]


def main(master_path):
    master = json.loads(Path(master_path).read_text())
    skills = []
    for s in master["skills"]:
        if s.get("tier") != "public":
            continue
        row = {k: s.get(k) for k in KEEP}
        row["evidence"] = [{k: e[k] for k in EVIDENCE_KEEP if k in e}
                           for e in s.get("evidence", [])]
        skills.append(row)
    out = {k: master[k] for k in
           ("updated", "name", "headline", "summary", "views", "categories", "category_blurbs")}
    out["skills"] = skills
    target = Path(__file__).resolve().parent.parent / "skills" / "skills.json"
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {len(skills)} public skills to {target}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
