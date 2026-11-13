import Std

/-!
# Filtered straight-arm return interferometer in the signed sheet lift

Position is unwrapped on the integer line. The masks coherently admit two
position/direction cells at each tick. Each distinct entry of the list denotes
one distinct microscopic history, with its accumulated sign and sheet shift.
True denotes a left turn or a negative sign, according to the field.
-/
namespace CoinInterferometer

structure Entry where
  x : Int
  left : Bool
  sheet : Int
  negative : Bool
  deriving DecidableEq

def move (p : Entry) (left : Bool) : Entry :=
  ⟨p.x + (if left then -1 else 1), left, p.sheet + p.x,
   xor p.negative (p.left && left)⟩

def selected (k : Nat) (inward : Bool) (p : Entry) : Bool :=
  ((p.x == (k:Int)) && (p.left == inward)) ||
  ((p.x == -(k:Int)) && (p.left == !inward))

def tick (k : Nat) (inward : Bool) (paths : List Entry) : List Entry :=
  paths.flatMap fun p => [move p false, move p true].filter (selected k inward)

private def triangle : Nat → Int
  | 0 => 0
  | n+1 => triangle n + (n:Int)

private theorem triangle_double (n : Nat) : triangle n + triangle n = (n:Int)*((n:Int)-1) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [triangle, Int.natCast_succ]
    have sub : ((n:Int)+1)-1=(n:Int) := by omega
    rw [sub, Int.add_mul, Int.one_mul]
    rw [Int.mul_sub, Int.mul_one] at ih
    omega

def outPaths (inputLeft : Bool) : Nat → List Entry
  | 0 => [⟨0,inputLeft,0,false⟩]
  | n+1 => tick (n+1) false (outPaths inputLeft n)

private def outPair (n : Nat) (c : Bool) : List Entry :=
  [⟨n+1,false,triangle (n+1),false⟩,
   ⟨-((n:Int)+1),true,-triangle (n+1),xor c (decide (n%2=1))⟩]

private theorem parity_next (n : Nat) : decide ((n+1)%2=1) = !(decide (n%2=1)) := by
  by_cases h : n%2=1 <;> simp [h] <;> omega

theorem outward_histories (n : Nat) (c : Bool) :
    outPaths c (n+1) = outPair n c := by
  induction n with
  | zero => cases c <;> decide
  | succ n ih =>
    change tick _ false (outPaths c (n+1)) = _
    rw [ih]
    have p₁ : (n:Int)+1 > 0 := by omega
    have p₂ : ¬ -((n:Int)+1)+1 = ((n:Int)+1)+1 := by omega
    have p₃ : ¬ (n:Int)+1+(-1) = -(((n:Int)+1)+1) := by omega
    have negPos : -((n:Int)+1)+(-1) = -(((n:Int)+1)+1) := by omega
    have negSheet : -triangle (n+1) + -((n:Int)+1) = -(triangle (n+1)+((n:Int)+1)) := by omega
    simp only [outPair, tick, List.flatMap_cons, List.flatMap_nil, List.filter_cons,
               selected, move, Int.natCast_succ, Bool.false_eq_true, Bool.not_false,
               Bool.not_true, Bool.true_beq, Bool.false_beq, Bool.and_false, Bool.and_true,
               Bool.false_and, Bool.true_and, Bool.or_false, Bool.false_or, Bool.xor_false,
               Bool.xor_true, Bool.false_xor, beq_self_eq_true, p₂, p₃, negPos]
    cases c <;> by_cases parity : n%2=1 <;>
      simp [p₂,p₃,negPos,triangle, negSheet, parity_next, parity] <;> omega

/-- On the return, after the turning step, the radii drop from r to zero.
The right arm points left and the left arm points right. -/
def descend : Nat → List Entry → List Entry
  | 0, ps => ps
  | r+1, ps => descend r (tick r true ps)

private def inwardPair (r : Nat) (S : Int) (rightNeg leftNeg : Bool) : List Entry :=
  [⟨r,true,S,rightNeg⟩,⟨-(r:Int),false,-S,leftNeg⟩]

private def toggle : Nat → Bool → Bool
  | 0, b => b
  | r+1,b => toggle r (!b)

private def returnSum : Nat → Int
  | 0 => 0
  | r+1 => (r:Int)+1 + returnSum r

private theorem returnSum_eq (r : Nat) : returnSum r = triangle (r+1) := by
  induction r with
  | zero => rfl
  | succ r ih => simp only [returnSum, triangle, Int.natCast_succ] at *; omega

private theorem inward_step (r : Nat) (S : Int) (rightNeg leftNeg : Bool) :
    tick r true (inwardPair (r+1) S rightNeg leftNeg) =
      inwardPair r (S+((r:Int)+1)) (!rightNeg) leftNeg := by
  have a : ((r:Int)+1)+(-1)=r := by omega
  have b : -((r:Int)+1)+1 = -r := by omega
  have c : ((r:Int)+1)+1 ≠ -r := by omega
  have d : -((r:Int)+1)+(-1) ≠ r := by omega
  have e : -S + -((r:Int)+1) = -(S+((r:Int)+1)) := by omega
  simp [tick,inwardPair,move,selected,Int.natCast_succ,a,b,c,d,e]

private theorem descend_pair (r : Nat) (S : Int) (rightNeg leftNeg : Bool) :
    descend r (inwardPair r S rightNeg leftNeg) =
      inwardPair 0 (S+returnSum r) (toggle r rightNeg) leftNeg := by
  induction r generalizing S rightNeg with
  | zero => simp [descend,returnSum,toggle]
  | succ r ih =>
    rw [descend,inward_step,ih]
    simp [returnSum,toggle,Int.add_assoc]

private theorem toggle_parity (r : Nat) (b : Bool) :
    toggle r b = xor b (decide (r%2=1)) := by
  induction r generalizing b with
  | zero => simp [toggle]
  | succ r ih =>
    rw [toggle,ih,parity_next]
    cases b <;> cases decide (r%2=1) <;> rfl

def roundTrip (n : Nat) (inputLeft : Bool) : List Entry :=
  descend n (tick n true (outPaths inputLeft (n+1)))

private theorem turn (n : Nat) (c : Bool) :
    tick n true (outPair n c) =
      inwardPair n (triangle (n+1) + ((n:Int)+1)) false (xor c (decide (n%2=1))) := by
  have a : ((n:Int)+1)+(-1)=n := by omega
  have b : -((n:Int)+1)+1 = -n := by omega
  have no₁ : ((n:Int)+1)+1 ≠ -n := by omega
  have no₂ : -((n:Int)+1)+(-1) ≠ n := by omega
  have e : -triangle (n+1) + -((n:Int)+1) = -(triangle (n+1)+((n:Int)+1)) := by omega
  simp [tick,outPair,inwardPair,move,selected,a,b,no₁,no₂,e]

/-- For k=n+1 the output of the two k-step arms returning to the origin
contains exactly two histories, gaining +k² and -k². The common sign is
(-1)^n and the negative-sheet term has the extra Hadamard input sign. -/
theorem return_histories (n : Nat) (inputLeft : Bool) :
    roundTrip n inputLeft =
      [⟨0,true,((n:Int)+1)^2,decide (n%2=1)⟩,
       ⟨0,false,-(((n:Int)+1)^2),xor inputLeft (decide (n%2=1))⟩] := by
  rw [roundTrip,outward_histories,turn,descend_pair,returnSum_eq,toggle_parity]
  have twice := triangle_double (n+1)
  simp only [Int.natCast_succ] at twice
  have h : ((n:Int)+1)-1=n := by omega
  rw [h,Int.add_mul,Int.one_mul] at twice
  have square : triangle (n+1) + ((n:Int)+1) + triangle (n+1) = ((n:Int)+1)^2 := by
    simp only [Int.pow_succ,Int.pow_zero,Int.one_mul,Int.add_mul,Int.mul_add,Int.one_mul,Int.mul_one]
    omega
  simp [inwardPair,square]

/-! A component in a sheet character applies a unit rotation to the two-real
coordinate representation of each coin amplitude. The arm formula leaves the
unnormalized coin map (r,l) ↦ (r-l,r+l), followed by separate phase rotations
and the common sign. The following norm statement only uses the defining
identities of the selected real Euclidean amplitude plane. -/

structure NormLaws (V S : Type) [Add S] where
  plus : V → V → V
  minus : V → V → V
  normSq : V → S
  phase : Int → V → V
  sign : Bool → V → V
  phase_preserves : ∀ a v, normSq (phase a v) = normSq v
  sign_preserves : ∀ b v, normSq (sign b v) = normSq v
  hadamard : ∀ r l, normSq (minus r l) + normSq (plus r l) =
                    (normSq r + normSq l) + (normSq r + normSq l)

def returnedCoin [Add S] (law : NormLaws V S) (n : Nat) (r l : V) : V × V :=
  let area := ((n:Int)+1)^2
  let sign := decide (n%2=1)
  (law.sign sign (law.phase (-area) (law.minus r l)),
   law.sign sign (law.phase area (law.plus r l)))

/-- The squared norm of the unnormalized operation on any input coin is
twice its initial squared norm. Each of the 2k microscopic steps contributes
a 1/√2 amplitude normalization, so the normalized success is 2/4^k. -/
theorem return_weight [Add S] (law : NormLaws V S) (n : Nat) (r l : V) :
    let w := returnedCoin law n r l
    law.normSq w.1 + law.normSq w.2 =
      (law.normSq r + law.normSq l) + (law.normSq r + law.normSq l) := by
  simp [returnedCoin,law.sign_preserves,law.phase_preserves,law.hadamard]

def gateWord [Add S] (law : NormLaws V S) (word : List Nat) (input : V × V) : V × V :=
  word.foldl (fun c n => returnedCoin law n c.1 c.2) input

private def doubleWeight [Add S] : Nat → S → S
  | 0, z => z
  | n+1,z => doubleWeight n (z+z)

theorem word_weight [Add S] (law : NormLaws V S) (word : List Nat) (input : V × V) :
    let w := gateWord law word input
    law.normSq w.1 + law.normSq w.2 =
      doubleWeight word.length (law.normSq input.1 + law.normSq input.2) := by
  induction word generalizing input with
  | nil => rfl
  | cons n rest ih =>
    change law.normSq (gateWord law rest (returnedCoin law n input.1 input.2)).1 +
           law.normSq (gateWord law rest (returnedCoin law n input.1 input.2)).2 = _
    rw [ih,return_weight]
    rfl

end CoinInterferometer
