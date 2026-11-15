# Candidate Z10, "Slow Clock": specification

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

Written to the standard of the Mathematics and Science modules of the method (ACR Mathematics 1.0 Sections 2, 4, 6, 7; ACR Science 1.0 Sections 2, 4.1, 5.3, 7.2), which the principal selected for this session.

## 1. Question and what would count against it (Science 2)

**Question.** Does Λ(T)/T converge to c* on the carrier C1, and is Λ(T) ≤ Λ_c(T) at every length? **Counts against,** fixed before release: R7 outside (0.0020, 0.0035); any length with Λ(T)/T ≥ c* or Λ(T) > Λ_c(T); a proof of another limit or of none; a demonstration that C5 is empty; a sentence of the brand or overview that claims more than C1 to C5.

## 2. Mathematical signature (Mathematics 2)

- **Objects.** The line Z; vertices (x,R), (x,L); walks of length T from (0,R); sign of a walk = (−1)^(number of left steps that follow a left step), the start counting as arrived by a right step; ε(v), n(v) as in C2.
- **Quantities.** p(v) = ε(v)²/2^T; p_c(v) = n(v)/2^T; Λ(T) = Σ_{v: ε(v)≠0} p(v)·log₂ n(v); Λ_c(T) = Σ_v p_c(v)·log₂ n(v); gap(T) = c* − Λ(T)/T.
- **Quantifiers.** E1 to E3 for every T ≥ 1. E4 to E7 for the stated finite ranges only. C4 is a statement about the limit T → ∞ and is not established.
- **Boundary.** T = 1, 2: Λ = 0. No masks, no rings, one start.
- **The constant.** c* is defined by the integral in BRAND.md; the integrand is smooth on the closed interval.

## 3. Statements

E1 to E8 and C4 of FORM.md, with status there.

## 4. Computation (Mathematics 6; Science 4.1 and 5.3)

| Control | Where |
|---|---|
| Exact premises and inputs | docstrings of `../SPRINT_2026-11-15/kill_test_z10.py` and `function/slow_clock_instances.py` |
| Algorithm | exact integer propagation of ε and n; logarithms in 60-digit decimal arithmetic; c* by Simpson's rule in double precision |
| Kind of numerical evidence | approximation with a stability check: c* at 100,000 and 200,000 panels agrees to 10⁻¹⁴; this is agreement at two resolutions, not a certified enclosure |
| Margins | comparisons of ages use a margin of 10⁻⁴⁰ against 60 digits; comparisons with c* are at the scale 10⁻³ against an uncertainty of about 10⁻¹³ |
| Implementation checks | two programs written separately give the same rates at T = 300, 600 |
| Coverage | all T to 1200 for E5, E6; to 600 for E4; a finite range, not a proof of C4 |
| Sensitivity | none examined: one carrier, one start (weak point 5) |
| Empirical applicability | none claimed |
| Failed predicates | none for Z10; its predecessor Ledger Clock failed a strict inequality at T = 3, 4, which is why E6 here says "equality exactly for T ≤ 4" |

## 5. Status table

| Item | Status |
|---|---|
| E1 to E3 | PROVED |
| E4 to E8 | COMPUTED on the stated ranges |
| C4 (the limits) | STIPULATED, supported by computation, NOT PROVED |
| The source of the formula | RECALLED, NOT INSPECTED |
| C5 | STIPULATED |
| Any statement about the physical world | NONE MADE |

## 6. Limits

Reviewers so far are the director and programs written in this session. The candidate has not been read by Director G. The formula for c* was written before c* was computed, but its author knew the rates up to T = 300 (0.755 at 300) when writing it.
