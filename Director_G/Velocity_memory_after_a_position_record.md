# How a position record sets the classical scattering law of a signed walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and computational checks by OpenAI Codex.

A particle starts at one lattice site and makes a long free Hadamard walk. Record its exact site, let it walk again, and compare the directions of the two displacements. The limiting chance of continuing in the same direction is **3/4** if the position read preserves the two local rails, **5/8** if it also measures the rail, and **1/2** if it prepares a fair fresh rail. All three devices give the same first position distribution. The difference survives at macroscopic distances and can be read from two successive displacements without reconstructing the microscopic coin.

When these writes are rare, their recorded positions admit a classical description as flights with a continuum of velocities. The velocity after a write retains a computable fraction of the previous velocity. The derivation uses the signed walk's unitary kinematics, ordinary probabilities for records, and an explicit instrument. The [native probability tests](../candidates/composition_record/return_memory/three_grains.md) constrain a family of terminal detector responses. They leave the update after a write as a separate physical question.

## The law of two successive flights

Take the infinite line, or a ring large enough to avoid wrapping through the final tick. At each tick apply the real Hadamard coin on the R,L rails, then move R right and L left. Prepare at site zero with coin density matrix \(\rho=(I+r_xX+r_yY+r_zZ)/2\), with \(Z=+1\) on R. Record the position at the end of each flight. A flight velocity in these statements is the signed difference of two recorded positions divided by the ticks between them.

Use \(\nu\) for the symmetric velocity law, with density

$$
\frac{1}{\pi(1-v^2)\sqrt{1-2v^2}},\qquad -1/\sqrt2<v<1/\sqrt2 .
$$

Equivalently draw a uniform momentum \(k\) and a fair band, then take the group's velocity \(v=\pm\cos k/\sqrt{1+\cos^2 k}\). The actual first-flight law is \([1+(r_x+r_z)v]\nu(dv)\). In particular it is tilted for a sharp R source. The moments used below are \(c=\int v^2d\nu=1-1/\sqrt2\) and \(\int|v|d\nu=1/2\). The latter follows by substituting \(u=\sin k\) in the integral on a quadrant. [Grimmett, Janson and Scudo, weak limit](https://arxiv.org/abs/quant-ph/0309135) · [Program's finite radius symmetry](One_exact_site_record_changes_a_ballistic_history.md)

For the three boundary operations in the table, successive macroscopic velocities follow the transition law

$$
 K_\kappa(v,dw)=(1+\kappa vw)\,\nu(dw).
$$

| Operation on the coin at the recorded site | \(\kappa\) | Chance the next displacement has the same sign |
| --- | ---: | ---: |
| Keep both rails coherent | 2 | \(3/4\) |
| Measure R versus L, discard the rail label | 1 | \(5/8\) |
| Replace the coin by \(I/2\) | 0 | \(1/2\) |

A partial R/L record with a fixed real environmental overlap \(\eta\) multiplies the off-diagonals by \(\eta\) and leaves the populations unchanged. It has \(\kappa=1+\eta\), including \(\eta<0\) if a relative sign is applied. This permits a continuous family of record disturbances. Since \(|v|,|w|\le1/\sqrt2\), all displayed kernels are nonnegative. Their integrals are one by symmetry. Integrating the two signs gives \(E[\operatorname{sgn}V_1\operatorname{sgn}V_2]=\kappa/4\), independently of the initial tilt. The sign-agreement rate is \(1/2+\kappa/8\); zero displacements have zero limiting mass. Later absolute speeds have law \(|\nu|\) (the pushforward by absolute value) even conditional on the previous velocity. A speed histogram alone cannot distinguish these instruments.

## Why the retained coin matters

Let \(T_d^{(m)}\) be the two-by-two amplitude matrix for displacement \(d\) in \(m\) free ticks. For a continuous test \(f\) of the recorded velocity the site-write instrument is the linear map

$$
 \mathcal I_m(f)[\rho]=\sum_d f(d/m)T_d^{(m)}\rho\,T_d^{(m)\dagger}.
$$

It retains the coin dependence needed for subsequent measurements. For \(f(v)=e^{i\xi v}\) its Fourier integral has factors \(U(k+\xi/m)^m\) to the left of \(\rho\) and \(U(k)^{-m}\) to the right, where \(U(k)=\operatorname{diag}(e^{ik},e^{-ik})H\). The band phases are \(\omega=\arcsin(\sin k/\sqrt2)\) and \(\pi-\omega\). Equal-band terms converge to \(e^{i\xi\omega'_b(k)}P_b(k)\rho P_b(k)\). Cross-band terms now have a coin matrix between projectors and generally **do not vanish pointwise**. Their integrated phases contain \(m(2\omega-\pi)\) or its negative. Remove arbitrarily short neighborhoods of the finitely many stationary points. On the remainder an integration by parts gives a vanishing oscillatory integral since the projectors are smooth, the phase derivative is bounded away from zero, and the bounded shift \(\xi/m\) contributes a smooth, uniformly bounded amplitude with bounded first derivative. The removed part is bounded by its length. Uniform approximation on the compact velocity interval \([-1,1]\) extends the limit to continuous \(f\).

Consequently the limiting instrument is the integral of \(f(v_b)P_b\rho P_b\) over both bands and uniform momentum. At fixed \(v\), the paired Bloch directions of those projectors are

$$
 n_\pm=(v,\ \pm\sqrt{1-2v^2},\ v)
$$

with equal weights. This follows from diagonalizing \(U(k)\) and pairing \(k,-k\); the sign reverses again on changing bands. A rank-one projector in direction \(n\) leaves \(P_n\rho P_n=\mathrm{tr}(P_n\rho)P_n\). Averaging these two expressions gives the trace density \(d=1+(r_x+r_z)v\) relative to \(\nu\). In the unnormalized output the \(X,Z\) Bloch components each equal \(vd\) and the \(Y\) component is \((1-2v^2)r_y\). On velocities of positive density the retained normalized coin therefore has \(x=z=v\). A real source gives \(y=0\). The imaginary component of a general preparation need not vanish, but neither a site-only write nor real rail dephasing converts it into the \(x+z\) that determines the next velocity. These identities give the kernels in the table. They describe averages on velocity events. At one exact lattice site the conditional coin can oscillate with flight length.

The same proof applies to any fixed number of long flights with different numbers of ticks, provided the shortest of them tends to infinity. Translation invariance makes each displacement instrument independent of the starting *location*. For continuous product tests, compose its finite-dimensional coin maps and insert the specified boundary operations. Convergence on a basis of coin matrices gives convergence of the product. The compact support and approximation by sums of products give convergence of the joint law. Signs can be taken afterward since the limiting marginals have no atom at zero. An exact position record followed by deletion of that record still has this back-action; a device that only couples to a coarse position bin is a different instrument. [Coherent-bin histories](Reflected_position_histories.md)

## A kinetic limit with an explicit source for the record times

Use \(n\) lattice ticks per unit physical time and scale displacements by \(1/n\). After each tick, an independently prepared control enables a write with probability \(p_n\), where \(np_n\to\lambda>0\). The effective rate follows from a finite reversible preparation if the ordinary record law is available. Prepare \(b_n\) blank binary controls with Hadamards, compute whether their integer value is below \(k_n\), and in the selected sector copy the current position into a fresh protected register and apply the chosen coin instrument. Mark whether a write occurred, so a write at coordinate zero differs from a blank. Retain the flag and earlier registers, or trace them out after their last use. Disjoint control sectors yield the no-write map \((1-p_n)\rho\) and the write maps \(p_n\mathcal I_x(\rho)\), with \(p_n=k_n/2^{b_n}\). For example \(b_n=\lceil2\log_2(n+1)\rceil\), \(k_n=\lfloor\lambda 2^{b_n}/n\rfloor\) for sufficiently large \(n\) implements the limit. Fresh blanks, controlled copies and a protected record are physical additions. The preparation gives a way to test their consequences without postulating a classical random clock independently of this model.

On each bounded macroscopic horizon the Bernoulli clock converges to a Poisson clock of rate \(\lambda\). Conditional on finitely many distinct limiting event times, every intervening positive duration contains divergingly many ticks. This can be seen by coupling geometric waiting times to exponential ones by inverse distribution functions. Apply the joint flight result conditionally and truncate the number of writes; the count tail is uniformly small on a bounded horizon. Add one position read at the final time. The polygon joining the recorded positions converges in law to the polygon of a continuous-velocity random flight, with velocities updated by \(K_\kappa\). Event counts, times, and the final partial segment are included. The polygon interpolates between actual records. It does not specify a measured microscopic path between them.

For a smooth test function of position and velocity the limiting generator is

$$
 \mathcal L f(x,v)=v\,\partial_x f(x,v)
 +\lambda\int [f(x,w)-f(x,v)](1+\kappa vw)\nu(dw).
$$

The uniform-momentum symmetric law \(\nu\) is invariant and \(K_\kappa v=\kappa c v\). Write \(\beta=\lambda(1-\kappa c)>0\). Starting in that symmetric law, \(E[V_sV_t]=c e^{-\beta|t-s|}\), and the displacement \(X_t-X_0=\int_0^t V_s\,ds\) has variance

$$
 2c\left[\frac{t}{\beta}-\frac{1-e^{-\beta t}}{\beta^2}\right].
$$

This starts as \(ct^2\) and later grows as \(2Dt+O(1)\), with \(D=c/\beta\). A sharp R launch instead gives \(E[V_t]=c e^{-\beta t}\). Its raw two-time product is unchanged because the first law's odd tilt leaves the second moment unchanged and all later laws retain this property. Its position variance therefore subtracts \([c(1-e^{-\beta t})/\beta]^2\) from the displayed expression. Misidentifying the raw product as the centered covariance would give the wrong finite-time result for this source.

At a second, longer time scale the kinetic process has a Brownian limit with variance rate \(2D\). In fact the velocity generator solves \(-\mathcal L_v(v/\beta)=v\). Subtracting its bounded endpoint correction makes the displacement a jump martingale. Its predictable squared variation has stationary mean rate \(2c/\beta\) by integrating \(\mathcal L_v[(v/\beta)^2]-2(v/\beta)\mathcal L_v(v/\beta)\). For ergodicity, the two-jump kernel has density \(1+\kappa^2c\,vw\ge1-\kappa^2c/2>0\) relative to \(\nu\) in all three cases. Time averages converge to equilibrium even from the tilted source. The jumps of the martingale are bounded, so the martingale functional central limit theorem applies after division by the square root of elapsed time. This is an **iterated** limit, first the rare-write scaling and then long time of the resulting classical flight. A single unrestricted simultaneous scaling requires additional uniform estimates. [Hillen and Othmer, diffusion limit for velocity-jump processes](https://doi.org/10.1137/S0036139999358167) · [Whitt, martingale functional central limit theorem](https://doi.org/10.1214/07-PS122)

## Comparing with data and earlier limits

Romanelli and colleagues use simultaneous position and chirality measurements in the \(Y\) basis. Both eigenstates in that basis have a symmetric subsequent position law on the real Hadamard walk, giving an independent-increment example. Chisaki and colleagues study position-measurement crossover limits for specified measurement schedules and preparations. The earlier program result uses three consecutive position writes to generate a renewal flight. Here preserving the coin at a *single* position write leaves a directly measurable adjacent-flight correlation. [Romanelli et al., §3](https://arxiv.org/html/quant-ph/0403192#S3) · [Chisaki et al.](https://arxiv.org/abs/1009.2131) · [Three consecutive position records](Diffusion_from_three_position_records.md)

For a sharp R source with two flights of 256 ticks each, exact finite walk propagation gives the following probabilities per launch. No spatial bins, coincident displacements or incomplete sign pairs have been dropped.

| Coin at the intermediate position read | Same nonzero sign | Opposite signs | At least one zero |
| --- | ---: | ---: | ---: |
| Preserved | 0.748765 | 0.246287 | 0.004948 |
| R/L measured and forgotten | 0.623145 | 0.371907 | 0.004948 |
| Replaced by \(I/2\) | 0.497526 | 0.497526 | 0.004948 |

The [exact checker](check_velocity_collisions.py) also accepts unequal segment lengths and distinguishes centered covariances from raw products. To test the prediction in hardware, record a source, intermediate site and final site on the same launch; interleave coin-preserving and rail-measuring boundary operations, retain both zero and missing reports, and calibrate misclassification of each displacement sign. The [available walk datasets](../candidates/composition_record/return_memory/experimental_coverage.md) do not establish these joint rates. The inferred classical motion is free transport with an instrument-dependent scattering law. Deriving the carrier, the response of real records and interacting classical dynamics from common prephysical primitives remains open.
