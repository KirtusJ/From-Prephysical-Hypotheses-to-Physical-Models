import Std

namespace PairedSiteContrast

private theorem squareNonneg (a : Int) : 0 ≤ a*a := by
  by_cases h : 0 ≤ a
  · exact Int.mul_nonneg h h
  · have hn : a ≤ 0 := by omega
    exact Int.mul_nonneg_of_nonpos_of_nonpos hn hn

/-- Four ordered product numerators from two spectator rates. -/
theorem pairDifference (a b : Int) :
    a*a - a*b - b*a + b*b = (a-b)*(a-b) := by
  simp only [Int.sub_mul, Int.mul_sub]
  omega

/-- Clearing positive rational denominators and repeating types according to
their integer weights leaves a sum of squares. Each listed contrast vanishes. -/
theorem zeroSum (xs : List Int)
    (h : (xs.map (fun x => x*x)).sum = 0) :
    ∀ x ∈ xs, x = 0 := by
  have nonnegative (ys : List Int) : 0 ≤ (ys.map (fun x => x*x)).sum := by
    induction ys with
    | nil => decide
    | cons y rest ih =>
      simp only [List.map_cons, List.sum_cons]
      exact Int.add_nonneg (squareNonneg _) ih
  induction xs with
  | nil => simp
  | cons a rest ih =>
    simp only [List.map_cons, List.sum_cons] at h
    have ha := squareNonneg a
    have hs := nonnegative rest
    have hz : a*a = 0 := by omega
    have hrest : (rest.map (fun x => x*x)).sum = 0 := by omega
    intro x hx
    rcases List.mem_cons.mp hx with e | tail
    · subst x
      rcases Int.mul_eq_zero.mp hz with h | h <;> exact h
    · exact ih hrest x tail

end PairedSiteContrast
