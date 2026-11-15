# Challenger attack on Z10 "Slow Clock", 2026-11-15 (challenger_number)

Same model family as the candidate's author. Written at the end of the run in one piece (not after each target, as the brief asked); the stdout files carry the order of events.
Tool installed: mpmath 1.4.1 (`pip install --user mpmath`, pure-Python backend) for 400-bit logarithms and quadrature. Nothing outside this folder was modified. Not read: `function/`, the sprint folder, the director's forward-prediction folder.

## Command lines (cwd = this folder)
- `python3 t1_exact.py 2400 4800 t1_result_2400_4800.json > t1_stdout_2400_4800.txt` (exit 0, 225 s)
- `python3 t1_exact.py 4 9600 t1_result_4_9600.json > t1_stdout_4_9600.txt` (exit 0, 42 s)
- `python3 t2_limit.py t1_result_4_9600.json t2_result.json` (run 1, exit 1, TypeError in my quadrature; kept as `t2_stdout_run1_FAILED_typeerror.txt`, `t2_result_run1_FAILED_empty.json`)
- `python3 t2_limit.py t1_result_4_9600.json t2_result_run2.json > t2_stdout_run2.txt` (exit 0; program edited between runs: integration variable only, predicates unchanged)
- `python3 t3b_structure.py 600 t3b_result.json > t3b_stdout.txt` (exit 0)
- `python3 t5_carriers.py t5_result.json > t5_stdout.txt` (exit 0; one predicate FAILED: QB)
- `pcpos plot < plot_gap_input.json > plot_gap.svg`; `pcpos instrument visualization.ranges "$(cat plot_gap_ranges_call.json)"` (exit 0, digest matches)

## Control
T=3 from (0,R): (3,R) eps 1 n 1; (1,R) eps 2 n 2; (1,L) eps 1 n 1; (-1,R) eps -1 n 1; (-1,L) eps 0 n 2; (-3,L) eps 1 n 1. Sum eps^2 = 8. Lambda(3) = 1/2 bit, Lambda_c(3) = 1/2 bit.

## Target 1 (R7): HELD
gap(2400) = 0.002683481347181005858390517805848729329678567523... ; inside (0.0020, 0.0035).
gaps: 300 0.016472328478745096; 600 0.009068229481686017; 1200 0.004950459019699699; 2400 0.002683481347181006; 4800 0.001445886813718262; 9600 0.000775021582408019.
ratios: 0.550513, 0.545912, 0.542067, 0.538810, 0.536018.
c* = 0.77155330316361197264361236985146426157255923726521 (own trapezoid 64..512 panels, tanh-sinh, Gauss-Legendre; max pairwise difference 2.3e-61; agreement of rules, not an enclosure). Weight integrates to 1.
Arithmetic error of Lambda < 1e-100 (fixed-point log table against direct 400-bit log2 of the propagated integer counts at 300, 600, 1200, 2400: differences <= 2.3e-109). Counts equal C(T-1,r-1), C(T-1,r) exactly for all T <= 2400.

## Target 2 (c* and the limit): HELD, not a proof
- c* recomputed: agrees with 0.7715533031636 in all thirteen places.
- Fits over T = 300..9600: a/T max relative residual 0.20; a/sqrt(T) 0.61; a*log2(T)/T + b/T 5.4e-5 with a = 0.49969, b = 0.8296. Free-limit fit L - c* = -3.6e-7.
- B(T) = T*gap - (1/2)log2 T: 0.827289, 0.826528, 0.826141, 0.825946, 0.825847, 0.825798; differences halve each doubling (B = 0.82575 + O(1/T)). So numerically Lambda(T) = c*T - (1/2)log2 T - 0.8257 + O(1/T). A limit other than c* by delta would add delta*T to B: |delta| < about 1e-8 under that form. Numerical agreement only.
- Law: exact site law at T = 1200, 2400, 4800 against f(v)(1+v), f(v)(1-v), f(v), f = 1/(pi(1-v^2)sqrt(1-2v^2)). Max |CDF difference| at ten points: (1+v): 3.4e-3, 1.9e-3, 1.1e-3 (falling about as 1/T); (1-v): 0.496; symmetric: 0.248. Second moment minus (1 - 1/sqrt2): 3.6e-7, 9.1e-8, 2.3e-8. Mean -> +(1 - 1/sqrt2). So the sharp start (0,R) has the factor (1+v); E[h((1+v)/2)] is the same under all three laws to 1e-51 because h((1+v)/2) is even: the candidate's remark is right.
- max over records |log2 n / T - h((1+x/T)/2)|: 0.0097, 0.0053, 0.0028 at 1200, 2400, 4800 (O(log T / T), also provable from 2^(mh)/(m+1) <= C(m,a) <= 2^(mh)).
- Conditional derivation: p(v) is exactly the Hadamard-walk law; IF x/T converges weakly to the law above (Konno's theorem, recalled, not inspected by me either), THEN Lambda(T)/T -> c* because log2 n/T - h -> 0 uniformly and h is bounded continuous. The only step not proved here is the weak limit theorem itself. Lambda_c/T -> 1 follows from the law of large numbers the same way.

## Target 3 (E6): HELD on 1..2400; reduced, not proved
No violation for T <= 2400; equality exactly at T = 1,2,3,4 (difference at T=5: 0.14624 bits, the smallest for T > 4).
Identity (proved, checked exactly to 600): Lambda(T+1) = sum_x P_T(x) log2 C(T,r), Lambda_c(T+1) = sum_r C(T,r)/2^T log2 C(T,r), P_T the site law. Hence E6 at T+1 follows from S1: P_T(|x| <= k) <= Binom_T(|x| <= k) for all k. S1 has no violation for T <= 600 (exact integers). S1 for all T is unproved; it is the natural lemma. For large T, E6 follows from the limits (c* < 1) but without an explicit threshold.

## Target 4 (E1-E4): HELD
E1 exact for all T <= 2400 and at 4800, 9600 (the program checks it only where Lambda is evaluated, not at every T to 9600). E2, E3 hold for all T <= 2400; proofs follow (E2 needs n(child) >= n(parent), true here: child count C(T,r)). E4: Lambda(1)=Lambda(2)=0 exactly, strict rise 3..2400. Strictness is provable for every T: the increment Lambda(T+1)-Lambda(T) is at least (T-1)^2 log2(T/(T-1))/2^T from the record (T-2,R) (eps = n = T-1), T >= 2.
E5 also holds to 2400 and at 4800, 9600 (Lambda/T < c*).

## Target 5 (weak point 5): WOUND (wording); my reading, the director decides
- Start (0,L); -1 on R-after-R, on L-after-R, on R-after-L; starts R+L, R-L, R+iL: Lambda(T) is IDENTICAL to C1 at every T <= 600 (the symmetrised site law is the same exact integers, t3b S2; the unsymmetrised law differs for the other starts). So for these the rate is the same c* and E6 holds unchanged.
- Uniform time-periodic rules (period 2, 3) and rules depending on x mod 4, all norm-preserving, T=200, float64: rates from 0.748 (C1) up to 0.875, 0.916, 0.950; none above counting. An origin defect gives 0.705 to 0.913. So other sign rules have other rates (not converged values).
- FAILED PREDICATE QB, kept: static random admissible signs per site (40 seeds, 40 of 40) give Lambda(200) > Lambda_c(200). Exact integer confirmation for seed 822759165: Lambda - Lambda_c = +0.7070, +0.7056, +0.7074 bits at T = 200, 400, 600; sum eps^2 = 2^T exactly; Lambda > Lambda_c at 592 of the 600 lengths (from T = 9). Both rates tend to 1 (0.99008 against 0.98890 at 600). This is localisation: the walk stays near the origin where log2 n is largest; the excess is about 1/(2 ln 2) = 0.72 bits.
- Out-of-hypothesis probe (all signs +, not norm-preserving, renormalised): Lambda > Lambda_c by 0.36 bits at 600. Not counted.
- Sentences attacked: BRAND commitment 4 "so interference slows a world's clock, by the factor c* on this carrier"; OVERVIEW "so that interference makes a world's clock run slow". On the disordered carrier interference does not slow the clock: the interfering age is above the counting age. BRAND "What it is not" says "No claim is made for rings, other signs, other starts", and the overview says "nothing about ... other rules of walking". Read with those disclaimers the sentences are about C1 and stand; read alone they are general and false. I mark WOUND: the clause needs "on this carrier" attached to "slows", not only to the factor. If the director judges the clause general (FORM weak point 5), it is a KILL by the candidate's own rule.

## Overall
Not killed by this attack. R7 held; c* held to the stated numerical precision; E1-E6 held on the ranges; one wound to the wording of commitment 4.

## Not checked
Konno's theorem in a source; any T above 9600; E6 and S1 beyond the ranges; B-family carriers beyond T=200 except the one exact confirmation; C5 (emptiness, weak point 3); MAP.md, ANSWERS.md, LEDGER.md; no Lean.
