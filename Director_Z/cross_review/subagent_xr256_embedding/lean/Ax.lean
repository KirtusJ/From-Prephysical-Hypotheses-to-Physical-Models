import Std

/-! Exact finite certificate for the parity-addressed nine-tick walk.
A pair (a,b) denotes a+b√2. Each tick omits the common amplitude divisor √2,
so the three recorded block masses below have divisors 8, 64 and 512.
The order test chooses the ordinary positive real √2. For opposite-signed
coefficients it compares a² and 2b², both integers. The final finite
enumerations use Lean's native evaluator. -/

namespace AddressedCoinEmbedding

abbrev Q2 := Int × Int
abbrev Spin := Q2 × Q2
abbrev Field := Nat → Spin

def plus (x y : Q2) : Q2 := (x.1 + y.1, x.2 + y.2)
def minus (x y : Q2) : Q2 := (x.1 - y.1, x.2 - y.2)
def neg (x : Q2) : Q2 := (-x.1, -x.2)
def conj (x : Q2) : Q2 := (x.1, -x.2)
def rootTimes (x : Q2) : Q2 := (2*x.2, x.1)
def times (x y : Q2) : Q2 :=
  (x.1*y.1 + 2*x.2*y.2, x.1*y.2 + x.2*y.1)
def mass (s : Spin) : Q2 := plus (times s.1 s.1) (times s.2 s.2)

/-- Conjugation preserves the squared, pooled real norm algebraically. -/
theorem mass_conjugate (r l : Q2) :
    mass (conj r, conj l) = conj (mass (r,l)) := by
  rcases r with ⟨a,b⟩
  rcases l with ⟨c,d⟩
  simp [mass, times, plus, conj, Int.mul_neg, Int.neg_mul, Int.neg_add]

def zero : Q2 := (0,0)
def fromSite (x : Nat) (s : Spin) : Field :=
  fun j => if j = x then s else (zero,zero)
def launch : Field := fromSite 0 ((1,0),zero)

/-- After scaling a tick by positive √2, H contributes integer ±1 entries.
The conjugate implementation changes H to -H but keeps even-address X fixed. -/
def coin (flipH addressed : Bool) (x : Nat) (s : Spin) : Spin :=
  if addressed && x % 2 == 0 then (rootTimes s.2, rootTimes s.1)
  else
    let hr := plus s.1 s.2
    let hl := minus s.1 s.2
    if flipH then (neg hr,neg hl) else (hr,hl)

/-- A right rail stays at its left-step address; a left rail arrives from j−1. -/
def tick (flipH addressed : Bool) (f : Field) : Field := fun j =>
  let prev := (j+3)%4
  ((coin flipH addressed j (f j)).1, (coin flipH addressed prev (f prev)).2)

def flight (flipH : Bool) (f : Field) : Field :=
  tick flipH false (tick flipH true (tick flipH false f))

/-- A written address projects onto that site and keeps BOTH incoming rails.
The spin is left unnormalized, so word masses use the original launch ensemble. -/
def after (flipH : Bool) : List Nat → Field
  | [] => launch
  | j :: rest => fun k =>
    let f := after flipH rest
    fromSite j (flight flipH f j) k

def weight (flipH : Bool) (history : List Nat) : Q2 :=
  match history.reverse with
  | [] => (1,0)
  | j :: revPrefix => mass (flight flipH (after flipH revPrefix) j)

def positive (x : Q2) : Bool :=
  if x.1 ≥ 0 then
    if x.2 ≥ 0 then x != zero else x.1*x.1 > 2*x.2*x.2
  else
    x.2 > 0 && 2*x.2*x.2 > x.1*x.1

def gt (x y : Q2) : Bool := positive (minus x y)
def sites : List Nat := [0,1,2,3]
def children (h : List Nat) : List (List Nat) := sites.map (fun j => h ++ [j])
def words2 := sites.flatMap (fun j => children [j])
def words3 := words2.flatMap children

theorem first_write :
    sites.map (fun x => weight false [x]) = [(0,0),(3,2),(4,-2),(1,0)] ∧
    sites.map (fun x => weight true  [x]) = [(0,0),(3,-2),(4,2),(1,0)] := by
  decide

set_option maxRecDepth 8000

/-- Every named word, including the 37 dark ones, conjugates under the
physical H-sign change. Both embeddings remain positive on exactly 27 words. -/
theorem all_words :
    words3.length = 64 ∧
    words3.all (fun w => weight true w == conj (weight false w)) = true ∧
    (words3.filter (fun w => positive (weight false w))).length = 27 ∧
    (words3.filter (fun w => positive (weight true w))).length = 27 ∧
    (words3.filter (fun w => weight false w == zero)).length = 37 ∧
    words3.foldl (fun n w => plus n (weight false w)) zero = (512,0) := by
  native_decide

/-- Along (2,3,1) each conjugate branch strictly dominates its siblings;
the final word also strictly dominates all other words globally. -/
theorem selected_conjugate_maxima :
    [[0],[1],[3]].all (fun h => gt (weight true [2]) (weight true h)) = true ∧
    [[2,0],[2,1],[2,2]].all
      (fun h => gt (weight true [2,3]) (weight true h)) = true ∧
    (words3.filter (fun w => w != [2,3,1])).all
      (fun w => gt (weight true [2,3,1]) (weight true w)) = true := by
  native_decide

/-- The three exact siblings establish m²<lh and 2l<m, the comparisons
used by the log-tangent separation argument. Its analytic inequality and
the assumptions connecting the record to a detector are outside this file. -/
theorem selected_weights :
    let l := weight false [2,3,1]
    let m := weight false [2,3,3]
    let h := weight false [2,3,0]
    l = (86,-60) ∧ m = (18,-8) ∧ h = (40,4) ∧
    gt m l = true ∧ gt h m = true ∧
    gt (times l h) (times m m) = true ∧ gt m (plus l l) = true := by
  native_decide

end AddressedCoinEmbedding

#print axioms AddressedCoinEmbedding.mass_conjugate
#print axioms AddressedCoinEmbedding.first_write
#print axioms AddressedCoinEmbedding.all_words
#print axioms AddressedCoinEmbedding.selected_conjugate_maxima
#print axioms AddressedCoinEmbedding.selected_weights
