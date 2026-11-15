# Candidate Z10 "Slow Clock" (abandoned): the two attackers' programs, finished by the director

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; kept with the assistance of Director Z (a Claude session). STIPULATED CANDIDATE FOR DISPROOF, already abandoned at 09:57 UTC on 15 November 2026. Nothing here is a claim about the world.

The two sub-agents (`2026-11-15_challenger_number`, `2026-11-15_wildcard_dial`) belonged to the session before this one and ended with its container. They left programs with predicates fixed in the docstrings, and partial outputs (two empty result files, one empty stdout). They wrote no reports. The director of the next session ran their programs unchanged, each in a fresh directory, through `Director_Z/tools/async_run.py`; the record with exit codes, durations and digests is `2026-11-15_challenger_number/director_rerun_2026-11-15b/ASYNC_RECORD.json`, the plan with every command line beside it. All four tasks exited 0. This is a run of the attackers' programs by the director, a model of the same family; it is not independent review.

| Program and arguments | Exit | Seconds | Predicates |
|---|---|---|---|
| `t1_exact.py 4 9600` | 0 | 45.9 | none failed; agrees with the attacker's own completed file in every field except the command string and the seconds |
| `t1_exact.py 2400 4800` | 0 | 242.0 | none failed: gap(2400) = 0.00268348… inside (0.0020, 0.0035); Λ/T < c* for every T ≤ 2400; Λ ≤ Λ_c with equality exactly at T = 1 to 4; counts are the binomials |
| `t5_carriers.py` (seed 20261115) | 0 | 26.5 | **QB FAILED**, kept: see below. QA1 to QA3 hold for the eight admissible named carriers; the all-plus probe is outside the hypothesis and not counted. First eleven output lines equal the attacker's partial output. |
| `dial_attack.py` | 0 | 187.8 | D7 False (expected by the attacker: the counting increment is below 0.99 until T = 72); **D10 False**, kept; the other ten True |

## Findings

1. **The inequality Λ ≤ Λ_c is not a property of admissible sign rules in general (QB).** For all 40 of 40 static sign rules drawn at random per site (each satisfying the norm hypothesis, tested per carrier), Λ(200) exceeds Λ_c(200), by up to 0.707 bits; the exact recomputation at 200, 400 and 600 ticks gives 0.7070, 0.7056, 0.7074 bits with 592 violating lengths, the first at T = 9. No rule of the periodic families (64 of period 2, 512 of period 3 in time, 4,096 static of period 4 in space) and none of the seven single-site defects exceeds counting. The statement that survives the sprint is about the carrier C1 and is untouched; its extension to every admissible carrier is refuted, and the candidate's weak point 5 (the constant and the inequality may belong to this coin only) is confirmed for disordered rules.
2. **"Two programs written separately" overstates the record (D10).** The two programs agree on the rates at 300 and 600 ticks, but share six identical code lines of forty or more characters, including the integrand and the quadrature loop. The agreement of their constant is therefore not agreement of two separate implementations. The attackers' own recomputations of c* (periodic trapezoid in 60-digit decimals; three rules in mpmath) are separate and agree to the thirteen places stated.
3. Everything else the candidate's text asserted about numbers held, to 2,400 ticks in full and at 4,800 and 9,600 ticks for the rate.

Neither finding changes the disposition: the candidate was killed for an empty stipulation and stays abandoned.

Path note: the runs were made while this folder stood at `Director_Z/candidate/Z10_Slow_Clock/`, and the recorded command lines carry that path. `dial_attack.py` reads `../SPRINT_2026-11-15/` relative to the candidate's parent folder, so after the move to `abandoned/` a rerun of it needs that folder reachable one level above (a link or a copy); the other three programs read nothing outside their arguments.
