# What a classical arrival front tells us about microscopic position weights

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The ordinary position distribution of the sharp rightward Hadamard walk has an integrable peak at its maximum ballistic velocity. The probability in a window of width \(\epsilon\) just inside that front is of order \(\sqrt\epsilon\). This feature tests whether the detector samples **microscopic sites or rails** with their ordinary weights. Even if the exponent varies between launches and the detector decides separately at each site whether to resolve the rails, convergence to the ordinary macroscopic arrival distribution forces exponent one on almost every launch. The result holds on the line and on the specified reflecting interval where one front has already hit the wall. The number of settings and flight lengths required for exact limiting identification is unbounded. [Earlier test with velocity bins pooled before weighting](Which_probability_powers_preserve_the_classical_velocity_law.md)

## The detector and the accessible record

Launch the sharp right rail at site zero, apply the usual real Hadamard and stream right and left each tick. Let \(p_t(x)\) be the calculated sum of squared rail amplitudes at site \(x\). For a single launch either retain both squared rail masses there as separate cells or pool them into one cell. Denote the resulting normalized kinematic masses by \(w_i\). Their sum over any set of sites is the ordinary kinematic mass of that set. Draw a finite \(q\ge0\), weight each occupied cell by \(w_i^q\), normalize over all cells, and report the site. At zero power each occupied cell contributes one and all empty cells stay dark. The population law of \(q\) is fixed across the flight family. The conditional choice of which sites split may vary with \(q\), clock and the preparation. It cannot hide a site, merge different sites, add false counts or produce arbitrarily many hidden cells per site. We use at most two elementary cells per site. Collect the complete terminal site record on original exposure under this model. Velocity intervals below are selections made *after* that read.

For a Borel velocity interval \(A\), write \(P_t(A)=\sum_{x/t\in A}p_t(x)\). Its ordinary weak limit \(P\) has density \(f(v)=(1+v)/[\pi(1-v^2)\sqrt{1-2v^2}]\) on \((-v_*,v_*)\), \(v_*=1/\sqrt2\). Two consequences suffice.

* For \(I_\epsilon=[v_*-2\epsilon,v_*-\epsilon)\), there are constants \(c,C>0\) such that \(c\sqrt\epsilon\le P(I_\epsilon)\le C\sqrt\epsilon\) for all small \(\epsilon>0\). For each fixed \(\epsilon\) these bounds also hold for sufficiently late \(P_t(I_\epsilon)\) with modified constants.
* Outside any fixed open neighborhoods of both fronts, \(t\,p_t(x)\) is uniformly bounded for sufficiently late \(t\). On compact subsets of the allowed region this is the uniform bulk estimate including its oscillatory term. In the separated exterior there are no stationary points of the Fourier phases; one integration by parts bounds the amplitudes there by \(O(t^{-1})\) uniformly. The phase derivative stays bounded away from zero and the band amplitudes are smooth.

These statements permit microscopic interference fringes and actual zeros. We do not replace \(p_t(x)^q\) by a power of a smooth density. [Konno on the limiting walk](https://arxiv.org/abs/quant-ph/0206103) · [Sunada and Tate, Theorem 1.1 and Fourier representation](https://arxiv.org/pdf/1108.1878) · [Walk conventions and exterior bound](Which_probability_powers_preserve_the_classical_velocity_law.md)

## A square-root window on one reflected interval

Alternatively let \(L=\lceil4t/3\rceil\), \(x_0=\lfloor L/8\rfloor\), launch there on \(R\), and read \(z=(x+1/2)/L\) after \(t\) ticks. An outward step at either wall holds for one tick, reverses its rail and has positive amplitude. The signed unfolding gives one reachable parity lift per occupied physical well for \(t<L\). Each lifted site's weight and its two rail weights are transported to this well, up to an exchange of the rails. The ordinary limit is the pushforward by \(z=F(y+\tau v)\) with \(F(s)=\mathrm{dist}(s,2\mathbb Z)\), \(y=1/8\), \(\tau=3/4\). The two macroscopic fronts are \(z_-=F(y-\tau v_*)\approx0.4053\) and \(z_+=F(y+\tau v_*)\approx0.6553\). The incoming negative front has already reflected. [Physical unfolding and front positions](Which_probability_powers_preserve_the_classical_velocity_law.md)

Take the fixed physical window \(I_\epsilon=[z_+-2\tau\epsilon,z_+-\tau\epsilon)\). For sufficiently small \(\epsilon\) its lower end exceeds \(5/8\), the farthest coordinate reached by the reflected *negative* route even at microscopic velocity \(-1\). The upper end stays below \(7/8\), the farthest positive light-cone coordinate. Its only limiting preimage is the positive-velocity shell above. Weak convergence at these fixed window boundaries gives the same square-root mass estimates. The rounding of \(L,x_0\) changes the mapping by \(O(t^{-1})\). Away from neighborhoods of \(z_\pm\), the corresponding line velocities stay separated from both fronts uniformly for large \(t\), so the second bound also transfers. Each shell contains at most \(C_0t\epsilon+O(1)\) microscopic cells in either experiment, including when all rails are split. For a fixed small \(\epsilon\), take \(t\) large before shrinking the shell. The test requires matched spacetime scaling and recording the actual well even as the number of wells grows.

## Powers above one

Let \(D_t=t^{q-1}\sum_i w_i^q\) and \(H_t(A)=t^{q-1}\sum_{i\in A} w_i^q\) for this launch type, including its choice of partitions. Its conditional displayed probability of \(A\) is \(H_t(A)/D_t\). Use the appropriate spatial variable for the line or interval. Suppose the population display law converges weakly to the ordinary law \(P\).

If a positive fraction has \(q>1\), some compact \(K=[1+a,B]\), \(a>0\), has population mass \(m>0\). Choose a fixed open union \(U\) around the two fronts with \(P(U)<m/8\) and endpoints of zero \(P\)-mass. At large \(t\) the observed population puts at most \(m/4\) in \(U\). Writing \(J=U^c\), the types in \(K\) must therefore contribute at least \(3m/4\) to the observed probability of \(J\). But \(tw_i\le M\) on \(J\), where we may take \(M\ge1\). Hence for these types
\[
 H_t(J)=\sum_{i\in J} w_i(tw_i)^{q-1}\le M^{B-1}=C_J.
\]
Those with \(D_t>4C_J\) contribute at most \(m/4\) to \(J\). Consequently at least \(m/2\) of the entire population is in \(K\) with \(D_t\le4C_J\), at each sufficiently large \(t\). This conclusion does not assume that the same particular individuals are selected at every clock.

For a fixed small \(\epsilon\), there are at most \(C_1t\epsilon\) cells in \(I_\epsilon\) at sufficiently late times. Jensen's inequality, padding with zero cells if needed, gives
\[
 H_t(I_\epsilon)\ \ge\ (C_1\epsilon)^{1-q}P_t(I_\epsilon)^q
 \ \ge\ c_K\,\epsilon^{\,1-q/2}
 \ \ge\ c_K\,\epsilon^{(1-a)/2}
 \qquad(q\in K).
\]
The positive constant \(c_K\) is uniform on the compact \(K\). At least \(m/2\) of the launches therefore contribute a shell probability at least \(c_K\epsilon^{(1-a)/2}/(4C_J)\) each. For a small enough *fixed* \(\epsilon\) this lower bound on the population exceeds the ordinary \(O(\sqrt\epsilon)\) probability, because \(\epsilon^{-a/2}\) can grow arbitrarily large. All other contributions are nonnegative. This contradicts convergence and excludes every \(q>1\). It includes the subcritical range \(1<q<2\) without finding the limiting shape of its microscopic interference fringes.

## Powers below one

Fix a positive-mass interior interval \(J_0\) separated from both fronts. For all large \(t\), \(P_t(J_0)\ge b>0\) and \(tw_i\le M_0\) there, with \(M_0\ge1\). For \(0\le q\le1\), sum only over positive \(w_i\); each term in \(H_t(J_0)\) is \(w_i(tw_i)^{q-1}\ge w_i/M_0\). Thus \(D_t\ge b/M_0\) uniformly, even for a detector counting occupied cells at \(q=0\).

Concavity gives the reverse Jensen bound \(H_t(I_\epsilon)\le (C_1\epsilon)^{1-q}P_t(I_\epsilon)^q\) for \(0<q\le1\). For \(q=0\) this follows directly from the upper bound on the number of cells divided by \(t\). Thus, after division by \(D_t P(I_\epsilon)\), each \(q<1\) contributes at most \(C_2\epsilon^{(1-q)/2}\) to the ratio of displayed and ordinary shell probabilities for all sufficiently large \(t\). Here \(C_2\) works for all \(0\le q<1\). The \(q=1\) component gives exactly \(P_t(I_\epsilon)\) in each trial law. Taking the long-flight limit first at fixed \(\epsilon\) now gives
\[
 1\le \Pr(q=1)+C_2\int_{[0,1)}\epsilon^{(1-q)/2}\,d\mu(q).
\]
The integral tends to zero by bounded convergence, even if the subunit exponents accumulate at one. Therefore \(\mu(\{1\})=1\). Conversely every such population gives the ordinary law independently of the rail partition. This reasoning does not require a particular clock subsequence or a full-support assumption about every microscopic site.

## Finite checks and scope

For a finite comparison, read the velocity sites in the same shell and in \(0\le x/t<1/4\), and take the ratio of their probabilities from the same flight ensemble. The following entries are per-type ratios with both rails pooled at each site. They come from integer signed counts. At 1,536 ticks:

| \(\epsilon\) | Reachable shell sites | \(q=1/2\) | \(q=1\) | \(q=3/2\) |
|---:|---:|---:|---:|---:|
| \(1/24\) | 32 | 0.3747 | 0.9829 | 2.7701 |
| \(1/48\) | 16 | 0.2344 | 0.7885 | 2.8467 |
| \(1/96\) | 8 | 0.1352 | 0.5287 | 2.2513 |
| \(1/192\) | 4 | 0.0952 | 0.5065 | 2.8863 |

At 12 ticks three of these windows are empty. At 24 ticks the \(1/48\) shell contains one site, and its ordinary odds exceed three. The [full record](results/microscopic_velocity_shells.json) retains the empty windows, nonmonotone finite values, zero-power occupied-cell convention, all-split and alternating split controls. The [checker](check_microscopic_velocity_shells.py) uses integer bounds for square roots in half-integer powers, exact integer shell-membership tests and direct signed paths through ten ticks. It separately verifies the physical fold for nineteen choices of the reflecting carrier and source. No fit to measured observations is involved.

These tests select the ordinary power among launches sharing one exponent throughout their terminal table and a common population across the indefinitely growing family. A detector using \(q_t=1+1/t\) on all launches can still have ordinary limiting records. With at most \(2(t+1)\) occupied cells, the entropy bound gives total variation at most \(\log(2(t+1))\log(1+1/t)\to0\). Allowing arbitrary local score functions, hidden losses or pooling between different sites changes the question. The stipulated linear kinematics and measurement access, the physical status of the square rule, and the origins of the carrier and clock remain open. [Quantitative finite-power comparison](From_five_forward_ticks_to_a_coherent_position_read.md)
