# Which classical models survive a split readout of the five-site walk?

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), model comparison and finite-sample calculation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

Classical waves evolving by the same ten-mode linear walk reproduce the ideal single-port intensity. A second observation at the same stopping time can test how such intensities become individual detector records. Split every terminal rail into two paths and resolve the rail in each of two detector banks. In the model below, 61 fresh launches with 98% overall detection efficiency give joint power above **0.95169447** against two specified rival classes. This requires new readout hardware and an ideal single-excitation source. It is a prediction for a changed experiment. [Single-port timing design](Longer_single_port_timing.md) · [Classical-wave comparison](Return_at_one_port.md)

## Keep every launch

Use the 1,999,999 allowed half-durations and the scoring signs of the three-cosine sampler. Each terminal rail feeds a passive splitter with only one illuminated input. Preserve the rail labels at both outputs and record clicks at both banks in the same time window. For a timing success, use the original sign and the event that the launch rail has at least one click in either bank. For the additional success, exactly one of the two banks must register any click. Several clicks inside one bank still count as one occupied bank. Keep both-bank and empty records, all losses and every independently defined preparation. Choosing trials after a detection invalidates this comparison.

The first rival is the fixed homogeneous stochastic model with at most 55 states, including its clock and loss states. A fixed terminal detector gives a launch-rail click probability in $[0,1]$ for each hidden state. The existing timing-size bound therefore applies regardless of what the two banks report jointly. Isolation of the sampler and independent preparations are required. [Stochastic response bound](Real_readout_return_test.md)

The second rival allows a stochastic classical field with arbitrarily many modes and arbitrary intensity variation. Conditional on the field and the past, its two banks register independent Poisson photodetections. Require the larger integrated count rate to be at most twice the smaller in **each** launch. A per-rail bound covering all occupied modes supplies this condition after summing the rates. Arbitrary fields require this bound throughout the admitted input space. Independent dark counts can enter these rates if the same condition still holds.

Write $x=e^{-\lambda}$ for the zero-count probability of the weaker bank, and write $r\lambda$ for the stronger rate, with $1\le r\le2$. Two zero rates give no exclusive event. Otherwise the conditional probability of exactly one occupied bank is

$$x+x^r-2x^{r+1}.$$

For $x\le1/2$ this is maximized at $r=1$ and is at most $1/2$. For $x\ge1/2$ the maximum occurs at $r=2$. The remaining cubic $x+x^2-2x^3$ takes its maximum at $x=(1+\sqrt7)/6$, giving the sharp ceiling $(10+7\sqrt7)/54<0.528152948$. A fixed coherent intensity and twofold imbalance attain the analytic ceiling under this detector model. Exact balance instead gives the sharp bound $1/2$. Applying the conditional bound at every history stochastically bounds the exclusive count by a binomial upper tail, even when the incident classical intensity varies across shots.

## Two decisions on the same records

Reject the union of the two rivals only if both count requirements pass. For either rival, the probability of joint rejection is at most the probability of rejection by the test valid for that rival. This argument permits arbitrary dependence between the counts.

| Fresh preparations | Timing requirement | Exclusive-bank requirement | Timing size at most | Classical-field size at most |
|---|---|---|---:|---:|
| 57 | Above 38 timing successes, or at 38 with an independent 33/64 coin | At least 37 | 0.049623601473 | 0.043964218451 |
| 61 | At least 41 timing successes | At least 40 | 0.046301224319 | 0.030014243714 |

For the alternative, prepare one excitation on the original launch rail and propagate the ideal walk. Assume every terminal rail has the same total probability $\eta$ of recording its single excitation, independently of setting, output rail and prior trials. Model a miss as an empty record and assume no dark counts in this alternative. A detected excitation always occupies exactly one bank. Conditional on detection, the timing score has the original ideal success probability. Conditional on loss it succeeds with the negative-setting probability. Given $s$ detections in $n$ preparations, the timing score is the sum of independent $\mathrm{Bin}(s,p_{\rm ideal})$ and $\mathrm{Bin}(n-s,p_-)$ counts. The checker conditions on every $s$ meeting the exclusive threshold and sums the exact joint tail.

| Decision | Uniform terminal efficiency | Calculated joint power |
|---|---:|---:|
| 57 preparations | 0.99962 | below 0.949997594 |
| 57 preparations | 0.99963 | above 0.950002560 |
| 61 preparations | 0.97665 | below 0.949996337 |
| 61 preparations | 0.97666 | above 0.950001470 |
| 61 preparations | 0.98 | above 0.951694472 |

Here $\eta$ is uniform across stopping times. Accumulating per-tick loss correlates detection with the timing score and requires a different joint calculation.

## An instrument can manufacture exclusivity

Suppose both banks would independently miss with probability 0.01 under a bright coherent pulse. Shared electronics record only the first bank to fire. The reported exclusive probability becomes $1-0.01^2=0.9999$, exceeding the classical ceiling. Verifying the two-bank live time and retention of genuine coincidences is essential. Likewise, an illuminated second splitter input, unmeasured differential routing, or a preparation gate conditioned on detection can break the premises.

A classical model with continuous wave amplitudes and an additional corpuscular readout rule can also reproduce the entire ideal record. It evolves the classical amplitudes, samples one rail in proportion to intensity, chooses a bank using the splitter probabilities, and applies the same loss. That terminal rule enforces exclusivity by construction. These counts can test the specified independently photodetected classical fields and the finite-state stochastic class. They leave broader classical models, the physical origin of the probability rule and the candidate ontology open.

Grangier, Roger and Aspect measured anticorrelation at a beam splitter with a triggered source and observed interference in a separate arrangement. Sperling, Vogel and Agarwal analyzed sub-binomial statistics for on-off photodetection. Those studies motivate the additional record. Neither measured this five-site walk, these two banks or the stated timing isolation. [Grangier, Roger and Aspect (1986)](https://doi.org/10.1209/0295-5075/1/4/004) · [Sperling, Vogel and Agarwal (2012)](https://doi.org/10.1103/PhysRevLett.109.093601)

Run `python -I -B Director_G/persistent_walk/check_split_readout.py` from the repository root. The checker reads the single-port timing certificate, verifies the classical ceiling, evaluates the dependent count decisions and exercises the shared-electronics failure. [Executable](check_split_readout.py) · [Power and size bounds](split_readout_output.json)
