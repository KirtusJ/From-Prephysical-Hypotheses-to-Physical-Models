# Cross-review of three statements in G10

Director G for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Source reviewed was the issued Z32 branch at commit 13770838651b504726d31455f10a9a206c33db5f. The review concerns mathematical conclusions under the stated walk, mask and readout hypotheses. The three delegated readings share a model family with G and are outside the manuscript author's Claude model family. [Issued G10 subsection](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/13770838651b504726d31455f10a9a206c33db5f/edition/PAPERS/G10_Histories_as_Events_the_Order_of_the_Pair_Rule_First_Order_Weights_an/source/body.tex#L1290-L1398)

## Theorem 5.64 · FOLLOWS

For a sharp launch, $T\ge1$, $N\ge3$ and an occupied final site $x$, stop one tick before the final step. Write $M=N/\gcd(N,2)$ and let $l_0$ be the smallest final left-step count at $x$. In the integer deficit cover the sources are $iM$. The consecutive sinks for level $j$ are $l_0-1+jM$ (ends L) and $l_0+jM$ (ends R). Whole-site masks lift to sets periodic in $M$. The order is strict even at $M=2$. Restricting the infinite strip to the finite cone of the selected sources loses no path relevant to the minor.

There is a direct finite-matrix proof. In one tick the deficit stays fixed or increases by one. A nonidentity matching of increasing source indices to increasing distinct target indices cannot contribute a nonzero determinant term, since some two endpoints would have to reverse order. Every one-step minor therefore equals zero or one. Deleting closed vertices preserves this property. Iterated Cauchy–Binet counts choices of ordered disjoint intermediate vertices between the selected sources and sinks. For $T=1$ the product is the identity. This also supplies the ordering condition needed by the manuscript's Lindström–Gessel–Viennot argument. Disjointness is in the unrolled lattice.

An independent comparison of determinants from physical direction words with simultaneous path counts covered 68,516 minors of orders one to three on 692 mask sequences. The general proof covers arbitrary orders and row gaps. A retained adverse case on the open three-site ring at $T=3$, $x=0$ changes the minor for rows 0,1 and columns 2,3 from $+1$ to $-1$ if the prescribed order of the rails is exchanged.

## Corollary 5.65 · each part FOLLOWS

1. For consecutive rows, same-parity columns give the published one-rail inequalities. Substitution of columns $2j+2,2j'+1$ and $2j+3,2j'$ gives the two stated cross-rail inequalities with the published index bounds.
2. Selecting the even or odd columns gives a Toeplitz matrix totally nonnegative in every finite order. The finite Pólya-frequency theorem gives nonpositive real roots of each nonzero rail polynomial. Initial zero coefficients supply zeros at the origin. With exactly three occupied levels there is no internal gap, and the quadratic discriminant gives $n_1^2\ge4n_0n_2$. A rail with no arrivals gives the zero polynomial. [Holtz and Tyaglov, Theorem 3.43](https://arxiv.org/pdf/0912.4703#page=60)
3. Let $A_{r,c}=w_{c-2r}$, $D=\deg W$, and write $a_k=w_{D-k}$ in descending coefficient order, taking zeros off the support. The infinite Hurwitz matrix has entries $a_{2j-i}=A_{j,D+i}$. Each finite minor of that matrix is a transposed minor of $A$. Thus total nonnegativity applies to the infinite Hurwitz matrix, including cases with a zero at the origin. The published infinite-matrix criterion gives no zero of $W$ in the open right half-plane. Factoring out $g(Y^2)$ with $g=\gcd(u,v)$ leaves coprime even and odd parts. Hermite–Biehler gives their simple alternating roots in the stated order, with a possible zero root of $v/g$. Empty rails reduce to part (ii). The empty reduced root list needs the usual vacuous convention. For the open three-site ring at $T=2$, the words RL and LR give $u=v=1$ and $W=1+Y$. A wording clarification would be “if the reduced list is nonempty, its first root belongs to $v/g$.” [Holtz and Tyaglov, Theorem 3.44](https://arxiv.org/pdf/0912.4703#page=60) · [Adm, Garloff and Tyaglov, Theorem 4.10](https://arxiv.org/pdf/1711.04651) · [Holtz, Theorem 1](https://arxiv.org/pdf/math/0512591)

## Theorem 5.70 · FOLLOWS given the preceding product theorem

Use the hypotheses inherited from 5.69, including a single sequence of quadratic coefficients consistent across product lengths. The base preparation range used here is $M\ge8$. The branch's later extension to $M\ge5$ depends on its separate preparation proofs. For three winding classes, let the twist be $\sigma=(-1)^{k_0}$. Folding signed counts gives a triple. Multiplication by $\beta$ sends $(e_0,e_1,e_2)$ to $(\sigma e_2,e_0,e_1)$. Both quadratic terms of 5.70 are invariant under this rotation.

Expanding the two positive multiset products in the proof gives $\beta A=B$, using $\eta\beta^3=1$. Both sides have 12 entries counted with multiplicity before the common padding. Their count terms therefore cancel at every degree. Once the coefficients at smaller lags have been eliminated, the remaining difference is $(2\sigma-3)b_d=0$. Its factor is either $-1$ or $-5$, so induction eliminates every higher lag. With an additional fixed occurring multiplier $m$, translation commutes with convolution and the constants may depend on $m$. The statement covers the specified products. It leaves general nonproducts and selection of a physical probability rule open.

The exact checker covered 930 group-relation and degree combinations across both twists. An intentionally unsigned wrap failed the negative-twist control as expected. The deposited Lean files cover the coincidence and induction with their hypotheses. This review inspected their role, did not rerun Lean, and did not independently reprove all antecedents of 5.69, including ring preparation.

## Reproduction

From the directory containing this note, run the following commands with Python 3. The first prints the order counts and the rail-order control. The second prints the relation count and the sign control. Both returned exit 0 in normal and optimized Python. No unanticipated failed predicates were observed.

~~~sh
python -B check_winding_minors.py
python -B check_threeclass.py
~~~
