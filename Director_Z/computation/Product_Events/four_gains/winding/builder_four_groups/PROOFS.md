# Proofs: the exact count model, trimming, completeness of the search

Second builder, same model family as the author; not independent review. No gate is passed by anything here.
Notation as in the draft `G10_subsection_winding_products.tex`: N >= 3, M = N/gcd(N,2), masks A_1..A_T, walks from
site 0, after t steps at (t, lambda_t), site t - 2 lambda_t mod N. Profile w at a site x: w_{2j} = v_j, w_{2j+1} = u_j,
l0 the least lambda of the walks ending at x.

The earlier builder's abstract packet model (copy / merge / delete moves on a gapless cyclic list) is NOT used and
is NOT claimed equivalent: in the real dynamics adjacent occupied residues cannot be frozen independently, so the
gaps matter. It is replaced by Lemma 1, which is exact.

## Lemma 1 (exact model). PROVED.
Let n_t(e) be the number of walks of length t that pass the first t masks and have lambda_t = e. Then
n_0 = delta_0 and n_t = 1_{O_t} (n_{t-1} + S n_{t-1}), where (S n)(e) = n(e-1) and
O_t = {e in Z : t - 2e mod N in A_t}. O_t is a union of classes mod M, and every union of classes mod M is O_t for
some A_t. The profiles that occur at sites of position product events of length T >= 1 are exactly the
restrictions of the reachable n_{T-1} (T-1 >= 0) to two classes c-1, c mod M, read as
w_{2j} = n(c-1+jM), w_{2j+1} = n(c+jM), shifted by an even number of places so that the first non-zero entry has
index 0 or 1, and trailing zeros removed (non-zero restrictions only).

Proof. A walk at (t-1, e') steps to (t, e') or (t, e'+1); it survives step t iff its new site is in A_t, i.e. iff
its new point is in O_t. Summing over the two predecessors of (t, e) gives the recursion. 2M = 0 mod N, so
t - 2(e+M) = t - 2e mod N: O_t is M-periodic. The map e mod M -> t - 2e mod N is injective (t-2e = t-2e' mod N
iff N | 2(e-e') iff M | e-e'), so any union B + MZ is O_t for A_t = {t - 2b : b in B}. By the draft's proof of
thm:tp ("Sources and sinks"), u_j = n_{T-1}(l0+jM) and v_j = n_{T-1}(l0-1+jM), where x in A_T is the only
condition of the last step; so with c = l0 mod M the profile is the stated restriction; the normalisation "l0 least
lambda" is the even shift. Conversely, for a reachable n_{T-1} and a class c, the site x = T - 2c mod N with
A_T = {x} realises that restriction (any c, any T-1 >= 0). QED

## Lemma 2 (trimming; totals never increase backwards). PROVED.
If a profile w with total K = sum w occurs, then there is a run n_0 = delta_0, ..., n_{T-1} of the model of
Lemma 1 (periodic masks) with sum n_t <= sum n_{t+1} <= K for all t, and n_{T-1} supported on the two classes
c-1, c with the restriction equal to w.

Proof. Take the run of Lemma 1, masks O_t. Put E_{T-1} = (c-1+MZ) u (c+MZ) and, backwards,
E_{t-1} = {e : e in O_t n E_t or e+1 in O_t n E_t}; each E_t is M-periodic. Let m_t = 1_{E_t} n_t. For
e in O_t n E_t both e and e-1 lie in E_{t-1}, so m_{t-1} = n_{t-1} there and
m_t(e) = n_{t-1}(e) + n_{t-1}(e-1) = m_{t-1}(e) + m_{t-1}(e-1); for e not in O_t n E_t, m_t(e) = 0 (either e is
not in E_t, or n_t(e) = 0 since e is not in O_t). So m_t = 1_{O'_t}(m_{t-1} + S m_{t-1}) with O'_t = O_t n E_t,
M-periodic; m_0 = delta_0 (if 0 is not in E_0 then all m_t = 0 and w = 0, excluded). Totals:
sum m_t = sum_{e'} m_{t-1}(e') * #({e', e'+1} n O'_t) >= sum m_{t-1}, because every e' with m_{t-1}(e') > 0 is in
E_{t-1}, which by definition means at least one of e', e'+1 is in O'_t. Finally m_{T-1} = 1_{E_{T-1}} n_{T-1},
whose total is K. QED
(This is the statement the earlier builder wanted: no relevant packet is wholly deleted, so the search may be done
with totals <= K. Deletion of whole irrelevant classes is what the trimming removes.)

## Lemma 3 (completeness in width). PROVED.
Let R(K, W) be the set of configurations (up to translation in Z) reached from delta_0 by runs all of whose states
have total <= K and support width <= W. If the largest width in R(K, W) is w* < W, then every configuration reached
by a run with all totals <= K has width <= w*, and R(K, W) = R(K, infinity).

Proof. The support of 1_F(n + S n) lies in [min supp n, max supp n + 1], so the width grows by at most one per
tick. Suppose a run with totals <= K reaches a state of width > w*; take the first such state. Its predecessor and
all earlier states have width <= w* <= W, and it has width <= w* + 1 <= W; so it lies in R(K, W), contradicting the
maximality of w*. Translation invariance: shifting a configuration by 1 and the masks by 1 is again a run (masks
are arbitrary unions of classes), so configurations may be taken up to translation. QED

## Theorem A (finite range). COMPUTED, exhaustive, with completeness PROVED by Lemmas 1-3.
The profiles (1,2,3,3,2), (2,3,3,2,1) (total 11) and (1,2,3,5,1) (total 12) occur at no site of any position
product event without gains on Z_N for any N with 3 <= M <= 8 (N in {3,5,6,7,8,10,12,14,16}) -- total-11
profiles for M = 3..7 (cap 11) and M = 3..8 (cap 12), the total-12 profile for M = 3..8 (cap 12); all three satisfy
cor:tp (ii),(iii) (numerical, roots separated from the axis, smallest non-zero |Re| 6.9e-4 at 60 digits).
The program is a proof by exhaustion only for the listed M; it says nothing about M >= 9.

## Not proved
- Uniformity in M (CONJECTURED): the reachable profile set of total <= K does not depend on M for M >= M0(K).
  Evidence: equal sets for M = 4..7 at K = 11 (1144 profiles), M = 5..8 at K = 12 (1648); M = 4 at K = 12 lacks
  (1,2,8,1), (1,8,2,1) and their R-first forms, so the set does grow with M and M0(12) >= 5.
- Max gap between occupied points <= M (CONJECTURED; seen in every state, K = 11, M = 3,4,5); the naive induction
  fails (S = {0,2,5,7}, M = 4, B = {0} would give gap 8), so it needs the history.
Hence the answer NO to rem:tpprod(b) is established for 3 <= M <= 8 only; "large rings" is open.
