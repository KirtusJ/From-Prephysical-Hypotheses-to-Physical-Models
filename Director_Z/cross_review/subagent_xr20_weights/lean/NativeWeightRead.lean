import Std

/-!
# Terminal one-left reads with staircase departure gain

The outgoing rail is a Boolean (R=true). Start at x=0, coin R, sheet 0.
Each physical tick adds floor(x/2) on departure. Hadamard's only negative
entry is L→L; the common amplitude denominator after t ticks is sqrt(2^t).
-/
namespace NativeWeightRead

private def move (b : Bool) : Int := if b then 1 else -1
def gain (x : Int) : List Bool → Int
  | [] => 0
  | b::w => x/2+gain (x+move b) w

def finish (x : Int) : List Bool → Int
  | [] => x
  | b::w => finish (x+move b) w

def sign (last : Bool) : List Bool → Int
  | [] => 1
  | b::w => (if !b && !last then -1 else 1)*sign b w

/-- i right moves before the sole left, then j more rights in the initialLeg.
The last right tick is additional and fixes the final rail. -/
def initialLeg (i j : Nat) := List.replicate i true ++ [false] ++ List.replicate j true
def word (i j : Nat) := initialLeg i j ++ [true]

theorem endpoint_count (x : Int) (w : List Bool) :
    finish x w = x+(w.length:Int)-2*(w.count false:Int) := by
  induction w generalizing x with
  | nil => simp [finish]
  | cons b w ih =>
    cases b <;> simp [finish,ih,move,List.count_cons] <;> omega

theorem endpoint_class (w : List Bool) (n : Nat) (h : w.length=n) :
    finish 0 (w++[true])=(n:Int)-1 ↔ w.count false=1 := by
  rw [endpoint_count]
  simp [h,List.count_cons]
  omega

private theorem all_right (w : List Bool) (z : w.count false=0) : w=List.replicate w.length true := by
  induction w with
  | nil => rfl
  | cons b w ih =>
    cases b with
    | false => simp [List.count_cons] at z
    | true =>
      simp [List.count_cons] at z
      change true::w = true::List.replicate w.length true
      exact congrArg (List.cons true) (ih z)

theorem one_left (w : List Bool) : w.count false=1 ↔ ∃ i j, w=initialLeg i j := by
  constructor
  · induction w with
    | nil => simp
    | cons b w ih =>
      intro h
      cases b with
      | false =>
        have z : w.count false=0 := by simpa [List.count_cons] using h
        exact ⟨0,w.length,by simpa [initialLeg] using all_right w z⟩
      | true =>
        have z : w.count false=1 := by simpa [List.count_cons] using h
        obtain ⟨i,j,h⟩ := ih z
        exact ⟨i+1,j,by simp [initialLeg,List.replicate_succ,h]⟩
  · rintro ⟨i,j,rfl⟩
    simp [initialLeg,List.count_replicate,List.count_cons]

private theorem leading_R (i j : Nat) : (initialLeg i j).takeWhile id=List.replicate i true := by
  induction i with
  | zero => simp [initialLeg,List.takeWhile]
  | succ i ih => simp [initialLeg,List.replicate_succ,List.takeWhile] at ih ⊢

theorem unique_left_time (i j u v : Nat) (h : initialLeg i j=initialLeg u v) : i=u ∧ j=v := by
  have n := congrArg List.length h
  simp [initialLeg] at n
  have lead := congrArg (fun w : List Bool => (w.takeWhile id).length) h
  simp only [leading_R,List.length_replicate] at lead
  omega

theorem port_words (n : Nat) (w : List Bool) (h : w.length=n) :
    finish 0 (w++[true])=(n:Int)-1 ↔ ∃ i j, i+j+1=n ∧ w=initialLeg i j := by
  rw [endpoint_class _ _ h,one_left]
  constructor
  · rintro ⟨i,j,rfl⟩
    refine ⟨i,j,?_,rfl⟩
    simp [initialLeg] at h
    omega
  · rintro ⟨i,j,_,h⟩
    exact ⟨i,j,h⟩

private theorem sign_right_run (b : Bool) (n : Nat) : sign b (List.replicate n true)=1 := by
  induction n generalizing b with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ,sign,ih]

theorem positive_word (i j : Nat) : sign true (word i j)=1 := by
  induction i with
  | zero =>
    change sign true (false :: (List.replicate j true ++ [true]))=1
    rw [← List.replicate_succ']
    simp [sign,sign_right_run]
  | succ i ih => simpa [word,initialLeg,List.replicate_succ,sign] using ih

private theorem interchange (x : Int) (w : List Bool) :
    gain x (true::false::w)=gain x (false::true::w)+1 := by
  dsimp [gain,move]
  rw [show x+1+(-1)=x+(-1)+1 by omega]
  omega

private theorem common_prefix (x : Int) (i : Nat) (w z : List Bool) (d : Int)
    (h : ∀y,gain y w=gain y z+d) :
    gain x (List.replicate i true ++ w)=gain x (List.replicate i true ++ z)+d := by
  induction i generalizing x with
  | zero => exact h x
  | succ i ih =>
    simp only [List.replicate_succ,List.cons_append,gain]
    rw [ih]; omega

theorem adjacent_counts (x : Int) (i j : Nat) :
    gain x (word (i+1) j)=gain x (word i (j+1))+1 := by
  unfold word initialLeg
  rw [List.replicate_succ' (n:=i)]
  simp only [List.append_assoc,List.cons_append,List.nil_append]
  apply common_prefix x i _ _ 1
  intro y
  simpa only [List.replicate_succ,List.cons_append] using interchange y (List.replicate j true ++ [true])

theorem consecutive_gain (x : Int) (i j : Nat) :
    gain x (word i j)=gain x (word 0 (i+j))+(i:Int) := by
  induction i generalizing j with
  | zero => simp
  | succ i ih =>
    rw [adjacent_counts,ih]
    rw [show i+1+j=i+(j+1) by omega]
    simp only [Int.natCast_succ]
    omega

/-- Wraparound does not introduce false spatial endpoints when 2t<B.
An N=4M base has this property at t<=M+2 for M>=3. -/
theorem ring_to_line (N : Int) (t : Nat) (w : List Bool) (len : w.length=t)
    (wide : 2*(t:Int)<N) (target : Int) (lo : -(t:Int)≤target) (hi : target≤t)
    (matched : (finish 0 w)%N=target%N) : finish 0 w=target := by
  have cnt := List.count_le_length (a:=false) (l:=w)
  have ep := endpoint_count 0 w
  rw [len] at cnt ep
  have eq := Int.emod_eq_emod_iff_emod_sub_eq_zero.mp matched
  by_cases ge : finish 0 w≥target
  · rw [Int.emod_eq_of_lt (by omega) (by omega)] at eq
    omega
  · have n : ((finish 0 w-target)+N)%N=0 := by simpa using eq
    rw [Int.emod_eq_of_lt (by omega) (by omega)] at n
    omega

/-- Correlation at distance h is stored as C h, including the self-pair.
The finite weighted sums below use integer numerators; a common rational
denominator is allowed by replacing 1 with the supplied scale s. -/
def gaps (C : Nat → Int) : Nat → Int
  | 0 => 0
  | n+1 => gaps C n+C (n+1)

private def dist (n i : Nat) := (n-i)+(i-n)
private theorem dist_eq_sub_of_le {n i : Nat} (h : i≤n) : dist n i=n-i := by unfold dist; omega
private theorem dist_self (n : Nat) : dist n n=0 := by simp [dist]
private theorem dist_comm (n i : Nat) : dist n i=dist i n := by unfold dist; omega

private theorem sum_append (x y : List Int) : (x++y).sum=x.sum+y.sum := by
  induction x with
  | nil => simp
  | cons a x ih => simp only [List.cons_append,List.sum_cons,ih]; omega

private def row (C : Nat → Int) (i n : Nat) : Int :=
  ((List.range n).map fun j => C (dist i j)).sum

def orderedPairs (C : Nat → Int) (n : Nat) : Int :=
  ((List.range n).map fun i => row C i n).sum

def weight (c : Int) (C : Nat → Int) (n : Nat) := (n:Int)*c+orderedPairs C n

private theorem descending (f : Nat → Int) (n : Nat) :
    ((List.range n).map fun i => f (n-i)).sum = gaps f n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [List.range_succ_eq_map]
    simp only [List.map_cons,List.sum_cons,List.map_map,Function.comp_def,Nat.sub_zero,
      Nat.succ_sub_succ_eq_sub]
    rw [ih,gaps]
    omega

private theorem combined_sum (xs : List Nat) (a b : Nat → Int) :
    (xs.map (fun i => a i+b i)).sum = (xs.map a).sum+(xs.map b).sum := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons,List.sum_cons,ih]; omega

private theorem expanding_row (C : Nat → Int) (i n : Nat) :
    row C i (n+1) = row C i n + C (dist i n) := by
  simp [row,List.range_succ,sum_append]

private theorem final_row (C : Nat → Int) (n : Nat) :
    row C n (n+1)=C 0+gaps C n := by
  rw [expanding_row]
  have h : ((List.range n).map fun i => C (dist n i)) =
      ((List.range n).map fun i => C (n-i)) := by
    apply List.map_congr_left
    intro i hi
    have lt := List.mem_range.mp hi
    rw [dist_eq_sub_of_le (Nat.le_of_lt lt)]
  unfold row
  rw [h,descending,dist_self]
  omega

theorem ordered_succ (C : Nat → Int) (n : Nat) :
    orderedPairs C (n+1) = orderedPairs C n+C 0+2*gaps C n := by
  unfold orderedPairs
  rw [List.range_succ,List.map_append,sum_append]
  simp only [List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,Int.add_zero]
  simp only [expanding_row]
  rw [combined_sum]
  have dist : ((List.range n).map fun i => C (dist i n)) =
      ((List.range n).map fun i => C (n-i)) := by
    apply List.map_congr_left
    intro i hi
    rw [dist_comm,dist_eq_sub_of_le (Nat.le_of_lt (List.mem_range.mp hi))]
  have last := final_row C n
  rw [expanding_row] at last
  rw [dist,descending]
  omega

theorem weight_zero (c : Int) (C : Nat → Int) : weight c C 0=0 := by
  simp [weight,orderedPairs]

theorem weight_one (c : Int) (C : Nat → Int) : weight c C 1=c+C 0 := by
  change 1*c+((C 0+0)+0)=c+C 0
  omega

theorem second_difference (c : Int) (C : Nat → Int) (n : Nat) :
    weight c C (n+2)-2*weight c C (n+1)+weight c C n = 2*C (n+1) := by
  simp only [weight, Int.natCast_succ,Int.add_mul,Int.one_mul]
  have a := ordered_succ C n
  have b := ordered_succ C (n+1)
  change orderedPairs C (n+2)=_ at b
  rw [gaps] at b
  omega

theorem complete_residue (c scale : Int) (C : Nat → Int) (M : Nat)
    (periodic : C M=C 0) (normalized : weight c C 1=scale) :
    weight c C (M+1)-2*weight c C M+weight c C (M-1) = 2*(scale-c) ∨ M=0 := by
  cases M with
  | zero => exact Or.inr rfl
  | succ n =>
    left
    rw [weight_one] at normalized
    have f := second_difference c C n
    simpa using (show weight c C (n+2)-2*weight c C (n+1)+weight c C n=2*(scale-c) by omega)

/-- Named guide table on the 4M-cycle agrees with its line lift modulo M.
Each subtraction of one base lap changes the unwrapped gain by 2M. -/
theorem guide_periodic (x M : Int) : ((x+4*M)/2)%M=(x/2)%M := by
  have d : (x+4*M)/2=x/2+2*M := by omega
  rw [d,Int.add_mul_emod_self]

theorem guide_canonical (x M : Int) : ((x%(4*M))/2)%M=(x/2)%M := by
  have eq := Int.ediv_add_emod x (4*M)
  have decomp : x/2=(x%(4*M))/2 + 2*M*(x/(4*M)) := by
    have multiplied : 4*M*(x/(4*M))=2*(2*M*(x/(4*M))) := by
      simp only [Int.mul_assoc]
      generalize M*(x/(4*M))=z
      omega
    rw [multiplied] at eq
    omega
  rw [decomp]
  rw [show 2*M*(x/(4*M))=(2*(x/(4*M)))*M by simp [Int.mul_assoc,Int.mul_comm,Int.mul_left_comm],
      Int.add_mul_emod_self]

/-- Position difference of the two positive paths at a fixed depth is
twice the change in the number of left moves; on our specific returned
one-left family the relevant pair difference is in the *sheet* gains. -/
theorem endpoint_pair_gap (x : Int) (i j u v : Nat) (equalDepth : i+j=u+v) :
    gain x (word i j)-gain x (word u v) = (i:Int)-u := by
  rw [consecutive_gain x i j,consecutive_gain x u v,equalDepth]
  omega

private def allWords : Nat → List (List Bool)
  | 0 => [[]]
  | n+1 => (allWords n).map (true::·) ++ (allWords n).map (false::·)

private def fiveWords := (allWords 5).filter fun w => finish 0 w == 1 && w.getLast? == some true
private def gainSigns := fiveWords.map (fun w => (gain 0 w,sign true w))

/-- All six physical histories at (1,R) in five ticks. Exactly two
opposite signs share integer sheet -1. -/
theorem five_raw : gainSigns = [(1,-1),(0,1),(-1,-1),(-1,1),(-2,1),(-3,-1)] := by
  decide +kernel

private theorem residue_distinct (M j : Int) (h : 3≤M) (s : j=-2 ∨ j=-1 ∨ j=1 ∨ j=2) :
    j%M≠0 := by
  rcases s with h₁|h₁|h₁|h₁ <;> subst j
  · intro bad
    have k := Int.add_emod_self (a := -2) (b := M)
    rw [Int.emod_eq_of_lt (by omega) (by omega)] at k
    omega
  · intro bad
    have k := Int.add_emod_self (a := -1) (b := M)
    rw [Int.emod_eq_of_lt (by omega) (by omega)] at k
    omega
  · rw [Int.emod_eq_of_lt (by omega) (by omega)]
    decide
  · rw [Int.emod_eq_of_lt (by omega) (by omega)]
    decide

theorem dark_sheet (M : Int) (h : 3≤M) :
    (gainSigns.filter (fun p => p.1%M==(-1)%M)).map Prod.snd=[-1,1] := by
  have guard (x : Int) (s : x=-3 ∨ x=-2 ∨ x=0 ∨ x=1) : x%M≠(-1)%M := by
    have n : (x-(-1))%M≠0 := residue_distinct M _ h (by omega)
    intro eq
    exact n (Int.emod_eq_emod_iff_emod_sub_eq_zero.mp eq)
  have h1 := guard 1 (by omega)
  have h0 := guard 0 (by omega)
  simp only [Int.zero_emod] at h0
  have h2 := guard (-2) (by omega)
  have h3 := guard (-3) (by omega)
  simp [five_raw,List.filter_cons,h1,h0,h2,h3]

/-- If an actually dark two-history sheet has zero readout under the
count-plus-squared rule, the count coefficient vanishes. -/
theorem sharp_dark_removes_count (c K : Int) (sharp : 2*c+K*(1-1)^2=0) : c=0 := by
  simp at sharp
  omega

/-- For a real even Fourier kernel transfer the underlying scalar argument
to Nat absolute differences. Here the proof is in integer-scaled
coefficients as in the weighted sums above. -/
theorem actual_path_correlation (K : Int → Int) (even : ∀z,K (-z)=K z)
    (x : Int) (i j u v : Nat) (commonLength : i+j=u+v) :
    K (gain x (word i j)-gain x (word u v)) = K (dist i u : Int) := by
  rw [endpoint_pair_gap _ _ _ _ _ commonLength]
  by_cases h : i≤u
  · have eq : (i:Int)-u = -(dist i u:Int) := by unfold dist; omega
    rw [eq,even]
  · have eq : (i:Int)-u = (dist i u:Int) := by unfold dist; omega
    rw [eq]

theorem four_M_separates (M t : Nat) (hM : M≥3) (flight : t≤M+2) :
    2*(t:Int)<4*(M:Int) := by omega

theorem period_read (c scale : Int) (C : Nat → Int) (M : Nat) (hM : 0<M)
    (periodic : C M=C 0) (normalized : weight c C 1=scale) :
    weight c C (M+1)-2*weight c C M+weight c C (M-1) = 2*(scale-c) := by
  rcases complete_residue c scale C M periodic normalized with h|h
  · exact h
  · omega

end NativeWeightRead
