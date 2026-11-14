# What an unread local record fixes about a site detector

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Suppose a detector scores each well by the **same unknown scalar function** of its total squared amplitude across rails and unobserved registers. A change at a distant well should leave this detector's original-launch rate alone. A family of routed walk experiments then forces the score to be affine on each tested dyadic grid. One empty-well measurement fixes the intercept. This removes the power-law assumption from the [bare-walk remote tests](Remote_position_counts_and_the_spatial_probability_law.md), at the cost of a programmable source and routing. No physical data for this family have been acquired.

## Two routes, four settings and one observed well

Start at $x=0$ on rail R with $m$ zero label bits and a separate blank flag. Apply a real Hadamard to each label bit, giving $N=2^m$ orthogonal labels of amplitude $1/\sqrt N$. The label bits stay protected. Coherent, label-controlled rail permutations can route different labels through the same two-rail lattice. Assume these operations, stable memory, local balanced coins and ballistic straight or turnaround commands. A fixed Hadamard at every step without those controls does not prepare this experiment. The final detector ignores both types of register. In the kinematic calculation, sums over orthogonal labels are made **before** applying the site response. Applying that response to each classical label and averaging describes a different preparation law.

Write $u=1/N$. Choose $k=2,\ldots,N-1$. The same $k$ labels enter the local apparatus in both source wirings, leaving a strictly positive spectator mass $s=(N-k)u$. The following nine streamed ticks suffice following the label preparation.

1. In the first six ticks, the $N-k$ spectators move R each time. The active labels follow the directions R,L,R,L,L,R and hence finish at zero on R. In wiring B, a single designated active label follows R,L,R,L,R,L instead, finishing on L. Wiring A uses the first path for all $k$ labels. The conditional permutations preserve the labels and produce no residual route record other than the stated coordinates.
2. At tick seven apply the balanced coin at zero and stream. The two arms reach $+1$ and $-1$. Pick either the identity or an XOR of the **position predicate $x=1$** into the blank flag at this surface. Leave the flag unread for all remaining operations.
3. Turn the active rails around and stream back to zero at tick eight. Apply the balanced coin and stream once more to the two output wells at tick nine. Spectators continue straight to $x=9$. A local choice at $+1$ has two ticks left and cannot reach this read through the walk. Independent selection of the late setting, isolation of the actual distant read and a common terminal clock are operational conditions.

Take a fixed finite detector bank, for example a 20-well ring with the same three named wells and no path from the switch to the spectator in the last two ticks. The kinematic masses at the dark/bright output pair and the spectator are

| Route and late setting | $-1$ | $+1$ | $9$ |
|---|---:|---:|---:|
| A, blank | $0$ | $ku$ | $s$ |
| A, unread copy | $ku/2$ | $ku/2$ | $s$ |
| B, blank | $u$ | $(k-1)u$ | $s$ |
| B, unread copy | $ku/2$ | $ku/2$ | $s$ |

The intervening turnaround exchanges the two rails. With a blank flag the local coin product is $HXH$, diagonal with entries $+1,-1$. With a copy, the two paths carry different flags at their second balanced coin, so each input label contributes half of its mass to each local output. The spectator has the same label-resolved amplitudes in all four trials. All other wells are empty. A detector can first choose a protected label uniformly, apply any positive power to its internal site and flag masses, normalize within that label, then report its site. For each label all populated final cells in these four settings are either deterministic or equiprobable, so every exponent gives ordinary site rates, including the dark control. This tests the logical role of one shared normalizer across all labels. A global normalization of separately powered labels defines yet another response. This calculation requires the signed kinematics and the specified site grouping. It has not used a rule for converting the masses to observed outcomes.

## A finite characterization with a measured boundary

Let $f(w)$ be finite, nonnegative, strictly positive for each nonempty mass in use, and common across participating wells and settings. For each complete panel set
$$P_i=\frac{f(w_i)}{\sum_j f(w_j)}.$$
This class allows $f(0)>0$. Require complete, normalized counts on the common detector bank, or a justified reconstruction of these original-launch probabilities. A fixed positive spectator efficiency multiplying its original-launch rate preserves each exact equality. Conditioning on clicks across the whole bank generally does not. Untested setting-, label-, or history-dependent detectors need additional calibration. The assumption is one stable score, not an arbitrary mixture of normalized score laws across launches.

Denote the four spectator rates by $r_A,r_{A'},r_B,r_{B'}$, with primes for copies. The common scalar response predicts $r_{A'}=r_{B'}$, which can itself be checked. The two operational locality tests ask for $r_A=r_{A'}$ and $r_B=r_{B'}$. Since all four rates have the same positive numerator $f(s)$, the blank settings then have equal normalizers. Their difference is exactly
$$f(ku)+f(0)-f((k-1)u)-f(u)=0.$$
Writing $h_i=f(iu)-f(0)$, the recursion gives $h_i=i h_1$ for all $0\le i<N$. The empty bank sites contribute the same terms on both sides even if their scores are positive. Conversely an affine score on **all the occupied panel arguments**, including half-grid values in the copies, and at zero makes every remote rate invariant because all kinematic masses sum to one. Finite data also constrain the odd half-grid points used by the copies; no claim of uniqueness away from the checked arguments follows. The grid result needs $2(N-2)$ late-setting comparisons. It uses neither a measured local bright probability nor a symmetry that fixes its value.

An independently verified zero original-launch rate at any physically empty site forces $f(0)=0$ if that read has positive calibrated efficiency. The conclusions then give $f(i/N)=i f(1/N)$ for $1\le i<N$. Every normalized output table whose masses are on this grid has ordinary position probabilities, including a sharp table: at $w=1$, any positive value of $f(1)$ gives the sharp occupied site probability one. With $f(0)>0$, the response $f(w)=w+1/20$ passes every remote invariance test and assigns nonzero rates to empty wells. For $N=4,k=2$ on 20 wells its spectator rate is $11/40$ in all four settings. At the same point a squared-site score gives $1/2$ on A blank and $2/3$ on A copy.

Even the zero-probability dark control leaves a distinct competitor when the fixed scalar-score premise is relaxed. Let a marker hold its label, follow deterministic switches and choose either exit of each balanced coin fairly. It ignores the flag. The spectator then has exactly its ordinary rate $s$ in all four settings. Sites outside the route remain dark. At $x=-1$ in wiring A with the blank flag, however, this marker gives $ku/2$ while the coherent flight gives zero. If a setting-independent fraction $c$ of launches are fair markers, the remainder uses a single score, and an unused-well test has fixed $f(0)=0$ for that component, this one local read gives $c=2P_{-1}/(ku)$ at calibrated positive efficiency after correcting for misses. Each remote contrast of the fair component is zero by itself. When $c<1$ the exact invariance conditions therefore constrain the score component just as above.

Across nested grids with a common stable score the affine slopes agree at $1/2$, fixing one affine function on every dyadic mass below unity. A continuous score extends that equality to $[0,1]$. Monotonicity on the whole interval suffices on its interior by squeezing between dyadics; it leaves the full-occupancy endpoint convention free unless continuity there is required. Without regularity, even all dyadic experiments can coexist with a score changed on a single non-dyadic mass. At finite $N$, a smooth positive bump supported in an open interval avoiding every tested grid and half-grid value passes as well. No finite panel or scalar-score theorem selects a general noncontextual probability law on arbitrary preparations.

## Finite errors and controls

The error can be expressed in observable reciprocal rates. For the ideal detector class,
$$
\frac{f(ku)+f(0)-f((k-1)u)-f(u)}{f(s)}
  =\frac1{r_A}-\frac1{r_B}.
$$
Thus $|r_A-r_{A'}|\le\epsilon_A$ and $|r_B-r_{B'}|\le\epsilon_B$ give a residual at most $(\epsilon_A+\epsilon_B)/(r_A r_B)$ in units of $f(s)$. If copy-rate matching itself is allowed a measured error $\epsilon_C$, add it to the numerator. Use true rates or joint bounds and positive lower limits for the two blank-setting rates. With $E_k$ the resulting bound in units of $f(s)$, summation gives
$$
|h_i-i h_1|\le\sum_{k=2}^i f((N-k)u) E_k.
$$
A small spectator fraction can limit precision. Turning this dimensioned consequence into an absolute score error requires a scale convention and bounds on the score ratios. The source should not treat a null difference from a detector that rarely responds as an exact locality constraint.

The [physical-coordinate checker](check_dyadic_site_score.py) propagates signed integer amplitudes on well, rail, label and flag from a sharp source for $N=4,8,16,32,64$, including every permitted $k$ and all four settings. It retains the affine background and squared-site alternatives, and an interval that a finite $N=8$ panel misses. The [Lean recurrence](lean/DyadicSiteScore.lean) checks finite-grid propagation for an integer-scaled score. [All original rational predictions](results/dyadic_site_score.json)

Earlier [protected-record comparisons](Protected_records_and_coordinate_weights.md) treat unrestricted probabilities on fully specified coordinates with stronger matching, covariance and preparation-equivalence controls. The [separate-rail theorem](Separate_rail_scores.md) uses faithful oriented parent-to-daughter transport across successive clocks and scores signed rail totals independently. Here both output rails and register values contribute to one site's mass, the comparison is at one terminal clock, and response dependence on that mass is an explicit restriction. Other reconstructions use their own ensemble and composition assumptions. [Masanes, Galley and Müller](https://www.nature.com/articles/s41467-019-09348-x)
