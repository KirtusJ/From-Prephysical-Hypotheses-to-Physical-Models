# When a position histogram identifies its probability power

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) with independent derivations by Codex workers.

On the [six-well reciprocal ring](A_reciprocal_sheet_connection_on_six_wells.md), recording the final well and sheet can select ordinary weighting. Recording the well alone at the same tick admits an exact alternative in which every detector uses exponent zero. The result below characterizes this loss of information for *any* finite terminal histogram under a specified family of readouts.

## The readout family and criterion

Fix one preparation, evolution, terminal measurement basis and deterministic map from orthogonal terminal modes to reported bins. Give each occupied mode its positive squared amplitude, treated here as a **kinematic** mass, and denote each bin total by \(m_x\). A *pure bin* here means a reported bin with exactly one occupied mode. Several pure bins of the same mass supply only one distinct mass. A pure quantum state can occupy many modes of a bin.

Each launch chooses a common finite exponent \(q\ge0\) and independently partitionable sets of modes within the bins. Any partition is allowed at each bin, and the choices and exponent can be arbitrarily correlated across the population. Pool the masses within each partition cell \(C\), apply \(m_C^q\), normalize by the sum \(Z\) over all bins, then return the cell's reported bin. Empty cells stay dark even at \(q=0\). This is one terminal operation. The ordinary histogram \(p_x=m_x/\sum_y m_y\) is independent of the partition at \(q=1\). The calibrated observable is the full population histogram on the original exposure.

**Theorem.** The ordinary histogram forces \(q=1\) almost surely among these mixtures if and only if the histogram has at least **three distinct positive masses among its pure bins**. Sufficiency also holds when a maximal-cell rule can place any distribution on tied maximal cells. If there are fewer than three distinct pure masses, a finite mixture of finite nonordinary exponents reproduces the entire ordinary histogram exactly. The exponents can all be confined to any prescribed punctured neighborhood of one.

### Three masses suffice

Let the three masses be \(a<b<c\), with bin probabilities \(P_a,P_b,P_c\) referring to these individual bins. Set \(\lambda=\log(c/b)/\log(c/a)\), so \(a^\lambda c^{1-\lambda}=b\). The expectation
\[
S=\lambda P_a/a-P_b/b+(1-\lambda)P_c/c
\]
has numerator \(\lambda a^{q-1}+(1-\lambda)c^{q-1}-b^{q-1}\). The weighted arithmetic–geometric mean inequality makes this nonnegative and gives equality only for \(q=1\). All unscored bins still enter the normalizer. At maximal-cell readout neither \(a\) nor \(b\) can win, since \(c\) is an unsplittable larger cell. Thus \(S\ge0\), even when there are ties elsewhere. If the measured histogram is ordinary, \(S=0\) leaves only ordinary types and possibly maximal-cell types with zero score. For the latter \(P_a=0\); for the former \(P_a=a/\sum m_y>0\). The observed ordinary value of \(P_a\) eliminates the latter ambiguity. No uniquely largest cell or persisting exponent across launches is required.

### Why fewer than three cannot work

Restrict first to finite powers in any two-sided punctured neighborhood of one contained in \([0,\infty)\). Let \(C\) be the convex hull of the resulting histograms and \(K=\overline C\). Then \(p\in K\) by continuity. Work relative to the affine hull, so that a linear identity shared by every histogram cannot be mistaken for a separating observation. If \(p\) lay on its relative boundary in \(K\), there would be a linear functional supporting \(K\) there whose restriction to the affine hull is nonconstant. Center its coefficients \(h_x\) by subtracting their ordinary mean, and orient it to be nonnegative on \(K\). Then \(\sum_x h_xm_x=0\).

For any fixed admissible partition \(\pi\), the **unnormalized** expectation
\[
F_\pi(q)=\sum_x h_x\sum_{C\in\pi(x)}m_C^q
\]
is nonnegative near one, takes value zero there, and therefore satisfies \(F_\pi'(1)=0\). Compare two partitions differing only within one mixed bin \(x\). Pool that bin in one partition and split it into two positive cells \(u,v\) in the other. Subtracting the derivative equations gives
\[
h_x\{(u+v)\log(u+v)-u\log u-v\log v\}=0.
\]
The bracket is strictly positive. Thus every mixed bin has \(h_x=0\). Dark bins have probability zero throughout.

For each distinct pure mass \(m\), put \(A_m=m\sum_{x\,{\rm pure}:m_x=m}h_x\). The remaining conditions are \(\sum_m A_m=0\) and \(\sum_m A_m\log m=0\). With at most two distinct masses they force every \(A_m=0\), since distinct positive masses have distinct logarithms. The functional then vanishes on *every* powered histogram, as its numerator is \(\sum_m A_m m^{q-1}\). This contradicts a nonconstant supporting functional on the affine hull. Hence \(p\) belongs to the relative interior of \(K\). A finite-dimensional convex set and its closure have the same relative interior, so \(p\in C\). Membership in the convex hull gives an actual finite mixture; with \(n\) occupied bins at most \(n\) types suffice by Carathéodory's theorem. This includes a zero-dimensional hull, where a single nonordinary histogram already equals \(p\). [K. C. Border, finite-dimensional support and relative-interior theorems](https://kcborder.caltech.edu/Courses/Notes/SeparatingHyperplane.pdf)

The proof uses free *single-bin* partition changes and powers on both sides of one. If the entire detector must share one resolution, or if only powers above one are admitted, these derivative constraints need not hold. The [seven-tick free-walk score](Seven_free_ticks_and_one_position_read.md) illustrates the difference between a single detector-wide resolution and a separate resolution at each well.

## What is lost on the six-well ring

At tick eleven, the three occupied base wells \(1,3,5\) have ordinary mass numerators \((729,558,761)\) out of 2,048. Each has three occupied modes when the rails and sheets underlying the base read are taken together. At \(q=0\), pool two wells and split the third into two nonempty cells. Each of the four positive cells then weighs one. The split well occurs with probability \(1/2\) and each other well with \(1/4\).

| Selected split well | Share of launches | Conditional probabilities at wells 1, 3, 5 |
|---|---:|---|
| 1 | \(217/512\) | \(1/2,\ 1/4,\ 1/4\) |
| 3 | \(46/512\) | \(1/4,\ 1/2,\ 1/4\) |
| 5 | \(249/512\) | \(1/4,\ 1/4,\ 1/2\) |

These three populations reproduce \((729,558,761)/2048\) exactly. Indeed, on three occupied wells admitting such splits, the construction reaches every histogram whose entries are at least \(1/4\): choose the well \(x\) with weight \(4p_x-1\). If \(p_x=1/4\), that particular well never needs to be split. The counterexample also survives independent repetition on identical launches when the choices are redrawn independently.

Adding a final sheet bit at a subset of these occupied wells creates one pure bin per addressed well, of respective masses 576, 225 and 81. Thus reading it at any two wells still permits a finite false mixture; reading it at all three meets the theorem. This counts the wells on which the read must distinguish the two sheets. One shared output bit alongside the well label can do so. As a check on the extent of the obstruction, a full finite scan over base circumferences 3 through 90 and ticks 1 through 120 found no base-only histogram with three distinct pure masses for the reciprocal double cover, sharp right-going launch and balanced coin. The [archive](results/pure_mass_criterion.json) retains all 10,560 settings. This scan does not establish an all-time obstruction on every ring.

## The full set of histograms at one fixed exponent

There is a sharper diagnostic when the exponent is the same on **every** launch but the detector resolution varies. Write \(a_{xi}>0\) for the occupied mode masses in bin \(x\), \(m_x=\sum_i a_{xi}\), and define
\[
L_x(q)=\min\{m_x^q,\ \sum_i a_{xi}^q\},\qquad
U_x(q)=\max\{m_x^q,\ \sum_i a_{xi}^q\}.
\]
For any prescribed histogram \(p'\) strictly positive on the occupied bins, the attainable set is specified exactly by
\[
\max_x L_x(q)/p'_x\ \le\ \min_x U_x(q)/p'_x. \tag{1}
\]
A distribution with positive mass in a dark bin fails; a distribution with a zero at an occupied bin also fails for finite \(q\).

To see this, write \(B=\prod_x[L_x,U_x]\) for the box of unnormalized weights and \(N(w)=w/\sum_x w_x\). Convexity or concavity of \(z^q\) puts every partition vector inside \(B\), with full pooling and full splitting attaining the two endpoints independently in each bin. At \(q=0\) the endpoints are one and the number of occupied modes. Thus every vertex of \(B\) is available. Normalization sends a line segment to the segment between its normalized endpoints. More explicitly, if \(w=\sum_j t_jv_j\) is a convex combination of vertices, \(N(w)\) mixes their normalized histograms with launch weights \(t_j\sum_x v_{jx}/\sum_x w_x\). Conversely any mixture of normalized partitions lies in \(N(B)\), by reweighting the unnormalized vectors inversely by their totals. So a common scalar multiple of \(p'\) must lie in \(B\), which gives (1). The proof includes variation of the normalizer with each launch; averaging raw weights with the launch frequencies could give a different result.

For the ordinary histogram let \(m_*=\min_x m_x\) over occupied bins and define the weighted power mean
\[
M_s(x)=\left[\sum_i(a_{xi}/m_x)a_{xi}^{\,s}\right]^{1/s},
\qquad M_0(x)=\exp\!\left(\sum_i(a_{xi}/m_x)\log a_{xi}\right).
\]
For finite \(q\ne1\), the ordinary histogram is attainable **exactly when**
\[
\max_x M_{q-1}(x)\ \le\ m_* . \tag{2}
\]
For \(q>1\), division by \(m_x\) in (1) gives \(\max_x\sum_i a_{xi}^q/m_x\le\min_y m_y^{q-1}\). For \(q<1\) the inequalities reverse before taking the negative power \(1/(q-1)\), yielding the same criterion. In particular \(M_{-1}(x)=m_x/n_x\) for \(n_x\) occupied modes, which tests zero power. Weighted power means are nondecreasing in \(s\), strictly so at a bin containing unequal masses. This follows from Jensen's inequality applied to the change of power or, across zero, to the convex function \(s\mapsto\log\sum_i(a_{xi}/m_x)e^{s\log a_{xi}}\), which vanishes at zero. Thus finite exponents obeying (2) form an initial interval, possibly empty, a singleton or unbounded. The ordinary exponent always passes directly, including when (2) fails at \(s=0\). This fixed-exponent result is compatible with the earlier necessity theorem: a mixture using *different* powers can pass outside the single-power set.

For the six-well base read the positive mode masses at wells \(1,3,5\) are \((144,9,576),(225,324,9),(4,676,81)\) and \(m_*=558\). All finite powers from \(0\) to one common upper endpoint \(q_*\) can reproduce the ordinary histogram by varying only resolution. The endpoint lies in
\[
1.2675150158 < q_* < 1.2675150159 .
\]
It is the nonordinary root of \(4^q+676^q+81^q=761\cdot558^{q-1}\). At the lower bracket all three surplus expressions \(\sum_i a_{xi}^q-m_x558^{q-1}\) are negative; at the upper bracket only the third is positive. Monotonicity of the means then gives the full interval, including its endpoint. At \(q=2\), the third split numerator is 463553, larger than \(761\cdot558\), so even the most favorable resolution mixture cannot match the ordinary histogram. These are compatibility calculations on exact model probabilities. Inferring a limit for an apparatus requires its measured histogram and uncertainty.

Two controls illustrate (2). At exponent one half, the site weights \(m_x/23\) are inside all three intervals: each exceeds its pooled square root and is at most the corresponding fully split weight 39, 36 or 37. Normalizing that box point gives the full ordinary histogram. For a different instrument with just two bins of internal masses (4,4) and (1,1), the smallest total is 2 and the first bin has every power mean equal to 4. Only the ordinary exponent passes. Thus an interval of invisible nonordinary exponents is an apparatus-specific result.

The [fixed-power checker](check_fixed_power_resolution.py) constructs a rational mixture of normalized vertices at zero power, reuses the recorded physical spectrum, and brackets the endpoint using outward enclosures for logarithms and exponentials in decimal arithmetic. The [output](results/fixed_power_resolution.json) retains all three site inequalities on both sides. [Decimal logarithm and exponential rounding](https://docs.python.org/3/library/decimal.html#decimal.Decimal.exp)

## Counting, other detectors and physical identification

Fair counting of microscopic words is an additional model. If its \(S\) is positive, the preceding argument excludes it along with the finite nonordinary powers. A dark bin with positive counted frequency supplies another test. In general the count histogram must be checked directly. The three masses alone classify mixtures of powers. The six-well joint-read paper checks the actual 2,048 word counts. The theorem diagnoses a single setting; multiple settings can constrain a shared population if their readout models justify that extra relation.

The criterion concerns terminals with fixed, known mode masses, known reported bins and lossless or independently corrected frequencies. If the masses or bin assignments depend on uncontrolled preparation, different ordinary comparison laws can enter the same mixture. No phase, dynamical law, physical detector, or absolute cyclotomic embedding is derived from these finite statistics. The [checker](check_pure_mass_criterion.py) uses both physical seam-crossing paths and an independent cover recurrence. The [Lean check](lean/PureMassControls.lean) verifies the integer countermixture and the elimination identity used for two mass classes. The convex-geometric argument above treats arbitrary real masses.
