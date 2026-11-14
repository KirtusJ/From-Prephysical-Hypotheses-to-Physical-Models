# A forward-only test of which position record was kept

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two instruments can give the same intermediate binary answer while retaining different information about the walker. On the signed Hadamard line, a later visit to the origin distinguishes keeping one site-membership bit from retaining the detailed site. Six forward ticks suffice for every input coin. The complementary records share one clock and one final well. An eight-well version needs only a final position measurement if four more ticks are available. These are predictions for a physical comparison. [Earlier parity-record analyzer](Parity_record_eraser.md) · [Measured eraser comparisons and their scopes](What_two_eraser_experiments_measure.md)

## One bit at tick three and the return at tick six

Launch at the origin with unknown normalized rail state $(\alpha,\beta)$, ordered right, left. Every tick applies the real Hadamard then shifts the two rails. At tick three write $b=1$ for $x=-3,+1$ and $b=0$ otherwise into a blank bit. Let three more ticks act on the walker, keeping $b$ available. Read the complete triple $(b,x,r)$; record a hit for $(1,0,R)$ or $(0,0,L)$. The same mask on an eight-ring is $\{5,1\}$. The apparatus requires an addressed binary position write and a complete final read. All original launches count, including those ending elsewhere.

* **Pooled write.** The instrument stores only $b$ and preserves coherence within each of its two site sets. Both hit ports are dark for every input.
* **Sharp lookup.** A nondemolition site instrument retains mutually orthogonal labels for all distinct intermediate sites and preserves the rails at each site. It also outputs $b$. All subsequent walk dynamics leave these labels untouched. The kinematic hit effect is exactly $I/16$ on the input coin.

To verify the arithmetic, propagate the input to each intermediate site, then take three ordinary ticks from that site. The entries are integer row vectors acting on $(\alpha,\beta)$ with a common factor $1/8$.

| Hit cell | Intermediate site | Signed row | Intermediate site | Signed row |
|---|---:|---|---:|---|
| $(1,0,R)$ | $-3$ | $(1,-1)$ | $+1$ | $(-1,1)$ |
| $(0,0,L)$ | $+3$ | $(1,1)$ | $-1$ | $(-1,-1)$ |

Adding the rows gives zero in each reported cell. With orthogonal site labels the norms add and the two cells contribute $2|\alpha-\beta|^2/64$ and $2|\alpha+\beta|^2/64$. Their sum is $1/16$. Linearity of the input density matrix gives the same effect for mixed coins and for coins entangled with an untouched spectator. The complementary cells matter. Using only the first would leave the input $(1,1)/\sqrt2$ blind. The site write and rail-resolved return are the only switched instruments in this design. The earlier parity analyzer stores a first direction and repositions rails before its terminal coin. The present witness uses the homogeneous forward tick throughout both flights.

**Finite minimality.** Consider the line, one sharp launch site, one deterministic binary site predicate at an interior tick, no other interventions and a terminal event made of any cells $(b,x,r)$. Require zero coherent mass for every coin and strictly positive sharp-lookup mass for every coin. For a universal null, each selected terminal row must annihilate both basis vectors, since the different read cells are orthogonal. For every predicate the checker gathers all such rows and forms the sum of their sharp-lookup Gram matrices. This is the greatest available positive-semidefinite effect from dark cells. A positive determinant is necessary and sufficient for uniform positivity. At final ticks 2, 3, 4 and 5 all 4, 12, 28 and 60 predicates respectively fail, counting every possible write time and constant predicates. At tick 6 exactly two of 124 pass, related by complementing the bit. This finite result has the line geometry, initial state family and intervention budget just specified.

## What partial records would do

Suppose the site also leaves a normalized memory vector $e_x$, with all four vectors living in one Hilbert space. The write acts identically on the two rails at a given site, initially with the same independent memory preparation. Afterward its conditional vectors undergo no path-dependent evolution. For a pure coin the squared-norm hit rate is

$$\frac{|\alpha-\beta|^2[1-\operatorname{Re}\langle e_{-3},e_{+1}\rangle]+|\alpha+\beta|^2[1-\operatorname{Re}\langle e_{+3},e_{-1}\rangle]}{32}.$$

Thus a relative phase can brighten the dark port, even if the two memory rays carry no distinguishable site information. Conversely a record distinguishing only the already retained bit can preserve both cancellations. One unknown coin may probe only one of the overlaps. A device that erases detailed information before the return can reproduce the pooled result. A detector that merely assigns a terminal site in software once the walk is over makes no unique prediction about a physically inserted site instrument. This proposed experiment tests its specified persistent nondemolition realization. The relation between fringe amplitude and marker overlap also occurs in two-path interferometry. [Englert, *Fringe Visibility and Which-Way Information*](https://doi.org/10.1103/PhysRevLett.77.2154)

## Position-only alternative on an eight-ring

At tick four write the predicate of $\{0,4\}$ into the bit. After six more ticks, count $b=1$ together with $x\in\{2,6\}$, pooling both rails. At each of the two sites the two intermediate contributions to the right-rail row are $(-4,0)$ from site 0 and $(4,0)$ from site 4. On the left rail they are $(0,-4)$ and $(0,4)$. The common amplitude factor is $1/32$. Summing the four position-and-rail cells gives the hit effect

$$ \frac{1-\operatorname{Re}\langle e_0,e_4\rangle}{16}\,I .$$

Consequently this position-only experiment probes one overlap at any incident coin, including a mixture. Equal memory vectors give zero; orthogonal vectors give $1/16$. The unmonitored complement and positions outside the hit set remain in the original-launch denominator. The conclusion concerns this eight-ring and these two intermediate sites.

**Probability and experimental scope.** The rational rate is a quantitative prediction under complete squared-norm readout with the specified loading and gates. Perfect destructive cancellation gives a prohibited event under any readout that forbids counts in a zero kinematic sector. To predict a positive rival count also requires the detector to register a positive kinematic sector with nonzero probability. Without a lower sensitivity bound the rival need not produce a detectable excess at finite exposure. For independent trials with ideal squared-norm readout and perfect sharp lookup, the probability of no hit in $N$ launches is $(15/16)^N$, below 5% at 47 launches. Dark counts, lost outcomes and imperfect phases need their own calibration. Neither instrument is selected by the bare walk or by the previously proposed agreement of one-time mask rates.

The [exact checker](check_forward_mask_coherence.py) independently enumerates signed histories for both input columns and compares them with site-block propagation on the line and the eight-ring. The [record](results/forward_mask_coherence.json) retains the row for every intermediate-site contribution at every reachable final cell, complete pooled and sharp-lookup Gram matrices, and the search counts. Lean 4.19.0 checks the [integer numerator identity](lean/ForwardMaskAudit.lean) for the six-tick sharp effect. The checker and the signed rows establish the link to the physical port conventions. There are no measured detector counts in the record.
