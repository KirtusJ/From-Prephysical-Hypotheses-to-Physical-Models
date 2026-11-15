import Std

namespace ProtectedWordEcho

/-- Enumerate forward and inverse proposals in displacement coordinates relative to
    well 8. Six forward steps cannot reach a wall. A clean-return history consists
    of two forward paths with the same turnaround, so this forward enumeration
    suffices for all the certified clean statistics. -/
structure Path where
  site : Int
  left : Bool
  word : Nat
  sign : Int
  deriving DecidableEq, Repr

def advance (t : Nat) (p : Path) (left : Bool) : Path :=
  let x := if left then p.site-1 else p.site+1
  let hi := if t == 3 && decide (x ≤ -3) then 2 else 0
  let lo := if t == 6 && decide (4 ≤ x) then 1 else 0
  ⟨x, left, p.word + hi + lo, if p.left && left then -p.sign else p.sign⟩

def paths : Nat → List Path
  | 0 => [⟨0, false, 0, 1⟩]
  | t+1 => (paths t).flatMap fun p => [advance (t+1) p false, advance (t+1) p true]

def innerSum (word : Nat) (signed : Bool) : Int :=
  ((paths 6).map fun p =>
    ((paths 6).map fun q =>
      if p.word == word && q.word == word && p.site == q.site && p.left == q.left then
        (if signed then p.sign * q.sign else 1)
      else 0).sum).sum

theorem signed_returns :
    (List.range 4).map (fun w => innerSum w true) = [29,27,8,0] := by native_decide

theorem fair_returns :
    (List.range 4).map (fun w => innerSum w false) = [405,27,12,0] := by native_decide

theorem fair_score_sign_witness :
    12 * 729 > 27 * 64 ∧ 405 * 729 > 27 * 841 := by decide

end ProtectedWordEcho
