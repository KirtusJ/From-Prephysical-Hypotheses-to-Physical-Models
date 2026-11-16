# Changing the polarization analyzer before counting both outputs

Kirtus Justus, research direction. OpenAI ChatGPT (Director G), optical bounds and counting designs. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

A field polarized along one output of a fixed polarizing splitter can produce clicks in that bank and leave the other bank dark. The [previous coincidence design](Retaining_coincidences_on_random_gates.md) excludes such inputs through a lower bound on both rate shares. Here the apparatus admits every polarization in a specified optical mode. It draws a fresh analyzer axis after the source has committed the field and reads both outputs. At 10% total efficiency, three orthogonal, equally likely axes give a 2,164-preparation optical test with both errors below 5%. A balanced single excitation and an explicit mixture of classical fields give a lower bound of 1,621 preparations even when every axis and bank label is retained.

## What the random analyzer measures

Use two independent threshold banks on each preparation. Record the chosen axis and both bank bits, including empty and double gates. The axes are directions on the Poincaré sphere. Horizontal versus vertical, diagonal versus antidiagonal, and circular left versus right supply the three orthogonal directions. Orthogonality here refers to the Stokes vectors of the analyzers. McWilliam and colleagues describe these complementary polarization projections and report a different, four-projection polarimeter. Their measurements establish optical context for the analyzer choices. The coincidence and sample counts below are predictions for a proposed experiment. [McWilliam et al., *Optics Express* 32, 21909 (2024), §2.1](https://eprints.gla.ac.uk/327200/1/327200.pdf)

At a given preparation, condition on the field and earlier records. Assume a total detected Poisson rate $\lambda$ that is invariant under the current analyzer choice, and a normalized classical Stokes vector $s$ with $|s|\le1$. A calibrated analyzer with unit axis $a$ sends rate fractions $(1\pm a\cdot s)/2$ to independent banks. This encompasses an integrated classical polarization coherency matrix if the same analyzer acts across the admitted modes and the count law holds conditionally. It requires matching bank throughputs and a polarization transformation with common total loss. A general field sent into disjoint, uncharacterized detector modes need not obey this model.

Write $t=1-e^{-\lambda}$ for the probability of any click, $y=1-e^{-\lambda/2}$, and $x=a\cdot s$. Then $t=2y-y^2$ and the probability of a double is
$$
d(x)=1+e^{-\lambda}-2e^{-\lambda/2}\cosh(\lambda x/2).
$$
For $|x|\le1$, every nonconstant term in the even power series satisfies $x^{2k}\le x^2$. It follows that $d(x)\ge(1-x^2)y^2$, with equality at $x=0$ and $|x|=1$. For axis probabilities $p_j$ define $M=\sum_j p_j a_j a_j^{\mathsf T}$ and $m=1-\lambda_{\max}(M)$. Averaging over the fresh axis gives
$$
\overline d\;\ge\; [1-s^{\mathsf T}Ms]y^2\;\ge\;m y^2.
$$
This step averages the click law for each incident field. Substituting the mean polarization of a pulse ensemble into the nonlinear click formula can give a false stronger bound.

Choose $L=2$ or $3$ orthogonal axes uniformly. Then $m=1-1/L$. A pure input along one chosen axis gives no doubles on that axis and exactly $y^2$ on every other one. The bound is sharp at every intensity. With three measured unit axes of pairwise absolute dot product at most 0.05 and uniform selection, the Gram matrix has maximum absolute row sum at most 1.10. Hence $\lambda_{\max}(M)\le1.10/3$ and $m\ge19/30$. Throughput errors are a separate calibration. Among all random polarization axes, the trace of $M$ is one in three dimensions, so $m\le2/3$. The uniform triad attains the best low-intensity worst-case coefficient, since $d(x)=(1-x^2)\lambda^2/4+O(\lambda^3)$ uniformly. This argument makes no finite-intensity optimality claim for other axis distributions.

## Counting rule and a lower bound that retains bank labels

Let $K$ count occupied preparations, including doubles, and $D$ count doubles. For a design allowing $D\le j$, assign the observation product $w^K r^D$ with $0\le r<1$ and $0^0=1$. Put $y_0=\eta/2$, $\beta=m(1-r)$, $w=(1-y_0)/[1-(1+\beta)y_0]$ and $A=1+(w-1)y_0$. Fresh independent axis choices bound each conditional field factor by
$$
1+(w-1)(2y-y^2)-w\beta y^2=A-(w-1+w\beta)(y-y_0)^2.
$$
When $D=0$ and $K\ge k$, the choice $r=0$ gives field false rejection at most $A^n/w^k$. A clean independently prepared single excitation with total efficiency $\eta$ has $D=0$ and $K\sim\mathrm{Bin}(n,\eta)$ regardless of its polarization. For $r>0$, the more permissive rule $K\ge k, D\le j$ has field false rejection at most $A^n/(w^k r^j)$. The field bounds allow the incident intensity and polarization to vary with the earlier records.

| Total efficiency | Orthogonal axes | Necessary preparations | Sufficient preparations | Minimum occupied gates, with zero doubles |
|---:|---:|---:|---:|---:|
| 5% | 2 | 9,070 | 10,836 | 505 |
| 5% | 3 | 6,774 | 8,299 | 383 |
| 10% | 2 | 2,180 | 2,794 | 254 |
| 10% | 3 | 1,621 | 2,164 | 194 |
| 62% | 2 | 34 | 65 | 34 |
| 62% | 3 | 24 | 53 | 27 |

Both columns target at most 5% field false rejection and at least 95% power for independent clean preparations. For the calibrated triad with absolute dot products at most 0.05, 2,400 preparations, at least 216 occupied gates and zero doubles suffice at 10% efficiency. For an ideal triad and an independent source whose average-over-axis double probability is at most 0.0002 and whose total occupancy is at least 0.10 on every preparation, 9,000 preparations, at least 819 occupied gates and up to five doubles give power above 0.9877. Take $r=1/2$. A union bound on the two binomial tails allows correlation between occupancy and doubles within a gate.

For necessity, take an unpolarized single excitation and a classical competitor that chooses a signed eigenpolarization uniformly from the $2L$ possibilities before the analyzer selection. Its $d=m y^2$ and its left-only and right-only probabilities are equal in each measured basis. Choose
$$
y=\frac{\eta}{1+\sqrt{(1-\eta)(1-m\eta)}}.
$$
This solves $(2y-y^2-d)/(1-d)=\eta$. Conditional on seeing no double, the competitor then produces exactly the clean distribution, including axis, left/right and empty labels. On independent trials the classical distribution contains the entire $n$-trial clean distribution with weight $(1-d)^n$. Consequently the classical rejection probability of *any* fixed-sample rule with 95% clean power is at least $0.95(1-d)^n$. Each necessary entry is the first integer for which this bound is at most 0.05. A one-axis instrument permits exact imitation by the random signed eigenpolarizations at every $0<\eta<1$. If the current axis leaks to the source, the same construction defeats even the triad.

For fixed $m>0$ the lower bound grows as $4\log(19)/(m\eta^2)$ at low efficiency. The field rule achieves the same inverse-square order. For example choose $k=\lceil3n\eta/4\rceil$, $r=0$. With $y_0=\eta/2$, the log size bound per preparation before rounding is $\log A-(3\eta/4)\log w=-m\eta^2/8+O(\eta^3)$, while the excitation miss probability is at most $e^{-n\eta/32}$. The constants of the upper and lower bounds need not coincide.

A direct hardware control sends a stable linearly polarized input aligned with one analyzer axis and measures full occupancy and doubles in all three settings. Occupancy should track the same total throughput. Doubles should occur in the other two settings for a sufficiently bright input. Repeat with a circular input and test for shared bank dead time. These calibrations and independent source preparations would be needed to apply the result to a walk output. The optical comparison leaves the walk timing, the origin of its probability law, Stage 1 Initial External Grounding and physical identification open.

Run `python -I -B Director_G/persistent_walk/check_polarization_banks.py` from the repository root. The [checker](check_polarization_banks.py) reproduces the [counts and thresholds](polarization_banks_output.json) using exact binomial arithmetic, directed powers, a labeled field-mixture check and explicit adverse controls.
