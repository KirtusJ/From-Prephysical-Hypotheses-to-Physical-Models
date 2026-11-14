import Std

/-! Renewal words for a monitored return. The scalar and state types are
abstract. For the quantum specialization the states are unnormalized
positive operators, the multiplying scalars are nonnegative reals, and
the final weight is trace. No probability rule is derived by this file.
Tested with Lean 4.19.0 and Std. -/

namespace ReturnRenewal

variable {Weight State : Type} [Mul Weight]

/-- Read chronologically. A true bit is a return. -/
def recordMass (miss hit : State → State) (mass : State → Weight)
    (v : State) : List Bool → Weight
  | [] => mass v
  | false :: tail => recordMass miss hit mass (miss v) tail
  | true :: tail => recordMass miss hit mass (hit v) tail

theorem recordMass_scale (miss hit : State → State) (mass : State → Weight)
    (scale : Weight → State → State)
    (miss_scale : ∀ a v, miss (scale a v) = scale a (miss v))
    (hit_scale : ∀ a v, hit (scale a v) = scale a (hit v))
    (mass_scale : ∀ a v, mass (scale a v) = a * mass v)
    (a : Weight) (v : State) (bits : List Bool) :
    recordMass miss hit mass (scale a v) bits =
      a * recordMass miss hit mass v bits := by
  induction bits generalizing v with
  | nil => exact mass_scale a v
  | cons bit rest ih =>
    cases bit <;> simp only [recordMass, miss_scale, hit_scale, ih]

def ageState (miss : State → State) (reset : State) : Nat → State
  | 0 => reset
  | k+1 => miss (ageState miss reset k)

/-- A complete word contributes one first-return mass per completed gap
and the survival mass of its final, possibly empty, string of misses.
The argument k counts misses already elapsed in the first gap. -/
def gapProduct (survival first : Nat → Weight) (k : Nat) : List Bool → Weight
  | [] => survival k
  | false :: tail => gapProduct survival first (k+1) tail
  | true :: tail => first k * gapProduct survival first 0 tail

/-- Rank-one return restores the same state up to a mass factor. Each
first k refers to a hit after k misses, hence to tick k+1. -/
theorem reset_factorization (miss hit : State → State) (mass : State → Weight)
    (scale : Weight → State → State) (reset : State) (first : Nat → Weight)
    (miss_scale : ∀ a v, miss (scale a v) = scale a (miss v))
    (hit_scale : ∀ a v, hit (scale a v) = scale a (hit v))
    (mass_scale : ∀ a v, mass (scale a v) = a * mass v)
    (on_return : ∀ k, hit (ageState miss reset k) = scale (first k) reset)
    (k : Nat) (bits : List Bool) :
    recordMass miss hit mass (ageState miss reset k) bits =
      gapProduct (fun j => mass (ageState miss reset j)) first k bits := by
  induction bits generalizing k with
  | nil => rfl
  | cons bit rest ih =>
    cases bit with
    | false => exact ih (k+1)
    | true =>
      simp only [recordMass, gapProduct, on_return,
        recordMass_scale miss hit mass scale miss_scale hit_scale mass_scale]
      exact congrArg (fun v => first k * v) (ih 0)

variable [OfNat Weight 1]

/-- A classical age record multiplies conditional transition probabilities.
A miss advances the age; a click resets it to zero. -/
def ageRecord (pass fire : Nat → Weight) (k : Nat) : List Bool → Weight
  | [] => 1
  | false :: tail => pass k * ageRecord pass fire (k+1) tail
  | true :: tail => fire k * ageRecord pass fire 0 tail

/-- Only transition identities at ages strictly below H are needed.
For normalized survival S, take pass k = S(k+1)/S(k) and
fire k = first(k)/S(k) whenever S(k)>0. At S(k)=0 either transition
may be chosen as long as they form a distribution: both weighted
identities are zero. The state following the final tick is immaterial. -/
theorem finite_age_telescope
    (assoc : ∀ a b c : Weight, (a*b)*c = a*(b*c))
    (one_left : ∀ a : Weight, 1*a = a)
    (one_right : ∀ a : Weight, a*1 = a)
    (survival first pass fire : Nat → Weight) (H : Nat)
    (fresh : survival 0 = 1)
    (miss_mass : ∀ k, k < H → survival k * pass k = survival (k+1))
    (hit_mass : ∀ k, k < H → survival k * fire k = first k)
    (k : Nat) (bits : List Bool) (within : k + bits.length ≤ H) :
    survival k * ageRecord pass fire k bits = gapProduct survival first k bits := by
  induction bits generalizing k with
  | nil => exact one_right (survival k)
  | cons bit rest ih =>
    simp only [List.length_cons] at within
    have hk : k < H := by omega
    cases bit with
    | false =>
      rw [ageRecord, ← assoc, miss_mass k hk, gapProduct]
      exact ih (k+1) (by omega)
    | true =>
      rw [ageRecord, ← assoc, hit_mass k hk, gapProduct]
      have fresh_record := ih 0 (by omega)
      rw [fresh, one_left] at fresh_record
      exact congrArg (fun v => first k * v) fresh_record

/-- The last available age is L, so the machine has exactly L+1
possible internal states. After a miss at age L it may stay there:
no further output is required within the promised horizon. -/
def cappedAgeRecord (pass fire : Nat → Weight) (L k : Nat) : List Bool → Weight
  | [] => 1
  | false :: tail => pass k * cappedAgeRecord pass fire L (min (k+1) L) tail
  | true :: tail => fire k * cappedAgeRecord pass fire L 0 tail

theorem cap_next_in_range (L k : Nat) : min (k+1) L ≤ L := Nat.min_le_right _ _

theorem capped_age_exact (pass fire : Nat → Weight) (L k : Nat) (bits : List Bool)
    (within : k + bits.length ≤ L+1) :
    cappedAgeRecord pass fire L k bits = ageRecord pass fire k bits := by
  induction bits generalizing k with
  | nil => rfl
  | cons bit rest ih =>
    simp only [List.length_cons] at within
    cases bit with
    | true =>
      exact congrArg (fun v => fire k * v) (ih 0 (by omega))
    | false =>
      cases rest with
      | nil => rfl
      | cons next later =>
        simp only [List.length_cons] at within
        have inside : k+1 ≤ L := by omega
        simp only [cappedAgeRecord, Nat.min_eq_left inside, ageRecord]
        exact congrArg (fun v => pass k * v) (ih (k+1) (by simp; omega))

/-- Integer counts on a common denominator. At positive age mass s
the miss and hit probabilities have numerators t and s-t and share
denominator s. The zero-mass case is unreachable. -/
theorem count_kernel (s t : Nat) (nested : t ≤ s) :
    t + (s-t) = s ∧ t ≤ s ∧ s-t ≤ s := by omega

/-- Polynomial identity used at angle pi/5, in denominator-cleared
coordinates. Substitution of u²=5 gives the numerator of
c(c+1)²−2 with c=(1+u)/4. This checks the expansion only. -/
theorem phase_trace_expansion (u : Int) :
    (1+u)*(5+u)*(5+u)-128 - 8*(-6+5*u) =
      (u+11)*(u*u-5) := by
  simp only [Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul,
    Int.one_mul, Int.mul_one]
  have u5 : u * (5*u) = 5*(u*u) := by
    rw [← Int.mul_assoc, Int.mul_comm u 5, Int.mul_assoc]
  have u11 : 11 * u * u = 11*(u*u) := Int.mul_assoc _ _ _
  simp only [Int.mul_assoc, Int.mul_comm (5 : Int) u, u5, u11] at *
  omega

/-- Cleared polynomial for the mixed whole-mask / resolved-port contrast.
    A nonnegative integer u corresponds to the algebraic variable 4^q.
    The proof is a coefficient check, independent of the exponent law. -/
theorem mixed_order_polynomial (u : Int) :
    (u-4)*(u*u+3*u+4-32) = (u-4)*(u-4)*(u+7) := by
  have factor : u*u+3*u+4-32 = (u-4)*(u+7) := by
    simp only [Int.sub_mul, Int.mul_add, Int.mul_one, Int.mul_comm u 7]
    omega
  rw [factor, Int.mul_assoc]

end ReturnRenewal
