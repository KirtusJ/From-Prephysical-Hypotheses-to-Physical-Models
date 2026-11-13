# Candidate model Z1, version 0.1: stipulated, open for attack

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada

Prepared with Director Z (Claude, Anthropic) as assistant. 13 November 2026.

**Status.** This is a stipulated candidate, written down so that other directors and agents can attack it. It is not an ontology and it is not claimed to be true of anything. No gate of the program is passed by it; the root review is open. Every line below is marked STIPULATED (assumed, with no derivation), PROVED (a statement of paper G10 with its number; unrefereed, reviewed only inside one model family), COMPUTED (an exact or numerical instance), or NOT OBTAINED.

The purpose of a stipulated model is to make the assumptions few, explicit and separately breakable. An attack that kills one stipulation is a result.

## 1. The model in one page

**Carrier.**

- S1 (STIPULATED). A finite gain digraph D: vertices V, arcs with gains in a finite abelian group C, at most one arc for each ordered pair of vertices, exactly d >= 2 arcs leaving every vertex, and a strongly connected derived digraph (the digraph on pairs of vertex and gain). A starting vertex x0.

**Events.**

- S2 (STIPULATED). A history is an unending walk from x0. An event is a set of walks of one length from x0, standing for the set of histories that begin with one of them. The weight of an event does not depend on the length at which it is described, up to the factor d per step (consistency under continuation).

**Records.**

- S3 (STIPULATED). End vertices are records: the weight is a sum over end vertices, and the term at a vertex depends on the walks ending there only through the multiset of their gains. The term may be a different function at each vertex. The empty multiset has weight zero.

**Normalization.**

- S4 (STIPULATED). Weights are non-negative and a single walk has weight one.

**Return.**

- S5 (STIPULATED). The weight of returning to the starting vertex, divided by the number of all walks, comes arbitrarily close to one at positive lengths.

**Composition.**

- S6 (STIPULATED). On pairs of events of one large length the weight is multiplicative, with the same formula on the product.

**Character.**

- S7 (STIPULATED, only where needed). Where S1 to S6 leave more than one rule, one class of characters of C is chosen by hand. On the primary instance below nothing is chosen.

**What follows.**

- D1 (PROVED, G10 Theorem 5.26 from S1, S2, S3). The weight of every event is a|S| + sum of c_psi ||v^psi_S||^2, with |S| the number of walks, v^psi_S(y) the sum of psi(gain) over the walks of S ending at y, the sum over the characters psi of C for which the step matrix A^(psi) satisfies A* A = d (counted up to an identification), and constants that depend on neither the vertex nor the length.
- D2 (PROVED, G10 Corollary 5.29 from D1, S4, S5). a = 0: no counting part. S4 forces the coefficients of the distinct restricted character classes to be non-negative. The proof uses single-endpoint events with arbitrarily large gain multiplicities. [Coefficient signs and exact witnesses](attacks/2026-11-13_Codex_D2.md)
- D3 (PROVED, G10 Corollary 5.28 from D1, S6). The rule is zero, the count, or the squared norm for one class of characters; with D2 and S4 it is the squared norm for one class.
- D4 (consequence of D1 to D3 and S7). The model's rule: **mu(S) = ||v_S||^2**, for one character. The probability that the walk is found at y after t steps is P_t(y) = |(U^t)_{y x0}|^2 with U = A/sqrt(d), a unitary matrix. This is the rule and the dynamics of a discrete-time quantum walk on D.

So the model is: a walk on a finite gain digraph whose amplitudes are sums of gains, with squared-norm probabilities, in which the squared norm is not assumed but follows from S1 to S6.

## 2. Primary instance Z1-R: the signed ring

- Vertices (x, R) and (x, L) for x in Z/N. From either vertex at x one arc goes to (x+1, R) and one to (x-1, L). Gain -1 on the arcs (x, L) -> (x-1, L), gain +1 on all others. C = {+1, -1}, d = 2, x0 = (0, R).
- S1 holds for every N >= 3 (COMPUTED for N = 3, 4, 5, 8, 16; the derived digraph has period 1 for odd N and 2 for even N, both covered by Theorem 5.26).
- C has one non-trivial character, the sign, and the step is norm-preserving for it. So D1 gives a|S| + c||v_S||^2, and S4 with S5 gives a = 0, c = 1 **without S6 and without S7**. On this instance the rule is forced by S1 to S5.

Exact values (COMPUTED, `candidate_z1_instance.py`, 6 of 6 predicates; ring of 16 sites so that nothing wraps):

| t | model: probability by end vertex | count rule, for comparison |
|---|---|---|
| 1 | (1,R) 1/2; (-1,L) 1/2 | the same |
| 2 | (0,R), (0,L), (2,R), (-2,L): 1/4 each | the same |
| 3 | (1,R) 1/2; (1,L), (3,R), (-3,L), (-1,R): 1/8 each; **(-1,L): 0** | (1,R) 1/4; (-1,L) 1/4; the others 1/8 |
| 4 | (2,R) 9/16; seven others 1/16 each | 3/16 at four vertices, 1/16 at four |

- The first difference from counting is at three steps: the vertex (-1, L) is dark, and (1, R) has probability 1/2 against 1/4.
- Return (S5): on the ring of 4 sites the model returns to x0 with weight exactly 1 at t = 8, on the ring of 8 at t = 24; under counting the return weight never exceeds 1/4 on these rings.

## 3. Extended instance Z1-F: a force (weaker standing)

- Gains in the q-th roots of unity, with the additional gain m(x) = e^(-i Phi x), Phi = 2 pi / q, on every arc leaving site x (a linear gain).
- PROVED (G9 Proposition 6.3; G10 Proposition 6.1): this gain translates the quasi-momentum by Phi per step, and no gain of smaller order does so exactly.
- COMPUTED, not proved (G10 Section 7): the centroid of a packet follows the ray averaged over the packet, with a remainder that falls about as the first power of the field.
- Here C has several characters for which the step is norm-preserving, the conjugates of the faithful one. S7 is needed: the model stipulates the faithful character with zeta = e^(2 pi i/q). Another conjugate, zeta -> zeta^j, is the same model with the field j Phi. **The choice of character is the choice of the unit of force**, and nothing in the model makes it.

## 4. What the model does not contain

NOT OBTAINED, each a place to attack by showing the model cannot be extended:

- a reason for any of S1 to S7;
- more than one space dimension; a continuum limit with a proof; a mass (Director G has constructions; not part of Z1);
- more than one particle, interaction, or composite systems beyond the formal product events of S6;
- a dynamics of records: S3 names end vertices as records and does not say how a record is made, kept or read;
- classical mechanics: only the ray statement above, computed and not proved;
- any correspondence with a physical system.

## 5. Known weaknesses, stated by the author

- W1. **Weights of events are not probabilities of events.** On Z1-R at t = 3 the event of all eight walks but one (the walk (0,R) -> (1,R) -> (0,L) -> (-1,L), gain -1) has weight 9, that is 9/8 after division by 2^3 (COMPUTED; Director G found the same kind of event, 33/32, on the staircase). Only the weights of the end-vertex classes of the full event form a probability distribution. Yet S2 demands consistency for every subset of walks, including those no instrument selects. The theorems D1 to D3 use that demand in full.
- W2. **S3 and S5 pull against each other.** S3 treats end vertices as records. S5 asks the walk to return to its start with weight near one, which a system that keeps permanent records of where it has been cannot do. The model has no account of when a record is permanent.
- W3. **S5 is late.** On Director G's staircase the first return above 0.99 is at tick 11736 for the smallest order (reviewer's scan). A premise that can only be tested after ten thousand steps carries the exclusion of counting.
- W4. **S6 is formal.** It is a statement about a formula on pairs of events, not about a composite carrier; consistency on the product carrier is not examined.
- W5. **S1 is narrow.** Constant out-degree, no parallel arcs, finiteness and strong connectivity of the derived digraph are each used by a proof; outside them counterexamples exist (parallel loops: a rule that is not of degree two; the infinite tree: every rule; two components: constants that differ).
- W6. **The rule is forced only up to the character.** On Z1-R there is one; on Z1-F the choice is a stipulation with a physical meaning.
- W7. **All review so far is by sub-agents of one model family and by Director G in contact with the author.** Nothing here has been refereed.

## 6. Attack sheet

An attack names its target, states what it would take to succeed, and leaves a file. Kills are wanted more than confirmations.

| Target | The attack invited | It succeeds if |
|---|---|---|
| D1 | break Theorem 5.26 | a carrier satisfying S1 and a family of functions satisfying S2, S3 whose event weights are not of the stated form; or a failing step in the proof |
| D2 | break Corollary 5.29 | a rule with a > 0 satisfying S1 to S5; or a carrier where the bound 1 - a(1 - 1/d) fails |
| D3 | break Corollary 5.28 | a multiplicative consistent mixture at large length |
| S2 | show the consistency demand is unphysical or stronger than needed | a weaker, instrument-level demand (only events an apparatus on the carrier can select) under which D1 fails, with the surviving rules exhibited; or a proof that D1 survives the weakening |
| S3 | show "records" is carrying the result | a rule not additive over end vertices, or one that sees more of a walk than its gain, that satisfies the rest and is not ||v||^2; or a second, equally natural choice of what the records are that gives a different rule on the same carrier |
| S3 with S5 (W2) | show the two are inconsistent | a precise sense of "record" under which S5 fails for every non-trivial carrier, or a model of records in which both hold |
| S5 | show the premise is empty, circular or false | a derivation of near-return from S1 to S4 (then it is not a premise); or a carrier satisfying S1 on which the ||v||^2 rule does not return (it always does, by unitarity: attack the claim); or an argument that S5 assumes reversibility, which is the quantum conclusion in other words |
| S6 | attack the formal product | a composite carrier on which the product rule is not consistent; or two different carriers whose product admits a consistent multiplicative mixture |
| S7 | find what selects the character | any structure on the carrier, the records or the events that distinguishes zeta from zeta^j; or a proof that none of a stated kind can |
| S1 | widen or break the carrier class | the classification on carriers with parallel arcs, unequal out-degrees, non-abelian gains, infinitely many vertices, or a derived digraph that is not strongly connected |
| Z1-R | recompute | any value of the table above, or of the return times, that does not reproduce |
| Z1-F | attack the force | a staircase or other gain of bounded order that follows the ray of its mean field (G10 found none); or a failure of the ray statement at small field |
| The whole | show the model is a restatement | an argument that S1 to S6 together are equivalent to assuming a unitary evolution with the Born rule, so that nothing is explained; or the opposite, a strictly weaker set of stipulations with the same consequences |

## 7. Rules of engagement

- File an attack as `Director_Z/candidate/attacks/<date>_<attacker>_<target>.md` with its program and result file beside it, or as a note in `Director_G/` for Director G. One target per file.
- A program states its predicates before its first run, tests each hypothesis per instance, refuses to overwrite its result, and keeps failed predicates.
- Verdict line first: KILL (the target is false or empty), WOUND (a hypothesis is missing or a statement must be narrowed), HELD (the attack was carried out and failed, with what was tried), NOT ATTEMPTED.
- A failed attack is kept. A successful one is carried into the next version of this file, with the stipulation struck or narrowed and the attacker named.
- Nobody, the author included, marks a target as surviving without naming the attack it survived.

## 8. Ledger

| Date | Attacker | Target | Verdict | File |
|---|---|---|---|---|
| 13 Nov 2026 | challengers 9, 10, 11 and micro-reviews (sub-agents of the author) | D1, D3, D2 | HELD, with wording wounds corrected in editions Z21 to Z23 | `edition/REVIEW_RECORDS/Director_Z/Session_4/challenger_9/`, `challenger_10/`, `challenger_11/` |
| 13 Nov 2026 | Director G | S5 on the staircase | proposed the premise and a reason for it; cross-read in `Director_Z/cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_10.md` | `Director_G/Return_records_and_reversible_dynamics.md` |
| 13 Nov 2026 | Codex case-study review | D2, sign hypothesis of Corollary 5.29 | HELD on the full S2 event space | [Proof and exact cases](attacks/2026-11-13_Codex_D2.md) |
