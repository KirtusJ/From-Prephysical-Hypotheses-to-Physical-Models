import Std

/-!
# One cyclic sheet for a pair of signed walkers

The two Hadamard direction choices advance simultaneously. A single shift of
the physical sheet is attached to the pair of *departure* positions. Character
evaluation of the lifted, signed path sum intertwines this rule with a complex
phase applied before both shifts. The proof works at every finite depth and
allows a different joint gain and a different base-coordinate mask per step.
-/
namespace SharedSheet

structure Character (M : Nat) (R : Type) [Mul R] [Neg R] [OfNat R 1] where
  order_pos : 0 < M
  value : Nat → R
  at_zero : value 0 = 1
  at_add : ∀ i j, value ((i+j)%M) = value i * value j
  neg_mul : ∀ a b : R, (-a)*b = -(a*b)
  neg_neg : ∀ a : R, -(-a) = a

structure Vertex (X : Type) where
  first : X
  second : X
  firstRight : Bool
  secondRight : Bool
  deriving DecidableEq

structure Lifted (X : Type) where
  vertex : Vertex X
  sheet : Nat
  negative : Bool

structure Term (X R : Type) where
  vertex : Vertex X
  weight : R

private def negativeEdge (v : Vertex X) (d e : Bool) : Bool :=
  xor (!v.firstRight && !d) (!v.secondRight && !e)

private def next (move : X → Bool → X) (v : Vertex X) (d e : Bool) : Vertex X :=
  ⟨move v.first d, move v.second e, d, e⟩

private def signs : List (Bool × Bool) :=
  [(false,false),(false,true),(true,false),(true,true)]

def liftEdge (M : Nat) (move : X → Bool → X) (gain : X → X → Nat)
    (v : Lifted X) (dirs : Bool × Bool) : Lifted X :=
  ⟨next move v.vertex dirs.1 dirs.2,
   (v.sheet + gain v.vertex.first v.vertex.second) % M,
   xor v.negative (negativeEdge v.vertex dirs.1 dirs.2)⟩

variable {R : Type} [Mul R] [Neg R] [OfNat R 1]

def evaluate (χ : Character M R) (v : Lifted X) : Term X R :=
  ⟨v.vertex, if v.negative then -(χ.value v.sheet) else χ.value v.sheet⟩

def sectorEdge (χ : Character M R) (move : X → Bool → X) (gain : X → X → Nat)
    (v : Term X R) (dirs : Bool × Bool) : Term X R :=
  let phase := χ.value (gain v.vertex.first v.vertex.second)
  let w := v.weight * phase
  ⟨next move v.vertex dirs.1 dirs.2,
   if negativeEdge v.vertex dirs.1 dirs.2 then -w else w⟩

theorem character_edge (χ : Character M R) (move : X → Bool → X) (gain : X → X → Nat)
    (v : Lifted X) (dirs : Bool × Bool) :
    evaluate χ (liftEdge M move gain v dirs) = sectorEdge χ move gain (evaluate χ v) dirs := by
  rcases v with ⟨base,sheet,negative⟩
  cases negative <;> cases edge : negativeEdge base dirs.1 dirs.2 <;>
    simp [liftEdge, sectorEdge, evaluate, edge, χ.at_add, χ.neg_mul, χ.neg_neg]

structure Tick (X : Type) where
  gain : X → X → Nat
  keep : Vertex X → Bool

def liftStep (M : Nat) (move : X → Bool → X) (tick : Tick X) (paths : List (Lifted X)) :=
  (paths.flatMap fun p => signs.map (liftEdge M move tick.gain p)).filter (fun p => tick.keep p.vertex)

def sectorStep (χ : Character M R) (move : X → Bool → X) (tick : Tick X) (paths : List (Term X R)) :=
  (paths.flatMap fun p => signs.map (sectorEdge χ move tick.gain p)).filter (fun p => tick.keep p.vertex)

theorem character_step (χ : Character M R) (move : X → Bool → X) (tick : Tick X)
    (paths : List (Lifted X)) :
    (liftStep M move tick paths).map (evaluate χ) =
      sectorStep χ move tick (paths.map (evaluate χ)) := by
  have expanded : (paths.flatMap fun p => signs.map (liftEdge M move tick.gain p)).map (evaluate χ) =
                  (paths.map (evaluate χ)).flatMap fun p => signs.map (sectorEdge χ move tick.gain p) := by
    simp only [List.map_flatMap, List.flatMap_map, List.map_map, Function.comp_def, character_edge]
  unfold liftStep sectorStep
  rw [← expanded, List.filter_map]
  rfl

def liftRun (M : Nat) (move : X → Bool → X) (ticks : List (Tick X)) (paths : List (Lifted X)) :=
  ticks.foldl (fun current tick => liftStep M move tick current) paths

def sectorRun (χ : Character M R) (move : X → Bool → X) (ticks : List (Tick X))
    (paths : List (Term X R)) :=
  ticks.foldl (fun current tick => sectorStep χ move tick current) paths

theorem character_run (χ : Character M R) (move : X → Bool → X) (ticks : List (Tick X))
    (paths : List (Lifted X)) :
    (liftRun M move ticks paths).map (evaluate χ) =
      sectorRun χ move ticks (paths.map (evaluate χ)) := by
  induction ticks generalizing paths with
  | nil => rfl
  | cons t ts ih =>
    change (liftRun M move ts (liftStep M move t paths)).map (evaluate χ) =
           sectorRun χ move ts (sectorStep χ move t (paths.map (evaluate χ)))
    rw [ih, character_step]

def endpointWeight [DecidableEq X] [OfNat R 0] [Add R]
    (atVertex : Vertex X) (paths : List (Term X R)) : R :=
  ((paths.filter fun p => decide (p.vertex = atVertex)).map Term.weight).foldr (· + ·) 0

/-- Interference is retained by summing signed character terms at a common
endpoint. Both sums omit the same per-step Hadamard amplitude factor 1/2. -/
theorem character_amplitude [DecidableEq X] [OfNat R 0] [Add R] (χ : Character M R)
    (move : X → Bool → X) (ticks : List (Tick X)) (paths : List (Lifted X)) (v : Vertex X) :
    endpointWeight v ((liftRun M move ticks paths).map (evaluate χ)) =
    endpointWeight v (sectorRun χ move ticks (paths.map (evaluate χ))) :=
  congrArg (endpointWeight v) (character_run χ move ticks paths)

private theorem expandedLength (M : Nat) (move : X → Bool → X) (gain : X → X → Nat)
    (paths : List (Lifted X)) :
    (paths.flatMap fun p => signs.map (liftEdge M move gain p)).length = 4*paths.length := by
  induction paths with
  | nil => rfl
  | cons p ps ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_map, List.length_cons, ih]
    change 4 + 4*ps.length = 4*(ps.length+1)
    omega

/-- With no masking there are four equal-depth histories per incoming history
per step. The positive modulus per path is 1/2 per step for the tensor product
of the two normalized Hadamard coins; its squared modulus is 1/4 per step. -/
theorem unobserved_path_count (M : Nat) (move : X → Bool → X) (gains : List (X → X → Nat))
    (paths : List (Lifted X)) :
    (liftRun M move (gains.map (fun g => ⟨g, fun _ => true⟩)) paths).length =
      4^gains.length * paths.length := by
  induction gains generalizing paths with
  | nil => simp [liftRun]
  | cons g gs ih =>
    change (liftRun M move (gs.map (fun h => ⟨h, fun _ => true⟩))
               (liftStep M move ⟨g, fun _ => true⟩ paths)).length = _
    rw [ih]
    have noMask (xs : List (Lifted X)) : xs.filter (fun _ => true) = xs :=
      List.filter_eq_self.mpr (by simp)
    simp only [liftStep, noMask, expandedLength, List.length_cons,
               Nat.pow_succ, Nat.mul_assoc]

/-- Squared norm scaling of one joint unnormalized coin. Four signed input
counts become four joint successor counts before vertex and sheet shifts. -/
theorem joint_coin_norm (a b c d : Int) :
    ((a+b)+(c+d))^2 + ((a-b)+(c-d))^2 + ((a+b)-(c+d))^2 + ((a-b)-(c-d))^2 =
      4*(a^2 + b^2 + c^2 + d^2) := by
  simp only [Int.pow_succ, Int.pow_zero, Int.one_mul, Int.add_mul, Int.sub_mul,
             Int.mul_add, Int.mul_sub]
  omega

/-- For an integer-valued potential sampled on a cyclic spatial lattice, a
translation of either integer coordinate by a whole period is invisible.
The outer remainder gives the actual nonnegative sheet displacement. -/
def relativeGain (N M : Nat) (potential : Int → Int) (x y : Int) : Nat :=
  (potential ((x - y) % (N : Int)) % (M : Int)).toNat

theorem gain_periodic (N M : Nat) (potential : Int → Int) (x y : Int) :
    relativeGain N M potential (x+N) y = relativeGain N M potential x y ∧
    relativeGain N M potential x (y+N) = relativeGain N M potential x y := by
  have a : (x+(N:Int))-y = (x-y)+N := by omega
  have b : x-(y+(N:Int)) = (x-y)-N := by omega
  simp [relativeGain, a, b, Int.sub_eq_add_neg, Int.add_emod]

/-- Round a signed rational numerator/positive denominator to the nearest
integer, choosing the greater integer at ties. Integer-only computation. -/
def nearestGain (a d : Int) : Int := (2*a+d)/(2*d)

/-- Half a gain unit is a uniform error bound. This applies in particular to
a=2L(C(0)-C(x)) and d=C(0)-C(N/2), once the count denominator is positive. -/
theorem gain_rounding_error (a d : Int) (positive : 0 < d) :
    -d ≤ 2*(d*nearestGain a d - a) ∧ 2*(d*nearestGain a d-a) ≤ d := by
  have divisor : 0 < 2*d := by omega
  have eqn := Int.ediv_add_emod (2*a+d) (2*d)
  have lo := Int.emod_nonneg (2*a+d) (Int.ne_of_gt divisor)
  have hi := Int.emod_lt_of_pos (2*a+d) divisor
  unfold nearestGain
  rw [Int.mul_assoc] at eqn
  omega

end SharedSheet
