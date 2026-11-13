import Std

/-!
# A dyadic herald for equal-amplitude leaves

Coordinates are integer numerators; the auxiliary column denominator is D.
Lists denote orthogonal coordinates, and separate input labels are retained.
Success and failure have their own ports. Squared integer lengths below
certify the prepared columns; they do not assume an empirical probability law.
-/
namespace HeraldedWeights

def normSq : List Int → Nat
  | [] => 0
  | a :: xs => a.natAbs^2 + normSq xs

private theorem norm_replicate (n : Nat) (a : Int) :
    normSq (List.replicate n a) = n*a.natAbs^2 := by
  induction n with
  | zero => simp [normSq]
  | succ n ih => simp [List.replicate_succ, normSq, ih, Nat.succ_mul, Nat.add_comm]

/-- A zero input still gets a normalized auxiliary column: take one
success coordinate of amplitude m, whose amplitude on that input is zero. -/
def successColumn (a : Int) (m : Nat) : List Int :=
  if a = 0 then [(m:Int)]
  else List.replicate (a.natAbs^2) (if 0 ≤ a then ((m/a.natAbs : Nat):Int)
                                               else -((m/a.natAbs : Nat):Int))

def failureColumn (D m : Nat) : List Int := List.replicate (D^2-m^2) 1

theorem success_norm (a : Int) (m : Nat) (divides : a ≠ 0 → a.natAbs ∣ m) :
    normSq (successColumn a m) = m^2 := by
  unfold successColumn
  split
  · simp [normSq]
  · rename_i hn
    have h := Nat.mul_div_cancel' (divides hn)
    rw [norm_replicate]
    split <;> simp only [Int.natAbs_neg, Int.natAbs_ofNat] <;>
      rw [← Nat.mul_pow, h]

theorem normalized_column (a : Int) (D m : Nat) (fits : m ≤ D)
    (divides : a ≠ 0 → a.natAbs ∣ m) :
    normSq (successColumn a m) + normSq (failureColumn D m) = D^2 := by
  have sq := Nat.pow_le_pow_left fits 2
  rw [success_norm a m divides]
  simp [failureColumn, norm_replicate]
  omega

/-- Every occupied input produces exactly |a|² nonzero leaves with common
positive numerator m, using the sign of a in the controlled column. -/
theorem occupied_success_output (a : Int) (m : Nat) (ha : a ≠ 0)
    (divides : a.natAbs ∣ m) :
    (successColumn a m).map (fun c => a*c) = List.replicate (a.natAbs^2) (m:Int) := by
  have h := Nat.mul_div_cancel' divides
  have hp : (a.natAbs:Int)*((m/a.natAbs : Nat):Int) = (m:Int) := by exact_mod_cast h
  simp only [successColumn, if_neg ha, List.map_replicate]
  split
  · rename_i pos
    rw [Int.natAbs_of_nonneg pos] at hp
    rw [hp]
  · rename_i neg
    have hs : a = -(a.natAbs:Int) := by
      rcases Int.natAbs_eq a with pos | minus
      · have nonneg : 0 ≤ (a.natAbs:Int) := by omega
        omega
      · exact minus
    have pp : a * -((m/a.natAbs : Nat):Int) = (m:Int) := by
      calc
        a * -((m/a.natAbs : Nat):Int) = -(a.natAbs:Int) * -((m/a.natAbs : Nat):Int) :=
          congrArg (fun v : Int => v * -((m/a.natAbs : Nat):Int)) hs
        _ = (m:Int) := by rw [Int.neg_mul_neg]; exact hp
    rw [pp]

theorem zero_success_output (m : Nat) :
    (successColumn 0 m).map (fun c => (0:Int)*c) = [0] := by simp [successColumn]

/-- The failure output is the old signed amplitude times one fixed vector.
The same assertion includes a zero coordinate and an empty failure block. -/
theorem factorized_failure_output (a : Int) (D m : Nat) :
    (failureColumn D m).map (fun c => a*c) = List.replicate (D^2-m^2) a := by
  simp [failureColumn]

/-- The product of nonzero magnitudes suffices; an lcm can be smaller. -/
def commonMultiple : List Int → Nat
  | [] => 1
  | a :: xs => (max 1 a.natAbs) * commonMultiple xs

theorem common_factors (xs : List Int) :
    0 < commonMultiple xs ∧ ∀ a ∈ xs, a ≠ 0 → a.natAbs ∣ commonMultiple xs := by
  induction xs with
  | nil => simp [commonMultiple]
  | cons a xs ih =>
    have pos : 0 < max 1 a.natAbs := by omega
    refine ⟨Nat.mul_pos pos ih.1, ?_⟩
    intro b mem nz
    rcases List.mem_cons.mp mem with same | tail
    · subst b
      have ha := Int.natAbs_pos.mpr nz
      simpa [commonMultiple, Nat.max_eq_right ha] using Nat.dvd_mul_right a.natAbs (commonMultiple xs)
    · exact Nat.dvd_mul_left_of_dvd (ih.2 b tail nz) _

/-- Each finite signed input admits a positive common multiplier and a
power-of-two column denominator, even if all input coordinates vanish. -/
theorem finite_dyadic_budget (xs : List Int) :
    ∃ m k : Nat, 0 < m ∧ m ≤ 2^k ∧ ∀ a ∈ xs, a ≠ 0 → a.natAbs ∣ m := by
  have h := common_factors xs
  exact ⟨commonMultiple xs, commonMultiple xs, h.1, Nat.le_of_lt Nat.lt_two_pow_self, h.2⟩

/-- Choose the largest admissible multiple at any larger dyadic denominator.
Its shortfall in amplitude numerator is less than one fixed multiple. -/
theorem rounded_multiplier (L k : Nat) (positive : 0 < L) (fits : L ≤ 2^k) :
    ∃ m : Nat, 0 < m ∧ L ∣ m ∧ m ≤ 2^k ∧ 2^k-m < L := by
  refine ⟨L*(2^k/L), ?_, Nat.dvd_mul_right _ _, ?_, ?_⟩
  all_goals
    have div := Nat.mod_add_div (2^k) L
    have rem := Nat.mod_lt (2^k) positive
    omega

/-- The squared integer length modulo four counts the odd entries modulo
four, allowing those entries to be grouped into quartets at a nonzero
denominator exponent. -/
def oddCount : List Int → Nat
  | [] => 0
  | a::xs => (a.natAbs%2) + oddCount xs

theorem odd_count_mod_four (xs : List Int) : normSq xs % 4 = oddCount xs % 4 := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    have sq (u : Nat) : u^2%4 = u%2 := by
      have four := Nat.mod_lt u (by decide : 0 < 4)
      rw [Nat.pow_two, Nat.mul_mod]
      have reduce : (u%4)%2=u%2 := by omega
      rw [← reduce]
      have choices : u%4=0 ∨ u%4=1 ∨ u%4=2 ∨ u%4=3 := by omega
      rcases choices with hz | hz | hz | hz <;> rw [hz] <;> decide
    change (a.natAbs^2+normSq xs)%4=(a.natAbs%2+oddCount xs)%4
    rw [Nat.add_mod, sq, ih]
    have small : a.natAbs%2 < 4 := by omega
    calc
      _ = (a.natAbs%2%4 + oddCount xs%4)%4 := by rw [Nat.mod_eq_of_lt small]
      _ = _ := (Nat.add_mod _ _ _).symm

/-- Elementary parity reduction for the four-mode unnormalized Walsh mixer.
Signs have already been chosen so that the four old numerators are 1 mod 4.
After the actual Walsh divisor 2 each new numerator is even. -/
theorem quartet_even_outputs (a b c d : Int) (ha : a%4=1) (hb : b%4=1)
    (hc : c%4=1) (hd : d%4=1) :
    ((a+b+c+d)/2)%2=0 ∧ ((a-b+c-d)/2)%2=0 ∧
    ((a+b-c-d)/2)%2=0 ∧ ((a-b-c+d)/2)%2=0 := by omega

/-- A common failure factor gives the old-label refinement relation over any
weight domain satisfying the three displayed arithmetic laws. We keep
normalization homogeneous so the statement also applies to real weights.
W is a candidate old-record mass, U its total scale, H>0 the common
success factor, and c the mass per successful leaf in common units.
The caller supplies cancellation at H, as on the reals when H is positive. -/
theorem cancel_common_herald {R : Type} [Add R] [Mul R]
    (W U H F J T c n N : R)
    (distribute : ∀ x y z : R, x*(y+z) = x*y + x*z)
    (add_cancel : ∀ x y z : R, x+z = y+z → x=y)
    (reorder : ∀ x y z : R, (x*y)*z = (x*z)*y)
    (positive_cancel : ∀ x y : R, x*H = y*H → x=y)
    (total_ports : H+F=T) (old_marginal : J+W*F=W*T)
    (equal_weight : J=c*n) (whole_success : U*H=c*N) :
    W*N=U*n := by
  have joint : J=W*H := by
    apply add_cancel _ _ (W*F)
    rw [old_marginal, ← distribute, total_ports]
  apply positive_cancel
  calc
    (W*N)*H = (W*H)*N := reorder ..
    _ = (c*n)*N := by rw [← joint, equal_weight]
    _ = (c*N)*n := reorder ..
    _ = (U*H)*n := by rw [whole_success]
    _ = (U*n)*H := reorder ..

/-- Let w_i = W_i/D0 and h = H/D1 be exact fractions, with h>0. If a
direct old-record read agrees with refinement and both ports have common
old-record effects, the formal joint success mass is w_i*h. Equal success
leaves then enforce w_i = n_i/N. The theorem below is the denominator-cleared
version; the w_i share denominator D0 and all joint weights share D0*D1. -/
theorem old_record_cancellation (W D0 H D1 n N J F : Nat) (hpos : 0 < H)
    (hfits : H ≤ D1) (partition : J+F = W*D1) (failure : F = W*(D1-H))
    (equal_leaves : J*N = n*(D0*H)) :
    W*N = n*D0 := by
  have sum : H+(D1-H) = D1 := by omega
  have split : W*H + W*(D1-H) = W*D1 := by rw [← Nat.mul_add, sum]
  have joint : J = W*H := by omega
  have eq : (W*N)*H = (n*D0)*H := by
    calc
      (W*N)*H = (W*H)*N := by ac_rfl
      _ = n*(D0*H) := by rw [← joint]; exact equal_leaves
      _ = (n*D0)*H := by ac_rfl
  exact Nat.eq_of_mul_eq_mul_right hpos eq

end HeraldedWeights
