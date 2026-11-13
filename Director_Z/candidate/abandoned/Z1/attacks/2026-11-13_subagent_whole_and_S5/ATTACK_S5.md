**Verdict: WOUND.** Target: S5. Attacker: sub-agent of the author's model family; not independent review.

S5 is not empty and not derivable. It is a condition on the rule, equivalent to the conclusion it serves, too weak as worded, and never met exactly on most rings.

**(i) Not derivable from S1 to S4.** The count satisfies them and has R_t <= 1/d (ring of 8: max 1/4 over t <= 48). HELD on this point.

**(ii) Not a statement about the system.** "The weight of returning" is the rule's weight. Given D1 and S4, S5 holds if and only if a = 0, so S5 is D2 in other words. Its rule-independent content is different: "some character has A*A = d", a property of the carrier, necessary for S5, and the unitarity of the step. Without it S1 to S5 have no rule at all. S5 therefore carries reversibility of the carrier plus a ban on the count.

**Wording.** "Comes arbitrarily close to one" is met by a single equality. The rule (37/5)||v||^2 - (32/5)|S| on the ring of 8 has R_10 = 1, is consistent, additive and normalized, and has a != 0; only non-negativity excludes it. S5 should say limsup.

**(iii) How late.** Signed ring, x0 = (0,R), exact integers, t up to 100000:

| N | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| first R_t = 1 | never | 8 | never | never | never | 24 | never | never | never | never |
| first R_t > 0.99 | 38 | 8 | 264 | 38 | 504 | 24 | 95946 | 264 | not by 100000 | 6416 |

"Never" is proved for all t: if R_t = 1 then (U^2)^t fixes e_x0, so the minimal polynomial of U^2 at e_x0 divides x^t - 1 and has integer coefficients; for every N in 3..12 except 4 and 8 it has a non-integer coefficient (N = 3: x^3 - (3/2)x^2 + (3/2)x - 1). The candidate's two exact returns are the only ones here. Growth is irregular: 3 and 6 agree, 5 and 10 agree, 9 needs 95946 steps and 11 more than 100000. No growth law is proved. W3 holds on the primary instance itself.

**(iv) S3 against S5.** No formal conflict. The model weights sets of walks of one length; "record" enters only as the grouping by end vertex at that length. Intermediate vertices are not records. Ring of 8, t = 24: return weight 1 with no intermediate record, 1/4 with the vertex recorded at t = 12, 2049/16384 with it recorded at every step. The conflict is with the word. End-vertex distributions at two lengths are not marginals of one distribution: the classes "at y at length 2 and at z at length 3" sum to 1/4 at (1,R) and at (7,L), against P_3 = 1/2 and 0. If records persist, the rule is the count and S5 fails. S5 is compatible with S3 only because S3's records are not kept.

**Failed predicates, kept.** Q4: N = 11 is not above 0.99 by 100000. Q5: "a midpoint record always lowers the return" is false on N = 4, where the walk is at one vertex with certainty at t = 4.

**Computed.** `return_times.py`, 4 of 6 predicates; a first run crashed before writing a result and is recorded in `FINDINGS.md`.

**Not tried.** N > 12, including N = 16 of the candidate's table. A proof of the growth rate. Other starting vertices. Director G's staircase.
