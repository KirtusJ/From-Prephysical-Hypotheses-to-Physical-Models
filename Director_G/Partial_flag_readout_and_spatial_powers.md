# Does the spatial probability test survive a finer reading of the flag?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A local position recorder can change how a nonlinear probability law treats a site. A detector might apply its power law to a site total, or apply it to the two flag cells and then add their probabilities. Five ticks admit an exact false pass from these choices alone. Seven ticks give a test for which every choice has the same sign. A nine-tick ring control extends the inference to powers approaching zero. Each comparison uses only a sharp launch, balanced forward ticks, a blank one-bit record and a final position read. [Locality test for the original walk](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/91)

## Readout convention and the first failure

Start at $(0,R)$. The coin sends $(r,l)$ to $(r+l,r-l)/\sqrt 2$ and the rails move right and left. At a specified time, toggle a blank bit on the marked well without resolving the rail. Its two final values are orthogonal. At site $x$ let $(a_x,b_x)$ be the two nonnegative squared-rail-sum numerators on the original denominator $2^T$. A readout can resolve the two flag cells or combine them as $(a_x+b_x)$. Independently at each site allow either choice. Given the resulting nonzero cells $v_i$, the tested family samples them in proportion to $v_i^q$, $q>0$, then reports the site. Write $Z(q)=\sum_i v_i^q$. The exponent distribution is common across the controls. The cell partitions can vary with site, experiment, exponent and launch. All reported probabilities use the original launches, with physical detection efficiency and any losses controlled in the interpretation. This model assumes Born-form *kinematic* sums within each of two orthogonal records. Arbitrary resolving of rail, histories or subcells is a different readout family.

After marking $-2$ at tick 2 and reading at tick 5, the bare site numerators are $(1,5,4,4,17,1)$. In the same order from $-5$ to $5$, step two, the marked pairs are
$$(0,1),(0,5),(1,1),(5,1),(17,0),(1,0).$$
At $q=2$ the bare denominator is 348. The fully combined readout gives 356 and the fully resolved one gives 344. Choose the combined readout with probability $89/261$ and the resolved one otherwise. Then $E[1/Z_{\rm marked}]=1/348$. Every remote site, whose populated cell is identical across arms, passes the comparison at this wrong exponent. [Complete signed paths and exact partition denominators](results/spatial_flag_partitions.json)

## Seven ticks constrain every partition

Mark site $1$ just after tick 5. At tick 7 the position numerators are as follows, in increasing order from $-7$ to $7$:

| | $-7$ | $-5$ | $-3$ | $-1$ | $1$ | $3$ | $5$ | $7$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bare | 1 | 17 | 5 | 9 | 17 | 41 | 37 | 1 |
| Flag 0 | 1 | 17 | 5 | 13 | 13 | 25 | 37 | 1 |
| Flag 1 | 0 | 0 | 0 | 4 | 8 | 4 | 0 | 0 |

The sorted affected bare triple $(41,17,9)$ strictly majorizes the combined marked triple $(29,21,17)$: the totals agree and the first two partial sums are larger. Splitting any marked cell into two nonnegative parts can only reduce those partial sums after sorting and padding with zeros. Thus bare strictly majorizes every partition. For $q>1$ strict convexity of $z^q$ gives $Z_{\rm bare}>Z_{\rm marked}$, and for $0<q<1$ strict concavity gives the reverse. Equivalently, the inequality for the triples follows by transferring mass from larger to smaller entries, and can only be strengthened by splitting. [Karamata's inequality and strict convexity, Theorem 2.3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6133051/)

Sites 5 and 7 are outside the two-tick cone of the mark. Each has only a single populated flag cell, with unchanged numerators 37 and 1. Subtract 37 times the change in rate at 7 from the change at 5, each change taken as marked minus bare. For given $q$ and partition $p$ this gives
$$L(q,p)=(37^q-37)(1/Z_{\rm marked}-1/Z_{\rm bare}).$$
Both factors have the sign of $q-1$. Consequently $L>0$ at every finite positive $q\ne1$, in all eight partitions. It vanishes at one and approaches one as $q\to\infty$ because the bare maximum is 41 and the unique marked maximum is the remote 37. Both equal remote rates under a stable mixture therefore force $q=1$ almost surely for positive exponents. This uses linearity in the frequencies of separate launches. It allows the partition and exponent to be correlated.

## The support limit and a ring control

At $q=0$ define a readout by uniform sampling of cells of positive mass, the right-hand limit. The fully combined seven-tick experiment has the same support size in both arms, so $L(0,p)=0$ for that choice. It also admits arbitrarily small contrast near zero. A separate finite control can address this endpoint.

Take an eight-well periodic ring with the same balanced coin. After seven ticks mark well 1 and after two more read the odd wells. Distances are measured on the ring. Well 5 is four edges from the marked well, outside its two-tick cone.

| Site | 1 | 3 | 5 | 7 |
|---|---:|---:|---:|---:|
| Bare | 0 | 128 | 256 | 128 |
| Flag 0 | 32 | 80 | 256 | 80 |
| Flag 1 | 32 | 16 | 0 | 16 |

Let $J(q,r)$ be the remote site-5 frequency **bare minus marked** at ring partition $r$. At order zero bare has three positive cells and marked has at least four. Hence $J(0,r)\ge1/12$. At $q=1$ it vanishes. Bare strictly majorizes the combined marked list $(256,96,96,64)$ and hence all its partitions, so $J\ge0$ on $[0,1]$ and $J<0$ for $q>1$. If $E[L]=0$, only $q=0$ or $1$ can survive. Requiring $E[J]=0$ eliminates the endpoint at zero. **The same distribution of exponents on the line and the ring is a substantive cross-apparatus premise.** A common large periodic device that implements a line segment and an eight-site ring still requires this stability.

There is also a finite-error statement uniform over all partitions. Write $J^- = \max(0,-J)$. There is a finite $K$ such that $J^-(q,r)\le K\sqrt{L(q,p)}$ for all $q\ge0$ and all pairs $p,r$. For $q\le1$ the numerator is zero. Near $q=1$ the strict majorization gives $\sum v_{\rm bare}\log v_{\rm bare}>\sum v_{\rm marked}\log v_{\rm marked}$ on the line (zero terms are zero). This is the positive derivative at 1 of $Z_{\rm bare}-Z_{\rm marked}$. Hence $L$ has a strictly positive quadratic coefficient there, while $J$ vanishes at least linearly. At infinity $L\to1$ and $|J|\le1$. Continuity on the remainder and the finite family of partitions give the bound. For different partition distributions in the two apparatuses one can couple them in any way conditional on their common $q$.

Suppose the two line-rate changes have magnitude at most $e_7$ and the ring change has magnitude at most $e_9$. Then $E[L]\le38e_7$. Choose $\delta\in(0,1)$ with $J\ge1/24$ on $[0,\delta]$ for every partition, which exists by continuity. Cauchy–Schwarz gives
$$\Pr(q\le\delta)\le24\bigl(e_9+K\sqrt{38e_7}\bigr).$$
Away from this interval and any chosen neighborhood of one, the minimum of $L$ over all partitions is positive, including its limit at infinity. Dividing $38e_7$ by that minimum bounds the remaining unwanted mass. The perturbation estimates state existence of uniform constants. They do not constitute an apparatus precision estimate. An additional ordinary path-count component is invisible to the remote locality equalities when it propagates causally. These bounds then address the powered component with its mixture weight, and its identification requires a separate local read.

The independent word checker enumerates every direction history with its sign, final rail and recorded bit, plus every within-site partition. The Lean calculation checks all majorization certificates at seven and nine ticks on the extracted integer columns. Neither check establishes a physical locality equality. [Checker](check_spatial_flag_partitions.py) · [Exact records](results/spatial_flag_partitions.json) · [Lean proof](lean/SpatialFlagPartitions.lean)
