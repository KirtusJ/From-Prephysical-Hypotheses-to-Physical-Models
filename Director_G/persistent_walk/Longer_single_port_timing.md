# A 57-launch return test at one port of the five-site walk

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), mathematical design and computational checks. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A single detector at the launch port can distinguish the ideal five-site Hadamard return law from the specified class of time-homogeneous stochastic models in **57 independent preparations**, provided the walk remains coherent for up to **3,999,996 ticks**. The detector is the same for every duration. The timing distribution and its scoring sign are fixed in advance. The tradeoff is a longer maximum evolution compared with the published 432-launch protocol. These probabilities are calculated from two mathematical models. [Original test and stochastic rival](Real_readout_return_test.md)

| Timing distribution | Maximum ticks | Reject rule for the count of successes | Size at most | Ideal power at least |
|---|---:|---|---:|---:|
| Three cosines, 57 launches | 3,999,996 | Above 38, or at 38 with independent probability 33/64 | 0.049623601473 | 0.950186069145 |
| Same distribution, 61 launches | 3,999,996 | At least 41 | 0.046301224319 | 0.960946577493 |
| One cosine, three timing draws, 386 launches | 999,982 | Above 226, or at 226 with independent probability 769/1024 | 0.049996016379 | 0.950387104817 |
| Same distribution, 389 launches | 999,982 | At least 228 | 0.049214207016 | 0.951245692489 |

## Preparation, timing and scoring

Start on the right-moving rail at site zero. Write $u,v$ for the upper-half-plane unit phases with real parts $(3-\sqrt5)/8$ and $(3+\sqrt5)/8$. The ideal amplitude at the launch rail at tick $2j$ is $(1+2\operatorname{Re}u^j+2\operatorname{Re}v^j)/5$. For the long experiment independently draw two uniform integers from 0 through 999,999 and take their sum $j$. The signed timing weight is the mean of $\operatorname{Re}(u/v)^j$, $\operatorname{Re}u^j$ and $\operatorname{Re}(uv)^j$. For the shorter experiment draw three integers uniformly from ranges of lengths 166,152, 167,983 and 165,859, each starting at zero. Use the single weight $\operatorname{Re}(u/v)^j$. [Ideal return amplitude](Return_at_one_port.md)

In either experiment, form the signed integer threshold from the specified fixed-point centers in the checker. Accept the proposal when an independent uniform 32-bit integer falls strictly below the threshold magnitude. Repeat until acceptance, then prepare the walk and stop it at tick $2j$. A positive sign scores a click as success. A negative sign scores a miss as success. Record every preparation, including a loss as a miss. The device may learn the elapsed duration through its evolution. Preparation, readout and transition probabilities must otherwise be independent of the chosen setting. A controller that learns the sign and clicks exactly on positive settings can score 100% using a single state. This is an adverse control for the isolation assumption.

## Bound for the stochastic rival

Let $P$ be a fixed stochastic matrix on at most 55 states, including clock and loss states. Put $S=P^2$. For a real terminal response $0\le b\le1$, center the response on $c=b-\mathbf1/2$. A uniform timing index over a range of length $n$ contributes $H_n(S/z)=n^{-1}\sum_{j=0}^{n-1}(S/z)^j$ to the signed response at phase $z$. Independent indices multiply the factors. If $R_z\ge\|(I-S/z)^{-1}\|_\infty$, the unnormalized signed response for $k$ indices of lengths $n_i$ is bounded in magnitude by

$$
\frac{R_z^k M_z}{2\prod_i n_i}.
$$

Here $M_z$ bounds the modulus of the expanded numerator $\prod_i(I-(S/z)^{n_i})(2c)$ at any coordinate. Each real value of $2S^m c$ lies in $[-1,1]$. Checking sign vertices of that cube bounds the maximum by convexity, including when some subset sums coincide. For the long design, $R_z$ is respectively 36,733, 121,786 and 130,167. For the shorter design use 36,733. The checker verifies the 55 angular inequalities separately for every phase by outward integer intervals. The disjoint-cap proof uses only stochastic contraction and the 55-state limit and also covers reducible matrices. [Resolvent proof](Real_readout_return_test.md)

Average the frequency bounds before dividing by the actual acceptance probability. For the long design this probability is exactly $1308791557480504867339/4294967296000000000000$. The checker calculates proposal multiplicities by counting integer pairs or triples, and sums the signed ideal intensity over every allowed duration. Its grid spacing is $2^{-128}$. Initial phase constants have complex error below 128 grid units, and each multiplication discards less than two units. At lag $j$ the phase error is bounded by $260j$ grid units by induction while this bound is below one in physical units. Threshold quantization adds at most $2^{-32}$ to the timing-weight error. The centered stochastic response has magnitude at most $1/2$. For the ideal intensity the checker charges three times the maximum phase error.

The resulting long-design endpoints are $p_0\le0.557844796873$ and $p_1\ge0.762530256739$. At 56 independent binary scores the most powerful level-5% randomized test between those two rounded endpoints has power below 0.949048018717. The likelihood ratio increases with the count, so this follows by spending the remaining test size on the boundary count. The 57-launch minimum applies to that Bernoulli comparison. The greatest attainable stochastic success for the actual model class, other choices of timing law and the effect of measured apparatus imperfections remain open. A coherent classical-wave realization with the same amplitudes and square-law readout shares the ideal prediction.

## Loss accumulated during the walk

Suppose an otherwise ideal walker is independently lost with probability $r$ on each physical tick. Loss is permanent and gives a miss. If $w_j$ is the signed integer timing weight including proposal multiplicity, $D=\sum_j|w_j|$, and $I_j$ the ideal launch-port intensity, the signed success probability is

$$
p(r)=\frac{\sum_j\max(-w_j,0)+\sum_j w_j I_j(1-r)^{2j}}{D}.
$$

The negative-setting miss contribution matters because a lost click can turn a negative-sign trial into a success. The checker proves that $p(r)$ decreases over $0\le r\le1.2\times10^{-8}$ by bounding its derivative across the entire interval. It checks all 1,999,999 lags, rounding the survival recurrence down on the same 128-bit grid and allowing two grid units of error per update.

| Prespecified decision | Per-tick loss with ideal power above 95% | Per-tick loss with ideal power below 95% |
|---|---:|---:|
| 57 launches, randomized at 38 | $1.876\times10^{-10}$ | $1.877\times10^{-10}$ |
| 61 launches, reject at 41 | $1.183\times10^{-8}$ | $1.184\times10^{-8}$ |

Four additional preparations give the second rule more than 63 times the per-tick loss tolerance of the first in this model. The bounds concern alternative power under uniform loss. An apparatus needs a measured loss rate for comparison. The stochastic guarantee counts every loss state toward the 55-state budget.

Run `python -I -B Director_G/persistent_walk/check_single_port_loss.py` to reproduce the brackets. [Loss calculation](check_single_port_loss.py) · [Recorded bounds](single_port_loss_output.json)

## Reproduction

Run the following from the repository root and compare standard output to the recorded JSON. The checker exercises a negative scoring sign, rejection exactly at the threshold, fixed detectors, sign disclosure, both timing distributions and all four decisions. Calculations use the Python standard library. Physical identification and Stage 1 Initial External Grounding remain open.

~~~sh
python -I -B Director_G/persistent_walk/check_single_port_timing.py
~~~

[Executable checker](check_single_port_timing.py) · [Recorded output](single_port_timing_output.json) · [Source revision](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/commit/34fa3fea5c8fc8b95ed690be370d3eb16ed9dde2)
