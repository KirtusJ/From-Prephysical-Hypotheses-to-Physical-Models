# Measuring a refinement charge by the distance of a fall

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The staircase used to distinguish cyclic characters also supplies the force for a flight. At a fixed elapsed time, the distance of a rested packet from its starting site distinguishes bounded absolute character labels, even when its mean displacement is zero. This comparison requires the same site pitch, clock and force calibration for every candidate label.

## The staircase is linear on every occupied slice

On the $4M$-site ring a signed Hadamard tick adds $g(x)=\lfloor x/2\rfloor\bmod M$ to the sheet at departure and moves the base by one site. Choose the character convention $\chi_k(j)=e^{-2\pi i k j/M}$, put $h_k=\pi k/M$, and start on spatial parity $p_0$. At departure $t$ the occupied parity is $p_t=(p_0+t)\bmod2$. Thus

$$
\chi_k(g(x))=e^{i h_k p_t}e^{-i h_k x}.
$$

The formula is single-valued across the seam because $4Mh_k=4\pi k$. Through $n$ ticks the scalar multiplying the ordinary linear-force evolution is $\exp[ih_k\lfloor(n+p_0)/2\rfloor]$. Direction-only projections preserve the identity branch by branch. Replacing $k$ by $k+M$ leaves the original multiplier unchanged. In contrast, shifting $k$ by $M/2$ at even order changes the relative phase of paths whose gains differ by one. The two positive words $RLR,LRR$ from $(0,R)$ end at $(1,R)$ with gains $0,-1$. Their character-square port probability at tick three is $(1+\cos(2\pi k/M))/4$, with pure count giving $1/4$. This single contrast is already injective on pure folded labels $0\le |k|_M\le\lfloor M/2\rfloor$; general mixtures need more lags. For a superposition on both spatial parities, the two scalars must be retained if subsequent controls reconnect them. The same qualification applies when different sheet characters are compared coherently. [Finite staircase calibration](Counting_and_character_records.md) · [Doubled-lag alias on the distinct uniform carrier](Force_calibration_across_scales.md)

## A rail test for charges outside the weak-field regime

The three-tick experiment also works with a detector that sums over every site and reads only $L$ or $R$. Here are all native words from $(0,R)$ on the unwrapped neighbourhood, with sheet initially at zero for the history tally. A pure character response assigns the same phase relation on each launch. A preparation localized on the *physical* sheet and then traced generally gives a mixture of characters.

| Word | End site | Rail | Departure gain | Sign |
|---|---:|:---:|---:|---:|
| RRR | 3 | R | 1 | + |
| RRL | 1 | L | 1 | + |
| RLR | 1 | R | 0 | + |
| RLL | −1 | L | 0 | − |
| LRR | 1 | R | −1 | + |
| LRL | −1 | L | −1 | + |
| LLR | −1 | R | −2 | − |
| LLL | −3 | L | −2 | + |

Write $d_M=|k|_M$ and $h=\pi d_M/M$. With the field on, summing squared amplitudes at distinct ports yields $P_{\rm on}(L)=1/2-\cos(2h)/4$. Disabling only the sheet increment throughout a matched three-tick reference run gives $P_{\rm off}(L)=1/4$ in *every* coherent sector. Thus the excess left-rail probability is $\sin^2(h)/2$, exactly. It stays at least $\sin^2(\pi\eta)/2$ on any subsequence with $d_M/M\ge\eta>0$. Neither the launch, number of ticks nor definition of the rail event depends on $M$. The control compares two runs with identical free coin motion and requires a switch or matched reference for the gain. An independently established pure square law would also allow a field-on reading to be compared directly with its theoretical baseline.

In the classified mixture, ordinary counting gives $P_{\rm off}(L)=P_{\rm on}(L)=1/2$. If the incident count weight $c$ and character weights $b_j$ are shared by both preparations, their field-off baseline is $(1+c)/4$ and

$$
P_{\rm on}(L)-P_{\rm off}(L)
 =\tfrac12\sum_j b_j\sin^2(\pi j/M).
$$

The total incident character weight outside $d_M/M<\eta$ is therefore bounded above by $2[P_{\rm on}(L)-P_{\rm off}(L)]/\sin^2(\pi\eta)$ for $0<\eta\le1/2$. Equality is possible when the only contributing outer labels sit on the boundary and all inner ones have zero slope. Pure counting produces zero excess at every order. An observed vanishing excess cannot establish character purity. Both formulas assume that the same real probability law applies to the ports of the two instruments; extrapolation to an arbitrary assignment of positive endpoint scores would need an independent classification.

For a pure compatible folded label on a doubling tower, vanishing rail excess forces $d_M/M\to0$ and $P_3(1,R)\to1/2$. In particular $P_3(1,R)>1/4$ eventually. The child of $d_M$ at order $2M$ is either $d_M$ or $M-d_M$. The latter lies at or above one quarter of the child order and cannot change the fold on this tail. Even the weaker tail inequality $P_3(1,R)\ge1/8$ forces stabilization for faithful labels. Indeed it says $d_M/M\le1/3$. An increase consistent with the child bound then requires $d_M/M=1/3$ exactly, which represents a character of order three and fails faithfulness for $M>3$. On that tower alone, dropping faithfulness allows $M=3\cdot 2^j$, $d_M=M/3$ to give the boundary probability $1/8$ forever. On the full divisibility system the argument using a common multiple of $3z$ removes this exceptional case. [Closed-boundary proof](Refining_the_sheet.md#a-fixed-time-record-at-increasing-resolution) A count contribution, or a mixture of distinct coherent labels, requires the preceding weighted test instead.

## Which continuum continuity would force this result?

One sufficient hypothesis concerns just one smooth packet, without demanding convergence in operator norm on the whole lattice. On the $4M$ ring prepare a common normalized parity packet whose Fourier support lies within $C\delta$ of $q_*=-\pi/2$ and its parity replica $q_*+\pi$, with $\delta\to0$. For instance the two supports can carry parity-related samples of a fixed smooth compactly supported envelope; require $M\delta\to\infty$ to resolve it. The coin spinor on that support may depend on momentum. The first departure kick translates the support by $-h_k$ before applying the usual free tick, whereas the free control preserves the support. Along any rough subsequence $\pi\eta\le |h_k|\le\pi/2$, the two output supports are disjoint modulo $\pi$ for sufficiently small $\delta$. Their exact overlap is zero and their pure-state trace distance is one. Vanishing incident norm tails in place of compact support give overlap tending to zero.

Suppose a common, norm-preserving identification retains the full output of both settings, including every rail and any weight outside the putative weak band. If their evolution of that same input converges locally uniformly in scaled time, including one tick tending to time zero, to strongly continuous propagators with the same initial state, the two outputs must approach one another in norm up to common demodulation. The disjoint-support calculation excludes a rough subsequence. Conjugating both settings by the same free micromotion leaves their overlap unchanged. A separately drifting momentum frame for each candidate could instead erase the shift. This is a conditional transfer of a continuum hypothesis, not evidence that any laboratory has verified strong convergence.

Coarse position continuity alone supplies no such implication. From the sharp origin, every path after three ticks lies within $3\delta^2$ of the launch, even at order-three character phase. Any fixed bin with the origin in its interior eventually reports the same result in both runs. For a Lipschitz position test $f$ the difference of expectations is at most $6\delta^2\operatorname{Lip}(f)$. More strongly, on *any* common single-parity packet the first field-on and field-off steps have exactly the same site-and-rail probabilities: the phase multiplies both input rails at departure, then each output rail streams from a unique site. Those probabilities agree even when the two output spinors above are orthogonal. Identifying a scaled flight from smooth position data at fixed positive times would require a separate argument to control microscopic tick times. [Exact signed checks](check_staircase_rail_field.py) · [All checked rows](results/staircase_rail_field.json)

## A common flight

Fix $F_1>0$ and a sequence of increasing sheet orders $M$. At each order choose $\delta=(\pi/(MF_1))^{1/4}$. One site has length $\delta^2$ and one tick takes $\delta^3$. For any fixed centred integer label $k$ on this sequence, the same apparatus gives $h_k=kF_1\delta^4$. In the scaled momentum $p=(q-q_*)/\delta$, a departure kick changes $p$ by $-kF_1\delta^3$. At band curvature $b=\pm1$, the Hamiltonian is $bp^2/2+kF_1Y$. A rested packet therefore has displacement $-bkF_1T^2/2$ at flight time $T$. A change of character convention reverses the signed potential slope. [Forced spinor estimate](Forced_envelope_and_classical_motion.md)

One preparation with the field left on starts at $(0,R)$ and accepts the opposite rail after every two ticks, without resolving position or sheet. Take the nearest even $m$ to $\delta^{-5/2}$ such blocks. In a bounded weak sector the acceptance is asymptotic to $\delta^{5/4}/\sqrt{\pi}$, and preparation consumes $2m\delta^3=O(\delta^{1/2})$ time. These are per-launch yield and elapsed time for the prescribed string of outcomes. At release the packet is concentrated in scaled position and momentum. The output rail has equal limiting contributions from both curvatures. Take $n$ more ordinary ticks with $n\delta^3\to T>0$. The ring agrees with the line on this entire experiment for sufficiently large $M$, since $2m+n=o(M)$. The two-ray theorem then gives, conditionally on acceptance,

$$
Y-Y_0\ \Longrightarrow\ \tfrac12\delta_{-kF_1T^2/2}
                         +\tfrac12\delta_{+kF_1T^2/2},
\qquad
|Y-Y_0|\ \longrightarrow\ |k|F_1T^2/2\quad\text{in probability}.
$$

Here $\delta_z$ is a unit point mass. The signed mean cannot separate the two curvatures in this limiting law. The absolute displacement can. For example, orders $M=2^j$ support the faithful families $k=1$ and $k=3$. At $F_1=T=1$ the radii tend to $1/2$ and $3/2$. The same preassigned event $|Y-Y_0|>1$ has limiting conditional probabilities zero and one. Real preparations and real base readouts give exactly the same probabilities for conjugate characters, at every order. Position at a specified time is a terminal measurement on fresh launches. [Direction filter and two-ray proof](Base_preparation_and_two_rays.md) · [Calibrated preparation of a single curvature](Returning_loops_and_one_classical_ray.md)

For an incident count fraction $c$ and character weights $b_k$, use accepted weights proportional to $c\,2^{-m}$ and $b_kP_k(\mathrm{accept})$. Count increments after release remain independent fair signs, with scaled displacement variance $n\delta^4\to0$. Its release position also concentrates: within each accepted two-tick block the first move is still fair, while the prescribed second moves alternate and sum to zero for even $m$, giving release variance $m\delta^4$. Thus count and $k=0$ both contribute at radius zero. An independent short port calibration can distinguish them. For mixtures of bounded labels the radial limit gives the **post-preparation** masses at their respective radii. Uniform tightness of those masses in the folded label extends the conclusion by truncation; a large unclassified strong-field weight leaves the prediction open. The folded Gaussian and four-tick rotation construction uses a programmed rail rotation as its source of force. It requires a separate calibration to test a sheet charge. [Count and heralding](Count_weight_in_classical_flight.md) · [Free folded field](Folded_field_and_native_gaussian.md) · [Four-tick rotation](Four_tick_force.md)

On a divisibility tower, a uniformly bounded compatible folded label is eventually constant as an absolute integer: above twice the bound, reducing a larger common level preserves its centred magnitude. Faithfulness on a tower of powers of two permits every odd integer charge. Faithfulness on a divisor-cofinal tower covering all positive orders forces any such integer to have no prime divisor, hence absolute value one. The arithmetic conclusion needs compatibility between the different preparations. One calibrated flight compares their effects at its order; a finite panel alone cannot establish that compatibility everywhere. If the phase gradient or the effective band mass can be refitted for each candidate, the acceleration determines only their ratio.

## What an atomic walk has measured

Genske et al. accelerated two spin-dependent optical lattices together and independently measured the resulting phase gradient with a two-site atom interferometer. At $\Phi=2\pi/8$, fluorescence measurements of individual cesium atoms showed partial position revivals at eight and sixteen steps. Figure 2 distinguishes measured points with 68% binomial intervals from ideal and dephasing-adjusted predictions. Their launch was a localized spin state and the observable was finite-strength transport. Their experiment demonstrates an independent gradient calibration and a terminal transport readout. An empirical estimate of a staircase charge would additionally require an identified cyclic sheet, the same gradient standard across orders, and the specified packet preparation and success records. [Genske et al., *Physical Review Letters* **110**, 190601 (2013), Fig. 2](https://doi.org/10.1103/PhysRevLett.110.190601) · [Authors' accessible paper](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/genske-2013.pdf)
