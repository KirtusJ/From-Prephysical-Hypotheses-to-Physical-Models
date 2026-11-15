# How early can a fixed detector exclude 55 stochastic states?

Director G research note for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Prepare site zero on rail R of the five-site Hadamard walk. Write p(t) for its ideal probability of returning to that same port at tick t, measured once on a fresh launch. A rival predicts q(t) = αPᵗb from one launch distribution, one row-stochastic matrix with at most 55 states, and one fixed readout vector in [0,1]. Define T★ as the earliest T for which no rival fits all p(0),…,p(T) exactly. **Then 56 ≤ T★ ≤ 79.** The upper bound is the previously established degree-26 recurrence result. Two finite sets of ticks also admit explicit, very small, worst-case error margins. [Pinned recurrence and spectrum](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/3941409ac22febbac7fe0f937e22ca0477aab857/Director_G/persistent_walk/Return_at_one_port.md)

| Terminal settings | Settings | Latest tick | At least one absolute probability error exceeds |
|---|---:|---:|---:|
| All ticks 0 through 79 | 80 | 79 | 10⁻⁴¹ |
| Even ticks 0 through 132 | 67 | 132 | 10⁻⁵¹ |

## A 55-state model fits through tick 55

Give states 0,…,54 readouts p(0),…,p(54), start at state zero, and advance deterministically until state 54. Its next transition enters state zero with probability p(55) and state one otherwise. Because p(0)=1 and p(1)=0, tick 55 has exactly the required readout. Integer walk propagation gives p(55) = 21627680410249/36028797018963968. Thus even exact data through that tick cannot decide against the full 55-state class.

## The even-clock frequencies

The signed even-time amplitude is [1+uⁿ+u⁻ⁿ+vⁿ+v⁻ⁿ]/5 at t=2n. The square has thirteen distinct nodes uⁱvʲ, with exponents (0,0) and both signs of (1,0), (0,1), (2,0), (0,2), (1,1), (1,−1). Their distinctness follows from the pinned independence proof, and each has a strictly positive coefficient. In particular the coefficient at η=u/v is 2/25. The ideal even trace has an order-13 recurrence. The rival on the same clock has transition P², whose characteristic polynomial has degree at most 55 and a root at 1. The two recurrence polynomials share this root, so their least common multiple has degree at most 67 and annihilates the difference. Agreement at the first 67 even times would imply agreement on all even times, contradicting the two-phase density and finite-chain convergence theorem. This saves settings at the cost of a longer final tick. Neither bound asserts a minimal number of settings.

## Uniform error on each finite grid

Pad the rival to 55 states with unused absorbing states. On the chosen clock write $Q=P$ or $P^2$, and $\chi(X)=\det(XI-Q)$. For a unit node $z$, put $d(z)=\min_{1\leq k\leq55}|1-z^k|$. Each eigenvalue $\lambda$ of $Q$ satisfies $|z-\lambda|\geq d(z)^2/440$. To see this, take an eigenvector of sup norm one and rotate its unit coordinate to one. A smaller one-step residual would, by telescoping, place a convex average of its coordinates within $k d(z)^2/440$ of $z^k$. At least one coordinate then lies at distance less than $d(z)/2$ from that center for $1\leq k\leq55$. Together with the original unit coordinate at $k=0$, the 56 disjoint neighborhoods would require 56 coordinates. [Finite-duration resolvent proof](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/3941409ac22febbac7fe0f937e22ca0477aab857/Director_G/persistent_walk/A_finite_duration_return_test.md)

Let $Z$ contain all non-torsion frequency nodes on this clock, put $s=|Z|$ and $F(X)=\prod_{z\in Z}(X-z)$. Partial fractions at the simple roots give

$$
\frac{1}{|F(\lambda)|}
\leq \sum_{z\in Z}\frac{1}{|F'(z)|\,|\lambda-z|}
\leq H,\qquad
H=\sum_{z\in Z}\frac{440}{|F'(z)|\,d(z)^2}.
$$

Multiply over the 55 eigenvalues, counted with multiplicities. The order of the two products can be interchanged, giving $\prod_{z\in Z}|\chi(z)|\geq H^{-55}$. At least one node therefore has $|\chi(z)|\geq H^{-55/s}$. This step lets the entire set of frequencies constrain a single stochastic transition matrix.

For the full clock, write $e_j=\exp(i\omega_j)$ with $\sin\omega_j=\sin(2\pi j/5)/\sqrt 2$ and $0<\omega_j<\pi/2$ for $j=1,2$. Then $e_1^2=u$ and $e_2^2=v$. The ten amplitude eigenvalues have the form $\pm e_1^i e_2^j$ with $(i,j)\in\{(0,0),(\pm1,0),(0,\pm1)\}$. Their probability frequencies are the ordered ratios. The distinctness of the phase labels follows by squaring and applying the previously proved independence of $u,v$. Along the even clock each signed pair of nodes becomes one node and its two nonnegative coefficients add. At each spatial momentum $k$, the launch weight of the positive branch $\exp(i\omega)$ is $[1+\cos k/(\sqrt2\cos\omega)]/10$. Its partner $-\exp(-i\omega)$ has the complementary weight in the block of mass $1/5$. The checker groups all 100 products of weights by their ratio, including the two zero-momentum modes $\pm1$.

Write $S$ for the forward shift of a sequence. Suppose the largest discrepancy between $p$ and $q$ on the selected grid is $\varepsilon$. By Cayley–Hamilton, $\chi(S)q=0$. Each available $\chi(S)p$ has magnitude at most $2^{55}\varepsilon$, since the absolute coefficients of $\chi$ sum to at most $2^{55}$ for eigenvalues in the closed unit disk. The constant node vanishes because $\chi(1)=0$. Let $m$ be the number of remaining nodes, including $-1$ on the full clock. For any $z\in Z$ let $D(z)$ be the product of its distances to the other $m-1$ nodes. If $c_z$ is its coefficient, applying the Lagrange polynomial at $z$ to the first $m$ values of $\chi(S)p$ extracts $c_z\chi(z)$. That polynomial has coefficient sum in absolute value at most $2^{m-1}/D(z)$. Thus

$$
\varepsilon\geq
\frac{\min_{z\in Z} c_z D(z)}{2^{55+m-1}}\,H^{-55/s}.
$$

The required indices run from 0 through $55+m-1$ on the selected clock. The checker obtains the following strict bounds by outward-rounded integer arithmetic. On both clocks every $c_z>1/100$.

| Clock | Non-torsion nodes $s$ | Nodes after removing 1, $m$ | Upper bound on $H$ | Lower bound on every $D(z)$ | Resulting lower bound on $\varepsilon$ |
|---|---:|---:|---:|---:|---:|
| Every tick | 24 | 25 | 6,000,000 | 6 | $10^{-41}$ |
| Even ticks | 12 | 12 | 3,000,000 | 5 | $10^{-51}$ |

## What finite counts would require

For N settings and the displayed margin δ, launch n independent Bernoulli trials per setting. Reject the ideal prediction when the maximum absolute difference between empirical and ideal probabilities exceeds δ/2. Under the ideal and under every rival, the corresponding one-sided decision error is at most 2N exp(−nδ²/2). Under a rival, the discrepant setting follows from the uniform margin. Thus n ≥ 2 log(40N)/δ² suffices for 5% error on each side. For example, on the 80-setting grid n = 18 × 10⁸² launches per setting is sufficient. This sufficient budget establishes finite-count distinguishability on the short grid. Its size gives no lower bound on the number of launches a better design could achieve. The calculations assume a common stable preparation, evolution and readout independent of stopping time, with every launch counted. The optimal finite horizon and achievable experimental margins remain open.

Run `python3 -I -B -O check_short_horizon.py`. It checks the 55-state prefix fit with fractions and encloses the selected spectral coefficients and distances using outward-rounded dyadic arithmetic. The finite-grid conclusions concern the specified mathematical models.
