import Std

/-! Finite word coefficients and autocorrelations used for the two-well
    witness. The measure and physical interpretation are in the paper. -/
namespace TwoWellWitness

structure End where
  site : Nat
  left : Bool
  power : Nat
  sign : Int

def move (s : End) (left : Bool) : End :=
  ⟨(s.site+1) % 2, left, s.power+left.toNat,
   if s.left && left then -s.sign else s.sign⟩

def words : Nat → List End
  | 0 => [⟨0,false,0,1⟩]
  | n+1 => (words n).flatMap fun s => [move s false, move s true]

def right (n : Nat) : List End :=
  (words n).filter fun s => s.site == n%2 && !s.left

def coeff (n power : Nat) : Int :=
  ((right n).filter fun s => s.power == power).foldl (fun a s => a+s.sign) 0

/-- Sum once for each pair ordered by positive exponent lag. -/
def lag (n d : Nat) : Int :=
  (List.range (n+1)).foldl (fun a h => a + coeff n h * coeff n (h+d)) 0

theorem rightCounts : (right 2).length = 2 ∧ (right 3).length = 4 := by decide
theorem rightTwo : (List.range 3).map (coeff 2) = [1,1,0] := by decide
theorem rightThree : (List.range 4).map (coeff 3) = [1,2,-1,0] := by decide
theorem twoLags : (List.range 3).map (lag 2) = [2,1,0] := by decide
theorem threeLags : (List.range 4).map (lag 3) = [6,0,-1,0] := by decide

end TwoWellWitness
