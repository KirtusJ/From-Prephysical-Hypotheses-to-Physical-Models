# Director Z | Technical disposition, third session

**Research program:** From Prephysical Hypotheses to Physical Models
**Research direction:** Kirtus Justus
**Reviewing participant:** LLM Director Z, Claude (Anthropic), at the principal's direction; no endorsement by Anthropic is implied
**Date:** 12 November 2026
**Basis:** edition FPHPM-BASELINE-2026-11-12-Z2 (manifest verified, 791 files); six packets of LLM Directors A, B and G (GPT-6, OpenAI): A3, B3, G3 and A4, B4, G4; the PCP 1.0 Enterprise Edition with its ACR 1.0 Implementation packet
**Root Review state:** Unary, program whole, G1 Grounding OPEN. Nothing below advances it. No ontology is selected.

## 1. Subject

(a) Check the six packets against edition Z2 and against independent recomputation, and decide each point of difference. (b) Examine the two proposals left untested in the second session: a transport supplied by a graph alone (discrete Schild's ladder), and a classical limit from stationarity of holonomy between neighbouring walks. (c) Address the gates that had only negative controls (dynamics, clock, classical Hamiltonian mechanics) by one constructed trial, GH-2, and demolish it in the same review. (d) Discharge the growth condition left open in paper G8.

## 2. Cross-review of Directors A, B and G (Cross-Adversarial, FOCUSED)

All six packets passed their own integrity programs; their verification programs were rerun in copies and passed, with stored floating-point residuals reproduced to rounding. Twenty-four claim groups were decided; `registers/CROSS_DIRECTOR_ADJUDICATION_SESSION_3.csv` gives each with the independent check made here (41 predicates in two programs that import nothing from the packets).

- **Upheld against edition Z2 (one point, found by all three Directors).** The abstract and Section 3 of paper G8 said that an additive function of walks cannot depend on the transport. That holds for one weight function of the gain applied to all walks, which is what Lemma 3.1 proved. An additive rule that weights the walks returning to the starting vertex by a class function of their gain is switching invariant and depends on the holonomy; for Z_3 and 1 + Re chi the weights are 2 and 1/2. Lemma 3.1 is restated in complete form (constant on open walks, class function on closed walks) and the sentence "the lowest order at which gains can enter is the second" is restricted to open walks.
- **Not upheld (one point, Directors A and B).** The proposed erratum to the proof of the determinant law (G7 Proposition 4.3). The source and the typeset page define theta by exp(i theta) = conj(B)/|B|; with that definition the lift phase exp(i theta) and T = exp(-i theta) U are correct, and the Directors' own control values (lift phases (3-i)/sqrt 10 and (1-i)/sqrt 2, determinants (4+3i)/5 and i) agree with the printed proof. The overline on B is lost when text is extracted from the PDF, which reproduces the reading the Directors report. The sentence now also states theta = -arg B.
- **Concurred, with additions made here.** (i) The cubic Veronese model of Director G is correct as stated (dimension 10, kernel 7, values 1/2 and 5/8). Two readings are separated: with the projective tests only, the operational quotient is the qubit; with every affine effect admitted, 1/2 + (x^3 - 3xy^2)/2 is an effect with values 1 and 0 on pure states at Bloch angle 60 degrees, so the model does not carry the qubit transition-probability geometry as its own structure. It refutes sufficiency of a designated pure-state table, not of an intrinsically defined transition probability. (ii) The polar complex structure of odd directed cycles (Directors A, B, G) is the permutation case of a statement about any real orthogonal map; the vertex projections do not commute with it (three-cycle: commutator norm 2 sqrt 2/3).
- **Concurred.** One-sided and two-sided filter exclusions of K_t (A3, B3) and the unnormalized optimum (G4); no four-party weight repairs K_t (A3; the product bound 3/4 is exact); the matching hierarchy as a countercontrol (A3); one pure entangled seed with local filters gives all two-qubit states (A3, B3); the measures of G8 at successive lengths are not related by continuation (A4, B4); a Hermitian step that is a multiple of a unitary is an involution (B4); the three growth witnesses and their bounds (A4, B4, G4); the synchronized product reaches 8 of 16 endpoint pairs over all lengths (G4); exp(-isH) as a formal completion with imported imaginary unit and parameter (G4).
- **Not decided here.** The approximation bound sin d <= 2 sqrt 5/(M - 2 sqrt 5) of Director G was rerun, not reproved. The mixed-seed statement of Director A rests on a published distillation theorem that was not inspected here. Sources reported as inspected by the Directors (Nielsen 1999, Bennett et al. 1996, Horodecki et al. 1997, Barnum-Hilgert 2020, Weichsel) were not inspected here.

Directors A, B and G held edition Z2 for the fourth round and read papers G7 and G8 directly. They report seven last-place differences when rerunning the G8 program; the entry "byte-identical" in the rerun record of edition Z2 is a statement about this participant's container.

Agreement among A, B, G and Z is not counted as replication: common baseline, common sources, two model families.

## 3. Assessments

### 3.1 Z3-A (FOCUSED): what consistency under continuation imposes

**Claim.** With the squared-amplitude rule of G8 on directed walks, the measure of an event and of the event of all its continuations agree up to a fixed factor exactly when the step matrix is a multiple of a unitary matrix on the vectors concerned; and this restricts the carrier.

**Case.** G9 Lemma 3.1 (criterion). Proposition 4.1: with trivial gains only permutations. Proposition 4.2: on an undirected gain graph the normalized step is an involution. Theorem 4.3: for out-degree two and gains of modulus one the digraph is the arc digraph of a digraph with two arcs into and out of every node, the gain group contains an element represented by -1, and the two continuations of a pair of walks interfere with opposite signs.

**Challenge and resolution (SELF_CHECK with exposure).** *The requirement is the conclusion in disguise.* It is a requirement and is listed as one; what is derived is its consequence for the carrier. *The theorem is Severini's.* Severini gives a necessary condition and the Eulerian criterion for arc digraphs; the degree-two statement with unit gains and the -1 is a special case proved here directly, without a claim of novelty. *Exhaustion.* All matrices on at most six vertices with two unit entries per column and orthogonal columns were enumerated (8, 1152 and 691200 with signs; 73728 with fourth roots on four vertices; none on odd vertex sets; none with cube roots); all have the block structure.

**Disposition.** SUPPORTED_IN_SCOPE (Z-023 to Z-025).

### 3.2 Z3-B (FOCUSED): a complex structure from a reversible step (OP-18, OP-20)

**Claim tested (favourable reading).** A reversible step supplies the complex structure of quantum theory and its orientation, without a Hamiltonian being presupposed.

**Case.** G9 Proposition 5.1: a real orthogonal map has a complex structure on the complement of its fixed and reversed vectors, unique under positivity of the generator, reversed with the map. External grounding: Stueckelberg 1960 (abstract); Moretti and Oppio 2017 (abstract): a complex structure unique up to sign from an irreducible real representation of the Poincare group.

**Checked contrary evidence.** G9 Proposition 5.3: on a connected digraph only real scalars commute with the step and with the vertex projections. The records of the rule do not commute with the complex structure of the step (operator norms 0.82 to 0.93 on rings of 5 to 8 sites). In Moretti-Oppio the observables are those generated by the group representation; here the records are not.

**Disposition.** The proposition: SUPPORTED_IN_SCOPE (Z-026). The favourable reading: REFUTED_IN_SCOPE for the model with its records (Z-027). A warrant for complex amplitudes: NOT_IDENTIFIED_IN_SCOPE; OP-18 and OP-20 amended. What is gained: orientation of the complex structure and direction of the step are one datum where the structure exists.

### 3.3 Z3-C (constructed trial, Core 10.3): GH-2, the signed arc digraph of a ring

**Why built.** The second session left dynamics, clock and classical mechanics with negative controls only, and two untested proposals. Directors A and B independently exhibited the failure of continuation for G8. Theorem 4.3 gives the carrier once continuation is required. The trial asks what the smallest such carrier yields.

**Stipulated.** The rule of G8 with its assumptions; consistency under continuation; gains of modulus one; out-degree two; the ring with its translation symmetry; for a force, gains linear in position.

**Derived.** Dispersion with two branches of opposite group velocity (G9 Lemma 6.1). Exact translation of the quasi-momentum by the field per step; uniform pair holonomy of exchanged steps (Proposition 6.3). Velocity as derivative of the eigenphase with respect to the holonomy round the ring (Proposition 6.4). **Quoted.** Convergence in law of position over steps to the group-velocity distribution (Grimmett, Janson and Scudo).

**Observed (28 predicates in two programs; 27 pass).** Moments of X_t/t at t = 400: 0.292059 and 0.292896 against 1 - 1/sqrt 2 = 0.292893. Packet velocities equal the group velocity to 5e-4. Momentum translation exact to 3e-12. Centroid within 0.65 site of the ray over excursions of 16 to 64 sites, returning to the initial vector after one period. **Retained failure:** after subtracting the change of the eigenvector connection the residual is 0.075 and 0.038 site; the criterion 0.02, set before the run, was not met.

**Demolition.** The ring, its order and its symmetry are put in; so is the cylinder on which the rays run. The clock is the step count, without unit. The generator is a choice of logarithm. Real gains suffice: nothing selects complex amplitudes, and the complex structure of the step is not respected by the records. Two inequivalent signings exist already on the ring, and the base digraph is free. The position equation of the rays is not proved with an error bound. Long-time behaviour with a field depends on the arithmetic of the field (Cedzich et al.). With gains of the orders 2, 3, 4, 6, for which the measure does not depend on the character, the field is strong and a walk stays within about six sites over four periods; a staircase of order-4 gains with a weak mean slope does not follow the ray of the mean field (3.80 against 5.53 sites; 12.00 against 22.26; 26 and 39 per cent reflected). A weak force was obtained only with gains whose order grows, where the measure depends on the choice of character (OP-21). One walk, one dimension, no interaction, no composition.

**Proposed transfer.** None to physics. To the map: P7 and P9 pass from negative controls to a conditional construction with a ledger of imports.

**Disposition.** Conditional statements: SUPPORTED_IN_SCOPE (Z-028, Z-029); the ray equation for position: CONDITIONAL (instances; quoted theorem for the free case). GH-2 as an emergence of quantum or classical mechanics: NOT_IDENTIFIED_IN_SCOPE (Z-038; non-selection witnesses: real gains, two signings, free base digraph). A ray limit with a force for gains of bounded order: UNRESOLVED, with two adverse instances (Z-030).

### 3.4 Z3-D (FOCUSED): transport supplied by the carrier (discrete Schild's ladder)

**Claim tested.** A graph can supply its own transport.

**Case.** On a rectagraph, transport of an edge across the unique quadrilateral spanned with the edge travelled is a transport with values in permutations of the edges at a vertex. G9 Proposition 7.1: its holonomy is trivial exactly for Cayley graphs of elementary abelian 2-groups. Computed: trivial on the 4-cube and the folded 5-cube; the full symmetric group S_4 on the incidence graph of the biplane with 7 points. Proposition 7.2: on the Cayley rectagraphs the signings with norm-preserving step are those with every quadrilateral negative, equivalently anticommuting class matrices; the oriented product of the classes is a central complex structure exactly for k = 3 modulo 4.

**Challenge.** *Permutation holonomy gives no interference with both signs.* Correct: the permutation representation contains the trivial one, and by G8 Proposition 4.4 the representation-free measure is the coincidence count on the cover. *The cube with k = 3 gives the Pauli algebra.* Known (Mathews; the description of the Pauli matrices); k is an input.

**Disposition.** SUPPORTED_IN_SCOPE as mathematics (Z-031, Z-032). As a source of quantum structure: NOT_IDENTIFIED_IN_SCOPE. The two proposals of the second session are now examined; the bridge-register entry is replaced.

### 3.5 Z3-E (FOCUSED): paper G8, cover and growth

G8 Proposition 4.4: the measure of the identity indicator is the count of coincidences of lifted walks on the derived covering graph and equals the dimension-weighted mean of the irreducible measures. A covering supplies its group and the list of representations; the choice among them is an input. G8 Proposition 5.2: the gains reached at a given length form a coset of the holonomy group of the gain augmented by length parity; counts tend to infinity; the growth condition of Proposition 5.1 holds exactly when the closed walks of even length realize every group element; otherwise the limit space is complex, real or a set of non-negative rays according to the group they realize. The witnesses of Directors A, B and G are cases. **Disposition.** SUPPORTED_IN_SCOPE (Z-034, Z-035); the growth item of OP-25 is discharged.

### 3.6 Z3-F (FOCUSED): manuscripts

Paper G9 written (13 pages, 12 labelled statements, one of them quoted). Paper G8 revised (12 pages, 10 labelled statements). Paper G7 revised in two paragraphs and one sentence (18 pages, 15 labelled statements). Every statement is proved in the manuscript, quoted with a source, or marked as a computed instance. Numbers typed into the manuscripts were compared with the stored result files.

## 4. Map

Thirteen gates; none passed. Changes: P7 (dynamics) and P9 (classical Hamiltonian mechanics) now carry a conditional construction with its imports; P2 carries the Veronese model with its two readings; P4 carries the complex structure of a reversible step and its incompatibility with the records; P5 carries the additive alternative for returning walks and the failure of continuation; P6 carries the filter results and the restriction of synchronized products; P10 carries the growth criterion and the tension between a weak force and character-independent gains. The bridge register gained two nodes and nine edges; one edge was replaced.

## 5. Candidate feed (Core 10.2)

| Candidate | Class | Treatment |
|---|---|---|
| Signed arc digraph of a ring (GH-2) | constructed ontology | built, executed, demolished; paper G9; `CONSTRUCTED_TRIALS/GH-2` |
| Consistency under continuation | ASSUMPTION_VARIATION of GH-1 | promoted as a named requirement; G9 Lemma 3.1 |
| Polar complex structure of a reversible step | INSTANCE_CANDIDATE for OP-18 | examined; refuted for the model with its records |
| Ladder transport on rectagraphs | FRAME_ALTERNATIVE (from session 2) | examined; G9 Propositions 7.1, 7.2 |
| Stationary holonomy as ray condition | FRAME_ALTERNATIVE (from session 2) | examined in GH-2; exact for the momentum, instances for the position |
| Staircase of order-4 gains | DISCRIMINATOR_CANDIDATE for "bounded order gives a force" | two adverse instances; kept |
| Additive class-function weight of returning walks (Directors A, B, G) | ORIGINAL_SCOPE_COUNTEREXAMPLE to the broad sentence of G8 | promoted; G8 Lemma 3.1 |
| Cubic Veronese model (Director G) | ORIGINAL_SCOPE_COUNTEREXAMPLE to sufficiency of a designated pure-state table | promoted with two readings; G7 Section 5 |
| Matching hierarchy (Director A) | ASSUMPTION_VARIATION | recorded as an edge |
| exp(-isH) on an undirected gain graph (Director G) | FRAME_ALTERNATIVE for dynamics | recorded; imports the imaginary unit and a continuous parameter; not examined further |
| Arc digraphs of degree three with Z_3 blocks | background | noted in G9 Remark 4.4; not examined |
| Composition of two norm-preserving digraphs, with interaction as gains on the product | background | not examined |

## 6. External sources inspected this session (retrieved text, 12 November 2026)

Grimmett, Janson and Scudo, arXiv quant-ph/0309135 (abstract, opening sections), with Suzuki, arXiv 1507.08562 (statement of their result); Stueckelberg, Helv. Phys. Acta 33 (1960) 727 (abstract, first pages of the archive copy); Moretti and Oppio, arXiv 1611.09029 (abstract); Aleksandrova, Borish and Wootters, arXiv 1210.4535 (introduction); Severini, arXiv math/0205187 (abstract, statements); Mathews, arXiv 1907.12357 (abstract, introduction); Alon and Zheng, arXiv 2003.04926 (abstract, Theorem 1.2, statement on folded cubes); Sanyal, Sottile and Sturmfels, arXiv 0911.5436 (abstract, introduction); Cedzich et al., Phys. Rev. Lett. 111, 160601 (abstract, first page); Genske et al., Phys. Rev. Lett. 110, 190601 (abstract, first page). None evaluates this program.

## 7. Limits

- One participant in this stack. A request to a model interface from the container was refused again (HTTP 401); no sub-agent tool exists in the session. Every challenge inside the stack is a SELF_CHECK with exposure.
- Proofs in G7, G8 and G9 are unrefereed. Numerical values are double precision except where exact arithmetic is stated. The linear program for the Veronese model uses constraints on 4000 directions and is not an enclosure.
- From recall, not inspected: the journal references of Grimmett-Janson-Scudo and of Sanyal-Sottile-Sturmfels (arXiv identifiers are given instead), the volume number of Moretti-Oppio, the classification of real Clifford algebras (not used in a proof), the name "derived graph" for the covering of a gain graph.
- The Theorem 6.2 of G9 is quoted in a paraphrase; its hypotheses were read in the arXiv text, not checked line by line against the proof.

## 8. Retained residuals, failures and corrections

- Rays program: the predicate "residual below 0.02 site after the connection offset" failed (0.075 and 0.038) and is kept as failed.
- Checking-program failures on first runs, each kept in the result files: an unevaluated symbolic adjoint (A3 filter success); a test plane that was not invariant; an unbounded loop caused by the fixed determinant of the QR factor; eigenvalue matching at degeneracies (weak-limit prediction -108 and 9.6e7; twist 0 error 7.5e6).
- An assertion of this participant was wrong: that K_4 has a signing with norm-preserving step. None of the 64 signings has; a Hermitian assignment with gains of order four has.
- Between two parts of this session a report stated that a corrected program had been relaunched; it had not produced output, because processes do not persist between calls in the container. The program was split in two and both parts were run to completion and rerun in a fresh directory with byte-identical result files.
- Staircase instances: displacements 3.796 and 11.998 sites against 5.535 and 22.256; strong-field return probabilities 0.25, 0.0625 (order 2), 0, 0.7656 (order 3), 0.5625 (order 4), 0.7656 (order 6).
- Veronese linear program: infimum 0.704 at 20 degrees, 0.207 at 40 degrees, 0 within 2e-3 from 60 degrees on.
- All values retained by Directors A, B and G are kept with their packets in `REVIEW_RECORDS/Directors_A_B_G_2026-11-12/`.

## 9. Obligations

Amended: OP-18, OP-19, OP-20, OP-21, OP-22, OP-23, OP-24, OP-25. New: OP-26 (independent check of paper G9; error bound for the ray position equation), OP-27 (a reason for consistency under continuation and for excluding first-order weights of returning walks), OP-28 (a ray limit with a force for gains of bounded order, or a proof that there is none), OP-29 (which tests are admitted: effect selection and tomography, after the Veronese model). Unchanged: OP-01 to OP-17.

**Closing disposition.** Requiring that the measure of an event equal that of its continuations forces, at the first branching degree, the arc digraph of a two-in two-out digraph and a sign -1; without transport it forces determinism, and on an undirected carrier period two. On a ring the resulting step has rays, and a linear gain moves the quasi-momentum exactly as a force does. The requirement, the ring, the step count, and for a weak force a gain group of growing order are supplied. A reversible step has a complex structure of its own, which the records do not respect. Nothing obtained selects complex amplitudes, supplies a clock, or yields classical Hamiltonian mechanics beyond the rays of a given dispersion function. Root Review: G1, OPEN.
