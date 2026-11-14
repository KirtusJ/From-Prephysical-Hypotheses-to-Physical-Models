import Std

/-! Exact, unnormalized, signed word counts at the two-well R port.
    start false = an incoming R, switch true = a gain on each outgoing L.
    Gain control, detector and measure assumptions are outside these counts. -/
namespace CommonClockWitness

structure Cell where
  left : Bool
  well : Bool
  gain : Nat
  sign : Int

def move (c : Cell) (on l : Bool) : Cell :=
  ⟨l, !c.well, c.gain + (on && l).toNat,
   if c.left && l then -c.sign else c.sign⟩

def words (switches : List Bool) (start : Bool := false) : List Cell :=
  switches.foldl (fun cells on =>
    cells.flatMap (fun c => [move c on false, move c on true])) [⟨start,false,0,1⟩]

def atR (s : List Bool) (j : Nat) : Int :=
  ((words s).filter (fun c => !c.left && (c.gain == j))).foldl (fun n c => n+c.sign) 0

def lags (s : List Bool) : List Int :=
  (List.range (s.length+1)).map fun d =>
    (List.range (s.length+1)).foldl (fun a h => a+(atR s h)*(atR s (h+d))) 0

theorem one (a : Bool) : lags [a] = [1,0] := by cases a <;> decide

theorem two (a b : Bool) : lags [a,b] = if a then [2,1,0] else [4,0,0] := by
  cases a <;> cases b <;> decide

theorem three (a b c : Bool) :
    lags [a,b,c] = if a && b then [6,0,-1,0] else [4,0,0,0] := by
  cases a <;> cases b <;> cases c <;> decide

theorem four :
    lags [false,false,false,false] = [16,0,0,0,0] ∧
    lags [true,false,false,false] = [8,4,0,0,0] ∧
    lags [false,false,true,false] = [8,4,0,0,0] ∧
    lags [true,false,true,false] = [8,0,4,0,0] := by decide

end CommonClockWitness
