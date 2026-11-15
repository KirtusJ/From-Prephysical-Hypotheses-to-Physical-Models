import Std

/-! Exact finite threshold inversion for signed weighted bin contrasts.
Integers may be numerators over an arbitrary common positive denominator.
`contrastAt` and `tail` both return zero beyond the last bin.
Checked with Lean 4.19.0 and its standard library. -/

namespace MarkedTail

def contrastAt : List Int → Nat → Int
  | [], _ => 0
  | r :: _, 0 => r
  | _ :: rs, k + 1 => contrastAt rs k

def tail (rs : List Int) (k : Nat) : Int := (rs.drop k).sum

theorem recover (rs : List Int) (k : Nat) :
    contrastAt rs k = tail rs k - tail rs (k + 1) := by
  induction rs generalizing k with
  | nil => simp [contrastAt, tail]
  | cons r rs ih =>
    cases k with
    | zero => simp [contrastAt, tail]
    | succ k => simpa [contrastAt, tail] using ih k

theorem all_zero_of_zero_tails (rs : List Int)
    (h : ∀ k, tail rs k = 0) : ∀ k, contrastAt rs k = 0 := by
  intro k
  simp [recover, h]

theorem error_bound (rs : List Int) (k : Nat) (e : Int)
    (left : -e ≤ tail rs k ∧ tail rs k ≤ e)
    (right : -e ≤ tail rs (k + 1) ∧ tail rs (k + 1) ≤ e) :
    -2 * e ≤ contrastAt rs k ∧ contrastAt rs k ≤ 2 * e := by
  rw [recover]
  omega

end MarkedTail
