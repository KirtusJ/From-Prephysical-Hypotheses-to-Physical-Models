# A lower exposure bound for adaptive routed-mass selection

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Under the [two-detector pair protocol](Exposure_for_two_paired_detector_laws.md) at $M=10^{-8}$, even a policy selecting each next mass using its full observed history needs **more than 3.800930 quadrillion pairs** for 5% equal-prior error. Repeating a single mass suffices at 3.800950 quadrillion. The difference is at most 20 billion pairs, or less than 5.27 parts per million of that demonstrated exposure. The exact advantage, if any, is unresolved. These are hard caps, including early decisions within the cap.

### Simulating an adaptive experiment

Use a Brownian coordinate $X$ of variance one per unit clock time, starting at zero, with drift $+1/2$ under $P$ and $-1/2$ under $Q$. At deterministic time $T$ its path likelihood ratio is $\exp(X_T)$ and its optimum equal-prior error is $\Phi(-\sqrt T/2)$. This auxiliary clock carries no physical time interpretation. [Change of measure for Brownian drift](https://www.math.uchicago.edu/~lawler/finbook.pdf)

For a chosen mass sort the four cells by $p_j/q_j$. Build a balanced two-level binary tree. Each group's value is its conditional mean of $p_j/q_j$ under $Q$; the root is one. Starting at the log of the current value, run the coordinate to either child log value. Under $Q$ the exponential coordinate is a martingale. The bounded stopped exponential therefore gives exactly the $Q$ branching probabilities by linear interpolation. The likelihood tilt gives the $P$ probabilities as well: the terminal branch probability under $P$ is its $Q$ probability times the ratio of child to parent values. This follows first on exit by a finite horizon and then by taking the horizon to infinity; exit has finite mean under both drifts as shown below. If the child values coincide, split by the corresponding $Q$ probabilities using an independent coin; the branching probabilities under $P$ are then the same. Deterministic zero-probability leaves at controls can be omitted. Identical-law controls need only independent randomness.

The emitted cell and log increment have the exact one-pair laws. Restart in relative coordinates at each leaf. Feed only the emitted cells and the policy's own random seed back to the mass selector. The strong Markov property yields the correct transcript under both laws, even when masses depend on earlier outcomes.

### Bounding clock use uniformly over the schedule

The [interval checker](check_adaptive_clock.py) verifies that all informative leaf log ratios lie between $-b$ and $b$ for $b=4.82\times10^{-7}$. Each tree edge is an exit from an interval $[l,r]$ of width at most $2b$. The function $(x-l)(r-x)/(1-b)$ is nonnegative inside and zero on the boundary. For either drift its generator is at most $-1$, since the quadratic has second derivative $-2$ and first derivative of magnitude at most $2b$ before division. Optional stopping at exit or a bounded time and then monotone convergence give mean exit time at most $b^2/(1-b)$. From any intermediate history within a pair, the remaining expected time is at most $K=2b^2/(1-b)$.

Let $\tau$ be the full time for one pair. Stopping the drift-subtracted Brownian martingale gives mean clock $m=2D(P_s\Vert Q_s)$ under $P$, and $m=2D(Q_s\Vert P_s)$ under $Q$. The stopping argument follows by truncating, since the pre-exit coordinate is bounded and the time has finite mean. The computed maximum of these means over the nodes and both laws is approximately $2.84723366208\times10^{-15}$.

For completeness the conditional moments satisfy $\mathbb E\tau^k\le k!K^{k-1}m$. Apply the identity $\tau^k=k\int_0^\tau(\tau-u)^{k-1}\,du$ and induct on residual moments from any live history, whose remaining mean is at most $K$. Thus for $0<\lambda<1/K$, the log moment generating function of $\tau-m$ is at most $mK\lambda^2/(1-\lambda K)$. These statements condition on the past and chosen mass. With $\mu=N\max m$, iterated conditioning bounds total clock $S_N$ under either law by
$$\Pr(S_N>\mu+\delta)\le\exp\left(-\frac{\delta^2}{4K\mu+2K\delta}\right).$$
Use $\lambda=\delta/[K(2\mu+\delta)]$ in the exponential bound. A shorter experiment can be padded to $N$.

### Deterministic-horizon comparison

At $T=\mu+\delta$ the Brownian observer simulates the transcript decision if it finishes on time and makes an arbitrary decision otherwise. This increases risk by at most the overflow probability. Conversely no such observer beats the optimal deterministic-time Brownian test. It follows that the original risk is at least the Gaussian error minus the overflow bound.

For $N=3{,}800{,}930{,}000{,}000{,}000$ and $\delta=0.000020$, interval arithmetic gives $T<10.822156$, overflow below $2.31\times10^{-9}$, and risk **above 0.0500001385**. This excludes every randomized adaptive policy at that cap and all smaller caps. The physically relevant count is in pairs, two launches per pair. Fresh independent types across pairs, the two specified lossless laws, a finite routed mass menu and a deterministic exposure cap are essential to the stated result. A same-family second reader checked the embedding, likelihood tilt, residual-time moments and risk comparison. No detector data were acquired.
