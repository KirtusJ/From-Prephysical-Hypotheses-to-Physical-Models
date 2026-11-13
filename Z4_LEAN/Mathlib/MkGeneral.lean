import Mathlib

/-!
# The law (M k) implies the parallelogram law, for every k ≥ 1

(M k):  ∀ a b, k * f (a - b) + f (a + k • b) = (k + 1) * f a + k * (k + 1) * f b.

Key observation: three instances of (M k), at `(a, b)`, `(a + b, b)` and `(a + k • b, -b)`,
combine with weights `k + 1`, `-k`, `1` to give
`k (k + 1) (f (a + b) + f (a - b)) = k (k + 1) (2 f a + f b + f (-b))`.
Evenness is then derived from (M k) itself.
-/

namespace FPHPM.Mk

variable {G : Type*} [AddCommGroup G]

/-- The law (M k). -/
def M (k : ℕ) (f : G → ℝ) : Prop :=
  ∀ a b : G, (k : ℝ) * f (a - b) + f (a + k • b) = (k + 1) * f a + k * (k + 1) * f b

/-- Without evenness: (M k) gives a "pre-parallelogram" law. -/
theorem pre_parallelogram {k : ℕ} (hk : 1 ≤ k) {f : G → ℝ} (h : M k f) (a b : G) :
    f (a + b) + f (a - b) = 2 * f a + f b + f (-b) := by
  have E1 := h a b
  have E2 := h (a + b) b
  have E3 := h (a + k • b) (-b)
  have e1 : a + b - b = a := by abel
  have e2 : a + b + k • b = a + k • b + b := by abel
  have e3 : a + k • b - -b = a + k • b + b := by abel
  have e4 : a + k • b + k • (-b) = a := by rw [smul_neg]; abel
  rw [e1, e2] at E2
  rw [e3, e4] at E3
  have key : (k : ℝ) * (k + 1) * (f (a + b) + f (a - b) - (2 * f a + f b + f (-b))) = 0 := by
    linear_combination ((k : ℝ) + 1) * E1 + E3 - (k : ℝ) * E2
  have hne : (k : ℝ) * (k + 1) ≠ 0 := by positivity
  have := (mul_eq_zero.mp key).resolve_left hne
  linarith

/-- (M k) with evenness as a hypothesis implies the parallelogram law. -/
theorem parallelogram_of_M_of_even {k : ℕ} (hk : 1 ≤ k) {f : G → ℝ} (h : M k f)
    (heven : ∀ x, f (-x) = f x) (a b : G) :
    f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  have := pre_parallelogram hk h a b
  rw [heven b] at this
  linarith

/-- Evenness follows from (M k) for `k ≥ 1`. -/
theorem even_of_M {k : ℕ} (hk : 1 ≤ k) {f : G → ℝ} (h : M k f) (x : G) : f (-x) = f x := by
  -- odd part `o x = f x - f (-x)` is additive
  have hsub : ∀ a b : G, (f (a - b) - f (-(a - b))) = (f a - f (-a)) - (f b - f (-b)) := by
    intro a b
    have p1 := pre_parallelogram hk h a b
    have p2 := pre_parallelogram hk h b a
    have e1 : b + a = a + b := by abel
    have e2 : b - a = -(a - b) := by abel
    rw [e1, e2] at p2
    linarith
  have h0 : f 0 - f (-0) = 0 := by simp
  have hadd : ∀ a b : G, (f (a + b) - f (-(a + b))) = (f a - f (-a)) + (f b - f (-b)) := by
    intro a b
    have := hsub a (-b)
    rw [sub_neg_eq_add, neg_neg] at this
    linarith
  have hsmul : ∀ (n : ℕ) (b : G), f (n • b) - f (-(n • b)) = n * (f b - f (-b)) := by
    intro n b
    induction n with
    | zero => simp
    | succ n ih =>
      rw [succ_nsmul, hadd, ih]; push_cast; ring
  have E1 := h x x
  have E2 := h (-x) (-x)
  have e1 : -x - -x = x - x := by abel
  have e2 : -x + k • (-x) = -(x + k • x) := by rw [smul_neg]; abel
  rw [e1, e2] at E2
  have A := hadd x (k • x)
  have S := hsmul k x
  have hK : (0 : ℝ) < k := by exact_mod_cast hk
  have key : (k : ℝ) * (k + 1) * (f x - f (-x)) = 0 := by
    linear_combination E2 - E1 + A + S
  have hne : (k : ℝ) * (k + 1) ≠ 0 := by positivity
  have := (mul_eq_zero.mp key).resolve_left hne
  linarith

/-- **Main theorem.** For every `k ≥ 1`, (M k) implies the parallelogram law
(no evenness hypothesis needed). -/
theorem parallelogram_of_M {k : ℕ} (hk : 1 ≤ k) {f : G → ℝ}
    (h : ∀ a b : G, (k : ℝ) * f (a - b) + f (a + k • b) = (k + 1) * f a + k * (k + 1) * f b) :
    ∀ a b : G, f (a + b) + f (a - b) = 2 * f a + 2 * f b :=
  fun a b => parallelogram_of_M_of_even hk h (even_of_M hk h) a b

end FPHPM.Mk

#print axioms FPHPM.Mk.parallelogram_of_M_of_even
#print axioms FPHPM.Mk.even_of_M
#print axioms FPHPM.Mk.parallelogram_of_M
