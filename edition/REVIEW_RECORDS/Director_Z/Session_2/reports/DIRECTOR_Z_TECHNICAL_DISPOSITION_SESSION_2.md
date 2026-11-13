# Director Z | Technical disposition, second session

**Research program:** From Prephysical Hypotheses to Physical Models
**Research direction:** Kirtus Justus
**Reviewing participant:** LLM Director Z, Claude (Anthropic), at the principal's direction; no endorsement by Anthropic is implied
**Date:** 12 November 2026
**Basis:** edition FPHPM-BASELINE-2026-11-12-Z1 (manifest verified, 657 files); six packets of LLM Directors A, B and G (GPT-6, OpenAI): A overlay and A2 continuation, B1 and B2, G initial grounding and G reconciliation
**Root Review state:** Unary, program whole, G1 Grounding OPEN. Nothing below advances it. No ontology is selected.

## 1. Subject

(a) Check the six packets against edition Z1 and against independent recomputation, and decide each point of difference. (b) Continue the two foundational questions left by the first session: what the transition-probability geometry determines, and what a finite carrier can supply. (c) Build and test one constructed trial where the map gave enough support to make it a test.

## 2. Cross-review of Directors A, B and G (Cross-Adversarial, FOCUSED)

All six packets passed their own integrity programs, and their verification programs were rerun with the stored results reproduced. Twenty-three claim groups were then decided one by one; `registers/CROSS_DIRECTOR_ADJUDICATION.csv` gives each with the independent check made here. Summary:

- **Upheld against edition Z1 (three points).** (i) The sentence of G7 Remark 5.2 that no holonomy measurement round contractible loops separates the real three-level theory from the qubit was false: with `d = arccos √p` the curvatures are 1 and 4. The commutant criterion needs the non-contractible loop; the geometries differ locally. (ii) The cap radius was written as 10.48° in the abstract and in OP-10; the proved constant is `arccos(59/60) = 10.4753°`. For rotation orbits it is `arccos(29/30) = 14.8351°`. (iii) The class of Theorem 5.1 was abbreviated in the abstract and in OP-11 as "without third-order interference"; the class needs all three Barnum–Müller–Ududec postulates. One further correction was found here: Gelander's corollary is 1.3, not 1.2.
- **Concurred.** The determinant law as conditional mathematics; non-identification of the signed phase by the metric; the Gram family in `CP^2`; the classical-spin scope example; the minimal-composite witness and the family `K_t` with its four-system closure failure `t(1−t)/4`; the non-selection of dynamics by static geometry; the three-cycle algebra `C² = −3` and its classical counter-completion; whole-model conjugation as a gauge.
- **Resolved.** Director B (B2) exhibits two `CP^2` triangles with equal pair probabilities and equal determinant holonomy and Bargmann phases 0 and 2π/3. The fan construction of G7 Proposition 4.6 returns 0 and 2.0944 for them. The determinant of one loop loses a root of unity; the holonomies of a family of loops do not.
- **Not decided here.** The CNOT closure theorem of Director G and the finite-net bounds of Directors A and B were rerun, not reproved. The D8 item of Director B was outside the subject. Barnum–Hilgert (2020), reported by Director A, was not inspected.

The Directors' packets record that edition Z1 and paper G7 were not available to them; their dispositions on Z1 are dispositions on a transmitted summary. Their three upheld points were nevertheless correct about the text of Z1.

Agreement among A, B, G and Z is not counted as replication: the four worked from one baseline and, for A, B and G, from this participant's summary. The model families differ (GPT-6; Claude), the sources do not.

## 3. Assessments

### 3.1 Z2-A (FOCUSED): what the transition probabilities determine

**Claim.** The transition probabilities of `CP^n` determine every Bargmann phase up to one conjugation common to all, by an explicit construction, and determine nothing finer.

**Case.** G7 Proposition 4.6: subdivide the sides opposite a base vertex; the phases of the thin triangles multiply to the phase of the polygon; each is the root nearest 1 of a holonomy determinant once the cells are small. Corollary 4.7: the only choice is between the two parallel complex structures. This closes the item left open in OP-19 (phase beyond its `(n+1)`-th power).

**Challenge and resolution (SELF_CHECK with exposure).** *It is Wigner's theorem.* The uniqueness statement is; the construction is not, and the paper says so. *Three overlaps do not fix the phase (Director A).* True for the triple alone; the corollary uses the transition probabilities to intermediate states. *The base vertex may be orthogonal to a side.* Excluded by hypothesis; such polygons are nowhere dense and the phase is continuous.

**Disposition.** SUPPORTED_IN_SCOPE (Z-011, Z-012).

### 3.2 Z2-B (FOCUSED): forms of the one postulate that selects complex amplitudes (OP-18)

Within the comparison class the following are equivalent or necessary for each other: holonomy commutant `C`; a symplectic form on pure states; a dynamical correspondence in the sense of Alfsen and Shultz (inspected through Baez's account); observability of energy (Barnum–Müller–Ududec); and, as a necessary count, equality of the dimensions of generators and of observables modulo constants (G7 Proposition 5.4: equality only for the complex theories and the three-dimensional ball). OP-18 asked for a warrant not presupposing Hamiltonian dynamics. None was found. What is gained is that the candidates for such a warrant are one requirement in several forms. **Disposition.** The equivalences: SUPPORTED_IN_SCOPE on quoted dimensions (Z-014). The warrant: NOT_IDENTIFIED_IN_SCOPE.

### 3.3 Z2-C (FOCUSED): finite generating data and the ordering of values

**Claim (favourable reading of the second limit form of OP-19).** A finitely generated dense group with a stabilizer subgroup, specified algebraically, determines the transition-probability geometry of its orbit.

**Checked contrary evidence.** G7 Proposition 7.4: for the group generated by `H` and `T` the field automorphism `ζ ↦ ζ³` gives a second invariant transition probability `σ∘p` on the same orbit, with the same completion, and the identity is not uniformly continuous between the two. Exact values: `HTH` has `(2+√2)/4` against `(2−√2)/4`. For cyclic phases the measure of a set of walks is independent of the faithful character only for orders 1, 2, 3, 4, 6 (G8 Proposition 8.1).

**Disposition.** REFUTED_IN_SCOPE for the favourable reading (Z-015, Z-019). What survives: data over the rationals, the Gaussian or the Eisenstein field have complex conjugation as their only automorphism, and conjugation does not change `p`. New obligation OP-21.

### 3.4 Z2-D (FOCUSED): composition and orientation

Single-system geometry leaves open the composite (G7 Proposition 8.1, after Director B) and the relative orientation of the complex structures of the parts (Proposition 8.2): reflecting one Bloch sphere is an isometry of that system and maps the two-qubit state space to a different set. For `m` systems the relative orientations form a balanced signing of the complete graph; only the common reversal is without effect. Together with Corollary 4.7 and Director B's whole-model conjugation: the orientation of one system is a gauge; relative orientations are fixed by composition. **Disposition.** SUPPORTED_IN_SCOPE (Z-016). What fixes them in a prephysical structure: NOT_IDENTIFIED_IN_SCOPE (OP-20).

### 3.5 Z2-E (constructed trial, Core 10.3): GH-1, holonomy counts on a gain graph

**Why built.** Four independent lines now agree on what a finite carrier cannot be (homogeneous) and on what must be supplied (a transport's representation, an orientation, a composition rule). The program's own primitives include signed graphs (G3) and cycle products (G6). A gain graph is the transport of the principal's stipulation on a finite carrier, with holonomy as its only invariant. The trial asks which set functions on walks can depend on that transport.

**Stipulated.** Second order; end vertices as records; one rule for all graphs; strong positivity; the group and representation; step count.

**Observed (proved in paper G8, executed in 15 predicates).** No additive function depends on the transport. Invariant pair rules are class functions of the holonomy of the pair; strongly positive ones are non-negative combinations of irreducible characters; the extreme ones are squared norms of summed representation matrices, of real, complex or quaternionic type; a character and its conjugate give the same measure; third-order interference is absent; the Dowker–Johnston–Sorkin construction gives a Hilbert space and, under a growth condition, a dense inhomogeneous subset of `CP^{m−1}` or `RP^{m−1}`; the product of gain graphs gives the full tensor product; recorded walks give the counting measure.

**Demolition.** The second order is assumed, and a fourth-order invariant positive rule exists. The record role of end vertices is assumed. The group and representation are inputs: the trial does not select complex amplitudes. Walk length is not unitary; the signed hypercube is unitary with period two; long walks converge to one eigenvector. No reversible dynamics, no continuous symmetry, no clock, no Hamiltonian classical limit, no operational meaning for the transition probability. The growth condition is unproved for any class of graphs.

**Proposed transfer.** None to physics. To the map: two conditional edges (probability rule; composition) and four named postulates replace three imports of FAR-1.

**Disposition.** Conditional statements: SUPPORTED_IN_SCOPE (Z-017). GH-1 as an emergence of quantum or classical mechanics: NOT_IDENTIFIED_IN_SCOPE (Z-018).

### 3.6 Z2-F (FOCUSED): manuscripts

Paper G7 was revised (18 pages, 15 labelled statements) and paper G8 written (9 pages, 8 labelled statements). Every statement is proved in the manuscript, quoted with a source, or marked as a computed instance.

## 4. Map

`PROGRAM/registers/ONTOLOGY_GATE_MAP.json` and `PROGRAM/figures/Gate_Map_2026-11-12.pdf` hold thirteen gates with the evidence bearing on each; the gate list follows Director A. No gate is passed. Two gates (probability rule, composition) now have conditional derivations from a stated primitive; two (transition geometry, phase) are restricted or sharpened by proved statements; dynamics, clock and space, classical Hamiltonian mechanics and empirical correspondence have nothing but negative controls. The bridge register gained three nodes and ten edges.

## 5. Candidate feed (Core 10.2)

| Candidate | Class | Treatment |
|---|---|---|
| Gain graph with pair measure (GH-1) | constructed ontology | built, proved, demolished; paper G8; `CONSTRUCTED_TRIALS/GH-1` |
| Fan of thin triangles | INSTANCE_CANDIDATE for OP-19 | promoted; G7 Proposition 4.6 |
| Field automorphisms of generating data | ORIGINAL_SCOPE_COUNTEREXAMPLE to the favourable reading of limit form (2) | promoted; G7 Proposition 7.4 |
| Rigid phase groups of order 1, 2, 3, 4, 6 | ASSUMPTION_VARIATION | promoted as a restriction, not a selection; G8 Proposition 8.1 |
| Directed three-cycle (Director A) | INSTANCE_CANDIDATE with counter-completion | recorded as an edge; quoted in G8 |
| Interpolated composites `K_t` (Director G) | ORIGINAL_SCOPE_COUNTEREXAMPLE to pairwise selection of the composite | recorded as an edge |
| Discrete Schild's ladder on a graph (transport of edge directions across quadrilaterals) as a source of gains from the graph alone | FRAME_ALTERNATIVE | not examined; RECALL_ONLY; entered as an untested transfer |
| Stationary holonomy of neighbouring walks as a discrete form of the stationary-phase condition | FRAME_ALTERNATIVE for the classical limit | not examined; speculation; entered as an untested transfer |
| Unitary matrices over the Gaussian dyadic ring as a rigid generating set | background | not examined |

## 6. External sources inspected this session (retrieved text, 12 November 2026)

Gelander, L'Enseignement Math. (2) 59 (2013) 195–206 (Theorem 1.1, Corollary 1.3, Remarks 1.5); Lavi, arXiv 2001.03885 (full text); Gorodski–Kollross, arXiv 1505.02852 (curvature normalization; journal reference); notes and papers on `HP^n` and `OP^2` (isotropy `Sp(n)Sp(1)`, `Spin(9)`); Li–Wagner–Zhang, Phys. Rev. A 113, 012428 (2026) (abstract, summary of results); Dowker–Johnston–Sorkin, arXiv 1002.0589; Dowker–Wilkes (2022) (abstract); Selinger, arXiv 1212.6253 (Section 3.2); Giles–Selinger, arXiv 1212.0506 (abstract); Baez, arXiv 2006.14741 (abstract, introduction); Niestegge, arXiv 0912.0203 (abstract); Barnum–Müller–Ududec, New J. Phys. 16, 123029 (abstract); Eftaxias–Weilenmann–Colbeck, Phys. Rev. A 108, 062212 (introduction); Boykin et al., Inf. Process. Lett. 75 (2000) 101–107 (first pages); Reff, arXiv 1110.4554, and two further papers on gain graphs (abstracts). None evaluates this program.

## 7. Limits

- One participant in this stack. No sub-agent facility (tested; see the calibration record). Every challenge inside the stack is a SELF_CHECK with exposure. The packets of Directors A, B and G are separate submissions from another model family working from shared sources.
- The ACR packet was not among this session's inputs and was not read in this session.
- Proofs in G7 and G8 are unrefereed. Numerical values are double precision except where exact arithmetic is stated.
- From recall, not inspected: the dimensions of the Lie and Jordan algebras in G7 Proposition 5.4; that continuous automorphisms of `SO(3)` are inner; the classification of finite subgroups of `O(3)` (inspected by Directors B and G in their ledgers, not here); bibliographic details of Berger, Besse, Coxeter, Kostant, Souriau, Perelomov, Cushman–Duistermaat, Duistermaat, Vũ Ngọc, O'Neill, Kibble, Ashtekar–Schilling, Alfsen–Shultz, Zaslavsky, Huang, Sinha et al., Boës–Navascués, Serre, and the authorship of arXiv 2111.12428.

## 8. Retained residuals, failures and corrections

- First run of the icosahedral check failed its predicate: the three axes chosen did not bound one fundamental triangle (sides 37.4°, 31.7°, 54.7°). With the correct face centre the sides are 37.377°, 31.717°, 20.905° and the circumradius is 18.7125°.
- First run of the gauge check for the quaternion group: a non-class weight left the measure of a single set unchanged (change 0.0). Every conjugacy class of that group is `{x, x⁻¹}`, so the symmetrized weight is a class function. The predicate was restated for two different sets; the observation is kept in the result file.
- First draw of the interference check: one set had summed amplitude 0 and `I₄` of the fourth-order rule was 0. Kept in the result file.
- Paper G8, Tables 2 and 3, were first typed from a run that preceded a change of the random stream; they were reset to the stored results (272 walks; differences 0.214, 0.140, 0.068, 0.236).
- Phase recovery: for `n = 4`, five vertices, the root of the undivided polygon is 0.2023 and the phase is 2.7156.
- Conjugate embeddings: largest `p − p'` among 21310 elements 0.928; the element with `p = 0.9953` has `p' = 0.0672`.
- All values retained by Directors A, B and G in their packets are kept with the packets in `REVIEW_RECORDS/Directors_A_B_G_2026-11-12/`.

## 9. Obligations

Amended: OP-10, OP-11, OP-17, OP-18, OP-19. New: OP-20 (orientation), OP-21 (ordering of values), OP-22 (composition and multipartite closure), OP-23 (dynamics, clock and classical limit for any candidate, with the negative results of GH-1), OP-24 (independent review; no sub-agent facility in any Director session), OP-25 (independent check of paper G8 and its growth condition). Unchanged: OP-01 to OP-09, OP-12 to OP-16.

**Closing disposition.** The transition-probability geometry fixes its phases up to one bit per system, and composition fixes the relative bits. Algebraic generating data fix that geometry only up to field automorphisms. On a finite graph with a transport, invariance and positivity force the squared-norm rule in a unitary representation once a second-order rule with end-vertex records is assumed, and the product of graphs gives the tensor product. Nothing obtained selects complex amplitudes, supplies a reversible dynamics or a clock, or yields classical Hamiltonian mechanics. Root Review: G1, OPEN.
