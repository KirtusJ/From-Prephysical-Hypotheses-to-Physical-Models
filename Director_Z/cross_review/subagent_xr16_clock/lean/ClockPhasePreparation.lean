import Std

/-!
# An eight-sheet clock herald followed by ten balanced ticks

All arrays below contain signed integer amplitudes. The initial odd herald and
every reference tick omit their factors of 1/2. The launch and each walk tick
omit a factor of 1/√2. Site probabilities sum over both coins and all sheets.
-/
namespace ClockPhasePreparation

structure Sheet where
  a : Int
  b : Int
  c : Int
  d : Int
  e : Int
  f : Int
  g : Int
  h : Int
  deriving DecidableEq

def zero : Sheet := ⟨0,0,0,0,0,0,0,0⟩
def pulse : Sheet := ⟨1,0,0,0,0,0,0,0⟩

def add (x y : Sheet) : Sheet :=
  ⟨x.a+y.a,x.b+y.b,x.c+y.c,x.d+y.d,x.e+y.e,x.f+y.f,x.g+y.g,x.h+y.h⟩

def sub (x y : Sheet) : Sheet :=
  ⟨x.a-y.a,x.b-y.b,x.c-y.c,x.d-y.d,x.e-y.e,x.f-y.f,x.g-y.g,x.h-y.h⟩

def rot (x : Sheet) : Sheet := ⟨x.h,x.a,x.b,x.c,x.d,x.e,x.f,x.g⟩
def shift : Nat → Sheet → Sheet
  | 0, x => x
  | n+1, x => rot (shift n x)

def dot (x y : Sheet) : Int :=
  x.a*y.a + x.b*y.b + x.c*y.c + x.d*y.d + x.e*y.e + x.f*y.f + x.g*y.g + x.h*y.h

def mass (x : Sheet) := dot x x
def adjacent (x : Sheet) := 2 * dot x (rot x)
def oddSheet (a b c d : Int) : Sheet := ⟨a,b,c,d,-a,-b,-c,-d⟩

/-- A particular reference outcome, including an independently selectable sign
and a direction for its unit translation. The initial herald is always odd. -/
def prepare (positive : Bool) (unit : Nat) : Nat → Sheet
  | 0 => sub pulse (shift 4 pulse)
  | n+1 =>
    let s := prepare positive unit n
    if positive then add s (shift unit s) else sub s (shift unit s)

structure Cell where
  h : Sheet
  v : Sheet
  deriving DecidableEq

def depart (t plate : Nat) (p : Cell × Nat) : Cell :=
  let s := if 2*p.2 = t then plate else 0
  ⟨shift s (add p.1.h p.1.v),shift s (sub p.1.h p.1.v)⟩

def stream (previous : Sheet) : List Cell → List Cell
  | [] => [⟨zero,previous⟩]
  | p::rest => ⟨p.h,previous⟩ :: stream p.v rest

/-- At tick t list index j denotes the physical position 2*j−t. Both modes
departing the origin receive the plate shift on the same reference sheet. -/
def walk (seed : Sheet) (launch plate : Nat) : Nat → List Cell
  | 0 => [⟨seed, shift launch seed⟩]
  | t+1 => stream zero (((walk seed launch plate t).zipIdx).map (depart t plate))

def cellMass (p : Cell) := mass p.h + mass p.v
def allMass (xs : List Cell) : Int := (xs.map cellMass).sum
def totals (s : Sheet) (launch plate : Nat) : Int × Int :=
  let cells := walk s launch plate 10
  (cellMass (cells.getD 5 ⟨zero,zero⟩), allMass cells)

theorem direct_plus :
    [0,1,2,3].map (fun m => totals (prepare true 1 m) 6 3) =
    [(1376,4096),(4672,8192),(15936,24576),(54400,81920)] := by decide +kernel

theorem direct_minus :
    [0,1,2,3].map (fun m => totals (prepare false 1 m) 6 3) =
    [(1376,4096),(832,8192),(576,24576),(640,81920)] := by decide +kernel

theorem direct_controls :
    [0,1,2,3].map (fun m => totals (prepare true 7 m) 2 5) =
      [0,1,2,3].map (fun m => totals (prepare true 1 m) 6 3) ∧
    [0,1,2,3].map (fun m => totals (prepare true 1 m) 6 0) =
      [(288,4096),(576,8192),(1728,24576),(5760,81920)] := by decide +kernel

/-- Total squared-amplitude denominator of a single reference word and the
whole subsequent experimental branch, before conditioning on that word. -/
def referenceDenominator (m : Nat) : Nat := 4^(m+1)
def jointDenominator (m : Nat) : Nat := referenceDenominator m * 2^11

theorem reference_normalization :
    [0,1,2,3].map (fun m => (mass (prepare true 1 m), referenceDenominator m)) =
      [(2,4),(4,16),(12,64),(40,256)] ∧
    [0,1,2,3].map jointDenominator = [8192,32768,131072,524288] := by decide +kernel

theorem plus_transfer (a b c d : Int) :
    let x := oddSheet a b c d
    let y := add x (rot x)
    mass y = 2*mass x + adjacent x ∧ adjacent y = 2*adjacent x + 2*mass x := by
  dsimp [oddSheet, add, rot, mass, adjacent, dot]
  constructor <;> simp only [Int.sub_eq_add_neg, Int.add_mul, Int.mul_add,
    Int.neg_mul, Int.mul_neg, Int.neg_neg, Int.mul_comm] <;> omega

theorem minus_transfer (a b c d : Int) :
    let x := oddSheet a b c d
    let y := sub x (rot x)
    mass y = 2*mass x - adjacent x ∧ adjacent y = 2*adjacent x - 2*mass x := by
  dsimp [oddSheet, sub, rot, mass, adjacent, dot]
  constructor <;> simp only [Int.sub_eq_add_neg, Int.add_mul, Int.mul_add,
    Int.neg_mul, Int.mul_neg, Int.neg_neg, Int.mul_comm] <;> omega

/-- Every signed sheet operation used for launch or plate commutes with a
superposition of the first four translations. On the odd herald this
superposition spans every possible localized real-amplitude preparation. -/
def combine (a b c d : Int) : Int → Int → Int → Int → Int :=
  fun x y z w => a*x+b*y+c*z+d*w

def linear4 (a b c d : Int) (x y z w : Sheet) : Sheet :=
  let l := combine a b c d
  ⟨l x.a y.a z.a w.a,l x.b y.b z.b w.b,l x.c y.c z.c w.c,l x.d y.d z.d w.d,
   l x.e y.e z.e w.e,l x.f y.f z.f w.f,l x.g y.g z.g w.g,l x.h y.h z.h w.h⟩

def translate (a b c d : Int) (s : Sheet) : Sheet :=
  linear4 a b c d s (rot s) (shift 2 s) (shift 3 s)

private theorem tr_zero (a b c d : Int) : translate a b c d zero = zero := by
  simp [translate,linear4,combine,shift,rot,zero]

private theorem tr_add (a b c d : Int) (x y : Sheet) :
    translate a b c d (add x y) = add (translate a b c d x) (translate a b c d y) := by
  simp [translate,linear4,combine,shift,rot,add,Int.mul_add,Int.add_assoc,Int.add_left_comm,Int.add_comm]

private theorem tr_sub (a b c d : Int) (x y : Sheet) :
    translate a b c d (sub x y) = sub (translate a b c d x) (translate a b c d y) := by
  simp [translate,linear4,combine,shift,rot,sub,Int.mul_sub] <;> omega

private theorem tr_shift (a b c d : Int) (s : Sheet) (n : Nat) :
    translate a b c d (shift n s) = shift n (translate a b c d s) := by
  induction n with
  | zero => rfl
  | succ n ih => change rot (translate a b c d (shift n s)) = rot (shift n (translate a b c d s))
                 rw [ih]

private def liftCell (f : Sheet → Sheet) (p : Cell) : Cell := ⟨f p.h,f p.v⟩

private theorem tr_depart (a b c d : Int) (i t plate : Nat) (p : Cell) :
    let tr := translate a b c d
    depart t plate (liftCell tr p, i) = liftCell tr (depart t plate (p,i)) := by
  dsimp [depart, liftCell]
  rw [tr_shift, tr_shift, tr_add, tr_sub]

private theorem tr_layers (a b c d : Int) (t plate start : Nat) (xs : List Cell) :
    let f := liftCell (translate a b c d)
    (((xs.map f).zipIdx start).map (depart t plate)) =
      (((xs.zipIdx start).map (depart t plate)).map f) := by
  induction xs generalizing start with
  | nil => rfl
  | cons p ps ih =>
    dsimp only
    simp only [List.map_cons,List.zipIdx_cons]
    rw [tr_depart,ih]

private theorem tr_stream (a b c d : Int) (s : Sheet) (xs : List Cell) :
    let tr := translate a b c d
    stream (tr s) (xs.map (liftCell tr)) = (stream s xs).map (liftCell tr) := by
  induction xs generalizing s with
  | nil => simp [stream,liftCell,tr_zero]
  | cons p ps ih => simp [stream,liftCell,ih]

theorem translate_walk (a b c d : Int) (s : Sheet) (launch plate t : Nat) :
    let tr := translate a b c d
    walk (tr s) launch plate t = (walk s launch plate t).map (liftCell tr) := by
  induction t with
  | zero => simp [walk,liftCell,tr_shift]
  | succ n ih =>
    dsimp only
    rw [walk,walk,ih,tr_layers,← tr_zero a b c d,tr_stream,tr_zero]

def anchor := oddSheet 1 0 0 0
def anchorOrigin : Cell := ⟨oddSheet (-12) (-10) 0 10, oddSheet 0 10 12 10⟩

private theorem anchor_return : (walk anchor 6 3 10)[5]? = some anchorOrigin := by decide +kernel

private theorem tr_anchor (a b c d : Int) :
    translate a b c d anchor = oddSheet a b c d := by
  simp [translate,linear4,combine,shift,rot,anchor,oddSheet]

theorem odd_origin_cell (a b c d : Int) :
    (walk (oddSheet a b c d) 6 3 10)[5]? =
      some (liftCell (translate a b c d) anchorOrigin) := by
  rw [← tr_anchor, translate_walk,List.getElem?_map,anchor_return]
  rfl

private theorem coefficient_tail (a b n : Int) : a*(b*n) = n*(a*b) := by
  rw [Int.mul_comm b n, Int.mul_left_comm]

private theorem integer_coefficients :
    10*10=(100:Int) ∧ 10*12=(120:Int) ∧ 12*12=(144:Int) ∧ 2*480=(960:Int) := by decide

theorem odd_origin_numerator (a b c d : Int) :
    let s := oddSheet a b c d
    (totals s 6 3).1 = 688 * mass s + 480 * adjacent s := by
  dsimp only [totals]
  rw [List.getD_eq_getElem?_getD,odd_origin_cell]
  dsimp [liftCell,translate,linear4,combine,shift,rot,cellMass,mass,adjacent,dot,anchorOrigin,oddSheet]
  simp only [Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.add_mul, Int.mul_add,
    Int.mul_assoc, Int.sub_eq_add_neg, Int.neg_mul, Int.mul_neg, Int.neg_neg, Int.mul_comm,
    Int.mul_left_comm]
  have hc := integer_coefficients
  simp only [hc.1,hc.2.1,hc.2.2.1,hc.2.2.2,coefficient_tail _ _ 688,coefficient_tail _ _ 960,
    coefficient_tail _ _ 100,coefficient_tail _ _ 120,coefficient_tail _ _ 144]
  omega

private theorem shift_mass (n : Nat) (s : Sheet) : mass (shift n s) = mass s := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [shift,← ih]
    dsimp [mass,dot,rot]
    omega

private theorem split_mass (u v : Sheet) : mass (add u v) + mass (sub u v) = 2*(mass u+mass v) := by
  dsimp [add,sub,mass,dot]
  simp only [Int.add_mul,Int.mul_add,Int.sub_mul,Int.mul_sub]
  omega

private theorem depart_mass (t plate : Nat) (u : Cell × Nat) :
    cellMass (depart t plate u) = 2*cellMass u.1 := by
  dsimp [depart,cellMass]
  rw [shift_mass,shift_mass,split_mass]

private theorem layer_mass (t plate : Nat) (xs : List Cell) (i : Nat) :
    allMass ((xs.zipIdx i).map (depart t plate)) = 2 * allMass xs := by
  induction xs generalizing i with
  | nil => rfl
  | cons x xs ih =>
    change allMass (depart t plate (x,i) :: ((xs.zipIdx (i+1)).map (depart t plate))) =
      2 * (cellMass x + allMass xs)
    change cellMass (depart t plate (x,i)) + allMass ((xs.zipIdx (i+1)).map (depart t plate)) = _
    rw [depart_mass,ih]
    dsimp only
    omega

private theorem stream_mass (xs : List Cell) (s : Sheet) :
    allMass (stream s xs) = mass s + allMass xs := by
  induction xs generalizing s with
  | nil => simp [allMass,cellMass,stream,zero,mass,dot]
  | cons x xs ih =>
    change (mass x.h + mass s) + allMass (stream x.v xs) =
      mass s + (cellMass x + allMass xs)
    rw [ih]
    dsimp [cellMass]
    omega

theorem complete_walk_mass (s : Sheet) (launch plate t : Nat) :
    allMass (walk s launch plate t) = (2 : Int)^(t+1) * mass s := by
  induction t with
  | zero =>
    simp [walk,allMass,cellMass,shift_mass]
    omega
  | succ t ih =>
    rw [walk,stream_mass,layer_mass,ih]
    simp only [zero,mass,dot,Int.zero_mul,Int.zero_add,Int.pow_succ]
    rw [Int.mul_assoc (2^t*2) 2,Int.mul_left_comm]

private theorem prepared_is_odd (positive : Bool) (m : Nat) :
    ∃ a b c d, prepare positive 1 m = oddSheet a b c d := by
  induction m with
  | zero => exact ⟨1,0,0,0,rfl⟩
  | succ m ih =>
    obtain ⟨a,b,c,d,h⟩ := ih
    cases positive with
    | false =>
      refine ⟨a-(-d),b-a,c-b,d-c,?_⟩
      simp only [prepare,h,shift,sub,rot,oddSheet,Bool.false_eq_true,if_false]
      congr 1 <;> omega
    | true =>
      refine ⟨a+(-d),b+a,c+b,d+c,?_⟩
      simp only [prepare,h,shift,add,rot,oddSheet,if_true]
      congr 1 <;> omega

private theorem totals_second (s : Sheet) (launch plate : Nat) :
    (totals s launch plate).2 = 2048 * mass s := by
  simp only [totals,complete_walk_mass]
  rfl

/-- The integer numerator and denominator of the conditional squared record.
The input factor 1/2^(m+1) cancels in this ratio. This equality requires no
division or assumed positivity, including on any zero seed. -/
theorem prepared_origin (positive : Bool) (m : Nat) :
    let s := prepare positive 1 m
    totals s 6 3 = (688*mass s+480*adjacent s,2048*mass s) := by
  obtain ⟨a,b,c,d,h⟩ := prepared_is_odd positive m
  dsimp only
  apply Prod.ext
  · rw [h,odd_origin_numerator]
  · rw [totals_second]

end ClockPhasePreparation
