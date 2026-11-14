import Std

namespace TwoWalkMemory

/-- Word digits are true for a left proposal. -/
def paths : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => (paths n).flatMap fun w => [false :: w, true :: w]

def walk (x : Int) (rail : Bool) (sign : Int) : List Bool → (Int × Bool) × Int
  | [] => ((x, rail), sign)
  | next :: rest =>
    walk (if next then x-1 else x+1) next (if next && rail then -sign else sign) rest

def amplitude (t : Nat) (source : Bool) (x : Int) (rail : Bool) : Int :=
  ((paths t).map fun w =>
    let out := walk (if source then -1 else 1) source 1 w
    if out.1 == (x, rail) then out.2 else 0).sum

def gram (t : Nat) (a b : Bool) (x : Int) : Int :=
  ([false,true].map fun rail => amplitude t a x rail * amplitude t b x rail).sum

def sites : List Int := [-3,-1,1,3]

theorem site_effects :
    sites.map (fun x => (gram 2 false false x, gram 2 false true x, gram 2 true true x)) =
      [(0,0,1), (1,-1,2), (2,1,1), (1,0,0)] := by decide

theorem earlier_cross_terms :
    ([-1,1] : List Int).all (fun x => gram 0 false true x == 0) ∧
    ([-2,0,2] : List Int).all (fun x => gram 1 false true x == 0) := by decide

def opens (a b : Bool) : Bool :=
  (((if a then 0 else 1) + (if b then 0 else 1) + 4) % 5 : Nat) == 0

def jointAmp (x : Int) (r : Bool) (y : Int) (s : Bool) : Int :=
  ([false,true].flatMap fun a => [false,true].map fun b =>
    if opens a b then amplitude 2 a x r * amplitude 2 b y s else 0).sum

def sign (x : Int) : Int := if x == -3 || x == 1 then 1 else -1

def jointSum (signed : Bool) : Int :=
  (sites.flatMap fun x => sites.flatMap fun y =>
    [false,true].flatMap fun r => [false,true].map fun s =>
      let weight := (jointAmp x r y s)^2
      if signed then sign x * sign y * weight else weight).sum

/-- Six Hadamards for the two walkers give denominator 64. -/
theorem delayed_coherent_totals : jointSum false = 32 ∧ jointSum true = 8 := by
  native_decide

theorem direct_odd_herald :
    ([false,true].flatMap fun a => [false,true].filterMap fun b =>
      if opens a b then some (a,b) else none) = [(false,true),(true,false)] := by decide

end TwoWalkMemory
