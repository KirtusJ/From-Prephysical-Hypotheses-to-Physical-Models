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

/-- A history records its ports at clocks two, three and four, plus its sign. -/
def four (x : Nat) (r : Bool) : List (Port × Port × Port × Int) :=
  dirs.flatMap fun a => dirs.flatMap fun b => dirs.flatMap fun c => dirs.map fun d =>
    let p := move x a
    let q := move p.1 b
    let t := move q.1 c
    let f := move t.1 d
    (q,t,f,stepSign (x,r) a * stepSign p b * stepSign q c * stepSign t d)

def sampled (x : Nat) (r fin : Bool) (mid : Port × Port → Bool) : Int :=
  ((four x r).filter fun h => h.2.2.1 == (x,fin) && mid (h.1,h.2.1)).map (·.2.2.2) |>.sum

def coast (p : Port) := move p.1 p.2
def sgn (r : Bool) : Int := if r then -1 else 1

theorem four_tick_opposite_and_companion :
    (List.range 8).all (fun x => dirs.all fun r =>
      let y := move x r
      let v := move x (!r)
      let z := (coast y).1
      let w := (coast v).1
      (List.range 8).all fun j =>
        let atSite := fun (p : Port × Port) => p.1.1 == j
        sampled x r (!r) atSite == (if j == x then 2*sgn r else if j == z then -(sgn r) else 0) &&
        sampled x r r atSite == (if j == w then -1 else 0) &&
        dirs.all fun h =>
          let atPort := fun (p : Port × Port) => p.2 == (j,h)
          sampled x r (!r) atPort ==
            (if j != y.1 then 0 else if h == y.2 then 2*sgn r else -(sgn r)) &&
          sampled x r r atPort == (if j == v.1 && h != v.2 then -1 else 0)) = true := by
  native_decide

end ForwardCut
