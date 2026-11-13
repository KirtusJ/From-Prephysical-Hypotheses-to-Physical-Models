# Calibrating two unknown detector laws on a single sharp walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The edge argument in [G1 v1.0](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/4f3468b/Director_G/candidates/edge_record_walk/specification.md) assumes one response shape shared by both rails. Here the detector bank can have *two* unknown response functions, each sensitive even to the sign of a single total. A final switch interchanging the two signed outputs supplies enough comparisons to identify both functions on every integer. If each detector is independently insensitive to sign, an ordinary unswitched sharp launch already suffices. The physical assumption retained in both results is that each oriented detector probability depends on its local signed total through a fixed scalar score and a common panel normalization.

Goldstein and Struyve studied the related uniqueness question for distributions equivariant under a given Bohmian dynamics, assuming a local functional of the continuum wave function. Dürr, Goldstein, Tumulka and Zanghì construct stochastic configuration dynamics with squared distributions in other models. Here the tested assumptions concern two discrete terminal scores, conservation at a parent site, and physically attainable walk inputs; the conditional history law remains free. [Goldstein and Struyve](https://arxiv.org/abs/0704.3070) · [Dürr et al.](https://arxiv.org/abs/quant-ph/0407116)

## What is compared

Launch one positive input on the right rail at zero. A site with raw inputs \((u,v)\) sends \(a=u+v\) right and \(b=u-v\) left. Work on the line with a finite cone at each read, or use rings large enough to avoid wrapping through the next tick. Suppose the terminal score is \(F(k)\) on the fixed right rail and \(G(k)\) on the fixed left rail. The two functions are nonnegative on the integers, share no presupposed proportionality or sign symmetry, satisfy \(F(0)=G(0)=0\), and \(F(1)>0\). In each panel divide each score by the sum of all its detector scores. An exact cancellation and an unused port with the same zero input have the same response under this premise. The functions are stable across sites, horizons and, for the unbounded result, ring sizes.

A conserved marker moves from its parent site to either daughter, and a faithful complete read reports its oriented port. Up to the parent tick the dynamics are the same whether the run stops there or continues. The two daughter probabilities in the latter ensemble therefore sum to the parent-site probability in the former. No rule is specified for dividing the marker population between the two daughters. For the optional switched experiment, perform the same preparation and the same prefix, then exchange the outgoing **signed tallies** after their final coin and before their shift to the fixed detectors. The marker still leaves through one of those two ports and the score laws remain stable. This can be a simultaneous rail exchange at every site. A permutation of already recorded outcome names cannot implement this experiment.

Write \(Z,Z'\) for the full parent and daughter panel score sums. The native rightmost parent \((1,0)\) has daughter totals \((1,1)\). Thus \(Z'/Z=\lambda=(F(1)+G(1))/F(1)\) at every native depth. In a final switched tick the two rightmost-parent daughter totals are again \((1,1)\): conservation at that parent fixes the very same ratio, even if all sites switch. Prefix invariance, stable scores and complete accounting are used in this cancellation.

## Four signed units determine the normalization

The pairs \((1,0),(0,1),(0,-1),(-1,0)\) occur at \((t,x)=(0,0),(1,-1),(2,-2),(3,-1)\), respectively. For each pair, parent conservation gives

\[
 F(u+v)+G(u-v)=\lambda[F(u)+G(v)].
\]

Adding these four equations counts each of \(F(1),G(1),F(-1),G(-1)\) twice on the left. Their sum is positive, so \(\lambda=2\). Substituting in the four equations gives \(F(1)=G(1)=F(-1)=G(-1)=c>0\). In particular \(Z_t=2^tc\) for the sharp launch. The two rail response scales were allowed to differ. The result requires a faithful complete read; losses outside this model would require calibration. No balance condition was imposed on the marker coin.

## Identifying the two shapes

Define \(J(k)=F(k)-G(k)\). At a chosen final parent the ordinary and exchanged daughter sums must both be \(2[F(u)+G(v)]\). Subtraction gives \(J(u+v)=J(u-v)\) for every tested pair. The unmodified walker actually prepares two infinite strips:

- At \(t=n+1,\ x=n-1\), exactly one step goes left. The incoming pair is \((n,1)\). Hence \(J(n+1)=J(n-1)\) for \(n\ge1\). The zero and unit results give \(J=0\) on all nonnegative integers.
- At \(t=m+3,\ x=-m-1\), exactly one step goes right. A right-ending word has \(t-2\) left-to-left sign changes. Of the left-ending words, the one beginning right has \(t-2\) such factors, and each of the other \(t-2\) words has \(t-3\). Thus the pair is \((-1,m)\) for even \(m\), and \((1,-m)\) for odd \(m\). For even \(m\ge2\) the exchange equates \(J(-m-1)\) and \(J(m-1)\); for odd \(m\ge1\) it equates \(J(1-m)\) and \(J(1+m)\). Together with \(J(-1)=0\), these cover all negative inputs.

Write the resulting common shape as \(f\). The ordinary right-strip equation becomes \(f(n+1)+f(n-1)=2[f(n)+c]\), so \(f(n)=cn^2\) by induction for \(n\ge0\). On the left strip, the even-\(m\) identity reads \(f(m-1)+f(-m-1)=2[c+f(m)]\). This supplies the odd negative arguments. For odd \(m\) the identity \(f(1-m)+f(1+m)=2[c+f(-m)]\) supplies the even negative arguments. Thus \(F(k)=G(k)=ck^2\) on all integers. The complete normalized panel is \(D_t(x,r)^2/2^t\) under these hypotheses. The [Lean exchange lemmas](lean/RailExchange.lean) check cancellation with integer-scaled scores and the signed strip argument for arbitrary codomain. The physical comparison and the proof for real scores are given above.

**Sign-insensitive detectors.** If \(F\) and \(G\) are each even, the ordinary right and left strips give

\[
 F(n+1)+G(n-1)=2[F(n)+c],\qquad
 F(n-1)+G(n+1)=2[c+G(n)].
\]

Each next pair is determined from the preceding two pairs. Starting with both zero and both \(c\) gives \(F(n)=G(n)=cn^2\) by simultaneous induction. This route uses no final exchange. [Lean verification of the integer-scaled recurrence](lean/TwoRailScores.lean)

## What the finite checks establish

The checker builds the raw field by local signed addition, verifies all four signed units, and checks the actual strip inputs through \(n=34\). Exact elimination then projects the solution space for the raw balance equations onto the 132 rail-specific signed entries with \(1\le|k|\le33\), treating every larger entry as an unknown. The ordinary strips and unit rows leave dimension 65, including the scale. The exchanged strips leave only the scale. In the separately even class the ordinary strips also leave only the scale. These are dimensions for the specified **raw linear equations**. A positive exact probability \(p\) imposes the additional relation \(F(k)=pZ_t\) or \(G(k)=pZ_t\). The unit reference and conservation give the stated normalization. A zero port alone supplies no scale, and sampled frequencies have uncertainty.

For example, increase only \(F(-3)\) and \(G(-2)\) by one above the squared values. The ordinary raw strip equations remain exact. Nevertheless the full normalization first changes at tick five, from 32 to 33, as \(G(-2)\) occurs in the interior. The perturbed right frontier then fails conservation against its previous panel. This example cannot serve as a rival matching the normalized experiment. Adding the full normalizer constraints from tick zero through tick 20 to the raw strip system reduces the projected dimension from 65 to 57, including the scale. A stronger native comparison imposes conservation on *every* visited parent, including interior sites. On the 49 nonzero rail-and-tally labels reached through tick 12, the projected dimension after 14 ordinary ticks is two. Through tick 18 it is one, so the ordinary walk already fixes all 49 scores up to the common multiplier. This finite fact neither proves nor refutes all-integer identification with no switch. [Exact input rows, projected dimensions and full panel sums](results/separate_rail_scores.json) · [Checker](check_separate_rail_scores.py)

There are conserved-marker models outside the endpoint-score premise. For example, at each occupied site send the marker right or left in proportion to \((u+v)^4\) and \((u-v)^4\), with fair splitting if both are zero. This rule respects exchange of the signed daughters, preserves every parent mass and is fair on the signed unit parents. At tick three and \(x=1\) its raw pair is \((2,1)\) and its parent mass is \(5/8\). Its next right daughter receives \(405/656\), compared with \(9/16\) under squared terminal scoring. Conservation and a wire permutation alone do not supply a fixed scalar score of the final signed total.

Access to large counts is also an operational limitation. Under the selected law, the right frontier used as the unit reference has probability \(2^{-(n+1)}\) at the parent depth of the \(n\)-th right-strip comparison. Seeing that one reference even once with probability at least \(1-\eta\) needs at least \(\lceil\log(\eta)/\log(1-2^{-(n+1)})\rceil\) independent launches at that depth. This is a detection cost, prior to estimating its odds precisely. Site homogeneity is material. On an even ring with one sharp launch, one can multiply both scores at each site by a positive parity-dependent constant. Each complete panel occupies one parity, so its normalized probabilities stay the same even though the inferred raw normalizer ratio changes. The theorem removes the common-rail-shape premise in two stated protocols. It leaves the physical origin of signed transport, detector sufficiency, attainable switching and record formation open.
