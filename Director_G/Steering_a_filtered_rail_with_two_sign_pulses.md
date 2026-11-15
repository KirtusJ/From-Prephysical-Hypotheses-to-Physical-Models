# Steering a filtered rail with two sign pulses

A localized right-rail launch, position-blind rail measurements and two uniform rail sign pulses can prepare either extremal velocity of the Hadamard walk. Its own measurement record selects the sign and sets the two flight durations. The preparation works on the line with the field off. It replaces the site-uniform four-route analyzer in the [tagged transport construction](Preparing_one_transport_band_with_rail_records.md) with a coherent rail read every two ticks and two timed applications of $Z=\mathrm{diag}(1,-1)$. The conditional position prediction extends through a finite field impulse. The preparation uses the stipulated squared-coordinate law and the physical coherence of each recorded operation.

## Count the changes of rail

Write $U(k)=\mathrm{diag}(e^{-ik},e^{ik})H$ with $H=(X+Z)/\sqrt2$, $k\in[-\pi,\pi)$ and measure $dk/(2\pi)$. At the origin start on $R$. For each of $D$ pairs of ordinary ticks, measure $R$ or $L$ coherently across the occupied sites. Record its sign $d_j=+1$ or $-1$, respectively. Let $A$ count changes, including the comparison with $d_0=+1$. Set $B=D-A$, $C=\sum_j d_j$, and $\tau=d_D=(-1)^A$. By direct multiplication of $U^2$, every stay contributes $e^{-id_j k}\cos k$ and every switch contributes $-i e^{-id_j k}\sin k$. The fine word ends on the sharp rail $\tau$ with scalar amplitude

$$(-i)^A e^{-iCk}\sin^A k\cos^B k.$$

Thus $C$ is the prepared position centre for that word. It is available from the record. Any pooling of final positions below uses this recorded origin. There are $\binom DA$ words of the same count. A beta integral gives the exact incident probability

$$q_D(A)=p_Ap_B,\qquad p_j=4^{-j}\binom{2j}{j}.$$

Each individual word has weight $q_D(A)/\binom DA$. Fix an integer $a\ge1$ with $2a<D$. Retain $a\le A\le2a$. The per-launch yield for label $\tau$ is the sum of $q_D(A)$ in this interval with $(-1)^A=\tau$. Its complement across both signs is the reject rate. If $a\to\infty$ and $a/D\to0$, Stirling's formula uniformly gives $q_D(A)\sim1/(\pi\sqrt{AD})$ on the interval. Summing the two parity classes separately gives yield $(\sqrt2-1)\sqrt{a/D}/\pi$ asymptotically for **each** sign. Every launch costs $2D$ walk ticks and $D$ rail reads through this decision.

Fold $k$ modulo $\pi$ to $[-\pi/2,\pi/2)$ and let $r$ be its absolute value. The two signs and both parity replicas remain coherent in a fine word. The folded density is proportional to $\sin^{2A}r\cos^{2B}r$. Its mode is $\kappa=\arctan\sqrt{A/B}$. Write $L$ for its log density. Since $L'(\kappa)=0$ and $L''\le-2D$, integrating the derivative of $(r-\kappa)e^L$ gives

$$\|r-\kappa\|_2\le (2D)^{-1/2},\qquad R_D=\kappa+(2D)^{-1/2}\ \ge\ \|r\|_2.$$

Here and below the norms use the conditional state or the associated conditional momentum law. The endpoint terms vanish for $A,B\ge1$. Before the pulses the position standard deviation is

$$s^2=\frac D2\left(\frac A{A-1/2}+\frac B{B-1/2}\right).$$

Indeed for the real amplitude $f=\sin^A k\cos^B k$, integration by parts gives $\|f'\|^2/\|f\|^2=-\mathbb E L''/4$ on a folded quadrant. The expectations of $\csc^2r,\sec^2r$ are $D/(A-1/2),D/(B-1/2)$ by the same beta integral.

## Two free flights and two sign reversals

Let $\omega(k)=\arcsin(\sin k/\sqrt2)$ and let $\boldsymbol n(k)=(\cos k,\sin k,\cos k)/\sqrt{1+\cos^2 k}$. In the positive folded quadrant any even $T$ obeys $U(k)^T=\exp[-iT\omega(k)\boldsymbol n(k)\cdot\boldsymbol\sigma]$. Choose $T_1,T_2$ to be the nearest nonnegative even integers to $\pi/[4\omega(\kappa)]$ and $\pi/[8\omega(\kappa)]$, respectively, taking the lower at a tie. On the whole walker apply

$$U^{T_1},\quad Z,\quad U^{T_2},\quad Z$$

in chronological order. These are rail sign changes between walk shifts and cost two controlled pulses on each passing launch. The additional walk time is $T_1+T_2=O(\sqrt{D/a})$. The release clock starts after the second pulse.

For the ideal rotations write $\boldsymbol h=(1,0,1)/\sqrt2$, $\boldsymbol j=(-1,0,1)/\sqrt2$, and $\boldsymbol e=\boldsymbol h\times\boldsymbol j$. Conjugation by $Z$ sends $\boldsymbol h$ to $\boldsymbol j$. Rotation through $+\pi/2$ about $\boldsymbol h$ takes the input $+\boldsymbol z=(\boldsymbol h+\boldsymbol j)/\sqrt2$ to $(\boldsymbol h+\boldsymbol e)/\sqrt2$. Rotation through $+\pi/4$ about $\boldsymbol j$ then gives $\boldsymbol h$. The same two rotations take $-\boldsymbol z$ to $-\boldsymbol h$. The chart at negative folded momentum has the conjugate spinor because the apparatus is real. Its target eigenprojector of $\tau H$ is real. On shifting $k$ by $\pi$ each even walk power is identical. These identities account for all four lobes.

Here is a finite error bound. In the positive quadrant $\|\boldsymbol n(r)-\boldsymbol h\|\le\sqrt2 r$, $|\omega'|\le1$ and $|T_i\omega(\kappa)-\theta_i/2|\le\omega(\kappa)$ for $\theta_1=\pi/2,\theta_2=\pi/4$. Comparing cosines and sines in the matrix exponential, the operator error of flight $i$ from its ideal spinor rotation is at most $T_i|r-\kappa|+\omega(\kappa)+\sqrt2 r$. Telescoping the two unitaries and using the preceding chart symmetries yields the same RMS spinor error bound on each chart. The desired velocity branch at launch has projector $(I+\tau\,\mathrm{sgn}(\cos k)\boldsymbol n(k)\cdot\boldsymbol\sigma)/2$. Its distance from $(I+\tau H)/2$ is at most $r/\sqrt2$. Therefore its complementary conditional mass $\ell$ obeys

$$\sqrt{\ell}\ \le\ E_D=
\frac{T_1+T_2}{\sqrt{2D}}+2\omega(\kappa)+(2\sqrt2+1/\sqrt2)R_D
=O\!\left(a^{-1/2}+\sqrt{a/D}\right).$$

The four lobes approach the two extremal-velocity chart centres as the conditional error vanishes. In a finite control, omit both $Z$ pulses while keeping the same waiting times and success record. The surviving free powers preserve band populations; the opposite-velocity weight is then at least $(1-1/\sqrt2)/2$ at every momentum. A later long free position read relative to the registered centre can distinguish the two preparations.

For a short position comparison use $D=16$, $a=1$, and 127 free release ticks. Both accepted counts have $(T_1,T_2)=(4,2)$. The tested event is a terminal position on the wrong side, $\tau(X_{127}-C)<0$. There is no tie at this clock. The table gives joint probabilities per original launch, calculated by signed path addition. The common reject fraction is $0.87172553$.

| Tag and count | Incident tag rate | Tag and wrong side, two pulses | Tag and wrong side, omitted pulses |
|---|---:|---:|---:|
| $-$, one change | 0.07223222 | 0.00456091 | 0.01119736 |
| $+$, two changes | 0.05604224 | 0.00677691 | 0.00904110 |

At $D=2^{20}$ the measured variable in the replay is instead the calculated band projection. For counts 1024 and 1025 the pulse times are $(36,18)$. Numerical quadrature gives opposite-band masses $0.00019519$ and $0.00020134$, respectively. With the pulses omitted they are $0.14653302$ and $0.14653311$. These are conditional on the specified counts; each count has incident mass about $9.7\times10^{-6}$.

## Released position in a weak field

Attach $e^{-ihx}$ at each departure after release. Set $v(k)=\cos k/\sqrt{1+\cos^2k}$ and $\bar v_{N,h}=N^{-1}\sum_{j=1}^N v(-jh)$. The [finite-impulse estimate and proof](Preparing_one_transport_band_with_rail_records.md) control the derivative of the flight propagator in operator norm. They apply also when the released rail depends on $k$. Each preparation tick adds at most one to the norm of the position derivative, since $\|\partial_k U(k)\|=1$, and $Z$ is constant. Hence the RMS distance from $C$ at release is at most $s+T_1+T_2$. Using $|v'|\le1$ to fold the initial momentum and the preceding wrong-band bound gives the following estimate for one terminal position $X_N$:

$$
\left\|(X_N-C)/N-\tau\bar v_{N,h}\right\|_2
\le (s+T_1+T_2+4)/N+16|h|+32Nh^2+\sqrt2 E_D+R_D .
$$

For $h=F/n$, $N=\lfloor nt\rfloor$, fixed $t>0$ and $\sqrt D/n\to0$, the recorded displacement $(X_N-C)/n$ converges in mean square to $\tau\int_0^t v(-Fs)\,ds$ under the stated count scaling. The bound is uniform over the accepted counts and fine words of each sign. Free release gives $\tau t/\sqrt2$. This describes one endpoint per launch. The preparation occupies $2D+O(\sqrt{D/a})$ ticks before release on a success. The probability that an incident launch enters either trajectory tends to zero. Coherent direction writes, a switchable departure field, a calibrated uniform $Z$, and the physical units and timing remain experimental premises.

## What the last sharp read allows

Consider adaptive finite fine histories using exclusively ordinary free ticks and two sharp measurements on the line: a full site write preserving both rails, or a position-blind $R/L$ write. At the last site write the momentum density becomes uniform and stays uniform under subsequent free ticks. A sharp-site source followed solely by free waiting has the same property. At a last rail write the state is a sharp rail with some scalar spatial state, possibly mixed. In either case of sharp rail the projection onto the undesired signed-velocity branch is at least $(1-1/\sqrt2)/2$ pointwise, because $|n_z(k)|\le1/\sqrt2$. Free ticks commute with the band projections. Thus these fine words cannot simultaneously concentrate momentum at $0,\pi$ and select one transport band. Pooling cannot circumvent the obstruction: if the mass outside shrinking chart windows vanishes, the pooled fraction ending with a site write must vanish, leaving the rail floor. The same reasoning applies if a [sharp-site tagged rail](A_rail_measurement_from_four_free_steps.md) is transferred from the ring to a single site on the line. An eventual sharp rail write removes the incoming polarization, and free waiting at the sharp source retains its uniform momentum density.

Two sign pulses take the positive construction outside that restricted class. A [coherent positional flight window](Flight_window_preparation.md) changes the measurement class; [returning gain paths](Returning_loops_and_one_classical_ray.md) address the different mechanical band edge. The [replay](check_two_pulse_band_source.py) enumerates incident signed paths, tests the pulse order against direct walk matrices, and compares a finite field flight in position and Fourier coordinates.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed the protocol, estimates and replay.
