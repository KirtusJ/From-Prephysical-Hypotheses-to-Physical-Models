import Std

namespace FourGainWinding

/-- false = R, true = L. Proof works over Z before group orders are imposed. -/
def edge (a b c d : Int) (old new : Bool) : Int :=
  if old then (if new then d else c) else (if new then b else a)

structure Counts where
  rail : Bool
  ticks : Int
  left : Int
  ll : Int
  gain : Int

def step (a b c d : Int) (x : Counts) (new : Bool) : Counts :=
  ⟨new, x.ticks + 1, x.left + new.toNat, x.ll + (x.rail && new).toNat,
    x.gain + edge a b c d x.rail new⟩

def formula (a b c d : Int) (x : Counts) : Prop :=
  x.gain = x.ticks*a + (x.rail.toNat : Int)*(a-c) + x.left*(b+c-2*a) + x.ll*(a+d-b-c)

theorem formula_step (a b c d : Int) (x : Counts) (h : formula a b c d x)
    (k : Bool) : formula a b c d (step a b c d x k) := by
  rcases x with ⟨old,t,l,m,g⟩
  cases old <;> cases k <;>
    simp [formula, step, edge, Bool.toNat, Int.add_mul] at h ⊢ <;> omega

theorem formula_all (a b c d : Int) (w : List Bool) (x : Counts)
    (hx : formula a b c d x) : formula a b c d (w.foldl (step a b c d) x) := by
  induction w generalizing x with
  | nil => exact hx
  | cons k tail ih => exact ih _ (formula_step a b c d _ hx k)

theorem from_sharp_R (a b c d : Int) (w : List Bool) :
    formula a b c d (w.foldl (step a b c d) ⟨false,0,0,0,0⟩) :=
  formula_all _ _ _ _ _ _ (by simp [formula, Bool.toNat])

/-- Crossing of a shifted deficit wire with another wire. No path gains are used. -/
theorem hits_zero (z : Nat → Int) (n : Nat) (start : 0 < z 0) (finish : z n ≤ 0)
    (slow : ∀ i, i < n → z i ≤ z (i+1) + 1) :
    ∃ i, i ≤ n ∧ z i = 0 := by
  induction n with
  | zero => omega
  | succ n ih =>
    by_cases before : z n ≤ 0
    · obtain ⟨i, le, h⟩ := ih before (fun i hi => slow i (by omega))
      exact ⟨i, by omega, h⟩
    · have := slow n (by omega)
      exact ⟨n+1, by omega, by omega⟩

/-- The shifted wires start and finish strictly on opposite sides. -/
theorem interior_crossing (z : Nat → Int) (n : Nat) (start : 0 < z 0)
    (finish : z n < 0) (slow : ∀ i, i < n → z i ≤ z (i+1) + 1) :
    ∃ i, 0 < i ∧ i < n ∧ z i = 0 := by
  obtain ⟨i, le, h⟩ := hits_zero z n start (by omega) slow
  have hn : i ≠ n := by intro e; subst i; omega
  have hz : i ≠ 0 := by intro e; subst i; omega
  exact ⟨i, by omega, by omega, h⟩

end FourGainWinding
