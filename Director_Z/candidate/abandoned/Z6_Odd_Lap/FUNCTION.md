# Candidate Z6, "Odd Lap": function

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md).

What the candidate computes, exactly, and the predictions that could fail. Programs and result files are in `function/`; every predicate was fixed in the program's docstring before its first run, and the result files were reproduced in a fresh folder with identical bytes.

## Toy worlds computed

The universal carrier of `function/odd_lap_instances.py`: gains in Z₂ × Z₂M with a = (0,0), b = (0,1), c = (0,0), d = (1,1). It satisfies O2 on every ring. Rings of 16, 18, 20, 9 and 11 sites (M = 8, 9, 10, 9, 11).

## Predictions

| # | Prediction | Value | Checked |
|---|---|---|---|
| P1 | The fork (masks {t, −t} for t = 1 to M, then every site), read at length M + 1: weight at ((M+1) mod N, R) and at ((M−1) mod N, L), in units 2^−(M+1) | M even: 4 and 0. M odd: 0 and 4. | 5 rings here, 9 rings in the sprint tests; all as predicted |
| P2 | No position product event of length at most M separates odd lap from even lap | equal weights at every vertex | all walks, T ≤ M, 5 rings |
| P3 | The event of all walks separates them from length M + 1; the total variation distance between the two distributions over vertices | ring of 16 sites: 1/128 at length 9, 7/128 at 10, 45/256 at 11, 353/1024 at 12, 281487/524288 at 24 | computed exactly; plotted |
| P4 | Total weight of all walks of length T | 2^T at every T | 5 rings, T up to 3M |
| P5 | Return to (0,R) on the ring of 16 sites | 289/16384 at length 16, 0 at 17, 169/16384 at 18 | computed exactly |

The even-lap world, the other square, has P1 with the two ports exchanged. So one two-history experiment at one clock decides between the two worlds, and inside the odd-lap world the same experiment reads the parity of M.

## The graph

`function/plot_odd_even_distance.svg`: the distance of P3 against the length, for rings of 16, 18 and 20 sites. Made with the PCP OS plot instrument (provenance "model"), input in `plot_odd_even_distance.json`, receipt of `visualization.ranges` beside it. The values are model quantities of a stipulated candidate; they are not observations.

## What would refute the function

Any position product event on a ring allowed by O1 and O2 for which the rule (ε₀ − ε₁)² fails P4, or fails multiplicativity; or a fork whose weights are not those of P1.
