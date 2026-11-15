# Candidate Z10, "Slow Clock": form

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

Every numbered stipulation is separately breakable.

## 1. Stipulations

| # | Stipulation | Kind |
|---|---|---|
| C1 | **Carrier.** Histories are walks from (0,R) on the two-rail digraph of the line: a right step from either rail of x leads to (x+1,R), a left step to (x−1,L). A left step that follows a left step carries the sign −1; every other step +1. The world runs free: every walk of length T is in the event. | carrier |
| C2 | **Chances.** With ε(v) the sum of the signs and n(v) the number of the walks of length T ending at v: the interfering world gives the record v the chance p(v) = ε(v)²/2^T; the counting world gives it p_c(v) = n(v)/2^T. | rules, stipulated |
| C3 | **Age.** The ledger entry of a record is log₂ n(v). The age of the interfering world at length T is Λ(T) = Σ_v p(v)·log₂ n(v); of the counting world, Λ_c(T) = Σ_v p_c(v)·log₂ n(v). Age is a property of the record of what was done (here: T free steps from a sharp start), not of the present state. | definition and identification |
| C4 | **The limit.** Λ(T)/T tends to c* as T grows, with c* the integral of BRAND.md, and Λ_c(T)/T tends to 1. | the claim |
| C5 | **The clock.** Age is the time that a world's own records keep. | identification, far-fetched |

## 2. What is proved, computed and stipulated

| Statement | Status |
|---|---|
| E1. Σ_v ε(v)² = 2^T, so p is a probability. | PROVED (each site's two children carry twice its weight; as in T-1 of the abandoned candidate Two Books) |
| E2. Λ(T+1) ≥ Λ(T) and Λ_c(T+1) ≥ Λ_c(T). | PROVED (T-1 of Two Books, which survived its kill; it holds for any rule whose weight is conserved site by site) |
| E3. Λ(T) ≤ T − 1 and Λ_c(T) ≤ T − 1 for T ≥ 1. | PROVED (the last step is fixed by the rail, so n(v) ≤ 2^(T−1)) |
| E4. Λ(1) = Λ(2) = 0; Λ(T) > Λ(T−1) for 3 ≤ T ≤ 600. | COMPUTED |
| E5. Λ(T)/T < c* for 1 ≤ T ≤ 1200; the gap is 0.016472, 0.009068, 0.004950 at T = 300, 600, 1200. | COMPUTED |
| E6. Λ(T) ≤ Λ_c(T) for 1 ≤ T ≤ 1200, with equality exactly for T ≤ 4. | COMPUTED |
| E7. 1 − Λ_c(1200)/1200 = 0.005967. | COMPUTED |
| E8. c* = 0.7715533031636; the weight under the integral is a probability density. | COMPUTED (Simpson's rule at two resolutions agreeing to 10⁻¹⁴) |
| C4: the two limits. | STIPULATED; supported by E5, E7; not proved |
| The origin of the formula for c*: the mean of the binomial exponent h((1+v)/2) over the limiting law of the walk's position per tick, density 1/(π(1−v²)√(1−2v²)) on |v| < 1/√2. | RECALLED from the literature on the Hadamard walk, NOT INSPECTED in a source; the candidate stakes itself on the number whatever its origin |
| C5. | STIPULATED |

## 3. Where it is most likely to break (named in advance)

1. **The number.** If Λ(T)/T converges to anything other than c*, or does not converge, C4 is false: KILL. The cheapest test is the forward prediction: gap(2400) strictly between 0.0020 and 0.0035. A proof of the limit, or of a different limit, decides it outright.
2. **The inequality E6 beyond 1200, or a proof that it fails.** If Λ(T) > Λ_c(T) at some length, commitment 3 of the brand is false: KILL.
3. **C5 is empty.** If nothing an inhabitant can do distinguishes "age is time" from "ticks are time", C5 says nothing. The candidate's only handle is that Λ is computable from the record of the masks (none, here) and the length; an attacker who shows that every statement of the candidate is unchanged when C5 is deleted has shown C5 empty. The process counts an empty stipulation as a KILL.
4. **The clock can stand still or run backwards.** Λ(1) = Λ(2) = 0 (stated). Under masks the same quantity can fall (shown for Two Books). The candidate restricts itself to free running from a sharp start on the line; if its brand or overview is found to claim more, that is a kill of the wording.
5. **c* is a property of a coin, not of interference.** Another norm-preserving choice of signs or another start may give another constant, or one above the counting world's rate. The candidate claims c* for C1 only. If the brand's fourth commitment ("interference slows a world's clock") is judged to assert the general statement, a carrier where interference speeds the clock up is a KILL.

## 4. Director's own attacks before release

| Attack | Result |
|---|---|
| KZ10 (a) to (f), predicates and the formula fixed before c* or any rate beyond 300 was computed | HELD, all six |
| K1 to K4 of `function/slow_clock_instances.py` | HELD |
| Is the formula's weight a probability density? | HELD (integral 1 to 10⁻¹⁴) |
| Weak points 1 to 5 | NOT ATTACKED further by the director; the forward prediction is left for others |
