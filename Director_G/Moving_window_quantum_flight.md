# A translating position aperture suppresses counting and retains a Fresnel wave

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

At fixed action, displace a single coherent position aperture by more than the width of the fair counting walk while keeping it inside the Hadamard walk's ballistic cone. The square-character passing probability remains of order $\delta$. The count passing probability decays exponentially in $1/\delta$. In a frame following the aperture at its precisely specified group velocity, the accepted square component gives the same limiting Fresnel position law as the central aperture. [Central-aperture derivation and source assumptions](Central_window_chirps.md)

Use physical site pitch $\delta=(\pi/(MF))^{1/3}$, clock $\delta^2$, bounded unit-sheet label $s=\pm1$ and departure slope $h=sF\delta^3$ on the $4M$-well ring. Start at the sharp origin on R. Put $v=\sqrt\delta$, choose $t\delta^2\to\kappa>0$ and $L\delta\to A>0$. Retain all wells satisfying $|x-vt|\le L$ as one binary outcome without resolving the individual wells. Use the real center $vt$ in that predicate, including when it is not a lattice site. After another $n$ uninterrupted ticks with $n\delta^2\to T>0$, record

$$
 Y=\delta[x-v(t+n)] .
$$

During preparation use $Y_{\rm in}=\delta(x-vt)$. These coordinates use the actual integer clocks. In physical units the translating detector moves at velocity $v/\delta=\delta^{-1/2}$ and its flight displacement diverges. This is a calibrated moving frame; the released waves do not remain near a fixed laboratory origin on this scale. The native light cone through $t+n=O(\delta^{-2})$ embeds in the physical ring.

## The action at the moving aperture

Write $\omega(k)=\arcsin(\sin k/\sqrt2)$ and let $P(k)$ be the rail projector of the eigenvalue $e^{-i\omega(k)}$. The two stationary roots with **the same exact group velocity** $v$ are $k_b(v)=-b\arccos[v/\sqrt{1-v^2}]$, $b=\pm1$. Their curvatures are $\omega''(k_b(v))=b c(v)$, with $c(v)=(1-v^2)\sqrt{1-2v^2}\to1$. Let $S_b(v)=v k_b(v)-\omega(k_b(v))$. If $z=x-vt$ then uniformly on $|z|\le L$,

$$
 tS_b(x/t)=tS_b(v)+k_b(v)z+\frac{b z^2}{2t c(v)}+O(L^3/t^2).
$$

The remainder is $O(\delta)$. The rapidly changing branch scalar $e^{itS_b(v)}$ need not converge. Expanding instead at the zero-velocity carrier and discarding higher terms before translating the well coordinate would not control this scalar or the prescribed recentering.

In the field-on momentum product, the centered eigenphase contributes $-b h^2t(t^2-1)c(v)/24+o(1)$ to the scalar phase. The position gauge $e^{-i(t-1)hx/2}$ contributes a common home phase and $e^{-isF\kappa Y_{\rm in}/2+o(1)}$ on the interval. The pre-aperture norm error after keeping the curvature phase is $O(t|h|+t^5h^4)=O(\delta)$. The stationary expansion's per-well remainder is $O(t^{-3/2})$ uniformly on this moving window, whose velocities lie in a fixed neighborhood of zero for small $\delta$. Thus the errors after restricting to the interval are $o(\sqrt\delta)$ in norm. [Centered momentum estimate](Uninterrupted_sheet_read.md) · [Stationary branches and parity](Central_window_chirps.md)

On the occupied parity, each saddle has amplitude vector $2P(k_b(v))e_R/\sqrt{2\pi t c(v)}$ up to its phase and vanishing relative window error. Its squared spinor projection is $(1+v)/2$. The mutual overlap of the two spinors tends to zero as $O(v+L/t)$. Summing the two contributions gives the per-original-target-launch pass probability $2A\delta/(\pi\kappa)+o(\delta)$, with asymptotically equal masses. After recentering by $vt$ and demodulating each exact carrier, its normalized scalar converges to

$$
 f_b(Y_{\rm in})=(2A)^{-1/2}\,\mathbf1_{[-A,A]}(Y_{\rm in})
        \exp[i bY_{\rm in}^2/(2\kappa)-i sF\kappa Y_{\rm in}/2].
$$

This wave is sampled on a possibly shifted parity grid of spacing $2\delta$. Uniform Riemann sums on those translates justify the norm statements, including endpoint rounding. The remaining branch scalars include the stationary phase $e^{-ib\pi/4}$ and the curvature scalar above. The two carriers modulo $\pi$ now have separation $2v+O(v^3)$, which is much larger than $\delta$. Each also has its parity replica translated by $\pi$.

## Unmodified flight and the count control

First approximate each $f_b$ in $L^2$ by a smooth function supported on a bounded momentum interval $|p|\le P$, where momentum is measured in units of $\delta$ about $k_b(v)$. Along the forced characteristic the microscopic momentum is $k_b(v)+\delta(p-sFj\delta^2)$ at tick $j$. Expand the eigenphase at the exact carrier. Its constant is a branch phase. Its linear contribution to the positive action sum through $n$ ticks is

$$
 v\delta n p-vh\,n(n+1)/2.
$$

In the inverse transform the first term's drift cancels on translating the physical coordinate by $nv$, using the prescribed output frame. The other term and the difference between incoming and outgoing momentum in that translation are scalar phases. The quadratic term converges to the time integral of $b(p-sFu)^2/2$, because $c(v)\to1$. For bounded $p,T$ the accumulated cubic Taylor error is $O(n\delta^3)=O(\delta)$ and moving the gapped rail eigenframe costs $O(n|h|)=O(\delta)$. The opposite parity replica has the same curvature. Position characteristic functions at fixed wave number only shift microscopic momenta by $O(\delta)$ and cannot reconnect the separated carrier charts after cutoff. Remove the smooth momentum approximation using unitarity; the sharp interval waves need not have finite momentum variance. This yields the equal mixture generated by $H_b=bp^2/2+sFY$ from $f_b$. [Forced-envelope comparison](Forced_envelope_and_classical_motion.md)

In particular put $\Lambda=\max(2A-|T\xi|,0)$ and $\operatorname{sinc}u=\sin(u)/u$ with $\operatorname{sinc}0=1$. In the specified moving frame the conditional terminal characteristic function is

$$
 \frac{\Lambda}{2A}\,
 \operatorname{sinc}\!\left(\frac{\xi(1+T/\kappa)\Lambda}{2}\right)
 \cos\!\left(\frac{sF\xi(\kappa T+T^2)}{2}\right).
$$

It vanishes in the limit for $|T\xi|\ge2A$. This is a position read on the coherent passing subensemble, with the same force active before and after the aperture. [Derivation of the overlap of the translated finite intervals](Central_window_chirps.md)

Under the fair counting law the well $X_t$ is the sum of $t$ independent signs. The aperture pass is contained in $X_t\ge vt-L$. Its probability is at most $\exp[-t(v-L/t)^2/2]$ once $v>L/t$, and $t(v-L/t)^2\sim\kappa/\delta$. For a source with a fixed count fraction $c_0<1$ and the remaining weight in the physical unit pair, its total pass probability is asymptotic to $(1-c_0)2A\delta/(\pi\kappa)$ and the conditional count fraction tends to zero. More generally, count is negligible relative to target weight $b_1$ if $c_0\exp[-t(v-L/t)^2/2]=o(b_1\delta)$. An unspecified competing coherent sector with appreciable passing probability is a different case: incident contaminant weight $o(b_1\delta)$ suffices without a model for its pass. A source with zero unit weight cannot provide a genuine unit-character herald. [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)

An aperture that stays inside $|\delta x|\le A_0$ for fixed $A_0$ cannot produce this count rejection at this clock, regardless of which subset of those wells it passes. On every occupied parity site there the fair binomial probability is at least $c/\sqrt t$, by Stirling's formula uniformly for $|x|=O(\sqrt t)$. The stationary amplitudes of the coherent centered approximation are $O(1/\sqrt t)$ there, and its global norm error $O(\delta)=O(1/\sqrt t)$ also bounds each well's residual norm. The coherent probability is therefore at most $C/t$ per site. Summing on any such subset $S$ gives $\Pr_s(S)\le C'\delta\Pr_{\rm count}(S)$. This argument concerns one diagonal position mask from a sharp launch. It gives no bound for a sequence of adaptive tests or an interferometric readout.

Each attempt on the supplied sector takes $t\sim\kappa/\delta^2$ native ticks. Independent restarted target launches require asymptotically $\pi\kappa/(2A\delta)$ attempts per herald. Thus the mean serial physical preparation time is asymptotic to $\pi\kappa^2/(2A\delta)$ before any charge-selection, source-reset or detector-latency overhead. The positive comparison is a polynomial-yield field-on quantum flight in its tracked frame; it neither favors one of the conjugate unit orientations nor establishes the parent square rule.

The finite model records give the aperture yield, exact fair-count pass and terminal position characteristic function at six sheet orders. A separate shrinking-action schedule keeps the observation coordinates in the laboratory frame. [Checker](check_moving_window_flight.py) · [Full finite records](results/moving_window_flight.json) · [Displacing a classical window](Displacing_a_classical_window.md)
