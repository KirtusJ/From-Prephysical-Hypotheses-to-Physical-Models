#!/usr/bin/env python3
"""Write the program documents, remaining registers, computation tree, negative controls, review records,
legacy folder, manifest and verifier of the 12 November 2026 baseline.  Run after assemble.py."""
import csv, hashlib, json, os, shutil, sys, zipfile
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_plan import P, SERIES, AUTHOR, AUTHOR_TITLE, AUTHOR_LOCATION, PROGRAM, BASELINE_DATE, BASELINE_ID

SRC = "/home/claude/work/Review_Materials"; W = "/home/claude/work"
OUT = "/home/claude/bb/out/FPHPM_Baseline_2026-11-12"
REG = os.path.join(OUT, "PROGRAM", "registers")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rd = lambda n: list(csv.DictReader(open(os.path.join(REG, n))))
def wcsv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "w").write(text.strip() + "\n")
HEAD = f"**{AUTHOR}**, {AUTHOR_TITLE}  \n{AUTHOR_LOCATION}  \nBaseline {BASELINE_ID}, {BASELINE_DATE}\n"
INPUTS = {"Review packet, 10 November 2026": "fde41b3789930b0848cffd80b0ced68b052645808c393525266b1457d6d669cf",
          "Director B handoff, 11 November 2026": "547a89f0e49565c197a8edffe7f7502f611e47ef9f38a5a89c86d3fe2a5a5925",
          "Director C audit, 11 November 2026": "0bf18a8fa81e826705c9f6c82181faf5cff50d14c52b5edc595ab0062386296b",
          "Toy Universe session packet": "6c512b6a54c05b568afff95d0e73c15e4a72284234badb5c2c64da31bb891cb2",
          "PCP 1.0 Enterprise Edition": "1282bcd3f0ec8bd22bfb0575a6cf7e3e38f29f8cbdb278082dcfd317da907be7"}

index = rd("PAPER_INDEX.csv"); registry = rd("THEOREM_REGISTRY.csv"); cross = rd("COMPONENT_CROSSWALK.csv")

# ------------------------------------------------------------------ computation
comp_dst = os.path.join(OUT, "COMPUTATION")
if os.path.exists(comp_dst): shutil.rmtree(comp_dst)
shutil.copytree(os.path.join(SRC, "Computational_Material"), os.path.join(comp_dst, "Computational_Material"))
shutil.copy(os.path.join(SRC, "requirements.txt"), comp_dst); shutil.copy(os.path.join(SRC, "COMPUTATIONAL_SCOPE.txt"), comp_dst)
new_dir = os.path.join(comp_dst, "Baseline_Additions"); os.makedirs(new_dir)
for f in ("verify_monodromy_index.py", "Monodromy_Index_Results.json", "check_Ms_bound.py", "Ms_Bound_Sanity.json"):
    shutil.copy(os.path.join("/home/claude/d2", f), new_dir)
dd = "/home/claude/outputs/Director_D_Transport_Bridges_2026-11-11/verification"
for f in ("verify_transport_bridges.py", "Transport_Bridge_Results.json"): shutil.copy(os.path.join(dd, f), new_dir)
batch = json.load(open("/home/claude/batch_results.json"))
NOTE = {"verify_control_identification.py": "requires source/Operational_Identification_of_Records_Controls_and_Continuous_Time_Dynamics.tex at a path absent from the packet",
        "verify_structural_controls.py": "requires results/Structural_Controls.json at a path absent from the packet",
        "graph_sampling.py": "requires reconciliation_results.json, absent from the packet",
        "verify_declared_calibration_experiment.py": "refuses to overwrite its stored result by design; rerun from a fresh copy reproduced the stored result byte-identically",
        "binary_factors.py": "differs from the stored output only in the endpoint_error diagnostic at the 1e-16 level; all reported values agree",
        "certify_four_vertex.py": "prints a summary line while the stored .expected file is the written certificate; the summary values 4.38610947e-51 and 1.83231743e-29 agree with it"}
rows = []
for r in batch:
    name = os.path.basename(r["script"])
    rows.append(dict(program=r["script"], status=r["status"], stored_output_compared=("yes" if "stdout_equals_expected" in r else "no stored stdout"),
                     stdout_equals_stored=str(r.get("stdout_equals_expected", "")), note=NOTE.get(name, "")))
rows.append(dict(program="Computational_Material/Weak_Readout_Gain/verify_weak_gain_precision.py (documented command, fresh output path)", status="RAN_OK",
                 stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note="197 predicates"))
rows.append(dict(program="Computational_Material/Joint_Calibration_Check/verify_declared_calibration_experiment.py (documented command, fresh copy)", status="RAN_OK",
                 stored_output_compared="yes", stdout_equals_stored="result file byte-identical", note="comparator reports 0 mismatches over 45 identified sets"))
wcsv(os.path.join(comp_dst, "RERUN_RECORD_2026-11-12.csv"), rows)
cidx = []
for d in sorted(os.listdir(os.path.join(SRC, "Computational_Material"))):
    if os.path.isdir(os.path.join(SRC, "Computational_Material", d)):
        cidx.append(dict(directory="COMPUTATION/Computational_Material/" + d, papers=" ".join(p["id"] for p in P if d in p["computation"])))
cidx.append(dict(directory="COMPUTATION/Baseline_Additions", papers="D8 G7"))
wcsv(os.path.join(REG, "COMPUTATION_INDEX.csv"), cidx)

# ------------------------------------------------------------------ readiness
ready = []
for row in index:
    pid = row["id"]; parts = [c for c in cross if c["paper"] == pid]
    regs = [r for r in registry if r["paper"] == pid]
    nsrc = sum(1 for c in parts if int(c["editable_sources"]) > 0); n = len(parts)
    gaps = []
    if row["kind"] == "planned": gaps.append("manuscript not written")
    if n and nsrc < n: gaps.append(f"{n - nsrc} of {n} parts have no editable source (PDF only)")
    na = sum(1 for r in regs if r["status"] == "PROOF_NOT_ADJACENT")
    if na: gaps.append(f"{na} statements without an adjacent proof paragraph: proof location to be confirmed")
    nn = sum(1 for r in regs if r["status"] == "RESULT_NOTE_WITHOUT_LABELLED_STATEMENT")
    if nn: gaps.append(f"{nn} parts state results without labelled theorems")
    if row["kind"] in ("collection", "synthesis"): gaps.append("assembled from separate notes; a single continuous manuscript with one bibliography is not yet written")
    if pid in ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"): gaps.append("linear proof order across the D series not yet established (OP-02)")
    ready.append(dict(paper=pid, title=row["title"], kind=row["kind"], pages=row["pages"], parts=n, parts_with_editable_source=nsrc,
                      labelled_statements=row["statements"], independent_referee_report="none", gaps="; ".join(gaps) or "none recorded"))
wcsv(os.path.join(REG, "READINESS.csv"), ready)

# ------------------------------------------------------------------ open problems
OPS = [
 ("OP-01", "D3 D5 D8", "mathematics", "Independent verification of the fixed-mass finite-part theorem (D3-01-01) and its inputs. The boundary input (B9) of D8 part 1 uses a constant M_s that the manuscript does not define; D8-17-02 supplies and bounds it. That note is new and unrefereed.", "open; one input addressed by D8-17-02 pending independent check"),
 ("OP-02", "D1-D8", "mathematics", "A linear proof order for the D series. D4 cites Theorem 7 of D3 and D3 lists Theorem 3, Corollary 4 and Theorem 6 of D4 among its references; the technical notes also mention the later main theorems. Non-circularity has to be exhibited as an explicit dependency order.", "open"),
 ("OP-03", "D3 D4 G6 B1", "manuscript", "D3, D4 and G6 and twelve supporting notes of B1 exist only as PDF. Editable sources have to be reconstructed before revision or submission.", "open"),
 ("OP-04", "D1 D5", "mathematics", "Relative leading law along vanishing scaled mass, moving-edge expansions, general filling and sharper boundary-entropy control for the Wilson-Dirac relative entropy.", "open"),
 ("OP-05", "E1", "mathematics", "The correlation-dependent correction crossing is supported by a high-precision numerical root only; an outward-rounded enclosure of the augmented crossing system is required.", "open"),
 ("OP-06", "E2", "mathematics", "Sharp Bessel moving-window ultraviolet limits and the proposed noncommuting ultraviolet construction: quantified remainder hypotheses and a complete construction are not supplied.", "open"),
 ("OP-07", "G2", "mathematics", "Coherent output-entropy optimization for partition outputs, distinct from the solved order-only communication maximum.", "open"),
 ("OP-08", "program", "mathematics", "Exact eight-output quantum-copying optimum. Recorded as unresolved in the Director B and C records; no statement of the problem is contained in the baseline documents.", "open; statement to be recovered"),
 ("OP-09", "program", "physical correspondence", "No correspondence between any mathematical structure of the program and physical preparations, controls, records, units or clocks has been established. No prephysical structure has been shown to select quantum or classical mechanics.", "open"),
 ("OP-10", "G1 G3 G7", "foundations", "Any finite relational candidate must supply a limit construction whose pure-state space is a compact homogeneous space under a connected group, and tomographic locality, before continuous-reversibility reconstructions of quantum theory apply. The limit is not canonical: the cyclic groups Z_n have a direct-limit closure U(1), which is connected, and an inverse limit, the profinite integers, which is totally disconnected.", "open obligation"),
 ("OP-11", "G4 G6 G7", "foundations", "Transport structure does not select a representation: finite-group loop products, the Levi-Civita rotation and the spin-j phase are holonomies of the same loop. G6 proves reconstruction of a connected Hermitian matrix from edge magnitudes and cycle products up to diagonal phase gauge; what would select complex phases with vanishing third-order interference from a prephysical structure is not identified.", "not identified"),
 ("OP-12", "program", "sources", "Two historical source identities remain unresolved: an earlier comprehensive claim-status inventory and the exact verifier named in one older model specification.", "open"),
 ("OP-13", "COMPUTATION", "reproducibility", "Three inherited programs require input files at paths absent from the packet (verify_control_identification.py, verify_structural_controls.py, graph_sampling.py).", "open"),
 ("OP-14", "all", "manuscript", "Statements with status PROOF_NOT_ADJACENT and parts with status RESULT_NOTE_WITHOUT_LABELLED_STATEMENT need a confirmed proof home or a labelled statement.", "open"),
 ("OP-15", "F7 G7", "manuscript", "Manuscripts for the finite-sample CHSH tests and for the transport bridge assessment are not written; their results exist as review records only.", "open"),
 ("OP-16", "REVIEW_RECORDS", "method", "The Director B and C records were made under PCP-2026-11-10-R13; the Director D records and this baseline under ACR 1.0. The two rule texts differ and have not been mapped clause by clause. No evidence exists on whether either procedure improves correctness over ordinary review.", "open"),
]
wcsv(os.path.join(REG, "OPEN_PROBLEMS.csv"), [dict(id=a, scope=b, type=c, statement=d, state=e) for a, b, c, d, e in OPS])
br = json.load(open("/home/claude/outputs/Director_D_Transport_Bridges_2026-11-11/registers/BRIDGE_CANDIDATE_REGISTER.json"))
br["date"] = "2026-11-12"
br["retained_outliers"]["monodromy_integer_index"] = "1 for enclosing loops and 0 for control loops at hbar = 0.05, 0.04, 0.03, 0.02 (two loops); see COMPUTATION/Baseline_Additions"
br["edges"].append({"from": "PRE-REL", "to": "QT", "type": "exact_correspondence", "statement": "For supplied operator data, a connected Hermitian matrix is reconstructed from edge magnitudes and a fundamental set of complex cycle products up to diagonal phase gauge; the generated algebra detects connected components but not the support graph.", "locator": "Paper G6, Invariant Relational Selection and Approximate Symmetry", "status": "PROOF_IN_MANUSCRIPT; operator data are supplied, not derived"})
br["edges"].append({"from": "PRE-REL", "to": "QT", "type": "obstruction", "statement": "The limit construction owed by a finite candidate is not canonical: Z_n has direct-limit closure U(1) (connected) and inverse limit the profinite integers (totally disconnected).", "locator": "OPEN_PROBLEMS OP-10", "status": "standard mathematics; reasoned, not executed"})
json.dump(br, open(os.path.join(REG, "BRIDGE_CANDIDATE_REGISTER.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ program documents
series_tbl = ""
for s, name in SERIES.items():
    series_tbl += f"\n### Series {s}: {name}\n\n| Paper | Title | Kind | Pages | Labelled statements |\n|---|---|---|---:|---:|\n"
    for r in index:
        if r["id"][0] == s: series_tbl += f"| {r['id']} | {r['title']} | {r['kind']} | {r['pages']} | {r['statements']} |\n"
w(os.path.join(OUT, "PROGRAM", "PAPER_INDEX.md"), f"# {PROGRAM}: paper index\n\n{HEAD}\n"
  "Each paper has one folder under `PAPERS/` holding the assembled PDF, its parts and the available sources. "
  "`registers/PAPER_INDEX.csv` is the machine-readable form and adds the papers each one cites.\n" + series_tbl)

w(os.path.join(OUT, "PROGRAM", "CHARTER.md"), f"""
# {PROGRAM}: program charter

{HEAD}
## 1. Aim

The program asks what would justify interpreting a proposed relational, informational or algebraic structure as a physical model. Its stated target is an explained emergence of quantum mechanics and of classical mechanics from stated primitives, together with a complete map of the relations among the structures used. The target is a direction of work. The program proceeds on the working expectation that it will not be reached, and no document of this baseline claims that it has been.

## 2. Three questions kept apart

1. **Specify.** Which primitives, relations and equivalences can be defined without assuming the physical structure being sought?
2. **Derive and challenge.** Which conclusions follow from stated assumptions, and which proposed implications fail?
3. **Discriminate.** Which observations distinguish candidate models once calibration and uncertainty are included?

A mathematical premise, a derived result, a computed instance and a physical correspondence are different kinds of statement (`STANDARDS.md`). No correspondence between a mathematical structure of this program and physical preparations, controls, records, units or clocks has been established.

## 3. Structure of the baseline

The work is divided into {len(index)} papers in seven series (`PAPER_INDEX.md`). A paper is the unit of statement, proof and review. Shared conventions are in paper A3. Program-level relations are held in registers, outside the papers:

| Register | Content |
|---|---|
| `THEOREM_REGISTRY.csv` | every labelled statement, with a stable identifier, its paper, part and page, its status and its locator in the 10 November 2026 edition |
| `CITATIONS_BETWEEN_PAPERS.csv` | each citation of one paper by another, by title mention or explicit locator |
| `OPEN_PROBLEMS.csv` | open mathematical, foundational, manuscript and reproducibility items |
| `READINESS.csv` | per paper: sources available, statements needing a proof home, recorded gaps |
| `COMPONENT_CROSSWALK.csv` | every part of every paper against the 10 November 2026 component it came from, with both digests and the nature of any change |
| `BRIDGE_CANDIDATE_REGISTER.json` | typed map of exact correspondences, postulates, obstructions, discriminators and untested transfers between model classes |
| `COMPUTATION_INDEX.csv` | computation directories against papers |

Series G contains the structures proposed without physical interpretation (relational structures, equality patterns, signed graphs) and the assessment of bridge candidates. Series B to F are conventional models in which the requirements for a physical interpretation can be examined; they assume quantum states, space or time where stated. The series are parallel lines of work. They are not successive derived stages of one theory.

## 4. Withdrawn and stipulated constructions

`NEGATIVE_CONTROLS/` holds two constructions that are not candidates: the contextual toy TO-0, withdrawn as a physical ontology because unrestricted contextual tables do not select the quantum subset, and FAR-1, a finite amplitude-record model in which complex amplitudes, tensor products, the probability rule, the update index and the expansion law are all imported. They are retained as counterexamples and test objects.

## 5. Responsibility and contributions

{AUTHOR} directs the research and is the sole named author and the responsible party for every claim. `CONTRIBUTIONS.md` records assistance. Assistance by an AI system implies no endorsement by its provider, no external peer review and no institutional endorsement.
""")

w(os.path.join(OUT, "PROGRAM", "STANDARDS.md"), f"""
# {PROGRAM}: standards for statements, proofs, computation and citation

{HEAD}
## 1. Kinds of statement

| Kind | What it establishes |
|---|---|
| Mathematical premise | a state space, relation, probability rule, composition or observation menu chosen for a model; not established by a theorem that assumes it |
| Derived result | a statement following from displayed assumptions and a proof; its scope includes the dimension, topology, normalization and measurement access used |
| Computed instance | an exact finite enumeration, a rational certificate or a numerical evaluation; numerical precision is distinct from an error enclosure |
| Physical correspondence | a warranted relation between a mathematical experiment and physical preparations, controls and records, with units and uncertainty |

## 2. Statements and proof homes

Each labelled statement has one identifier in `THEOREM_REGISTRY.csv`, of the form *paper*-*part*-*sequence*, and one proof home: the part in which it is stated with its proof. A displayed copy elsewhere is a restatement and names its source. Cite a result by registry identifier, or by paper, part title and label. The registry column `legacy_locator` resolves citations written against the 10 November 2026 edition.

Registry status values:

| Status | Meaning |
|---|---|
| `PROOF_IN_MANUSCRIPT` | a proof paragraph follows the statement in its part; the proof has not been independently refereed |
| `PROOF_NOT_ADJACENT` | no proof paragraph lies between the statement and the next labelled statement; the proof may be assembled in later sections or lie in another paper, and its location is to be confirmed |
| `CONDITIONAL_ON_NAMED_INPUTS` | the statement names estimates of other papers as hypotheses |
| `RESTATEMENT` | a displayed copy of a result whose proof home is elsewhere |
| `RESULT_NOTE_WITHOUT_LABELLED_STATEMENT` | the part states its results in prose or tables without a labelled theorem |

The status values were assigned mechanically from the typeset text. They describe the manuscripts; they are not verdicts on correctness. No statement in this baseline has an independent referee report.

## 3. Conditional statements and limits

A conditional statement lists each premise as a mathematical assertion that can be checked. An exact finite identity, an identity of formal expansion coefficients, a finite-order uniform estimate and an empirical inference are different claims. A bounded remainder does not identify its limit; uniformity at fixed interior cutoff does not give a moving-edge theorem; an additive error tending to zero need not be small relative to a leading term that also vanishes.

## 4. Computation

A program is cited for the conclusion it establishes. Exact symbolic or rational results are identities on their stated domains. A numerical value is a certificate only with outward rounding or rational bounds covering all truncation errors. Counts of successful predicates are not theorem counts. `COMPUTATION/RERUN_RECORD_2026-11-12.csv` states which programs were executed for this baseline and how their output compared with the stored output.

## 5. Front matter

Every paper names {AUTHOR}, {AUTHOR_TITLE}, {AUTHOR_LOCATION}, and carries the contributions statement. Papers do not contain editorial history; changes between editions are recorded in `COMPONENT_CROSSWALK.csv` and `TEX_SOURCE_EDITS.json`.

## 6. Review

A review record states its subject, its question, what was inspected or executed, and a scoped finding. Review records are kept in `REVIEW_RECORDS/`, apart from the papers. A finding made by the party that drafted the work, or by an AI system at the author's direction, is not an independent review.
""")

w(os.path.join(OUT, "PROGRAM", "CONTRIBUTIONS.md"), f"""
# {PROGRAM}: contributions

{HEAD}
- **{AUTHOR}** ({AUTHOR_TITLE}, {AUTHOR_LOCATION}): research direction, selection of questions and models, publication standards; sole named author; responsible for all claims.
- **ChatGPT (OpenAI)**: derivations, critical checks, computation and manuscript preparation across the collection, including the Wilson–Dirac continuation, the opening studies and the five further studies.
- **LLM Director B and LLM Director C**: the review records in `REVIEW_RECORDS/Director_B` and `Director_C`, and (Director C) the FAR-1 specification, produced in sessions directed by the author; their handoffs do not record a provider.
- **Claude (Anthropic)**: the Director D assessment of transport, holonomy and monodromy as bridge candidates; the note *A Uniform Sobolev Bound for the Continuum Cross-Block Interpolants* (paper D8, part 17); the reconciliation of the collection into this baseline (paper plan, registers, separation of the calibration and Wilson uniform-limit studies, standalone editions of the opening studies, location normalization, reruns).
- **Gemini (Google), Grok (SpaceXAI), DeepSeek (High-Flyer)**: contributions to the wider research process; attribution of particular arguments is limited to traceable records.

The credit does not specify or imply equal contributions, independent verification or identical roles. Assistance does not imply provider endorsement.
""")

# figures
fd = os.path.join(OUT, "PROGRAM", "figures"); os.makedirs(fd, exist_ok=True)
for f in ("Diagram/Program_Questions_Models_and_Physical_Correspondence.pdf", "Diagram/Structure_Observation_and_Physical_Identification.pdf"):
    shutil.copy(os.path.join(SRC, f), fd)

# ------------------------------------------------------------------ negative controls
nc = os.path.join(OUT, "NEGATIVE_CONTROLS", "FAR-1"); os.makedirs(nc)
for f in os.listdir(os.path.join(W, "FAR1_Research_Handoff")): shutil.copy(os.path.join(W, "FAR1_Research_Handoff", f), nc)
w(os.path.join(OUT, "NEGATIVE_CONTROLS", "README.md"), f"""
# Negative controls

{HEAD}
**TO-0** (contextual toy). Withdrawn as a candidate physical ontology: unrestricted contextual tables contain local, quantum and Popescu–Rohrlich-type behaviours and do not select the quantum subset or a mechanism. Its mathematics on contextuality comparisons is retained in the Director B and C records. No separate TO-0 document was supplied with the packets used for this baseline.

**FAR-1** (finite amplitude-record model), folder `FAR-1/`. A stipulated finite model; complex amplitudes, tensor products, the trace probability rule, the update index and the expansion law are imported. Its files are byte-identical to the supplied session packet. `verify_toy_models.py` writes to a fixed absolute path; with that path redirected its output is identical to `verified_toy_results.json`.

Neither construction is evidence for or against any physical claim.
""")

# ------------------------------------------------------------------ review records
rr = os.path.join(OUT, "REVIEW_RECORDS")
b = os.path.join(W, "Director_B_CHSH_Memory_Sequential_QA_2026-11-11"); c = os.path.join(W, "Director_C_Unknown_Orientation_Adversarial_Audit_2026-11-11")
for src, name, keep in ((b, "Director_B", ["README.md", "reports", "verification", "subreviews", "receipts", "registers/DB_NEW_SCOPED_FINDINGS_8.csv", "registers/C_NEW_SOURCE_12.csv"]),
                        (c, "Director_C", ["README.md", "reports", "verification", "subreviews", "registers/NEW_C_SCOPED_FINDINGS_13.csv", "registers/NEW_NUMERICAL_WATCH_9.csv", "source/SOURCE_RECEIPTS.json"])):
    for k in keep:
        s = os.path.join(src, k); d = os.path.join(rr, name, k)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copytree(s, d) if os.path.isdir(s) else shutil.copy(s, d)
ddst = os.path.join(rr, "Director_D"); shutil.copytree("/home/claude/outputs/Director_D_Transport_Bridges_2026-11-11", ddst)
w(os.path.join(ddst, "ADDENDUM_2026-11-12.md"), f"""
# Director D addendum, 12 November 2026

Reviewing participant: LLM Director D — Claude (Anthropic), at the direction of {AUTHOR}. One participant; every check below is a self-check. ACR 1.0, absorbed text with retrieval; nothing is host-enforced.

1. **Monodromy index.** The lattice shift reported on 11 November as 0.984 and 0.985 in units of the local cell vector is an integer index. Carrying the cell round the loop and recording the index of the point on which the transported vector ends gives exactly 1 for loops enclosing the focus-focus value and 0 for control loops, at ħ = 0.05, 0.04, 0.03 and 0.02 (two loops). The non-integer values measured unequal level spacing in neighbouring columns. Program and result: `COMPUTATION/Baseline_Additions/verify_monodromy_index.py`. Finding D-TRN-002 is unchanged in disposition; its residual obligation is discharged for the computed cases.
2. **In-program home of the holonomy theme.** Paper G6 proves reconstruction of a connected Hermitian matrix from edge magnitudes and a fundamental set of complex cycle products up to diagonal phase gauge. Cycle products are discrete holonomies. The 11 November nonselection finding stands: the operator data in G6 are supplied, not derived.
3. **Limit constructions are not canonical.** The obligation in D-TRN-006 does not determine its own solution: the cyclic groups have a connected direct-limit closure and a totally disconnected inverse limit. Recorded as OP-10. Reasoned, not executed.
4. **Wilson–Dirac boundary input.** The constant M_s in the display preceding (B9) of *Cross-Boundary Trace-Class Estimates* is not defined in that manuscript. Paper D8, part 17 defines the space on which it acts and proves M_s ≤ 1/2 + max{{c_s, c_s′}}, independent of the interpolation parameter, the scaled mass and the lattice size, using the Shamir–Strichartz multiplier theorem. Disposition: SUPPORTED_IN_SCOPE as a derived result on a reasoned proof with an inspected external theorem; a finite-grid computation is consistent with it and is not part of the proof. (B6)–(B8), the Chebyshev approximation rate and the remainder of the Wilson chain were not re-examined. Independent verification remains open (OP-01).
5. **Reruns.** The two current exact calculations reproduce their stored results byte-identically. Of 66 inherited programs, 62 ran; 38 of the 41 with a stored standard output matched it; the exceptions are itemized in `COMPUTATION/RERUN_RECORD_2026-11-12.csv`.
6. **Baseline.** The 10 November 2026 collection is reorganized into {len(index)} papers with registers. Root Review state: G1 Grounding, open. No ontology is selected.
""")
w(os.path.join(rr, "README.md"), f"""
# Review records

{HEAD}
Records of reviews made in AI-assisted sessions directed by the author. They are not independent reviews. Directors B and C worked under PCP-2026-11-10-R13; Director D under ACR 1.0. The large inherited identifier registers and the nested source archives of the Director B and C handoffs are not duplicated here; the complete handoffs are identified by digest in `MANIFEST.json`.
""")

# ------------------------------------------------------------------ legacy
lg = os.path.join(OUT, "LEGACY"); os.makedirs(lg)
shutil.copy(os.path.join(SRC, "New_Studies/Calibration_Identified_Sets_and_Uniform_Limits.pdf"), lg)
shutil.copytree(os.path.join(SRC, "New_Studies/Calibration_and_Uniform_Limits_Source"), os.path.join(lg, "Calibration_and_Uniform_Limits_Source"))
shutil.copytree(os.path.join(SRC, "Related_Source_Editions"), os.path.join(lg, "Related_Source_Editions"))
shutil.copytree(os.path.join(SRC, "Source_Corrections"), os.path.join(lg, "Source_Corrections"))
shutil.copytree(os.path.join(SRC, "Studies/Source"), os.path.join(lg, "Studies_Source_2026-11-10"))
for f in ("README.txt", "CONTENTS.txt", "SOURCE_EDITING_NOTE.txt", "SOURCE_EDITION_NOTES.txt", "VOLUME_CONTENTS.json", "FILE_MANIFEST.json", "Computational_Material/Prior_Computation_Account.txt"):
    shutil.copy(os.path.join(SRC, f), os.path.join(lg, "2026-11-10_" + os.path.basename(f)))
w(os.path.join(lg, "README.md"), f"""
# Legacy material from the 10 November 2026 edition

{HEAD}
The 10 November 2026 review packet (SHA-256 `{INPUTS['Review packet, 10 November 2026']}`) is the preceding edition. Its two assembled volumes are not duplicated here. This folder keeps what the papers do not carry: the combined study *Calibration, Identified Sets and Uniform Limits* with its source (now papers F4 and D5), the related source editions and cited notes, the source-correction records, the original study sources, and the preceding edition's descriptive files, manifest and contents.
""")

# tools
td = os.path.join(OUT, "tools"); os.makedirs(td)
for f in ("paper_plan.py", "build_tex.py", "assemble.py", "finalize.py"): shutil.copy(os.path.join("/home/claude/bb/tools", f), td)

# ------------------------------------------------------------------ README, manifest, verifier
npages = sum(int(r["pages"]) for r in index)
w(os.path.join(OUT, "README.md"), f"""
# {PROGRAM}

{HEAD}
This is the baseline edition of the research program. It replaces the two-volume arrangement of 10 November 2026 by {len(index)} papers in seven series ({npages} assembled pages; two papers are planned and not yet written), with program-level registers held outside the papers.

## Where to start

1. `PROGRAM/CHARTER.md` — aim, structure and responsibility.
2. `PROGRAM/STANDARDS.md` — kinds of statement, proof homes, registry status values, computation and citation.
3. `PROGRAM/PAPER_INDEX.md` — the papers. Paper A1 is the program overview.
4. `PROGRAM/registers/` — theorem registry ({len(registry)} rows), open problems, readiness, citations, component crosswalk, bridge-candidate map.

## Layout

| Folder | Content |
|---|---|
| `PROGRAM/` | charter, standards, paper index, contributions, registers, the two program figures |
| `PAPERS/` | one folder per paper: assembled PDF, `parts/`, `source/` |
| `COMPUTATION/` | the computational material of the preceding edition with unchanged relative paths, additions made for this baseline, and the rerun record |
| `NEGATIVE_CONTROLS/` | withdrawn and stipulated constructions kept as counterexamples |
| `REVIEW_RECORDS/` | records of AI-assisted reviews directed by the author |
| `LEGACY/` | material of the preceding edition that the papers do not carry |
| `tools/` | the programs that built this edition |

## Scope

The collection establishes conditional mathematics, obstructions and counterexamples. It establishes neither a prephysical substrate nor a physical ontology, and it contains no experimental observation. No paper has been independently refereed. `PROGRAM/registers/READINESS.csv` and `OPEN_PROBLEMS.csv` state what each paper still lacks.

## Checking this edition

`python3 verify_baseline.py` recomputes the digest of every file against `MANIFEST.json`, checks that every component of the preceding edition is accounted for in the crosswalk, that registry identifiers are unique and point to existing papers, and that every assembled paper names the author, title and location. A pass is a local fact about these files; it authenticates nobody and certifies no proof.
""")

open(os.path.join(OUT, "verify_baseline.py"), "w").write('''#!/usr/bin/env python3
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
''')
files = {}
for dp, _, fs in os.walk(OUT):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), OUT)
        if rel == "MANIFEST.json": continue
        files[rel] = dict(sha256=sha(os.path.join(dp, f)), size=os.path.getsize(os.path.join(dp, f)))
json.dump(dict(baseline=BASELINE_ID, date=BASELINE_DATE, author=AUTHOR, author_title=AUTHOR_TITLE, author_location=AUTHOR_LOCATION,
               inputs_sha256=INPUTS, scope="file identity only; not an external signature and not a certificate of scientific correctness",
               files=dict(sorted(files.items()))), open(os.path.join(OUT, "MANIFEST.json"), "w"), indent=1)
print(len(files), "files;", npages, "assembled pages;", len(registry), "registry rows")
