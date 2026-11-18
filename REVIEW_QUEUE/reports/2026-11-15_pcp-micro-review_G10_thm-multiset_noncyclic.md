Target: the dimension formula of G10 Theorem 5.18 (thm:multiset) on the non-cyclic groups C2 x C2 and C2 x C4 (director's Z17 request); master a8c9608.
Control: number of characters of C2 x C4. Expected 8; reported 8. Control passed.
Outcome: NONE FOUND.
Reviewer kind: pcp-micro-review run as a sub-agent of the queue session. Same model family as the author.

Method: J0 and U computed exactly; the block law solved over the rationals on every multiset of size at most 3 with every input tuple of total size at most 3. A truncated nullity is at least the true dimension, so agreement is consistent with the formula, not a proof at larger sizes.
- C2 x C2, d = 4, the Corollary's first matrix: formula 4, nullity 4 (also the paper's stated dimension). PASS.
- C2 x C2, d = 4, a matrix where U is one character (kernel {1, b}), as the paper says: formula 2, nullity 2. PASS.
- C2 x C2, d = 2, entries not generating C (outside the Corollary): formula 5, nullity 5. PASS.
- C2 x C4, d = 2, two matrices with |U| = 4: formula 14, nullity 14 for both. PASS.
- C2 x C4, d = 2, U empty: formula 1, nullity 1 (multiples of |m| only). PASS.
No ambiguous wording. Not tested: multisets of size 4 or more for C2 x C4 (a first exact run timed out; kept); d >= 3 on C2 x C4.
