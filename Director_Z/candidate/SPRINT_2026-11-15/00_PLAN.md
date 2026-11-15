# Candidate sprint of 15 November 2026: plan

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by `../CANDIDATE_PROCESS.md`.

**Label for everything in this folder: STIPULATED CANDIDATES FOR DISPROOF.** None is a claim about the world, none is an ontology, no gate of the program is passed by any of them, and each is written to be broken. The candidates are intentionally far-fetched, at the principal's word: "a crazy candidate model (intentionally out there, explicitly stipulated, to push the boundaries) for immediate disproof".

## The principal's three rules for this sprint

1. Give yourself an overall time period to work.
2. Abandon a candidate as soon as it is broken in the period.
3. Settle on a final candidate by the end, to steelman, and properly brand, for disproof across the stack and by Director G's stack.

## Period

Start 08:35 UTC, end 10:05 UTC, 15 November 2026 (90 minutes). At the end the candidate then standing is the final one; if none stands, that is said and the least-broken idea is not rescued.

## Order of work

| Minutes | Work |
|---|---|
| 0 to 10 | this plan: every candidate's stipulations and its first kill test, with the predicate fixed before the test is run |
| 10 to 45 | the kill tests, one program each; a candidate that fails is moved to `../abandoned/` at once with `WHY_ABANDONED.md` |
| 45 to 90 | the survivor is steelmanned in full (form, function, brand, overview, specification, map, answers, ledger) and sent to attackers of this stack and to Director G |

## The candidates, in the order they are tested

Common ground for all four (STIPULATED, taken from paper G10 as issued in edition Z31, and not argued for here): histories are walks from (0,R) on the two-rail digraph of a ring of N sites; a right step goes to (x+1,R), a left step to (x−1,L); events are position product events; a rule adds over end vertices a function of the walks there.

### Z3 "Count Veil"
- **Stipulation.** The weight of an event is the number of its walks, divided by 2^T. There is no interference anywhere; what is called a dark port is a port that the masks emptied.
- **Kill test KZ3 (fixed now).** The published four-step cesium walk of Robens, Alt, Meschede, Emary and Alberti (Phys. Rev. X 5, 011003, 2015), blank run, as archived by Director G in `Director_G/results/cesium_negative_read.json`: the counts at the wells j = −1 and j = +1. Z3 predicts equal probability at the two wells (4/16 each). Predicate: the exact two-sided binomial probability of a split at least as uneven as the observed one, under p = 1/2, is below 10^−6. If so, Z3 is KILLED by an observation. The threshold is far below any correction for the choice of wells (at most 5 wells, 3 rows, 2 directions: a factor 30).
- **Grounding label.** The counts were reconstructed by Director G from the published vector figure; this session does not re-extract them. SUPPLIED by the other director, EXTERNAL in origin.

### Z4 "Lap Time"
- **Stipulation.** Physical time is the winding of a history round the ring, not the number of its steps. Fix a long length T and the signed carrier (gain −1 on a left step that follows a left step). For each winding level j let ψ_j be the vector, over the 2N vertices, of the signed sums of the walks of length T at that vertex and level. Z4 says: there is one linear map L on the 2N-dimensional space, the same for all levels and all lengths in a stated family, with ψ_{j+1} = L ψ_j. "One lap is one tick, and L is the clock."
- **Kill test KZ4 (fixed now).** All walks (no masks) on rings N = 4, 6, 8, lengths T = 6M, 6M+2, 6M+4 (M = N/2). Collect all pairs (ψ_j, ψ_{j+1}) with both non-zero over these lengths; solve exactly for L by least squares over the rationals (exact linear algebra: is the system ψ_{j+1} = L ψ_j consistent?). Predicate: the system is consistent on at least one of the three rings. If it is inconsistent on all three, Z4 is KILLED: no clock map exists even in the simplest event.

### Z5 "Lap Blind"
- **Stipulation.** Walks that differ in winding never interfere: the weight at a vertex is the sum over winding classes of the squared signed sum in each class, q·Σ_i ε_i² in the notation of G10 Theorem 5.61. And the world composes: the weight of a product event of two independent copies is the product of the weights.
- **Kill test KZ5 (fixed now).** Ring N = 16 is too large to enumerate; use the abstract two-class setting on a ring N = 4 with Z_2 x Z_2 gains chosen with s = 2, k even (so the rule is in the consistent family), all walks of lengths T = 4 and 6, and the product of the carrier with itself. Compare μ(S×S') with μ(S)μ(S') for the events S, S' = "all walks of length T ending at one vertex", over all pairs of vertices. Predicate: equality in every pair. If any pair fails, Z5 is KILLED by its own two stipulations contradicting each other.

### Z6 "Odd Lap" (the fallback, tested last)
- **Stipulation.** The count part is zero, the world composes, and every lap multiplies the summed gain by −1: χ(β) = −1 in the notation of G10 Theorem 5.61. A closed world returns to itself with a sign.
- **Kill test KZ6 (fixed now).** On rings with s = 2 and k even the two squares are (ε_0+ε_1)² and (ε_0−ε_1)²; Z6 is the second. Test (a): it must be consistent on every position product event examined (random masks, rings N = 4, 6, 8; factor 2 exactly). Test (b): it must be multiplicative on the product events of KZ5. Test (c), the prediction that could fail: with the fork event of G10 (masks {t, −t} to length M, then all sites), the weight at clock M+1 must equal 2^−(M+1)·[2 + 2(−1)^(M−1)·(−1)], that is zero for M odd and 4·2^−(M+1) for M even, on rings N = 6, 8, 10, 12, 14. Predicate: (a), (b), (c) all hold. Any failure KILLS Z6.

## What is not done in this sprint

No candidate is repaired. A killed candidate's surviving statements may seed a later one under a new name, not in this period.

## Outcome (written at the end of the testing part of the period)

| Candidate | First test | Verdict | Where it is now |
|---|---|---|---|
| Z3 "Count Veil" | KZ3 | KILLED by an observation (binomial probability 3.0 x 10^-14) | `../abandoned/Z3_Count_Veil/` |
| Z4 "Lap Time" | KZ4 | KILLED by exact computation (no clock map on rings of 4, 6, 8 sites) | `../abandoned/Z4_Lap_Time/` |
| Z5 "Lap Blind" | KZ5 | KILLED: its two stipulations contradict (32 of 32 pairs) | `../abandoned/Z5_Lap_Blind/` |
| Z6 "Odd Lap" | KZ6 (a), (b), (c) and a follow-up for odd M | STANDS | `../Z6_Odd_Lap/`, steelmanned, branded, open for attack |

Deviation from the plan, recorded: test KZ6(c) named rings of 6, 8, 10, 12 and 14 sites; the carrier of the first program has two classes with k even only for M = 2 modulo 4, so it ran on 4, 12 and 20 sites, and a follow-up with its predicate fixed first ran on 6, 10, 14, 7, 9 and 11 sites with another carrier. Rings of 8 sites (M = 4) were covered by neither; the instances program covers M = 8, 9, 10, 11.

**Final candidate of the sprint: Z6 "Odd Lap".**

## After the testing part: the survivor was killed, and a second batch

At 08:46 UTC a wildcard attacker killed Z6 "Odd Lap" (its ADDED answer and brand against its own composition stipulation); the director checked the files and abandoned it at once: `../abandoned/Z6_Odd_Lap/WHY_ABANDONED.md`. A second attacker, reporting after the kill, found no kill and one wound of substance: the odd-lap weights equal those of the plain square on another carrier, so the "choice" was a matter of description.

The period runs to 10:05 UTC. Rule 3 asks for a final candidate by its end, so a second batch follows. Stipulations and kill tests are fixed here before any test is run. **Label as before: STIPULATED CANDIDATES FOR DISPROOF.**

Common ground for both: the signed two-rail carrier (gain −1 on a left step that follows a left step), walks from (0,R), on the line and on rings; the weight of a vertex is the square of the signed sum of the walks ending there, divided by 2^T; n(v) is the number of walks ending at v.

### Z7 "Dark Arrow"
- **Stipulation.** The arrow of time is the growth of darkness. In the event of all walks, a vertex is dark at length T if walks end there and their signed sum is zero. Z7 says: the number of dark vertices never decreases as T grows.
- **Kill test KZ7 (fixed now).** The line, T = 1 to 60, and rings of 16 and 18 sites, T = 1 to 60. Predicate: the number of dark vertices at T + 1 is at least the number at T, for every T in the range, on all three carriers. One decrease KILLS Z7.

### Z8 "Two Books"
- **Stipulation.** The same histories are read in two books. The book of chance weighs a record (an end vertex) by the square of its signed sum. The book of heat gives the same record the entropy log n(v), the logarithm of the number of histories that end there. Z8 says: these two are the quantum and the thermal description of one world, and the second law holds between them: for an event of all walks continued freely, the mean entropy H(T) = Σ_v p_T(v)·log n_T(v), the average over the book of chance of the entropy in the book of heat, never decreases with T.
- **Kill test KZ8 (fixed now).** (a) The line, T = 1 to 80; rings of 16 and 18 sites, T = 1 to 80: H(T+1) ≥ H(T) for every T. (b) 200 random position product events on the ring of 16 sites (seed 20261115, length 4 to 16, mask density 0.5 to 0.9), each continued freely for 12 further steps: H non-decreasing over the free steps. Arithmetic: probabilities exact; logarithms in 60-digit decimal arithmetic; a decrease counts if it exceeds 10^−40 (far above the rounding of 60 digits over at most a few hundred terms, far below any real difference). Predicate: (a) and (b) both hold. One decrease KILLS Z8.

If both die, the sprint ends with no standing candidate, and that is said.
