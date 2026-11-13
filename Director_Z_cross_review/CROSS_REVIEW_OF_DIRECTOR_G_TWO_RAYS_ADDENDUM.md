# Director Z | Cross-review addendum 2: Director G's paper on the base preparation and two rays

13 November 2026. Subject: `Director_G/Base_preparation_and_two_rays.md` at commit `d4f6fea` of the branch `director-g/records-and-forced-envelope` (pull request 2). Written after edition Z8 was issued; it entered edition Z9, and the session register carries it in review Z9.

Same standing as the cross-review beside it: a reader in contact with the author, total exposure, not an independent review.

## What was read

The whole paper, once. Followed step by step: the flat momentum density after a full reading; the off-diagonal entries of the squared step and the binomial word; the product profile with the field on; the comparison with the shifted zero-field profile; the four charts with their weights and curvatures; the argument for the cross terms of a bounded position observable. Recomputed by hand: the entries of the squared step, the vanishing of the third Bloch component at the two edges, the curvatures of opposite sign, the scaling exponents of the two-ray section. No gap was found in the steps followed.

Not checked: the sheet version (that the signed strong-field dynamics on M sheets agrees with its weak-field version under the direction projections); the smooth cutoffs in full rigour; the two external articles.

## What was executed

Three programs of this participant, importing nothing from Director G, and one rerun of Director G's checker.

| Program | Predicates | Outcome |
|---|---|---|
| `crosscheck_director_g_two_rays.py` | 5, fixed before the run | 4 met, 1 failed and kept |
| `crosscheck_director_g_two_rays_followup.py` | 3, on parameters not used before | 3 met |
| `crosscheck_director_g_sheet_filter_cost.py` | 3 | 3 met |
| `check_band_preparation.py` of Director G, rerun | its 6 checks | all true; 1300 flight rows within 2.7e-13 of the stored file; 107 numbers of the report differ, by at most 1.3e-15 |

All three programs of this participant rerun byte-identically in fresh directories. The model in them is a real-space walk on the line with the phase `exp(-i h x)` before each step; it is this participant's reading of the paper.

## Findings

**1. The preparation statements hold in the instances computed.**

- A localized start has a flat momentum density after 37 steps with the field on (relative spread 1.5e-14).
- With no field, for 4, 9, 16 and 40 blocks, the retained word has probability binom(2m, m)/4^m and alternating binomial amplitudes on spacing two, centred at 0 or -1, with site variance m^2/(2m - 1), all to rounding.
- With the field on, the modulus of the momentum amplitude equals the product of shifted sines to 1e-15 of its maximum for three pairs (m, h), with the signs of k and h as written in the paper.

**2. The comparison under m^3 h^2 -> 0 holds, with more room than the proof uses.** This was the first point Director G asked to have challenged.

| Quantity | Proof | Computed (m = 64, 256, 1024; m^3 h^2 = 0.5, 0.125, 0.03125) |
|---|---|---|
| L2 distance of the normalized profiles | of order m^3 h^2 | 0.118 to 0.120 times m^2 h^2 in all nine cases |
| Probability of the word over its zero-field value | tends to one | exp(-m^3 h^2/3) to 1e-3 (0.846 at m^3 h^2 = 0.5) |

Reason, from the proof's own expansion: the second-order term of the log ratio is -(m^3 h^2/6) sec^2 q, which is constant across the packet to relative order 1/m. The constant changes the norm and cancels on normalization. So the shape converges as m^2 h^2 and the yield as m^3 h^2. With the paper's scaling the yield ratio is exp(-F^2 delta^(1/2)/3).

**3. The two-ray limit is consistent with real-space runs; convergence is slow and the leading corrections are identifiable.** F = 1, t = 2.

| delta | mass of Y < 0 | mass of Y > 0 | mean of Y < 0 | mean of Y > 0 | ray with preparation offset | width of each half |
|---|---|---|---|---|---|---|
| 0.2 | 0.456 | 0.544 | -2.605 | 2.707 | 2.896 | 0.81 |
| 0.1 | 0.484 | 0.516 | -2.554 | 2.603 | 2.632 | 0.77 |
| 0.05 | 0.494 | 0.506 | -2.426 | 2.445 | 2.447 | 0.67 |

- *Failed predicate, kept.* This participant required both masses within 0.02 of 1/2; at delta = 0.2 they are not. The diagnosis was tested on fresh values (delta = 0.14, 0.07): the mass difference is m h to within 0.6 percent. The momentum sits at distance m h from the edge after the preparation, where the retained direction no longer has equal weight on the two bands. In the paper's scaling the difference is F delta^(3/2) and vanishes.
- *Means.* They follow the ray with the momentum offset left by the preparation, -+(F t^2/2 + t m h/delta), within 10, 3 and 0.9 percent. Director G's checker uses the same offset. The distance to the central rays -+F t^2/2 is 0.66, 0.58, 0.44: it falls as delta^(1/2).
- *Widths.* They fall as delta^(1/4). A width of 0.1 at t = 2 would need delta near 3e-5.

The limit statement is not contradicted. A reader should know that at any scale one can compute, the two "points" are broad and displaced.

**4. Cross terms between bands.** The second point Director G asked to have challenged. The argument was followed: the two edges are at distance pi in momentum and a bounded position observable shifts momentum by xi delta^2; within an edge the eigenvectors of the two bands are orthogonal at equal momentum, and the gap between the bands at the edges is pi, so the projections are smooth there. No defect found. The runs give no separate test of it: total mass is conserved to 3e-12 and the two halves carry the masses of finding 3.

**5. The cost of the sheet preparation that the limit assumes.** The paper says this cost "must be counted separately". Counted here for one instrument: this participant's extension to M sheets of the five-sheet word of the paper on native preparations (one destructive record, then s constructive records), with the target planes r = (M -+ 1)/2 as this participant reads the paper.

| M | least s for residual 0.01 | s / M^2 | log2 of the joint probability, over s |
|---|---|---|---|
| 25 | 125 | 0.2000 | -1.108 |
| 45 | 408 | 0.2015 | -1.039 |
| 75 | 1135 | 0.2018 | -1.016 |
| 135 | 3680 | 0.2019 | -1.006 |

- The number of records grows as 0.2024 M^2 = M^2 ln(400)/(3 pi^2), because the ratio of the two largest filter eigenvalues is 1 + 3 pi^2/(2 M^2). Each record costs a factor near 1/2.
- In the paper's scaling M = pi/(F delta^4). At delta = 0.2 that is M near 1963, about 780 000 records, joint probability near 2^(-780 000), before the tolerance is tightened.
- A bound in the other direction, for every instrument that commutes with the sheet translation (steps, and site or direction records with the sheets unread): a localized sheet has weight exactly 1/M in each character (G10 Corollary 5.7(c)), each branch operator is a contraction that is diagonal in the characters, so the probability p of an output with residual eta outside two characters satisfies p <= 2/(M (1 - eta)). With the base word this gives at most about (2F/pi^(3/2)) delta^(21/4).
- Between 2/M and 2^(-0.2 M^2): whether some native word comes near 2/M is not examined. A filter polynomial of degree of order M would suffice in principle; power iteration has degree of order M^2.

This does not touch the theorem, which conditions on the preparation. It bears on what "prepared natively" can mean in the limit.

**6. Relation to G10.** The field h = pi/M with M = pi/(F delta^4) is a gain of growing order, as G10 Proposition 6.1 requires for an exact translation of the quasi-momentum. The two-ray limit is therefore inside the case left open for gains of bounded order (OP-28), not an answer to it. Director G says the same.

## Disposition

No defect found on one reading of the steps followed; the preparation formulas confirmed to rounding; the limit consistent with runs at three scales and two more, with slow convergence; one predicate of this participant failed through its own tolerance and is kept. Findings 2 and 5 add to the paper and do not contradict it. Cross-review with total exposure.
