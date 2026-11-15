import Std

namespace ContactOrder

/- Exact over the integers, with twice the central coordinate. Reducing
   modulo an odd prime and dividing the last coordinate by two gives the
   contact law used by the walk. Lists are read in chronological order. -/
inductive Move where
  | right | left
  deriving DecidableEq, Repr

open Move

structure State where
  r : Int
  l : Int
  twiceZ : Int
  deriving DecidableEq, Repr

def tick (s : State) : Move → State
  | right => ⟨s.r+1, s.l, s.twiceZ-s.l⟩
  | left  => ⟨s.r, s.l+1, s.twiceZ+s.r⟩

def run (s : State) : List Move → State
  | [] => s
  | m :: rest => run (tick s m) rest

def shift (s : State) (k : Int) : State := ⟨s.r,s.l,s.twiceZ+k⟩

theorem run_append (s : State) (u v : List Move) :
    run s (u ++ v) = run (run s u) v := by
  induction u generalizing s with
  | nil => rfl
  | cons m rest ih => exact ih (tick s m)

theorem run_shift (s : State) (k : Int) (w : List Move) :
    run (shift s k) w = shift (run s w) k := by
  induction w generalizing s with
  | nil => rfl
  | cons m rest ih =>
    have h : tick (shift s k) m = shift (tick s m) k := by
      cases s
      cases m <;> simp [shift,tick] <;> omega
    simp only [run,h,ih]

/-- In any surrounding word, changing L,R to R,L preserves both counts and
    adds exactly one (undoubled) central unit. -/
theorem adjacent_swap (s : State) (before after : List Move) :
    run s (before ++ right :: left :: after) =
      shift (run s (before ++ left :: right :: after)) 2 := by
  simp only [run_append,run]
  rw [← run_shift]
  generalize run s before = b
  cases b
  congr 1
  simp [tick,shift]
  omega

theorem right_run (s : State) (n : Nat) :
    run s (List.replicate n right) =
      ⟨s.r+(n:Int), s.l, s.twiceZ-(n:Int)*s.l⟩ := by
  induction n generalizing s with
  | zero => simp [run]
  | succ n ih =>
    simp only [List.replicate_succ,run,ih,tick,Int.natCast_succ,Int.add_mul,Int.one_mul]
    congr 1 <;> omega

theorem left_run (s : State) (n : Nat) :
    run s (List.replicate n left) =
      ⟨s.r, s.l+(n:Int), s.twiceZ+(n:Int)*s.r⟩ := by
  induction n generalizing s with
  | zero => simp [run]
  | succ n ih =>
    simp only [List.replicate_succ,run,ih,tick,Int.natCast_succ,Int.add_mul,Int.one_mul]
    congr 1 <;> omega

def base (n : Nat) := List.replicate n left ++ List.replicate n right

/-- f complete columns and p remaining squares of the area. The second
    right string may be empty, as may either left string. -/
def partialWord (n f p : Nat) :=
  List.replicate f right ++ List.replicate (n-p) left ++
  [right] ++ List.replicate p left ++ List.replicate (n-f-1) right

theorem partial_area (s : State) (n f p : Nat) (hf : f < n) (hp : p ≤ n) :
    run s (partialWord n f p) =
      shift (run s (base n)) (2*((n:Int)*(f:Int)+(p:Int))) := by
  have hc : n - f - 1 + f + 1 = n := by omega
  have hc' := congrArg Int.ofNat hc
  have hp' := congrArg Int.ofNat (Nat.sub_add_cancel hp)
  simp only [Int.natCast_add, Int.natCast_one] at hc' hp'
  have hr : ((n-f-1:Nat):Int) = (n:Int)-(f:Int)-1 := by omega
  have hl : ((n-p:Nat):Int) = (n:Int)-(p:Int) := by omega
  simp only [partialWord,base,run_append,right_run,left_run,run,tick,shift,hr,hl]
  simp only [Int.mul_add,Int.mul_sub,Int.add_mul,Int.sub_mul,Int.one_mul,Int.mul_one]
  rw [Int.mul_comm (f:Int) (n:Int)]
  congr 1 <;> omega

theorem full_area (s : State) (n : Nat) :
    run s (List.replicate n right ++ List.replicate n left) =
      shift (run s (base n)) (2*((n:Int)*(n:Int))) := by
  simp only [base,run_append,right_run,left_run,shift,Int.mul_add]
  congr 1 <;> omega

/-- Every integer area from zero through n² is realized with exactly 2n
    positive contacts; the reference word has n left and n right contacts.
    The equality of final states includes the two individual source counts. -/
theorem selected_area (s : State) (n k : Nat) (hk : k ≤ n*n) :
    ∃ w : List Move, w.length = 2*n ∧ run s w = shift (run s (base n)) (2*(k:Int)) := by
  by_cases exactSquare : k = n*n
  · refine ⟨List.replicate n right ++ List.replicate n left, ?_, ?_⟩
    · simp; omega
    · simpa only [exactSquare, Int.natCast_mul] using full_area s n
  · have positive : 0 < n := by
      cases n with
      | zero => simp at hk; omega
      | succ _ => omega
    have hf : k/n < n := (Nat.div_lt_iff_lt_mul positive).2 (by omega)
    have hp := Nat.le_of_lt (Nat.mod_lt k positive)
    refine ⟨partialWord n (k/n) (k%n), ?_, ?_⟩
    · simp [partialWord]
      omega
    · have natural : n*(k/n)+k%n = k := by
        rw [Nat.add_comm]
        exact Nat.mod_add_div k n
      have h : (n:Int)*((k/n:Nat):Int)+((k%n:Nat):Int) = (k:Int) := by
        exact_mod_cast natural
      rw [partial_area s n _ _ hf hp, h]

end ContactOrder
