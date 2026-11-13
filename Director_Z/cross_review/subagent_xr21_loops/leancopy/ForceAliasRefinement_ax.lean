import Std

/-! # Coherent bounded doubled residues over all odd moduli

An odd modulus is represented by the positive integer 2j+1. k and its inverse
are represented modulo each odd modulus, rather than chosen as signed lifts
in advance. Every modulus is included. Directed cofinal data can be extended
to these residues by reduction from a common multiple. All arithmetic is exact.
-/
namespace ForceAliasRefinement

private theorem no_wrap (u v M B : Int) (wide : 2*B<M)
    (hu : -B≤u ∧ u≤B) (hv : -B≤v ∧ v≤B) (h : u%M=v%M) : u=v := by
  have c := Int.emod_eq_emod_iff_emod_sub_eq_zero.mp h
  by_cases pos : v≤u
  · rw [Int.emod_eq_of_lt (by omega) (by omega)] at c
    omega
  · have shifted : (u-v+M)%M=0 := by simpa using c
    rw [Int.emod_eq_of_lt (by omega) (by omega)] at shifted
    omega

theorem odd_cancel (m u v : Int) (h : (2*u)%(2*m+1)=(2*v)%(2*m+1)) :
    u%(2*m+1)=v%(2*m+1) := by
  have inverse (z : Int) :
      (2*z*(m+1))%(2*m+1)=z%(2*m+1) := by
    have e : (2*z)*(m+1)=z+(2*m+1)*z := by
      simp [Int.add_mul,Int.mul_add,Int.mul_comm,Int.mul_left_comm,Int.mul_assoc] <;> omega
    rw [e,Int.add_mul_emod_self_left]
  calc
    _ = ((2*u)*(m+1))%(2*m+1) := (inverse u).symm
    _ = ((2*v)*(m+1))%(2*m+1) := by rw [Int.mul_emod (2*u),h,← Int.mul_emod]
    _ = _ := inverse v

def modulus (j : Nat) : Int := 2*(j:Int)+1

def commonIndex (i j : Nat) := 2*i*j+i+j

private theorem common_value (i j : Nat) : modulus (commonIndex i j) = modulus i * modulus j := by
  simp only [commonIndex,modulus,Int.natCast_add,Int.natCast_mul,
    Int.add_mul,Int.mul_add,Int.one_mul,Int.mul_one,Int.mul_assoc]
  rw [Int.mul_left_comm (i:Int) 2 (j:Int)]
  generalize (i:Int)*(j:Int)=z
  omega

abbrev Family := Nat → Int

def Compatible (k : Family) :=
  ∀ i j, modulus i ∣ modulus j → k j % modulus i=k i % modulus i

/-- A real signed observed representative of the doubled phase sits within
the stated range. The sign of d is not fixed externally. -/
def BoundedRead (k : Family) (B : Int) :=
  ∀ j, ∃ d : Int, (-B≤d ∧ d≤B) ∧ (2*k j)%modulus j=d%modulus j

private theorem double_reduce (k : Family) (coh : Compatible k) (i j : Nat)
    (divides : modulus i ∣ modulus j) (z : Int) (at_j : (2*k j)%modulus j=z%modulus j) :
    (2*k i)%modulus i=z%modulus i := by
  have red := congrArg (fun a : Int => a%modulus i) at_j
  dsimp only at red
  rw [Int.emod_emod_of_dvd _ divides,Int.emod_emod_of_dvd _ divides] at red
  calc
    _ = (2*k j)%modulus i := by
      rw [Int.mul_emod 2 (k i),← coh i j divides,← Int.mul_emod]
    _ = _ := red

/-- One sufficiently large reference modulus and one intersecting common
observation suffice to force equality of the small representatives. -/
theorem two_scale_determination (u v : Int) (i : Nat) (B : Int)
    (wide : 2*B<modulus i) (left : -B≤u ∧ u≤B) (right : -B≤v ∧ v≤B)
    (coherentRead : u%modulus i=v%modulus i) : u=v :=
  no_wrap _ _ _ _ wide left right coherentRead

theorem bounded_identification (k : Family) (coh : Compatible k) (B : Nat)
    (bound : BoundedRead k B) :
    ∃ n : Int, (-(B:Int)≤n ∧ n≤(B:Int)) ∧ ∀ j, (2*k j)%modulus j=n%modulus j := by
  obtain ⟨n,hn,ref⟩ := bound B
  refine ⟨n,hn,?_⟩
  intro j
  let p := commonIndex B j
  have pr : modulus B ∣ modulus p := by rw [common_value]; exact Int.dvd_mul_right _ _
  have pj : modulus j ∣ modulus p := by rw [common_value]; exact Int.dvd_mul_left _ _
  obtain ⟨v,hv,h⟩ := bound p
  have fromRef := double_reduce k coh B p pr v h
  have eq : n=v := two_scale_determination n v B B (by dsimp [modulus]; omega) hn hv
    (ref.symm.trans fromRef)
  rw [eq]
  exact double_reduce k coh j p pj v h

def Units (k : Family) := ∀ j, ∃ v : Int, (k j*v)%modulus j=1%modulus j

private theorem unit_not_zero (k u M : Int) (size : 1<M) (inverse : (k*u)%M=1%M) :
    k%M≠0 := by
  intro hz
  rw [Int.mul_emod k u,hz,Int.zero_mul,Int.zero_emod,
      Int.emod_eq_of_lt (by decide : (0:Int)≤1) size] at inverse
  omega

/-- The doubled global integer cannot have an odd divisor >1, prime or not. -/
theorem no_odd_divisor (k : Family) (units : Units k) (n : Int)
    (same : ∀j,(2*k j)%modulus j=n%modulus j) (d : Nat) (odd : d%2=1)
    (divisor : d ∣ n.natAbs) : d=1 := by
  by_cases h1 : d=1
  · exact h1
  let j := d/2
  have size : 1<(d:Int) := by omega
  have rep : modulus j=(d:Int) := by dsimp [modulus,j]; omega
  have zero : n%modulus j=0 := Int.emod_eq_zero_of_dvd (by
    rw [rep]; exact Int.ofNat_dvd_left.mpr divisor)
  have obs := (same j).trans zero
  have cc : k j % modulus j=0 := by
    have hc : (2*k j)%(2*(j:Int)+1)=(2*0)%(2*(j:Int)+1) := by simpa [modulus] using obs
    simpa [modulus] using odd_cancel j (k j) 0 hc
  obtain ⟨v,hi⟩ := units j
  have impossible := unit_not_zero (k j) v (modulus j) (by rw [rep]; exact size) hi
  exact (impossible cc).elim

private theorem power_of_two (s : Nat) (pos : 0<s)
    (divs : ∀d : Nat,d%2=1 → d∣s → d=1) : ∃a : Nat,s=2^a := by
  induction s using Nat.strongRecOn with
  | ind s ih =>
    by_cases odd : s%2=1
    · exact ⟨0,by simpa using divs s odd (Nat.dvd_refl _)⟩
    · have even : s=2*(s/2) := by omega
      have right : ∀d : Nat, d%2=1 → d∣s/2 → d=1 := by
        intro d h hd
        apply divs d h
        have factor : s/2∣s := ⟨2,by omega⟩
        exact Nat.dvd_trans hd factor
      obtain ⟨a,ha⟩ := ih (s/2) (by omega) (by omega) right
      refine ⟨a+1,?_⟩
      calc
        s=2*(s/2) := even
        _=2*2^a := by rw [ha]
        _=2^(a+1) := by rw [Nat.pow_succ,Nat.mul_comm]

theorem bounded_unit_classification (k : Family) (coh : Compatible k) (units : Units k)
    (B : Nat) (bound : BoundedRead k B) :
    ∃ (n : Int) (a : Nat), n.natAbs=2^a ∧ (-(B:Int)≤n ∧ n≤(B:Int)) ∧
      ∀j,(2*k j)%modulus j=n%modulus j := by
  obtain ⟨n,range,h⟩ := bounded_identification k coh B bound
  have divs := no_odd_divisor k units n h
  have nonzero : 0<n.natAbs := by
    by_cases z : n.natAbs=0
    · have e := divs 3 (by decide) (by simp [z])
      omega
    · omega
  obtain ⟨a,ha⟩ := power_of_two n.natAbs nonzero divs
  exact ⟨n,a,ha,range,h⟩

/-- Half is represented by j+1 mod 2j+1. Its doubled signed residue is 1.
Although the measured effective size is 1/2 at every modulus >1, the
shortest undoubled representative at order 2j+1 has size j. -/
def half (j : Nat) : Int := (j:Int)+1

theorem doubled_half (j : Nat) : (2*half j)%modulus j = 1%modulus j := by
  have eq : 2*half j = 1+modulus j := by dsimp [half,modulus]; omega
  rw [eq,Int.add_emod_self]

theorem half_unit : Units half := by
  intro j
  exact ⟨2,by rw [Int.mul_comm]; exact doubled_half j⟩

theorem half_compatible : Compatible half := by
  intro i j divides
  apply odd_cancel i
  have h := congrArg (fun a : Int => a%modulus i) (doubled_half j)
  dsimp only at h
  rw [Int.emod_emod_of_dvd _ divides,Int.emod_emod_of_dvd _ divides] at h
  exact h.trans (doubled_half i).symm

theorem calibrated_unit_scale (j : Nat) (k : Int) :
    ((2*k)%modulus j=2%modulus j ∨ (2*k)%modulus j=(-2)%modulus j) ↔
    k%modulus j=1%modulus j ∨ k%modulus j=(-1)%modulus j := by
  constructor
  · rintro (h|h)
    · left; apply odd_cancel j; simpa using h
    · right; apply odd_cancel j; simpa using h
  · rintro (h|h)
    · left; rw [Int.mul_emod 2 k,h,← Int.mul_emod]; simp
    · right; rw [Int.mul_emod 2 k,h,← Int.mul_emod]; simp

/-- A uniform bound is needed only on a divisor-cofinal collection of
observed orders. Agreement with finer orders propagates it to every level. -/
theorem extend_bounds_from_cofinal (k : Family) (coh : Compatible k) (B : Nat)
    (observed : Nat → Prop) (cofinal : ∀ i,∃ j,observed j ∧ modulus i∣modulus j)
    (bound : ∀j,observed j → ∃ d : Int, (-(B:Int)≤d ∧ d≤(B:Int)) ∧
                                         (2*k j)%modulus j=d%modulus j) :
    BoundedRead k B := by
  intro i
  obtain ⟨j,hj,hdiv⟩ := cofinal i
  obtain ⟨d,hd,h⟩ := bound j hj
  exact ⟨d,hd,double_reduce k coh i j hdiv d h⟩

/-- A physical calibration matching effective magnitude one at arbitrarily
fine divisor-cofinal orders picks one sign for all orders simultaneously.
Conjugation flips that global sign. -/
theorem calibrated_global (k : Family) (coh : Compatible k) (observed : Nat → Prop)
    (cofinal : ∀ i,∃ j,observed j ∧ modulus i∣modulus j)
    (matchData : ∀ j,observed j → (2*k j)%modulus j=2%modulus j ∨
      (2*k j)%modulus j=(-2)%modulus j) :
    (∀j,k j%modulus j=1%modulus j) ∨ (∀j,k j%modulus j=(-1)%modulus j) := by
  have observedBound (j : Nat) (hj : observed j) :
      ∃d : Int,(-(2:Int)≤d ∧ d≤(2:Int)) ∧ (2*k j)%modulus j=d%modulus j := by
    rcases matchData j hj with h|h
    · exact ⟨2,by decide,h⟩
    · exact ⟨-2,by decide,h⟩
  obtain ⟨n,hN,full⟩ := bounded_identification k coh 2
    (extend_bounds_from_cofinal k coh 2 observed cofinal observedBound)
  obtain ⟨s,hs,ds⟩ := cofinal 2
  have useSign : n=2 ∨ n= -2 := by
    rcases matchData s hs with h|h
    · left
      have eq := (full 2).symm.trans (double_reduce k coh 2 s ds 2 h)
      exact no_wrap _ _ _ 2 (by decide) hN (by decide) eq
    · right
      have eq := (full 2).symm.trans (double_reduce k coh 2 s ds (-2) h)
      exact no_wrap _ _ _ 2 (by decide) hN (by decide) eq
  rcases useSign with h|h
  · left; intro j; apply odd_cancel j; simpa [h,modulus] using full j
  · right; intro j; apply odd_cancel j; simpa [h,modulus] using full j

/-- All integral nonnegative powers of two, as well as the preceding
half-family, give actual coherent units. -/
theorem power_units (a : Nat) : Units (fun _ => (2:Int)^a) := by
  intro j
  induction a with
  | zero => exact ⟨1,by simp⟩
  | succ a ih =>
    obtain ⟨v,h⟩ := ih
    refine ⟨v*half j,?_⟩
    have rearrange : (2:Int)^(a+1)*(v*half j)=((2:Int)^a*v)*(2*half j) := by
      simp only [Int.pow_succ,Int.mul_assoc,Int.mul_comm,Int.mul_left_comm]
    rw [rearrange,Int.mul_emod ((2:Int)^a*v) (2*half j),h,doubled_half,← Int.mul_emod,Int.one_mul]

theorem power_compatible (a : Nat) : Compatible (fun _ => (2:Int)^a) := by
  intro i j _
  rfl

theorem signed_half (j : Nat) : half j%modulus j = (-(j:Int))%modulus j := by
  have eq : half j = -(j:Int)+modulus j := by dsimp [half,modulus]; omega
  rw [eq,Int.add_emod_self]

theorem negative_unit (k : Family) (units : Units k) : Units (fun j => -(k j)) := by
  intro j
  obtain ⟨v,h⟩ := units j
  exact ⟨-v,by simpa [Int.neg_mul,Int.mul_neg] using h⟩

end ForceAliasRefinement
#print axioms ForceAliasRefinement.odd_cancel
#print axioms ForceAliasRefinement.two_scale_determination
#print axioms ForceAliasRefinement.bounded_identification
#print axioms ForceAliasRefinement.no_odd_divisor
#print axioms ForceAliasRefinement.bounded_unit_classification
#print axioms ForceAliasRefinement.doubled_half
#print axioms ForceAliasRefinement.half_unit
#print axioms ForceAliasRefinement.half_compatible
#print axioms ForceAliasRefinement.calibrated_unit_scale
#print axioms ForceAliasRefinement.extend_bounds_from_cofinal
#print axioms ForceAliasRefinement.calibrated_global
#print axioms ForceAliasRefinement.power_units
#print axioms ForceAliasRefinement.power_compatible
#print axioms ForceAliasRefinement.signed_half
#print axioms ForceAliasRefinement.negative_unit
