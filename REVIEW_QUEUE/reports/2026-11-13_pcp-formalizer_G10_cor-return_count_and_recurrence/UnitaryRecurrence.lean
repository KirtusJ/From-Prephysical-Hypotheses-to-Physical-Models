import Mathlib

/-!
Recurrence of the powers of a unitary: for every `ε > 0` and every `T` there is
`t ≥ T`, `t ≥ 1`, with `‖U ^ t - 1‖ < ε`.

Norm used for matrices: the L2 operator norm (`open scoped Matrix.L2OpNorm`,
instances `Matrix.instL2OpNormedRing`, `Matrix.instCStarRing`).
-/

open Filter Topology

namespace UnitaryRecurrence

/-- General form: a unitary element of a C⋆-ring whose closed balls are compact. -/
theorem unitary_pow_recurrence {E : Type*} [NormedRing E] [StarRing E] [CStarRing E]
    [ProperSpace E] {U : E} (hU : U ∈ unitary E) {ε : ℝ} (hε : 0 < ε) (T : ℕ) :
    ∃ t : ℕ, T ≤ t ∧ 1 ≤ t ∧ ‖U ^ t - 1‖ < ε := by
  have hpow : ∀ k : ℕ, U ^ k ∈ unitary E := fun k => pow_mem hU k
  have hmem : ∀ k : ℕ, U ^ k ∈ Metric.closedBall (0 : E) ‖(1 : E)‖ := by
    intro k
    rw [mem_closedBall_zero_iff]
    have := CStarRing.norm_mem_unitary_mul (1 : E) (hpow k)
    rw [mul_one] at this
    exact this.le
  obtain ⟨a, -, φ, hφ, hlim⟩ :=
    (isCompact_closedBall (0 : E) ‖(1 : E)‖).tendsto_subseq hmem
  obtain ⟨N, hN⟩ := (Metric.tendsto_atTop.1 hlim) (ε / 2) (half_pos hε)
  have hgap : ∀ k : ℕ, φ N + k ≤ φ (N + k) := by
    intro k
    induction k with
    | zero => simp
    | succ k ih =>
      have h : φ (N + k) < φ (N + (k + 1)) := hφ (by omega)
      omega
  have hk := hgap (T + 1)
  refine ⟨φ (N + (T + 1)) - φ N, by omega, by omega, ?_⟩
  have h1 := hN N le_rfl
  have h2 := hN (N + (T + 1)) (by omega)
  simp only [Function.comp_apply] at h1 h2
  have hfac : U ^ φ N * (U ^ (φ (N + (T + 1)) - φ N) - 1) = U ^ φ (N + (T + 1)) - U ^ φ N := by
    rw [mul_sub, mul_one, ← pow_add]
    congr 2
    omega
  rw [← CStarRing.norm_mem_unitary_mul _ (hpow (φ N)), hfac, ← dist_eq_norm]
  calc dist (U ^ φ (N + (T + 1))) (U ^ φ N)
      ≤ dist (U ^ φ (N + (T + 1))) a + dist (U ^ φ N) a := dist_triangle_right _ _ _
    _ < ε / 2 + ε / 2 := add_lt_add h2 h1
    _ = ε := add_halves ε

open scoped Matrix.L2OpNorm in
/-- Matrix form, in the L2 operator norm. -/
theorem matrix_unitary_pow_recurrence {n : Type*} [Fintype n] [DecidableEq n]
    (U : Matrix n n ℂ) (hU : U ∈ Matrix.unitaryGroup n ℂ) (ε : ℝ) (hε : 0 < ε) (T : ℕ) :
    ∃ t : ℕ, T ≤ t ∧ 1 ≤ t ∧ ‖U ^ t - 1‖ < ε := by
  haveI : ProperSpace (Matrix n n ℂ) := FiniteDimensional.proper_rclike ℂ (Matrix n n ℂ)
  exact unitary_pow_recurrence hU hε T

end UnitaryRecurrence

#print axioms UnitaryRecurrence.unitary_pow_recurrence
#print axioms UnitaryRecurrence.matrix_unitary_pow_recurrence
