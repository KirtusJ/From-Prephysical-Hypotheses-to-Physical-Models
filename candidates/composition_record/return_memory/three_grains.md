# One fixed mask tests three detector resolutions

Keep both rails of sites 0 and 2 as the target on a nine-site ring. One event is reported on every launch. By changing the launch site and choosing between three and five free Hadamard ticks, one can distinguish the ordinary binary probabilities from launch-dependent positive powers scored at any of three resolutions. A detector may switch resolution and power together. Ten experimental settings are used in all, including two to establish the reporting baseline. This is a prospective test. The path sums and the sign certificate are computations. The published three-spin measurements used different preparations and readouts. [Earlier two-resolution test](mixed_order.md) · [Signed-path specification and replay](translated_mask.md) · [Published experiment](https://doi.org/10.1073/pnas.2529694123)

## Observable inputs

Start at site $s$ on the right rail. A tick sends signed amplitude $R+L$ one site right on rail R and $R-L$ one site left on rail L. The total integer squared weight at time $t$ is $2^t$. For each setting $i$, define $p_i$ as the fraction in the target mask. Columns 4 and 5 specify the positive target terms prior to scoring. Repeated weights denote distinct outcomes at the indicated resolution.

| $i$ | $(t,s)$ | $p_i$ | Site weights | Oriented-port weights |
| --- | --- | ---: | --- | --- |
| 1 | (3,5) | 1/8 | 1 | 1 |
| 2 | (3,3) | 1/4 | 1, 1 | 1, 1 |
| 3 | (5,4) | 1/32 | 1 | 1 |
| 4 | (5,1) | 1/4 | 4, 4 | 4, 4 |
| 5 | (5,3) | 9/32 | 4, 5 | 1, 4, 4 |
| 6 | (5,5) | 6/32 | 1, 5 | 1, 1, 4 |
| 7 | (5,6) | 18/32 | 1, 17 | 1, 1, 16 |
| 8 | (5,8) | 21/32 | 4, 17 | 1, 4, 16 |

Let $P_{g,i}(q)$ denote the target chance for resolution $g$ and $0<q<\infty$. At whole-mask resolution it equals $p_i^q/[p_i^q+(1-p_i)^q]$. At each of the two finer resolutions it equals the sum of $q$th powers of the listed target weights divided by the sum over all occupied outcomes at that resolution. The denominator's multiset is

| $t$ | Sites | Oriented ports |
| --- | --- | --- |
| 3 | 1, 1, 1, 5 | 1, 1, 1, 1, 4 |
| 5 | 1, 1, 4, 4, 5, 17 | 1, 1, 1, 1, 4, 4, 4, 16 |

A launch carries a mode $(g,q,a,b)$, which would report a click with probability $a+bP_{g,i}(q)$ under setting $i$. Take $0\le a,a+b\le1$, $b\ge0$ and $E[b]>0$. Correlations between all mode coordinates are allowed. The mode distribution and reporting rule must be common across sites and clock choices. Measure the actual report rate $Y_i$ per assigned launch, including losses in the defined record. Untracked postselection can alter the mode population. Randomized, interleaved assignment helps check for setting-dependent changes.

Measure also the dark launch $Y_0=Y_{3,0}$ and the rate $Y_{3,1}$ for squared target mass $3/4$. Set $B=Y_2+Y_{3,1}-2Y_0$. The target fractions on launches (3,3) and (3,1) sum to one **for every resolution and every exponent**. Whole-mask scoring pairs complementary masses. Site scoring partitions the weights into $(1,1)$ and $(1,5)$, while port scoring gives $(1,1)$ and $(1,1,4)$. Consequently $Y_0=E[a]$ and $B=E[b]$. This supplies the same gain reference regardless of how the detector resolves each launch.

## One signed sum of ten rates

Write $P_g(q)$ and $p$ for the eight-component column vectors in the table. Use

$$
w=(1,w_2,1,-1,-1,w_6,w_7,-7/10),\qquad
w\cdot P'_g(1)=0\quad\text{for each of the three resolutions}.
$$

These three linear equations define the coefficients exactly. In the row order whole mask, site, port, the determinant on columns 2, 6 and 7 is approximately $-0.00681553328$. The solution is $(w_2,w_6,w_7)\simeq(-0.1206417484,0.0316160716,0.0881794911)$. Put $c=w\cdot p\simeq-0.8090064599$. A rate contrast that includes the offset and gain measurements is

$$
L=\sum_{i=1}^8 w_i(Y_i-Y_0)-cB
  =E[b F_g(q)],\qquad F_g(q)=w\cdot(P_g(q)-p).
$$

At $q=1$ every resolution has $P_g(1)=p$. The derivative equations make $F'_g(1)=0$ at each resolution. These local identities alone do not determine the sign away from one. The interval calculation checks the full domain. [Sign certificate](check_three_grains.py)

Run `python -I -B -O check_three_grains.py` from this directory. The checker encloses the three linear equations by Cramer's rule and 48-digit outward-rounded interval arithmetic. On $[0,0.95]$ and $[1.05,64]$ it encloses $F_g$ itself on closed subintervals. On $[0.95,1.05]$ it bounds $F_g''$ below; the exact zero and zero derivative at one then imply strict positivity elsewhere in that interval. For $q\ge64$, each score is divided by the largest input weight raised to $q$. Every smaller rescaled weight is bounded between zero and its value at 64. For logarithms and exponentials the checker extends each correctly rounded result by one representable neighbor on each side. The following conservative limits hold throughout the indicated domains. [Python decimal arithmetic](https://docs.python.org/3/library/decimal.html#decimal.Decimal.ln)

| Resolution | Lower bound for $F_g$ on the two outer finite intervals | Lower bound for $F_g''$ on the central interval | Lower bound for $F_g$ at $q\ge64$ |
| --- | ---: | ---: | ---: |
| Whole mask | $9.94\times10^{-7}$ | 0.2053 | 0.19718 |
| Sites | $1.21\times10^{-5}$ | 0.1576 | 0.19718 |
| Oriented ports | $1.37\times10^{-6}$ | 0.0799 | 0.19718 |

The endpoint values are convenient independent checks. As $q\downarrow0$, positive cells become equally weighted at their respective resolution, giving $F_g(0^+)\simeq0.45858337,0.30528411,0.24317310$ for whole mask, site and port. As $q\to\infty$, every resolution gives the limiting target indicators $(0,0,0,0,0,0,1,1)$. All three limits are $0.19718595$ to the precision shown. The curvatures at one are approximately $0.46757144,0.40170894,0.40173731$.

In the common-mode model, strict positivity of $F_g(q)$ away from one makes $L=0$ equivalent to $q=1$ almost surely on launches with positive gain. The data at exponent one are identical at the three resolutions, so the test cannot determine the detector resolution on those modes. The signed sum closes the explicit individual-site counterexample to the two-resolution contrast. It does not identify an arbitrary response function on untested weights.

## Precision of an experimental comparison

For independent binary shots within each setting, let $N_j>0$ be the assigned counts in the ten arms. With probability at least $1-\alpha$, all ten rate errors satisfy $e_j=\sqrt{\log(20/\alpha)/(2N_j)}$ as simultaneous absolute upper bounds. The coefficients of the measured rates in $L$ are $w_i$ on the eight table rows, with $w_2$ replaced by $w_2-c$, plus $-\sum_iw_i+2c$ on $Y_0$ and $-c$ on $Y_{3,1}$. Multiply their absolute values by their corresponding $e_j$ and sum to obtain $e_L$. For equal arm sizes the multiplier is approximately 7.234334. Also $e_B=e_2+e_{3,1}+2e_0$. These bounds account for reusing the same arms in the gain estimate and the signed contrast. [Hoeffding's inequality](https://doi.org/10.1080/01621459.1963.10500830)

When $\widehat L>e_L$ the observed contrast separates the data from ordinary response in the declared family. Conversely, finite precision permits exponents close to one. For a fixed closed exponent range $S$ separated from one, take a certified lower bound $v>0$ for every $F_g(q)$ on $S$, including endpoint limits when relevant. The gain-weighted fraction of modes in $S$ is then at most $(\widehat L+e_L)/[v(\widehat B-e_B)]$ whenever the denominator is positive and the intervals permit the model. A lower bound on each mode's gain would be needed to control its frequency per original launch. Stable gains and mode distributions across both clocks remain physical assumptions of the experiment.


For the concrete range $0<q\le1/2$ or $q\ge2$, the checker also certifies **$v=0.06$** at every resolution over the full two tails. For example, a valid upper confidence limit $L/B\le0.006$ bounds the gain-weighted fraction in this range by 10%. This is a proposed precision target. The cited datasets do not supply the ten required rates.

Where changing the clock could itself change the detector, a second design uses one five-tick source and calibrated terminal permutations at a common read time. Three successive comparisons isolate the same three resolutions. It requires more control over routing. [Single-clock design and exact port assignments](routed_resolutions.md)
