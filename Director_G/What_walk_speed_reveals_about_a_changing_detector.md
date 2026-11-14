# What the speed of a walk reveals about a changing detector

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch the one-dimensional Hadamard walk from a single well. An observer records the absolute displacement from that well divided by the flight time. **If microscopic site or rail weights are raised to a common power on each launch, the population's speed distribution approaches the ordinary one exactly when its powers approach one in probability.** The source coin can be unknown, differ on every launch, and correlate with the exponent and the choice of which rails to resolve. This removes the fixed detector population and calibrated rail launch used in the [sharp-source front test](Microscopic_position_weights_at_a_classical_front.md). It also gives a different, finite test when the apparatus pools equal radii *before* powering.

## Why speed removes the incoming coin

Use the real Hadamard \(H=2^{-1/2}\bigl(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\bigr)\) followed by the right/left conditional shift on the line. Preparation is a sharp position and any two-dimensional coin density matrix \(\rho\). Set \(J=\bigl(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\bigr)\). Reflection of position together with \(J\) commutes with the shift, and \(JH=-HJ\). Thus the full transformation commutes with one step up to a minus sign. At any tick \(t\), the initial-coin effect of a reflection-symmetric set of sites commutes with \(J\): the final position projector is invariant and the two factors of \((-1)^t\) cancel. This effect is real symmetric since the walk and the projector are real. A real symmetric two-by-two matrix commuting with \(J\) is scalar. Consequently the ordinary probability of **every** radius set at finite \(t\), with both final rails included, is identical for all pure and mixed coins. Reality matters here: the commutant among arbitrary complex Hermitian matrices also contains \(iJ\).

Write \(s=1/\sqrt2\). The ordinary speed law \(R_t\) at speed \(|x|/t\) has weak limit \(R\) with density
\[
 g(z)=\frac{2}{\pi(1-z^2)\sqrt{1-2z^2}},\quad 0<z<s .
\]
For example take a sharp right coin and add the positive and negative velocity densities. The scalar identity makes this the same limit for any varying sequence of coins. In particular \(R\) has no atom at \(s\), and \(R(S_\epsilon)\) is bounded above and below by positive constants times \(\sqrt\epsilon\) for \(S_\epsilon=[s-2\epsilon,s-\epsilon]\) at small \(\epsilon\). For each fixed such shell the finite probabilities converge. [Konno's limit theorem](https://arxiv.org/abs/quant-ph/0206103) · [Finite-dimensional radial certificate](lean/SpeedCoin.lean)

## Microscopic weights and a population that changes with flight length

At each site either keep a single cell or its two rail cells, then power all the cells of that launch by one exponent \(q\in[0,\infty]\) and normalize. At \(q=0\) count each nonempty cell once. At \(q=\infty\) any normalized choice on the cells of maximum weight is allowed. The choice at each site can depend on the clock, the exponent and the input state. The terminal record retains the radius of the selected cell. The sole use of a split in the proof is that there are at most two nonnegative weights per site summing to the ordinary site weight. This permits an arbitrary local terminal rail basis as well. The read counts every launch and has no position-dependent censorship, extra spatial bins before the power, or intervening instruments.

Let \(Q_t\) be the population exponent at clock \(t\), and let \(D_t\) be the reported speed distribution. The theorem asserts
\[
 D_t\ \Rightarrow R \quad\Longleftrightarrow\quad
 \Pr(|Q_t-1|>\eta)\longrightarrow0\quad\text{for each }\eta>0 .
\]
It also holds along any unbounded sequence of integer clocks. These are properties of the specified model's probability laws. Finite experimental samples cannot on their own establish a weak limit over all clocks.

**Uniform inputs to the proof.** Outside a fixed neighborhood of speed \(s\), each cell has \(tw_i\le M\) for all clocks and coins. This follows from the Fourier estimate through both fronts; its proof also gives \(d_{\rm TV}(P_{q,t},P_{1,t})\le A|q-1|\) for \(|q-1|\le1/4\) with an absolute \(A\), even on microscopic cells. Any fixed \(S_\epsilon\) contains at most \(C t\epsilon\) cells at sufficiently late clocks, counting both signs and both rails, and the ordinary weight summed there is exactly \(R_t(S_\epsilon)\) regardless of the hidden type. The total cell count is at most \(2(t+1)\). [Uniform estimates and their grid proof](Uniform_stability_of_microscopic_arrival_probabilities.md) · [Interior and front asymptotics, Sunada and Tate](https://arxiv.org/pdf/1108.1878)

**High powers.** Uniformly over every localized coin and partition, \(t\sum_i w_i^2\to\infty\). Indeed for each fixed dyadic partition of \([0,1]\) of width \(\Delta\), there are at most \(C(t\Delta+1)\) cells in each bin \(I\). By Cauchy–Schwarz, the uniform lower limit of \(t\sum w_i^2\) is at least \(C^{-1}\sum_I R(I)^2/\Delta\). These sums diverge on refining the partitions because their piecewise-constant densities converge to \(g\) almost everywhere and \(g^2\) has a logarithmically divergent integral at \(s\). On the complement of a fixed neighborhood of \(s\), \(w_i\le M/t\). On the entire table, cells of weight at most \(M/t\) account for at most \(M/t\) of the sum of squares. Hence the squared weight of the heavier cells multiplied by \(t\) diverges uniformly; all such cells are inside the neighborhood. For \(q\ge2\) the outside \(q\)-sum is at most \((M/t)^{q-2}\) times the light squared weight and the heavy inside \(q\)-sum is at least this factor times its squared weight. This proves uniform concentration inside the neighborhood, including any maximum choice at infinity. If \(D_t\Rightarrow R\), a positive subsequential fraction of these types would give an atom at \(s\) by shrinking closed neighborhoods. Thus \(\Pr(Q_t\ge2)\to0\).

**Powers bounded above one.** If \(K=[1+a,2)\), \(0<a<1\), has mass at least \(m>0\) on an infinite subsequence, fix a small neighborhood \(U\) of \(s\) with boundary of zero \(R\)-mass and \(R(U)<m/8\). At late clocks \(D_t(U)<m/4\), so the members of \(K\) contribute at least \(3m/4\) to the total displayed probability of \(U^c\). Write \(H(B)=t^{q-1}\sum_{i\in B}w_i^q\) and \(Z=H([0,1])\) for a given type. On \(U^c\), \(H(U^c)=\sum_{i\in U^c}w_i(tw_i)^{q-1}\le M\) uniformly, enlarging \(M\ge1\). Those types with \(Z>4M/m\) contribute at most \(m/4\) in the population to \(U^c\). At least \(m/2\) of all launches therefore belong to \(K\) with \(Z\le4M/m\). For each fixed small shell, convexity gives
\[
 H(S_\epsilon)\ge (C\epsilon)^{1-q}R_t(S_\epsilon)^q
                   \ge c_a\epsilon^{(1-a)/2}
\]
at late clocks, with \(c_a>0\) uniform for \(q\in K\). These launches alone give \(D_t(S_\epsilon)\ge m^2 c_a\epsilon^{(1-a)/2}/(8M)\), inconsistent with its ordinary \(O(\sqrt\epsilon)\) limit for a sufficiently small fixed \(\epsilon\). This excludes \(\Pr(Q_t\ge1+a)\) for each fixed \(a>0\) in the limit.

**Powers below one and types approaching one.** Choose a fixed interior speed interval of ordinary mass at least \(b>0\) eventually with \(tw_i\le M_0\), \(M_0\ge1\). For \(0\le q\le1\) every positive cell there contributes at least \(w_i/M_0\) to \(Z\), including the convention at zero. Thus \(Z\ge b/M_0\). Concavity, and direct counting at \(q=0\), give the uniform bound
\[
 \frac{H(S_\epsilon)}{Z R(S_\epsilon)}
 \le C_0\,\epsilon^{(1-q)/2},\qquad 0\le q<1,               \tag{1}
\]
at all sufficiently late clocks for the fixed \(\epsilon\). The constant is independent of \(q,\epsilon\): the numerator is at most \((C\epsilon)^{1-q}R_t(S_\epsilon)^q\) before division by \(Z\); use the two square-root shell bounds.

Take any weak subsequential limit \(\nu\) of the exponent laws on the compactified interval \([0,\infty]\). The preceding steps imply its support is in \([0,1]\). At fixed \(\epsilon\), split at \(1-\eta,1+\eta\), choosing \(0<\eta\le1/4\) with \(\nu(\{1-\eta\})=0\). The upper tail vanishes. The central types give shell probability at most \(R_t(S_\epsilon)+A\eta\) each. Apply (1) to the remaining lower types. Integration against the subsequential limit is valid there because \(\epsilon^{(1-q)/2}\) is bounded and continuous and the chosen cutoff has zero limiting mass. Taking \(t\to\infty\) first and then \(\eta\downarrow0\) *at fixed \(\epsilon\)* yields
\[
 1\le\nu(\{1\})+C_0\int_{[0,1)}\epsilon^{(1-q)/2}\,d\nu(q).
\]
The \(A\eta/R(S_\epsilon)\) term vanishes in this order. The integral then vanishes by bounded convergence as \(\epsilon\downarrow0\). Hence \(\nu=\delta_1\). Every subsequential limit is the same, which proves convergence in probability to the constant one. This handles lower powers drifting towards one as well as a component fixed below one. Conversely if \(Q_t\to1\) in probability, convexity of total variation gives \(d_{\rm TV}(D_t,R_t)\le A\eta+\Pr(|Q_t-1|>\eta)\), and \(R_t\Rightarrow R\). This establishes the equivalence for this actual microscopic walk record. An arbitrary detector table carrying abstract speed labels need not obey either the kernel estimate or the radial identity.

## A finite test if radii are pooled before the power

Eight unobserved ticks from a sharp well give the following shell weights for every input coin. The origin is counted once. An unsigned independent fair direction word gives the second row.

| Radius | 0 | 2 | 4 | 6 | 8 |
|---|---:|---:|---:|---:|---:|
| Signed ordinary weight, in units of \(1/256\) | 18 | 44 | 116 | 76 | 2 |
| Fair direction count, in units of \(1/256\) | 70 | 112 | 56 | 16 | 2 |

Let \(a=44\), \(b=76\), \(c=116\) and \(\theta=\log(c/b)/\log(c/a)\), so \(b=a^\theta c^{1-\theta}\). For any displayed radius distribution \(p\), define
\[
 T(p)=\theta\,p(2)/a+(1-\theta)p(4)/c-p(6)/b .
\]
If the apparatus **first pools both positions and both rails at each radius**, then on a given launch \(p(r)=n_r^q/\sum_j n_j^q\) for the five integers in the first row. After multiplying by the normalizer, the score is the weighted arithmetic mean of \(a^{q-1},c^{q-1}\) minus their weighted geometric mean. It is strictly positive for every finite \(q\ne1\), zero at \(q=1\), and positive for \(q=\infty\), whose unique maximizing radius is four. The fair row also has \(T>0\) since both \(112/44\) and \(56/116\) exceed \(16/76\). Thus an exactly zero population score in this finite protocol forces ordinary exponent one and zero fair fraction within the stated family, even if its parameters or coin depend on the chosen launch. A growing line or interval with eight unreflected ticks near the launch realizes this read. This provides a finite test for a different order of operations.

A site-powered detector can give the opposite sign. Squaring each site weight before pooling radii gives unnormalized radius numerators \((324,1000,11336,3176,2)\) for a right input and \((1296,5024,31520,21920,16)\) for the real balanced input \((R+L)/\sqrt2\). The first score is positive and the second negative. One can verify the signs using just \(2/5<\theta<1/2\), which follows from \(a^2 c^3>b^5\) and \(ac<b^2\). The scores are affine in \(\theta\). A mixture with about 49.358% right inputs therefore has zero score with every launch using exponent two. Its five-bin distribution differs from the ordinary table by 0.16719 in total variation. In fact both components individually give the origin less than its ordinary probability \(18/256\), so every mixture of these two fails that component of the full table. The replay gives all five frequencies and independent comparisons of the exact Gram matrices. [Replay](check_speed_coin.py) · [Finite tables](results/speed_coin.json) · [Lean 4.19.0 calculation](lean/SpeedCoin.lean)

The speed experiment is a single terminal read on the line, or on a carrier allowing unreflected displacement. After a wall reflection, distance from the launch well can cease to equal the line speed. The two-launch-rail symmetry alone supplies no general inverse estimate for a folded physical-position record. Deriving the coin and stream, the admission and composition of records, and whether a physical detector implements any member of this family remains open.
