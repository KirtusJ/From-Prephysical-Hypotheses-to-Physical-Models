#!/usr/bin/env python3
"""Compile the manuscripts that the 12 November 2026 baseline typesets from supplied TeX sources:
the program overview, the six opening studies as standalone papers, and the two papers obtained by
separating the combined calibration / Wilson uniform-limit study.

Bodies are taken verbatim from the 10 November 2026 sources except for the substitutions listed in
EDITS (each is also written to tex_edits.json for the component crosswalk).  Legacy section numbers of
the opening studies are preserved with \\setcounter{section}, so legacy theorem and equation numbers
remain valid locators.
"""
import json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_plan import P, STUDIES, AUTHOR, AUTHOR_TITLE, AUTHOR_LOCATION, PROGRAM

SRC = "/home/claude/work/Review_Materials"
OUT = "/home/claude/bb/tex"
ST = os.path.join(SRC, "Studies/Source")
CAL = os.path.join(SRC, "New_Studies/Calibration_and_Uniform_Limits_Source")

ABSTRACT = {
"overview": open(os.path.join(ST, "Collections_Studies.tex")).read().split("\\textbf{Abstract}\\par")[1].split("\\par")[0].strip(),
"relational": ("Finite relational structures, positive event kernels and marginal families are examined for what they determine "
 "under explicit mathematical assumptions. Every finite structure of a fixed positive-arity signature has a core, unique up to "
 "isomorphism in its homomorphism-equivalence class, and the equivalence is characterized by Boolean probes. A rank obstruction "
 "limits operational idempotence under factorizing composition. For positive event kernels, bounded affine observations under a "
 "singular normalizer are characterized, and deterministic and conditional aggregation are distinguished. An exact four-variable "
 "extension interval shows how matching marginals constrain a joint law without fixing it. Symmetry alone supplies neither a "
 "probability law nor a metric. None of the constructions assigns a physical clock, spatial metric, detector, source law or "
 "quantum state space."),
"signed_graphs": ("Finite signed-graph models are studied as mathematical comparators. For a graph double-well functional built from "
 "the signless Laplacian, an exact threshold separates the unique trivial minimum from nonzero minimizers, and zero-action "
 "configurations of a connected graph exist exactly when the graph is bipartite. Action-count statistics are computed for trees and "
 "cycles through an even-subgraph formula, together with a reduced sign law and its conditional mixedness. Complete-bipartite "
 "spectra illustrate dependence on the chosen operator. One four-sign law has unique five- and six-coordinate exact extensions and "
 "no seven-coordinate exact extension; sharp finite and infinite approximation distances form an odd\\textendash even staircase, and "
 "an exact action-range tradeoff is given. Quadratic weights are not closed under deletion. A variational minimum does not by "
 "itself choose a sampling law or an observation instrument."),
"resources": ("Classical probability models are used to separate invariance, consistency, observable information and controllable "
 "communication. One common normalized reference and a bound on the relative entropy of the complete preparation bound the "
 "accessible information; marginal budgets alone do not. Entropy under a mean-cost constraint is finite under a Gibbs summability "
 "condition, and an explicit example has a finite entropy supremum without a maximizer. Paintbox families can agree through any "
 "prescribed finite order before separating. The entropy of quotient outputs is distinguished from controllable messages. "
 "Deterministic operations of fixed finite arity on finite equivalence relations that are natural under every restriction are "
 "classified, and a stochastic selection theorem with a local bound is proved. Counts of positions or repetitions are not "
 "assigned physical time, spatial volume or energy without a separate resource model."),
"statistics": ("Source sampling, query sampling, report errors and errors in a comparison reference are separated in specified "
 "mathematical experiments. Exact overlap counting gives the variance of complete collision statistics, and two sources with "
 "matching pair statistics are compared through triple collisions. A half-credit score extends triple equality to inconsistent "
 "pair reports and has a sharp single-report sensitivity. Sparse random queries are analysed with the complete variance, including "
 "the requirement that the report population be fixed before the queries. Reference sampling with a quality gap gives "
 "finite-population calibration guarantees, and a minimum worst-case query cap is proved for separating adjacent error counts. "
 "All numerical guarantees concern the specified experiments; they are not results of physical trials."),
"quantum_families": ("Ordinary complex qubit Hilbert spaces, tensor products, density operators and Born measurements are taken as "
 "explicit assumptions, and several state families are compared within that formalism: a shared latent pure-product mixture, "
 "phase-paired families with an unchanged signed outcome law, ordered singlet dimers, canonical minimum-spin and maximum-spin "
 "mixtures, and a fixed-temperature Casimir Gibbs law. A matched projective family is constructed; a Hamiltonian invariant under "
 "diagonal $SU(2)$ and all qubit permutations has no unique pure ground ray for three or more qubits; restriction consistency, "
 "infinite extension and finite-temperature limits are determined for the stated families. Relative-reference calculations "
 "distinguish a common group action from independently randomized frames, and loop products and oriented triple invariants are "
 "treated as formal group-valued transport. None of the results derives the quantum apparatus from signed labels or from a "
 "relational quotient."),
"operational": ("For finite conventional models \\textemdash{} probability kernels, hidden-state models, quantum states and "
 "continuous-time Markov generators \\textemdash{} the paper determines which features are fixed by a stated menu of observations "
 "and interventions. Results include an exact criterion for controlled reduction and a complete-history bound under uniform row "
 "error; a parity-shift process with exact innovation coordinates; classical realization rank with finite-sample certificates; "
 "anytime-valid likelihood-mixture tests for complete record laws; nonidentification of fragment factorization from a final "
 "channel; sharp control criteria for positive hidden realizations; calibration-induced identification intervals; and, for sampled "
 "generators, two positive generators with all integer-time samples equal, exact identification from two incommensurate times, and "
 "the absence of uniform inverse stability over unbounded rates. Identifiability within a menu does not establish that the chosen "
 "states, controls or time coordinate describe a particular physical system."),
}
PID = {}
for p in P:
    for k, v in p["parts"]:
        if k in ("study", "split"): PID[v] = p["id"]

EDITS = []
def sub(body, old, new, where):
    assert body.count(old) == 1, (where, old, body.count(old))
    EDITS.append(dict(file=where, old=old, new=new))
    return body.replace(old, new)

def titlepage(pid, title, abstract, date_line):
    return rf"""\begin{{titlepage}}
{{\small\sffamily \ProgramTitle\hfill Paper {pid}\par}}
\vspace*{{16mm}}
{{\LARGE\bfseries\raggedright\hyphenpenalty=10000 {title}\par}}
\vspace{{11mm}}
{{\large {AUTHOR}\par}}
\vspace{{1mm}}
{AUTHOR_TITLE}\par
\AuthorLocation\par
\vspace{{2mm}}
{date_line}\par
\vspace{{11mm}}
\textbf{{Abstract}}\par
{abstract}\par
\vfill
{{\small Research direction and scholarly responsibility: {AUTHOR}.\par
Mathematical, computational and editorial assistance: ChatGPT (OpenAI). Editorial preparation of this edition: Claude (Anthropic).
Assistance does not imply provider endorsement.\par
This manuscript is prepared for scholarly assessment. Such preparation does not establish independent peer review,
experimental replication or institutional endorsement.\par}}
\end{{titlepage}}
\setcounter{{page}}{{2}}
"""

def bib_entries():
    items = {}
    for f in ("Scientific_References.tex", "operational_references.tex", "finite_signs_references.tex"):
        txt = open(os.path.join(ST, f)).read()
        parts = re.split(r"(?=\\bibitem\{)", txt)
        for part in parts:
            m = re.match(r"\\bibitem\{([^}]+)\}", part)
            if m: items[m.group(1)] = part.strip()
    return items

def cited_keys(body):
    keys = []
    for m in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", body):
        for k in m.group(1).split(","):
            k = k.strip()
            if k not in keys: keys.append(k)
    return keys

def run_xelatex(workdir, name):
    for _ in range(3):
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", name + ".tex"], cwd=workdir, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:]); raise SystemExit(f"xelatex failed for {name}")
    log = open(os.path.join(workdir, name + ".log"), errors="replace").read()
    undefined = sorted(set(re.findall(r"Reference `([^']+)' on page", log)) | set(re.findall(r"Citation `([^']+)' on page", log)))
    return undefined

def build_study(key):
    fname, legacy_section, title = STUDIES[key]
    pid = PID[key]
    wd = os.path.join(OUT, pid); os.makedirs(wd, exist_ok=True)
    shutil.copy(os.path.join(ST, "Scientific_Preamble.tex"), wd)
    body = open(os.path.join(ST, fname)).read()
    extra = ""
    if key == "overview":
        extra = open(os.path.join(ST, "Observation_Memory_Control_and_Time_Overview.tex")).read()
        shutil.copy(os.path.join(ST, "Observation_Memory_Control_and_Time_Overview.tex"), wd)
    open(os.path.join(wd, "body.tex"), "w").write(body)
    bibs = bib_entries(); keys = [k for k in cited_keys(body + extra) if k in bibs]
    missing = [k for k in cited_keys(body + extra) if k not in bibs]
    assert not missing, (key, missing)
    counter = "" if legacy_section is None else f"\\setcounter{{section}}{{{legacy_section - 1}}}\n"
    tex = ("\\documentclass[11pt,a4paper]{article}\n\\input{Scientific_Preamble.tex}\n"
           f"\\hypersetup{{pdftitle={{{title}}},pdfauthor={{{AUTHOR}}}}}\n\\begin{{document}}\n"
           + titlepage(pid, title, ABSTRACT[key], "10 November 2026 \\textperiodcentered{} baseline edition 12 November 2026")
           + ("\\clubpenalty=10000\n\\widowpenalty=10000\n" if key == "overview" else "")
           + counter + "\\input{body.tex}\n\\clearpage\n\\begin{thebibliography}{99}\n"
           + "\n".join(bibs[k] for k in keys) + "\n\\end{thebibliography}\n\\end{document}\n")
    name = f"{pid}_manuscript"
    open(os.path.join(wd, name + ".tex"), "w").write(tex)
    return pid, wd, name

def fix_cross_study_refs():
    """Replace references to labels of other studies by the legacy number and the title of the target paper."""
    # label -> (number, study key) from a compile of the legacy combined document
    aux = open("/home/claude/bb/studies/Mathematical_Studies.aux", errors="replace").read()
    lab = {m.group(1): m.group(2) for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", aux)}
    prefix = {"str": "relational", "fin": "signed_graphs", "pat": "resources", "sam": "statistics", "qua": "quantum_families", "op": "operational"}
    return lab, prefix

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    report = {}
    lab, prefix = fix_cross_study_refs()
    for key in STUDIES:
        pid, wd, name = build_study(key)
        if key != "overview":
            body = open(os.path.join(wd, "body.tex")).read()
            own = [k for k, v in prefix.items() if v == key][0]
            for m in sorted(set(re.findall(r"(?:Section|Sections|Theorem|Proposition|Lemma|Corollary|Equation)?~?\\(?:eq)?ref\{([a-z]+):([^}]+)\}", body))):
                pfx, rest = m
                if pfx != own:
                    label = f"{pfx}:{rest}"; num = lab[label]; tgt = prefix[pfx]
                    old = f"\\ref{{{label}}}"
                    new = f"{num} of \\emph{{{STUDIES[tgt][2]}}} (Paper {PID[tgt]})"
                    assert body.count(old) >= 1
                    EDITS.append(dict(file=STUDIES[key][0], old=old, new=new, occurrences=body.count(old)))
                    body = body.replace(old, new)
            open(os.path.join(wd, "body.tex"), "w").write(body)
        undefined = run_xelatex(wd, name)
        report[pid] = dict(tex=name + ".tex", undefined=undefined)
        assert not undefined, (pid, undefined)

    # ---- split of the combined calibration / Wilson study ----
    jc = open(os.path.join(CAL, "Joint_Calibration_and_Sampling.tex")).read()
    wil = open(os.path.join(CAL, "Wilson_Uniform_Limits.tex")).read()
    # F4: joint calibration without the Wilson section
    pid = PID["joint_calibration"]; wd = os.path.join(OUT, pid); os.makedirs(wd)
    shutil.copy(os.path.join(CAL, "Coverage_Table.tex"), wd)
    f4 = jc
    f4 = sub(f4, "\\input{Wilson_Uniform_Limits.tex}\n\n", "", "Joint_Calibration_and_Sampling.tex")
    f4 = sub(f4, "\\fancyhead[L]{\\small\\sffamily Calibration and uniform limits}\\fancyhead[R]{\\small Mathematical Supplement}",
             f"\\fancyhead[L]{{\\small\\sffamily Calibration and identified sets under joint sampling}}\\fancyhead[R]{{\\small Paper {pid}}}", "Joint_Calibration_and_Sampling.tex")
    f4 = sub(f4, "\\title{\\color{ink}\\sffamily From Prephysical Hypotheses to Physical Models\\\\[7pt]\\Large Mathematical Supplement\\\\[7pt]\\large Calibration, identified sets and uniform limits}",
             "\\title{\\color{ink}\\sffamily\\large From Prephysical Hypotheses to Physical Models\\\\[9pt]\\LARGE Calibration and Identified Sets under Joint Sampling}", "Joint_Calibration_and_Sampling.tex")
    f4 = sub(f4, "\\author{Kirtus Justus\\\\\\small Port Coquitlam, British Columbia, Canada}",
             f"\\author{{{AUTHOR}\\\\\\small {AUTHOR_TITLE}\\\\\\small {AUTHOR_LOCATION}}}", "Joint_Calibration_and_Sampling.tex")
    f4 = sub(f4, "\\date{10 November 2026}", "\\date{10 November 2026 \\textperiodcentered{} baseline edition 12 November 2026}", "Joint_Calibration_and_Sampling.tex")
    for key in ("dlmf", "wilson"):
        m = re.search(r"\\bibitem\{" + key + r"\}.*?\n", f4); assert m and f"\\cite{{{key}}}" not in f4
        EDITS.append(dict(file="Joint_Calibration_and_Sampling.tex", old=f"\\bibitem{{{key}}} (entry)", new="(removed; cited only in the separated Wilson note)"))
        f4 = f4.replace(m.group(0), "")
    name = f"{pid}_manuscript"; open(os.path.join(wd, name + ".tex"), "w").write(f4)
    und = run_xelatex(wd, name); assert not und, und; report[pid] = dict(tex=name + ".tex", undefined=und)

    # D5: Wilson conditional uniform additive limit
    pid = PID["wilson_uniform"]; wd = os.path.join(OUT, pid); os.makedirs(wd)
    pre = jc.split("\\title{")[0]
    pre = pre.replace("\\fancyhead[L]{\\small\\sffamily Calibration and uniform limits}\\fancyhead[R]{\\small Mathematical Supplement}",
                      f"\\fancyhead[L]{{\\small\\sffamily Conditional uniform additive limit}}\\fancyhead[R]{{\\small Paper {pid}}}")
    d5title = [p["title"] for p in P if p["id"] == pid][0]
    body = wil
    body = sub(body, "\\section{Wilson relative entropy: additive and relative limits}\\label{sec:wilson}",
               "\\section{Additive and relative limits}\\label{sec:wilson}", "Wilson_Uniform_Limits.tex")
    body = sub(body, "This section records a consequence", "This note records a consequence", "Wilson_Uniform_Limits.tex")
    bibs = {k: re.search(r"\\bibitem\{" + k + r"\}.*?\n", jc).group(0) for k in ("dlmf", "wilson")}
    abstract = ("For interval restrictions of infinite-chain Wilson\\textendash Dirac occupied-band projectors with scaled mass $\\mu=mL$, the "
                "fixed-positive-mass expansion of the relative entropy has logarithmic coefficient $\\mu^2/6$ and an explicit finite part. "
                "This note shows that the additive remainder is uniform on bounded mass intervals $0\\le\\mu\\le M$, at rate $O_M(1/\\log L)$, "
                "conditional on named finite-dimensional and trace-class estimates of the companion manuscripts, in particular the uniform "
                "boundary estimate (B9) of \\emph{Cross-Boundary Trace-Class Estimates for Wilson\\textendash Dirac Quasifree States}. "
                "The additive bound does not establish a relative leading law along sequences of vanishing mass; a logical example shows why.")
    d5 = (pre + f"\\title{{\\color{{ink}}\\sffamily\\large From Prephysical Hypotheses to Physical Models\\\\[9pt]\\LARGE {d5title.replace(chr(0x2013), '--')}}}\n"
          f"\\author{{{AUTHOR}\\\\\\small {AUTHOR_TITLE}\\\\\\small {AUTHOR_LOCATION}}}\n"
          "\\date{10 November 2026 \\textperiodcentered{} baseline edition 12 November 2026}\n\\begin{document}\n\\maketitle\n"
          f"\\begin{{abstract}}\n{abstract}\n\\end{{abstract}}\n\n" + body +
          "\n\\section*{Research and computational disclosure}\n"
          "This is an AI-assisted mathematical research manuscript prepared within the same research program as the cited companion "
          "manuscripts. The argument is presented for examination. It checks the uniform assembly of the cited estimates; it does not "
          "independently certify those estimates, and it does not constitute independent peer review. "
          "Mathematical, computational and editorial assistance: ChatGPT (OpenAI). Editorial preparation of this edition: Claude (Anthropic).\n\n"
          "\\begin{thebibliography}{9}\n" + bibs["dlmf"] + bibs["wilson"] + "\\end{thebibliography}\n\\end{document}\n")
    EDITS.append(dict(file="Wilson_Uniform_Limits.tex", old="(section of the combined study)", new="standalone note with title page, abstract, disclosure paragraph and its two references"))
    name = f"{pid}_manuscript"; open(os.path.join(wd, name + ".tex"), "w").write(d5)
    und = run_xelatex(wd, name); assert not und, und; report[pid] = dict(tex=name + ".tex", undefined=und)
    json.dump(dict(report=report, edits=EDITS), open(os.path.join(OUT, "tex_edits.json"), "w"), indent=1, ensure_ascii=False)
    for k, v in report.items(): print(k, v)

if __name__ == "__main__":
    main()
