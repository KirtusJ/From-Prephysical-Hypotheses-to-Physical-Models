# A 432-launch test of the five-site return signal

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

For the ideal five-site walk, 432 independent launches suffice to distinguish its single-port return from the specified class of homogeneous stochastic models with at most 55 hidden states. Use the [existing stopping-time generator](Choosing_stopping_times_before_launch.md) at $N=250{,}000$. Draw a fresh accepted setting before each launch and count every outcome, including loss. The longest run is 999,996 ticks. The reductions below use real detector responses and the geometry of phases on the unit circle.

## Two prespecified count decisions

Let $X$ be the number of successes. As in the existing protocol, a positive setting scores a click as success and a negative setting scores a miss as success. The setting can influence the device only through the duration of the evolution. The following choices use independent preparations and fresh independent settings throughout.

| Launches | Reject the stochastic model when | False rejection | Ideal rejection |
|---:|---|---:|---:|
| 432 | $X\ge255$, or $X=254$ and an independent uniform ten-bit integer is below 858 | $<0.049988$ | $>0.950023$ |
| 437 | $X\ge257$ | $<0.049878$ | $>0.952065$ |

These are calculated design guarantees. The ideal return probabilities must hold over the sampled durations for the stated power to apply.

## The resolvent

Let $P$ be the model's transition matrix, $S=P^2$, and $\zeta=u/v$, where $u,v$ are the upper-half-plane unit phases whose real parts are $(3-\sqrt5)/8$ and $(3+\sqrt5)/8$. Put $R=36{,}733$. For $\|x\|_\infty=1$, rotate $x$ so that $x_i=1$ at a maximizing coordinate, and write $e=\|Sx-\zeta x\|_\infty$. Stochastic contraction gives $\|S^kx-\zeta^kx\|_\infty\le ke$. At coordinate $i$, the convex average $(S^kx)_i$ has projection on $\zeta^k$ at least $1-ke$. Some coordinate of $x$ has at least that projection.

If $e<1/R$, that coordinate has nonzero modulus at most one and its angular distance from $\zeta^k$ is at most $\phi_k=\arccos(1-k/R)$ for $0\le k\le55$. At lag $d$ the largest possible sum of two cap half-widths is $\phi_{55}+\phi_{55-d}<\pi$. The checker verifies the 55 strict inequalities

$$
\operatorname{Re}\zeta^d <
(1-55/R)(1-(55-d)/R)
-\frac{\sqrt{55(2R-55)(55-d)(2R-55+d)}}{R^2},
\qquad 1\le d\le55.
$$

The right-hand side is the cosine of that largest sum. Thus all 56 caps are disjoint, requiring at least 56 distinct coordinates of $x$. This proves invertibility and $\|(I-S/\zeta)^{-1}\|_\infty\le R$.

## The real detector response

Write $c=b-\mathbf1/2$ for the centered click vector, where $0\le b_i\le1$, and $H_N(A)=N^{-1}\sum_{j=0}^{N-1} A^j$. For the triangular proposal times the signed mean before acceptance is $\operatorname{Re}\{\alpha H_N(S/\zeta)^2 c\}$. With $w=\zeta^{-N}$,

$$
H_N(S/\zeta)^2c
=N^{-2}(I-S/\zeta)^{-2}(I-w S^N)^2 c.
$$

For each coordinate the last factor has value $(x-2wy+w^2z)/2$, where $x,y,z$ are the corresponding coordinates of $2c,2S^Nc,2S^{2N}c$. All three lie in the **real** interval $[-1,1]$. The modulus attains its maximum over this cube at a sign vertex by separate convexity. Dividing by $w$ gives $x\bar w-2y+wz$. At $x=z$ its largest modulus is $2+2|\operatorname{Re}w|$. At $x=-z$ its squared modulus is $4(2-(\operatorname{Re}w)^2)$. Outward evaluation of $\zeta^N$ gives a bound $M=2.821536$ for the numerator before the factor $1/2$. Consequently the null signed mean is at most $R^2 M/(2N^2)$.

The [sampler certificate](check_prelaunch_time_sampling.py) gives the normalization bounds $0.636615<W<0.636625$ and a $10^{-9}$ allowance for integer thresholds. The [ideal spectral calculation](Shorter_return_test.md) gives a signed mean at least $20699999689/258750000000$. The resulting one-launch probabilities satisfy

$$
p_{\rm null}\le\tfrac12+\frac{R^2M}{2N^2(0.636615)}+10^{-9}
<0.547842242,\qquad
p_{\rm ideal}>0.625662671.
$$

The count rules follow by evaluating the two binomial tails at the displayed decimal endpoints, treated as exact rationals. With 431 launches the likelihood ratio between those two Bernoulli endpoints increases with $X$. The most powerful level-5% test rejects above 253 and uses its remaining size at 253. Its endpoint power is below 0.949470. Shorter tests could ignore the final observations of a 431-launch record. Thus 432 is minimal for these two rounded Bernoulli endpoints. The launch minimum for the physical model comparison is open.

For prespecified reuse, two launches per draw give a 778-launch test. Holding a setting for a larger block allows just 32 independent assignments. A separate rule tolerates eight arbitrary score changes among 804 launches. [Paired launches](Paired_stopping_times.md) · [Repeated blocks](Repeating_stopping_times.md) · [Timing faults](Timing_reuse_and_faults.md)

Run the [arithmetic check](check_real_readout_bound.py) alongside the two existing checkers it imports.

~~~sh
python -I -B -O check_real_readout_bound.py
~~~
