import Std

/-!
# Arithmetic of the finite three-sheet return source and radial Bell test

Integers and pairs of integers represent exact amplitudes in the Eisenstein
ring, with w a primitive cube root and w²+w+1=0. All endpoint normalizations
are kept outside the sums; no floating-point evaluation enters the checks.
-/
namespace RadialBell

structure E where
  a : Int
  b : Int
  deriving DecidableEq, Repr

def plus (z u : E) : E := ⟨z.a+u.a,z.b+u.b⟩
def minus (z : E) : E := ⟨-z.a,-z.b⟩
def times (z u : E) : E :=
  ⟨z.a*u.a-z.b*u.b,z.a*u.b+z.b*u.a-z.b*u.b⟩
def conj (z : E) : E := ⟨z.a-z.b,-z.b⟩
def root (k : Int) : E :=
  if k%3=0 then ⟨1,0⟩ else if k%3=1 then ⟨0,1⟩ else ⟨-1,-1⟩

private def labels := [false,true]
private def dir (left : Bool) : Int := if left then -1 else 1

/-- In the two joint return steps each coin reverses at its intermediate
position; no negative L-to-L edge is traversed. The common sheet receives
both intermediate positions and one extra count when they coincide. -/
def source (a b : Bool) : E :=
  let x := -dir a
  let y := -dir b
  root (x+y+(if x=y then 1 else 0))

def sourceNorm : E :=
  (labels.flatMap (fun a => labels.map fun b =>
     times (conj (source a b)) (source a b))).foldr plus ⟨0,0⟩

theorem source_norm : sourceNorm = ⟨4,0⟩ := by decide +kernel

def Matrix := Bool → Bool → E

def correlate (A B : Matrix) : E :=
  (labels.flatMap (fun a => labels.flatMap (fun b =>
    labels.flatMap (fun i => labels.map fun j =>
      times (conj (source a b)) (times (A a i) (times (B b j) (source i j))))))).foldr plus ⟨0,0⟩

def xAxis : Matrix := fun a i => if a==i then ⟨0,0⟩ else ⟨1,0⟩
def zAxis : Matrix := fun a i => if a != i then ⟨0,0⟩ else ⟨dir a,0⟩

theorem xz_correlations :
    correlate xAxis xAxis = ⟨1,0⟩ ∧ correlate zAxis zAxis = ⟨0,0⟩ ∧
    correlate xAxis zAxis = ⟨-3,0⟩ ∧ correlate zAxis xAxis = ⟨-3,0⟩ := by decide +kernel

def negative (A : Matrix) : Matrix := fun a b => minus (A a b)

/-- Matrix for √3 Y, represented within the same exact coefficient ring.
For the convention w = exp(-2πi/3), i√3=-1-2w. -/
def root3YAxis : Matrix := fun a b =>
  if a==b then ⟨0,0⟩ else if a then ⟨-1,-2⟩ else ⟨1,2⟩

theorem source_y : correlate zAxis root3YAxis = ⟨-3,0⟩ ∧
    correlate xAxis root3YAxis = ⟨-3,0⟩ := by decide +kernel

/-- Unnormalized meeting matrix. Bob's positive arm has acquired q sheets,
the negative arm -q. The old direction determines the output row and the
two physical signs reduce to one parity after removing a common phase. The
single Hadamard split supplies the final unit normalization 1/√2. -/
def gate (q : Nat) (lastInward relativeMinus : Bool) : Matrix := fun out input =>
  if out == lastInward then root (q:Int)
  else if xor input relativeMinus then minus (root (-(q:Int))) else root (-(q:Int))

def pulled (G B : Matrix) : Matrix := fun i j =>
  (labels.flatMap (fun a => labels.map (fun b =>
    times (conj (G a i)) (times (B a b) (G b j))))).foldr plus ⟨0,0⟩

def onSettingSum (B : Matrix) : E :=
  plus (correlate zAxis B) (correlate xAxis B)

def meetingScore (q : Nat) (lastInward relativeMinus : Bool) : Nat :=
  let G := gate q lastInward relativeMinus
  max ((onSettingSum (pulled G xAxis)).a.natAbs)
      ((onSettingSum (pulled G zAxis)).a.natAbs)

private def choice (q : Nat) (i parity : Bool) : Matrix :=
  let G := gate q i parity
  let x := pulled G xAxis
  let z := pulled G zAxis
  let B := if (onSettingSum x).a.natAbs > (onSettingSum z).a.natAbs then x else z
  if (onSettingSum B).a < 0 then negative B else B

private def chosen (q : Nat) : Matrix := choice q false false

theorem chosen_observable_agrees :
    [0,1,2].all (fun q => labels.all (fun i => labels.all (fun p =>
      labels.all (fun a => labels.all (fun b => decide (choice q i p a b = chosen q a b)))))) = true := by
  decide +kernel

/-- Outcome-sign relabelling eliminates any dependence of the two individual
correlations on the other excursion data, once q is specified. -/
private def aliceOnBob (q : Nat) (isX : Bool) : Int :=
  (correlate (if isX then xAxis else zAxis) (chosen q)).a

/-- Units 1/8: source norm 4, return-gate norm 2. The sign of each local
port may be relabelled, hence the greater of the two absolute correlations.
All twelve physically different phase/permutation/sign cases are evaluated. -/
theorem endpoint_score_table :
    [0,1,2].all (fun q => labels.all (fun last => labels.all (fun parity =>
       meetingScore q last parity == [6,9,4][q]!))) = true := by decide +kernel

theorem direct_and_timeout :
    plus (correlate zAxis (negative xAxis)) (minus (correlate xAxis (negative xAxis))) = ⟨4,0⟩ ∧
    onSettingSum (negative xAxis) = ⟨2,0⟩ := by decide +kernel

/- A count occupies three cyclic sheet-gain residues at each radius. An
absorbed word is doubled at subsequent ticks to share a single denominator
with late words. An active word moves once in each direction; its sheet
residue shifts by its departure radius before the move. -/
structure Triple where
  zero : Nat
  one : Nat
  two : Nat
  deriving DecidableEq, Repr

private def sum (a b : Triple) : Triple := ⟨a.zero+b.zero,a.one+b.one,a.two+b.two⟩
private def twice (a : Triple) := sum a a
private def shifted (k : Nat) (a : Triple) :=
  if k%3=0 then a else if k%3=1 then ⟨a.two,a.zero,a.one⟩ else ⟨a.one,a.two,a.zero⟩

structure Counts where
  low : Triple
  r1 : Triple
  r2 : Triple
  r3 : Triple
  r4 : Triple
  r5 : Triple
  high : Triple
  deriving Repr

private def empty : Triple := ⟨0,0,0⟩
private def start : Counts := ⟨empty,⟨1,0,0⟩,empty,empty,empty,empty,empty⟩

private def tick (c : Counts) : Counts :=
  let a := shifted 1 c.r1
  let b := shifted 2 c.r2
  let d := shifted 3 c.r3
  let e := shifted 4 c.r4
  let f := shifted 5 c.r5
  ⟨sum (twice c.low) a,b,sum a d,sum b e,sum d f,e,sum f (twice c.high)⟩

private def counts : Nat → Counts
  | 0 => start
  | n+1 => tick (counts n)

private def totals (t : Triple) := t.zero+t.one+t.two
private def active (c : Counts) := totals c.r1+totals c.r2+totals c.r3+totals c.r4+totals c.r5
private def hit (c : Counts) : Triple := sum c.low c.high

private theorem mass_tick (c : Counts) :
    totals (hit (tick c)) + active (tick c) = 2*(totals (hit c)+active c) := by
  simp [totals,hit,tick,active,shifted,twice,sum]
  omega

/-- Every active and absorbed word is retained, at every deadline. -/
theorem mass_all (n : Nat) : totals (hit (counts n)) + active (counts n) = 2^n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [counts,mass_tick,ih,Nat.pow_succ,Nat.mul_comm]

private def b0Eighths (c : Counts) :=
  let m := hit c
  6*m.zero + 9*m.one + 4*m.two + 4*active c

private def individualB0 (isX : Bool) (c : Counts) : Int :=
  let m := hit c
  (m.zero:Int)*aliceOnBob 0 isX + (m.one:Int)*aliceOnBob 1 isX +
    (m.two:Int)*aliceOnBob 2 isX +
    (active c:Int)*2*(correlate (if isX then xAxis else zAxis) (negative xAxis)).a

/-- Deadline at radial tick 24 = the initial split and 23 fair binary updates.
The numerator uses unit 1/(8·2²³). B1 contributes exactly 1. -/
theorem finite_chsh :
    active (counts 23) = 177147 ∧
    b0Eighths (counts 23) = 67394571 ∧
    b0Eighths (counts 23) + 8*2^23 = 134503435 ∧
    2*(8*2^23) < 134503435 ∧ 8*2^23 = 67108864 := by decide +kernel

theorem exact_correlations :
    hit (counts 23) = ⟨1339052,6232407,640002⟩ ∧
    individualB0 false (counts 23) = 23600115 ∧
    individualB0 true (counts 23) = 43794456 ∧
    correlate zAxis (negative xAxis) = ⟨3,0⟩ ∧
    correlate xAxis (negative xAxis) = ⟨-1,0⟩ := by decide +kernel

end RadialBell
