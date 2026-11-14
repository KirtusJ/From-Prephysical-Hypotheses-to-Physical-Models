# A field-on preparation and its release clock

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Keep the physical staircase gain and the ordinary signed Hadamard tick running through sheet selection, base preparation, retries and flight. On the same retained sheet one limit gives a spreading quantum position distribution and another gives two accelerating classical tracks. The field changes the finite-action packet *during preparation*. Ignoring that change predicts the wrong later centers and the wrong elapsed time.

## Preparing again at the site of a failure

The direction-only passing outcome is an operation on the enlarged walk with a carried bit. This section uses its coherent squared-coordinate realization, or an independently verified instrument with the same action on the contributing sectors. The position-product theorem on the original walk determines the sharp selector transcripts; it does not by itself determine how a new pointer updates an extended packet. [Position-product scope](Position_transcripts_and_selected_laws.md)

Begin at the known well and rail of a successful sheet-selection record. For each consecutive pair of ticks, ask whether the rail has switched from its last recorded value. The passing outcome preserves coherence over all its sites. On failure record the site and rail and start the next attempt right there. Release immediately after $m$ consecutive switches, with $m$ even. The reference position $Y_0$ is the start of the successful attempt. Elapsed flight time $T$ begins at release. The probability law does not assign a common $Y_0$ to all launches. The ring, an initially sharp base on the retained sheet, and a record that preserves site coherence only on the passing rail suffice for the calculation. A permanent which-site record on that rail changes it. [Field-on and field-off controls](Field_reversal_during_preparation.md) · [Constructing the direction read](Direction_from_position_toggles.md) · [Sheet selection from sharp reads](Native_multiscale_selector.md)

At character $s=\pm1$ the staircase is a linear phase gradient $h=s\pi/M$ on each occupied parity, up to a common phase. Write $q$ for outgoing lattice momentum. Let $P_j(h)$ be the probability that one attempt survives its first $j$ blocks, $P_0(h)=1$. For either launch rail and every sharp home it is the normalized momentum average of

$$
\left|\prod_{a=1}^{j}\sin(q+(2a-1)h)\right|^2 .
$$

The postselected amplitude for an even number of switches is this unsquared product up to a common phase and the translation of its home. For odd $j$ the additional one-site displacement phase has unit modulus. The finite momentum grid gives the same average as the integral when $2j<4M$, since nonconstant Fourier modes of the product have degree at most $2j$. In particular $P_j(0)=\binom{2j}{j}/4^j$. Hölder gives $P_j(h)\le P_j(0)$ at every signed sector in this regime. [Two-tick physical amplitude and exact phase](Field_reversal_during_preparation.md)

For a persistent character the success probability after any recorded failure is $P_m(h)$, independent of the specific failure history. The mean cost per attempt counts blocks reached, including the final failing block. Conditioning on the end of that attempt gives

$$
\mathbb E_s[\text{moving ticks until release}]
=\frac{2\sum_{j=0}^{m-1} P_j(h)}{P_m(h)} .
$$

This is conditional on the character. For example the survival function and the mean ratio cannot be averaged over a persistent mixture before division. A finite deadline includes TIMEOUT. Given a successful sheet herald with unwanted weight $\eta$, for a deadline $D$ in physical time the failure probability is at most $\eta+(1-\eta)\Pr_{\rm unit}(\text{timeout})$ even if one of the unwanted sectors never prepares. A finite deadline also avoids assigning a bounded unconditional mean to arbitrarily slow unwanted sectors. The sheet remains coherent between its characters along a sharp record; tracing a translation-invariant subsequent read gives the same probabilities as this conditional mixture.

## The finite-action limit

Take $F>0$, $\delta=(\pi/(MF))^{1/3}$, site pitch $\delta$, tick duration $\delta^2$ and $m\delta^2\to\lambda>0$. Fold the two parity replicas about $q_*=-\pi/2$ and set $p=(q-q_*)/\delta$. For a prefix $j$ with $j\delta^2\to u>0$, the centers of its factors span $O(\delta)$. In the central chart they are cosines. Their mean offset is $jh$, and the sum of squared deviations from that mean is $h^2 j(j^2-1)/3$. Consequently, on compact $p$ sets the log modulus of the unnormalized product tends to

$$
-\tfrac12 u(p+sFu)^2-s^2F^2u^3/6 .
$$

Indeed $\log\cos z=-z^2/2+O(z^4)$, and on such sets $j\,O(\delta^4)=o(1)$. For norm convergence, on the central half of the folded chart all factors are positive in the centered cosine convention for sufficiently large $M$ and $\log\cos z\le-z^2/2$ gives an integrable translated Gaussian bound in $p$. On the rest of the chart their moduli are bounded uniformly below one in the sense $|\cos z|\le\rho<1$, and the integrated tail divided by $\delta$ vanishes. The ring grid in $p$ has spacing $\pi/(2M\delta)\to0$; the same Gaussian bound controls its Riemann sums. Thus

$$
\frac{P_j(h)}{P_j(0)}\longrightarrow e^{-F^2u^3/3},\qquad
G_{\rm released}(p)=(\lambda/\pi)^{1/4}
                  e^{-\lambda(p+sF\lambda)^2/2}.
$$

The second expression gives the normalized scalar for the complete passing word, up to a common phase, with momentum measured relative to the release chart and position relative to its home. The normalization removes the survival factor, but the momentum drift remains.

Since $P_j(0)\sim(\pi j)^{-1/2}$, the exact renewal formula gives the limiting mean **moving time**

$$
2\sqrt{\lambda}\,e^{F^2\lambda^3/3}
\int_0^\lambda u^{-1/2}e^{-F^2u^3/3}\,du .
$$

The prefix convergence is uniform away from $u=0$ by the same compact bounds or sequential compactness. Near zero, $P_j(h)\le P_j(0)\le C/\sqrt{j+1}$ dominates the sum. The zero-field limit is $4\lambda$. Even the first uninterrupted success requires $2\lambda+o(1)$ units of time. Detector and logic latency are additional if they occupy clock slots. At fixed posterior error the preceding fixed-coin sharp sheet selector has worst time $O(M^{2/3}\delta^2)=O(1)$ on this clock. Its lower bound also precludes a vanishing uniform worst-case duration at fixed positive target completeness. At decreasing error the proven upper bound acquires $1+\log(1/\eta)$; the dependence on accuracy is not known to be sharp.

On bounded flight times the two smooth band envelopes evolve with Hamiltonians $b p^2/2+sFY$, $b=\pm1$. After an even number of switches the retained real rail has squared projection $1/2$ on each circular curvature eigenvector at the folded momentum edge. The initial mean momentum is $-sF\lambda$, position mean zero relative to $Y_0$, variances $1/(2\lambda)$ and $\lambda/2$, and symmetrized covariance zero. The shear $Y\mapsto Y+bTp-bsFT^2/2$ gives an equal mixture of two Gaussians centered at

$$
Y_0\pm F(\lambda T+T^2/2),\qquad
\sigma_T^2=(\lambda+T^2/\lambda)/2
$$

with the stated common within-component variance. Both sheet conjugates predict this same position distribution. The finite chart and tail proof uses the earlier forced-envelope estimate. Cross-band terms in a macroscopic position characteristic function vanish because eigenvectors in opposite bands at momenta a distance $O(\delta)$ apart have overlap $O(\delta)$ on compact scaled charts. A smooth cutoff followed by its removal handles the full Gaussian. A sharp rail read at the release edge has equal probabilities on the two circular polarizations; it cannot tell which curvature is present. The Gaussians overlap at each finite time. [Norm estimate on a bounded flight](Forced_envelope_and_classical_motion.md) · [Fixed-action field-off comparison and parity chart](From_a_local_sheet_to_a_flight.md)

A phase-sensitive comparison would distinguish these packets from position-diagonal mixtures with the same terminal histograms. Compare a packet to itself translated an even $k$ sites, with $k\delta\to\ell\ne0$, and remove the carrier sign $(-1)^{k/2}$. In a terminal momentum expectation, translation is multiplication by $e^{ikq}$. The exact force update shifts the initial momentum density by $-sFT$ in scaled units while the unitary rail action preserves its norm along each characteristic. The real corrected overlap therefore tends to $e^{-\ell^2/(4\lambda)}\cos[F(\lambda+T)\ell]$ in either conjugate. A position-diagonal state has zero overlap at nonzero separation before wrapping. This optional observable requires a coherent translation comparison; the position apparatus alone supplies only the density. [Translation read assumptions](From_a_local_sheet_to_a_flight.md)

## Classical records and preparation costs

At shrinking action use site pitch $\delta^2$, tick duration $\delta^3$, $\delta=(\pi/(MF))^{1/4}$ and even $m\sim\delta^{-5/2}$. Now $m^3 h^2=O(\delta^{1/2})$, $mh/\delta=O(\delta^{1/2})$, and $P_m(h)/P_m(0)\to1$ uniformly for the two targets. For all shorter prefixes the same weak-field comparison holds uniformly up to $m$: for bounded $j$ this follows from continuity at zero field, and for diverging $j\le m$ the quadratic-offset bound tends uniformly to zero. The renewal formula gives $(4+o(1))m$ moving ticks in the target pair, or $O(\delta^{1/2})$ physical time. A direction deadline $\delta^{1/4}$ loses $O(\delta^{1/4})$ of the target weight. The site of a failed restart may be retained as a classical record without transporting the walker back to any preferred well.

For a localized square-coordinate sheet, choose selector error $\eta=M^{-\gamma}$ with $\gamma>0$. Even a completed sharp selector then takes $O(M^{-1/12}\log M)=o(1)$ physical time on this clock. Its original-launch acceptance is asymptotic to $2/M$. Conditional on the unit pair, the successful packet has vanishing position width and scaled momentum bias about its last home. Keeping this same field on for $T>0$ puts its terminal displacement at $\pm FT^2/2$ with equal limiting weights. The probability of a sheet herald, a completed direction preparation by the deadline and arrival in the union of disjoint fixed tubes about both positions, divided by $2/M$, tends to one. Each individual tube gives limit $1/2$ for that ratio. A position read of the side at a separated positive time can select a track for later coarse readings if sites within each retained side remain coherent. It requires another specified instrument. When reading only one final position, the result concerns that single time. [Classical packet estimate](Base_preparation_and_two_rays.md) · [Joint coarse position records and disturbance bounds](Sequential_position_records.md)

All these limits are relative to the start of the successful attempt and the recorded release clock. The final sharp well after the sheet stage can be far from the original source. Each individual attempt and subsequent bounded-time flight fit on an unwrapped cone for sufficiently large $M$, even if the preselection record wraps the ring. The short early-rejection mean for fresh localized sheets counts rejected sources. The selected walker follows the whole successful schedule. Replacing failed sheets, resetting a common origin or waiting for simultaneous releases are distinct resources.

## Finite checks

At $M=8192$, with $F=1$ and the actual even length nearest $\lambda=1$, the computed field-on survival ratio is $0.71369$ against a prediction of $0.71445$. The mean moving time is $5.37489$ against $5.36795$. Including the preparation drift reduces the unit-wavenumber position characteristic-function error from $0.29712$ to $0.02529$. Across 24 finite flights the largest such error was $0.10597$. A separate small-order calculation follows failures at their actual wells and checks the scalar renewal deadline. It finds a positive probability that a successful packet starts away from the original home. Every sampled error, reflected launch, zero-field run and timeout remains available. [Checker](check_field_on_renewal.py) · [All finite comparisons](results/field_on_renewal.json)
