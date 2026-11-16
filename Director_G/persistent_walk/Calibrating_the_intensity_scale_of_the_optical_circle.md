# Calibrating the intensity scale of the optical circle

Kirtus Justus directed the research. OpenAI ChatGPT (Director G) constructed the response example and derived and checked the saturation bounds. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

**The preprint PNG’s intensity ordering alone cannot exclude a fixed optical walk and fixed analyzers.** One equal-mixture launch and ten fixed positive analyzers reproduce all 190 site bands in rounds 1–19 of the experimental ten-site PNG panel if the response curve is allowed to be any strictly increasing function and both incident power and displayed normalization are free each round. A calibrated on/off response gives a different result. For a single ideal Poisson on/off channel per site, the six-round sign test still excludes the fixed model if round 4's brightest measured site clicks on at most **8.75927%** of trials. With multiple channels read separately and then summed, a sufficient occupancy ceiling is **3.98272% per channel** across the six rounds. These are bounds on raw click probabilities. Figure colors alone do not measure them.

Lorz et al. report combining acquisitions at two input powers to handle early saturation and late signal loss. They resolve internal channels and normalize each round's total intensity. The plotted circle can lose light to other positions. Their description motivates checking the response assumption but does not supply the per-channel occupancies for the selected bins. The arbitrary response and free powers in the first construction give more freedom than the reported two-power protocol. [Lorz et al., Secs. II and IV.3, Fig. 7(c)](https://arxiv.org/html/1809.00591v2) · [Previous six-round test and exact scores](A_counting_test_for_static_circle_readout.md)

The journal PDF retains a brightness difference where the PNG maps two sites to black. Four journal site orders exclude this equal-mixture explanation under the stated CMYK extraction. [Comparison and preparation control](Four_site_orders_in_the_journal_figure.md)

## What survives if only the ordering of intensities is calibrated?

Use the homogeneous ten-site walk with coin $(I-iX)/\sqrt{2}$ and the two opposite shifts. Launch the equal rail mixture at site 2. Let $B_{tm}$ be the transfer to site $m$ in round $t$. The ideal analyzer output is $x_{tm}=\operatorname{tr}(H_mB_{tm}B_{tm}^{\dagger})/2$. Each fixed Hermitian matrix has the form $H_m=\left(\begin{smallmatrix}p&iz\\-iz&s\end{smallmatrix}\right)$. The entries below give a constructive fit. All satisfy $p>0$ and $ps>z^2$. A common rescaling can put every effect below the identity and be absorbed into incident power.

| Site | $p$ | $s$ | $z$ | Site | $p$ | $s$ | $z$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 156 | 184 | −141 | 5 | 533 | 551 | −35 |
| 1 | 229 | 744 | −56 | 6 | 345 | 144 | −80 |
| 2 | 1 | 264 | 0 | 7 | 469 | 1 | 0 |
| 3 | 764 | 49 | −191 | 8 | 108 | 263 | 33 |
| 4 | 224 | 430 | −281 | 9 | 220 | 666 | −185 |

In each round, sort sites by $x_{tm}$, grouping ties. Fix zero at zero. For each positive input choose the largest of the group's lower band endpoints and the preceding output plus $10^{-6}$. The checker verifies that every chosen output $y_{tm}$ stays below all upper endpoints in its group. The sums over the ten sites range from 0.3292 to 0.9727, rounded. The check includes the sites that are unreachable by parity.

A *single* bounded curve serves the entire construction. For each successive round choose $a_t>0$ so every positive $a_t x_{tm}$ exceeds the preceding round's largest argument. Likewise choose $b_t>0$ to put the positive $b_t y_{tm}$ above the preceding values. Divide all these output coordinates by twice their overall maximum $K$. The resulting 90 distinct knots, including $(0,0)$, lie in strictly increasing order. Interpolate linearly between them and extend monotonically above the last knot $(X,1/2)$, for example by $1-1/[2(1+x-X)]$ for $x\ge X$. The common curve $f$ gives $y_{tm}=(2K/b_t)f(a_t x_{tm})$ at every cell. It is a fit to the published bands at nine added RGB levels. Its normalization, power sequence and curve shape are unmeasured. Locked exposures or an independently measured curve would test additional restrictions.

## What changes with Poisson on/off registration?

Suppose the detected arrivals at fixed illumination are Poisson with mean $I$ and a live, ideal on/off channel returns a click with probability $c=1-e^{-I}$. With efficiency absorbed into $I$, the linear intensity is $L(c)=-\log(1-c)$. Finite dead time between gates, pulse-to-pulse power variation, dark counts and subtraction require separate checks. The basic no-click formula follows by averaging $(1-\eta)^n$ over Poisson photon number. [Zambra et al., Eq. (1)](https://doi.org/10.1103/PhysRevLett.95.063602)

In the [fixed-readout proof](Six_even_rounds_test_static_coherent_readout.md), the signed transfer matrices for the [counting-test weights](check_circle_count_design.py) are positive definite. Therefore the six round scores of the **linear** intensities cannot all be negative, even after separate positive round scalings. Let $P_t$ sum the positive weighted upper band endpoints and let $N_t$ sum the absolute negative weights times their lower endpoints. The smallest $N_t/P_t$ over all six rounds is $59755/58557$, at round 4.

**Separate channels.** Suppose a displayed site value is proportional, by a common round factor, to the sum of raw channel click probabilities. The corresponding linear site signal is the sum of $L(c)$ over those channels. If every contributing channel has $c\leq b$, then $c\leq L(c)\leq c L(b)/b$ by convexity. After the same scaling the signed linear score is at most $P_t L(b)/b-N_t$. Thus all six scores remain strictly negative if $L(b)/b<59755/58557$. Its crossing lies between 0.0398272 and 0.0398273. This sufficient bound permits different occupancy patterns across the channels.

**One pooled channel per site.** Now $c_m=u_t q_m$ for displayed site value $q_m$ and a common unknown positive scale $u_t$. In rounds 2, 10, 14, 16 and 18 every negative-score site has a lower band endpoint at least as large as the biggest positive-score upper endpoint. The monotone factor $L(c)/c$ therefore gives at least as much relative weight to the negative terms as to the positive terms. All five scores stay negative at every admissible occupancy below one.

In round 4, site 4 is the brightest of the three scored sites throughout their bands. Fix its raw occupancy $b=c_4$. The signed score is bounded above at
$$
(q_0,q_2,q_4)=(95/366,\ 22/183,\ 119/244).
$$
Decreasing $q_0$ and increasing $q_2$ maximize the score at fixed $q_4$. Increasing $q_4$ also increases the score at fixed $b$, because $q_0>q_2$ and $5661q_0>513q_2$, so shrinking $bq_0/q_4$ removes more negative weight than shrinking $bq_2/q_4$ removes positive weight. Put $u=b/q_4$ at this corner. The limiting equation is
$$
-5661 L(uq_0)+513 L(uq_2)+2826 L(uq_4)=0.
$$
The coefficient of $u$ is negative. All coefficients of $u^n$ for $n\ge2$ are positive since $2826q_4^2>5661q_0^2$ and $q_4>q_0$. Dividing by $u$ yields a strictly increasing series, with a unique crossing as $uq_4$ approaches one. Rational enclosures of the logarithms put the crossing **between 0.0875927 and 0.0875928** in $b$. Above the upper endpoint, this allowed round-four assignment reverses the sign. Whether the complete six-round physical model fits there remains open.

## An acquisition that distinguishes the assumptions

Record the number of live trials and misses for **each channel and site**, including the input-power setting, before normalizing any round. Independent calibration pulses at intensities $I$ and $2I$ predict $c(2I)=2c(I)-c(I)^2$ in the ideal model. A failure of this relation would invalidate that response assumption in the tested range. A match at one pair of powers leaves the rest of the response curve unresolved. For a finite acquisition the occupancy ceiling needs a statistical upper bound and an error allowance shared with the sign test. The percentages above are population bounds.

The [checker](check_circle_response_curve.py) rebuilds all 190 bands from the [authors’ image](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png), verifies the common curve and the transfer minors, and brackets both thresholds using exact fractions. Run `python -I -B Director_G/persistent_walk/check_circle_response_curve.py Fig7_asymmetricwalk_circle.png` with Pillow and PyMuPDF. [Recorded output](circle_response_curve_output.json)

The construction and the two thresholds describe distinguishability under stated observation laws. The apparatus response, physical identification and Stage 1 Initial External Grounding remain open.
