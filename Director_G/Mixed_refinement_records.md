# Testing the ordinary character without assuming a pure source

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On the signed staircase, two single-walker probability measurements suffice under a compatibility hypothesis. A four-tick port at order three excludes counting and the trivial character. The size of a three-tick rail response along a cofinal sequence of increasing orders then separates one unit of charge from all larger charges, even for mixtures. The second measurement requires resolving a probability difference of order $M^{-2}$ with a specified coefficient. The qualitative positive-click tests at individual primes require a different prior hypothesis about purity. [Pure-label and mixed-cover comparisons](Refining_the_sheet.md) · [Native staircase law](Counting_and_character_records.md)

## A nonnegative quantity measured on the walk

At order $M$, assume the classified normalized law has count weight $c$ and folded square weights $b_M(d)$, $0\le d\le\lfloor M/2\rfloor$. They sum to one including count. For $m\mid M$, require that the count fraction is preserved and that $b_m$ is the pushforward of $b_M$ under $d\mapsto |d|_m=\min(d\bmod m,-d\bmod m)$, with each remainder taken in $[0,m-1]$. This is a condition on the measured single-walk marginals. A shared unknown label in two trials can correlate their outputs even when these one-trial marginals agree. The theorem does not assume independently refreshed labels, common hidden labels, or any particular two-trial coupling. The mixed-cover comparison identifies the separate marginals. [How to compare covers](Refining_the_sheet.md)

Launch at $(0,R)$ and read only the rail after three ticks. Subtract the field-off left probability from its field-on value on the same ensemble. For a coherent label the excess is $\tfrac12\sin^2(\pi d/M)$; for counting it is zero. Define

$$
v_M(d)=\frac M\pi\sin(\pi d/M),\qquad
C_M=\frac{2M^2}{\pi^2}\,[P_{\rm on}(L)-P_{\rm off}(L)]
    =\sum_d b_M(d)v_M(d)^2 .
$$

The scale assigns a single turn of the designated sheet generator limiting squared charge one. It is a dimensionless calibration. Establishing the native probability law, matching preparations across controls, and fixing this scale are physical inputs. The field-off baseline is $(1+c)/4$. [Eight signed words and the rail read](Refinement_and_free_fall.md)

If $m\mid M$ and $e=|d|_m$, then $e\le d$ and $v_m(e)\le v_M(e)\le v_M(d)$. For fixed $e$, the first inequality follows because $\sin x/x$ decreases on $[0,\pi/2]$; the second follows from sine monotonicity on the same interval. Therefore $C_m\le C_M$ under compatible refinement. On any divisibility-cofinal sequence (each fixed order eventually divides every order in the sequence), finite $\liminf C_M$ bounds every $C_m$.

## One dark port and the exact criterion

At any fixed order $m\ge3$, measure $(m-1,R)$ at tick $m+1$. Its $m$ positive words put a single left move in the first $m$ steps. Their staircase gains run through every residue once. The count numerator is $m$, the trivial square numerator is $m^2$, and every other square numerator is zero by the sum of the roots of unity. At $m=3$ this gives the ordinary, unfiltered four-tick measurement

$$
\rho=P_4(2,R)=\frac{3c+9b_3(0)}{16}.
$$

**Criterion.** For the compatible classified family on all orders, the following two conditions together are necessary and sufficient for the ordinary folded character at every order:

1. $\rho=0$.
2. Along one divisibility-cofinal sequence, $\liminf C_M\le1$.

The ordinary law has $\rho=0$ and $C_M=v_M(1)^2\to1$. Conversely, the dark result forces both $c=0$ and $b_3(0)=0$. This excludes every multiple of three in any integer-charge description, including zero. Orders divisible by three have no mass at zero. For $M\ge4$, write $A_M=v_M(1)^2$, $B_M=v_M(2)^2$, with $B_M>A_M$. Then

$$
C_M\ge A_M+(B_M-A_M)\sum_{d\ge2}b_M(d).
$$

On the cofinal tail $A_M\to1$ and $B_M\to4$. For every fixed index in the sequence, all sufficiently late orders are multiples of it, so monotonicity and the liminf bound imply $C_M\le1$ at each index. The mass above one therefore tends to zero. At each fixed order $m$, the coarse mass outside the folded label one is no larger than the corresponding mass at a common fine multiple. It is therefore zero. No two-copy purity test or family of prime-order nonzero tests is needed for this implication. The conclusion fixes the folded probabilities; global conjugate orientations remain indistinguishable in these single-walker records.

## Finite precision and an order-four alternative

At a fine order $M\ge4$ divisible by three let $z=c+b_M(0)$ and let $u=\sum_{d\ge2}b_M(d)$. The measured anchor bounds $z\le\eta=\min(1,16\rho/3)$. Directly at that order,

$$
u\le\frac{C_M-A_M(1-z)}{B_M-A_M},\qquad
z+u\le\min\left(1,\frac{C_M-A_M+B_M\eta}{B_M-A_M}\right).
$$

Any coarse order dividing this fine order inherits this bound on its total nonordinary mass. In particular, exact $\rho=0$ and $C_M\le A_M$ at **one** such fine order select the ordinary law there and on every divisor. Larger orders can still differ. If an independent field-off measurement has determined $c$, the sharper anchor is $\eta=c+(16\rho-3c)/9$. Finite estimates require upper confidence limits for $\rho$ and the contrast $C_M$ at their actual measurement precision. With $\liminf C_M\le1+e$, $e\ge0$, the resulting bound on every order is $\min(1,(e+4\eta)/3)$. The coefficient is sharp where the bound is below one: take count mass $\eta$, integer charge two of mass $(e+\eta)/3$, and charge one for the remainder. At finite order the analogous three-point choice attains the finite inequality whenever the prescribed weights are feasible.

There are two accessible parity ports at order four. At tick four each of $(0,L)$ and $(-2,L)$ has square numerators $(1,5,1)$ for folded labels $(0,1,2)$ and count numerator three, all over 16. The three words at the first port are RRLL, RLRL, LRRL. At the second they are RLLL, LRLL, LLRL. From either probability $p$,

$$
D=5-16p=2c+4[b_4(0)+b_4(2)] .
$$

So $p=5/16$ alone excludes count and all even charges. It can replace the order-three dark requirement. On a multiple $M\ge8$ of four, every folded odd label other than one is at least three. Put $B'_M=v_M(3)^2$ and let $s$ be the total mass of count and even labels, so $s\le D/2$. Bounding the energy of these labels below by zero gives total nonordinary mass at most

$$
\min\left(1,\frac{C_M-A_M+B'_M D/2}{B'_M-A_M}\right).
$$

This transfers to dividing orders and gives $\min(1,(e+9D/2)/8)$ on the cofinal limit. At exact saturation the bound is $e/8$. Count mass $D/2$, charge-three mass $(e+D/2)/8$, and the remaining weight at one attain the cofinal bound wherever these weights are nonnegative. Both ports can be summed in the same terminal histogram; their maximal summed probability is $5/8$. No independence between their counts is required.

## What finite curvature says about arbitrary mixtures

Finite cofinal energy has a stronger interpretation. Since $v_M(d)\ge2d/\pi$, all fine folded distributions have uniformly bounded second moments. Thus their mass above any integer $J$ is at most $\pi^2\sup_M C_M/(4J^2)$. Along increasingly divisible orders select a subsequence on which the weight at each fixed integer converges, by successive subsequence extraction and a diagonal choice. The uniform tail bound shows these limits $w_j$ sum to $1-c$. For a fixed smaller order, fold the finitely many labels up to $J$, then send $J$ to infinity; compatibility gives exactly

$$
b_m(d)=\sum_{j:\,|j|_m=d} w_j .
$$

The integer weights are unique: at large orders all finitely many ordinary integers below a chosen cutoff are read without aliasing and the remaining tail tends to zero. In this representation $v_M(|j|_M)^2$ increases on a divisibility chain and tends to $j^2$ for each $j$. Monotone convergence of a series yields $\lim C_M=\sum_{j\ge0}j^2w_j$. A uniform finite energy bound really does reduce the compatible mixture to a distribution on ordinary nonnegative integers and count. It supplies neither purity nor faithfulness by itself. A mixture of charge two with mass $1/4$ and charge zero with mass $3/4$ has limiting energy one. Half charge three and half charge five pass the odd order-four anchor and give a positive dark response at every odd prime, while their limiting energy is 17. The weaker upper bound $\limsup C_M<4$, together with the order-three dark port, excludes all single fixed nonordinary labels. It still admits a mixture with a small positive charge-two weight; selecting the ordinary label from the full mixed class needs the sharper coefficient.

Without cover compatibility, small nonordinary fractions at a succession of tested orders do not imply the same bound at an intervening order. Without the $M^2$ normalization, even a fixed charge three gives a vanishing three-tick excess. The finite integer inequality underlying the cofinal gap also has a Lean proof. For nonnegative integer weights it gives $\mathrm{mass}+3\,\mathrm{mass}(K\ge2)\le \mathrm{energy}+\mathrm{mass}(K=0)$, extending to rational weights by common scaling. The trigonometric and infinite-mixture steps are the analytic arguments above. [Lean proof of the mass bound](lean/MixedWindingEnergy.lean) · [Independent numerical checks](check_mixed_refinement.py) · [Retained finite comparisons](results/mixed_refinement.json)

In independent on/off rail frequency estimates with binomial noise, both raw probabilities stay away from zero and one for the ordinary label. Resolving a fixed separation in $C_M$ by those frequencies costs order $M^4$ launches at fixed accuracy and confidence. After the exact null anchor has excluded counting, a less costly measurement uses only the field-on port $(-1,L)$ at tick three. Its probability is $p=\sum_d b_M(d)\sin^2(\pi d/M)/2$, exactly the rail excess; counting would have added $c/4$ to this port. Estimate $C_M$ by $2M^2\widehat p/\pi^2$. Across $S$ independent launches its variance is $(2M^2/\pi^2)C_M(1-p)/S$, so order $M^2$ launches suffice for fixed absolute precision when $C_M$ stays bounded. This savings needs a calibrated dark detector with negligible or separately characterized background. A genuine nonzero $c$ must also be estimated or bounded at the required precision if this replacement is used. No finite sequence of null detections establishes an exactly zero probability, and macroscopic position continuity alone does not establish the cofinal inequality. [Native dark port and full rail comparison](Refinement_and_free_fall.md)
