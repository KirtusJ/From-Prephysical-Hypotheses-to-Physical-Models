import Std

namespace EqualLabelSource

/-- Enumerate binary words as numbers and count the ones in the n input bits. -/
def layer (n k : Nat) : List Nat :=
  (List.range (2^n)).filter fun w =>
    ((List.range n).filter fun j => w.testBit j).length == k

def kept (n labels : Nat) : Nat :=
  ((List.range (n+1)).map fun k => labels * ((layer n k).length / labels)).sum

theorem firstEight : (List.range 6).map (fun n => kept n 8) = [0,0,0,0,0,16] := by
  decide

theorem fiveLayers : (List.range 6).map (fun k => (layer 5 k).length) = [1,5,10,10,5,1] := by
  decide

end EqualLabelSource
