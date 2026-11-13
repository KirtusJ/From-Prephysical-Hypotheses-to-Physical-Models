# Director D | Transport, Holonomy and Monodromy as Bridge Candidates: Scoped Assessment and Map Segment

**Research program:** From Prephysical Hypotheses to Physical Models  
**Research direction:** Kirtus Justus  
**Reviewing participant:** LLM Director D — Claude (Anthropic), at the principal's direction; no endorsement by Anthropic is implied  
**Date:** 11 November 2026  
**Basis:** frozen 10 November 2026 review packet (SHA-256 `fde41b37…6669cf`), Toy Universe session packet, Director B and Director C 11 November handoffs, ACR 1.0 Implementation packet as supplied in the PCP 1.0 Enterprise Edition (release fingerprint `42341ddf…41c79`)  
**Root Review state:** Unary, TOTAL extent against the program whole, G1 Grounding still open. Nothing below advances it. No ontology is selected.

## 1. Commission as understood

The standing direction is to pursue "total ontology" — emergent and explained quantum and classical mechanics with a full map — under the working disposition that it will not be reached, while doing what is required to reach it. The principal supplied one stipulation to be treated with ordinary skepticism: that monodromy, parallel transport, holonomy and Schild's ladder may be relevant in finding candidates for a prephysical–physical bridge, if only as abstractions or as a check.

This session treats that stipulation as a Claim constructed by the principal, not as a premise. It commissions three bounded assessments on it (Section 3), executes fresh calculations (Section 4), grounds the decisive points externally (Section 5), and files the result as a map segment with explicit edge types (Section 6). The inherited open items are restated, not resolved (Section 7).

## 2. State of the program on intake

The November 10 baseline passes its own packet verifier in strict file-set mode (445 payload files, 85 component PDFs, 547 source body pages compared). The Director B and Director C handoffs pass their native validators; the Toy Universe checks reproduce byte-identically once a hard-coded absolute output path in `verify_toy_models.py` is redirected (a portability defect in the verifier, not in the mathematics). Upload digests match the receipts recorded inside the later packets, so the provenance chain B → C → Toy → this session is internally consistent. None of this authenticates authorship or establishes any physical claim.

Two reconciliations were needed and are recorded here rather than raised with the principal:

1. Directors B and C worked under `PCP-2026-11-10-R13` ("Council" vocabulary, Sections 1–14). The packet supplied for this session is ACR 1.0 of 11 November ("Review" vocabulary, Section 15 operating floor, explicit evidence status). The two Core texts differ in 344 lines; the Mathematics, Science, Statistics and Quality-Assurance modules also differ. Compatibility was not assessed clause by clause. This session applies ACR 1.0; the earlier records keep their own rule basis and are not relabelled as conforming to it. "Council", "Parent Unary PCP" and "Initial External Grounding" are read as the team's own names for a root Unary Review whose G1 has not passed; they carry no ACR 1.0 meaning beyond that mapping.
2. The research record contains two withdrawn or stipulated ontologies, TO-0 and FAR-1. Both remain negative controls. FAR-1's statement that the Clay Mathematics Institute continues to list Navier–Stokes as open while evaluating a September 2026 claim was checked against the Institute's own 11 September 2026 announcement and contemporaneous reporting; it is accurate as of this date and has no bearing on the program.

The substantive scientific state is unchanged: the collection establishes conditional mathematics and obstructions; no prephysical structure has been shown to select quantum or classical mechanics; the Wilson–Dirac cross-boundary dependency, the eight-output copying optimum, the physical observation bridge and physical time remain open.

## 3. The three bounded assessments

All three were performed by one participant in separate executions (ACR 1.0 §3.1, §4.2). Each challenge is therefore a SELF_CHECK with exposure to the developed case; its weight comes from the sources inspected and the checks executed, not from being a second pass.

### 3.1 D-TRN-A (FOCUSED): can transport structure alone select quantum mechanics?

**Claim (principal-constructed, strongest reading).** A prephysical structure carrying parallel transport, holonomy or monodromy selects, or approximates, the quantum formalism.

**Case developed.** Holonomy is not foreign to quantum mechanics: the geometric phase is the holonomy of the natural connection on the bundle of unit vectors over projective Hilbert space (Berry; Simon's holonomy interpretation), and the Bargmann invariant `arg Tr(P_1 P_2 P_3)` of three pure states is the discrete holonomy of a geodesic triangle (Pancharatnam; Samuel–Bhandari geodesic rule). Geometric quantization makes the classical–quantum link exact: the prequantum line bundle's connection has the symplectic form as curvature, and trivial holonomy on Lagrangian tori is the Bohr–Sommerfeld condition. Hamiltonian monodromy (Duistermaat) obstructs global action variables classically and reappears as a lattice defect in the quantum joint spectrum, with a theorem that the quantum monodromy equals the classical monodromy (Vũ Ngọc). So transport concepts organize both mechanics and the passage between them.

**Adverse check (nonselection witness, executed).** The same base loop — the octant geodesic triangle on the sphere, solid angle Ω = π/2 — carries three different holonomies depending on the representation chosen, and nothing in the loop structure chooses among them:

| Representation of transport | Holonomy of the octant loop | Checked |
|---|---|---|
| Finite group-valued frames on a graph (program's own S₃ loop products) | a conjugacy class; no continuum, no phase | inherited, not re-executed |
| Levi-Civita connection on S² (classical frame, Foucault/Hannay type), computed by Schild's ladder | rotation by Ω = 1.5707969 (Ω = 1.5707963) | Check F |
| Hopf/prequantum U(1) connection, spin-j coherent states | phase jΩ for j = 1/2, 1, 3/2, 2 | Checks A–C |

The quantum content is not the existence of a holonomy but the choice of a complex line bundle with half-integral charge over a projective state space. That choice is exactly what the program's existing note already identified: formal gauge covariance, cocycles and holonomy do not by themselves identify physical gauge fields. The witness upgrades that statement from a caution to a checked ambiguity.

**Disposition.** NOT_IDENTIFIED_IN_SCOPE for the strong Claim. Transport structure is necessary vocabulary for both mechanics and for the bridge between them, but it does not select the quantum representation. A narrower substitute Claim is reported beside it in D-TRN-B; it is a different Claim.

### 3.2 D-TRN-B (FOCUSED): what exact bridge segments does transport supply inside and between the two mechanics?

**Claim (reviewer-constructed substitute).** Within classical mechanics, within quantum mechanics, and across the classical–quantum passage, holonomy and monodromy give exact, checkable correspondences that belong on the map.

**Executed support (Section 4).** (i) Exact general formula `Tr(P_a P_b P_c) = (1 + a·b + b·c + c·a + i a·(b×c))/4` for qubit projectors, so the oriented triple invariant is the signed volume `a·(b×c)`; (ii) spin-j triple phase = jΩ, modulus `(√2/4)^{2j}`; (iii) continuous Berry line integral along the geodesic triangle = −Ω/2 and the discrete chain of any refinement N = 1, 3, 30, 3000 gives +Ω/2 to 10⁻⁹ (geodesic rule; the two sign conventions are opposite and both are stated); (iv) Schild's ladder on S² reproduces the Levi-Civita holonomy Ω to 6×10⁻⁷; (v) the quantum spherical pendulum's joint spectrum shows a lattice-cell shift of +0.98 (ħ = 0.05) and +0.99 (ħ = 0.04) in units of the vertical cell vector after transport around the focus-focus value (ℓ, E) = (0, 1), and 0.00 for control loops that do not enclose it.

**External precedent.** Berry 1984; Simon 1983; Samuel–Bhandari 1988; Mukunda–Simon 1993; Duistermaat 1980; Cushman–Duistermaat 1988; Vũ Ngọc 1999; Cushman–Vũ Ngọc 2002 (the oriented monodromy index of a focus-focus value is positive; the sign convention of the present transport rule was not mapped onto theirs, so only the magnitude is compared). These establish the mathematics; they do not evaluate this program.

**Disposition.** SUPPORTED_IN_SCOPE as mathematics within the specified finite models. The 0.98/0.99 lattice shifts are nearest-neighbour continuation values, not exact integers; the integer is the limiting statement of the cited theorem, and the residual is retained as a datum, not rounded away.

### 3.3 D-TRN-C (FOCUSED): what discriminator does the transport axis give, and what obligation does it impose on any prephysical candidate?

**Claim (reviewer-constructed).** The oriented triple phase is a discriminator along a classical → real-quantum → complex-quantum → beyond-quantum axis, and reconstruction theorems locate the "transport" content of quantum theory in a continuity postulate that finite prephysical structures cannot supply without a limit construction.

**Executed support.** Classical point states give triple products in {0, 1}; real-amplitude states give triple phases in {0, π} only (200 random triples, exact); complex qubit states give a continuous phase. Therefore a continuously varying oriented triple phase witnesses complex amplitudes. Pairwise overlaps alone cannot (the program's +X, +Y, +Z example: all overlaps 1/2, triple phase π/4); this is consistent with the 2024 result that pairwise overlaps witness imaginarity for sets of four states but not three.

**External grounding.** Bargmann invariants are measurable by generalized SWAP tests (Oszmaniec–Brod–Galvão 2021/2024); real quantum theory makes different predictions from complex quantum theory in network scenarios and has been experimentally disfavored (Renou et al. 2021; Li et al. 2022). Above complex quantum theory, Sorkin's hierarchy: third-order interference `I₃` vanishes in quantum theory and in every Jordan-algebraic theory, and `I₃ = 0` has been tested to 10⁻⁴ (Sinha et al.; later three-path experiments); theories with PR-box or pentagon-state correlations require `I₃ ≠ 0` (Niestegge). Reconstruction: with Tomographic Locality, the Subspace Axiom (or Existence of an Information Unit) and Continuous Reversibility — every pair of pure states joined by a continuous reversible transformation — the state space is forced to be quantum (Hardy 2001; Masanes–Müller 2011; Masanes–Müller–Augusiak–Pérez-García 2013).

**Obligation derived.** Continuous Reversibility requires a connected group acting transitively on pure states. A finite relational structure (the program's finite positive-arity signatures with homomorphic equivalence) has a finite automorphism group and therefore cannot satisfy it directly. Any finite or discrete prephysical candidate must deliver a limit construction whose pure-state space is a compact homogeneous space under a connected group before any reconstruction theorem applies, and must separately deliver tomographic locality. This is an obstruction statement about a model class, not a refutation of any particular candidate: it says what a candidate has to produce.

**Disposition.** SUPPORTED_IN_SCOPE for the mathematical discriminator ladder (executed controls plus inspected sources). CONDITIONAL for any physical application: it requires calibrated preparations, known overlaps, and independence assumptions the program already lists as unsupplied. The obligation on finite candidates is SUPPORTED_IN_SCOPE as a logical consequence of the cited postulates; whether those postulates are the right ones is not settled by this assessment.

### 3.4 Check-against item: the Ehlers–Pirani–Schild construction

The principal's mention of Schild's ladder points at the one existing rigorous "pre-metric to metric" construction. Ehlers, Pirani and Schild (1972) take events, light rays and freely falling particles as primitives; light propagation yields a conformal structure, free fall a projective structure, their compatibility a Weyl structure with a constructive parallel displacement; a Lorentzian metric follows only with a further axiom equivalent to the absence of a second clock effect. The residual axiom is an empirical input, and Perlick's standard clock exists only in Weyl spaces. This is the right template for the program's geometry line: primitives → conformal/projective → Weyl → metric, with each step's added axiom named. It is also a negative lesson: even with physical primitives, the construction stops one axiom short of the metric, and the missing axiom is a clock statement. Recorded as external precedent; not a result of this program.

## 4. Executed calculations

`verification/verify_transport_bridges.py` (Python 3.12, NumPy 2.5.4, SymPy 1.14.0, standard library) writes `Transport_Bridge_Results.json`; it refuses to overwrite an existing result file. Seventeen predicates pass. Exact symbolic checks: A. Numerical checks with tolerances stated in the file: B–F. Residuals are retained in the JSON. The spherical-pendulum model is `H = (ħ²/2)L² + cos θ` in the `Y_l^m` basis, `l ≤ 160`, levels below `E = 3` only; the transport rule is nearest-neighbour continuation of the cell vector to the next column; loops are rectangles in `(ℏm, E)` chosen inside the regular region (the control loop at `ℓ = ±0.4` stays above the relative-equilibrium energy ≈ −0.58). Successful predicates are not theorem counts.

## 5. Grounding settings (ACR 1.0 §15.8)

| Setting | Value for this session |
|---|---|
| Delivery | ABSORBED_TEXT for the kernel and the Core sections read; RETRIEVAL from the Markdown sources in the supplied Implementation packet. Not TOOL_ASSISTED, not HOST_ENFORCED; no halt, fence or permission control is enforced by anything outside this participant's context |
| Extent | ACR 1.0 Implementation packet, release fingerprint `42341ddf38a21a659d974af7d27c739605dd192b2d16c76ef1ae2dcdbdd41c79`; Core descriptor `bf1952a3e14f3fdb71e9c87df7e36165325a050d76aa7486aa8b6de8fa460386` (as printed in the packet; the Core files' digest was not independently recomputed) |
| Grounding | EXTERNAL_INSPECTED for the points in Section 5 of the disposition (web sources retrieved and read on 11 November 2026); SUPPLIED_ONLY for the program's own claims; RECALL_ONLY for standard textbook mathematics that was then executed |
| Execution | EXECUTED for every verifier run and every predicate in Section 4; REASONED for the obligation argument in 3.3 |
| Observability | BLACK_BOX; this participant's account of its own processing is not evidence |
| Participants | One. No separate assessor, no sub-agent. Every "challenge" above is a SELF_CHECK |

ACR has not been peer reviewed, independently reviewed or evaluated in use; nothing here describes it as validated.

## 6. Map segment delivered

`registers/BRIDGE_CANDIDATE_REGISTER.json` adds a typed segment to the program map. Nodes are model classes or structures; edges carry one of five types: `exact_correspondence` (proved, with locator), `postulate` (an axiom that would have to be supplied), `obstruction` (a checked nonselection or impossibility within a class), `discriminator` (an observable that separates classes, with its calibration obligations), and `untested_transfer` (proposed, no warrant). The segment includes the inherited negative controls TO-0 and FAR-1 and the inherited open items so that nothing is lost. It is a map of obligations and checked relations, not a derivation.

## 7. Remaining obligations (unchanged unless stated)

- Wilson–Dirac cross-boundary trace path `𝒮(µ)` dependency in Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*: open; not examined this session.
- Exact eight-output copying optimum: open; not examined.
- Physical observation and calibration bridge; physical time: open. Section 3.3 adds a precise obligation (continuous transitive reversibility and tomographic locality must be delivered by any candidate), which narrows the search without discharging it.
- Comparative effectiveness of ACR/PCP against ordinary review: open; no evidence was produced here.
- New: the lattice-shift residuals (0.984, 0.985) should be driven to the limit with a Bohr–Sommerfeld counting check (Vũ Ngọc's exact counting function) before the monodromy segment is cited as more than a numerical demonstration.
- New: the Director B/C basis (`PCP-2026-11-10-R13`) and ACR 1.0 have not been mapped clause by clause; a Reconciliation Review is justified before any finding is reported as conforming to both.

**Director D closing disposition.** The principal's stipulation survives as a check-against template and as an exact classical–quantum map segment, and fails as a selection mechanism. Transport structure is necessary vocabulary; it is not a bridge from prephysical structure to physics. Root Review remains at G1, OPEN.
