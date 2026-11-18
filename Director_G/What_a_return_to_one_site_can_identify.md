# What a return to one site can identify

For the ideal eight-site Hadamard walk, the probability of returning to the launch site at every terminal clock has an exact realization by a stationary mixture of two deterministic cycles. The agreement covers arbitrarily late clocks and every coin prepared at the launch site. A binary intermediate measurement gives a different fourth-step prediction. These statements concern specific records and instruments on effective models. [Published circuit and position experiment, Razzoli et al., Fig. 8](https://www.mdpi.com/1099-4300/26/4/313) · [Position-figure replay](Two_equal_ideal_position_distributions_on_IBM_Cairo.md)

## Reading a return

For a common distribution of launches under a fixed deterministic update, write $w_d$ for the mass of initial states with least positive return period $d$. A return to the complete initial state at time $t$ means $d$ divides $t$. Consequently $r_t=\sum_{d\mid t}w_d$. Subtracting the contributions of proper divisors yields each $w_d$ from earlier rates. Through a finite clock $T$, the exact feasibility conditions are nonnegative recovered masses with total at most one. To realize the rates, give mass $w_d$ to a cycle of length $d$ and assign the remainder to a longer cycle. For an infinite sequence passing every finite-prefix test, summing the recovered masses and assigning the remainder to states that never return gives a global fit. The premise is identity of the full state on return. A site detector can report the same outcome for different states. [Puri and Ward, related periodic-point counting identity](https://cs.uwaterloo.ca/journals/JIS/VOL4/WARD/short.html)

In particular $r_2\le r_4$. A common stationary binary reporting law with positive gain preserves this ordering. The optimized Cairo position histograms give approximately 0.336340 at site zero at two ticks and 0.146020 at four. A common complete-state-return model misses at least one displayed rate by 0.095160. This maximum absolute discrepancy is sharp across the eight displayed positive clocks. Assign probability 0.241180 to least period two and the rest to a period greater than eight. This reproduces neither the ideal position nor the measured hardware; it attains the optimum in the stated error measure. The figures use separately compiled circuits and deposit no full microscopic state identity. The bound is a property of the displayed rates, with precision limited by the plot. [Source transcription](results/cairo_cycle_figure8.json)

## Two deterministic cycles with all the ideal origin rates

Take two copies of a 24-phase cycle. The hidden transition always increments phase by one modulo 24. In the first copy mark phases $S_1=\{0,2\}$ and in the second mark $S_2=\{0,2,4,10,14,16\}$. The detector reports the origin precisely at a marked phase. If positions elsewhere are desired, report site one at every odd phase and site two at the remaining even phases. Every reported step then moves to a nearest neighbor. That choice visits only three of the eight sites and can be rejected with the full position distribution.

Use uniform phase on each cycle, with prior cycle probabilities $5/6$ and $1/6$. Condition the launch on observing the origin once. The conditional weights are $5/8$ and $3/8$. For each set $S$, the probability of a subsequent hit after $t$ ticks is $|S\cap(S-t)|/|S|$. The ideal walk's position effect at the origin is $r_t I$ on the two input coin modes at every clock. Exact propagation of its two input columns gives the rates below.

| Even clock | 0 | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|
| First cycle | 1 | 1/2 | 0 | 0 | 0 | 0 | 0 |
| Second cycle | 1 | 1/2 | 1/3 | 1/3 | 1/3 | 2/3 | 2/3 |
| Mixture and ideal walk | 1 | 1/2 | 1/8 | 1/8 | 1/8 | 1/4 | 1/4 |

Odd clocks have zero probability. The second half of the period follows by reflection $r_t=r_{24-t}$. The checker propagates all 24 steps, including the full matrix return at step 24. The walk commutes with translation, so return of both origin columns to their initial values there implies the identity at 24 on the whole ring. One passive terminal origin read per fresh launch therefore gives identical probabilities in the two models at all clocks.

A single stationary ergodic binary observation process cannot give this exact conditional curve. Let $X_j$ indicate the origin mark on a stationary trajectory and suppose its stationary probability is positive. Perfect conditional return at 24, together with stationarity, implies $X_{j+24}=X_j$ almost surely. Thus $K=\sum_{j=0}^{23}X_j$ is shift-invariant. Ergodicity would make it a constant integer. Yet the conditional expected value of $K$ given $X_0=1$ equals $\sum_{j=0}^{23}r_j=7/2$. Two ergodic components suffice by construction. The argument depends on preparation by conditioning the stationary distribution on the same mark.

Exact equality here matters. Concatenate $5n$ blocks of the first 24-phase pattern and $n$ blocks of the second into a single cyclic pattern. It has $16n$ marked starts. Their proportions in the two block types are again $5/8$ and $3/8$. Couple each marked launch to the same within-block phase on its original cycle. A trajectory can disagree with that cycle through clock $T$ only if it reaches one of the two boundaries between different patterns. At most $2T$ starting phases do so. The total variation distance of the entire passive binary record through $T$ is at most $\min(1,T/(8n))$. Exactly four marked starts lose the mark at lag 24, so the single-cycle rate there is $1-1/(4n)$. Finite data with positive tolerance cannot certify exact nonergodicity from this conditional record alone.

## One additional operation at the same site

Launch from site zero. In one setting evolve for four ticks and read whether the walker is at zero. In the other, at tick two couple a binary pointer to the projector onto site zero, preserving its coin and preserving coherence throughout the complementary space. Keep every launch and ignore the intermediate answer when tabulating the final origin rate. A destructive hit, a full position measurement, and resolved coin detection define different instruments.

The normalized two- and four-step amplitude matrices at site zero are

$$
K_2=\tfrac12\begin{pmatrix}1&-1\\1&1\end{pmatrix},
\qquad K_4=\tfrac14\begin{pmatrix}-1&-1\\1&-1\end{pmatrix}.
$$

The intermediate-hit branch has matrix $K_2^2$ and weight $1/4$ at the final origin. The complementary branch has matrix $K_4-K_2^2$ and weight $1/8$. Each weight is independent of the input coin. Ignoring the binary record adds the branch probabilities to $3/8$. Without the intermediate record the amplitudes add coherently, giving $1/8$. The passive cycle mixture gives $1/8$ in either setting. Any stationary or nonstationary trajectory description in which reading the label leaves the subsequent trajectory, launch population and final detector unchanged also predicts equality between settings. Coupling the apparatus to hidden state can change that prediction. Figure 8(b) measured terminal position without this intermediate operation. Implementing the test requires a calibrated, selective-in-position binary coupling, the same preparation in both arms, and the same launch denominator and terminal response. [Kofler and Brukner on comparing records with and without an earlier measurement](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.87.052115)

Run `python check_passive_origin.py` in this directory. It uses the existing integer transfer routine, exact fractions for the cycles and both projections, and the deposited Figure 8(b) coordinates. OpenAI Codex constructed and checked the comparison. Kirtus Justus holds scholarly responsibility for the research program.
