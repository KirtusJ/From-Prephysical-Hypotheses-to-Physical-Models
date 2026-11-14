import Std

namespace ContactBus

/- Lean 4.19.0, standard library only. A row or column is labeled by two
   routes, false = 0 and true = 1. Numerical witnesses are scaled by four. -/
abbrev Local := Bool → Bool → Int
abbrev PairMatrix := Bool → Bool → Bool → Bool → Int

def ident : Local := fun a b => if a == b then 1 else 0
def pauliX : Local := fun a b => if a == b then 0 else 1
def pauliZ : Local := fun a b => if a != b then 0 else if a then -1 else 1

def kron (u v : Local) : PairMatrix := fun a b c d => u a c * v b d
def xPlus : Local := fun a b => ident a b + pauliX a b
def xMinus : Local := fun a b => ident a b - pauliX a b

/-- Four times the witness written in locally measurable real observables.
    xPlus and xMinus are twice the two corresponding local projectors. -/
def fourWitness : PairMatrix := fun a b c d =>
  4 * kron ident ident a b c d - kron xPlus xPlus a b c d +
  2 * kron pauliZ xMinus a b c d + 2 * kron xMinus pauliZ a b c d +
  2 * kron pauliZ pauliZ a b c d

def witnessVector : Bool → Bool → Int
  | false, false => 3
  | _, _ => -1

/-- 8W = vvᵀ + (vvᵀ)^{T_B}. This is the matrix identity used in the
    separable bound: on a product vector each addend has a nonnegative
    expectation, the second after conjugating the second local vector. -/
theorem local_witness_identity (a b c d : Bool) :
    2 * fourWitness a b c d =
    witnessVector a b * witnessVector c d + witnessVector a d * witnessVector c b := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

/-- Real part of 4nρ for a balanced product launch, with x/n = Re γ.
    An unread endpoint phase affects entries joining 11 to its complement. -/
def stateNumerator (n x : Int) : PairMatrix := fun a b c d =>
  if (a && b) == (c && d) then n else x

def sumBit (f : Bool → Int) : Int := f false + f true

def tracePair (w r : PairMatrix) : Int :=
  sumBit fun a => sumBit fun b => sumBit fun c => sumBit fun d => w a b c d * r c d a b

/-- The left side is 16n times the witness expectation. -/
theorem balanced_signal (n x : Int) :
    tracePair fourWitness (stateNumerator n x) = 2 * (x-n) := by
  simp [tracePair, sumBit, fourWitness, kron, stateNumerator, ident, pauliX, pauliZ, xPlus, xMinus]
  omega

/-- White noise has expectation 3/4 because both witness and state have
    been scaled by 4 on the left. -/
theorem white_noise_signal : tracePair fourWitness (kron ident ident) = 12 := by
  decide

/-- For a blank, the integer-scaled mixed signal is negative exactly when
    the white-noise weight w/(b+w) is below 1/7, for positive total weight. -/
theorem blank_noise_threshold (b w : Int) :
    b * tracePair fourWitness (stateNumerator 1 0) +
      w * tracePair fourWitness (kron ident ident) < 0 ↔ 7*w < b+w := by
  rw [balanced_signal, white_noise_signal]
  omega

end ContactBus
