# A 31-launch test with two coherent terminal modes on the five-site ring

Kirtus Justus, research direction. OpenAI ChatGPT, terminal-measurement construction and computational checks. 15 November 2026, British Columbia.

On the ideal five-site Hadamard walk, one fixed terminal measurement gives a signed success probability between **0.814150670081 and 0.814150670082**. With fresh independent preparations and settings, **22 or more successes in 31 launches** rejects the bounded stochastic model. The false-rejection probability is below 0.049711 and the ideal rejection probability exceeds 0.951218. These are design predictions. The record needed to test them experimentally is one binary outcome for every original launch, together with its independently drawn stopping time and scoring sign.

## Experiment and rival

Start on the right rail of site zero. Use the existing prelaunch timing generator with horizon $N=250{,}000$. It selects a tick $2j$ in the range 0 to 999,996 and a sign. Read the ten rails once at that tick using a fixed detector. A positive sign scores a click and a negative sign scores a miss. Other ports and loss are misses. Include every preparation and draw each accepted setting afresh. The preparation, evolution and readout must be isolated from the timing choice except for when evolution stops. [Timing protocol](../../Director_G/persistent_walk/Choosing_stopping_times_before_launch.md)

The rival has a fixed time-homogeneous transition on at most 55 stochastic states, including its clock and loss states. Any fixed terminal stochastic instrument gives a click probability $b_i$ in $[0,1]$ for each premeasurement state $i$. Even a randomized detector is therefore covered by the published bound $p_0=0.547842242$ on signed success. A detector with access to the sign or to a separate time-dependent response would require a different bound. The ideal walk requires coherence among rails in the terminal analyzer, in addition to coherence during propagation. [Real-readout bound for the same sampler](../../Director_G/persistent_walk/Real_readout_return_test.md)

## Three fixed detectors

Use rail order $(R_0,L_0,R_1,L_1,\ldots,R_4,L_4)$ and zero-based indices. Let $X$ count signed successes. Each row is a separate prespecified experiment. At a randomized boundary, draw a uniform eight-bit integer independently of the launches.

| Terminal click | Ideal signed success, rounded | Decision | False rejection at most | Ideal rejection at least |
|---|---:|---|---:|---:|
| Detect rails 0, 1 or 7 directly | 0.730021733919 | In 74 launches, reject above 48, or at 48 if the integer is below 243 | 0.049986468 | 0.951624490 |
| Also accept the symmetric output of each balanced mixer on (2,4), (3,5), (6,8) | 0.774482413923 | In 46 launches, reject above 31, or at 31 if the integer is below 191 | 0.049956762 | 0.950752454 |
| Detect either of the two normalized modes below | 0.814150670081 | In 31 launches, reject at 22 or above | 0.049710926 | 0.951218265 |

The balanced mixers act on disjoint pairs. For each pair $(i,j)$, a click at its symmetric output contributes $|\psi_i+\psi_j|^2/2$. In the third experiment replace the whole analyzer with the projector $E=aa^T/20+bb^T/684$, where

$$
a=(-4,0,1,0,1,0,1,0,1,0),\qquad
b=(0,-16,1,2,-9,-2,9,16,-1,0).
$$

The modes are orthogonal with squared lengths 20 and 684. An ideal mode sorter can extend them to an orthonormal basis and combine the first two output labels into one click. Counting those rails separately before combining would destroy the interference terms. Demonstrating the specified transformation on the actual ten rails remains an experimental requirement.

## Calculation and launch bound

Let $h_j$ be the generator's signed integer threshold, $w_j=(N-|j-(N-1)|)h_j$, $D=\sum_j|w_j|$, and $p_-=\sum_j\max(-w_j,0)/D$. Let $\psi_j$ be the rail state at tick $2j$. For any fixed binary quantum effect $0\le F\le I$, the probability of a signed success is

$$
p(F)=p_-+\mathrm{tr}(FM),\qquad M=D^{-1}\sum_j w_j\,\psi_j\psi_j^*.
$$

The checker propagates all 499,999 lags on the integer grid $S=2^{104}$ and accumulates the signed outer products. Each two-tick update rounds ten coordinates by at most $1/(2S)$ each. Unitarity bounds vector error at lag $j$ by $2j/S$. For any effect, the absolute quadratic-form error is at most $2(2j/S)+(2j/S)^2\le 6j/S$. Weighting by $|w_j|/D$ gives the uniform bound $\epsilon=6(2N-2)/S$. The checker also projects onto the two modes at each lag before accumulating and compares the exact result to the matrix contraction. [Underlying rail step](../../Director_G/persistent_walk/check_804_timing.py) · [Integer timing table](../../Director_G/persistent_walk/check_prelaunch_time_sampling.py)

For every complex Hermitian effect, the largest possible trace against the real symmetric grid matrix is the sum of its positive eigenvalues. Rational symmetric elimination of the grid matrix minus a scalar shift counts eight eigenvalues below $2\times10^{-11}$ and all ten below $0.157079632800$. Thus every fixed effect has ideal success bounded above by $p_-+8(2\times10^{-11})+2(0.157079632800)+\epsilon<0.814159265724$.

**Scope of the 31-launch minimum.** Retain only independent binary scores, use the original sampler and a common fixed effect, and require size at most 5% for the entire Bernoulli null envelope $0\le p\le p_0$. An alternative inside that envelope has power at most 5%. Above $p_0$, the most powerful test against the endpoint $p_0$ rejects large counts, with boundary randomization if needed. At 30 launches its power even at $p=0.814159265724$ is below **0.93819744414**. A shorter test could ignore the remaining launches. This establishes the minimum under those conditions. The physical null might admit a tighter calibration, and a test retaining times or port labels has a different observation space.

## How much terminal coherence is needed?

Suppressing all off-diagonal entries of $E$ preserves its individual rail click rates but gives a signed success probability between 0.628214404754 and 0.628214404755. The 31-launch decision then has power below **0.228244**. A calibration that probes each rail separately would miss this failure.

In the specific dephasing model $F_v=vE+(1-v)\operatorname{diag}(E)$, the success probability is affine in $v$. The checker verifies that $v\ge0.995847$ suffices for 95% power. More generally, if the walk states and timing law are ideal, $\|F-E\|_{\mathrm{op}}\le0.000772305651$ also suffices. Each per-launch click probability can shift by at most this norm, and the signed probabilities move by at most the same amount. These tolerances specify calibration targets. Real detector loss, relative phases, reset and timing isolation still require measurements.

## Reproduce

From the repository root, run the command below with Python 3. It uses only the standard library. The certificate uses rational comparisons throughout. Decimal values in the transcript are rounded for display.

~~~sh
python -I -B Director_PT/persistent_walk/check_terminal_readouts.py
~~~

[Executable certificate](check_terminal_readouts.py) · [Recorded output](terminal_readouts_output.txt) · [Base research revision](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/commit/34fa3fea5c8fc8b95ed690be370d3eb16ed9dde2)
