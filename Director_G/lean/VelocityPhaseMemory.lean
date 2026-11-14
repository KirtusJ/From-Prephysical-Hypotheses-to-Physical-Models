import Std

/-! Polynomial part of the phase-kicked Hadamard velocity instrument.
This formalizes composition of the stated maps. Identification of those maps
with a ballistic limit, positivity on its support and integration against the
base velocity law are separate analytic steps. -/

namespace VelocityPhaseMemory

/-- Unnormalized trace and Bloch coordinates in a common integer scale. -/
structure Coin where
  mass : Int
  x : Int
  y : Int
  z : Int

/-- With physical velocity v/d, the velocity instrument times d².
The two signs of the unresolved y-component have been averaged. -/
def flight (d v : Int) (s : Coin) : Coin :=
  let a := d*s.mass + v*(s.x+s.z)
  ⟨d*a, v*a, (d*d-2*v*v)*s.y, v*a⟩

/-- Fixed +π/2 phase kick about z (after the preceding site read). -/
def quarter (s : Coin) : Coin := ⟨s.mass, -s.y, s.x, s.z⟩

/-- Read the two z rails, then pool their outputs. -/
def readRail (s : Coin) : Coin := ⟨s.mass, 0, 0, s.z⟩

/-- Pooled adjacent velocities agree for every real initial coin. -/
theorem pair_equal (d v w m x z : Int) :
    (flight d w (quarter (flight d v ⟨m,x,0,z⟩))).mass =
    (flight d w (readRail (flight d v ⟨m,x,0,z⟩))).mass := by
  simp [flight, quarter, readRail]

/-- Quarter minus rail on a triple. Common denominator d⁶ when the
initial coin coordinates are ordinary integers and velocities are v/d,w/d,u/d.
An initial common coin denominator multiplies the result's denominator too. -/
theorem triple_difference (d v w u m x z : Int) :
    (flight d u (quarter (flight d w (quarter (flight d v ⟨m,x,0,z⟩))))).mass -
    (flight d u (readRail (flight d w (readRail (flight d v ⟨m,x,0,z⟩))))).mass =
    -(d*u*(d*d-2*w*w)*v*(d*m+v*(x+z))) := by
  simp only [flight, quarter, readRail, Int.mul_zero, Int.neg_zero,
    Int.zero_add, Int.add_mul, Int.mul_add, Int.neg_mul, Int.mul_neg,
    Int.mul_assoc] <;> omega

/-- At velocities (-1/2,0,1/2) and (1/2,0,1/2) the order switches,
for a trace-one initially mixed coin. These are rational density evaluations,
not probabilities of three prescribed exact real velocities. -/
theorem opposite_signs :
    let run (v : Int) (boundary : Coin → Coin) :=
      (flight 2 1 (boundary (flight 2 0 (boundary (flight 2 v ⟨1,0,0,0⟩))))).mass
    run (-1) quarter > run (-1) readRail ∧
    run 1 quarter < run 1 readRail := by decide

end VelocityPhaseMemory
