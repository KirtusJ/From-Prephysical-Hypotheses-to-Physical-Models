# Candidate Z8, "Two Books": specification

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

Written to the standard of the Mathematics and Science modules of the method (ACR Mathematics 1.0 Sections 2, 4, 6, 7; ACR Science 1.0 Sections 2, 4.1, 7.2), which the principal selected for this session.

## 1. Question and what would count against it (Science 2)

**Question.** With chances given by squared signed sums and entropy by the logarithm of the number of histories, does the mean entropy obey a second law under free running, and do the identifications S4 to S6 hold up as an account of entropy and of time's direction? **Counts against:** a position product event of non-zero weight whose mean entropy falls after a free step; a property that any entropy must have and that H lacks; a demonstration that n(v) is beyond anything an inhabitant can know; a demonstration that S6 is circular. Fixed in FORM.md section 3 before release.

## 2. Mathematical signature (Mathematics 2)

- **Objects.** Line Z or ring Z_N, N ≥ 1; vertices (x,R), (x,L); walks from (0,R); sign of a walk = (−1)^(number of left steps that follow a left step); an event = position product event of length T; ε(v), n(v) = signed sum and number of the walks of the event ending at v.
- **Quantities.** p(v) = ε(v)²/Σε², defined when Σε² > 0; S(v) = log n(v) for n(v) ≥ 1, natural logarithm; H = Σ_{v: p(v)>0} p(v)·S(v).
- **Quantifiers.** T-1 holds for every event of non-zero weight on the line and on every ring, for one free step, hence for any number.
- **Boundary.** Events of zero total weight are excluded (p undefined). A step with a mask is not covered by T-1 (T-3 shows it can fail). Records of zero chance contribute nothing to H whatever their count.
- **Conventions.** The start (0,R) counts as arrived by a right step.

## 3. Statements

T-1 to T-4 of FORM.md with their proofs. Nothing is taken from outside this folder except the definition of the carrier, which is that of paper G10.

## 4. Computation (Mathematics 6, Science 4.1 "computational or theoretical")

| Control | Where |
|---|---|
| Exact premises and inputs | docstrings of `function/two_books_instances.py` and `../SPRINT_2026-11-15/kill_tests_batch2.py` |
| Algorithm | exact propagation of signed sums and counts by vertex; the inequality of T-1 is tested as an inequality of integers, with no logarithm |
| Implementation checks | two programs written separately (the kill test with 60-digit logarithms, the instances with integer powers) agree that no decrease occurs |
| Numerical error | none in Q1 to Q4; Q5 and the graph use 60-digit decimal logarithms, compared with a margin of 10⁻⁴⁰ |
| Coverage | Q1, Q2 exhaustive on rings of 3, 4, 5 sites to lengths 5, 4, 3; larger rings sampled; the proof covers all |
| Sensitivity | line and rings; sharp start and masked preparations |
| Empirical applicability | none claimed |
| Failed predicates | none |

## 5. Status table

| Item | Status |
|---|---|
| T-1 to T-4 | PROVED |
| Q1 to Q5 | COMPUTED on the ranges listed |
| S1 to S6 | STIPULATED |
| That log n(v) is a thermodynamic entropy; that free running is time's direction | STIPULATED, not argued |
| Any statement about the physical world | NONE MADE |

## 6. Limits

Reviewers so far are the director and programs written in this session. The proof of T-1 is short and has been read by no one else. The candidate has not been read by Director G.
