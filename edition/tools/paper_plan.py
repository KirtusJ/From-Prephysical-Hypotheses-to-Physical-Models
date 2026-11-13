"""Declarative paper plan for the 12 November 2026 baseline of
From Prephysical Hypotheses to Physical Models.

Each paper lists its parts.  A part is one of
  ("component", index)   component index in the 10 November 2026 VOLUME_CONTENTS.json (0-based)
  ("study", key)         opening study recompiled standalone from Studies/Source
  ("split", key)         manuscript recompiled from the supplied source of the combined calibration/Wilson study
  ("figure", key)        program figure
  ("new", key)           manuscript first issued with this baseline
  ("planned", note)      manuscript not yet written; source records are named
Series letters:  A program, B observation and instruments, C fermionic and operator identification,
D Wilson-Dirac relative entropy, E spectral measures and compact groups, F information, calibration and
statistics, G relational structures and bridge candidates.
"""

AUTHOR = "Kirtus Justus"
AUTHOR_TITLE = "Theoretical Physicist"
AUTHOR_LOCATION = "Port Coquitlam, British Columbia, Canada"
PROGRAM = "From Prephysical Hypotheses to Physical Models"
BASELINE_DATE = "12 November 2026"
BASELINE_ID = "FPHPM-BASELINE-2026-11-12"

STUDIES = {
    # key: (source file, legacy section number in the 10 Nov Mathematical Studies, standalone title)
    "relational": ("Relational_Structures_and_Observation.tex", 1, "Relational Structures and the Limits of Observation"),
    "signed_graphs": ("Finite_Signed_Graphs_and_Extensions.tex", 2, "Finite Signed Graphs and Binary Extension Constraints"),
    "resources": ("Resources_and_Equality_Patterns.tex", 3, "Resources, Equality Patterns and Composition"),
    "statistics": ("Statistical_Comparisons_and_Reference_Errors.tex", 4, "Statistical Comparisons and Reference Errors"),
    "quantum_families": ("Quantum_State_Families_and_Symmetry.tex", 5, "Quantum State Families, Symmetry and Relative References"),
    "operational": ("operational_supplement.tex", 6, "Observation, Memory, Control, and Time in Finite Models"),
    "overview": ("Collections_Overview.tex", None, "Program Overview: Questions, Models and Physical Correspondence"),
}

P = []
def paper(pid, title, parts, scope=None, depends=(), computation=(), kind="article"):  # depends is filled from detected citations by the build
    P.append(dict(id=pid, title=title, parts=parts, scope=scope, depends=list(depends), computation=list(computation), kind=kind))

# ---------------- A: program ----------------
paper("A1", "Program Overview: Questions, Models and Physical Correspondence",
      [("study", "overview"), ("figure", "program"), ("figure", "observation")], kind="overview")
paper("A2", "Model-Specific Mathematical Results: Summary and Limits of Transfer", [("component", 1)], kind="overview")
paper("A3", "Mathematical Terminology", [("component", 84)], kind="reference")

# ---------------- B: observation and instruments ----------------
paper("B1", "What Does an Observation Identify? A Synthesis with Supporting Notes",
      [("component", 0)] + [("component", i) for i in range(52, 84)], kind="synthesis",
      scope=("The synthesis states, with examples, which properties of a specified model are fixed by a specified family "
             "of observations. The supporting notes that follow it give the detailed arguments for individual examples: "
             "source, gain and detector ambiguity, graph and scale observations, predictive dimension and history-dependent "
             "readout, and constraints on phase contrast, purity and paired-input data for conditional operations. "
             "Each note is restricted to its stated state space, observation menu and calibration premises."),
      computation=["Causal_Readout", "Instrument_and_Graph_Examples"])
paper("B2", "Operational Identification and Conditional Quantum Instruments", [("component", 12)])
paper("B3", "Identification from Restricted Measurements", [("component", 13)])
paper("B4", "Four-Preparation Tests for a Conditional Quantum Operation", [("component", 14)])

# ---------------- C: fermionic and operator identification ----------------
paper("C1", "Projector-Equivalent Wilson\u2013Dirac Hamiltonians and Dynamical Identification", [("component", 2)])
paper("C2", "Operational Identification and Calibration in Two-Mode Quasifree Systems", [("component", 4)])
paper("C3", "Calibrated Dynamical Identification in Fermionic Systems", [("component", 17)])
paper("C4", "Clock-Scale Ambiguity, Static CAR States, and Gibbs Modular Equivalence", [("component", 18)])
paper("C5", "Continuum and Finite-Lattice Two-Time Identification", [("component", 19)])
paper("C6", "Local Number-Conserving Response and Inference", [("component", 20)])
paper("C7", "Restricted Observables and CAR-State Distinguishability", [("component", 21)])

# ---------------- D: Wilson-Dirac relative entropy ----------------
paper("D1", "Relative Entropy of Finite-Interval Wilson\u2013Dirac Quasifree States", [("component", 3)])
paper("D2", "Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law", [("component", 50)])
paper("D3", "Finite Part of Wilson\u2013Dirac Relative Entropy", [("component", 15)])
paper("D4", "Uniform Modular Control and Nonlinear Convergence for Wilson\u2013Dirac Intervals", [("component", 16)])
paper("D5", "Conditional Uniform Additive Limit of Wilson\u2013Dirac Relative Entropy on Bounded Scaled Masses",
      [("split", "wilson_uniform")])
paper("D6", "Concentration Spectrum of the Half-Filled Sine Kernel: Periods, Tails and Plunge Windows",
      [("component", i) for i in (45, 46, 47, 48, 49)], kind="collection",
      scope=("Five articles on the discrete concentration problem for the half-filled sine kernel: higher-order modular "
             "periods, concentration eigenvalues from logarithmic connection coefficients, spectral tails and exact "
             "concentration logits, reciprocal traces and the plunge law, and positive moment bounds on growing plunge "
             "windows. They supply reference-kernel inputs used in the Wilson\u2013Dirac relative-entropy papers."))
paper("D7", "Reference Modular and Jacobi Estimates for a Half-Filled Fermion Interval",
      [("component", i) for i in (22, 24, 31, 32, 38, 40, 44)], kind="collection",
      scope=("Seven notes on the half-filled reference state of a finite fermion interval and its commuting Jacobi "
             "matrix: all-degree Jacobi estimates, exact occupation weights and particle\u2013hole pairing, logarithmic "
             "weighted modular control, the sharp logarithmic boundary moment, the sine-kernel endpoint, the fixed-index "
             "spectral expansion and the occupation logarithm. Each statement is for the specified reference kernel."))
paper("D8", "Wilson\u2013Dirac Covariance, Majorant and Boundary Estimates",
      [("component", i) for i in (23, 25, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 39, 41, 42, 43)] + [("new", "ms_bound")], kind="collection",
      scope=("Notes on interval restrictions of infinite-chain Wilson\u2013Dirac occupied-band projectors: "
             "cross-boundary trace-class estimates, exact spectral majorants, reference geometry and the two-bond "
             "asymptotic, Fourier-space boundary defects, the Hilbert\u2013Schmidt scaling limit, square-root-mass control, "
             "majorant moments and boundary corrections, and positive reference-modular traces, followed by a note that bounds the "
             "continuum cross-block interpolants on a fractional Sobolev space. Each statement keeps its "
             "stated infinite-chain, filling and scaling conditions."))

# ---------------- E: spectral measures and compact groups ----------------
paper("E1", "Positive Spectral Measures Under Finite Moment and Laplace Constraints", [("component", 5)])
paper("E2", "Compact-Group Transfer Spectra and Ultraviolet Operator Limits", [("component", 6)])

# ---------------- F: information, calibration and statistics ----------------
paper("F1", "Abstract Channels and Gaussian Capacity", [("component", 7)], computation=["Channel_and_Operational_Examples"])
paper("F2", "Stochastic Recovery from Information Loss and Equality of Channel Capacity", [("component", 8)], computation=["Channel_Recovery"])
paper("F3", "Calibration Uncertainty and Finite-Sample Identification", [("component", 9)], computation=["Joint_Calibration"])
paper("F4", "Calibration and Identified Sets under Joint Sampling", [("split", "joint_calibration")], computation=["Joint_Calibration_Check"])
paper("F5", "Statistical Precision under Weak Readout Gain", [("component", 11)],
      computation=["Weak_Readout_Gain"])
paper("F6", "Statistical Comparisons and Reference Errors", [("study", "statistics")], computation=["Finite_Examples"])
paper("F7", "Finite-Sample CHSH Tests against Popescu\u2013Rohrlich-Type Alternatives: Memory, Orientation Learning and Sequential Validity",
      [("planned", "Results are recorded in REVIEW_RECORDS/Director_B and REVIEW_RECORDS/Director_C; no manuscript has been written.")],
      kind="planned")

# ---------------- G: relational structures and bridge candidates ----------------
paper("G1", "Relational Structures and the Limits of Observation", [("study", "relational")], computation=["Finite_Examples"])
paper("G2", "Resources, Equality Patterns and Composition", [("study", "resources")], computation=["Finite_Examples"])
paper("G3", "Finite Signed Graphs and Binary Extension Constraints", [("study", "signed_graphs")], computation=["Finite_Examples"])
paper("G4", "Quantum State Families, Symmetry and Relative References", [("study", "quantum_families")], computation=["Finite_Examples"])
paper("G5", "Observation, Memory, Control, and Time in Finite Models", [("study", "operational")],
      computation=["Finite_Examples", "Channel_and_Operational_Examples"])
paper("G6", "Invariant Relational Selection and Approximate Symmetry", [("component", 51)])
paper("G7", "Transport, Holonomy and Monodromy as Bridge Candidates between Classical and Quantum Models",
      [("planned", "Results are recorded in REVIEW_RECORDS/Director_D; no manuscript has been written.")], kind="planned")

SERIES = {
    "A": "Program",
    "B": "Observation and conditional instruments",
    "C": "Fermionic and operator identification",
    "D": "Wilson\u2013Dirac relative entropy",
    "E": "Spectral measures and compact groups",
    "F": "Information, calibration and statistics",
    "G": "Relational structures and bridge candidates",
}

def check_plan(n_components=85):
    used = [i for p in P for (k, i) in p["parts"] if k == "component"]
    assert len(used) == len(set(used)), "component used twice"
    missing = sorted(set(range(n_components)) - set(used) - {10})   # component 10 is split into D5 and F4
    assert not missing, f"components not assigned: {missing}"
    ids = [p["id"] for p in P]
    assert len(ids) == len(set(ids))
    for p in P:
        for d in p["depends"]:
            assert d in ids, (p["id"], d)
    return True

if __name__ == "__main__":
    check_plan(); print(len(P), "papers; plan consistent")
