import Std

namespace ReflectingPath

/-- Unnormalized integer propagation on wells 0 through n-1.
    At an endpoint the outward component stays at the well and reverses rail.
    With signs off, the two components count all direction words. -/
def rails (n : Nat) (signed : Bool) : Nat → Nat → Int × Int
  | 0, x => if x = 0 then (1, 0) else (0, 0)
  | t+1, x =>
    let left := rails n signed t (x-1)
    let right := rails n signed t (min (x+1) (n-1))
    let rOut (p : Int × Int) := p.1 + p.2
    let lOut (p : Int × Int) := if signed then p.1 - p.2 else p.1 + p.2
    (if x = 0 then lOut left else rOut left,
     if x+1 = n then rOut right else lOut right)

def rows (n t : Nat) (signed : Bool) : List (Int × Int) :=
  (List.range n).map (rails n signed t)

theorem six_signed :
    rows 6 11 true = [(0,9),(12,3),(3,-18),(-15,0),(0,-24),(2,26)] := by native_decide

theorem six_fair_counts :
    (rows 6 11 false).map (fun p => p.1 + p.2) = [463,463,341,341,220,220] := by
  native_decide

theorem three_wells_four_ticks :
    rows 3 4 true = [(-1,1),(1,0),(3,2)] ∧
    (rows 3 4 false).map (fun p => p.1 + p.2) = [6,5,5] := by native_decide

end ReflectingPath
