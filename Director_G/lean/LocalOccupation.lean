import Std

/-!
# Exterior-square update for a local two-mode gate

The polynomial proof uses only the displayed commutative scalar laws, which
hold in particular for complex numbers. Ordered mode indices are integers;
cell labels and scalar sites are distinct concepts. No continuum limit here.
-/
namespace LocalOccupation

structure Scalars (A : Type) where
  add : A → A → A
  mul : A → A → A
  sub : A → A → A
  assoc : ∀ a b c, mul (mul a b) c = mul a (mul b c)
  comm : ∀ a b, mul a b = mul b a
  addMul : ∀ a b c, mul (add a b) c = add (mul a c) (mul b c)
  mulSub : ∀ a b c, mul a (sub b c) = sub (mul a b) (mul a c)
  subSub : ∀ a b c d, sub (sub a b) (sub c d) = sub (add a d) (add b c)
  regroup : ∀ a b c d, sub (add a b) (add c d) = add (sub a c) (sub b d)
  addCancel : ∀ a b c, sub (add a b) (add a c) = sub b c
  addComm : ∀ a b, add a b = add b a

variable (R : Scalars A)

def wedge (f g : Int → A) (x y : Int) := R.sub (R.mul (f x) (g y)) (R.mul (g x) (f y))

def row (a b u v : A) := R.add (R.mul a u) (R.mul b v)

theorem mulAdd (a b c : A) : R.mul a (R.add b c) = R.add (R.mul a b) (R.mul a c) := by
  rw [R.comm,R.addMul,R.comm b a,R.comm c a]

theorem swap_inner (a b c : A) : R.mul a (R.mul b c) = R.mul b (R.mul a c) := by
  rw [←R.assoc,R.comm a b,R.assoc]

theorem product4 (a b c d : A) :
    R.mul (R.mul a b) (R.mul c d) = R.mul (R.mul a c) (R.mul b d) := by
  rw [R.assoc,R.assoc,swap_inner R b c]

theorem row_left (a b u v U V s t : A) :
    R.sub (R.mul (row R a b u v) t) (R.mul (row R a b U V) s) =
    row R a b (R.sub (R.mul u t) (R.mul U s)) (R.sub (R.mul v t) (R.mul V s)) := by
  simp only [row,R.addMul,R.assoc,R.mulSub,R.regroup]

theorem row_right (a b u v U V s t : A) :
    R.sub (R.mul s (row R a b U V)) (R.mul t (row R a b u v)) =
    row R a b (R.sub (R.mul s U) (R.mul t u)) (R.sub (R.mul s V) (R.mul t v)) := by
  rw [R.comm s,R.comm t,row_left,R.comm U s,R.comm u t,R.comm V s,R.comm v t]

theorem det_gate (a b c d u v U V : A) :
    R.sub (R.mul (row R a b u v) (row R c d U V))
          (R.mul (row R a b U V) (row R c d u v)) =
    R.mul (R.sub (R.mul a d) (R.mul b c)) (R.sub (R.mul u V) (R.mul U v)) := by
  let a0 := R.mul (R.mul a c) (R.mul u U)
  let d0 := R.mul (R.mul b d) (R.mul v V)
  let A1 := R.mul (R.mul a d) (R.mul u V)
  let A2 := R.mul (R.mul a d) (R.mul U v)
  let B1 := R.mul (R.mul b c) (R.mul u V)
  let B2 := R.mul (R.mul b c) (R.mul U v)
  have lhs :
      R.sub (R.mul (row R a b u v) (row R c d U V))
        (R.mul (row R a b U V) (row R c d u v)) =
      R.sub (R.add (R.add a0 A1) (R.add B2 d0)) (R.add (R.add a0 A2) (R.add B1 d0)) := by
    simp only [row,R.addMul,mulAdd,product4 R a u,product4 R b v,
      product4 R a U,product4 R b V]
    change _ = R.sub (R.add (R.add _ _) (R.add _ _)) (R.add (R.add _ _) (R.add _ _))
    simp only [a0,d0,A1,A2,B1,B2,R.comm U u,R.comm v U,R.comm V u,R.comm V v]
  rw [lhs,R.regroup,R.addCancel,R.addComm B2 d0,R.addComm B1 d0,R.addCancel]
  rw [R.comm (R.sub (R.mul a d) (R.mul b c)),R.mulSub,R.comm _ (R.mul a d),
    R.comm _ (R.mul b c),R.mulSub,R.mulSub]
  change R.add (R.sub A1 A2) (R.sub B2 B1) = R.sub (R.sub A1 A2) (R.sub B1 B2)
  rw [R.subSub,R.regroup]

structure Gate (A : Type) where
  a : A
  b : A
  c : A
  d : A

def advance (G : Gate A) (i : Int) (f : Int → A) (x : Int) :=
  if x=i then row R G.a G.b (f i) (f (i+1))
  else if x=i+1 then row R G.c G.d (f i) (f (i+1)) else f x

def occupation (G : Gate A) (i : Int) (F : Int → Int → A) (x y : Int) :=
  if x=i ∧ y=i+1 then R.mul (R.sub (R.mul G.a G.d) (R.mul G.b G.c)) (F i (i+1))
  else if x=i then row R G.a G.b (F i y) (F (i+1) y)
  else if x=i+1 then row R G.c G.d (F i y) (F (i+1) y)
  else if y=i then row R G.a G.b (F x i) (F x (i+1))
  else if y=i+1 then row R G.c G.d (F x i) (F x (i+1)) else F x y

theorem physical_minor (G : Gate A) (i : Int) (f g : Int → A) (x y : Int) (ordered : x<y) :
    wedge R (advance R G i f) (advance R G i g) x y =
    occupation R G i (wedge R f g) x y := by
  unfold wedge advance occupation
  have adj : i+1≠i := by omega
  by_cases xi : x=i
  · by_cases yi : y=i+1
    · simp [xi,yi,adj,det_gate]
    · have h : y≠i := by omega
      simp [xi,h,yi,row_left]
  by_cases xi1 : x=i+1
  · have yi : y≠i := by omega
    have yi1 : y≠i+1 := by omega
    simp [xi,xi1,yi,yi1,adj,row_left]
  by_cases yi : y=i
  · simp [xi,xi1,yi,row_right]
  by_cases yi1 : y=i+1
  · simp [xi,xi1,yi,yi1,adj,row_right]
  · simp [xi,xi1,yi,yi1]

abbrev Gaussian := Int × Int
def plus (z w : Gaussian) : Gaussian := (z.1+w.1,z.2+w.2)
def times (z w : Gaussian) : Gaussian := (z.1*w.1-z.2*w.2,z.1*w.2+z.2*w.1)
def diff (z w : Gaussian) : Gaussian := (z.1-w.1,z.2-w.2)

def gaussian : Scalars Gaussian where
  add := plus
  mul := times
  sub := diff
  assoc a b c := by
    apply Prod.ext <;> simp only [times,Int.add_mul,Int.sub_mul,Int.mul_add,Int.mul_sub,Int.mul_assoc]
    all_goals omega
  comm a b := by
    apply Prod.ext <;> simp only [times]
    all_goals simp only [Int.mul_comm b.1 a.1,Int.mul_comm b.2 a.2,
      Int.mul_comm b.1 a.2,Int.mul_comm b.2 a.1] <;> omega
  addMul a b c := by apply Prod.ext <;> simp [times,plus,Int.add_mul] <;> omega
  mulSub a b c := by apply Prod.ext <;> simp [times,diff,Int.mul_sub] <;> omega
  subSub a b c d := by apply Prod.ext <;> dsimp [diff,plus] <;> omega
  regroup a b c d := by apply Prod.ext <;> dsimp [diff,plus] <;> omega
  addCancel a b c := by apply Prod.ext <;> dsimp [diff,plus] <;> omega
  addComm a b := by apply Prod.ext <;> dsimp [plus] <;> omega

/-- Hopping numerators, with common denominator 5 for one orbital and
25 in the two-occupied minor. Restoring the latter gives determinant one. -/
def alpha : Gate Gaussian := ⟨(3,0),(0,-4),(0,-4),(3,0)⟩
def beta : Gate Gaussian := ⟨(4,0),(0,3),(0,3),(4,0)⟩
def det (G : Gate Gaussian) := diff (times G.a G.d) (times G.b G.c)

theorem normalized_gate_determinants : det alpha = (25,0) ∧ det beta = (25,0) := by decide

theorem gaussian_minor (G : Gate Gaussian) (i : Int) (f g : Int → Gaussian)
    (x y : Int) (ordered : x<y) :
    wedge gaussian (advance gaussian G i f) (advance gaussian G i g) x y =
    occupation gaussian G i (wedge gaussian f g) x y :=
  physical_minor gaussian G i f g x y ordered

end LocalOccupation
