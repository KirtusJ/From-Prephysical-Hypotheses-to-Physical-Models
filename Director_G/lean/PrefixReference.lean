import Std

/-! Integer numerator convention for the coherent strict-threshold prefix circuit. -/

namespace PrefixReference

/-- An offshoot with r unused address bits represents 2^r equally weighted
addresses. At even r the common numerator is 2^(r/2). -/
theorem evenTail (k : Nat) :
    ((2 : Nat)^k) * (2^k) = 2^(2*k) := by
  rw [← Nat.pow_add]
  congr 1
  omega

/-- At odd r the offshoot can be split once more with a balanced Hadamard.
Its two children have equal integer numerator in the same whole-flight scale. -/
theorem oddTail (k : Nat) :
    ((2 : Nat)^k) * (2^k) + (2^k) * (2^k) = 2^(2*k+1) := by
  rw [evenTail, Nat.pow_succ]
  omega

/-- Read MSB first. At depth one, the first-difference leaf contains precisely
all suffixes when that threshold bit is 1. The equal prefix continues. The
empty remaining word is equality, and strict comparison makes it unmarked. -/
def acceptedPrefixes : List Bool → Nat
  | [] => 0
  | bit :: suffix => (if bit then 2^suffix.length else 0) + acceptedPrefixes suffix

def wordValue (bits : List Bool) : Nat :=
  bits.foldl (fun n b => 2*n + (if b then 1 else 0)) 0

private theorem foldFrom (bits : List Bool) (start : Nat) :
    bits.foldl (fun n b => 2*n + (if b then 1 else 0)) start =
      start * 2^bits.length + acceptedPrefixes bits := by
  induction bits generalizing start with
  | nil => simp [acceptedPrefixes]
  | cons bit suffix ih =>
    rw [List.foldl_cons, ih]
    cases bit <;> simp [acceptedPrefixes, Nat.pow_succ, Nat.add_mul, Nat.mul_comm,
      Nat.mul_left_comm, Nat.mul_assoc, Nat.add_assoc]

/-- For every threshold word the recursive sum of accepted address counts is
its usual binary value; equality's separate tie leaf contributes zero. -/
theorem strictThreshold (bits : List Bool) : acceptedPrefixes bits = wordValue bits := by
  unfold wordValue
  rw [foldFrom]
  simp

end PrefixReference
