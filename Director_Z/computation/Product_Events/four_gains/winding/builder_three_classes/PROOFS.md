# builder_three_classes: statements and proofs (15 November 2026; nothing here is issued)

Notation of the paper (subsection "Four arc gains on rings: the winding of the walks at one vertex"): ring Z_N,
M = N/gcd(N,2), lambda = number of left steps, n(l), n_R(l), n_L(l) the numbers of walks of a position product event
S of length T ending at a vertex / at (x,R) / at (x,L) with lambda = l; C_i = beta^i <delta>; s = least j >= 1 with
beta^j in <delta>; beta^s = delta^k.  "Level" = a value of lambda at the site, levels differ by multiples of M.

## Proposition N (no one-level partner for three levels)   PROVED (from Lemma lem:windingrails)
Let S be a position product event on Z_N and x a site.  If one rail of x carries walks at three or more levels and
the other rail is not empty, then the other rail carries walks at two or more levels.
Consequently, if s >= 3: there is NO site of any position product event with m(x,R) meeting three cosets of <delta>
and m(x,L) non-empty inside one coset of <delta>, and none with the rails exchanged.  The pairs asked for in the
problem ("one side in one coset, the other spread over three classes") occur only with the one-coset side EMPTY.

Proof. Write X1: l'-l >= M implies n_L(l) n_R(l') <= n_L(l+M) n_R(l'-M); X2: l'-l >= 2M implies
n_R(l) n_L(l') <= n_R(l+M) n_L(l'-M)  (Lemma lem:windingrails).
(a) R has levels l_0 < l_0+M < l_0+2M among its levels (the levels of a vertex form a progression without gaps,
Lemma lem:winding), and L has exactly one level j, n_L(j) > 0.  If j <= l_0+M: X1 with l = j, l' = l_0+2M
(l'-l >= M) gives n_L(j) n_R(l_0+2M) <= n_L(j+M) n_R(l_0+M) = 0, because j+M is not a level of L; contradiction.
If j >= l_0+2M: X2 with l = l_0, l' = j gives n_R(l_0) n_L(j) <= n_R(l_0+M) n_L(j-M) = 0; contradiction.
(b) L has levels j_0, j_0+M, j_0+2M and R exactly one level l'.  If l' >= j_0+M: X1 with l = j_0 gives
n_L(j_0) n_R(l') <= n_L(j_0+M) n_R(l'-M) = 0.  If l' <= j_0: X2 with l = l', l' := j_0+2M gives
n_R(l') n_L(j_0+2M) <= n_R(l'+M) n_L(j_0+M) = 0.  Contradiction in both cases.
Consequence: a multiset inside one coset of <delta> sits on levels congruent modulo sM; these form a progression of
difference M without gaps, so (s >= 2) it is ONE level; a multiset meeting three cosets has >= 3 levels.  QED

## Lemma W' (a sharper form of lem:winding(ii) when an outer level is single)   PROVED
In the situation of Lemma lem:winding: if n(l) = 1 or n(l+2M) = 1, then n(l) n(l+2M) <= C(n(l+M), 2) =
n(l+M)(n(l+M)-1)/2.  In particular the one-vertex profiles (1,2,2) and (2,2,1) (hence (1,2,2,1)) do not occur,
although lem:winding(ii) allows them (2 <= 2), and (1,3,4), (1,4,7) do not occur.
Proof. The exchange of the paper sends (w,w'), lambda(w) = l, lambda(w') = l+2M, to the ORDERED pair (h,h') of distinct
walks with lambda = l+M, where tau is the least t with lambda_t(w')-lambda_t(w) = M, h = w'[0,tau] w(tau,T],
h' = w[0,tau] w'(tau,T]; it is injective, and tau is the least t with lambda_t(h)-lambda_t(h') = M.  Suppose two
pairs (w_1,w_1') != (w_2,w_2') have images with the same underlying set: (h,h') and (h',h).  Let tau_1, tau_2 be
their exchange times; tau_1 is the least t with lambda_t(h)-lambda_t(h') = M and tau_2 the least t with
lambda_t(h')-lambda_t(h) = M, so tau_1 != tau_2; say tau_1 < tau_2 (the other case is symmetric).  Then
w_1 = h'[0,tau_1] h(tau_1,T] and w_2 = h[0,tau_2] h'(tau_2,T] (exchange back).  On [0,tau_1] the walk w_1 is h' and
w_2 is h, and lambda_{tau_1}(h) != lambda_{tau_1}(h'), so w_1 != w_2.  Likewise w_1' = h[0,tau_1] h'(tau_1,T] and
w_2' = h'[0,tau_2] h(tau_2,T] differ on [0,tau_1].  So two pairs with the same unordered image share neither w nor w'.
If n(l) = 1 all pairs share w, if n(l+2M) = 1 all share w'; so (w,w') -> {h,h'} is injective.  QED
Remark (general form, PROVED by the same argument): the n(l) n(l+2M) pairs are partitioned into classes of size 1 or 2
indexed by unordered pairs of level l+M, the classes of size 2 being two pairs with no common walk; so
n(l) n(l+2M) <= C(n(l+M),2) + (number of 2-classes).
The same holds across rails (same proof with the exchange of Lemma lem:windingrails), not written out: CONJECTURED.

## Theorem A (s >= 3: the rule on multisets inside two adjacent cosets)   PROVED given the conclusion of prop:threegroups
Let D be Z_N with M >= 8, four gains in a finite abelian group, s >= 3, beta^s = delta^k.  Assume the conclusion of
Proposition prop:threegroups on this ring.  Let F_R, F_L not depend on the site, vanish at the empty multiset, and
let (eq:ppcons) hold with the factor 2.  Then F_L = F_R o T_c and F_R o T_h = F_R (h in H) on the multisets that
occur, and there are real alpha, q, c such that for every i and every m in M(C_i u C_{i+1}) (indices mod s)
   F_R(m) = alpha |m| + q (eps_i^2 + eps_{i+1}^2) + c_i eps_i eps_{i+1},   eps_j(m) = sum_n (-1)^n m(beta^j delta^n),
   j = 0..s-1,  c_i = c for 0 <= i <= s-2 and c_{s-1} = (-1)^k c (the pair C_{s-1}, C_0);  q = c = 0 if r is odd.
All these multisets occur.  For s = 3 this says: on every multiset that meets at most two cosets of <delta>, F_R is
the restriction of alpha|m| + sum over pairs {chi, chi^{-1}}, chi(delta) = -1, of gamma_chi |sigma_chi|^2, and the
two coefficients gamma_chi (r even) are determined by q and c; so a consistent rule is determined, among the
count and the squares, by its values on two-coset multisets, and what is NOT decided is only whether
   D = F_R - (alpha|m| + sum gamma_chi |sigma_chi|^2)  vanishes on the occurring multisets that meet all three cosets.

Proof.  Pairs available.  As in the proof of thm:fgtwo (prefixes, Lemma lem:fgkappa), with kappa' any element of H:
mode (ii) gives U = T_{kappa'}G_3 + T_{kappa' beta}G_1, V = T_{kappa' beta b delta/d}G_2; mode (i) gives
U = T_{kappa'}G_2, V = T_{kappa' b delta/d}(G_3 + T_beta G_1).  In the variables u = T_kappa^{-1}U,
v = T_{kappa a}^{-1}T_c V of thm:fgsolve(ii) (bc delta/(ad) = 1) these are, after translation by beta^i in H:
   (A_i)  u in M(C_i u C_{i+1}) arbitrary,  v in M(C_{i+1}) arbitrary;
   (B_i)  u in M(C_i) arbitrary,            v in M(C_i u C_{i+1}) arbitrary.
(Unlike s = 2, the pairs "u in M(C_i u C_{i+1}), v in M(C_i)" and "u in M(C_{i+1}), v two-coset" are NOT available:
they are excluded by lem:windingrails X1.)  Parts (i), (ii) of thm:fgsolve use V empty or U empty and translations:
F_L = F_R o T_c, F_R is H-invariant, and f = F_R restricted to M(Delta_N) is Delta_N-invariant and satisfies
(eq:fgQ) at the pairs (A_i), (B_i).  Fix i = 0 and write D = C_0 u C_1.
Step 1.  E_g = sum_{j<r} e_{g delta^j}.  For g in C_1, (A_0) at (u,E_g): f(u+E_g) = f(u)+f(E_g), u in M(D).  For g in
C_0, (B_0) at (E_g, v): f(E_g+v)+f(E_g+T_delta v) = 2f(E_g)+2f(v), and f(E_g+T_delta v) = f(T_delta(E_g+v)) =
f(E_g+v) by invariance; so again f(v+E_g) = f(v)+f(E_g), v in M(D).  f(E_g) = f(E_1) =: r alpha by H-invariance.
G_0 = f - alpha|.| is Delta_N-invariant, satisfies (A), (B) and G_0(u+E_g) = G_0(u) on M(D).
Step 2.  G_0(W) := G_0(W + n(E_{C_0}+E_{C_1})) extends G_0 to Z^D with T_delta-invariance; (A_0) persists for
u in Z^D, v in Z^{C_1} (apply it at u+n(E_{C_0}+E_{C_1}), v+nE_{C_1}) and (B_0) for u in Z^{C_0}, v in Z^D.
Step 3.  h in C_1: (A_0) at (W-e_h, e_h) and at (W-e_h, e_{h delta^{-1}}) have equal right sides (invariance), so
G_0(W-e_h+e_{h delta}) = G_0(W-e_h+e_{h delta^{-1}}) for all W in Z^D.  h in C_0: (B_0) at (e_h,V) and at
(e_{h delta^{-1}},V) have equal right sides; with G_0(e_h+T_delta V) = G_0(e_{h delta^{-1}}+V) the first reads
G_0(e_h+V)+G_0(e_{h delta^{-1}}+V) = RHS and the second G_0(e_{h delta^{-1}}+V)+G_0(e_{h delta^{-2}}+V) = RHS; so
G_0(e_h+V) = G_0(e_{h delta^{-2}}+V).  Hence G_0 is invariant under the lattice L generated by the E_g and the
e_{h delta^2}-e_h, h in D.
Step 4, r odd.  Modulo L, T_delta is the identity and r e_g = 0.  (A_0) reads G_0(u+v) = G_0(u)+G_0(v) for v in
Z^{C_1}, u in Z^D; (B_0) with v in Z^{C_0} gives additivity on Z^{C_0}; so G_0 is additive on Z^D and
r G_0(W) = G_0(rW) = 0.  So f = alpha|.| on M(D).
Step 5, r even.  P_g = e_g+e_{g delta}, T_delta P_g - P_g in L.  g in C_1: (A_0) at (u,P_g) gives
G_0(u+P_g) = G_0(u)+G_0(P_g).  g in C_0: (B_0) at (P_g,W): G_0(P_g+W)+G_0(P_g+T_delta W) = 2G_0(P_g)+2G_0(W) and
G_0(P_g+T_delta W) = G_0(T_delta^{-1}P_g+W) = G_0(P_g+W).  E_g is congruent to (r/2)P_g modulo L, so
(r/2)G_0(P_g) = G_0(E_g) = 0.  The P_g and L generate the kernel of eps = (eps_0,eps_1): Z^D -> Z^2, so
G_0 = gamma o eps; gamma(-s) = gamma(s) because eps o T_delta = -eps; and
   (A) gamma(s+t)+gamma(s-t) = 2gamma(s)+2gamma(t)   for s in Z^2, t = (0,t_1);
   (B) the same for s = (s_0,0), t in Z^2.
Step 6'.  (A) with s on axis 1 and (B) with t on axis 0 are the full equation on Z: gamma(0,n) = n^2 gamma(0,1),
gamma(n,0) = n^2 gamma(1,0).  phi = gamma - gamma(s_0,0) - gamma(0,s_1).  From (A) minus (A) at s_1 = 0:
phi(s_0,s_1+t_1)+phi(s_0,s_1-t_1) = 2phi(s_0,s_1): phi is affine in s_1, zero at s_1 = 0, phi = s_1 phi(s_0,1).
From (B) with t = (t_0,t_1) and evenness, gamma(t_0+s_0,t_1)+gamma(t_0-s_0,t_1) = 2gamma(s_0,0)+2gamma(t_0,t_1);
subtracting the same at t_1 = 0: phi(t_0+s_0,t_1)+phi(t_0-s_0,t_1) = 2phi(t_0,t_1): affine in the first coordinate,
zero at 0.  So phi = c_0 s_0 s_1 and gamma = q_0 s_0^2 + q_0' s_1^2 + c_0 s_0 s_1.
Gluing.  The same on every C_i u C_{i+1} with (q_i, q_i', c_i).  T_beta maps M(C_i u C_{i+1}) onto
M(C_{i+1} u C_{i+2}), eps_{j+1}(T_beta m) = eps_j(m) for j+1 <= s-1 and eps_0(T_beta m) = (-1)^k eps_{s-1}(m)
(beta^{-1} = beta^{s-1} delta^{-k}).  Invariance of f under T_beta gives q_i = q_i' = q, c_i = c for i <= s-2 and
c_{s-1} = (-1)^k c.  For s = 3 and chi(delta) = -1, chi(beta) = z, z^3 = (-1)^k: sigma_chi = eps_0+z eps_1+z^2 eps_2,
|sigma_chi|^2 = sum eps_j^2 + 2Re(z)(eps_0 eps_1+eps_1 eps_2) + 2Re(z^2) eps_0 eps_2; k even: z = 1 gives (2,2,2),
z = omega gives (-1,-1,-1); k odd: z = -1 gives (-2,-2,2), z = e^{i pi/3} gives (1,1,-1).  In both cases the two
squares span {q sum eps^2 + c(eps_0 eps_1+eps_1 eps_2+(-1)^k eps_2 eps_0)}.  QED

## What stops the rest (s = 3)
1. The route proposed in the problem is closed by Proposition N: with V in one coset and U in three classes no pair
   exists.  Every equation that contains a three-class multiset m as U+V has (levels of U, levels of V) of one of the
   shapes allowed by the lemmas, e.g. U on levels (l, l+M), V on levels (l+M, l+2M) with
   n_R(l) n_L(l+2M) <= n_R(l+M) n_L(l+M), or U on three levels and V on two.
2. No construction of such pairs for M >= 8 was made here (item (2) of the problem: NOT DONE).
3. Whether D = 0 on occurring three-class multisets: COMPUTED only, see FINDINGS (on N = 4 the search closes and
   the answer is yes to size 7 with bound 8; on N = 3 an excess of one dimension at size 4 persists at bounds 6 and 8
   in a search that is sampled beyond length 9; undecided).
