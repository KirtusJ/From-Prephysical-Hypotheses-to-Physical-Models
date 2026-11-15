# What a clean return certifies about hidden position records

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Suppose a position reader reports a cell of the reflecting walk but may leave a finer mark in an inaccessible environment. A source return can certify that this reader preserves coherence on a whole set of future states. The result depends on a specific physical model of the hidden mark and gives a sharp transfer constant. It addresses the measurement assumption behind the [successive reflected position records](Reflected_position_histories.md). The earlier [protected-word return](Returning_a_protected_position_word.md) tests probability weighting given a specified coherent inverse.

## The tagged cell

Within one reported cell let \(Q_i\) be orthogonal projections onto the locations that may leave distinct marks. A site-only reader has one projector per site, including both rails. If the apparatus can distinguish rails, use the finer projectors. The unknown interaction is a nondemolition isometry
\[
 Q_i\psi\otimes|0\rangle\ \longmapsto\ Q_i\psi\otimes e_i,\qquad \|e_i\|=1 .
\]
A relative phase at a site is included in \(e_i\). The map preserves each sector’s wavefunction and has the same tags across calibration and science. Discard the environment. The reported cell is written coherently with no further action inside it. Assume ordinary probabilities and a calibrated inverse of the preparation that leaves the inaccessible environment untouched.

For a calibration launch prepare \(\psi=Ue\) from one sharp state \(e\). Set \(m_i=\|Q_i\psi\|^2\) and \(P=\sum_i m_i>0\) in the nominated cell. Read that cell, undo \(U\), and test the exact initial state on all original degrees of freedom. Keep failures, other reported cells and their incident rates. The environment amplitude at the joint clean return is \(\sum_i m_i e_i\) because \(\langle e|U^\dagger Q_i U|e\rangle=m_i\). With \(p_i=m_i/P\) and \(R\) the joint return probability per incident launch, the normalized deficit is
\[
 d_p=1-R/P^2
    =1-\left\|\sum_i p_i e_i\right\|^2
    =\sum_{i<j}p_i p_j\|e_i-e_j\|^2 .
\]
At \(d_p=0\) all tags of positive weight are identical, including relative phases. Distinct orthogonal hidden marks, for example, give \(R=\sum_i m_i^2\). A noiseless classical copy of one *common* label in the environment is harmless inside this cell. For a fixed calibration deficit many different tag geometries can yield the same number.

## Transfer to different preparations

For a future pure state entirely within the cell, let \(q_i\) be its sector weights, allowing entanglement with an external reference. After tracing out the environment its fidelity with the original pure state, in the squared-overlap convention, is \(1-d_q\). This follows by projecting the tagged state onto the original joint state, leaving environment amplitude \(\sum_i q_i e_i\). The half trace distance from the ideal output is at most \(\sqrt{d_q}\): purify the ideal output with the normalized environmental return amplitude and use contractivity of trace distance. If that amplitude vanishes the bound is one. Purifying a mixed input gives the same operational bound.

Consider several calibrations with distributions \(p_a\) and positive testing weights \(\alpha_a\) summing to one. Use a graph on the target sectors with edge weights \(c_{ij}=\sum_a\alpha_a p_{ai}p_{aj}\). Include any additional sectors reached by the calibrations. The total normalized deficit is
\[
 D=\sum_a\alpha_a d_{p_a}=\sum_{i<j}c_{ij}\|e_i-e_j\|^2 .
\]
A zero deficit certifies exact preservation on all inputs supported on a target set \(S\) precisely when its vertices lie in one connected component. In fact equality forces identical tags along every positive edge. Conversely choose opposite phase tags on two disconnected components. Every calibration then passes perfectly, while an equally weighted superposition across those components is sent to an orthogonal state. Thus one full-support probe suffices, and two-sector probes require a connected set of pairs, at least \(n-1\) when the graph has \(n\) target sectors and no other vertices.

For a connected target define \(R_{ij}\) as the effective resistance, equivalently the supremum of \((h_i-h_j)^2/\mathcal E(h)\) over nonconstant real potentials, with \(\mathcal E(h)=\sum_{k<l}c_{kl}(h_k-h_l)^2>0\). Set \(R_*=\max_{i,j\in S}R_{ij}\). For a singleton take \(R_*=0\). The sharp universal bound for all future states on \(S\) is
\[
                    d_q\ \le\ \min(1,R_*D/4).
\]
To prove it for a scalar potential \(h\), its variance under \(q\) is at most one fourth of its squared range on \(S\). This follows by subtracting the midpoint of the extreme values before squaring. The resistance inequality bounds that squared range by \(R_*\mathcal E(h)\). Apply this to each real coordinate of the environment vectors in their finite-dimensional real span and sum. For a given known \(q\) the optimal linear coefficient is the supremum of \(\operatorname{Var}_q(h)/\mathcal E(h)\). [Spielman, effective resistance and the Laplacian energy](https://www.cs.yale.edu/homes/spielman/561/lect14-18.pdf)

Sharpness is local around perfect return. Take a maximizing pair and the scalar voltage attaining its resistance, and balance \(q\) on that pair. Use unit scalar tags \(e_i=\exp(i\epsilon h_i)\). Their squared separations divided by \(\epsilon^2\) tend to \((h_i-h_j)^2\). Hence \(d_q/D\to R_*/4\). The same phase construction proves sharpness of the variational coefficient for prescribed \(q\). Phases alone can exhaust the small-error bound even when the environment carries no distinguishable classical information. For one full-support probe \(\mathcal E(h)=\operatorname{Var}_p(h)\), giving \(R_{ij}=1/p_i+1/p_j\) for distinct \(i,j\). Weighted Cauchy–Schwarz proves the upper bound, and the potential with entries \(1/p_i,-1/p_j\) at those sites and zero elsewhere attains it. Rarely visited sectors can amplify a small calibration error substantially.

## One reflecting walk tests both sides

Use the [six-well reflecting interval](Reflecting_wells_and_the_classical_limits_of_a_walk.md) with positive wall phases, source \(0,R\), uniform Hadamards and a binary position read at the midpoint. The left cell consists of wells 0, 1 and 2. At tick eleven its site masses have numerators \((81,153,333)\) over 2,048. For tags depending only on the site this single return controls all left-cell coin and site preparations with coefficient
\[
 \frac{567}{4}\left(\frac1{81}+\frac1{153}\right)=\frac{91}{34}.
\]
For rail-dependent tags the same launch misses \(0,R\), whose amplitude vanishes at the read. A minus sign on that sole mode passes the left return with zero deficit at tick eleven. It sends an equal superposition of the two rails at well zero to an orthogonal state on a future use.

Keep the same bin, source, coins and walls; take six ticks before the read instead. The left rail masses have numerators \((4,4,4,1,4,9)\) and the right rail masses \((9,1,25,1,1,1)\), in well order \(R,L'\) and units of \(1/64\). Every directed mode is now tested. One clock and one binary read provide a clean-return rate for each reported half. Their uniform fidelity-deficit coefficients are \(65/8\) and \(19\) respectively. The hidden minus at \(0,R\) changes the left returned signed numerator from 26 to 18 over 64 and gives \(d_p=88/169\). This clock is the first from this launch with both rails occupied in all six wells. Its use in a later flight requires the same tag interaction on the later encounter. The kinematic probabilities and the time independence of this interaction have not been measured here.

With fresh environments implementing the same calibrated channel on each use, the classical–quantum record after a bin read has half trace distance at most \(\sum_B P_B\min(1,\sqrt{R_{*,B}D_B/4})\) from an ideal coherent projection on the same input, with \(P_B\) its incident bin probabilities. This uses the exact classical labels and the conditional within-bin bounds. The supremum over inputs is at most the largest bin bound. Summing per-use worst bounds by telescoping contracts through all later gates and adaptive record processing. Reused environment memory conditioned on past outcomes requires calibration on its relevant states. A sector-dependent rotation inside an unmodeled rail space, finite readout errors, and inverse drift lie beyond the diagonal-tag hypothesis. A measured deficit attributes none of those errors individually.

The [exact checker](check_tag_echo_resistance.py) propagates the six-well wavefunction and its tagged return, replays the two tested clocks by direction words, and evaluates real unit-vector tags using rational arithmetic. The [complete results](results/tag_echo_resistance.json) retain all clocks through eleven, the failed and passing phase controls and a sequence approaching the sharp coefficient. [Finite Lean certificate](lean/TagEchoResistance.lean) verifies both rail-support patterns and the hidden sign at the source. These are model calculations on the proposed recorder.
