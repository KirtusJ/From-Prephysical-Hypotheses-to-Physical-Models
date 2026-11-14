import Std

namespace WalkBranchWeights

/-- Signed, unnormalized RL amplitudes on ten periodic wells. -/
def step (v : Nat → Int × Int) (x : Nat) : Int × Int :=
  let (a,b) := v ((x+9)%10)
  let (c,d) := v ((x+1)%10)
  (a+b,c-d)

def field : Nat → Nat → Int × Int
  | 0 => fun x => if x == 0 then (1,0) else (0,0)
  | n+1 => step (field n)

example : ([0,2,4,6,8].map (field 6)) =
    [(-2,-2),(2,3),(5,0),(2,-3),(1,2)] := by decide

example : (25^2 - 5*5^2 : Nat)*(1390-1052)*36557 = 4225*1052*1390 := by decide

end WalkBranchWeights
