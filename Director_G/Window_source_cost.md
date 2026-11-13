# What does it cost to obtain one heralded flight packet?

**Kirtus Justus**, Theoretical Physicist<br>
Port Coquitlam, British Columbia, Canada<br>
Research supplement prepared by Director G (OpenAI Codex), 13 November 2026.

An ideal binary position window can prepare a packet whose free terminal position approaches a prescribed ray. At the published scaling, one attempt takes vanishing physical time, yet a serial source with a bounded total preparation time succeeds with probability tending to zero. The distinction comes from charging the failed preparations. A spatial Fourier bound gives a second obstruction that also applies to the force scaling $\varepsilon=\delta^{9/10}$. [Window preparation and its detector assumptions](Flight_window_preparation.md)

## One window

Use site pitch $a=\varepsilon\delta$ and tick duration $\tau=\varepsilon\delta^2$. Start sharply at $(s,R)$, propagate $T$ ticks, and copy a bit for $|(x-s)/T-v|\le w$, with $v=\delta p_0$ and fixed $p_0$. The yes operation retains both signed rail amplitudes at every accepted site, coherently. Under the common square score for the full pointer and endpoint records, the yes probability is $p=\|M U^T|s,R\rangle\|^2$. A complete site read inside the window defines a different operation. The apparatus must preserve the accepted vector while it reads the bit. If relative displacement is stored cyclically modulo $D$ and the apparatus must operate by equality on that register, $D>2T$ suffices to distinguish every displacement in the launch cone. A smaller register requires checking that the accepted residues have no extra preimages in that cone. Wrapping can otherwise admit remote packets and change both yield and quality. [Signed records and full-site controls](results/flight_window.json)

Let $L$ count the accessible sites in this window. The occupied parity gives $L\le Tw+1$. Every normalized two-rail packet $h$ supported on these sites satisfies, for any measurable momentum region $K$,

$$
\int_K \|\widehat h(k)\|^2\frac{dk}{2\pi}
\le \frac{L |K|}{2\pi}.
$$

Indeed the norm squared of $\sum_x e^{-ikx}h(x)$ is at most $L\sum_x\|h(x)\|^2=L$. In band $b$ the lattice velocity is $\nu_b(k)=\pm\cos k/\sqrt{1+\cos^2 k}$. For $|\nu_b-\delta p_0|\le\delta\eta$ with small $\delta$, all preimages lie near the regular roots $\pm\pi/2$. The union $K$ for both bands has length at most $C\delta\eta$. Projecting onto the matching bands can only reduce the spinor norm on $K$. Consequently,

$$
\Pr_h(|V/\delta-p_0|\le\eta)\le C L\delta\eta .
$$

If the prepared velocity concentrates at $p_0$ in probability, apply this inequality at each fixed $\eta>0$ and then let $\eta\downarrow0$. It requires $L\delta\to\infty$, hence $\delta(Tw+1)\to\infty$. The probability here denotes the spectral measure of the asymptotic velocity in the normalized prepared state. A direct moving terminal-focus test at a single time does not establish velocity concentration. The window preparation theorem supplies the stronger property by norm approximation to a velocity-filtered state. For a folded complex field, a non-symmetric momentum interval of the scalar is insufficient by itself to bound an individual physical eigenband. The full-spinor projector argument includes both signs and all their physical preimages. On a ring the integral bound uses the fraction of Fourier grid points in $K$ in place of $|K|/(2\pi)$; the line result applies directly on growing rings free of wrapping throughout the flight.

The sharp launch puts at most $C/T$ probability at each site with $|(x-s)/T|$ in a fixed compact neighborhood of zero. To see this, Fourier-invert each band. The amplitude is an oscillatory integral with smooth bounded projector weight and phase $k(x-s)/T\mp\omega(k)$, where $\sin\omega=\sin k/\sqrt2$. On small neighborhoods of $\pm\pi/2$ the second derivative is bounded away from zero. The second-derivative estimate for oscillatory integrals gives $O(T^{-1/2})$ uniformly in the chosen velocities. On the complementary arcs the first derivative is bounded away from zero and integration by parts gives $O(T^{-1})$. Squaring and summing the two rails proves the bound. The estimate is restricted to the interior and does not cover the ballistic caustics. Thus $p\le C(w+1/T)$, and $p\le C'w$ for any family meeting the velocity concentration condition above.

## Serial time and parallel copies

Let $b_\delta$ be the physical duration of an attempt, including reset and flag access if those are charged. Suppose that conditional on every earlier failure a fresh attempt has the same success probability $p$ and the same accepted packet up to a known origin. In $K$ serial attempts the chance of producing a packet is exactly $1-(1-p)^K$. Its mean acquisition time without a cap is $b_\delta/p$ when attempts have equal duration. For $p\to0$, a bounded positive clock budget $B$ permits success tending to one exactly when $\lfloor B/b_\delta\rfloor p\to\infty$, equivalently $b_\delta/p\to0$. If $b_\delta/p\to c\in(0,\infty)$ the limiting success probability is $1-e^{-B/c}$. For varying known conditional hazards $p_j$ along the failure sequence, the corresponding criterion is $\sum_j-\log(1-p_j)\to\infty$. Marginal success rates alone permit perfect correlation and cannot justify repetition.

Even with a free reset, $b_\delta\ge T\tau$. For a velocity-sharp preparation with $w=o(\delta)$ the preceding inequalities give

$$
\frac{b_\delta}{p}\ \ge\ c\,\frac{\varepsilon\delta}{w^2}\,(\delta T w),
\qquad \delta T w\longrightarrow\infty .
$$

In particular this lower bound diverges for $\varepsilon=\delta$ and $\varepsilon=\delta^{9/10}$. It applies to repeated sharp launches using this position aperture. A previously prepared momentum source, an amplitude-amplifying controller or a force acting *during* the preparatory flight calls for a separate estimate of the incoming state, the instrument and the attempt duration.

For the published free example $w=\delta^{11/10}$, $T\sim\delta^{-14/5}$ and $\varepsilon=\delta$, one has $p\sim 2w/\pi$, $b_\delta\sim\delta^{1/5}$ with zero overhead, and mean serial time $\sim(\pi/2)\delta^{-9/10}$. With $J$ independent occupied lanes in each of $K=\lfloor B/b_\delta\rfloor$ rounds, success is $1-(1-p)^{JK}$. At fixed $B$, success tends to one exactly when $J\delta^{9/10}\to\infty$. A single parallel round instead requires $J\delta^{11/10}\to\infty$. For target failure $\alpha$, the exact total number of trials required is $\lceil\log\alpha/\log(1-p)\rceil$.

The four-tick force construction uses the same free preparation with $\varepsilon=\delta^{9/10}$ and applies the force after release. Its single-attempt duration is $\sim\delta^{1/10}$ with zero overhead, so the mean serial acquisition time is $\sim(\pi/2)\delta^{-1}$. For independent lanes at fixed positive deadline $B$, the high-success condition becomes $J\delta\to\infty$. The force result predicts the terminal position conditional on the source flag. These time and lane counts charge each attempted preparation. [Four-tick force and sharp-launch theorem](Four_tick_force.md) · [Merged PR #17](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/17)

Select the first successful label using flags alone. Its conditional wave function is the common accepted packet when the independent registers factor and addressing the winner preserves coherence across its window. Keeping only runs with exactly one success loses a finite fraction even at the optimal mean count. A single marker in a superposition or classical mixture of lane labels still has total success $p$ under this duplicated block-diagonal test. Simultaneous independent lanes use $J$ particles and associated pointers. If lanes are laid out with separation $\ell$ on a line and signals travel at speed $c$, only $1+2cB/\ell$ lane centers can inform a specified output port within $B$. Transfer of the packet also requires an actual coherent route. A rejected carrier localized at a new position can launch another trial from that recorded origin; delivering the result to a fixed laboratory origin incurs a distinct cost.

## Changing the scale

The existing sufficient window theorem assumes $Tw^{5/2}\to\infty$, $a/w\to0$, $aTw\to0$, $w/\delta\to0$. Among power laws $\varepsilon=\delta^r$, $w=\delta^\beta$, $T\sim\delta^{-\gamma}$, the ideal serial source can meet these conditions and have $T\tau/p\to0$ exactly when $r>3/2$. Indeed $\beta>1$ and $5\beta/2<\gamma<r+2-\beta$ are necessary. For $r>3/2$, choose $\beta$ sufficiently close to one and then $\gamma$ in that interval; both spatial localization requirements follow. For instance $(r,\beta,\gamma)=(1.75,1.02,2.60)$ gives mean acquisition time of order $\delta^{0.13}$. This threshold concerns the published sufficient estimates and equal-duration sharp resets. The Fourier obstruction alone leaves the intermediate action exponents $1<r\le3/2$ open. A ray assertion after release still requires the applicable mechanics and force estimates at the new scales.

Two finite checks of the resource accounting use the raw signed update at each tick and sum $R^2+L^2$ over both rails at the inclusive window. At $T=16$, $W=[0,2]$, acceptance is exactly $1275/16384$ and 37 independent trials suffice for 95% success. At $T=64$, $W=[2,6]$, it is $282728967155285175/9223372036854775808$ and 97 trials are needed. These are finite acceptance calculations. At the finest published flight, $\delta=1/40$, acceptance was 0.0112854 but 45.4% of the accepted mass was still outside the declared velocity tolerance. Replication improves availability alone; its conditional packet quality remains that of one successful attempt. [Complete flight census](results/flight_window.json)

Run `python Director_G/check_window_source_cost.py OUTPUT_DIRECTORY` from the repository root to reproduce both exact budgets and the two published clock scalings. The checker independently enumerates all 65,536 signed words in the 16-tick panel and retains the accepted signed rail counts, including parity zeros, in both panels. [Checker](check_window_source_cost.py) · [Finite budgets and exponents](results/window_source_cost.json)
