#!/usr/bin/env python3
"""Apply the Director Z changes of 12 November 2026 to a copy of FPHPM_Baseline_2026-11-12, giving edition Z1.
Inputs are read from the directory given as the first argument (manuscript build, records, computation);
the baseline copy is the second argument.  Rewrites MANIFEST.json last."""
import csv, hashlib, json, os, shutil, sys
SRC, OUT = sys.argv[1], sys.argv[2]
REG = os.path.join(OUT, "PROGRAM", "registers")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def rd(n):
    with open(os.path.join(REG, n), newline="") as f: return list(csv.DictReader(f))
def wcsv(n, rows):
    with open(os.path.join(REG, n) if not os.path.isabs(n) else n, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
OLD, NEW = "FPHPM-BASELINE-2026-11-12", "FPHPM-BASELINE-2026-11-12-Z1"
TITLE = "Transport, Holonomy and Monodromy as Bridge Candidates between Classical and Quantum Models"
PDIR = "PAPERS/G7_Transport_Holonomy_and_Monodromy_as_Bridge_Candidates_between_Classica"
PDF = PDIR + "/G7_Transport_Holonomy_and_Monodromy_as_Bridge_Candidates_between_Classica.pdf"
PART = PDIR + "/parts/01_G7_manuscript.pdf"
changes = []

# ---- paper G7
d = os.path.join(OUT, PDIR); os.remove(os.path.join(d, "PLANNED.md")); changes.append(("removed", PDIR + "/PLANNED.md", "superseded by the manuscript"))
os.makedirs(os.path.join(d, "parts")); os.makedirs(os.path.join(d, "source"))
shutil.copy(os.path.join(SRC, "g7", "G7_manuscript.pdf"), os.path.join(OUT, PDF)); shutil.copy(os.path.join(SRC, "g7", "G7_manuscript.pdf"), os.path.join(OUT, PART))
for f in ("G7_manuscript.tex", "body.tex", "Scientific_Preamble.tex"): shutil.copy(os.path.join(SRC, "g7", f), os.path.join(d, "source", f))
for f in (PDF, PART, PDIR + "/source/G7_manuscript.tex", PDIR + "/source/body.tex", PDIR + "/source/Scientific_Preamble.tex"): changes.append(("added", f, "paper G7"))
import pymupdf
pages = pymupdf.open(os.path.join(OUT, PDF)).page_count

# ---- computation
ba = os.path.join(OUT, "COMPUTATION", "Baseline_Additions")
for f in ("verify_holonomy_field_discriminator.py", "Holonomy_Field_Discriminator_Results.json"):
    shutil.copy(os.path.join(SRC, f), ba); changes.append(("added", "COMPUTATION/Baseline_Additions/" + f, "computation cited by paper G7"))
rr = os.path.join(OUT, "COMPUTATION", "RERUN_RECORD_2026-11-12.csv")
with open(rr, newline="") as f: rows = list(csv.DictReader(f))
rows += [dict(program="Baseline_Additions/verify_holonomy_field_discriminator.py (fresh directory)", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note="11 predicates; added in edition Z1"),
         dict(program="REVIEW_RECORDS/Director_D/validate_release.py", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="fresh verification agrees with stored results", note="rerun for edition Z1"),
         dict(program="NEGATIVE_CONTROLS/FAR-1/verify_toy_models.py (output path redirected)", status="RAN_OK", stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note="rerun for edition Z1")]
wcsv(rr, rows); changes.append(("changed", "COMPUTATION/RERUN_RECORD_2026-11-12.csv", "three rows appended"))

# ---- registers
index = rd("PAPER_INDEX.csv")
for r in index:
    if r["id"] == "G7": r.update(kind="article", file=PDF, pages=str(pages), parts="1", statements="9", cites_papers="G6")
wcsv("PAPER_INDEX.csv", index)
reg = rd("THEOREM_REGISTRY.csv")
ST = [("Proposition", "3.1", "Transport on a finite graph takes arbitrary values in an arbitrary group", "PROOF_IN_MANUSCRIPT", 3),
      ("Proposition", "4.1", "Triple invariant of a qubit", "PROOF_IN_MANUSCRIPT", 4),
      ("Lemma", "4.2", "Levi-Civita transport along a geodesic of complex projective space", "PROOF_IN_MANUSCRIPT", 4),
      ("Proposition", "4.3", "Determinant law", "PROOF_IN_MANUSCRIPT", 4),
      ("Corollary", "4.5", "Transition probabilities determine the Bargmann phase power up to conjugation", "PROOF_IN_MANUSCRIPT", 5),
      ("Theorem", "5.1", "Holonomy commutant and symplectic form characterize complex quantum theory in the comparison class", "PROOF_IN_MANUSCRIPT", 5),
      ("Proposition", "7.1", "Finite homogeneous subsets of the sphere leave a cap uncovered", "PROOF_IN_MANUSCRIPT", 8),
      ("Theorem", "7.2", "Turing; Gelander", "RESTATEMENT", 8),
      ("Corollary", "7.3", "Quantum pure-state spaces are not limits of finite homogeneous metric spaces", "PROOF_IN_MANUSCRIPT", 9)]
for i, (k, num, name, st, pg) in enumerate(ST, 1):
    reg.append(dict(id=f"G7-01-{i:02d}", paper="G7", part="1", part_title=TITLE, kind=k, number=num, name=name, status=st, paper_file_page=str(pg), part_page=str(pg), legacy_locator=""))
wcsv("THEOREM_REGISTRY.csv", reg)
cross = rd("COMPONENT_CROSSWALK.csv")
cross.append(dict(paper="G7", part="1", title=TITLE, kind="new", legacy_path="", legacy_volume="", legacy_volume_pages="", legacy_sha256="", baseline_path=PART,
                  baseline_sha256=sha(os.path.join(OUT, PART)), pages=str(pages), change="first issued with edition Z1", editable_sources="3"))
wcsv("COMPONENT_CROSSWALK.csv", cross)
cit = rd("CITATIONS_BETWEEN_PAPERS.csv")
cit.append(dict(citing_paper="G7", citing_part="1", cited_paper="G6", cited_part="1", cited_title="Invariant Relational Selection and Approximate Symmetry", evidence="title mention", locator=""))
wcsv("CITATIONS_BETWEEN_PAPERS.csv", cit)
ready = rd("READINESS.csv")
for r in ready:
    if r["paper"] == "G7": r.update(kind="article", pages=str(pages), parts="1", parts_with_editable_source="1", labelled_statements="9",
                                    gaps="first issued with edition Z1; proofs not independently checked and bibliographic details partly unverified (OP-17)")
wcsv("READINESS.csv", ready)
ops = rd("OPEN_PROBLEMS.csv")
for r in ops:
    if r["id"] == "OP-10":
        r["statement"] += " Paper G7 restricts the form of the limit: a finite subset of the Bloch sphere that is homogeneous leaves a cap of angular radius 10.48 degrees uncovered (G7-01-07), and by the theorems of Turing and Gelander no quantum pure-state space is a Gromov-Hausdorff limit of finite homogeneous metric spaces (G7-01-09). Finite stages therefore cannot have a transitive symmetry group; inhomogeneous approximants, finite generating data with unbounded words, and cyclic-group-valued phases remain."
        r["state"] = "open obligation; restricted by G7-01-07 and G7-01-09"
    if r["id"] == "OP-11":
        r["statement"] += " Paper G7 identifies, inside the class of single-system theories without third-order interference, a discriminator (the commutant of the Levi-Civita holonomy group of the transition-probability geometry, with monodromy) and an equivalent condition (the pure states admit a symplectic form) (G7-01-06). Both presuppose the transition-probability geometry; neither is a selection from a prephysical structure."
    if r["id"] == "OP-15":
        r.update(scope="F7", statement="The manuscript for the finite-sample CHSH tests is not written; its results exist as review records only. Paper G7 was issued with edition Z1.", state="open")
ops += [dict(id="OP-17", scope="G7", type="manuscript", statement="Independent verification of the proofs of paper G7. The holonomy groups of the quaternionic projective spaces of dimension at least two, of the octonionic plane and of the higher real projective spaces, the classification of finite subgroups of O(3) and the submersion property used in Lemma 4.2 are quoted, and most bibliographic details were written from memory; all are to be checked against the sources. The theorems of Turing and Gelander were inspected as retrieved extracts only.", state="open"),
        dict(id="OP-18", scope="G7", type="foundations", statement="A reason for requiring that pure states form a symplectic manifold that does not presuppose Hamiltonian dynamics, and its relation to observability of energy and to tomographic locality as alternative postulates selecting complex amplitudes.", state="not identified"),
        dict(id="OP-19", scope="G1 G3 G7", type="foundations", statement="For any of the three remaining forms of a finite-to-continuum limit (inhomogeneous approximants, finite generating data, cyclic-group-valued phases): a construction from a finite relational structure that yields a transition-probability geometry of the comparison class, together with a rule for composing systems. For a geodesic polygon whose vertices span the space, a transport construction of the Bargmann phase itself, beyond its (n+1)-th power, is also not given.", state="open")]
wcsv("OPEN_PROBLEMS.csv", ops)
for n in ("PAPER_INDEX.csv", "THEOREM_REGISTRY.csv", "COMPONENT_CROSSWALK.csv", "CITATIONS_BETWEEN_PAPERS.csv", "READINESS.csv", "OPEN_PROBLEMS.csv"):
    changes.append(("changed", "PROGRAM/registers/" + n, "paper G7 entered" if n != "OPEN_PROBLEMS.csv" else "OP-10, OP-11, OP-15 amended; OP-17 to OP-19 added"))

# ---- bridge register
bp = os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"); br = json.load(open(bp))
br["author"] = "LLM Director D (Claude, Anthropic) and LLM Director Z (Claude, Anthropic) at the direction of Kirtus Justus"
br["nodes"]["GPT-NO-I3"] = "non-classical single-system theories with classical decomposability, strong symmetry and no third-order interference: real, complex and quaternionic quantum theory, three-level octonionic theory, ball state spaces [Barnum–Müller–Ududec 2014]"
br["nodes"]["PSTP"] = "Poisson spaces with a transition probability: common description of classical and quantum pure-state spaces [Landsman 1997]"
E = lambda **k: br["edges"].append(k)
E(**{"from": "QT", "to": "QT", "type": "exact_correspondence", "statement": "Levi-Civita holonomy of a geodesic polygon in CP^n is unitary with complex determinant (B/|B|)^(n+1), B the Bargmann invariant, and multiplies by B/|B| the tangent vectors orthogonal to the vertices. The transport is fixed by the transition probabilities (d = arccos sqrt p); Schild's ladder computes it.", "locator": "Paper G7, G7-01-03 to G7-01-05; verify_holonomy_field_discriminator.py A", "status": "PROOF_IN_MANUSCRIPT; executed by an independent route for n = 1, 2, 3; unrefereed"})
E(**{"from": "GPT-NO-I3", "to": "QT", "type": "discriminator", "statement": "The commutant of the Levi-Civita holonomy group of the pure-state manifold is C exactly for complex quantum theory. Restricted holonomy does not separate the real three-level theory (RP^2) from the qubit; the monodromy round the non-contractible loop is a reflection and does.", "locator": "Paper G7, G7-01-06 and Remark 5.2; verify_holonomy_field_discriminator.py B, C", "status": "CONDITIONAL on quoted holonomy groups (HP^n for n>=2, OP^2, RP^m for m>=3 not computed); presupposes the transition-probability geometry"})
E(**{"from": "GPT-NO-I3", "to": "QT", "type": "postulate", "statement": "The pure states form a symplectic manifold. Within the class this holds only for complex quantum theory; it also holds for classical Hamiltonian mechanics. No reason for imposing it that avoids presupposing Hamiltonian dynamics is identified.", "locator": "Paper G7, G7-01-06 (c); compare observability of energy in Barnum–Müller–Ududec 2014; OPEN_PROBLEMS OP-18", "status": "obligation, not discharged"})
E(**{"from": "CM-SYMP", "to": "PSTP", "type": "exact_correspondence", "statement": "Classical mechanics is the instance p = Kronecker delta with an unrestricted Poisson structure.", "locator": "Landsman, Rev. Math. Phys. 9 (1997) 29; arXiv quant-ph/9603005, quant-ph/9604008", "status": "external precedent; inspected in extract"})
E(**{"from": "QT", "to": "PSTP", "type": "exact_correspondence", "statement": "Quantum mechanics is the instance in which two-point subspaces are qubit spheres and the sectors of p are the symplectic leaves; the Poisson structure is then fixed up to a constant identified with Planck's constant.", "locator": "Landsman, as above; consistent with the last statement of G7-01-06", "status": "external precedent; inspected in extract"})
E(**{"from": "QT", "to": "CM-SYMP", "type": "exact_correspondence", "statement": "Restricted to spin-j coherent states the transition probability is cos^{4j}(theta/2), which tends to the Kronecker delta with half-probability angle sqrt(2 ln 2 / j), while the Bargmann phase is j times the solid angle.", "locator": "Paper G7, equation (6.1); verify_holonomy_field_discriminator.py E", "status": "standard formula; executed"})
E(**{"from": "PRE-REL", "to": "QT", "type": "obstruction", "statement": "Finite carriers with a transitive symmetry group cannot approximate a quantum pure-state space: a finite homogeneous subset of the Bloch sphere leaves a cap of radius arccos(59/60) uncovered, and CP^n is not a Gromov–Hausdorff limit of finite homogeneous metric spaces. The circle and tori are such limits.", "locator": "Paper G7, G7-01-07 to G7-01-09; Turing, Ann. Math. 39 (1938) 105; Gelander, arXiv 1205.6553", "status": "G7-01-07 PROOF_IN_MANUSCRIPT; G7-01-09 CONDITIONAL on the quoted theorems"})
E(**{"from": "PRE-REL", "to": "QT", "type": "untested_transfer", "statement": "Forms of a finite-to-continuum limit not excluded by the obstruction: inhomogeneous finite approximants; finite generating data with words of unbounded length; cyclic-group-valued phases. A trial with two stipulated rotations reaches covering radius 4.4 degrees at word length 28.", "locator": "Paper G7, Section 7 and Table 4; OPEN_PROBLEMS OP-19", "status": "no construction supplied; the trial imports its generators"})
br["obligations_for_any_prephysical_candidate"] += [
    "do not rely on exact transitive symmetry at finite stages; state which form of limit is used and why the symmetry of the limit appears",
    "either derive that pure states form a symplectic manifold or name the postulate (observability of energy, tomographic locality) that selects complex amplitudes"]
br["retained_outliers"].update({"schild_one_sided_determinant_residual_rung_1e-3": 3.3e-4, "schild_one_sided_determinant_residual_rung_2e-3": 6.5e-4,
    "covering_radius_deg_icosahedral_chiral_and_full": [18.718, 18.713], "RP2_restricted_holonomy_commutant_dimension": 2})
json.dump(br, open(bp, "w"), indent=1, ensure_ascii=False); changes.append(("changed", "PROGRAM/registers/BRIDGE_CANDIDATE_REGISTER.json", "two nodes, eight edges, two obligations, retained values added"))

# ---- program documents
def edit(rel, pairs, why):
    p = os.path.join(OUT, rel); s = open(p).read()
    for a, b in pairs:
        assert a in s, (rel, a[:60]); s = s.replace(a, b)
    open(p, "w").write(s); changes.append(("changed", rel, why))
for rel in ("PROGRAM/CONTRIBUTIONS.md", "PROGRAM/PAPER_INDEX.md", "PROGRAM/STANDARDS.md", "PROGRAM/CHARTER.md", "REVIEW_RECORDS/README.md", "README.md", "LEGACY/README.md", "NEGATIVE_CONTROLS/README.md"):
    extra = []
    if rel == "PROGRAM/PAPER_INDEX.md": extra = [(f"| G7 | {TITLE} | planned | 0 | 0 |", f"| G7 | {TITLE} | article | {pages} | 9 |")]
    if rel == "PROGRAM/CONTRIBUTIONS.md": extra = [("the reconciliation of the collection into this baseline (paper plan,", "the Director Z assessment of the holonomy of transition-probability geometry and of finite carriers, with paper G7; the reconciliation of the collection into this baseline (paper plan,")]
    if rel == "REVIEW_RECORDS/README.md": extra = [("Director D under ACR 1.0.", "Directors D and Z under ACR 1.0.")]
    if rel == "README.md": extra = [("(594 assembled pages; two papers are planned and not yet written)", f"({594 + pages} assembled pages; one paper is planned and not yet written)"), ("theorem registry (344 rows)", f"theorem registry ({len(reg)} rows)")]
    if rel == "PROGRAM/CHARTER.md": extra = []
    edit(rel, [(OLD + ",", NEW + ",")] + extra, "edition identifier" + ("; paper G7" if extra else ""))

# ---- review records
rz = os.path.join(OUT, "REVIEW_RECORDS", "Director_Z"); shutil.copytree(os.path.join(SRC, "rec"), rz)
shutil.copy(os.path.abspath(__file__), os.path.join(OUT, "tools", "director_z_update.py")); changes.append(("added", "tools/director_z_update.py", "the program that applied these changes"))
for dp, _, fs in os.walk(rz):
    for f in fs: changes.append(("added", os.path.relpath(os.path.join(dp, f), OUT), "Director Z record"))
changes.append(("added", "REVIEW_RECORDS/Director_Z/CHANGES_TO_BASELINE.md", "this list")); changes.append(("changed", "MANIFEST.json", "edition identifier, digests"))
with open(os.path.join(rz, "CHANGES_TO_BASELINE.md"), "w") as f:
    f.write("# Changes from FPHPM-BASELINE-2026-11-12 to edition Z1\n\n12 November 2026. Every other file is byte-identical to the baseline.\n\n| Change | File | Reason |\n|---|---|---|\n")
    for c in changes: f.write(f"| {c[0]} | `{c[1]}` | {c[2]} |\n")

# ---- manifest
man = json.load(open(os.path.join(OUT, "MANIFEST.json")))
man["baseline"] = NEW; man["predecessor"] = OLD
man["predecessor_manifest_sha256"] = sha(os.path.join(SRC, "PREDECESSOR_MANIFEST.json"))
files = {}
for dp, _, fs in os.walk(OUT):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), OUT)
        if rel == "MANIFEST.json" or "__pycache__" in rel: continue
        files[rel] = dict(sha256=sha(os.path.join(OUT, rel)), size=os.path.getsize(os.path.join(OUT, rel)))
man["files"] = dict(sorted(files.items()))
json.dump(man, open(os.path.join(OUT, "MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
print("edition Z1:", len(files), "files;", len(reg), "registry rows;", pages, "pages in G7")
