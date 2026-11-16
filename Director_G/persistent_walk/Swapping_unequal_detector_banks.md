# Swapping two detector banks of unequal efficiency

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), counting bound and calibration design. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A polarizer sends light to two detectors with different efficiencies. A pulse aligned with the more efficient output can then raise the chance of any detection. This breaks the common-throughput premise of the [random-axis polarization test](Changing_the_polarization_analyzer.md). An independent optical swap on each preparation restores a useful bound. At 10% average single-excitation efficiency, a triad of analyzer axes can tolerate a 3:1 bank-efficiency ratio and still distinguish the stipulated Poisson fields with 2,794 preparations and both errors below 5%.

## Which randomization compensates for unequal banks?

Choose one of three orthogonal analyzer axes uniformly. Independently choose a fair swap that exchanges the two optical paths *before* detection. Keep both bank bits, axis and swap on every preparation, including empty gates. The source must commit its incident field before either choice. Assume fixed, linear bank efficiencies $g_A,g_B$ over the occupied modes and rates, with independent conditional Poisson counts. The swap must preserve transmission apart from routing the paths. A software relabeling of two already recorded bits cannot compensate for physical loss.

Let $\epsilon=(g_A-g_B)/(g_A+g_B)$ and let $\Lambda$ be the incident Poisson intensity times the mean efficiency. For a unit analyzer axis $a$, put $x=a\cdot s$ for the normalized classical Stokes vector, with $|s|\le1$. The two mean bank counts in one routing are $\Lambda(1+\epsilon)(1+x)/2$ and $\Lambda(1-\epsilon)(1-x)/2$. For the reverse routing, replace $x$ by $-x$. Thus the probability $T$ of any click averaged over the swaps is
$$
T=1-e^{-\Lambda}\cosh(\Lambda\epsilon x)\le 1-e^{-\Lambda}=2y-y^2,
\qquad y=1-e^{-\Lambda/2}.
$$
This upper bound holds even for an axis aligned with the input. On that axis a pulse directed only to the more efficient bank without the swap would exceed the bound.

Write $F(u)=1-e^{-u}$ and $u_\pm=\Lambda(1\pm\epsilon)/2$. For each sign of $x$, the double probability is $F(u_+(1+x))F(u_-(1-x))$. The arithmetic mean of the two routed double probabilities is at least their geometric mean. For each $u\ge0$,
$$
F(u(1+x))F(u(1-x))\ge(1-x^2)F(u)^2,
$$
by the even-series bound for $\cosh(ux)$ in the random-axis analysis. Grouping the four factors by bank therefore gives a swap-averaged double probability of at least $(1-x^2)F(u_+)F(u_-)$. Applying the same inequality again, now with $u=\Lambda/2$ and $x=\epsilon$, gives
$$
\overline D\ge m(1-\epsilon^2)y^2,\qquad
m=1-\lambda_{\max}\!\left(\sum_j p_j a_j a_j^{\mathsf T}\right),
$$
after averaging over the axes. The uniform orthogonal triad has $m=2/3$. The loss of the factor $1-\epsilon^2$ is sharp to leading order at low intensity for an input along an axis of the triad. Then two axes have $x=0$ and one has $|x|=1$. At finite intensity the bound is conservative. The same proof uses a separately calibrated lower bound on $m$ if the axes are imperfect.

A clean single excitation routed to either output has mean detection efficiency $(g_A+g_B)/2$ after the fair swap, times any common source and path throughput. Its double probability is zero. Pulse polarization can vary independently of the current analyzer and swap. The finite power calculations assume independent fresh preparations with averaged click probability at least $\eta$. A uniform conditional lower bound also gives binomial tail domination.

## Sample counts for a calibrated efficiency ratio

Let $K$ count occupied gates and require zero doubles. For a bound $|\epsilon|\le e$, use the preceding test with $m$ replaced by $b=m(1-e^2)$. With $y_0=\eta/2$, put $w=(1-y_0)/[1-(1+b)y_0]$ and $A=1+(w-1)y_0$. Each full field observation gets weight $w$ for a single bank click, zero for a double, and one for an empty gate. The conditional expected weight is $1+(w-1)T-w\overline D\le A$. Iteration gives false rejection at most $A^n/w^k$ when the decision requires $K\ge k$. This allows the incident field to change with the previous records.

| Maximum absolute imbalance | Largest efficiency ratio | Preparations $n$ | Minimum occupied gates $k$ |
|---:|---:|---:|---:|
| 0.25 | 5:3 | 2,289 | 206 |
| 0.50 | 3:1 | 2,794 | 254 |
| 0.80 | 9:1 | 5,468 | 511 |

All rows use an orthogonal triad and $\eta=0.10$, with false rejection below 5% and clean-source power above 95%. These are feasible sample sizes. If one bank is entirely dead, even reading all bank, axis and swap labels can fail to distinguish the hypotheses. For example, a live bank with efficiency 0.8 detects an unpolarized single excitation with probability 0.4. An unpolarized Poisson input can be tuned so that the live bank has empty probability 0.6. In each labeled setting the live bank then has the same click law, while the dead bank is always empty.

## Paying for the calibration

One possible reference delivers equal independent Poisson illumination to the two banks in the same operating regime as the science run. Under constant relative sensitivity, labels of individually counted detections are independent Bernoulli draws with $p=g_A/(g_A+g_B)=(1+\epsilon)/2$. A common intensity that varies in time cancels if it multiplies both rates and events are counted continuously under this model. A first-click latch, pileup, overlapping dead times, unequal illumination or a switch-dependent loss can change the label law. The reference must characterize those effects, and its average absolute efficiency requires a separate measurement.

Count 512 reference detections. Accept the calibration if 219 through 293 came from A, inclusive. Outside $|\epsilon|\le0.25$, the probability of passing is below 0.008133, by the binomial tail at $p=5/8$ and its reflection. At equal gains the probability of passing exceeds 0.99909. The 512 are detected reference events. Their acquisition time and incident photon count depend on the reference flux.

Use a fresh science run of 2,494 preparations and require at least 223 occupied gates and zero doubles. Reject the Poisson explanation only if calibration and science both pass. For fixed gains, there are two cases. Within the gain interval, the science false rejection is below 0.03992. Outside it, accepting the calibration has probability below 0.008133. Their maximum bounds the joint size even without independence of the two pass indicators, under the stated conditional models. At truly balanced gains and independent runs, total clean-source power exceeds 0.9644. The shorter 2,289-preparation rule has science power above 0.95 on its own but joint power only 0.94933 after this same reference gate. At the edge of the allowed imbalance interval the calibration is designed to pass only rarely. The joint power claim is specific to balanced banks.

Gerrits and colleagues measured detector efficiency, spatial uniformity, count-rate effects and afterpulsing in named devices. Their time-tagged data for a free-space silicon detector showed a dead interval of about 52 ns. Those observations identify an operating variable the proposed reference would have to control. The proposed swap apparatus and its gains have no measurements in this study. [Gerrits et al., *Metrologia* 57, 015002, §§2.3–2.4](https://doi.org/10.1088/1681-7575/ab4533)

A direct control sends the same polarized pulse down each route and measures occupancy and doubles at both swap settings over the science count-rate range. Repeating with orthogonal input polarizations tests whether a single pair of efficiencies describes the admitted modes. A change in relative efficiency between the reference and science runs invalidates the calibration argument. The comparison gives a detector-level condition for applying the earlier optical test. Stage 1 Initial External Grounding and physical identification remain open.

Run `python -I -B Director_G/persistent_walk/check_swapped_banks.py` from the repository root. The [checker](check_swapped_banks.py) uses exact binomial tails, directed powers and explicitly constructed Poisson outputs to reproduce the [thresholds and error bounds](swapped_banks_output.json).
