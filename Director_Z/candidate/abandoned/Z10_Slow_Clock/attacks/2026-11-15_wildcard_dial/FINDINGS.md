# Wildcard attack "dial" on Z10 "Slow Clock" (15 November 2026)

STIPULATED CANDIDATE FOR DISPROOF; nothing here is a claim about the world. Attacker: wildcard sub-agent, same model family as the author.
The candidate was already abandoned by the director (WHY_ABANDONED.md, 09:57 UTC) when this attack finished; these findings confirm, extend and correct that record. R7 (T = 2400) was not computed here.

Commands (run in this folder):
  python3 dial_attack.py result_dial_run1.json > dial_run1.stdout     (exit 0, 2 min 49 s; 12 predicates fixed first; D7, D10 false, kept)
  python3 kappa_probe.py result_kappa_probe_run1.json                 (exit 0; exploratory, no predicate, double precision)
  pcpos plot < ../../function/plot_age_rate.json | sha256sum          -> 1ebe22b4...fccfd6b, equals the receipt and the svg

Control. T = 3: (1,R) chance 1/2, 2 histories; (3,R), (1,L), (-1,R), (-3,L) chance 1/8, 1 history each; (-1,L) has 2 histories, signs cancel, chance 0. Lambda(3) = (1/2)*log2(2) = 1/2. Right. (D1 true.)

(a) C5: KILL confirmed, and stronger than "empty".
 - Deletion test: no E, R, kill condition or number changes. Two rows missing from the director's table: ANSWERS line 12 ("Does time have a beginning?", marked FOLLOWS (E4)) keeps its fact but stops being an answer about time, so FOLLOWS was FOLLOWS-from-C5; MAP line 13 (C5 on P8) and "would add to OP-23" disappear.
 - "age, not the number of ticks" (BRAND line 18) is not a contrast an inhabitant can draw: Lambda is a function of T alone, needs T to be computed, and is not injective (Lambda(0) = Lambda(1) = Lambda(2) = 0 while the supports of the chances at 0, 1, 2 ticks differ: D2 true). No single record carries it: 200 records have non-zero chance at both T = 100 and T = 102, ages 73.003 and 74.532 (D3 true). So the age is a coarser relabelling of the tick count, kept by no record.
 - BRAND contradicts itself: line 26 "'Clock' and 'age' are names for a defined quantity" against line 18 "age, not the number of ticks, is the time".
(b) Wording.
 - OVERVIEW "There the age grows by very nearly one bit per tick": FALSE as worded for short lengths. Counting increment 0, 0.5, 0.689, 0.781 at T = 1..4; below 0.99 for every T from 1 to 72; Lambda_c/T = 0.903 at 50 (the candidate's own table). WOUND (D7 false, kept).
 - OVERVIEW "the number was written down before any long run was computed" against SPECIFICATION section 6 (author knew 0.755 at T = 300 from KZ9): WOUND, the overview omits the admission.
 - "favour records far from the middle, which have fewer histories": HELD at T = 100 (largest chance at (68,R), 0.1116, log2 n = 59.97; central record log2 n = 95.35; chance of |x| >= 50 is 0.622 against 5.6e-7). Not said: the chances are lopsided, 0.747 on x > 0, mean x = 28.98.
 - One line "fixed fraction ... per tick in the long run": increments at T = 1000..1199 lie in [0.770815, 0.770966] (D8 true). HELD as far as computed; limit stipulated.
 - "c* = 0.7715533031636 to thirteen places": HELD. Periodic trapezoid rule, 50-digit decimals, N = 200 and 400 agree to 5e-60: c* = 0.77155330316361197264361236985146426157...; the author's double is 7e-15 below.
(c) SPECIFICATION "two programs written separately": WOUND. Rates agree, but 6 of 16 long code lines of slow_clock_instances.py are byte-identical to kill_test_z10.py (h, g, simpson, the propagation loop). It is one implementation run twice (D10 false, kept). This program is a third, with a different quadrature, and agrees: 0.755081, 0.762485, 0.766603. E3's proof: HELD (max n = C(T-1, floor((T-1)/2)) for T to 1200, D5).
(d) E2 from T-1 of Two Books: HELD. Counting weight of the two children of x is 2(n_R + n_L): conserved site by site, so the proof applies; checked to T = 1199 for both ages (D4); strict rise of Lambda from 3 to 1199.
(e) ANSWERS "no ADDED answer": true to the letter; but see (a) for the FOLLOWS row.
(f) Plot: HELD. All 36 intervals contain my values (D11); digest matches; smallest plotted value 0.698395 against the floor 0.65, nothing cut.
(g) MAP: gate titles P0, P1, P5, P8, P10 match the issued map; OP-23 exists. HELD.

What can be made stronger (for the surviving conjecture, not for the candidate).
 gap(T)*T - (1/2)*log2(T) = 0.82729, 0.82653, 0.82614 at T = 300, 600, 1200 (and 0.8248 +/- 0.0012 from the director's 4-digit gap at 2400).
 Stirling's formula under the recalled limiting law gives the constant kappa = c* + (1/2) E[log2(pi(1 - v^2)/2)] = 0.825748 (double precision).
 Sharper conjecture: Lambda(T) = c* T - (1/2) log2 T - kappa + o(1). Forward value NOT computed here: gap(4800) = (0.5*log2(4800) + 0.825748)/4800 = 0.0014459.
 Exploratory: one probe, no predicate fixed first; the O(1) term of T*(E_T[h] - c*) is assumed to vanish and was not examined.
