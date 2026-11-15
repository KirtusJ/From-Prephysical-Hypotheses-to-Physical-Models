# The 804-launch decision for the five-site return experiment

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

With independent preparations, the ideal five-site return test reaches both 5% error targets after **804 launches** if one count at the decision boundary is randomized. Each launch uses one terminal read of the original port. The maximum run lasts **999,996 ticks**. The deterministic 811-launch decision and the setting generator were given previously. [Pinned protocol and error certificates](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/d494a7514a6ff99c94863c95df513e3a257a2e34/Director_G/persistent_walk/Choosing_stopping_times_before_launch.md) · [Setting generator and current numerical bounds](check_prelaunch_time_sampling.py)

A subsequent calculation tightens the stochastic bound for a real detector and gives a 432-launch test. Reusing even one setting changes the power of the original 804-launch decision. [Sharper fresh-setting test](Real_readout_return_test.md) · [Effect of a duplicated setting](Timing_reuse_and_faults.md)

## Decision

Use the accompanying generator with $N=250{,}000$. Before each launch, propose two independent uniform integers $J,K$ from $0$ through $N-1$. The generator's signed cosine table gives the acceptance probability and sign for $J+K$. Redraw rejected candidates before preparation. At the accepted tick $2(J+K)$, a positive sign scores a detector click as success and a negative sign scores a miss as success. Every original preparation contributes one Bernoulli score, including losses. The timing cannot influence the preparation, transition or detector response except by stopping the evolution. The null comprises fixed homogeneous stochastic models with at most 55 states, including any hidden clock and loss states. The target is the ideal five-site walk under the same observation protocol.

After 804 scores let $X$ be the total successes. For $X\ge481$, reject the null. For $X\le479$, retain it. At exactly $X=480$, draw an independent uniform ten-bit integer and reject if it is below 115. Prespecify the rule before recording data.

The stopping time and its scoring sign must be drawn afresh for each launch. To see the effect of reusing one accepted assignment for the whole run, take the one-state model that always clicks. Its count is then either 804 or 0 according to the shared sign. If the signed integer thresholds are $h_l$, the rejection probability is the fraction of accepted words with a positive sign. Each sum $l=J+K$ has $w_l=N-|l-(N-1)|$ proposal pairs. The generator gives

$$
\frac{\sum_l w_l\max(h_l,0)}{\sum_l w_l|h_l|}
=\frac{85445659438818037790}{170891318864992614874}
\simeq 0.500000000037.
$$

With fresh assignments, direct propagation of the ten ideal rail amplitudes gives a rejection probability between **0.950013337855 and 0.950013337856**. The calculation covers every allowed stopping time, bounds the accumulated rounding error using unitarity, and evaluates the binomial decision at both endpoints. [Direct propagation and shared-setting control](check_804_timing.py)

## Exact endpoint calculation

The pinned spectral and sampling calculations bound the null success probability above by $p_0$ and the target success probability below by $p_1$, where

$$
p_0=\tfrac12+\frac{1369/31250}{636615/10^6}+10^{-9},\qquad
p_1=\tfrac12+\frac{20699999689/258750000000}{636625/10^6}-10^{-9}.
$$

The $10^{-9}$ terms cover the finite-bit setting assignment. The success rates are respectively below $0.568813963$ and above $0.625662671$. Under independent launches, the rejection probability is increasing in the success probability. For $X\sim\operatorname{Binomial}(804,p)$ it is
$\Pr_p(X>480)+(115/1024)\Pr_p(X=480)$. Exact endpoint tails give

| Guarantee | Bound |
|---|---:|
| False rejection under the stochastic model | below 0.049994392 |
| Rejection under the ideal walk | above 0.950007055 |

For the two simple Bernoulli endpoints with 803 launches, the likelihood ratio increases strictly with the success count. The most powerful level-5% decision therefore rejects above 480 and spends its remaining size at exactly 480. The required randomization probability there is $(0.05-\Pr_{p_0}(X>480))/\Pr_{p_0}(X=480)$, which lies between zero and one. Its power is below **0.949699353**. Any decision using fewer launches could ignore the suffix of an 803-launch record. Thus 804 is minimal for the **two conservative Bernoulli endpoints** at these guarantees. The physical model class may satisfy tighter success-rate bounds, and procedures retaining the full time and port records may use more information. The optimal launch count for the original model comparison remains open.

Run the companion program with standard-library Python. It uses the certified fractions above and integer binomial coefficients for the two tail calculations. The accompanying setting generator verifies the preceding spectral and assignment bounds. [Companion program](check_one_port_boundary.py)

~~~sh
python -I -B -O check_one_port_boundary.py
python -I -B -O check_804_timing.py
~~~
