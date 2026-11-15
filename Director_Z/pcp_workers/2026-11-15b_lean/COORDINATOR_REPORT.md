CONTROL: besides f(∅)=0, lem:twolevelabs asks (1) invariance under T_δ; (2) f(m)=f(T_β m) for m ∈ M(C_0); (3) eq. fgQ at pairs u ∈ M(C_0∪C_1), v ∈ M(C_1) and at pairs u ∈ M(C_0), v ∈ M(C_0∪C_1).

BLOCK: no Agent tool in this session, so no pcp-formalizer or pcp-micro-review child was launched and there are no child controls. The coordinator wrote and ran all four files itself. One agent of the author's model family; not independent review, and not even the two-reader structure asked for.

All four: Lean 4.12.0, Mathlib v4.12.0, exit 0, axioms propext, Classical.choice, Quot.sound only, no sorry. Each rerun by me from this folder after resumption.

T1 SymQuad.lean. mon x y = ![x², xy, y²].
- symquad_two: t : Fin 3→Fin 3→ℝ with t i j = t j i ⟹ Σ_ij t i j·mon p i·mon q j = t00 π0² + t22 π2² + t01 π0π1 + t12 π1π2 + t02 π1² + (t11 − 2 t02) π0π2.
- symquad_two_fun: symmetry of the function implies symmetry of the array.
- symquad_two_unique: a quadratic form in π vanishing at all real (p,q) is zero.
- symquad_three: k=3, t symmetric under both adjacent swaps ⟹ T = t000π0² + t001π0π1 + (t011−2t002)π0π2 + (t111−3t012)π0π3 + t002π1² + t012π1π2 + (t112−2t022)π1π3 + t022π2² + t122π2π3 + t222π3².
Not covered: general k; uniqueness and function-to-array symmetry for k=3; the dimension count. First run failed (my wrong multiplicities), recorded.

T2 Transfer.lean. V a real vector space, b, b' linear, d bilinear, g = a n1 n2 + n1 b(x2) + n2 b'(x1) + d(x1,x2).
- transfer_core: g(u n1, s x1, n2, x2) = g(n1, x1, u n2, s x2) for u ∈ {τ,τ'}, τ≠τ' ⟹ n1 b(x2) = n2 b'(x1).
- transfer_vanish: on a set S of points containing (n0,0), n0≠0: b and b' vanish at every x occurring.
- transfer_zero: if those x span V, b = b' = 0.
Not covered: that g has this shape (the "linearly independent, so sum of products" step), more than two factors with the other factors as parameters, existence of the multisets (count 2, p=0; two A with equal ε_0), that the monomial vectors span R³. Remark: one A with |A| ≠ ε_0(A)² would suffice.

T3 ThreeStep.lean (ℝ[X], d = e+2).
- L_single: deg π ≤ d, b_{d'}=0 for d'<d, d<K ⟹ Σ_{d'<K} b_{d'} Σ_{i<K} π_i π_{i+d'} = b_d π_0 π_d.
- piA/piB coefficients for every e and every real σ: constant 4+σ and 1; top σ and 2(2+σ); degrees ≤ e+2.
- step: σ=±1 and L(π_A)=L(π_B) ⟹ b_{e+2}=0. all_zero: strong induction, b_d=0 for d<K.
- Qbar_shift: Q̄(σe2,e0,e1)=Q̄(e0,e1,e2) given σ²=1.
- AB_coincidence: X(4+σ+σX)(1+X) − (1+2X)(1+(2+σ)X) = σ(X³−σ) given σ²=1.
Not covered: that φ(Xπ) = (σπ̄2, π̄0, π̄1); that Q̄∘φ has the banded shape with c*_0=q, c*_1=c; the multiset identity e_β*A=B in N[A] (only its polynomial shadow); F_R(A*C)=F_R(B*C). First run failed (one_mul/mul_one), output kept.

T4 AxisQuad.lean. γ : ℤ→ℤ→ℝ.
- axis_quad: the equation for all s and all t on either axis ⟹ ∃ q0 q1 c, γ = q0 s0² + q1 s1² + c s0 s1. No evenness hypothesis: "even" is not needed; axis_even derives it.
- axis_quad_unit: unit steps and γ(0,0)=0 suffice.
- axis_quad_AB: the families as thm:fgadj has them ((A) t on second axis; (B) s on first axis, t arbitrary) give the same conclusion; evenness follows from (B) at s=0. So the sentence of lem:twolevelabs deriving evenness separately is not needed for this step.
Not covered: that G_0 = γ∘ε (Steps 1–5). WindingAxis.lean not read.

Files: this folder, NOTES.md, four .lean with .out, ThreeStep.run1_failed.out.
