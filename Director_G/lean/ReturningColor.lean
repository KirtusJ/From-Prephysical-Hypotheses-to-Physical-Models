import Std

namespace ReturningColor

/-- Only the additive identities used by the unnormalized Hadamard numerators.
    The statements admit real or complex components via their additive laws. -/
structure CoeffLaws (A : Type) [Add A] [Sub A] [Neg A] [Zero A] : Prop where
  addComm : ∀ a b : A, a + b = b + a
  subIsAddNeg : ∀ a b : A, a - b = a + (-b)
  negateSub : ∀ a b : A, -(a - b) = b - a
  sumSub : ∀ a b : A, (a + b) + (a - b) = a + a
  diffSub : ∀ a b : A, (a + b) - (a - b) = b + b
  addZero : ∀ a : A, a + 0 = a
  zeroAdd : ∀ a : A, 0 + a = a
  subZero : ∀ a : A, a - 0 = a
  zeroSub : ∀ a : A, 0 - a = -a
  zeroNeg : -(0 : A) = 0
  negNeg : ∀ a : A, -(-a) = a
  negAdd : ∀ a b : A, -(a + b) = (-a) + (-b)
  subNeg : ∀ a b : A, a - (-b) = a + b
  addNeg : ∀ a : A, (-a) + a = 0

theorem intLaws : CoeffLaws Int := by constructor <;> intros <;> omega

inductive Rail | R | L deriving DecidableEq
open Rail

/-- A spectator index is carried through every operation. Arbitrary joint
    amplitude functions allow correlations with both position and rail. -/
abbrev Wave (A S : Type) := Int → Rail → S → A

variable {A S : Type} [Add A] [Sub A] [Neg A] [Zero A]

def coin (f : Wave A S) : Wave A S
  | x, R, s => f x R s + f x L s
  | x, L, s => f x R s - f x L s

def shift (d : Int) (f : Wave A S) : Wave A S
  | x, R, s => f (x-d) R s
  | x, L, s => f (x+d) L s

def flip (f : Wave A S) : Wave A S
  | x, R, s => f x L s
  | x, L, s => f x R s

def phase (f : Wave A S) : Wave A S
  | x, R, s => f x R s
  | x, L, s => -f x L s

def tick (f : Wave A S) := shift 1 (coin f)
def v0 (f : Wave A S) := flip (coin f)
def v1 (f : Wave A S) := shift 2 (phase (coin f))
def undo0 (f : Wave A S) := coin (flip f)
def undo1 (f : Wave A S) := coin (phase (shift (-2) f))
def color (x : Int) := x / 2 % 2

theorem color_left (x : Int) : color (x-2) ≠ color x := by unfold color; omega
theorem color_right (x : Int) : color (x+2) ≠ color x := by unfold color; omega

/-- U² numerator: each output rail receives its same-site term and precisely
    one term from the opposite position color. -/
theorem two_ticks (laws : CoeffLaws A) (f : Wave A S) (x : Int) (r : Rail) (s : S) :
    tick (tick f) x r s = v0 f x r s + v1 f x r s := by
  cases r <;> simp [tick, shift, coin, v0, v1, flip, phase, Int.sub_sub,
    Int.add_assoc, laws.negateSub]
  · exact laws.addComm _ _
  · rw [laws.subIsAddNeg (f x R s + f x L s), laws.negateSub]

/-- Start and end color XORs on a blank bit select the initial color from
    which the amplitude at output x can arrive. -/
def selected (b : Bool) (x : Int) (f : Wave A S) : Wave A S :=
  fun y r s => if decide (color y ≠ color x) == b then f y r s else 0

def written (b : Bool) (f : Wave A S) : Wave A S :=
  fun x r s => tick (tick (selected b x f)) x r s

theorem blank_branches (laws : CoeffLaws A) (b : Bool) (f : Wave A S) :
    written b f = if b then v1 f else v0 f := by
  funext x r s
  cases b <;> cases r <;>
    simp [written, two_ticks laws, selected, v0, v1, shift, flip, phase, coin,
      color_left, color_right, laws.addZero, laws.zeroAdd, laws.subZero, laws.zeroNeg]

theorem double_coin (laws : CoeffLaws A) (f : Wave A S) (x : Int) (r : Rail) (s : S) :
    coin (coin f) x r s = f x r s + f x r s := by
  cases r <;> simp [coin, laws.sumSub, laws.diffSub]

def corrected (b : Bool) (f : Wave A S) :=
  if b then undo1 (written b f) else undo0 (written b f)

/-- Raw common numerator 2f, with three Hadamards omitted from each path's
    denominator: each corrected branch is f/sqrt(2) in the normalized circuit. -/
theorem corrected_blank (laws : CoeffLaws A) (b : Bool) (f : Wave A S)
    (x : Int) (r : Rail) (s : S) : corrected b f x r s = f x r s + f x r s := by
  cases b <;> cases r <;>
    simp [corrected, blank_branches laws, undo0, undo1, v0, v1, coin, flip, phase,
      shift, laws.negNeg, laws.sumSub, laws.diffSub, Int.sub_sub, Int.add_assoc]

/-- Same-rail source lookup for the carrier block of the escaped half-threshold
    sign echo, up to global sign and the two Hadamard normalization factors. -/
def escaped (f : Wave A S) := undo0 (v1 f)

/-- On control one the opposite cross-block has precisely the reversed sign.
    This is the concrete anti-adjoint relation for V0† V1. -/
theorem cross_anti (laws : CoeffLaws A) (f : Wave A S) (x : Int) (r : Rail) (s : S) :
    undo1 (v0 f) x r s = -(escaped f x r s) := by
  have offset : x + (-2) = x - 2 := by omega
  cases r <;> simp [undo0, undo1, v0, v1, escaped, coin, shift, flip, phase,
    laws.negAdd, laws.negateSub, laws.subNeg, laws.negNeg, Int.sub_neg, offset]
  rw [← laws.negAdd, laws.subNeg, laws.subIsAddNeg (f (x - 2) R s + f (x - 2) L s),
    laws.negateSub, laws.addComm]

/-- A sign on address zero followed by the inverse pointer Hadamard moves
    all clean amplitude to address one. Its overall minus cancels the minus
    in the reverse cross-block, leaving the escaped carrier A f. These are
    numerator identities; the forward branch factor is common to both arms. -/
theorem signed_pointer_and_cross (laws : CoeffLaws A) (f : Wave A S)
    (x : Int) (r : Rail) (s : S) :
    (-(corrected false f x r s) + corrected true f x r s = 0) ∧
    (-(corrected false f x r s) - corrected true f x r s =
      -((f x r s + f x r s) + (f x r s + f x r s))) ∧
    (-(undo1 (v0 f) x r s) = escaped f x r s) := by
  simp [corrected_blank laws, laws.addNeg, laws.negAdd, laws.subIsAddNeg,
    cross_anti laws, laws.negNeg]
  exact (congrArg (fun z => z + (f x r s + f x r s))
    (laws.negAdd (f x r s) (f x r s)).symm).trans (laws.addNeg _)

theorem sharp_escape_support (laws : CoeffLaws A) (f : Wave A S) (origin x : Int)
    (localized : ∀ y, y ≠ origin → ∀ r s, f y r s = 0)
    (awayLeft : x ≠ origin-2) (awayRight : x ≠ origin+2) (r : Rail) (s : S) :
    escaped f x r s = 0 := by
  have h1 : x - 2 ≠ origin := by omega
  have h2 : x + 2 ≠ origin := by omega
  cases r <;> simp [escaped, undo0, v1, shift, coin, flip, phase, localized _ h1,
    localized _ h2, laws.addZero, laws.subZero, laws.zeroNeg]

end ReturningColor
