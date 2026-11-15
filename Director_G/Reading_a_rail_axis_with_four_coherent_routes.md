# Reading a rail axis with four coherent routes

A stopped sequence of ordinary fair walk records can [reproduce a three-tick address distribution](A_stopped_walk_reference_for_the_real_embedding.md). Can the rail itself be prepared and read against that reference? Four coherent routes give a measurement of the rail axis $H=(X+Z)/\sqrt2$. Reusing the same apparatus brings its two recorded conditional preparations arbitrarily close to the opposite eigenstates. A final position-label test approaches the two algebraic address tables. An additional controlled gate call measures its phase relative to this prepared rail axis.

These are predictions of ordinary conditional quantum measurement in the synchronized circuit menu. The menu consists of uniform Hadamards, signed permutations, sharp auxiliary bits, coordinate reads and classical feedback. The digital routing and auxiliary memories are additional to a bare two-rail shift. The construction gives a way to compare instruments on a common rail. It assumes the outcome and state-update rule on which the comparison is calculated.

## Four paths on a two-bit selector

Prepare two selector bits in zero, apply a Walsh transform $H\otimes H$, apply $I,X,Z,I$ respectively to the data rail on selector paths $00,01,10,11$, then undo the Walsh and read the two selector bits. The controlled $X$ and $Z$ are signed permutations. Put $S=X+Z$. The four raw Kraus matrices, in the same binary order, are

$$
 (2I+S)/4,\quad (Z-X)/4,\quad (X-Z)/4,\quad (2I-S)/4 .
$$

The middle results each occur with probability $1/8$ on every input, including inputs entangled with a spectator. After either, apply $XHX=(X-Z)/\sqrt2$ on the data rail. This restores its input up to the recorded branch's global sign. Each corrected null is then a scalar identity. Keep its time and outcome and try again. Report $+$ on $00$ and $-$ on $11$. The coarse nonnull probability is $3/4$. The normalized nonnull matrices $K_\pm=(2I\pm S)/\sqrt{12}$ are positive square roots of $(I\pm\eta H)/2$, where $\eta=2\sqrt2/3$. Thus each nonnull sign weakly reads $H$ and preserves its eigenstates. A finer write during route interference would change the calculation. A sign error on the $Z$ path can be tested independently: on sharp $Z+$ versus $Z-$ inputs the raw $00$ rate should have contrast $+1/2$. Reversing that path's sign makes this contrast $-1/2$ and leaves the $X+$ versus $X-$ contrast at $+1/2$. A common change to the preparation and analyzer would need an independent calibration. This use of a coherent sum of signed gates follows the linear-combination construction. [Childs and Wiebe](https://arxiv.org/abs/1202.5822)

## A stopped read with a known strength and cost

From zero, count $+1$ or $-1$ on the respective nonnull signs and zero on a corrected null. Stop at either $+m$ or $-m$, with $m\ge1$, and keep the reached sign $\tau$. The matrices commute, and $K_+K_-=I/6$. On each finite history reaching $+m$, the remaining data operator is a scalar times $K_+^m$; at $-m$ it is proportional to $K_-^m$. The terminal probabilities on the opposite $H$ eigenstates follow from the two-barrier random walk. On the positive eigenstate the odds for each nonnull step are $(1+\eta)/(1-\eta)=u^{-2}$ for $u=3-2\sqrt2$. The probability of hitting $+m$ is $1/(1+u^{2m})$. The negative eigenstate reverses the two signs. Therefore the two stopped effects and state updates are

$$
 E_{m,\tau}=(I+\tau\eta_m H)/2,\qquad
 \eta_m=\frac{1-u^{2m}}{1+u^{2m}},\qquad
 \mathcal I_{m,\tau}(\rho)=\sqrt{E_{m,\tau}}\,\rho\,\sqrt{E_{m,\tau}} .
$$

Completeness follows from almost-sure termination. For fixed $m$ there is a positive bound on the probability of exiting in a block of $2m$ raw attempts, uniform over interior scores and inputs, by requiring all plus signs until exit. On an eigenstate the raw signed displacement has mean $\pm1/\sqrt2$. The mean terminal displacement is $\pm m\eta_m$. The stopped-sum identity gives a mean of $\sqrt2\,m\eta_m$ raw selector reads. It is the same for every initial rail density by linearity and diagonality of all history effects. This cost includes null attempts. At a finite deadline, keep uncompleted launches as a separate result. The exact stopped instrument uses a finite threshold and an unbounded number of attempts. For general repeated nondemolition measurements, the connection between repeated indirect records and eigenstate selection is established independently. [Bauer and Bernard](https://doi.org/10.1103/PhysRevA.84.044103)

## A positioned rail preparation for the stopped scalar reference

Start with the mixed rail $I/2$ at one known site, prepared by an independent balanced choice between the two sharp rails. Each stopped tag has probability $1/2$. Its conditional output density is exactly $E_{m,\tau}$. Make one more raw probe. Report code 1 on $00$, code 2 on $11$ or $01$, and code 3 on $10$. Code 0 is dark. This labels a selector outcome as a port; recording those labels as distinct physical positions would require a reversible route to the corresponding sites. The complete positive-tag and negative-tag predictions are

| Threshold and tag | Code 0 | Code 1 | Code 2 | Code 3 |
|---|---:|---:|---:|---:|
| $m=1$, positive | 0 | $17/24$ | $1/6$ | $1/8$ |
| $m=1$, negative | 0 | $1/24$ | $5/6$ | $1/8$ |
| $m=2$, positive | 0 | $99/136$ | $5/34$ | $1/8$ |
| $m=2$, negative | 0 | $3/136$ | $29/34$ | $1/8$ |

For arbitrary $m$ the code-one rate is $3/8+\tau\sqrt2\,\eta_m/4$. The positive tag approaches the ordinary addressed table, whose code-one probability is $(3+2\sqrt2)/8$. The negative tag approaches the conjugated table, with $(3-2\sqrt2)/8$. The total variation error in either panel is $\sqrt2(1-\eta_m)/4$. All these finite-threshold panels have rational entries. Retain the tag and its original-launch denominator. Pooling the two tags gives code-one rate $3/8$ at every threshold and loses the contrast. [Independently generated scalar reference](A_stopped_walk_reference_for_the_real_embedding.md) · [Original coherent addressed experiment](../candidates/composition_record/velocity_experiment/addressed_embedding.md)

## What a separate gate comparison identifies

Suppose a coherent control rail can be prepared independently of the tagged data, and the tested invocation acts as $I\oplus V$ with the idle phase preserved. For the addressed $X\oplus V$ form, remove the known exchange on its even arm with a signed permutation. This requires independent access to the control and target before the invocation. Prepare the control in $|+\rangle$, invoke the gate once, and read the control in the $X$ basis. On tag $\tau$ its $X$ expectation is $\operatorname{Re}\operatorname{tr}(V E_{m,\tau})$. Combining both tags yields the probability that the control sign equals the recorded tag,

$$
 P_\mathrm{agree}=\tfrac12+\tfrac{\eta_m}{4}\operatorname{Re}\operatorname{tr}(VH).
$$

For the fixed implementations $V=+H$ and $V=-H$, the predictions are $(1+\eta_m)/2$ and $(1-\eta_m)/2$. Already at $m=1$ these are approximately $0.9714$ and $0.0286$ per completed launch. An extra propagation phase is part of $V$ here. For general $V$, this reads its real trace overlap with $H$; it does not identify all matrix entries. Via this controlled read the prepared rail does test coherent action. The scalar reference agrees with the named limiting table, but supplies no phase-bearing wire. A simultaneous algebraic conjugation and compensating physical sign change in the addressed operation still gives identical records.

The [exact checker](check_weak_rail_reference.py) reconstructs the four routed matrices and solves the finite renewal system on all four input matrix units at $m=1,2,3,4$. It compares both complete stopped superoperators and the mean attempt counts. A [separate gate-by-gate replay](check_four_route_gates.py) builds the Walsh and controlled signed permutations on all eight basis coordinates. Without the null correction the three-read word $00,01,00$ from the mixed input changes from $17/512$ to $1/512$. With a three-attempt tag deadline the unresolved fractions are $1/64$ for $m=1$ and $13/64$ for $m=2$. A [seeded Aer simulation](results/weak_rail_aer.json) retains all 256 four-read words and all 32,768 simulated shots. Its total variation from the exact word probabilities is $813/32768$. No laboratory counts enter the result. The [range of strengths with an exact square-root update](Which_rail_measurements_preserve_the_square_root_update.md) follows from the fine branch support.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed and independently checked the four-route instrument, stopped preparations and comparisons.
