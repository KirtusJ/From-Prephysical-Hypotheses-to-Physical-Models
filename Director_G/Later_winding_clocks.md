# How long a ring must run to reveal its winding mixture

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On a 16-well ring, two specified populations first give different terminal records at tick 81. Distinguishing them with both errors at most 5% using clocks through 81 requires more than $10^{24}$ independent launches. At tick 144, the same source and four named output ports meet those error targets with 163 launches. The later clock changes where histories with different windings can interfere. All probabilities below are predictions of the balanced walk. [Earliest-clock result](Fixed_ring_winding_weights.md#launch-cost-at-the-earliest-clock)

## The test at tick 144

Launch from well zero on the right rail. At each tick the balanced Hadamard coin acts on the two rails, $R$ moves one well clockwise, and $L$ moves one well counterclockwise. Consecutive left steps contribute a minus sign. A left step also contributes a phase $e^{2\pi i s/q}$, with $q=21$. For the two populations, the label $s$ has probability $[1\pm\cos(2\pi\cdot 80s/21)]/21$, respectively. Every launch draws a fresh label. The terminal well and rail have ideal calibrated responses, and every launch enters the denominator.

Record a hit when the final rail is $R$ and the well is $0,4,8$ or $12$. The read time was chosen after examining the model at clocks 81 through 220. It involves one binary observation per launch.

At tick 144 the hit probabilities are **0.4294360477** under plus and **0.3055997206** under minus. Those four ports are exactly the ones at which the plus law exceeds the minus law. Their difference, **0.1238363272**, is therefore the full one-launch total variation. At ticks 81 and 82 the full distances are only $2^{-80}$ and $79\,2^{-80}$. Translating the four right-rail detectors by two wells at tick 144 reverses the sign of their contrast. At ticks 143 and 145 all four detectors are dark because every path reaches an odd well.

For the exact rates, let $a_j$ be the signed number of histories at one oriented port with left-step count congruent to $j\bmod 21$. Squaring its character amplitude and averaging over $s$ selects equal exponents and the lags $\pm17\bmod21$, since $80\equiv17\pmod{21}$. The two port probabilities are
$$2^{-144}\left(\sum_j a_j^2\ \pm\sum_j a_j a_{j+17}\right).$$
Summing over the four ports gives numerators $598546492470538701899396757872292453252737$ and $425943843822132599281979972562490031225077$ with common denominator $2^{140}$. Physical ring counts and a separate line recurrence folded by well and gain give the same integers. [Lean calculation](lean/LaterWinding.lean) · [Exact rates and controls](results/later_winding.json)

With $m$ independent launches, the hit count $X$ is binomial with one of those two rates. A decision at a tie uses a fresh independent random draw.

| Launches | Choose plus if | Error under $+$ | Error under $-$ |
|---:|---|---:|---:|
| 163 | $X>60$, or with probability $9/10$ at $X=60$ | 4.933372% | 4.996791% |
| 168 | $X\ge62$ | 4.773006% | 4.613831% |

**163 is the minimum for this bit at this clock.** The likelihood ratio of the ordered record increases strictly with its hit count, so assigning the largest counts to plus maximizes power at any fixed minus error. At 162 launches the most powerful test of minus error $1/20$ chooses plus above 59 hits and randomizes at 59 with probability approximately $0.224334241846$. Its plus error exceeds $0.050710954422$. Any test using fewer launches could be run on the first part of a 162-launch record. The checker compares the binomial tail sums as rational numbers. Reading all ports on each repetition or choosing a different clock could change the minimum. [Neyman and Pearson on most powerful tests](https://doi.org/10.1098/rsta.1933.0009)

### If the phase label persists

If the source draws one label for the entire run, the single-launch hit probabilities still hold. Conditional on that label, the two populations generate records by the same rule. Applying any such rule, including adaptive clock choices, can only decrease the total variation between the two label distributions. Their distance is $\frac1{21}\sum_{l=0}^{20}|\cos(2\pi l/21)|=\csc(\pi/42)/21$. The positive cosines occupy the eleven centered residues $-5,\ldots,5$. Their sum is $\sin(11\pi/21)/\sin(\pi/21)$, and the sum of all 21 cosines is zero. The minimum equal-prior error is therefore at least $(1-\csc(\pi/42)/21)/2\approx18.1393\%$, however long the run. An application of the launch budget needs evidence that the source refreshes between launches.

## How far the first-clock obstruction extends

For $N\ge3$ wells let $D=N/\gcd(N,2)$, $Q=q/\gcd(D,q)\ge2$, $K=\lfloor Q/2\rfloor$, and $L=KD$. The two reduced-label populations have masses $(1\pm\cos(2\pi K l/Q))/Q$ at $l$. Their cosine moment difference at harmonic $g$ is
$$\Delta J_g=\mathbf1_{g\equiv K\bmod Q}+\mathbf1_{g\equiv-K\bmod Q}.$$
Both terms contribute when $Q$ is even. Distinct windings first enter different terminal probabilities at $T=L+1$ for this pair.

Write $t=T+h$ and $n=t-1$. After fixing the last rail, two paths with prefix left counts $j$ and $j+gD$ reach the same well. Only $g\ge K$ can contribute a difference. Put $e=n-gD$. Then $0\le j\le e$. The magnitudes of the two signed prefix counts are bounded by $\binom nj$ and $\binom n{e-j}$. Summing their products over $j$ gives the upper bound $\binom{2n}e$ by choosing $e$ objects from two sets of size $n$. The factor two from squaring cancels the half in total variation. Summing both final rails gives
$$\delta_t\le 2^{1-t}\sum_{g=K}^{\lfloor n/D\rfloor}\Delta J_g\binom{2n}{n-gD}
 \le 2^{2-t}\sum_{e=0}^h\binom{2n}e.$$
The first inequality is sharp at $h=0$. At any fixed $h$ the final expression is $O_h(T^h2^{-T})$, uniformly in the ring and phase order. A few extra ticks therefore leave this pair exponentially difficult to distinguish as $T$ grows.

### A bound from the propagation speed

There is also exponential suppression for $t\le(\sqrt2-\varepsilon)L$ at any fixed $0<\varepsilon<\sqrt2-1$. Let $A_t(y,r)$ be the normalized signed amplitude on the line. A lag $gD$ in left counts pairs amplitudes at $y$ and $y-2gD$ on the same rail. After the triangle inequality over ring outputs, its contribution to $\delta_t$ is at most $\Delta J_g\sum_{y,r}|A_t(y,r)A_t(y-2gD,r)|$. For $\lambda>0$, Cauchy–Schwarz bounds this sum of products by $e^{-2\lambda gD}\|e^{\lambda y}A_t\|_2\|e^{-\lambda y}A_t\|_2$.

In Fourier coordinates the positively tilted step is $M=U_k E_\lambda H$, with $U_k=\operatorname{diag}(e^{ik},e^{-ik})$, $E_\lambda=\operatorname{diag}(e^\lambda,e^{-\lambda})$, and $H$ the normalized Hadamard coin. Because $U_k$ and $E_\lambda$ commute, $M^2=U_k(E_\lambda H E_\lambda)U_k H$. The outer factors are unitary. This real symmetric matrix has determinant $-1$ and trace $\sqrt2\sinh(2\lambda)$. Its norm is $e^{2\eta}$ for $\eta=\tfrac12\operatorname{arsinh}(\sinh(2\lambda)/\sqrt2)$. The same norm holds under the negative tilt. Taking pairs of steps, allowing $e^\lambda$ for an odd last step, and applying Parseval bounds each weighted line norm by $e^{t\eta+\lambda}$. Since $\Delta J_g\le2$, summing over all $g\ge K$ gives
$$\delta_t\le\frac{2e^{2\lambda}}{1-e^{-2\lambda D}}\exp(2t\eta-2\lambda L).$$
As $\lambda\downarrow0$, $\eta/\lambda\to1/\sqrt2$. Choose $\lambda$ small enough that $(\sqrt2-\varepsilon)\eta<\lambda$. Since $D\ge2$, the prefactor is bounded uniformly, giving exponential decay in $L$. This estimates winding interference before the two separated line amplitudes overlap appreciably. The exact time that optimizes a finite experiment remains open. Sunada and Tate derive related line-walk large-deviation asymptotics. [Line-walk asymptotics](https://doi.org/10.1016/j.jfa.2011.12.016) · [Earlier cubic front calculation](Unfiltered_winding_fronts.md)

Both results assume a sharp right launch, the specified balanced coin, a finite winding mixture, and terminal detection on the unfiltered ring. Experimental frequencies and the choice of an underlying physical law remain open.
