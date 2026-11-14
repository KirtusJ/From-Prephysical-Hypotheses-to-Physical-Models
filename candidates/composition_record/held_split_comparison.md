# Splitting a large remote well while a detector response is held

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical derivation and verification with OpenAI Codex.

The [spectator refinements](spectator_refinements.md) identify a per-launch response $f(y)=cy$ for $0\le y\le1/2$ under their population and resolution assumptions. A remote station can use those cells to check a larger mass. It resolves a large well in one setting and divides it into smaller cells in the other. A near station retains the same tag throughout. The proposed measurement compares variation of two observed **block frequencies**. It needs neither an assumed binomial count law nor independence of the read noise within the block. No such block frequencies have been reported for this apparatus.

## A three-tick walk supplies both settings

Launch a walker at the origin in its right-going rail. Three free Hadamard-and-shift ticks give these signed rail numerators over $\sqrt8$:

| Well | $-3$ | $-1$ | $+1$ | $+3$ |
|---|---:|---:|---:|---:|
| $(R,L)$ | $(0,1)$ | $(-1,0)$ | $(2,1)$ | $(1,0)$ |
| Whole-well mass | $1/8$ | $1/8$ | $5/8$ | $1/8$ |

After the walk, coherently write a near tag for membership in the three minor wells, retain the position and rail, then separate the tag and walker. Choose the far setting after separation. In the unsplit setting Bob records the well while pooling its rails. In the split setting he also copies the rail at $+1$ to a fresh resolved bit. Thus the $5/8$ cell becomes $1/2$ and $1/8$. There is no change at the three minor wells. The read must score the joint near-tag and far-output cells at the stated resolution. Sampling a rail before that score, or deriving a random second port after an already sampled whole-well result, changes the hypothesis.

A position-only implementation gives Bob identical reporting clocks and eliminates his extra register. After the near tag is written at tick three, apply an identity coin and shift everywhere at tick four. At tick five the baseline applies a rail swap $X$ everywhere and shifts. Every ray returns to its original well. The split arm changes only the tick-five coin at $+2$ from $X$ to identity. The heavy right rail travels $+1\to+2\to+3$ with mass $4/8$. The heavy left rail still returns to $+1$ with mass $1/8$. All three minor rays return to their original wells. At $+3$ the heavy and minor arrivals have different near tags, so they are distinct **joint** cells even with Bob's rail pooled. If Bob's well alone were scored first there, its total would again be $5/8$. The eight-site ring suffices. At tick four, the two rays at $+4\equiv-4$ occupy opposite rails and both return under the baseline swap there. [Exact eight-site replay](check_remote_refinements.rs) · [Signed walk and coasting ports](two_remote_splitters.md) · [Reversible tag lookup and whole-cell resolution](spectator_refinements.md)

## What the near detector measures

More generally take a single joint cell of mass $1/2<m<1$ and put $r=1-m$. Tag all the minor cells at Alice. Their total is $r$ and each falls in the calibrated range. Let Bob split $m$ into positive leaves of size at most $1/2$; a balanced split suffices, although the walk above gives an unequal split. The new cells need no mutual interference in this test. A register bank can implement this choice at dyadic $m$ by assigning balanced labels to the two groups and retaining their original labels in unobserved memory. Every leaf remains distinct at the final score before summing over Bob. Writing Alice’s tag leaves each intended cell intact.

On a block of fresh separately normalized reads, let $F$ denote the held physical response, and $c>0$ its slope through one half. The type-specific probabilities for Alice's tag under unsplit and split reads are, respectively,

$$
q_F=\frac{cr}{f_F(m)+cr},\qquad r.
$$

Consequently $q_F=r$ if and only if $f_F(m)=cm$. An unchanged near spectator with smaller total mass $0<b\le r$ also works. Its two probabilities are $(b/r)q_F$ and $b$, so its frequency-gap bound below acquires a factor $(r/b)^2$. Bob's output, including structural zeros, should be retained to check the intended preparation and partition even if only the near bits enter the statistic.

## A bound from matched blocks

Fix the arm schedule before seeing the outcomes, or draw it independently of the preparation and read noise. Each block supplies nonempty groups of unsplit and split reads. Denote their near-tag hit fractions in $[0,1]$ by $U$ and $V$. The necessary link from records to the held response is

$$
E[U-V\mid F]=q_F-r.
$$

For example, it suffices that each scheduled unsplit slot has the stated conditional mean $q_F$ and each scheduled split slot has conditional mean $r$ given the held response. The order of the reads can be interleaved. Shared noise, anticorrelation and within-block memory are allowed as long as the mean link holds for the assigned slots. Conditional Jensen gives the observable population bound

$$
E[(q_F-r)^2]\le E[(U-V)^2].
$$

The right side is estimated by squaring the frequency difference **within each block** and then averaging over blocks. Squaring the difference of the two ensemble means permits opposite type-specific errors to cancel. If the squared block gap has population upper bound $D$, then $\Pr\{|q_F-r|\ge\eta\}\le D/\eta^2$ for $\eta>0$. Zero forces $f_F(m)=cm$ almost surely. A sequence of increasing block sizes with $D\to0$ gives the same conclusion for a common law of held responses. Ordinary finite-sample noise can give a positive squared gap even for an ordinary response. The conclusion uses the observed upper limit and its uncertainty. Holding one apparatus setting while its effective scale and response change independently on every read does not identify those individual responses.

The relative raw weight $g_F=f_F(m)/c$ can be assessed without an inverse estimate near a vanishing tag probability. For $\delta>0$, any $|g_F-m|\ge\delta$ gives $|q_F-r|\ge r\delta/(1+\delta)$ because $q_F=r/(g_F+r)$ and $m+r=1$. Thus

$$
\Pr\{|g_F-m|\ge\delta\}
 \le \min\!\left\{1,\frac{D(1+\delta)^2}{r^2\delta^2}\right\}.
$$

The finite fixture has $m=5/8$ and $r=3/8$. Repeating the intervention on a countable dense set of $m$ between one half and one can identify each type's response there by monotonicity if the same type law and lower-half calibration transfer across preparations. At $m=1$ the spectator disappears and the sole positive cell always wins. [Finite held-count bounds](held_walk_counts.md) · [A finite adaptive panel that hides a fluctuating response](adaptive_held_response.md)

## Separate banks and physical linkage

Independent pairing of an unsplit bank and a split bank also gives the bound. Here $F$ refers to the unsplit bank alone. Independence gives $E[V\mid F]=E[V]$; if the split table is calibrated for the split-bank population, $E[V]=r$ even if that population differs from the unsplit population. One may instead measure $E[(U-r)^2]$, using the independently identified all-small-cell reference $r$ directly. A common detector across the two arms is unnecessary for these numerical bounds. A randomized comparison with the **same near apparatus and pre-choice ensemble** is needed to interpret an observed change as caused by the remote choice. The positive result concerns the held unsplit population actually sampled.

Independent pairing is sufficient but needlessly adds split-arm sampling noise if $r$ is already known exactly. If split calibration is verified only to a mean error $|E[V]-r|\le e$, independence and the mean-square triangle inequality give $\sqrt{E[(q_F-r)^2]}\le\sqrt{E[(U-V)^2]}+e$. Common drift can correlate a split-bank deviation with the unsplit response even when the unconditional split rate is $r$. Matched-slot means or independent banks must then be justified. Count uncertainty across blocks requires a sampling or dependence model for those blocks.

A source that samples a classical tag first and sends copies to both stations can keep Alice's frequency unchanged under both far settings. Such an apparatus presents a conditioned single tag to its response, in place of the stipulated joint cell table. Likewise, a herald obtained after the choice, pairing only coincident clicks, or losses that depend on the tag can change the frequencies. Register block and trial IDs, planned exposures, flags, misses and both setting assignments. The three-tick table supplies a kinematic preparation and proposed intervention. Evidence that the same physical response governs its repeated unsplit reads is an additional requirement.
