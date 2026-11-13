# Findings, attacks on S6, S7, Z1-F of candidate model Z1 v0.1

Attacker: sub-agent of the author's model family (Claude). Agreement or disagreement here is not independent review. 13 November 2026.
Target read only: Director_Z/candidate/CANDIDATE_MODEL_Z1.md; proofs in G10 body.tex (thm:periodic, cor:composition, prop:compo, sec:force).

## Log, in order

1. attack_s6.py, first run, 11 predicates. A2 (S1 on ring4 x ring4) FAILED as predicted: product of even ring with itself is disconnected. All others passed.
   - ring3 x ring3: S1 holds in both gain versions; rule space dimension 2 (count, square of (sign,sign)); nullity mod p exactly 2.
   - (sign,1), (1,sign) not norm-preserving on the product.
   - S3-form of count x square not consistent: 128 vs 120 at length 3.
   - B_q x B_q with C x C gains (q = 5, 8): mu+ and mu- agree on all product events, differ on an entangled event (0.382 / 2 vs 4); half-half mixture is consistent and multiplicative on product events. With gains multiplied in C: dimension 4 (q=5), 3 (q=8) = 1 + classes of the factor.
   - Side finding: B_5 (C = Z_10) has a non-faithful norm-preserving character k = 5 (the Hadamard walk); B_5 has 3 classes, not 2.
   - ring3 x B_8: mixture over j = 1, 3 consistent; multiplicative with a mixture on the B_8 factor.
2. attack_s7.py, first run, 13 predicates.
   - B1c, F2 FAILED as predicted (non-faithful norm-preserving characters exist).
   - F4 FAILED against prediction: on the Z1-F ring N = q = 8 all four faithful characters give identical tables. KEPT.
   - F6 FAILED against prediction: for q = 8 every unit of Z_8 is induced by a carrier automorphism with switching. KEPT.
   - B_q: conjugates differ at t = 2; Galois identity exact; equality-type invariants coincide; order-type invariants separate.
3. attack_s7_followup.py (follow-up to the failures of F4, F6), 5 predicates, all pass: classes = orbits of k -> -k and, if 4 | q, k -> k + q/2. One faithful class for q = 4, 8, 12; two for q = 5, 10, 16. Non-faithful k with field 0 or pi gives exactly Z1-R.
4. Reruns of all three programs in a fresh directory: result files byte-identical.

## Limits

- Rule spaces: polynomial ansatz only (degree <= 3 or 2), sampled events, rank modulo 2^31-1 (gives an upper bound on the dimension; the bound is met by known rules, so it is exact for the ansatz on these carriers).
- No general proof of the class rule for Z1-F; computed instances only.
- The staircase / ray part of the Z1-F row was not attempted.
- Long return search on B_q is double precision (threshold 0.99 taken from the document's W3).

## Files

ATTACK_S6.md, ATTACK_S7.md, attack_s6.py, attack_s7.py, attack_s7_followup.py, Attack_S6_Results.json, Attack_S7_Results.json, Attack_S7_Followup_Results.json, rerun/ (byte-identical copies).
