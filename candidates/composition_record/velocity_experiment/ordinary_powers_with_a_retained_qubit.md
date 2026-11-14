# Ordinary probability from a walk with an unread rail state

A twelve-tick walk on sixteen sites records its position while retaining a qubit. Its eight possible displacements have ordinary probabilities

\[
 (58,10,2,10,26,10,2,10)/128
\]

in spatial order \(d=0,2,4,6,8,10,12,14\bmod16\). These probabilities are the same for every incoming qubit. An observer can use position records alone to test whether the detector instead raises the site masses to a power, even if the power and the rail state change together after every write.

## How to produce the record

Start at a known well. Apply the same rail coin at every site, then move the R rail one well clockwise and L one well counterclockwise. In each block use **H H H I I H I H H I I H**. Write the exact site only after the twelfth tick. \(H\) is the real Hadamard and \(I\) the identity. Repeat on the same walker as desired. The address at each write locates the beginning of the next block. There are seven global Hadamards per block. Replacing all of them by their negatives only multiplies the block by a global sign. No controlled bypass or independently supplied relative phase is needed.

For a displacement \(d\), let \(T_d\) be the two-by-two matrix of signed path sums between the input and output rails. Every matrix satisfies \(T_d^\dagger T_d=p_d I\), with the eight values above. Thus \(\operatorname{tr}(T_d\rho T_d^\dagger)=p_d\) for a pure, mixed or entangled localized input (use the reduced state on the rail for an idle reference system). The result concerns a ring: clockwise and counterclockwise paths which wind differently can recombine. On an unwrapped line the extreme path traveling right on every tick gives a nonzero rank-one site effect. The same full table does not transfer to that geometry. [Signed paths and circuit export](check_scalar_walk.py) · [Position measurements as effects on a coin](https://arxiv.org/abs/1208.1800)

The [Lean 4.19 calculation](../../../Director_G/lean/ScalarPositionBlock.lean) checks the Gram matrices, zeros and normalization. The [classical position chain and retained qubit](classical_positions_with_a_retained_qubit.md) give the individual matrices, their conditional action and a contrasting experiment that records the site on every tick. Those extra measurements change the final position law by \(13/32\) in total variation.

## One score for all reached histories

Let \(p_w\) be the kinematic mass of a displacement with numerator \(w\in\{2,10,26,58\}\) above. The multiplicities of these four values are 2, 4, 1 and 1. The competing local reader draws \(q\) before the outcome and assigns probability \(w^q/Z(q)\) to each such site, where

\[
 Z(q)=2\cdot2^q+4\cdot10^q+26^q+58^q .
\]

The state left after a site write may depend on the site, hidden type, past outcomes and the prior powers. It need only be a normalized rail state localized at the reported starting well before the next specified free block. Hidden choices must preserve this conditional outcome rule; arbitrary outcome-dependent losses or individual exponents for different potential outputs change it. The detector scores whole sites with both rails pooled. Odd displacements are structurally unreachable. Zero and negative powers here act on the eight positive cells.

Put \(\theta=\log5/\log29\), so \(10=2^{1-\theta}58^\theta\). Assign each reported site a score as follows.

| \(w\) | 2 | 10 | 26 | 58 |
| --- | ---: | ---: | ---: | ---: |
| Score \(s(w)\) | \(32(1-\theta)\) | \(-128/40\) | 0 | \(128\theta/58\) |

The ordinary mean score is zero. For a finite power its mean is

\[
 G(q)=128\frac{(1-\theta)2^{q-1}+\theta58^{q-1}-10^{q-1}}{Z(q)}.
\]

Weighted arithmetic–geometric mean gives strict positivity unless \(q=1\), for every real \(q\). An extreme maximum selector scores \(128\theta/58>0\); either choice at the minimum scores \(32(1-\theta)>0\). The multiplicities in the score are essential: together the two minima contribute the intended coefficient. An unknown mixture of these responses has zero expected score only if its exponent equals one almost surely. A single measured sample mean cannot force exact equality.

For a **whole-word reader**, the ordinary mass of a finite displacement history \((d_1,\ldots,d_J)\) is exactly \(\prod_i p_{d_i}\), even when the hidden rail state changes with earlier outcomes. Raising this product once to \(Q\) and normalizing gives \(\prod_i (p_{d_i}^Q/\sum_{d}p_d^Q)\). A finite whole-word power is therefore indistinguishable from the sequential reader using that fixed power. At an infinite power any extremal word takes an extremal displacement at every block, including correlated tie choices. As a result, at **every clock** the same score tests both whole-word and past-dependent sequential powers in an arbitrary mixture. There is no need to fit the incoming coin or estimate a future continuation correction. [Earlier full-tree test with calibrated branch states](test_each_write.md)

For original-launch fraction \(f_j(h)\) with a power at least \(h>0\) away from one at write \(j\), the quantitative claim is \(f_j(h)\le E[s_j]/v_h\) for any certified lower bound \(v_h>0\) for \(G(q)\) over that range, including the two extrema. A margin used by the analyzer is obtained without a grid search. For \(t=q-1\), the denominator satisfies \(Z(q)\le128\cdot58^t\) if \(t\ge0\), and \(Z(q)\le128\cdot2^t\) if \(t\le0\). These follow by summing \(w\,w^t\) over the eight sites. Therefore for \(h>0\) take

\[
v_h=\min\{\theta+(1-\theta)29^{-h}-(5/29)^h,\ \
                  1-\theta+\theta29^{-h}-5^{-h}\}.
\]

On each side the bounding function increases with distance from one. For example on the positive side its derivative is \(\log(29/5)[(5/29)^h-29^{-h}]>0\), using the defining logarithmic identity for \(\theta\). On the negative side it is \(\log(5)[5^{-h}-29^{-h}]>0\). Both are zero at \(h=0\). At \(h=1/2\) the smaller bound is approximately 0.15967. Finite error is consequently amplified for powers close to one.

The [count analyzer](analyze_scalar_records.py) works from original launch counts and stored addresses. It brackets losses, retains every displacement class, and reports simultaneous per-clock uncertainty under independent launches. The within-launch dependence of scores is unrestricted. If an upper limit for the score is below zero, the combined response and measurement assumptions are challenged at that confidence level. The bound above concerns the fraction of decisions made on the actual launches. Identifying a fraction among visitors to a rare prefix would also require adequate observations of those visits. [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)

## What the experiment selects

Under the specified alternatives, exact zero for the population scores selects ordinary probabilities at all actual writes. The resulting full sequence of position records is a classical translation-invariant Markov chain on the eight reachable positions. Its increments are independent although, under the ideal coherent site write, a recoverable qubit can remain entangled with a reference throughout. An apparatus that resets the qubit can produce the same position chain. A conditional rail read discriminates those two mechanisms.

Every finite probability in this synchronized position experiment is rational. It tests *how the kinematic masses become recorded frequencies*. It cannot distinguish field embeddings that give those same masses. The [addressed-coin experiment](selecting_the_real_embedding.md) addresses that additional question with a calibrated relative phase. Deriving the signed linear transport, localization, and physical record mechanism from common prephysical primitives remains open. These are prospective circuit predictions.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility for the program. OpenAI Codex developed the construction, comparisons and checks.
