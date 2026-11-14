# Which winding weights one ring can read

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

When $D$ is coprime to the stipulated finite phase order $q$, a walk on **one fixed ring** can identify every conjugate pair of winding weights from its exact model probabilities. Other circumferences identify the folded weights on a quotient. The preparations are all identical: start at one site on the right rail, let the walk run freely, and read a site and rail at a chosen tick. Increasing the clock makes one more pair of windings interfere. Their coefficient is always nonzero, even when many shorter path sums cancel. At the earliest clock that reveals the last independent winding moment, just two outputs distinguish populations that agree on every earlier moment. Their probability difference can be exponentially small in the clock. Two explicit alternatives to that cost for the three-fold gain are studied separately. [First-front read](Unfiltered_winding_fronts.md) · [Interior read](Interior_winding_read.md)

## Finite identification

Use the balanced signed walk with arc gains $(1,g,1,zg)$ from the preceding paper, on $N\ge3$ wells. Write $D=N/\gcd(N,2)$ for the period in left-step counts. The sign character sends $z$ to $-1$. The order of $g$ is $q\ge1$, the label $s$ sends $g$ to $e^{2\pi i s/q}$, and a coherent port has the squared modulus of the sum of its character amplitudes. Assume single-launch weights $b_s\ge0$ for these coherent alternatives and $c\ge0$ for fair path counting, summing to one. They must be stable across the different read times. The exposures and rail/site responses are calibrated, with ideal unit efficiency in these formulas. The numbers $c,b_s$ are the same at every clock. The number of launches at each clock is known. There is no assumption about transport between rings. [Arc identity and coherent port law](Four_arc_gains_and_winding_records.md)

A word with $\ell$ left steps reaches $t-2\ell\bmod N$. Two words reach the same well exactly when their left counts agree modulo $D$. For odd $N$, there is also a direct correspondence with the even ring of $2N$ wells. From a sharp launch at zero every lifted word ends at a site of parity $t$. The two representatives $x,x+N$ of any one odd-ring well have opposite parity, so exactly one can be occupied. Reducing its label modulo $N$ preserves every word, final rail, gain and sign, hence also each port's count and squared amplitude. This is a clock-dependent relabeling. For example, on a triangle a first left step is recorded at site 2, whose occupied lift on the six-cycle is 5. The same parity correspondence holds after prescribed whole-position masks by pulling back each mask at its own tick. [Odd-cycle double cover](https://conferences.famnit.upr.si/event/28/attachments/44/180/jajcay.pdf)

Write $Q=q/\gcd(D,q)$, $\theta_s=2\pi Ds/q$, and $J_j=\sum_s b_s\cos(j\theta_s)$. At tick 3 the left rail at well $-1$ receives just $RLL$ and $LRL$ with opposite signs and equal numbers of left steps. The additional displacement $+3$ on a four-well ring ends on $R$. Thus this unconditional port rate is $c/4$ for all $D\ge2$ and $J_0=1-c$.

For each $k=1,\ldots,\lfloor Q/2\rfloor$ take $t=kD+1$ and read the right rail at $x=t\bmod N$. The total number of left steps is a multiple of $D$ between 0 and $kD$, since the last step is right. For each $h=0,\dots,k$ let $a_h$ be the sum of $(-1)^{n_{LL}}$ over the words with $hD$ left steps and last step $R$. These integers can be computed on the line. Their endpoints are
$$a_0=1,\qquad a_k=(-1)^{kD-1}.$$
Indeed the two extreme words are $R^t$ and $L^{kD}R$. The fair number of words at the port is $F_k=\sum_{h=0}^k\binom{t-1}{hD}$. The observed original-launch probability $p_k$ obeys
$$2^t p_k-cF_k=J_0\sum_{h=0}^k a_h^2+
2\sum_{j=1}^k J_j\sum_{h=0}^{k-j}a_h a_{h+j}. \tag{1}$$
This follows by expanding the squared modulus of $\sum_h a_h e^{ih\theta_s}$ and averaging the stipulated models. At stage $k$, the coefficient of $J_k$ is exactly $2a_0a_k=\pm2$. Starting with $c$ and $J_0$, solve (1) for the one new moment at each clock. Zeros among the interior $a_h$ cannot destroy this coefficient.

Put $d=\gcd(D,q)$. On the reduced cycle of length $Q$, let $w_l$ be the coherent mass at $l=(D/d)s\bmod Q$. The real part of its Fourier transform is $J_j$. Reflection gives $J_{Q-j}=J_j$, so the measured indices cover the full real transform. Finite Fourier inversion gives
$$\frac{w_l+w_{-l}}2=\frac1Q\sum_{j=0}^{Q-1}J_j\cos(2\pi jl/Q).$$
For the classes $l=0$ and, for even $Q$, $l=Q/2$, this is the individual mass. Elsewhere double it to obtain the conjugate-pair mass. Thus when $D$ and $q$ are coprime all folded label weights on the original cycle are determined. Otherwise labels with the same folded $Ds\bmod q$ remain indistinguishable on this fixed ring by sharp-launch terminal position-and-rail reads at **any** clock: at each port the admissible left counts occupy a single residue modulo $D$ and the real-coefficient amplitude polynomial in $e^{i\theta_s}$ has the same squared modulus under conjugation. This also applies to the squared model with coherent whole-position masks. The result concerns the declared mixture and named arc generator. A model with a different event law or detector response can evade the inversion.

## The first clock that can distinguish characters

For $q=3$ and $3\nmid D$, the two rates can even be collected at the **same clock**. Write $\varepsilon=(-1)^{D-1}$, $t=D+1$. The right rail at $D-1\bmod N$ receives $D$ words with one left step, all with positive sign. The other accessible lift ends on $L$. The right rail at $D+1\bmod N$ receives exactly $R^{D+1}$ and $L^D R$. Calling these event probabilities $p_A,p_B$ gives
$$2^{D+1}p_A=D^2(1-c)+Dc,\qquad 2^{D+1}p_B=2+2\varepsilon J_1.$$
Hence $c=(D^2-2^{D+1}p_A)/(D^2-D)$ and $J_1=\varepsilon(2^{D+1}p_B-2)/2$. With $T=1-c$, the trivial character has mass $(T+2J_1)/3$ and the unit conjugate pair mass $2(T-J_1)/3$. At $D=2$ the responses, in units of $1/8$, are

| Three ticks on four wells | Trivial winding | Unit winding pair | Fair count |
|---|---:|---:|---:|
| Site 1, right rail | 4 | 4 | 2 |
| Site 3, right rail | 0 | 3 | 2 |

The three probability pairs are noncollinear. In particular the stipulated pure unit response has probabilities $1/2$ and $3/8$. At $t<D$ every port has at most one lift, and at $t=D$ the only colliding extreme words end on opposite rails. Therefore $D+1$ is the earliest tick for a sharp right launch and the prescribed terminal site-and-rail read to distinguish any winding phases on this ring. Three ticks are sufficient and earliest on four wells. For $3\mid D$ the two cubic winding phases coincide at every clock on this ring.

For higher $q$ a count tie at one cosine (for example $\cos\theta=0$ at $q=4$) leaves (1) intact, since the three-tick count anchor is separate. Choosing $D$ coprime to $q$ is needed to identify all folded labels. Equation (1) gives an exact inverse in the infinite-data or noiseless-probability problem; its $2^t$ factor can amplify sampling error. No uniform large-$q$ launch bound follows here. The later fixed-gap read for $q=3$ assumes a more finely resolved terminal position. [Interior sampling and resolution](Interior_winding_read.md)

## The last required clock is optimal for these measurements

Let $K=\lfloor Q/2\rfloor$. At a fixed complete port, the allowed left counts are congruent modulo $D$ and lie in $[0,t-1]$ for a right-ending word or $[1,t]$ for a left-ending word. Every squared port frequency therefore contains only harmonics of order at most $\lfloor(t-1)/D\rfloor$, even if intermediate whole-position masks remove some words. When $Q\ge2$, consider the two coherent ensembles with reduced-cycle weights $w_l^\pm=(1\pm\cos(2\pi Kl/Q))/Q$. Both sum to one and have nonnegative weights. They are attainable by choosing one original label per reduced class. Fourier orthogonality gives equal moments at every $j<K$ and unequal moments at $K$, since the mean of $\cos^2(2\pi Kl/Q)$ is positive. Thus their complete site-and-rail transcripts from separate sharp launches at all clocks through $KD$ have identical one-launch laws. With independently refreshed launches this also holds under adaptive choice of those clocks. At $Q=1$ fair count still has to be distinguished from the sole squared law. Every complete port through tick 2 has at most one word for $D\ge2$ and tick 3 supplies the count anchor. Hence the smallest possible maximum clock for the full mixture is $\max(3,KD+1)$. This is a lower bound on time within the specified preparations and terminal records. Other detector bases, joint preparations or correlated multi-launch observations can supply different information.

In the exact replay, the $D=8,q=21$ trivial-character control recovers every cosine moment as one. A second calculation rounded the probabilities to binary64 and iterated the same algebraic inverse. At the tenth moment it returned about $-5.03\times10^{18}$ even with zero sampling noise. A nonzero diagonal proves identifiability; it gives no guarantee of a numerically or statistically stable inverse. On small rings the three-tick example avoids this loss of precision.

## Launch cost at the earliest clock

Take $Q\ge2$, $K=\lfloor Q/2\rfloor$, and $T=KD+1$. Compare two populations with the same fair-count mass and the same $J_0,\ldots,J_{K-1}$. Write $\Delta J_K=J_K^+-J_K^-$. At clock $T$ a right-ending word can have between 0 and $KD$ left steps. Only the pair of extreme counts differs by $KD$. It consists of $R^T$ and $L^{KD}R$, with sign product $\varepsilon=(-1)^{KD-1}$. For a left-ending word the range is $1,\ldots,T$, so the only such pair is $R^{T-1}L$, $L^T$, with sign product $-\varepsilon$. All shorter lags and all fair contributions agree. This gives the entire difference of terminal laws:

| Output at $T$ (well labels modulo $N$) | $P^+-P^-$ |
|---|---:|
| $(T,R)$ | $2^{1-T}\varepsilon\,\Delta J_K$ |
| $(T-2,L)$ | $-2^{1-T}\varepsilon\,\Delta J_K$ |
| Every other site and rail | $0$ |

Thus the one-launch total variation distance is $\delta=2^{1-T}|\Delta J_K|$. It vanishes at all earlier clocks. For the two populations $w_l^\pm$ above, $\Delta J_K=(2/Q)\sum_l\cos^2(2\pi Kl/Q)$ is 2 for even $Q$ and 1 for odd $Q$.

Suppose every new sharp launch independently samples its label and terminal outcome with the prescribed law for the chosen clock. Even if a protocol chooses each clock from earlier outcomes, $m$ terminal reads at clocks at most $T$ have total variation at most $1-(1-\delta)^m$. Couple the two experiments with identical decision randomness. Whenever the records so far agree, the next clock is the same, and the next outputs can be coupled to agree with probability at least $1-\delta$. Iteration gives the bound. For a binary decision, the sum of the two error probabilities is at least one minus the transcript total variation. To make each error at most 5% therefore requires $(1-\delta)^m\le1/10$. For the previously computed $D=8,q=21$ panel this gives an exact one-launch distance of $2^{-80}$ at clock 81. Already $1-(1-\delta)^m\le m\delta$ forces $m\ge\lceil0.9\,2^{80}\rceil>10^{24}$ to distinguish that pair at these clocks. The obstruction applies even with exact model probabilities and exact arithmetic. [Coupling and total variation](https://ocw.mit.edu/courses/18-445-introduction-to-stochastic-processes-spring-2015/5bd4774f613aa28bd111c36f3a3beeed_MIT18_445S15_lecture4.pdf)

For $Q=2$, these populations are the pure winding phases $+1$ and $-1$. At either exceptional port there are exactly two histories. One phase has probability $4/2^T$ there and the other has zero, with the roles reversed at the other port. All other records have identical probabilities. Read at $T$ each time, identify the phase on the first exclusive outcome, and toss a fair coin if all $m$ launches miss both. Each error probability is exactly $\tfrac12(1-4/2^T)^m$. The preceding lower bound proves this is optimal among the stated protocols, including ones that choose earlier clocks.

| Odd ring with $q=2$ | Earliest clock $T$ | Chance of a decisive record per launch | Fewest launches for both errors at most 5% |
|---:|---:|---:|---:|
| 3 wells | 4 | $1/4$ | 9 |
| 7 wells | 8 | $1/64$ | 147 |
| 15 wells | 16 | $1/16384$ | 37,725 |

The two distinguishing wells are different for every $N\ge3$, so discarding the rail preserves their one-launch total variation. It can still cost information on repetition. On the triangle at clock 4 the site probabilities in order $0,1,2$ are $(2,5,9)/16$ and $(2,1,13)/16$. For two independent launches at that clock, summing half the smaller likelihood over the nine ordered site pairs gives equal-prior error $19/64$. Reading the rail as well gives $9/32$. Thus equality of the one-launch distances alone does not extend the sharp repeated-launch formula to coarser records.

These costs concern known clocks, ideal terminal measurement, independent launches and this specified pair of laws. On the same 16-well ring with phase order 21, a four-port read at tick 144 distinguishes the pair with both errors below 5% in 163 independent launches. When one label persists across the run, the equal-prior error exceeds 18.13% at any launch count. [Later clocks and the persistent-label control](Later_winding_clocks.md) · [Physical-ring checker](check_first_winding_clock.py) · [Exact finite results](results/first_winding_clock.json)

## What would select the ordinary embedding?

Choose the arc generator in advance and call $s=\pm1$ its ordinary winding pair. In this finite family on a coprime ring the ordinary pair is selected **if and only if** the measured probabilities agree with $c=0,\ \sum_{s\in\{1,-1\}\bmod q} b_s=1$, with each residue counted once. The predicates above also return any competing population in the family. The mathematical experiment supplies discriminating predictions. It supplies no observed population, and simultaneous relabeling of the apparatus and gains preserves the description. Quantum mechanics, a universal probability law, and a classical limit have yet to emerge from independently justified primitives.

Lean 4.19.0 enumerates the four-well walk and proves uniqueness for weights in common integer units from the two three-tick numerators. It also checks which odd-ring lift has the required parity and proves the two endpoint-count implications at the first clock. The real-weight inverse, probability coupling and asymptotics have mathematical arguments above and in the companion notes. Director Z independently classified separation of two pure characters, including aliases when the order of the phase is unknown. [Lean certificate](lean/ThreeTickRing.lean) · [Director Z’s criterion](../Director_Z/computation/Character_Separation/CRITERION.md)

Run the checker from its repository directory alongside `check_character_tomography.py`, which supplies the exact cyclotomic remainder. An independent computation compares the clock formulas with the walk propagated directly on physical sites and gain residues. [Fixed-ring checker](check_fixed_ring_moments.py) · [Exact records](results/fixed_ring_moments.json)
