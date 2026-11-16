# Can one launch state explain four rounds of the optical circle?

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), derivation, figure analysis and exact calculation. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

In the ten-site optical walk of Lorz et al., the experimental intensity bands at rounds **7, 13, 17 and 19** exclude every common localized launch rail state under the ideal homogeneous evolution, even with **two arbitrary fixed detector gains per site** and a freely varying overall scale per round. This holds for pure and mixed preparations. The [earlier calculation](When_the_detector_weights_the_two_rails_differently.md) checked particular launch states. The additional rounds allow a test over the entire state space. Three different three-round subsets admit explicit fits. [Lorz et al., Eq. (13) and Fig. 7(c)](https://doi.org/10.1103/PhysRevResearch.1.033036) · [Authors’ source PNG](https://arxiv.org/html/1809.00591v2/Fig7_asymmetricwalk_circle.png)

## Which properties of the launch can the figure see?

Launch at site 2. Each round applies the balanced coin $(I-iX)/\sqrt2$ and shifts the two rails in opposite directions on the cycle. Write the input density matrix in the R,L basis. Two real coordinates determine all the outgoing **individual rail probabilities** in this model:

$$
z=\rho_{RR}-\rho_{LL},\qquad y=2\operatorname{Im}\rho_{LR},\qquad z^2+y^2\leq 1.
$$

For any terminal rail, let $u,v$ be the complex integer amplitude numerators obtained by starting at R and L, respectively. Their common denominator is $2^{t/2}$. One path family has an even number of rail changes and the other an odd number, so $\operatorname{Re}(u^*v)=0$. Consequently its probability for any launch is

$$
p(z,y)=\frac{|u|^2+|v|^2+(|u|^2-|v|^2)z-2\operatorname{Im}(u^*v)y}{2^{t+1}}.
$$

Real input coherence drops out. Every point of the closed disk is attainable by taking that coherence to be zero. The checker verifies the coefficient sign against a launch proportional to $(1,i)$ and verifies normalization as a function of both coordinates.

## A contradiction that cancels the unknown gains

At site $m$ and round $t$, suppose the displayed intensity obeys
$q_{t,m}=k_t\sum_{r=R,L}g_{m,r}p_{t,m,r}$.
The scale $k_t$ is positive. Both gains are positive, may differ by an arbitrary factor, and are fixed between rounds. The model adds rail intensities. It assumes a fixed spatial launch and no additive background.

Consider two rounds $s,t$. On a small rectangle of possible launch states, choose $b>0$ such that $p_{t,m,r}\geq b p_{s,m,r}$ on both rails. Positive gains preserve this inequality when summing. If the earlier observed band has a positive lower endpoint $L_{s,m}$ and the later band ends at $U_{t,m}$, then

$$
\frac{k_t}{k_s}\leq \frac{U_{t,m}}{bL_{s,m}}.
$$

A different site can bound $k_s/k_t$ by the same reasoning in reverse. If the two upper bounds multiply to less than one, no choice of round scales or fixed gains can fit that rectangle. For example, at the center of the disk, rounds 13 and 17 at sites 9 and 3 give the upper-bound product $6017210452/10246695329$, about 0.587. Near the boundary, a different pair can give the contradiction.

The calculation starts from the four unit squares covering $[-1,1]^2$. It discards a rectangle only if its nearest point to the origin lies strictly outside the disk. For each remaining rectangle, affine probabilities attain their extrema at corners. A zero lower bound supplies no positive ratio from that rail. A rail whose earlier upper probability is zero makes no contribution to the earlier intensity. If the two-way bounds do not exclude a rectangle, the checker splits it into four and repeats, up to the specified depth limit.

| Added RGB tolerance | Boxes entirely outside disk | Boxes excluded by incompatible scales | Smallest box width |
|---:|---:|---:|---:|
| 8 | 13 | 177 | 1/32 |
| 12 | 15 | 238 | 1/32 |

The terminal rectangles cover a total area of exactly four at each tolerance. Thus the result includes the disk boundary and all intermediate states between grid points. At eight levels the largest product used for an exclusion is $13109432/13110669$, strictly below one. That value measures the tightness of one interval calculation. It gives no experimental error estimate. With the tolerance widened to 16, the same test left a box unresolved at width 1/64. The eight-level tolerance also accepts the equal-mixture prediction at all 20 selected cells of the paper's numerical panel. [Exact output and counts by site pair](common_circle_launch_output.json)

## What fewer rounds permit

Each row below has a single physical launch, ten strictly positive site-and-rail gains and one scale per retained round. All 15 occupied-position predictions in each row lie inside the eight-level experimental bands. The total predicted on-circle intensity is at most one in every round. The exact gains and scales are in the linked output.

| Rounds retained | A launch that fits $(z,y)$ |
|---|---:|
| 7, 13, 19 | $(-7/8,3/8)$ |
| 7, 17, 19 | $(3/4,1/2)$ |
| 13, 17, 19 | $(0,1)$ |

These fits establish that removing round 17, 13 or 7, respectively, can erase the contradiction. The three-round combination 7, 13, 17 remains open here. The overall result concerns one preparation shared across rounds. Independently changing the rail state each round, a coherent analyzer that mixes the two output amplitudes, or changes in the walk itself require separate tests.

The rounds were chosen after inspecting the figure. The bands describe uncertainty in reading its colors. A prospective check would fix the four rounds, verify repeatability of the spatial and rail preparation, characterize the two-rail detection response and backgrounds, and retain unnormalized counts and off-circle intensity. The current figure cannot identify the apparatus mechanism or support a statistical rejection without the corresponding uncertainty model. Stage 1 Initial External Grounding and physical identification remain open.

With Pillow and PyMuPDF installed, run `python -I -B Director_G/persistent_walk/check_common_circle_launch.py Fig7_asymmetricwalk_circle.png`. The [checker](check_common_circle_launch.py) verifies the source digest, reads both figure panels, covers the disk with exact rational bounds, and tests the three constructive fits.
