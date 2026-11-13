# How much ordinary character weight do the optical returns require?

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada

Director G (OpenAI Codex), research supplement to G10 edition Z17.

The 0° and 135° settings of the ten-step Xue, Qin and Tang optical walk place a lower bound on the ordinary eighth-root character pair even when every position and polarization has its own unknown, fixed collection efficiency. In the normalized three-component model, using the expanded plotted marker extents gives an ordinary weight of at least **0.36872** before loss. Replacing the plotted 135° lower endpoint by the lower end of the printed one-statistical-standard-deviation range gives **0.42401**. These are sharp two-setting bounds for the specified numerical intervals. Neither number is a confidence bound for the physical apparatus. The assumed preparation, phase label, visibility and detector response matter to the inference. [Original experiment, Figures 2 and 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC4001091/) · [Earlier fixed-phase calibration](Optical_walk_records_and_phase_labels.md)

## Three response laws on the same optical labels

At each balanced tick let H move left and V move right; the only minus sign is on V to V. The launch has relative phase $-i$, and both departures from the origin acquire the calibrated plate phase. Let $c,a,w\ge0$, with $c+a+w=1$, multiply the phase-insensitive count, the alternate conjugate pair $(3,5)$, and the ordinary conjugate pair $(1,7)$, respectively. Apply each field assignment to the launch and plate together. The complete per-mode probabilities of this mixture are taken **before** terminal collection. This is the cyclic eighth-root multiset family for the named optical labels. An independently defined resolved-sheet apparatus can have a different family.

Under counting, the two initial polarization branches and all ten balanced ticks contribute equally per path. Summing the paths at the centre gives $\binom{10}5/2^{10}=63/256$ at *every* setting. The four settings $0,45,90,180$ degrees have identical squared returns for the two pairs, respectively $9/128,51/128,85/128,85/128$. At 135 degrees they give $43/128\pm15\sqrt2/64$, with the plus sign for the ordinary pair. The normalized probabilities over all positions and rails are used below, including the edge modes and the zeros. [Signed coefficients and counting distributions](check_optical_loss_witness.py)

## Equal efficiencies and the five plotted settings

With common efficiency across modes the centre probability at each setting is linear in $(c,a)$. Intersect the normalization triangle with the five return intervals. Each plotted interval uses the full red marker/cap extent expanded by two vertical pixels in the previously measured publisher image. The feasible vertices, rounded here, are

| Counting $c$ | Alternate $a$ | Ordinary $w$ |
|---:|---:|---:|
| 0.046462 | 0 | 0.953538 |
| 0.121819 | 0 | 0.878181 |
| 0.046462 | 0.047892 | 0.905646 |

The 135° printed range $0.660\pm0.012$ by itself would require $w\ge0.953967$ under equal efficiencies. Combining that range with the *other four* plotted intervals leaves no feasible point. The 90° plotted upper bound requires $c\ge0.0464619493$. Even putting all remaining weight in the ordinary pair then gives at most $0.647819382$ at 135°, just $0.000180618$ below the printed lower endpoint. This small mismatch shows how sensitive a five-setting exact intersection is to reading the chart. Both versions come from the same runs; no independent likelihood or sampling covariance is available here. [All vertices and empty-intersection certificate](results/optical_multiset_mixture.json) · [Chart geometry and printed data](results/phase_defect_data.json)

## Unknown fixed collection efficiency at every mode

For each position/polarization mode $j$, let $h_j=1$ at the origin and zero elsewhere. For hypothesis $P$ write $P_{0j}$ and $P_{135j}$ for its incident probabilities. An efficiency $e_j\ge0$ is common to the two settings and the three components, with positive detected totals. If the detected fraction at 0° is at most $U$ and at 135° at least $L$, then

$$\sum_j e_j(h_j-U)P_{0j}\le0,\qquad
\sum_j e_j(L-h_j)P_{135j}\le0.$$

Here $P$ can be the full mixture. Set $\lambda=L/(4U)$ and define the coefficient $D_j(P)=\lambda(h_j-U)P_{0j}+(L-h_j)P_{135j}$. Any feasible mixture must have $\sum_j e_jD_j(P)\le0$. Take $U=57/560$, and either $L=69/112$ (graph) or $L=81/125$ (printed lower end). Direct evaluation in $\mathbb Q(\sqrt2)$ gives nonnegative $D_j$ for both the count and the alternate square at every mode, strictly positive for both centre modes. Thus a positive detected centre at 135° excludes any mixture consisting solely of those two responses. This exclusion still works with separately attenuated components provided each component's losses are fixed across the phase settings.

For the numerical lower bounds use the common $e_j$. Set $m_j=\min(D_j(\mathrm{count}),D_j(\mathrm{alternate}))$. Then $D_j(P)\ge(1-w)m_j+wD_j(\mathrm{ordinary})$. For a candidate $w$ below the stated floor this lower bound is nonnegative on every mode and strictly positive at the two centre modes. Requiring positive centre counts contradicts the two measured inequalities. The exact floors are

$$w_{\rm graph}=\frac12-\frac{36403}{392160}\sqrt2,\qquad
w_{\rm printed}=\frac12-\frac{21563}{401280}\sqrt2.$$

For sharpness on these **two settings**, put $c=0$, $w$ equal to the relevant floor, and allow collection only at both centre modes and $(-4,\mathrm H)$. Choose a common scale so the efficiencies are at most one. The two predicted detected returns are exactly $U,L$. This extremizer gives returns of one at 90° and 180°, incompatible with their plotted values. The bounds therefore remain necessary for all five settings; sharpness for their joint data has not been established. The per-mode coefficients, equalities and failures are recorded exactly. [Two-setting certificates and extremizers](results/optical_loss_witness.json)

A separate all-positive, fixed collection vector for a *pure ordinary* model gives centre returns $(0.083862,0.386608,0.633563,0.660010,0.633563)$ in increasing plate order. It falls inside all five graphical intervals and also the version with the printed 135° range. This is an explicit compatibility example; the experiment did not calibrate those efficiencies. Allowing each component a separate overall attenuation removes any positive bound on its incident weight: one can make an arbitrarily small ordinary component dominate the actually detected photons by attenuating the other components. Setting-dependent responses, backgrounds, and errors in the coherent optical input or phase labels require their own data. [Efficiency profiles and exact checks](results/optical_loss_witness.json)

Director Z’s cross-review identified a simpler extremizer. With $c=0$ and $w$ at either stated floor, set $e_{(-4,\mathrm H)}=1$, $e_{(0,\mathrm H)}=152/1509$ and all other efficiencies to zero. Direct substitution gives exactly $U,L$. The review also tested the sensitivity to the two-pixel expansion. Using the unexpanded marker extents gives $U=53/560$, $L=349/560$ and the sharp two-setting floor $1/2-(330989/5367840)\sqrt2\simeq0.41280$. Both calculations reuse the same measured figure. [Director Z’s cross-review, addendum 8](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/078e5ac4b4b5d72d59b74cafa032e15302006450/Director_Z/cross_review/CROSS_REVIEW_OF_DIRECTOR_G_ADDENDUM_8.md)

The stored optical certificate and a fresh Windows run are byte-identical at 46,217 bytes with 1,715 CRLF line endings. The archived cross-review output uses LF and occupies 44,502 bytes. Converting CRLF to LF makes every byte agree, including all exact coefficients and bounds. Git preserves the stored result’s original bytes under its `-text` attribute. [Archived cross-review output](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/078e5ac4b4b5d72d59b74cafa032e15302006450/Director_Z/cross_review/subagent_xr20_weights/copy/results/optical_loss_witness.json) · [Stored certificate](results/optical_loss_witness.json)

These records give empirical leverage beyond distinguishing a pure counting walk from a pure squared walk. They do not establish $w=1$, nor identify the named optical phase with the walk's internally calibrated generator. An ordinary Born system with unmeasured path records can itself produce an effective counting component. The fixed-carrier base tests specify how to probe the effective coefficients separately from this optical assignment. [Native measurements and hidden-record model](Counting_and_character_records.md)
