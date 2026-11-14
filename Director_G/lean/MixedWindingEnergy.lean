import Std

/-! Finite rational mixtures, after clearing a common weight denominator.
Weights, winding numbers and all sums are natural numbers. A counting
sector, if present, is tracked separately from the integer labels. -/
namespace MixedWindingEnergy

abbrev Rows := List (Nat × Nat)  -- (absolute winding, weight)

def sumBy (score : Nat → Nat → Nat) (xs : Rows) :=
  (xs.map (fun e => score e.1 e.2)).sum

def mass := sumBy (fun _ w => w)
def energy := sumBy (fun k w => w*(k*k))
def blind := sumBy (fun k w => if k=0 then w else 0)
def bad := sumBy (fun k w => if 2≤k then w else 0)

private theorem pointwise (k w : Nat) :
    w+3*(if 2≤k then w else 0) ≤ w*(k*k)+(if k=0 then w else 0) := by
  by_cases zero : k=0
  · simp [zero]
  by_cases one : k=1
  · simp [one]
  have ge : 2≤k := by omega
  have sq : 4≤k*k := Nat.mul_le_mul ge ge
  have weighted := Nat.mul_le_mul_left w sq
  simp only [if_pos ge, if_neg zero, Nat.add_zero]
  omega

/-- The subtraction-free inequality is exactly energy-mass ≥ 3*bad-blind
after conversion to integers. No normalization or division is necessary. -/
theorem energy_excess (xs : Rows) : mass xs+3*bad xs ≤ energy xs+blind xs := by
  induction xs with
  | nil => decide
  | cons e xs ih =>
    rcases e with ⟨k,w⟩
    have row := pointwise k w
    simp only [mass,bad,energy,blind,sumBy,List.map_cons,List.sum_cons,Nat.mul_add] at ih ⊢
    omega

private theorem at_most_sum (f : Nat → Nat → Nat) (k w : Nat) (xs : Rows)
    (h : (k,w) ∈ xs) : f k w ≤ sumBy f xs := by
  induction xs with
  | nil => simp at h
  | cons e xs ih =>
    rcases List.mem_cons.mp h with eq | mem
    · subst e
      simp [sumBy]
    · have := ih mem
      simp only [sumBy,List.map_cons,List.sum_cons] at this ⊢
      omega

/-- An anchored mixture with energy at most total mass and no zero
winding has no nonzero weight at any label except one. -/
theorem ordinary_support (xs : Rows) (no_blind : blind xs=0)
    (budget : energy xs≤mass xs) :
    bad xs=0 ∧ ∀ k w, (k,w)∈xs → 0<w → k=1 := by
  have excess := energy_excess xs
  have no_bad : bad xs=0 := by omega
  refine ⟨no_bad,?_⟩
  intro k w mem positive
  have bz := at_most_sum (fun n a => if n=0 then a else 0) k w xs mem
  have bh := at_most_sum (fun n a => if 2≤n then a else 0) k w xs mem
  change (if k=0 then w else 0) ≤ blind xs at bz
  change (if 2≤k then w else 0) ≤ bad xs at bh
  by_cases z : k=0
  · rw [if_pos z] at bz; omega
  by_cases large : 2≤k
  · rw [if_pos large] at bh; omega
  omega

/-- A null anchor deficit can remove counting and zero before the
energy test. The empirical anchor must supply the stated lower bound
with strictly positive penalties on these two sectors. -/
theorem anchor_excludes (xs : Rows) (count deficit p q : Nat)
    (pc : 0<p) (qc : 0<q) (floor : p*count+q*blind xs ≤ deficit)
    (exact_anchor : deficit=0) : count=0 ∧ blind xs=0 := by
  have hc : p*count=0 := by omega
  have hb : q*blind xs=0 := by omega
  constructor
  · exact (Nat.mul_eq_zero.mp hc).resolve_left (by omega)
  · exact (Nat.mul_eq_zero.mp hb).resolve_left (by omega)

/-- Equality persists at the sharp coefficient: a unit of mass at two
offsets three units of blind mass, leaving energy exactly total mass. -/
example : let xs : Rows := [(0,3),(2,1)]
    energy xs=mass xs ∧ bad xs=1 ∧ blind xs=3 ∧
    mass xs+3*bad xs=energy xs+blind xs := by decide

end MixedWindingEnergy
