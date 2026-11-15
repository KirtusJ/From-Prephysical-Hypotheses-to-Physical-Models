import Std

namespace ActualPrefixMemory

abbrev Port := Nat × Bool

def step (p : Port) (left : Bool) : Port :=
  if left then
    if p.1 == 0 then (0,false) else (p.1-1,true)
  else
    if p.1 == 3 then (3,true) else (p.1+1,false)

def words : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => [false,true].flatMap fun d => (words n).map (fun w => d::w)

structure Flight where
  port : Port
  weight : Int
  bit : Bool
  trace : Nat

def evolve (defect : Bool) (word : List Bool) : Flight := Id.run do
  let mut n := 0
  let mut state : Flight := ⟨(1,false),1,false,0⟩
  for left in word do
    n := n+1
    let p := step state.port left
    let read := n == 2 || n == 4 || n == 8
    let high := 2 ≤ p.1
    let activated := defect && n == 4 && state.bit && p == (2,true)
    let coinMinus := state.port.2 && left
    state := ⟨p, if activated != coinMinus then -state.weight else state.weight,
      if n == 2 then decide high else state.bit,
      if read then 2*state.trace+(if high then 1 else 0) else state.trace⟩
  return state

def numerators (defect : Bool) : List Int :=
  let paths := (words 8).map (evolve defect)
  let ports := (List.range 4).flatMap fun x => [(x,false),(x,true)]
  (List.range 8).map fun w =>
    (ports.map fun p =>
      ((paths.map fun h => if h.port == p && h.trace == w then h.weight else 0).sum)^2).sum

theorem wrong_two_words :
    numerators false = [100,12,20,60,12,4,28,20] ∧
    numerators true = [100,12,20,60,12,4,12,36] := by native_decide

end ActualPrefixMemory
