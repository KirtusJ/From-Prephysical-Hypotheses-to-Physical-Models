import Std

/-!
# Coin-controlled returning loops

The R input of a balanced real Hadamard has two positive outgoing coefficients,
with the common scalar 1/√2 suppressed. All later coins are permutations.
Each physical tick adds the departure site to the sheet before streaming.
There is one base coordinate, one rail, and one sheet per term.
-/
namespace LoopCoinPreparation

structure Cell where
  site : Int
  right : Bool
  sheet : Int
  coefficient : Int
  deriving DecidableEq

def dir (right : Bool) : Int := if right then 1 else -1

def stream (p : Cell) (b : Bool) : Cell :=
  ⟨p.site + dir b, b, p.sheet + p.site, p.coefficient⟩

def straight (edge : Cell → Bool → Cell) : Nat → Cell → Cell
  | 0, p => p
  | n+1, p => straight edge n (edge p p.right)

/-- First tick chooses rail b, then n identity-coin ticks continue on it. -/
def leg (edge : Cell → Bool → Cell) (n : Nat) (p : Cell) (b : Bool) :=
  straight edge n (edge p b)

/-- From the R input of H, followed by n identities, X, and n identities. -/
def splitAndReturn (edge : Cell → Bool → Cell) (n : Nat) (x y w : Int) : List Cell :=
  [true,false].map fun b =>
    let turn := leg edge n ⟨x,true,y,w⟩ b
    leg edge n turn (!turn.right)

def tri : Nat → Int
  | 0 => 0
  | n+1 => tri n + (n : Int)

theorem straight_sum (n : Nat) (x y w : Int) (b : Bool) :
    straight stream n ⟨x,b,y,w⟩ =
    ⟨x + (n:Int)*dir b, b, y + (n:Int)*x + dir b*tri n, w⟩ := by
  induction n generalizing x y with
  | zero => simp [straight,tri]
  | succ n ih =>
    simp only [straight,stream,ih,tri,Int.natCast_succ,Int.add_mul,Int.mul_add,
      Int.one_mul]
    rw [Int.mul_comm (dir b) (n:Int)]
    congr 1 <;> omega

theorem leg_sum (n : Nat) (p : Cell) (b : Bool) :
    leg stream n p b =
    ⟨p.site + ((n+1:Nat):Int)*dir b, b,
      p.sheet + ((n+1:Nat):Int)*p.site + dir b*tri (n+1), p.coefficient⟩ := by
  simp only [leg,stream,straight_sum,tri,Int.natCast_succ,Int.add_mul,
    Int.mul_add,Int.one_mul]
  rw [Int.mul_comm (dir b) (n:Int)]
  congr 1 <;> omega

/-- Written in physical return order L,R. The two rails are orthogonal even
if their sheet translations coincide modulo the sheet circumference. -/
theorem exact_return (n : Nat) (x y w : Int) :
    let a : Int := ((n+1:Nat):Int)
    splitAndReturn stream n x y w =
    [⟨x,false,y + 2*a*x + a*a,w⟩, ⟨x,true,y + 2*a*x - a*a,w⟩] := by
  dsimp only
  simp only [splitAndReturn,List.map_cons,List.map_nil,leg_sum]
  generalize ((n+1:Nat):Int) = a
  simp only [Bool.not_true,Bool.not_false,dir,if_true,if_false,Bool.false_eq_true,
    Int.mul_one,Int.one_mul,Int.mul_neg,Int.neg_mul,Int.mul_add,Int.mul_assoc]
  have forward : y+a*x+tri (n+1)+(a*x+a*a) + -tri (n+1) =
      y+2*(a*x)+a*a := by omega
  have backward : y+a*x+ -tri (n+1)+(a*x+ -(a*a))+tri (n+1) =
      y+2*(a*x)-a*a := by omega
  rw [forward,backward,show x+a+ -a = x by omega,show x+ -a+a = x by omega]

def project (N M : Int) (p : Cell) : Cell :=
  ⟨p.site % N,p.right,p.sheet % M,p.coefficient⟩

def ringStream (N M : Int) (p : Cell) (b : Bool) : Cell :=
  ⟨(p.site + dir b) % N,b,(p.sheet + p.site) % M,p.coefficient⟩

theorem projected_tick (N M : Int) (wrap : M ∣ N) (p : Cell) (b : Bool) :
    ringStream N M (project N M p) b = project N M (stream p b) := by
  simp only [ringStream,project,stream,Int.emod_add_emod]
  rw [Int.add_emod p.sheet (p.site % N) M,Int.emod_emod_of_dvd p.site wrap,
    ← Int.add_emod]

theorem projected_coast (N M : Int) (wrap : M ∣ N) (n : Nat) (p : Cell) :
    straight (ringStream N M) n (project N M p) =
    project N M (straight stream n p) := by
  induction n generalizing p with
  | zero => rfl
  | succ n ih =>
    simp only [straight]
    change straight _ n (ringStream N M (project N M p) p.right) = _
    rw [projected_tick N M wrap,ih]

theorem projected_leg (N M : Int) (wrap : M ∣ N) (n : Nat) (p : Cell) (b : Bool) :
    leg (ringStream N M) n (project N M p) b = project N M (leg stream n p b) := by
  simp only [leg,projected_tick N M wrap,projected_coast N M wrap]

theorem ring_return (N M : Int) (wrap : M ∣ N) (n : Nat) (x y w : Int) :
    let a : Int := ((n+1:Nat):Int)
    splitAndReturn (ringStream N M) n (x%N) (y%M) w =
    [⟨x%N,false,(y + 2*a*x + a*a)%M,w⟩, ⟨x%N,true,(y + 2*a*x - a*a)%M,w⟩] := by
  have arm (b : Bool) :
      leg (ringStream N M) n (leg (ringStream N M) n ⟨x%N,true,y%M,w⟩ b)
        (!(leg (ringStream N M) n ⟨x%N,true,y%M,w⟩ b).right) =
      project N M (leg stream n (leg stream n ⟨x,true,y,w⟩ b)
        (!(leg stream n ⟨x,true,y,w⟩ b).right)) := by
    change leg _ n (leg _ n (project N M ⟨x,true,y,w⟩) b)
      (!(leg _ n (project N M ⟨x,true,y,w⟩) b).right) = _
    rw [projected_leg N M wrap]
    exact projected_leg N M wrap ..
  have h := congrArg (List.map (project N M)) (exact_return n x y w)
  simpa only [splitAndReturn,List.map_cons,List.map_nil,arm,project] using h

/-- An R-packet is a list of (site,sheet,signed coefficient). Linear extension
means collecting at identical output coordinates after concatenating these
terms; no register retains which input supplied a coefficient. -/
abbrev RPacket := List (Int × Int × Int)

theorem packet_kernel (N M : Int) (wrap : M ∣ N) (n : Nat) (packet : RPacket) :
    let a : Int := ((n+1:Nat):Int)
    (packet.flatMap fun (x,y,w) =>
      splitAndReturn (ringStream N M) n (x%N) (y%M) w) =
    (packet.flatMap fun (x,y,w) =>
      [⟨x%N,false,(y + 2*a*x + a*a)%M,w⟩, ⟨x%N,true,(y + 2*a*x - a*a)%M,w⟩]) := by
  simp only [ring_return N M wrap]

/-- Each output rail at a fixed base point is a translation on the whole
sheet. Its inverse is valid on a coherently occupied sheet as well. -/
theorem sheet_preimage (M y z gain : Int) :
    (y+gain)%M = z%M ↔ y%M = (z-gain)%M := by
  simpa only [Int.sub_add_cancel] using
    (Int.emod_add_cancel_right (m := y) (k := z-gain) (n := M) gain)

/-- The Fourier phase splits into one common linear momentum shift and two
opposite, site-independent coin factors, for *any* additive character.
The multiplication on the codomain is supplied explicitly, so this theorem
also applies directly to an abstract character on integer exponents. -/
theorem character_factors (χ : Int → A) (mul : A → A → A)
    (character : ∀ i j, χ (i+j) = mul (χ i) (χ j)) (k a x : Int) :
    χ (k*(2*a*x + a*a)) = mul (χ (k*(2*a*x))) (χ (k*(a*a))) ∧
    χ (k*(2*a*x - a*a)) = mul (χ (k*(2*a*x))) (χ (-(k*(a*a)))) := by
  simp only [Int.sub_eq_add_neg,Int.mul_add,Int.mul_neg,character,and_self]

end LoopCoinPreparation
