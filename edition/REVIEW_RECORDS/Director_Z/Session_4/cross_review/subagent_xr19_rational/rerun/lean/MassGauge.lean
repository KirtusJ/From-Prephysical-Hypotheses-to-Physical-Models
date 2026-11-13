import Std

/-!
# Removing a fixed sheet translation from repeated mass coins

Each term is a signed history on the real lifted carrier. Sheet coordinates
are residues; the physical order M is positive. H uses unnormalised signs:
both versions have the same two factors 1/√2 per mass tick.
-/
namespace MassGauge

structure Term where
  site : Int
  right : Bool
  sheet : Int
  weight : Int
  deriving DecidableEq

def shift (M q : Int) (p : Term) : Term := {p with sheet := (p.sheet+q)%M}
def rotate (M q : Int) (p : Term) : Term := shift M (if p.right then 0 else q) p

def stream (p : Term) : Term := {p with site := p.site + (if p.right then 1 else -1)}

theorem rotate_shift (M q g : Int) (p : Term) :
    rotate M q (shift M g p) = shift M g (rotate M q p) := by
  simp only [rotate,shift,Int.emod_add_emod]
  rw [Int.add_right_comm p.sheet]

theorem undo (M q : Int) (p : Term) :
    rotate M (-q) (rotate M q p) = shift M 0 p := by
  cases p with
  | mk x b y w =>
    cases b <;> simp [rotate,shift,Int.emod_add_emod,Int.add_assoc,show q + -q = 0 by omega]

theorem force_undo (M q g : Int) (p : Term) :
    rotate M (-q) (shift M g (rotate M q p)) = shift M g p := by
  rw [rotate_shift,undo]
  simp [shift,Int.emod_add_emod]

theorem stream_rotate (M q : Int) (p : Term) :
    stream (rotate M q p) = rotate M q (stream p) := rfl

/-- H, opposite sheet translations of stride j, H. For two signs H(b,d)
the only negative transition is L-to-L, here represented by false/false. -/
def hSign (b d : Bool) : Int := if b || d then 1 else -1

def mixed (M j : Int) (p : Term) : List Term :=
  [true,false].flatMap fun b =>
    [true,false].map fun d =>
      {p with right := d, sheet := (p.sheet + (if b then j else -j))%M,
              weight := p.weight * hSign p.right b * hSign b d}

structure Setting where
  stride : Int
  gain : Int → Int
  accept : Int → Bool → Bool

/-- A selected outcome may depend arbitrarily on the arrived site and rail. -/
def record (s : Setting) (ps : List Term) :=
  ps.filter fun p => s.accept p.site p.right

theorem record_rotate (s : Setting) (M q : Int) (ps : List Term) :
    record s (ps.map (rotate M q)) = (record s ps).map (rotate M q) := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    by_cases h : s.accept p.site p.right = true
    · simp [record,rotate,shift,h] at ih ⊢
      exact ih
    · simp [record,rotate,shift,h] at ih ⊢
      exact ih

def bareTick (M : Int) (s : Setting) (p : Term) : List Term :=
  record s ((mixed M s.stride (shift M (s.gain p.site) p)).map stream)

def dressedTick (M q : Int) (s : Setting) (p : Term) : List Term :=
  record s ((mixed M s.stride (rotate M (-q) (shift M (s.gain p.site) p))).map
    (fun v => stream (rotate M q v)))

theorem intertwine_tick (M q : Int) (s : Setting) (p : Term) :
    dressedTick M q s (rotate M q p) = (bareTick M s p).map (rotate M q) := by
  unfold dressedTick bareTick
  change record s ((mixed M s.stride (rotate M (-q)
    (shift M (s.gain p.site) (rotate M q p)))).map _) = _
  rw [force_undo, ← record_rotate, List.map_map]
  rfl

def run (tick : Setting → Term → List Term) : List Setting → List Term → List Term
  | [], ps => ps
  | s::ss, ps => run tick ss (ps.flatMap (tick s))

/-- The settings can follow any chosen transcript. Fixing the transcript
fixes its sequence of masks and subsequent adaptive settings. -/
theorem intertwine_schedule (M q : Int) (ss : List Setting) (ps : List Term) :
    run (dressedTick M q) ss (ps.map (rotate M q)) =
    (run (bareTick M) ss ps).map (rotate M q) := by
  induction ss generalizing ps with
  | nil => rfl
  | cons s ss ih =>
    simp only [run,List.flatMap_map,List.map_flatMap,Function.comp_def,intertwine_tick]
    rw [← List.map_flatMap,ih]

/-- Same *complete* physical output cell. Coinciding paths interfere. -/
def same (M : Int) (a b : Term) :=
  a.site=b.site ∧ a.right=b.right ∧ a.sheet%M=b.sheet%M

theorem same_rotate (M q : Int) (a b : Term) :
    same M (rotate M q a) (rotate M q b) ↔ same M a b := by
  cases a with
  | mk x d y w =>
    cases b with
    | mk z e v u =>
      cases d <;> cases e <;>
        simp [same,rotate,shift,Int.emod_emod,Int.emod_add_cancel_right]

/-- Ordered-pair expansion of the squared norm of all accepted bins:
Σ_c (Σ_{p in c} w_p)². This never treats tagged histories as an orthogonal basis. -/
def pair (M : Int) (a b : Term) : Int :=
  if a.site=b.site ∧ a.right=b.right ∧ a.sheet%M=b.sheet%M then a.weight*b.weight else 0

theorem pair_rotate (M q : Int) (a b : Term) :
    pair M (rotate M q a) (rotate M q b) = pair M a b := by
  by_cases h : same M a b
  · have k := (same_rotate M q a b).mpr h
    unfold same at h k
    unfold pair
    rw [if_pos k,if_pos h]
    rfl
  · have k := fun h' => h ((same_rotate M q a b).mp h')
    unfold same at h k
    simp only [pair,if_neg h,if_neg k]

def square (M : Int) (ps : List Term) : Int :=
  (ps.map (fun a => (ps.map (pair M a)).sum)).sum

theorem square_rotate (M q : Int) (ps : List Term) :
    square M (ps.map (rotate M q)) = square M ps := by
  simp only [square,List.map_map,Function.comp_def,pair_rotate]

theorem same_record (M q : Int) (ss : List Setting) (ps : List Term) :
    square M (run (dressedTick M q) ss (ps.map (rotate M q))) =
    square M (run (bareTick M) ss ps) := by
  rw [intertwine_schedule,square_rotate]

theorem launch_change (M q : Int) (p : Term) :
    rotate M q (rotate M (-2*q) p) = rotate M (-q) p := by
  cases p with
  | mk x b y w =>
    cases b <;> simp [rotate,shift,Int.emod_add_emod,
      show y + -2*q + q = y + -q by omega]

/-- If the physical source after its H split is D^{-1}v, the bare source
is D^{-2}v rather than v. Standalone equality of a full record sequence. -/
theorem original_launch (M q : Int) (ss : List Setting) (ps : List Term) :
    square M (run (dressedTick M q) ss (ps.map (rotate M (-q)))) =
    square M (run (bareTick M) ss (ps.map (rotate M (-2*q)))) := by
  have h := same_record M q ss (ps.map (rotate M (-2*q)))
  simpa only [List.map_map,Function.comp_def,launch_change] using h

/-- For an odd order index on a cycle of size 4q, the inverse half turn
has exponent 2q modulo 4q: the character sign is -1 on L. -/
theorem odd_half_turn (q k u : Int) (odd : k=2*u+1) :
    (k*(-2*q)) % (4*q) = (2*q) % (4*q) := by
  have factor : k*(-2*q) = 2*q + (-u-1)*(4*q) := by
    rw [odd,Int.add_mul,Int.one_mul,Int.sub_mul,Int.one_mul,Int.neg_mul,Int.mul_neg]
    have hu : u*(4*q)=4*(u*q) := by
      rw [← Int.mul_assoc, Int.mul_comm u 4, Int.mul_assoc]
    simp only [Int.mul_assoc,Int.neg_mul] at *
    rw [show u*(2*q) = 2*(u*q) by rw [← Int.mul_assoc,Int.mul_comm u 2,Int.mul_assoc],
        hu]
    omega
  rw [factor,Int.mul_comm (-u-1),Int.add_mul_emod_self_left]

theorem even_half_turn (q k u : Int) (even : k=2*u) :
    (k*(-2*q)) % (4*q) = 0 := by
  have factor : k*(-2*q) = (4*q)*(-u) := by
    rw [even,show -2*q = -(2*q) by omega,Int.mul_neg,Int.mul_neg,Int.mul_assoc]
    rw [show u*(2*q) = 2*(u*q) by rw [← Int.mul_assoc,Int.mul_comm u 2,Int.mul_assoc],
      Int.mul_assoc,Int.mul_comm q u]
    omega
  rw [factor,Int.mul_emod_right]

end MassGauge
