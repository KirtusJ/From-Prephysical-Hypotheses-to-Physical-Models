Target: edition/PAPERS/G10_*/source/body.tex, Corollary 5.13 (cor:vsl), two questions set by the director for edition Z14; text of Z15, commit b84056e.
Outcome: NONE FOUND. Answer to the question left open in the paper: yes, the hypothesis of Corollary 5.13 follows from that of Theorem 5.3.
Reviewer kind: pcp-challenger + pcp-micro-review, queue session; same model family as the author; paper text only. Not independent review.

Question 1: does the hypothesis of Corollary 5.13 follow from the hypotheses of Theorem 5.3 (finite, gains +-1, norm-preserving of degree two, connected)?
Argument (each step is in the paper, edition Z15):
- D is strongly connected (in- and out-degree two, connected). The gains of closed walks generate Z2: otherwise a switching makes all gains +1, which Proposition 3.1 of G9 excludes for a branching step. So D-hat is strongly connected.
- By the first step of the proof of Corollary 5.15 the elements u u_z' lie in C0 and sum to zero, so C0 is not trivial; for C = Z2 this gives C0 = C, that is r = r0.
- Proposition 5.14(b),(c) then gives both gains at both vertices of every block, at least N times at one length, from every starting vertex.
So the sentence after Corollary 5.13, "whether the corollary's hypothesis follows from theirs is not examined", can be replaced for Theorem 5.3 by the statement that it does. For Theorem 5.2 it does not: that theorem has no roots of unity.
Computed: 305 carriers built, 234 satisfy the hypothesis of Theorem 5.3 (2 to 16 vertices, rings of 3, 4, 5, 8 sites included). On all 234: D and D-hat strongly connected, r = r0. For every pair with a common successor and every starting vertex (6904 instances) a length exists with both gains at least 25 times at both vertices. Control: on the paper's q = 4 four-vertex example the same test fails in 8 of 8 instances, as it should.

Question 2 (micro-review): merging vertices whose successors are not all common (m < d), through actual events.
- W(4,3), gains +-1: d = 3, m = 2; conference matrix C6: d = 5, m = 4; W(4,3) with row and column gains in Z4: d = 3, m = 2, q0 = 4. A*A = d exact; abundance holds (24/24, 90/90, 24/24).
- The pair event with a = b = 1 has 2(d - m) components of modulus one and m components |1 + u_z| with sum of u_z zero: PASS on all three.
- 600 random events each: the squared modulus solves every consistency equation exactly: PASS. The solution space restricted to moduli with |v|^2 <= 9 has rank 1: PASS on all three (unique up to a factor, as Corollary 5.13 gives for q0 = 2 and 4).

Failed predicates: none.
Not checked: m < d with q0 > 4; carriers of degree two with gains of higher order; the "for every N" of the hypothesis beyond N = 25 (it follows from growth, 5.14(b)).
