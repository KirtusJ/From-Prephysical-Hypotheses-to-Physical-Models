#!/usr/bin/env python3
"""Apply the twenty-sixth addendum of Director Z (15 November 2026) to a copy of edition Z29, giving edition Z30:
paper G10 revised (Lemmas 5.53 to 5.55, Corollary 5.56, Propositions 5.57 and 5.58, Theorem 5.59: four arc gains on rings, the winding of the walks
at one vertex), paper G8 with one proof clause corrected, the programs, a Lean file, review records, register amendments.
Arguments: build directory (g10, g8, mathlib, prog, rec), copy of edition Z29, optional directory holding the session register (.pcp).
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
OLD, NEW = "FPHPM-BASELINE-2026-11-15-Z29", "FPHPM-BASELINE-2026-11-15-Z30"
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
P8 = [d for d in os.listdir(os.path.join(OUT, "PAPERS")) if d.startswith("G8_")][0]; PD8 = "PAPERS/" + P8
PDF8 = PD8 + "/" + P8 + ".pdf"; PART8 = PD8 + "/parts/01_G8_manuscript.pdf"
old_pages8 = pymupdf.open(os.path.join(OUT, PDF8)).page_count
put(os.path.join(SRC, "g8", "G8_manuscript.pdf"), PDF8, "paper G8, one proof clause corrected"); put(os.path.join(SRC, "g8", "G8_manuscript.pdf"), PART8, "paper G8, one proof clause corrected")
put(os.path.join(SRC, "g8", "body.tex"), PD8 + "/source/body.tex", "paper G8, one proof clause corrected")
assert pymupdf.open(os.path.join(OUT, PDF8)).page_count == old_pages8
for f in sorted(os.listdir(os.path.join(SRC, "mathlib"))): put(os.path.join(SRC, "mathlib", f), "COMPUTATION/Lean/Mathlib/" + f, "Lean file for the step replacing Step 6 in Theorem 5.59 of G10")
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
        rel = os.path.relpath(os.path.join(dp, f), PROG); put(os.path.join(dp, f), "COMPUTATION/Baseline_Additions/Four_Gains/" + rel, "programs and result files on the winding of the walks at one ring vertex")
# registers
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-54", "Lemma", "5.53", "Gain and winding of one walk: gain kappa g_delta(w) with kappa = a^(T-2 lambda)(bc)^lambda; lambda + M multiplies kappa by beta = (bc/a^2)^M; on a ring walks of one length to one vertex have lambda congruent modulo M"),
 ("G10-01-55", "Lemma", "5.54", "Winding at one vertex of a position product event on a ring: n(l)n(l') <= n(l+M)n(l'-M) for l'-l at least 2M and n(l)n(l+2M) <= n(l+M)(n(l+M)-1); the values of lambda form a gap-free progression of difference M and inner values are taken at least twice"),
 ("G10-01-56", "Lemma", "5.55", "The two rails of one site: n_L(l)n_R(l') <= n_L(l+M)n_R(l'-M) for l'-l at least M and n_R(l)n_L(l') <= n_R(l+M)n_L(l'-M) for l'-l at least 2M"),
 ("G10-01-57", "Corollary", "5.56", "No vertex of a position product event carries exactly three walks in three cosets of <delta>; for three or more classes of winding the preparation of all pairs does not exist; one walk on L at level j with one walk on R at level j+1 and nothing else never occurs at a site"),
 ("G10-01-58", "Proposition", "5.57", "Given that D_delta on the ring has preparations with one number of left steps at the target, every pair of multisets in kappa<delta> x kappa b d^-1<delta> is prepared for arbitrary four gains, a consistent site-independent rule is the count and one square on one-coset multisets, and Theorem 5.51(i) holds when (bc/a^2)^M lies in <delta>"),
 ("G10-01-59", "Proposition", "5.58", "Three groups on two levels: for M at least 8 and all multisets G1, G2, G3 of powers of delta, events with G2 on R at level l and G3, G1 on L at levels l, l+M, or G3, G1 on R at levels l, l+M and G2 on L at level l+M, and nothing elsewhere"),
 ("G10-01-60", "Theorem", "5.59", "Two classes of winding: on rings with M at least 8, given Proposition 5.58, the consistent site-independent rules are alpha|m| + q(eps_0^2+eps_1^2) + c eps_0 eps_1 with c = 0 if beta^2 is an odd power of delta and q = c = 0 if r is odd, that is the count and the squares of the characters of Delta_N with value -1 on delta")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-54 to G10-01-60 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]; assert old_statements == "53", old_statements
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="60")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 to Z30")
    if c["paper"] == "G8": c.update(baseline_sha256=sha(os.path.join(OUT, PART8)), change=c["change"] + "; one proof clause corrected in edition Z30")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 and G8 digests"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="60", gaps=r["gaps"] + " Edition Z30: the case (bc/a^2)^M != 1 on rings is treated by the number s of cosets of <delta> generated by the winding gain: s = 1 as on the line, given a computed property of the one-gain construction (Proposition 5.57); s = 2 and M at least 8 complete, given a computed preparation of three groups (Theorem 5.59); for s at least 3 the preparation of all pairs does not exist (Corollary 5.56) and the classification is open. Three challengers and one Lean file; reviewers of the author's model family.")
    if r["paper"] == "G8": r.update(gaps=r["gaps"] + " Edition Z30: in the proof of Proposition 5.2(c) the ring generated by chi(H_e) was called dense in C for order at least 3; for orders 3, 4 and 6 it is a lattice; the step now uses the field of fractions, as the proof of Proposition 5.1 does. The statement is unchanged.")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-30": " Edition Z30: the ring case (bc/a^2)^M != 1 is settled for one class of winding given a computed property of the one-gain construction (G10-01-58) and for two classes on rings with M at least 8 given a computed preparation (G10-01-60); for three or more classes the preparation of all pairs does not exist (G10-01-57). Open: whether the count and the squares are the only rules for three or more classes (computed on one ring of 4 sites to length 6); rings with M at most 7 for two classes; a proof of the one-winding property and of Proposition 5.58 in the paper.",
      "OP-25": " Edition Z30: one false clause in the proof of Proposition 5.2(c) corrected (density of the ring for orders 3, 4 and 6); the statement stands."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-30 and OP-25 amended"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z30: on rings the four-gain result is extended to one and two classes of winding under stated computed hypotheses (G10-01-58, G10-01-60) and shown not to follow from a preparation of all pairs for three or more (G10-01-57); no state changed."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z29, 15 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z29, 15 November 2026", "edition Z30, 15 November 2026").replace("Editions Z4 to Z29 change evidence", "Editions Z4 to Z30 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 15 November 2026", NEW + ", 15 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR], "edition identifier")
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for dp_, _, fs_ in os.walk(os.path.join(SRC, "rec")):
    for f in sorted(fs_):
        rel_ = os.path.relpath(os.path.join(dp_, f), os.path.join(SRC, "rec")); put(os.path.join(dp_, f), S4 + rel_, "twenty-sixth addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z30")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z30; earlier editions end at earlier events of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "a cross-review of Director G; finding Z-146 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z30.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_26.csv`, `four_gains_winding/`, `calibration_2026-11-15/` | the twenty-sixth addendum: the winding of the walks at one ring vertex in paper G10 (Lemmas 5.53 to 5.55, Corollary 5.56, Propositions 5.57 and 5.58, Theorem 5.59) with its reviews, a corrected proof clause in paper G8, the calibration record of the session; findings Z-147 to Z-151 |").replace("`CHANGES_Z28_TO_Z29.md`", "`CHANGES_Z28_TO_Z29.md`, `CHANGES_Z29_TO_Z30.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; twenty-sixth addendum listed"))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 60 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - len(NEWST)} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_30.py")); changes.append(("added", "tools/director_z_update_30.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z29_TO_Z30.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z29_TO_Z30.md"), "w") as f:
    f.write("# Changes from edition Z29 to edition Z30\n\n15 November 2026. Every other file is byte-identical to edition Z29.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z30:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
