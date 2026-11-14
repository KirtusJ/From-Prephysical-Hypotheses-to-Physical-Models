import Std

namespace TwoTerminalClocks

/-- At a fixed tick a well on the odd ring has at most one occupied sheet
    from a sharp source. Compute the two bare rail amplitudes there. -/
def rails : Nat → Nat → Int × Int
  | 0, x => if x == 0 then (1, 0) else (0, 0)
  | t+1, x =>
    let left := rails t ((x+6)%7)
    let right := rails t ((x+1)%7)
    (left.1 + left.2, right.1 - right.2)

theorem ten : (List.range 7).map (rails 10) =
    [(6,6),(14,-7),(-6,-8),(1,8),(0,7),(-4,-6),(21,0)] := by native_decide

theorem twelve : (List.range 7).map (rails 12) =
    [(-10,10),(42,14),(14,-7),(0,7),(-21,-14),(11,-10),(28,0)] := by native_decide

def halfTen : List Nat := [882,882,490,490,200,200,144,144,130,130,104,104,98,98]
def splitTwelve : List Nat := [1764,784,441,196,196,196,121,100,100,100,49,49]

theorem prefix_bounds :
    (List.range 15).all (fun k => (halfTen.take k).sum ≤ (splitTwelve.take k).sum) = true ∧
    halfTen.sum = splitTwelve.sum := by native_decide

end TwoTerminalClocks
