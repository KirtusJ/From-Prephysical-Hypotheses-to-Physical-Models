# How much of a fluctuating detector response can one remote record determine?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and verification with OpenAI Codex.

A fixed detector response can be tested by changing a distant part of a walk while observing an untouched well. If the response is redrawn on each launch, two opposing changes can disappear from the average. A preparation with **two equally weighted routes and a third, untouched route** gives a comparison with one sign on *every* launch. With a growing bank of balanced labels it determines the response, up to a per-launch scale, through half the total kinematic mass. Above one half there are smooth fluctuating responses that reproduce *every* ordinary one-shot histogram. The dividing point comes from the number of equally large cells that can coexist in a normalized experiment. [Earlier fixed-response walk](../../Director_G/Local_writes_and_dyadic_site_scores.md) · [A single-pulse test for power-law mixtures](remote_split_read.md)

## The apparatus and its identification assumptions

A **kinematic mass** is the squared norm assigned to an orthogonal cell by the prepared signed walk. Calling it a mass specifies a quantity in the model. Its interpretation as a physical frequency is the question under test. Suppose that, on each heralded launch, a random type supplies one strictly increasing response $f:[0,1]\to[0,\infty)$ with $f(0)=0$. For a normalized finite table $(x_i)$ of terminal masses, that launch assigns probabilities $f(x_i)/\sum_j f(x_j)$. The detector resolves the specified cells before applying this rule. Outcomes are pooled afterwards. Assume the same distribution of types for the preparations and independently randomized remote choices being compared. No persistence of a type between launches is needed. Comparisons of infinitely many preparations below concern that same distribution throughout.

Prepare $N=2^n$ labels from a sharp blank by $n$ balanced coins. Give the two test routes $k$ labels each, and give the remaining $N-2k>0$ labels to a spectator route. A reversible lookup can copy a matched route tag to the near station before separation. At the distant station, a route-controlled lookup writes either one common well label for all $k$ labels of a route or distinct well labels for them. Keep its original labels orthogonal in unobserved memory. The terminal read sums the squared masses of all labels sharing a named well **before** applying $f$ to the joint near-tag and distant-well cells. Unused output addresses stay dark. The spectator is left alone in every setting. This gives a signed-register implementation assuming coherent label preparation, routing, persistent blanks and the stated detector resolution. A source that first samples a single label and sends copies scores a different table on each launch and evades the test. The same caveat applies to hidden early reads.

No actual near rate has been measured here. An implementation would need to count all trials in the same pre-choice ensemble, verify that the remote configuration does not alter the near detector or herald, and record the far cells, losses and their deadlines. The operational hypothesis being tested is invariance of the near marginal across the remote choices. A prior use of spacelike causal conditions to constrain probability assignments and a symmetry-based treatment of quantum probabilities have different assumptions about states and measurements. [Han and Choi](https://arxiv.org/abs/1307.2026) · [Zurek](https://arxiv.org/abs/quant-ph/0211037)

## Three choices with one untouched event

Each equal route has mass $m<1/2$. Write $P,Q$ for any two available partitions of that mass, $A=\sum_{p\in P}f(p)$ and $B=\sum_{q\in Q}f(q)$. The spectator has response weight $C>0$. For a single type its near probability under the remote arrangements $PP,PQ,QQ$ is respectively
$$
 p_{PP}=\frac{C}{2A+C},\qquad p_{PQ}=\frac{C}{A+B+C},\qquad p_{QQ}=\frac{C}{2B+C}.
$$
The observable difference of arm means is the expectation of
$$
 p_{PP}+p_{QQ}-2p_{PQ}
 =\frac{2C(A-B)^2}{(2A+C)(2B+C)(A+B+C)}.
$$
Thus equality of the three observed near rates forces $A=B$ for almost every type. In fact, vanishing of this single contrast suffices. The comparison uses the unchanged spectator without knowing its absolute rate, its response, or the sign of the error on a given launch. Positivity of the spectator matters. When $m=1/2$ its weight is zero and the contrast always vanishes. The [finite Lean certificate](SpectatorRefinement.lean) verifies the cross-multiplied identity and equality condition.

For a finite example take eight labels, two per test route, and four for the spectator. Use one leaf of mass $1/4$ or two leaves of mass $1/8$. Under $f(x)=x^2$ the spectator rates are $2/3,8/11,4/5$, giving a contrast of $2/165$. Under ordinary weighting every rate is $1/2$. At $q=0$ with dark cells kept empty the three rates are $1/3,1/4,1/5$, giving $1/30$. These are model predictions. Free walk realizations of two other comparisons, which use fewer general routing controls under a narrower response class, are given in the [one-split](remote_split_read.md) and [single-tag](two_remote_splitters.md) supplements.

The measured contrast also bounds a normalized weight discrepancy without interpreting a small number as exact equality. Write $j=C/(A+B+C)=p_{PQ}$ and $z=(A-B)/(A+B+C)$. The per-type gap is $2jz^2/(1-z^2)$. For $j_0,\eta>0$, an upper bound $U$ on the population gap implies
$$
\Pr\{j\ge j_0,\ |z|\ge\eta\}\ \le\ \frac{U}{2j_0\eta^2}.
$$
Types with very small spectator probability contribute little. A bound on the *mean* spectator rate alone cannot furnish a positive lower bound for every type. Finite observations require a sampling model and a confidence bound for the three-arm contrast.

## From a finite grid to the sharp cutoff

Take $P$ to contain one leaf of mass $k/N$ and $Q$ to contain $k$ unit leaves of mass $1/N$. Invariance gives
$$
 f(k/N)=k f(1/N)\quad\text{almost surely},\qquad 1\le k<N/2 .
$$
On a finite tested grid this is a statement only at those masses. Over all dyadic grids the needed experiments are countable, so one common set of types of probability one satisfies all the identities. For $N\ge8$, the common point $1/4$ fixes the slope to $c=4f(1/4)>0$ for each such type. Monotonicity between dyadics then gives $f(x)=cx$ for every $0\le x<1/2$ on that same set, without a continuity assumption.

To test the endpoint, use a near binary tag with two blocks of mass $1/2$. In one remote setting split both into quarters. The near rate of either tag is then $1/2$ for every type. In the other setting leave one of the halves intact. Its near rate is $f(1/2)/(f(1/2)+2 f(1/4))$. Monotonicity from below gives $f(1/2)\ge c/2$. The latter rate is at least $1/2$ on each launch. If its measured mean also equals $1/2$, equality holds almost surely and $f(1/2)=c/2$. The telescope across grids and this endpoint comparison require one family of comparable prepared populations. Distinct unconstrained populations on each grid would not yield a claim about a single detector type across the continuum.

## An explicit invisible fluctuation above one half

Choose a smooth nonzero function $h$ supported strictly inside $(1/2,1)$. On each launch choose a fair sign and set $T_\pm(x)=x\pm\epsilon h(x)$. Take $\epsilon$ small enough that both maps remain strictly increasing and inside $(0,1)$ on the support. Outside the support use $f_\pm(x)=x$. Inside it use
$$
 f_\pm(x)=(1-x)\frac{T_\pm(x)}{1-T_\pm(x)} .
$$
These responses are smooth and strictly increasing for sufficiently small $|\epsilon|$, since their derivatives approach 1 uniformly on the compact support. If a table has no perturbed cell, its frequencies are ordinary on every launch. Otherwise it has exactly one perturbed cell of mass $x>1/2$. Its normalized probability is $T_\pm(x)$. Every other cell of mass $y$ has normalized probability $y(1-T_\pm(x))/(1-x)$. Averaging over the sign returns exactly $x$ and $y$ at **every cell in every normalized finite table**. An adaptively chosen sequence of such tables also has the ordinary transcript law if a fresh independent sign is drawn each time. This follows by conditioning on the past at each step. Increasing the preparation bank or repeating the ordinary comparison at different remote settings cannot reveal this particular fluctuation in that regime. The overall scale of $f$ also always cancels.

Different evidence can distinguish this rival. If two separately normalized reads of the same table have the *same* sign and are conditionally independent given it, the probability that both hit the large cell is $x^2+\epsilon^2 h(x)^2$. Independent redraw gives $x^2$. More generally, for a fixed $1/2<x<1$, let the other cells be in the calibrated range and set $p_f=f(x)/(f(x)+c(1-x))$. If two reads share $f$ and are conditionally independent, the observable $E[(X_1-x)(X_2-x)]=E[(p_f-x)^2]$ for the two large-cell indicators. Zero forces $f(x)=cx$ almost surely. A three-tick free walk from a sharp right rail supplies the concrete whole-well mass $x=5/8$. Using this test for a countable dense family followed by monotone squeezing would extend the identification through the open interval $(1/2,1)$. At exactly one the only positive cell always wins and its weight cancels. Demonstrating shared response and conditional independence is a further experimental obligation. Combining two copies into a single globally normalized joint table stays within the one-shot counterexample.

Through half mass the comparisons identify the *individual response functions up to scale* on a common full-measure set of types. Consequently every table with all masses at most one half has ordinary frequencies. A larger untested cell can change the common denominator even for a small cell. The signed kinematics, coherent resolution, spacelike isolation and emergence of classical paths remain open. [Exact Rust replay of the finite examples](check_remote_refinements.rs)
