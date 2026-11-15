#!/usr/bin/env python3
"""Apply the twenty-seventh addendum of Director Z (15 November 2026) to a copy of edition Z30, giving edition Z31:
paper G10 revised (proof of the three-group preparation written out; Lemma 5.54(iii), Corollary 5.57, Lemma 5.59, Theorem 5.62 on three or
more classes of winding), plots made with the PCP OS plot instrument, review records, register amendments.
Arguments: build directory (g10, mathlib, prog, rec), copy of edition Z30, optional directory holding the session register (.pcp).
Rewrites MANIFEST.json last.  Requires PyMuPDF and Graphviz (dot)."""
import csv, hashlib, json, os, re, shutil, subprocess, sys
import pymupdf
SRC, OUT = sys.argv[1], sys.argv[2]
PCP = sys.argv[3] if len(sys.argv) > 3 else None
REG = os.path.join(OUT, "PROGRAM", "registers")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def rd(n):
    with open(os.path.join(REG, n), newline="") as f: return list(csv.DictReader(f))
def wcsv(n, rows):
    with open(os.path.join(REG, n) if not os.path.isabs(n) else n, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
OLD, NEW = "FPHPM-BASELINE-2026-11-15-Z30", "FPHPM-BASELINE-2026-11-15-Z31"
changes = []
def put(src, rel, why):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = "changed" if os.path.exists(dst) else "added"; shutil.copy(src, dst); changes.append((k, rel, why))
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
man0 = json.load(open(os.path.join(OUT, "MANIFEST.json"))); assert man0["baseline"] == OLD, man0["baseline"]
predecessor_manifest = sha(os.path.join(OUT, "MANIFEST.json"))
T10 = "Histories as Events: the Order of the Pair Rule, First-Order Weights and Forces from Gains of Bounded Order"
P10 = [d for d in os.listdir(os.path.join(OUT, "PAPERS")) if d.startswith("G10_")][0]; PD = "PAPERS/" + P10
PDF10 = PD + "/" + P10 + ".pdf"; PART10 = PD + "/parts/01_G10_manuscript.pdf"
old_pages = pymupdf.open(os.path.join(OUT, PDF10)).page_count
put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), PDF10, "paper G10, revised"); put(os.path.join(SRC, "g10", "G10_manuscript.pdf"), PART10, "paper G10, revised")
for f in ("G10_manuscript.tex", "body.tex"): put(os.path.join(SRC, "g10", f), PD + "/source/" + f, "paper G10, revised")
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean file")
def pages_of(pdf, labels):
    d = pymupdf.open(os.path.join(OUT, pdf)); out = {}
    for i in range(d.page_count):
        for blk in d[i].get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                t = " ".join("".join(sp["text"] for sp in ln["spans"] if "Bold" in sp["font"]).split())
                for lab in labels:
                    if lab not in out and (t == lab or t.startswith(lab + " ") or t.startswith(lab + ".")): out[lab] = i + 1
    for lab in labels: assert lab in out, (pdf, lab)
    return d.page_count, out

# programs
PROG = os.path.join(SRC, "prog")
for dp, _, fs in os.walk(PROG):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), PROG); put(os.path.join(dp, f), "COMPUTATION/Baseline_Additions/Four_Gains/" + rel, "plots of the computed dimensions and of one winding profile, with their inputs and receipts")
# registers
reg = rd("THEOREM_REGISTRY.csv")
RENUM = {"G10-01-58": ("Proposition", "5.58"), "G10-01-59": ("Proposition", "5.60"), "G10-01-60": ("Theorem", "5.61")}
for r in reg:
    if r["id"] in RENUM: assert r["kind"] == RENUM[r["id"]][0]; r["number"] = RENUM[r["id"]][1]
    if r["id"] == "G10-01-55": r["name"] += "; if an outer level carries one walk, n(l)n(l+2M) <= n(l+M)(n(l+M)-1)/2 (part (iii), edition Z31)"
    if r["id"] == "G10-01-59": r["name"] += " (delta of finite order; proof in the manuscript from edition Z31)"
    if r["id"] == "G10-01-60": assert "given Proposition 5.58, " in r["name"]; r["name"] = r["name"].replace("given Proposition 5.58, ", "")
NEWST = [("G10-01-61", "Corollary", "5.57", "At a site of a position product event on a ring, three or more levels on one rail and a non-empty other rail force two or more levels on the other rail; for three or more classes of winding no site pairs a multiset meeting three cosets of <delta> with a non-empty multiset inside one coset"),
 ("G10-01-62", "Lemma", "5.59", "Invariance without preparation: on the line and on rings with N at least 3, a consistent site-independent rule has F_R o T_h = F_R for h in H and F_L = F_R o T_c on every multiset that occurs"),
 ("G10-01-63", "Theorem", "5.62", "Three or more classes of winding, M at least 8: on multisets in two adjacent cosets C_i, C_(i+1) the rule is alpha|m| + q(eps_i^2+eps_(i+1)^2) + c_i eps_i eps_(i+1), c_i = c for i at most s-2 and c_(s-1) = (-1)^k c, q = c = 0 for r odd; for three classes this fixes the combination of the count and the two squares")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages and numbers updated; rows G10-01-61 to G10-01-63 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]; assert old_statements == "60", old_statements
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="63")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z31")
    pass
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="63", gaps=r["gaps"] + " Edition Z31: the three-group preparation (Proposition 5.60) is proved in the paper and replayed from its text, so Theorem 5.61 (two classes) is unconditional for M at least 8; the one-winding property behind Proposition 5.58 is traced to the stage statements of the one-gain note; for three or more classes the rule is determined on multisets in two adjacent cosets (Theorem 5.62) and open on multisets meeting three cosets. Review under the Mathematics and Science modules; plots by the PCP OS plot instrument.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-30": " Edition Z31: two classes of winding are settled for M at least 8 without hypothesis (G10-01-59, G10-01-60); for three or more classes the rule is fixed on multisets in two adjacent cosets (G10-01-63) and no site pairs a three-coset multiset with a one-coset one (G10-01-61). Open: the rule on multisets meeting three cosets; rings with M at most 7; the short stages of the one-gain note."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-30 amended"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z31: two classes of winding proved for M at least 8; three or more classes determined on two adjacent cosets only (G10-01-63); no state changed."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z30, 15 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z30, 15 November 2026", "edition Z31, 15 November 2026").replace("Editions Z4 to Z30 change evidence", "Editions Z4 to Z31 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 15 November 2026", NEW + ", 15 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "twenty-seventh addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z31")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z31; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "the calibration record of the session; findings Z-147 to Z-151 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z31.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_27.csv`, `four_gains_winding/builder_three_classes/`, `four_gains_winding/challenger_proof/`, `four_gains_winding/challenger_three/` | the twenty-seventh addendum: proofs for the two hypotheses of edition Z30, three or more classes of winding (Lemma 5.54(iii), Corollary 5.57, Lemma 5.59, Theorem 5.62), the Mathematics and Science modules selected, plots; findings Z-152 to Z-154 |").replace("`CHANGES_Z29_TO_Z30.md`", "`CHANGES_Z29_TO_Z30.md`, `CHANGES_Z30_TO_Z31.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; twenty-seventh addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 63 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_31.py")); changes.append(("added", "tools/director_z_update_31.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z30_TO_Z31.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z30_TO_Z31.md"), "w") as f:
    f.write("# Changes from edition Z30 to edition Z31\n\n15 November 2026. Every other file is byte-identical to edition Z30.\n\n| Change | File | Reason |\n|---|---|---|\n")
    for c in changes: f.write(f"| {c[0]} | `{c[1]}` | {c[2]} |\n")
man = json.load(open(os.path.join(OUT, "MANIFEST.json")))
man["baseline"] = NEW; man["predecessor"] = OLD; man["predecessor_manifest_sha256"] = predecessor_manifest
files = {}
for dpth, _, fs in os.walk(OUT):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dpth, f), OUT)
        if rel == "MANIFEST.json" or "__pycache__" in rel: continue
        files[rel] = dict(sha256=sha(os.path.join(OUT, rel)), size=os.path.getsize(os.path.join(OUT, rel)))
man["files"] = dict(sorted(files.items()))
json.dump(man, open(os.path.join(OUT, "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
print("edition Z31:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
