import Mathlib

/-!
Algebraic steps of Lemma lem:maxp (1), (2) and of the paragraph
"Every vertex of R has at most one predecessor" in the proof of Theorem thm:vertexlaw.
-/

open Finset Matrix

/-- Lemma A, general form: real inner product space, no `μ`, no `card s ≥ 1`. -/
theorem eq_of_sum_eq_card_nsmul {ι E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (s : Finset ι) (w : ι → E) (c : E) (hw : ∀ i ∈ s, ‖w i‖ ≤ ‖c‖)
    (hsum : ∑ i in s, w i = s.card • c) : ∀ i ∈ s, w i = c := by
  have hle : ∀ i ∈ s, inner (w i) c ≤ ‖c‖ * ‖c‖ := fun i hi =>
    (real_inner_le_norm (w i) c).trans (mul_le_mul_of_nonneg_right (hw i hi) (norm_nonneg c))
  have hs : ∑ i in s, (inner (w i) c : ℝ) = ∑ _i in s, ‖c‖ * ‖c‖ := by
    rw [← sum_inner, hsum, ← Nat.cast_smul_eq_nsmul ℝ, real_inner_smul_left,
      real_inner_self_eq_norm_mul_norm, sum_const, nsmul_eq_mul]
  have heq := (sum_eq_sum_iff_of_le hle).1 hs
  intro i hi
  have h1 := norm_sub_sq_real (w i) c
  rw [heq i hi] at h1
  have h2 := hw i hi
  have h3 : ‖w i - c‖ ^ 2 ≤ 0 := by nlinarith [norm_nonneg (w i), norm_nonneg c]
  have h4 : ‖w i - c‖ = 0 := by nlinarith [norm_nonneg (w i - c)]
  exact sub_eq_zero.1 (norm_eq_zero.1 h4)

/-- Lemma A as stated, for `ℂ`. -/
theorem complex_eq_of_sum_eq_card_mul {ι : Type*} (s : Finset ι) (w : ι → ℂ) (μ : ℝ) (c : ℂ)
    (hw : ∀ i ∈ s, ‖w i‖ ≤ μ) (hc : ‖c‖ = μ)
    (hsum : ∑ i in s, w i = (s.card : ℂ) * c) : ∀ i ∈ s, w i = c :=
  eq_of_sum_eq_card_nsmul s w c (fun i hi => hc ▸ hw i hi) (by rw [hsum, nsmul_eq_mul])

section B
variable {R K : Type*} [Fintype R] [DecidableEq R] [Field K]

/-- Lemma B: invertibility. -/
theorem isUnit_det_of_mul_eq_smul_diagonal (M A : Matrix R R K) (f : R → K) (d : K)
    (hf : ∀ i, f i ≠ 0) (hd : d ≠ 0) (h : M * A = d • Matrix.diagonal f) :
    IsUnit A.det := by
  have h1 := congrArg Matrix.det h
  rw [det_mul, det_smul, det_diagonal] at h1
  have : M.det * A.det ≠ 0 := by
    rw [h1]; exact mul_ne_zero (pow_ne_zero _ hd) (Finset.prod_ne_zero_iff.2 fun i _ => hf i)
  exact isUnit_iff_ne_zero.2 (right_ne_zero_of_mul this)

theorem mul_inv_eq_one_of_mul_eq_smul_diagonal (M A : Matrix R R K) (f : R → K) (d : K)
    (hf : ∀ i, f i ≠ 0) (hd : d ≠ 0) (h : M * A = d • Matrix.diagonal f) :
    A * A⁻¹ = 1 :=
  Matrix.mul_nonsing_inv A (isUnit_det_of_mul_eq_smul_diagonal M A f d hf hd h)

/-- Lemma B, row version (the one the paper uses). -/
theorem eq_zero_of_vecMul_eq_zero_of_mul_eq_smul_diagonal (M A : Matrix R R K) (f : R → K)
    (d : K) (hf : ∀ i, f i ≠ 0) (hd : d ≠ 0) (h : M * A = d • Matrix.diagonal f)
    (g : R → K) (hg : Matrix.vecMul g A = 0) : g = 0 :=
  Matrix.eq_zero_of_vecMul_eq_zero
    (isUnit_det_of_mul_eq_smul_diagonal M A f d hf hd h).ne_zero hg

/-- Lemma B, column version. -/
theorem eq_zero_of_mulVec_eq_zero_of_mul_eq_smul_diagonal (M A : Matrix R R K) (f : R → K)
    (d : K) (hf : ∀ i, f i ≠ 0) (hd : d ≠ 0) (h : M * A = d • Matrix.diagonal f)
    (g : R → K) (hg : Matrix.mulVec A g = 0) : g = 0 :=
  Matrix.eq_zero_of_mulVec_eq_zero
    (isUnit_det_of_mul_eq_smul_diagonal M A f d hf hd h).ne_zero hg
end B

/-- Lemma C: pigeonhole. Only the heads of the arcs need lie in `W`. -/
theorem exists_two_predecessors {V : Type*} [DecidableEq V] (W : Finset V) (E : Finset (V × V))
    (d : ℕ) (hd : 2 ≤ d) (hW : W.Nonempty) (hE : ∀ p ∈ E, p.2 ∈ W)
    (hcard : d * W.card ≤ E.card) :
    ∃ z ∈ W, ∃ y y', y ≠ y' ∧ (y, z) ∈ E ∧ (y', z) ∈ E := by
  have hpos := hW.card_pos
  have hlt : W.card < E.card := by nlinarith
  obtain ⟨p, hp, q, hq, hne, hpq⟩ := exists_ne_map_eq_of_card_lt_of_maps_to hlt hE
  obtain ⟨y, z⟩ := p
  obtain ⟨y', z'⟩ := q
  simp only at hpq
  subst hpq
  exact ⟨z, hE _ hp, y, y', fun h => hne (by rw [h]), hp, hq⟩

#print axioms eq_of_sum_eq_card_nsmul
#print axioms complex_eq_of_sum_eq_card_mul
#print axioms isUnit_det_of_mul_eq_smul_diagonal
#print axioms mul_inv_eq_one_of_mul_eq_smul_diagonal
#print axioms eq_zero_of_vecMul_eq_zero_of_mul_eq_smul_diagonal
#print axioms eq_zero_of_mulVec_eq_zero_of_mul_eq_smul_diagonal
#print axioms exists_two_predecessors
