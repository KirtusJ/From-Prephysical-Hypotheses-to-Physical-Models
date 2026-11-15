# Candidate Z6, "Odd Lap": specification

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md).

Written to the standard of the Mathematics and Science modules of the method (ACR Mathematics 1.0 Sections 2, 4, 6, 7; ACR Science 1.0 Sections 2, 4.1, 7.2), which the principal selected for this session.

## 1. Question and what would count against it (Science 2)

**Question.** Is there a rule, on the stated carrier and events, that satisfies O1 to O7, and is it unique? **Counts against:** a position product event on which the rule fails consistency or multiplicativity; a second rule satisfying O1 to O7; a proof that one stipulation is empty or implied by the others in a way the form denies; a symmetry of the event weights that changes χ(β). These were fixed in FORM.md section 3 before release.

## 2. Mathematical signature (Mathematics 2)

- **Objects.** Ring Z_N, M = N/gcd(N,2) ≥ 8; vertices (x,R), (x,L); walks from (0,R) as sequences of steps; gains a, b, c, d in a finite abelian group A; δ = ad/(bc); B = bc/a²; β = B^M; H = ⟨a, bc, δ⟩; Δ_N = ⟨δ, β⟩.
- **Hypotheses in the form the proofs use.** δ of even order r; β ∉ ⟨δ⟩; β² = δ^k with k even (O2). Events are position product events (O3). The rule is Σ over end vertices of F(multiset of gains), F site-independent, F(∅) = 0, weight of Ext S = 2 × weight of S for every position product event S (O4).
- **Quantifiers.** D1 to D5 hold for every ring and every gain assignment allowed by O1 and O2. D7 is for every position product event of length at most M.
- **Boundary.** Rings with M ≤ 7 are outside the candidate (the preparation behind G10 Theorem 5.61 is proved for M ≥ 8). k odd is outside (then χ(β) = ±i and there is one square, not two). r odd is outside (then no square exists).
- **Conventions.** ε_i(m) = Σ_n (−1)^n m(κβ^i δ^n) for a base point κ of the coset; (ε₀ − ε₁)² does not depend on κ.

## 3. Statements

D1 to D7 of FORM.md, with their proofs or references there. The only statements taken from outside this folder are G10 Theorems 5.51(ii) and 5.61 and Proposition 5.60 (edition Z31), which were reviewed there by sub-agents of the author's model family and not independently.

## 4. Computation (Mathematics 6, Science 4.1 "computational or theoretical")

| Control | Where |
|---|---|
| Exact premises and inputs | carrier and masks in the docstrings of `function/odd_lap_instances.py`, `../SPRINT_2026-11-15/kill_tests.py`, `function/kill_test_z6_followup.py` |
| Algorithm | exact propagation of counts by site, rail, number of left steps and sign; integers and fractions only |
| Implementation checks | group gains against level bookkeeping on the ring of 16 sites (predicate F4); two programs written separately agree on the fork |
| Numerical error | none: exact arithmetic |
| Coverage | 5 rings for the instances, 9 for the fork, 208 random events for consistency; a finite range, not a proof; the proofs are D1 to D6 |
| Sensitivity | two different carriers (Z₂ × Z₄ and Z₂ × Z₂M) give the same fork weights |
| Empirical applicability | none claimed |
| Failed predicates | none in this folder; the first fork test could not reach odd M and said so; the follow-up fixed its predicate first |

## 5. Status table

| Item | Status |
|---|---|
| Existence and uniqueness of the rule under O1 to O7 | PROVED given G10 Theorems 5.51(ii), 5.61 and Proposition 5.60 |
| P1 to P5 | COMPUTED on the rings listed; P1 and P2 also follow from G10 |
| O1 to O7 themselves | STIPULATED |
| Any statement about the physical world | NONE MADE |

## 6. Limits

Reviewers so far are the director and programs written in this session. The cited theorems are one day old. The candidate has not been read by Director G.
