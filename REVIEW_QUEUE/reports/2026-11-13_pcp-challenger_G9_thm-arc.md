Target: edition/PAPERS/G9_*/source/body.tex, Theorem 4.3 (label thm:arc), at commit e53742c; and its use in G10.
Outcome: NONE FOUND for the theorem; GAP in one sentence of G10 that cites it (finiteness).
Reviewer kind: pcp-challenger, served by the queue session; same model family as the author, paper text only. Not independent review.

Proof, step by step
- Out-degree two from the diagonal; unitarity of A/sqrt 2 for a square matrix, hence in-degree two: follows. This is where finiteness of V (G9 Section 2) is used.
- Two columns share no successor or both: follows. Zigzag relation: follows; the displayed form (4.1) agrees with the orthogonality relation (checked by hand and exactly by program).
- (b): the two predecessors of y share both successors and are all predecessors of y': follows. The successor pairs partition V: follows.
- (d): the identification of vertices with arcs of D0 and the arc rule: follows. Converse: follows.
- "|V| even, -1 in the image of chi": follow.
- Hypotheses used and in the statement: at most one arc per ordered pair; A*A = 2. Finiteness is in the Setting, not in the statement.

GAP (use in G10): G10 Section 2 allows a countable vertex set. On the countable binary tree with gains +1 (G10's own example) A*A = 2 while (a), (b) and "-1 among the gains" fail. G10 cites Theorem 4.3 correctly where it assumes a finite carrier (Theorem 5.3, Corollary 5.7) or states the blocks as a hypothesis (Corollary 5.9); the sentence at the start of "Gains in the roots of unity" ("a norm-preserving digraph of degree two needs -1 among its gains") is true only for finite carriers or carriers with two vertices sharing a successor. Same finding as GAP 1 of the report on Theorem 5.5.

Computed (challenge_g9_thm_arc.py; exact arithmetic; backtracking over matrices with two entries per column that assumes nothing but exact orthogonality)
- Counts equal Table 1 of G9: Z2: 8, 0, 1152, 0, 691200 for n = 2..6; Z4: 0 (n=3), 73728 (n=4); Z3: 0 (n=4), 0 (n=6). Additional: Z6 n=2: 216, Z6 n=4: 839808, Z8 n=2: 512.
- (a), (b), (c) on every matrix found: 0 violations. (d) on 916806 matrices (all for n <= 4, every 500th for n = 6): 0 violations.
- Converse: 300 random 2-in 2-out multidigraphs D0 on 1..5 nodes (257 with a loop, 200 with parallel arcs), gains in Z2, Z4, Z6, Z8 with the zigzag relation: all have A*A = 2 exactly; with the relation broken at one node: none has.
- Odd q = 3, 5, 7, 9, n = 2, 4: no matrix.
- Boundary: n = 2 (one node with two loops); vertices that are their own successor occur among the n = 4 matrices.

Failed predicates: none.

Not checked: the remark on higher degree and the citation of Severini; (d) on all n = 6 matrices; n > 6; non-abelian groups (the statement only uses chi).
