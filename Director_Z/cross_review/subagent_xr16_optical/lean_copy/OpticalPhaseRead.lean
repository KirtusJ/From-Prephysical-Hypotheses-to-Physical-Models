import Std

/-!
# Ten-step return of the phase-defect Hadamard walk

Coefficients are in the basis `1,z,z²,z³`, with `z⁴ = -1`. Setting `s`
means a departure phase `z^s` at site 0. Embedding `k` sends the named
root to `z^k` in both the plate and the `(1,-i)` circular launch. Each
coin and the launch omit one common normalization factor `1/√2`.
-/
namespace OpticalPhaseRead

structure Poly where
  a : Int
  b : Int
  c : Int
  d : Int
  deriving DecidableEq, Inhabited

def zero : Poly := ⟨0,0,0,0⟩
def one : Poly := ⟨1,0,0,0⟩
def add (x y : Poly) : Poly := ⟨x.a+y.a, x.b+y.b, x.c+y.c, x.d+y.d⟩
def sub (x y : Poly) : Poly := ⟨x.a-y.a, x.b-y.b, x.c-y.c, x.d-y.d⟩

def mul (x y : Poly) : Poly :=
  ⟨x.a*y.a - x.b*y.d - x.c*y.c - x.d*y.b,
   x.a*y.b + x.b*y.a - x.c*y.d - x.d*y.c,
   x.a*y.c + x.b*y.b + x.c*y.a - x.d*y.d,
   x.a*y.d + x.b*y.c + x.c*y.b + x.d*y.a⟩

def conj (x : Poly) : Poly := ⟨x.a, -x.d, -x.c, -x.b⟩
def absSq (x : Poly) : Poly := mul x (conj x)

def shift : Nat → Poly → Poly
  | 0, x => x
  | n+1, x => let y := shift n x; ⟨-y.d, y.a, y.b, y.c⟩

/-- In the ordinary embedding `z-z³` is the positive square root of 2. -/
def radical (k : Nat) : Poly := sub (shift (k%8) one) (shift ((3*k)%8) one)

theorem root_and_radical : shift 4 one = ⟨-1,0,0,0⟩ ∧
    radical 1 = ⟨0,1,0,-1⟩ ∧ mul (radical 1) (radical 1) = ⟨2,0,0,0⟩ ∧
    radical 7 = radical 1 ∧ radical 3 = sub zero (radical 1) ∧
    radical 5 = radical 3 := by decide +kernel

structure Cell where
  h : Poly
  v : Poly
  deriving DecidableEq, Inhabited

def weight (p : Cell) : Poly := add (absSq p.h) (absSq p.v)

/-- At depth `t` the ordered sites have positions `2*j-t`.
H moves left, V right. The marked site multiplies both outgoing modes. -/
def depart (t plate : Nat) (p : Cell × Nat) : Cell :=
  let exponent := if 2*p.2 = t then plate else 0
  ⟨shift exponent (add p.1.h p.1.v), shift exponent (sub p.1.h p.1.v)⟩

/-- An H output keeps its list index. A V output advances one list index. -/
def stream (prevV : Poly) : List Cell → List Cell
  | [] => [⟨zero, prevV⟩]
  | p :: ps => ⟨p.h, prevV⟩ :: stream p.v ps

def walk (s k : Nat) : Nat → List Cell
  | 0 => [⟨one, shift ((6*k)%8) one⟩]
  | t+1 => stream zero (((walk s k t).zipIdx).map (depart t ((s*k)%8)))

def origin (s k : Nat) : Cell := (walk s k 10).getD 5 ⟨zero,zero⟩
def total (s k : Nat) : Poly := ((walk s k 10).map weight).foldl add zero

theorem origin_amplitudes_135 : origin 3 1 =
    ⟨⟨-12,-10,0,10⟩, ⟨0,10,12,10⟩⟩ := by decide +kernel

def plusWeight : Poly := ⟨688,480,0,-480⟩
def minusWeight : Poly := ⟨688,-480,0,480⟩

theorem radical_form : plusWeight = add ⟨688,0,0,0⟩ (mul ⟨480,0,0,0⟩ (radical 1)) ∧
    minusWeight = sub ⟨688,0,0,0⟩ (mul ⟨480,0,0,0⟩ (radical 1)) := by decide +kernel

/-- The unnormalized squared weights represent `688 ± 480√2`.
The two conjugate embeddings in each pair give the same weight. -/
theorem fixed_label_split : [1,3,5,7].map (fun k => weight (origin 3 k)) =
    [plusWeight, minusWeight, minusWeight, plusWeight] := by decide +kernel

theorem complete_denominator : [1,3,5,7].map (total 3) =
    List.replicate 4 ⟨2048,0,0,0⟩ ∧ 2^(10+1) = (2048 : Nat) := by decide +kernel

/-- The other four named phase settings give the same rational origin
weights under all four embeddings, in setting order 0°, 45°, 90°, 180°. -/
theorem rational_phase_controls :
    [1,3,5,7].map (fun k => [0,1,2,4].map (fun s => weight (origin s k))) =
    List.replicate 4 [⟨144,0,0,0⟩, ⟨816,0,0,0⟩, ⟨1360,0,0,0⟩, ⟨1360,0,0,0⟩] := by
  decide +kernel

end OpticalPhaseRead
