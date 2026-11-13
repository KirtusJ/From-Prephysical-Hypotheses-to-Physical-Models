import Std

/-! # A two-launch three-tick local holonomy read

The base is the integer line, the launch is (0,R,0), and the sheet is cyclic.
The Hadamard contributes a minus only at L→L. The two independently prepared
launches are compared at the same complete base port. Sheet amplitudes at
the same port and same residue are summed coherently before squaring.
-/
namespace HolonomyRead

structure Path where
  site : Int
  right : Bool
  area : Int
  sign : Int
  deriving DecidableEq

def start : Path := ⟨0,true,0,1⟩

def step (p : Path) (b : Bool) : Path :=
  ⟨p.site+(if b then 1 else -1), b, p.area+p.site,
   if !b && !p.right then -p.sign else p.sign⟩

def layer (xs : List Path) : List Path :=
  xs.flatMap fun p => [step p true,step p false]

def paths := layer (layer (layer [start]))

theorem exhaustive_three_ticks : paths =
  [⟨3,true,3,1⟩,⟨1,false,3,1⟩,⟨1,true,1,1⟩,⟨-1,false,1,-1⟩,
   ⟨1,true,-1,1⟩,⟨-1,false,-1,1⟩,⟨-1,true,-3,-1⟩,⟨-3,false,-3,1⟩] := by decide +kernel

/-- Each signed pair at one of the two double ports, before translating
the area into the physically named sheet. -/
def port (x : Int) (b : Bool) := paths.filter (fun p => p.site==x && p.right==b)

theorem port_tables :
    port 1 true = [⟨1,true,1,1⟩,⟨1,true,-1,1⟩] ∧
    port (-1) false = [⟨-1,false,1,-1⟩,⟨-1,false,-1,1⟩] ∧
    (port 3 true).length=1 ∧ (port 1 false).length=1 ∧
    (port (-1) true).length=1 ∧ (port (-3) false).length=1 := by decide +kernel

def numerator (M k x : Int) (b : Bool) (y : Int) : Int :=
  ((port x b).map fun p => if (p.area*k)%M = y then p.sign else 0).sum

theorem signed_double_ports (M k y : Int) :
    let A := if k%M=y then (1:Int) else 0
    let B := if (-k)%M=y then (1:Int) else 0
    numerator M k 1 true y = A+B ∧ numerator M k (-1) false y = -A+B := by
  simp only [numerator,port_tables.1,port_tables.2.1,List.map_cons,List.map_nil,
    List.sum_cons,List.sum_nil,Int.one_mul,Int.neg_one_mul,Int.add_zero]
  split <;> split <;> simp_all

/-- Circular separation ±2. When M=4 the two readings are the same
residue, so their union must be counted once. -/
def atDistanceTwo (M q : Int) : Prop := q%M = 2%M ∨ q%M = (-2)%M
instance (M q : Int) : Decidable (atDistanceTwo M q) := inferInstanceAs
  (Decidable (q%M = 2%M ∨ q%M = (-2)%M))

private theorem neg_mod_eq (M u v : Int) (h : u%M=v%M) : (-u)%M=(-v)%M := by
  calc
    _ = (0-u%M)%M := by rw [Int.sub_emod_emod, Int.zero_sub]
    _ = (0-v%M)%M := by rw [h]
    _ = _ := by rw [Int.sub_emod_emod,Int.zero_sub]

theorem matches_neg (M q : Int) : atDistanceTwo M (-q) ↔ atDistanceTwo M q := by
  constructor <;> intro h
  · rcases h with h|h
    · exact Or.inr (by simpa using neg_mod_eq M _ _ h)
    · exact Or.inl (by simpa using neg_mod_eq M _ _ h)
  · rcases h with h|h
    · exact Or.inr (neg_mod_eq M _ _ h)
    · exact Or.inl (by simpa using neg_mod_eq M _ _ h)

private theorem residue_difference (M u v : Int) : (u%M-v%M)%M=(u-v)%M := by
  rw [Int.emod_sub_emod,Int.sub_emod_emod]

private theorem double_sum (k : Int) : 2*k=k+k := by omega

theorem aligned_cells_distinct (M k : Int) (noCollision : (2*k)%M≠0) : k%M≠(-k)%M := by
  intro eq
  have h := Int.emod_eq_emod_iff_emod_sub_eq_zero.mp eq
  apply noCollision
  simpa only [Int.sub_neg,double_sum] using h

/-- The squared mass for each sheet coordinate at either double port. -/
theorem registered_unit_cells (M k : Int) (hc : (2*k)%M≠0) :
    let a := k%M
    let b := (-k)%M
    (numerator M k 1 true a)^2=1 ∧ (numerator M k 1 true b)^2=1 ∧
    (numerator M k (-1) false a)^2=1 ∧ (numerator M k (-1) false b)^2=1 := by
  have ne := aligned_cells_distinct M k hc
  have f := signed_double_ports M k (k%M)
  have g := signed_double_ports M k ((-k)%M)
  simp [ne,Ne.symm ne] at f g
  dsimp only
  rw [f.1,g.1,f.2,g.2]
  decide

def orderedContribution (M k x : Int) (b : Bool) : Int :=
  let a := k%M
  let d := (-k)%M
  let mass := fun y => (numerator M k x b y)^2
  (if atDistanceTwo M (a-d) then mass a * mass d else 0) +
  (if atDistanceTwo M (d-a) then mass d * mass a else 0)

theorem favorable_read (M k : Int) (hc : (2*k)%M≠0) :
    orderedContribution M k 1 true + orderedContribution M k (-1) false =
      if atDistanceTwo M (2*k) then 4 else 0 := by
  have a := registered_unit_cells M k hc
  have f : atDistanceTwo M (k%M-(-k)%M) ↔ atDistanceTwo M (2*k) := by
    simp only [atDistanceTwo,residue_difference,Int.sub_neg,double_sum]
  have g : atDistanceTwo M ((-k)%M-k%M) ↔ atDistanceTwo M (2*k) := by
    rw [show (-k)%M-k%M = -(k%M-(-k)%M) by omega,matches_neg,f]
  simp only [orderedContribution,a.1,a.2.1,a.2.2.1,a.2.2.2,f,g]
  split <;> decide

theorem collision_control (M k : Int) (eq : k%M=(-k)%M) :
    numerator M k 1 true (k%M)=2 ∧ numerator M k (-1) false (k%M)=0 := by
  have v := signed_double_ports M k (k%M)
  simpa [eq] using v

/-- Positive odd modulus admits exact cancellation of doubling modulo M,
proved by multiplying by the integer inverse m+1 of two modulo 2m+1. -/
theorem odd_cancel (m u v : Int)
    (h : (2*u)%(2*m+1)=(2*v)%(2*m+1)) : u%(2*m+1)=v%(2*m+1) := by
  have product (z : Int) :
      ((2*z)*(m+1))%(2*m+1) = z%(2*m+1) := by
    have id : (2*z)*(m+1) = z+(2*m+1)*z := by
      simp [Int.add_mul,Int.mul_add,Int.mul_comm,Int.mul_left_comm,Int.mul_assoc] <;> omega
    rw [id,Int.add_mul_emod_self_left]
  calc
    _ = ((2*u)*(m+1))%(2*m+1) := (product u).symm
    _ = ((2*v)*(m+1))%(2*m+1) := by rw [Int.mul_emod (2*u),h,← Int.mul_emod]
    _ = _ := product v

theorem odd_selector (m k : Int) : atDistanceTwo (2*m+1) (2*k) ↔
    k%(2*m+1)=1%(2*m+1) ∨ k%(2*m+1)=(-1)%(2*m+1) := by
  constructor
  · rintro (h|h)
    · exact Or.inl (odd_cancel m k 1 (by simpa using h))
    · exact Or.inr (odd_cancel m k (-1) (by simpa using h))
  · rintro (h|h)
    · left; rw [Int.mul_emod, h,← Int.mul_emod]; simp
    · right; rw [Int.mul_emod, h,← Int.mul_emod]; simp

/-- On the even sheet, the displacement added by k→k+m at a departure
depends only on the tick parity along any path from zero. -/
private def travel : Bool → Int | true => 1 | false => -1

def area (x : Int) : List Bool → Int
  | [] => 0
  | e::w => x+area (x+travel e) w

def staircase (t : Int) : Nat → Int
  | 0 => 0
  | n+1 => t+staircase (t+1) n

private theorem area_parity (x t : Int) (w : List Bool) (h : x%2=t%2) :
    (area x w)%2=(staircase t w.length)%2 := by
  induction w generalizing x t with
  | nil => rfl
  | cons e w ih =>
    have stepParity : (x+travel e)%2=(t+1)%2 := by cases e <;> dsimp [travel] <;> omega
    rw [area,List.length_cons,staircase,Int.add_emod,h,ih _ _ stepParity,← Int.add_emod]

theorem even_alias (m k : Int) (w : List Bool) :
    ((k+m)*area 0 w)%(2*m) =
      (k*area 0 w + m*staircase 0 w.length)%(2*m) := by
  have h := area_parity 0 0 w rfl
  have lift (z : Int) : (m*z)%(2*m)=(m*(z%2))%(2*m) := by
    have hd := Int.ediv_add_emod z 2
    have eq : m*z = m*(z%2)+(2*m)*(z/2) := by
      calc
        _ = m*(2*(z/2)+z%2) := by rw [hd]
        _ = _ := by simp [Int.mul_add,Int.add_comm,Int.mul_assoc,Int.mul_comm,Int.mul_left_comm]
    rw [eq,Int.add_mul_emod_self_left]
  rw [Int.add_mul,Int.add_emod, lift (area 0 w),h,← lift (staircase 0 w.length),← Int.add_emod]

/-- The finite denominator of two independent three-H launches. -/
theorem two_launch_denominator : paths.length * paths.length = 64 := by decide +kernel

/-- A cyclic unit is exhibited by a multiplicative inverse modulo M. -/
theorem unit_no_collision (M k inverse : Int) (size : 3≤M) (unit : (k*inverse)%M=1) :
    (2*k)%M≠0 := by
  intro collision
  have two := Int.emod_eq_of_lt (a:=2) (b:=M) (by decide) (by omega)
  have fromUnit : (2*(k*inverse))%M=2 := by
    rw [Int.mul_emod 2 (k*inverse),unit,Int.mul_one,Int.emod_emod,two]
  have fromCollision : ((2*k)*inverse)%M=0 := by
    rw [Int.mul_emod (2*k) inverse,collision,Int.zero_mul,Int.zero_emod]
  rw [Int.mul_assoc] at fromCollision
  omega

theorem fixed_unit_read (M k inverse : Int) (size : 4≤M) (unit : (k*inverse)%M=1) :
    orderedContribution M k 1 true + orderedContribution M k (-1) false =
      if atDistanceTwo M (2*k) then 4 else 0 :=
  favorable_read M k (unit_no_collision M k inverse (by omega) unit)

/-- A fresh R-launched ruler has four two-step histories; the two nonzero
displacements end on different output rails even when their sites coincide.
Its opposite-rail mixed paths return to the launching site. -/
theorem ruler_legs : (layer (layer [start])).map (fun p => (p.site,p.right,p.sign)) =
    [(2,true,1),(0,false,1),(0,true,1),(-2,false,-1)] := by decide +kernel

def rulerNumerator (M l z : Int) : Int :=
  (if (2*l)%M=z%M then 1 else 0) + (if (-2*l)%M=z%M then 1 else 0) +
  (if 0=z%M then 2 else 0)

private theorem neg_mod_iff (M u v : Int) : (-u)%M=(-v)%M ↔ u%M=v%M := by
  constructor
  · intro h
    simpa using neg_mod_eq M _ _ h
  · exact neg_mod_eq M u v

private theorem ruler_symmetric (M l z : Int) : rulerNumerator M l (-z) = rulerNumerator M l z := by
  have a : (2*l)%M=(-z)%M ↔ (-2*l)%M=z%M := by
    simpa [Int.neg_mul] using (neg_mod_iff M (-(2*l)) z)
  have b : (-2*l)%M=(-z)%M ↔ (2*l)%M=z%M := by
    simpa [Int.neg_mul] using (neg_mod_iff M (2*l) z)
  have n : (0:Int)=(-z)%M ↔ (0:Int)=z%M := by simpa using neg_mod_iff M 0 z
  simp only [rulerNumerator,a,b,n]
  omega

/-- Numerator over 256 after the registered cells of the two launches
are distinct, with two orderings entering each of two return ports. -/
def two_ports_with_ruler (M k l : Int) : Int :=
  2*(rulerNumerator M l (2*k) + rulerNumerator M l (-(2*k)))

theorem ruler_read (M k l : Int) (separate : (2*k)%M≠0) :
    two_ports_with_ruler M k l =
    4*((if (2*l)%M=(2*k)%M then 1 else 0) + (if (-2*l)%M=(2*k)%M then 1 else 0)) := by
  rw [two_ports_with_ruler,ruler_symmetric]
  simp [rulerNumerator,Ne.symm separate]
  omega

theorem order_four_ruler : two_ports_with_ruler 4 1 1 = 8 ∧ two_ports_with_ruler 4 3 1 = 8 :=
  by decide +kernel

private theorem odd_ruler_separate (m l inverse : Int) (size : 3≤2*m+1)
    (unit : (l*inverse)%(2*m+1)=1) : (2*l)%(2*m+1)≠(-2*l)%(2*m+1) := by
  intro collision
  have doubled := odd_cancel m l (-l) (by simpa [Int.mul_neg,Int.neg_mul] using collision)
  exact aligned_cells_distinct (2*m+1) l (unit_no_collision _ _ inverse size unit) doubled

theorem odd_ruler_read (m k l inverse : Int) (size : 3≤2*m+1)
    (unit : (l*inverse)%(2*m+1)=1) (sep : (2*k)%(2*m+1)≠0) :
    two_ports_with_ruler (2*m+1) k l =
      if (2*k)%(2*m+1)=(2*l)%(2*m+1) ∨ (2*k)%(2*m+1)=(-2*l)%(2*m+1) then 4 else 0 := by
  rw [ruler_read _ _ _ sep]
  have ne := odd_ruler_separate m l inverse size unit
  by_cases p : (2*l)%(2*m+1)=(2*k)%(2*m+1)
  · have n : (-2*l)%(2*m+1)≠(2*k)%(2*m+1) := fun q => ne (p.trans q.symm)
    simp [p,n]
  · by_cases q : (-2*l)%(2*m+1)=(2*k)%(2*m+1)
    · simp [p,q]
    · simp [p,q,Ne.symm p,Ne.symm q]

/-- The force layer has four distinct complete ports at two ticks. The third
coin is fresh, but its two unit shifts act on the existing force sheet. -/
theorem anchored_force_legs : (layer (layer [start])).map (fun p => (p.site,p.right,p.area,p.sign)) =
    [(2,true,1,1),(0,false,1,1),(0,true,-1,1),(-2,false,-1,-1)] := by decide +kernel

def anchoredNumerator (M k l : Int) : Int :=
  ((layer (layer [start])).map fun p =>
    (if (p.area*k+l)%M=0 then p.sign^2 else 0) +
    (if (p.area*k-l)%M=0 then p.sign^2 else 0)).sum

private theorem zero_sub_iff (M a b : Int) : (a-b)%M=0 ↔ a%M=b%M :=
  Int.emod_eq_emod_iff_emod_sub_eq_zero.symm

private theorem zero_add_iff (M a b : Int) : (a+b)%M=0 ↔ a%M=(-b)%M := by
  simpa using zero_sub_iff M a (-b)

theorem anchored_read (M k l : Int) (strideSeparated : (2*l)%M≠0) :
    anchoredNumerator M k l =
    if k%M=l%M ∨ k%M=(-l)%M then 4 else 0 := by
  have distinct := aligned_cells_distinct M l strideSeparated
  have force : layer (layer [start]) =
    [⟨2,true,1,1⟩,⟨0,false,1,1⟩,⟨0,true,-1,1⟩,⟨-2,false,-1,-1⟩] := by decide +kernel
  have r : (-k)%M=l%M ↔ k%M=(-l)%M := by simpa using neg_mod_iff M k (-l)
  simp only [anchoredNumerator,force,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,
    Int.one_mul,Int.neg_one_mul,zero_add_iff,zero_sub_iff,neg_mod_iff,r]
  by_cases a : k%M=l%M
  · have b : k%M≠(-l)%M := fun h => distinct (a.symm.trans h)
    simp [a,distinct]
  · by_cases b : k%M=(-l)%M
    · simp [a,b,distinct,Ne.symm distinct]
    · simp [a,b]

theorem anchored_unit_read (M k l inverse : Int) (size : 3≤M) (unit : (l*inverse)%M=1) :
    anchoredNumerator M k l =
    if k%M=l%M ∨ k%M=(-l)%M then 4 else 0 :=
  anchored_read M k l (unit_no_collision M l inverse size unit)

theorem even_marker_distinguishes : anchoredNumerator 8 1 1 = 4 ∧ anchoredNumerator 8 5 1 = 0 :=
  by decide +kernel

end HolonomyRead
