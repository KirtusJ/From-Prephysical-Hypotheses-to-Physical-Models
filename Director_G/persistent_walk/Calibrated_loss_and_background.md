# Counting launches with calibrated loss and background

Director G research for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

A single five-site return detector still distinguishes the specified noisy walk from every homogeneous stochastic predictor with at most 55 states under the following calibration. The true port-detection efficiency is at least 90%, the probability of an independent background click per terminal read is at most 1%, and the per-tick probability of loss or reset is at most four in ten million. Two choices trade coherence duration against independent launches.

| Maximum tick | Independent launches | Prespecified threshold | Stochastic mean at most | Noisy-walk mean greater than |
|---:|---:|---:|---:|---:|
| 999,996 | 14,100 | 0.05118 | 0.043808 | 0.0585539 |
| 1,799,996 | 2,400 | 0.0319 | 0.013521 | 0.0502698 |

Each row bounds both one-sided errors individually below 5%. The calibration values are assumptions. No instrument measurements or optimal design claim enter either row.

## Record and noise law

Use the sharp preparation at site zero on the right rail of the open five-site Hadamard ring. For each launch, draw independent uniform integers $J,K$ on $0,\ldots,N-1$. Stop at $t=2L$ ticks with $L=J+K$. In the first row $N=250{,}000$, and in the second $N=450{,}000$. A click at the launch port gives $C=1$ and every other terminal outcome gives $C=0$. Every launched trial counts. Use the same single-port score $Y=(C-1/2)\operatorname{Re}(\zeta^{-L})$ from the earlier design. For the upper unit phases $u,v$ with real parts $(3-\sqrt5)/8$ and $(3+\sqrt5)/8$, respectively, $\zeta=u/v$. Reject the stated class when the mean score reaches the selected row's threshold. The settings are fixed before data collection. [Original design and frequency certificate](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/f9da544f6b438fca30b195854f47a7f480ee0630/Director_G/persistent_walk/Shorter_return_test.md)

Independently each tick, the walk follows the ideal dynamics with fixed probability $r$, where $0.9999996\le r\le1$. Otherwise it either undergoes permanent loss ($c=0$ throughout the experiment) or resets to the invariant, maximally mixed state on the ten modes ($c=1/10$ throughout). The raw port probability is $c+r^t(p_t-c)$, where $p_t$ is the ideal probability. A true port event triggers detection with fixed probability $\eta\ge0.90$. An independent background event triggers a click with fixed probability $0\le d\le0.01$ irrespective of the true outcome. The binary detector registers either event. Thus

$$\Pr(C=1\mid t)=d+A\{c+r^t(p_t-c)\},\qquad A=(1-d)\eta\ge0.891.$$

The same budgets also cover both mechanisms acting together. Suppose each tick independently has survival probability $s$ and, conditional on survival, retains ideal coherence with probability $q$ or resets to the maximally mixed state. Write $r=sq$. Provided $r\ge 0.9999996$, the raw port law is $r^t p_t+(s^t-r^t)/10$. The reset-only and loss-only laws are recovered at $s=1$ and $q=1$, respectively. In this joint model $r$ is the probability per tick of surviving and following the ideal step. The lower bound is on that product.

The alternative needs these dynamics, a fresh preparation for each launch, and independence of the terminal choice from the evolution. The competing class only requires its observed click law to admit $\alpha P^t b$, with one fixed launch distribution, one row-stochastic matrix of dimension at most 55, and one fixed response $0\le b\le\mathbf1$. Background events at fixed rate and detection efficiency can be absorbed into the terminal response. Hidden clock and loss states used by this representation count toward the state budget. Both error bounds require independent launches.

## Attenuation at the sampled times

Write $H_N(x)=N^{-1}\sum_{j=0}^{N-1}x^j$ and $M=\{1,u,\bar u,v,\bar v\}$. For an ordered pair $a,b\in M$, multiplying its ideal even-tick frequency $(a/b)^L$ by $r^{2L}\zeta^{-L}$ and averaging gives $H_N(r^2(a/b)/\zeta)^2$. The two pairs with $a/b=\zeta$ supply $2H_N(r^2)^2/25$. This includes every sampled stopping time. At the calibration floor $r_0=0.9999996$ the mean surviving fraction $H_N(r_0^2)^2$ exceeds 0.8214641 and 0.7052443 for the two rows. Survival at the single longest run is about 0.6703211 and 0.48675296, respectively.

For any unit phase $w$, the identity $|1-r^2 w|^2=(1-r^2)^2+r^2|1-w|^2$ bounds the sidelobes. The earlier checker established chord separations $|1-(a/b)/\zeta|>0.23$ for all 23 remaining ordered pairs, $|1-\zeta|>0.60$, and $|1-\zeta^2|>1$. The geometric sum at any nonresonant phase has numerator of modulus at most two. Since $0\le c\le1/10$, $A\le1$, and $|d+Ac-1/2|\le1/2$, the alternative mean is bounded below by

$$
0.891\frac{2}{25}H_N(r_0^2)^2
-\frac{23}{25}\left(\frac{2}{0.23 N r_0}\right)^2
-\frac2{10}\left(\frac{2}{0.60 N r_0}\right)^2
-\frac12\left(\frac{2}{0.60N}\right)^2.
$$

The term with coefficient $2/10$ covers the two reset contributions at damping factors $s$ and $r$, each at least $r_0$. For the joint law the remaining constant is $d-1/2$ and has magnitude at most one half. The stochastic upper bound is $\tfrac12(74{,}000/N)^2$ by the previous 55-state resolvent proof. The score has the same second moment for every binary click law since $Y^2=\cos^2(L\arg\zeta)/4$. Hence $\operatorname{Var}(Y)\le V=(1+(2/N)^2)/8$. For the smaller of the two proven margins $\delta$ between the chosen threshold and the corresponding mean bound, the one-sided Bernstein inequality gives $\exp[-m\delta^2/(2(V+\delta/3))]$. In the first row this is below 0.0495, and in the second below 0.0456. These bounds concern only the declared stochastic class and noisy alternative. A different noise law or an uncalibrated time-dependent background requires a separate calculation.

## What a dark-count floor changes about exact realization

For pure loss, the prior zero-background result excludes *every* exact finite stochastic representation for each $0<r<1$. Once the click floor is a fixed $0<d<1$, the observed law $d+A r^t p_t$ admits an exact realization with some finite number of states. This holds however small $d$ is. Take a finite prefix of length $k$ so $A r^k\le\min(d,1-d)$. Expand $p_t$ in cosines with nonnegative weights summing to one. For each frequency $\omega$ choose a regular polygon containing $r e^{i\omega}$ and express the latter as a convex combination of its vertices. A cyclic random walk with these vertex increment probabilities has phase mean $(r e^{i\omega})^s$ at time $s$. Choose the frequency block according to its cosine weight at the end of the prefix. A block readout $d+A r^k\cos(k\omega+2\pi j/n)$ at vertex $j$ of an $n$-gon now gives the exact tail. Use the prescribed click probabilities for the prefix. The same interior-baseline argument was used for reset in the [loss and reset study](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/f9da544f6b438fca30b195854f47a7f480ee0630/Director_G/persistent_walk/Loss_and_reset_at_one_port.md).

The construction gives no 55-state upper bound. Thus a strictly positive background can allow an exact finite realization while the calibrated test still excludes every model at or below the stated budget at its specified error rates.

## Reproduction

Place [the pinned frequency checker](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/f9da544f6b438fca30b195854f47a7f480ee0630/Director_G/persistent_walk/check_shorter_return.py) beside the companion program and run

~~~sh
python -I -B -O check_calibrated_return.py
~~~

The checker reruns the frequency tests, encloses the geometric means by integer interval exponentiation, and proves both sampling certificates with rational arithmetic and a finite positive exponential series.
