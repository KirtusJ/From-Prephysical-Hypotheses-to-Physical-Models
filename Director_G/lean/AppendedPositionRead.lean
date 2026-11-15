import Std

namespace AppendedPositionRead

abbrev Mode := Int × Bool
abbrev Route := Mode × Int

def advance (length : Int) (path : Route) (left : Bool) : Route :=
  let (⟨x,r⟩, a) := path
  let y := if left then x-1 else x+1
  let arrival : Mode := if 0 ≤ y ∧ y < length then (y,left) else (x,!left)
  (arrival, if r && left then -a else a)

def paths (length : Int) (source : Mode) : Nat → List Route
  | 0 => [(source,1)]
  | n+1 => (paths length source n).flatMap fun p =>
    [advance length p false,advance length p true]

def fold (length j : Int) : Int :=
  let k := j % (2*length)
  min k (2*length-1-k)

def signed (out : List Route) (p : Mode) : Int :=
  ((out.filter fun route => route.1 == p).map Prod.snd).sum

def read (length x : Int) (left : Bool) : List (Int × Nat) :=
  let out := paths length (x,left) 4
  ([-4,-2,0,2,4] : List Int).map fun offset =>
    let y := fold length (if left then x-offset else x+offset)
    (signed out (y,false)^2 + signed out (y,true)^2,
     (out.filter fun route => route.1.1 == y).length)

def expected : List (Int × Nat) := [(1,1),(2,4),(2,6),(10,4),(1,1)]

theorem all_starts_five_six_seven :
    [5,6,7].all (fun n =>
    (List.range n).all (fun x => [false,true].all (fun left =>
     read n x left == expected))) = true := by native_decide

theorem hidden_rail_mix :
    (9*88 + 11*81*8 : Nat) * 16 = 9 * (20*8*88) ∧
    (9*10 + 11*2 : Nat) * 25 = 7 * (20*2*10) := by decide

end AppendedPositionRead
