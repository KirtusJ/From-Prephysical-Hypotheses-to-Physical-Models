# FINDINGS - two-rail starts (builder; same model family as the director; not independent review; no gate claimed)

Setting as in CRITERION.md. Start alpha|0,R> + beta|0,L>. u=chi(B), eta=chi(H), omega=u^D, gamma=chi(c/a),
kappa = conj(alpha) beta gamma, s=(-1)^(D-1).

LEMMA 0 (word gain from rail L). PROVED. For steps w=s_1..s_t taken from start rail L,
 G_L(w) = (c/a) a^t (a/c)^e B^l H^m, l = number of left steps of w, m = number of LL arcs counting (L,s_1), e as before.
Proof. The word Lw from a sharp R start has gain b*G_L(w) (its first arc is RL=b, the others are the arcs of w from L).
By identity (1) it equals a^(t+1) (a/c)^e B^(l+1) H^m, its LL arcs being exactly those of w from L. Divide by b:
a B / b = c/a. QED.

THEOREM A (invariance). PROVED. Hypotheses: N>=1; abelian A, gains a,b,c,d; chi unitary with eta real; alpha, beta
complex (normalisation not used). For every mask event and port (t,x,rail):
 2^t P = |alpha|^2 |S_R|^2 + |beta|^2 |S_L|^2 + 2 Re kappa * Re T - 2 Im kappa * Im T,
 S_R = sum_k cR_k omega^k, S_L = sum_k cL_k omega^k, T = conj(S_R) S_L, with real cR_k, cL_k depending only on the
 event, the port and eta. Consequently P depends on (alpha,beta,chi,carrier) only through
   Q = ( |alpha|^2, |beta|^2, eta, Re omega, Re kappa, Im omega * Im kappa ).
Proof. Words at the port have t-2l = x mod N from either start rail (both start at site 0), so l = l_0 + kD with the
same l_0. By (1) and Lemma 0 the amplitude is 2^(-t/2) chi(a)^t chi(a/c)^e u^(l_0) [alpha S_R + beta gamma S_L],
cR_k (cL_k) = sum of eta^m over admitted words from R (from L) with winding k. The prefactor has modulus 1. Expand
|alpha S_R + beta gamma S_L|^2. |S_R|^2, |S_L|^2, Re T are real Laurent polynomials invariant under omega -> 1/omega,
hence polynomials in Re omega; Im T = sum t_k sin(k theta) = Im omega * (polynomial in Re omega) (Chebyshev U).
So P is a function of Q. QED.
Line (Z instead of Z/N): no k; T real; P depends only on (|alpha|^2,|beta|^2,eta,Re kappa). PROVED, same lines.

THEOREM B (each item is read). PROVED. Hypotheses: N>=3, eta=-1, alpha,beta with |alpha|^2+|beta|^2=1.
(B1) tick 1, well 1 (= port (1,R)):  P = 1/2 + Re kappa.   (well -1: 1/2 - Re kappa.)  [B1 holds for any eta at (1,R).]
(B2) retain well 1 at tick 1, then the fork of Prop 2(b) translated by one site and one tick, read well D+2:
       P = (1/2 + Re kappa) * 2^-(D+1) (2 + 2 s Re omega);
     retain well -1 at tick 1, then the mirror fork (wells -1-j, -1+j at ticks 1+j, j<D; well -1-D; read well -D-2):
       P = (1/2 - Re kappa) * 2^-(D+1) (2 + 2 s Re omega).  One of the two prefactors is nonzero.
(B3) the fork of Prop 2(b) itself, from the two-rail start:
       P = 2^-(D+1) [ 2 + 2 s (|alpha|^2-|beta|^2) Re omega + 4 s Im omega Im kappa ].
Hence for a fixed known (|alpha|^2,|beta|^2): two data have the same statistics on all events IFF they have the same
(Re omega, Re kappa, Im omega*Im kappa); equivalently iff (omega,kappa) agree, or are jointly conjugate, or
omega=omega' real and Re kappa = Re kappa'.
Proof. (B1) words: right step from R (gain a), from L (gain c): amplitude chi(a)(alpha+beta gamma)/sqrt2. At (-1,L):
chi(b)(alpha + beta chi(d/b))/sqrt2 and d/b = H c/a, so alpha - beta gamma. For N>=3 wells 1 and -1 differ.
(B2) after the mask the state is one rail at one site; the rest is the sharp-start event, by linearity and
translation. For the sharp L start, Lemma 0: admitted words L^(D+1) (l=D+1,m=D+1) and R^D L (l=1,m=0), ratio
omega eta^(D+1) = s omega; |1+s omega|^2 = 2+2s Re omega. (B3) masks act on sites only, so from either rail the
admitted step sequences are R^(D+1) and L^D R (Prop 2(b) enumeration, N>=3). From R: (k,m)=(0,0),(1,D-1); from L:
(0,0),(1,D). S_R = 1+s omega, S_L = 1-s omega, T = (1+s conj omega)(1-s omega) = -2 i s Im omega. Insert in Thm A.
"IFF": (<=) Theorem A. (=>) B1 gives Re kappa, B2 gives Re omega, then B3 gives Im omega Im kappa. Last sentence:
Re omega equal => omega' in {omega, conj omega}; if Im omega != 0 the product fixes Im kappa' = +-Im kappa
accordingly; if Im omega = 0 the product is 0 for both. QED.

COROLLARY C (conjugation, Q2). PROVED (N>=3, eta=-1, normalised start). chi and conj chi have the same statistics
on every event IFF  Im(conj(alpha) beta) = 0  or  (gamma = +-1 and omega = +-1).
So with a real relative amplitude (including the equal superposition and a sharp start) conjugation stays
unreadable. With conj(alpha)beta = r e^(i phi), r sin phi != 0, it is read: if gamma=e^(i theta) is not real by B1,
P = 1/2 + r cos(phi+theta) against 1/2 + r cos(phi-theta); if gamma=+-1 and Im omega != 0 by B3, the two values
differ by 2^-(D+1) * 8 r |sin phi| |Im omega|.
Proof. conj chi has (conj omega, conj(alpha)beta conj gamma). Equal Re kappa iff r sin phi sin theta = 0; equal
third invariant iff r Im omega sin phi cos theta = 0. Both iff r sin phi = 0 or (sin theta = 0 and Im omega = 0). QED.
Caveat: "known phase" means known relative to the rails' phase convention in which the gains are named.

THEOREM D (preparation, Q3). PROVED (eta real, N>=1; also the line). From a sharp start (0,R), after any mask
sequence, the state at a single site x at tick t is
   (psi_R, psi_L) = 2^(-t/2) chi(a)^t u^(l_0) ( p(omega), conj(gamma) q(omega) ),
p, q real Laurent polynomials fixed by the event and eta. Used as a new start it has effective
   kappa' = conj(psi_R) psi_L gamma = 2^-t conj(p(omega)) q(omega),
in which gamma has cancelled; |psi_R|^2, |psi_L|^2, kappa' are functions of (eta, omega) alone, and are conjugated
by omega -> conj omega. So every state reachable by steps and masks carries the compensating phase conj chi(c/a),
and events continued from it read only (eta, Re omega): this is Prop 1 seen from the inside.
Reachable set: exactly the pairs (p, conj(gamma) q) up to a common factor, (p,q) the pair of port sums of an event.
Examples: tick 2, site 0 (N>=3): (1, conj gamma)/2, kappa' = 1/4. Tick D, site D (N>=3; R^D and L^D):
(1, conj(gamma) eta^(D-1) omega) 2^(-D/2), kappa' non-real when omega is non-real.
Proof. Identity (1): e=0 on rail R, e=1 on rail L gives the factor chi(a/c) = conj gamma on psi_L; the rest as in
Prop 1. QED.
Consequence: the follow-up's example needs a rail superposition whose relative phase is NOT locked to chi(c/a),
i.e. one prepared by something other than the walk's steps and position masks. No such preparation is given here.

COMPUTED (rails.py, result_v2.json; N=3..8, groups = products of 1..3 cyclic groups of orders in {2,3,4,6,12},
random gains and character, 12 starts in Z[zeta_12]; 549 drawn, 260 qualify (eta=+1: 183, eta=-1: 77); 16 events/N):
| predicate | checked | failed |
| P1 equal Q => equal statistics (eta=+-1) | 3629 pairs | 0 |
| P2 eta=-1, same |alpha|^2,|beta|^2, different Q => different statistics | 4981 pairs | 0 |
| P3a B1 formula | 1560 | 0 |
| P3b B3 formula | 462 | 0 |
| P3c, P3d B2 formulas | 462, 462 | 0 |
| P4 Corollary C both directions | 462 (342 unreadable side, 120 readable side) | 0 |
| P5 Theorem D | 130260 site-states (230 distinct non-real kappa') | 0 |
Controls meant to fail: C1 "only (eta,Re omega,Re kappa)": 8 counterexample pairs of 3696. C2 "gamma itself is read":
3289 of 6650 equal-statistics pairs have different gamma. C3 "omega itself is read": 328 of 6650.

FAILED / REPLACED
F-a. Conjecture "statistics read the phase chi(c/a)+arg(conj(alpha)beta)": replaced by Re kappa and Im omega*Im kappa.
     When omega = +-1 (and on the line) Im kappa is not read at all.
F-b. "(eta, Re omega, Re kappa) suffice": false (C1), e.g. the fork B3.
F-c. "a two-rail start reads all of chi(B)": false (C3); still only omega = chi(B)^D, and of it Re omega plus the
     sign correlation with Im kappa.
F-d. Run 1 crashed (helper bug), no predicate evaluated; rails_v1_crashed.py, result_v1.json (empty) kept.

NOT DONE / CONJECTURED
- Whether |alpha|^2 is itself readable (Theorem B takes it as known). Not addressed.
- eta not real; N=1,2 for Theorem B; Lean (the algebra is (1+s conj w)(1-s w) = -2 i s Im w for |w|=1, s=+-1).
- Theorem B "IFF" across different carriers uses Theorem A as stated (it never uses that the two data share a group).
