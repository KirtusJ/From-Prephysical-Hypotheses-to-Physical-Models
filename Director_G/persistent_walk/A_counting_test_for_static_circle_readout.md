# A counting test for static readout on the ten-site circle

Kirtus Justus directed the research. OpenAI ChatGPT (Director G) derived the counting test, selected the scores and checked the bounds. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A new experiment can test the fixed-detector explanation of the six even rounds with a prespecified stopping rule. Under the sampling conditions below, the chance of falsely excluding that model is at most **5%**, however often the experimenter checks the running scores. If future categorical probabilities fall within the specified Fig. 7(c) bands, **1,714,991 recorded outcomes** allocated as below guarantee at least **90% power**. The budget counts eligible outcomes. Optical loss and acquisition time determine how many launches are needed to obtain them. [Six-round model and figure comparison](Six_even_rounds_test_static_coherent_readout.md) · [Lorz et al., Fig. 7(c)](https://arxiv.org/html/1809.00591v2)

## What to record

Choose a round before an outcome is revealed. Record exactly one site from a stable categorical law for that round. Give sites 0, 2 and 4 the scores below and every other outcome score zero. The eligible population and the treatment of misses and multiple clicks must be fixed in advance. For example, conditioning on a single registered site is applicable when that registration samples the postulated intensity distribution up to a positive round normalization. Site-dependent censoring or count-rate-dependent registration needs a detector model of its own. An integrated intensity, or repeated readings of one stored event, do not supply fresh categorical draws.

For each round start a separate product at 1. On observing score $X$, multiply that round's product by $1-X/D$, using its divisor $D$ below. Record the first crossing of 20 and stop sampling that round if desired. Exclude the model only when **all six** products have crossed 20. Rounds can be interleaved. For the stated power, give each round its listed number of outcomes unless it crosses first. A round still below threshold at the cap leaves the model unresolved.

| Round | Site 0 | Site 2 | Site 4 | Divisor $D$ | Largest mean score in the design bands | Outcome cap |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1,165 | −406 | −247 | 131,072 | −343/61 | 371,103 |
| 4 | −5,661 | 513 | 2,826 | 786,432 | −1797/61 | 400,358 |
| 10 | −1,453 | 1,099 | 1,249 | 196,608 | −6967/732 | 245,999 |
| 14 | 0 | −802 | 943 | 131,072 | −2213/366 | 288,283 |
| 16 | 10,000 | 1,256 | −5,541 | 786,432 | −19973/366 | 203,536 |
| 18 | 1,604 | 0 | −656 | 131,072 | −1448/183 | 205,712 |

## Why checking during acquisition is valid

The null model launches any fixed, localized two-rail preparation into the ideal balanced ten-site walk. Each site has a fixed positive semidefinite coherent response. Each round has a free positive overall scale. With the round weights above, all eight leading principal minors of the three signed transfer matrices in the [six-round proof](Six_even_rounds_test_static_coherent_readout.md) are strictly positive. The same trace inequality therefore gives at least one round with nonnegative population mean score. The [exact results](circle_count_design_output.json) identify the three matrices by their leading minors.

Assume that for each selected round the conditional site probabilities, given all previous observations and scheduling decisions, equal that round's population probabilities. Fresh independent draws within and across rounds suffice. Fix a model and any one of its nonnegative-mean rounds. Its product starts at 1, has positive factors, and has conditional expected multiplier at most 1. It is unchanged when another round is sampled. Stopping this nonnegative supermartingale at the first crossing or any finite horizon gives a crossing probability at most $1/20$. Taking increasing horizons covers all later checks. A declaration needs a crossing in this particular round, even when its identity is unknown to the experimenter. This proves the global error bound without dividing the threshold probability among six rounds. [Waudby-Smith and Ramdas, bounded-mean betting processes](https://arxiv.org/abs/2010.09686)

## What the power calculation assumes

For the power calculation, the **conditional categorical probabilities** at the three sites in each round must lie in the experimental color bands read at nine added RGB levels. Treating displayed intensities as this exact probability scale is a design assumption. A sign survives an unknown round normalization, but the number of outcomes needed can change with the zero-score mass. The published figure supplies neither these future conditional probabilities nor a sample of the required size.

Write $w_m$ for the site scores and $p_m$ for their probabilities in one round. The expected reciprocal multiplier is
$$
r(p)=1+\sum_m p_m\frac{w_m}{D-w_m}.
$$
Its maximum $r_*$ on the box takes the upper probability endpoint at each positive score and the lower endpoint at each negative score. All six maximizing assignments admit a nonnegative zero-score remainder. Each gives $0<r_*<1$. By iterated conditional expectation, the expected reciprocal product after $n$ draws is at most $r_*^n$. To analyze early stopping, continue the sequence mathematically to its prespecified cap. If it has never crossed 20, its final reciprocal exceeds $1/20$. Hence the probability of missing the crossing is at most $20r_*^n$.

Choose $n=\lceil7.1/(1-r_*)\rceil$. Since $r_*^n\leq\exp[-n(1-r_*)]$ and $e^{7.1}>1200$, each miss probability is less than $1/60$. Summing over six rounds gives a total below $1/10$. No optimality of the scores, divisors or caps is claimed. For comparison, applying this same bound to the [original sign-test weights](even_circle_readout_output.json), using separately chosen divisors, gives **5,901,868,095** outcomes. Round 16 accounts for 5,795,620,271. Those weights had a small negative mean relative to the spread of single outcomes. The new weights preserve the transfer-matrix inequalities while improving that margin.

## A dependence control that makes the test fail

Use the ideal equal-mixture launch and equal detector efficiencies. Its round means include $53/2$ at round 2, as the null allows. Draw one uniform number on $[0,1]$ for the entire experiment. For each round, use its correct categorical distribution to map that number to a site, placing all negative-score sites first. Repeat the resulting site on every nominal draw of that round. Every single draw has the correct marginal distribution.

The six probabilities assigned to negative scores are $3/4$, $3/8$, $67/512$, $3449/8192$, $5763/32768$ and $70401/262144$. With probability at least **$67/512$ (13.09%)**, all six repeated scores are strictly negative. Even the slowest negative outcome in each round then crosses 20 by its cap. This exceeds the claimed 5% error under fresh sampling. Marginal histograms alone cannot validate the sampling condition.

Run `python -I -B Director_G/persistent_walk/check_circle_count_design.py Fig7_asymmetricwalk_circle.png` with the [authors’ image](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png), Pillow and PyMuPDF. The [checker](check_circle_count_design.py) verifies the positive minors, endpoint bounds, integer caps and repeated-draw control. The scores were selected using the existing figure. Only a fresh, prespecified acquisition can use this procedure to make the experimental decision. Stage 1 Initial External Grounding and physical identification remain open.
