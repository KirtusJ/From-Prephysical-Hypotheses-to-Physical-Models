# A terminal phase test for coherent readout on the optical circle

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), derivation, figure analysis and exact calculation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

One fixed launch and one fixed analyzer basis fit **all twenty occupied-position cells** at rounds 7, 13, 17 and 19 of the ten-site optical-circle experiment. The same sites and rounds exclude every common launch when the detector adds the original rail intensities with fixed gains. A controlled phase on one output rail distinguishes the explanations. Every fit using time-independent positive detector responses at the five sites must change the normalized position distribution by more than **0.00325164 in total variation** upon dephasing in at least one of those rounds. This conclusion allows a separate unknown intensity normalization for every round and intervention. [Earlier exclusion](Three_sites_and_four_rounds_of_the_optical_circle.md) · [Lorz et al., Eq. (13) and Fig. 7(c)](https://doi.org/10.1103/PhysRevResearch.1.033036) · [Source image](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png)

## A single fixed change of detection basis

Use the paper’s balanced coin $H'=(I-iX)/\sqrt{2}$, opposite rail shifts on the ten-site circle, and one launch at site 2. Choose the initial rail amplitudes $(4,1-2i)/\sqrt{21}$. At every occupied site and every round, resolve the same two orthogonal output vectors $(2,-1+2i)/3$ and $(-1-2i,-2)/3$. Multiply their intensities by the pair of gains below and divide their sum by the reciprocal round scale. Each pair of gains applies throughout the four rounds.

| Site | Gain for the first output | Gain for the second output |
|---:|---:|---:|
| 1 | 15720 | 10202 |
| 3 | 39715 | 1986 |
| 5 | 7551 | 17982 |
| 7 | 431 | 8613 |
| 9 | 61387 | 4102 |

The reciprocal scales in round order are 10000, 15885, 20598 and 13782. One common scaling of the gains and reciprocal scales leaves every prediction invariant. The integer-amplitude walk gives a point strictly inside the eight-level RGB band at each of the twenty cells. The smallest distance to a band endpoint is about 0.000179 in the figure's intensity scale. The totals on the five occupied sites are about 0.984, 0.896, 0.812 and 0.570. The [exact predictions](coherent_circle_readout_output.json) give the two output-phase settings separately. This construction was fitted to the published raster. It establishes a possible readout mechanism within this model. The apparatus response and physical launch state have not been identified.

## A bound that survives independent normalization

Let $H_m$ be any fixed positive semidefinite two-rail intensity response at site $m$, and $W_{tm}$ its local outgoing rail state, including the probability mass at that site. The displayed intensity is $q_{tm}=k_t\operatorname{tr}(H_m W_{tm})$ for a positive common scale $k_t$. This class includes site-specific analyzer bases and efficiencies. Retain the ideal walk and a common localized launch, pure or mixed. Assume the intervention acts only on the terminal rail phase and leaves the preparation, walk and detector responses fixed.

Immediately before detection, apply either the identity or $Z=\operatorname{diag}(1,-1)$. An equal mixture of these operations removes the off-diagonal rail terms. At the original scale its site response is exactly that of the diagonal gains $(H_{m,RR},H_{m,LL})$. Denote the four round-wise distributions over the five occupied sites by $P_t$ before the intervention and $D_t$ after dephasing, each divided by its own total. A fit has positive total in each compared round. Purely diagonal responses give $P_t=D_t$ exactly.

To see why a coherent fit needs a nonzero change, let $s_t=\sum_m q_{tm}$ and $B_t=\sum_m U_{tm}$, summing the five upper endpoints of the experimental bands. Suppose $\mathrm{TV}(P_t,D_t)\le\epsilon$ in every round. The singleton bound gives $|P_{tm}-D_{tm}|\le\epsilon$. Rescale the dephased distribution to $d_{tm}=s_t D_{tm}$. Its positive normalization may differ in each round. It is a fixed diagonal-gain prediction satisfying

$$
 L_{tm}-\epsilon B_t\ \le\ d_{tm}\ \le\ U_{tm}+\epsilon B_t.
$$

The [three-site certificate](three_circle_site_certificate.json) excludes that possibility on sites 3, 5 and 9 for $\epsilon=46484/14295555$. For each launch rectangle its multipliers $u_{tm},l_{tm}$ weight the upper and lower inequalities. Widening the bands leaves all six coefficients of the gains strictly positive. The coefficient for a reciprocal round scale decreases from $C_t=\sum_m(l_{tm}L_{tm}-u_{tm}U_{tm})$ by $\epsilon B_t\sum_m(u_{tm}+l_{tm})$, where the multiplier sums cover the three certificate sites. Taking the smallest quotient over the stored multipliers and nonzero denominators gives the fraction above. The [checker](check_coherent_circle_readout.py) recomputes every widened coefficient across all 496 rectangles. All four scale coefficients remain nonnegative, including at equality. At least one of the six diagonal gains must be positive because the figure has positive signal at the selected sites and a positive semidefinite response with both diagonals zero vanishes. The weighted sum is therefore strictly positive, contradicting the simultaneous band inequalities. The fraction is a certified lower bound. Whether it equals the smallest possible change is open.

## What to measure

For the fitted example, a fixed $\pi$ shift on one terminal rail changes the round-17 share at site 9 from about 0.148 to 0.736 after independently normalizing each setting. Across the five sites, total variation is 0.588 between the two phase settings. The balanced dephasing intervention gives 0.326 relative to the original at that round. Other admissible coherent fits can give different signs, sites and magnitudes. The proven bound concerns the **largest over the four rounds**, with total variation defined as half the sum of absolute changes in normalized site shares.

A prospective test would prespecify the four rounds, interleave equal-exposure terminal phase settings, verify that the phase operation preserves the separate rail intensities, and record unnormalized counts and exposure for every occupied site. Reconstruct the dephased distribution by pooling intensities from the two phase settings on a common exposure and gain scale, then normalize. Averaging separately normalized histograms can give a different distribution if the total detected intensity changes. Direct balanced dephasing with a separately measured histogram is an alternative. The exclusion uses figure-reading tolerances and supplies no statistical error model for that future measurement. Stage 1 Initial External Grounding and physical identification remain open.

Run `python -I -B Director_G/persistent_walk/check_coherent_circle_readout.py Fig7_asymmetricwalk_circle.png` with Pillow and PyMuPDF installed. It verifies the source digest, the launch and readout calculation, the earlier disk cover and the widened inequalities, and reproduces the recorded fractions.
