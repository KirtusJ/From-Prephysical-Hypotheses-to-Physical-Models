# Can a single return port identify its phases and a fixed detector calibration?

Director G research note for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

Let u and v be the known independent even-clock multipliers of the five-site Hadamard walk. Write z,w for the two unknown unit phases at the reference time. A fresh launch at offset 2k has ideal port return probability

$$p_k=[1+zu^k+(zu^k)^{-1}+wv^k+(wv^k)^{-1}]^2/25.$$

Suppose the detector has one unknown offset d and one unknown contrast g throughout the experiment. The observable click probability is Yₖ = d + g pₖ. For an ordinary binary detector d and d+g are its click probabilities at ideal input zero and one. The result needs g ≠ 0 and even permits reversed contrast. Each setting must use the same reproducible reference phases, walk and detector.

**Twelve exact probabilities at offsets 0,2,…,22 uniquely determine z,w,g,d in this family.** A thirteenth reading at offset 24 gives a direct linear solve followed by explicit ratios. This counts distinct settings. Finite empirical estimates have their own uncertainties. [Exact even-clock spectrum and phase independence](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/a1eee36656ab413eac2cfa92c9d2bb62a1bea25e/Director_G/persistent_walk/Return_at_one_port.md)

## Direct recovery with thirteen settings

Expanding the square gives thirteen nodes λ₍ᵢ,ⱼ₎ = uⁱvʲ. The exponent vectors are (0,0) and both signs of (1,0), (0,1), (2,0), (0,2), (1,1), (1,−1). They are distinct by multiplicative independence. Using ordinary complex coefficients Cₑ, expand Yₖ = Σₑ Cₑ λₑᵏ. The zero coefficient is C₀ = d+g/5. At the six listed positive representatives the coefficients are (g/25)mₑ zⁱwʲ with multiplicities m = (2,2,1,1,2,2). The inverse representatives have the conjugate coefficients.

The thirteen rows k=0,…,12 form an invertible Vandermonde matrix. After solving for its coefficients, form

$$
z=2C_{2,0}/C_{1,0},\qquad
w=2C_{0,2}/C_{0,1},\qquad
g=25C_{1,0}^{\,2}/(4C_{2,0}),\qquad
d=C_0-g/5.
$$

## Why the first twelve already suffice

For rows k=0,…,11 the Vandermonde matrix has one null direction, with components $n_e=1/\prod_{f\ne e}(\lambda_e-\lambda_f)$. This follows by taking the degree-12 coefficient in the Lagrange interpolation formulas for powers of degree below 12. The nodes are closed under conjugation, so n at exponent −e equals the conjugate of n at e. The element n₀ is real and nonzero. Any difference of two admissible coefficient vectors in the null space is therefore a real multiple of n.

Assume a collision has a nonzero such multiple. Absorb that multiple and the factor of 25 into two real contrasts G,G′. For each nonconstant exponent e=(i,j), the squared magnitude of nₑ/mₑ equals

$$
  |G z^i w^j-G' {z'}^i {w'}^j|^2
   = K-V\cos(iA+jB),
$$

where K = G² + G′², V = 2GG′, A = arg(z/z′), B = arg(w/w′). Denote the six squared magnitudes, in the order listed above, by a,b,c,e,h,j, and put D = (h+j)/2. Multiplication of the complex conjugate nodes computes every squared magnitude exactly in the underlying number field.

The cosine addition and doubling identities imply, respectively,

$$
\begin{aligned}
K(K-V)&=K(a+b)-VD-ab,\\
(K-V)(2K+V)&=4Ka-Vc-2a^2
            =4Kb-Ve-2b^2.
\end{aligned}
$$

In particular K = [V(c−e) + 2(a²−b²)]/[4(a−b)]. The field map below proves that a−b is nonzero. Substituting this affine expression into the first equation and the first half of the second leaves two quadratic equations in V. A common root would force their Sylvester determinant, the resultant, to vanish.

Work modulo 1009 with √5↦244, u↦667, v↦387. The two distinct even-clock trace equations hold there, and both quadratic roots may be selected independently because the two quadratic extensions over the real quadratic field are independent. Equivalently the monic trace relations with 2 inverted present a free module over the localized base ring, which embeds in their compositum. All thirteen node differences and the denominator 4(a−b) map to units. Thus a nonzero modular result certifies a nonzero algebraic value in characteristic zero. The six squared magnitudes use nₑn₋ₑ/mₑ² under this map.

The residues of (a,b,c,e,h,j) are (814,853,1005,1006,739,284), D maps to 7, and K maps to 304V+329. The required polynomials reduce to

$$
 293V^2-322V-128,\qquad -120V^2+172V+256.
$$

Their resultant is 833 modulo 1009. Their characteristic-zero originals cannot share a complex root. An earlier calculation used $(K-V)(K+2V)$ on the left of the second identity. Direct expansion and two unequal-gain fixtures reject that expression. The corrected left side is $(K-V)(2K+V)$, and the certificate reported here uses it. This excludes a nonzero null-space difference. Equal coefficient vectors determine equal parameters by the direct ratios above. One constructive twelve-setting inversion is to parameterize the real affine line of coefficient solutions and retain the member that satisfies the unit-phase, gain and coefficient identities. For data in the model existence follows from preparation and uniqueness from the certificate. The thirteen-setting decoder avoids this nonlinear selection.

## A finite-precision bound for the direct decoder

Let M be the largest sum of absolute entries in the four inverse Vandermonde rows for (1,0), (0,1), (2,0), (0,2). If |g| ≥ g₀ > 0 and each of the thirteen observed frequencies differs from its true click probability by at most ε, each recovered coefficient differs by at most Mε. For Mε ≤ g₀/25, the estimated denominator in either phase ratio has magnitude at least g₀/25. The numerator of the difference from the true unit phase, before division, has magnitude at most 3Mε. Hence the two complex phase estimates each lie within 75Mε/g₀ of their true values. The estimates here are the ratios before optional normalization to the circle.

With n independent Bernoulli launches per setting, the two-sided Hoeffding bounds and a union bound give simultaneous coverage at least 1 − 26 exp(−2nε²). This is a sufficient sample bound conditional on the detector law and a contrast floor. It uses thirteen settings and a sensitivity coefficient determined entirely by the known clock. It provides no guarantee as the contrast tends to zero.

## What calibration still assumes

At g = 0 all phase pairs yield the constant record d. Without a positive lower bound on |g|, even different phases giving distinguishable ideal records can have arbitrarily close observed probabilities, since |Yₖ−Y′ₖ| ≤ |g| for any two phase choices at fixed d,g. A time-dependent offset with a free value for each setting can also absorb differences in the ideal traces. Consequently this theorem concerns a common affine detector with nonzero contrast. Clock-dependent loss or reset requires a separate record model. Independent evidence of constant response is needed for physical interpretation. If two independently established zero- and unit-return reference preparations are available, their click rates directly give d and d+g under the same detector law. Such reference preparations are additional physical inputs. The minimal number of settings for the unknown-calibration problem and the optimal sample budget at a given precision are open here.

Run `python3 -I -B check_unknown_detector.py` alongside this note. The standard-library checker verifies the 12 null moments, exact finite-field coefficients, nonzero resultant and the unreduced trigonometric identities using three exact rational-angle fixtures. Twelve direct-decoder fixtures independently interpolate all thirteen coefficients from a raw trace, check the twelve-row affine solution line by varying its constant term, and recover the input parameters. No experimental launches enter these calculations.
