import Mathlib

open Finset

namespace FPHPM.MultisetBlock

/-! ## Lemma A (unit sum) -/

/-- Complex numbers of norm at most one, indexed by a finset, whose sum is the cardinality
of the finset, are all equal to one. -/
theorem unit_sum {ι : Type*} (s : Finset ι) (z : ι → ℂ)
    (hz : ∀ i ∈ s, ‖z i‖ ≤ 1) (hsum : ∑ i in s, z i = (s.card : ℂ)) :
    ∀ i ∈ s, z i = 1 := by
  have hre : ∀ i ∈ s, (z i).re ≤ 1 := fun i hi => (Complex.re_le_abs (z i)).trans (hz i hi)
  have hs : ∑ i in s, (z i).re = ∑ _i in s, (1 : ℝ) := by
    have := congrArg Complex.re hsum
    simpa using this
  have hall := (Finset.sum_eq_sum_iff_of_le hre).1 hs
  intro i hi
  have h1 : (z i).re = 1 := hall i hi
  have h2 : Complex.normSq (z i) ≤ 1 := by
    have h0 := hz i hi
    rw [Complex.norm_eq_abs] at h0
    rw [Complex.normSq_eq_abs]
    have := Complex.abs.nonneg (z i)
    nlinarith
  rw [Complex.normSq_apply, h1] at h2
  have h3 : (z i).im = 0 := by nlinarith [mul_self_nonneg (z i).im]
  exact Complex.ext (by simpa using h1) (by simpa using h3)

/-- Lemma A as asked: norm exactly one, indexed by `Fin d`, sum equal to `d`. -/
theorem unit_sum_fin (d : ℕ) (z : Fin d → ℂ) (hz : ∀ i, ‖z i‖ = 1)
    (hsum : ∑ i, z i = (d : ℂ)) : ∀ i, z i = 1 := by
  intro i
  exact unit_sum Finset.univ z (fun i _ => (hz i).le) (by simpa using hsum) i (Finset.mem_univ i)

/-! ## Lemma B (triple pairing forces a zero vector) -/

/-- Over any field, for any finite index type and any nonzero constant `c`: if the triple
pairing of `u y`, `v y'`, `r y''` is `c` on the diagonal and `0` off it, then `u y * v y'`
is the zero vector for `y ≠ y'`. -/
theorem triple_pairing_zero {K ι : Type*} [Field K] [Fintype ι] [DecidableEq ι]
    (u v r : ι → ι → K) (c : K) (hc : c ≠ 0)
    (h : ∀ y y' y'', ∑ z, u y z * v y' z * r y'' z = if y = y' ∧ y = y'' then c else 0)
    {y y' : ι} (hy : y ≠ y') : ∀ z, u y z * v y' z = 0 := by
  let M : Matrix ι ι K := Matrix.of fun y'' z => c⁻¹ * r y'' z
  let N : Matrix ι ι K := Matrix.of fun z x => u x z * v x z
  have hMN : M * N = 1 := by
    ext a b
    simp only [M, N, Matrix.mul_apply, Matrix.of_apply, Matrix.one_apply]
    have := h b b a
    have e : ∑ z, c⁻¹ * r a z * (u b z * v b z) = c⁻¹ * ∑ z, u b z * v b z * r a z := by
      rw [Finset.mul_sum]; exact Finset.sum_congr rfl fun z _ => by ring
    rw [e, this]
    by_cases hab : a = b
    · subst hab; simp [hc]
    · have : ¬ b = a := fun hh => hab hh.symm
      simp [hab, this]
  have hNM : N * M = 1 := (Matrix.mul_eq_one_comm).1 hMN
  set w : ι → K := fun z => u y z * v y' z with hw
  have hMw : M.mulVec w = 0 := by
    ext a
    simp only [M, Matrix.mulVec, Matrix.dotProduct, Matrix.of_apply, Pi.zero_apply, hw]
    have := h y y' a
    have e : ∑ z, c⁻¹ * r a z * (u y z * v y' z) = c⁻¹ * ∑ z, u y z * v y' z * r a z := by
      rw [Finset.mul_sum]; exact Finset.sum_congr rfl fun z _ => by ring
    rw [e, this]
    simp [hy]
  have hw0 : w = 0 := by
    have : (N * M).mulVec w = w := by rw [hNM, Matrix.one_mulVec]
    rw [← this, ← Matrix.mulVec_mulVec, hMw, Matrix.mulVec_zero]
  intro z
  exact congrFun hw0 z

/-- Corollary over any field: with at least two indices and nowhere-vanishing `u`, `v`,
the pairing hypothesis is contradictory. -/
theorem triple_pairing_false {K ι : Type*} [Field K] [Fintype ι] [DecidableEq ι] [Nontrivial ι]
    (u v r : ι → ι → K) (c : K) (hc : c ≠ 0)
    (hu : ∀ y z, u y z ≠ 0) (hv : ∀ y z, v y z ≠ 0)
    (h : ∀ y y' y'', ∑ z, u y z * v y' z * r y'' z = if y = y' ∧ y = y'' then c else 0) :
    False := by
  obtain ⟨y, y', hy⟩ := exists_pair_ne ι
  exact mul_ne_zero (hu y y) (hv y' y) (triple_pairing_zero u v r c hc h hy y)

/-- Lemma B as asked: `Fin d`, complex entries, constant `d`, `d ≥ 2`. -/
theorem triple_pairing_zero_fin (d : ℕ) (hd : 2 ≤ d) (u v r : Fin d → Fin d → ℂ)
    (h : ∀ y y' y'', ∑ z, u y z * v y' z * r y'' z = if y = y' ∧ y = y'' then (d : ℂ) else 0)
    {y y' : Fin d} (hy : y ≠ y') : ∀ z, u y z * v y' z = 0 :=
  triple_pairing_zero u v r (d : ℂ) (by exact_mod_cast (by omega : d ≠ 0)) h hy

/-- Corollary as asked: if moreover all entries of `u` and `v` have norm one, `False`. -/
theorem triple_pairing_false_fin (d : ℕ) (hd : 2 ≤ d) (u v r : Fin d → Fin d → ℂ)
    (hu : ∀ y z, ‖u y z‖ = 1) (hv : ∀ y z, ‖v y z‖ = 1)
    (h : ∀ y y' y'', ∑ z, u y z * v y' z * r y'' z = if y = y' ∧ y = y'' then (d : ℂ) else 0) :
    False := by
  haveI : Nontrivial (Fin d) := Fin.nontrivial_iff_two_le.2 hd
  refine triple_pairing_false u v r (d : ℂ) (by exact_mod_cast (by omega : d ≠ 0)) ?_ ?_ h
  · intro y z hz; have := hu y z; rw [hz] at this; simp at this
  · intro y z hz; have := hv y z; rw [hz] at this; simp at this

/-! ## Lemma C (quadratic vanishing) -/

/-- Evaluation of a general quadratic at `x e_i + x' e_k`. -/
theorem quad_eval {K ι : Type*} [Field K] [Fintype ι] [DecidableEq ι]
    (c : K) (a : ι → K) (G : ι → ι → K) (i k : ι) (x x' : K) :
    (c + ∑ j, a j * (Pi.single i x + Pi.single k x' : ι → K) j
      + ∑ j, ∑ l, G j l * (Pi.single i x + Pi.single k x' : ι → K) j
          * (Pi.single i x + Pi.single k x' : ι → K) l)
    = c + a i * x + a k * x' + G i i * x * x + G i k * x * x' + G k i * x' * x
        + G k k * x' * x' := by
  simp only [Pi.add_apply, Pi.single_apply, mul_add, add_mul, Finset.sum_add_distrib, mul_ite,
    ite_mul, mul_zero, zero_mul, Finset.sum_ite_eq', Finset.sum_ite_eq, Finset.mem_univ, if_true]
  ring

/-- General form, any field with `2 ≠ 0`, any finite index type, full coefficient matrix `G`
(no order needed): a quadratic vanishing at `0`, `e_i`, `2 e_i` and `e_i + e_k` (`i ≠ k`) has
`c = 0`, `a = 0`, zero diagonal and antisymmetric `G`, and vanishes identically. -/
theorem quad_vanish_matrix {K ι : Type*} [Field K] [Fintype ι] [DecidableEq ι]
    (h2 : (2 : K) ≠ 0) (c : K) (a : ι → K) (G : ι → ι → K)
    (p : (ι → K) → K)
    (hp : ∀ t, p t = c + ∑ j, a j * t j + ∑ j, ∑ l, G j l * t j * t l)
    (h0 : p 0 = 0) (h1 : ∀ i, p (Pi.single i 1) = 0) (h2e : ∀ i, p (Pi.single i 2) = 0)
    (h11 : ∀ i k, i ≠ k → p (Pi.single i 1 + Pi.single k 1) = 0) :
    c = 0 ∧ (∀ i, a i = 0) ∧ (∀ i, G i i = 0) ∧ (∀ i k, G i k + G k i = 0) ∧ ∀ t, p t = 0 := by
  have hc : c = 0 := by
    have := h0; rw [hp] at this; simpa using this
  have e1 : ∀ i, a i + G i i = 0 := by
    intro i
    have := quad_eval c a G i i (1 : K) 0
    simp only [Pi.single_zero, add_zero] at this
    have h := h1 i; rw [hp, this, hc] at h
    simpa using h
  have e2 : ∀ i, 2 * a i + 4 * G i i = 0 := by
    intro i
    have := quad_eval c a G i i (2 : K) 0
    simp only [Pi.single_zero, add_zero] at this
    have h := h2e i; rw [hp, this, hc] at h
    linear_combination h
  have hG : ∀ i, G i i = 0 := by
    intro i
    have : 2 * G i i = 0 := by linear_combination e2 i - 2 * e1 i
    exact (mul_eq_zero.1 this).resolve_left h2
  have ha : ∀ i, a i = 0 := fun i => by have := e1 i; rw [hG i, add_zero] at this; exact this
  have hGs : ∀ i k, G i k + G k i = 0 := by
    intro i k
    by_cases hik : i = k
    · subst hik; rw [hG i, add_zero]
    · have := quad_eval c a G i k (1 : K) 1
      have h := h11 i k hik; rw [hp, this, hc, ha i, ha k, hG i, hG k] at h
      linear_combination h
  refine ⟨hc, ha, hG, hGs, ?_⟩
  intro t
  rw [hp, hc]
  have s1 : ∑ j, a j * t j = 0 := Finset.sum_eq_zero fun j _ => by rw [ha j, zero_mul]
  have s2 : (∑ j, ∑ l, G j l * t j * t l) = 0 := by
    have hsw : (∑ j, ∑ l, G j l * t j * t l) = ∑ j, ∑ l, G l j * t j * t l := by
      rw [Finset.sum_comm]
      exact Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun l _ => by ring
    have hadd : (∑ j, ∑ l, G j l * t j * t l) + (∑ j, ∑ l, G j l * t j * t l) = 0 := by
      nth_rewrite 2 [hsw]
      rw [← Finset.sum_add_distrib]
      refine Finset.sum_eq_zero fun j _ => ?_
      rw [← Finset.sum_add_distrib]
      refine Finset.sum_eq_zero fun l _ => ?_
      linear_combination (t j * t l) * hGs j l
    have : 2 * (∑ j, ∑ l, G j l * t j * t l) = 0 := by linear_combination hadd
    exact (mul_eq_zero.1 this).resolve_left h2
  rw [s1, s2]; ring

/-- Lemma C in the form of the paper: linearly ordered finite index type, coefficients
`c`, `a i`, `b i` (of `t_i^2`) and `g i k` used only for `i < k`. -/
theorem quad_vanish {K ι : Type*} [Field K] [Fintype ι] [DecidableEq ι] [LinearOrder ι]
    (h2 : (2 : K) ≠ 0) (c : K) (a b : ι → K) (g : ι → ι → K)
    (p : (ι → K) → K)
    (hp : ∀ t, p t = c + ∑ i, a i * t i + ∑ i, b i * t i ^ 2
      + ∑ i, ∑ k, if i < k then g i k * t i * t k else 0)
    (h0 : p 0 = 0) (h1 : ∀ i, p (Pi.single i 1) = 0) (h2e : ∀ i, p (Pi.single i 2) = 0)
    (h11 : ∀ i k, i < k → p (Pi.single i 1 + Pi.single k 1) = 0) :
    c = 0 ∧ (∀ i, a i = 0) ∧ (∀ i, b i = 0) ∧ (∀ i k, i < k → g i k = 0) ∧ ∀ t, p t = 0 := by
  let G : ι → ι → K := fun i k => if i = k then b i else if i < k then g i k else 0
  have hp' : ∀ t, p t = c + ∑ j, a j * t j + ∑ j, ∑ l, G j l * t j * t l := by
    intro t
    rw [hp, add_assoc (c + _)]
    congr 1
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun i _ => ?_
    have : b i * t i ^ 2 = ∑ k, if i = k then b i * t i * t k else 0 := by
      rw [Finset.sum_ite_eq]; simp; ring
    rw [this, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    simp only [G]
    by_cases hik : i = k
    · subst hik; simp
    · simp [hik]
  have h11' : ∀ i k, i ≠ k → p (Pi.single i 1 + Pi.single k 1) = 0 := by
    intro i k hik
    rcases lt_or_gt_of_ne hik with h | h
    · exact h11 i k h
    · rw [add_comm]; exact h11 k i h
  obtain ⟨hc, ha, hG, hGs, hall⟩ := quad_vanish_matrix h2 c a G p hp' h0 h1 h2e h11'
  refine ⟨hc, ha, fun i => by simpa [G] using hG i, ?_, hall⟩
  intro i k hik
  have := hGs i k
  simpa [G, hik.ne, hik.ne', hik, not_lt_of_gt hik] using this

/-- Lemma C over the reals, variables indexed by `Fin n`. -/
theorem quad_vanish_real (n : ℕ) (c : ℝ) (a b : Fin n → ℝ) (g : Fin n → Fin n → ℝ)
    (p : (Fin n → ℝ) → ℝ)
    (hp : ∀ t, p t = c + ∑ i, a i * t i + ∑ i, b i * t i ^ 2
      + ∑ i, ∑ k, if i < k then g i k * t i * t k else 0)
    (h0 : p 0 = 0) (h1 : ∀ i, p (Pi.single i 1) = 0) (h2e : ∀ i, p (Pi.single i 2) = 0)
    (h11 : ∀ i k, i < k → p (Pi.single i 1 + Pi.single k 1) = 0) :
    c = 0 ∧ (∀ i, a i = 0) ∧ (∀ i, b i = 0) ∧ (∀ i k, i < k → g i k = 0) ∧ ∀ t, p t = 0 :=
  quad_vanish two_ne_zero c a b g p hp h0 h1 h2e h11

end FPHPM.MultisetBlock

#print axioms FPHPM.MultisetBlock.unit_sum
#print axioms FPHPM.MultisetBlock.unit_sum_fin
#print axioms FPHPM.MultisetBlock.triple_pairing_zero
#print axioms FPHPM.MultisetBlock.triple_pairing_false
#print axioms FPHPM.MultisetBlock.triple_pairing_zero_fin
#print axioms FPHPM.MultisetBlock.triple_pairing_false_fin
#print axioms FPHPM.MultisetBlock.quad_eval
#print axioms FPHPM.MultisetBlock.quad_vanish_matrix
#print axioms FPHPM.MultisetBlock.quad_vanish
#print axioms FPHPM.MultisetBlock.quad_vanish_real
