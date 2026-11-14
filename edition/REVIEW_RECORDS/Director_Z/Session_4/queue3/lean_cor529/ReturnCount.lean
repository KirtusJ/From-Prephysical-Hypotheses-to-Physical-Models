import Mathlib

/-!
Return count bound (part (1) of the proof of the return-weight corollary).

Convention: `A i j` = number of arcs from `j` to `i`, so the out-degree of `j`
is the COLUMN sum `∑ i, A i j`, and `(A ^ t) i j` = number of walks of length `t`
from `j` to `i`.
-/

open Finset

namespace ReturnCount

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- All column sums of `A ^ t` equal `d ^ t` (no entry bound needed). -/
theorem col_sum_pow (A : Matrix n n ℕ) (d : ℕ) (hcol : ∀ j, ∑ i, A i j = d)
    (t : ℕ) (j : n) : ∑ i, (A ^ t) i j = d ^ t := by
  induction t generalizing j with
  | zero => simp [Matrix.one_apply]
  | succ t ih =>
    simp only [pow_succ', Matrix.mul_apply]
    rw [Finset.sum_comm]
    simp only [← Finset.sum_mul, hcol]
    rw [← Finset.mul_sum, ih]

/-- Main bound: closed walks of length `t+1` at any vertex number at most `d ^ t`. -/
theorem return_count_le (A : Matrix n n ℕ) (d : ℕ) (h01 : ∀ i j, A i j ≤ 1)
    (hcol : ∀ j, ∑ i, A i j = d) (t : ℕ) (x0 : n) :
    (A ^ (t + 1)) x0 x0 ≤ d ^ t := by
  rw [pow_succ', Matrix.mul_apply, ← col_sum_pow A d hcol t x0]
  exact Finset.sum_le_sum fun y _ => by
    calc A x0 y * (A ^ t) y x0 ≤ 1 * (A ^ t) y x0 := Nat.mul_le_mul_right _ (h01 x0 y)
      _ = (A ^ t) y x0 := one_mul _

/-- More general: any two vertices, walks of length `t+1` from `x` to `y`. -/
theorem walk_count_le (A : Matrix n n ℕ) (d : ℕ) (h01 : ∀ i j, A i j ≤ 1)
    (hcol : ∀ j, ∑ i, A i j = d) (t : ℕ) (x y : n) :
    (A ^ (t + 1)) y x ≤ d ^ t := by
  rw [pow_succ', Matrix.mul_apply, ← col_sum_pow A d hcol t x]
  exact Finset.sum_le_sum fun z _ => by
    calc A y z * (A ^ t) z x ≤ 1 * (A ^ t) z x := Nat.mul_le_mul_right _ (h01 y z)
      _ = (A ^ t) z x := one_mul _

/-- The entry bound is needed: one vertex with two parallel loops, `d = 2`, `t = 0`. -/
theorem entry_bound_needed :
    ∃ (A : Matrix (Fin 1) (Fin 1) ℕ) (d : ℕ), (∀ j, ∑ i, A i j = d) ∧
      ∀ t : ℕ, ¬ (A ^ (t + 1)) 0 0 ≤ d ^ t := by
  refine ⟨Matrix.of fun _ _ => 2, 2, fun j => by simp, fun t => ?_⟩
  have h : ∀ k : ℕ, ((Matrix.of fun _ _ => 2 : Matrix (Fin 1) (Fin 1) ℕ) ^ k) 0 0 = 2 ^ k := by
    intro k
    induction k with
    | zero => simp
    | succ k ih => simp [pow_succ, Matrix.mul_apply, ih]
  rw [h, pow_succ]
  have : 0 < 2 ^ t := by positivity
  omega

end ReturnCount

#print axioms ReturnCount.col_sum_pow
#print axioms ReturnCount.return_count_le
#print axioms ReturnCount.walk_count_le
#print axioms ReturnCount.entry_bound_needed
