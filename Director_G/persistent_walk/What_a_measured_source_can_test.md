# What a measured single-photon source can test in the five-site design

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), analysis of published observations and design calculations. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

Sekatski and colleagues measured a heralded light source with two detector outputs and reported a total signal efficiency of 62% at their highest transmission. Their Table 1 provides enough information to check a prediction of the split-bank field model against observations from that apparatus. Their inputs did not traverse the five-site walk. They acquired data in separate attenuation runs. A second calculation below asks how the walk experiment could operate at 62% efficiency if its own optical and timing conditions were met. [Published experiment, Eqs. (9), (26), (28) and Tables 1–2](https://doi.org/10.22331/q-2022-12-13-875) · [Authors' data archive](https://doi.org/10.5281/zenodo.7245446)

## An optical prediction that can be checked against the published table

Assign +1 when exactly one bank clicks, −1 when both click, and zero to an empty gate. Let the probabilities of an empty gate, left only, right only and both be $e,l,r,b$. The empirical mean score is $s=l+r-b$. Equation (9) of the paper gives two reported quantities, $4l+e-1$ and $4r+e-1$. Their arithmetic mean is exactly $s$. This algebra uses all heralds, including empty gates. It does not use a photon-number reconstruction.

Under the [conditional Poisson model](Split_readout_at_the_walk_output.md), suppose the banks are conditionally independent and the stronger rate is at most twice the weaker one for each admitted field. Let $x$ be the weaker bank's empty probability and $r_0$ the rate ratio. The expected score is $-1+2x+(2-3x)x^{r_0}$. For $x\le2/3$, equal rates give the largest value, at most $1/3$. For $x\ge2/3$, the maximizing ratio is two. The remaining cubic takes its maximum at $x=(2+\sqrt{22})/9$. The **sharp field ceiling is between 0.359581454 and 0.359581455**. An intensity mixture cannot raise it.

| Published total signal efficiency | Bank score from the two central estimates | Lower edge allowing 0.0005 decimal rounding | Published Eq. (28) statistic |
|---:|---:|---:|---:|
| 62% | 0.6195 | 0.6190 | 0.554 |
| 52% | 0.5165 | 0.5160 | 0.453 |
| 42% | 0.4205 | 0.4200 | 0.369 |

The rounding column describes the displayed estimates. Sampling uncertainty enters separately. For $n$ independently heralded trials with the model bound at each history and fixed sample size (or conditioning on an exogenous herald schedule), Hoeffding's one-sided bound for the mean bank score subtracts $2\sqrt{\log(1/\alpha)/(2n)}$. The authors' Eq. (28) subtracts **twice** that amount from the smaller of the two empirical Eq. (9) values. Consequently their displayed Eq. (28) statistic, even allowing 0.0005 for rounding, is below our score's one-sided lower confidence bound in each row. All three exceed the twofold field ceiling at the reported per-row $\alpha=10^{-10}$. A union bound over all three comparisons is $3\times10^{-10}$. This derives a bound for the observed bank score directly. The paper's own confidence statement concerns single-photon weight.

This retrospective comparison uses the published table and its declared acquisition model. The archive inventory includes time tags and count summaries grouped by attenuation. The time tags were not replayed here. Table 2 characterizes the efficiencies of the two paths. Path averages alone cannot establish the twofold rate bound for arbitrary untested modes or rule out shared electronics that erase coincidences. The comparison is conditional on those premises. It supplies external optical evidence, with no walk timing, rail-return or generator measurement.

## A five-site test at 62% terminal efficiency

At 62% efficiency and relative transmission 0.51 the [158-preparation design](Random_transmission_at_the_walk_output.md) has optical power below **0.003728** under the clean single-excitation model. Testing longer with its original score need not fix this problem. Its mean optical success is 0.6439888, below its field ceiling of 0.683392808. Changing the setting probabilities and the decision thresholds does fix it at this efficiency.

Use 2,500 fresh preparations with the existing timing sampler. Independently choose full transmission with probability $54/125$ after the incident field has been fixed. Otherwise use relative intensity transmission in $[0.49,0.51]$. Keep two counts across all preparations.

* Count full settings with any click, plus attenuated settings with an empty gate. Require at least **1,595**.
* Count full settings that pass the original signed launch-rail test. An attenuated setting contributes zero to this count. Require at least **639**.

The optical success probability under the field model is at most 0.621874655, obtained by the one-variable maximization in the linked attenuation note. The clean optical alternative has success probability at least 0.6562384. Multiplying the full-setting probability by the old timing null endpoint bounds the probability of a counted timing success under the finite-state rival. Under the alternative the corresponding lower bound is $(54/125)[0.62p_1+0.38p_-]$, including the negative-sign trials whose timing score succeeds on a miss.

| Quantity | Bound |
|---|---:|
| Field false rejection | < 0.049982270 |
| Timing false rejection | < 0.046710768 |
| Clean optical power | > 0.973518279 |
| Clean timing power | > 0.999725501 |
| Clean joint power | > 0.973243780 |

Each rival need only obey its own test. The joint lower bound adds the two marginal powers and subtracts one. The 62% here means uniform survival of one excitation across all stopping times and rails in the proposed walk with a background-free, correctly labeled first hit. The published source's 62% is a measured efficiency in a different apparatus. Transport loss can depend on duration. Establishing the walk power requires knowing that dependence or separately justifying uniform loss. A setting-aware source and a propagating amplitude with a corpuscular readout remain adverse cases.

## Where two empty-gate probabilities cease to distinguish the models

Let $\eta$ be the clean single-excitation efficiency, and $x=1-\eta$ its full-setting empty probability. For a field mixture whose full-setting empty mean is $x$, the largest possible attenuated empty mean is $x^{0.49}$ by concavity. At actual transmission 0.51 the single excitation gives the smallest empty probability allowed for that alternative, $1-0.51\eta$. Thus the two observed probabilities separate the entire field envelope uniformly over transmission precisely when
$$1-0.51\eta > (1-\eta)^{0.49}.$$
For positive efficiency the crossing lies between **0.147910776 and 0.147910777**. The difference is strictly convex, starts at zero with negative slope and ends positive. The checker verifies the bracket with integer powers.

Below the crossing the altered optical class has an actual imitation for positive efficiency. At field transmission 0.49, choose a mixture over full-setting empty probabilities with mean $x$. The constant choice gives the upper endpoint $x^{0.49}$. A mixture on $\{a,1\}$ with $0<a<x$, adjusted to the same mean, approaches lower endpoint $x$ as $a$ decreases to zero. The target $1-0.51\eta$ is strictly above $x$, so a finite choice of $a$ and a mixture with the constant law reproduce it exactly. At the crossing a single finite intensity suffices. This witness compares two allowed transmission values across the rivals. A common independently measured transmission tightens the comparison. The witness concerns empty-gate records only.

Run `python -I -B Director_G/persistent_walk/check_efficiency.py` from the repository root. The checker uses integer binomial masses and verifies the bracket and the four bank outcomes. [Executable](check_efficiency.py) · [Recorded endpoints](efficiency_output.json)
