# Sorting two wells before the same site read

An eight-site Hadamard walk can give the three masses $1/8,2/8,5/8$ at three distinct addresses of an ordinary full-position detector. One controlled Hadamard on the position register just before detection makes this possible. At six and eight ticks the same analyzer interchanges which of two wells is bright. The unsorted walks have identical site effects at those clocks for every localized coin. This proposes two new circuits for a position-encoded walk. The [published Cairo comparison](Two_equal_ideal_position_distributions_on_IBM_Cairo.md) concerns the unsorted circuit.

## A gate on the existing address register

Start at well zero with any rail, possibly correlated with an idle spectator. After $t$ free Hadamard-and-stream ticks write the site-transfer matrix as $K_t(j)$. Encode $j=4b_2+2b_1+b_0$. Apply $H$ to $b_2$ controlled by $b_1=1$, leaving the rail alone, then physically measure the three position bits jointly as a site. The address bit order specifies the logical wires independently of hardware qubit numbering. The gate exchanges amplitudes between 2 and 6 through the real sum and difference

$$K'_t(2)=(K_t(2)+K_t(6))/\sqrt2,\qquad K'_t(6)=(K_t(2)-K_t(6))/\sqrt2.$$

It acts identically on the pair 3 and 7, both dark at these even clocks, and fixes 0 and 4. At six ticks $K_6(2)=K_6(6)$, at eight $K_8(2)=-K_8(6)$, and at eighteen $K_{18}(2)=K_{18}(6)$. In the orientation where R increases position, writing the raw integer matrices in rail order $(R,L)$ gives

$$K_6(2)=\tfrac18\begin{pmatrix}2&-2\\2&2\end{pmatrix},\qquad
K_8(2)=\tfrac1{16}\begin{pmatrix}-4&-4\\-4&4\end{pmatrix}.$$

Reflecting the ring exchanges the two inputs of the address Hadamard, changing only the global sign at its difference output. For each clock the unsorted effects at 0,2,4,6 are $(1,1,5,1)I/8$. The sorted effects are therefore proportional to the identity, with the following incident ordinary masses. All odd sites are dark.

| Flight and setting | Site 0 | Site 2 | Site 4 | Site 6 |
|---|---:|---:|---:|---:|
| Six or eight ticks, bypass | 1/8 | 1/8 | 5/8 | 1/8 |
| Six or eighteen ticks, analyzer | 1/8 | 1/4 | 5/8 | 0 |
| Eight ticks, analyzer | 1/8 | 0 | 5/8 | 1/4 |
| Either clock, both paths distinctly marked before analyzer | 1/8 | 1/8 | 5/8 | 1/8 |

The six-minus-eight difference in $P(2)-P(6)$ is $1/2$ under ordinary scoring and ideal unmarked evolution. A fixed stochastic relabeling of the equal bare site laws gives zero. More generally, normalized environmental records of the two wells with overlap $\gamma$ give $P(2)-P(6)=s_t\operatorname{Re}\gamma/4$, where $s_6=s_{18}=1$ and $s_8=-1$. This expression assumes the marks preserve the two local rail maps up to their distinct environmental factors. A relative phase enters the same real overlap. Reversing the sign of address bit $b_2=1$ before the analyzer exchanges the two output probabilities. A null real contrast alone cannot distinguish a quarter-turn phase from complete marking. The analyzer needs its own phase and gate calibration.

## Testing the support power with exact site writes

Suppose each launch scores the positive masses of the physically written sites by a common real power $q$, normalizing on that support. The rail remains unresolved. Write $P_b$ for the incident probability at the designated bright site, 2 at six ticks and 6 at eight. The [three-mass witness and proof](Reading_distance_on_an_eight_site_ring.md) apply to the addresses themselves. For $\theta=\log2/\log5$ the score

$$S=(1-\theta)P_0-P_b/2+\theta P_4/5$$

is nonnegative for every $q$ and vanishes exactly at $q=1$, including under mixtures in the sense of almost-sure equality. Indeed its numerator after multiplication by $1+2^q+5^q$ is $(1-\theta)+\theta5^{q-1}-2^{q-1}$. Strict weighted arithmetic–geometric mean gives the claim. A designated dark-port event has incident probability zero in this ideal-support model. Keep its observed count and all missing reports in an experiment. Power zero gives equal weight to each positive port, so even tiny positive leakage changes the support discontinuously. The exact three-port inference requires calibrated zeros or an explicit leakage model. A hidden coin-resolving write or an early address record also changes the prediction.

At six ticks one can reverse the same gate immediately after the full site read. The bright outcome then restores the symmetric position state on wells 2 and 6 with their common rail. The outer two outcomes at 0 and 4 are fixed. On this prepared family, the re-encoded write implements the three-radius state update, including on a spectator. Four further free ticks give zero joint probability for bright then radius two because $K_4(0)=-K_4(4)$. This identity concerns the specified input subspace; a general state could populate both analyzer outputs. A hidden-position read followed by a fresh coherent analyzer can itself prepare a symmetric state on the bright branch, so the continuation alone does not certify how that branch was prepared.

The [exact replay](check_two_well_sort.py) compares the signed coordinate recurrence and direction words, computes every effect in both rail columns, checks the phase-flip and distinct-mark controls, and verifies the continuation. These are circuit predictions. The original two-clock Cairo histograms already differ in the bypass despite ideal equality, so their discrepancy matters when designing a new hardware comparison. The published data contain no controlled-Hadamard analyzer arm. [Razzoli et al., Fig. 8](https://doi.org/10.3390/e26040313)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed the address analyzer and its replay.
