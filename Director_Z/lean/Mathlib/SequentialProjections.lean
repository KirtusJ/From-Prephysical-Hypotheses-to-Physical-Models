import Mathlib

open RCLike Finset

namespace FPHPM.SequentialProjections

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]

local notation "⟪" x ", " y "⟫" => @inner 𝕜 _ _ x y

/-- Pythagoras for an idempotent self-adjoint operator. -/
theorem proj_pyth (P : E →L[𝕜] E) (hid : ∀ x, P (P x) = P x)
    (hsa : ∀ x y, ⟪P x, y⟫ = ⟪x, P y⟫) (x : E) :
    ‖x‖ ^ 2 - ‖P x‖ ^ 2 = ‖x - P x‖ ^ 2 := by
  have h0 : ⟪P x, x - P x⟫ = 0 := by
    rw [hsa, map_sub, hid, sub_self, inner_zero_right]
  have h := norm_add_sq (𝕜 := 𝕜) (P x) (x - P x)
  rw [h0, add_sub_cancel] at h
  simp at h
  linarith

/-- Gao's sequential-measurement bound, sequences indexed by `ℕ`.
`Q j` (for `j < K`) are idempotent and self-adjoint, `w 0 = v`, `w (j+1) = Q j (w j)`. -/
theorem gao_nat (Q : ℕ → E →L[𝕜] E) (K : ℕ)
    (hid : ∀ j < K, ∀ x, Q j (Q j x) = Q j x)
    (hsa : ∀ j < K, ∀ x y, ⟪Q j x, y⟫ = ⟪x, Q j y⟫)
    (v : E) (hv : ‖v‖ = 1) (w : ℕ → E) (hw0 : w 0 = v)
    (hw : ∀ j < K, w (j + 1) = Q j (w j)) :
    ‖v - w K‖ ^ 2 ≤ ∑ j in range K, ‖v - Q j v‖ ^ 2 ∧
    1 - ‖w K‖ ^ 2 ≤ 4 * ∑ j in range K, ‖v - Q j v‖ ^ 2 := by
  -- telescoping of the norms
  have hL : ∑ j in range K, ‖w j - w (j + 1)‖ ^ 2 = 1 - ‖w K‖ ^ 2 := by
    have : ∀ j ∈ range K, ‖w j - w (j + 1)‖ ^ 2 = ‖w j‖ ^ 2 - ‖w (j + 1)‖ ^ 2 := by
      intro j hj
      have hj' := mem_range.1 hj
      rw [hw j hj', proj_pyth (Q j) (hid j hj') (hsa j hj')]
    rw [sum_congr rfl this, sum_range_sub' (fun j => ‖w j‖ ^ 2), hw0, hv]
    norm_num
  -- telescoping of the inner products
  have hT : ∑ j in range K, re ⟪v - Q j v, w j - w (j + 1)⟫ = 1 - re ⟪v, w K⟫ := by
    have : ∀ j ∈ range K, re ⟪v - Q j v, w j - w (j + 1)⟫
        = re ⟪v, w j⟫ - re ⟪v, w (j + 1)⟫ := by
      intro j hj
      have hj' := mem_range.1 hj
      have h0 : ⟪Q j v, w j - w (j + 1)⟫ = 0 := by
        rw [hw j hj', hsa j hj', map_sub, hid j hj', sub_self, inner_zero_right]
      rw [inner_sub_left, h0, sub_zero, inner_sub_right, map_sub]
    rw [sum_congr rfl this, sum_range_sub' (fun j => re ⟪v, w j⟫), hw0,
      inner_self_eq_norm_sq, hv]
    norm_num
  set S := ∑ j in range K, ‖v - Q j v‖ ^ 2 with hS
  set L := 1 - ‖w K‖ ^ 2 with hLdef
  have hS0 : 0 ≤ S := sum_nonneg fun j _ => sq_nonneg _
  have hL0 : 0 ≤ L := by rw [← hL]; exact sum_nonneg fun j _ => sq_nonneg _
  -- Cauchy–Schwarz
  have hCS : 1 - re ⟪v, w K⟫ ≤ √S * √L := by
    rw [← hT, ← hL, hS]
    calc ∑ j in range K, re ⟪v - Q j v, w j - w (j + 1)⟫
        ≤ ∑ j in range K, ‖v - Q j v‖ * ‖w j - w (j + 1)‖ :=
          sum_le_sum fun j _ => re_inner_le_norm _ _
      _ ≤ _ := Real.sum_mul_le_sqrt_mul_sqrt _ _ _
  have hD : ‖v - w K‖ ^ 2 = 2 * (1 - re ⟪v, w K⟫) - L := by
    rw [norm_sub_sq (𝕜 := 𝕜), hv, hLdef]; ring
  have hs0 := Real.sqrt_nonneg S
  have hs2 : √S ^ 2 = S := Real.sq_sqrt hS0
  have hl2 : √L ^ 2 = L := Real.sq_sqrt hL0
  have hDnn : 0 ≤ ‖v - w K‖ ^ 2 := sq_nonneg _
  constructor
  · rw [hD]
    nlinarith [sq_nonneg (√S - √L)]
  · have h1 : √L ^ 2 ≤ 2 * (√S * √L) := by linarith
    have hl0 := Real.sqrt_nonneg L
    rcases le_or_lt (√L) (2 * √S) with h | h
    · nlinarith
    · nlinarith

/-- Gao's sequential-measurement bound for `K` projections `Q : Fin K → (E →L[𝕜] E)`
(each idempotent and self-adjoint), with `w 0 = v`, `w (j+1) = Q j (w j)`. -/
theorem gao_sequential {K : ℕ} (Q : Fin K → E →L[𝕜] E)
    (hid : ∀ j x, Q j (Q j x) = Q j x)
    (hsa : ∀ j x y, ⟪Q j x, y⟫ = ⟪x, Q j y⟫)
    (v : E) (hv : ‖v‖ = 1) (w : Fin (K + 1) → E) (hw0 : w 0 = v)
    (hw : ∀ j : Fin K, w j.succ = Q j (w j.castSucc)) :
    ‖v - w (Fin.last K)‖ ^ 2 ≤ ∑ j, ‖v - Q j v‖ ^ 2 ∧
    1 - ‖w (Fin.last K)‖ ^ 2 ≤ 4 * ∑ j, ‖v - Q j v‖ ^ 2 := by
  have key := gao_nat (𝕜 := 𝕜) (fun j => if h : j < K then Q ⟨j, h⟩ else 0) K
    (fun j hj x => by simp only [dif_pos hj]; exact hid _ x)
    (fun j hj x y => by simp only [dif_pos hj]; exact hsa _ x y)
    v hv (fun j => if h : j < K + 1 then w ⟨j, h⟩ else 0)
    (by simpa using hw0)
    (fun j hj => by
      simp only [dif_pos hj, dif_pos (Nat.succ_lt_succ hj), dif_pos (Nat.lt_succ_of_lt hj)]
      exact hw ⟨j, hj⟩)
  have hsum : ∑ j in range K, ‖v - (if h : j < K then Q ⟨j, h⟩ else 0) v‖ ^ 2
      = ∑ j : Fin K, ‖v - Q j v‖ ^ 2 := by
    rw [Finset.sum_range]
    exact Fintype.sum_congr _ _ fun j => by simp
  rw [hsum] at key
  simpa [Fin.last] using key

end FPHPM.SequentialProjections

#print axioms FPHPM.SequentialProjections.gao_sequential
