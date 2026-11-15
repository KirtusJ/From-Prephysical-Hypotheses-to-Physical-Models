import Std

namespace TagEchoResistance

abbrev Pair := Int × Int

def flight : Nat → Nat → Pair
  | 0, x => if x = 0 then (1, 0) else (0, 0)
  | t+1, x =>
    let (r,l) := flight t (x-1)
    let (a,b) := flight t (min (x+1) 5)
    (if x = 0 then r-l else r+l, if x = 5 then a+b else a-b)

def squares (t : Nat) : List Pair :=
  (List.range 6).map fun x =>
    let (r,l) := flight t x
    (r*r, l*l)

def leftReturn (t : Nat) (minusAtOrigin : Bool) : Int :=
  ((List.range 3).map fun x =>
    let (r,l) := flight t x
    (if x = 0 && minusAtOrigin then -(r*r) else r*r) + l*l).sum

theorem six_support : squares 6 =
    [(4,4),(4,1),(4,9),(9,1),(25,1),(1,1)] := by native_decide

theorem eleven_support : squares 11 =
    [(0,81),(144,9),(9,324),(225,0),(0,576),(4,676)] := by native_decide

theorem minus_at_zero :
    [leftReturn 6 false, leftReturn 6 true, leftReturn 11 false, leftReturn 11 true] =
    [26,18,567,567] := by native_decide

end TagEchoResistance
