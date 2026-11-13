Target: Director_G/Periodic_interaction_and_two_limits.md with check_periodic_force.py, check_cycle_interaction.py and their result files, at commit e53742c.
Outcome: GAP (wording and evidence; no defect found in the note's mathematics or reported numbers).
Reviewer kind: pcp-cross-reviewer run as a sub-agent of the queue session; the queue session rechecked only what is listed at the end. Same model family as Director Z; cross-review from shared sources, not independent replication. Director G's files were read, not modified.

The queue entry says this note was already assigned to a sub-agent of the director; no report was present in Director_Z_cross_review/ at this commit, so it was done here. If the director's own report exists elsewhere, the two should be compared.

Conventions used by the reviewer: coin 0 = right; Hadamard minus sign on left-to-left; psi(x) = sum c_k e^{+ikx}; step eigenvalue e^{-i omega}, omega(k*) = -pi/4; sheet character e^{-2 pi i g/M}; kappa > 0 attractive; ties round upward; all quantities dimensionless. Taken from the checker because the note omits them and the numbers depend on them: initial data, band-section gauge, target time 0.75, round(0.5/delta^2) ticks for count flights.

Derivations
- Count construction (eigenvalues, leading pair, bound on rho_N, log-ratio integral, power bound): follows.
- theta_N bound: follows; tight (worst ratio 0.99954 over 480 qualifying instances).
- Claim (1), steps 1 to 5: the orders follow. Constants and the core/density argument not checked.
- Edge estimate |q|^4/6: follows (series -q^4/6 + 19 q^6/180).
- Two limits; M = N^3 + 1 odd and coprime to N: follows.
- Newton equations, [K, Z_j], Gronwall sources; entanglement minor; folded preparation: follow.
- GAP (wording): "36 runs" are 36 comparison rows from 30 walks; the repulsive walk is compared twice.
- GAP (evidence): the gap between the walk statistic and the Newton value is 0.112 at N = 64 and 0.095 at N = 128 (reviewer's run). The Newton limit rests on the proof alone; the note says so.
- GAP (remark): the stated O(a sqrt m) yield error is valid and loose; at N = 96, m = 30 the ring mean equals the integral mean to 2.7e-16.

Reviewer's program (xrev_periodic.py, seed 20261113; hypothesis N >= 8 and N divisible by 4 tested per N: 8 of 12 qualify)
- Reproduced at N = 64, kappa = 1: distances 0.0069737 and 0.0358236; statistics 0.809627, 0.807330, 0.697360.
- Count flights N = 24: 0.4835312 at depth 1, 0.00043916 at depth 2880. N = 32 (not in the note), depth 5120: 0.001077 against the bound 0.002456.
- Folded yield N = 96, m = 30: 0.01052228.
- Sizes not in the note, kappa = 1: fixed action 0.003123 (N = 96), 0.001766 (N = 128), slope -1.92; shrinking action 0.02515, 0.01857, slope -1.07.
- Conjugate character matches the kappa = -1 reference (0.00733), not kappa = +1 (1.3135).

Failed predicates of the reviewer (kept)
- A2 (rho bound) at N = 20..40 and A3 (power bound) at N = 28..40: 60-digit arithmetic floors rho near 1e-61 while the bounds are 1e-64 to 1e-77. Follow-ups at 400 digits pass, stable at 800.
- B1 (edge estimate) at q = 0 and B1' at q = 1e-11, 1e-12: the same cancellation. B1'' at 200 digits passes.
All three trace to the reviewer's precision, not to the note.

Checker rerun (Python 3.13.18, numpy 2.5.3; stored run 3.12.14, 2.3.5): all 15 checks true; cycle_interaction.csv byte-identical; float differences at most 4.7e-14; no quoted digit changes.

Lean: not rechecked by the sub-agent (it was told not to install a toolchain). Static reading of SharedSheet.lean: no sorry or axiom; the analytic parts are not formalized. GAP: Director_G/lean/lean-toolchain pins 4.19.0, not this repository's 4.12.0.

Rechecked by the queue session: the result files exist and their pass flags are as reported (A2, A3, B1 false; 17 others true); the toolchain pin is 4.19.0; the note's sentence "Over 36 runs" is at line 96. Nothing else in this report was rechecked.

Not checked: constants in (1); the preparation-stage claims that cite other notes; folded-flight values 0.10649 and 0.30566; Periodic_force_review.md; external references.
