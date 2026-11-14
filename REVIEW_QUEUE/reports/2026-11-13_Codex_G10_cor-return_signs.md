**HELD on the coefficient-sign implication.** Target: G10 Theorem 5.26(c), Corollary 5.29 and their application to the event space specified by Z1.
Outcome: NONE FOUND for the conditional implication under the full event space.
Reviewer: OpenAI Codex, with an internal Codex challenger. The project withdrew Z1 on 13 November 2026.

Assume the classification of Theorem 5.26(c) and nonnegative weight on every admissible event, with arbitrarily large gain multiplicities realizable by allowing unbounded walk lengths. Then the count coefficient and the squared-term coefficients for distinct observable character classes are nonnegative. The sign conclusion does not require singleton normalization. Giving a single walk weight one adds the separate normalization used by Corollary 5.29. The withdrawal has a different target. In the classified, normalized family, near-return in the rule's own weights is equivalent to a zero count coefficient. Treating near-return as a stipulation about those weights cannot independently explain the choice of rule. The argument below supplies no empirical premise for that choice. [Withdrawal record](../../Director_Z/candidate/abandoned/Z1/WHY_ABANDONED.md)

## Which coefficients an event can distinguish

In Theorem 5.26 put \(H=C_0\), the subgroup of gain quotients that can occur at the same vertex and length. On a single endpoint the D1 rule applied to multiplicities \(m_h\) has the form

\[
a\sum_h m_h + \sum_{[\rho]} c_{[\rho]}\left|\sum_h m_h\rho(h)\right|^2.
\]

The index runs over distinct nontrivial restrictions to \(H\), identified with their inverses. The restrictions are nontrivial by 5.26(b). Lemma 5.25(4) lets us realize every nonnegative integer vector \(m\) at one endpoint with all other endpoints empty, at a sufficiently large allowed length. Translating its support into a physical gain coset multiplies each character sum by a unit-modulus constant.

First put one walk at each gain of \(H\). Every nontrivial character sums to zero, so the weight is \(a|H|\) and S4 gives \(a\ge0\). A singleton gives \(a+\sum c_{[\rho]}=1\).

Now fix a restricted class \([\rho]\). For integer \(T>0\) choose the nonnegative integer multiset

\[
m_T(h)=\lfloor T(1+\operatorname{Re}\rho(h))\rfloor.
\]

The count grows at most linearly in \(T\). By finite character orthogonality, the Fourier sum for the target equals \(T|H|/2+O(|H|)\), or \(T|H|+O(|H|)\) when \(\rho\) has order two. Every other indexed class has sum bounded by \(|H|\), from rounding. Divide the nonnegative event weight by \(T^2\) and take the limit. Only a strictly positive multiple of \(c_{[\rho]}\) survives, hence \(c_{[\rho]}\ge0\). If there are no character classes, the same count and singleton arguments give \(a=1\).

If two full characters restrict identically up to inversion, only the **sum** of their coefficients is observable. A redundant list can assign signed coefficients to identical squares. The proof establishes the signs in the unique class expansion of 5.26(c). With that expansion, normalization and S5, Corollary 5.29(3) gives \(a=0\). The test uses the availability of arbitrarily large one-endpoint multisets. Positivity restricted to an instrument's selected finite list of events would require a separate argument.

## An exact boundary for a bounded test

Consider a carrier in the classification with two observable gains and one nontrivial sign character, for example the signed ring of the archived candidate. For same-endpoint multiplicities $r,s$ the normalized rule reads
$$
W(r,s)=(1-c)(r+s)+c(r-s)^2 .
$$
Each singleton has weight one. Fix an integer $M\ge2$ and test every $0\le r,s\le M$. Among rules with $c\le0$, all these tests pass exactly when $c\ge -1/(M-1)$. Indeed, whenever $r+s>0$,
$$
\frac{(r-s)^2}{r+s}\le |r-s|\le M .
$$
The maximum $M$ is attained at $(M,0)$. Since $c$ is nonpositive, the smallest weight divided by $r+s$ is $1+c(M-1)$. The empty event has weight zero. At $c=-1/(M-1)$ the entire box therefore passes and the next box already contains the negative event $W(M+1,0)=-(M+1)/(M-1)$. As all endpoint weights add, the same bounded tests pass across multiple endpoints. For $M=1$ the two singletons have weight one and the mixed pair has weight $2(1-c)$, so every $c\le0$ passes that box.

For a concrete instance, the eight-site signed ring launched at the right rail of site 0 has three paths ending at the right rail of site 2 at tick four. Their words LRRR, RLRR and RRLR each have a positive sign, giving $(3,0)$. With $M=2$ and $c=-1$ its weight is $-3$, although every multiplicity through two per gain passes. This explicit family explains how a bounded search can miss the negative coefficients recorded by Director Z's challenger. [Challenger results](../../Director_Z/challenger/twelfth_signs/FINDINGS.md)

## Exact events in a proper subgroup

Use the complete directed graph on \(\mathbb F_5\) with gain \((1,ij)\) on arc \(i\to j\) in \(\mathbb F_5^2\), launched at 0. At length three, walks ending at vertex 1 have multiplicities \((9,4,4,4,4)\) indexed by the second gain. The first coordinate is fixed. Twenty qualifying full characters yield two distinct squared terms, indexed by frequencies 1 and 2 on the second gain coordinate. In the following rows the coefficients are ordered as count, class 1, class 2. Each rule gives one on a singleton.

| Coefficients | Selected walk counts by gain | Exact event weight |
|---|---|---|
| (−1, 1, 1) | (1, 1, 1, 1, 1) | −5 |
| (1, −1, 1) | (2, 2, 0, 0, 2) | \(6-4\sqrt5<0\) |
| (1, 1, −1) | (2, 0, 2, 2, 0) | \(6-4\sqrt5<0\) |

The checker verifies both directions of reachability on all 125 lifted vertices, the degree and character condition, walk availability, all three exact weights and a nonnegative control. The argument above applies beyond these three instances. An internal Codex challenger received the hypotheses without this derivation and separately recovered the sign proof, including the order-two case. Review remains internal to the project.

[Exact checker](2026-11-13_Codex_G10_cor-return_signs/check_d2_signs.py) · [Recorded output](2026-11-13_Codex_G10_cor-return_signs/d2_signs.json)
