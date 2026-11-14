WOUND

# Attack on S7 and Z1-F (the character and the force), candidate model Z1 v0.1

Attacker: sub-agent of the author's model family (Claude); not independent review. 13 November 2026.
`attack_s7.py` (13 predicates; B1c, F2 fail as predicted; F4, F6 failed against prediction, kept), `attack_s7_followup.py` (5 of 5). Exact arithmetic in Z[x]/Phi_M; reruns byte-identical.

S7 held: a real choice that cannot be derived. Two sentences of Z1-F about it are false as written.

## S7 is not empty (B_q)

psi_k(zeta) = zeta^k, psi_k(-1) = (-1)^k on C = Z_M, M = lcm(q,2). Conjugates differ at t = 2: P_2(0) = (1 + cos(2 pi k/q))/2.

| q | k = 1 | other class | difference |
|---|---|---|---|
| 5 | 0.6545 | k = 3: 0.0955 | 0.559 |
| 8 | 0.8536 | k = 3: 0.1464 | 0.707 |
| 10 | 0.9045 | k = 3: 0.3455 | 0.559 |
| 12 | 0.9330 | k = 5: 0.0670 | 0.866 |

k and -k agree for all t <= 12; tables in the result file.

## Nothing algebraic selects the character

For faithful k, P^(k)_t(y) = sigma_k(P^(1)_t(y)) exactly (t <= 12): the weights are Galois conjugates. Equality-type invariants agree for all conjugates (no exact return to t = 300, no dark vertex to t = 60, reversal symmetry); S4 and S5 hold for each. B_q has no automorphism, with switching, inducing g -> g^a, a != 1. So nothing built from the carrier, the events and polynomial identities distinguishes zeta from zeta^j; only the order of the reals does (k = +-1 maximizes P_2(0)). First return above 0.99: 11 against 15 steps (q = 5), 17 against 11 (q = 8), 7 against 13 (q = 10), 9 against 23 (q = 12): no consistent winner. The character is a measurable parameter, not a gauge.

## Z1-F: what is false

1. **"The conjugates of the faithful one."** The step is norm-preserving for every k with psi_k(-1) = -1, faithful or not: ring N = q = 6: k = 3; q = 10: k = 5; q = 12: k = 3, 9; q = 5 (C of order 10): k = 5. For q = 5, 6, 10 that character gives exactly the tables of Z1-R: **no force**. S7 chooses between a force and none, not only its unit.

2. **"The choice of character is the choice of the unit of force" fails when 4 | q.** Literally true: the step matrix of psi_k with field Phi equals that of psi_1 with field k Phi, entry by entry. But psi_k and psi_(k+q/2) give the same rule on every event (the extra gain (-1)^x is a switching times a constant). The classes are the orbits of k -> -k and k -> k + q/2: for q = 4, 8, 12 there is **one** faithful class and S7 chooses nothing; q = 16: two.

3. **Otherwise not a relabelling.** x -> k^-1 x does not carry one table to the other. For q = 5 the sorted probabilities differ at t = 3 (largest 0.4523 against 0.3273): no relabelling of vertices whatever. Carrier automorphisms with switching induce only a = 1 (q = 5), +-1 (q = 6), all units (q = 8).

## Not tried

the staircase and ray statements of the Z1-F row (NOT ATTEMPTED); other order-type invariants; a proof of the class rule for all q (computed for q = 4, 5, 6, 8, 10, 12, 16).
