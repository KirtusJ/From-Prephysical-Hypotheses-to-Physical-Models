# Director Z | Technical disposition, fourth session

**Research program:** From Prephysical Hypotheses to Physical Models
**Research direction:** Kirtus Justus
**Reviewing participant:** LLM Director Z, Claude (Anthropic), at the principal's direction; no endorsement by Anthropic is implied
**Date:** 13 November 2026
**Basis:** edition FPHPM-BASELINE-2026-11-12-Z3 (manifest verified, 967 files); the PCP 1.0 Enterprise Edition (build 19) with its ACR 1.0 Implementation packet; the two PCP plugins for Claude (build 22) with the method text of that build
**Root Review state:** Unary, program whole, G1 Grounding OPEN. Nothing below advances it. No ontology is selected.

## 1. Subject

The third session left three items that sit under the probability-rule, dynamics and classical-mechanics gates: a reason for consistency under continuation and for excluding first-order weights of returning walks (OP-27), a force from gains of bounded order (OP-28), and an error bound for the position of a ray (OP-26). It also left the second order of the rule of paper G8 as a supplied assumption (OP-19). This session asked what the continuation requirement decides about the rule itself, and returned to the other two items. No packet of another Director was among the inputs; there was no cross-review.

## 2. Assessments

### 2.1 Z4-A (FOCUSED): what consistency under continuation is, and what it excludes

**Claim.** A family of set functions on walks of each length is one function on cylinder sets of histories exactly when it is consistent under continuation; an additive switching-invariant rule with that property is a multiple of the number of walks.

**Case.** G10 Lemma 3.1: a set of unending walks described at length j and at length j + 1 is the same set, so a function of sets of histories has to give an event and the event of all its continuations the same value; conversely consistency makes the family well defined on the algebra of cylinder sets. G10 Proposition 4.1: on a loopless digraph of constant out-degree the consistency equations force the weight of returning walks to equal the weight of the others. External grounding: Dowker, Johnston and Surya define the decoherence functional of a finite unitary system on this algebra (arXiv 1007.2725, Section 3, equations 19 to 29, read).

**Challenge and resolution (SELF_CHECK with exposure).** *The lemma moves the assumption; it does not remove it.* Accepted. "Events are sets of histories" is an assumption about the event structure and is entered as supplied; what is gained is that the requirement of G9 is no longer a dynamical law added to the rule. *The exclusion could be an artefact of the degree hypothesis.* The linear system was solved on three gain graphs: on the complete graph on four vertices with one gain of order three and on the signed ring the only solutions are constant, with the factor equal to the out-degree; on two triangles with a common vertex (degrees 2 and 4) no factor tried admits a solution.

**Disposition.** SUPPORTED_IN_SCOPE (Z-041, Z-042). The reason asked for in OP-27 is supplied in conditional form: under the event-structure assumption. The assumption itself: not derived.

### 2.2 Z4-B (FOCUSED): the order of the rule (OP-19)

**Claim tested (favourable reading).** The second order of the pair rule follows from the program's primitives.

**Case.** G10 Theorem 5.1: on the signed arc digraph of the line a rule adding over end vertices a function phi of the modulus of the summed gains is consistent under continuation only for phi(n) = n^2 phi(1). The proof uses one event for each a: a walks arriving at a site from the left and one from the right, all of gain +1; its continuation has amplitudes a + 1 and a - 1, which is the parallelogram identity at b = 1. G10 Theorem 5.2: on any norm-preserving gain digraph in which two walks of equal length end at distinct vertices with a common successor, the only consistent power of the modulus is the second (convexity of p -> sum |1 + u_z|^p with sum u_z = 0).

**Checked contrary evidence.** On the same digraph with all gains +1 the rule phi(t) = t, the count, is consistent (control, executed). The event-structure assumption therefore admits a classical first-order rule; it does not select the quadratic one. Rules that are not sums over end vertices of a function of one modulus are not classified.

**Disposition.** The two theorems: SUPPORTED_IN_SCOPE (Z-043, Z-044). The favourable reading as posed: NOT_IDENTIFIED_IN_SCOPE (Z-045; non-selection witness: the count with trivial gains). The substitute, stated beside it: the second order is derived conditional on three supplied items (events as sets of histories; the record-sum form of the rule; a branching norm-preserving carrier), CONDITIONAL. In the ledger of GH-1 the assumption GH1-A1 changes from supplied to conditionally derived.

### 2.3 Z4-C (FOCUSED): a force from gains of bounded order (OP-28)

**Claim as posed.** Gains of bounded order, in particular the orders 2, 3, 4, 6, can produce the rays of a weak force in a controlled limit.

**Case and contrary evidence.** G10 Proposition 6.1: the commutation relation that translates the quasi-momentum holds exactly only for the linear gain, so a translation by Phi needs gains of order at least 2 pi / Phi. G10 Proposition 6.2: the spectrum of the free step is two arcs of length pi/2 with gaps of length pi/2; for q >= 3 no point lies in all q rotations of it by multiples of 2 pi / q, except the four band edges for q = 4 (exact arithmetic for q up to 48, and a proof). Computed: staircases of order 3, 4, 6 hold a walk within about one block for block lengths 16 and 64 up to 2048 steps, leak for block length 4, and are strong fields for block length 1, where the spread is ballistic as Cedzich et al. prove for rational fields (arXiv 1302.2081, abstract, table and the section on the rational case read). A staircase of order 4 reaches 0.69, 0.54 and 0.16 of the displacement of the linear gain of its mean slope at block lengths 16, 64 and 256; the first two reproduce the third session, the third is new.

**Challenge.** *Proposition 6.2 is about local spectra, not dynamics.* Correct, and stated in the paper: the gains are periodic, the theorem of Grimmett, Janson and Scudo applies with the period as cell, and exact confinement is not expected. *Only staircases were tried.* Correct. One quasi-periodic rounding of a linear phase was run and stayed within seven sites over 1024 steps; it is recorded and was not examined further.

**Disposition.** The two propositions: SUPPORTED_IN_SCOPE (Z-046, Z-047). The claim as posed: UNRESOLVED (Z-048), narrowed: an exact force is excluded below the order 2 pi / Phi; for winding gains on long blocks the local spectra have no common quasi-energy; no instance follows the ray of its mean field. A dynamical theorem, and arrangements other than staircases, are open.

### 2.4 Z4-D (FOCUSED): the position of a ray (OP-26)

**Claim tested first.** After the connection offset the deviation of the centroid from the ray through the central quasi-momentum falls as the first power of the field. **Result.** REFUTED_IN_SCOPE as posed (Z-050): 0.075, 0.038, 0.038, 0.062, 0.117, 0.232 site at the periods 64 to 2048; the criterion, fixed before the run, was a fitted exponent in (-1.3, -0.7).

**Second claim, fixed after that failure and before its run.** With the ray and the connection averaged over the quasi-momentum distribution of the packet the remainder decreases monotonically with exponent in (-2.3, -0.7). **Result.** Met: 0.0735, 0.0273, 0.0135, 0.0071, 0.0029, 0.0016 site; exponent -1.1; a packet of half the width gives 0.0075 and 0.0018 at the periods 512 and 2048.

**Grounding.** Panati, Spohn and Teufel (arXiv math-ph/0212041; abstract, introduction with equations 1 to 5, Theorem 3 and Corollary 4 read) prove the first-order semiclassical equations with the Berry connection for Schroedinger operators with a periodic potential. Their theorem does not cover the discrete step of G9.

**Disposition.** UNRESOLVED as a bound (Z-051); the instances are entered in the ledger of GH-2. The criterion of 0.02 site of the third session is met by the averaged prediction from the period 256 on; the failed predicate of the third session stands for the ray through the central quasi-momentum.

### 2.5 Z4-E: the trials as a candidate

**Claim.** With events taken as sets of histories, GH-1 and GH-2 yield quantum mechanics and classical mechanics. **Disposition.** NOT_IDENTIFIED_IN_SCOPE (Z-052). Non-selection witnesses: the count is consistent with trivial gains on the same carrier; real gains satisfy every statement; the carrier, the form of the rule, the group and the character are supplied. No clock, no composition compatible with the step, no physical correspondence.

### 2.6 Z4-F (FOCUSED): manuscript

Paper G10 written (9 pages, 6 labelled statements). Every statement is proved in the manuscript or marked as a computed instance; equation (7.1) is marked as heuristic. Numbers typed into the manuscript were compared with the stored result files. Papers G7, G8 and G9 are unchanged; no statement of them is withdrawn. One sentence of G9 is qualified by G10: the bounded distance of a walk under a linear gain of order 2, 3, 4, 6 is a statement about four periods, and the spread is ballistic at long times.

## 3. Transport, holonomy and the stipulation

The principal's stipulation that monodromy, parallel transport, holonomy and Schild's ladder may bear on a bridge was again treated as a claim under test. What this session adds to it: (i) a measure on histories cannot see the holonomy at first order at all (Proposition 4.1), so the holonomy of a transport enters a history measure at second order or not at all, within the forms examined; (ii) the parallelogram identity that forces the square is the zigzag holonomy -1 of G9 Theorem 4.3 read at one site; (iii) a force is an exact uniform pair holonomy of exchanged steps (G9 Proposition 6.3), and exactness ties its size to the order of the holonomy group (Proposition 6.1). None of these selects a carrier or a number system.

## 4. Map

Thirteen gates; none passed. Changes: P1 carries the event-structure assumption and what it excludes; P5 carries the conditional derivation of the second order and the classical alternative; P7 carries the restatement of the continuation requirement; P9 and P10 carry the bounded-order results and the remainder of the ray. The bridge register gained four edges and one obligation; two edges were amended.

## 5. Candidate feed (Core 10.2)

| Candidate | Class | Treatment |
|---|---|---|
| Events as sets of histories | ASSUMPTION_VARIATION of GH2-A2 | promoted; G10 Lemma 3.1; entered as supplied |
| Rules of the form sum over end vertices of phi(modulus) | FRAME_ALTERNATIVE to "second order is assumed" | promoted; G10 Theorems 5.1, 5.2 |
| The count with trivial gains | ORIGINAL_SCOPE_COUNTEREXAMPLE to "history consistency selects the quadratic rule" | promoted as a non-selection witness |
| Staircases of order 3 and 6; block lengths 1 to 256 | DISCRIMINATOR_CANDIDATE for OP-28 | executed; kept |
| Quasi-periodic rounding of a linear phase to order 4 | INSTANCE_CANDIDATE | one run recorded (displacement within 7 sites over 1024 steps); not examined |
| Packet-averaged ray with connection | INSTANCE_CANDIDATE for OP-26 | executed; heuristic; no bound |
| Isometries of l_p as the ambient form of Theorem 5.2 (Li and So) | background | cited from secondary sources; not inspected; not used |
| Rules that are not sums over end vertices of one modulus | background | not examined |
| A principle requiring that the transport be visible to the measure, as a selector of branching norm-preserving carriers | FRAME_ALTERNATIVE | speculation; not examined; OP-30 |
| Aperiodic arrangements of gains of bounded order; gains depending on the step | background | not examined |

## 6. External sources inspected this session (retrieved 13 November 2026, 06:58 UTC)

Full text retrieved from arXiv and read in the parts named: Dowker, Johnston and Surya, 1007.2725 (abstract; Section 3 to equation 30; Claim 6); Panati, Spohn and Teufel, math-ph/0212041 (abstract; introduction; Theorem 3, Corollary 4); Cedzich et al., 1302.2081 (abstract; Table I; the rational case); Grimmett, Janson and Scudo, quant-ph/0309135 (abstract; Theorem 1). Journal references of the first three were read from the arXiv listing pages. Status as preprint with journal reference; retractions and corrections were not looked for. None evaluates this program. `sources/SOURCE_LEDGER_SESSION_4.md` gives digests.

## 7. Limits

- One participant in this stack. The host of this session has a sub-agent facility; it was not used, because the host reserves it for an explicit request of the principal and this session's instruction did not make one. Every challenge is a SELF_CHECK with exposure.
- The proofs in G10 are unrefereed. Numerical values are double precision; Proposition 6.2 was also checked in exact rational arithmetic.
- The serving model changed during the session (the host named three model identifiers in turn). The record cannot attribute a statement to one of them.
- From recall, not inspected: the bibliographic details and statement of Li and So (1994); the name "cylinder set" for the generators is as in the inspected source.
- Checks recorded in the session register are this participant's reports; no host observed a command.

## 8. Retained residuals, failures and corrections

- Seven failed predicates are kept in the result files: S5 (two: the staircase of period 64 did not drift within 1024 steps; the band velocities came out below 2e-6), C1 and C1b (band velocities from sorted eigenphases returned 21 and 5.5 sites per step for the orders 12 and 24, above the largest possible speed, and 5e-4 for order 2 against an observed spread of 0.17 site per step: the instrument is discarded; order 12 stayed within 24 sites where spreading was expected), M1 and L3 of the first modulus-rule program (unknowns that occurred in no equation; block length 4 is not confined), E1 (ray through the central quasi-momentum).
- First run of the continuation program stopped on a division by zero: an event of two walks with opposite phases has vector zero. The predicate now requires the continuation of such an event to have measure zero as well.
- Two expectations of this participant were wrong and are recorded as such: that a periodic staircase would visibly drift, and that the remainder of the central ray would fall with the field.
- Staircase spreads after 2048 steps (sites), orders 2, 3, 4, 6 by block length 1, 2, 4, 16, 64: 1108, 750, 403, 346, 347; 520, 520, 160, 9.3, 31; 750, 365, 102, 8.4, 34; 520, 181, 27, 11, 48.
- Transmission through one interface for gain steps pi/12, pi/6, pi/4, pi/3, pi/2, 2 pi/3, pi: 0.99974, 0.99944, 0.97466, 0.00254, 3e-13, 3e-13, 0.47693.
- Quasi-periodic rounding: displacements every 64 steps between -6.6 and 5.75 sites.

## 9. Obligations

Amended: OP-16, OP-19, OP-23, OP-24, OP-26, OP-27, OP-28. New: OP-30 (independent check of paper G10; a reason for taking events to be sets of histories; classification of consistent rules outside the record-sum form; what selects a carrier on which a rule that depends on the gains is consistent). Unchanged: all others.

**Closing disposition.** If events are sets of histories, the continuation requirement of the third session is a consequence, a first-order rule is the count and cannot see the transport, and a rule of the record-sum form that does see it on a branching norm-preserving carrier is the squared modulus. The event structure, the form of the rule and the carrier are supplied, and with trivial gains the same structure gives the classical count. An exact force needs a holonomy group whose order grows as the force decreases; gains of the orders 3, 4, 6 wound through long blocks have no common quasi-energy and in the instances computed do not follow the ray of their mean field. Nothing obtained selects complex amplitudes, supplies a clock or a composition, or yields classical Hamiltonian mechanics. Root Review: G1, OPEN.
