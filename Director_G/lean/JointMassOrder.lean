import Std

namespace JointMassOrder

/-- The first Walsh output sums the signs after the address-controlled plate. -/
def marker (k : Nat) : Int :=
  ((List.range 8).map (fun y => if y < 4+k then (1:Int) else -1)).sum

theorem four_markers : [marker 1,marker 2,marker 3,marker 4] = [2,4,6,8] := by
  native_decide

/-- Compare products with their common denominators cleared. The candidate
    vectors have integer coordinates [5,3] and [3,1], respectively. -/
def rows (h : List Nat) (r : List Nat) :=
  h.flatMap (fun v => r.map (fun w => v*w))

def comparisons (xs : List Nat) :=
  xs.flatMap (fun x => xs.map (fun y => compare x y))

theorem same_five_tick_order :
    comparisons (rows [5,3] [0,1,4,16]) =
    comparisons (rows [3,1] [0,1,4,16]) := by native_decide

theorem four_address_inequalities :
    5 * 2^2 < 3 * 3^2 ∧ 3 * 2^2 > 1 * 3^2 := by decide

end JointMassOrder
