import Std

namespace ContactPositionWeights

/-! Lean 4.19.0, standard library only. Integer coefficient rows represent
linear forms in arbitrary weights f(0), …, f(11). Checking a coefficient
identity once allows a separate evaluation in any ordered additive group,
including real-valued weights. No field, exponentiation or continuity
operation appears in the two finite convexity comparisons. -/

abbrev Row := Fin 12 → Int

/-- Coefficient of f(k) in f(j+1) - 2 f(j) + f(j-1), j≥1. -/
def secondRow (j : Nat) (k : Fin 12) : Int :=
  if k.val = j+1 then 1 else if k.val = j then -2 else if k.val+1 = j then 1 else 0

/-- Difference of the coefficient rows of two equally long lists. -/
def difference (xs ys : List Nat) (k : Fin 12) : Int :=
  ((xs.count k.val : Nat) : Int) - ((ys.count k.val : Nat) : Int)

/-- Repeated centers represent positive integer multiples of curvature. -/
def addRows : List Row → Row
  | [] => fun _ => 0
  | r::rs => fun k => r k + addRows rs k

def coarseCenters : List Nat := [2,3,4,5,6]
def wellCenters : List Nat := [1,1,1, 2,2,2,2, 3,3,3, 4,4,4, 5,5,5, 6,6, 7,8,9,10]

theorem binary_coefficients :
    difference [7,1] [6,2] = addRows (coarseCenters.map secondRow) := by
  funext k
  exact (by decide : ∀ i : Fin 12, difference [7,1] [6,2] i =
    addRows (coarseCenters.map secondRow) i) k

theorem well_coefficients :
    difference [11,7,3,2,1,0,0,0] [10,5,2,2,2,1,1,1] =
      addRows (wellCenters.map secondRow) := by
  funext k
  exact (by decide : ∀ i : Fin 12, difference [11,7,3,2,1,0,0,0] [10,5,2,2,2,1,1,1] i =
    addRows (wellCenters.map secondRow) i) k

/-- Minimal facts about evaluating coefficient rows at weights. Ordinary
evaluation over real weights sends r to ∑ k, r(k) f(k). Only additivity,
zero and positivity of addition are needed for the forward theorem. -/
structure Evaluation (V : Type) [Zero V] [Add V] [LT V] where
  eval : Row → V
  eval_zero : eval (fun _ => 0) = 0
  eval_add : ∀ (r s : Row), eval (fun k => r k + s k) = eval r + eval s
  add_positive : ∀ a b : V, 0 < a → 0 < b → 0 < a+b
  right_zero : ∀ a : V, a+0=a

variable {V : Type} [Zero V] [Add V] [LT V]

private theorem positive_rows (e : Evaluation V) (r : Row) (rs : List Row)
    (h : ∀ t ∈ r::rs, 0 < e.eval t) : 0 < e.eval (addRows (r::rs)) := by
  induction rs generalizing r with
  | nil => simpa [addRows, e.eval_add, e.eval_zero, e.right_zero] using h r (by simp)
  | cons s tail ih =>
    rw [addRows, e.eval_add]
    exact e.add_positive _ _ (h r (by simp))
      (ih s (fun t ht => h t (List.mem_cons_of_mem _ ht)))

private theorem zero_rows (e : Evaluation V) (rs : List Row)
    (h : ∀ r ∈ rs, e.eval r = 0) : e.eval (addRows rs) = 0 := by
  induction rs with
  | nil => exact e.eval_zero
  | cons r tail ih =>
    rw [addRows, e.eval_add, h r (by simp), ih (fun t ht => h t (List.mem_cons_of_mem _ ht)),
      e.right_zero]

/-- Holds for evaluating any f with strictly positive second differences
at levels 2..6. To obtain the strict reverse inequality use -f. -/
theorem binary_strict (e : Evaluation V)
    (h : ∀ j ∈ coarseCenters, 0 < e.eval (secondRow j)) :
    0 < e.eval (difference [7,1] [6,2]) := by
  rw [binary_coefficients]
  apply positive_rows
  change ∀ t ∈ coarseCenters.map secondRow, 0 < e.eval t
  simpa only [List.forall_mem_map] using h

/-- On the fine board the coefficients of the second differences at levels
1..10 are [3,4,3,3,3,2,1,1,1,1]. Zero padding turns the five nonzero
entries into an equal-length comparison. Take f(0)=0 for the odds test. -/
theorem well_strict (e : Evaluation V)
    (h : ∀ j ∈ wellCenters, 0 < e.eval (secondRow j)) :
    0 < e.eval (difference [11,7,3,2,1,0,0,0] [10,5,2,2,2,1,1,1]) := by
  rw [well_coefficients]
  apply positive_rows
  change ∀ t ∈ wellCenters.map secondRow, 0 < e.eval t
  simpa only [List.forall_mem_map] using h

theorem binary_affine (e : Evaluation V)
    (h : ∀ j ∈ coarseCenters, e.eval (secondRow j) = 0) :
    e.eval (difference [7,1] [6,2]) = 0 := by
  rw [binary_coefficients]
  apply zero_rows
  simpa only [List.forall_mem_map] using h

theorem well_affine (e : Evaluation V)
    (h : ∀ j ∈ wellCenters, e.eval (secondRow j) = 0) :
    e.eval (difference [11,7,3,2,1,0,0,0] [10,5,2,2,2,1,1,1]) = 0 := by
  rw [well_coefficients]
  apply zero_rows
  simpa only [List.forall_mem_map] using h

/-- Reversing both weights and the sign of the comparison is the same proof.
The additive negation laws here allow every ordered additive group. -/
def negated (e : Evaluation V) (neg : V → V) (nz : neg 0 = 0)
    (na : ∀ a b, neg (a+b) = neg a + neg b) : Evaluation V where
  eval r := neg (e.eval r)
  eval_zero := by rw [e.eval_zero, nz]
  eval_add r s := by rw [e.eval_add, na]
  add_positive := e.add_positive
  right_zero := e.right_zero

theorem strict_concave (e : Evaluation V) (neg : V → V) (nz : neg 0 = 0)
    (na : ∀ a b, neg (a+b) = neg a + neg b) (sign : ∀ a, 0 < neg a ↔ a < 0) :
    ((∀ j ∈ coarseCenters, e.eval (secondRow j) < 0) →
      e.eval (difference [7,1] [6,2]) < 0) ∧
    ((∀ j ∈ wellCenters, e.eval (secondRow j) < 0) →
      e.eval (difference [11,7,3,2,1,0,0,0] [10,5,2,2,2,1,1,1]) < 0) := by
  constructor
  · intro h
    apply (sign _).mp
    apply binary_strict (negated e neg nz na)
    exact fun j hj => (sign _).mpr (h j hj)
  · intro h
    apply (sign _).mp
    apply well_strict (negated e neg nz na)
    exact fun j hj => (sign _).mpr (h j hj)

/-- Weak convexity permits zero curvature at some levels. Under the usual
ordered-additive laws, the gap vanishes exactly when every represented
level has zero curvature. -/
private theorem weak_rows [LE V] (e : Evaluation V)
    (z : (0:V) ≤ 0) (aa : ∀ a b : V, 0 ≤ a → 0 ≤ b → 0 ≤ a+b)
    (eqz : ∀ a b : V, 0 ≤ a → 0 ≤ b → (a+b=0 ↔ a=0 ∧ b=0))
    (rs : List Row) (h : ∀ r ∈ rs, 0 ≤ e.eval r) :
    0 ≤ e.eval (addRows rs) ∧
      (e.eval (addRows rs) = 0 ↔ ∀ r ∈ rs, e.eval r = 0) := by
  induction rs with
  | nil => simp [addRows, e.eval_zero, z]
  | cons r tail ih =>
    have hr := h r (by simp)
    have ht := ih (fun s hs => h s (List.mem_cons_of_mem _ hs))
    rw [addRows, e.eval_add]
    exact ⟨aa _ _ hr ht.1, by rw [eqz _ _ hr ht.1, ht.2, List.forall_mem_cons]⟩

theorem weak_boundary [LE V] (e : Evaluation V)
    (z : (0:V) ≤ 0) (aa : ∀ a b : V, 0 ≤ a → 0 ≤ b → 0 ≤ a+b)
    (eqz : ∀ a b : V, 0 ≤ a → 0 ≤ b → (a+b=0 ↔ a=0 ∧ b=0))
    (h : ∀ j ∈ wellCenters, 0 ≤ e.eval (secondRow j)) :
    (e.eval (difference [11,7,3,2,1,0,0,0] [10,5,2,2,2,1,1,1]) = 0 ↔
      ∀ j ∈ wellCenters, e.eval (secondRow j) = 0) ∧
    (e.eval (difference [7,1] [6,2]) = 0 ↔
      ∀ j ∈ coarseCenters, e.eval (secondRow j) = 0) := by
  have sub : ∀ j ∈ coarseCenters, j ∈ wellCenters := by
    intro j hj
    simp [coarseCenters] at hj
    rcases hj with h | h | h | h | h <;> subst j <;> decide
  rw [well_coefficients, binary_coefficients]
  constructor
  · simpa only [List.forall_mem_map] using
      (weak_rows e z aa eqz (wellCenters.map secondRow) (List.forall_mem_map.mpr h)).2
  · simpa only [List.forall_mem_map] using
      (weak_rows e z aa eqz (coarseCenters.map secondRow)
        (List.forall_mem_map.mpr (fun j hj => h j (sub j hj)))).2

end ContactPositionWeights
