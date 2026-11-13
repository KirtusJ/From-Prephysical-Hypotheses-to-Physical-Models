WOUND

# Attack on S6 (the product is only formal), candidate model Z1 v0.1

Attacker: sub-agent of the author's model family (Claude); not independent review. 13 November 2026.
`attack_s6.py`, `Attack_S6_Results.json`: 11 predicates fixed first; 10 pass, A2 fails as predicted; rerun byte-identical.

## What held

On the primary instance the product carrier changes nothing. Ring N = 3, D x D (36 vertices, one step moves both walkers):

- S1 holds (out-degree 4, no parallel arcs, derived digraph strongly connected), with pair gains multiplied in C = {+-1} and with pair gains kept in C x C.
- Of the three non-trivial characters of C x C only (sign, sign) is norm-preserving; (sign, 1) and (1, sign) are not.
- Polynomial rules with free coefficients at every vertex, degree <= 3 on C (324 unknowns) and <= 2 on C x C (504 unknowns): dimension 2 in both, the count and ||v||^2 for (sign, sign).
- "Count on factor 1 times square on factor 2" in the form of S3 is not consistent (length 3: mu(Ext S) = 128, 4 mu(S) = 120).

## Wounds

1. **The even ring times itself is not a carrier of S1.** For N = 4, and every even N (the document's table uses N = 16), x1 - x2 keeps its parity: D x D is not connected; 32 of 64 vertices are reachable. On the reachable part the derived digraph is strongly connected (period 2) and the dimension is again 2. The restriction must be stated.

2. **S6 does not fix the gain group of the composite, and with C x C it does not select one class.** B_q x B_q, pair gains in C x C, q = 5, 8: all 25, respectively 16, pairs (chi^a, chi^b) of norm-preserving characters are norm-preserving. mu+ = ||v^(chi,chi)||^2 and mu- = ||v^(chi,chi^-1)||^2 are both consistent with factor 4, equal on every product event (exhaustive at length 2, 300 sampled at length 3), and different on the non-product event E = {(0-0-0, 0-0-0), (0-1-0, 0-1-0)}: mu+ = |1 + zeta^2|^2 = 0.382 (q = 5), 2 (q = 8); mu- = 4; count 2. So (mu+ + mu-)/2 is consistent, non-negative, normalized, multiplicative on all product events at every length, and not the squared norm of one class. D3's conclusion fails on this composite, and S6, a condition on product events only, cannot see it: no pair of single-carrier rules fixes the weight of an entangled event. With pair gains multiplied in C the product has exactly the factor's characters and dimension 1 + classes (4 for q = 5, 3 for q = 8). S6 therefore needs an unstated stipulation: the composite records only the product of the gains. The primary instance escapes because its character is real; Z1-F does not.

3. **Different carriers.** On ring(3) x B_8, gains in Z2 x Z8, (mu_1 + mu_3)/2 with mu_j = ||v^(sign, chi^j)||^2 is consistent, a mixture, and equals mu1(S1) mu2(S2) with mu2 a mixture on B_8. Multiplicativity between different carriers selects nothing; "a carrier with itself, same formula" is necessary.

4. **Records.** Count times square is consistent and multiplicative once the whole walk of factor 1 is the record (300 events). S3 does not say what the records of a composite are.

## Not tried

No kill: no composite was found on which the model's own rule is inconsistent. Non-polynomial rules on the product; rings N >= 5; null spaces are modulo 2^31 - 1 on sampled events (an upper bound, met by the known rules); the full C x C rule space on B_q x B_q (20600 unknowns).
