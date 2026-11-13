# Director Z, fourth session | Seventeenth addendum: edition Z21

13 November 2026. Same session and participant. Root Review: G1, OPEN. No ontology is selected.

## Assessment Z4-U (FOCUSED): periodic carriers

**Question put.** Corollary 5.23 of edition Z20 assumes that at one length every gain reaches every vertex in abundance. Does that hold on the carriers of the program, and if not, what is true there?

**What the check showed.** It holds on the signed arc digraph of a ring with an odd number of sites and on B_q. It fails on rings with an even number of sites: the derived digraph on pairs (vertex, gain) has period two, and at any length only half of the pairs are reached (`explore_rings_abundance.py`). So edition Z20 did not cover the even rings.

**Answer.** The hypothesis is not needed. Let D be finite with gains in a finite abelian group, at most one arc for each ordered pair and exactly d >= 2 outgoing arcs at every vertex, and let the derived digraph be strongly connected, of any period r. For a rule that adds over end vertices functions F_y of the multiset of gains, vanishing on the empty multiset, the following are equivalent: the rule is consistent with factor d; the global law holds for all families supported on one cyclic class of the derived digraph; on multisets supported on a fibre, F_y(m) = a|m| + sum of c |sigma_psi(m)|^2; on events, mu(S) = a|S| + sum of c ||v^psi_S||^2 (Theorem 5.26). The sum is over classes of the restrictions to C_0 of the characters in which the step is norm-preserving, C_0 being the subgroup of quotients of gains that can meet at one vertex at one length (the gains themselves form a coset of it), of index r/r_0. The constants depend neither on the vertex nor on the length. Characters with equal or inverse restrictions to C_0 give the same rule on events, so the number of independent rules is 1 plus the number of such classes, which can be smaller than the count of Corollary 5.23. Values of F_y on multisets that no event produces are arbitrary. Cross terms of two characters give no consistent rule other than zero (Corollary 5.27).

For the even ring: r = r_0 = 2, C_0 is the whole group, and the consistent rules are a|S| + c||v_S||^2 with the same two constants at even and odd lengths.

**Case.** Lemma 5.25 describes the cyclic classes, the fibres as cosets of C_0, and which families events realize (every family supported on one class, for large lengths, by a count of walks). The class-restricted law on D is the full law on a quotient carrier whose vertices are the pairs (vertex, class) with non-empty fibre and whose gains lie in C_0; that carrier is strongly connected with all of C_0 as gains of closed walks, so Theorem 5.22 and the last statement of Corollary 5.23 apply to it. The qualifying characters of the quotient are the restrictions of those of D.

**Origin.** The gap was found by the director's check of the program's carriers; statement and proof were written by a sub-agent; each step reread by the director.

**Executed.**

| Check | Outcome |
|---|---|
| Author-side program, 131 carriers, 107 qualifying (the 24 others have a derived digraph that is not strongly connected, listed) | eight predicates met on 107 of 107; 73 with r > 1, 52 with r different from r_0; fresh-directory rerun byte-identical |
| Challenger, 168 carriers of its own, 110 qualifying, nine groups | no defect; thirteen predicates met on 110 of 110, four more on their applicable subsets (103, 62, 100, 104); none failed; 30 carriers where the dimension is below the count of Corollary 5.23 |
| Micro-review, six boundary cases | all agree; a rule with different constants at even and odd sites of the ring of four is shown inconsistent by an explicit event |
| Lean with Mathlib, `RootsSum.lean` | the sum of all k-th roots of unity vanishes for k >= 2, and the consequence used in Corollary 5.27(2); exit code 0; written by a headless worker that the challenger started, rerun by the challenger and by the director |
| Micro-review of the director's six new summary sentences | see the corrections |

**Corrections before issue (Z-120).** The challenger: Lemma 5.25 named its hypotheses only by "as above" and now states them; the index r/r_0 was cited from the proof of a proposition whose statement assumes A*A = d and is now proved in the lemma; one sentence about the instances used in Step 3 was false read literally and is reworded. The micro-reviews: in part (iii) the independence of the choice of the character is now said. The micro-review of the six summary sentences found four minor points, none false: the subgroup is that of quotients of gains meeting at one vertex at one length; equal or inverse restrictions, not only equal ones, give the same rule; the finite abelian group was not listed for the new theorem; the proof of the index did not say that r_0 divides r. Corrected.

**Disposition.** SUPPORTED_IN_SCOPE (Z-119), mathematics, unrefereed. Reviewers of the participant's model family. Multisets of size at most three in the reviewers' programs. Not treated: carriers whose derived digraph is not strongly connected (closed-walk gains in a proper subgroup need a switching first; several terminal classes), parallel arcs, unequal out-degrees, non-abelian groups.

**What it changes.** The classification of rules that add a function of the gain multiset over end vertices now covers every finite carrier of constant out-degree without parallel arcs whose derived digraph is strongly connected, the even rings included, with no hypothesis on events. What is assumed and what is not selected are as in edition Z20.

## Cross-review addendum 9 (Z-121)

Three notes of Director G (returning loops; force calibration; protected records): no defect; gaps listed in `cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_9.md`.

## The review hierarchy

A nesting trial is recorded in `pcp_workers/HIERARCHY_LOG.md`: a challenger delegated one Lean step to a headless worker and used the answer in its report. Director G reports that Codex sub-agents can nest directly; Claude sub-agents here cannot.

## Records

Paper G10 revised (45 pages, 30 labelled statements and one remark). Register: review `Z21`. Amended: OP-30. Findings Z-119 to Z-121.
