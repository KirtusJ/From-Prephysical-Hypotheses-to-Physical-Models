import Std

/-! A list contains the herald flag from every independent fresh launch
up to a deadline, including misses. These lemmas are combinatorial. -/
namespace StoppedHeralds

def reached : Nat → List Bool → Bool
  | 0, _ => true
  | _ + 1, [] => false
  | k + 1, true :: rest => reached k rest
  | k + 1, false :: rest => reached (k+1) rest

/-- Reaching the kth flag by the last launch is exactly a threshold on its
ordinary count. This is valid for every list, irrespective of its law. -/
theorem reached_iff (k : Nat) (flags : List Bool) :
    reached k flags = true ↔ k ≤ flags.count true := by
  induction flags generalizing k with
  | nil => cases k <;> simp [reached]
  | cons flag rest ih =>
    cases k with
    | zero => simp [reached]
    | succ k => cases flag <;> simp [reached, ih, Nat.succ_le_succ_iff]

/-- For a Bernoulli probability a/(a+b), the numerator of the chance
of reaching the target within n launches, with denominator (a+b)^n.
A success contributes a and a miss contributes b at each branch. -/
def mass (a b : Nat) : Nat → Nat → Nat
  | 0, n => (a+b)^n
  | _+1, 0 => 0
  | k+1, n+1 => b*mass a b (k+1) n + a*mass a b k n

/-- At p = 10/109 and 5% risk, four launches are early enough for the
two-herald test; five are too late. At this p one launch already puts
the probability of a first herald over the risk threshold. -/
theorem worked_boundary :
    20 * mass 10 99 2 4 < 109^4 ∧ 109^5 < 20 * mass 10 99 2 5 ∧
    109 < 20 * mass 10 99 1 1 := by decide

end StoppedHeralds
