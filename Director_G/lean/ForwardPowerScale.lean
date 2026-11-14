import Std

namespace ForwardPowerScale

/-- On the line each tick proposes one of the two directions. Negative coin
    signs occur only on consecutive left rails, including the launch rail. -/
abbrev Port := Int × Bool
def dirs : List Bool := [false, true]
def words : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => dirs.flatMap fun r => (words n).map (fun w => r :: w)

def walk (x : Int) (rail : Bool) (sign : Int) : List Bool → Port × Int
  | [] => ((x,rail),sign)
  | r :: w =>
    walk (if r then x-1 else x+1) r (if rail && r then -sign else sign) w

def amplitude (p : Port) : Int :=
  ((words 5).map fun w =>
    let h := walk 0 false 1 w
    if h.1 == p then h.2 else 0).sum

def positions : List Int := [-5,-3,-1,1,3,5]
def ports : List Port := positions.flatMap fun x => dirs.map (fun r => (x,r))
def masses : List Int := ports.map (fun p => amplitude p ^ 2)
def multiplicity (m : Int) := (masses.filter (· == m)).length

/-- Every reachable signed endpoint is contained in the enumeration. All
    squared amplitudes in the following statements use a common divisor 32. -/
theorem all_slots :
    (words 5).length = 32 ∧
    (words 5).all (fun w => ports.contains (walk 0 false 1 w).1) = true ∧
    (multiplicity 0, multiplicity 1, multiplicity 4, multiplicity 16) = (4,4,3,1) ∧
    masses.sum = 32 := by native_decide

/-- We can score these named ports with +16, -8, +1 respectively. -/
theorem representatives :
    [amplitude (-5,true)^2, amplitude (-3,true)^2, amplitude (3,false)^2] =
    [1,4,16] := by native_decide

/-- Exact score numerator for any rational t = n/d before division by the
    positive normalizer. The analytic application sets t = 4^q and holds
    for real t by the same polynomial identity. -/
theorem scaled_numerator (n d : Int) :
    16*d*d - 8*n*d + n*n = (n-4*d)*(n-4*d) := by
  have h1 : n*(4*d) = 4*(n*d) := by ac_rfl
  have h2 : 4*d*n = 4*(n*d) := by ac_rfl
  have h3 : (4*d)*(4*d) = 16*(d*d) := by
    calc
      (4*d)*(4*d) = (4*4)*(d*d) := by ac_rfl
      _ = _ := rfl
  simp only [Int.sub_mul, Int.mul_sub, h1, h2, h3, Int.mul_assoc]
  omega

end ForwardPowerScale
