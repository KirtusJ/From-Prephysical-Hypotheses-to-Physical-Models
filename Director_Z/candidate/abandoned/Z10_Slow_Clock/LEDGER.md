# Candidate Z10, "Slow Clock": ledger of attacks

**Label: STIPULATED CANDIDATE FOR DISPROOF.** Not a claim about the world, not an ontology; no gate of the program is passed by it. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada; compiled with the assistance of Director Z (a Claude session). Governed by [the candidate process](../CANDIDATE_PROCESS.md). Final candidate of the sprint of 15 November 2026.

| # | Date (UTC) | Attacker | Target | Verdict | Files |
|---|---|---|---|---|---|
| 1 | 15 Nov 2026 | director | KZ10 (a) to (f): c* against the rates at 300, 600, 1200; the inequality with the counting world; the counting rate | HELD | `../SPRINT_2026-11-15/result_kill_z10_run1.json` |
| 2 | 15 Nov 2026 | director | K1 to K4: start of the age, its rise to T = 600, the bound T − 1, the constant at two resolutions | HELD | `function/result_instances_run1.json` |
| 3 | 15 Nov 2026 | director (the two sub-agents assigned had been stopped by the account's usage limit and had written nothing) | the forward prediction R7, and E6 and the bound by c* extended to T = 2400 | HELD: gap(2400) = 0.002683 | `attacks/2026-11-15_director_forward_prediction/` |
| 4 | 15 Nov 2026 | director | weak point 3: C5 deleted, every statement, prediction and kill condition unchanged | **KILL**: C5 is an empty stipulation, by the criterion fixed in FORM before release | `WHY_ABANDONED.md` |
| 5 | 15 Nov 2026 | wildcard sub-agent, seed `dial` (resumed after the usage limit; reported after the kill) | C5 | **KILL confirmed and extended**: the age is a function of the length alone, needs the length to be computed, and is not injective (0 at lengths 0, 1, 2); no record carries it; the director's deletion table missed two rows (ANSWERS "Does time have a beginning?", MAP's row for C5) | `attacks/2026-11-15_wildcard_dial/` |
| 6 | 15 Nov 2026 | same | OVERVIEW "very nearly one bit per tick" (false below about 72 ticks); OVERVIEW "before any long run was computed" (omits that rates to 300 ticks were known); SPECIFICATION "two programs written separately" (they share their propagation loop) | WOUND three times | same |
| 7 | 15 Nov 2026 | same | c* to thirteen places (recomputed in 50-digit decimals: 0.7715533031636119726…), E2, E3, the plot, the map | HELD | same |
| 8 | 15 Nov 2026 | challenger sub-agent (resumed after the usage limit; reported after the kill) | the forward prediction R7, computed separately | HELD: gap(2400) = 0.002683481347, equal to the director's; also 0.001445887 at 4,800 ticks and 0.000775022 at 9,600 | `attacks/2026-11-15_challenger_number/` |
| 9 | 15 Nov 2026 | same | C4, the limit | HELD to its precision, not a proof: c* = 0.77155330316361197264… by three quadrature rules; the gaps fit ½·log₂T/T + 0.8257/T, and a fit with the limit left free differs from c* by 3.6 × 10⁻⁷; the exact site law agrees with the recalled limiting density times (1+v), to 1.1 × 10⁻³ at 4,800 ticks | same |
| 10 | 15 Nov 2026 | same | E6, E1 to E4 | HELD to 2,400 ticks; E6 reduced to an unproved dominance lemma, with no violation to 600 ticks | same |
| 11 | 15 Nov 2026 | same | weak point 5: brand commitment 4 read as general | WOUND: with random norm-preserving signs per site the interfering age is above the counting age (40 of 40 seeds at 200 ticks; one seed confirmed in exact integers at 200, 400, 600 ticks). The brand's disclaimers cover it; read alone the sentence is false. | same |

The director reran `dial_attack.py` (identical bytes) and `t1_exact.py 2400 4800` (identical apart from the recorded run time).

**Closed: the candidate was abandoned on 15 November 2026 at 09:57 UTC. See `WHY_ABANDONED.md`.** The text below is kept as written before the kill.

Open for attack by the sub-agents of this stack and by Director G's stack from the moment this file is pushed. A verified KILL ends the candidate; it will not be repaired. The forward prediction R7 has not been computed by the author.
