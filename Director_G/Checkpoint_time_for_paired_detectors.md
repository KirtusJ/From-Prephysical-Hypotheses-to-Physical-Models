# When does checking more often save time?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

The [160-checkpoint rule](Finer_checkpoints_for_paired_detectors.md) collects fewer pairs than its 80-checkpoint predecessor. Under either specified detector model it makes between 44.9166 and 44.9490 extra checkpoint evaluations per run on average. If a checkpoint takes less time than collecting **177.1629 billion pairs**, the finer rule saves time on average. If it takes longer than collecting **197.9568 billion pairs**, the earlier rule saves time on average. The present enclosure leaves the ordering between these thresholds unresolved. These are serial-time comparisons at the same four-quadrillion-pair cap.

### Translating exposure into time

Assume a constant acquisition time p > 0 per pair and the same additional nonoverlapping time c per executed checkpoint under either schedule, including the final decision. For a schedule with block size B and mean exposure E, the realized pair count always equals B times its number of evaluated checkpoints. Its expected time is therefore E(p+c/B). A common fixed startup time cancels. In the worst case both schedules reach the full pair cap, so the finer rule then incurs 80 additional checkpoint delays.

Fix a detector law and write A and F for the mean pair counts of the earlier and finer schedules. The respective block sizes are 2B and B, with B = 25 trillion pairs. Equality of mean times occurs at

$$c/p=(A-F)/(F/B-A/(2B)).$$

The denominator is positive under both laws. This ratio increases with A and decreases with F: differentiating gives derivatives proportional to F and −A, respectively, with the same positive factor. Substitution of opposite enclosure endpoints therefore bounds the crossover. The [checker](check_checkpoint_cost.py) encloses each schedule's mean from both sides using integer survival propagation and finite-block corrections, and verifies the thresholds under P and Q separately.

The cost model concerns total elapsed time only when the checkpoint delay adds to acquisition time. If evaluation overlaps acquisition, c represents only the added delay. Different overheads for the two schedules can be inserted separately into their expected-time formulas. Neither detector throughput nor checkpoint latency has been measured here. The error bounds and the fresh independent pair assumptions are those of the underlying schedule comparison.
