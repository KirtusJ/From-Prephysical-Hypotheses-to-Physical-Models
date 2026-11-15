# Testing the retained qubit with four preparations at one site

Can the walk's own records distinguish a quantum memory from a device that measures its input and prepares a replacement? Four preparations and a final position probe suffice **if the preparation labels stay private and the readout is trusted**. No entangled reference qubit is needed for this test. After seven position writes the ideal four-label decoder predicts **82.42%** correct across all launches. Every channel that measures and prepares a replacement scores at most **75%** under these conditions. Keeping only the last site gives an entanglement-breaking channel at this clock. [Final-site channels and recovery with a Bell reference](recovering_a_qubit_from_position_messages.md)

## One source, one site, one clock

Use the sixteen-site ring, start at 0 on rail R, and apply H (balanced Hadamard) or I before every compulsory shift. R moves clockwise and L moves anticlockwise.

| Ticks | Source action | Result |
|---|---|---|
| 1–8 | Apply H, write the resulting position privately, then coast for seven I ticks. | Both outcomes reach site 8. The first private direction bit selects the basis, clockwise for Z and anticlockwise for X. |
| 9–16 | Again apply H, write the position privately and coast for seven ticks. | Both outcomes reach site 0. The second private direction bit selects the plus or minus member of the chosen basis. |
| 17–24 | Start with I for the Z basis or H for the X basis, then coast for seven ticks. Preserve coherence during this flight. | All four preparations reach site 8 at tick 24. The states, up to global phase, are R, L, $(R+L)/\sqrt2$ and $(R-L)/\sqrt2$. |

Each joint label has probability $1/4$ under ordinary position scoring. The two source writes are balanced conditional on the earlier label. No launch is discarded. Equal scoring of the two bright arms also makes these particular source bits fair in normalized power models that treat the two arms identically and leave dark arms dark. This symmetry alone cannot select the ordinary probability rule. Lean checks both signed input branches, the sites and the extra-copy control below from elementary shifts. [Lean certificate](../../../Director_G/lean/FourLocalPreparations.lean)

At site 8 begin $m$ copies of the same twelve-tick position-write block. These write outcomes determine the real orthogonal rail gate $O$ in the ideal instrument. The encoder receives only these $m$ positions and sends one label at their fixed deadline. A separate tester measures the rail in the private source basis. The Z test uses I followed by a shift and an exact position read. The X test uses H followed by the same shift and read. The score is one if the decoded answer matches the private sign and zero otherwise. Count against every incident launch. A receiver channel, including its selected correction, must be common to the four preparations and fixed before the tester reveals the basis. [Block specification](classical_positions_with_a_retained_qubit.md)

## Why the benchmark is 75%

Write the four input Bloch vectors as $r\in\{\pm e_x,\pm e_z\}$. In a measure-and-prepare channel, an input measurement with outcome $j$ has effect $w_j(I+a_j\cdot\sigma)$ and prepares an output with Bloch vector $b_j$. Here $\sum_jw_j=1$ and both vector lengths are at most one. Averaging the probability of a correct matching-basis read over the four inputs gives

$$
A=\frac12+\frac14\sum_j w_j(a_{jx}b_{jx}+a_{jz}b_{jz})\le\frac34 .
$$

Measuring Z and sending its observed eigenstate attains the bound. Classical memory of the measurement result, a public random seed independent of the source, or a refinement of the measurement outcomes can be absorbed into $j$. This is the accessible-fidelity benchmark for the specified input ensemble and trusted output test. [Fuchs and Sasaki on measuring and re-preparing an ensemble](https://arxiv.org/abs/quant-ph/0302092) · [Horodecki, Shor and Ruskai on entanglement-breaking channels](https://arxiv.org/abs/quant-ph/0302031)

The source must have the stated four states, with no side record of its choices accessible to the memory. For example, a device that learns the basis before measuring its input can measure that basis and score one. An unrestricted classical readout can also measure the input along $(e_x+e_z)/\sqrt2$, store the sign and report that same sign for either requested basis. Its mean is $(1+1/\sqrt2)/2$, above the benchmark. Trusted preparation and a physical matching-basis measurement on one output qubit are needed even if the reported setting frequencies look correct. A single classical register in the simulator records the label for later scoring and cannot establish physical isolation. A score above the bound excludes the measure-and-prepare class under these assumptions. It does not reconstruct the full channel or establish a prephysical origin for the tested states.

## What the four position labels carry

### Checking the preparation before testing the memory

A zero-write bypass runs the same source and immediately reads the matching basis. With a trusted readout, let $e_j$ be its wrong-sign probability on actual input $\sigma_j$, let $q_j$ be the actual prior, and set $\bar e=\sum_jq_je_j$. The trace distance from $\sigma_j$ to the ideal pure state $|j\rangle$ is at most $\sqrt{e_j}$. Any subsequent common quantum channel and binary read can change their success probabilities by no more than this distance. Thus the measure-and-prepare ceiling for the imperfect source is at most

$$
\frac34+\operatorname{TV}(q,\mathrm{uniform})+\sqrt{\bar e}.
$$

This bound uses the triangle inequality and concavity of the square root. It assumes that the tested and bypassed launches use the same source ensemble and that the memory has no further source information. A private random routing choice lets both arms sample the same incident ensemble. The bypass sees only the label-conditional rail states. An extra record that identifies the basis with reliability $g$ leaves those states unchanged and lets a replacement device score $(1+g)/2$. A separate six-qubit version tests source coherence at the release cut. [Claude’s cross-review and counterexample](../../../Director_Z/cross_review/subagent_xr259_four_preparations/REPORT.md) · [Six-qubit revival and sharp leakage bound](a_source_revival_bounds_hidden_records.md)

Actual sampling would require upper confidence bounds for the calibration errors and a lower bound for the memory score. An ideal coherent bypass scores one, while the extra-copy bypass below scores $3/4$. The same [circuit exporter](four_state_circuit.py) accepts a zero block count for either arm. [Fuchs and van de Graaf on trace distance and fidelity](https://arxiv.org/abs/quant-ph/9712042)

### Recovering the sign

Write $(\cos\theta,\sin\theta)$ for the first column of $O$, up to overall sign. For a rotation choose the nearer of identity I and the quarter-turn J. For a reflection choose the nearer of Z and the rail swap X. Choose I or Z when the two first-column magnitudes tie. Undoing the indicated gate would leave a rotation on the rail. A matching-basis read has the same survival probability for each of the four inputs,

$$
\max(\cos^2\theta,\sin^2\theta)=\frac{1+|\cos 2\theta|}{2}.
$$

The inverse corrections need no additional physical gates in this test. J flips the two possible readout bits in either basis, X flips only the Z-basis answer, Z flips only the X-basis answer, and I leaves either answer alone. The encoder selects its label without seeing the source basis, source sign or probe outcome. These fixed sign permutations are equivalent to the indicated physical Pauli corrections followed by the trusted readout.

For optimality, let $B$ denote the XZ block of the Bloch matrix of any trace-preserving quantum recovery. Antipodal input states show that $B$ has operator norm at most one. Its singular-value decomposition represents it as a convex mixture of orthogonal planar matrices, by mixing diagonal sign matrices to obtain the singular values. Every orthogonal action on that Bloch plane is realized by conjugation by a real qubit unitary. The average best-label score is convex separately in each decoder, so an optimal choice can be taken from these realized orthogonal actions. The affine offset drops out of the four-input average. The encoder can choose the best label on each record because the ideal record law is independent of the input. Final-site-dependent recoveries are allowed throughout.

A correction line at angle $\phi$ in the gate's own determinant sector gives excess over $1/2$ equal to $\cos(2\theta-2\phi)/2$. A correction from the opposite sector leaves a reflection, whose four-state average is exactly $1/2$. At each final site the limiting angle is uniform modulo $\pi$ and the two determinant signs are equiprobable. Each label's positive excess averages to $1/(4\pi)$ over both sectors. The maximum excess is at most the sum of all positive excesses. With two, three or four labels this upper bound is attained by distributing the labels between the signs and using orthogonal lines in a sign plane that gets two. Their positive angular intervals have disjoint interiors, and an opposite-sector fallback is available. Thus the optimal limiting scores for two, three and four labels are **65.92%, 73.87% and 81.83%**, respectively, or $1/2+t/(4\pi)$ for $t=2,3,4$. Weak convergence applies uniformly over these fixed-size decoder tuples by compactness. [Conditional angular mixing and its premises](recovering_a_qubit_from_position_messages.md)

The [finite calculation](check_four_state_alphabet.py) propagates the angular harmonics at each final site and sign by integer arithmetic. For three labels it bounds each possible line's positive excess from above. For the four Pauli labels it bounds $|\cos 2\theta|$ below. It also sums all path weights by their exact projective gate at seven writes. The seven-write score is $226560354573/274877906944$. At **eighty writes** every three-label decoder scores **below 0.748**, while the specified four-label encoder scores **above 0.781**. The same final-site information is available on both sides of this comparison.

The four transmitted labels can require a much larger working memory to compute. For any passive streaming controller that maintains a fixed four-state score above chance at increasing read times $N$, four native two-write records imply a lower bound of order $(\log N)^2$ on the number of working states. This bound still allows the decoder access to the final site and determinant sign. [Two independent angles and the memory bound](memory_cost_of_four_position_words.md)

## A control that damages only two preparations

Make one extra position copy immediately after the shift at tick 17. For the X preparations, the two signed components are then recorded at different sites. Even when they later meet, the reduced rail density is $I/2$ for either private sign. The Z preparations are already sharp and keep their original performance. All subsequent scalar position records retain the same distribution in the ideal and extra-copy experiments. A private readout that ignores the extra copy therefore has mean $1/4+A_{\rm ideal}/2$ for the four-label decoder, or **66.21%** at seven writes. The ideal position records by themselves cannot reveal this defect. [Signed branch and density calculation](../../../Director_G/lean/FourLocalPreparations.lean)

## Replay and scoring

Two ideal Aer replays used 8,192 launches apiece. Counts give correctly recovered signs divided by launches in that preparation. All launches and every observed output word are retained.

| Source preparation | Coherent preparation | Extra copy at tick 17 |
|---|---:|---:|
| R | 1,710 / 2,048 | 1,669 / 2,048 |
| L | 1,646 / 2,019 | 1,652 / 2,018 |
| $+$ | 1,706 / 2,069 | 1,042 / 2,069 |
| $-$ | 1,687 / 2,056 | 1,061 / 2,057 |
| **All launches** | **6,749 / 8,192 (82.39%)** | **5,424 / 8,192 (66.21%)** |

Every recorded probe jump decoded. The two X rows account for most of the score loss, as predicted by the source control. These separate seeded runs used the same encoder. [Coherent-source count record](../../../Director_G/results/four_state_coherent_8192.json.gz) · [Extra-copy count record](../../../Director_G/results/four_state_copied_8192.json.gz)

The [four-qubit exporter](four_state_circuit.py) uses one rail and three address qubits. At seven writes both circuits take 109 ticks. Bits 0 and 1 of the output are the private basis and sign. The next seven triples encode the intermediate absolute address $y$, the number of left shifts modulo eight. The final triple encodes the probe address. Its difference from the last intermediate code, modulo eight, is 0 for clockwise or 1 for anticlockwise. Only the seven intermediate triples enter the position encoder. Missing launches and invalid probe jumps count as failures in the [scorer](four_state_records.py). The source and matching probe must also be independently calibrated on a physical device.

    python -I -B four_state_circuit.py --blocks 7 --qasm seven.qasm
    python -I -B four_state_circuit.py --blocks 7 --copy-at-17 --qasm seven-copy.qasm
    python -I -B four_state_records.py simulate seven.qasm seven.json.gz --blocks 7 --shots 8192 --seed 24127
    python -I -B four_state_records.py simulate seven-copy.qasm seven-copy.json.gz --blocks 7 --shots 8192 --seed 24128
    python -I -B four_state_records.py score seven.json.gz

Simulation requires Qiskit, its OpenQASM 3 importer and Aer. Scoring saved counts uses standard Python. Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the source, control, mathematics and replays. No hardware measurements enter this result.
