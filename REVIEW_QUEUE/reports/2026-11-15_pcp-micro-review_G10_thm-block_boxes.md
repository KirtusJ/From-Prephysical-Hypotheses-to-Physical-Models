Target: G10 Theorem 5.16 (thm:block) and Corollary 5.17, exact box solutions without symmetry for a block of degree four and one of order five or more (director's Z16 request); master a8c9608.
Control: phi(10). Expected 4; reported 4. Control passed.
Outcome: NONE FOUND.
Reviewer kind: pcp-micro-review run as a sub-agent of the queue session. Same model family as the author.

Method: an unknown real value at each point of a box of Z[zeta_q] (power basis, coefficients in [-L, L]); no symmetry imposed, the value at 0 not fixed; hypothesis B*B = d tested per block; all instances of the block law inside the box at L = 2, 60,000 random instances for larger boxes; ranks exact modulo the prime 2147483629 (a rank over a prime field is a lower bound for the rational rank); dimension on interior points.
- Fourier block, q = 4, d = 4: dimension 1 at L = 2 and L = 3 (expected 1). PASS.
- The paper's 3 x 3 block of order 6: dimension 1 at L = 2 and 3 (expected 1). PASS.
- Fourier block, q = 5, d = 5: dimension 2 at L = 3 (expected 2). At L = 2 only 45 equations fit and 81 interior points stay free: too small a box, not a counterexample.
- Real Hadamard block over Z4 (entries generating a proper subgroup; control): dimension 3, all real quadratic forms, as the paper's remark on dropping the generation condition says. PASS.
Self-error, kept: the reviewer first entered the order-6 block with two rows swapped; the hypothesis test caught it (B*B != d). No ambiguous wording found. Not covered: d = 2, q = 2.
Rechecked by the queue session: the control.
