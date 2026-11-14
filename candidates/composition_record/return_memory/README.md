# Does a recorded return reset the walk?

At one gate setting, the excitation was recorded at site 0 on tick two. A return on tick three occurred in 37.15% of shots whose first measurement was 0, and in 53.98% of shots whose first measurement was 1. These rates use the same apparatus, gate setting, clock and immediately preceding readout. The first recorded bit still predicted the third. Across the 99 settings, 26 showed a difference at a familywise 5% level under independent, identically distributed shots within each setting. [All 99 three-bit tables](three_ticks.csv)

## The reset prediction

Quancheng Liu, Sabine Tornow, David A. Kessler and Eli Barkai prepared one excitation in a three-site chain and repeatedly measured site 0. Within the ideal one-excitation sector, a true projective return has rank one. Its normalized post-measurement state is the excitation at site 0 for every history of positive probability that gives a return. For the archived gate order, the (1,2) rotations first leave that state alone. The (0,1) rotations then give the site-0 amplitude $\cos J$. With the same next step the subsequent true-return probability is $\cos^2 J$, independent of the previous history. The equality between histories needs no knowledge of $J$ if the reset state, next evolution and readout are common. The experimental test asks whether the **recorded** bit supplies such a reset for the next recorded outcome. [Experiment and measurement protocol](https://arxiv.org/html/2401.09810v2#S8) · [Source data](https://doi.org/10.5281/zenodo.18429670)

The histories are the first two chronological bits, 01 and 11. Both end in a recorded 1. Within each, the outcome is whether tick three is 1. This includes shots with earlier returns, which are needed to form the 11 group. It also counts every shot whose later records are all zero. In the source a raw string ends in the three bits in reverse time order. For example, the stored suffix `110` yields the chronological triple 011. The eight triples partition all 40,000 shots per setting. Rows in the CSV retain the four triples with middle bit 0 as well. We use a single clock across the complete angle sweep. [Source digest, read order and circuit validation](../first_return_data/README.md)

| QASM angle (radians) | Earlier bits | Tick 3 = 0 | Tick 3 = 1 | Tick-3 recorded return |
| --- | --- | ---: | ---: | ---: |
| 5.152211951887261 | 01 | 3,390 | 2,004 | 2,004 / 5,394 |
| 5.152211951887261 | 11 | 1,666 | 1,954 | 1,954 / 3,620 |
| π/2 | 01 | 161 | 1,510 | 1,510 / 1,671 |
| π/2 | 11 | 13 | 147 | 147 / 160 |

The first two rows are job `cxs87x74a290008xpvv0`, the 82nd sweep point (82π/50). It had the smallest two-sided p-value of the 99 comparisons. The gap in recorded return rates, 11 minus 01, was 0.16825509. At π/2, the gap was 0.01510, with unadjusted two-sided $p\approx0.672$. With perfect operations, that circuit moves the excitation from site 0 to 1 to 2 and back to 0. Both histories conditioning on a return at tick two have **zero** ideal probability at this angle. Their observed counts measure behavior on histories populated by experimental imperfections.

## What the differences establish

Under the null of one recorded tick-three probability for both histories, independent, identically distributed shots within a gate setting give a hypergeometric table conditional on the margins. The checker weights every table on that finite support by exact integers. Its two-sided Fisher p-value sums the probabilities of all tables whose probability is at most that of the observed one, including ties. The reported values round upward to seven significant digits. At setting 82 the p-value is at most $5.866950\times10^{-56}$, and at most $5.808280\times10^{-54}$ after adjusting for all 99 settings. No independence across gate settings is needed for the Bonferroni adjustment. Shot-order drift and inter-shot dependence cannot be diagnosed from these aggregate histograms.

The effect size also permits a simultaneous bound. With history denominators $n_0,n_1$, conditional Hoeffding bounds for the two-sample difference and a union bound over settings and signs give half-width $\sqrt{(1/n_0+1/n_1)\log(198/0.05)/2}$. At setting 82 this is 0.04373. The underlying signed difference is at least 0.12452 on the joint 95% confidence event, under the same independent-shot assumption.

This observation rejects a common **effective** recorded reset followed by a common recorded transition at those settings. It cannot locate the history dependence. For an explicit ordinary-probability model, suppose an unobserved sector persists through tick three and equally often takes either of two values. In both sectors let tick two report 1. In the first sector let ticks one and three report 1 independently with probability 0.2, and in the second with probability 0.8. The tick-three probabilities conditional on 01 and 11 are then 0.32 and 0.68. Clock-specific readout errors, state-preparation errors, population outside the one-excitation sector, or a drifting common cause can alter the composition of the two observed groups. The example establishes a possible explanation for a contrast, without fitting this device. The authors report representative readout and gate errors; these aggregate error figures do not calibrate the two history-conditioned preparations. [Experimental methods](https://arxiv.org/html/2401.09810v2#Sx1.SSx2)

One quantitative interpretation is available **if** both histories have the same clean next-return probability $p$ and at most a fraction $\epsilon$ of each history can have any other probability. Both observed population rates then lie between $(1-\epsilon)p$ and $(1-\epsilon)p+\epsilon$. Their absolute gap cannot exceed $\epsilon$; the bound is attained by assigning opposite deterministic outcomes to the contaminating fraction. The confidence bound above implies $\epsilon\geq0.12452$ at setting 82 *within this model*. This is a bound on composition within the two selected histories. A calibration on all shots averages over different histories. A direct-versus-split probability experiment would still need to check its own reset, control gates and resolved readout.

## Which outcomes does the walk actually score?

A nine-site walk with one fixed two-well detector and ten launch settings gives a common test for three hypotheses. Each launch can score the whole target, each site, or each oriented port, and its probability exponent can vary. Within that family, agreement with the ordinary population rates forces exponent one for every responsive mode except a set of probability zero. The construction assumes stable gains and an independently randomized choice of starting site and read time. The settings have yet to be measured. [Ten settings and full-domain interval certificate](three_grains.md) · [A single-clock test with a terminal switch](routed_resolutions.md)

## From this experiment to the signed walk

The archived jobs used different gate angles. A proposed fixed-angle experiment adds one phase after the second recorded miss. Three phase settings test a fixed exponent. Four can test a mixture with unknown common-sign gains. The signed walk supplies its own controls through translations of a sharp source, or through routed paths with a separately characterized selector. [Three phases](phase_cycle.md) · [Four phases for a mixture](four_phase_mixture.md) · [Five settings for mixed detector resolutions](mixed_order.md) · [Native signed-walk checks and rival](translated_mask.md) · [Routed two-rail preparations](native_odds.md)

## Companion tests

The first seven arrival bins resolve a classical memory bound at six gate settings. A pair of complementary angles also preserves the one-step site transition probabilities while changing the third-tick first-arrival rate. The memory proof and angle comparison state the extra assumptions each requires. [Finite classical memory](finite_memory.md) · [Complementary angles and a fixed-angle phase intervention](angle_pairs/README.md)

## Reproduce

Use the [first-return data adapter and instructions](../first_return_data/README.md) to generate `word_counts.tsv` from the pinned authors' JSON. Run the following from this directory with Python 3. The checker takes about five seconds here and creates a new output. It uses only standard-library integer arithmetic for the hypothesis tests.

```sh
python check.py word_counts.tsv rebuilt.csv
python -c "from pathlib import Path; assert Path('rebuilt.csv').read_bytes() == Path('three_ticks.csv').read_bytes()"
```

The derived CSV has SHA-256 `d66b6d74212e0cafdd872f03c8c71993ac646495c054ccbdea2c89a4ba42b542`. It regroups the authors' CC BY 4.0 histograms into chronological three-bit counts and adds conditional test results. [Original dataset and credit](https://zenodo.org/records/18429670) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
