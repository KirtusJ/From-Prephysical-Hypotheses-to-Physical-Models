import Std

/-! Counts of paths in the three-tick, four-well read. The coherent score
    uses the cubic relation 1 + ω + ω² = 0 and the stipulated squared law. -/
namespace ThreeTickRing

structure Port where
  site : Nat
  left : Bool
  gain : Nat
  negative : Bool

def move (s : Port) (l : Bool) : Port :=
  ⟨(s.site + if l then 3 else 1) % 4, l,
   (s.gain + l.toNat) % 3, xor s.negative (s.left && l)⟩

def histories : Nat → List Port
  | 0 => [⟨0, false, 0, false⟩]
  | n+1 => (histories n).flatMap (fun s => [move s false, move s true])

def scores (n site : Nat) : Int × Int × Int :=
  let accepted := (histories n).filter (fun s => s.site == site && !s.left)
  let signed := fun j => (accepted.filter (fun s => s.gain == j)).foldl
    (fun (z : Int) s => if s.negative then z-1 else z+1) 0
  let a := signed 0
  let b := signed 1
  let c := signed 2
  ((a+b+c)^2, a^2+b^2+c^2-a*b-b*c-c*a, Int.ofNat accepted.length)

theorem tickThree : scores 3 1 = (4,4,2) ∧ scores 3 3 = (0,3,2) := by decide

/-- Rational mixture weights represented in common integer mass units.
    A total unit count and two numerator tallies determine all three weights. -/
theorem uniqueWeights (a b c d e f : Int)
    (total : a+b+c = d+e+f)
    (siteOne : 4*a+4*b+2*c = 4*d+4*e+2*f)
    (siteThree : 3*b+2*c = 3*e+2*f) : a = d ∧ b = e ∧ c = f := by
  omega

/-- On an odd N-cycle the two lift representatives of one site have opposite
    parity. Exactly one agrees with a given tick in a sharp launch from zero. -/
theorem oddLiftParity (n x t : Nat) (odd : n % 2 = 1) :
    ((x+n) % 2 = t % 2) ↔ x % 2 ≠ t % 2 := by
  omega

/-- In a path of length span+1 ending in R, two left-step counts separated by
    span must be the zero and span extremes. -/
theorem firstSpanRight (lo hi span : Nat) (lastR : hi ≤ span)
    (gap : hi = lo+span) : lo = 0 ∧ hi = span := by
  omega

/-- An L-ending path has at least one left step, shifting both extremes by one. -/
theorem firstSpanLeft (lo hi span : Nat) (lastL : 1 ≤ lo) (bound : hi ≤ span+1)
    (gap : hi = lo+span) : lo = 1 ∧ hi = span+1 := by
  omega

end ThreeTickRing
