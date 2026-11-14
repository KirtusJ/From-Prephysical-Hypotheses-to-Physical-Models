# Testing detector orientation at one clock with a cubic phase

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

How far can a two-rail experiment test the squared-amplitude probability if its detector can drift between clocks? At one even tick count, three controls that nearly return the prepared rail to itself bound the tilt of an affine fit. The bound applies to each additional preparation checked at that same clock. It needs neither a quarter-turn generator nor a comparison of frequencies taken at different terminal clocks. The controls still assume a coherent two-mode sphere, a stable response to each prepared point within the panel, two labelled launch rails and calibrated switching. No physical acquisition of this panel is reported.

## The measured inputs

At one terminal well and tick $T$, use coordinates $s=(x,\sqrt3 Y,z)$ for the unit sphere of coherent preparations. Let $F_T(s)$ be the probability of one specified event per original launch. The reference preparations are the north pole $e_z$ and three points at $z=-1/2$ related by $120^\circ$ rotations about $z$. The first bottom point has $(x,Y)=(0,1/2)$. These four noncoplanar points fix a unique real affine interpolant $A(s)=\mu+v\cdot s$ through their event probabilities. The [cubic-phase comparison](Three_phase_rail_probability.md) describes how to check this fit at individual rays.

For clarity, if $s=\sum_i\lambda_i r_i$, $\sum_i\lambda_i=1$, define $K_s=1+\sum_{\lambda_i<0}|\lambda_i|$. On one side prepare $s$ with weight one and each negative reference with weight $|\lambda_i|$. On the other side prepare each positive reference with weight $\lambda_i$. Divide both totals by $K_s$. If the two observed event probabilities differ by at most $\epsilon_s$, then $|F_T(s)-A(s)|\le\delta_s=K_s\epsilon_s$. These are frequencies of specified preparation mixtures, with all attempts counted. Establish the size of each discrepancy from the data with its own uncertainty. All bounds below use true rates or simultaneous confidence bounds on those rates. Testing other rays makes no assumption that this particular comparison succeeds there.

Let the north pole have $F_T(e_z)\ge1-\eta$ and the south pole, prepared on the separate named L rail, have $F_T(-e_z)\le\eta$. North is a reference, so $A(e_z)=F_T(e_z)$ exactly for the underlying probabilities. Test the south mixture to error $\delta_-$. Positivity gives $A(-e_z)\ge-\delta_-$. At a positive latitude $z<1$, prepare three points $s_j=(\rho u_j,z)$, where $\rho=\sqrt{1-z^2}$ and the horizontal unit directions $u_j$ are $120^\circ$ apart. Test those three mixtures, with $\delta_h=\max_j\delta_{s_j}$. Their true probabilities are at most one. Writing $v_\perp$ for the horizontal component yields

$$
\rho\,v_\perp\cdot u_j=A(s_j)-\frac{1+z}{2}A(e_z)-\frac{1-z}{2}A(-e_z)
\le 1+\delta_h-\frac{1+z}{2}(1-\eta)+\frac{1-z}{2}\delta_- .
$$

One of the three $u_j$ lies within $60^\circ$ of a nonzero $v_\perp$. Thus

$$
|v_\perp|\le B_T(z)=\frac{1-z+(1+z)\eta+2\delta_h+(1-z)\delta_-}{\sqrt{1-z^2}}.
$$

For another tested ray $s$ at the same clock let $w=(1+s_z)/2$. Interpolating the two pole errors and using the transverse bound gives

$$
|F_T(s)-w|\le \delta_s+\eta+(1-w)\delta_-+B_T(z)\sqrt{1-s_z^2}.
$$

The geometric coordinate $w$ is the squared R amplitude of the two-mode spinor. This is a quantitative test on finite, named preparations. One can change an untested response at an isolated point, or smoothly in a cap avoiding the finite panel, with no change to these observations. A uniform statement on the entire sphere needs additional evidence. A response that depends separately on control history can also distinguish the preparations used to form an assigned sphere point.

## Explicit returns with one switchable phase

Let the chronological bit $k\in\{0,1\}$ give one two-well tick $U_k=D^kH$ with $D=\operatorname{diag}(1,e^{2\pi i/3})$. The plate $D$ itself has bit word 01. Write $B$ for $HDH$ followed by $D$. Its six bits are 001001. Start at the north pole, apply $B^n$, and append zero, one or two $D$ plates to obtain the three azimuths. Pad the shorter options with $H^2$ so every setting ends at $T=6n+4$. Both launch rails start at the same well. The four reference preparations and both pole checks also end at this $T$. Their exact bit schedules are in the [checker](check_cubic_clock_tilt.py).

Under $B$, rotate first about $x$ by $120^\circ$ and then about $z$ by $120^\circ$. In coordinates $(x,Y,z)$ the first map is $(x,(-Y-z)/2,(3Y-z)/2)$ and the second is $((-x-3Y)/2,(x-Y)/2,z)$. The checker also derives each result tick by tick, using $H:(x,Y,z)\mapsto(z,-Y,x)$. It verifies the reconstruction coefficients, norm, padding and azimuths exactly. The [archive](results/cubic_clock_tilt.json) contains the latitude after every power through 603, including negative latitudes and every nonrecord. This finite scan gives examples; it does not establish optimal synthesis length.

| Power $n$ | Clock $T$ | Bound on $\lvert v_\perp\rvert$ at exact agreement | Bound with $\eta=\epsilon_s=0.001$ |
|---:|---:|---:|---:|
| 2 | 16 | 0.480385 | 0.486950 |
| 12 | 76 | 0.098151 | 0.120208 |
| 19 | 118 | 0.079334 | 0.106233 |
| 31 | 190 | 0.018690 | 0.127267 |
| 143 | 862 | 0.004438 | 0.456715 |
| 603 | 3,622 | 0.000940 | 2.132376 |

All entries round upward and describe hypothetical rate tolerances. At exact agreement $B_T=\sqrt{(1-z)/(1+z)}$. With a fixed error allowance the transverse projection divides by $\rho$, so a closer return can give a weaker bound. In the last row the noisy estimate alone gives no useful accuracy for an equatorial event. The query bound must include $\delta_s$ and the pole error as above. Statistical precision and the stability of long coherent schedules are separate experimental requirements.
