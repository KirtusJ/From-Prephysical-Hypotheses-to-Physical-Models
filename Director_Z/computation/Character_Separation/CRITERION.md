# When a ring measurement separates two norm-preserving characters

Builder report. Same model family as the director; this is not independent review. No gate is claimed.
All probabilities are the note's model predictions (squared terminal-port law per original sharp launch).

## Setting (the note's definitions, in the form the proofs use)

Start (0,R). A right step goes to (x+1,R), a left step to (x-1,L), sites in Z/N (or Z for the line).
Arc gains RR=a, RL=b, LR=c, LL=d in an abelian group A. B = bc/a^2, H = ad/(bc). D = N/gcd(N,2).
Word gain (the note's identity (1)): G(w) = a^t (a/c)^e B^l H^m, with l = number of left steps,
m = number of LL arcs, e = 1 if the final rail is L, else 0.
Event: masks S_1..S_t (sets of wells retained at ticks 1..t). A word is admitted when its site at tick j is in S_j.
Port probability at (t,x,rail): P_chi = 2^-t |sum_w chi(G(w))|^2 over admitted words ending there.
Well probability: the sum over the two rails. A general final mask is a sum of well probabilities.
chi is a unitary character of A. "Norm-preserving" means chi(H) = -1.
Write beta = chi(B), omega = chi(B^D) = beta^D.

## Control (known answer) - reproduced

control.py, brute enumeration of the 256 words with individual arc gains, ring of 7, 8 ticks, port (1,R):
fork 1/64 (chi_0), 1/256 (chi_1), fair count 1/128; singleton reference 1/256, 1/256, 1/256.
Also the review's numbers: N=9 gives 1/256 and 1/256; N=8 gives 0 and 3/32; C2xC4, chi(g)=i gives 1/128.
File control_result.json.

## Proposition 1 (what the ring adds: one real number). PROVED

Hypotheses: N >= 1; any abelian A and gains a,b,c,d; chi_0, chi_1 unitary characters with
chi_0(H) = chi_1(H) = eta, eta real (so eta = -1 in the norm-preserving case, and the proof also covers eta = 1);
omega_i = chi_i(B^D).
Claim: if Re omega_0 = Re omega_1 (equivalently omega_1 = omega_0 or omega_1 = conj omega_0), then every port
probability and every well probability of every event on the ring of N sites is the same for chi_0 and chi_1.

Proof. Fix an event and a port (t,x,rail). A word ending at x has x = t - 2l mod N, so 2l is fixed mod N and l is
fixed mod D. Choose l_0 in that class and write l = l_0 + kD, k an integer depending on the word. The rail fixes e.
By (1), chi(G(w)) = chi(a)^t chi(a/c)^e beta^(l_0) * omega^k eta^m. The first three factors are the same for all
words at the port and have modulus 1. Hence
  P_chi = 2^-t | sum_k c_k omega^k |^2,   c_k = sum over admitted words at the port with winding k of eta^m.
The c_k are real (integers when eta = +-1) and depend on the event and on eta only. So P_chi is a function of
omega alone; and since the c_k are real, replacing omega by conj omega conjugates the sum and leaves the modulus.
Well probabilities and general final masks are sums of port probabilities. QED.

Remark (weaker hypothesis, PROVED by the same lines): for eta not real the same argument gives equality when
(eta, omega) agree or are jointly conjugate. Not computed.
Remark: on the line there is no k, so P depends on eta only (the note's statement). The ring adds exactly Re omega.

## Proposition 2 (the criterion). PROVED

Hypotheses: as above with eta = -1 (norm-preserving), N >= 3 for well events, N >= 1 for rail-resolved ports.
(a) No port or well event of length t <= D separates any two norm-preserving characters.
(b) The fork of length D+1 (retain wells +j and -j mod N at ticks 1 <= j < D, well D mod N at tick D, read well
    D+1 mod N at tick D+1) has probability
        P_chi = 2^-(D+1) * (2 + 2 (-1)^(D-1) Re omega)          (N >= 3).
(c) Hence, for N >= 3: chi_0 and chi_1 are separated by some position-mask event on the ring of N sites
    if and only if Re chi_0(B^D) != Re chi_1(B^D); when they are, the fork separates them, and D+1 is the
    least length of any separating event.
(d) N = 1, 2 (D = 1): no well event separates any pair (every well probability is 0 or 1). With the terminal rail
    resolved, the unmasked port (2, 2 mod N, R) has P = (1 + Re beta)/2 and separates iff Re beta differ.

Proof. (a) At a port with t <= D the left counts lie in [0,t] and in one class mod D. Two different values need
{0, D} with t = D, i.e. the words R^D and L^D, which end on different rails. So all words at one port have the
same k, the factor omega^k leaves the modulus, and P = 2^-t |sum (-1)^m|^2 for every chi.
(b) By the note's enumeration (its paragraph "A physically named positive comparison", valid for D >= 2) exactly
R^(D+1) and L^D R are admitted, both at ((D+1) mod N, R). They have (l,m) = (0,0) and (D,D-1), so k = 0 and 1 and
P = 2^-(D+1) |1 + (-1)^(D-1) omega|^2 = 2^-(D+1) (2 + 2(-1)^(D-1) Re omega), using |omega| = 1. The L rail of that
well is empty, so the well probability is the port probability.
(c) "Only if" is Proposition 1. "If" is (b): the fork probabilities differ exactly when Re omega differ. Minimality
is (a).
(d) On N <= 2 all words at tick t are in the same well, so a mask keeps everything or nothing; the two local
columns are orthonormal when chi(H) = -1, so the total is 1 while anything is kept. For the port: words RR and LR,
(l,m) = (0,0),(1,0), P = |1 + beta|^2/4. Then use Proposition 1 with D = 1. QED.

Corollary (fair count). PROVED. The fork rate equals the fair count 2^-D iff Re omega = 0. (C2xC4, chi(g) = i,
N = 7: omega = -i; this is the review's failed predicate P9, kept, now explained.)

Corollary (the note's group, a=c=1, b=g, d=zg, g of order 3; chi_r(g) = exp(2 pi i r/3)). PROVED.
chi_1 and chi_2 are separated on no ring. chi_0 is separated from chi_1 (and from chi_2) on the ring of N sites
iff 3 does not divide N. In general, for B of order q: chi and chi' are inseparable on the ring of N sites iff
(chi/chi')(B^D) = 1 or (chi chi')(B^D) = 1.

## Proposition 3 (what a set of rings determines). PROVED

For unit complex numbers beta, beta':
(a) If Re beta^D = Re beta'^D for D = 2, 3 and 5 then beta' = beta or beta' = conj beta.
(b) For any two D_1, D_2 >= 2 there are beta, beta', not equal and not conjugate, with Re beta^D = Re beta'^D for
    both. So no two rings (with D >= 2) suffice for all beta.
(c) If beta, beta' are q-th roots of unity and gcd(D,q) = 1, then Re beta^D = Re beta'^D implies beta' = beta or
    conj beta: one ring with D prime to the order of B suffices inside a known finite group.

Proof. For unit u,v: Re u = Re v iff v in {u, conj u}. (a) From D = 2, after replacing beta' by its conjugate,
beta'^2 = beta^2, so beta' = beta (done) or beta' = -beta. Then D = 3: -beta^3 in {beta^3, beta^-3} forces
beta^6 = -1; D = 5: -beta^5 in {beta^5, beta^-5} forces beta^10 = -1. Dividing, beta^4 = 1, so beta^2 = beta^6 = -1,
beta = +-i and -beta = conj beta. (b) Take eta != 1 with eta^(D_1) = 1 and tau != 1 with tau^(D_2) = 1, beta with
beta^2 = tau/eta, beta' = eta beta. Then beta'^(D_1) = beta^(D_1); beta'^(D_2) beta^(D_2) = eta^(D_2) beta^(2 D_2)
= tau^(D_2) = 1, so beta'^(D_2) = conj beta^(D_2); beta' != beta since eta != 1; beta' beta = tau != 1 so beta' is
not conj beta. (c) x -> x^D is a bijection of the q-th roots commuting with conjugation. QED.
Rings realizing D = 2, 3, 5: N = 4, 3 (or 6), 5 (or 10).

## Table (COMPUTED; table.py, table_result.json, sha256 03bcd177...dae7b0, rerun byte-identical)

Ranges: N = 1..12; groups C2xC3 (the note's), C2xC4, C2xC12 with a=c=1, b=g, d=zg.
Hypothesis per case: characters with chi(H) = -1: 3 of 6, 4 of 8, 12 of 24; only these enter.
Exhaustive part: every mask sequence (all nonempty subsets of occupied wells per tick) with every single final
well and port, to length T(N) = 9,9,8,9,6,8,6,7,6,6,6,6 for N = 1..12 (cap 20000 distinct filtered states per
level; affordability only). 1,499,612 port events and 1,075,365 well events in total, including 200 random
events of length 2D+3 per (N >= 3, group), seed 20261113.
Predicates (fixed in the docstring before the first run), all met, 0 failures:
P1 no event separates a pair with equal Re omega; P2 no event of length <= D separates any pair;
P3 the fork formula and "fork separates iff Re omega differ", N = 3..12; P4 shortest separating well event has
length exactly D+1, reached for N = 3,4,5,6,8,10 (NOT reached for N = 7,9,11,12: there the statement rests on the
proof only); P5 the N = 1,2 statements; P6 below; P7 fair-count corollary.
P6: among 60th roots of unity, no non-conjugate pair agrees on D = 2,3,5; non-conjugate pairs agreeing on {2,3}
are exactly primitive 12th roots (zeta_12 with zeta_12^5 or zeta_12^7); on {2,5} exactly primitive 20th roots.
In the rows below, r labels chi_r(g) = exp(2 pi i r/q). In the JSON the field "smallest_separating_*_event_found"
is the first one met; where T < D+1 it comes from the random part and is NOT minimal (the fork is).

| group | N | D | qualifying / all chars | pairs | inseparable pairs (r,r') [Re w equal] | separable pairs | fork length D+1 | exhaustive to length T | shortest separating well event in exhaustive range |
|---|---|---|---|---|---|---|---|---|---|
| C2xC3 | 3 | 3 | 3 / 6 | 3 | (0, 1) (0, 2) (1, 2) | 0 | 4 | 8 | none exists (all pairs inseparable) |
| C2xC3 | 4 | 2 | 3 / 6 | 3 | (1, 2) | 2 | 3 | 9 | length [3]; e.g. masks [[1, 3], [2]] then well 3: 0 vs 3/8 |
| C2xC3 | 5 | 5 | 3 / 6 | 3 | (1, 2) | 2 | 6 | 6 | length [6]; e.g. masks [[1, 4], [2, 3], [2, 3], [1, 4], [0]] then well 1: 1/16 vs 1/64 |
| C2xC3 | 6 | 3 | 3 / 6 | 3 | (0, 1) (0, 2) (1, 2) | 0 | 4 | 8 | none exists (all pairs inseparable) |
| C2xC3 | 7 | 7 | 3 / 6 | 3 | (1, 2) | 2 | 8 | 6 | none of length <= 6 (proved: none below 8); fork at 8 |
| C2xC3 | 8 | 4 | 3 / 6 | 3 | (1, 2) | 2 | 5 | 7 | length [5]; e.g. masks [[1, 7], [2, 6], [3, 5], [4]] then well 5: 0 vs 3/32 |
| C2xC3 | 9 | 9 | 3 / 6 | 3 | (0, 1) (0, 2) (1, 2) | 0 | 10 | 6 | none exists (all pairs inseparable) |
| C2xC3 | 10 | 5 | 3 / 6 | 3 | (1, 2) | 2 | 6 | 6 | length [6]; e.g. masks [[1, 9], [2, 8], [3, 7], [4, 6], [5]] then well 6: 1/16 vs 1/64 |
| C2xC3 | 11 | 11 | 3 / 6 | 3 | (1, 2) | 2 | 12 | 6 | none of length <= 6 (proved: none below 12); fork at 12 |
| C2xC3 | 12 | 6 | 3 / 6 | 3 | (0, 1) (0, 2) (1, 2) | 0 | 7 | 6 | none exists (all pairs inseparable) |
| C2xC4 | 3 | 3 | 4 / 8 | 6 | (1, 3) | 5 | 4 | 8 | length [4]; e.g. masks [[1, 2], [1, 2], [0]] then well 1: 1/4 vs 1/8 |
| C2xC4 | 4 | 2 | 4 / 8 | 6 | (0, 2) (1, 3) | 4 | 3 | 9 | length [3]; e.g. masks [[1, 3], [2]] then well 3: 0 vs 1/2 |
| C2xC4 | 5 | 5 | 4 / 8 | 6 | (1, 3) | 5 | 6 | 6 | length [6]; e.g. masks [[1, 4], [2, 3], [2, 3], [1, 4], [0]] then well 1: 1/16 vs 1/32 |
| C2xC4 | 6 | 3 | 4 / 8 | 6 | (1, 3) | 5 | 4 | 8 | length [4]; e.g. masks [[1, 5], [2, 4], [3]] then well 4: 1/4 vs 1/8 |
| C2xC4 | 7 | 7 | 4 / 8 | 6 | (1, 3) | 5 | 8 | 6 | none of length <= 6 (proved: none below 8); fork at 8 |
| C2xC4 | 8 | 4 | 4 / 8 | 6 | (0, 1) (0, 2) (0, 3) (1, 2) (1, 3) (2, 3) | 0 | 5 | 7 | none exists (all pairs inseparable) |
| C2xC4 | 9 | 9 | 4 / 8 | 6 | (1, 3) | 5 | 10 | 6 | none of length <= 6 (proved: none below 10); fork at 10 |
| C2xC4 | 10 | 5 | 4 / 8 | 6 | (1, 3) | 5 | 6 | 6 | length [6]; e.g. masks [[1, 9], [2, 8], [3, 7], [4, 6], [5]] then well 6: 1/16 vs 1/32 |
| C2xC4 | 11 | 11 | 4 / 8 | 6 | (1, 3) | 5 | 12 | 6 | none of length <= 6 (proved: none below 12); fork at 12 |
| C2xC4 | 12 | 6 | 4 / 8 | 6 | (0, 2) (1, 3) | 4 | 7 | 6 | none of length <= 6 (proved: none below 7); fork at 7 |
| C2xC12 | 3 | 3 | 12 / 24 | 66 | 21 pairs (see json) | 45 | 4 | 8 | length [4]; e.g. masks [[1, 2], [1, 2], [0]] then well 1: 1/4 vs 1/8 |
| C2xC12 | 4 | 2 | 12 / 24 | 66 | 14 pairs (see json) | 52 | 3 | 9 | length [3]; e.g. masks [[1, 3], [2]] then well 3: 0 vs 1/8 |
| C2xC12 | 5 | 5 | 12 / 24 | 66 | (1, 11) (2, 10) (3, 9) (4, 8) (5, 7) | 61 | 6 | 6 | length [6]; e.g. masks [[1, 4], [2, 3], [2, 3], [1, 4], [0]] then well 1: 1/16 vs (2*z^0 + -2*z^1 + 1*z^3)/2^6 |
| C2xC12 | 6 | 3 | 12 / 24 | 66 | 21 pairs (see json) | 45 | 4 | 8 | length [4]; e.g. masks [[1, 5], [2, 4], [3]] then well 4: 1/4 vs 1/8 |
| C2xC12 | 7 | 7 | 12 / 24 | 66 | (1, 11) (2, 10) (3, 9) (4, 8) (5, 7) | 61 | 8 | 6 | none of length <= 6 (proved: none below 8); fork at 8 |
| C2xC12 | 8 | 4 | 12 / 24 | 66 | 34 pairs (see json) | 32 | 5 | 7 | length [5]; e.g. masks [[1, 7], [2, 6], [3, 5], [4]] then well 5: 0 vs 3/32 |
| C2xC12 | 9 | 9 | 12 / 24 | 66 | 21 pairs (see json) | 45 | 10 | 6 | none of length <= 6 (proved: none below 10); fork at 10 |
| C2xC12 | 10 | 5 | 12 / 24 | 66 | (1, 11) (2, 10) (3, 9) (4, 8) (5, 7) | 61 | 6 | 6 | length [6]; e.g. masks [[1, 9], [2, 8], [3, 7], [4, 6], [5]] then well 6: 1/16 vs (2*z^0 + -2*z^1 + 1*z^3)/2^6 |
| C2xC12 | 11 | 11 | 12 / 24 | 66 | (1, 11) (2, 10) (3, 9) (4, 8) (5, 7) | 61 | 12 | 6 | none of length <= 6 (proved: none below 12); fork at 12 |
| C2xC12 | 12 | 6 | 12 / 24 | 66 | 30 pairs (see json) | 36 | 7 | 6 | none of length <= 6 (proved: none below 7); fork at 7 |

(Fork probabilities by r for C2xC3 and C2xC4, and all C2xC12 pair data, are in table_result.json; compact rows in
table_extract.txt.)

## What this does to "which character is the physical one"

Within the model (squared law, coherent masks, chi(H) = -1 assumed):
- One ring of N >= 3 sites fixes the single real number Re chi(B)^D and nothing else. PROVED (Props 1, 2).
  So it fixes chi(B) up to conjugation and up to multiplication by D-th roots of unity (beta' with
  beta'^D = beta^(+-D)).
- Rings with D = 2, 3, 5 together (e.g. N = 4, 3, 5) fix chi(B) up to complex conjugation. PROVED (Prop 3a).
  No two rings do for all beta (Prop 3b); inside a known finite group one ring with gcd(D, order of B) = 1 does
  (Prop 3c).
- Undetermined on every ring and every position-mask event. PROVED (Prop 1):
  (i) the orientation: chi against conj chi (in the note's group, chi_1 against chi_2);
  (ii) chi(a) and chi(c): they enter only as a common unimodular factor at each port. Since a, c, B, H generate
       the same subgroup as a, b, c, d, the events see chi only through (chi(H), chi(B)) and of that only
       (-1, Re chi(B)^D);
  (iii) the group: any two carriers and characters with the same chi(H) and the same chi(B) up to conjugation give
       identical statistics, so neither the order of the gain group nor faithfulness of chi is read.
- chi(H) = -1 is an input here, not something the ring measures. The physical identification of the gain group or
  of a character stays open, as the note says.

## Failed attempts, kept

F1. "Separated iff chi_0(B^D) != chi_1(B^D)" is FALSE. Counterexample: chi_1, chi_2 of C2xC3 on N = 7:
    omega = w and w^2, both give 1/256 at the fork, and by Prop 1 agree on every event. The invariant is Re omega.
F2. "A ring of suitable size identifies the character up to conjugation" is FALSE for one ring and for two rings
    in general (Prop 3b). Explicit: beta = exp(i pi/6), beta' = exp(5 i pi/6) agree on D = 2, 3 (and 4); they
    differ at D = 5. In C2xC12 (table): r = 1 and r = 5 inseparable on N = 3, 4, 6, 8, 9, 12, separable on N = 5, 7, 10, 11.
F3. "A separating event makes the rate differ from the fair count" is FALSE (review's P9): Re omega = 0.
F4. "Well events separate on N = 2 as on larger rings" is FALSE: every well probability is 0 or 1 there; only a
    rail-resolved port separates (Prop 2d).
F5. table.py v1 (table_v1.py, table_result_cap3000.json): 0 predicate failures, but its exhaustive range stopped
    one level early when the state cap was hit, so P4 was not reached for N = 5, 10. v2 fixed the loop only.

## Not done

No Lean. The algebra is |1 + s omega|^2 = 2 + 2 s Re omega for |omega| = 1, s = +-1, and Prop 3; both are short
and could be formalized. Carriers with a, c nontrivial are covered by the proof of Prop 1 but were not computed.
P4 not reached for N = 7, 9, 11, 12.
