Target: edition/PAPERS/G10_*/source/body.tex, Propositions 6.1 (prop:exact) and 6.2 (prop:local), at commit e53742c.
Outcome: NONE FOUND (three wording remarks).
Reviewer kind: pcp-challenger + pcp-micro-review, served by the queue session; same model family as the author, paper text only. Not independent review.

Proposition 6.1
- T commutes with U; T M_m T^-1 is multiplication by m(x-1); U invertible: follow. Both directions of the equivalence follow.
- lambda = m(x-1)/m(x) lies in the group of values: follows. Order at least n for Phi = 2 pi/n: follows.
Remarks: (1) on a ring of N sites m(x) = m(0) lambda^-x is a function only if lambda^N = 1; the statement does not say so. (2) "order at least n" can be sharpened: the order of the group is a multiple of the order of lambda; for Phi = 2 pi k/n in lowest terms it is a multiple of n, and for Phi/2 pi irrational no finite group works. The summary sentence "needs a gain of order at least 2 pi/Phi" is true and weaker. (3) The proposition takes the operator identity as the meaning of "translates the quasi-momentum exactly"; gains that do so only after a position-dependent change of basis, or over several steps, are outside it.

Proposition 6.2
- Orbit criterion; q <= 2 from Sigma = -Sigma; q >= 5 from spacing below pi/2; q = 4 (both end points of a gap); q = 3 (two points in one arc at distance 2 pi/3 > pi/2): all follow.
- The q = 4 result depends on the bands being closed; with open bands the intersection is empty. Sigma is a spectrum, hence closed; fine.

Computed (challenge_prop_exact_prop_local.py). Conventions: (T psi)(x) = psi(x-1); A[target, source]; U M_m applies M_m first; angles in units of pi, exact fractions.
- U unitary, commutes with T (N = 4, 6, 12): defect 2.2e-16.
- Exhaustive over all m: Z_N -> q-th roots for (N,q) = (4,2),(4,4),(6,2),(6,3),(6,6),(5,5),(4,8): the m satisfying the operator identity are exactly those with constant m(x-1)/m(x): 4, 16, 4, 9, 36, 25, 32 of 16, 256, 64, 729, 46656, 3125, 4096. Every lambda is a q-th root with lambda^N = 1; orders of lambda divide q.
- Staircase (blocks of 2 sites, q = 3, N = 12) is not in the set, defect 1.22. For m = exp(-i Phi x), lambda = exp(+i Phi) with the convention above.
- Spectrum of U on rings of 64, 256, 1024 sites: no eigenphase outside the two arcs; band edge reached to 1e-15.
- Intersection in exact arithmetic: q = 1, 2: Sigma; q = 4: the four points 1/4, 3/4, 5/4, 7/4 (times pi) and nothing else; empty for q = 3 and every q from 5 to 200.
- Micro boundary cases, all PASS: constant m; lambda = -1; q = 8 and 12 empty although 4 divides q; q = 6 empty; open bands at q = 4 give the empty set.

Failed predicates: none.

Not checked: Lemma 6.1 of G9 as a derivation (only the numerical spectrum and a hand computation of the eigenvalues of U(k)); Table 6.1; the observed items (a) to (d); the cited theorems of Grimmett-Janson-Scudo and Cedzich et al.
