# Four site orders in the published optical-circle figure

Kirtus Justus directed the research. OpenAI ChatGPT (Director G) audited the two renderings, derived the order identity and checked the controls. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

At round 8, sites 0 and 4 are both pure black in the preprint PNG. **The journal PDF gives them different native palette colors.** Its color scale places site 0 above site 4 under the extraction rule below. Combined with three other rounds, this reverses the scientific conclusion for one particular preparation. A fixed equal incoherent mixture and fixed analyzers can fit the PNG bands under a freely chosen monotone response. They cannot fit the four journal orders, even with a separate increasing curve in every round. The crucial assumptions are a common curve across the two sites *within* each round and the specified equal-mixture preparation. [Journal paper, Fig. 7(c), page 8](https://physik.uni-paderborn.de/fileadmin-nw/physik/Arbeitsgruppen/integrierte-quantenoptik/publications/2019/PhysRevResearch.1.033036.pdf#page=8) · [Authors’ PNG](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png) · [PNG construction](Calibrating_the_intensity_scale_of_the_optical_circle.md)

## What each rendering resolves

The journal's two panels have indexed CMYK palettes. The legend on the same page contains 249 filled CMYK strips spanning 256 equal vertical subdivisions. Some strips cover several subdivisions. For each cell the checker reads its stored palette entry and compares the four channel values, expressed on a 0–255 scale, with every legend strip. It takes the outer edges of every strip within a specified allowance of the nearest match, using maximum absolute channel difference. It also verifies the uniform center region in each cell and checks that the strip endpoints tile the legend. These calculations use the stored ink values before conversion to screen RGB.

We set the allowance using the numeric panel separately. Among integer allowances 0 through 4, **4 is the first that recovers all 200 ideal position probabilities** for the equal-mixture calculation, including parity zeros. At 3, it recovers 98/100 reachable and 100/100 unreachable cells. Using only the closest match gives 67/100 and 87/100. This control checks a way of reading a graphic. It supplies no frequency coverage for experimental error and cannot independently establish the numerical or experimental launch.

Changing the distance to the sum of the four absolute channel differences provides an independent sensitivity check on that choice of metric. Its first integer allowance covering the numerical control is 5. It yields the same four strict orders, with minimum gaps 2/256, 8/256, 9/256 and 24/256. Both readings use the same journal colors.

| Round | Dimmer site | Brighter site | Journal band, dimmer | Journal band, brighter | Minimum brightness gap |
|---:|---:|---:|---:|---:|---:|
| 2 | 0 | 4 | [53, 57]/256 | [58, 62]/256 | 1/256 |
| 6 | 0 | 4 | [29, 31]/256 | [39, 42]/256 | 8/256 |
| 8 | 4 | 0 | [13, 17]/256 | [24, 28]/256 | 7/256 |
| 14 | 0 | 4 | [26, 29]/256 | [53, 56]/256 | 24/256 |

At round 8 the experimental image contains palette index 15 at site 0 and 32 at site 4. Their stored CMYK bytes are (110, 227, 206, 170) and (136, 200, 180, 200). Both corresponding PNG cells have RGB (0, 0, 0), with the same nine-level band [0, 22/183]. Thus the two files resolve different amounts of ordering information from the same published experiment. Treating their readings as independent measurements would count that experiment twice.

## A four-round identity

Use the homogeneous balanced coin $(I-iX)/\sqrt{2}$ followed by opposite shifts on the ten-site circle. Launch the equal incoherent rail mixture at site 2. Let $x_{tm}$ be its unscaled intensity after a fixed positive Hermitian analyzer at site $m$. Put $D_t=x_{t4}-x_{t0}$. The walk gives the exact identity

$$
1545D_2+1648D_6-7444D_8+1280D_{14}=0.
$$

To check the identity, write the site transfer as $2^{-t/2}\left(\begin{smallmatrix}a&ib\\ic&d\end{smallmatrix}\right)$ with integer numerators. For the equal mixture and analyzer with diagonals $p,s$ and upper off-diagonal element $q+iz$, the intensity is
$$
x_{tm}=\frac{p(a^2+b^2)+s(c^2+d^2)-2z(ac-bd)}{2^{t+1}}.
$$
The real off-diagonal part $q$ drops out. Substituting the four exact transfers gives zero separately for each of the three analyzer coefficients at each of the two sites. No fit of the analyzers, similarity measure or rate calibration enters the identity. The [checker](check_journal_circle_order.py) constructs both input columns from the walk and checks all six zeros.

A common nondecreasing response within a round preserves the direction of any *strict* displayed difference when inferring the underlying order. This also allows common positive input-power and output-normalization factors that change by round. The journal bands at allowance 4 require all four contributions on the left to be strictly positive. At 5 they are still strict. At 6 and 7 the round-2 bands just touch. For a **strictly increasing** response, the resulting weak order at round 2 and the three remaining strict orders still contradict the identity. A response with a flat segment can hide a reversed pair under a displayed tie. At allowance 8 even the weak round-2 order is undetermined. The order argument alone gives no decision there.

**Preparation control.** Launch only the second input rail and take diagonal analyzer gains (1, 3) at site 0 and (5, 2) at site 4. In the directions shown in the table, the four unscaled brighter-minus-dimmer differences are $1/2$, $1/64$, $1/128$ and $1823/8192$. This other preparation gives all four orders with a linear response. These are order predictions only. Whether it fits all 190 journal bands with some common monotone response remains open. An independent launch record and a calibrated comparison between the site channels would be needed to interpret an apparatus test.

A [near-equal launch construction](How_close_to_the_equal_launch_can_the_four_orders_reach.md) now establishes how closely a different preparation can approach the equal mixture while retaining these same four orders.

## Which earlier claims survive?

- **Six linear scores.** Re-reading the journal at allowance 4 leaves all six original linear score upper bounds strictly negative. Their exact values in round order are −149/256, −467/256, −4383/256, −47/256, −1419/32 and −1943/256. This supports the same conditional exclusion of a common localized preparation and fixed linear readout on the ideal walk. It does not localize the failing assumption in the apparatus. [Six-round proof](Six_even_rounds_test_static_coherent_readout.md)
- **Sequential counting.** The 5% false-exclusion bound depends on the conditional score law and selection of the round before the draw. It uses no figure colors. The power budget does depend on the assumed future probabilities. Using these journal bands with the previously published weights, divisors and stopping rule gives **605,660 eligible outcomes** for at least 90% conditional power. The PNG calculation remains **1,714,991** under its own bands. Neither number counts a new experiment. [Sampling assumptions and shared-draw counterexample](A_counting_test_for_static_circle_readout.md)
- **Monotone response and saturation.** The 190-cell fit remains a verified construction for the specified PNG bands. It cannot establish a fit to the journal's indexed colors under the equal-mixture assumption. The earlier 3.98272% and 8.75927% sufficient ceilings depend on the PNG bands and specific Poisson readout models. Neither rendering supplies raw per-channel occupancy or dead-time records. [Detector assumptions and thresholds](Calibrating_the_intensity_scale_of_the_optical_circle.md)

Run `python -I -B Director_G/persistent_walk/check_journal_circle_order.py lorz.pdf Fig7_asymmetricwalk_circle.png` with PyMuPDF and Pillow. The checker pins both input files, calculates the orders and tests the polarized preparation. [Exact output](journal_circle_order_output.json)

The comparison leaves Stage 1 Initial External Grounding and physical identification open.
