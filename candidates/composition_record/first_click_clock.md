# What the first two detection times can say about the walk's probability rule

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical construction, independent challenge and computational checks with OpenAI Codex.

A detector can assign the three-step walk's largest well a hit probability of $2/3$ on some launches and $7/12$ on others. A fair mixture gives the ordinary $5/8$ even when every terminal well is reported. A clock gives another observable. Record the first detection in two successive opportunities, including every launch with no detection. Under a specific relation between the clock and the cell scores, those counts measure a **mean squared difference** between the direct and split detector responses. No apparatus mode has to survive from one launch to the next. The critical assumption concerns what happens *within* a launch after the first opportunity passes without a detection. [Terminal-table counterexample](spectator_refinements.md) · [Earlier test with a coherent pointer](light_probe_extrapolation.md)

## Prepare once and hold one setting

Launch the right rail at the origin. Three Hadamard-and-shift ticks give whole-well masses $(1,1,5,1)/8$. The heavy well contains rail masses $4/8$ and $1/8$. Write a tag for the three minor wells, of total mass $r=3/8$. Choose the direct arm $U$, which pools the heavy rails, or the split arm $S$, which resolves them. The earlier five-tick routing construction gives both arms the same flight duration and a position read at the far station. These routing ticks precede the detection opportunities below. [Signed rails, controls and resolution](held_split_comparison.md#a-three-tick-walk-supplies-both-settings)

Suppose a fresh apparatus mode $F$ supplies nonnegative nondecreasing scores $f_F(w)$, with $f_F(w)=c_F w$ on each calibrated small cell and $c_F>0$. Use the same incident-mode law for independent assignments to both arms. For the two detection opportunities postulate a common positive exposure factor $g_F$ such that the per-opportunity total chances in the direct and split arms are

$$a=g_F[f_F(1-r)+c_F r],\qquad b=g_Fc_F.$$

Require each cell's absolute click chance per opportunity to be its unnormalized score times the same exposure factor. These chances sum to at most one. The three protected minor cells then each contribute $g_F f_F(1/8)$ and together contribute $rb$ in either arm. The two totals alone would not specify the mark. A compatible detector reports the heavy cell with direct conditional probability $p_F=1-rb/a$ on a click. This link between **absolute chances per opportunity** and the direct detector's relative scores is a physical hypothesis. A downstream clock started by an already chosen outcome has no reason to obey it.

Leave the assigned arm in place for both opportunities. Conditional on the mode and survival, the second opportunity must retain the same total chance. The second direct opportunity must also retain minor chance $rb$. No law for an unrecorded second hit following a first hit is needed. The packet must remain available at the intended read coordinates, or be restored for a second opportunity following a miss. For example, a swap followed by the conditional shift is an involution on position and rail. Two such coherent ticks restore the coordinates between exposures when a null result leaves the packet unchanged up to a scalar. This echo cannot restore amplitudes selectively removed by the first exposure. Record the incident denominator, setting, first detection opportunity and well, or final timeout. A genuinely missed read with unknown status belongs in the uncertainty accounting.

## Two arm totals and one marked second detection

Write $Q_{Xj}$ for the fraction of *all incident launches in arm* $X$ with no detection by opportunity $j$. Let $M_{U2}$ be the incident fraction with first detection at opportunity two in a minor well. In population units the observable is

$$C=Q_{S2}+Q_{U2}-2Q_{U1}+\frac{2}{r}M_{U2}.$$

Conditional on $F$, substitute $(1-b)^2$, $(1-a)^2$, $1-a$, and $(1-a)rb$ in this order. The expression is $(a-b)^2$. Averaging then gives

$$C=\mathbb E (a-b)^2.$$

Thus an exact population zero forces $f_F(5/8)=c_F(5/8)$ almost surely on this model. A finite sample needs an uncertainty bound on the signed contrast, which can be negative by sampling error. When $C\le L$ is established at population level, the **first-opportunity detected population** satisfies

$$\mathbb E_{\rm click}|p_F-5/8|
 =\frac{r\,\mathbb E|a-b|}{\mathbb E a}
 \le \frac{r\sqrt L}{1-Q_{U1}}.$$

Here the conditional mode weights are proportional to $a$. Extending a finite-error result to all launched modes requires some control of nearly blind modes. For instance if $a\ge a_0>0$ almost surely, then $\mathbb E(p_F-5/8)^2\le r^2 L/a_0^2$. Absolute continuity of the type distribution across different preparations is a separate question. On a common population, repeating exact population-zero tests on all achievable masses in a countable dense subset of $(1/2,1)$ would extend small-cell linearity through that open interval by monotonicity. The weight of the sole cell of mass one always cancels. Interpreting a sequence of recorded positions as a classical trajectory further requires joint records and control of their disturbance across the flight. [Conditional transfer to trajectory records](refined_reflecting_histories.md)

The named fair rival has $b=1/2$ in both modes and $a=9/16$ or $9/20$. Its conditional heavy fractions are respectively $2/3$ and $7/12$. Its predicted $C$ is $41/12800$. This example's first-bin totals already differ in their means. The square identity also separates a pair that defeats the entire first-bin test: choose $a=9/20$ in both modes, and $b=2/5$ or $1/2$ with equal chances. Every first-bin outcome, including timeout, has the ordinary pooled probability for rate $9/20$, as does the fair mean of the separately normalized heavy fractions. Holding that mode through the second opportunity gives $C=1/400$.

## How the same timestamp can mislead

**Port-dependent absorption.** Consider ordinary readout on the actual heavy-right, heavy-left and minor sectors of masses $4/8,1/8,3/8$. In $U$, each sector clicks with chance $1/2$ per opportunity. In $S$, take per-sector chances $3/8,1,1/2$. Use a diagonal no-click filter that multiplies each amplitude by the square root of its survival chance and reapply the same filter. The first total and minor chances agree exactly between arms, at $1/2$ and $3/16$. The direct second-bin correction relative to its ordinary minor share vanishes. Split survival after two opportunities is $37/128$, while direct survival is $1/4$. The measured contrast is $5/128$ even though the two first-bin totals match and the detector uses ordinary quantum probabilities. The surviving split packet now contains a different mixture of rails. Conditional evolution after a null result appears explicitly in the quantum-jump treatment of photodetection. [Dalibard, Castin and Mølmer](https://doi.org/10.1103/PhysRevLett.68.580)

One can bound this effect if the apparatus has independent calibrations. Write $a+u,b+v$ for the second total chances conditional on survival and $rb+w$ for the second direct minor chance, all at fixed $F$. The contribution to $C$ differs from $(a-b)^2$ by

$$-(1-a)u-(1-b)v+\frac{2}{r}(1-a)w.$$

Bounds on the three terms give an explicit allowance in either direction. A common pooled first-bin calibration alone gives none for the mode-conditional drift. A physical check on one necessary condition is possible from a single arm. Under any mixture of stationary per-opportunity hazards $s$, its incidence at opportunity $j$ is $\mathbb E[s(1-s)^{j-1}]$. Such incidences must decrease or stay constant. A complete published record of monitored returns can test this restriction directly. [Published three-qubit records and reanalysis](first_return_data/README.md)

**Redraw after a miss.** Use the second fair pair above but redraw the sign independently at each opportunity. In each arm the one-opportunity distribution, ordered as minor, heavy, and no click, averages to $(27,45,88)/160$. A fresh independent draw on survival repeats that same kernel. Every direct/split setting word, including a later setting chosen after no click, gives the ordinary marked first-detection law. At two opportunities the complete record probabilities are

$$\left(\frac{27}{160},\frac9{32},\frac{297}{3200},\frac{99}{640},\frac{121}{400}\right)$$

in order first minor, first heavy, second minor, second heavy, and timeout. When the arm splits the heavy well its internal labels can be sampled in the ordinary $4:1$ ratio. The three separate minor wells retain their ordinary equal shares in both arms. The direct heavy fraction in each individual mode is still $2/3$ or $7/12$. No two-setting timing comparison alone can exclude this implementation.

**A clock independent of the scoring mechanism.** Even a continuous timestamp can be drawn from one common arbitrary law on every launch, independently of the mode. At the time of detection, let the fair terminal sampler choose the well from the stipulated table. Conditional on the timestamp and past records, averaging the signs gives every ordinary cell probability. Including timeouts, changing the remote gate, or adding independent arrival deadlines preserves this equality whenever the instantaneous pre-read table and common clock carry no information about the sign. A source that splits one pulse into early and late half-mass replicas changes the scoring cells themselves and cannot calibrate a direct heavy-cell rate by this maneuver.

## A bounded experiment if the apparatus uses continuous time

Some apparatuses have rates per unit time. For these let $a,b>0$ denote constant first-event hazards conditional on $F$ in the direct and split arms. Let the direct minor cause-specific hazard be $rb$ conditional on survival. Hold the routing static during observation. An exponential event law with those constant hazards is a different model from two Bernoulli opportunities. Under continuous hazards the direct minor chance in a fixed gate of length $t$ is $rb(1-e^{-at})/a$. It need not equal $r(1-e^{-bt})$.

Choose a passive reporting threshold $D$ uniformly from $[0,H]$ independently on every launch and stop observation at $H>0$. It may be assigned in software after collecting the first-click time. The choice must leave the detector dynamics unchanged. Record whether there was no detection by $D$ and whether the first detection fell between $D$ and $H$, with its minor flag $I$. Let $\Phi(s)=H^{-1}\int_0^H e^{-st}\,dt$. The split rate of survival to $D$ minus the direct rate, plus the direct-arm mean of $\mathbf1_{\{D<T\le H\}}(I/r-1)$, has the value

$$\mathbb E\!\left[\Phi(b)-\Phi(a)-(b-a)\Phi'(a)\right].$$

Indeed a first detection at time $t\le H$ is in the marked window with probability $t/H$, giving the last term from its direct cause-specific density. The integral makes $\Phi$ strictly convex. This single bounded experiment has a nonnegative mean and equality exactly at $a=b$ almost surely. It requires the event-time/label link throughout exposure. A marginal fit of the time distribution to an exponential curve supplies insufficient information about the labels or the unobserved modes. The two discrete opportunities and this continuous gate specify different physical experiments.

The [integer Rust reconstruction](check_timed_reads.rs) checks full two-opportunity records, the ordinary absorber and all four words for the redrawn rival. The [Lean certificate](ExposureContrast.lean) verifies the cleared polynomial identity, drift correction and rational examples. Neither computation supplies experimental evidence of a score-linked detection clock on the signed walk.
