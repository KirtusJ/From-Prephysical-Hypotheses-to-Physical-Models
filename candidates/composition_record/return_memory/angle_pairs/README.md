# Testing coherence between two unobserved sites with a first return at tick three

The first return occurred on tick three in 3,318 of 40,000 shots at a gate angle of \(3\pi/10\), and in 10,590 of 40,000 at \(7\pi/10\). Complementary angles give identical one-tick population transfers from every initial site in the ideal three-spin circuit. They give different return probabilities when the two surviving paths keep their relative phase. This comparison reuses the published IBM Sherbrooke jobs. A separate circuit proposed below would hold the gate angle fixed and intervene directly on the phase. [Original experiment, §VIII](https://arxiv.org/html/2401.09810v2#S8) · [Authors' data](https://doi.org/10.5281/zenodo.18429670) · [First-return extraction and circuit order](../../first_return_data/README.md)

## Prediction from the gate order

Write \(|i\rangle\) for one excitation on physical qubit \(i\), and \(c=\cos\theta,\ s=\sin\theta\) for the literal QASM gate argument. One RXX–RYY pair on a link acts on its two sites by \(G=cI-isX\) and leaves the unoccupied link unchanged. Each round applies \(U=G_{01}G_{12}\), rightmost gate first. Starting from site 0, the detector measures site 0 after each round. A null projects onto the two-dimensional span of sites 1 and 2 while preserving coherence within that span. The survivors have unnormalized column \(v_1=(-is,0)^\mathsf{T}\) after one round. Their subsequent null transfer \(M\) and return row \(r\) are

$$
M=\begin{pmatrix}c^2&-ics\\-is&c\end{pmatrix},\qquad
r=\begin{pmatrix}-isc&-s^2\end{pmatrix}.
$$

The second null gives \(v_2=Mv_1=(-isc^2,-s^2)^\mathsf{T}\). Insert a relative phase \(e^{i\phi}\) on site 2 immediately before the third round. The first-hit probabilities, with every launched shot in the denominator, are

$$
F_1=c^2,\quad F_2=s^4c^2,\quad
F_3(\phi)=\big|-s^2c^3+e^{i\phi}s^4\big|^2.
$$

The phase contrast \(F_3(\pi)-F_3(0)=4s^6c^3\) is positive for \(0<\theta<\pi/2\). A site Markov chain which uses the same per-link transfer probabilities \(c^2,s^2\) and observes site 0 gives \(s^4c^6+s^8\) in both arms, the midpoint. Each one-tick entry also equals \(|U_{ij}|^2\), since there is only one within-tick route between each ordered pair of sites. The first two hits therefore agree under either model. The second unobserved site must have had time to acquire amplitude for the pulse to matter.

The sign change can also be obtained by replacing \(\theta\) by \(\pi-\theta\). Now \(s\) is fixed and \(c\) changes sign. With \(Z=\mathrm{diag}(1,-1)\) acting on the survivor column, \(M(\pi-\theta)=M(\theta)Z,\ r(\pi-\theta)=-r(\theta)Z\). Because \(Zv_1=v_1\), the complementary angle reproduces a single pulse through tick three. At later ticks the equivalence requires a pulse before **every** subsequent survivor round. A reflected pair in the other half of the \(2\pi\) cycle complex conjugates the circuit and keeps the same ideal probabilities.

## All complementary archived angles

Use \(k\pi/50\) for gate angle \(k\). For each \(j=1,\ldots,24\), compare settings \((k_A,k_B)=(j,50-j)\) and also \((100-j,50+j)\). This geometric pairing uses the complete nondegenerate pairs regardless of the observed sign. The three remaining settings, \(k=25,50,75\), have zero ideal contrast and no distinct archived partner under this pairing. Their third-hit counts are 35,497, 0 and 35,085 respectively. The ideal gap is maximal at \(c^2=1/3\), with value \(32/(81\sqrt3)\). Its grid maximum selects \(j=15\) before considering the counts. This is a retrospective study.

| \(k_A,k_B\) | Shots per arm | First hits A/B, tick 1 | Tick 2 | Tick 3 | Still unhit after 3 | Observed third-hit gap \(B-A\) | Ideal gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| 15, 35 | 40,000 | 15,305 / 15,141 | 5,830 / 5,503 | 3,318 / 10,590 | 15,547 / 8,766 | 0.181800 | 0.227752 |
| 85, 65 | 40,000 | 15,296 / 15,853 | 6,176 / 5,559 | 2,936 / 10,283 | 15,592 / 8,305 | 0.183675 | 0.227752 |

Here the ideal no-pulse, pulse and Markov third-hit probabilities are respectively 0.087301, 0.315053 and 0.201177. The noiseless coherent circuit **overpredicts both observed gaps**. The signed empirical gaps are positive in 22 of 24 positive-sine pairs and 21 of 24 negative-sine pairs. The negative count differences occur at \(j=1,3\) in the first family (−6, −4), and \(j=1,23,24\) in the second (−7, −562, −53). The table also retains each arm's residual from the coherent prediction. [All 48 comparisons, including four disjoint observed categories per arm](pairs.csv) · [All 20 first-hit bins, censored counts and original job IDs](../../first_return_data/first_returns.csv)

Assuming independent shots within and across the two jobs in each pair, let \(n_A,n_B\) be their shot counts and let \(\widehat D\) be the difference of third-hit sample fractions. Applying Hoeffding's inequality to the signed sum of bounded observations and a union bound across 48 pairs gives simultaneous 99% intervals \(\widehat D\pm\sqrt{(1/n_A+1/n_B)\log(96/0.01)/2}\) for differences of the mean recorded probabilities. The common half-width is 0.015141. The two displayed pairs give intervals [0.166659, 0.196941] and [0.168534, 0.198816]. The positive lower bounds occur in 15 and 14 pairs, respectively. Within-shot dependence between measurement ticks is allowed. Job histograms cannot establish inter-shot independence, pulse fidelity or stationarity. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

## Detector gains and a direct intervention

Under the site Markov rival with identical gate transition kernels, both angles give the same distribution of true site paths. A common reporting process then gives the same observed first-hit histogram, even with site-, time- or history-dependent readout errors. A sensitivity bound allows the readout to differ between arms. Suppose one can couple their site paths identically, and, given any such path and matching recorded history, the two binary readout probabilities differ by at most \(\delta\) per tick. Couple each bit with the same uniform variate while the histories match. Their three-bit records disagree with probability at most \(1-(1-\delta)^3\), which also bounds the probability gap for the event “001” in chronological order. For example, \(\delta\le0.05\) allows a gap at most 0.142625, below the 99% lower limit 0.166659 for settings 15 and 35. This sensitivity calculation also covers two gains individually bounded within 0.025 of a common bit-response law. The experiment does not supply this calibration. Angle-specific gate errors, unobserved detector memory affecting the two jobs differently, or differences in their initial ensembles can violate these premises.

A direct experiment would run three identical gate rounds in both arms. Between the second measurement and the third round, apply either identity or \(\mathrm{RZ}(\pi)\) on **q[2]**, with a randomly assigned setting and matched compilation/timing. The pulse can be unconditional on the measured bits because earlier hits already belong to other bins. On the ideal survivor subspace it gives \(Z\) up to a global phase. Record the complete shot counts and compare \(F_3\) with all launched shots as denominator. With accurate earlier history and common final false-positive and true-positive probabilities \(f,e\), the observed gap is \((e-f)\,4s^6c^3\). The contribution \(f\,P(\text{two nulls})\) cancels because the pulse is later. If earlier reports can misclassify the physical projections the quantitative formula needs their measurement instrument. Randomization should be interleaved in acquisition time and accompanied by basis-site calibrations, so drift, unwanted transitions and pulse-dependent readout can be bounded. [IBM RZ definition and virtual implementation](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate)

The released jobs changed the gate angle at every round and contain no randomized q[2] phase intervention. Their comparison tests a model with shared one-step transfer and readout laws. A classical model that carries extra internal phase information or changes its transition rates with the programmed controls can reproduce a phase response. The prediction also uses squared amplitudes and coherent null projection as input. Agreement cannot independently derive the probability law or establish the research program's ontology.

## Reproduction

Run `python -I -O compare.py` in this directory. It checks the published first-return table's SHA-256 after LF normalization, accounts for every shot, compares the closed forms with direct three-site complex and stochastic gate evolution, and reproduces the comparison table. The output option `--output PATH` writes a new copy. The normalized SHA-256 of `pairs.csv` is `3cd9fda6e720d48e1e867227c7227e5f9c968d13e9fc6b2e02354adcbe382000`. The original grid and histograms are from Quancheng Liu, Sabine Tornow, David A. Kessler and Eli Barkai. The complementary-angle pairing, first-three-tick grouping and gate predictions are derived here. [Original dataset and CC BY 4.0 license](https://zenodo.org/records/18429670)
