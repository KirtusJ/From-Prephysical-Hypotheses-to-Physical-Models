# Two terminal clocks select ordinary weighting from position alone

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch the balanced walk from well 0, sheet 0, right rail on the seven-well reciprocal ring. On each launch, independently assign a terminal time of ten or twelve ticks with positive probability. Leave the walk undisturbed until that time, then record its base well. A single contrast of the two position histograms selects ordinary weighting among the terminal powers, largest-cell rules and fair direction-word counting defined below. The detector may group modes differently at different wells and clocks. The proof requires the same population of powers and counting rules in both arms. A single clock by itself admits exact mixtures of nonordinary powers.

## What the two clocks measure

Each tick applies the real balanced coin \((R,L)\mapsto(R+L,R-L)/\sqrt2\), shifts the two rails one well in opposite directions and flips the sheet on traversing the seam in either direction. Within each final well, the detector partitions the occupied rail-and-sheet modes into cells. Give each mode its positive squared-amplitude mass. A cell of mass \(m\) receives weight \(m^q\) for a common \(q\ge0\) on that launch. Normalize across all occupied cells before reporting the well. At zero power every positive cell counts once. The largest-cell rule can assign its mass arbitrarily among maximal cells. Fair direction-word counting assigns equal weight to all \(2^t\) microscopic words. The conditional histograms use lossless or independently corrected exposures in each arm. No rail or sheet record enters the contrast.

| Well | Ordinary mass at 10, in 1,024ths | Direction words at 10 | Ordinary mass at 12, in 4,096ths | Direction words at 12 |
|---|---:|---:|---:|---:|
| 0 | 72 | 252 | 200 | 924 |
| 1 | 245 | 55 | 1,960 | 286 |
| 2 | 100 | 210 | 245 | 793 |
| 3 | 65 | 121 | **49** | 507 |
| 4 | **49** | 121 | 637 | 507 |
| 5 | 52 | 210 | 221 | 793 |
| 6 | **441** | 55 | **784** | 286 |

Each bold entry has exactly one occupied mode. Call the clocks \(A,B\) and label the two pure masses at each by \(\ell_j<h_j\), using probabilities as mass units. Thus \(\ell_A/\ell_B=4\), \(h_A/h_B=9/4\), \(h_A/\ell_A=9\), and \(h_B/\ell_B=16\). Let \(P_{j,h},P_{j,\ell}\) be the observed probabilities of those wells. Define
\[
D_j=\frac{P_{j,h}/h_j-P_{j,\ell}/\ell_j}{\log(h_j/\ell_j)},\qquad W=D_A-D_B.
\]
Both ordinary contrasts vanish. The four reported probabilities have distinct, fixed clock and well addresses, even though well 6 appears at both clocks.

## Why every alternative gives a positive score

Let \(Z_j\) be the sum of the cell masses raised to \(q\) in arm \(j\). At a fixed finite power write \(r=q-1\). For either clock,
\[
D_j=\frac{r}{Z_j}\int_0^1\big(\ell_j^{\,1-s}h_j^{\,s}\big)^r\,ds .
\]
The normalizers can differ. To compare them, take the most pooled cell vector at clock A and split every entry into equal halves. The most finely split B vector majorizes it. In units of \(1/4096\) the differences of the sorted prefix sums, padding with zeros, are
\[
882,\ 784,\ 735,\ 441,\ 437,\ 433,\ 410,\ 366,\ 336,\ 306,\ 251,\ 196,\ 98,\ 0 .
\]
Pooling any B cells raises its sorted prefix sums. Splitting an A cell refines each of its two halves. Thus the result holds for every allowed pair of partitions. Applying convexity to the power sums gives \(Z_B\ge 2^{-r}Z_A\) for \(r>0\). Concavity gives \(Z_B\le 2^{-r}Z_A\) for \(-1<r<0\), extending to \(r=-1\) by the one-sided limit on positive cells. [Marshall, Olkin and Arnold, *Inequalities: Theory of Majorization and Its Applications*](https://doi.org/10.1007/978-0-387-68276-1)

At every \(s\), the ratio of the geometric interpolants in A and B is \(4^{1-s}(9/4)^s>2\). For \(r>0\) the ratio of the integrals therefore exceeds \(2^r\ge Z_A/Z_B\). For \(r<0\) it is below \(2^r\le Z_A/Z_B\), and the prefactor \(r\) changes sign. In both cases \(W>0\). This compares normalized probabilities across two exposure times of the same unaltered walk.

Under the largest-cell rule, A always reports well 6. Its pure mass 441 exceeds every other whole well. B can report neither scored well because well 1 contains a mode of mass 1,764. Hence \(W=1/(h_A\log9)>0\), including arbitrary ties elsewhere. Fair counting gives
\[
W\log9=(55/441-121/49)+(\log9/\log16)(507/49-286/784)>18673/7056>0 .
\]
The rational lower bound follows from \(\log9/\log16>1/2\). For an arbitrary common type distribution, condition on each type and pair any two conditional partition choices. The inequalities hold for every pairing. Taking expectations leaves zero only if the power equals one almost surely.

Each time has only two distinct pure masses, so the [single-histogram necessity theorem](When_a_position_histogram_identifies_its_probability_power.md) supplies finite mixtures of nonordinary powers that match each arm separately. Allowing the detector to choose a different exponent distribution in response to the time therefore defeats identification, even if assignment was randomized. The positive result assumes transfer of the type law across the assigned times. It applies to ideal population probabilities. Finite data need uncertainty estimates and timing and detection controls. Parity on an odd ring makes a trivial sheet connection give the same site records for this sharp source. These observations constrain the terminal probability rule within the specified family and leave the sheet connection undetermined. [Parity and position records](A_reciprocal_sheet_connection_on_six_wells.md#what-a-base-site-instrument-can-see-on-an-odd-ring)

## Why adding clocks sometimes fails

For comparison, consider any finite list of clock settings, each with at most **one** distinct positive mass among its pure wells. Partition choices are free in each well and setting. Even with a common exponent law, all their ordinary position histograms together admit a finite exact mixture of nonordinary powers in any prescribed two-sided neighborhood of one.

To prove this, take the convex hull of vectors of conditional histograms formed with one common finite nonordinary exponent and a partition for every setting. Its closure contains the ordinary vector by continuity. Suppose a nonconstant functional in the relative affine hull supports it there. Center the observable at each setting by subtracting its ordinary expectation, giving \(\sum_x h_{jx} m_{jx}=0\) separately for each \(j\). The total score is a sum of normalized expectations. At \(q=1\) each numerator vanishes and each denominator equals one, so its derivative agrees with the sum of the numerator derivatives. A supporting score has zero derivative there for every choice of partitions. Changing the partition at just one mixed bin forces its coefficient to vanish, since \((u+v)\log(u+v)>u\log u+v\log v\) for \(u,v>0\). Centering then makes the aggregate coefficient of the sole pure mass class at each setting vanish. The score consequently vanishes for every admissible common power and choice of partitions, contrary to proper support. The ordinary vector is in the relative interior of the closure and hence in the convex hull itself. Membership supplies a finite mixture. [Border, *Separating Hyperplane Theorems*](https://kcborder.caltech.edu/Courses/Notes/SeparatingHyperplane.pdf) Â· [Single-setting proof](When_a_position_histogram_identifies_its_probability_power.md#why-fewer-than-three-cannot-work)

On the **six-well** ring, our sharp-source scan through tick 120 gives 117 clocks with zero pure mass classes and three with one. All 120 conditional histograms can therefore be matched exactly by one common distribution of nonordinary powers when within-well partitions may depend on the clock. The finite scan makes no claim about later times. Sharing a power law can identify it on the seven-well protocol above because *both* of its clocks provide a comparison between distinct pure masses.

The [checker](check_two_terminal_clocks.py) replays the signed recurrence on the double cover and separately enumerates all physical direction words at the two clocks. It verifies every prefix for all 1,024 pairs of within-well partition choices, the strict integer controls for fair counting and maximizers, and the six-well comparison. The [Lean calculation](lean/TwoTerminalClocks.lean) independently evaluates both bare ring vectors and checks the sorted-prefix inequalities. The [output](results/two_terminal_clocks.json) retains all wells, zero amplitudes and all 120 six-well clocks. No physical trials enter the calculation.
