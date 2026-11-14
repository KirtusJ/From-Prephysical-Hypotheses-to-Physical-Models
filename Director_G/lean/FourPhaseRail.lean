import Std

/-! Discounting of local four-setting defects on a finite doubling orbit.
    E and D are signed errors in common integer units, D at double scale. -/
namespace FourPhaseRail

def tailWeight (d : Nat → Int) (start : Nat) : Nat → Int
  | 0 => 0
  | k+1 => (2:Int)^k * d start + tailWeight d (start+1) k

theorem chain (e d : Nat → Int) (rec : ∀ n, 2 * e n = e (n+1) + d n)
    (k start : Nat) :
    (2:Int)^k * e start = e (start+k) + tailWeight d start k := by
  induction k generalizing start with
  | zero => simp [tailWeight]
  | succ k ih =>
    calc
      (2:Int)^(k+1) * e start = (2:Int)^k * (2 * e start) := by
        rw [Int.pow_succ, Int.mul_assoc]
      _ = (2:Int)^k * (e (start+1) + d start) := by rw [rec]
      _ = e (start+(k+1)) + tailWeight d start (k+1) := by
        rw [Int.mul_add, ih (start+1)]
        simp only [tailWeight]
        rw [show start+1+k = start+(k+1) by omega]
        omega

end FourPhaseRail
