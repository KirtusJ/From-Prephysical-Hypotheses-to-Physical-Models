# A narrower range for the checkpoint time crossover

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

For the same 80- and 160-checkpoint detector schedules, the common added checkpoint delay at which expected elapsed times coincide lies between **179.69618 and 195.42032 billion pair acquisition times** under either model. This narrows the [previous enclosure](Checkpoint_time_for_paired_detectors.md) by about 24.4%. The finer schedule is faster below the new lower endpoint and the coarser schedule is faster above the upper endpoint. This calculation changes neither decision rule.

### Bounding remaining checks at each score

For a live integer score just before a block, charge one checkpoint and add the expected number of later checks. The latter is a function of the updated score, extended by zero outside the two continuing boundaries. Immediately before the last block every live score has value one. Working backward from this terminal value yields a reference table of expected remaining checks. The [checker](check_checkpoint_value_bounds.py) uses the rounded normal block increments from the earlier analysis and integer arithmetic for this table.

For a finitely supported function f of the updated score, let V(f) be the sum of its absolute differences across adjacent integers, including the jumps to and from zero. Discrete summation by parts gives an expectation difference at most ε V(f) when the two increment CDFs differ by at most ε. Translating the current score leaves this variation unchanged. The iid Berry–Esseen bound on ε applies under either detector law with the corresponding moments. It includes either convention at rounding ties by continuity of the comparison normal. [Finite-block justification](Tapered_thresholds_for_paired_detectors.md)

At each stage the checker evaluates the actual variation of the integer reference table. A CDF rounding allowance of 1300 units on a denominator of 10²² is added to ε. Only interior bin probabilities enter the recursion. Their integer differences telescope under summation by parts, so the same variation bound also covers this CDF rounding. Rounding the updated value downward costs at most one further unit of 10⁻²². The exact-law transition is a contraction in maximum absolute error, as each continuation expectation integrates against probability mass at most one. Summing the one-stage residual bounds therefore encloses the exact expected number of checks at the initial zero score. This proof does not assume smoothness or monotonicity of the reference table.

### Applying the time model

Both conditional expected counts lie within 45.26805–45.27173 for the 80-checkpoint rule and 90.19230–90.21306 for the 160-checkpoint rule. Let A and F denote the respective expected numbers of checks under a fixed law. With 25 trillion pairs per finer block, the delay in pair-time units at equality is 25 trillion times (2A−F)/(F−A). This increases with A and decreases with F on the certified intervals. The checker uses unrounded conditional endpoints separately under each law.

The analysis assumes a common additive, nonoverlapping checkpoint delay, constant pair acquisition time, and the two specified lossless detector laws with fresh independent pairs. The interval is numerical uncertainty in the comparison. Actual detector throughput and checkpoint latency remain unmeasured.
