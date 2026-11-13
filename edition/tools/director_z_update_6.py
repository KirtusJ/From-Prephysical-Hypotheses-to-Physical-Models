#!/usr/bin/env python3
"""Apply the second addendum of the fourth Director Z session (13 November 2026) to a copy of edition Z5, giving edition Z6:
paper G10 revised (Lemma 5.4 and Theorem 5.5 added), one program, register amendments.
Arguments: build directory (g10, comp, rec), copy of edition Z5, optional directory holding the session register (.pcp).
Rewrites MANIFEST.json last.  Requires PyMuPDF and Graphviz (dot)."""
import csv, hashlib, json, os, shutil, subprocess, sys
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
OLD, NEW = "FPHPM-BASELINE-2026-11-13-Z5", "FPHPM-BASELINE-2026-11-13-Z6"
changes = []
def put(src, rel, why):
    dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    k = "changed" if os.path.exists(dst) else "added"; shutil.copy(src, dst); changes.append((k, rel, why))
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:70]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
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
ba = "COMPUTATION/Baseline_Additions/"
for f in sorted(os.listdir(os.path.join(SRC, "comp"))): put(os.path.join(SRC, "comp", f), ba + f, "computation cited by paper G10 (Theorem 5.5)")
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
R = lambda p, n: dict(program=p, status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note=n)
rows += [R("Baseline_Additions/verify_cyclotomic_modulus_rules.py (fresh directory)", "4 predicates; exact arithmetic in Z[zeta] for q = 2, 4, 6, 8, 10, 12; added in edition Z6")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "one row appended"))
reg = rd("THEOREM_REGISTRY.csv")
NEWST = [("G10-01-08", "Lemma", "5.4", "Parallelogram law on an abelian group: the function is a quadratic form"),
         ("G10-01-09", "Theorem", "5.5", "Gains in the q-th roots of unity: the consistent modulus rules are the combinations of the squared moduli in the conjugate characters; dimension phi(q)/2; unique exactly for q = 2, 4, 6")]
labels = [f"{r['kind']} {r['number']}" for r in reg if r["paper"] == "G10"] + [f"{k} {n}" for _, k, n, _ in NEWST]
n10, pg = pages_of(PDF10, labels)
for r in reg:
    if r["paper"] == "G10": r["paper_file_page"] = r["part_page"] = str(pg[f"{r['kind']} {r['number']}"])
for i_, k, num, name in NEWST:
    reg.append(dict(id=i_, paper="G10", part="1", part_title=T10, kind=k, number=num, name=name, status="PROOF_IN_MANUSCRIPT", paper_file_page=str(pg[f"{k} {num}"]), part_page=str(pg[f"{k} {num}"]), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg); changes.append(("changed", "PROGRAM/registers/THEOREM_REGISTRY.csv", "G10 pages updated; rows G10-01-08 and G10-01-09 added"))
old_statements = [r["statements"] for r in rd("PAPER_INDEX.csv") if r["id"] == "G10"][0]
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G10": r.update(pages=str(n10), statements="9")
wcsv("PAPER_INDEX.csv", index); changes.append(("changed", "PROGRAM/registers/PAPER_INDEX.csv", "paper G10 revised"))
cross = rd("COMPONENT_CROSSWALK.csv")
for c in cross:
    if c["paper"] == "G10": c.update(baseline_sha256=sha(os.path.join(OUT, PART10)), pages=str(n10), change="first issued with edition Z4; revised in editions Z5 and Z6")
wcsv("COMPONENT_CROSSWALK.csv", cross); changes.append(("changed", "PROGRAM/registers/COMPONENT_CROSSWALK.csv", "G10 digest"))
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G10": r.update(pages=str(n10), labelled_statements="9", gaps="first issued with edition Z4; revised in editions Z5 (Theorem 5.3) and Z6 (Lemma 5.4, Theorem 5.5); proofs not independently checked; equation (7.1) is heuristic and supported by computed instances only; the instance of Director G quoted in Section 5.3 and the reference to Li and So were not inspected (OP-30)")
wcsv("READINESS.csv", ready); changes.append(("changed", "PROGRAM/registers/READINESS.csv", "paper G10 revised"))
ops = rd("OPEN_PROBLEMS.csv")
AM = {"OP-19": " Edition Z6: for gains in the q-th roots of unity the consistent rules of the record-sum form are exactly the combinations of the squared moduli in the conjugate characters (G10-01-09), under a growth hypothesis on one block that holds on the two-vertex carrier with step matrix [[1, zeta], [1, -zeta]]. The order of the rule is forced; the representation is not.",
      "OP-21": " Edition Z6: consistency on history events does not supply the ordering. The consistent rules for gains of order q form a space of dimension phi(q)/2 spanned by the squared moduli of the conjugate characters, so the rule is unique exactly for the orders 2, 4, 6 (G10-01-09); for other orders every embedding, and every combination with unequal weights, is consistent. Director G (Codex participant, 13 November 2026, review thread of the program) reports an instance on five sheets with three-step values (3 + sqrt 5)/16 and (3 - sqrt 5)/16 under two embeddings, and is examining which measurement assumptions select the ordinary embedding; not inspected by Director Z.",
      "OP-30": " Edition Z6: gains that are not real are covered for cyclic gains under the growth hypothesis (G10-01-09). Open in addition: whether a combination of conjugate rules with unequal weights is excluded by positivity or by composition; carriers on which the growth hypothesis fails; degrees above two."}
for r in ops:
    if r["id"] in AM: r["statement"] += AM[r["id"]]
wcsv("OPEN_PROBLEMS.csv", ops); changes.append(("changed", "PROGRAM/registers/OPEN_PROBLEMS.csv", "OP-19, OP-21 and OP-30 amended"))
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp)); k = 0
for e in br["edges"]:
    if e["statement"].startswith("Among rules that add over end vertices a function of the modulus"):
        e["statement"] += " Edition Z6: for gains in the q-th roots of unity the consistent rules are exactly the combinations of the squared moduli in the conjugate characters (G10-01-09); this replaces the sentence on gains of order four."
        e["locator"] += "; G10-01-09; verify_cyclotomic_modulus_rules.py"; k += 1
assert k == 1
br["edges"].append({"from": "PRE-ARC", "to": "QT", "type": "obstruction", "statement": "Consistency on history events forces the order of the rule and does not select the embedding of the amplitudes: for gains of order q the consistent rules of the record-sum form are the real combinations of the squared moduli in the phi(q)/2 conjugate characters; the rule is unique exactly for q = 2, 4, 6. A combination with unequal weights is a consistent rule that is the squared modulus of no character.", "locator": "Paper G10, G10-01-08, G10-01-09; verify_cyclotomic_modulus_rules.py; compare G8-01-08 and G7-01-13", "status": "PROOF_IN_MANUSCRIPT under a growth hypothesis on one block; exact computation for q = 2, 4, 6, 8, 10, 12"})
br["retained_outliers"]["consistent_modulus_rule_solution_dimension_for_q_2_4_6_8_10_12"] = [1, 1, 1, 2, 2, 2]
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "one edge amended; one edge and one retained value added"))
gp = os.path.join(REG, "ONTOLOGY_GATE_MAP.json"); gm = json.load(open(gp)); gm["edition"] = NEW
for g in gm["gates"]:
    if g["id"] == "P5": g["evidence"] += " Edition Z6: for gains of order q the consistent rules are the combinations of the squared moduli in the conjugate characters, a space of dimension phi(q)/2 (G10-01-09): the order is forced, the character is not."
    if g["id"] == "P10": g["evidence"] += " Edition Z6: consistency on histories leaves the ordering of values open for every order other than 2, 4, 6 (G10-01-09); what selects the ordinary embedding is under examination by Director G."
json.dump(gm, open(gp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/ONTOLOGY_GATE_MAP.json", "evidence of P5 and P10 amended; no state changed"))
dp = os.path.join(OUT, "PROGRAM", "figures", "Gate_Map_2026-11-13.dot"); dot = open(dp).read(); assert "edition Z5, 13 November 2026" in dot
open(dp, "w").write(dot.replace("edition Z5, 13 November 2026", "edition Z6, 13 November 2026").replace("Editions Z4 and Z5 change evidence", "Editions Z4 to Z6 change evidence")); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.dot", "edition label"))
subprocess.run(["dot", "-Tpdf", dp, "-o", dp[:-4] + ".pdf"], check=True); changes.append(("changed", "PROGRAM/figures/Gate_Map_2026-11-13.pdf", "edition label"))
HDR = (OLD + ", 13 November 2026", NEW + ", 13 November 2026")
edit("CONSTRUCTED_TRIALS/README.md", [HDR, ("| group, representation, ordering of values | supplied; for cyclic orders other than 1, 2, 3, 4, 6 the values depend on the character | G8 Proposition 8.1 |",
  "| group, representation, ordering of values | supplied; for cyclic orders other than 1, 2, 3, 4, 6 the values depend on the character; consistency on histories admits every conjugate character and every combination of them, and is unique exactly for the orders 2, 4, 6 (derived) | G8 Proposition 8.1; G10 Theorem 5.5 |")], "edition identifier; GH-1 ledger")
p = os.path.join(OUT, "CONSTRUCTED_TRIALS", "GH-1", "GH-1_Assumptions_and_Dispositions.json"); d = json.load(open(p))
d["derived"].append(dict(id="G10-01-09", text="gains in the q-th roots of unity: consistent modulus rules are the combinations of the squared moduli in the conjugate characters; unique exactly for q = 2, 4, 6")); d["revised"] = "2026-11-13, edition Z6"
a5 = [a for a in d["assumptions"] if a["id"] == "GH1-A5"][0]; a5["note"] = a5.get("note", "") + "; edition Z6: consistency on histories does not select the character (G10-01-09)"
json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "CONSTRUCTED_TRIALS/GH-1/GH-1_Assumptions_and_Dispositions.json", "GH-1 ledger amended"))
S4 = "REVIEW_RECORDS/Director_Z/Session_4/"
for f in sorted(os.listdir(os.path.join(SRC, "rec"))): put(os.path.join(SRC, "rec", f), S4 + f, "second addendum to the fourth-session record")
if PCP:
    put(os.path.join(PCP, "register.jsonl"), S4 + "register/register.jsonl", "register of the fourth session, extended by review Z5")
    nev = len(open(os.path.join(PCP, "register.jsonl")).read().strip().split("\n"))
    import re
    p4 = os.path.join(OUT, S4 + "README_SESSION_4.md"); t = open(p4).read(); m = re.search(r"The register: .*?present chain\)\.", t, re.S); assert m
    t = t.replace(m.group(0), "The register: %d events; head digest of the chain `%s`; SHA-256 of the file `%s` (edition Z6; the heads of editions Z4 and Z5 were `ea97886d0cc8dcd7aba4d95f9844cc8c95f312e56c4796f8da0d5123e1b250d8` and `d79915e5eb5a24959bc14dd7d73a0c7567a5543bebc692eefe2ffc57410a49e6`, events 36 and 52 of the present chain)." % (nev, os.environ.get("PCP_HEAD", "see pcpos verify"), sha(os.path.join(PCP, "register.jsonl"))))
    a_ = "| `ADDENDUM_EDITION_Z5.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM.csv` | the addendum: Theorem 5.3 of paper G10, findings Z-055 to Z-057 |"; assert a_ in t
    t = t.replace(a_, a_ + "\n| `ADDENDUM_EDITION_Z6.md`, `NEW_Z_SCOPED_FINDINGS_SESSION_4_ADDENDUM_2.csv` | the second addendum: Lemma 5.4 and Theorem 5.5 of paper G10, findings Z-058 to Z-060, and the record of contact with Director G |").replace("`CHANGES_Z3_TO_Z4.md`, `CHANGES_Z4_TO_Z5.md`", "`CHANGES_Z3_TO_Z4.md`, `CHANGES_Z4_TO_Z5.md`, `CHANGES_Z5_TO_Z6.md`")
    open(p4, "w").write(t); changes.append(("changed", S4 + "README_SESSION_4.md", "register digests; second addendum listed"))
T9 = "Reversible Steps on Gain Digraphs: Arc Structure, Complex Structure and the Ray Limit"
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G10 | {T10} | article | {old_pages} | {old_statements} |", f"| G10 | {T10} | article | {n10} | 9 |")]
    if rel == "README.md": extra = [(f"({637 + old_pages} assembled pages;", f"({637 + n10} assembled pages;"), (f"theorem registry ({len(reg) - 2} rows)", f"theorem registry ({len(reg)} rows)")]
    edit(rel, [HDR] + extra, "edition identifier" + ("; paper G10 revised" if extra else ""))
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update_6.py")); changes.append(("added", "tools/director_z_update_6.py", "the program that applied these changes"))
changes.append(("added", S4 + "CHANGES_Z5_TO_Z6.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(OUT, S4, "CHANGES_Z5_TO_Z6.md"), "w") as f:
    f.write("# Changes from edition Z5 to edition Z6\n\n13 November 2026. Every other file is byte-identical to edition Z5.\n\n| Change | File | Reason |\n|---|---|---|\n")
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
print("edition Z6:", len(files), "files;", len(reg), "registry rows;", n10, "pages in G10;", len(changes), "changes")
