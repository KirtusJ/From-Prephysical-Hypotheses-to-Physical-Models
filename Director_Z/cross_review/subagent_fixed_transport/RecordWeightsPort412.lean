import Std

/-!
# Persistent records and the squared response on integer counts

All results are conditional on their stated hypotheses. The response space is
additive, commutative and cancellative; the proof needs neither an order nor
division. In a real probability model the odds equations below have first been
cross-multiplied on branches with positive denominators.
-/

namespace RecordWeights

structure AdditiveLaws (R : Type u) [Add R] [OfNat R 0] : Prop where
  assoc : ∀ a b c : R, (a + b) + c = a + (b + c)
  comm : ∀ a b : R, a + b = b + a
  zero_add : ∀ a : R, 0 + a = a
  cancel_right : ∀ a b c : R, a + c = b + c → a = b

variable {R : Type u} [Add R] [OfNat R 0]

def copies (unit : R) : Nat → R
  | 0 => 0
  | n + 1 => copies unit n + unit

private theorem copies_add (law : AdditiveLaws R) (unit : R) (m n : Nat) :
    copies unit (m+n) = copies unit m + copies unit n := by
  induction n with
  | zero => simp [copies, law.comm (copies unit m) 0, law.zero_add]
  | succ n ih =>
    change copies unit (m+n) + unit = copies unit m + (copies unit n + unit)
    rw [ih, law.assoc]

private theorem left_comm (law : AdditiveLaws R) (a b c : R) :
    a + (b + c) = b + (a + c) := by
  rw [← law.assoc, law.comm a b, law.assoc]

/-- A spectator contributes the same doubled weight on either side. -/
theorem cancel_spectator (law : AdditiveLaws R) (a b big small spectator : R)
    (h : ((a+b)+spectator) + ((a+b)+spectator) =
         (big+small) + (spectator+spectator)) :
    big+small = (a+a)+(b+b) := by
  apply law.cancel_right _ _ (spectator+spectator)
  calc
    (big+small)+(spectator+spectator) = ((a+b)+spectator)+((a+b)+spectator) := h.symm
    _ = ((a+a)+(b+b))+(spectator+spectator) := by
      simp only [law.assoc, law.comm, left_comm law]

private theorem square_indices (n : Nat) :
    (n+2)*(n+2) + n*n = ((n+1)*(n+1) + (n+1)*(n+1)) + (1+1) := by
  simp [Nat.add_mul, Nat.mul_add]
  omega

private theorem square_recurrence (law : AdditiveLaws R) (unit : R) (n : Nat) :
    copies unit ((n+2)*(n+2)) + copies unit (n*n) =
      (copies unit ((n+1)*(n+1)) + copies unit ((n+1)*(n+1))) + (unit+unit) := by
  have units : copies unit (1+1) = unit+unit := by simp [copies, law.zero_add]
  rw [← copies_add law, square_indices n, copies_add law, copies_add law, units]

/-- The second-difference equation and its two initial values determine every
response, for integer multiplicities of arbitrarily large magnitude. -/
theorem square_from_recurrence (law : AdditiveLaws R) (f : Nat → R)
    (zero : f 0 = 0)
    (recurrence : ∀ n : Nat, f (n+2) + f n =
                  (f (n+1)+f (n+1)) + (f 1 + f 1)) :
    ∀ n : Nat, f n = copies (f 1) (n*n) := by
  have pair (n : Nat) :
      f n = copies (f 1) (n*n) ∧ f (n+1) = copies (f 1) ((n+1)*(n+1)) := by
    induction n with
    | zero => simp [zero, copies, law.zero_add]
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      apply law.cancel_right _ _ (f n)
      calc
        f (n+2) + f n = (f (n+1)+f (n+1)) + (f 1 + f 1) := recurrence n
        _ = copies (f 1) ((n+2)*(n+2)) + f n := by
          rw [ih.2, ih.1]
          exact (square_recurrence law (f 1) n).symm
  exact fun n => (pair n).1

/-- For each corridor length the calibration flag leaves twice the unaltered
spectator mass, as well as the two interfering outputs. The spectator can vary
with the corridor length. -/
theorem square_from_corridor_odds (law : AdditiveLaws R) (f : Nat → R)
    (zero : f 0 = 0) (spectator : Nat → R)
    (persistent : ∀ n : Nat,
      ((f (n+1) + f 1) + spectator n) + ((f (n+1) + f 1) + spectator n) =
        (f (n+2) + f n) + (spectator n + spectator n)) :
    ∀ n : Nat, f n = copies (f 1) (n*n) :=
  square_from_recurrence law f zero fun n =>
    cancel_spectator law _ _ _ _ _ (persistent n)

/-- The small fixed-carrier flag constrains only the second response. -/
theorem double_from_five_step_odds (law : AdditiveLaws R) (unit double : R)
    (persistent : copies unit 20 + double = copies unit 24) :
    double = copies unit 4 := by
  apply law.cancel_right _ _ (copies unit 20)
  rw [law.comm double (copies unit 20), persistent, ← copies_add law]

/-! An independent finite calculation of the input to the five-step lemma.
Each member of the list below represents one literal signed path. Aggregation
occurs only when the old flag and all four endpoint coordinates agree. -/

private structure PathEntry where
  site : Nat
  right : Bool
  y : Nat
  z : Nat
  yes : Bool
  sign : Int

private def start : PathEntry := ⟨0,true,0,0,false,1⟩

private def extend (v : PathEntry) (right : Bool) : PathEntry := Id.run do
  let j := v.site / 2
  let a := if v.site % 2 = 0 then 0 else j
  let b := if v.site % 2 = 0 then j else (5 - (j*(j+1)/2)%5) % 5
  return ⟨(v.site + (if right then 1 else 9))%10, right,
           (v.y+a)%5, (v.z+b)%5, v.yes,
           if !v.right && !right then -v.sign else v.sign⟩

private def step (paths : List PathEntry) : List PathEntry :=
  paths.bind fun v => [extend v true, extend v false]

private def label (v : PathEntry) : PathEntry :=
  {v with yes := v.site == 2 && v.right}

private def before : List PathEntry := (step (step [start])).map label

private def after : List PathEntry := step (step (step before))

private def sameEndpoint (u v : PathEntry) : Bool :=
  u.site == v.site && u.right == v.right && u.y == v.y && u.z == v.z && u.yes == v.yes

private def multiplicities (paths : List PathEntry) (yes : Bool) : Nat × Nat × Nat := Id.run do
  let selected := paths.filter (fun v => v.yes == yes)
  let cells := selected.foldl (fun (seen : List PathEntry) u =>
    if seen.any (sameEndpoint u) then seen else u :: seen) []
  let counts := cells.map (fun u => (((selected.filter (sameEndpoint u)).map PathEntry.sign).foldl (· + ·) 0).natAbs)
  return ((counts.filter (· == 1)).length, (counts.filter (· == 2)).length,
          (counts.filter (· > 2)).length)

/-- Positive weights at the persistent coordinate flag, with signs summed
before their absolute value is taken. Kernel computation on 4 and 32 paths. -/
theorem five_step_histograms :
    multiplicities before true = (1,0,0) ∧
    multiplicities before false = (3,0,0) ∧
    multiplicities after true = (8,0,0) ∧
    multiplicities after false = (20,1,0) := of_decide_eq_true (Eq.refl true)

/-! Two structural parts of the moving-corridor construction. After t steps
the position of a path with q left moves is t-2q modulo 2m. The three masks
therefore see the lag q modulo m and the last direction. -/

def corridorMask (m time turns : Nat) (lastLeft : Bool) : Prop :=
  (turns % m = 0 ∧ lastLeft = false) ∨
  (turns % m = 1 ∧ (lastLeft = false ∨ time % (2*m) = 1))

inductive Admitted (m : Nat) : Nat → Nat → Prop where
  | initial : Admitted m 0 0
  | step {t q} (past : Admitted m t q) (left : Bool)
      (accepts : corridorMask m (t+1) (q + (if left then 1 else 0)) left) :
      Admitted m (t+1) (q + (if left then 1 else 0))

/-- No path that has made two left moves can survive by wrapping around. -/
theorem at_most_one_left {m t q : Nat} (ringSize : 3 ≤ m) (path : Admitted m t q) :
    q ≤ 1 := by
  induction path with
  | initial => decide
  | @step t q _ left accepts ih =>
    have small : q + (if left then 1 else 0) < m := by cases left <;> simp_all <;> omega
    rcases accepts with ⟨hz,_⟩ | ⟨ho,_⟩ <;> rw [Nat.mod_eq_of_lt small] at * <;> omega

theorem admitted_left_time {m time turns : Nat} (h : corridorMask m time turns true) :
    time % (2*m) = 1 := by
  rcases h with ⟨_,bad⟩ | ⟨_,bad | good⟩
  · contradiction
  · contradiction
  · exact good

/-- A proposed left time a is reached on a right-moving path. All subsequent
right steps pass the one-turn mask even when their clock is outside the left
window. This is existence of a masked path for every legal switch time. -/
theorem each_left_time_survives (m a : Nat) (ringSize : 3 ≤ m)
    (positive : 0 < a) (window : a % (2*m) = 1) :
    ∀ extra : Nat, Admitted m (a+extra) 1 := by
  have straight (t : Nat) : Admitted m t 0 := by
    induction t with
    | zero => exact .initial
    | succ t ih =>
      exact .step ih false (Or.inl ⟨by simp, rfl⟩)
  have first : Admitted m a 1 := by
    cases a with
    | zero => omega
    | succ a =>
      exact .step (straight a) true (Or.inr ⟨Nat.mod_eq_of_lt (by simp; omega), Or.inr window⟩)
  intro extra
  induction extra with
  | zero => exact first
  | succ extra ih =>
    exact .step ih false (Or.inr ⟨Nat.mod_eq_of_lt (by simp; omega), Or.inl rfl⟩)

def intervalSum (g : Int → Int) (start : Int) : Nat → Int
  | 0 => 0
  | n+1 => intervalSum g start n + g (start + (n : Int))

private theorem interval_shift (g : Int → Int) (s : Int) (n : Nat) :
    intervalSum g (s+1) n + g s = intervalSum g s n + g (s+(n : Int)) := by
  induction n with
  | zero => simp [intervalSum]
  | succ n ih =>
    simp only [intervalSum, Int.ofNat_succ]
    have inside : (s+1)+(n:Int) = s+((n:Int)+1) := by omega
    rw [inside]
    omega

private theorem whole_periods (N blocks : Nat) (g : Int → Int)
    (periodic : ∀ k : Int, g (k+(N:Int)) = g k) (s : Int) :
    g (s + ((blocks*N : Nat) : Int)) = g s := by
  induction blocks with
  | zero => simp
  | succ blocks ih =>
    rw [Nat.succ_mul, Int.natCast_add, ← Int.add_assoc, periodic, ih]

/-- Move the single left step by any number of complete ring periods.
Between its two possible times, the departure coordinates differ by two. The
unshifted and shifted intervals accumulate equal sheet increments, coordinate
by coordinate, even before reducing the sums modulo the sheet order. -/
theorem one_turn_sheet_identity (N blocks : Nat) (g : Int → Int)
    (periodic : ∀ k : Int, g (k+(N:Int)) = g k) (s : Int) :
    intervalSum g s (blocks*N) = intervalSum g (s-2) (blocks*N) := by
  have shift (z : Int) :
      intervalSum g (z+1) (blocks*N) = intervalSum g z (blocks*N) := by
    have edge := interval_shift g z (blocks*N)
    rw [whole_periods N blocks g periodic z] at edge
    omega
  have first := shift (s-1)
  have second := shift (s-2)
  have i₁ : s-1+1 = s := by omega
  have i₂ : s-2+1 = s-1 := by omega
  rw [i₁] at first
  rw [i₂] at second
  exact first.trans second

end RecordWeights

#print axioms RecordWeights.five_step_histograms
#print axioms RecordWeights.square_from_corridor_odds
#print axioms RecordWeights.square_from_recurrence
#print axioms RecordWeights.double_from_five_step_odds
#print axioms RecordWeights.at_most_one_left
#print axioms RecordWeights.admitted_left_time
#print axioms RecordWeights.each_left_time_survives
#print axioms RecordWeights.one_turn_sheet_identity
