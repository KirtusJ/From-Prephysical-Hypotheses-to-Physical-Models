# One remote coin split tests a mixture of probability powers

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical derivation and computational assistance by OpenAI Codex.

Can a split at Bob’s station change the distribution at Alice’s station? Alice takes three free walk ticks. Bob takes one tick and changes the coin at just one well. Within a family that raises each terminal joint well mass to a common power and then normalizes, a change of Alice's frequencies has a strictly positive signed contrast for every finite nonordinary positive exponent. Therefore even exponents redrawn for each launch cannot cancel in this contrast. The derivation uses a paired-route preparation, the local walk, and a specified resolution of the terminal read. No measurements of this apparatus are reported. For the earlier distant-clock test, see [joint position weights](position_weight_marginals.md).

## The two remote instruments

Write $0=|+1,R\rangle$ and $1=|-1,L\rangle$ at both stations. The [heralded contact source](heralded_bell.md) has populations $a=1/3$ on $00$ and $b=2/3$ on $11$. In the general calculation take any state supported on those two routes, with $a,b>0$ and $a+b=1$. Alice pools both rails at each well after three homogeneous Hadamard-and-shift ticks. Bob uses the identity at $+1$. At $-1$ he chooses either the identity (baseline) or a Hadamard (split), then applies the shift in both settings. The unsplit right route reaches $+2$. The left route reaches $-2$ in the baseline and reaches the two distinct wells $-2,0$ with equal kinematic masses under the split. Use a line segment large enough to contain all the reached wells before reflection.

The following table uses the general source populations. Divide each entry by 8 to obtain the joint kinematic mass in that well pair. In the split setting replace the left column by two half-columns. Bob’s outcome wells distinguish the two original routes, so these masses depend only on the route populations and are independent of the $00,11$ coherence. The two columns follow from the [three-tick walk matrices](terminal_bell_read.md).

| Alice well $x$ | Bob left route | Bob right route |
|---:|---:|---:|
| $-4$ | $b$ | $0$ |
| $-2$ | $5b$ | $a$ |
| $0$ | $b$ | $a$ |
| $+2$ | $b$ | $5a$ |
| $+4$ | $0$ | $a$ |

Each column sums to eight times its route population. The unused baseline well $0$ at Bob and all zero entries stay dark. Bob records the separate terminal wells. The response powers each **joint well pair**, including the individual output ports of the splitter. Summing over Bob gives the frequencies at Alice. Alice’s instrument, its time, the herald and the accepted trial definition are identical in both arms.

## A contrast with one sign on both sides of exponent one

On each launch a finite exponent $q>0$ gives each joint well mass $m$ weight $m^q$. Divide by the sum of the weights at that setting before averaging over launches. Write $\Delta_x$ for the split-arm Alice rate minus the baseline-arm Alice rate at $x$. Assign Alice score $4$ at $-4$, $-1$ at $-2$ and zero elsewhere. The difference in mean scores between the arms is

$$
S=4\Delta_{-4}-\Delta_{-2}.
$$

Allow the left column to split into any finite set of distinct ports with kinematic fractions $r_j\ge0$, summing to one, common to all Alice wells. At least two fractions must be positive for a genuine split. Define $d=\sum_{j:r_j>0}r_j^q$, $t=(b/a)^q$ and $u=5^q$. After omitting a common factor, the powered column vectors are $t(1,u,1,1,0)$ and $(0,1,1,u,1)$. Bob's split multiplies the first vector by $d$. The baseline normalizer is $(3+u)(t+1)$ and the split normalizer is $(3+u)(dt+1)$. Subtraction gives

$$
C=\Delta_{-4}=\frac{t(d-1)}{(3+u)(dt+1)(t+1)},\qquad
\Delta_{-2}=(u-1)C,\qquad S(q,a,b,r)=(5-u)C .
$$

For $0<q<1$, both $d-1$ and $5-u$ are positive. For $q>1$ both are negative. For $q=1$ both vanish. Hence a zero **population** contrast forces $q=1$ almost surely on the jointly occupied, genuinely split portion of the stated family. This remains true under arbitrary correlations between the source populations, potential splitter fractions and exponent, provided independent remote assignment samples the same joint distribution of these quantities in both arms. The comparison requires no shared latent exponent between two different trials and no calibrated value for either Alice frequency. A directly related protected-record contrast compares old walk words across a future local write. Here the two frequencies belong to a separate station. [Earlier five-tick comparison](../../Director_G/Two_five_tick_records_and_the_probability_power.md)

## An explicit bound for the modeled source and fair splitter

For $b/a=2$ with two equal output ports, $t=2^q$, $d=2^{1-q}$ and $dt=2$. The per-exponent contrast reduces to

$$
s(q)=\frac{(2-2^q)(5-5^q)}{3(1+2^q)(3+5^q)} .
$$

This gives $s(1)=0$ and $s(2)=2/21$. With the convention that power zero counts only occupied cells, $s(0)=1/6$. Under the normalized power law $s(q)\to1/3$ as $q\to\infty$. Each signed factor $(2-2^q)/(1+2^q)$ and $(5-5^q)/(3+5^q)$ strictly decreases through zero at one. Their product strictly decreases up to one and strictly increases thereafter. For $0<\delta\le1$ put $c_\delta=\min\{s(1-\delta),s(1+\delta)\}$. For $\delta>1$ use $c_\delta=s(1+\delta)$. At $\delta=1$ the lower endpoint matters if support counting is admitted. For a distribution $\mu$ on finite nonnegative exponents the population bound is

$$
\mu\{|q-1|\ge\delta\}\le \min\{1,S/c_\delta\}.
$$

For $q>0$ only and $\delta\ge1$, $s(1+\delta)$ alone suffices. Finite data require an upper confidence bound for the difference of the two arm means. Retain all post-herald launches in their assigned arm, including dark-site counts and missed outcomes as separate diagnostics. Outcome-dependent loss generally changes the ideal score. A near-empty source column or a nearly trivial splitter also removes the uniform sensitivity unless its size is controlled.

## Boundaries of the test

* A rule choosing any largest cell can select Alice’s $-2$ well in both arms. For $a=1/3$, $b=2/3$, the baseline largest mass is uniquely there. After the fair split, three equal largest cells remain, two at Alice’s $-2$ and one at $+2$. The normalized power limit weighs them equally, while arbitrary tie-breaking can give $S=0$. A four-port equal split, requiring additional routing, would make $+2$ the unique largest Alice well after the split and give $S=1$ under any such rule.
* One occupied route, an unsplit branch, or splitting and then pooling Bob’s ports **before** powering produces identical Alice rates for all exponents. A detector that first samples the baseline joint outcome and then randomly duplicates Bob's recorded label has the same property. A physical splitter followed by a read of separate wells implements a different order of operations. Evidence of interference between the split ports would require a phase-sensitive read.
* Support only on $00$ and $11$ fixes the two column shapes used in the proof. If instead the source is supported on $01$ and $10$, the columns exchange shapes. For any genuine split the same signed score then has the opposite sign off one, as follows by interchanging $(1,u,1,1,0)$ with $(0,1,1,u,1)$ in the subtraction. A mixture of uncharacterized pairings can cancel. An extra local rail resolution, a hidden partition of the cells, a setting-dependent source or changes of registration also require their own calculation.
* A classical shared-route source can draw one route and send the same label to both stations. Sample Alice's conditional well distribution in the table and Bob's ports conditionally on that route using ordinary probabilities. This gives all the ordinary histograms in both arms. Even a nonordinary conditional response can leave Alice's distribution independent of Bob if each station normalizes within the chosen route. The contrast tests the declared global cell weighting. Identifying source entanglement or a particular mediator needs other settings. [Bell experiment](heralded_bell.md) · [Two remote splitters](two_remote_splitters.md)

The use of remote marginal independence to constrain probability assignments has precedents. Han and Choi study relativistic causal consistency for probability assignments in measurements on composite quantum systems. This finite experiment asks what one pair of local instruments can distinguish within a specified mixture of powers. [Han and Choi (2016)](https://doi.org/10.1038/srep22986)

The [Rust replay](check_remote_refinements.rs) reconstructs the finite walk spectra. The [Lean certificate](RemoteSplitWeights.lean) checks the algebra of the signed comparisons with denominators cleared. The [spectator comparison](spectator_refinements.md) treats fluctuating responses beyond the power family.
