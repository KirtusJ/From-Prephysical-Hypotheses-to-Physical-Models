import Std

namespace TwoTickInstrument

/-- Eight wells, False for R and True for L. An outward proposal stays and flips its rail. -/
abbrev Port := Nat × Bool

def advance (x : Nat) (left : Bool) : Port :=
  if left then
    if x = 0 then (0, false) else (x-1, true)
  else
    if x = 7 then (7, true) else (x+1, false)

def choices := [false, true]

def amplitude (out : Port) : List Bool → Port → Int
  | [], atPort => if out = atPort then 1 else 0
  | direction :: rest, atPort =>
    let sign : Int := if atPort.2 && direction then -1 else 1
    sign * amplitude out rest (advance atPort.1 direction)

/-- Sum all four signed direction words before testing whether a port is occupied. -/
def twice (home : Nat) (out : Port) : Int :=
  (choices.flatMap fun a => choices.map fun b => amplitude out [a,b] (home,false)).sum

def jointlyLit (a b : Port) : Bool :=
  (List.range 8).any fun home => decide (twice home a ≠ 0 ∧ twice home b ≠ 0)

theorem same_well_rail_edges :
    (List.range 8).all (fun x => jointlyLit (x,false) (x,true)) = true := by native_decide

/-- Stride two joins like-parity wells within each of the two halves. -/
theorem stride_edges :
    [0,1,4,5].all (fun x => jointlyLit (x,false) (x+2,false)) = true := by native_decide

/-- An additional edge in each half joins its two parity chains. -/
theorem wall_edges :
    jointlyLit (0,false) (1,false) && jointlyLit (6,true) (7,true) = true := by native_decide

def centralWeight (home : Nat) (usePhase : Bool) : Int :=
  ([2,3,4,5].flatMap fun x => choices.map fun rail =>
    let a := twice home (x,rail)
    let phase : Int := if usePhase && x % 2 = 1 then -1 else 1
    phase * a*a).sum

/-- Every central-bin echo squared norm is invariant under a sign on the odd wells.
    Different launches can acquire different return-amplitude signs. -/
theorem parity_phase_passes_every_probe :
    (List.range 8).all (fun home =>
      decide (centralWeight home true ^ 2 = centralWeight home false ^ 2)) = true := by
  native_decide

theorem central_bin_probe_masses :
    (List.range 8).map (fun home => centralWeight home false) = [1,1,3,3,3,3,1,1] := by
  native_decide

end TwoTickInstrument
