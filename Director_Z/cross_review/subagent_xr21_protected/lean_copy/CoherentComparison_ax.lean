import Std

/-!
# Cross-table comparison for finite coherent preparations

A table is a list of occurrences (signed numerator, coordinate mass). All
tables compared have the same amplitude denominator sqrt(2^t). Masses can
take values in the reals or another additive cancellative domain. A coherent
joint table is used only to compare equal signed entries between two
preparations; no conditional or heralded probability enters the argument.
-/
namespace CoherentComparison

structure Laws (R : Type u) [Add R] [OfNat R 0] : Prop where
  assoc : ∀ a b c : R, (a+b)+c = a+(b+c)
  zero_add : ∀ a : R, 0+a=a
  add_zero : ∀ a : R, a+0=a
  cancel : ∀ a b c : R, a+c=b+c → a=b

variable {R : Type u} [Add R] [OfNat R 0]

def copies (p : R) : Nat → R
  | 0 => 0
  | n+1 => copies p n + p

private theorem split_copies (L : Laws R) (p : R) (a b : Nat) :
    copies p (a+b) = copies p a + copies p b := by
  induction b with
  | zero => simp [copies, L.add_zero]
  | succ b ih => change copies p (a+b) + p = copies p a + (copies p b + p)
                 rw [ih, L.assoc]

private theorem mul_copies (L : Laws R) (p : R) (n m : Nat) :
    copies (copies p n) m = copies p (m*n) := by
  induction m with
  | zero => simp [copies]
  | succ m ih => simp [copies, ih, Nat.succ_mul, split_copies L]

def sumMass : List (Int × R) → R
  | [] => 0
  | (_,p)::xs => p + sumMass xs

def sqCounts : List Int → Nat
  | [] => 0
  | n::ns => n.natAbs^2 + sqCounts ns

private theorem entry_bound (ns : List Int) (n : Int) (mem : n ∈ ns) :
    n.natAbs^2 ≤ sqCounts ns := by
  induction ns with
  | nil => simp at mem
  | cons x xs ih =>
    rcases List.mem_cons.mp mem with eq | rest
    · subst n; simp [sqCounts]
    · have := ih rest; simp [sqCounts]; omega

/-- Equal protected coordinates from coherent alternatives give equal
original marginal masses. Protection reconstructs the original mass from
the two equal joint copies. There is no division or nonzero requirement. -/
structure JointComparison (n n' : Int) (p p' : R) : Type u where
  left : R
  right : R
  left_protected : p=left+left
  right_protected : p'=right+right
  equal_joint : n=n' → left=right

omit [OfNat R 0] in
theorem equal_coordinate {n n' : Int} {p p' : R}
    (same : n=n') (j : JointComparison n n' p p') : p=p' := by
  calc
    p = j.left+j.left := j.left_protected
    _ = j.right+j.right := congrArg (fun x : R => x+x) (j.equal_joint same)
    _ = p' := j.right_protected.symm

private theorem sum_identical (L : Laws R) (rows : List (Int × R))
    (n : Int) (p : R) (h : ∀ x ∈ rows, x.1=n ∧ x.2=p) :
    sumMass rows = copies p rows.length := by
  induction rows with
  | nil => rfl
  | cons x xs ih =>
    have head := (h x (by simp)).2
    have tail := ih (fun z hz => h z (by simp [hz]))
    change x.2 + sumMass xs = copies p (xs.length+1)
    rw [head, tail, Nat.add_comm xs.length 1, split_copies L]
    simp [copies, L.zero_add]

private theorem sum_append (L : Laws R) (xs ys : List (Int × R)) :
    sumMass (xs++ys) = sumMass xs + sumMass ys := by
  induction xs with
  | nil => simp [sumMass, L.zero_add]
  | cons a xs ih => simp [sumMass, ih, L.assoc]

/-- The table rows have only one numerator value and each one therefore
matches a chosen reference mass. -/
private theorem mass_block (L : Laws R) (rows : List (Int × R))
    (v : Int) (p : R) (label : rows.map Prod.fst = List.replicate rows.length v)
    (match_occurrence : ∀ x ∈ rows, x.1=v → x.2=p) :
    sumMass rows = copies p rows.length := by
  apply sum_identical L rows v p
  intro x hx
  have hm : x.1 ∈ rows.map Prod.fst := List.mem_map_of_mem (f := Prod.fst) hx
  rw [label] at hm
  have eq := (List.mem_replicate.mp hm).2
  exact ⟨eq, match_occurrence x hx eq⟩

/-- Sharp zero support returns exactly zero weight from any padding block. -/
private theorem zero_block (L : Laws R) (rows : List (Int × R))
    (label : rows.map Prod.fst = List.replicate rows.length (0:Int))
    (sharp : ∀ x ∈ rows, x.1=0 → x.2=0) : sumMass rows = 0 := by
  rw [mass_block L rows 0 0 label sharp]
  have all_zero (k : Nat) : copies (0:R) k = 0 := by
    induction k with
    | zero => rfl
    | succ k ih => simp [copies, ih, L.add_zero]
  exact all_zero _

/-- Cross-table calibration for any entry of an actual input of squared
integer length 2^t. The uniform reference has exactly 2^t unit numerators.
The calibrator has the signed numerator n, 2^t-|n|² ones, and arbitrary
zero padding. All unit occurrences are protected against the same reference
mass u. For the signed target and every unit occurrence, the supplied joint
marginals witness protection and symmetry on equal entries. -/
theorem normalized_coordinate (L : Laws R) (t : Nat) (input : List Int)
    (n : Int) (p u whole : R) (input_norm : sqCounts input = 2^t) (mem : n ∈ input)
    (uniform uniformZeros ones zeros : List (Int × R)) (distinguished : R)
    (uniform_size : uniform.length=2^t) (ones_size : ones.length=2^t-n.natAbs^2)
    (uniform_labels : uniform.map Prod.fst = List.replicate uniform.length 1)
    (ones_labels : ones.map Prod.fst = List.replicate ones.length 1)
    (uniform_padding : uniformZeros.map Prod.fst = List.replicate uniformZeros.length 0)
    (padding : zeros.map Prod.fst = List.replicate zeros.length 0)
    (common_units : ∀ x ∈ uniform++ones, JointComparison x.1 1 x.2 u)
    (sharp_zero : ∀ x ∈ uniformZeros++zeros, x.1=0 → x.2=0)
    (compared : JointComparison n n p distinguished)
    (uniform_normalization : sumMass (uniform++uniformZeros)=whole)
    (calibrator_normalization : sumMass ((n,distinguished)::(ones++zeros))=whole) :
    copies p (2^t) = copies whole (n.natAbs^2) := by
  have bound := entry_bound input n mem
  rw [input_norm] at bound
  have match_n := equal_coordinate rfl compared
  have um := mass_block L uniform 1 u uniform_labels
    (fun x hx eq => equal_coordinate eq (common_units x (by simp [hx])))
  have om := mass_block L ones 1 u ones_labels
    (fun x hx eq => equal_coordinate eq (common_units x (by simp [hx])))
  have uz := zero_block L uniformZeros uniform_padding (fun x hx => sharp_zero x (by simp [hx]))
  have cz := zero_block L zeros padding (fun x hx => sharp_zero x (by simp [hx]))
  have whole_uniform : copies u (2^t) = whole := by
    simpa only [sum_append L, um, uniform_size, uz, L.add_zero] using uniform_normalization
  have cal : p + copies u (2^t-n.natAbs^2) = whole := by
    simpa only [sumMass, sum_append L, om, ones_size, cz, L.add_zero, match_n] using calibrator_normalization
  have total : n.natAbs^2 + (2^t-n.natAbs^2) = 2^t := by omega
  have own_mass : p = copies u (n.natAbs^2) := by
    apply L.cancel _ _ (copies u (2^t-n.natAbs^2))
    rw [cal, ← split_copies L, total, whole_uniform]
  rw [own_mass, ← whole_uniform, mul_copies L, mul_copies L, Nat.mul_comm]

private theorem sum_diff_sq (x y : Int) :
    (x+y)*(x+y)+(x-y)*(x-y) = 2*(x*x+y*y) := by
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  omega

/-- A matched-parity integer pair at denominator sqrt(2^t) is the
Hadamard image of the recovered pair at denominator sqrt(2^(t-1)).
The numerator sum of squares halves exactly in the reverse direction. -/
theorem parity_fold (a b : Int) (same_parity : a%2=b%2) :
    let x := (a+b)/2
    let y := (a-b)/2
    x+y=a ∧ x-y=b ∧ 2*(x*x+y*y)=a*a+b*b := by
  dsimp only
  have plus : (a+b)/2+(a-b)/2=a := by omega
  have minus : (a+b)/2-(a-b)/2=b := by omega
  refine ⟨plus, minus, ?_⟩
  rw [← sum_diff_sq, plus, minus]

end CoherentComparison

#print axioms CoherentComparison.normalized_coordinate
#print axioms CoherentComparison.equal_coordinate
#print axioms CoherentComparison.parity_fold
