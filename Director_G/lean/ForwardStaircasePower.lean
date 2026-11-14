import Std

namespace ForwardStaircasePower

/-- Coordinates of the eight occupied rails ordered by site and then R, L. -/
def tick (odd flipped : Bool) (v : Fin 8 → Int) : Fin 8 → Int :=
  fun j =>
    let x := j.val / 2
    let p := if j.val % 2 = 0 then (x + (if odd then 3 else 0)) % 4
             else (x + (if odd then 0 else 1)) % 4
    let r := v ⟨2*p % 8, Nat.mod_lt _ (by decide)⟩
    let l := v ⟨(2*p+1) % 8, Nat.mod_lt _ (by decide)⟩
    let phase : Int := if flipped && p % 2 == 1 then -1 else 1
    phase * (if j.val % 2 = 0 then r+l else r-l)

def source : Fin 8 → Int := fun j => if j.val == 0 then 1 else 0

def run (word : List Bool) : Fin 8 → Int :=
  (word.foldl (fun (a : Bool × (Fin 8 → Int)) b =>
    (!a.1, tick a.1 b a.2)) (false,source)).2

def corners : List (Bool × Bool × Bool) :=
  [ (false,false,false), (false,false,true), (false,true,false), (false,true,true),
    (true,false,false), (true,false,true), (true,true,false), (true,true,true) ]

def matrixEntry (side : Bool) (i j : Fin 8) : Int :=
  (corners.map fun (a,b,c) =>
    if xor (xor a b) c == side then
      let s := run [false,false,false,false,a,true,b,c,c]
      s i * s j
    else 0).sum

theorem equalMatrices : ∀ i j : Fin 8, matrixEntry false i j = matrixEntry true i j := by
  native_decide

/-- Per-word site-one numerator and sum of all site squares on the integer scale. -/
def siteWeight (s : Fin 8 → Int) (x : Fin 4) : Int :=
  let r := s ⟨(2*x.val) % 8, Nat.mod_lt _ (by decide)⟩
  let l := s ⟨(2*x.val+1) % 8, Nat.mod_lt _ (by decide)⟩
  r*r + l*l

theorem siteOneProfile : ∀ a b c : Bool,
    let state := run [false,false,false,false,a,true,b,c,c]
    let odd := xor (xor a b) c
    siteWeight state 0 = (if odd then 128 else if a then 256 else 0) ∧
    ([0,1,2,3].map (fun (x : Fin 4) => (siteWeight state x)^2)).sum = 98304 := by
  native_decide

end ForwardStaircasePower
