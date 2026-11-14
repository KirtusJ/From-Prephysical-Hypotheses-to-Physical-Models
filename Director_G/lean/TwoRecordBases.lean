import Std

namespace TwoRecordBases

abbrev Amplitude := Nat → Bool → Bool → Int

def start : Amplitude := fun x rail flag =>
  if x == 0 && !rail && !flag then 1 else 0

/-- For a fixed outgoing rail the preceding site is unique. -/
def step (s : Amplitude) : Amplitude := fun x left b =>
  let prior := (x + (if left then 1 else 7)) % 8
  let rightIn := s prior false b
  let leftIn := s prior true b
  if left then rightIn - leftIn else rightIn + leftIn

def copyAtOne (s : Amplitude) : Amplitude := fun x r b =>
  s x r (xor b (x == 1))

def unanalysed : Amplitude := step (step (copyAtOne (step start)))

def finalState (h : Bool) : Amplitude := fun x r b =>
  if h then unanalysed x r false +
              (if b then -unanalysed x r true else unanalysed x r true)
  else unanalysed x r b

def weights (h b : Bool) : List Nat :=
  [1,3,5,7].map (fun (x : Nat) =>
    ((finalState h x false b)^2 + (finalState h x true b)^2).toNat)

theorem fourPointerRows :
    weights false false = [1,0,1,2] ∧ weights false true = [2,1,0,1] ∧
    weights true false = [5,1,1,1] ∧ weights true true = [1,1,1,5] := by decide

end TwoRecordBases
