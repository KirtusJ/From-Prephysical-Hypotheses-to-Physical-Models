# When detector resolution erases a classical track

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and computational checks by OpenAI Codex.

A detector exponent can approach one while its reported position differs macroscopically from the ordinary walk. Below, a single spatial walker ordinarily finishes near $-1$ with probability tending to one. A detector scoring the same terminal wells by powers $q_k\to1$ reports nearly half the walkers near $+1$. The construction uses spatially addressed coins and one terminal read. It also gives a criterion for preserving a track on flights where such dilution is impossible. Earlier work bounded the error of a **complete probability profile** through the variance of its log weights. A track needs only a bound on the probability outside its tube. [Calibration and flight profiles](Calibration_and_the_log_weights_of_a_flight.md) · [Ten-setting detector calibration](../candidates/composition_record/return_memory/three_grains.md)

## How many scored cells can share the leakage?

Let $p_i$ be ordinary masses of the cells the detector resolves before reporting. Let $O$ denote cells outside a specified position tube at a given clock, $I$ the remaining cells, and $\epsilon=\sum_O p_i$. For $0<\epsilon<1$, put $r_O=p|_O/\epsilon$ and $r_I=p|_I/(1-\epsilon)$. Raise each cell mass to $q>0$ and normalize. The resulting odds of a report outside are **exactly**

$$
R_q=\left(\frac{\epsilon}{1-\epsilon}\right)^q
       \frac{\sum_{i\in O}r_{O,i}^{q}}{\sum_{i\in I}r_{I,i}^{q}} .
$$

The log of the last factor is $(1-q)[H_q(r_O)-H_q(r_I)]$, where $H_q(r)=\log(\sum_i r_i^q)/(1-q)$ for $q\ne1$. Thus the relevant quantity is the difference between the conditional Rényi entropies on opposite sides of the tube. At $q=1$ the factor is one. Empty or full outside events retain their probability under every positive power. [Rényi, definition of order-$q$ entropy](https://digicoll.lib.berkeley.edu/record/112906)

With at most $d_I,d_O$ occupied cells inside and outside, respectively, the following upper bound is sharp:

$$
R_q\leq\left(\frac{\epsilon}{1-\epsilon}\right)^q
     d_I^{(q-1)_+}\,d_O^{(1-q)_+},\qquad (z)_+=\max(z,0).
$$

For $q>1$ spread the inside mass uniformly over $d_I$ cells and put all outside mass in one. For $q<1$ reverse the roles. These choices realize the bound because the uniform and point distributions extremize the power sum. Binary scoring of the entire tube against its complement has $d_I=d_O=1$. A finer detector must count the cells it actually normalizes, including any labels discarded later.

For example, if $\epsilon<1/2$ and $|q-1|\le h<1$, the powered odds are at most $[\epsilon/(1-\epsilon)]^{1-h}\max(d_I,d_O)^h$. Vanishing of this product gives concentration at that clock uniformly over the stated powers. Along a single-particle, nearest-neighbor line flight of $t$ ticks there are at most $t+1$ occupied sites and at most $2(t+1)$ oriented ports. Exponentially decaying ordinary leakage then beats this polynomial factor for fixed $h<1$. With only $\epsilon\to0$ and no rate, that conclusion can fail.

## Two rails per well have a dimension-independent bound

Let $P$ be the site law after scoring site masses by $q$, and let $Q$ be the reported site law after scoring at most $r$ rails at each occupied site. If $s_{j|x}$ are the ordinary fractions of well $x$ on its rails, then $Q(x)\propto P(x)\sum_j s_{j|x}^q$. The ratio between the largest and smallest such multipliers is at most $K=r^{|q-1|}$. For every reported site event $A$, the ratio of its $Q$-odds to its $P$-odds lies in $[1/K,K]$. It follows that

$$
d_{\rm TV}(P,Q)\le\frac{\sqrt K-1}{\sqrt K+1}
=\tanh\!\left(\frac{|q-1|\log r}{4}\right).
$$

Indeed, if the original odds are $o>0$, the largest increase in event probability is $Ko/(1+Ko)-o/(1+o)$, maximized at $o=1/\sqrt K$. Taking a supremum over events proves the bound. It is attained by putting all conditional rail mass in one rail on one side and splitting equally among $r$ rails on the other, with the appropriate ordinary site masses. For $q>1$ the concentrated rails have the higher multiplier; for $q<1$ it is the equal split. Thus the rail-to-site discrepancy vanishes as $q\to1$ for $r=2$, uniformly in the number of wells. This compares two **powered** outputs. The change from scoring a whole target to scoring its many constituent sites can be much larger.

## A single walk with the wrong macroscopic endpoint

Let $k\ge2$, $m=2^k$ and $M=2^{k^2}$. Start at the origin on one right-moving rail. Use the signed Hadamard $H$, identity $I$ and rail exchange $X$, chosen by a fixed site-and-clock schedule. There is no label register. The branch labels in this description name disjoint spatial locations in the schedule.

1. Use $D=k+k^2$ blocks of lengths $\ell_j=2^{D-j}$, $1\le j\le D$. At the start of each of the first $k$ blocks split each occupied site using $H$. Use $I$ during the remaining ticks of the block, so its children finish at displacements $\pm\ell_j$. The first $k$ decisions give $m$ locations of squared mass $1/m$. Designate the location reached by taking the right branch every time as the outside parent.
2. For $q_k=1+1/k$, split all descendants of the $m-1$ inside parents at the start of each remaining block. At the sole outside descendant continue without splitting. For the separate preparation at $q_k=1-1/k$, split the outside descendants and continue each inside descendant without splitting. An unsplit branch can simply keep its rail. Every complete signed displacement sum has a unique length-$D$ choice of signs: sums at the end of block $j$ are separated by at least $2\ell_j$ and distinct parents at its start by at least $4\ell_j$. No two branches meet during a splitting block after their departure. Each split divides the squared mass by two, even when its incoming rail carries a minus sign.
3. The splitting stage takes $T=2^D-1$ ticks and ends within $[-T,T]$. At each occupied terminal site use $I$ or $X$ to point inside descendants left and outside descendants right. Propagate for $R=T^2$ ticks, the first including that choice of coin. Opposite directions pass through one another on different rails under $I$. Every inside well ends in $[-R-T,-R+T]$, and every outside well in $[R-T,R+T]$. At that clock the two intervals are disjoint and every occupied well has a single occupied rail. The number of wells and prescribed split sites is polynomial in the actual elapsed clock. The clock grows exponentially in $k^2$.

Scale position by $R$. Under ordinary scoring, the outside probability is $1/m$ and the endpoint converges weakly to the point $-1$. Under well or port scoring, the outside-to-inside odds in the two preparations are, respectively,

$$
\frac{M^{q_k-1}}{m-1}=\frac{m}{m-1},
\qquad
\frac{M^{1-q_k}}{m-1}=\frac{m}{m-1}.
$$

The outside probability is $m/(2m-1)$, tending to one half. Both powered endpoint laws converge to $(\delta_{-1}+\delta_{+1})/2$. A single nonordinary exponent per scale suffices. The same layouts apply to complete-mask scoring with only two cells; in that case outside odds are $(m-1)^{-q_k}$ and still tend to zero. These are different measurement resolutions of the same spatial preparations. For $k=2$ the ordinary outside fraction is $1/4$ and the two powered fine-read fractions are both $4/7$. The replay checks every physical tick at $k=2$, all splitting pulses and their disjoint propagation intervals at $k=3,4$, and all six powered fractions with exact rational arithmetic. Run `python -I -B Director_G/check_track_resolution.py` from the repository root. [Signed spatial replay](check_track_resolution.py)

This example uses addressed splitting and free translations. An autonomous walk with a prescribed uniform coin has its own dynamics. In particular, the available scattering and front estimates for the free Hadamard walk can restrict its microscopic distribution. The construction makes no claim that its endpoint law arises under that uniform dynamics. [Classical velocity laws for the uniform walk](Which_probability_powers_preserve_the_classical_velocity_law.md)

## What the ten calibration rates can transfer

In the ten-setting protocol, let $g$ be the terminal resolution and $F_g(q)$ its calibrated nonnegative gap per unit gain. If $L=E[bF_g(q)]$, $B=E[b]>0$, define the calibrated responsive population $d\nu=b\,dP/B$. For $0<h<1$, the certificate gives a positive minimum $v_h$ for the three gaps on $|q-1|\ge h$, including their endpoint limits. The fraction of those exponents under $\nu$ is at most $L/(Bv_h)$. Use confidence limits for finite calibration data. A flight requires evidence that the calibrated mode law applies to that flight and to its actual scored cells. The original-launch fraction additionally needs a gain bound, or direct calibration on the original cohort. In a binary flight report $Y=E[a+bP_{\rm outside}]$, subtraction of the common mean offset and division by $B$ recover the gain-weighted target chance. Arbitrary reporting errors after a many-outcome read require separate control.

For the matched gain-weighted population, add this exceptional fraction to an upper bound for $R_q/(1+R_q)$ on $|q-1|<h$, using the actual cell counts or conditional power sums. This directly bounds outside reports at the specified clock. The two spatial examples above have single powers approaching one and fixed positive gain; their calibration gaps are $O(k^{-2})$ by the double zeros at one. Their fine-read leakage nevertheless stays macroscopic. Even perfect transfer of the mode distribution cannot replace a concentration or resolution bound on the flight.

A track through several clocks requires a law for the **joint records**. If each outside probability is bounded under the actual common sequence of measurements, their sum bounds the probability of leaving at any monitored clock. A refining clock grid requires the sum to vanish, or a separate joint bound. Measurements in distinct single-time experiments can have different back-action. Between monitored clocks an additional propagation bound is needed; at bounded speed the maximum clock spacing controls the missed displacement. The spatial counterexample already fails at its final clock. It does not impute unrecorded trajectories to the splitter.
