Target: G10 Theorem 5.32 (thm:posprod), parts (ii) and (iv), body.tex lines 775-875, master a8c9608; and edition/COMPUTATION/Lean/Mathlib/ProductEvents.lean.
Control: decide in Lean that n^2 >= 2n for all natural n. Expected: refuted (n = 1). Delivered: a proof of the negation with n = 1. Control passed.
Outcome: NONE FOUND. Parts (ii) and (iv) check in Lean in the abstracted form below; no hypothesis is missing; a shorter argument for (ii).
Reviewer kind: pcp-formalizer run as a sub-agent of the queue session; the file was rerun by the queue session (exit 0, standard axioms on every theorem, no sorry / axiom / native_decide). Same model family as the author. Not independent review.

The existing ProductEvents.lean (rerun unedited, output identical to ProductEvents.out) covers only the site-independent algebra of part (i) and its converse.
PosProd.lean (Lean 4.12.0, Mathlib v4.12.0) proves:
- part_ii: functions FR, FL from sites (integers) and pairs to reals, vanishing at (0,0), satisfying the site equation with factor 2 at every site and for all pairs, and bounded below in the site for each fixed pair, are independent of the site, are equal, and have the form a(p+q) + c(p-q)^2 with a = F(1,1)/2 and c = F(1,0) - a.
- part_ii_ring: the same for functions of period N on the integers (the ring lifted), with no condition on N.
- part_iv: for F of that form, the continuation identity summed over any finite set of sites.
Abstracted: the walk and event layer (Lemmas 5.30 and 5.31) is replaced by the equation they give, at every site and for all pairs; the ring condition N/gcd(N,2) >= 11 enters only through Lemma 5.30, which is not formalized; in (iv) the assignment of the continued multisets to vertices is taken, not proved.
Shorter argument: on the line, the functionals s = alpha + (phi - 1) beta and t = alpha - phi beta satisfy s(x+1) = phi s(x) and t(x-1) = -phi t(x), so boundedness forces both to vanish, with no eigenvectors; the ring case follows from the line case because a periodic function is bounded.
Cost reported: about 9 minutes, 5 tool calls.
