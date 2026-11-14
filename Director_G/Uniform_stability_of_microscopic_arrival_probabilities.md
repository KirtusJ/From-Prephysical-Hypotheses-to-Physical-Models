# How a small error in the probability exponent changes a walk's arrival record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

In the one-dimensional Hadamard walk a detector can assign a terminal cell of ordinary weight \(w\) a probability proportional to \(w^q\). **Changing \(q\) by a small amount changes the full arrival distribution by at most a constant times \(|q-1|\), uniformly in flight length.** This applies even to individual sites and rails, where interference leaves dark cells and produces sharp peaks. It allows arbitrary localized initial coin states. The statement is a sufficiency result about this detector family. It leaves the physical origin of the probability law open.

## Preparation and recorded cells

Start at a single lattice site with any two-dimensional coin density matrix \(\rho\), including a coherent superposition. Apply the Hadamard coin \(H=2^{-1/2}\bigl(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\bigr)\), then shift the right and left rails one site in their respective directions. After \(t\ge1\) ticks let \(K_t(x)\) be the two-by-two amplitude matrix at displacement \(x\). The site weight is \(p_t(x)=\operatorname{tr}(K_t(x)\rho K_t(x)^*)\). At each site the detector either pools its two rails into one cell or keeps them as two cells, independently of how it treats other sites. Its resulting weights \(w_i\) sum to one and each is at most the weight of its site. The proof also permits a local orthonormal basis for the two terminal coin outputs. The detector divides each \(w_i^q\) by their sum; zero cells remain dark. For a population of launches, the coin, partition and exponent may be sampled jointly and vary with \(t\). The ordinary comparison keeps the same distribution of preparations and partitions and uses exponent one on each.

The one-site preparation is substantive. Coherent superpositions of spatially separated sources, conditioning on detection in a small window, and weighting many sites as one cell before the power need their own bounds. A common reporting operation **after** the power, including forgetting the rail, binning positions or adding the same readout noise, contracts total variation.

## Velocity-dependent amplitude estimate

Write \(v=x/t\), \(s=1/\sqrt2\), \(d=\big||v|-s\big|\) and \(a=t^{-2/3}\). Uniformly on the reachable cone \(|x|\le t\),
\[
 \|K_t(x)\|_{\rm op}\le C\,t^{-1/2}(d+a)^{-1/4},
 \qquad t\,p_t(x)\le C^2(d+a)^{-1/2}.                         \tag{1}
\]
Outside the cone and on the wrong parity the kernel vanishes. The \(t^{-2/3}\) velocity scale cuts off the apparent singularity at either front. Sunada and Tate give interior stationary-phase and fixed-width Airy-transition asymptotics. Maeda, Sasaki, Segawa, Suzuki and Suzuki prove the global free-walk \(t^{-1/3}\) amplitude estimate for a spectral band. Here a split depending on \(d\) connects these regimes with a uniform bound suitable for summing over the lattice. [Sunada and Tate, Theorems 1.1 and 1.3](https://arxiv.org/pdf/1108.1878) · [Maeda et al., Proposition 4.12 and Lemma 7.1](https://arxiv.org/pdf/1808.05714)

**Proof.** In Fourier coordinates the one-step matrix is \(\mathrm{diag}(e^{-ik},e^{ik})H\), with inverse transform \(e^{ikx}\). Its eigenvalues are \(e^{-i\omega(k)}\) and \(-e^{i\omega(k)}\), where \(\omega(k)=\arcsin(\sin(k)/\sqrt2)\). Their separation is \(2\cos\omega\ge\sqrt2\), so the spectral projectors are smooth periodic matrices with bounded entries and derivatives. Discarding only the constant phase \((-1)^t\) on the second band, the two integrals have phases \(t\phi(k)=t(kv\pm\omega(k))\). The group velocity and its derivative are
\[
 \omega'(k)=\frac{\cos k}{\sqrt{1+\cos^2 k}},\qquad
 \omega''(k)=-\frac{\sin k}{(1+\cos^2 k)^{3/2}}.
\]
The two degeneracies on the circle are \(k_0=0,\pi\); there \(\omega'(k_0)=\pm s\) and \(|\omega'''(k_0)|=2^{-3/2}\). In fixed small disjoint neighborhoods of them, using local coordinate \(u=k-k_0\), we have \(|\omega'''|\ge c\), \(|\omega''|\ge c|u|\), and \(|\omega'(k)-\omega'(k_0)|\le B u^2\). Off these neighborhoods \(|\omega''|\ge c'>0\). Applying van der Corput of order three in the neighborhoods and order two on their complement gives \(C t^{-1/3}\) uniformly. For an amplitude entry this follows by integration by parts against a primitive of the unweighted oscillatory integral. The multiplier is bounded by the supremum plus the integrated absolute derivative of that entry, uniform on every subinterval.

For \(d\ge a\) choose a fixed small \(\alpha>0\) with \(B\alpha^2\le1/2\) and with \(\alpha\sqrt d\) inside each chosen neighborhood for all \(|v|\le1\). On \(|u|\le\alpha\sqrt d\), each band has \(|\phi'|\ge d-B\alpha^2d\ge d/2\). On the two half-caps \(\phi'\) is monotone, since \(\omega''\) has constant sign there. Integration by parts gives \(C/(td)\), including variable endpoints, because \(1/\phi'\) has total variation at most \(4/d\) on each half. In the remainder of each neighborhood \(|\phi''|\ge c\alpha\sqrt d\); the second-derivative bound gives \(C t^{-1/2}d^{-1/4}\). The unchanged complement contributes \(C t^{-1/2}\). As \(t d^{3/2}\ge1\), the half-cap bound is also at most \(C t^{-1/2}d^{-1/4}\). Combining with the global estimate for \(d<a\) proves (1), up to a fixed factor from replacing \(\max(d,a)\) by \(d+a\). Taking the matrix operator norm after bounding four entries changes only the constant. The density-matrix inequality \(p_t(x)\le\|K_t(x)\|_{\rm op}^2\) proves the second assertion, for every \(\rho\). This proof uses the same two estimates on the interior and exterior sides of both fronts.

## Summing over actual lattice sites

Put \(u_i=t w_i\). For every fixed \(1<r<2\) there is \(M_r<\infty\), independent of clock, coin and partition, such that
\[
 \frac1t\sum_i u_i^r=t^{r-1}\sum_i w_i^r\ \le\ M_r .          \tag{2}
\]
Indeed the core \(d<a\) contains at most \(C(ta+1)\) integer sites, counting both fronts and even allowing the unused parity. For \(h=2^j a\le1\) the shell \(h\le d<2h\) is covered by four velocity intervals of length at most \(h\), hence has at most \(4(th+1)\) sites. Multiplying these counts by two allows either number of cells. Since \(ta=t^{1/3}\ge1\), the core contributes at most \(C_r a^{1-r/2}\) to the left side of (2), and a shell at most \(C_r h^{1-r/2}\). Their geometric sum from the largest scale down is bounded by \(C_r/(1-2^{-(1-r/2)})\). This counting argument includes the nearest lattice point on each side of the front, even when the distance is smaller than one grid spacing. At \(r=2\) it gives an \(O(1+\log t)\) upper bound. It makes no uniform second moment assertion. At \(t=1\) the core and endpoint bounds still hold.

## Total variation at one clock and over a population

There is an absolute finite \(A\), depending only on the specified walk, for which
\[
 d_{\rm TV}\left(\frac{w_i^q}{\sum_jw_j^q},w_i\right)
 \le \min\{1,A|q-1|\},\qquad 3/4\le q\le5/4.                 \tag{3}
\]
For \(u>0\), differentiation in the exponent and the mean-value theorem yield
\[
 |u^q-u|\le (4/e)|q-1|\,(1+u^{3/2}).
\]
For \(u\le1\) use \(u^{3/4}|\log u|\le4/(3e)\); for \(u\ge1\) use \(u^{-1/4}\log u\le4/e\). At \(u=0\) the difference vanishes. Count only the at most \(2(t+1)\) cells on reachable sites, retaining dark rails within them. Equation (2) at \(r=3/2\) gives
\[
 D=\frac1t\sum_i |u_i^q-u_i|\le (4/e)(4+M_{3/2})|q-1|.
\]
Write \(b_i=u_i^q/t\) and \(Z=\sum_i b_i>0\). The normalized distribution is \(b_i/Z\), with \(\sum_i|b_i/Z-b_i|=|1-Z|\le D\). The triangle inequality and the factor \(1/2\) in total variation give (3) with \(A=(4/e)(4+M_{3/2})\). At \(q=1\) the two laws coincide. At \(t=0\) the same scalar bound applies directly to the at most two initial rail weights with scale one. A Lean 4.19.0 certificate checks the normalization inequality for arbitrary finite lists of nonnegative integer numerator pairs, which includes every rational table after a common rescaling. The proof above also covers real powers. [Lean normalization certificate](lean/ArrivalNormalization.lean)

Let \(Q_t\) now denote the random exponent, and let \(\bar P_t,\bar P_t^{\,1}\) denote the reported and ordinary population distributions on a common output space. Encode a pooled or split rail by its own label, or map both to a shared position read. For every \(0<\eta\le1/4\), convexity of total variation under mixing yields
\[
 d_{\rm TV}(\bar P_t,\bar P_t^{\,1})\le A\eta+
                  \Pr(|Q_t-1|>\eta).                         \tag{4}
\]
Outside the central range only normalization and the trivial bound one are used. A normalized tie rule on maximum cells, or the zero power uniform on nonempty cells, is allowed there. Thus \(Q_t\to1\) in probability implies microscopic total variation tends to zero without any prescribed rate involving \(t\). Every coarsening has the same guarantee, and every event probability differs by at most (4). This includes triangular populations with arbitrary changes in their localized coin mixture. A reduced coin obtained by tracing out an untouched spectator is such a mixture if only the stated terminal outputs are read. The proof does not infer the distribution of \(Q_t\) from an already coarsened record.

The walk's structure matters. On an unrestricted panel take one cell of weight \(1/2\) and \(2^n\) cells each of weight \(2^{-n-1}\). At \(q=1+1/n\) the total small-cell weight after powering is exactly half the large-cell weight. The normalized large-cell probability is \(2/3\) and the total variation distance is \(1/6\) for every \(n\), even though \(q\to1\).

## Reflections and checks

The same microscopic total variation bound applies to the signed reflecting interval with \(L\) wells and \(t<L\), even when the flight reaches a wall. Unfold onto the \(2L\)-cycle with the signed wrap for odd \(L\). The line positions at clock \(t\) have one parity and span \(2t<2L\), so their residues are distinct. The two lifts of a physical site have opposite parity, hence at most one is occupied. Decoding permutes the rails and changes their signs by a matrix independent of the initial coin. Therefore at each occupied site its position weight is the weight on a unique line site; a physical split is a two-cell partition there. For another local measurement basis the permutation and signs merely transform that basis. This transports (2)–(4), even if the physical position alone cannot distinguish the front velocities in a macroscopic limit. After distinct line amplitudes can meet in one lift the proof no longer applies. [Signed interval unfolding, including its boundary convention](Reflecting_wells_and_the_classical_limits_of_a_walk.md)

The [executable check](check_spatial_weight_envelope.py) reproduces the [finite tables](results/spatial_weight_envelope.json). It checks both initial basis columns by independent short path enumeration, including dark rails. It also compares exact local two-by-two effects after physical reflection and after unfolding. The clock table retains the maximizing displacements for the velocity envelope, including ties, and gives finite moment and total variation examples. These numerical examples measure the size of the effect at the recorded clocks. The bounds for arbitrary clocks and input density matrices are the analytic statements above.
