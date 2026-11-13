import Std

/-!
Finite reference checks. A permutation of spectral labels must act on the
labelled input and effect together. The separate three-site calculation admits
a phase-fixed coherent choice between a bypass and three full Hadamard steps.
-/
namespace InternalReference

/-- Multiplying both the unit root exponent by a and its named eigenlabel by
an inverse b preserves every physical power of that eigenvalue. -/
theorem root_label_cancellation (m a b r d : Nat)
    (hab : (a*b) % m = 1) :
    (a*(b*r)*d) % m = (r*d) % m := by
  have group : a*(b*r)*d = (a*b)*(r*d) := by
    simp [Nat.mul_assoc]
  rw [group, Nat.mul_mod, hab]
  simp [Nat.mod_mod]

/-- For a finite list of signed sheet counts this identity holds for the
entire evaluated sum, with coefficients and any choice of value table. -/
theorem path_sum_cancellation (m a b r : Nat)
    (hab : (a*b) % m = 1) (value : Nat → Int) (counts : List (Nat × Int)) :
    (counts.map (fun p => p.2 * value ((a*(b*r)*p.1) % m))).sum =
    (counts.map (fun p => p.2 * value ((r*p.1) % m))).sum := by
  induction counts with
  | nil => rfl
  | cons p rest ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [root_label_cancellation m a b r p.1 hab, ih]

/-- With root exponent doubled modulo 5, holding the abstract index fixed
changes the eigenvalue exponent; inverse relabelling restores it. -/
theorem five_sheet_named_control :
    ((2*1*1) % 5 : Nat) ≠ (1*1) % 5 ∧ ((2*(3*1)*1) % 5 : Nat) = (1*1) % 5 := by
  decide +kernel

/-- On residues in [0,m), mirror distances either choose the same residue
or a pair whose sum is m; the redundant possibility for zero is harmless. -/
def fold (m u : Int) : Int := min (u % m) ((-u) % m)

private theorem negate_residues (m a b : Int) (hab : a%m = b%m) : (-a)%m = (-b)%m := by
  calc
    (-a)%m = (0-a%m)%m := by rw [Int.sub_emod_emod, Int.zero_sub]
    _ = (0-b%m)%m := by rw [hab]
    _ = (-b)%m := by rw [Int.sub_emod_emod, Int.zero_sub]

private theorem fold_class (m u v : Int)
    (same : fold m u = fold m v) :
    u % m = v % m ∨ u % m = (-v) % m := by
  unfold fold at same
  rcases Int.le_total (u % m) ((-u) % m) with h | h <;>
    rcases Int.le_total (v % m) ((-v) % m) with k | k
  · rw [Int.min_eq_left h, Int.min_eq_left k] at same
    exact Or.inl same
  · rw [Int.min_eq_left h, Int.min_eq_right k] at same
    exact Or.inr same
  · rw [Int.min_eq_right h, Int.min_eq_left k] at same
    right
    simpa only [Int.neg_neg] using negate_residues m (-u) v same
  · rw [Int.min_eq_right h, Int.min_eq_right k] at same
    left
    simpa only [Int.neg_neg] using negate_residues m (-u) (-v) same

/-- Distances from adjacent named references determine the oriented residue.
The result also holds for even moduli above two. -/
theorem folded_neighbours_determine (m u v : Int) (hm : 2 < m)
    (atZero : fold m u = fold m v)
    (atNext : fold m (u+1) = fold m (v+1)) : u % m = v % m := by
  rcases fold_class m u v atZero with eq | reflected
  · exact eq
  rcases fold_class m (u+1) (v+1) atNext with eq | twice
  · exact (Int.emod_add_cancel_right 1).mp eq
  · have shifted := Int.add_emod_eq_add_emod_right 1 reflected
    have both := shifted.symm.trans twice
    have lhs : -v+1 = 1+ -v := by omega
    have rhs : -(v+1) = -1+ -v := by omega
    rw [lhs,rhs] at both
    have impossible := (Int.emod_add_cancel_right (-v)).mp both
    have zero := Int.emod_eq_emod_iff_emod_sub_eq_zero.mp impossible
    change (2:Int) % m = 0 at zero
    rw [Int.emod_eq_of_lt (by decide) hm] at zero
    omega

/-- One reference leaves a reversal ambiguity even at order five. -/
theorem one_fold_misses_orientation :
    fold 5 1 = fold 5 4 ∧ fold 5 (1+1) ≠ fold 5 (4+1) := by decide

structure Cell where
  x : Int
  dir : Int
  sheet : Int
  deriving DecidableEq, Repr

def source : Cell := ⟨1,1,0⟩
def output (v : Cell) (d : Int) : Cell :=
  ⟨(v.x+d)%3, d, (v.sheet+v.x)%3⟩
def coinSign (old newDir : Int) : Int :=
  if old = -1 ∧ newDir = -1 then -1 else 1

def signedStep (s : List (Cell × Int)) : List (Cell × Int) :=
  s.flatMap fun (v,n) => ([1,-1] : List Int).map fun d => (output v d, n*coinSign v.dir d)

def threeSteps := signedStep (signedStep (signedStep [(source,1)]))
def pathsAt (s : List (Cell × Int)) (cell : Cell) :=
  s.filter fun p => p.1 == cell
def countAt (s : List (Cell × Int)) (cell : Cell) : Int :=
  ((pathsAt s cell).map Prod.snd).sum
def allCells : List Cell :=
  ([0,1,2] : List Int).flatMap fun x =>
  ([1,-1] : List Int).flatMap fun d =>
  ([0,1,2] : List Int).map fun y => ⟨x,d,y⟩

/-- Only one three-tick history returns to the initially occupied full cell;
the squared sum of coherent integer endpoint counts is eight. -/
theorem odd_ring_return :
    (pathsAt threeSteps source) = [(source,1)] ∧
    (allCells.map (fun v => (countAt threeSteps v)^2)).sum = 8 := by
  decide +kernel

/-- a+b sqrt(2) with the displayed integer denominator tracked separately. -/
structure Quad where
  a : Int
  b : Int
  deriving DecidableEq, Repr

def add (x y : Quad) : Quad := ⟨x.a+y.a, x.b+y.b⟩
def square (x : Quad) : Quad := ⟨x.a*x.a+2*x.b*x.b, 2*x.a*x.b⟩
def sigma (x : Quad) : Quad := ⟨x.a,-x.b⟩
def total (items : List Quad) : Quad := items.foldr add ⟨0,0⟩

/-- In units of 1/8, a bypass at the source contributes 4 and each three-step
integer walk amplitude contributes sqrt(2). The sign is the output port of
the recombined two-level control; every entry explicitly uses the walked cell. -/
def coherentPort (port : Int) : Quad :=
  total (allCells.map fun cell =>
    square ⟨if cell=source then 4 else 0, port*countAt threeSteps cell⟩)

/-- Orthogonal tags of bypass and active histories prevent this cross term.
Squared branch contributions carry the same denominator 64. -/
def markedPort : Quad :=
  total (allCells.map fun cell =>
    add (square ⟨if cell=source then 4 else 0,0⟩)
        (square ⟨0,countAt threeSteps cell⟩))

theorem clock_port_probabilities :
    coherentPort 1 = ⟨32,8⟩ ∧ coherentPort (-1) = ⟨32,-8⟩ ∧
    add (coherentPort 1) (coherentPort (-1)) = ⟨64,0⟩ ∧
    sigma (coherentPort 1) = coherentPort (-1) ∧
    markedPort = ⟨32,0⟩ ∧ sigma markedPort = markedPort := by
  decide +kernel

end InternalReference
