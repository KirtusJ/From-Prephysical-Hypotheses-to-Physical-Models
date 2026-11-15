#!/usr/bin/env python3
"""Apply the twenty-third addendum of the fourth Director Z session (14 November 2026) to a copy of edition Z26, giving edition Z27:
paper G10 revised (new subsection "What position masks read of a character": Lemma 5.37 to Corollary 5.44), three Lean files,
the programs of the subsection, review records, register amendments.
Arguments: build directory (g10, mathlib, prog, rec), copy of edition Z26, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-14-Z26", "FPHPM-BASELINE-2026-11-14-Z27"
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

# Lean
LEAN_NEW = sorted(f for f in os.listdir(os.path.join(SRC, "mathlib")))
assert set(LEAN_NEW) == {"CharSeparation.lean", "CharSeparation.out", "TwoRail.lean", "TwoRail.out", "MaskOrbit.lean", "MaskOrbit.out"}, LEAN_NEW
for f in LEAN_NEW: put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean 4 lemmas used in the subsection on position masks (Propositions 5.39, 5.42, 5.43, Corollary 5.41)")
edit("COMPUTATION/Lean/README.md", [
    ("holds twenty-one files for Lean 4.12.0 with Mathlib v4.12.0 (and the compiler output of the two newest)", "holds twenty-four files for Lean 4.12.0 with Mathlib v4.12.0 (and the compiler output of the five newest)"),
    ("and the sequential-projection inequality used by Director G (SequentialProjections).", "and the sequential-projection inequality used by Director G (SequentialProjections); since edition Z27 also the algebra of Propositions 5.39 and 5.43 (TwoRail), of Proposition 5.42(a),(b) (CharSeparation) and of Corollary 5.41 (MaskOrbit).")],
    "three Mathlib files added")

# programs
PROG = os.path.join(SRC, "prog")
for dp, _, fs in os.walk(PROG):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), PROG); put(os.path.join(dp, f), "COMPUTATION/Baseline_Additions/Mask_Reading/" + rel, "programs and result files of the subsection on position masks")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
for lf, ax in (("CharSeparation", "propext, Classical.choice, Quot.sound"), ("TwoRail", "propext, Classical.choice, Quot.sound"), ("MaskOrbit", "propext, Classical.choice, Quot.sound")):
    rows.append(dict(program=f"COMPUTATION/Lean/Mathlib/{lf}.lean", status="RAN_OK", stored_output_compared="not applicable", stdout_equals_stored=f"exit code 0; axioms {ax}", note="rerun by the director for edition Z27"))
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "three rows appended"))

# registers
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-39", "Lemma", "5.37", "Word gain (Director G's identity, proved in the paper): on the two-rail digraph with arc gains a, b, c, d, the gain of a word from rail R with t steps, l left steps, e exits from L and m LL-pairs is a^t (a/c)^e u^l H^m in the stated normal form"),
         ("G10-01-40", "Proposition", "5.38", "For real eta every position-mask event and port has 2^t P = |alpha|^2|S_R|^2 + |beta|^2|S_L|^2 + 2 Re kappa Re(conj S_R S_L) - 2 Im kappa Im(conj S_R S_L) with real polynomials S_R, S_L in omega; P depends only on |alpha|^2, |beta|^2, eta, Re omega, Re kappa and Im omega Im kappa"),
         ("G10-01-41", "Proposition", "5.39", "For N at least 3 and eta = -1: the ports (3,1,R), (3,-1,L), (1,1,R), (1,-1,L), the fork and the fork after one tick read |alpha|^2, |beta|^2, Re kappa, Re omega and Im omega Im kappa"),
         ("G10-01-42", "Corollary", "5.40", "For N at least 3, eta = -1 and n = 1, two data give the same probability at every port of every position-mask event iff they have the same |alpha|^2, Re omega, Re kappa and Im omega Im kappa; from sharp starts characters are separated iff Re(chi(B)^M) differ, by the fork and by no port of length at most M"),
         ("G10-01-43", "Corollary", "5.41", "From a sharp start on rings with N at least 3, two evaluated coins give the same statistics on all position-mask events iff a common phase, a relative rail phase, a site phase zeta^x with zeta^N = 1 and complex conjugation carry one to the other (Director G's classification)"),
         ("G10-01-44", "Proposition", "5.42", "Equal Re u^M for M = 2, 3 and 5 forces u' in {u, conj u}; no two values of M suffice in general; inside a finite group one M prime to the order of u suffices"),
         ("G10-01-45", "Proposition", "5.43", "From a sharp start the two rail amplitudes at any port of any position-mask event are zeta p(omega) and zeta conj(gamma) q(omega) with real polynomials; states the walk prepares carry the factor conj(gamma) on rail L and read nothing more"),
         ("G10-01-46", "Corollary", "5.44", "For N at least 3, eta = -1, n = 1, chi and its conjugate agree on every position-mask event iff Im(conj alpha beta) = 0, or gamma = +-1 and omega = +-1; never separated from a sharp start")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-39 to G10-01-46 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]; assert old_statements == "38", old_statements
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="46")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z27")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="46", gaps=r["gaps"] + " Edition Z27: subsection on what position masks read of a character (Lemma 5.37 to Corollary 5.44, word gain and fork from Director G, orbit classification by Director G): from a sharp start a ring with N at least 3 reads only Re(chi(B)^M); proofs by the author; a micro-review, a challenger on the subsection and a challenger with a micro-review on Corollary 5.41; Lean for the algebra; the counting of admitted words is not formalized.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-30": " Edition Z27: what position masks read of a character is settled on rings with N at least 3 for real eta (G10-01-40 to G10-01-46): from a sharp start only Re(chi(B)^M), the class of the evaluated coin under changes of description; the walk cannot prepare a start that reads more. Open: eta not real; events that are not position masks; mixtures of starts; a physical reason for a start whose relative rail phase is fixed independently of the gains."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-30 amended"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z27: position masks from a sharp start read a character only through Re(chi(B)^M) on each ring with N at least 3, that is, through the class of its evaluated coin under changes of description (G10-01-42, G10-01-43, with Director G); neither the orientation nor the gain group is read, and the walk cannot prepare a start that reads more (G10-01-45)."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z26, 14 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z26, 14 November 2026", "edition Z27, 14 November 2026").replace("Editions Z4 to Z26 change evidence", "Editions Z4 to Z27 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 14 November 2026", NEW + ", 14 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "twenty-third addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z27")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z27; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "findings Z-137 to Z-140 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z27.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_23.csv`, `masks/`, further files in `cross_review/` and `pcp_workers/` | the twenty-third addendum: the subsection of paper G10 on what position masks read of a character (Lemma 5.37 to Corollary 5.44), its reviews, the abandonment of candidate Z2, four cross-reviews of Director G; findings Z-141 to Z-143 |").replace("`CHANGES_Z25_TO_Z26.md`", "`CHANGES_Z25_TO_Z26.md`, `CHANGES_Z26_TO_Z27.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; twenty-third addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 46 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_27.py")); changes.append(("added", "tools/director_z_update_27.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z26_TO_Z27.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z26_TO_Z27.md"), "w") as f:
    f.write("# Changes from edition Z26 to edition Z27\n\n14 November 2026. Every other file is byte-identical to edition Z26.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z27:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
