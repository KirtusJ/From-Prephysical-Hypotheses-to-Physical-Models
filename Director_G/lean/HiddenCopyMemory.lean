import Std

/- Exact zero-field segment weights. Four switches share denominator 4^4.
   The general numerator identity uses 4(d+1)(d+2) after division by a_d. -/
namespace HiddenCopyMemory

def choose : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _+1 => 0
  | n+1, k+1 => choose n k + choose n (k+1)

def central (n : Nat) : Nat := choose (2 * n) n

def segmentWeight (word : List Bool) (run : Nat := 1) : Nat :=
  match word with
  | [] => central run
  | false :: rest => segmentWeight rest (run + 1)
  | true :: rest => central run * segmentWeight rest 1

theorem noMiddleNumerator (d : Nat) :
    (2*d+1)*(2*d+3) + (d+1)*(d+2) =
      2*((2*d+1)*(d+2)) + (d*d+d+1) := by
  simp only [Nat.two_mul, Nat.mul_add, Nat.add_mul, Nat.one_mul, Nat.mul_one]
  omega

theorem numeratorPositive (d : Nat) : 0 < d*d+d+1 := by omega

/-- Endpoint mixed difference, middle bit zero, in units of 1/256. -/
theorem fourPassMiddleZero :
    segmentWeight [false,false,false] + segmentWeight [true,false,true] =
      segmentWeight [false,false,true] + segmentWeight [true,false,false] + 14 := by decide

/-- Endpoint mixed difference, middle bit one, in the same units. -/
theorem fourPassMiddleOne :
    segmentWeight [false,true,false] + segmentWeight [true,true,true] =
      segmentWeight [false,true,true] + segmentWeight [true,true,false] + 4 := by decide

end HiddenCopyMemory
