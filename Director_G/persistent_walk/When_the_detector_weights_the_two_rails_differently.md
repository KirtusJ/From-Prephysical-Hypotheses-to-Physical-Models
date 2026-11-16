# When the detector weights the two rails differently

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), model construction and source-figure analysis. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A detector model with separate fixed gains for the two outgoing rails at each site reproduces every displayed cell of rounds 1, 11 and 13 in the experimental panel of the ten-site optical walk. It uses a single sharp R launch and the ideal evolution throughout. Adding **round 7** rules out every such choice of fixed gains for that launch. For a real diagonal launch or an equal incoherent mixture, rounds 11 and 13 already suffice to rule out the model. These results use the eight-level color tolerance defined in the [source-figure comparison](Reading_the_ten_site_circle_figure.md). [Lorz et al., Eq. (13) and Fig. 7(c)](https://doi.org/10.1103/PhysRevResearch.1.033036)

## A fixed set of gains that fits three rounds

Write $p_{t,m,R}$ and $p_{t,m,L}$ for the two outgoing rail probabilities at site $m$ after round $t$. Launch at site 2, apply the homogeneous coin $(I-iX)/\sqrt2$, then shift R forward and L backward on the circle. The record model is

$$q_{t,m}=k_t\left(g_{m,R}p_{t,m,R}+g_{m,L}p_{t,m,L}\right).$$

The gains are positive and fixed across all rounds. The common scale $k_t>0$ can vary by round. The [earlier three-site test](Testing_three_unequal_circle_detectors.md) required $g_{m,R}=g_{m,L}$ at each site. The following construction tests the consequence of relaxing that assumption. Only odd sites carry intensity at the three rounds in question.

| Relative gain | Site 1 | Site 3 | Site 5 | Site 7 | Site 9 |
|---|---:|---:|---:|---:|---:|
| R | 1279 | 1046 | 6422 | 296 | 922 |
| L | 904 | 175 | 1071 | 1771 | 5448 |

Use $k_1=1/1000$, $k_{11}=1/1633$ and $k_{13}=1/1441$. The common unit of gain is arbitrary. The table below gives the resulting intensities rounded to four decimals. The comparison with the color bands uses exact fractions.

| Round | Site 1 | Site 3 | Site 5 | Site 7 | Site 9 | Total on the circle |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.4520 | 0.5230 | 0 | 0 | 0 | 0.9750 |
| 11 | 0.1541 | 0.0469 | 0.2641 | 0.2442 | 0.1582 | 0.8675 |
| 13 | 0.3229 | 0.0021 | 0.2291 | 0.0923 | 0.1808 | 0.8272 |

All fifteen entries fit their own experimental color bands. The other fifteen cells also admit their predicted zero values. The authors retained light outside the displayed circle in their normalization. The construction fits the displayed on-circle fraction and leaves the missing intensity and its origin unspecified. It makes no claim to reproduce the paper's internal-state-resolved similarity or the separate numerical panel. [Original figure](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png) · [Exact predictions](rail_dependent_circle_output.json)

## Why round 7 breaks the fit

For two rounds $s,t$ at the same site, the ratio of the gain-weighted rail sums is a weighted average of $p_{t,m,R}/p_{s,m,R}$ and $p_{t,m,L}/p_{s,m,L}$ whenever the earlier rail probabilities are positive. The later-to-earlier ratio of displayed intensities is that average times the **same** $k_t/k_s$ at every site. Dividing a lower observed intensity ratio by the larger rail ratio gives a lower bound on $k_t/k_s$. Dividing an upper observed ratio by the smaller rail ratio gives an upper bound. The exact input- and round-specific contradictions are as follows.

| Launch and gain condition | Rounds | Site giving lower bound | Required lower bound | Site giving upper bound | Allowed upper bound |
|---|---|---:|---:|---:|---:|
| Sharp R, arbitrary positive rail gains | 7, 13 | 5 | 4008/2527 ≈ 1.5861 | 7 | 68992/92781 ≈ 0.7436 |
| Real diagonal or equal incoherent mixture, arbitrary positive rail gains | 11, 13 | 9 | 992/1025 ≈ 0.9678 | 7 | 49456/83749 ≈ 0.5905 |
| Sharp R, larger/smaller rail gain at every site at most 23/4 | 11, 13 | 5 | 1080824/945459 ≈ 1.1432 | 9 | 1208704/1061105 ≈ 1.1391 |

For example, the sharp launch gives rail probabilities $(25,9)/128$ at site 5 in round 7 and $(361,361)/8192$ in round 13. Even putting all weight on the rail with the larger relative increase cannot accommodate the displayed site-5 change with the scale allowed by site 7. The round-7 bounds stay disjoint through 46 added RGB levels. The diagonal-input bounds stay disjoint through 31. The final row restricts the gain ratio at each site. Its two endpoint values suffice because the ratio of two positive linear functions of $g_{m,R}/g_{m,L}$ is monotone or constant. Its narrow separation lasts through nine levels. At eight levels the sharp-launch contrast required for rounds 1, 11 and 13 is thus **greater than 5.75 and at most 6422/1071**, about 5.9963. The upper limit comes from the explicit construction.

A rail-by-rail calibration at sites 5, 7 and 9, an independently recorded launch rail, and fixed-in-advance observations at rounds 7, 11 and 13 would directly test these alternatives. The gains were chosen after inspecting the figure. The color bands quantify reading ambiguity, and no count uncertainty or detector gains were measured here. Other launch states, time-varying response, additive backgrounds and dynamics that move intensity among sites require separate checks. Stage 1 Initial External Grounding and physical identification remain open.

With Pillow and PyMuPDF installed, run `python -I -B Director_G/persistent_walk/check_rail_dependent_circle_response.py Fig7_asymmetricwalk_circle.png` from the repository root. The [checker](check_rail_dependent_circle_response.py) matches the input digest, calculates both rail probabilities, reads the source pixels, checks the positive construction and reproduces all three bounds.
