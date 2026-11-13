#!/usr/bin/env python3
"""Local consistency check of the baseline.  Requires PyMuPDF for the front-matter check (skipped with a notice if absent)."""
import csv, hashlib, json, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(ROOT, "MANIFEST.json"))); bad = []
listed = set(man["files"])
for rel, meta in man["files"].items():
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): bad.append(("missing", rel)); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != meta["sha256"]: bad.append(("digest", rel))
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        if rel not in listed and rel != "MANIFEST.json" and "__pycache__" not in rel: bad.append(("unlisted", rel))
reg = os.path.join(ROOT, "PROGRAM", "registers")
rd = lambda n: list(csv.DictReader(open(os.path.join(reg, n))))
cross, registry, index = rd("COMPONENT_CROSSWALK.csv"), rd("THEOREM_REGISTRY.csv"), rd("PAPER_INDEX.csv")
legacy = {c["legacy_sha256"] for c in cross if c["legacy_sha256"]}
vc = json.load(open(os.path.join(ROOT, "LEGACY", "2026-11-10_VOLUME_CONTENTS.json")))
for c in vc["components"]:
    if c["sha256"] not in legacy: bad.append(("component not in crosswalk", c["title"]))
ids = [r["id"] for r in registry]
if len(ids) != len(set(ids)): bad.append(("duplicate registry id", ""))
papers = {r["id"] for r in index}
for r in registry:
    if r["paper"] not in papers: bad.append(("registry row without paper", r["id"]))
for c in cross:
    if c["kind"] != "legacy" and hashlib.sha256(open(os.path.join(ROOT, c["baseline_path"]), "rb").read()).hexdigest() != c["baseline_sha256"]:
        bad.append(("crosswalk digest", c["baseline_path"]))
try:
    import pymupdf
    for r in index:
        if r["kind"] == "planned": continue
        d = pymupdf.open(os.path.join(ROOT, r["file"])); t = d[0].get_text() + (d[1].get_text() if d.page_count > 1 else "")
        t = " ".join(t.split())
        for need in ("Kirtus Justus", "Theoretical Physicist", "Port Coquitlam, British Columbia, Canada"):
            if need not in t: bad.append(("front matter lacks " + need, r["id"]))
        if "Vancouver" in "".join(pg.get_text() for pg in d): bad.append(("location not normalized", r["id"]))
except ImportError:
    print("notice: PyMuPDF not installed; front-matter check skipped")
if bad:
    print("BASELINE_CHECK_FAIL"); [print(" ", b) for b in bad[:40]]; sys.exit(1)
print(f"BASELINE_CHECK_PASS {len(man['files'])} files; {len(index)} papers; {len(registry)} registry rows; {len(vc['components'])} legacy components accounted for "
      "(local consistency only; not authentication, peer review or proof certification)")
