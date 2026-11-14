# Checking what a direction detector preserves

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A rail detector can give the right pass frequency while leaving an unreported record of the walker’s site. Five native ticks on a small staircase already distinguish the two instruments. Eight ticks on larger orders allow two ordinary terminal probabilities to separate partial site marking from persistent path counting. Both tests start with one localized base and one localized sheet. [Direction-only source](Base_preparation_and_two_rays.md) · [Related position-window test](Flight_window_preparation.md)

## A five-tick interference record

Launch at $(0,R,0)$ on the $4M$-site ring with signed Hadamard coin and departure gain $\lfloor x/2\rfloor\bmod M$. At tick two read only the rail. For the $L$ report the surviving words are $RL$ and $LL$, at sites $0$ and $-2$. They each carry one quarter of the original probability. The sheet addresses on these branches are $0$ and $-1$ respectively. A broad pass keeps their signed joint amplitudes. A hidden site copy attaches distinguishable tags before the flight continues. Tracing that copy adds probabilities across the two sites even when later motions bring the branches to the same physical base **and** sheet. Under either instrument $P(L)=1/2$.

At $M=3$ the accepted words ending at $(-1,L)$ at tick five are exactly

| Word | Site at tick two | Signed amplitude numerator | Unwrapped final sheet gain |
|---|---:|---:|---:|
| RLRLL | 0 | −1 | 0 |
| RLLRL | 0 | −1 | −1 |
| LLRRL | −2 | −1 | −3 |

The first and third words end on the same sheet modulo three. Their interference gives joint probability $5/32$ for the broad detector and $3/32$ for an orthogonal hidden site copy. Given the $L$ report, the corresponding probabilities are $5/16$ and $3/16$. The full joint rail/site/rail laws differ by total variation $1/4$. Suppose more generally that the site tags are normalized pure states with overlap $\gamma$, and that attaching them induces no other site-, sheet- or path-dependent disturbance. The same joint port probability is $(3+2\operatorname{Re}\gamma)/32$. A relative sign in the marker can give $1/32$; a purely imaginary overlap gives the same probability as zero overlap. This read measures the real interference term in the specified phase convention.

The counts use the localized physical sheet. At this same port a prepared constant Fourier character instead gives broad/copied numerators $9,5$ over 32; a conjugate nonzero character gives $3,2$. Thus imposing a character or allowing an uncalibrated source can change the inferred overlap. Simple counting gives $3/32$ for every marker and the same pass rate. For a mixture with count fraction $c$, the one localized-sheet joint port gives $[3+2(1-c)\operatorname{Re}\gamma]/32$.

The checker takes every possible single rail-read prefix and both flag values, continues with unmodified ticks and reads the final position and rail with sheet unresolved. Within precisely this instrument family, the first distinct joint law occurs at total depth five at $M=3$, six at $M=4,5,6$, and seven for all $M\ge7$. If the flag must occur at tick two, $M=6$ first distinguishes at seven. All lower depths, absent differences and port tables for the named witnesses are retained. For general order the proof beyond the finite panel is elementary: at depth at most seven each unwrapped gain has absolute value at most $\sum_{j=0}^{6}\lceil j/2\rceil=12$. For $M>24$ no distinct such gains collide modulo $M$, and the base endpoints cannot wrap together. For smaller orders the exact cyclic census checks them directly. This is a minimal depth for a sharp launch and a *single* intermediate rail measurement; a separate coin or an active phase probe would be a different experiment. [Integer word checker](check_direction_record_witness.py) · [All finite comparisons](results/direction_record_witness.json)

## Two terminal bins separate counting from a site copy

Use the same launch and $L$ report at tick two. For every $M\ge10$ consider joint events $A,B$ that the report is followed at tick eight by $(-2,R),(0,L)$ respectively. Their integer numerators are

| Model on the original launches | $256P(A)$ | $256P(B)$ |
|---|---:|---:|
| Broad direction report, localized-sheet squares | 17 | 17 |
| Orthogonal hidden site copy, localized-sheet squares | 13 | 21 |
| Fair path counting | 15 | 15 |

At these two ports the unwrapped final sheet gains span at most nine, so the collisions in the table persist at every order at least ten. The checker retains the altered small-order rows. If the count fraction is $c$ and the coherent component sees tags with one overlap $\gamma$, put $a=256P(A)$ and $b=256P(B)$. Squaring the two tag branches separately, then restoring their cross term, gives

$$
a=15c+(1-c)(13+4\operatorname{Re}\gamma),\qquad
b=15c+(1-c)(21-4\operatorname{Re}\gamma).
$$

Consequently $c=(34-a-b)/4$, and for $c<1$,

$$
\operatorname{Re}\gamma=1+\frac{a-b}{8(1-c)} .
$$

These are per-original-launch probabilities. If only accepted launches are counted, each conditional rate must be multiplied by the measured $L$ yield before inversion. A sharp unwrapped seven-tick control exposes the need for the extra tick: with the $L$ flag, every broad terminal bin at tick seven agrees with counting, although four bins distinguish broad from copied. At eight ticks the two independent contrasts break that ambiguity. At $c=1$ the real overlap is unidentifiable. As $c$ approaches one the inverse becomes sensitive to small errors. Inverting two observed frequencies assumes a stable source, calibrated terminal efficiencies, the specified phases, a common marker on each intermediate site, and no additional disturbance. A different state update or branch-dependent loss can change both probabilities.

## A dark port that tests small site leakage

Use order $M=3$ or $6$. After successive native ticks admit the site sets

$$
\{-1,+1\},\quad\{-2,+2\},\quad\{-1,+3\},\quad\{0,2\},\quad\{1\},\quad\{0\}.
$$

At tick three also require $R$, coherently across its two accepted sites. Record the first failed mask separately. The only words passing every mask are $\mathrm{RRRLLL}$ and $\mathrm{LLRRRL}$. The tick-three positions are $3,-1$, on rail $R$ for both. They enter site one at tick five on opposite rails, and the final Hadamard sends both to $(0,L)$. Including all coin signs, their final amplitudes are $+1/8,-1/8$ at sheet gains $+3,-3$. Those addresses agree modulo three and six. The port is exactly dark on a localized sheet and for every coherent character, because the two translations are the same operator. A permanent orthogonal site tag at tick three instead gives a click probability $2/64=1/32$ per original launch, or $1/8$ given survival to tick three. The complementary output at the last splitter accounts for the missing probability.

More generally, for a pure-square source with an otherwise calibrated apparatus the unconditional click probability is $(1-\operatorname{Re}\gamma)/32$. An incoherent mixture with persistent count fraction $c$ gives $[1-(1-c)\operatorname{Re}\gamma]/32$. In particular, an ideal broad record does not make a counted input dark. Earlier mask records must also preserve the two routes without a relative phase: an orthogonal tag attached instead at tick one, two or four produces the same $1/32$ signal. Copying the common site at tick five leaves the null intact. These controls and every first-miss coordinate are in the checker. A count calibration, relative path phase and detector efficiency are needed to assign positive clicks specifically to leakage at the chosen rail read.

Preassign the event, fixed validation sample and confidence level. With zero clicks in $N$ fresh independent original launches, the exact one-sided $1-\alpha$ binomial upper limit is $U=1-\alpha^{1/N}$. For the pure-square model this bounds $1-\operatorname{Re}\gamma$ by $32U$. To certify a bound $\kappa/m$ following zero clicks, $N\ge\log(\alpha)/\log(1-\kappa/(32m))$ suffices, for $0<\kappa/(32m)<1$. This is order $m$ at fixed confidence and $\kappa$. A known positive detection efficiency divides the observed-rate bound by that efficiency if every true click is independently retained; unknown losses can hide leakage. If the count fraction is calibrated, the corresponding bound on $\operatorname{Re}\gamma$ is $(1-32U)/(1-c)$ for $c<1$. At an uncharacterized multi-step instrument, the null limits the total disturbance tested by this circuit. Reusing that number at other sites, orders or times, or interpreting it as the failure probability of each of $m$ future steps, requires an explicit transfer and disturbance model. The published experiments below supplied no trials for this preassigned port.

Six ticks are minimal for a pair of opposite-sign equal-gain words isolated by the union of their site paths with the stated single intermediate common-rail and final-port requirements, over $M\ge3$. At four and five ticks the only absolute unwrapped gain difference of an isolated pair is two. At six ticks the possibilities are $2,5,6$; order five therefore has another six-tick construction. The cited null uses modular coincidence. In fact, even admitting *more* histories cannot give an unwrapped cancellation under these controls. Fix a positive branch of time-indexed site masks, fixed reported rails, and a final port on the line. All admissible paths have the same site parity at each tick. The pointwise maximum of two such paths is again a nearest-neighbour path: it is 1-Lipschitz and changes parity each tick. It stays in the allowed sites, preserves every stipulated step direction and ends at the same port. The finite family therefore has a greatest path. Every other path is lower by at least two on some departure slice, so its staircase gain is strictly smaller. The greatest path contributes a unique coefficient $+1$ or $-1$ to the final sheet polynomial. Thus a nonempty port cannot be dark on a localized unwrapped sheet, regardless of how often the routes cross. In particular no single fixed finite circuit of this kind is dark at all sufficiently large cyclic orders. If $t<2M$ excludes base wrap between different endpoints, a dark localized-sheet port requires the reachable gain width to reach at least $M$, hence $t(t-1)/2\ge M$. At a fixed exit this is a necessary condition; the width alone does not construct a dark port. [Gain-width bound](Local_filter_resolution.md)

## What experiments have measured inside a reported subspace

Welte et al. prepared two separated atomic qubits in an equal product superposition and detected the polarization of an ancillary optical pulse after its interaction with the atoms. The two polarization results reported the even or odd atomic parity. Full two-atom tomography conditioned on each report gave fidelities $0.808\pm0.014$ with $\Phi^+$ and $0.753\pm0.015$ with $\Psi^+$; the authors report standard deviations of the means. From $F=(\rho_{uu}+\rho_{vv})/2+\operatorname{Re}\rho_{uv}$, the central estimates alone imply $\operatorname{Re}\rho_{uv}\ge0.308,0.253$ respectively for their targeted pairs. The authors’ public Figure 2b matrices directly give $\rho_{\uparrow\uparrow,\downarrow\downarrow}=0.343306-0.0521978i$ on herald A and $\rho_{\uparrow\downarrow,\downarrow\uparrow}=0.315800+0.0838468i$ on herald D. Their published populations and coherences reproduce the reported fidelities when rounded. Orthogonal permanent records of the two basis alternatives would set these entries to zero in a pure site-marking model. The archive contains reconstructed density matrices for these measurements. They are photon-heralded atomic statistics and do not give a sample count or an efficiency bound for either walker port. [Welte et al., Fig. 2 and fidelity definition](https://doi.org/10.1038/s41566-021-00802-1) · [Primary data and basis order](https://zenodo.org/records/4604775)

Two studies of actual atomic walks illustrate the transfer limit. In the four-step cesium experiment of Robens et al. the negative intervention occurs after the first step, when each surviving rail determines a unique site. Copying that site within the surviving rail has no effect at that instant. Their reported $K=1.435\pm0.074$ and measured terminal distributions constrain a different intervention. In a position-distribution fit to neutral-atom walks, Alberti et al. fixed their model’s spatial decoherence rate to zero and fitted a spin rate around five percent. A fixed fit parameter supplies no measured upper bound on a later, explicit site copy. None of these records supplies the two joint frequencies $P(A),P(B)$ or a numerical value of $\gamma$ for the staircase. [Robens et al., Fig. 3 and accompanying analysis](https://doi.org/10.1103/PhysRevX.5.011003) · [Alberti et al., Fig. 4 and fit assumptions](https://arxiv.org/pdf/1409.6145)
