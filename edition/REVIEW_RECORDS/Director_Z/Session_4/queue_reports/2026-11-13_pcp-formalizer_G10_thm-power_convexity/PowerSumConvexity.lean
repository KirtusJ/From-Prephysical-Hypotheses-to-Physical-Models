/-
Convexity step of G10 Theorem 5.2 (label thm:power), in general form.

For a finite nonempty family of reals t_i ≥ 0 with ∑ t_i^2 = 2·(number of terms), and a real p > 0,
  ∑ t_i^p = 2·(number of terms)  ↔  p = 2.
In the paper t_z = |1 + u_z| over the m common successors, and ∑ t_z^2 = 2m follows from ∑ u_z = 0.
The hypothesis ∑ u_z = 0 is used only through ∑ t_z^2 = 2m; the unit modulus of u_z is not used.
Lean 4.12.0, Mathlib v4.12.0.
-/
import Mathlib

open Finset

namespace PowerSum

/-- For `t ≥ 0` and `0 < p ≤ 2`: `t^p ≤ (1 - p/2) + (p/2) t^2` (weighted AM-GM with the point 1). -/
theorem term_le_low (t p : ℝ) (ht : 0 ≤ t) (hp0 : 0 < p) (hp2 : p ≤ 2) :
    t ^ p ≤ (1 - p / 2) + (p / 2) * t ^ 2 := by
  have h := Real.geom_mean_le_arith_mean2_weighted (w₁ := 1 - p / 2) (w₂ := p / 2)
    (p₁ := 1) (p₂ := t ^ 2) (by linarith) (by linarith) (by norm_num) (by positivity) (by ring)
  have e : (t ^ 2 : ℝ) ^ (p / 2) = t ^ p := by
    rw [← Real.rpow_two, ← Real.rpow_mul ht]; congr 1; ring
  rw [Real.one_rpow, one_mul, e] at h
  linarith

/-- For `t ≥ 0` and `p ≥ 2`: `t^2 ≤ (1 - 2/p) + (2/p) t^p`. -/
theorem term_le_high (t p : ℝ) (ht : 0 ≤ t) (hp2 : 2 ≤ p) :
    t ^ 2 ≤ (1 - 2 / p) + (2 / p) * t ^ p := by
  have hp0 : 0 < p := by linarith
  have h2p : 2 / p ≤ 1 := by rw [div_le_one hp0]; exact hp2
  have h := Real.geom_mean_le_arith_mean2_weighted (w₁ := 1 - 2 / p) (w₂ := 2 / p)
    (p₁ := 1) (p₂ := t ^ p) (by linarith) (by positivity) (by norm_num)
    (Real.rpow_nonneg ht p) (by ring)
  have e : (t ^ p : ℝ) ^ (2 / p) = t ^ 2 := by
    rw [← Real.rpow_mul ht, ← Real.rpow_two]; congr 1; field_simp
  rw [Real.one_rpow, one_mul, e] at h
  linarith

/-- Main statement. -/
theorem power_sum_eq_iff {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (t : ι → ℝ)
    (ht : ∀ i ∈ s, 0 ≤ t i) (h2 : ∑ i ∈ s, t i ^ 2 = 2 * (s.card : ℝ))
    (p : ℝ) (hp : 0 < p) :
    ∑ i ∈ s, t i ^ p = 2 * (s.card : ℝ) ↔ p = 2 := by
  have hc : (0 : ℝ) < s.card := by exact_mod_cast Finset.card_pos.mpr hs
  constructor
  · intro h
    by_contra hne
    rcases lt_or_gt_of_ne hne with hlt | hgt
    · -- p < 2
      have hsum : ∑ i ∈ s, t i ^ p ≤ ∑ i ∈ s, ((1 - p / 2) + (p / 2) * t i ^ 2) :=
        Finset.sum_le_sum fun i hi => term_le_low (t i) p (ht i hi) hp hlt.le
      rw [Finset.sum_add_distrib, Finset.sum_const, ← Finset.mul_sum, h2, h, nsmul_eq_mul] at hsum
      nlinarith
    · -- p > 2
      have hsum : ∑ i ∈ s, t i ^ 2 ≤ ∑ i ∈ s, ((1 - 2 / p) + (2 / p) * t i ^ p) :=
        Finset.sum_le_sum fun i hi => term_le_high (t i) p (ht i hi) hgt.le
      rw [Finset.sum_add_distrib, Finset.sum_const, ← Finset.mul_sum, h2, h, nsmul_eq_mul] at hsum
      have h2p : 2 / p < 1 := by rw [div_lt_one hp]; exact hgt
      nlinarith
  · rintro rfl
    rw [← h2]
    exact Finset.sum_congr rfl fun i _ => Real.rpow_two (t i)

/-- The two quantitative bounds of the paper's proof with `h₀` replaced by the number of terms `m`
(`h₀ ≤ m`): for `0 < p ≤ 2`, `∑ t^p ≤ (1 + p/2) m`; for `p ≥ 2`, `∑ t^p ≥ (1 + p/2) m`. -/
theorem power_sum_le_low {ι : Type*} (s : Finset ι) (t : ι → ℝ)
    (ht : ∀ i ∈ s, 0 ≤ t i) (h2 : ∑ i ∈ s, t i ^ 2 = 2 * (s.card : ℝ))
    (p : ℝ) (hp : 0 < p) (hp2 : p ≤ 2) :
    ∑ i ∈ s, t i ^ p ≤ (1 + p / 2) * (s.card : ℝ) := by
  have hsum : ∑ i ∈ s, t i ^ p ≤ ∑ i ∈ s, ((1 - p / 2) + (p / 2) * t i ^ 2) :=
    Finset.sum_le_sum fun i hi => term_le_low (t i) p (ht i hi) hp hp2
  rw [Finset.sum_add_distrib, Finset.sum_const, ← Finset.mul_sum, h2, nsmul_eq_mul] at hsum
  linarith

theorem power_sum_ge_high {ι : Type*} (s : Finset ι) (t : ι → ℝ)
    (ht : ∀ i ∈ s, 0 ≤ t i) (h2 : ∑ i ∈ s, t i ^ 2 = 2 * (s.card : ℝ))
    (p : ℝ) (hp2 : 2 ≤ p) :
    (1 + p / 2) * (s.card : ℝ) ≤ ∑ i ∈ s, t i ^ p := by
  have hp : 0 < p := by linarith
  have hsum : ∑ i ∈ s, t i ^ 2 ≤ ∑ i ∈ s, ((1 - 2 / p) + (2 / p) * t i ^ p) :=
    Finset.sum_le_sum fun i hi => term_le_high (t i) p (ht i hi) hp2
  rw [Finset.sum_add_distrib, Finset.sum_const, ← Finset.mul_sum, h2, nsmul_eq_mul] at hsum
  have key : (2 / p) * ∑ i ∈ s, t i ^ p ≥ (1 + 2 / p) * (s.card : ℝ) := by linarith
  have hone : (p / 2) * (2 / p) = 1 := by field_simp
  have e1 : (p / 2) * ((2 / p) * ∑ i ∈ s, t i ^ p) = ∑ i ∈ s, t i ^ p := by
    rw [← mul_assoc, hone, one_mul]
  have e2 : (p / 2) * ((1 + 2 / p) * (s.card : ℝ)) = (1 + p / 2) * (s.card : ℝ) := by
    have : (p / 2) * (1 + 2 / p) = 1 + p / 2 := by rw [mul_add, hone]; ring
    rw [← mul_assoc, this]
  have hp2' : (0 : ℝ) ≤ p / 2 := by positivity
  have := mul_le_mul_of_nonneg_left key hp2'
  rw [e1, e2] at this
  exact this

end PowerSum

#print axioms PowerSum.power_sum_eq_iff
#print axioms PowerSum.power_sum_le_low
#print axioms PowerSum.power_sum_ge_high
