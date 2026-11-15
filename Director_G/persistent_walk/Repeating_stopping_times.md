# Repeating a stopping time across launches

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

One detector can test the five-site walk with **32 independently assigned block settings**. The price is 180,800 physical launches. A second design uses 64 assignments and 89,600 launches. Several blocks may independently draw the same tick. The longest eligible run in both designs is 999,996 ticks. Each launch contributes one binary score, including losses.

| Independent block assignments | Launches per block | Total launches | Tolerance | False rejection at most | Ideal power at least |
|---:|---:|---:|---:|---:|---:|
| 32 | 5,650 | 180,800 | 0.024 | 0.047025 | 0.952311 |
| 64 | 1,400 | 89,600 | 0.051 | 0.032089 | 0.956015 |

## Assignment and decision

Let $\nu$ be the finite-bit distribution on terminal ticks in the [prelaunch design](Choosing_stopping_times_before_launch.md) with $N=250{,}000$. At each tick $t$, count the indicated outcome (click or miss) as one success. Write $s(t)$ for its ideal probability and $p(t)$ for its probability under a fixed homogeneous stochastic model with at most 55 hidden states. The [real-readout certificate](check_real_readout_bound.py) gives $\mathbb E_\nu p(t)\le 0.547842242$.

Choose one row in advance. For its tolerance $a$, the [integer controller](check_block_timing.py) tabulates a cutoff $c(t)=h(t)/2^{32}$ just below $\max(0,s(t)-a)$. Before the first launch of each block, propose a setting from $\nu$ and draw a fresh uniform 32-bit integer. Accept if the integer is below $h(t)$ and otherwise repeat. All proposal rejections occur before any preparation. Keep the accepted setting for the whole block, conceal it from preparation and transitions, and measure each launch once at that tick. A loss counts as a miss. The block passes when its success count $Y$ satisfies $2^{32}Y\ge m h(t)$, where $m$ is the launches per block. Reject the stochastic model if every block passes.

Use fresh block assignments and independent resets between blocks. Under the null it suffices that, conditional on the earlier block history and the current assignment, the expected success fraction in the new block is $p(t)$. Within-block independence is unnecessary for that bound. For ideal power the launches at each assigned tick are independent with success probability $s(t)$. Neither design estimates how often coherent experimental hardware meets this ideal assumption.

## Error bounds

The accepted setting law has mass $\nu(t)c(t)/Q$ with $Q=\mathbb E_\nu c(t)$. Given the tick, Markov's inequality gives $c(t)\Pr(\text{block passes}\mid t)\le p(t)$. Averaging under the accepted law and iterating the conditional bound across $b$ fresh blocks gives false rejection at most $(0.547842242/Q)^b$. The checker computes $Q$ exactly by summing the integer weights of the finite controller.

On every eligible setting $s(t)-c(t)\ge a$. Hoeffding's inequality and a union bound across blocks give ideal miss probability at most $b\exp(-2ma^2)$. For each lag $j=t/2$, the [integer walk propagation](check_804_timing.py) bounds the error of the signed success estimate by $6j/2^{104}$. Subtract this allowance and $a$ before flooring to the 32-bit grid and clipping at zero. The checker propagates all 499,999 lags, verifies the exact cutoff masses, and uses a rational lower bound on the exponential. [Hoeffding, 1963, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

Run `python -IB check_block_timing.py` from this directory. The first column counts independently accepted assignments and the third counts all physical launches. The prelaunch controller consumes a variable number of independent random words.
