# Candidate Z8, "Two Books": function

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

What the candidate computes, exactly, and the predictions that could fail. Programs and result files are in `function/`; every predicate was fixed in the docstring before the first run; the result file was reproduced in a fresh folder with identical bytes.

## Toy worlds computed

The signed line and rings of 3, 4, 5, 16 and 18 sites, from a sharp start at (0,R).

## Predictions

| # | Prediction | Value | Checked |
|---|---|---|---|
| Q1 | After one free step the mean entropy is not lower, for every position product event of non-zero weight | exact integer inequality Π(n_R+n_L)^(w_R+w_L) ≥ Π n_R^(w_R)·n_L^(w_L) | every mask sequence on rings of 3, 4, 5 sites to lengths 5, 4, 3: 45,218 events, 0 failures |
| Q2 | Equality in Q1 exactly when every site with chance has one rail empty of walks | — | 30,896 equality cases, 0 mismatches |
| Q3 | Entropy adds over a product of two events | identity of the coefficients of each logarithm | 200 random pairs, 0 failures |
| Q4 | A mask can lower the mean entropy | ring of 3 sites, an event of length 5, further mask {2}: 0.462… to 0 | one instance found, as predicted |
| Q5 | From a sharp start on the line the mean entropy rises at every step | H = 2.637 at T = 8, 14.799 at 32, 31.571 at 64 (natural logarithms) | T = 1 to 80, and rings of 16 and 18 sites |

Reported without a prediction: the gap to the ceiling, T·log 2 − H(T), is 2.908, 7.381 and 12.791 at T = 8, 32, 64 on the line.

## The graph

`function/plot_mean_entropy.svg`: H and the gap to the ceiling against the length, on the line, at even lengths. Made with the PCP OS plot instrument (provenance "model"). The plotted values are intervals of width 10⁻⁶ cut from 60-digit decimals; they are not certified enclosures. Input and the receipt of `visualization.ranges` are beside it. The values are model quantities of a stipulated candidate, not observations.

## What would refute the function

One position product event of non-zero weight whose mean entropy falls after a free step; an equality case outside Q2; a product of two events whose entropy is not the sum.
