# A fixed reciprocal sheet connection selects the terminal probability power on a ring

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Six wells, a two-state sheet and one fixed link suffice for a conditional probability test. A traveler crossing the link switches sheets in either direction. Launch a right-going walker on sheet zero, apply eleven uniform real Hadamard steps and read the well and sheet together. Two statistics of that single histogram distinguish ordinary probabilities from a mixture that redraws its power and its choice of rail resolution on each launch. The ordinary model sits at a positive distance from populations with a prescribed positive fraction of types a fixed distance from ordinary. The histogram has not been measured. [Earlier construction with two timed sheet swaps](Five_ticks_from_a_localized_sheet.md) · [Coined walks on cycles, Aharonov et al.](https://arxiv.org/abs/quant-ph/0012090)

## The connection and the recorded coordinates

Label wells \(x=0,\ldots,5\) and sheets \(s=0,1\). Every tick applies \(H(r,l)=(r+l,r-l)/\sqrt2\), then shifts the two outputs one well right and left. On the undirected edge \(\{5,0\}\) replace \(s\) by \(1-s\) on **each** crossing. All other transports are the identity. Traversing an edge and immediately retracing it restores the sheet. Parallel transport once around the base exchanges the two sheets, so its monodromy is the nonidentity permutation of two elements. In the joint coordinate \(j=x+6s\bmod12\), the conditional shifts are exactly \(j\mapsto j\pm1\). This identifies the lift with a twelve-cycle and makes the shift reversible. The inverse tick undoes the shift and then applies \(H\).

A local relabeling of the sheet at one or more wells moves the apparent seam. On an open chain all edge swaps can be removed that way. On a cycle the product of the transports around the loop is invariant up to relabeling at its base, and here is a swap. The device must maintain coherent transport along the ring and identify which joint output its terminal labels denote relative to the preparation. A permanently recorded crossing would retain extra path information and change interference. This construction stipulates a carrier with this connection. Its double-cover geometry alone fixes no probability rule. [Earlier fixed-ring winding measurements](Fixed_ring_winding_weights.md)

Starting at \((0,0,R)\), the cover amplitudes are signed integers over \(\sqrt{2048}\) at tick eleven. All six even coordinates have zero amplitudes and zero words by parity. The entries below include all other coordinates.

| \(j\) | \((x,s)\) | \(R,L\) | Squared mass numerator | Unsigned words |
|---:|---:|---:|---:|---:|
| 1 | (1,0) | 12, 3 | 153 | 463 |
| 3 | (3,0) | −15, 0 | 225 | 341 |
| 5 | (5,0) | 2, 26 | 680 | 220 |
| 7 | (1,1) | 24, 0 | 576 | 220 |
| 9 | (3,1) | 18, 3 | 333 | 341 |
| 11 | (5,1) | −9, 0 | 81 | 463 |

Removing the sheet swap gives a disconnected pair of six-cycles. Starting on sheet zero then leaves sheet one unoccupied, and the three occupied rail pairs become \((36,3),(3,3),(-7,26)\) at base sites 1, 3, 5. Measuring just the base site in the connected run instead pools the two sheets. For example the reported site 5 receives both the 680 row and the 81 row. These interventions change which histogram is available.

## Two statistics from one histogram

On each launch permit a finite \(q\ge0\) common to all its positive cells. At *each joint coordinate* a detector may pool its two rails before applying \(m\mapsto m^q\), or power each occupied rail separately and report their summed frequency. Normalize all resulting weights on that launch. At zero power every positive cell receives unit weight and dark cells remain dark. Also allow selection of a maximal cell (the infinite-power limit) or fair counting of the 2,048 direction words. Different detector types may be mixed in any proportions. All six reachable outcomes, including the unscored ones, enter each normalization.

Put \(a=81,b=225,c=576\), \(\lambda=\log(c/b)/\log(c/a)\), so \(a^\lambda c^{1-\lambda}=b\). From the probabilities \(P_j\) of the terminal joint outcomes compute
\[
D=\lambda P_{11}/a-P_3/b+(1-\lambda)P_7/c,\qquad H_5=P_5.
\]
Every scored coordinate has just one occupied rail. At finite power the numerator of \(D\), after multiplication by the positive normalizer, is
\[
\lambda a^{q-1}+(1-\lambda)c^{q-1}-b^{q-1}.
\]
Weighted arithmetic–geometric mean gives nonnegativity, with equality exactly at \(q=1\). For fair counting \(2048D=\lambda(463/81)+(1-\lambda)(220/576)-341/225>0\). Indeed \(\lambda>1/3\) follows from \(c^2a>b^3\), and \(463/(3\cdot81)>341/225\).

The unique largest cell is at \(j=5\) in every one of the eight distinct partitions of occupied rails. Its mass is either \(680\) or \(676\), and every other location has cells of mass at most \(576\). Consequently at infinite power \(D=0\) and \(H_5=1\). At the ordinary power \(D=0\) and \(H_5=680/2048=85/256\). If the population mean of \(D\) is zero, positivity confines its types almost surely to ordinary or infinite power. The second observed probability equals \(85/256\) only when the infinite-power fraction also vanishes. Each equality is needed for this argument. For instance, a population consisting entirely of maximal-cell reads passes the first equality.

## Finite deviations and scope

Fix \(0<\delta<\infty\). Give the powers the compact topology of \([0,\infty]\) under \(q\mapsto q/(1+q)\), include the eight possible partitions, and add fair counting as an isolated type. Both \(D\) and \(H_5\) are continuous on this compact space, including at infinity by the unique maximum. Call the closed set \(\{|q-1|\ge\delta\}\), including infinity, together with fair counting, \(B_\delta\). For each \(0<\eta\le1\), the probability measures on types with mass at least \(\eta\) on \(B_\delta\) form a compact set: under weak convergence the mass assigned to a closed set can increase at the limit. The image under the two expectations is compact. It excludes \((0,85/256)\) by the preceding argument. Its Euclidean distance from that pair is therefore positive. For a sequence of matched populations whose two statistics approach their ordinary values, the fraction of fair counts and powers outside each fixed \(\delta\)-neighborhood tends to zero. This compactness argument supplies no numerical sample budget. Arbitrarily small deviations from \(q=1\) still require high precision.

For an explicit diagnostic of the high-power end, there are at most seven occupied cells outside \(j=5\). Hence \(H_5(q)\ge[1+7(576/676)^q]^{-1}\), which is above 0.649 for \(q\ge16\). A population can mix high and low values of \(H_5\). The strict lower bounds on the intermediate powers come from the first statistic. To interpret either statistic in measured data requires a calibrated joint-site-and-sheet instrument, matched preparation, outcome efficiencies or independently bounded losses, and sampling uncertainty on the incident population. Applying an arbitrary per-coordinate exponent, keeping a which-crossing record, or changing the normalization after a loss exceeds the tested family. The finite ring provides a relative transport and a terminal weight test. It supplies no absolute cyclotomic embedding, continuum force, or emergence of the stipulated Hadamard dynamics.

## Reproduction

The [checker](check_reciprocal_ring_score.py) enumerates all 2,048 signed and unsigned words with the reciprocal link. It independently propagates on the cover, checks all eight partitions including the large-power limit, and runs the identity-connection control. Among \(3\le L\le t\le11\) only \((L,t)=(6,11)\) gives three distinct positive masses at coordinates with exactly one occupied rail. This finite scan concerns that particular sufficient construction. A smaller four-well example at tick 9 already gives a zero-amplitude coordinate reached by 136 unsigned words out of 512, which by itself distinguishes path counting from all positive-cell power rules. The [Lean 4.19.0 replay](lean/ReciprocalRingScore.lean) checks all twelve joint rail pairs directly on the physical seam and the integer inequalities for counting. Every trial, including the negative ones, is in the [record](results/reciprocal_ring_score.json). Run `python -B Director_G/check_reciprocal_ring_score.py fresh.json`.
