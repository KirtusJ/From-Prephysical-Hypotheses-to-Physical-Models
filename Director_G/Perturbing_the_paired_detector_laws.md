# How much error in the pair law can the detector test tolerate?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Measure error in a four-cell probability table by total variation (TV), half the sum of absolute cell discrepancies. Use the single mass and four-quadrillion-pair cap of the [160-checkpoint experiment](Finer_checkpoints_for_paired_detectors.md). The following radii apply to each law separately.

| Per-pair TV displacement | What is established |
|---|---|
| At most 5.2527 × 10⁻¹⁴ | The existing rule keeps each conditional error below 5% for every allowed perturbation. |
| About 1.49947 × 10⁻¹⁰ | An explicit pair of shifted laws gives even the best fixed-mass, capped decision equal-prior error above 5.01394%. |
| About 5.76719 × 10⁻⁹ | The two TV neighborhoods first share a pair law. Independent draws from that law remain indistinguishable at every exposure. |

These are mathematical sensitivity bounds on the observed joint distribution. They do not estimate instrument drift. The first two radii leave a gap in the robust 5% boundary.

### Uniform protection for the current rule

Let p be one nominal table, and let its actual conditional distribution before each collected pair, given the observed past, be p+u with TV at most δ. This assumption permits history-dependent errors. Internal policy randomness has the same distribution under both laws. The nominal table is strictly positive; at the stated δ all perturbed cells remain positive. Let m₁ and m₂ be the two smallest nominal cell probabilities. The positive entries of u sum to at most δ and the negative entries have the same total magnitude. Concentrating each sign on a different cell bounds the sum of uᵢ²/pᵢ by δ²(1/m₁+1/m₂). Taylor's bound on −log(1+x)+x for |x|≤δ/m₁ gives

$$D(p\Vert p+u)\leq \frac{\delta^2(1/m_1+1/m_2)}{2(1-\delta/m_1)^2}.$$

The KL chain rule applied to the stopped transcript sums this bound only over pairs actually entered. Equivalently pad the transcript to the cap with a shared deterministic symbol after stopping. Its divergence is bounded by the one-step bound times the **nominal** conditional mean pair count, below 2.25541057 quadrillion. Mapping that transcript to the wrong-decision indicator can only reduce divergence. If actual conditional error were at least 0.05 while nominal error is at most 0.04999529, its binary divergence would be at least D(Bern(0.04999529) ∥ Bern(0.05)), by monotonicity on these separated intervals. The [interval computation](check_detector_perturbation.py) shows the transcript upper bound is strictly smaller under both nominal laws at the protected radius. [Stopped change of measure](https://emiliekaufmann.github.io/GRETSI_270819.pdf)

### A finite-cap counterexample and exact overlap radius

Write P and Q for the nominal tables. In each law replace 1.3% of pairs, independently, with draws from the other table. The resulting distributions are 0.987P+0.013Q and 0.013P+0.987Q. Both retain the original single-detector marginals; each moves by exactly 0.013 TV(P,Q). Even an observer given every pair through the cap and told the two shifted laws cannot attain the 5% target at this mass. The optimal equal-prior full-data test decides by the sign of the shifted log likelihood. Applying the [iid normal approximation with explicit error bounds](check_fixed_exposure.py) to that statistic under each shifted law gives equal-prior error above 0.0501394, allowing fair ties. Any earlier stopping rule can be run on the full transcript and therefore cannot improve this optimum. This counterexample concerns the observed-law perturbation class and does not require either perturbed table to belong to the original mechanistic model family.

Finally the midpoint (P+Q)/2 is at TV(P,Q)/2 from each table, about 5.76719 × 10⁻⁹. The triangle inequality excludes any common table at a smaller equal radius. Choosing that same midpoint independently under both hypotheses makes the entire transcript law identical, so every binary decision has equal-prior error exactly one half. This conclusion is scoped to the selected mass. Other measurements could distinguish the hypotheses.
