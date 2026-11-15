# builder_span1: statements and proofs (15 November 2026; nothing here is issued)

Notation of STATEMENTS.md. Deficit frame: a walk of length t with lambda left steps is at the site t-2*lambda mod N,
so two walks at one time share a site exactly when their lambda agree modulo M. A set E of residues mod M at time t
is the site mask {t-2d mod N : d in E}; a walk at deficit d continues to deficit d (step R) and d+1 (step L), and
survives exactly when the new deficit is in E modulo M. A left step multiplies the D_delta gain by delta exactly when
the previous step was a left step (the start counts as R).

## Lemma X (winding across the two rails of one site)  PROVED
S a position product event of length T on Z_N, x a site, n_R(l), n_L(l) the numbers of walks of S ending at
(x,R), (x,L) with lambda = l. For l'-l in M*Z:
 (X1) l'-l >= M  : n_L(l) n_R(l') <= n_L(l+M) n_R(l'-M);
 (X2) l'-l >= 2M : n_R(l) n_L(l') <= n_R(l+M) n_L(l'-M).
Proof. (X1) w ends at (x,L) with lambda l, w' at (x,R) with lambda l'. Phi(t)=lambda_t(w')-lambda_t(w), Phi(0)=0,
steps in {-1,0,1}. The last step of w is L and of w' is R, so Phi(T-1)=l'-l+1 >= M+1; hence the least tau with
Phi(tau)=M has 0<tau<T-1. At time tau the two sites agree (deficits differ by M). h = first tau steps of w' then
last T-tau steps of w; h' = first tau steps of w then last T-tau steps of w'. As in Lemma W both are in S, h ends
where w ends, (x,L), with lambda l+M, and h' ends at (x,R) with lambda l'-M. The map is injective as in Lemma W
(tau is the least t with lambda_t(h)-lambda_t(h')=M; exchange the tails). Count pairs.
(X2) w at (x,R), lambda l; w' at (x,L), lambda l'. Phi(T-1)=l'-1-l >= 2M-1 >= M, so tau <= T-1 < T; same exchange. QED

Corollary X.1 (the requested two-level preparation does not exist)  PROVED
With l'=l: if V_0 and U_1 are non-empty then |V_0||U_1| <= |V_1||U_0|. Counterexample to the request, on every ring:
(U_0,U_1,V_0,V_1) = (empty,{1},{1},empty). With l'=l+M: if U_0 and V_1 non-empty then |U_0||V_1| <= |U_1||V_0|;
counterexample ({1},empty,empty,{1}). (X1 with l'=l+M, resp. X2 with l'=l+2M.) So neither relation serves all requests.
What X does not exclude: any request with U_1 empty or V_0 empty (relation l'=l); these are built below.

## Proposition T (three-group preparation)  PROVED for M >= 8; COMPUTED as in FINDINGS
Let M = N/gcd(N,2) >= 8 (N = 9, 11, 13, ... or N = 16, 18, ...), delta of any order q >= 1. For every site x and all
multisets G1,G2,G3 of powers of delta (possibly empty) there are position product events S_i and S_ii in D_delta and
integers l (depending on the request) such that the walks ending at the site x are exactly
 (i)  on R: G2 with lambda = l;                         on L: G3 with lambda = l and G1 with lambda = l+M;
 (ii) on R: G3 with lambda = l and G1 with lambda=l+M;  on L: G2 with lambda = l+M;
and no walk of the event ends at any other site. Each mask has at most 5 sites.
In the language of the request: (i) is (U_0,U_1,V_0,V_1)=(G2,empty,G3,G1) with l'=l; (ii) is (G3,G1,empty,G2) with l'=l.

Construction (deficits relative to the source, residues mod M; s = deficit of the source).
Packets: the source S (one walk, gain delta^r, r=0 at the start, s=0) and stocks. Invariant at stage boundaries:
every walk's last step was R; occupied relative deficits are 0 (source) and a subset of {2,4,6}.
 ADV (4 ticks): source LLRR, each stock LRLR; masks = the positions: {1,k+1},{2,k+1},{2,k+2},{2,k+2} (k over stocks).
 DEP (3 ticks): masks {0,1,2} u stocks, {0,2} u stocks, {0,2} u stocks.
 RUN X by one (2 ticks): masks (others u {k+1}) twice, X at k.
 KILL (1 tick): mask = stocks.  IDLE/COAST: mask = occupied positions.
 MERGE X at k into k+2: masks others u {k+1}, others u {k+2}, then one IDLE.
 FINAL with P at residue p and Q at p-2: masks {p-1,p}, {p}.
Schedule: slot A (constant c_A), then RUN A to 6; slot B, RUN B to 4; slot C at 2; KILL; RUN A to M; MERGE A into 2;
mode (i): P = residue 4 (B), Q = residue 2 (C and A);   A=G1 (c=3), B=G2 (c=1), C=G3 (c=2);  l = s+4.
mode (ii): RUN B to M; P = residue 2 (C and A), Q = residue 0 (B); A=G1 (c=2), B=G2 (c=2), C=G3 (c=1); l = s+2.
Then COAST (x - T0 - 2 + 2l) mod N ticks (T0 = ticks so far), then FINAL.
Within a slot with constant c the requested exponents j are sorted by (j-c-r) mod q (r at the start of the slot) and
before each DEP the source is advanced until r+c = j mod q.

Proof. All relative deficits used lie in 0..9; for M >= 8 the residues of 0..7 are distinct, 8 is 0 or 8, 9 is 1, 0 or 9.
ADV. Stocks k in {2,4,6}. Tick 1, mask {1,3,5,7} n (k+1): refused candidates are 0 and k (even, < 8): not in the mask.
 Tick 2, mask {2} u {k+1}: refused 1 and k+2 in {4,6,8}; 8 mod M is 0 or 8, not in {2,3,5,7}. Tick 3, mask {2} u {k+2}
 inside {2,4,6,8}: refused 3 and k+1 in {3,5,7}; not in it. Tick 4, same mask: refused 3 and k+3 in {5,7,9}; 9 mod M in
 {1,0,9}; not in it. So the source follows LLRR (one L after L: gain times delta, r -> r+1), stocks follow LRLR
 (no L after L because each arrived by R); all arrive by R; all deficits +2, relative positions unchanged.
DEP. Tick 1: source to 0 and 1 (both kept); stock k stays, k+1 in {3,5,7} refused. Tick 2: from 0, 0 kept and 1 refused;
 from 1, 1 refused and 2 kept (L after L: gain delta^{r+1}); stocks stay. Tick 3: all stay; 1, 3, 5, 7 refused.
 Result: source unchanged; one new walk at 2 with gain delta^{r+1}, last step R.
RUN X from k to k+1, when no other packet is at k+1 or k+2 mod M and no two others are adjacent: tick 1, X: k refused,
 k+1 kept; another packet j stays, j+1 refused. Tick 2: X stays, k+2 refused. Gains unchanged (L after R, then R).
 Uses: A from 2 to 6 with only the source at 0 (needs 3..7 not 0 mod M); B from 2 to 4 with A at 6 and the source at 0
 (M-6 >= 2); after KILL, A from 6 to M with others at 2, 4 (residues 7..M-1, 0, 1 are free); in mode (ii) B from 4 to M
 with the other at 2 (residues 5..M-1, 0, 1 free).
KILL: source's candidates 0, 1 refused; stocks stay (odd candidates refused).
MERGE A at residue 0: tick 1 mask {1,2,4} n occupied u {1}: A to 1 (0 refused); 2, 4 stay (3, 5 refused). Tick 2 mask
 {2,4}: from 1, 1 refused, 2 kept (L after L: times delta); others stay. IDLE: all stay, all last steps R.
COAST: stays. FINAL: from p-2: p-2 refused, p-1 kept; from p: p kept, p+1 refused; then from p-1: p-1 refused, p kept
 (L after L: times delta); from p: p kept, p+1 refused. So the walks of P end on rail R, those of Q on rail L, at one
 site, and no other walk survives. Its site is T-2l mod N = x by the number of COAST ticks.
Gains. A stored walk changes gain only at MERGE and at FINAL as part of Q. With r the source exponent at its DEP:
 mode (i): G2 (P, never merged) r+1; G3 (Q) r+2; G1 (merged, Q) r+3. Mode (ii): G3 (P) r+1; G1 (merged, P) r+2;
 G2 (Q) r+2. These are the constants c; the advance rule makes r+c = j for each item (r only increases; a repeated
 exponent needs no advance; at most q-1 advances per slot).
Levels. lambda equals the unwrapped deficit. At the end the source would be at s = 2(number of ADV).
 Mode (i): B at s+4 = l, ends on R with lambda l; C at s+2, ends on L with lambda s+4 = l; A at s+M+2, ends with l+M.
 Mode (ii): C at s+2 = l (R); A at s+M+2 = l+M (R); B at s+M, ends on L with lambda s+M+2 = l+M.
Empty groups: the corresponding packet and its stages are absent; the checks above only used absence of other
packets. All groups empty: the event is empty. QED

Sub-bound rings: the construction (not the statement) fails for M in {3,5,6,7}; see FINDINGS.

## Theorem Y (second target, s = 2)  PROVED from Proposition T and Theorem thm:fgsolve's steps
Hypotheses: ring Z_N with M >= 8; four gains in a finite abelian group; s = 2 (beta not in <delta>, beta^2 in <delta>);
F_R, F_L site-independent, zero at the empty multiset; mu(Ext S) = 2 mu(S) for every position product event.
(a) For every kappa in H the equation (eq:fg) holds for all U in M(kappa Delta_N), V in M(kappa b d^{-1} Delta_N)
    such that U or V has all its gains in ONE coset of <delta>.
(b) Hence on M_R(Delta_N), M_L(Delta_N): F_R = F_L o T_b... precisely the conclusion of Theorem thm:fgsolve with
    Delta = Delta_N, K = Delta_N: F(m) = alpha |m| + sum gamma_chi |sigma_chi(m)|^2 over chi a character of Delta_N
    with chi(delta) = -1, one term per pair {chi, chi^{-1}}; none if r is odd. With beta^2 = delta^k: k even gives two
    real characters (dimension 3 with the count), k odd one conjugate pair (dimension 2).
NOT obtained: the preparation of ALL pairs. Pairs with U and V both meeting two cosets are not prepared here.
Proof of (a). Fact 0 with kappa_l = a^{T-2l}(bc)^l: in mode (i) of Prop. T the gains are kappa_l G2 on R and
kappa_l b delta d^{-1} G3, kappa_l beta b delta d^{-1} G1 on L; in mode (ii) kappa_l G3, kappa_l beta G1 on R and
kappa_l beta b delta d^{-1} G2 on L. Bookkeeping of kappa as in Prop. W2(a): given kappa' in H choose x_0, mu_0 >= 0
with kappa_0 = a^{x_0}(bc)^{mu_0} in kappa'<delta>, take x = x_0 mod N; then T-2l = x_0+Ni; the prefix LR (masks
{N-1},{0}) and the prefix R^N (masks {1},..,{N-1},{0}) are single walks of gain 1 from (0,R) to (0,R) for N >= 3,
add 1 resp. 0 to lambda of every walk (so the two levels still differ by M) and multiply kappa_l by bc resp. a^N;
suitable numbers give kappa_l = kappa_0. Since beta in H, kappa' may be kappa or kappa*beta (times <delta>), and
beta^2 in <delta>. Mode (ii) with kappa' = kappa gives U arbitrary in M(kappa Delta_N), V arbitrary in
M(kappa beta b d^{-1}<delta>); with kappa' = kappa beta: U arbitrary (G3 in kappa beta<delta>, G1 in kappa<delta>),
V in M(kappa b d^{-1}<delta>). Mode (i) likewise gives U in one coset (either) and V arbitrary. The requested
D_delta multisets are the translates by kappa_0^{-1} etc. Lemma lem:fgonesite gives (eq:fg).
Proof of (b). Follow the proof of Theorem thm:fgsolve. (i) uses only V empty and U empty. (ii): (eq:fgQ) holds for
u, v in M(Delta_N) with u or v supported on one coset of <delta> (call this R-eq). (iii) Step 1 uses v=E_g (one
coset). Step 2: adding n*1 to u and nE_g to a one-coset v keeps R-eq, so it extends to Z^G. Step 3 uses R-eq at
(W-e_g, e_g) and (e_g, W-e_g). Step 4 (r odd): R-eq becomes G_0(u+v)=G_0(u)+G_0(v) for one-coset v, hence additivity,
and rG_0=0. Step 5 uses v=P_g. So G_0 = gamma o eps with D' = Z^2, coordinates (s_0,s_1) for the two cosets, and
 gamma(s+t)+gamma(s-t) = 2 gamma(s)+2 gamma(t)  for all s and all t on one axis.
Replacement for Step 6: on each axis gamma is n^2 gamma(1) (the full equation holds there). Put
phi(s_0,s_1)=gamma(s_0,s_1)-gamma(s_0,0)-gamma(0,s_1). For t=(t_0,0): phi(s_0+t_0,s_1)+phi(s_0-t_0,s_1)=2phi(s_0,s_1),
so phi is affine in s_0, and zero at s_0=0: phi = s_0 B(s_1). Likewise affine in s_1 and zero at s_1=0. So
phi = c s_0 s_1 and gamma is a quadratic form. Step 7 as written. QED
Remark: only two adjacent levels and three groups are used, consistent with Lemma W and Lemma X.
