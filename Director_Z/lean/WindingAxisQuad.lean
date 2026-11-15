import Mathlib
/-!
T4. The replacement of Step 6: gamma on Z^2 with
  gamma(s+t) + gamma(s-t) = 2 gamma(s) + 2 gamma(t)   for all s and all t on a coordinate axis
is q0 s0^2 + q1 s1^2 + c s0 s1.  Evenness is NOT assumed.
-/

/-- one variable: a second difference that is constant gives a quadratic polynomial -/
theorem second_diff (f : ℤ → ℝ) (k : ℝ)
    (h : ∀ n : ℤ, f (n + 1) + f (n - 1) = 2 * f n + 2 * k) :
    ∀ n : ℤ, f n = f 0 + n * (f 1 - f 0 - k) + k * n ^ 2 := by
  have pos : ∀ n : ℕ, f n = f 0 + n * (f 1 - f 0 - k) + k * (n:ℝ) ^ 2 ∧
      f (n + 1) = f 0 + (n + 1) * (f 1 - f 0 - k) + k * ((n:ℝ) + 1) ^ 2 := by
    intro n
    induction n with
    | zero => constructor <;> simp <;> ring
    | succ n ih =>
      obtain ⟨a, b⟩ := ih
      refine ⟨by push_cast; exact b, ?_⟩
      have := h (n + 1)
      simp only [add_sub_cancel_right] at this
      push_cast
      linarith
  have neg : ∀ n : ℕ, f (-(n:ℤ)) = f 0 + (-(n:ℝ)) * (f 1 - f 0 - k) + k * (n:ℝ) ^ 2 ∧
      f (-(n:ℤ) + 1) = f 0 + (-(n:ℝ) + 1) * (f 1 - f 0 - k) + k * (-(n:ℝ) + 1) ^ 2 := by
    intro n
    induction n with
    | zero => constructor <;> simp <;> ring
    | succ n ih =>
      obtain ⟨a, b⟩ := ih
      have e1 : (-((n + 1 : ℕ) : ℤ) + 1) = -(n:ℤ) := by push_cast; ring
      have e2 : -((n + 1 : ℕ) : ℤ) = -(n:ℤ) - 1 := by push_cast; ring
      have := h (-(n:ℤ))
      rw [e1, e2]
      push_cast
      constructor <;> linarith
  intro n
  rcases Int.eq_nat_or_neg n with ⟨m, rfl | rfl⟩
  · simpa using (pos m).1
  · have := (neg m).1
    simp only [Int.cast_neg, Int.cast_natCast, neg_sq]
    exact this

/-- unit steps only: the equation for t = (1,0) and t = (0,1), and gamma(0,0) = 0. -/
theorem axis_quad_unit (γ : ℤ → ℤ → ℝ) (h00 : γ 0 0 = 0)
    (hx : ∀ s0 s1 : ℤ, γ (s0 + 1) s1 + γ (s0 - 1) s1 = 2 * γ s0 s1 + 2 * γ 1 0)
    (hy : ∀ s0 s1 : ℤ, γ s0 (s1 + 1) + γ s0 (s1 - 1) = 2 * γ s0 s1 + 2 * γ 0 1) :
    ∀ s0 s1 : ℤ, γ s0 s1 = γ 1 0 * s0 ^ 2 + γ 0 1 * s1 ^ 2
        + (γ 1 1 - γ 1 0 - γ 0 1) * s0 * s1 := by
  intro s0 s1
  have a := second_diff (fun n => γ n s1) (γ 1 0) (fun n => hx n s1) s0
  have b := second_diff (fun n => γ 0 n) (γ 0 1) (fun n => hy 0 n) s1
  have c := second_diff (fun n => γ 1 n) (γ 0 1) (fun n => hy 1 n) s1
  simp only at a b c
  rw [a, b, c, h00]
  ring

/-- the statement of the paper without "even": the equation for all s and all t on an axis. -/
theorem axis_quad (γ : ℤ → ℤ → ℝ)
    (hx : ∀ s0 s1 t : ℤ, γ (s0 + t) s1 + γ (s0 - t) s1 = 2 * γ s0 s1 + 2 * γ t 0)
    (hy : ∀ s0 s1 t : ℤ, γ s0 (s1 + t) + γ s0 (s1 - t) = 2 * γ s0 s1 + 2 * γ 0 t) :
    ∃ q0 q1 c : ℝ, ∀ s0 s1 : ℤ, γ s0 s1 = q0 * s0 ^ 2 + q1 * s1 ^ 2 + c * s0 * s1 := by
  have h00 : γ 0 0 = 0 := by
    have := hx 0 0 0
    simp at this
    linarith
  exact ⟨γ 1 0, γ 0 1, γ 1 1 - γ 1 0 - γ 0 1,
    axis_quad_unit γ h00 (fun s0 s1 => hx s0 s1 1) (fun s0 s1 => hy s0 s1 1)⟩

/-- evenness is a consequence, not a hypothesis -/
theorem axis_even (γ : ℤ → ℤ → ℝ)
    (hx : ∀ s0 s1 t : ℤ, γ (s0 + t) s1 + γ (s0 - t) s1 = 2 * γ s0 s1 + 2 * γ t 0)
    (hy : ∀ s0 s1 t : ℤ, γ s0 (s1 + t) + γ s0 (s1 - t) = 2 * γ s0 s1 + 2 * γ 0 t) :
    ∀ s0 s1 : ℤ, γ (-s0) (-s1) = γ s0 s1 := by
  obtain ⟨q0, q1, c, h⟩ := axis_quad γ hx hy
  intro s0 s1
  rw [h, h]
  push_cast
  ring

/-- The form in which thm:fgadj has the two families:
    (A) all s, t on the second axis;  (B) s on the first axis, all t.
    Evenness follows from (B) at s = 0, and then (B) is the equation for a step on the first axis. -/
theorem axis_quad_AB (γ : ℤ → ℤ → ℝ)
    (hA : ∀ s0 s1 t : ℤ, γ s0 (s1 + t) + γ s0 (s1 - t) = 2 * γ s0 s1 + 2 * γ 0 t)
    (hB : ∀ s t0 t1 : ℤ, γ (s + t0) t1 + γ (s - t0) (-t1) = 2 * γ s 0 + 2 * γ t0 t1) :
    ∃ q0 q1 c : ℝ, ∀ s0 s1 : ℤ, γ s0 s1 = q0 * s0 ^ 2 + q1 * s1 ^ 2 + c * s0 * s1 := by
  have h00 : γ 0 0 = 0 := by
    have := hB 0 0 0
    simp at this
    linarith
  have ev : ∀ a b : ℤ, γ (-a) (-b) = γ a b := by
    intro a b
    have := hB 0 a b
    simp only [zero_add, zero_sub, h00] at this
    linarith
  apply axis_quad γ _ hA
  intro s0 s1 t
  have := hB t s0 s1
  have e := ev (t - s0) (-s1)
  simp only [neg_sub, neg_neg] at e
  rw [← e] at this
  rw [add_comm t s0] at this
  linarith

#print axioms second_diff
#print axioms axis_quad_unit
#print axioms axis_quad
#print axioms axis_even
#print axioms axis_quad_AB
