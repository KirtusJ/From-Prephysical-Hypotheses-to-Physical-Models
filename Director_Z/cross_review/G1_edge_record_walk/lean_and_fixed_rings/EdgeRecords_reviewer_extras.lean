import Std

/-! The ordinary signed Hadamard walk on the integer line. Entries are raw
signed sums over histories. The common attenuation per tick is omitted.
The final theorem assumes balance of the two output ports on each tested
block and a common integer-scaled response to absolute signed totals. -/
namespace EdgeRecords

abbrev Amplitudes := Int × Int

def step (field : Int → Amplitudes) (x : Int) : Amplitudes :=
  ((field (x-1)).1 + (field (x-1)).2, (field (x+1)).1 - (field (x+1)).2)

def walk : Nat → Int → Amplitudes
  | 0, x => if x = 0 then (1,0) else (0,0)
  | t+1, x => step (walk t) x

theorem beyond (t : Nat) (x : Int) (h : (t:Int) < x) : walk t x = (0,0) := by
  induction t generalizing x with
  | zero => simp [walk, show x ≠ 0 by omega]
  | succ t ih =>
    simp only [walk, step, ih (x-1) (by omega), ih (x+1) (by omega)]
    decide

theorem leading (t : Nat) : walk t t = (1,0) := by
  induction t with
  | zero => decide
  | succ t ih =>
    change ((walk t (((t+1:Nat):Int)-1)).1 + (walk t (((t+1:Nat):Int)-1)).2,
      (walk t (((t+1:Nat):Int)+1)).1 - (walk t (((t+1:Nat):Int)+1)).2) = (1,0)
    rw [show (((t+1:Nat):Int)-1) = (t:Int) by omega, ih, beyond t _ (by omega)]
    decide

/-- At time n+1 the first site behind the front is x=n-1. Here n-1 is
integer subtraction, so n=0 gives x=-1. -/
theorem behind (n : Nat) : walk (n+1) ((n:Int)-1) = ((n:Int),1) := by
  induction n with
  | zero => decide
  | succ n ih =>
    change step (walk (n+1)) (((n+1:Nat):Int)-1) = (((n+1:Nat):Int),1)
    simp only [step]
    rw [show (((n+1:Nat):Int)-1-1) = (n:Int)-1 by omega,
      show (((n+1:Nat):Int)-1+1) = ((n+1:Nat):Int) by omega, ih, leading]
    simp

/-- At the following tick these are the actual two successors of x=n-1.
The R port is at x+1=n and the L port at x-1=n-2. -/
theorem outgoing (n : Nat) :
    (walk (n+2) (n:Int)).1 = (n:Int)+1 ∧
    (walk (n+2) ((n:Int)-2)).2 = (n:Int)-1 := by
  change (walk (n+1) ((n:Int)-1)).1 + (walk (n+1) ((n:Int)-1)).2 = _ ∧
    (walk (n+1) ((n:Int)-2+1)).1 - (walk (n+1) ((n:Int)-2+1)).2 = _
  rw [show (n:Int)-2+1 = (n:Int)-1 by omega, behind]
  exact ⟨rfl,rfl⟩

def blockBalance (f : Nat → Int) (t : Nat) (x : Int) : Prop :=
  f ((walk (t+1) (x+1)).1.natAbs) + f ((walk (t+1) (x-1)).2.natAbs) =
    2 * (f ((walk t x).1.natAbs) + f ((walk t x).2.natAbs))

/-- Cross-multiplied equality of observed input and output block probabilities.
The raw scale Z may depend on the tick. -/
def observed (f : Nat → Int) (Z : Nat → Int) (t : Nat) (x : Int) : Prop :=
  Z t * (f ((walk (t+1) (x+1)).1.natAbs) + f ((walk (t+1) (x-1)).2.natAbs)) =
    Z (t+1) * (f ((walk t x).1.natAbs) + f ((walk t x).2.natAbs))

theorem observed_behind (f : Nat → Int) (Z : Nat → Int)
    (zero : f 0 = 0) (unit : f 1 ≠ 0) (scale : ∀ t, Z t ≠ 0)
    (front : ∀ t : Nat, observed f Z t t)
    (rear : ∀ n : Nat, observed f Z (n+2) (n:Int)) :
    ∀ n : Nat, blockBalance f (n+2) (n:Int) := by
  have doubles (t : Nat) : Z (t+1) = 2 * Z t := by
    have h := front t
    simp only [observed, walk, step] at h
    rw [show (t:Int)+1-1 = (t:Int) by omega, show (t:Int)-1+1 = (t:Int) by omega,
        leading] at h
    change Z t * (f 1 + f 1) = Z (t+1) * (f 1 + f 0) at h
    rw [zero, Int.add_zero, Int.mul_add] at h
    apply Int.eq_of_mul_eq_mul_right unit
    rw [Int.mul_assoc]
    omega
  intro n
  have h := rear n
  unfold observed at h
  rw [doubles (n+2), Int.mul_comm 2, Int.mul_assoc] at h
  exact Int.eq_of_mul_eq_mul_left (scale _) h

theorem edge_recurrence (f : Nat → Int)
    (balance : ∀ n : Nat, blockBalance f (n+2) (n:Int)) (n : Nat) :
    f (n+2) + f n = 2 * (f (n+1) + f 1) := by
  have b := balance n
  have input := behind (n+1)
  have ports := outgoing (n+1)
  have pos : (((n+1:Nat):Int)-1) = (n:Int) := by omega
  rw [pos] at input
  obtain ⟨right,left⟩ := ports
  have right_x : ((n+1:Nat):Int) = (n:Int)+1 := by omega
  have left_x : (((n+1:Nat):Int)-2) = (n:Int)-1 := by omega
  rw [right_x] at right
  rw [left_x] at left
  change f ((walk (n+3) ((n:Int)+1)).1.natAbs) + f ((walk (n+3) ((n:Int)-1)).2.natAbs) =
    2 * (f ((walk (n+2) (n:Int)).1.natAbs) + f ((walk (n+2) (n:Int)).2.natAbs)) at b
  rw [input, right, left, pos] at b
  change f (n+2) + f n = 2 * (f (n+1) + f 1) at b
  exact b

theorem square_response (f : Nat → Int) (zero : f 0 = 0)
    (balance : ∀ n : Nat, blockBalance f (n+2) (n:Int)) :
    ∀ n : Nat, f n = f 1 * (n:Int) * (n:Int) := by
  have pair (n : Nat) :
      f n = f 1 * (n:Int) * (n:Int) ∧
      f (n+1) = f 1 * ((n+1:Nat):Int) * ((n+1:Nat):Int) := by
    induction n with
    | zero => simp [zero]
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      change f (n+2) = f 1 * ((n+2:Nat):Int) * ((n+2:Nat):Int)
      have recurrence := edge_recurrence f balance n
      rw [ih.1, ih.2] at recurrence
      rw [show ((n+2:Nat):Int) = ((n+1:Nat):Int) + 1 by omega]
      simp only [Int.natCast_succ, Int.add_mul, Int.mul_add, Int.one_mul, Int.mul_one]
        at recurrence ⊢
      omega
  exact fun n => (pair n).1

end EdgeRecords

/-! Reviewer additions (not the author's). Purpose: (1) show the hypotheses of
`observed_behind` and `square_response` are satisfiable (not vacuous) by the
square score with Z t = 2^t; (2) state the composition the note describes;
(3) show the Lean hypotheses do not force nonnegativity or f 1 = 1. -/
namespace EdgeRecords

def sq (k : Nat) : Int := (k:Int) * (k:Int)

theorem step_right (t : Nat) (x : Int) :
    (walk (t+1) (x+1)).1 = (walk t x).1 + (walk t x).2 := by
  change (walk t (x+1-1)).1 + (walk t (x+1-1)).2 = _
  rw [show x+1-1 = x by omega]

theorem step_left (t : Nat) (x : Int) :
    (walk (t+1) (x-1)).2 = (walk t x).1 - (walk t x).2 := by
  change (walk t (x-1+1)).1 - (walk t (x-1+1)).2 = _
  rw [show x-1+1 = x by omega]

theorem sq_natAbs (a : Int) : sq a.natAbs = a * a := by
  unfold sq
  exact Int.natAbs_mul_self' a

/-- The square score balances every block on the line, at every site and tick. -/
theorem sq_balance_all (t : Nat) (x : Int) : blockBalance sq t x := by
  unfold blockBalance
  rw [step_right, step_left, sq_natAbs, sq_natAbs, sq_natAbs, sq_natAbs]
  generalize (walk t x).1 = a
  generalize (walk t x).2 = b
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  have : b * a = a * b := Int.mul_comm b a
  omega

def Zpow (t : Nat) : Int := 2 ^ t

theorem sq_observed_all (t : Nat) (x : Int) : observed sq Zpow t x := by
  have h := sq_balance_all t x
  unfold blockBalance at h
  unfold observed
  rw [h]
  unfold Zpow
  rw [Int.pow_succ, Int.mul_assoc]

/-- Non-vacuity: all five hypotheses of `observed_behind` hold for (sq, 2^t). -/
theorem observed_behind_hyps_satisfiable :
    sq 0 = 0 ∧ sq 1 ≠ 0 ∧ (∀ t, Zpow t ≠ 0) ∧
    (∀ t : Nat, observed sq Zpow t t) ∧ (∀ n : Nat, observed sq Zpow (n+2) (n:Int)) := by
  refine ⟨by decide, by decide, ?_, fun t => sq_observed_all t t, fun n => sq_observed_all (n+2) n⟩
  intro t
  unfold Zpow
  induction t with
  | zero => decide
  | succ t ih => rw [Int.pow_succ]; omega

/-- The composition the specification describes (not present in the author's file). -/
theorem observed_square (f : Nat → Int) (Z : Nat → Int)
    (zero : f 0 = 0) (unit : f 1 ≠ 0) (scale : ∀ t, Z t ≠ 0)
    (front : ∀ t : Nat, observed f Z t t)
    (rear : ∀ n : Nat, observed f Z (n+2) (n:Int)) :
    ∀ n : Nat, f n = f 1 * (n:Int) * (n:Int) :=
  square_response f zero (observed_behind f Z zero unit scale front rear)

/-- A negative-valued "score" passes the Lean hypotheses: f k = -k^2 with Z t = 2^t.
So nonnegativity of f and positivity of Z are not part of the formal premises. -/
def negsq (k : Nat) : Int := -((k:Int) * (k:Int))
theorem negsq_observed_all (t : Nat) (x : Int) : observed negsq Zpow t x := by
  have h := sq_observed_all t x
  unfold observed sq at h
  unfold observed negsq
  simp only [← Int.neg_add, Int.mul_neg]
  rw [h]

end EdgeRecords

#print axioms EdgeRecords.sq_balance_all
#print axioms EdgeRecords.observed_behind_hyps_satisfiable
#print axioms EdgeRecords.observed_square
#print axioms EdgeRecords.negsq_observed_all
