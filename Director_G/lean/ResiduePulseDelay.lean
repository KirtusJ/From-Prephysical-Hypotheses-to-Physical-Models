import Std

/-! Sheet gains are sums over departure coordinates. A pulse starts at a
reservoir, traverses a specified sequence of relative deficits, and lands
at a wall of width H. Delaying the same traversal trades H-wall holds for
zero-deficit holds within a fixed clock interval. -/
namespace ResiduePulseDelay

def tally : List Int → Int
  | [] => 0
  | d :: ds => d + tally ds

def physicalGain (clock : Int) : List Int → Int
  | [] => 0
  | d :: ds => (clock-2*d)/2 + physicalGain (clock+1) ds

def clockGain (clock : Int) : Nat → Int
  | 0 => 0
  | n+1 => clock/2 + clockGain (clock+1) n

theorem reduce_gain (ds : List Int) (clock : Int) :
    physicalGain clock ds = clockGain clock ds.length - tally ds := by
  induction ds generalizing clock with
  | nil => rfl
  | cons d ds ih =>
    simp only [physicalGain, List.length_cons, clockGain, tally, ih]
    omega

private theorem tally_append (a b : List Int) :
    tally (a++b) = tally a + tally b := by
  induction a with
  | nil => simp [tally]
  | cons d ds ih => simp [tally, ih, Int.add_assoc]

private theorem tally_holds (n : Nat) (d : Int) :
    tally (List.replicate n d) = (n:Int)*d := by
  induction n with
  | zero => simp [tally]
  | succ n ih =>
    simp [List.replicate_succ, tally, ih, Int.natCast_succ, Int.add_mul, Int.add_comm]

/-- Padding of length wait+tail, split before and after the traversal.
The list of departures for L^H R is 0,1,...,H. A single internal R at
deficit 2 repeats its 2 in that list. A global corridor offset b can
equivalently replace clock by clock-2*b in the two equal-length trials. -/
def padded (width : Int) (route : List Int) (wait tail : Nat) : List Int :=
  List.replicate wait 0 ++ route ++ List.replicate tail width

theorem delayed (width clock : Int) (route : List Int) (wait tail : Nat) :
    physicalGain clock (padded width route wait tail) =
    physicalGain clock (padded width route 0 (wait+tail)) + width*(wait:Int) := by
  rw [reduce_gain, reduce_gain]
  have len : (padded width route wait tail).length =
      (padded width route 0 (wait+tail)).length := by
    simp [padded]; omega
  rw [len]
  simp only [padded, tally_append, tally_holds, Int.natCast_add, Int.natCast_zero,
    Int.mul_zero, Int.zero_add, Int.add_mul]
  rw [Int.mul_comm width (wait:Int)]
  omega

/-- When width is M-1, choose delay (base-target) mod M, represented by
a nonnegative number strictly smaller than M. -/
theorem tune (M base target : Int) (positive : 0 < M) :
    ∃ delay : Nat, (delay:Int) < M ∧
      (base + (M-1)*(delay:Int)) % M = target % M := by
  let z := (base-target) % M
  have lo : 0 ≤ z := Int.emod_nonneg _ (by omega)
  have hi : z < M := Int.emod_lt_of_pos _ positive
  have cast : (z.toNat:Int) = z := by omega
  refine ⟨z.toNat, by omega, ?_⟩
  rw [cast]
  have h := Int.ediv_add_emod (base-target) M
  change M*((base-target)/M)+z = base-target at h
  have reduce : base+(M-1)*z = target + M*(((base-target)/M)+z) := by
    rw [Int.sub_mul, Int.one_mul, Int.mul_add]
    omega
  rw [reduce, Int.add_mul_emod_self_left]

/-- At exactly `route.length + (M-1)` ticks and at the same starting clock,
any prescribed sheet is reached by moving holds across that one route. -/
theorem fixed_slot (M : Nat) (positive : 0 < M) (clock target : Int)
    (route : List Int) :
    ∃ wait : Nat, wait < M ∧
      physicalGain clock (padded ((M:Int)-1) route wait (M-1-wait)) % (M:Int) =
        target % (M:Int) := by
  let width : Int := (M:Int)-1
  let base := physicalGain clock (padded width route 0 (M-1))
  obtain ⟨w, hw, hit⟩ := tune (M:Int) base target (by omega)
  have below : w < M := by omega
  refine ⟨w, below, ?_⟩
  have same_slot : w+(M-1-w) = M-1 := by omega
  rw [delayed, same_slot]
  exact hit

end ResiduePulseDelay
