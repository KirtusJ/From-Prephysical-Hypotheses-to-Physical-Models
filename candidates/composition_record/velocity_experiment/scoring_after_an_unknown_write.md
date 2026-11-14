# Testing the probability rule after an unknown position-write disturbance

A walker on sixteen sites gives a direct test of ordinary site probabilities with no phase comparison between a gate and a bypass. The test works even if an intermediate position detector leaves a different, unknown two-rail state after every result. Only three frequencies are needed. The same walk has an exactly classical two-state position record for every such rail-state history when the read probabilities are ordinary.

The [twelve-tick construction](ordinary_powers_with_a_retained_qubit.md) also makes the *entire* ordinary position distribution independent of the rail. The shorter schedule here offers an integer score and a two-state classical position projection.

## Ten ticks and one signed count

Start at a known site on the sixteen-site cycle. Each tick applies the same coin at every site, then shifts the R rail clockwise by one and the L rail counterclockwise by one. Use the ten coins **H I I H H H H H I I**, where \(H\) is the real balanced Hadamard and \(I\) is identity. Write the complete site and repeat the block as many times as specified. At each write use displacement \(d\) relative to the last actual site, reduced modulo 16. All eight even residues are available to the reporter. The origin of the next block may be any recorded site. Three address qubits record the cumulative left-step count modulo eight, and a fourth qubit stores the rail. From two recorded counts the displacement is \(10-2\Delta y\bmod 16\).

For each displacement let \(T_d\) propagate the two input rails to the two final rails at that site. The ordinary kinematic mass is \(\operatorname{tr}(\rho T_d^\dagger T_d)\). This use of position to measure an effect on the input coin also appears in quantum-walk realizations of generalized measurements. Here the effects are needed to specify competing read frequencies. A single density matrix \(\rho\) applies to all potential outputs of a given flight. It may be mixed, complex, entangled with an idle environment, chosen with the detector type, or set using the whole past. [Kurzyński and Wójcik](https://arxiv.org/abs/1208.1800)

| Displacement \(d\) | \(64T_d^\dagger T_d\) | Score given to this outcome |
| --- | --- | ---: |
| 0 | \(8I\) | \( -8 \) |
| 2 | \(\begin{pmatrix}5&1\\1&13\end{pmatrix}\) | 0 |
| 4 | \(2I\) | \(+8\) |
| 6 | \(\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\) | 0 |
| 8 | \(32I\) | \(+1\) |
| 10 | \(\begin{pmatrix}1&1\\1&1\end{pmatrix}\) | 0 |
| 12 | \(2I\) | \(+8\) |
| 14 | \(\begin{pmatrix}13&-1\\-1&5\end{pmatrix}\) | 0 |

In particular, the expected ordinary score \(8[P(4)+P(12)]-8P(0)+P(8)\) equals zero for *every* \(\rho\). The antipodal mass is strictly largest for all input states. The nonscalar effects above have eigenvalues \(9\pm\sqrt{17}\) or \(0,2\), before division by 64. A dark site of a particular coin state remains in the outcome table. [Reproduce the matrices, including zero entries](check_scalar_walk.py)

Suppose a reader assigns each complete site its kinematic mass to the power \(q\ge0\), then normalizes over occupied sites. Occupied-support counting means equal weight for positive sites at \(q=0\). Let \(w_d=64\,\operatorname{tr}(\rho T_d^\dagger T_d)\). The expected score is

\[
 G(q,\rho)=\frac{16\cdot2^q-8\cdot8^q+32^q}{\sum_{w_d>0} w_d^q}
 =\frac{32^q(1-4^{\,1-q})^2}{\sum_{w_d>0}w_d^q}.
\]

The numerator cancels only at \(q=1\). The maximum selector \(q=+\infty\) always reports the antipode and scores one. Since there are at most eight positive terms and none exceeds \(32^q\), the following bound has no unknown coin parameter. For \(h>0\),

\[
 \inf_{\rho,\,|q-1|\ge h}G(q,\rho)\ \ge\ v_h=(1-4^{-h})^2/8 .
\]

The bound covers both a fresh draw of \(q\) and persistent detector types. The hypothesis concerns a common exponent across the potential site outcomes of that particular read. A separate exponent per site, a rail-by-rail power before pooling, or a freely adjustable reporting channel gives a different experiment. A known position at the beginning of each flight is essential; coherence between two possible starting sites changes its site effects.

## Prior records and whole-word scoring

For a sequential instrument, the bound holds conditional on any actual history and the hidden state before the next outcome. Hence the unconditional mean score at a given write bounds the fraction of launches with \(|q-1|\ge h\) there by \(E[S]/v_h\). Mean zero forces ordinary scoring on that write almost surely. This proof requires localization at the recorded site and the stated free evolution in the next block. It requires no prescribed post-write coin, knowledge of its Bloch vector, or resetting of a hidden mode.

There is a second possibility: on a fixed finite horizon a mode might score an entire word of positions by a single power \(Q\) of its ordinary joint mass. Allow a different ordinary reference tree for each hidden type, provided the conditional masses at every occupied node come from the stated block and some localized coin. At the **last** write, conditional on a parent under the tilted word law, common prefix factors cancel and the relative probabilities of its leaves have the same power \(Q\). Any globally maximum word ends in the unique ordinary maximum at its parent, the antipode. Thus \(E[S_{\mathrm{last}}]\ge v_h\,\Pr(\text{whole-word},|Q-1|\ge h)\), also bounding nonordinary sequential incidences at the last write in the same sum. An exact zero forces ordinary global scoring. Ordinary global modes then contribute zero to every earlier score since ordinary future continuations sum to one. Zero mean at each earlier clock forces ordinary scoring at those realized sequential decisions. The proof applies to every specified finite number of writes. It leaves the relative population of the two ordinary implementations unidentifiable.

**Finite data.** For \(N\) independent incident launches and \(J\) prespecified writes, a simultaneous one-sided upper limit for each score mean adds \(16\sqrt{\log(J/\alpha)/(2N)}\) to its sample upper bound. Missing records take scores from \(-8\) to \(8\); a missing site may affect two consecutive displacements. A separately warranted bound \(k\) on the number of misclassified displacement scores widens a mean by at most \(16k/N\). These conservative bounds can share launches. Small populations and small deviations may be unresolved. [Hoeffding's inequality](https://doi.org/10.1080/01621459.1963.10500830)

For earlier clocks in the mixed global/sequential model, applying the local bound directly to the observed score can miss a signed whole-word contribution. For \(0<h<1\) the last score limits the far-global fraction to \(F=\min(1,U_{\rm last}/v_h)\), on the confidence event if the upper limit is nonnegative. On at most \(K=8^J\) positive words the total variation between an ordinary word law and its whole-word tilt with \(|Q-1|<h\) is at most \(\epsilon_h=\min(1,\sqrt{h\log K/(1-h)})\), uniformly even with very small weights. For an earlier mean upper limit \(U_j\) and a separation \(\delta>0\),

\[
 \Pr(\text{sequential},\,|q_j-1|\ge\delta)
 \ \le\ \frac{U_j+16\epsilon_h+8F}{v_\delta}.
\]

Here a far-global launch can score as low as \(-8\), and a near-global tilt changes a bounded score by at most its range times total variation. For a known sequential-only experiment the earlier bound is simply \(U_j/v_\delta\). Negative upper limits can challenge the model; conservative limits greater than one leave the corresponding fraction unresolved. The [shorter eight-tick variant and derivation of the tilt bound](uncalibrated_coin_error_bounds.md) treats the second required rate when the largest mass depends on the coin.

## A classical position record on the same apparatus

Record the class of \(X_{10j}-X_0\) modulo four: it is either zero or two. At each ordinary block this class flips on displacements \(2,6,10,14\). Their four matrices sum to \(20I\) in the units of the table, hence the flip probability is \(5/16\) for every localized coin. It remains \(5/16\) conditional on every past site record. The flip indicators are therefore independent Bernoulli variables under any permitted post-write rail dynamics. On the two classes the observed Markov chain has stay probability \(11/16\), and the expected product of class signs separated by \(m\) writes is \((3/8)^m\). This is an exact finite-ring statement. It makes no extrapolation to a continuous trajectory between site measurements.

The probability test and this classical chain share the same preparations and records. The global synchronized \(H\) factors change by a common sign under \(\sqrt2\mapsto-\sqrt2\); the frequencies here cannot name either field embedding. This removes the addressed-gate phase assumption when testing the **probability response**. The separate [addressed embedding test](selecting_the_real_embedding.md) needs that phase convention. Both constructions still assume linear signed propagation, physical site localization, and reliable or independently bounded reporting. Deriving those premises and the interacting quantum and classical dynamics from common prephysical primitives remains open.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility for the program. OpenAI Codex developed the construction, proof and checks.
