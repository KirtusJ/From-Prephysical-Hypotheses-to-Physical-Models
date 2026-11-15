# What the four-step ring measurements distinguish

Director G for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

The original five-site calculation compared a signed Hadamard walk and its fully dephased counterpart. The two settings admit an identical reference history paired with one of two signal histories. All three paths reach the same detector at tick four. A more demanding test is whether the joint readings require signed amplitudes, even if the three isolated path readings and all earlier rail intensities agree. [Original schedules](../Common_clocks_and_relative_gains.md)

## An explicit rival

At each site let $u,v$ be the incoming nonnegative masses on the two rails. With $s=(u+v)/2$ and $m=\min(u,v)$, send $s+m$ to the right and $s-m$ to the left. Apply the same masks as in the signed walk. The rule is homogeneous in space and time, conserves the incoming mass, and has no gain or phase variable. When both inputs are occupied it is nonlinear. For example, an equal amount on each rail sends all the mass right, while a random choice between two single-rail unit inputs sends half the mass right on average. Treating this as a physical process would require an interaction or a failure of ordinary affine mixing. It is a mathematical rival for these records.

| Five-site ring, tick four, read site zero on the left rail | Signed Hadamard walk | Fair dephased walk | Nonnegative nonlinear flow |
|---|---:|---:|---:|
| Each of three paths, isolated in its own run | 1/16 | 1/16 | 1/16 |
| Two paths with matching signs | 1/4 | 1/8 | 1/4 |
| Two paths with opposite signs | 0 | 1/8 | 0 |
| All sites open at every tick | 1/16 | 3/16 | 3/16 |

Each entry is a predicted detector weight per original launch. In the first five preparations, the nonlinear rule also reproduces the signed model's rail intensities at each intermediate tick. With the specified start and five-site ring, enumeration found agreement for every reachable mask prefix through three ticks. Opening all masks at the fourth tick distinguishes this rival.

For a mixture of fully dephased runs and a fraction $\theta$ of signed coherent runs, let $S=p_++p_-$, $D=p_+-p_-$, and $O=p_{\rm open}$. A mixture using the same fraction of nonlinear-flow runs gives identical singleton and two-path readings. The signed family gives $4O-3S=-2D$. The nonlinear family gives $4O-3S=0$. For nonzero $D$ the predictions differ even with one common nonzero detection efficiency, since all the quantities scale together. Setting-dependent loss reintroduces ambiguity. At $\theta=1/2$, for example, constructive and open detected weights $3/32,1/16$ are reproduced by a common efficiency $1/2$ for the signed mixture and efficiencies $1/2,1/3$ for the nonlinear mixture. Fits to a device would require calibrated detection and counts per launch, including losses.

## What a passive path distribution cannot reproduce

For any fixed distribution on complete paths, with masks implemented as passive deletion, each joint-event weight is the sum of its reference and signal weights. Write $p_P,p_N$ for the two isolated signal readings. Then $p_+-p_--p_P+p_N=0$. The signed mixture gives $\theta/4$. Moving each of the four readings by at most $\epsilon$ can change this quantity by at most $4\epsilon$, so $\epsilon\ge\theta/16$. The bound is attained on all five readings by assigning the reference weight $1/16$, the positive signal $(1+\theta)/16$, and the negative signal $(1-\theta)/16$, with the remaining probability on other paths. This excludes passive deletion under fixed path probabilities at smaller error. It leaves broader dynamical and setting-dependent models available. [History additivity in measure-theoretic form](https://arxiv.org/abs/gr-qc/9401003)

## Cross-check on Z's product argument

The even-order case of G10 Theorem 5.69 assumes the one-factor classification, preparation of the requisite two-coset stocks, and compatibility with multiplying occurring stocks. In a single factor the three allowed functions are the count $n$, the sum of squares $D_0=p_0^2+p_1^2$, and $B=p_0p_1$, with $p_0,p_1$ the signed counts in the two cosets. They are linearly independent on actual stocks. The singleton identity, a cancelling pair $E=1+\delta$, and $1+\beta$ give three evaluation rows with nonzero determinant.

Moving $E$ between two factors leaves their product fixed. Applying $E$ to one factor doubles its count and kills its two quadratic readings. Independence then rules out every product term with a count in one factor and a quadratic reading in another. A concrete test of this step takes the symmetric expression $n(P)D_0(Q)+D_0(P)n(Q)$. Starting from $P=1,Q=E$, transferring one additional $E$ from one side to the other yields 0 and 4 for two presentations of the same product. Separate one-factor tests and permutation symmetry would have accepted this expression.

For the surviving pure quadratic terms, expand
$$
\pi(X)\pi(X^{-1})=\prod_i\big[D_{0,i}+B_i(X+X^{-1})\big].
$$
The coefficient of the term at lag $d$ is a linear combination of symmetric products using $j=d,d+2,\ldots$ factors of type $B$, with coefficient one at $j=d$. This triangular relation provides a basis. Padding with the identity singleton preserves the earlier lag coefficients and the pure-count coefficient. The argument applies to a fixed occurring multiplier with coefficients allowed to depend on that multiplier. It supplies a second derivation of this part of 5.69 and retains the geometric assumptions it uses. Exact checks covered 3,905 ordered factor tuples. [Issued theorem](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/13770838651b504726d31455f10a9a206c33db5f/edition/PAPERS/G10_Histories_as_Events_the_Order_of_the_Pair_Rule_First_Order_Weights_an/source/body.tex#L1362-L1382)

Run both scripts in this directory with Python 3.9 or later. Ordinary and optimized Python produced identical outputs. Both models and their comparator are calculated here. The physical research gates retain their open dispositions.

~~~sh
python -I -B check_passive_masks.py
python -I -B check_product_parent.py
~~~
