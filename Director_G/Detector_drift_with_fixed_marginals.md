# Detector drift with both individual outcome rates fixed

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Suppose each detector retains its nominal binary outcome rate conditional on the selected mass and the preceding observations. The dependence between the two outcomes may vary with the history. At four quadrillion pairs the critical per-pair total variation radius for keeping both conditional decision errors at or below 5% lies between **1.4532909 × 10⁻¹⁰** (achievable) and **1.4533604 × 10⁻¹⁰** (impossible). This is about **75.18% more tolerance** than when the [individual outcome rates can also shift](Unknown_direction_in_detector_pair_laws.md). Fixed empirical averages over an entire run would be a weaker assumption.

### Why a single unknown dependence parameter suffices

Order the cells as 00, 01, 10, 11. With both binary margins fixed, every allowed table differs from its nominal table by h times (1,−1,−1,1). Its total variation displacement is 2|h|. The nominal P and Q tables at a given mass already have the same margins. Move each toward the other by a coordinate step equal to the smaller of half the radius and half their first-cell gap. This gives the inward endpoints L and R; when the intervals overlap it gives a common midpoint instead.

For separated intervals score each observation by log(L/R) for its cell. In the direction from R toward L, each lower-score event has nonincreasing probability. In detail, the derivative is the signed sum of the four direction entries whose likelihood ratios are at or below the event cutoff. The [checker](check_fixed_marginal_radius.py) verifies the sign for every distinct ratio using exact rational comparisons. Since the derivative is constant on the entire line of allowed tables, all admissible P scores dominate those under L, and all admissible Q scores are dominated by those under R. The conditional quantile coupling from the earlier proof applies even if the displacement depends on past observations.

### Achievable and excluded radii

At the lower radius, repeatedly sample mass approximately 0.123279641138, collect the full budget, and decide by the sign of the sum of the endpoint scores, splitting ties fairly. The worse of the finite-sample conditional error upper bounds is below 0.049999999923. The tester needs the radius and nominal models; the actual displacement can remain unknown.

At the upper radius the same endpoint construction supplies one admissible pair of independent conditional laws at every mass. Applying the menu-wide adaptive clock bound gives equal-prior error above 0.05000000016 even for a tester told the endpoint laws. Therefore no capped policy can meet both conditional targets uniformly. Identical-law controls add no information. Nested radius classes extend the two results outwards. Both computations use outward interval arithmetic following the [unknown-direction certificate](Unknown_direction_in_detector_pair_laws.md).

This is a comparison between two mathematical uncertainty classes at the same budget and on the same routed mass menu. Whether a detector preserves its conditional single-outcome rates to this precision remains untested.
