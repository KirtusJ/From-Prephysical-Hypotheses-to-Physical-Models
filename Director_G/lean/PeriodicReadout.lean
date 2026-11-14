import Std

/-! Finite concentration bound for mixtures of periodic detector records.
Each component carries an integer mass and a port response in the same units.
An arbitrary finite clock family and arbitrary common denominator are allowed.
A countably infinite family's unselected tail is represented by a separate
aggregate with no period hypothesis in `return_with_tail`. -/
namespace PeriodicReadout

structure Component where
  mass : Nat
  period : Nat
  period_pos : 0 < period
  port : Nat → Nat
  bounded : ∀ n, port n ≤ mass
  repeats : ∀ n, port (n+period) = port n

def total (cs : List Component) := (cs.map Component.mass).sum
def portAt (cs : List Component) (n : Nat) := (cs.map fun c => c.port n).sum
def outside (cs : List Component) (L : Nat) :=
  (cs.map fun c => if c.period ∣ L then 0 else c.mass).sum

theorem own_period_multiples (c : Component) (q : Nat) :
    c.port (q * c.period) = c.port 0 := by
  induction q with
  | zero => simp
  | succ q ih => simp only [Nat.succ_mul, c.repeats, ih]

theorem common_period_multiples (c : Component) (L k : Nat) (fits : c.period ∣ L) :
    c.port (k*L) = c.port 0 := by
  obtain ⟨q, hq⟩ := fits
  rw [hq, Nat.mul_comm c.period q, ← Nat.mul_assoc]
  exact own_period_multiples c (k*q)

theorem port_bounded (cs : List Component) (n : Nat) : portAt cs n ≤ total cs := by
  induction cs with
  | nil => simp [portAt, total]
  | cons c cs ih =>
    change c.port n + portAt cs n ≤ c.mass + total cs
    exact Nat.add_le_add (c.bounded n) ih

/-- Every component with a period dividing L returns its exact initial port
response at kL. Every other component can lose at most its whole mass. -/
theorem synchronized_bound (cs : List Component) (L k : Nat) :
    portAt cs 0 ≤ portAt cs (k*L) + outside cs L := by
  induction cs with
  | nil => simp [portAt, outside]
  | cons c cs ih =>
    change c.port 0 + portAt cs 0 ≤
      c.port (k*L) + portAt cs (k*L) +
        ((if c.period ∣ L then 0 else c.mass) + outside cs L)
    by_cases fits : c.period ∣ L
    · rw [if_pos fits, common_period_multiples c L k fits]
      omega
    · rw [if_neg fits]
      have := c.bounded 0
      omega

/-- The unselected tail need only have a nonnegative port response capped
by its mass. Loss also includes any selected clocks outside the common period
and the initial aggregate launch deficit. No term is dropped by normalization. -/
theorem return_with_tail (cs : List Component) (L k : Nat) (tailMass : Nat)
    (tailPort : Nat → Nat) (bounded : ∀ n, tailPort n ≤ tailMass)
    (launchDeficit : Nat)
    (launch : total cs + tailMass ≤ portAt cs 0 + tailPort 0 + launchDeficit) :
    total cs + tailMass ≤ portAt cs (k*L) + tailPort (k*L) +
      (tailMass + outside cs L) + launchDeficit := by
  have := synchronized_bound cs L k
  have := bounded 0
  omega

/-- A finite panel has an explicit common multiple even without a proposed
L. Its exact launch port therefore recurs at every integer multiple. -/
def common : List Component → Nat
  | [] => 1
  | c :: cs => c.period * common cs

theorem common_pos (cs : List Component) : 0 < common cs := by
  induction cs with
  | nil => decide
  | cons c cs ih =>
    change 0 < c.period * common cs
    exact Nat.mul_pos c.period_pos ih

theorem returns_on_common (cs : List Component) (k : Nat) :
    portAt cs (k * common cs) = portAt cs 0 := by
  induction cs generalizing k with
  | nil => rfl
  | cons c cs ih =>
    change c.port (k * (c.period * common cs)) + portAt cs (k * (c.period * common cs)) =
      c.port 0 + portAt cs 0
    rw [common_period_multiples c _ k (Nat.dvd_mul_right c.period (common cs)),
        ← Nat.mul_assoc, ih]

/-- For the explicit synchronized panel, every possible loss is in the tail
or in the initial aggregate launch deficit. -/
theorem finite_core_bound (cs : List Component) (k tailMass launchDeficit : Nat)
    (tailPort : Nat → Nat) (bounded : ∀ n, tailPort n ≤ tailMass)
    (launch : total cs + tailMass ≤ portAt cs 0 + tailPort 0 + launchDeficit) :
    total cs + tailMass ≤
      portAt cs (k * common cs) + tailPort (k * common cs) + tailMass + launchDeficit := by
  rw [returns_on_common]
  have := bounded 0
  omega

theorem exact_sharp_return (cs : List Component) (k : Nat) (sharp : portAt cs 0 = total cs) :
    portAt cs (k * common cs) = total cs := (returns_on_common cs k).trans sharp

end PeriodicReadout
