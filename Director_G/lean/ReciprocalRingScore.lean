import Std

namespace ReciprocalRingScore

/-- The two parents of a well. Exactly the seam parent crosses the fixed edge. -/
def rails : Nat → Nat → Bool → Int × Int
  | 0, x, sheet => if x == 0 && !sheet then (1, 0) else (0, 0)
  | t+1, x, sheet =>
    let left := rails t ((x+5)%6) (if x == 0 then !sheet else sheet)
    let right := rails t ((x+1)%6) (if x == 5 then !sheet else sheet)
    (left.1 + left.2, right.1 - right.2)

theorem full_terminal :
    (List.range 12).map (fun j => rails 11 (j%6) (decide (6 ≤ j))) =
    [(0,0),(12,3),(0,0),(-15,0),(0,0),(2,26),
     (0,0),(24,0),(0,0),(18,3),(0,0),(-9,0)] := by native_decide

-- Integer certificates for the two strict inequalities in the fair-path check.
example : 576^2 * 81 > 225^3 ∧ 463 * 225 > 3 * 81 * 341 := by decide

end ReciprocalRingScore
