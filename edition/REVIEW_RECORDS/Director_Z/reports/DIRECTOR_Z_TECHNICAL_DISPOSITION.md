# Director Z | Technical disposition

**Research program:** From Prephysical Hypotheses to Physical Models
**Research direction:** Kirtus Justus
**Reviewing participant:** LLM Director Z, Claude (Anthropic), at the principal's direction; no endorsement by Anthropic is implied
**Date:** 12 November 2026
**Basis:** baseline FPHPM-BASELINE-2026-11-12 (manifest verified, 645 files), Toy Universe session packet, ACR 1.0 Implementation packet as supplied in the PCP 1.0 Enterprise Edition (release fingerprint `42341ddf…41c79`)
**Root Review state:** Unary, program whole, G1 Grounding OPEN. Nothing below advances it. No ontology is selected.

## 1. Assignment as understood

Pursue the program's target, an explained emergence of quantum and classical mechanics with a full map, on the working expectation that it will not be reached, and treat the suggestion that monodromy, parallel transport, holonomy and Schild's ladder may bear on a prephysical–physical bridge as a claim to be tested. Director D had tested the strongest reading (transport selects the quantum formalism) and found it not identified. This session asked two questions that D's record left open and that sit at the foundation of the two open obligations OP-10 and OP-11:

- **A.** D's nonselection witness compared *chosen* transports on one loop. Once a transition-probability geometry is given, one transport is not chosen: the Levi-Civita transport of the metric `d = arccos √p`. What does that canonical holonomy determine?
- **B.** D's obligation says a finite candidate must supply a limit with a compact homogeneous pure-state space. What forms can such a limit take?

## 2. Assessments

### 2.1 Z-A (FOCUSED): canonical holonomy as a discriminator

**Claim.** The Levi-Civita holonomy of the transition-probability geometry, including its monodromy, separates complex quantum theory from the other single-system theories without third-order interference.

**Case.** (i) *Determinant law* (child Z-A1; paper G7, Lemma 4.2 and Proposition 4.3). For a geodesic polygon in `CP^n` the holonomy is `T = e^{-iθ} U` restricted to the horizontal space, where `U` is a product of plane rotations with determinant 1 that maps the base vector to `e^{iθ}` times itself and `e^{iθ}` is the conjugate phase of the Bargmann invariant `B`. Hence `T` is unitary, `det_C T = (B/|B|)^{n+1}`, and `T` multiplies by `B/|B|` every tangent vector orthogonal to the span of the vertices. The geometric phase is therefore contained in the Levi-Civita holonomy, which the transition probabilities fix; Schild's ladder computes it from geodesic midpoints. (ii) *Classification* (G7, Theorem 5.1). In the Barnum–Müller–Ududec class the pure-state manifolds are `RP^m`, `CP^n`, `HP^n`, `OP^2` and spheres. The commutant of the holonomy group is `C` only for `CP^n`; a symplectic form exists only on `CP^n`.

**Challenge map and resolution (SELF_CHECK with exposure).**

| Objection | Resolution |
|---|---|
| The discriminator presupposes the transition-probability geometry, so it selects nothing from a prephysical structure | Accepted. The claim is a discriminator claim; the selection claim D-TRN-001 keeps NOT_IDENTIFIED_IN_SCOPE. G7 states this in its first section and in its last |
| `RP^2` (real three-level theory) is locally isometric to the qubit sphere up to scale, so local holonomy cannot separate them (child Z-A2) | Holds for the restricted holonomy: computed commutant dimension 2 for contractible loops on `RP^2`. The non-contractible loop gives a reflection (derived; Schild's ladder determinant −0.999995), and the commutant of the full group is `R`. The separation is by monodromy. Recorded as G7 Remark 5.2 |
| The classification inputs (holonomy groups of `HP^n`, `OP^2`; cohomology) are textbook facts from recall | Accepted as a limit. The executed cases are `CP^2`, `CP^3`, `S^2`, `S^3`, `S^4 = HP^1`, `S^8`, `RP^2`. `HP^n` for `n ≥ 2`, `OP^2` and `RP^m` for `m ≥ 3` are quoted. Disposition lowered to CONDITIONAL |
| "Symplectic pure-state manifold" could be read as a derivation of complex amplitudes | It is a postulate. It holds for classical mechanics and for complex quantum theory and for no other member of the class, but no reason for imposing it that avoids presupposing Hamiltonian dynamics was found (Z-005, UNRESOLVED; OP-18) |
| Invariant symplectic forms: the full isometry group of `CP^n` contains an antiholomorphic involution that reverses the form | Correct; the statement in G7 is for the identity component of the isometry group |

**Disposition.** Z-A1: SUPPORTED_IN_SCOPE as mathematics (proof plus an executed check by a different route). Z-A: CONDITIONAL on the quoted classification inputs. The original strong claim of D-TRN-001 is not this claim and keeps its disposition.

### 2.2 Z-B (FOCUSED): finite carriers with exact symmetry

**Claim (favourable reading of the obligation in OP-10).** A sequence of finite carriers, each with a transitive symmetry group, can approximate the pure-state space of a quantum system.

**Checked contrary evidence.** (i) For subsets of the Bloch sphere: a finite subset homogeneous in the induced metric is an orbit of a finite subgroup of `O(3)`; axial groups leave a point at distance at least 45°, and polyhedral groups have order at most 120, which by an area count leaves a point at distance at least `arccos(59/60) = 10.48°` (G7, Proposition 7.1). (ii) In general: by Gelander's theorem a Gromov–Hausdorff limit of finite homogeneous metric spaces has a transitive compact isometry group with abelian identity component, and the only manifolds arising are tori; the underlying group statement is Turing's 1938 theorem (G7, Theorem 7.2 and Corollary 7.3).

**Disposition.** REFUTED_IN_SCOPE for subsets of the Bloch sphere (Z-006). CONDITIONAL in general, on the external theorems as stated in the extracts inspected (Z-007). The obligation OP-10 is not discharged; it is restricted: the finite stages cannot be homogeneous. The abelian case is not obstructed, so cyclic-group-valued holonomies approximating phases remain possible, with the non-canonical limit already recorded by Director D.

**Constructed trial Z-B1 (Core 10.3).** Question: does the possibility "finite generating data, unbounded words" evade the bound? Stipulated: two rotations of the Bloch sphere (the half-turn about `(1,0,1)/√2` and the rotation by `π/4` about `(0,0,1)`); these are imported quantum-gate rotations. Procedure: all words up to length 28, deduplicated; orbit of `(0,0,1)`; exact covering radius from the convex hull. Observed: covering radius 90.0°, 47.3°, 24.1°, 16.3°, 9.1°, 7.5°, 4.4° at lengths 4, 8, …, 28. Proposed transfer: none. The trial shows the form of the possibility; because the generators are imported it explains nothing (Z-008).

### 2.3 Z-C (SCREENING): a common node for the two mechanics

Landsman's axioms describe the pure states of either mechanics as a Poisson space with a transition probability. Classical mechanics: `p = δ`, Poisson structure unrestricted. Quantum mechanics: two-point subspaces are qubit spheres, sectors equal symplectic leaves, and the Poisson structure is fixed up to a constant identified with Planck's constant. This is the existing rigorous statement of what the two mechanics share and where they differ, and it agrees with the last statement of G7 Theorem 5.1. Recorded as external precedent (Z-009) and entered in the bridge register as a node. It does not derive either mechanics.

### 2.4 Z-D (FOCUSED): manuscript G7

The planned paper G7 was written. It contains nine labelled statements; each is proved in the manuscript, quoted with a source (Theorem 7.2), or supported by a table marked as a computed instance. Director D's executed results enter through the stored programs. OP-15 remains open for paper F7.

## 3. What this does and does not change on the map

Added to `BRIDGE_CANDIDATE_REGISTER.json`: two nodes (the Barnum–Müller–Ududec class; Poisson spaces with a transition probability) and eight edges (determinant law; holonomy/monodromy discriminator; symplectic postulate; obstruction for homogeneous finite carriers; three unassessed limit forms as an untested transfer; the two Landsman instances; the coherent-state restriction).

Not changed: no prephysical structure is shown to produce a transition-probability geometry, a composition rule, a probability rule or a clock. OP-09, OP-10 and OP-11 remain open. Three items were added (OP-17 to OP-19) and OP-15 was narrowed.

## 4. Candidate feed (Core 10.2)

| Candidate | Class | Treatment |
|---|---|---|
| Symplectic pure-state manifold as a requirement | SUFFICIENCY_CANDIDATE within the comparison class | promoted to the register as a postulate edge; warrant UNRESOLVED |
| Finite homogeneous approximants of a quantum pure-state space | ORIGINAL_SCOPE_COUNTEREXAMPLE to the favourable reading of OP-10 | promoted as an obstruction edge |
| Finite generating data with unbounded words | INSTANCE_CANDIDATE | run as trial Z-B1; promoted as an untested transfer |
| Cyclic-group-valued cycle products approximating phases | ASSUMPTION_VARIATION | recorded; not obstructed; limit not canonical (D) |
| Quantum theory over finite fields as a finite precursor | FRAME_ALTERNATIVE | background only; RECALL_ONLY; not examined |
| Transition-probability spaces that are not Hilbertian in dimension two (Mielnik) | ORIGINAL_SCOPE_COUNTEREXAMPLE to "a transition probability alone forces Hilbert space" | background only; RECALL_ONLY; not inspected |
| A finite toy universe with primitives (set, symmetric weight `p`, oriented triple phase) and a rank condition | constructed ontology | not built: positivity and the rank bound of the Gram matrix are the Hilbert-space structure, so the toy would import what it was meant to explain. Paper G6 already covers the reconstruction from supplied data |

## 5. External sources inspected this session (retrieved extracts, 12 November 2026)

| Point | Source | Portion inspected |
|---|---|---|
| Turing's theorem on finite approximation of connected compact Lie groups | E. Breuillard, arXiv 1512.01369, Theorem 4.5; T. Gelander, arXiv 1402.0962, Theorem 3.1 | statements as retrieved |
| Limits of finite homogeneous metric spaces | T. Gelander, arXiv 1205.6553, Theorem 1.1, Corollary 1.2, Remark 1.5; arXiv 1402.0962, Theorem 3.2 and the sentence that the only manifolds approximable are tori | statements as retrieved |
| Poisson spaces with a transition probability | N. P. Landsman, arXiv quant-ph/9603005 (abstract, introduction); quant-ph/9604008 (axioms QM1–QM3, classical case) | extracts |
| Single-system postulates; the comparison class; energy observability | H. Barnum, M. P. Müller, C. Ududec, arXiv 1403.4147 / New J. Phys. 16, 123029 | abstract and postulate list |

None of these sources evaluates this program.

## 6. Limits

- One participant. No separate assessor. Every challenge is a SELF_CHECK with exposure to the developed case.
- The proofs in G7 are unrefereed.
- From recall, not inspected this session: the holonomy groups and cohomology of the rank-one symmetric spaces; the classification of finite subgroups of `O(3)`; the submersion property used in Lemma 4.2; the bibliographic details of the references of G7, other than those that appear in an extract listed in section 5 (Barnum–Müller–Ududec; Landsman 1997; the arXiv identifiers of Breuillard, Gelander and Landsman). These are to be verified before submission (OP-17).
- Numerical values are double-precision evaluations, not enclosures.
- The method (ACR) is untested; this record does not show that its use improved the work.

## 7. Retained residuals, failures and corrections

- First run of the determinant check failed its predicate: the predicted phase had the wrong sign. The closing horizontal lift has phase `−arg B`; the law is `det_C T = (B/|B|)^{n+1}`. Corrected before any statement was written.
- Schild's ladder with a one-sided rung showed an error proportional to the rung length (determinant residual 3.3×10⁻⁴ at rung length 10⁻³, 6.5×10⁻⁴ at 2×10⁻³). Differencing the transports of `w` and `−w` removed the first-order term (residuals of order 10⁻⁶ at rung length 2×10⁻³). The one-sided values are kept here as data.
- Covering radii: chiral icosahedral group 18.718°, full icosahedral group 18.713°; octahedral 27.69° and 27.57°; tetrahedral 37.38°, pyritohedral 30.36°. A coarse-grid stage gave 18.32° and 18.51° for the icosahedral cases before exact evaluation. These are local numerical optima.
- `RP^2`, contractible loops only: commutant dimension 2, the same as the qubit. Retained as the datum that makes monodromy necessary.
- Draft corrections to G7 before issue: (1) the invariance statement for symplectic forms was restricted to the identity component of the isometry group; (2) a sentence attributing a continuous-field account of the classical limit to a source not inspected was removed; (3) the proof that the commutant contains `C` was rebased on Lemma 4.2 instead of a density argument; (4) the description of the determinant law as new was removed, since it is the statement that the anticanonical bundle is the `(n+1)`-th power of the hyperplane bundle; (5) an item listed as open (recovering `B/|B|` itself) was found to be answerable for polygons that do not span the space and was moved into Proposition 4.3; (6) the wide table was reset.
- Director D's retained values (lattice shifts 0.984 and 0.985; Schild residual 6.2×10⁻⁷ on `S^2`) are unchanged in the register.

## 8. Remaining obligations

Unchanged: OP-01 to OP-09, OP-12 to OP-14, OP-16. Restricted, still open: OP-10 (finite stages cannot be homogeneous), OP-11 (a discriminator and a postulate are identified inside the class; no selection). Narrowed: OP-15 (F7 only). New: OP-17 (independent check of G7 and of its references), OP-18 (warrant for the symplectic condition), OP-19 (a construction, including composition of systems, for any of the three limit forms).

**Closing disposition.** Holonomy and monodromy, taken on the transition-probability geometry, are a complete discriminator inside the class without third-order interference, and Schild's ladder is a way of computing them from transition probabilities. They remain a discriminator and not a bridge from a prephysical structure. Exact transitive symmetry at finite stages is excluded for quantum pure-state spaces. Root Review: G1, OPEN.
