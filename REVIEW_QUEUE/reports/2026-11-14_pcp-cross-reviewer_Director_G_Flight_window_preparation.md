Target: Director_G/Flight_window_preparation.md with its checker, Director_G/results/flight_window.json and lean/FlightWindow.lean; commit b07cff6. Named in the director's note of 13 November (late).
Outcome: GAP (four points; no defect found in the derivations or the reported numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; rechecked by the queue session only where stated at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

Claims of the note: asymptotic statements (position operator X_t = X + tV + B_t with a bounded B_t; an estimate (1); a density value rho(0) = 1/pi; an acceptance probability P_yes = (2/pi) w [1 + o(1)]; concentration of the accepted terminal position about a free ray); computed instances (5/8, 17/64, 0, 1/64; a run at delta = 1/40 with P_yes = 0.0112854, 2.54 percent above the leading term, mean 0.999114, tail 45.4 percent). Premises labelled as such: a coherent membership pointer, score transfer to pointer records, a terminal instrument.

Derivations: eigenvalues, the formula and bound for B_t, estimate (1) by Duhamel (uses the sharp launch, which is in the statement), rho(0) = 1/pi, the bracketing and edge bounds, the centred-norm bound and its transfer by unitarity, the explicit exponents: all follow.

GAPs
1. Stated in the surrounding text only: the Result paragraph says "asymptotically 2w/pi" and "approach a free ray" without the conditions T w^(5/2) -> infinity, v -> 0 and the four limits, which appear in later sections.
2. Stated nowhere: the size of the o(1). The measured relative error is about delta times p0, set by the slope of the density away from v = 0, so it is not uniform in p0. The "2.54 percent above" is this term, not slow convergence in w. At delta = 1/40 the ratio of P_yes to 2w/pi is 1.0254 for p0 = 1, 0.9772 for p0 = -1, 1.0550 for p0 = 2, 1.0020 for p0 = 0; against the exact spectral mass of V in the window the ratio is 0.99895.
3. Evidence: no finite run probes the regime of the proof. T w^(5/2) stays between 1.08 and 1.28 for 1/delta from 4 to 128. With T = delta^(-2.2), where T w^(5/2) tends to zero, the acceptance ratio still tends to one (1.0007 at 1/delta = 1024). So the acceptance numbers do not test estimate (1) or that hypothesis; the condition is sufficient and not shown necessary.
4. Reproducibility: the checker's rerun is not byte-equal to the stored result file. The exact panels, the text and the predicates are equal as data; 80 floating values differ, by at most 9.6e-14 in absolute terms.

Lean (file read, not elaborated: it pins 4.19.0): four theorems on an exclusive-or flag over lists of signed path amplitudes. The walk, the numbers 5/8, 17/64, 1/64, the spectral facts, estimate (1), rho(0), P_yes and the concentration are not formalized. The note labels the file "finite flag proof", which matches.

Reviewer's program (xcheck_window.py, seed 20261113, no failed predicate): the exact values 5/8, 17/64, the parity zero at 78 of 78 qualifying sites, the edge window 2^-T for T = 1..12; spectral facts to 1e-15; the delta = 1/40 run reproduced by direct iteration and by the spectral formula (agreement 6e-14): P_yes = 0.011285395, mean 0.9991137, tail 0.453964. Parameters not in the note: ratio 1.0559, 1.0238, 1.0168, 1.0108, 1.0080 at 1/delta = 20, 48, 64, 96, 128 (51 of 52 instances qualify). Tail beyond 1/2: 0.546, 0.501, 0.454, 0.442 at 1/delta = 8, 16, 40, 48, not monotone between 24 and 32.

Rechecked by the queue session: the rerun of the checker differs in bytes from the stored file, as reported. The sub-agent's numbers were not recomputed.
Not checked: Lean elaboration; estimate (1) numerically; the G1 specification and the cited literature; the finite-ring statement beyond the size condition used.
Cost reported by the sub-agent: about 5 minutes, 10 tool calls.
