# FOUNDATIONS OF R
## D3 Chiral-Regulator Computational Audit and Interim Findings

**Proposed v1.5 technical memorandum**  
**Authors:** [Kirtus Justus, Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google)]
**Date:** 18 October 2026  
**Status:** Exploratory finite-model computation. Not a proof of D3, a continuum theorem, or a derivation of R's fixed-capacity premise.

## Abstract

The finite chiral-edge probe proposed as the next state-restricted inclusion test has now been run with a factorized, singular-value-based solver through scale parameter \(n=6\). The solver avoids forming the regularized covariance in site space and avoids normal equations for the state-weighted least-squares problem. This resolves the previous Gram-matrix failure as a computational procedure, but does not resolve the sensitivity of the modular flow to small covariance eigenvalues.

Three findings are supported within the specified finite model and tested observable class. First, an edge-matched packet exhibits a pronounced directional asymmetry: at modular parameter \(t=\pm0.2\), the maximum of the annihilator and creator state-restricted linear defects is much smaller for the candidate half-sided sign \(t<0\). Second, reversing the Hamiltonian's chirality swaps the favored time sign to close numerical agreement for \(n=1\) through \(n=4\). Third, a wrong-edge-spinor control has essentially zero estimated overlap with the selected edge branch and does not show the same strong time-sign asymmetry.

The scaling claim is not established. At a boundary margin scaled as \(2n\), the candidate-side defect decreases from 0.00935 to 0.00234 for \(n=1\) through \(6\) with spectral floor \(10^{-14}\). At floors \(10^{-12}\) and \(10^{-10}\), the same sequence turns upward and ends at 0.00877 and 0.02435, respectively. The number of clipped covariance eigenvalues also grows with scale. In double precision, the raw covariance develops eigenvalues slightly outside \([0,1]\), invalidating an unregularized logarithmic modular generator at larger sizes. The regularization changes the state and can substantially change the defect despite a small Frobenius-norm covariance perturbation.

**Interim conclusion:** the directionality is a robust qualitative signal in this chiral-edge model, but the regulator-stable limiting behavior needed to support route A has not been shown. These runs do not compute the full algebraic half-sided modular inclusion defect and do not instantiate R's fixed total-capacity premise.

## 1. Question and scope

The immediate question is narrow: does the finite-regulator proposal show an increasingly accurate, state-restricted half-sided action for a declared family of edge-localized observables, and is that indication stable under numerical and geometric controls?

The calculation does **not** test whether R derives quantum theory, local tomography, the modular inclusion, spacetime geometry, or the cosmological capacity. It tests one candidate link in the proposed D3 structure. A successful one-particle result would remain necessary evidence for that link, not sufficient evidence for the full framework.

The previous trace-preserving conditional-expectation residual is not used as a continuum diagnostic here. For a nontrivial half-sided modular inclusion under standard hypotheses, a conditional expectation from the larger algebra onto the smaller algebra generally does not exist [1]. The present test instead defines a direct state-norm distance to a declared subalgebra of linear CAR fields. This avoids relying on an expectation, but is narrower than an algebra-level inclusion test.

## 2. Finite model and tested state

The model is a finite Chern-insulator strip with open transverse direction and an antiperiodic finite periodic direction. The canonical Hamiltonian used in the computation is

\[
H(k_x,k_y)=-\sin k_x\,\sigma_x+\sin k_y\,\sigma_y
 +(m+\cos k_x+\cos k_y)\,\sigma_z,
\qquad m=-1.
\]

This sign convention is deliberate. The v1.4 memorandum printed the opposite sign for the \(\sin k_x\,\sigma_x\) term. The calculation actually run uses the Hamiltonian above, with a top-edge dispersion \(E(k)=-\sin k\) and normal profile proportional to \(\lambda(k)^y\), where \(\lambda(k)=1-\cos k\) in the selected mass regime. The reversed-chirality control replaces \(k_x\) by \(-k_x\), reversing the edge propagation direction.

For scale parameter \(n\), the run uses \(L_x=128n\), \(L_y=10\), an interval of \(\ell=40n\) columns, and two transverse rows in the reduced region. The one-particle covariance for that region has dimension \(160n\). The packet has longitudinal length \(q=24n\), carrier momentum \(k_0=0.25/n\), and nominal offset \(d=6n\). The canonical spinor is \((1,1)/\sqrt2\). Two smooth envelopes are tested: \(\sin^4\) and a smooth bump. The covariance is obtained by restricting the finite-strip negative-energy projector to the selected region.

The global lattice system is finite at every fixed \(n\), but the total number of fermion modes grows with \(n\). There are \(2L_xL_y=2560n\) modes, so the Fock-space dimension is \(2^{2560n}\) and \(\ln\dim\mathcal H=2560n\ln2\). This is a sequence of increasing finite systems, not a calculation at one fixed total capacity \(N=\ln\dim\mathcal H\) as used in R's broader proposal.

## 3. Diagnostic definition

Let the unregularized regional covariance be \(C=V\operatorname{diag}(\nu_j)V^*\). For each explicit spectral floor \(\varepsilon\), set

\[
\nu_{j,\varepsilon}=\min(1-\varepsilon,\max(\varepsilon,\nu_j)),
\qquad
h_\varepsilon=\operatorname{diag}\!\left(\log\frac{1-\nu_{j,\varepsilon}}{\nu_{j,\varepsilon}}\right).
\]

For initial packet \(f\), the computed one-particle modular flow is

\[
v_t=V e^{-it h_\varepsilon}V^*f.
\]

Let \(S\) be the support of the tested right-tail subalgebra \(\mathcal N\) inside the finite region \(\mathcal M\). The annihilator and creator diagnostics are

\[
D_W(t)=\frac{\displaystyle\inf_{\substack{\operatorname{supp}(g)\subset S\\\|g\|_2\le1}}
 \|W_\varepsilon^{1/2}(v_t-g)\|_2}
 {\|W_\varepsilon^{1/2}f\|_2},
\quad W_\varepsilon=C_\varepsilon\text{ or }I-C_\varepsilon,
\]

and the reported defect is \(D_\varepsilon(t)=\max(D_{C_\varepsilon}(t),D_{I-C_\varepsilon}(t))\). The minimization is solved in the covariance eigenbasis using a thin SVD of the weighted support matrix, with a Euclidean norm cap \(\|g\|_2\le1\). The factorized calculation does not form \(C_\varepsilon\) in site space and does not solve normal equations.

The interpretation must remain precise:

- The observable class consists of a single specified packet field and its annihilator/creator diagnostics, with linear CAR approximants supported in \(\mathcal N\).
- It is not a supremum over all observables in \(\mathcal N\), not a full von Neumann-algebra defect, and not an operator-norm approximation.
- \(\varepsilon\) is a state regularization, not only a solver tolerance. It clips covariance eigenvalues and changes the state and its modular generator.
- The script's declared candidate half-sided sign is \(t<0\). This sign is assessed empirically with the chirality-reversal control; it is not imposed as an output condition.

## 4. Results

### 4.1 Directional asymmetry and chirality reversal

With the packet initially at the tested right-tail boundary and \(\varepsilon=10^{-14}\), the canonical \(\sin^4\) packet gives

| \(n\) | \(D(-0.2)\) | \(D(+0.2)\) | \(D(+0.2)/D(-0.2)\) | Clipped modes |
|---:|---:|---:|---:|---:|
| 1 | 0.013587 | 0.235014 | 17.30 | 0 |
| 2 | 0.007248 | 0.239363 | 33.02 | 0 |
| 3 | 0.004556 | 0.246031 | 54.00 | 2 |
| 4 | 0.003486 | 0.253773 | 72.83 | 6 |
| 5 | 0.003562 | 0.262332 | 73.65 | 8 |
| 6 | 0.006823 | 0.273588 | 40.08 | 14 |

These are the maximum of the annihilator and creator normalized distances. The ratio demonstrates directionality in this particular state and observable family. It is not an HSMI theorem. The dense-time runs at \(n=1\) and \(n=4\) show the same shape: the defect approaches numerical zero at \(t=0\), remains comparatively small on the negative-time side, and rises steeply for positive times, especially beyond \(t=0.1\).

Under chirality reversal, the smaller defect moves to the opposite time sign. For \(n=1\), matching the canonical \(D(-0.2)\) to the reversed-chirality \(D(+0.2)\) differs by about \(5.1\times10^{-9}\); for \(n=2\), by \(4.0\times10^{-7}\); for \(n=3\), by \(7.9\times10^{-6}\); and for \(n=4\), by \(2.1\times10^{-5}\). Matching the opposite, larger defects gives differences from about \(2.3\times10^{-10}\) to \(6.2\times10^{-5}\) over the same range. The directional swap is clear, although numerical agreement deteriorates with scale.

The two smooth envelopes give close results under matched settings. This is evidence that the result is not unique to one envelope shape. It remains evidence for only those two packet families.

### 4.2 The apparent scaling law is not stable

For a packet flush with the tested subalgebra boundary, the floor changes the candidate-side defect materially:

| Floor \(\varepsilon\) | \(D(-0.2)\), \(n=1\ldots6\) | \(D(+0.2)\), \(n=1\ldots6\) | Clipped modes, \(n=1\ldots6\) |
|---:|---|---|---|
| \(10^{-14}\) | 0.01359, 0.00725, 0.00456, 0.00349, 0.00356, 0.00682 | 0.2350, 0.2394, 0.2460, 0.2538, 0.2623, 0.2736 | 0, 0, 2, 6, 8, 14 |
| \(10^{-12}\) | 0.01359, 0.00754, 0.00726, 0.01312, 0.02127, 0.02603 | 0.2350, 0.2401, 0.2531, 0.2693, 0.2835, 0.2894 | 0, 2, 10, 16, 24, 30 |
| \(10^{-10}\) | 0.01359, 0.01654, 0.02634, 0.03177, 0.03241, 0.03411 | 0.2350, 0.2510, 0.2672, 0.2692, 0.2715, 0.2726 | 0, 12, 22, 34, 46, 58 |

The \(10^{-14}\) run alone might suggest a decreasing candidate-side defect through \(n=4\), but the sequence turns up at \(n=5,6\). The larger floors turn upward earlier and more strongly. Therefore, no regulator-independent power law or vanishing-limit result is established by the present data.

### 4.3 The size-aware boundary test has the same limitation

To separate a fixed-site boundary offset from a continuum-scaled geometry, the subalgebra boundary was also moved left of the packet by \(b=2n\) lattice sites. For the \(\sin^4\) packet:

| Floor \(\varepsilon\) | \(D(-0.2)\), \(n=1\ldots6\) | \(D(+0.2)\), \(n=1\ldots6\) | Clipped modes, \(n=1\ldots6\) |
|---:|---|---|---|
| \(10^{-14}\) | 0.00935, 0.00533, 0.00381, 0.00297, 0.00237, 0.00234 | 0.10064, 0.07703, 0.06703, 0.06009, 0.05524, 0.05099 | 0, 0, 2, 6, 8, 14 |
| \(10^{-12}\) | 0.00935, 0.00530, 0.00357, 0.00345, 0.00547, 0.00877 | 0.10064, 0.07749, 0.06850, 0.06304, 0.06155, 0.06583 | 0, 2, 10, 16, 24, 30 |
| \(10^{-10}\) | 0.00935, 0.00700, 0.01126, 0.01737, 0.02235, 0.02435 | 0.10064, 0.08451, 0.08727, 0.09774, 0.10608, 0.10790 | 0, 12, 22, 34, 46, 58 |

At floor \(10^{-14}\), both defects decrease across this six-point sweep, while the opposite-sign defect remains much larger. At \(10^{-12}\), the candidate-side defect begins increasing after \(n=4\). At \(10^{-10}\), it increases strongly from \(n=2\) onward. This is direct evidence that the apparent convergence is not robust to the regularization currently required by double-precision covariance diagonalization.

### 4.4 The boundary itself is a controlled variable

For \(\varepsilon=10^{-14}\), moving the tested right-tail boundary one, two, or four lattice sites before the packet support reduces both defects. At \(n=1\), \(D(+0.2)\) falls from 0.2350 with no margin to 0.0233 with a four-site margin. At \(n=4\), it falls from 0.2538 to 0.1457. The negative-time value changes more modestly. This is consistent with a boundary-sensitive propagation test, but it also means the placement of the packet relative to the subalgebra must be specified as part of the scaling limit rather than treated as a harmless implementation detail.

A fixed number of lattice sites is not a fixed scaled margin as \(n\) changes. The additional \(b=n\) and \(b=2n\) sweeps address this geometry issue, but do not remove spectral-floor sensitivity.

### 4.5 Controls

**Chirality-reversed model.** Reversing \(k_x\) reverses the edge propagation direction and swaps the favored time sign. This is the strongest control supporting a chirality-linked interpretation in the finite model.

**Wrong-edge-spinor control.** With spinor \((1,-1)/\sqrt2\), the computed edge-branch fraction is approximately \(10^{-34}\) at \(n=1,2,3\). Its two-sign defects at \(t=\pm0.2\) are similar in size: 0.01722 versus 0.01352 at \(n=1\), 0.01623 versus 0.01492 at \(n=2\), and 0.01683 versus 0.01545 at \(n=3\). This control does not reproduce the strong directional asymmetry. A small defect by itself is therefore not enough; it must be interpreted alongside edge-mode diagnostics and the opposite-time control.

**Time zero.** With the packet supported in \(\mathcal N\), the computed defect at \(t=0\) is at roundoff scale, around \(10^{-15}\). The state-norm invariance error under regularized modular flow is below about \(2.3\times10^{-16}\). These are useful implementation checks, not independent physics results.

## 5. Numerical conditioning and interpretation

The factorized SVD method resolves the negative Gram eigenvalue failure of the previous normal-equation method. It does not make the input covariance spectrum exact. For the canonical state, the minimum eigenvalue of \(C\) falls from about \(1.19\times10^{-10}\) at \(n=1\), to \(3.80\times10^{-13}\) at \(n=2\), and \(7.79\times10^{-15}\) at \(n=3\). At \(n=4\), the computed maximum covariance eigenvalue exceeds one by about \(2.2\times10^{-15}\); at \(n=5,6\), raw eigenvalues also lie outside the physical interval \([0,1]\) due to floating-point error. The matrix logarithm used in the modular generator is ill-conditioned near zero and one.

The spectral floor defines a different regularized covariance and modular flow. For example, at \(n=4\), changing the floor from \(10^{-14}\) to \(10^{-12}\) changes the relative Frobenius covariance perturbation from approximately \(2.0\times10^{-14}\) to \(2.0\times10^{-13}\), while changing \(D(-0.2)\) from about 0.00349 to 0.01312. At floor \(10^{-10}\), the relative perturbation is about \(3.0\times10^{-11}\) and the same defect is about 0.03177. A small covariance perturbation in Frobenius norm is not enough to establish stability of the logarithmic modular flow.

A direct comparison with the prior site-space normal-equation implementation gives differences of at most about \(5.3\times10^{-13}\) at \(n=1\), rising to roughly \(6.5\times10^{-7}\) at \(n=2\), \(8.8\times10^{-6}\) at \(n=3\), and \(1.4\times10^{-5}\) at \(n=4\) over the checked dense-time samples and envelopes. The factorized result is the preferred implementation, but the cross-code difference is non-negligible compared with the smallest candidate-side defects. It further discourages extracting an asymptotic exponent from these runs.

## 6. Status of the claims

| Claim | Status after this computation | Reason |
|---|---|---|
| The finite model has a directional state-restricted response for the tested edge-matched packet | **Supported within the model** | Large \(D(+0.2)/D(-0.2)\); chirality reversal swaps the favored sign |
| The response is linked to edge chirality rather than only to time-sign labelling | **Supported qualitatively within the model** | Reversal control and wrong-spinor control |
| The candidate-side defect tends to zero with scale | **Unresolved; not established** | Trend depends materially on the spectral floor, clipped mode count and boundary placement |
| The one-particle diagnostic establishes a half-sided modular inclusion of full algebras | **Not tested** | The calculation uses a single packet and linear CAR approximants, not a uniform algebra-level test |
| The calculation realizes R at fixed total capacity \(N\) | **Not tested** | The lattice model's number of modes and \(\ln\dim\mathcal H\) grow with \(n\) |
| Route A is viable or refuted | **Open** | The state-restricted test needs regulator-stable convergence and a broader observable class |

The computation neither proves nor refutes D3. It supplies a model-specific directional signal and a concrete obstruction to treating the current numerical scaling as evidence for convergence.

## 7. Required next tests

1. **Resolve covariance precision.** Reconstruct the finite covariance with higher precision, or use a regulator with a controlled analytic spectral error. Increasing the precision of the least-squares solver alone is insufficient if the eigenvalues entering the logarithm are already inaccurate.
2. **Separate state limit from arithmetic limit.** For each fixed geometry, document convergence as numerical precision increases while holding the regularized state definition fixed. Then vary the regularization parameter under a stated limiting procedure. Do not interpret a change of \(\varepsilon\) as a mere solver tolerance.
3. **Retain the scale-aware geometry.** Run margins \(b=0,n,2n\), with the boundary class fixed in advance. Record the packet support and algebra support independently.
4. **Expand the observable class.** Test multiple low-energy momenta, packets with boundary support and interior margins, both field types, and predeclared finite linear combinations. The class should be fixed before inspecting results, and the reported quantity should include a supremum or a justified approximation to one over that class.
5. **Use independent regulators.** A second regulator should have separately characterized chirality, locality, and edge-state content. Any regulator-induced chiral or bulk-edge error must be kept distinct from the inclusion defect.
6. **Keep the R bridge explicit.** State how the growing finite lattice relates to the proposed fixed total-state capacity and identify what further assumption, theorem, or construction makes that relation valid.

A reasonable acceptance criterion for the computational route is not a single small defect. It is stability of the declared state-restricted defect under increased arithmetic precision, independently characterized regularizers, scale-aware boundary placements, and the predeclared observable class, together with a consistent chirality control. Even passing that criterion would support only the tested route, not the whole R framework.

## 8. Reproducibility and sources

The associated reproducibility bundle contains the tested scripts, model source, raw CSV outputs, JSON metadata, derived tables, and figures. The principal solver is `r_d3_chiral_edge_v6_factorized.py`; the boundary tests are implemented in `r_d3_chiral_edge_v7_boundary_sensitivity.py` and `r_d3_chiral_edge_v7_scaled_buffer_chunk.py`. The computations use Python, NumPy, and SciPy. Raw results preserve the floor, geometry, covariance spectrum diagnostics, denominator checks, SVD conditioning, and edge-fraction estimate per run.

References:

[1] “Modular Structure and Inclusions of Twisted Araki-Woods Algebras,” *Communications in Mathematical Physics* (2023), §4.1, DOI: [10.1007/s00220-023-04773-y](https://link.springer.com/article/10.1007/s00220-023-04773-y). The cited section states the half-sided modular inclusion conditions and that nontrivial inclusions of the stated kind do not admit a conditional expectation from the larger algebra to the smaller one.

[2] H. Araki and L. Zsidó, “Extension of the structure theorem of Borchers and its application to half-sided modular inclusions,” *Reviews in Mathematical Physics* 17 (2005), 491–543, [arXiv:math/0412061](https://arxiv.org/abs/math/0412061). Used as mathematical context for the structural consequences of half-sided modular inclusions, not as a claim that the finite computation satisfies their hypotheses.

[3] “Relative positions of half-sided modular inclusions,” *Letters in Mathematical Physics* (2025), DOI: [10.1007/s11005-025-02008-w](https://link.springer.com/article/10.1007/s11005-025-02008-w). Used for context on standard subspaces and the relation between half-sided inclusions and positive translation generators.

These sources were checked for the specific statements used here; this memorandum is not a full literature review.

**Project acknowledgements:** Kirtus Justus; Claude (Anthropic); ChatGPT (OpenAI); DeepSeek. This acknowledgement records project participation and does not imply equal contribution or independent verification of every result.