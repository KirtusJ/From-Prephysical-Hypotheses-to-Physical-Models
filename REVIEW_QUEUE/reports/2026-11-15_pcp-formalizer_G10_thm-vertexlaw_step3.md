Target: the induction of Step 3 in the proof of G10 Theorem 5.22 (thm:vertexlaw) (director's Z20 request; Step 3 of Theorem 5.18 was also asked and not attempted); master a8c9608.
Control: decide in Lean that (a+b)^2 = a^2 + b^2 for all integers. Expected: refuted. Delivered a proof of the negation (a = b = 1). Control passed.
Outcome: NONE FOUND; the core and the induction check in Lean with four steps taken as hypotheses (listed).
Reviewer kind: pcp-formalizer run as a sub-agent of the queue session; the file was rerun by the queue session (exit 0, standard axioms, no sorry / axiom / native_decide). Same model family as the author. Not independent review.

Existing files rerun unedited: VertexLaw.lean (unit vectors summing to the count are equal; an invertibility lemma; the pigeonhole of Lemma 5.24(2)) and MultisetBlock.lean (unit sum, triple pairing, vanishing of a quadratic); neither has the assembled Step 3 or its induction.
VertexStep3.lean proves:
- step3_core: over any field K and finite V, with a predecessor relation, weights u, v, r nonzero on arcs, d != 0, the three-input identity (eq:vtri) and a hypothesis hW (a nonzero f has a vertex with f != 0 and two distinct predecessors), f = 0. The step "a vertex of R has at most one predecessor" (the matrix argument) is proved here, not assumed.
- step3_induction and step3_whole: the induction over the degree N >= 3, giving vanishing at every degree.
Taken as hypotheses (not proved): that (a) and (b) give eq:vtri (the ring of polynomials, the maps tau_k and the characters X_psi); Lemma 5.24(2) with (b), as hW; nonvanishing of u, v on arcs (character values); that the products X_psi span P_N.
No shorter route; the two-predecessor vertex only needs to lie in R, the closedness of W is used only to obtain hW.
Rechecked by the queue session: the rerun of VertexStep3.lean. Cost: about 12 minutes, 8 tool calls.
