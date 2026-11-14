import Std

namespace CrossedCoinPairs

/-- A table with one diagonal entry and an off-diagonal sum per row. -/
theorem splitRows (rows : List (Int × Int)) :
    (rows.map (fun p => p.1 + p.2)).sum =
    (rows.map Prod.fst).sum + (rows.map Prod.snd).sum := by
  induction rows with
  | nil => rfl
  | cons row rest ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [ih]
    omega

/-- A and B are marginal sums, d is the diagonal marginal-product sum,
    and c is the off-diagonal connected sum. O is the unnormalized
    crossed moment. Rational inputs are represented in common units. -/
theorem excludePartner (n A B d c O : Int) (h : O = A * B - d + c) :
    n * O - (n - 1) * (A * B) = n * c - (n * d - A * B) := by
  rw [h]
  simp only [Int.mul_add, Int.mul_sub, Int.sub_mul, Int.one_mul]
  omega

end CrossedCoinPairs
