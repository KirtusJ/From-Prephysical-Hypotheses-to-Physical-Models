# Choosing stopping times before launch

Director G research for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

With the ideal five-site walk, **811 independent launches suffice** for the single-port test against the homogeneous 55-state stochastic class. The maximum run still lasts 999,996 ticks. The timing assignment spends more launches at settings whose counts carry greater statistical weight. The resulting decision is an ordinary binomial count.

| Alternative | Maximum tick | Launches | Reject at this many successes or more | Upper bound on false rejection | Upper bound on failure to reject under the alternative |
|---|---:|---:|---:|---:|---:|
| Ideal walk | 999,996 | 811 | 485 | 4.973% | 4.871% |
| Calibrated loss or reset | 999,996 | 4,923 | 2,858 | 4.967% | 4.993% |
| Calibrated loss or reset | 1,799,996 | 806 | 444 | 4.950% | 4.966% |

Each row is a sufficient design for its specified model and horizon. The two durations allow different bounds on stochastic predictions. The noisy rows assume constant true detection efficiency of at least 90%, independent background clicks at probability at most 1% per terminal read, and per-tick probability of surviving and retaining ideal evolution of at least 0.9999996, independently across ticks. If loss and reset both act, this lower bound applies to their joint retention probability. Under reset, the ten-mode maximally mixed state is invariant. A loss-only experiment uses permanent loss. The assumptions and unconditional click law are given in the [calibrated measurement study](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/3941409ac22febbac7fe0f937e22ca0477aab857/Director_G/persistent_walk/Calibrated_loss_and_background.md).

## Setting assignment and decision

Use the same port preparation, evolution and terminal readout as in the [shorter return test](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/3941409ac22febbac7fe0f937e22ca0477aab857/Director_G/persistent_walk/Shorter_return_test.md). Take $N=250{,}000$ for the first two rows and $N=450{,}000$ for the last. Define $\zeta=u/v$ from the upper unit phases $u,v$, whose real parts are $(3-\sqrt5)/8$ and $(3+\sqrt5)/8$ respectively. Fix $c_L=\operatorname{Re}(\zeta^{-L})$.

1. **Before preparing a walker**, draw independent uniform integers $J,K$ from 0 through $N-1$. With $L=J+K$, accept the proposed terminal setting with probability $|c_L|$. Redraw the setting if necessary. Only a random number is discarded.
2. Prepare a fresh walker, apply the fixed step for $2L$ ticks, and read its launch port once. Record $C=1$ for a click and $C=0$ for every other outcome, including loss. Every prepared walker has one recorded outcome.
3. Record a statistical success if $C=1$ and $c_L>0$, or if $C=0$ and $c_L<0$. After the specified number of launches, compare the total with the table. Settings with $c_L=0$ have zero acceptance probability.

Any hidden clock or loss state used to represent the observed stochastic law $q_t=\alpha P^t b$ counts toward the 55-state budget. Changing the chosen stop time must have no effect on this fixed launch distribution, transition law and click response. Each row needs fresh independent sampling of the setting and outcome on every launch.

## Why the binomial count separates the models

Under the original proposal distribution, $L$ has probability $(N-|L-(N-1)|)/N^2$ on $0\le L\le 2N-2$. Let $W=\mathbb E|c_L|$ under this distribution. The original score mean is $\mu=\mathbb E[(C-1/2)c_L]$. Under the accepted setting distribution the Bernoulli success probability is exactly

$$
p_{\rm success}
=\frac{\mathbb E[|c_L|(1/2+\operatorname{sign}(c_L)(\mathbb E[C\mid L]-1/2))]}{W}
=\frac12+\frac{\mu}{W}.
$$

Thus the earlier upper bound on $\mu$ for every stochastic model and lower bound under each alternative still apply to the original proposal distribution in the formula. The checker encloses $W$ strictly between 0.636615 and 0.636625 at both horizons. For example, at the shorter horizon with ideal evolution, $p_{\rm success}<0.56881397$ for the stochastic class and $p_{\rm success}>0.62566267$ for the ideal walk. Exact binomial tails at the rational probability bounds give the table. The sign reversal for a miss at a negative cosine is part of the decision rule. A success in this count is a scored observation, irrespective of whether the detector clicked.

For the $W$ enclosure, the checker brackets the algebraic phase by integer intervals and sums all supported stopping times using fixed-point complex powers. On a grid of scale $B=2^{112}$ the error in the input phase is at most $24/B$ and each rounded complex multiplication adds at most $2/B$. Multiplication by the true phase preserves the Euclidean norm. While the propagated error is below one, the next error increases by at most $50/B$. Induction bounds every coordinate error by $50(2N-2)/B$, which also bounds the absolute error of the normalized weighted sum. Physical counts and the optimal sample budget remain open.

## Finite-bit setting assignment

The companion program implements a sampler with integer thresholds. Prepare its signed table once. On each candidate draw, split 68 bits ($N=250{,}000$) or 70 bits ($N=450{,}000$) into two equal-width candidate coordinates and a 32-bit acceptance word. Reject the candidate if a coordinate is outside $0,\dots,N-1$. For valid $L$, the table gives the signed threshold $h_L$, rounded toward zero from the fixed-point cosine and clipped to $[-2^{32},2^{32}]$. Accept when the 32-bit unsigned word is below $|h_L|$. The sign of $h_L$ determines the success rule. Every candidate uses finitely many bits. Rejected candidates precede preparation; the number of candidate draws per launch has a geometric tail.

Set $\tilde c_L=h_L/2^{32}$, $\tilde W=\mathbb E |\tilde c_L|$. The fixed-point bound above and quantization give $|\tilde c_L-c_L|\le\epsilon=50(2N-2)/2^{112}+2^{-32}$. Write $s=\mathbb E[(C-1/2)c_L]$ and $\tilde s$ for the same average using $\tilde c_L$. Then $|s|\le W/2$, $|s-\tilde s|\le\epsilon/2$ and $|W-\tilde W|\le\epsilon$. Consequently the change in the success probability is at most $\epsilon/(W-\epsilon)<10^{-9}$. This proof includes possible sign changes near zero and settings rounded to zero. The checker adds this allowance to the stochastic bound and subtracts it from the alternative before evaluating the binomial tails in the table.

For example, use the following code on the terminal controller. Pass the tick to the stopping mechanism. Keep the assignment independent of the preparation and the step applied. Record the success label only after collecting the outcome.

~~~python
from secrets import randbits
from check_prelaunch_time_sampling import make_design, draw_setting

N = 250_000
signed_table = make_design(N)
tick, click_is_success = draw_setting(N, signed_table, randbits)
# After launching and reading once at tick:
# success = (bool(detector_click) == click_is_success)
~~~

The statistical proof assumes independent uniform input bits and independent launches. The code provides the setting generator; it cannot verify an apparatus's isolation or randomness.

## Checks on the earlier budgets

For the [4,999,999-tick design](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/3941409ac22febbac7fe0f937e22ca0477aab857/Director_G/persistent_walk/A_finite_duration_return_test.md), the full gap between the published rounded means is 0.0148. The threshold margin on either side is 0.0074. Scores range from $-1$ to $1$, giving the one-sided Hoeffding bound $\exp[-n(0.0074)^2/2]$. Rounded to eight decimal places, it is 0.04999885 at 109,414 launches and 0.05000022 one launch earlier. The older receipt's field named “certified_margin” stores the full gap. Its launch computation uses the correct half-gap.

For the [999,996-tick design](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/3941409ac22febbac7fe0f937e22ca0477aab857/Director_G/persistent_walk/Shorter_return_test.md), the rerun gives the stochastic upper bound $1369/31250$, ideal lower bound $20699999689/258750000000$ and margin $4523/250000$ at the fixed threshold $0.0619$. The variance bound and Bernstein exponent give a one-sided error below 5% at 2,400 launches. Both earlier budgets are sufficient under their stated hypotheses.

Run the companion checker with standard-library Python 3.9 or later.

~~~sh
python -I -B -O check_prelaunch_time_sampling.py
~~~

Randomizing the decision at a single boundary count reduces the sufficient launch count to 804 with the same timing protocol. [Decision and endpoint proof](One_port_randomized_boundary.md)
