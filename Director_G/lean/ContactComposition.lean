import Std

/-!
# Four-site occupation composition test

Both rotation numerators use denominator 5. In the ordered hard-core basis
01,02,03,12,13,23, a bonded vacancy is the identity, a single occupant sees
the named real two-mode rotation, and a double occupant receives its
portable sign g. The plain swap of 1 and 2 has double-occupant sign s.
The same denominator is restored in both words of each comparison.
-/
namespace ContactComposition

inductive Angle | alpha | beta deriving DecidableEq
def c : Angle → Int | .alpha => 3 | .beta => 4
def h : Angle → Int | .alpha => 4 | .beta => 3
def sg (neg : Bool) : Int := if neg then -1 else 1

structure One where
  v0 : Int
  v1 : Int
  v2 : Int
  v3 : Int
  deriving DecidableEq

def oneA (r : Angle) (v : One) : One :=
  ⟨c r*v.v0-h r*v.v1,h r*v.v0+c r*v.v1,c r*v.v2-h r*v.v3,h r*v.v2+c r*v.v3⟩
def oneS (v : One) : One := ⟨v.v0,v.v2,v.v1,v.v3⟩
def oneB (r : Angle) (v : One) := oneS (oneA r (oneS v))

theorem one_commutes (r : Angle) (v : One) :
    oneA r (oneB r v) = oneB r (oneA r v) := by
  cases r <;> simp only [oneA,oneB,oneS,c,h,Int.mul_add,Int.mul_sub] <;>
    congr 1 <;> omega

structure Two where
  v01 : Int
  v02 : Int
  v03 : Int
  v12 : Int
  v13 : Int
  v23 : Int
  deriving DecidableEq

def first (r : Angle) (g : Int) (v : Two) : Two :=
  ⟨5*g*v.v01,c r*v.v02-h r*v.v12,c r*v.v03-h r*v.v13,
   h r*v.v02+c r*v.v12,h r*v.v03+c r*v.v13,5*v.v23⟩

def last (r : Angle) (g : Int) (v : Two) : Two :=
  ⟨5*v.v01,c r*v.v02-h r*v.v03,h r*v.v02+c r*v.v03,
    c r*v.v12-h r*v.v13,h r*v.v12+c r*v.v13,5*g*v.v23⟩

def A (r : Angle) (g : Int) (v : Two) := last r g (first r g v)
def S (s : Int) (v : Two) : Two := ⟨v.v02,v.v01,v.v03,s*v.v12,v.v23,v.v13⟩
def B (r : Angle) (g s : Int) (v : Two) := S s (A r g (S s v))

def start01 : Two := ⟨1,0,0,0,0,0⟩
def start02 : Two := ⟨0,1,0,0,0,0⟩

/-- Matched single-port squared output comparisons. Each product is
unnormalized by the same positive power of 25 on the two sides. -/
def passed (r : Angle) (g s : Int) : Prop :=
  let ab := (A r g (B r g s start01)).v02
  let ba := (B r g s (A r g start01)).v02
  let aab := (A r g (A r g (B r g s start02))).v02
  let aba := (A r g (B r g s (A r g start02))).v02
  ab*ab=ba*ba ∧ aab*aab=aba*aba

theorem both_finite_ports (r : Angle) (negG negS : Bool) :
    passed r (sg negG) (sg negS) ↔ negG=false ∧ negS=true := by
  cases r <;> cases negG <;> cases negS <;> simp only [passed,A,B,S,first,last,
    c,h,sg,start01,start02] <;> decide

/-- Exact polynomial book-keeping in an unknown double-block coefficient.
No truncation: d is the number of double-block phase contributions. -/
abbrev Poly := Nat → Int

def val (i : Int) : Poly := fun d => if d=0 then i else 0
def scale (p : Poly) (i : Int) : Poly := fun d => i*p d
def sum (p q : Poly) : Poly := fun d => p d+q d
def variableTimes (p : Poly) : Poly | 0 => 0 | k+1 => p k

structure Terms where
  v01 : Poly
  v02 : Poly
  v03 : Poly
  v12 : Poly
  v13 : Poly
  v23 : Poly

def mix (u v : Poly) (i j : Int) := sum (scale u i) (scale v j)
def polyA (r : Angle) (v : Terms) : Terms :=
  let a := c r
  let b := h r
  let on02 := mix v.v02 v.v12 a (-b)
  let on03 := mix v.v03 v.v13 a (-b)
  let on12 := mix v.v02 v.v12 b a
  let on13 := mix v.v03 v.v13 b a
  ⟨scale (variableTimes v.v01) 25,mix on02 on03 a (-b),mix on02 on03 b a,
    mix on12 on13 a (-b),mix on12 on13 b a,scale (variableTimes v.v23) 25⟩

def polyS (s : Int) (v : Terms) : Terms :=
  ⟨v.v02,v.v01,v.v03,scale v.v12 s,v.v23,v.v13⟩
def polyB (r : Angle) (s : Int) (v : Terms) := polyS s (polyA r (polyS s v))
def w01 : Terms := ⟨val 1,val 0,val 0,val 0,val 0,val 0⟩
def w02 : Terms := ⟨val 0,val 1,val 0,val 0,val 0,val 0⟩

theorem swap_plus_amplitudes (r : Angle) (d : Nat) :
    (polyA r (polyB r 1 w01)).v02 d = val (-288) d ∧
    (polyB r 1 (polyA r w01)).v02 d = val 0 d := by
  cases r <;> cases d with
  | zero => constructor <;> rfl
  | succ n => cases n <;> constructor <;> rfl

theorem swap_minus_suffix_amplitudes (r : Angle) (d : Nat) :
    (polyA r (polyA r (polyB r (-1) w02))).v02 d =
      variableTimes (val 1225) d ∧
    (polyA r (polyB r (-1) (polyA r w02))).v02 d =
      sum (val (-7200)) (variableTimes (val 8425)) d := by
  cases r <;> cases d with
  | zero => constructor <;> rfl
  | succ n => cases n <;> constructor <;> rfl

/-- An arbitrary swap double-occupancy coefficient s: its polynomial
on the raw dark witness, with an arbitrary integer evaluation of g. -/
def atG (r : Angle) (g : Int) (v : Terms) : Terms :=
  let out := polyA r v
  {out with v01 := scale v.v01 (25*g), v23 := scale v.v23 (25*g)}
def swapUnknown (v : Terms) : Terms :=
  ⟨v.v02,v.v01,v.v03,variableTimes v.v12,v.v23,v.v13⟩
def conjugateG (r : Angle) (g : Int) (v : Terms) :=
  swapUnknown (atG r g (swapUnknown v))

theorem arbitrary_swap_dark (r : Angle) (g : Int) (d : Nat) :
    (atG r g (conjugateG r g w01)).v02 d =
      sum (val (-144)) (variableTimes (val (-144))) d ∧
    (conjugateG r g (atG r g w01)).v02 d = val 0 d := by
  cases r <;> cases d with
  | zero => simp [atG,conjugateG,swapUnknown,w01,polyA,scale,sum,mix,val,variableTimes,c,h]
  | succ n => cases n <;> simp [atG,conjugateG,swapUnknown,w01,polyA,scale,sum,mix,val,variableTimes,c,h]

/-- A bivariate coefficient counts visits to a doubly occupied 01 and 23
separately. A maps either fully occupied pair back to itself with factor
25g_i; all four other outputs use two ordinary single-particle rows. -/
abbrev Bi := Nat → Terms
def zeroTerms : Terms := ⟨val 0,val 0,val 0,val 0,val 0,val 0⟩
def biStart (d : Nat) : Terms := if d=0 then w02 else zeroTerms
def biA (r : Angle) (v : Bi) (d : Nat) : Terms :=
  let prev := match d with | 0 => val 0 | k+1 => (v k).v01
  {polyA r (v d) with v01 := scale prev 25}
def biB (r : Angle) (v : Bi) (d : Nat) : Terms :=
  polyS (-1) (biA r (fun e => polyS (-1) (v e)) d)

def monomial (k l : Nat) (i : Int) (x y : Nat) :=
  if x=k ∧ y=l then i else 0

theorem distinct_bond_witness (r : Angle) (x y : Nat) :
    (biA r (biB r (biA r biStart)) x).v13 y =
      monomial 1 0 3600 x y + monomial 0 1 3600 x y + monomial 0 0 7200 x y ∧
    (biA r (biA r (biB r biStart)) x).v13 y = monomial 1 0 14400 x y := by
  cases r <;> cases x with
  | zero =>
    cases y with
    | zero => constructor <;> rfl
    | succ j => cases j <;> constructor <;> rfl
  | succ i =>
    cases i <;> cases y with
    | zero => constructor <;> rfl
    | succ j => cases j <;> constructor <;> rfl

end ContactComposition
