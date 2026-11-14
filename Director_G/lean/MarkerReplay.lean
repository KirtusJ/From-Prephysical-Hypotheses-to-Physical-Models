import Std

/-! Marker replay on the integer line. The mass at a given depth is stored
as an integer numerator with ONE common denominator, doubled at the next
depth. No empirical, continuity or stationary-phase assertion is used. -/
namespace MarkerReplay

abbrev Rails := Int × Int
abbrev Field := Int → Rails

def squares (s : Rails) : Rails := (s.1*s.1,s.2*s.2)

def flight (v : Field) (x : Int) : Rails :=
  ((v (x-1)).1 + (v (x-1)).2, (v (x+1)).1 - (v (x+1)).2)

theorem two_outputs (u v : Int) :
    (u+v)*(u+v)+(u-v)*(u-v) = 2*(u*u+v*v) := by
  simp only [Int.add_mul, Int.mul_add, Int.sub_mul, Int.mul_sub]
  omega

/-- Site-kernel hypothesis in cross-multiplied form. This fixes aggregate
marker masses at two successors. Marker routing may still depend on its
incoming rail in ways which give the same aggregate. -/
def localLaw (v m : Field) (out : Int → Rails) : Prop :=
  ∀ x, let (u,w) := v x
       let a := (m x).1+(m x).2
       let b := u*u+w*w
       (b = 0 → out x = (0,0)) ∧
       b*(out x).1 = a*((u+w)*(u+w)) ∧ b*(out x).2 = a*((u-w)*(u-w))

def stream (out : Int → Rails) (x : Int) : Rails := ((out (x-1)).1,(out (x+1)).2)

theorem replay_step (v m out : Field) (calibrated : ∀ x, m x = squares (v x))
    (law : localLaw v m out) : ∀ x, stream out x = squares (flight v x) := by
  have site (x : Int) : out x = squares ((v x).1+(v x).2,(v x).1-(v x).2) := by
    obtain ⟨dark,r,l⟩ := law x
    rw [calibrated x] at r l
    by_cases h : (v x).1*(v x).1+(v x).2*(v x).2 = 0
    · have sq (a : Int) : 0 ≤ a*a := by
        by_cases ha : 0 ≤ a
        · exact Int.mul_nonneg ha ha
        · exact Int.mul_nonneg_of_nonpos_of_nonpos (by omega) (by omega)
      have sqR := sq (v x).1
      have sqL := sq (v x).2
      have zR : (v x).1*(v x).1 = 0 := by omega
      have zL : (v x).2*(v x).2 = 0 := by omega
      have z (a : Int) (za : a*a = 0) : a = 0 := by
        exact (Int.mul_eq_zero.mp za).elim id id
      simp [dark h, squares, z _ zR, z _ zL]
    · apply Prod.ext
      · exact Int.eq_of_mul_eq_mul_left h r
      · exact Int.eq_of_mul_eq_mul_left h l
  intro x
  simp only [stream, flight, site, squares]

theorem replay (v m out : Nat → Field)
    (source : ∀ x, m 0 x = squares (v 0 x))
    (walk : ∀ t x, v (t+1) x = flight (v t) x)
    (route : ∀ t x, m (t+1) x = stream (out t) x)
    (law : ∀ t, localLaw (v t) (m t) (out t)) :
    ∀ t x, m t x = squares (v t x) := by
  intro t
  induction t with
  | zero => exact source
  | succ t ih =>
    intro x
    rw [route t x,walk t x]
    exact replay_step _ _ _ ih (law t) x

/-- f(c,b) gives an incoming numerator or tally at rail c and old tag b.
The R rail (false) preserves the tag; the L rail (true) toggles it. -/
def copy (f : Bool → Bool → Int) (c b : Bool) := f c (Bool.xor b c)

theorem copy_per_rail (f : Bool → Bool → Int) (c : Bool) :
    copy f c false + copy f c true = f c false + f c true := by
  cases c <;> simp [copy, Int.add_comm]

theorem copy_squares (v m : Bool → Bool → Int)
    (calibrated : ∀ c b, m c b = v c b * v c b) (c b : Bool) :
    copy m c b = copy v c b * copy v c b := calibrated _ _

/-- Starting with a blank bit creates separate tags for the two input
rails at the same site. Subsequent interfering contributions must be
grouped by the actual resulting tag. -/
theorem copy_blank (f : Bool → Bool → Int) (blank : ∀ c, f c true = 0)
    (c b : Bool) : copy f c b = if c = b then f c false else 0 := by
  cases c <;> cases b <;> simp [copy,blank]

/-- With a reused bit, distinct old rail/tag pairs can reach the same
new tag, even though the full rail/tag copy remains a permutation. -/
theorem copy_reused (f : Bool → Bool → Int) :
    copy f false false = f false false ∧ copy f true false = f true true := by
  exact ⟨rfl,rfl⟩

/-- A local direction copy before each chosen splitter. Each splitter
combines the two incoming rails that have the same tag AFTER the copy. -/
def atCopy (v : Bool → Field) (enabled : Int → Bool) (b : Bool) (x : Int) : Rails :=
  ((v b x).1, (v (Bool.xor b (enabled x)) x).2)

theorem tagged_replay (v m out : Nat → Bool → Field) (enabled : Nat → Int → Bool)
    (source : ∀ b x, m 0 b x = squares (v 0 b x))
    (walk : ∀ t b x, v (t+1) b x = flight (atCopy (v t) (enabled t) b) x)
    (route : ∀ t b x, m (t+1) b x = stream (out t b) x)
    (law : ∀ t b, localLaw (atCopy (v t) (enabled t) b)
      (atCopy (m t) (enabled t) b) (out t b)) :
    ∀ t b x, m t b x = squares (v t b x) := by
  intro t
  induction t with
  | zero => exact source
  | succ t ih =>
    intro b x
    rw [route t b x, walk t b x]
    apply replay_step _ _ _ _ (law t b) x
    intro y
    simp only [atCopy, ih, squares]

/- Two stored unit tallies whose depths differ by two represent amplitudes
in ratio 2:1 after alignment. Adding their unaligned numerators would give
a dark left output; adding the aligned values gives left numerator one. -/
example : squares ((1:Int)+1,1-1) = (4,0) ∧ squares ((2:Int)+1,2-1) = (9,1) := by
  decide

end MarkerReplay
