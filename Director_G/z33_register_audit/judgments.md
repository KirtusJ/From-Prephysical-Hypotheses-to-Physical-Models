# Judgments for the 33 flagged Z33 entries

Kirtus Justus, research direction. OpenAI Codex, source audit and computational checks. 15 November 2026. Each entry preserves the issued status and gives the audit judgment separately. Page numbers are one-based in the assembled PDF unless a component page is specified. [Issued register](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PROGRAM/registers/THEOREM_REGISTRY.csv)

## B1-05-03 · Corollary 3 electrical resistance and full reconstruction

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within scope**.

For normalized preparations with equal diagonals supported on i,j and nonzero zero-mode contrast, Theorem 2 gives Kij. Basis states give Kii,Kjj. Unit current from i to j has potential K(e_i−e_j) up to a constant, so its drop is Kii+Kjj−2Kij. For every labeled pair this recovers K and hence K⁺=L. The setting count is $n+2\binom n2=n^2$. The all-pairs nonzero contrast and unconditional scale normalization are essential.

Scale POVM §3, Corollary 3 (and Theorem 2 on the same page). [Assembled B1, p. 39](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes.pdf#page=39)

## B1-05-05 · Corollary 5

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within scope**.

Each windowed unconditional moment incurs absolute error at most B_{a,b}+h/2 by integrating the missing spectral tails and midpoint binning. Apply the triangle inequality to the two moment errors then divide by n|d|, d fixed and nonzero. The printed upper bound 2(B_{a,b}+h/2)/(n|d|) follows. For unbinned truncation the two errors have the same sign and the factor 2 is conservative.

Scale POVM §4, Corollary 5 and Lemma 4 on pp. 39–40, with Theorem 2 on p. 39. [Assembled B1, p. 40](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes.pdf#page=40)

## B1-13-02 · Theorem 2 explicit conditional counterexample

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified within scope**.

With λ=3/2 and p=63/100 the transformed map is trace preserving and its independently reconstructed unnormalized Choi matrix has minimum eigenvalue 1/300. Using |+0⟩, the two outputs' partial-transpose minimum eigenvalues are −11/400 and −3/25, so each gate can entangle. The accessible radii (1/2,3/4) and their reciprocally transformed effects are physical; the respective source purities are 5/8 and 25/32. Similarity cancels on every allowed transcript branch and hence after arbitrary feedback. The restricted gates and independently assayed calibrated operations are different observation classes.

Unitary scaling rigidity §4, Theorem 2; Pauli covariances p. 61 and explicit labeled one-qubit preparation/effect radii p. 14. [Assembled B1, p. 62](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes.pdf#page=62)

## B1-20-02 · Corollary sharp phase-contrast ceiling

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within scope**.

For fixed s,h optimize min{sh b,s(1−h)(1−s−b)} on 0≤b≤1−s. The lines meet at b=(1−s)(1−h); endpoints h=0,1 give zero. Choose real c=√[s(1−s)h(1−h)] and use the pure state and rank-one effect from the preceding achievability construction. Thus |q₀−qπ|=4|Re c| can reach the ceiling. With s=131/320,h=99/100 it is 9√30261/8000≈0.195701502613.

Four-phase response §2, corollary after equations F1–F3; population parameter s given on p. 80. [Assembled B1, p. 81](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes/B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes.pdf#page=81)

## C1-01-02 · Theorem 2 three-momentum necessary relation

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within scope**.

At mass one the band energies are √3,√7,3 and the positive deformation factors are 1+ε/2, 1−ε/2, 1−ε. Common clock scale cancels. Direct elimination gives √21 R12+2√7 R32=9 and ∂ε R12=√(3/7)/(1−ε/2)²>0 for |ε|<1. The relation alone does not identify family membership; for example an admissibly small factor 1+δ(c−1/2)(c+1/2)(c+1) is identically one at all three nodes and can alter the dispersion elsewhere.

§2, Theorem 2, three-momentum necessary relation; model on p. 2. [Assembled C1, p. 3](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/C1_Projector_Equivalent_Wilson_Dirac_Hamiltonians_and_Dynamical_Identific/C1_Projector_Equivalent_Wilson_Dirac_Hamiltonians_and_Dynamical_Identific.pdf#page=3)

## C2-01-02 · Theorem 2 three-momentum identification, conditional

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified within scope**.

Each complete strictly positive histogram recovers η,D and the orbital projection. At π the directional information gives cos θ; in (−π/2,π/2) only θ and −θ remain. For a=m+1≥1 define φ_a(k)=atan(sin k/(a−cos k)). Between π/2 and k* the two angles strictly decrease. For the equal-tilt alias, a'≠a would require the sum of the two angles to equal 2θ at each node, which contradicts decrease. Opposite-tilt aliasing requires φ_a−φ_a'=2θ there: its tangent magnitude |a'−a|sin k/[aa'+1−(a+a')cos k] strictly decreases and the reflected alternative would require φ_a+φ_a'=0. Two distinct cosine nodes recover λ and λε after dividing by E_a. For θ≠0 the π row and a nonzero interior row separate (a,θ); for θ=0 the two interior derivative rows have determinant sinφ₁sinφ₂(p₂−p₁)>0 since sin k*<1 and E_a(k*)²>a²+1. This holds one-sided at a=1 and at every finite admissible tuple.

§2, Theorem 2; proof pp. 3–4. [Assembled C2, p. 3](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/C2_Operational_Identification_and_Calibration_in_Two_Mode_Quasifree_Syste/C2_Operational_Identification_and_Calibration_in_Two_Mode_Quasifree_Syste.pdf#page=3)

## C2-01-03 · Theorem 3 calibrated directional rank recovery

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within scope**.

With four distinct known cosines the Vandermonde map gives the cubic coefficients. Differentiating the single calibrated interior direction s=(a−cos k)/E gives ∂as=sin²k/E³>0. The two coefficients Q0,Q1 have 2×2 Jacobian in (λ,ε) equal to 4λ³(a²+1)². Their augmentation with s gives a positive maximal minor at a=1 and at the positive-mass collision 1+ε(a+a⁻¹)/2=0. η is obtained from the vacuum/double ratio. Independently expanding all four original 3×3 minors gives the common printed factor times (1,ε,ε²,ε³).

§3, Theorem 3 and Explicit Jacobian minors on p. 4. [Assembled C2, p. 4](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/C2_Operational_Identification_and_Calibration_in_Two_Mode_Quasifree_Syste/C2_Operational_Identification_and_Calibration_in_Two_Mode_Quasifree_Syste.pdf#page=4)

## C6-01-06 · Theorem 2.2 Conditional confidence for the neutral response

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified within scope**.

Given the pre-design information, conditionally independent complete outcomes lie in [−1,1], so the centered sample mean has two-sided tail ≤2exp(−nη²/2). The specified η_n makes this α. On the pre-design calibration event F the conditional mean discrepancy is at most b. Intersect the events and use the union bound to obtain true scale in the inverted response set with probability at least 1−α−α_cal, even if those events depend. The sinc monotonicity/time restriction is relevant to identifiability and interval width, not needed for this coverage argument alone.

§2, Theorem 2.2, statement and proof pp. 7–8, conditions after the proof on p. 8. [Assembled C6, p. 7](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/C6_Local_Number_Conserving_Response_and_Inference/C6_Local_Number_Conserving_Response_and_Inference.pdf#page=7)

## D1-01-10 · Corollary uniform covariance distance

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Finite compression implication verified**.

For interval projection χ and T=P_m−P_0, χT²χ−(χTχ)²=χT(1−χ)Tχ≥0. The full-line Pauli identity gives χT²χ=G_N, so taking the trace gives the squared Hilbert–Schmidt bound μ/π on the stated Wilson mass bound. No commutation of compression and squaring is assumed.

D1 p.7, immediately after the imported majorant theorem; D8 part 2, full-line projector identity and its compression. [Assembled D1, p. 7](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=7)

## D1-01-12 · Proposition Conditional quantitative modular rate

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Conditional proof located; d4 supplies its spectral envelopes**.

Split at h≈√x with x=log N and h=2+|λ|. The named inside logarithmic estimate and the measure tail give O(x^(−1/103)) by (17); the outer envelope costs O(log x/√x), and Cauchy–Schwarz controls the transverse term. In this edition D4 bounds the same E, so its pointwise 14/N inside and 7 globally suffice for the named hypotheses. The exact concentration connection underlying D4 remains a dependency.

D1 p.8, (17)–(18); D4 pp.2–4, Theorem 3 and Corollary 4. [Assembled D1, p. 8](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=8)

## D1-01-20 · Corollary transverse modular reduction

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified trace estimate on stated inputs**.

In the common reference basis sum |e_j d_j|≤2 Σ |e_j|√(q_j b_j(1−b_j)). Cauchy–Schwarz gives 2√(Tr G_N)√Tr(W_N E_N²), hence O_μ(√log N) at fixed mass. This only bounds the transverse trace.

D1 pp.7, 11–12, majorant and pairing theorem, occupation-weighted theorem, and following corollary. [Assembled D1, p. 11](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=11)

## D1-01-21 · Theorem uniform interior modular expansion and weighted bounds

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Identified as a restatement with explicit upstream proof**.

D1 points to D2 for both the fixed-interior expansion and global linear bounds. The normalization and sign of E match. D2 §5 explicitly identifies the period coefficients and closes (4); Theorem 7 compares the Riccati solutions to give the two global bounds. Full acceptance shares the exact spectral input and domain dependencies of D2.

D1 p.12; D2 Theorem 1, pp.2–7, eqs. (4), (33), (38); D2 Theorem 7, p.8. [Assembled D1, p. 12](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=12)

## D1-01-24 · Theorem Conditional fixed-positive-mass Wilson relative-entropy expansion

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified conditional assembly**.

Subtract the two-bond and nonlinear constants in (22), with the entropy residual entering with a minus sign. At fixed μ the three faster remainders are dominated by (log L)^(−1/103). This is the older sufficient route. D3 uses different estimates to obtain the faster rate (log L)^(−1). The moving-window and global D1 assumptions are implied by D4 Theorem 3 on its own inputs.

D1 p.13, eqs. (21)–(22), corresponding residual estimates on pp.6–11. [Assembled D1, p. 13](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States/D1_Relative_Entropy_of_Finite_Interval_Wilson_Dirac_Quasifree_States.pdf#page=13)

## D2-01-01 · Theorem 1 Uniform interior expansion

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Deferred analytic proof located; upstream conditions identified**.

The integrating factor controls the L¹ Riccati residual on a fixed interior; even coefficient truncation and the contour calculation in Proposition 5 identify the actual finite spectral expansion. The manuscript explicitly concludes (4) after (38). This audit did not independently reconstruct every Friedrichs domain, spectral deletion or every coefficient of the appendix's rational certificate.

D2 pp.2–7, §§1–5, eqs. (4), (7)–(9), (27)–(38); explicit K=3 constant in Appendix A, pp.11–12. [Assembled D2, p. 2](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D2_Uniform_Bulk_Modular_Asymptotics_and_the_Leading_Wilson_Entropy_Law/D2_Uniform_Bulk_Modular_Asymptotics_and_the_Leading_Wilson_Entropy_Law.pdf#page=2)

## D3-01-01 · Theorem 1 Finite relative-entropy part

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Assembly verified on its identified analytic inputs**.

Insert (29), (27), (15) and (30) in the four-term identity (28). The total constant is μ²[13/36−π/12−(log μ)/6]−S(μ). The slowest of the four remainder estimates is O_μ(1/log L). D4 is unnecessary for this derivation. The boundary B9 and the exact spectral and finite-path inputs still carry mathematical content beyond locating this proof.

D3 pp.2 and 8, Theorem 1 and §7 after (30). D3 §8 distinguishes D4 refinements. [Assembled D3, p. 2](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy.pdf#page=2)

## D5-01-01 · Proposition 1 Conditional uniform additive consequence

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified conditional bounded-mass assembly**.

For bounded μ the four bounds have a common sufficiently large L and common truncation K. Positive powers of μ absorb log(1/μ) in the stated error bounds; μ²log μ extends continuously to 0. A single O_M(1/log L) remainder then follows. A relative error bound along vanishing scaled masses requires further control.

D5 pp.1–4, Proposition 1 and its four contributions. D4 Corollary 4 and (8); D8 part 1 (B9). [Assembled D5, p. 1](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D5_Conditional_Uniform_Additive_Limit_of_Wilson_Dirac_Relative_Entropy_on/D5_Conditional_Uniform_Additive_Limit_of_Wilson_Dirac_Relative_Entropy_on.pdf#page=1)

## D6-05-11 · Theorem 1.3

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **External citation misindexed as local theorem**.

The words “Theorem 1.3” form the final line of the reference entry, naming the external Toeplitz-eigenvalue theorem. There is no locally stated result 1.3 or deferred local proof. Remove it from the local theorem count and retain the external citation.

D6 p.38, part 5 p.9, bibliography [5]; see D6 p.37, part 5 p.8, historical comparison. Original source, Deift–Its–Krasovsky, arXiv:1110.4089v2 p.5, Theorem 1.3. [Assembled D6, p. 38](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D6_Concentration_Spectrum_of_the_Half_Filled_Sine_Kernel_Periods_Tails_an/D6_Concentration_Spectrum_of_the_Half_Filled_Sine_Kernel_Periods_Tails_an.pdf#page=38) · [Deift, Its and Krasovsky, p. 5](https://arxiv.org/pdf/1110.4089v2#page=5)

## D7-03-04 · Corollary 4 sufficient sublinear spectral envelope

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified conditional implication; issued d4 supplies the envelope on its analytic inputs**.

D4 and D7 specify identical even N, half-filled B_N, Jacobi offdiagonal j(N−j)/N, K_N=log(I−B_N)−log B_N and E_N=K_N+Nη(J_N/N), with the same hypergeometric η. Thus D4’s operator norm bound ||E_N||≤7 implies |e_j|≤7≤7(1+|λ_j|^α) for every 0<α<1, uniformly. The D7 sentence calling (11) unresolved is out of date if D4 Theorem 3 and its upstream exact connection are accepted. Its separate uniform-sublinearity condition (13) also follows, with tail sup |e|/|λ|≤7/R. Independently, the local Corollary 4 implication uses Σq_j|e_j|, the mass bound, the fractional moment (10) and the pre-existing reduction (8). A weighted trace estimate alone would not establish the pointwise envelope; D4 supplies an operator norm.

D7 pp.13,15–16, part 3, equations (8)–(12). Matching hypothesis in D4 p.2 §1 definitions, p.3 Theorem 3 (D4-01-03). D1 pp.7–8, equation (16) and moving-window assumption. [Assembled D7, p. 16](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter.pdf#page=16)

## D7-04-01 · Theorem 1 sharp second moment

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

The projection cross-block factorization squares to the moment. Reflection supplies the factor two. For even distances n≤N, summing the uncorrected numerator squares yields n(n²−1)/3; the finite correction and n>N tail both sum to O(1). The even sum of n/(n²−1) is (1/2)log N+O(1), giving 1/(3π²).

D7 pp.18–19, part 4 pp.1–2, §§2–3, (1)–(2); explicit conclusion at foot of p.19. [Assembled D7, p. 18](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter.pdf#page=18)

## D7-07-03 · Corollary 3

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

Insert I_N ≤ F_N from the elementary split-integral bound (2) into Tr√W_N ≤ (2/π)I_N. Multiply by the optimal scalar C_log via functional calculus (1) to get the second inequality. These are upper bounds, and give no matching asymptotic coefficient for Tr√W.

D7 pp.35–36, part 7 pp.1–2, imported crossing estimate and (1)–(4); earlier crossing derivation D7 part 3 p.14 §2. [Assembled D7, p. 36](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter.pdf#page=36)

## D7-07-04 · Corollary 4 fully explicit error

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

Apply T_K ≤ 2 C_log F_N/π to U_N=2√(M_N T_K). For fixed μ>0, M_N→μ/π follows by expanding arccos(r)/√(1−r²) at r=0, while F_N=(1/2)log N+O(1). This gives coefficient 2√(C_log μ)/π for the stated upper envelope. No matching lower bound on the trace error follows.

D7 p.37, part 7 p.3, §4 (5)–(7); p.35 mass identity; D8 part 10 Theorem 2 pp.45–46. [Assembled D7, p. 37](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter.pdf#page=37)

## D7-07-05 · Corollary 5

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

The triangle inequality for √W E gives the square root of the K moment plus Aη times the square root of the Jacobi moment. Inserting M₂ ≤ 32(H_N+1)/π² supplies exactly 4√2 Aη/π. The transverse trace bound uses Cauchy–Schwarz with the positive majorant mass.

D7 pp.37–38, part 7 pp.3–4, §5 immediately preceding (9) and following (10). [Assembled D7, p. 37](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter/D7_Reference_Modular_and_Jacobi_Estimates_for_a_Half_Filled_Fermion_Inter.pdf#page=37)

## D8-03-04 · Corollary 4 unconditional fixed-μ two-bond finite part

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified for the fixed-μ two-bond observable; register flag misleading**.

The proof starts on the same page. With r=μ/(2L+μ), DLMF complementary expansions and the exact odd/even-bond trace give the logarithmic coefficient μ²/6 and constant μ²[(1/6)log(8/μ)−1/4] with Oμ(log L/L). This requires the named model, fixed μ>0 and standard elliptic identities. It is unconditional within that model and addresses only the two-bond part of the entropy decomposition.

D8 pp.19–20, part 3 pp.3–4, Corollary 4 and immediately following Proof; Theorem 3 pp.18–19. [Assembled D8, p. 19](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=19)

## D8-05-02 · Corollary 2 discrete concavity for a fixed operator

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

First and second differences of min(L,|d|) select respectively |d|≥L+1 and minus |d|=L+1 in the nonnegative Fourier sum. Both signs hold for the same bounded translation-invariant self-adjoint T at all lengths.

D8 pp.23–24, part 5 pp.1–2, Theorem 1 (1), Corollary 2 (2)–(3), explanatory sentence directly below. [Assembled D8, p. 24](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=24)

## D8-05-03 · Proposition 3 derivative bounds

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

Differentiate Λ=π⁻²∫min(t,μ)Φ(t)dt and the positive remainder (6). The strict comparisons follow from 0<Φ(t)=t⁻²−W(t)<t⁻², since 0<K0<K1<1/t. This confirms both signs of the second derivatives and the 1/(π²μ) derivative upper bound.

D8 p.25, part 5 p.3, §3 (5)–(7), derivative computations and end-of-proof square immediately following the statement. [Assembled D8, p. 25](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=25)

## D8-07-01 · Theorem 1 Covariance scaling and relative-entropy bound

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

The rescaled multiplier converges in L² at fixed μ using min(1,μ/|t|). Its weighted squared norm Oμ(L) yields Oμ(1/L) squared step-sampling error after pair counting. The Bessel transform gives the HS norm limit. The scalar f″≥4 extends by divided differences to the trace Hessian, giving D≥2||A−B||²_HS. Taking the liminf yields (3); K0>0 makes the benchmark strict.

D8 pp.30–33, part 7 pp.1–4, §2 Lemmas 2–4, “Proof of the limit (2)” p.32, §3 Proposition 5 and “Proof of (3)” p.33. [Assembled D8, p. 30](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=30)

## D8-07-06 · Corollary 6 Monotonicity and convexity

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

The integrand G=K0²+(K1−1/t)² is positive and locally integrable at zero, bounded there by O(1+|log t|²), and continuous on t>0. Twice differentiating the triangular integral on μ>0 gives strict H′>0 and H″=G(μ)/π²>0.

D8 p.33, part 7 p.4, §4 (8)–(9), with the endpoint estimates immediately above Corollary 6. [Assembled D8, p. 33](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=33)

## D8-08-01 · Theorem 1 exact signed remainder and global quantitative bound

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

The Bessel first-moment primitive and Plancherel normalization ∫G=π fix the integration constants. For t>0, K0<K1<1/t yields 0<W<2K1/t. Integrating E″=W/π² twice with the infinity boundary condition gives E=A−H>0. K1(t)≤exp(μ−t)K1(μ) gives the strict global upper bound. The large-argument form and ∫s exp(−s)ds=1 give its stated leading equivalent.

D8 pp.35–37, part 8 pp.1–3, §1 (1)–(3), §2 Proof, (4)–(10). [Assembled D8, p. 35](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=35)

## D8-09-01 · Theorem 1

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified within stated scope**.

The Poisson/Laplace derivation gives the cross-block kernel. Keeping the finite-length numerator bounds the nuclear weight by C√(L/t) for 0<t≤1. The four regions each contribute O(√(Lκ)), including the square-root integrable singularity at t=κ. κ=log(1+μ/L)≤μ/L; Mirsky and the 2-Lipschitz scalar entropy of singular values give |ΔS|≤2C√μ. The theorem assumes 0<κ≤1/4 and makes no fixed-mass entropy convergence claim.

D8 pp.39–41, part 9 pp.1–3, §§2–5, (3)–(9) and entropy-continuity paragraph; p.42 §6 is a separate optimality observation. [Assembled D8, p. 39](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=39)

## D8-11-03 · Corollary 3

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Verified conditional reduction**.

Insert (6) into the imported four-branch estimate (10), using (7) for the cross-boundary trace. Commutation of B,J,E diagonalizes their part of the bulk trace; G need not commute because only the diagonal entries of G are traced. This proves the equivalence of the two o(log N) conditions, but does not prove either condition. The absolute weighted condition (14) is sufficient.

D8 pp.47–50, part 11 pp.1–4, §§1–4, especially p.49 (10)–(14) following Theorems 1–2 on p.48. [Assembled D8, p. 49](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=49)

## F2-01-06 · Proposition 6

Issued status `PROOF_NOT_ADJACENT`. Audit judgment **Contradicted as a local registry attribution**.

The registered page contains a bibliography entry identifying Proposition 6 of the companion Abstract Channels and Gaussian Capacity. It is not a local F2 Proposition 6. F2 p. 6 explicitly labels the example as [4, Proposition 6]. F1 p. 7 actually contains the named claim 'Equal capacity without recovery' with a proof. F2's own Theorem 5.2 extends the example, with error lower bound 1/4 from the convex relation and an attaining common reverse kernel. F2 §6 on p. 7 develops a separate rare-input formula in prose. Neither justifies a local numbered F2 Proposition 6.

§7 and references, especially [4] on p. 8; F2 §5 p. 6; actual companion F1 p. 7, Proposition 6 (ID F1-01-06). [Assembled F2, p. 8](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/F2_Stochastic_Recovery_from_Information_Loss_and_Equality_of_Channel_Capa/F2_Stochastic_Recovery_from_Information_Loss_and_Equality_of_Channel_Capa.pdf#page=8) · [F1, p. 7](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/F1_Abstract_Channels_and_Gaussian_Capacity/F1_Abstract_Channels_and_Gaussian_Capacity.pdf#page=7)

## G1-01-05 · Proposition 1.5 Deterministic and conditional aggregation

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified within scope**.

For the two specified input densities the trace distance is 1/4; for MD±M* it is 1/2. Contractivity and two error terms force maximum trace-distance error at least 1/8. The CPTP computational-basis measure-and-group channel attains 1/8 on each. (M/√2)† composed with M/√2 is the projector onto the span of the two group-sum vectors (equivalently (M/√2)†(M/√2)≤I). The operation has probability 1/2 on each named state and yields the exact normalized target when accepted. An arbitrary physical representation is not presumed.

§1, Positive event kernels and their normalization, Proposition 1.5 and adjacent proof p. 6. [Assembled G1, p. 6](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/G1_Relational_Structures_and_the_Limits_of_Observation/G1_Relational_Structures_and_the_Limits_of_Observation.pdf#page=6)

## G3-01-03 · Proposition 2.3 Reduced sign law and conditional mixedness

Issued status `CONDITIONAL_ON_NAMED_INPUTS`. Audit judgment **Verified within scope**.

With the given square-root weighted joint preparation and orthogonal configuration labels, partial trace gives a qubit with off-diagonal C/2, C=Z(ze^{2iθ})/Z(z). The independent-copy SWAP rule gives (3+|C|²)/4. Equal polynomials imply equal sign-register statistics on all independent copies at common parameters. On a triangle, condition on either fully specified equal retained pair: the two possible removed signs have counts 1,3 and weights z,z³. For z>0 and e^{4iθ}≠1 their conditional phase states differ so the mixture is not pure; at z=1/2,θ=π/8 exact conditional visibility squared is 17/25, purity 21/25 and complete-triangle SWAP acceptance 163/169.

§2, A stipulated quantum observation of the action count, Proposition 2.3 and adjacent proof p. 4. [Assembled G3, p. 4](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/G3_Finite_Signed_Graphs_and_Binary_Extension_Constraints/G3_Finite_Signed_Graphs_and_Binary_Extension_Constraints.pdf#page=4)
