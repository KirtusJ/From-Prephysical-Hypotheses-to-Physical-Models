# Reading acceleration and impulse from a position record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The prepared walk has two candidate classical positions, $+A(t)$ and $-A(t)$, where $A(t)=\int_0^t(t-s)F(s)\,ds$. Their unordered positions do not say which way a trajectory continues at a meeting. A particle that passes through and one that reverses direction there can give identical position histograms at every time. Four readings of the same position register can distinguish them by the change in slope across the meeting. The size of the time window relative to the position error determines whether this is measurable. Here force means acceleration in the supplied unit-mass clock and distance convention. [Prepared flight and its bin instrument](Sequential_position_records.md) · [A rank-preserving path with identical one-time marginals](Rank_paths_and_classical_flight.md)

## What the position theorem licenses

Use the previous prepared-flight theorem on a fixed interval $[a,T]$ with $A(a)\ne0$, conditional on the same successful release. Its instrument couples a fresh pointer to each uniform position bin and preserves coherence within that bin. Its position readouts are from one launch, and survive later readings. At the nominal sampling times connect the reported bin centers linearly to form $X_\delta$. With probability tending to one there is a sign $s=\pm1$ for which $\|X_\delta-sA\|_\infty\le e_\delta$, where each sign has limiting probability one half. One can assign the sign on these successful words from the first separated bin. The earlier proof gives $e_\delta=O_T(\delta^{1/16})$ on its good words because both the bin width and the reading interval have this order. The actual reads take place at the nearest native ticks. Interpolating on attained times instead adds at most a ray Lipschitz constant times the tick duration to the good-word error, by bounding the error at the displaced knots and interpolating. Use the common interior of the two time grids. The word success statement and its norm bound concern the ideal apparatus and assigned record probabilities. Any measured timing or readout error must also be included in $e_\delta$, and failed preparations remain outside the conditional ensemble.

For any twice continuously differentiable test function $\varphi$ supported inside $(a,T)$, the weak acceleration readout is

$$J_\delta(\varphi)=\int_a^T X_\delta(t)\varphi''(t)\,dt,\qquad
 \left|J_\delta(\varphi)-s\int_a^T F(t)\varphi(t)\,dt\right|
 \le e_\delta\|\varphi''\|_1.$$

This follows by integrating $A''=F$ by parts twice. For a piecewise-linear record there is also an exact discrete implementation: sum the jump of each consecutive secant slope times $\varphi$ at that knot. End terms vanish because of the support condition. Every finite collection of such readouts on a word shares its branch sign. Without assigning or conditioning on a branch, averaging the two opposite signals gives zero. Neither the convergence in probability nor a vanishing probability of bad words by itself controls unbounded moments on those words. Weak-form identification of dynamics from measured trajectories also uses derivatives of test functions. [Messenger and Bortz](https://arxiv.org/abs/2005.04339)

At an interior time $t$ define the centered acceleration
$$D_h^2X(t)=[X(t+h)-2X(t)+X(t-h)]/h^2.$$
For $sA$ this is exactly $s$ times the average of $F(t+u)$ against $(h-|u|)_+/h^2$. The change when substituting the measured record is at most $4e_\delta/h^2$. For finitely many force switches this yields the correct acceleration away from switches, and the symmetric average of the one-sided accelerations at a switch as $h\to0$. The program's bin schedule permits, for example, $h=\delta^{1/48}$, which tends to zero while $e_\delta/h^2\to0$. Reading at neighboring bins alone need not estimate a derivative. For the exact curve $t^2/2$ sampled at $-h,0,h$ with width $h$ centered at zero, all three readings can occupy the same bin although the acceleration is one. Sign, clock, spatial scale and the order of limits are part of the inference.

## A single crossing and two possible continuations

Let $t_*$ be an isolated transverse zero of $A$ with $v=A'(t_*)\ne0$ and a locally constant applied force. Compare the signed trajectory $sA$ to the ordered continuation $s|A|$. As distributions on this interval,

$$(|A|)''=\operatorname{sgn}(A)F+2|v|\,\delta_{t_*}.$$

Integrating on each side of the zero gives the displayed jump term: the left derivative tends to $-|v|$, the right to $+|v|$. The ordered lower track has the opposite jump. A tangency with $v=0$ supplies no nonzero impulse by this argument. This is a difference in the two proposed path laws which survives the equality of every one-time position distribution. It concerns how one recorded particle continues. Interpreting a jump as a microscopic collision would require separate evidence.

A direct finite read subtracts the secant slope on $[t_*-2h,t_*-h]$ from the secant slope on $[t_*+h,t_*+2h]$. For the signed quadratic the result is $3hsF(t_*)$; for the ordered upper or lower quadratic it is exactly $\pm2|v|$ when these intervals lie on the two crossing sides. Four perturbed position readings change either statistic by at most $4e_\delta/h$. This coefficient is attained by position errors $(e,-e,-e,e)$ in temporal order. Use values of the existing interpolated transcript. Inserting additional physical readings changes the experiment. For attained times $a<b<t_*<c<d$ in the same constant-force region, the position error bound is $2e_\delta[(b-a)^{-1}+(d-c)^{-1}]$. With midpoints $m_L,m_R$ the signed result is $sF(m_R-m_L)$ and the ordered result is $s\,\operatorname{sgn}(v)[2v+F(m_R+m_L-2t_*)]$. The latter retains a small timing term on asymmetric grids. If $t_*$ is estimated rather than supplied, its uncertainty must be small relative to $h$ for the four times to bracket the intended sides. In the reversal schedule $F=+1$ up to $\tau$, then $-1$, the noninitial crossing is $(2+\sqrt2)\tau$ and $|v|=\sqrt2\,\tau$. The signed read tends to zero and the ordered read has limiting magnitude $2\sqrt2\,\tau$. For an unknown source track compare the magnitude per launch. Taking the signed ensemble average would cancel the two impulses.

The rank model specifies a *silent* path. A comparison to actual data needs a model of how that path writes these four positions without altering its subsequent law. The established coarse quantum instrument produces the signed words under its own dynamics; this alone cannot falsify an unobserved path in an apparatus that disturbs it. Similarly a fully monitored per-tick walk has another classical limit. [Monitoring and the rank trajectory](Rank_paths_and_classical_flight.md)

## A finite resolution check

We propagated the recorded walk on one supplied unit sheet for orders 127, 509, 2039 and 8191, using the preceding paper's release, physical coordinate and signed Hadamard step. Set $\tau$ to the attained switch tick nearest $0.75$. Read at the nearest ticks to $t_*+(-0.6,-0.3,0.3,0.6)$. For this finite check use fixed bins of width $0.5$ and offset $0.125$. Track the four distinct bin words containing the two signed and two ordered target trajectories. The checker keeps the release yield from a sharp launch within the stipulated unit sheet, all four conditional probabilities, their unconditional products with the release probability, the complementary probability and the values of the slope statistic on both the binned and continuous positions. These fixed bins are illustrative and differ from the refining binnings in the limiting theorem.

| Sheet order | Both signed words | Both ordered words | Other words |
|---:|---:|---:|---:|
| 127 | 0.00321 | 0.000442 | 0.99635 |
| 509 | 0.00605 | 0.00137 | 0.99259 |
| 2039 | 0.00688 | 0.000624 | 0.99250 |
| 8191 | 0.01337 | 0.00116 | 0.98548 |

All table entries are conditional on preparation and are rounded. Even at the largest simulated order almost all words lie outside the four nominated bins. Inferring an observed force by discarding those words would give a selected statistic. The limit theorem supplies convergence for its refining experiment; these finite simulations do not demonstrate a resolved impulse. Absolute units, a physically realized force and the origin of the probability rule and pointer remain open. [Lean check of the symmetric secant identities and four-error bound](lean/CrossingImpulse.lean) · [Checker](check_crossing_force.py) · [Complete conditional and original-launch results](results/crossing_force.json)
