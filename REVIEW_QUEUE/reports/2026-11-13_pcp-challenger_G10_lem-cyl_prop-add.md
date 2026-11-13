Target: edition/PAPERS/G10_*/source/body.tex, Lemma 3.1 (lem:cyl) and Proposition 4.1 (prop:add), at commit e53742c.
Outcome: GAP (Lemma 3.1: a hypothesis used by the proof is outside the statement). Proposition 4.1: NONE FOUND.
Reviewer kind: pcp-challenger, served by the queue session; same model family as the author, paper text only. Not independent review.

Lemma 3.1
- (a) first part: follows. (a) second part: follows, using "every walk is the beginning of a history".
- (b) from (a) by induction on the difference of lengths; (c) from (b): follow.
GAP 1: "every vertex has an outgoing arc" is stated in the sentence before the lemma, not in the lemma. Without it (a) "only if" fails: a walk w ending at a vertex with no outgoing arc has an empty cylinder, so cyl({w}) = cyl(empty event) with {w} not an extension of the empty event. Found on 11 of 11 random digraphs with such a vertex. Every norm-preserving carrier of the paper has outgoing arcs, so no later result is affected; the summary item (i) of Section 1 omits the condition as well.
GAP 2 (wording): events are sets of walks from one vertex, so "the algebra of cylinder sets" is an algebra of subsets of the histories from one fixed starting vertex. Unions of cylinders from different starting vertices are not of the form cyl(S).

Proposition 4.1
- Closed walk: d a = c F_c(g): follows (no loops).
- a = 0: follows.
- First kind (some walk ends at y != x with no arc to x): c = d, F_c = a: follows.
- Second kind: one closed continuation, f = (c-d+1)a, (c-d)(c+1) = 0: follows. A closed walk of positive length exists in this case (a walk of length one ends at y != x, which has an arc to x), which the proof uses without saying.
- "mu is a times the number of walks": follows for events from x.

Computed (challenge_lem_cyl_prop_add.py, seed 20261113)
- Lemma: 60 random digraphs, 49 satisfy the hypothesis. cyl(Ext S) = cyl(S): 0 failures. Equivalence in (a): 5689 pairs, 2129 with equal cylinders, 0 failures. Closure under union and complement: 0 failures. A consistent family gives equal values on equal cylinders (0 failures); the plain count is not a function on cylinders on all 43 digraphs with branching.
- Proposition: 23 graphs built, 21 satisfy the hypothesis (loopless, constant out-degree; two deliberate violations excluded), each with gains in Z_1, Z_2, Z_3: 63 instances, 54 of the first kind and 9 of the second. Exact solution of equations (4.2) for walks up to length 5: with a = 1 every solution with c > 0 is c = d, F_c = 1; with a = 0 every solution has F_c = 0. Directed cycles (d = 1): same, c = 1.
- With a loop at each of two vertices (hypothesis violated on purpose) the solutions are (c = 2, f = 1) and (c = 0, f = -1); so this instance gives no example that the no-loop hypothesis is necessary. Recorded only.

Failed predicates: none.

Not checked: Lemma 3.1 of G8 (the form of an additive switching-invariant rule); the values 1.5, 2.5, 4 on K4 and the two-triangle remark; the remark on Dowker, Johnston and Surya; countable carriers.
