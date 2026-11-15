# Candidate Z10, "Slow Clock": function

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

What the candidate computes, exactly, and the predictions that could fail. Programs and result files are in `function/` and `../SPRINT_2026-11-15/`; every predicate was fixed before the first run; result files were reproduced in a fresh folder with identical bytes.

## Predictions, worded as tested

| # | Prediction | Value | Status |
|---|---|---|---|
| R1 | c* | 0.7715533031636 | computed at two resolutions |
| R2 | Λ(T)/T at T = 300, 600, 1200 | 0.755081, 0.762485, 0.766603; each below c* | computed |
| R3 | gap(T) = c* − Λ(T)/T at 300, 600, 1200 | 0.016472, 0.009068, 0.004950; each smaller than the one before | computed |
| R4 | Λ(1) = Λ(2) = 0; Λ(3) = 1/2; Λ(T) > Λ(T−1) for 3 ≤ T ≤ 600 | — | computed |
| R5 | Λ(T) ≤ Λ_c(T) for 1 ≤ T ≤ 1200, equal exactly for T ≤ 4 | — | computed |
| R6 | Λ_c(1200)/1200 | 0.994033 | computed |
| **R7** | **gap(2400)** | **strictly between 0.0020 and 0.0035** | **NOT COMPUTED by the author; left as the test** |

## The graph

`function/plot_age_rate.svg`: age per tick against the length, T = 50 to 600, for the interfering world, the stipulated limit and the counting world. Made with the PCP OS plot instrument (provenance "model"). The plotted values are intervals of width 10⁻⁶ cut from longer decimals; they are not certified enclosures. Input and the receipt of `visualization.ranges` are beside it. Model quantities of a stipulated candidate, not observations.

## What would refute the function

R7 outside its interval; a length at which Λ(T)/T exceeds c*; a length at which Λ exceeds Λ_c; a recomputation of c* that differs in the sixth place.
