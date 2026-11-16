# How many power settings fit the optical-circle figure?

Kirtus Justus directed the research. OpenAI ChatGPT derived the power bounds and checked the constructions against the two published renderings. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

Lorz et al. report two initial power levels, round-by-round normalization, and an interferometer round-trip efficiency of $63\pm3\%$. A previous reconstruction fits all 200 experimental display cells using a fixed rail preparation and fixed analyzers. Does it also fit with two initial powers once loop loss is included? **If the relevant intensity at the response stage retains between 60% and 66% at each round trip, the specified reconstruction needs exactly four initial power levels.** If the effective scale has no round-trip attenuation, the exact minimum is seven. Both minima allow arbitrary assignment of levels to rounds, a common increasing response and a separate positive normalization in each round. [Journal paper, experimental setup and Fig. 7(c)](https://physik.uni-paderborn.de/fileadmin-nw/physik/Arbeitsgruppen/integrierte-quantenoptik/publications/2019/PhysRevResearch.1.033036.pdf) · [Fixed preparation, analyzers and figure-reading rules](One_launch_fits_both_optical_circle_displays.md)

## The assumption about where loss acts

Keep the ten-site ideal walk, the launch at site 2 with Bloch vector $(1/2,-1/2,1/4)$, and the ten analyzer effects in the earlier construction. Their dimensionless site intensities are $x_{tm}$. Let $P_t$ be the initial power level used for round $t$, and let $C_t$ be a common transmission factor from launch to the input of the nonlinear response, with $C_0=1$. The model gives the display value

$$
q_{tm}=N_t f(P_t C_t x_{tm}).
$$

The response $f$ is common to all sites and rounds, $f(0)=0$, and the positive normalization $N_t$ is free in each round. The lower bounds hold even for a nondecreasing response. The constructions use a strictly increasing bounded one. The reported loop efficiency motivates the sensitivity calculation. Treating $0.60\le C_{t+1}/C_t\le0.66$ as a hard bound on every step at the nonlinear response input is an additional assumption. The report does not establish that bound for every round or for every loss in the detection chain. [Lorz et al., experimental setup](https://doi.org/10.1103/PhysRevResearch.1.033036)

## Why four powers are necessary with attenuation

If $P_t=P_h$ for $t<h$, write $R=C_h/C_t$. A site pair satisfying $x_{tm}\le R x_{hn}$ requires $N_t/N_h\ge l_{tm}/u_{hn}$, where $l,u$ are the original journal band edges. A second pair with the reverse latent order gives $N_t/N_h\le u_{tm'}/l_{hn'}$ for a positive denominator. Compare the first pair using the smallest allowed $R$, and the second using the largest. Both implications then hold for *every* permitted sequence of step transmissions, including sequences that vary from trip to trip.

| Rounds $t,h$ | Sites $m,n$ giving lower bound | At least | Sites $m',n'$ giving upper bound | At most |
|---|---|---:|---|---:|
| 3, 4 | 9, 8 | 27/16 | 5, 0 | 16/33 |
| 3, 5 | 9, 7 | 27/13 | 5, 9 | 16/33 |
| 3, 7 | 9, 3 | 27/22 | 5, 5 | 16/27 |
| 4, 5 | 0, 7 | 66/13 | 4, 9 | 41/22 |
| 4, 7 | 0, 3 | 3 | 4, 7 | 41/31 |
| 5, 7 | 9, 7 | 33/52 | 3, 5 | 14/27 |

In every row the lower bound exceeds the upper bound. Thus rounds 3, 4, 5 and 7 must all use different initial powers. Each inequality already follows from the journal reading alone. With $C_t=1$, the same calculation yields 21 conflicting pairs among seven rounds. [Earlier seven-round lower bound](One_launch_fits_both_optical_circle_displays.md) · [Exact site comparisons](circle_power_settings_output.json)

## Constructions attaining both bounds

Within each cell of the next table, one initial power serves all listed rounds. The grouping is the same for every permitted transmission profile in the attenuating case.

| Transmission | Groups of rounds sharing an initial power | Minimum |
|---|---|---:|
| $C_t=1$ | {0, 2, 3}, {5, 6, 17}, {4, 7, 8}, {9, 10, 15}, {11, 12, 13}, {1, 16, 19}, {14, 18} | 7 |
| Each step retains 60% to 66% | {2, 3, 9, 10, 16}, {4, 11, 13, 15, 19}, {0, 5, 6, 12, 14}, {1, 7, 8, 17, 18} | 4 |

To check a group, order its positive inputs $C_t x_{tm}$. For adjacent sites from rounds $t,h$, the comparison uses $C_h/C_t$. Its two extreme values come from raising the two per-step endpoints to $h-t$, with their order exchanged for a negative exponent. The strict ordering therefore holds for every permitted profile. The checker assigns each round a positive integer weight. In increasing input order, choose each response above the previous response and inside the weighted intersection of both display bands. Dividing by the corresponding round weight then recovers a value in both source bands. The round-zero launch site is fixed to 1. Every positive post-launch value lies at least $1/4096$ inside both bands, and the total displayed at each round is at most 1.

Multiply each group's input power until its whole positive input range clears the preceding group's upper bound. A separate positive multiplier on the response ordinates gives the same order across groups and is absorbed into $N_t$. Include the origin and interpolate the 91 knots. The checker scales the top ordinate to $1/2$. Above the final knot $(X,1/2)$ one possible continuation is $f(x)=1-1/[2(1+x-X)]$. The level choices and round weights can be kept fixed throughout the transmission interval. For each transmission profile the interpolation uses that profile's actual input coordinates. This establishes existence of a response for each profile. A single calibrated response valid simultaneously for all profiles would impose a further condition. [Exact construction and integer weights](check_circle_power_settings.py) · [Source renderings and prior tests](One_launch_fits_both_optical_circle_displays.md)

## A control with much stronger loss

Let $m_t$ and $M_t$ be the smallest positive and largest latent intensities in round $t$. Under constant retention $\eta$, every positive input in round $t+1$ falls below every positive input in round $t$ whenever $\eta<\min_{t<19} m_t/M_{t+1}$. For these analyzers the minimum is $534652/19857765$, about 0.0269241, from site 0 at round 18 and site 5 at round 19. For any positive retention below this value, **one** initial power suffices. Choose the response levels successively in reverse round order, retaining the same within-round display values and independent round normalizations. The checker evaluates the construction at half the limiting retention. At the endpoint, those two inputs coincide and this strict separation argument stops. The optimum one-power threshold could be larger. [Exact limits and replay](circle_power_settings_output.json)

These counts refer to the exhibited preparation and detector matrices. Free site-dependent loss, different analyzers, a different preparation, or a response measured elsewhere in the chain changes the inference. In particular the two reported initial powers cannot reproduce this specific fit under the stated transmission interval, even though the same model can fit the displayed probabilities when given four powers. The minimum over all preparations and detector choices remains unknown. A comparison with the actual instrument would require independent transmission, preparation and detector measurements. Stage 1 Initial External Grounding and physical identification remain open.

Replay with Python, PyMuPDF and Pillow from the repository root.

`python -I -B Director_G/persistent_walk/check_circle_power_settings.py lorz.pdf Fig7_asymmetricwalk_circle.png`
