# What repeated counts identify about the probability of a walk record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. OpenAI Codex developed the count analysis, counterexamples and computational checks for this working supplement.

A three-step walk gives a well with squared-amplitude mass $5/8$. A detector can favor that well in half its runs and disfavor it in the other half while giving precisely the ordinary one-launch frequencies. We ask what a bank of fresh launches can establish when the same physical detector response persists across the bank and its readouts may have arbitrary dependence. For one previously specified pair of responses the first separating bank has 483 launches. Even there, a rival differs from the entire ordinary count law by only about $0.00002463$ in total variation. These are population predictions. No bank records have been acquired.

## The measured quantity

Launch at the origin on the right rail of the eight-site ring. Apply the balanced real coin and stream three times, resolve all four occupied wells, and count a hit at the well of mass $m=5/8$. The remaining three masses are each $1/8$. Fix the preparation, resolution, normalization, deadline and treatment of losses before a run. A count per original launch requires either complete readout or an explicit model including missing outcomes. Repeating this terminal experiment requires freshly prepared walks. Repeatedly observing one evolving walk implements a different instrument. [Walk construction and original rival](../../Director_G/Fluctuating_site_scores_and_paired_launches.md)

Let $F$ denote a detector response present before the bank begins. Its hit probability on this fixed setting is $P=p_F$. For $N$ launches write $K$ for the hit count and $H=K/N$. The physical premise used throughout is
$$
E[H\mid F]=P .
$$
It holds if each preassigned slot has the same hit probability conditional on $F$. It also holds if that calibration applies to a uniformly chosen slot of the bank. An apparatus may have arbitrary outcome dependence within the bank. Inferring persistence requires evidence independent of retrospectively labeling a count as a type. Changing $N$ requires comparably prepared populations if bounds at different sizes are applied to one detector law.

## Which latent frequencies can a count law hide?

A probability law for $P$ is compatible with the count law exactly when it is smaller than the law of $H$ in convex order. This means that both have the same mean and $E[\phi(P)]\le E[\phi(H)]$ for every convex function $\phi$ on the unit interval. Necessity follows from conditional Jensen. For sufficiency, the one-dimensional martingale coupling theorem supplies a joint law with $E[H\mid P]=P$. Sample $P$ before the bank, draw its coupled count, then place the hits uniformly among the $N$ slots. Each preassigned slot has the required conditional marginal. This reconstructs any exchangeable binary word law with that histogram, including the ordinary independent word law when the histogram is binomial. An arbitrary observed nonexchangeable ordering can impose additional constraints. The theorem concerns the rates allowed at this one setting. A score function shared across settings must also satisfy their constraints. [Leskelä and Vihola, *Conditional convex orders and measurable martingale couplings*](https://doi.org/10.3150/16-BEJ827)

Taking $\phi(u)=(u-m)^2$ gives an observable upper bound
$$
E[(P-m)^2]\le E[(H-m)^2].
$$
If counts follow the ordinary $\mathrm{Binomial}(N,m)$ law the right side equals $m(1-m)/N$, here $15/(64N)$. A sequence of comparable bank sizes with the same rate law and $E[(H-m)^2]\to0$ forces $P=m$ almost surely. The bound only needs the observed second moment, so overdispersion, rare events and losses that change it cannot be discarded. Finite sampling of banks needs its own uncertainty calculation.

The scalar-score model restricts which rates are physically eligible. Suppose prior refinement tests establish $f(y)=cy$ through $y=1/2$, with a finite strictly increasing score and $c>0$ for each type. Then $P=f(m)/(f(m)+c(1-m))$ lies strictly between $a=4/7$ and 1. Every interior rate at this well admits an increasing extension through $f(m)=c(1-m)P/(1-P)$. Thus the admissible rate laws at this setting are precisely the convex-order family above supported in $(a,1)$. An urn assigning $P=K/N$ can fail this score restriction. [Half-mass calibration](spectator_refinements.md)

For completeness, the largest variance allowed by the *closed* floor $a$ can be computed directly from the count histogram with mean $m>a$. Pool the lowest values of $H$ until their mean is $a$, splitting the last atom if needed. Replace that pool by its mean and keep the rest unchanged. If there are no values below $a$, keep $H$ unchanged. Write $Z$ for the result and $z$ for the highest pooled value. For any admissible rate $P$, its convex call function $E[(P-t)_+]$ equals $m-t$ below $a$ and is bounded above everywhere by the corresponding call function of $H$. On $[a,z]$ it lies below the chord from $(a,m-a)$ to $(z,E[(H-z)_+])$. The call function of $Z$ equals that chord there and attains the other two bounds outside. The integrated call bound proves variance maximality, using $E[P^2]=2\int_0^1 E[(P-t)_+]\,dt$. The pooled law is achievable by conditional averaging. For the open interval, contract $Z$ toward $m$ by an arbitrarily small positive fraction and use the coupling theorem. For ordinary banks of sizes 2, 5 and 8 the resulting variance suprema are $9/448$, $20127/1146880$ and $12619581/939524096$, respectively.

## A sharp exclusion at 483 launches

The continuous increasing example in the earlier study has fair types $S=\pm1$ and heavy-well rates $P=m+Sd$, where $d=(3/8)(3/64)=9/512$. A count law of mean $m$ realizes these rates if and only if
$$
d\le D=\min_t E|H-t|.
$$
Indeed $E[S(H-t)]=d$ at every threshold $t$. For attainment, take any median $t$, assign the mass above it to the plus type and the mass below to the minus type. Split ties until each sign has mass one half. Then $E[S(H-t)]=E|H-t|$. Independently randomizing the sign with a suitable probability reduces that covariance to any requested $d$ between zero and $D$, without changing fairness or the count law. The joint distribution factors as a fair sign chosen first and a count chosen conditional on it. Uniformly choosing the hit positions gives the required per-slot rates. Assign a uniformly random one of the three minor labels to each miss with independent choices to reproduce the ordinary four-well word law whenever the counts are binomial. [Finite Lean proof of the bound and median allocation](HeldCountMedian.lean)

For ordinary counts put $D_N=E|K-k_N|/N$ with $k_N$ any binomial median. For $N\ge2$, deleting a uniformly chosen slot leaves a frequency of conditional mean $H$ and the ordinary $(N-1)$-slot distribution. Jensen at a minimizing threshold for the smaller bank gives $D_N\le D_{N-1}$. Using integer weights $\binom Nk5^k3^{N-k}$ gives the following strict enclosures. [Exact Rust calculation](held_count_check.rs)

| Launches per bank | Median count | $D_N$ |
|---:|---:|---:|
| 482 | 301 | $(0.017590866691,\ 0.017590866692)$ |
| 483 | 302 | $(0.017566584448,\ 0.017566584449)$ |

The specified shift $9/512=0.017578125$ lies between them. At 482 the previous construction reproduces every ordered four-well word probability. At 483 the exact ordinary count law excludes this fair pair for *any* dependence within its held bank. The variance bound alone first excludes it at 759. As a separate arithmetic control, the earlier discontinuous example with $d=3/16$ changes sides between 4 and 5. Its lower rate lies below $4/7$, so it is already incompatible with the strict half-calibrated score class.

## How far apart are the laws at 483?

Write $B$ for the ordinary count law and $Q$ for any count law of the specified fair pair. Both have $E[H]=m$. Fix $t=302/483$. The function $g(h)=|h-t|+(2t-1)h$ has equal endpoint values $t$ and a minimum at $t$. Its range is $2t(1-t)$. The equal means cancel the linear term, so bounded-score duality gives
$$
\operatorname{TV}(Q,B)\ \ge\ \eta
=\frac{9/512-D_{483}}{2t(1-t)} .
$$
Equality is attainable. From $B$ remove mass $\eta$ at the median and add $(1-t)\eta$ at count zero and $t\eta$ at count 483. This preserves the mean. The original median has mass greater than $0.0374$, and the resulting lower and upper tails are each below $0.485$. It remains a median, so the new mean absolute deviation is exactly $9/512$. The fair-sign construction realizes the resulting histogram. Uniform hit positions lift the same distance to the full word laws because both models then have identical conditional word distributions given the count.

The [exact checker](held_count_check.rs) encloses the sharp distance in $(0.000024626647717,0.000024626647718)$. Small changes in both extreme tails are enough to realize it. A bank size of 483 specifies the number of launches per bank. It gives no sample-size or significance guarantee for the number of independently repeated banks. A practical comparison can fix this threshold and score before data collection, estimate its bank mean with uncertainty appropriate to the sampling design, and retain the original extreme counts. A different walk-controlled test splits the dominant cell by changing one remote pulse and averages the squared difference between the two arms’ near-tag frequencies within each block. Its bound uses measured records without presupposing an ordinary binomial count law. [Remote split and measurement assumptions](held_split_comparison.md)

## From one well to a whole record

In any finite scalar-score table with one cell of mass $m>1/2$ and exact half-mass calibration, the other cells keep their relative proportions for each type. If the heavy-cell rate is $P$, a minor cell of mass $y$ has rate $y(1-P)/(1-m)$. Therefore the total variation between the *entire* type-specific table and its kinematic table is exactly $|P-m|$ for $m<1$. Sharp tables and tables with no cell above half have zero discrepancy. The estimate on $E[(H-m)^2]$ consequently bounds the mean whole-table distance by its square root, regardless of the number of minor cells.

This gives a conditional transfer to classical record bins. For a sequence of specified finite joint record tables, measure or bound the discrepancy for each table's dominant cell. If these bounds tend to zero and the kinematic record laws converge on the classical observables in question, their measured laws have the same limit on those observables. Deterministic binning of *recorded* words can only reduce total variation. One-time position marginals do not furnish a joint path law, and actively measuring an intermediate position can change the dynamics. Transfer requires a defined record instrument, the stated calibration across its tables and a separate kinematic convergence proof. Mean convergence over types alone gives no almost-sure convergence along the whole sequence for individual detectors. For a localized walker between reflecting walls, final-position refinement makes all resolved trajectory words light enough to recover the classical trajectory law without a held detector. [Terminal refinements and the three-clock test](refined_reflecting_histories.md)

For any fixed finite bank deadline, a pair with a sufficiently small nonzero amplitude can still match every ordinary adaptive transcript. The proof constructs a joint stream before the first setting and preserves each type's response on preassigned slots. Conditioning also on the observed past is a stronger physical requirement. A tag that independently establishes a persisting response, or a walk operation that forces the stronger condition, remains an open experimental obligation. [Finite adaptive counterexample](adaptive_held_response.md)
