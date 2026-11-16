# What can change the return on the far side of the optical circle?

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), reflection argument, source-figure analysis and exact calculation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

In Fig. 7(c) of Lorz et al., site 7 lies directly opposite the launch at site 2 on a ten-site circle. Under the authors’ effective homogeneous coin, **every rail state localized at the launch gives probability 41/64 at site 7 after nine rounds and 941/4096 after thirteen**. Both values fall inside the numerical panel’s color bands and above the corresponding experimental bands. Changing the launch polarization, even separately for each round, cannot bring the ideal predictions into those bands. The comparison concerns the position intensity summed over both outgoing rails. [Lorz et al., Eq. (13) and Fig. 7(c)](https://doi.org/10.1103/PhysRevResearch.1.033036) · [Earlier comparison of the two published preparation labels](Reading_the_ten_site_circle_figure.md)

## Why the input cancels

Measure displacement $x$ from the launch. One step applies $H'=(I-iX)/\sqrt 2$ to the rails and then shifts R one site forward and L one site backward. Here $X$ exchanges the rails. Spatial reflection $x\mapsto-x$ accompanied by $X$ commutes with each step. Let $B_x$ be the two-by-two matrix of amplitudes from the launch rails to the two rails at $x$ after any fixed number of steps. Reflection gives $B_{-x}=X B_x X$.

For a set of sites $O$ preserved by reflection, let $E_O=\sum_{x\in O} B_x^\dagger B_x$. The observed probability for a launch rail density matrix $\rho$ is $\operatorname{tr}(\rho E_O)$. Reflection gives $X E_O X=E_O$, so its diagonal entries are equal and its off-diagonal entry is real. Now inspect one outgoing rail. Paths ending in the same rail as their input have an even number of rail flips. Their amplitudes are real. Paths ending in the opposite rail have an odd number and their amplitudes are purely imaginary. Each summand in the off-diagonal entry of $E_O$ is therefore purely imaginary. The entry vanishes. Thus $E_O=p_O I$ for every round on every cycle with this coin and shift.

The origin is such a set by itself, as is the antipode on an even cycle. The sum at a pair of reflected sites also qualifies. Individual sites and individual output rails can retain preparation information. At round three, site 1 gives 1/8 or 5/8 for sharp R or L. At round nine, site 7 gives 81/128 or 1/128 in the **R output rail** for those two inputs. Summing both output rails gives 41/64 in either case. A sharp launch with complete rail dephasing after every coin gives a different benchmark on the same circle. Each step then chooses either direction with probability 1/2. The binomial walk gives 9/64 and 715/4096 at the antipode at rounds nine and thirteen.

## Two rounds with an internal intensity reference

Sites 5 and 9 form a reflected pair about launch site 2 modulo 10. Their **sum** supplies a second preparation-independent record at the same round. The intervals below use the published PNG’s color bar with eight RGB levels of additional tolerance above each cell’s closest match. For the pair, the two lower endpoints and the two upper endpoints are added separately. Displayed decimals are rounded outward. In particular, the black experimental cell at site 7 in round thirteen permits positive intensity up to 22/183. [Authors’ version-2 figure](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png) · [Exact readings and RGB values](fixed_site_return_output.json)

| Round | Position record | Ideal probability | Numerical panel | Experimental panel |
|---:|---|---:|---:|---:|
| 9 | Site 7 | 41/64 | 0.631–0.645 | 0.553–0.574 |
| 9 | Sites 5 and 9 combined | 49/256 | 0–0.241 | 0.165–0.296 |
| 13 | Site 7 | 941/4096 | 0.215–0.234 | 0–0.121 |
| 13 | Sites 5 and 9 combined | 699/2048 | 0.326–0.350 | 0.397–0.423 |

Suppose the intensity at a site is $q_{t,m}=k_t g_m p_{t,m}$, where $p$ is the ideal position probability, $k_t>0$ is an arbitrary common factor at round $t$, and $g_m>0$ is the site response summed over rails with equal sensitivity to both. The response model allows independent changes in total normalization at the two rounds. Assume also that the reference sites 5 and 9 have the same gain. Dividing site 7 by the reference sum then fixes the required relative gain

$$
\frac{g_7}{g_5} = \frac{q_{t,7}}{q_{t,5}+q_{t,9}}\,\frac{p_{t,5}+p_{t,9}}{p_{t,7}}.
$$

The round-nine colors require $g_7/g_5\ge 735/1312$ (about 0.560). The round-thirteen colors require $g_7/g_5\le 41008/91277$ (about 0.449). These limits exclude a single relative gain with that reference pair under the stated reading convention. Widening the color tolerance preserves the separation through 19 levels. At 20 levels the intervals first overlap. The simpler model with one fixed factor at site 7 alone and no round-dependent normalization requires factors in 0.863–0.896 and 0–0.524, respectively.

The authors describe normalization over all detected intensity in each step. For the circle they retain intensity that leaves the selected sites in the accounting. A common normalization cancels in the ratio above. Motion of intensity between particular sites and off-circle modes can change the ratio itself. The plot alone cannot distinguish that mechanism from unequal reference gains, rail-dependent response, spatial preparation error or a departure from the ideal evolution. The intervals describe digitization ambiguity. The selected rounds and sites were chosen by inspecting the figure, and the source supplies no shot-by-shot uncertainty for these cells. [Journal article, §II, §IV C and Fig. 8 caption](https://doi.org/10.1103/PhysRevResearch.1.033036)

A prospective test would fix the two rounds and three sites before collecting data, calibrate each site's rail-resolved response against the same reference, and record the counts in both rails, the off-circle intensity and the launch monitor at each round. Interchanging the readout channels between repeats would test whether the discrepancy follows a detector or a site. The ideal preparation invariance can then be tested directly by varying the localized launch rail state. Stage 1 Initial External Grounding and physical identification remain open.

With Pillow and PyMuPDF installed, run `python -I -B Director_G/persistent_walk/check_fixed_site_return.py Fig7_asymmetricwalk_circle.png` from the repository root. The [checker](check_fixed_site_return.py) verifies the image digest, computes each reflected-set probability operator on cycles of 3 through 12 sites for rounds 0 through 24, and replays the gain bounds against the source pixels.
