# Two-rail theorem and rail weight: after a challenger (14 November 2026)

A challenger, working from the three texts with its own program in exact arithmetic, found no defect in Lemma
0, Theorems A, B, D, Corollary C or the rail-weight statement, in its range: 12,170 qualifying data with
chi(H) = -1 and 4,225 with +1; rings 3 to 8 for the theorems and 3 to 12 and the line for the rail weight;
9,234,733 pairs with different five-tuples, all with different statistics; 98,852 pairs with equal five-tuples,
all with equal statistics. Its control (the port (3, 1, R) for a stated start) gave 9/50, which is |alpha|^2/2.
Rerun by the director in a fresh directory: exit code, duration and digest below; result byte-identical. Two
earlier runs of the challenger failed for its own reasons (a timeout; a factor 2 in its own comparison) and
are kept in `challenger/`. Same model family as the authors; not independent review. No gate is claimed.

## Corrections accepted (the filed texts stay as written; these lines amend them)

1. The "if and only if" (Theorem B's consequence, and RAIL_WEIGHT's consequence) compares two data on the SAME
   ring size N >= 3, both with chi(H) = -1. Neither text said so.
2. RAIL_WEIGHT's consequence was silent on normalization. Theorem B assumes |alpha|^2 + |beta|^2 = 1. The
   challenger found the consequence also holds unnormalized, with n = |alpha|^2 + |beta|^2 in place of 1 in
   B1 to B3; that is computed, not proved here.
3. In the proof for the port (3, -1, L): on a ring of 4 sites the word RRR also reaches site -1, but on rail R,
   so it does not enter. The proof mentioned the coincidence at N = 4 only for the other port.
4. "Each of the five is read by a named event" says too much. The two rail weights and Re kappa are read
   directly; Re omega (B2) and the product Im omega Im kappa (B3) are read only after dividing out earlier
   readings; Im omega and Im kappa are never read separately.
5. On rings of 1 or 2 sites (excluded by the statement) the true value is
   8 P(3, 1 mod N, R) = |alpha (1 + 2u - u^2) + beta gamma (1 + u^2)|^2 with u = chi(B); it is not
   |alpha|^2/2 in 3,712 of 4,032 cases.

Not checked by the challenger: chi(H) not real; rings above 8 for the theorems; character values beyond 12th
roots; longer exhaustive masks.
exit 0 seconds 57
c658fd821bf5eefd475e7c3c2dca36eea5298f2776076a69a1c370170bc4ee0c  chal3_result.json
identical
