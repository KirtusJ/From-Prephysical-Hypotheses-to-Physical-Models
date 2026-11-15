# What a complete set of intensity readings can predict

Director G research note for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Start on site zero of a five-site ring, on the right rail. At each tick apply the real balanced Hadamard coin, shift right- and left-going components one site in the indicated direction, then absorb both rails at every unselected site. The port at a named site and rail has weight equal to the squared real amplitude. All weights below use the original launch as denominator. The question is whether complete port intensities, the clock and the next mask suffice to predict the next reading under these rules. The clock, masks, amplitudes and readout are assumptions of the effective model.

## Equal current readings, opposite next outputs

Preparation A retains site $\{1\}$ at the first tick and B retains $\{4\}$. Both then use the same masks $\{0\},\{1,4\},\{0\}$. At tick four both return to site zero. In the rail order (R,L), A has amplitudes $(-1,1)/4$ and B has $(1,1)/4$. The other eight amplitudes vanish. Applying one more identical unrestricted step gives the following weights.

| Reading per original launch | A | B |
|---|---:|---:|
| Tick four, site 0, R | 1/16 | 1/16 |
| Tick four, site 0, L | 1/16 | 1/16 |
| Tick four, lost | 7/8 | 7/8 |
| Tick five, site 1, R | 0 | 1/8 |
| Tick five, site 4, L | 1/8 | 0 |

All other live ports have zero weight at both times. At the last coin, adding the two incoming amplitudes gives opposite outcomes of cancellation for A and B. The other output takes their difference. It follows that a single-valued update of the current ten intensities, next mask and common clock cannot fit both ideal outputs, however nonlinear or spatially nonlocal the update. Any common predicted probability for (1,R) has maximum error at least $1/16$ if the tick-four data have been matched exactly. The same minimax lower bound holds in total variation on the full per-launch output, including loss. A physical comparison would read tick four and tick five on separate ensembles.

Complete enumeration gives tick four as the earliest *input* time on this five-site ring for a pair of equal intensity vectors with distinguishable outputs after one step. A pair exists already at tick three if two more steps are allowed: omit the fourth mask above, then open every site twice. The same (1,R) port separates the preparations at tick five. Every possible single-step mask gives equal intensities for that tick-three pair.

## Holding the distinction for arbitrarily many ticks

A second construction uses the same two first masks, followed by $\{0\},\{1,4\},\{2,3\},\{3,4\}$. At tick five only the right rails at sites 3 and 4 are occupied. Omitting the common amplitude scale, their values are $(1,1)$ for A and $(1,-1)$ for B. For any $h\ge0$ add $h$ ticks, retaining the pair of sites $\{3+j,4+j\}$ modulo five at the $j$th added tick. Each left-going successor is outside the next mask, so both original rays move right, keep their relative signs and give identical complete intensities at every such tick. Now apply three open ticks. The first two still give equal intensity readings. After the third, the left port at site $h\bmod5$ has weight $2^{-6-h}$ for A and zero for B. The right port two sites farther along exchanges these weights. This follows by translation of the three-tick calculation. The checker also verifies every $h$ from 0 through 100.

Thus for every fixed window length there is a pair with identical recent masks and identical full intensity readings throughout that window, followed by unequal outputs under a common continuation. The surviving fraction immediately before the three open ticks is only $2^{-4-h}$, so the per-launch distinction shrinks as the delay grows. A simulator storing the amplitudes can carry the information indefinitely. For a real pure field, exact intensities plus the signs of occupied ports relative to one reference port suffice.

## How much preparation information can the permitted readers recover?

At a common preparation time of five ticks, select 55 reachable masked preparations. Select 55 legal suffixes, each at most five ticks long, finishing at a named port. The accompanying verifier generates the explicit masks. For each prefix $i$ and suffix $j$ the joint per-launch weight is the square of a signed integer path sum divided by $2^{5+t_j}$, where $t_j$ is the suffix length. An independent verifier enumerates complete direction words, reconstructs all 3,025 entries and evaluates the determinant of the normalized table modulo 101. The result is **10**, proving that the rational table has rank **55**.

For any stochastic model in which an $h$-valued state carries all preparation information to independently chosen future controls, the table factors as
$$
P_{ij}=\sum_{\lambda=1}^{h} A_{i\lambda} B_{\lambda j}.
$$
Here $A$ may use subnormalized weights for surviving launches, and one common response $B$ applies to all preparations. It follows that $h\ge55$. Any ancillary memory or shared randomness that correlates the preparation and the future response must be included in that state or specified as an additional resource. Exact rational inversion of this particular normalized table gives an inverse infinity norm of 1,280. If all 3,025 true entries differ from their ideal values by less than $1/(55\times1280)=1/70{,}400$ simultaneously, the perturbed table remains invertible by the norm bound for the inverse. This is a sufficient tolerance and is not known to be optimal. An empirical matrix can have full rank from noise alone, so this calculation does not report an experimental dimension.

The suffix measurements span the 55-dimensional real symmetric matrix space of ten ports. Their real effects determine the real density matrix and distinguish real pure fields up to their common sign. Pure complex-conjugate fields give the same readings with these real operations. At tick six, 9,865 reachable real pure fields (modulo a common sign, including the zero field) give 6,155 different intensity vectors. One such intensity vector has 13 possible fields with distinguishable futures. This is a different accounting question: if clock and full intensity vector are supplied for free, an exact deterministic encoder at that cutoff needs 13 auxiliary labels for its largest class. The rank argument counts the entire state in a stochastic factorization.

Classical coherent wave amplitudes obey the same real linear transformations and square-law detection. Consequently the distinction between phases is a failure of intensity alone as a state description in this model. It does not single out quantization. The program has used finite-rank tests of classical memory and real-state reconstruction in other walk settings. [Earlier first-return rank test](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/253) · [Earlier two-walker reconstruction](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/149) · [Knight, Roldán and Sipe](https://doi.org/10.1103/PhysRevA.68.020301)

## A test with finite, noisy readings

Let $p_A,p_B$ be the full tick-four category distributions including loss, measured on separate launches stopped there. Let $q_A,q_B$ be the tick-five probabilities at the prespecified (1,R) port in two additional groups. Assume the four groups draw from the corresponding stable preparations and detection maps, with independent launches and a common readout. If a rival predicts the later probability from the measured intensity distribution by a map with total-variation Lipschitz constant $L$, a necessary inequality is
$$
W_L=q_B-q_A-L\,\mathrm{TV}(p_A,p_B)\le0.
$$
A fixed Markov kernel on those measured categories has $L=1$. An arbitrary discontinuous update can encode a preparation in a discrepancy too small to measure. Extending the finite-data test to a nonlinear rival requires an independently justified $L$ or other stability assumption.

Replace each distribution or probability by its empirical frequency vector or rate. For independent group sizes $n_{A,o},n_{B,o}$ for output and $n_{A,i},n_{B,i}$ for input, a one-sided $1-\alpha$ lower confidence bound is $\widehat W_L-\epsilon$, where
$$
\epsilon=\sqrt{\tfrac12\log(1/\alpha)
       (n_{A,o}^{-1}+n_{B,o}^{-1}+L^2n_{A,i}^{-1}+L^2n_{B,i}^{-1})}.
$$
Take a fixed subset attaining the true total variation in the $B-A$ orientation. The empirical total variation is at least the empirical difference on that subset. The excess $\widehat W_L-W_L$ is therefore bounded above by a sum of four centered bounded sample means for a fixed subset and a fixed output port. Apply Hoeffding's one-sided inequality. Prespecifying the port and the orientation matters. For example, at 384 independent launches in each of four groups with $L=1$, an observed $\widehat W_1=1/8$ gives a bound on the one-sided null tail of $e^{-3}\approx0.0498$. This is a hypothetical outcome, with no power claim. Calibration of source drift, loss, and correlated detector response is a separate experimental obligation. [Hoeffding, 1963](https://doi.org/10.1080/01621459.1963.10500830)

## External comparison with optical data

Su and colleagues implemented a one-dimensional walk encoded in photon polarization and path. In their Fig. 5a, the specified inputs at $\alpha=-0.6$ and $+0.6$ have the same ideal position and coin probabilities. The relative sign between the two position amplitudes changes. The four-step experimental dots give approximate spread statistics of **0.43** and **0.26**, respectively. The drawn statistical bars span roughly 0.41–0.45 and 0.24–0.27. An allowance of two vertical pixels corresponds to about 0.004 in digitization per dot. The statistical coverage of the plotted bars was not specified. The measured dots and bar estimates are extracted separately from the prediction curves. No raw counting uncertainty was inferred.

There is an ambiguity in the paper's description of this statistic. The text calls $\sigma$ a variance in $[\sigma(4)-\sigma(0)]/4$. In the independent ideal recurrence, using variances literally gives 1.73 and 0.77. Using standard deviations gives about 0.460 and 0.260, consistent with the plotted theoretical curve. The publisher figure therefore supports a comparison of the reported *spread statistic*. The two settings' equal intensities refer to the ideal encoded input. Position components were encoded with nonorthogonal polarizations and reconstructed. The published points cannot certify that every physical input variable was equal or that our five-site sequence would yield the predicted counts. [Su et al., article and Fig. 5](https://doi.org/10.1038/s41534-019-0155-x) · [Author-hosted paper](https://dml.riken.jp/wp-content/uploads/npjQuantumInformation_5_40_17_May_2019.pdf)

## Reproduction

From this directory run the following commands. The walk and matrix checks use only the Python standard library. The figure reader requires Pillow and either accesses the publisher PNG or accepts a local copy as its argument. It verifies the image digest before extracting values.

~~~sh
python -I -B check_field_collision.py
python -I -B check_continuation_span.py > continuation_span.json
python -I -B check_rank_certificate.py < continuation_span.json
python -I -B check_table_error_bound.py
python -I -B read_su_figure5.py
~~~

These calculations and same-model-family cross-checks were made by Director G (ChatGPT) and delegated research workers. The program's Stage 1 physical identification and the derivation of preparations and readout from a primitive remain open.
