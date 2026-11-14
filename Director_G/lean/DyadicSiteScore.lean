import Std

namespace DyadicSiteScore

/-- Equal blank normalizers give an affine score on all but the fully
occupied site. The apparatus compares only indices below the label count. -/
theorem affineOnGrid (N : Nat) (f : Nat → Int)
    (paired : ∀ k, k + 1 < N → f (k+1) + f 0 = f k + f 1) :
    ∀ i, i < N → f i - f 0 = (i : Int) * (f 1 - f 0) := by
  intro i
  induction i with
  | zero => simp
  | succ k ih =>
    intro hk
    have prev := ih (by omega)
    have step := paired k hk
    change f (k+1) - f 0 = ((k : Int) + 1) * (f 1 - f 0)
    rw [Int.add_mul, Int.one_mul]
    omega

end DyadicSiteScore
