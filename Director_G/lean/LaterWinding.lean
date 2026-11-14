import Std

namespace LaterWinding

/-- Two compatible prefixes separated by a left-count gap fit inside a
    prefix of length gap + slack only at these distances from its ends. -/
theorem prefixEnds (j gap slack : Nat) (h : j + gap ≤ gap + slack) :
    j ≤ slack ∧ gap + slack - (j + gap) = slack - j := by omega

theorem remainingSlack (k g d slack : Nat) (h : k ≤ g) :
    k*d + slack - g*d ≤ slack := by
  have hmul := Nat.mul_le_mul_right d h
  omega

/-- Line amplitudes by number of left steps, with the common factor
    2^(-t/2) suppressed. LL is the only negative coin entry. -/
def step (rails : List (Int × Int)) : List (Int × Int) :=
  List.zipWith (fun (same prev : Int × Int) =>
    (same.1 + same.2, prev.1 - prev.2)) (rails ++ [(0,0)]) ((0,0) :: rails)

def line : Nat → List (Int × Int)
  | 0 => [(1,0)]
  | n+1 => step (line n)

/-- At clock 144, a path with j left steps reaches x iff x + 2j = 144
    modulo 16. Fold the signed R amplitudes by the gain exponent j mod 21. -/
def rightPort (paths : List (Int × Int)) (x : Nat) : Array Int := Id.run do
  let mut a := Array.replicate 21 (0 : Int)
  for (rails, j) in paths.zipIdx do
    if (x + 2*j) % 16 == 144 % 16 then
      let i := j % 21
      a := a.set! i (a[i]! + rails.1)
  return a

def numerators : Int × Int := Id.run do
  let paths := line 144
  let mut diagonal := 0
  let mut cross := 0
  for x in [0,4,8,12] do
    let a := rightPort paths x
    for j in [:21] do
      diagonal := diagonal + a[j]! * a[j]!
      cross := cross + a[j]! * a[(j+17)%21]!
  return (diagonal + cross, diagonal - cross)

/-- Numerators in units of 2^-144. The paper cancels their common factor 16. -/
theorem tick144 : numerators =
    (16 * 598546492470538701899396757872292453252737,
     16 * 425943843822132599281979972562490031225077) := by native_decide

end LaterWinding
