# Three forward ticks can test a hidden branch normalization

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [routed-bit experiment](Mixing_a_stored_label_at_two_sites.md) needed three extra routing bits to arrange the different site populations. A detector that normalized separately inside every complete routing label could evade it. The ordinary walk itself produces suitable multiplicities. Three forward ticks suffice for an exact comparison, six give sensitivity even at extreme exponents, and eight give an exact comparison inside both terminal rails. Each experiment uses one coherent branch bit in addition to the walk. No persistent bit labels the routes taken.

## A general calculation for these walks

Start the walker on R at site zero. On each tick use the real signed Hadamard and stream R right and L left. The branch bit can be prepared as $(|0\rangle+|1\rangle)/\sqrt2$ independently at launch or at the terminal surface before the two local operations. Let $\psi_{xc}$ denote the walk's outgoing spinor in unnormalized integer coordinates and $n_x=\sum_c|\psi_{xc}|^2$. Idle evolution of the branch bit leaves two identical rows. Select two wells with equal mass $m>0$. Place a fixed phase flip on branch 1 at the second of these wells. The variable setting is identity or a branch Hadamard simultaneously at the two wells, with no additional streamed tick before the final read. Thus the local vectors $(a,a)$ and $(b,-b)$ become $(\sqrt2 a,0)$ and $(0,\sqrt2 b)$ for each incident rail. Every total site mass and even every rail-resolved site mass is unchanged. Remote spinors are unchanged entry by entry.

Omit the common scale from the rows. Before the basis switch each branch has two local masses $(m,m)$. Afterwards their local masses are $(2m,0)$ and $(0,2m)$ respectively. A law that normalizes the powered site masses separately inside each branch assigns *the same remote rates in both branches* at a given setting. Thus arbitrary branch weights, including ones that vary by setting or with the exponent, cancel. Original-launch remote reads must cover the same incident exponent measure across settings and monitors. The late switch must be local relative to the reads in the physical apparatus; it is an additional reversible control beyond the unmodified balanced ticks.

Take two positive remote masses $A>B$. Write $Z_0(q)$ for the idle sum of powered masses in either row and $Z_1(q)=Z_0(q)-2m^q+(2m)^q$. The differences in the remote rates, idle minus mixed, are $A^qD$ and $B^qD$, $D=1/Z_0-1/Z_1$. Consequently their contrast is
$$
W(q)=\big[A^q-(A/B)B^q\big]D(q).
$$
Each factor has the sign of $q-1$. Equality of both remote rates therefore forces an intervention-independent mixture of positive exponents to be supported on $q=1$ under this branch-normalized law. A component using any fixed score after both branches are aggregated contributes zero to the contrast. So does a fair marker unaffected by operations on the local bit. If those components are present, the conclusion concerns the subprobability of launches using the branch-normalized rule. This test measures which labels the candidate normalization can resolve. Its affirmative prediction for the ordinary rule uses only the calculated equality of its two site tables.

## Three ticks and a ten-well recurrence at six ticks

After three ticks on the line the signed pairs at $x=-3,-1,1,3$ are $(0,1),(-1,0),(2,1),(1,0)$. Use $-3,-1$ as the local wells, $1,3$ as the remote monitors. Then $m=1,A=5,B=1$. At $q=2$, $W=1/21$ per original launch. The large-$q$ contrast tends to zero since the same site with mass five dominates both settings. In the protocol that needs two distinct occupied local wells and two distinct occupied monitors this is the earliest possible tick: at times zero, one and two a sharp launch occupies at most one, two and three sites. This counting bound says nothing about designs using another read.

On a ring of **ten wells**, ordinary wrapped walks from the same source instead give this six-tick field:

| Well | 0 | 2 | 4 | 6 | 8 |
|---|---:|---:|---:|---:|---:|
| R numerator | $-2$ | $2$ | $5$ | $2$ | $1$ |
| L numerator | $-2$ | $3$ | $0$ | $-3$ | $2$ |
| Site mass numerator | $8$ | $13$ | $25$ | $13$ | $5$ |

Use local wells 2 and 6 and monitor wells 4 and 8. Thus $m=13,A=25,B=5$, including an unchanged site of mass eight in both normalizers. At $q=2$ the sums are 1052 and 1390 and $W=4225/36557$. At $q\downarrow0$ the five occupied wells in each idle row become four in each mixed row, so $W\to(1-5)(1/5-1/4)=1/5$. At $q\to\infty$ the unique maximum moves from the remote 25 to a local 26, giving $W\to1$. Since $W$ extends continuously at zero and infinity, $c_\delta=\inf_{q>0,|q-1|\ge\delta}W(q)>0$ for every $\delta>0$. A simultaneous experimental upper bound $e$ on the contrast gives $\nu(|q-1|\ge\delta)\le e/c_\delta$ for the component under test. Quantitative use needs calibrated relative monitor efficiencies. Rates are measured on fresh original launches, at the same output surface, with misses included. A measurement conditioned on reporting some position can itself change the normalizer.

## What if the detector resolves both branch and rail?

The preceding three-tick test was designed on the basis of two-rail site totals. It cannot simply be applied to a detector normalizing independently in each $(\ell,c)$ block: the two local mass-one wells there occupy different rails. A second preparation needs no new register. On a line or ring of at least 18, after eight ticks the native signed pairs are

| $x$ | $-8$ | $-6$ | $-4$ | $-2$ | $0$ | $2$ | $4$ | $6$ | $8$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R | 0 | 1 | 3 | $-3$ | 3 | $-5$ | 9 | 7 | 1 |
| L | $-1$ | $-5$ | $-1$ | 3 | $-3$ | 1 | 5 | 1 | 0 |

Switch the bit at $x=-2,0$ with opposite preparatory sign as above. Each local well has $m=9$ on **each** rail. This time read the individual remote rails. Within R use $A=81$ at 4 and $B=1$ at 8. Within L use $A=25$ at 4 and $B=1$ at $-8$. The two contrasts are $\Delta_{4,R}-81\Delta_{8,R}$ and $\Delta_{4,L}-25\Delta_{-8,L}$. Suppose the measure $\nu_c(dq)$ of launches assigned to rail $c$ is stable across settings, with arbitrary conditional branch allocation within rail. The measured contrasts are $\int W_R\,d\nu_R,\int W_L\,d\nu_L$ respectively. Both have strictly positive integrand away from exponent one. If both vanish, each rail's measure is concentrated at one; the measures need not coincide. A model choosing different exponents on different rails is included. Choosing new rail proportions according to the setting can introduce a separate selection effect. A verified absolute rail calibration or a justified comparison of probabilities conditional on the same rail is then needed. The statement also requires the specified rail labels at each monitor. No conclusion follows from canceling uncalibrated relative gains across remote cells.

At $q\to\infty$ the dominant remote cell at site 4 in each rail exceeds $2m=18$. Both contrasts tend to zero. This is a genuine loss of uniform sensitivity for the rail-refined panel, so finite errors at eight ticks cannot give the uniform tail claim proved for the two-rail site totals at six ticks. Beyond the specified spatial, bit and rail coordinates a device can still condition on inaccessible histories or other environmental information. The full joint probability, rail mixing weights, admissibility of local bit control and physical identification remain open.

## Why routing labels cannot just be deleted

For two orthogonal routing records $|a\rangle$ and $|a'\rangle$ with otherwise identical output coordinates, a unitary cannot send both separately to the same blank record and the same rest of the apparatus: it preserves their zero inner product. It *can* undo the preparation of one known coherent superposition in a block, or move distinguishability to another observed coordinate or to the environment. An equal positive superposition over a complete binary subcube can be cleared with Hadamards on the corresponding bits if the block is known and its amplitudes and phases match. For a uniform three-label subset of a two-bit register the overlap squared with the zero cell after the two-bit Hadamard is $3/4$, leaving $1/4$ elsewhere. Thus even clearing the originally prepared four-bit source of the routed construction is not equivalent to clearing each of its final destination blocks. Simply tracing out an enduring route record supplies no coherent erasure. The three experiments here use physical interference of native paths to prepare the scalar entries directly. Given the stipulated isolated walk, their explicit coherent state has no routing index.

The [direct checker](check_walk_branch_switch.py) enumerates the real-space signed updates and both bit settings on the actual rings, verifies every invariant coordinate and branch spectrum, and retains finite and infinite-exponent outcomes separately for both rails. The [Lean check](lean/WalkBranchWeights.lean) computes the six-tick ten-well signed field and the exact square-power contrast. [Exact rational controls](results/walk_branch_switch.json) · [Orthogonal route records and a coarse detector](Protected_records_and_coordinate_weights.md)
