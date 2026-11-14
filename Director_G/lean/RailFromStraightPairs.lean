import Std

/-! A logical left/right step is represented by two identical physical
steps. A whole-well aperture after each pair keeps exactly straight pairs.
The intermediate physical well alone then recognizes the logical rail. -/
namespace RailFromStraightPairs

def dx : Bool → Int | false => 1 | true => -1
def leftBit : Bool → Int | false => 0 | true => 1

theorem pair_aperture (x : Int) (a b : Bool) :
    (2*x+dx a+dx b)%4 = (2*x+2)%4 ↔ a=b := by
  cases a <;> cases b <;> simp [dx] <;> omega

theorem middle_aperture (x : Int) (a desired : Bool) :
    (2*x+dx a)%4=(2*x+dx desired)%4 ↔ a=desired := by
  cases a <;> cases desired <;> simp [dx] <;> omega

/-- Logical departure wells on one time slice have a common parity. -/
theorem common_mask (x ref : Int) (same : x%2=ref%2) (offset : Int) :
    (2*x+offset)%4=(2*ref+offset)%4 := by omega

def doubled : List Bool → List Bool
  | [] => []
  | b :: bs => b :: b :: doubled bs

def site (x : Int) : List Bool → Int
  | [] => x
  | b :: bs => site (x+dx b) bs

def minusCount : List Bool → Int
  | [] => 0
  | b :: bs => leftBit b+minusCount bs

theorem left_count_fixed (x : Int) (w : List Bool) :
    2*minusCount w = x+(w.length:Int)-site x w := by
  induction w generalizing x with
  | nil => simp [minusCount,site]
  | cons b bs ih =>
    have h := ih (x+dx b)
    simp only [minusCount,site,List.length_cons,Int.natCast_succ]
    cases b <;> simp only [leftBit,dx] at h ⊢ <;> omega

theorem doubled_site (x : Int) (w : List Bool) : site (2*x) (doubled w)=2*site x w := by
  induction w generalizing x with
  | nil => rfl
  | cons b bs ih =>
    simp only [doubled,site]
    rw [show 2*x+dx b+dx b=2*(x+dx b) by omega,ih]

def gain (x : Int) : List Bool → Int
  | [] => 0
  | b :: bs => x/2+gain (x+dx b) bs

def paritySum (x : Int) : Nat → Int
  | 0 => 0
  | n+1 => x%2+paritySum (x+1) n

theorem parity_sum_same {x y : Int} (h : x%2=y%2) (n : Nat) :
    paritySum x n=paritySum y n := by
  induction n generalizing x y with
  | zero => rfl
  | succ n ih =>
    simp only [paritySum,h]
    rw [ih (x:=x+1) (y:=y+1) (by omega)]

theorem doubled_gain (x : Int) (w : List Bool) :
    gain (2*x) (doubled w) =
      4*gain x w + 2*paritySum x w.length - minusCount w := by
  induction w generalizing x with
  | nil => simp [doubled,gain,paritySum,minusCount]
  | cons b bs ih =>
    simp only [doubled,gain,List.length_cons,paritySum,minusCount]
    rw [show 2*x+dx b+dx b=2*(x+dx b) by omega,ih]
    have par : (x+dx b)%2=(x+1)%2 := by cases b <;> simp [dx] <;> omega
    rw [parity_sum_same par]
    cases b <;> simp only [dx,leftBit] <;> omega

def sign (source : Bool) : List Bool → Int
  | [] => 1
  | b :: bs => (if source && b then -1 else 1)*sign b bs

def leftPhase : List Bool → Int
  | [] => 1
  | b :: bs => (if b then -1 else 1)*leftPhase bs

theorem doubled_sign (source : Bool) (w : List Bool) :
    sign source (doubled w)=leftPhase w*sign source w := by
  induction w generalizing source with
  | nil => rfl
  | cons b bs ih =>
    simp only [doubled,sign,leftPhase,ih]
    cases source <;> cases b <;> simp [Int.neg_mul,Int.mul_neg]

end RailFromStraightPairs
