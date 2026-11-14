# Position product events with four arc gains in any finite abelian group

Builder report of 14 November 2026, written into the repository by the director from the builder's hand-back
(the builder's own file write was refused by its tool, and it did not go around the refusal). The text below is
the builder's, shortened only in layout. Same model family as the director: this is not independent review.
Mathematics about a model only; nothing here bears on any gate. Not in the paper yet.

Outcome: the two position-product theorems of paper G10 (`thm:posprod`, `thm:posprodq`) become one theorem for
any finite abelian group A and any four arc gains. The answer depends on the gains only through
delta = ad/(bc). The conjecture in the brief is false when H = <a, d, bc> is not all of A, and the brief's
preparation hypothesis (all pairs in N^A x N^A) is impossible unless delta generates A. Both are replaced.

## Control

C = Z/4: exactly one character has 1 + psi(h) = 0, namely psi(h^j) = (-1)^j. sigma_psi(2,1,0,1) = 0.

## Notation

- Arcs: (x,R)->(x+1,R) gain a; (x,R)->(x-1,L) gain b; (x,L)->(x+1,R) gain c; (x,L)->(x-1,L) gain d.
- delta = ad(bc)^-1, r = ord(delta), H = <a, d, bc> (contains delta).
- M(X) = multisets supported in X; T_g = translation by g.
- N_G = characters chi of G with chi(delta) = -1 (the condition chi(ad) = -chi(bc)); empty for r odd.
- Delta_N = <delta, (a/d)^(N/gcd(N,2))> for the ring Z_N.

## G1. The equation, and what can be prepared

**Lemma 1 (one site). PROVED.** Let F_R, F_L be site-independent and let S be a position product event with
m_S(x,R) = U, m_S(x,L) = V. Consistency with factor 2 gives

    (E4)  F_R(T_a U + T_c V) + F_L(T_b U + T_d V) = 2 F_R(U) + 2 F_L(V).

Proof: as the paper's one-site lemma. Take S' = walks of S ending at site x. A walk at (x,R) with gain g
continues with gains ga and gb; one at (x,L) with gc and gd. The two targets differ in rail. With
site-dependent functions and factor k the same proof gives
F_(x+1,R)(T_a U + T_c V) + F_(x-1,L)(T_b U + T_d V) = k F_(x,R)(U) + k F_(x,L)(V).
The functions must be allowed to depend on the rail: V = 0 gives F_R(T_a U) + F_L(T_b U) = 2 F_R(U), not
F_L = F_R. The true relation is F_L = F_R o T_c (Theorem 2(1)).

**Lemma 0 (cosets). PROVED.** On the line, a walk of length T from (0,R) to site x has rho = (T+x)/2 right
steps and lam = (T-x)/2 left steps. Its gain is a^rho d^lam delta^(-n) if it ends on R, and
a^rho d^(lam-1) b delta^(-n) if it ends on L, with n the number of LR arcs. So at one length the gains at (x,R)
lie in one coset kappa<delta>, and those at (x,L) in kappa b d^-1 <delta>, with the same kappa = a^rho d^lam
in H. On the ring Z_N the same holds with Delta_N in place of <delta>.

Proof: the rail after a step is R iff the step is to the right, so n_RR + n_LR = rho and n_RL + n_LL = lam.
Rail changes alternate starting with RL, so n_RL = n_LR (end R) or n_LR + 1 (end L). Substitute. On the ring
rho is fixed only modulo N' = N/gcd(N,2), and (rho + N'j, lam - N'j) multiplies the gain by (a/d)^(N'j).

**Consequence. PROVED.** "Every (U,V) in N^A x N^A occurs at one site" is false on the line unless
<delta> = A. Values of F on multisets not supported in one coset never enter mu.

**PREP(Delta). HYPOTHESIS, not claimed.** Delta is a subgroup containing delta. For every kappa in H,
U in M(kappa Delta), V in M(kappa b d^-1 Delta) there are a site x and a position product event S with
m_S(x,R) = U, m_S(x,L) = V. Line: Delta = <delta>. Ring: Delta = Delta_N. These are the largest families Lemma 0
allows. The proof uses exactly: (i) pairs (U,0) and (0,V) for all kappa in H; (ii) all pairs for kappa = 1.
For a = b = c = 1 this is the paper's preparation hypothesis. For four gains nothing is known about its truth.

## G2. Solution

Domains: MR(Delta) = union over kappa in H of M(kappa Delta); ML(Delta) = union of M(kappa b Delta).
Delta = A is the full equation on N^A.

**Theorem 2. PROVED.** Let delta be in Delta <= A, K = H cap Delta. Let F_R on MR(Delta) and F_L on ML(Delta)
vanish at 0 and satisfy (E4) for all kappa in H, U in M(kappa Delta), V in M(kappa b d^-1 Delta). Then:

1. F_R o T_h = F_R for h in H, and F_L = F_R o T_c.
2. f = F_R restricted to M(Delta) is K-invariant and satisfies
   (Q) f(u+v) + f(u + T_delta v) = 2 f(u) + 2 f(v) on M(Delta).
   The map (F_R, F_L) -> f is a linear bijection onto such f, with inverse F_R(m) = f(T_kappa^-1 m) for
   m in M(kappa Delta), and F_L = F_R o T_c.
3. Those f are exactly the real-valued combinations of sigma_omega (omega a character of Delta trivial on K)
   and of sigma_chi sigma_chi' (unordered pairs in N_Delta with chi chi' = 1 on K, chi = chi' allowed). These
   are independent, so

       dim = |Delta/K| + #{unordered {chi, chi'} in N_Delta : chi chi' = 1 on K}.

   There are no solutions of degree 3 or more and no non-polynomial ones.
4. Every such f gives a solution.

In (F_R, F_L) form with Delta = A: F_R = q sigma_chi sigma_chi', F_L = q (chi chi')(c) sigma_chi sigma_chi';
linear F_R = l sigma_omega, F_L = l omega(c) sigma_omega. The count and the squares |sigma_chi|^2 have the same
coefficient on both rails.

**Proof of 1.** The domains are closed under the four translations used. (E4) at V = 0, and at U = 0 with
V = m, gives F_R(T_a m) + F_L(T_b m) = 2 F_R(m) and F_R(T_c m) + F_L(T_d m) = 2 F_L(m). Fix m0. Let
Omega = {(R, T_h m0)} union {(L, T_(hb) m0)}, h in H; it is finite. Put phi = F on it, with
alpha(R,m) = (R, T_a m), beta(R,m) = (L, T_b m), alpha(L,m) = (R, T_c m), beta(L,m) = (L, T_d m). Then
phi = (phi o alpha + phi o beta)/2. So the set where phi is maximal is closed under alpha and beta. From (R,m)
one reaches (R, T_a m), (R, T_(bc) m) by beta-alpha, and (R, T_(bdc) m) by beta-beta-alpha. The elements a, bc,
bdc have finite order and generate H, so all of Omega is reached; from (L,m) one alpha leads to rail R. Hence
phi is constant: F_R(T_h m0) = F_R(m0) = F_L(T_b m0), so F_L(m) = F_R(T_(b^-1) m) = F_R(T_c m).

**Proof of 2 and 4.** Put u = T_(kappa^-1) U and v = T_((kappa a)^-1) T_c V. Both lie in M(Delta), since
kappa bc d^-1 = kappa a delta^-1. Then T_a U + T_c V = T_(kappa a)(u+v) and
T_b U + T_d V = T_(kappa b)(u + T_delta v). By 1, (E4) at (U,V) is (Q) at (u,v), and every (u,v) arises at
kappa = 1. Conversely F_R is well defined, because a non-empty m in M(kappa Delta) and M(kappa' Delta) has
kappa'/kappa in K. Read the computation backwards.

**Proof of 3.** Write G = Delta.
- Step 1. E_g = sum_{j<r} e_(g delta^j) is T_delta-invariant, so (Q) gives f(u + E_g) = f(u) + f(E_g). Put
  l(m) = (1/r) sum_g m(g) f(E_g). It is additive and K-invariant, hence satisfies (Q), and l(E_g) = f(E_g). So
  G0 = f - l satisfies (Q), is K-invariant, and G0(u + E_g) = G0(u).
- Step 2. The all-ones multiset 1 is a sum of E_g, so G0 extends to Z^G by G0(W) = G0(W + n1). (Q) and
  invariance persist because T_g 1 = 1.
- Step 3. Symmetry of (Q) gives G0(u + T_delta v) = G0(v + T_delta u). Replacing v by T_delta v gives
  G0(u + T_delta^2 v) = G0(u+v). So G0 is constant on cosets of L = <E_g, e_(g delta^2) - e_g>.
- Step 4, r odd. Then e_(g delta^j) = e_g mod L, T_delta W = W mod L, and r e_g = 0 mod L. (Q) becomes
  additivity, and r G0(W) = G0(rW) = 0. So G0 = 0 and f = l.
- Step 5, r even. P_g = e_g + e_(g delta) has T_delta P_g = P_g mod L, so G0(U + P_g) = G0(U) + G0(P_g).
  Since (r/2) P_g = E_g = 0 mod L, G0(P_g) = 0. Let eps(W)(g) = sum_j (-1)^j W(g delta^j). It maps onto
  D = {w : w(g delta) = -w(g)}, which is free of rank |G|/r, and its kernel is L + <P_g>: modulo L,
  W = sum_C (P_C e_(g_C) + Q_C e_(g_C delta)), and eps(W) = 0 gives P_C = Q_C. So G0 = g o eps. As
  T_delta = -1 on D, (Q) becomes g(s+t) + g(s-t) = 2 g(s) + 2 g(t) on D, with g K-invariant.
- Step 6. g is even. Put B(s,t) = (g(s+t) - g(s-t))/2. Two uses of the law give
  2B(s,t) + 2B(s',t) = B(s+s', 2t); with s' = 0, 2B(s,t) = B(s,2t). So B is additive in s, symmetric, and
  B(s,s) = 2 g(s). Hence g is a quadratic form. The converse is immediate.
- Step 7. l and g o eps are determined by f, since f(nm) = n l(m) + n^2 g(eps m). K-invariant additive
  functions have dimension |G/K|. For chi in N_G, sigma_chi(eps(e_x)) = r chi(x), so the |G|/r functionals
  sigma_chi form a basis of the dual of D tensor C. T_k multiplies sigma_chi sigma_chi' by (chi chi')(k), so
  the invariant forms are spanned by monomials with chi chi' = 1 on K. The real dimension equals the complex
  one.

**Corollary 3 (full equation, Delta = A). PROVED.**
dim = |A/H| + #{unordered {chi, chi'} in N_A : chi chi' = 1 on H}. The brief's conjecture
(1 + number of classes {chi, conj chi} in N_A) holds iff H = A. Counterexamples, kept:
- Z/2, a = d = 1, b = c = h: dimension 2, not 1. The extra solution is F_R = m(1) - m(h), F_L = -F_R.
- Z/4, a = h^2, b = c = d = 1: dimension 5, not 2.

**Corollary 4 (line). PROVED under HYPOTHESIS PREP(<delta>).** For every A and all four gains, on occurring
multisets F_R = F_L = alpha |m| for r odd, and alpha |m| + gamma |sigma_chi(m)|^2 for r even. chi may be any
character of A with chi(delta) = -1; all give the same function there, the squared alternating sum along the
coset. Dimension 1 + [r even]. Every linear and mixed solution of Corollary 3 collapses to these on the walk.

**Corollary 5 (rings). PROVED under HYPOTHESIS PREP(Delta_N).**
dim = 1 + #classes {chi, chi^-1} of characters of Delta_N with chi(delta) = -1; the solutions are the count and
the squares.

**Theorem 6 (converse on all events). PROVED, no hypothesis.** On the line and on every ring, the solutions of
Theorem 2 placed at every site satisfy mu(Ext S) = 2 mu(S) for every event of every length, zero included.
Proof: Lemma 0 puts (U_x, V_x) in the domain with one kappa; sum (E4) over x.

## G3. The paper's cases

- PROVED. a = b = c = 1, d = h, A = <h>: delta = h and H = A = <delta>, so Corollaries 3 and 4 coincide and
  give the paper's proposition for one gain of order q and part (i) of its theorem; q = 2 gives the signed
  walk. Theorem 6 gives the converse parts.
- The reduction in Theorem 2(2) shows the four-gain equation is the paper's one-gain equation with h replaced
  by delta, plus K-invariance.
- Agreement with the theorem on periodic carriers. PROVED by a short argument that deserves a challenger. On
  rings where that theorem applies (N >= 3, derived digraph strongly connected), C_0 = Delta_N. One inclusion:
  a closed walk of length divisible by the period has gain equal to a quotient of gains of two closed walks of
  one length (semigroup-difference argument using the finite order of A), which lies in Delta_N by Lemma 0.
  The other: delta and (a/d)^(N') are such quotients. U(D) = {chi : chi(delta) = -1}, so that theorem's
  dimension equals Corollary 5's, with the same functions. Without PREP only "all events implies product
  events" and Theorem 6 are available.

## G4. Mixed forms. PROVED and COMPUTED

- Full equation: the pair (qR, qL) times sigma_chi sigma_chi' is a non-zero solution iff chi, chi' are in N_A
  and chi chi' = 1 on H; then qL = (chi chi')(c) qR.
- So Re(c0 sigma_chi conj sigma_lam), for two different norm-preserving chi and lam, is a solution iff
  chi = lam on H, with rail phase (chi conj lam)(c). This never happens when H = A, and does happen when H is
  smaller.
- On the walk, for m in M(kappa<delta>): sigma_chi conj sigma_lam = (chi conj lam)(kappa) eps(m)^2. This is
  the square itself if chi = lam on H. Otherwise it is consistent only as the zero rule, since the coefficient
  must be constant in kappa and sums to zero over H.

## Computation

`four_gain.py`: predicates P1 to P9 in the docstring before the first run, seed 20261113, exact ranks in F_p
with p = 2147483629, lower bound over Q from the explicit solutions, result file opened so that it is never
overwritten. First run exit code 0 with 0 failed predicates; no predicate was edited. Rerun in a fresh
directory: exit code 0, byte-identical.

Full equation, dimension found against formula; "H = A" is the number of cases where the brief's conjecture is
right:

| Group | Cases | Found = formula | H = A | Largest box n |
|---|---|---|---|---|
| Z2 | 16 (all) | 16 | 14 | 5 |
| Z3 | 81 (all) | 81 | 78 | 4 |
| Z4 | 256 (all) | 256 | 224 | 3 (4 on 40) |
| Z2xZ2 | 256 (all) | 256 | 168 | 3 (4 on 40) |
| Z6 | 120 sampled | 120 | 101 | 3 (4 on 8) |
| Z2xZ4 | 60 sampled | 60 | 48 | 3 |

- The brief's conjecture equals the found dimension in exactly the H = A cases and in no other (P1c, 789 of
  789).
- Largest gaps between found dimension and conjecture: Z6 with r = 2, |H| = 2 gives 9 against 3; Z2xZ4 with
  r = 2, |H| = 4 gives 8 against 3; Z4 and Z2xZ2 with r = 2, |H| = 2 give 5 against 2 and 3.
- Stable in box size: the box nullity equals the projected rank at every n from 2 up, and P9 passes 908 of
  908.
- Line problem (P2): dimension 1 + [r even] in 789 of 789. Ring-like Delta = <delta, (a/d)^k>, k = 1 and 3
  (P3): formula holds in 789 of 789 each.
- P4: 17,145 ordered character pairs, 0 fail. P5: 3,503 characters, 0 fail.
- P6 (Lemma 0, line, T <= 12): 52,572 vertex-length instances, 0 outside the predicted coset.
- P7 (rings N = 3 to 7, T <= 14): 163,108 instances, 0 outside one coset.
- P8 (converse on random events): 16,176 events, 0 fail.
- Limits: for r = 6 the line box (n <= 4) does not contain a full delta-orbit multiset; Z6 and Z2xZ4 are
  samples; only k = 1 and 3 for the ring-like case.

## Status

- PROVED: Lemma 1, Lemma 0, the impossibility of full preparation, Theorem 2, Corollary 3 with its
  counterexamples, Theorem 6, G3, G4.
- PROVED under hypothesis PREP (not claimed): Corollaries 4 and 5.
- COMPUTED: the table above, to the ranges stated.
- CONJECTURED: nothing.
- FAILED or not done: the brief's conjecture for H != A; the brief's form of the preparation hypothesis; PREP
  for four gains, neither proved nor tested; site-dependent functions and unknown factor k; non-abelian A; no
  Lean file (Steps 3 and 6 of the proof of Theorem 2(3) are the natural candidates).

Digests as reported by the builder: `four_gain.py` 65cf0961...049823a; result 5657f0a5...2b2428af.
