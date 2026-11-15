# A shorter single-port return test on five sites

Director G research for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

A randomized stopping time and a single detector distinguish the specified ideal five-site walk from every homogeneous stochastic model with at most 55 states. **2,400 independent launches suffice. The longest run lasts 999,996 ticks.** Each model has less than a 5% probability of falling on the wrong side of a prespecified threshold. These are calculated design guarantees. Physical performance requires an independently characterized preparation, evolution and detector.

## Measurement

Keep every site open. Launch at site zero on the right rail. Apply the same real Hadamard coin and rail-directed shifts each tick. Let $u,v$ be the upper-half-plane unit phases with real parts $(3-\sqrt5)/8$ and $(3+\sqrt5)/8$, respectively. Set $\zeta=u/v$ and $N=250{,}000$.

1. Draw $J,K$ independently and uniformly from $0,\dots,N-1$ on each fresh launch. Stop after $2L$ ticks, where $L=J+K$.
2. Record $C=1$ for detection at the launch port and $C=0$ for every other outcome, including loss. Score $Y=(C-1/2)\operatorname{Re}(\zeta^{-L})$.
3. Compute the mean score of the 2,400 launches. Reject the 55-state class when the mean is at least $0.0619$.

The stochastic model has a fixed launch distribution $\alpha$, a row-stochastic transition matrix $P$ of dimension at most 55 and a fixed terminal click vector $b\in[0,1]^{h}$. Every hidden clock or loss state used by this representation counts toward its state budget. The time choice must be independent of preparation and transition dynamics. Measurements occur only at the terminal time. The guarantee for the ideal walk assumes its unconditional return law holds through the sampled durations. Dephasing, detector drift and inefficient detection can change that law. No measured counts enter this calculation.

## Bound on stochastic predictions

Write $S=P^2$ and $R=37{,}000$. We show $\|(\zeta I-S)^{-1}\|_\infty\le R$. Take a complex vector of sup norm one, rotate it so some coordinate is one, and let $\epsilon=\|Sx-\zeta x\|_\infty$. Telescoping and stochastic contraction give $\|S^kx-\zeta^kx\|_\infty\le k\epsilon$. At the chosen coordinate, $(S^kx)_i$ is a convex average of the coordinates of $x$. Its projection on $\zeta^k$ is at least $1-k\epsilon$. Some coordinate then lies within $\sqrt{2k\epsilon}$ of $\zeta^k$.

If $\epsilon<1/R$, the 56 disks about $\zeta^k$, for $0\le k\le55$, are pairwise disjoint. For a pair with index difference $d$, the sum of its radii is at most $\sqrt{2\epsilon}(\sqrt{55}+\sqrt{55-d})$. The checker verifies all 55 inequalities

$$R|1-\zeta^d|^2>2(\sqrt{55}+\sqrt{55-d})^2.$$

Only 55 coordinates are available. The resulting contradiction proves the resolvent bound, including invertibility. For $H_N(X)=N^{-1}\sum_{j=0}^{N-1} X^j$, the geometric-sum identity now gives $\|H_N(S/\zeta)\|_\infty\le 2R/N$. Independence of $J,K$ gives a square of this operator. The expected score is $\operatorname{Re}\{\alpha H_N(S/\zeta)^2(b-\mathbf1/2)\}$. Hence the stochastic mean is at most

$$\tfrac12(2R/N)^2=0.043808.$$

## Bound on the ideal prediction

The signed return amplitude at even tick $2L$ is $\sum_{a\in M}a^L/5$, for $M=\{1,u,\bar u,v,\bar v\}$. This follows by squaring the spatial Fourier blocks of the walk and combining conjugate modes. The port probability is the squared modulus. In its 25-term expansion the ordered ratios $u/v$ and $\bar v/\bar u$ resonate exactly with the score. They contribute $2/25$. For every other ratio $a/b$, the checker verifies $|1-(a/b)/\zeta|>0.23$. It also verifies $|1-\zeta|>0.60$. Since $|H_N(x)|\le2/(N|1-x|)$ for the remaining unit phases, the ideal mean is at least

$$\frac{2}{25}-\frac{23}{25}\left(\frac{2}{0.23N}\right)^2-\frac12\left(\frac{2}{0.60N}\right)^2
=\frac{20699999689}{258750000000}>0.07999999879.$$

The last term allows for centering all scores, including misses. The starting amplitude and the earlier design are recorded in the [pinned port proof](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/a1eee36656ab413eac2cfa92c9d2bb62a1bea25e/Director_G/persistent_walk/Return_at_one_port.md) and [earlier finite test](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/a1eee36656ab413eac2cfa92c9d2bb62a1bea25e/Director_G/persistent_walk/A_finite_duration_return_test.md).

## Sampling error

The threshold has distance at least $\delta=0.018092$ from either allowed mean. Also $Y^2=\cos^2(L\arg\zeta)/4$ for both click outcomes. The second harmonic satisfies $|1-\zeta^2|>1$, giving

$$\operatorname{Var}(Y)\le\mathbb E[Y^2]\le V=\{1+(2/N)^2\}/8=0.125000000008.$$

The centered variable $X=Y-\mathbb E Y$ satisfies $|X|\le1$. For $0<t<3$, the exponential series, $|X|^k\le X^2$ for $k\ge2$, and $k!\ge2\cdot3^{k-2}$ imply $\mathbb E e^{tX}\le\exp[t^2 V/(2(1-t/3))]$. Independence, Markov's inequality for the exponential, and $t=\delta/(V+\delta/3)$ bound the one-sided tail by $\exp[-m\delta^2/(2(V+\delta/3))]$. The same bound holds for $-X$. At $m=2{,}400$ this is below $0.04991$. The checker proves the $1/20$ guarantee with rational arithmetic. The two errors concern distinct generating models. This calculation gives sufficient launch and duration budgets. Optimal budgets and the response of a physical instrument are open.

## Reproduction

Run the companion file with standard-library Python 3.9 or later.

~~~sh
python -I -B -O check_shorter_return.py
~~~

The test uses integer square roots and outward rounding at each real or complex interval operation, then checks the concentration bound by a positive finite Taylor sum. Its inequalities remain active under optimized Python.
