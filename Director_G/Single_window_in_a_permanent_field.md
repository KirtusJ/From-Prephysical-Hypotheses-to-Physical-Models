# A sharper central flight window from one sharp launch

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

For the free Hadamard walk, one central position window at time $t$ selects small group velocity with vanishing relative state error whenever $w\to0$ and $tw^2\to\infty$. Here $w$ is the half-width in the velocity coordinate $x/t$. The proof uses the sharp launching well to bound the nonstationary amplitudes directly. The earlier comparison for general operator cutoffs required $tw^{5/2}\to\infty$. The improved timing is relevant to switching on or retaining a weak physical sheet field during preparation. [Previous window estimate and apparatus](Flight_window_preparation.md) · [Uninterrupted weak-field comparison](Uninterrupted_sheet_read.md)

## Source estimate

Work on the integer line with a sharp launch at zero and any fixed normalized rail spinor $\xi$. The Fourier input is constant. Write $U(k)=\operatorname{diag}(e^{-ik},e^{ik})H$ and use its two smooth orthogonal projectors $P_b(k)$, $b=\pm1$. Up to a clock-dependent scalar sign on the second band, the eigenphases are $e^{-ib\omega(k)}$, $\omega(k)=\arcsin(\sin k/\sqrt2)$. The band velocities are

$$v_b(k)=b\,\frac{\cos k}{\sqrt{1+\cos^2k}}.$$

Let $Q_w$ be the spectral indicator of $|v_b(k)|\le w$ on each band, $A_w$ the position indicator of $|x|\le tw$, and $\psi$ the launch. Since $|v_b|$ is the same on both bands, $Q_w$ acts by the scalar indicator on both rails. There are two simple zero-velocity points at $\pm\pi/2$. Direct integration gives

$$
\|Q_w\psi\|^2=\frac2\pi\arcsin\!\left(\frac{w}{\sqrt{1-w^2}}\right)
              =\frac{2w}{\pi}+O(w^3)
$$

for $0<w<1/\sqrt2$. The norm comparison is

$$
\frac{\|A_w U^t\psi-U^tQ_w\psi\|}{\sqrt w}
       \le C(tw^2)^{-1/4}
$$

for all sufficiently small $w$ and sufficiently large $tw^2$, independently of $\xi$. In particular the per-launch window probability is $(2w/\pi)(1+o(1))$, and the normalized accepted state approaches the normalized velocity-selected state in norm. The position read is a single coherent yes/no aperture; independently recording the individual wells and pooling them would change its continued state.

To prove the estimate use a relative boundary strip of width $\eta$, $0<\eta<1/2$. Write $Q_-$ for the inner spectral indicator $|v_b|\le(1-\eta)w$, and $Q_+$ for the indicator $|v_b|\le(1+\eta)w$. The launch norm in the strip $Q_+-Q_-$ is at most $C\sqrt{\eta w}$ by the bounded velocity density near zero. Sharp Fourier cuts are allowed in this argument.

At site $x$ put $u=x/t$. Each band amplitude is a sum of integrals with phase $t[uk-b\omega(k)]$ and smooth vector amplitude $P_b(k)\xi$. Split into a fixed number of arcs where $v_b$ is monotone, subdividing at the boundaries of the chosen velocity interval. On an arc whose velocities stay at distance at least $d>0$ from $u$, one integration by parts bounds the vector integral by $C/(td)$. In detail the endpoint terms and the derivative of the smooth amplitude give this bound; the integral of $|v_b'|/|u-v_b|^2$ is at most $2/d$ on a monotone arc. The number of arcs and the total variation of the amplitude are bounded independently of $w,\eta,u,t$.

For the inner indicator and sites outside the spatial window take $d\ge |x|/t-(1-\eta)w$. For the outer indicator $I-Q_+$ and sites inside the window take $d\ge(1+\eta)w-|x|/t$. In each case, summing the squared pointwise bounds gives at most $C/(t\eta w)$: moving integer sites away from the nearest boundary gives a reciprocal-square series bounded by its first term and its integral, with initial denominator at least $t\eta w$. This bound holds when $t\eta w\ge1$ and includes sites exactly on the permitted boundary. Thus

$$
\begin{split}
\|(1-A_w)U^tQ_-\psi\|+\|A_wU^t(1-Q_+)\psi\|
   &\le C(t\eta w)^{-1/2},\\
\|A_w U^t\psi-U^tQ_w\psi\|
   &\le C[(t\eta w)^{-1/2}+\sqrt{\eta w}].
\end{split}
$$

Taking $\eta=(tw^2)^{-1/2}$ proves the claim. The proof bounds the norm only for this sharp launch. It makes no regularity or finite-variance claim for the discontinuous normalized Fourier-cut state.

## Timing and use on a ring

For example $w=\delta^{17/16}$ and $t$ nearest $\delta^{-9/4}$ give $tw^2\asymp\delta^{-1/8}\to\infty$ while $tw^{5/2}\to0$. On the shrinking-action physical scales $Y=\delta^2x$ and $\tau=\delta^3$ per tick, the half-width of the accepted spatial interval is $\delta^2tw\asymp\delta^{13/16}$, the preparation time is $\delta^3t\asymp\delta^{3/4}$, and $w/\delta\to0$. These choices leave time for an unmasked force flight after the aperture.

On a $4M$ ring, place the coordinate seam outside the cone through the last physically compared tick, or work on its covering line and project back. If the horizon obeys $2(t+n)<4M$, then the native ring and line agree exactly on the paths of the preparation and $n$-tick release. Apply the Fourier-cut comparison on the line before returning to this finite native observable. The Fourier-cut auxiliary state need not have compact position support. A permanent field can move the input/output momentum chart, so extending the free comparison to such a flight must account for both the weak-field norm error and the position-dependent phase that remains at release.

## Keeping the same field on through release

At physical character $s=\pm1$ use the negative-exponent convention and set $\delta=(\pi/(MF))^{1/4}$ for $F>0$, so $h=s\pi/M=sF\delta^4$. At each clock the sharp launch occupies one site parity. There the departure staircase equals the linear phase $e^{-ihx}$ up to a clock-dependent scalar. With $\kappa_t=(t-1)h/2$, the centered momentum-product bound for the actual unitary $U_h$ gives, up to a global phase,

$$
\|U_h^t\psi-e^{-i\kappa_t X}U^t\psi\|
    \le \sqrt2(t-1)|h|+\tfrac1{24}t(t^2-1)h^2.
$$

Here $X$ is displacement relative to the launch. The sign of the phase follows from translating the output momentum argument by $+\kappa_t$. This estimate is on full state norm before projection. It is $O(\delta^{5/4})=o(\sqrt w)$ for the selected parameters. The phase commutes with the position window. After using the free estimate and dividing by the passing norm, the *actual accepted state* is $o(1)$ in norm from

$$
e^{-i\kappa_t X}U^tQ_w\psi/\|Q_w\psi\|.
$$

Its per-launch probability is $(2/\pi+o(1))w$ in each target sector. The shift $|\kappa_t|/\delta=O(\delta^{3/4})$ vanishes on scaled momentum, even though the phase need not be discarded in the norm comparison. A launch at any known well contributes its translation and a common sector phase. Either sharp rail gives the same leading probability. [Centered estimate and exact finite-ring momentum shift](Uninterrupted_sheet_read.md)

For the subsequent motion $n\delta^3\to T>0$, split the comparison state into the charts around $\pm\pi/2$ and the two eigenbands on each chart. Up to the vanishing error from the momentum shift in the smooth band projectors, each chart-band component of a sharp R or L launch has squared mass $1/4+o(1)$ before flight. Indeed the two charts have equal width, and the sharp rail has squared overlap $1/2$ with each circular eigenvector at their centers. Their curvatures $b=\pm1$ each have total weight $1/2$. Arbitrary complex rail superpositions in the free estimate need not have these same band weights.

A smooth taper justifies position control for the discontinuous Fourier cut. For fixed $0<\rho<1/2$, replace $Q_w$ by a smooth cutoff equal to one on $|v_b|\le(1-\rho)w$, supported in $|v_b|\le w$, with derivative $O(1/(\rho w))$. Before normalizing, the changed part has norm $O(\sqrt{\rho w})$. On each nonvanishing normalized chart component the slow momentum $(k-k_*)/\delta$ has magnitude $O((w+|\kappa_t|)/\delta)=o(1)$. Its displacement operator is $\delta^2 i\partial_k$. Differentiating its envelope, its smooth eigenvector and the retained free spectral phase shows that its root-mean-square displacement about the launch is at most

$$
C\delta^2\bigl(1+1/(\rho w)+tw\bigr)=o(1).
$$

The spatial rephasing is a translation in momentum and leaves this position bound unchanged. After it, replacing the band projector by its value at the translated momentum costs $O(|\kappa_t|)$ in norm. The forced-envelope norm estimate applies to these $\delta$-dependent inputs because their momenta lie in a fixed compact scaled chart and the estimate is uniform over its normalized envelopes. Each component evolves for bounded $T$ with Hamiltonian $bp^2/2+sFY$. Its position in the Heisenberg picture is its incident position plus $bTp-bsFT^2/2$. The two incident deviations just bounded therefore imply concentration at $Y_0-bsFT^2/2$ relative to the launch well's macroscopic coordinate $Y_0$. First take $\delta\to0$ with $\rho$ fixed, then send $\rho\to0$. The argument establishes concentration in probability without asserting finite second moments for the untapered sharp spectral cut. [Band estimate and forced linear motion](Forced_envelope_and_classical_motion.md)

At a terminal read the macroscopic characteristic functions add over these components. Multiplication by $e^{i\xi Y}$ shifts lattice momentum by $O(\delta^2)$; separated charts stay disjoint and the cross-band overlaps are $O(\delta^2)$ by orthogonality and smoothness. The conditional position law converges to equal masses at $Y_0\pm FT^2/2$. The sheet-conjugate sectors give the same position law, while the sign of the individual curvature paired with a displacement can reverse. A final binary position question can test one fixed narrow tube about either trajectory, giving $1/2+o(1)$ conditional on the window. A tube around their union gives $1-o(1)$. The source pointer reports only its membership bit; a persistent record of every passing well would produce a different preparation.

## Original launches and retries

For an originally localized sheet in the squared-coordinate realization, a preceding sharp selector can accept $1-o(1)$ of the Fourier pair $s=\pm1$, of original mass $2/M$. If its wrong posterior is $\eta=o(w)$, even assigning window probability one to each contaminating sector gives a wrong fraction $o(1)$ after the window. No uniform small-window probability for the competing sectors is required. On this original-launch accounting the sheet herald, window pass and terminal arrival in the union have combined probability $(2/M)(2w/\pi)(1+o(1))$. Either separate tube has half that rate. For an initial classified mixture, replace $2/M$ by its actual incident physical-unit weight and include the selector's actual unit completeness. A source with zero unit mass requires a different inference.

For a classified mixture that includes the persistent counting law, the tolerance $\eta=o(w)$ is sharp in this regime. From any sharp site and rail, counting makes each subsequent left/right choice fair and independent. Its window failure probability is at most $2e^{-tw^2/2}=o(1)$ by the fair-coin exponential bound. If the incident count weight at the window is $\eta\sim cw$ for fixed $c>0$ and the remaining input has the unit character law, the count fraction after a pass tends to $c/(c+2/\pi)$. Its conditional flight starts within $\delta^2tw=o(1)$ of $Y_0$, and its independent increments add variance $n\delta^4\to0$. It therefore puts this positive limiting mass at $Y_0$ between the two accelerated arrivals. This example concerns a count component permitted in the general score classification. [Counting and the classical flight](Count_weight_in_classical_flight.md)

One successful sharp-sector launch needs only one central window and an unmasked flight. Its window yield decays polynomially with refinement. If fresh identical sharp preparations are available, repeating until a window passes takes order $1/w$ attempts to obtain a fixed success probability. Sequential retries each costing $t$ ticks of duration $\delta^3$ would occupy order $\delta^3t/w=\delta^{-5/16}$ macroscopic time before release for the parameters above. Fixed-fraction success in vanishing time does not follow from a polynomial single-attempt yield. Restarting a failed coherent window is not automatically a fresh sharp launch. Its recorded well, rail and retained sheet, or a separately supplied replacement source, must be specified. An amplified yield also cannot be counted as one original trial. [Position-product record rules](Position_transcripts_and_selected_laws.md) · [Finite-time sheet selectors](Native_multiscale_selector.md)

The spectral comparison proves closeness to an entire normalized velocity-cut state. A complementary central-site stationary-phase expansion instead controls the Fourier concentration of the state actually retained in the aperture; it can therefore cover scales where the stronger velocity-cut norm approximation is unavailable. Finite preparation and release trials use the physical step on both actual rails and keep discrepancies from the limiting law. [Central-site argument](Central_window_chirps.md) · [Field-on flight checker](check_central_window_flight.py) · [Finite trials](results/central_window_flight.json) · [Serial preparation costs](Window_source_cost.md)
