# One mixed launch fits both optical-circle displays

Kirtus Justus directed the research. OpenAI ChatGPT constructed the example, derived the input-scale test and checked the two published renderings. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A single localized mixed rail preparation, ten fixed analyzers and one increasing response curve can reproduce **all 200 cell bands** of the experimental panel of Fig. 7(c) of Lorz et al., in both the journal PDF and the authors’ PNG. The construction uses freely adjustable effective intensity scales and display normalizations in each round. This freedom matters. **Seven specified rounds must have pairwise different effective input scales** for this particular preparation and these analyzers, even if the normalization in every round is free. [Journal paper, pp. 3 and 8](https://physik.uni-paderborn.de/fileadmin-nw/physik/Arbeitsgruppen/integrierte-quantenoptik/publications/2019/PhysRevResearch.1.033036.pdf) · [Authors’ Fig. 7(c) PNG](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png)

## Construction and direct checks

Use the ideal balanced ten-site walk with both input rails localized at site 2. The rail density is $\rho=(I+\mathbf r\cdot\boldsymbol\sigma)/2$ in Pauli order $(X,Y,Z)$, with $\mathbf r=(1/2,-1/2,1/4)$. Its radius is $3/4$, its eigenvalues are $7/8$ and $1/8$, and its purity is $25/32$. At site $m$, take the time-independent analyzer $H_m=\left(\begin{smallmatrix}p&u+iv\\u-iv&s\end{smallmatrix}\right)/1024$ from the following table. Each numerator has positive leading diagonal and positive determinant, and its trace is at most 1024. These checks put every analyzer between zero and the identity.

| Site | $p$ | $s$ | $u$ | $v$ |
|---:|---:|---:|---:|---:|
| 0 | 98 | 27 | 34 | −35 |
| 1 | 480 | 229 | −87 | 140 |
| 2 | 25 | 58 | 24 | −27 |
| 3 | 692 | 33 | −147 | 11 |
| 4 | 84 | 84 | −40 | −72 |
| 5 | 206 | 211 | 206 | 20 |
| 6 | 96 | 42 | −33 | −13 |
| 7 | 11 | 442 | −26 | −58 |
| 8 | 52 | 38 | −12 | 41 |
| 9 | 485 | 9 | −56 | 12 |

For each round and site, propagate the two input columns to obtain $B_{tm}$ and calculate $x_{tm}=\operatorname{tr}(H_m B_{tm}\rho B_{tm}^\dagger)$. Intersect the journal’s four-unit CMYK bands and the PNG’s nine-unit RGB bands. These are two encodings of the same reported experiment. The bands describe a figure-reading rule. They supply no experimental confidence level. [Journal band derivation](Four_site_orders_in_the_journal_figure.md) · [PNG band derivation](Reading_the_ten_site_circle_figure.md)

Within each post-launch round, sort the ten latent intensities. Equal inputs share one output. Assign zero to zero input, then choose each positive output inside its intersected band, increasing by at least one millionth from the preceding distinct output. The checker first moves both edges of every positive-input band inward by $1/2048$. All 89 positive-input cells still admit this construction. The other 101 post-launch cells have zero intensity and contain zero in both renderings. Across the nineteen rounds, the sum of the ten selected displayed values ranges from $1157/2048$ to $1005/1024$. The remaining normalized mass can lie outside the displayed sites. No dynamics for that mass are inferred.

One curve $f$ serves every site and round. Write the displayed value as $q_{tm}=N_t f(a_t x_{tm})$, with positive effective input scale $a_t$ and normalization $N_t$. Scale each round’s positive inputs to lie strictly above the preceding round’s and do the same to its outputs before normalization. A common final rescaling places the highest response at $1/2$. Linear interpolation through the resulting 90 knots, including the origin, gives a strictly increasing response on the sampled interval. It can be continued above the last knot toward 1. Round zero needs no new knot. Only site 2 is occupied, so reuse the first positive input of round 1 and normalize its output to 1. All ten round-zero predictions lie in both original bands. The same pair of scale factors applies to every site within a round. [Interpolation algorithm](check_circle_response_curve.py) · [Full calculation and source checks](check_full_circle_display.py)

Under the same analyzers, replacing this launch by $I/2$ reverses the required directions at rounds 8 and 14. The earlier equal-mixture identity excludes every choice of static analyzers for that preparation. The earlier near-equal family fits four selected pairs. The smallest launch radius allowing the *entire* journal panel remains open. [Equal-mixture exclusion](Four_site_orders_in_the_journal_figure.md) · [Four-pair family and conditional slope bound](How_close_to_the_equal_launch_can_the_four_orders_reach.md)

## Why the input scale matters

Suppose rounds $t$ and $h$ used the same effective input scale. For two positive latent intensities with $x_{tm}\le x_{hn}$, monotonicity implies $q_{tm}/N_t\le q_{hn}/N_h$. The lower journal edge at $(t,m)$ divided by the upper edge at $(h,n)$ is then a lower bound on $N_t/N_h$. Reversing the latent order and using the opposite band edges gives an upper bound whenever the denominator is positive.

For example, between rounds 3 and 6 the comparison of sites 9 and 2 requires $N_3/N_6\ge27/26$. Comparing sites 1 and 6 requires $N_3/N_6\le73/82$. Between rounds 12 and 16 the corresponding bounds nearly meet, but $31/39>19/24$ by exactly $1/312$. All 21 round pairs from $\{3,6,8,10,12,16,18\}$ give a strict contradiction under a shared effective input scale. Thus at least seven distinct scales would be necessary for this witness, regardless of the shape of the common nondecreasing curve or the positive normalizations. As a control, rounds 1 and 6 yield only the upper bound $N_1/N_6\le 3/2$ from these positive-site comparisons and give no pairwise contradiction. A subsequent [power-setting construction](How_many_power_settings_fit_the_optical_circle.md) attains seven and determines how the minimum changes under specified round-trip loss. The calculation uses the original journal bands, before intersection or inward adjustment. [All 21 bounds and their site pairs](full_circle_display_output.json)

The authors report two initial power levels and normalization by round. The effective power incident on a given response stage can also depend on accumulated losses and gain. Two initial settings alone do not determine the nineteen effective scales. The journal caption identifies an optical input as $|ccV\rangle$ and specifies the launch position. Assigning the effective mixed state above to that optical preparation would require an independently checked map into the model rails. Recorded powers at the response stage, channel calibrations and state preparation measurements would constrain this example. The construction fits displayed position intensities and gives no derivation of the propagation or measurement laws. Stage 1 Initial External Grounding and physical identification remain open. [Experimental setup and Fig. 7 caption](https://doi.org/10.1103/PhysRevResearch.1.033036) · [Preparation conventions in the two source versions](Reading_the_ten_site_circle_figure.md)

Run the checker with Python, PyMuPDF and Pillow from the repository root.

`python -I -B Director_G/persistent_walk/check_full_circle_display.py lorz.pdf Fig7_asymmetricwalk_circle.png`
