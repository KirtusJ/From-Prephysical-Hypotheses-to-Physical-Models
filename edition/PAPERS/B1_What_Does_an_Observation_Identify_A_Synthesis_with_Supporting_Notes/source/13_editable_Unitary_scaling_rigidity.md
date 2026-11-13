# Unitary scaling rigidity

## 2. Postulates and notation

Let `M_2(C)` denote one-qubit matrices and `M_4(C)` two-qubit matrices. For `lambda>0`, let `S_lambda` fix the identity and multiply every traceless Pauli component by `lambda`. Let `G_lambda=S_lambda⊗S_lambda`, acting on matrices on the *supplied* two-qubit tensor product. For a tensor-product Pauli `sigma_a⊗sigma_b`, put `w(a,b)=1_{a≠0}+1_{b≠0}`; then `G_lambda(sigma_a⊗sigma_b)=lambda^{w(a,b)}(sigma_a⊗sigma_b)`.

The channel `D(A)=Tr(A) I_4/4` is completely depolarizing. For a two-qubit unitary U write `Ad_U(A)=UAU†`. A gate set consists of physical preparations, effects and (trace-preserving or outcome-conditioned) completely positive maps with the same supplied product structure. The gauge transformation on operations is `Phi -> G_lambda Phi G_lambda^{-1}`, with effects transformed dually. This is a predictive similarity, **not** a physical channel `G_lambda` on arbitrary states if `lambda>1`.

## 3. Theorem: a noiseless entangling unitary forbids nontrivial Bloch-scaling gauge

**Theorem 1.** For `lambda>0`, `lambda≠1`, and a unitary `U` on two qubits, the linear map

`Psi=G_lambda∘Ad_U∘G_lambda^{-1}`

is CPTP **if and only if**, up to overall phase, `U` is a product of one-qubit unitaries or a product followed by SWAP. Consequently, if U can entangle some pure product input, Psi is not CPTP for `lambda≠1`.

**Proof.** In the normalized Hermitian Pauli basis, `Ad_U` is a real orthogonal 16×16 matrix `R` and `G_lambda` is positive diagonal `D`, with entries `1`, `lambda` (weight-one Paulis) and `lambda^2` (weight-two Paulis). The candidate `T=D R D^{-1}` is unital and trace preserving. Every unital trace-preserving completely positive map is a Hilbert–Schmidt contraction. If T is CPTP, all its singular values are at most one. But `|det T|=|det R|=1`; their product is one, so every singular value is exactly one and `T^T T=I`. This implies `R^T D^2 R=D^2`, hence R preserves the eigenspaces of D². Since `lambda≠1`, it must preserve the six-dimensional one-body subspace

`V_1=span{sigma_j⊗I, I⊗sigma_j : j=x,y,z}`.

Conjugation by U therefore normalizes the Lie algebra `su(2)⊕su(2)`. Its two simple ideals can only be individually preserved or exchanged; every automorphism of a single `su(2)` ideal is implemented by a one-qubit unitary. The remaining unitary commutes with the entire two-qubit matrix algebra and is scalar. Thus U is local or local followed by SWAP. Conversely, those unitaries preserve Pauli weight, commute with G, and yield exactly `Psi=Ad_U`, which is CPTP. QED.

The proof combines elementary Lie-algebra automorphisms with established Hilbert–Schmidt contractivity for unital CPTP maps. It is not asserted to be an original normalizer theorem.

**Direct CNOT witness.** For `U=CNOT`, one has

`Psi(X⊗I)=lambda X⊗X`, `Psi(X⊗X)=lambda^{-1} X⊗I`.

For either `lambda>1` or `lambda<1`, a norm-one Hermitian unitary Pauli is mapped to an operator of norm greater than one. A positive unital map cannot do that. This immediately proves nonpositivity for the CNOT instance without Choi analysis.

## 4. Exact noisy counterexample: physical entangling gates on both sides

**Theorem 2 (explicit conditional counterexample).** Take `lambda=3/2`, `p=63/100`, and

`Phi_A=(1-p)Ad_CNOT + p D`,

`Phi_B=G_lambda Phi_A G_lambda^{-1}`.

Both maps are CPTP and are entangling channels. The two complete models with the above A/B preparations and effects, their same calibrated one-qubit rotations, and their respectively defined joint gates predict identical probabilities for every circuit assembled from these named operations, including arbitrary repetitions and adaptive classical feedback. Their identically labeled source purities still differ.

**Proof of CPTP.** Trace preservation and unitality are immediate. Using the unnormalized 16×16 Choi matrix `J(Phi) = sum_ij |i><j| ⊗ Phi(|i><j|)`, exact Gaussian-rational arithmetic gives the spectrum of `J(G Ad_CNOT G^{-1})`:

| Eigenvalue | Multiplicity |
|---|---:|
| `25/6` | 1 |
| `5/12` | 4 |
| `-5/12` | 4 |
| `0` | 6 |
| `-1/6` | 1 |

Because `J(D)=I_16/4`, the transformed depolarized gate has Choi spectrum:

| Eigenvalue | Multiplicity |
|---|---:|
| `1/300` | 4 |
| `23/240` | 1 |
| `63/400` | 6 |
| `187/600` | 4 |
| `2039/1200` | 1 |

All eigenvalues are strictly positive. This proves CP. In fact the exact minimum depolarization making this transformed gate CP is `p=5/8`; the chosen `p=63/100` lies strictly inside that region, with minimum Choi eigenvalue `1/300`. The original Phi_A is trivially CPTP.

**Proof of entanglement generation.** For the pure product input `|+><+|⊗|0><0|`, the two output partial transposes have eigenvalue spectra respectively `{137/400 (three times), -11/400}` and `{87/200, 137/400 (twice), -3/25}`. Each has a negative eigenvalue, proving that each channel can produce entangled outputs from a product input.

**Even the labeled accessible outputs disagree on entanglement.** For the identically labeled product preparations `(+x,+z)`, use radii `a_A=1/2`, `a_B=3/4`. The output partial-transpose eigenvalues are

- A: `43/320`, `437/1600` (twice), `511/1600`, all nonnegative, hence separable for two qubits.
- B: `-13/1280`, `1933/6400` (twice), `2599/6400`, hence entangled.

Yet the permitted local preparations and local effects do not distinguish them. To prove the complete equality, observe that the corresponding product states transform by G and effects transform by the dual inverse. Every named gate, including the joint Phi_B, transforms by the same similarity. Thus all G and G^{-1} terms cancel telescopically in each circuit probability, including individual adaptive branches. Exact arithmetic additionally checks 36 product source pairs against 36 product effect pairs, all 1,296 single-joint-gate tests, plus all 36 pairs for the uncalibrated SWAP model.

This does **not** mean entanglement is an illusion or that the two full physically calibrated theories are equivalent. It means the restricted gate-set data do not identify the abstract purity and output entanglement assigned to those labels. Independent joint calibration changes the observation contract. QED.

## 5. Proposition: arbitrarily small nonzero noise can retain some ambiguity

Fix any `0<p<2/3` and choose preparation and effect contrasts strictly inside their positivity intervals. At `lambda=1`, `Phi_p=(1-p)Ad_CNOT+pD` has strictly positive Choi matrix, since `p>0`, and produces an entangled output from `|+0>` because `1-p>1/3`. The Choi matrix and the output partial transpose depend continuously on lambda. Therefore for all lambda sufficiently close to but different from one, the transformed Phi'_p remains CPTP and entangling. The source and effect gate sets also remain physical by continuity. The models remain observationally equivalent under their corresponding uncalibrated gates, yet give different preparation purities.

Thus there is **no universal positive lower noise threshold** below which every nontrivial similarity is automatically ruled out by merely requiring all available gates to be entangling CPTP channels. The allowed gauge differences shrink as noise tends to zero. This is a conditional finite-dimensional continuity argument, not a universal theorem about all noise models.
