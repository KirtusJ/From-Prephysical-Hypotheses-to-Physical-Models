# Can a local phase change a remote position count?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A walker starts on the right rail at the origin. After two balanced ticks, choose whether to change the sign of both rails at well $-2$. Three ticks later neither possible influence through the walk nor any altered amplitude has reached wells $3$ and $5$. Count arrivals at those two wells in separate, identically prepared trials of the two settings. Within the family that raises each site's squared amplitude to an unknown positive power and normalizes across the detector, equality of both remote rates selects the ordinary exponent. This remains true if the exponent varies from launch to launch. The test uses one addressed sign, forward ticks, and the original launch denominator. It needs no arbitrary rotation, reverse flight, intermediate position measurement or absolute reference rate. [Earlier spatial comparison and competing law](Two_rail_comparison_for_a_flight_bin.md)

## Five ticks from a sharp source

On the line the local coin takes incoming integer amplitudes $(a,b)$ to $(a+b,a-b)$ on the outgoing right and left rails, which stream one site. The omitted common factor at tick $t$ is $2^{-t/2}$. A flat ring of length at least 16 gives the same tables through tick seven. The binary intervention is a phase at one named well, independently selected after launch and before the next coin. It changes the sign on both rails there. It requires a local phase control in addition to the bare walk. Assume the same prepared input and stable terminal read. The operational premise compares the observed per-launch rates at *each* specified remote well between choices. A detector connected to a global gate or armed by a remote coincidence would need an independent check of that premise. Local choice and propagation through the apparatus concern its actual causal structure. [Beckman et al., causal quantum operations](https://arxiv.org/abs/quant-ph/0102043)

Write $n_x=a_x^2+b_x^2$ at each well. For a fixed exponent $q>0$, the candidate detector has probabilities $n_x^q/Z$, where $Z=\sum_y n_y^q$. On an isolated single well it may use the ordinary conditional proportions on its two rails, passing every single-well rail comparison. More generally take any probability measure $\mu$ on positive exponents. Sample the exponent independently of the intervention. Mixture probabilities are the averages of the *normalized* per-launch laws. This allows a broad class of hidden fluctuations but fixes the meaning of $q$ across settings.

| Five-tick setting | $-5$ | $-3$ | $-1$ | $1$ | $3$ | $5$ |
|---|---:|---:|---:|---:|---:|---:|
| Bare | 1 | 5 | 4 | 4 | 17 | 1 |
| Sign at $-2$ after tick two | 1 | 5 | 0 | 8 | 17 | 1 |

Both rows sum to 32. The column entries are computed kinematic numerators. Under the ordinary law the two monitor rates are $17/32$ and $1/32$ in either setting. For $q=2$ the rates at well $3$ are $289/348$ and $289/380$, even though its entire incident rail pair is unchanged. The rear edge at $5$ has rates $1/348$ and $1/380$.

Let $\Delta_x$ denote bare rate minus marked rate. For an individual exponent write $D=1/Z_{\rm bare}-1/Z_{\rm marked}$. The remote differences at $3,5$ are $17^qD,D$. The sign of $D$ is the sign of $8^q-2\cdot4^q$, which changes at $q=1$. Therefore

$$ W_5(q)=(17^q-17)D\ge0,\qquad W_5(q)=0\quad\Longleftrightarrow\quad q=1. $$

The measured combination $\Delta_3-17\Delta_5$ has expectation $\int W_5\,d\mu$. Equality of the two remote rates between settings at each site forces this integral to vanish. Thus $q=1$ almost surely. No fitted contrast was used in setting the coefficient 17. It is the ratio of the remote site numerators under the ordinary rule. The complete local input is unchanged at either monitor for each launch setting. Observed probabilities still require an experiment.

## Error bounds and a nearly invisible tail

At very large $q$ both five-tick distributions concentrate at well $3$. Each remote difference then tends to zero even though the exponent moves arbitrarily far from one. To give a uniform bound on a mixture tail using finite-precision measurements, use a second addressed experiment. Change the sign at well $1$ after five ticks and read two ticks later.

| Seven-tick setting | $-7$ | $-5$ | $-3$ | $-1$ | $1$ | $3$ | $5$ | $7$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bare | 1 | 17 | 5 | 9 | 17 | 41 | 37 | 1 |
| Marked | 1 | 17 | 5 | 25 | 25 | 17 | 37 | 1 |

Let $W_7$ be the contrast of well $5$ minus 37 times the contrast of well $7$, now taking *marked minus bare*. In the denominator only the pair $(9,41)$ has been replaced by $(25,25)$ up to permutation. Strict convexity of $u^q$ for $q>1$ and strict concavity for $0<q<1$ give the same sign to $Z_{\rm bare}-Z_{\rm marked}$ and $37^q-37$. Hence $W_7(q)\ge0$. At $q\to\infty$ the largest site moves from $3$ to the remote well $5$, so $W_7(q)\to1$. At $q\downarrow0$ each law gives equal weight to its occupied sites. The five-tick settings have six and five occupied sites, giving $W_5\to8/15$. Meanwhile $W_7\to0$.

For $\delta>0$ the infimum $c_\delta$ of $W_5+W_7$ over positive $q$ with $|q-1|\ge\delta$ is strictly positive. The functions extend continuously to zero and infinity by the displayed limits; on the closed remaining set their sum has no zero. With one common exponent law across the two experiments,

$$ \mu\{|q-1|\ge\delta\}\le\frac{\mathbb E W_5+\mathbb E W_7}{c_\delta}. $$

The numerator uses the signed combinations of actual rates given above. A bound from data needs simultaneous upper confidence limits and control of the relative detection efficiencies. An unknown positive site efficiency stable within a setting pair preserves a test that a given difference is exactly zero. Combining nonzero differences with weights 17 and 37 for a quantitative bound needs the efficiencies or adequate bounds on them. Selection on detection anywhere can change every conditional rate. All readouts should count every launch with misses retained. A drift in $\mu$ between the two experiments also invalidates the combined bound.

## Using the walk's position record in place of a phase

The five- and seven-tick experiments can also use a binary position **record**. Supply a blank bit. In one setting toggle it at the named site on both rails; in the other leave it untouched. The walk then proceeds with identical coins, preserving the bit. Sum over both final bit values on every launch. The required coherent operation is the position-controlled pointer permutation already used in the program. A destructive position measurement or a controller that keeps other path information requires separate characterization. [Position records on the walk](Position_transcripts_and_selected_laws.md)

Let $u,v$ be the terminal amplitude columns contributed at a well by paths through the selected site and paths bypassing it. The blank-copy run has joint output columns $u,v$ on different bit values. Its summed kinematic site mass is $\|u\|^2+\|v\|^2$, the average of the bare mass $\|u+v\|^2$ and the sign-marked mass $\|v-u\|^2$. Thus a sign gate can be dispensed with physically; the signed column is a calculation. In this variant the tested laws raise the **whole site's** kinematic mass, summed over rails and both bit values, to $q$. Applying the nonlinear response separately in the two record sectors is a different model.

At five ticks the bare interior pair $(4,4)$ becomes $(2,6)$ in the recorded setting. Every other site is unchanged. Strict convexity or concavity gives the same sign argument as for the phase, so equality at the two remote monitors again forces $q=1$ among positive exponents, including mixtures. At seven ticks the triple $(9,17,41)$ becomes $(17,21,29)$, up to reordering. In decreasing order the two leading partial sums fall from $41,58$ to $29,50$ at unchanged total 67. Equivalently transfer 8 from 41 to 9 and then 4 from 33 to 17. This strictly lowers a convex power sum and raises a strictly concave one. The sign-reversed seven-tick witness is again nonnegative and tends to 1 at large exponent.

The difference at the small-exponent boundary matters. With the blank-copy control all five- and seven-tick wells in those tables are occupied in both settings. Uniform weight on the support ($q\downarrow0$) makes **both** remote witnesses vanish. Finite precision on the line alone therefore gives no bound uniform down to zero. There is a third blank-copy experiment that closes this boundary if the same readout law operates on an eight-well ring. After seven free ticks, toggle at site 1, then read site 5 at tick nine. It is four edges from the control with only two forward ticks remaining. At sites $1,3,5,7$ the bare and recorded kinematic weights are $(0,4,8,4)/16$ and $(2,3,8,3)/16$. The remote bare-minus-recorded rate difference tends to $1/3-1/4=1/12$ as $q\downarrow0$ and is zero at $q=1$.

In detail, let $W$ be the sum of the two nonnegative blank-copy witnesses on the line, and $R$ this last signed difference on the ring. They extend continuously to the compact interval of exponents $[0,\infty]$. The only zeros of $W$ there are $0,1$, and $W(\infty)=1$. On the ring the bare triple $(0,4,4)$ is smoothed to $(2,3,3)$, so $R>0$ on $[0,1)$ and $R<0$ for finite $q>1$. Near 1, $R=O(|q-1|)$. The five-tick term in $W$ has a strictly positive quadratic coefficient, since $17^q-17$ and $2^q+6^q-2\cdot4^q$ have simple zeros there; the derivative of the latter at one is $2\log2+6\log6-8\log4>0$. Consequently $K=\sup \max(-R,0)/\sqrt W$ is finite, taking the supremum where $W>0$. There is no negative part near zero, and $W\to1$ at infinity.

For $0<\delta<1$, put $a_\delta=\min_{[0,1-\delta]}R>0$ and $b_\delta=\min_{[1+\delta,\infty]}W>0$, including the infinite endpoint. For any common positive measure $\nu$ of exponents of mass at most one in all three experiments, let $w=\int W\,d\nu$ and $r=\int R\,d\nu$. The upper tail has mass at most $w/b_\delta$. On the lower tail the integral of the positive part of $R$ is at least $a_\delta$ times the tail mass. Its full integral is $r+\int\max(-R,0)d\nu\le |r|+K\sqrt w$ by Cauchy–Schwarz. Together,

$$\nu\{|q-1|\ge\delta\}\le (|r|+K\sqrt w)/a_\delta+w/b_\delta.$$

The constants depend only on the displayed tables and the chosen tolerance. Simultaneous uncertainty in the five measured remote differences and relative efficiencies must be propagated before applying the bound. A common exponent distribution for the line and ring experiments is a substantive additional premise, even if the same apparatus can realize both geometries.

Fair path counting ignores the blank copy and its remote contrasts remain zero. On the eight-well ring the bare nine-tick site 1 is dark for every positive exponent. The fair walk gets there with one, five or nine right moves, totaling 136 of 512 paths. Its measured rate there is $17c/64$, giving an independent count calibration without a phase or a previously selected exponent. Alternatively, at well $-1$ in the five-tick recorded setting, the ordinary rate is $2/32$ and the count rate is $10/32$. After remote invariance has confined the exponent mass to $q=1$, a rate $r$ there implies $c=4r-1/4$. These tests need a stable detector and original launch counts.

## What a clock comparison alone tests

Even without a phase switch the pure $q=2$ candidate has an early obstruction if a persistent position moves at most one well per tick and terminal reads faithfully sample its unprobed marginals. At tick two $1/6$ of its mass is at $-2$. At tick three both reachable wells $-3,-1$ together carry only $2/28=1/14$. Any such coupling would have to carry at least $2/21$ of the launch mass to an unreachable position. Changing the two normalized marginals by total variation errors $e_2,e_3$ still requires $e_2+e_3\ge2/21$ to repair this cut. This inference uses a cross-clock position and readout premise. The local-choice experiments compare two settings at the same clock and require no unmeasured particle path. [Eckstein and Miller, causal coupling of probability measures](https://arxiv.org/abs/1510.06386) · [Position paths with ordinary marginals](Rank_paths_and_classical_flight.md)

## A count component in the same experiment

A finite-speed marker choosing either direction fairly on every tick ignores the sign. It gives identical remote rates in both controls. Include a fraction $c$ of these launches and a positive measure $\nu$ of exponent launches with total mass $1-c$. Every remote contrast from the fair component vanishes, so the five-tick equalities force $\nu$ to be supported on $q=1$. The same five-tick setting supplies a separate read of $c$. In the marked row, well $-1$ is dark for *every* positive exponent. Under fair counting, two right and three left moves end there in $\binom52=10$ of the 32 words. Thus its per-launch probability is $5c/16$. A calibrated dark-port rate $r$ gives $c=16r/5$ in this enlarged model, even before enforcing the remote equalities. Zero rate together with remote invariance selects the ordinary spatial law throughout this particular family. Readout leakage, background hits, and uncertainty on a finite dark sample enter that inference. Under finite remote errors the same integrated bound applies to the unnormalized contaminating mass of $\nu$.

Beyond this family, two interventions do not fix arbitrary local record laws. A model can follow the ordinary readout through tick seven and subsequently run an independent fair-direction marker initialized at the seventh-tick position. The two short tests then have all the ordinary statistics. Establishing the actual local signed preparation, the stable readout and the mapping from those readings to the program's quantum and Newtonian flights remains necessary. [Independent path enumeration and integer propagation](check_remote_site_rates.py) · [Exact tables and boundary controls](results/remote_site_rates.json)

Lean 4.19 checks both finite experiments by enumerating signed paths and counts all ten unsigned paths into the dark well. The proof for real exponents and arbitrary mixing measures is the positivity and limit argument above. [Lean path counts](lean/RemoteSiteRates.lean)
