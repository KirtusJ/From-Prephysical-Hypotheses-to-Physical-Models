# A finite-duration test of the homogeneous 55-state model

Consider the unrestricted real Hadamard walk on a ring of five sites, starting at site zero on the right rail. The target is the unconditional probability of returning to that port, in a fresh preparation measured once at the chosen time. A competing model has this probability in the form $f_t=\alpha P^t b$, where $\alpha$ is one initial distribution, $P$ one row-stochastic matrix with at most 55 states, and the components of $b$ are in $[0,1]$. Any clock phase or shared preparation memory that influences the response counts toward the state budget. An absorbing loss state or a substochastic matrix can instead be handled by a suitable state accounting. The numerical bound below is proved for a row-stochastic factorization within the stated budget.

## A uniform bound without a mixing-rate assumption

Take a point $\zeta$ on the unit circle with $d_h=\min_{1\le k\le h}|1-\zeta^k|>0$. Then
$$
\| (\zeta I-P)^{-1}\|_\infty\le 8h/d_h^2.
$$
To prove this, choose any complex vector $v$ of sup norm one and let $\epsilon=\|Pv-\zeta v\|_\infty$. Rotate the vector so one component $v_i=1$. Contraction and telescoping give $|(P^k v)_i-\zeta^k|\le k\epsilon$. The left entry of the comparison is a convex average of at most $h$ points $v_j$ in the closed unit disk. At least one point has real projection onto $\zeta^k$ of at least $1-k\epsilon$, hence distance at most $\sqrt{2k\epsilon}$ from $\zeta^k$. For $k=0,\ldots,h$ the centers are pairwise at least $d_h$ apart. If $\epsilon< d_h^2/(8h)$, every center needs a different $v_j$, impossible with at most $h$ points. This proves the inequality and invertibility in finite dimension.

## Randomize the measured time

Independently and uniformly sample $J,K$ from $\{0,\ldots,n-1\}$ and measure at $t=|J-K|$. Score a return at the chosen port by $\operatorname{Re}\zeta^{J-K}$ and every other outcome, including loss, by zero. The mean score is
$$
n^{-2}\Big(n f_0+2\sum_{t=1}^{n-1}(n-t) f_t\operatorname{Re}\zeta^t\Big).
$$
For a Markov model write $g_t=f_t-1/2=\alpha P^t(b-\mathbf1/2)$. The geometric sum and the resolvent bound give $|\sum_{t=0}^{k-1}\zeta^{-t}g_t|\le8h/d_h^2$. Here $\|I-(P/\zeta)^k\|_\infty\le2$ and $\|b-\mathbf1/2\|_\infty\le1/2$. The triangular sum for $g$ is twice the real part of the sum of these prefix sums for $1\le k\le n$, minus $ng_0$, all divided by $n^2$. The subtracted term costs at most $1/(2n)$. The constant contribution is $|\sum_{j=0}^{n-1}\zeta^j|^2/(2n^2)$. The total mean score is at most
$$
\frac{16h}{nd_h^2}+\frac{1}{2n}+\frac{2}{n^2|1-\zeta|^2}.
$$

For a unitary walk, the return amplitude is $\sum_j w_j\lambda_j^t$, with $\lambda_j$ on the unit circle and nonnegative weights $w_j$ obtained from the launch state's spectral projections. Its squared modulus $f_t$ extends to an even sequence at negative times. Each ordered pair of modes contributes a nonnegative quantity to the score, since averaging over both $J$ and $K$ gives a squared geometric sum divided by $n^2$. Equivalently, write the cosine as the real part of $\zeta^{-(J-K)}$ and use the evenness of $f$. Pairs with $\lambda_j/\lambda_l=\zeta$ contribute exactly $w_jw_l$ for every $n$.

## Specialization to the five-site ring

Let $k_1=2\pi/5$, $k_2=4\pi/5$, $\omega_i=\arcsin(\sin(k_i)/\sqrt2)$ and $\zeta=\exp(i(\omega_1-\omega_2))$. In a convention with right shift represented by $e^{ik}$, the two eigenvalues of each Fourier block are $e^{i\omega}$ and $-e^{-i\omega}$. For the first branch the sharp-launch spectral weight is $w_i=(1+\cos(k_i)/(\sqrt2\cos\omega_i))/10$, including its Fourier-site factor $1/5$. This follows from the diagonal entry of the spectral projector $(U_k+e^{-i\omega_i}I)/(2\cos\omega_i)$ and $(U_k)_{RR}=e^{ik_i}/\sqrt2$. The second weight is $w'_i=1/5-w_i$. The positive branches for $(k_1,k_2)$ and $(-k_2,-k_1)$ contribute to the selected ratio, as do the negative branches for $(k_2,k_1)$ and $(-k_1,-k_2)$. Thus the ideal score is at least $2(w_1w_2+w'_1w'_2)$.

This selected ratio is also provably non-torsion. The products $(1+\cos^2k_1)(1+\cos^2k_2)$ and $(1-\cos^2k_1)(1-\cos^2k_2)$ are $29/16$ and $5/16$. Thus $w=\zeta+\zeta^{-1}=(\sqrt{29}+\sqrt{5})/4$. The square $w^2=(17+\sqrt{145})/8$ has field norm $9/4$ over $\mathbb Q$. A root of unity would make $w^2$ an algebraic integer, which has integer norm. Consequently $d_h>0$ for every finite $h$. The Markov score bound tends to zero as $n$ grows at fixed $h$, whereas the ideal score always exceeds the indicated positive weight. Since every run scores in magnitude at most one and the time weights average to one, the supremum over all durations of the absolute return-probability error of any single finite-state rival is at least that weight. The maximizing time need not be common across rivals.

The accompanying integer interval calculation gives $d_{55}>0.10043$ and $2(w_1w_2+w'_1w'_2)>0.03257$. It uses square roots of rational radicals for each sine and cosine, with outward rounding after every operation. With $n=5{,}000{,}000$, the ideal mean exceeds $0.0325$ and the Markov mean is below $0.0177$. For the fixed threshold $0.0251$, 109,414 independent launches suffice for a one-sided error probability at most 0.05 on each specified side by Hoeffding's bound for scores in $[-1,1]$. The threshold and frequency are fixed in advance. This is one deliberately conservative construction. The longest possible scheduled run lasts 4,999,999 ticks.

The finite test assumes stable independent launches, a common detection rule, and no advance dependence of the initial state or transitions on the randomly selected terminal time. Loss and dephasing can suppress the ideal score. The calculation predicts separation for an ideal model and proves a uniform bound for the specified stochastic class. It establishes no physical count, guaranteed power for an uncalibrated instrument, or optimal sample budget. With the state budget free, a counting chain of $T+1$ states can encode any return sequence through tick $T$ in its fixed readout vector. No finite record rules out all finite budgets.

Run from the note's directory:

~~~sh
python -I -B check_finite_witness.py
~~~
