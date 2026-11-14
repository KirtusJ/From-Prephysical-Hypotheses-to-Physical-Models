import Std

namespace ForwardCut

/-- Use all eight three-tick histories. Directions and ports use true for left. -/
abbrev Port := Nat × Bool
def move (x : Nat) (left : Bool) : Port :=
  if left then
    if x = 0 then (0,false) else (x-1,true)
  else
    if x = 7 then (7,true) else (x+1,false)

def stepSign (p : Port) (left : Bool) : Int := if p.2 && left then -1 else 1
def dirs := [false,true]

def paths (x : Nat) : List (Port × Port × Port × Int) :=
  dirs.flatMap fun a => dirs.flatMap fun b => dirs.map fun c =>
    let p := move x a
    let q := move p.1 b
    let t := move q.1 c
    (p,q,t,stepSign p b * stepSign q c)

def matching (x : Nat) (t : Port) := (paths x).filter fun h => h.2.2.1 == t

theorem dark_and_companion_paths :
    (List.range 8).all (fun x =>
      let d := move x true
      let hs := matching x d
      hs.length == 2 && (hs.map (·.2.2.2)).sum == 0 &&
      hs.any (fun h => h.1 == move x false) && hs.any (fun h => h.1 == move x true) &&
      hs.any (fun h => h.2.1 == (x,false)) && hs.any (fun h => h.2.1 == (x,true)) &&
      (matching x (d.1,!d.2)).length == 1) = true := by native_decide

def shortEnds (x : Nat) :=
  dirs.flatMap fun a => dirs.map fun b => move (move x a).1 b

theorem shorter_histories_end_at_distinct_ports :
    (List.range 8).all (fun x => decide ((shortEnds x).Nodup)) = true := by native_decide

end ForwardCut
