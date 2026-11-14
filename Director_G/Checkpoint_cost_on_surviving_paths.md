# Checkpoint time bounds from runs still collecting pairs

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

The expected-time crossover between the existing 80- and 160-checkpoint rules lies between **181.77545 and 193.33909 billion pair acquisition times per checkpoint**, separately under either specified detector model. Below the lower bound the finer rule is faster on average. Above the upper bound the coarser rule is faster. The unresolved interval is 26.5% narrower than the [previous interval](Checkpoint_time_from_remaining_checks.md). All pair counts, thresholds and stopping decisions are as before.

### Weighting the backward calculation

A run enters its first block with probability one. For a later block, the run must have survived every preceding checkpoint. A local error in estimating the number of remaining checks contributes to the initial estimate only on paths that enter the corresponding block.

More precisely, extend each reference value table by zero on stopped states. Along the exact process take the differences between each table entry and its one-step expected update, including the cost of the next check. Taking expectations and summing over time cancels all the intermediate reference values. The terminal table gives exactly one check before the final block. Thus the absolute initial error is bounded by the sum of the absolute one-step residual bounds multiplied by the exact block-entry probabilities. The [previous proof](Checkpoint_time_from_remaining_checks.md) supplies the individual residual bounds in terms of the variation of each table and the block CDF error.

For block i+1, propagate an upper bound on rounded Gaussian survival through i checkpoints. The exact survival probability is at most that bound plus 2iε, capped at one. This follows by replacing one independent increment at a time. Conditional on all other increments, the scores surviving all earlier checkpoints restrict the replaced increment to an interval, whose probability differs by at most twice the one-block CDF bound ε. The [implementation](check_live_checkpoint_cost.py) applies these upper probabilities to the variation terms. It retains the full fixed-point rounding allowance for every block. No independence between survival and the local residual is required.

The resulting expected counts under both laws lie within **45.26853–45.27125** checks for the coarser rule and **90.19505–90.21031** for the finer rule. For fixed-law expected counts A and F, the crossover in pair-time units is 25 trillion times (2A−F)/(F−A). The checker uses each law's unrounded endpoints and verifies both reported bounds. This comparison assumes a common additional checkpoint delay and constant acquisition time per pair. Neither quantity was measured on a physical instrument.
