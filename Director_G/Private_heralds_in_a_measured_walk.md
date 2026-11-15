# How a private herald changes the large-scale motion of a measured walk

Two controllers have the same one-block position law on an ordinary Hadamard walk. Holding the first controller's private setting fixed can leave a mixture of diffusion rates visible at arbitrarily long times. A position measurement applied only on one side gives the same hidden setting a measurable velocity. These are predictions for a deliberately monitored walker on a line.

## The four-tick experiment

Start at a known site and sharp rail. In each block apply four Hadamard-and-shift ticks and write the whole position at ticks 1, 3 and 4. The last two locations reveal the incoming rail at the next boundary. The next block's first Hadamard and position write produce a fair direction conditional on either incoming rail. A fresh auxiliary [six-wire herald](../candidates/composition_record/velocity_experiment/a_private_controller_for_the_walk_herald.md) decides whether to make an extra write at tick 2. Generate it independently of the walk before that tick. Count all launches at the same public block clock, including both herald outcomes. The two private modes have success rates $p_0=1/2,p_1=25/146$, stationary weights $55/128,73/128$, mean $s=5/16$ and variance $v=495/18688$. Conditional on the mode sequence, fresh target draws and science samples give independent heralds. Holding the target itself changes that law.

Let $D_j$ be the signed displacement of block $j$. In units of sixteenths the kernels on $(-4,-2,0,2,4)$ are

| Tick-two action | −4 | −2 | 0 | 2 | 4 |
|---|---:|---:|---:|---:|---:|
| Leave the paths coherent | 1 | 6 | 2 | 6 | 1 |
| Write the whole site | 1 | 4 | 6 | 4 | 1 |
| Write membership of the site two places to the right of this block's origin | 1 | 6 | 4 | 4 | 1 |

For the last row, only the positive first step can reach the nominated site at tick 2. On that first-step branch the three remaining steps give masses $(1,1,5,1)/8$ at displacements $(-2,0,2,4)$ without the optional record, and $(1,3,3,1)/8$ with it. The negative first-step branch is untouched. Pool after the physical read. Translation of the probe with the recorded block origin is essential. The two-sided kernels and the regenerative role of the boundary writes were established in [Three position records between coherent flights](Diffusion_from_three_position_records.md).

## Equal mean-square displacement, different diffusion

With the two-sided write conditional displacement moments at mode rate $p$ are $0,5-p,44-4p$ for orders one, two and four. Given the entire exogenous mode path, the increments are independent. They share a common distribution conditional on a permanently held mode, or unconditionally if the modes are independently redrawn. Let the stationary mode remain with probability $\rho$ at each new block and otherwise redraw it independently from the original two weights. Then $\operatorname{Cov}(p_i,p_{i+h})=v\rho^h$. For distinct blocks the return indicators have covariance $v\rho^h/16$, and their squared displacements have covariance $v\rho^h$.

Write $X_n=\sum_{j=1}^nD_j$ and $V=5-s=75/16$. For all persistence rates $E X_n^2=nV$. Expanding the fourth power and conditioning on the modes gives

$$
 E X_n^4=n(44-4s)+3n(n-1)V^2+
          6v\sum_{h=1}^{n-1}(n-h)\rho^h .
$$

Fresh increments give $X_n/\sqrt n\Rightarrow N(0,V)$. With a permanently held mode the limit is the mixture of $N(0,9/2)$ and $N(0,705/146)$ with the two stated weights. A fixed $0<\rho<1$ recovers the single Gaussian in the long-time limit, although finite-lag squared displacements remain correlated. In physical walk ticks the variance growth is $V/4$ per tick, so the conventional diffusion coefficient is $V/8$. This clock excludes any extra laboratory time to prepare the exogenous controller.

## When the lifetime of the mode grows with the observation

Let $n(1-\rho_n)\to\lambda\in[0,\infty)$. On the rescaled block clock let $M_t$ start in the stationary two-point law and redraw from it at independent Poisson times of rate $\lambda$. Some redraws return the same mode and leave its observed path unchanged. The jump rate from mode $i$ to the other mode $j$ is $\lambda\pi_j$. Then, jointly with the mode,

$$
 n^{-1/2}X_{\lfloor nt\rfloor}\Rightarrow
 B_{A(t)},\qquad A(t)=\int_0^t(5-p_{M_u})\,du,
$$

where $B$ is a standard Brownian motion independent of $M$. To see this, geometric waiting times between redraws converge upon division by $n$ to exponential waiting times; when $\lambda=0$ the probability of any refresh in a fixed time interval vanishes. Bounded rates give joint convergence of the integrated discrete variance clocks. Conditional on every mode path, the characteristic function of a centered block at argument $z/\sqrt n$ is $1-z^2(5-p)/(2n)+O_z(n^{-3/2})$, uniformly because $|D|\le4$. Multiplying over disjoint intervals gives the Gaussian conditional characteristic functions and their joint limit with the modes. For tightness, the fourth moment of a sum of $k$ consecutive increments is bounded by $C k^2$ uniformly, using conditional centering, independence and bounded increments. Linear interpolation yields the same uniform fourth-moment bound $C'|t-u|^2$ after scaling (within a single grid interval use the bounded slope). The difference from the step path is at most $4/\sqrt n$.

The clock $A(1)$ has mass $\pi_i\exp[-\lambda(1-\pi_i)]$ at each endpoint $5-p_i$. Reaching an endpoint requires starting in that mode and making no jump to the other mode. Interior jumps almost surely have positive sojourn durations in both modes.

At time one the excess fourth moment over the fresh Gaussian limit is $6v(\lambda-1+e^{-\lambda})/\lambda^2$, with value $3v$ at zero, by the Riemann sum above. If $n(1-\rho_n)\to\infty$, the variance of the empirical mode average over each macroscopic interval is $O(1/[n(1-\rho_n)])$; the clock becomes deterministic. Switching diffusion in continuous time is established mathematics. Here the finite walk specifies the two coefficients and a position-only calibration of their persistence. [Grebenkov on two-state switching diffusion](https://arxiv.org/abs/1903.04783) · [Romanelli et al. on measurement-induced walk diffusion](https://arxiv.org/abs/quant-ph/0403192)

## One-sided measurement gives a velocity signal

With the right-site query, the conditional mean is $-p/4$ and the second moment is $5-p/2$. The unconditional mean velocity is $-s/4$ per block. The centered displacement variance equals

$$
 n(5-s/2-s^2/16)+\frac{v}{8}\sum_{h=1}^{n-1}(n-h)\rho^h .
$$

A permanently held mode therefore gives two limiting velocities $-1/8$ and $-25/584$ per block, with the stated mode weights, even though a fresh controller gives the single velocity $-5/64$. In the finite-rate scaling above, $X_{\lfloor nt\rfloor}/n$ converges to $-\int_0^t p_{M_u}\,du/4$. The centered martingale remainder has expected squared maximum $O(n)$ on a bounded macroscopic interval by the maximal inequality. Reflecting the site query reverses the drift. This ballistic contribution is due to the controller's persistent velocity choice; there is no inference of unmonitored coherent propagation.

Both protocols require an unwrapped walker, or rings large enough that the named sites and recorded displacements have the same meaning. They require actual site queries, ordinary conditional path updates, stable block timing, and an exogenous controller. Losses, timing delays or feedback linked to position can change the estimates. Retain these records on the original-launch denominator. No laboratory measurements enter these predictions. [Exact signed-path and finite-time checks](check_private_mode_transport.py) · [What finite position records can identify about controller memory](How_far_a_herald_record_can_identify_motion.md)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed the walk comparison.
