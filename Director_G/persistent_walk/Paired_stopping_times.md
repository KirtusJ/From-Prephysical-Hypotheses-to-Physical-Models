# Two launches at each stopping time

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

The same timing controller can serve two detector launches per independent draw. Draw a setting from the signed [finite-bit sampler](check_prelaunch_time_sampling.py) with $N=250{,}000$. Prepare the device afresh for both launches, run to that tick, and count both scores with the sign assigned by the sampler. Count every launch, including losses. The two launches must be independent conditional on the setting. Draw a fresh independent setting for the next pair. The setting can influence the device only through the duration of its evolution. The longest run is 999,996 ticks.

| Independent settings | Launches | Reject the 55-state null when | False rejection at most | Ideal rejection at least |
|---:|---:|---|---:|---:|
| 389 | 778 | At least 459 successes | 0.049624333 | 0.950869646 |
| 402 | 804 | Above 474 successes, or on heads of an independent fair coin at 474 | 0.046313539 | 0.952523132 |

For each setting $T$, let $s(T)$ be the single-launch success probability after sign scoring. Write $p=E[s(T)]$ and $m=E[s(T)^2]$. Conditional independence gives pair-score probabilities $(1-2p+m,\;2p-2m,\;m)$ for zero, one, and two successes. In the ideal walk, propagation of the ten real amplitudes in [the checker](check_paired_timing.py) encloses the two moments by

$$
0.62566370613899\le p\le0.62566370613900,\qquad
0.52966370805656\le m\le0.52966370805658.
$$

For the null, the [real-readout bound](Real_readout_return_test.md) gives $p\le p_0=0.547843$. To upper-bound an increasing decision, raise the response pointwise to $s+(1-s)(p_0-p)/(1-p)$. This preserves conditional independence and can only add successes under a coupling with the same uniforms. At mean $p_0$, the inequalities $p_0^2\le m\le p_0$ make the pair-score distribution a mixture of $\operatorname{Bin}(2,p_0)$ and $2\operatorname{Ber}(p_0)$, with weight $(m-p_0^2)/(p_0-p_0^2)$ on the latter. Expanding the independent product of $n$ such mixtures bounds its rejection probability by the largest rejection probability for

$$
2X+Y,\qquad X\sim\operatorname{Bin}(r,p_0),\quad Y\sim\operatorname{Bin}(2n-2r,p_0),\quad X\perp Y,\qquad 0\le r\le n.
$$

The checker takes all $n+1$ cases. For the 389-setting rule, the largest upper bound occurs at $r=388$. For the 402-setting rule it occurs at $r=402$. A mixture component used for the bound need not be realizable by a 55-state device. For ideal power the checker increases the zero-score probability to an outward upper bound and decreases the two-score probability to an outward lower bound, then convolves the resulting smaller score distribution over independent pairs. Its integer arithmetic rounds each null point mass upward and each ideal point mass downward. Run `python -I check_paired_timing.py` from this directory to reproduce the table.
