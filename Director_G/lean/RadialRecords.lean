import Std

/-!
# All outcomes of a mirrored radius measurement on a 2L-site ring

At an interior radius the old direction on the negative arm is the opposite
of the old direction on the positive arm. A pure radius record therefore admits
one microscopic edge per arm. At an endpoint the position residues coincide
and the output coins are opposite. The phase and sign fields below are carried
through the *actual* physical edges; the radius mask reads neither one.
-/
namespace RadialRecords

structure Entry where
  site : Int
  left : Bool
  sheet : Int
  negative : Bool
  deriving DecidableEq

private def period (L : Nat) : Int := 2*(L:Int)

def positions (L : Nat) (r : Int) : Int × Int :=
  (r % period L, (-r) % period L)

def edge (L : Nat) (g : Int → Int) (old : Entry) (left : Bool) : Entry :=
  ⟨(old.site+(if left then -1 else 1)) % period L, left,
   old.sheet+g old.site,xor old.negative (old.left && left)⟩

def mask (L : Nat) (r : Int) (out : Entry) : Bool :=
  out.site == (positions L r).1 || out.site == (positions L r).2

def branch (L : Nat) (g : Int → Int) (r : Int) (pair : List Entry) :=
  pair.flatMap fun c => [edge L g c false,edge L g c true].filter (mask L r)

private theorem distinctResidues {L : Nat} {a b : Int}
    (lo : 0 < a-b) (hi : a-b < period L) : a%period L ≠ b%period L := by
  intro eq
  have h := Int.sub_emod a b (period L)
  rw [eq,Int.sub_self,Int.zero_emod, Int.emod_eq_of_lt (by omega) hi] at h
  omega

private theorem distinct_shells (L : Nat) (r : Int) (_size : 4 ≤ L)
    (lo : 1 ≤ r) (hi : r < (L:Int)) :
    (positions L (r+1)).1 ≠ (positions L (r-1)).1 ∧
    (positions L (r+1)).1 ≠ (positions L (r-1)).2 ∧
    (positions L (r+1)).2 ≠ (positions L (r-1)).1 ∧
    (positions L (r+1)).2 ≠ (positions L (r-1)).2 := by
  unfold positions
  dsimp
  refine ⟨distinctResidues ?_ ?_,distinctResidues ?_ ?_,
          Ne.symm (distinctResidues ?_ ?_),Ne.symm (distinctResidues ?_ ?_)⟩ <;>
    (try unfold period) <;> omega

def positiveArm (L : Nat) (r : Int) (inward : Bool) (sheet : Int) (sign : Bool) : Entry :=
  ⟨(positions L r).1,inward,sheet,sign⟩

def negativeArm (L : Nat) (r : Int) (inward : Bool) (sheet : Int) (sign : Bool) : Entry :=
  ⟨(positions L r).2,!inward,sheet,sign⟩

/- The two signed output entries are defined before evaluation in any sheet
character. The previous radial increment determines the signs on both arms. -/
private theorem four_edges (L : Nat) (g : Int → Int) (r : Int) (i : Bool)
    (a b : Int) (s u : Bool) :
    let p := positiveArm L r i a s
    let m := negativeArm L r i b u
    (edge L g p false).site = (positions L (r+1)).1 ∧
    (edge L g p true).site = (positions L (r-1)).1 ∧
    (edge L g m false).site = (positions L (r-1)).2 ∧
    (edge L g m true).site = (positions L (r+1)).2 := by
  have x : -r+1 = -(r-1) := by omega
  have y : -r+(-1) = -(r+1) := by omega
  simp [positiveArm,negativeArm,edge,positions,Int.emod_add_emod,x,y,Int.sub_eq_add_neg]

/-- Both possible radius results are accounted for, including r=1 or r=L-1.
Each result carries the two old amplitudes to opposite output directions with
the explicit signed-Hadamard edges returned here. -/
theorem both_branches (L : Nat) (g : Int → Int) (r : Int) (size : 4 ≤ L)
    (lo : 1 ≤ r) (hi : r < (L:Int)) (i : Bool) (a b : Int) (s u : Bool) :
    let p := positiveArm L r i a s
    let m := negativeArm L r i b u
    branch L g (r+1) [p,m] = [edge L g p false, edge L g m true] ∧
    branch L g (r-1) [p,m] = [edge L g p true, edge L g m false] := by
  obtain ⟨pr,pl,mr,ml⟩ := four_edges L g r i a b s u
  obtain ⟨aa,ab,ba,bb⟩ := distinct_shells L r size lo hi
  dsimp only
  simp [branch,mask,pr,pl,mr,ml,aa,ab,ba,bb,Ne.symm aa,Ne.symm ab,Ne.symm ba,Ne.symm bb]

/-- At a boundary, reading only the position leaves two distinct coin rows to
decode. They share the site at both possible endpoints. -/
theorem boundary_sites (L : Nat) :
    (positions L 0).1 = (positions L 0).2 ∧
    (positions L L).1 = (positions L L).2 := by
  have same : -(L:Int)+period L = L := by unfold period;omega
  have h : (-(L:Int)+period L)%period L = (-(L:Int))%period L := Int.add_emod_self
  rw [same] at h
  exact ⟨by simp [positions],h⟩

/- Each retained microscopic edge has equal magnitude and gains only a phase
and a sign in a character sector. The unnormalized squared norm for each
branch equals the input norm. On dividing by two for the current normalized
Hadamard step, *each* accessible result therefore has probability one half. -/
structure Isometries (V S : Type) [Add S] where
  normSq : V → S
  phase : Int → V → V
  sign : Bool → V → V
  phase_preserves : ∀ z v, normSq (phase z v) = normSq v
  sign_preserves : ∀ z v, normSq (sign z v) = normSq v

def evaluateEdge [Add S] (law : Isometries V S) (g : Int → Int)
    (c : Entry) (left : Bool) (v : V) : V :=
  law.sign (c.left && left) (law.phase (g c.site) v)

theorem fair_branch [Add S] (law : Isometries V S) (g : Int → Int)
    (p m : Entry) (inward : Bool) (v w : V) :
    law.normSq (evaluateEdge law g p inward v) +
    law.normSq (evaluateEdge law g m (!inward) w) = law.normSq v + law.normSq w := by
  simp [evaluateEdge,law.phase_preserves,law.sign_preserves]

/- Characterization of the absorption probability and duration of the fair
radius chain. Quantities are integer-scaled; no division is required. For
probabilities multiply by L before specializing the boundary condition.
Uniqueness uses just the two boundary values and the first-step equations. -/
private theorem harmonic_line (L : Nat) (q : Nat → Int) (start : q 0 = 0)
    (rec : ∀ j, j+2 ≤ L → q (j+2)+q j = 2*q (j+1)) :
    ∀ j, j ≤ L → q j = (j:Int)*q 1 := by
  have pair (n : Nat) (bound : n+1 ≤ L) :
      q n = (n:Int)*q 1 ∧ q (n+1) = ((n:Int)+1)*q 1 := by
    induction n with
    | zero => simp [start]
    | succ n ih =>
      obtain ⟨a,b⟩ := ih (by omega)
      have eqn := rec n bound
      simp only [Int.natCast_succ]
      refine ⟨b,?_⟩
      change q (n+2) = (((n:Int)+1)+1)*q 1
      rw [b,a] at eqn
      simp only [Int.add_mul, Int.one_mul] at eqn ⊢
      omega
  intro j bound
  cases j with
  | zero => simp [start]
  | succ j => simpa only [Int.natCast_succ] using (pair j bound).2

private theorem harmonic_zero (L : Nat) (q : Nat → Int) (size : 4 ≤ L)
    (zero : q 0=0) (endZero : q L=0)
    (rec : ∀ j, j+2 ≤ L → q (j+2)+q j=2*q (j+1)) :
    ∀ j, j ≤ L → q j=0 := by
  have line := harmonic_line L q zero rec
  have e := line L (Nat.le_refl L)
  rw [endZero] at e
  have atOne := (Int.mul_eq_zero.mp e.symm).resolve_left (by omega)
  intro j bound
  simp [line j bound,atOne]

/-- The unique integer L-scaled hitting-probability table is j. -/
theorem scaled_hit_table (L : Nat) (q : Nat → Int) (size : 4 ≤ L)
    (start : q 0=0) (finish : q L=L)
    (rec : ∀ j, j+2 ≤ L → q (j+2)+q j=2*q (j+1)) :
    ∀ j, j ≤ L → q j=(j:Int) := by
  have hz := harmonic_zero L (fun j => q j-(j:Int)) size
    (by simp [start]) (by simp [finish]) (by
      intro j h
      have := rec j h
      change (q (j+2)-((j+2:Nat):Int))+(q j-(j:Int))=2*(q (j+1)-((j+1:Nat):Int))
      simp only [Int.natCast_add,Int.natCast_one]
      omega)
  intro j h
  have a := hz j h
  change q j - (j:Int) = 0 at a
  omega

def duration (L j : Nat) : Int := (j:Int)*((L:Int)-(j:Int))

private theorem duration_step (L j : Nat) :
    duration L (j+2)+duration L j+2 = 2*duration L (j+1) := by
  simp only [duration,Int.natCast_add,Int.natCast_one,
             Int.mul_sub,Int.add_mul,Int.mul_add,Int.one_mul,Int.mul_one]
  omega

/-- The unique integer mean-time table is j(L-j). The duration starts counting
after the first Hadamard split. Starting at radius one gives L-1 further ticks. -/
theorem mean_duration (L : Nat) (q : Nat → Int) (size : 4 ≤ L)
    (start : q 0=0) (finish : q L=0)
    (rec : ∀ j, j+2 ≤ L → q (j+2)+q j+2=2*q (j+1)) :
    ∀ j, j ≤ L → q j=duration L j := by
  have hz := harmonic_zero L (fun j => q j-duration L j) size
    (by simp [duration,start]) (by simp [duration,finish]) (by
      intro j h
      have := rec j h
      have := duration_step L j
      change (q (j+2)-duration L (j+2))+(q j-duration L j)=2*(q (j+1)-duration L (j+1))
      omega)
  intro j h
  have a := hz j h
  change q j - duration L j = 0 at a
  omega

/- The following homogeneous (cross-multiplied) form allows arbitrary common
denominators. It does not presuppose that the probability multiplied by L
is an integer. -/
theorem rational_hit_uniqueness (L : Nat) (mass : Int) (q : Nat → Int) (_size : 4 ≤ L)
    (start : q 0=0) (finish : q L=mass)
    (rec : ∀ j, j+2 ≤ L → q (j+2)+q j=2*q (j+1)) :
    ∀ j, j ≤ L → (L:Int)*q j=(j:Int)*mass := by
  have line := harmonic_line L q start rec
  have endpoint := line L (Nat.le_refl L)
  rw [finish] at endpoint
  intro j h
  rw [line j h,endpoint,← Int.mul_assoc,Int.mul_comm (L:Int) (j:Int),Int.mul_assoc]

theorem rational_duration_uniqueness (L : Nat) (unit : Int) (q : Nat → Int) (size : 4 ≤ L)
    (start : q 0=0) (finish : q L=0)
    (rec : ∀ j, j+2 ≤ L → q (j+2)+q j+2*unit=2*q (j+1)) :
    ∀ j, j ≤ L → q j=duration L j*unit := by
  have hz := harmonic_zero L (fun j => q j-duration L j*unit) size
    (by simp [duration,start]) (by simp [duration,finish]) (by
      intro j h
      have e := rec j h
      have d := congrArg (fun x : Int => x*unit) (duration_step L j)
      change (duration L (j+2)+duration L j+2)*unit = (2*duration L (j+1))*unit at d
      rw [Int.add_mul, Int.add_mul, Int.mul_assoc] at d
      change (q (j+2)-duration L (j+2)*unit)+(q j-duration L j*unit)=
              2*(q (j+1)-duration L (j+1)*unit)
      omega)
  intro j h
  have a := hz j h
  change q j - duration L j*unit = 0 at a
  omega

end RadialRecords
