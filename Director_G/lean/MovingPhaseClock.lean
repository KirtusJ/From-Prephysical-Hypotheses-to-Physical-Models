import Std

/-!
# A nonstationary clock code on a strictly streaming doubled cycle

M is a positive logical cycle size in the intended physical interpretation.
Integer arguments represent residues; reads may depend on either the sheet or
an arbitrary auxiliary label. Signed lists collect interfering histories.
-/
namespace MovingPhaseClock

def encode (M t j : Int) := (2*j-t) % (2*M)
def decode (M t x : Int) := ((x+t) % (2*M)) / 2

theorem encoded_coordinate (M t j : Int) :
    (encode M t j + t) % (2*M) = 2*(j%M) := by
  simp only [encode,Int.emod_add_emod,Int.sub_add_cancel,Int.mul_emod_mul_of_pos j M (by decide : (0:Int)<2)]

theorem decode_encode (M t j : Int) : decode M t (encode M t j) = j%M := by
  rw [decode,encoded_coordinate]
  omega

theorem encode_congr (M t i j : Int) (h : i%M=j%M) : encode M t i=encode M t j := by
  apply (Int.emod_add_cancel_right (-t)).mpr
  simpa only [Int.mul_emod_mul_of_pos _ M (by decide : (0:Int)<2)] using congrArg (fun x => 2*x) h

theorem injective_modulo (M t i j : Int) : encode M t i=encode M t j ↔ i%M=j%M := by
  constructor
  · intro h
    simpa only [decode_encode] using congrArg (decode M t) h
  · exact encode_congr M t i j

def logicalDelta : Bool → Int | false => 0 | true => 1
def physicalDelta : Bool → Int | false => -1 | true => 1

theorem stream_edge (M t j : Int) (advance : Bool) :
    (encode M t j + physicalDelta advance) % (2*M) =
    encode M (t+1) ((j+logicalDelta advance)%M) := by
  have reduce := encode_congr M (t+1) ((j+logicalDelta advance)%M) (j+logicalDelta advance)
    (Int.emod_emod ..)
  rw [reduce]
  unfold encode
  rw [Int.emod_add_emod]
  congr 1
  cases advance <;> dsimp [logicalDelta,physicalDelta] <;> omega

structure Term (A : Type) where
  label : A
  site : Int
  amplitude : Int
  deriving DecidableEq

structure Edge (A : Type) where
  label : A
  advance : Bool
  coefficient : Int

/-- Arbitrary local choices, including integer coin signs, address-dependent
permutations, zero masks, fixed classical outcomes and auxiliary labels.
The source-site argument to each choice list is reduced to the logical cycle. -/
abbrev Layer (A : Type) := A → Int → List (Edge A)

def encodeTerm (M t : Int) (x : Term A) : Term A :=
  ⟨x.label,encode M t x.site,x.amplitude⟩

def logicalEdge (M : Int) (x : Term A) (e : Edge A) : Term A :=
  ⟨e.label,(x.site+logicalDelta e.advance)%M,x.amplitude*e.coefficient⟩

def physicalEdge (M : Int) (x : Term A) (e : Edge A) : Term A :=
  ⟨e.label,(x.site+physicalDelta e.advance)%(2*M),x.amplitude*e.coefficient⟩

theorem corresponding_edge (M t : Int) (x : Term A) (e : Edge A) :
    physicalEdge M (encodeTerm M t x) e = encodeTerm M (t+1) (logicalEdge M x e) := by
  simp [physicalEdge,logicalEdge,encodeTerm,stream_edge]

def logicalStep (M : Int) (layer : Layer A) (xs : List (Term A)) :=
  xs.flatMap fun x => (layer x.label (x.site%M)).map (logicalEdge M x)

def physicalStep (M t : Int) (layer : Layer A) (xs : List (Term A)) :=
  xs.flatMap fun x => (layer x.label (decode M t x.site)).map (physicalEdge M x)

theorem corresponding_step (M t : Int) (layer : Layer A) (xs : List (Term A)) :
    physicalStep M t layer (xs.map (encodeTerm M t)) =
    (logicalStep M layer xs).map (encodeTerm M (t+1)) := by
  have choices (x : Term A) :
      layer (encodeTerm M t x).label (decode M t (encodeTerm M t x).site) =
      layer x.label (x.site%M) := by simp [encodeTerm,decode_encode]
  have edge (x : Term A) : physicalEdge M (encodeTerm M t x) =
      fun e => encodeTerm M (t+1) (logicalEdge M x e) := by
    funext e
    exact corresponding_edge M t x e
  simp only [physicalStep,logicalStep,List.flatMap_map,List.map_flatMap,List.map_map,
    Function.comp_def,choices,edge]

def logicalRun (M : Int) : List (Layer A) → List (Term A) → List (Term A)
  | [], xs => xs
  | f::fs, xs => logicalRun M fs (logicalStep M f xs)

def physicalRun (M : Int) (t : Int) : List (Layer A) → List (Term A) → List (Term A)
  | [], xs => xs
  | f::fs, xs => physicalRun M (t+1) fs (physicalStep M t f xs)

theorem finite_schedule (M t : Int) (fs : List (Layer A)) (xs : List (Term A)) :
    physicalRun M t fs (xs.map (encodeTerm M t)) =
      (logicalRun M fs xs).map (encodeTerm M (t+(fs.length:Int))) := by
  induction fs generalizing t xs with
  | nil => simp [logicalRun,physicalRun]
  | cons f fs ih =>
    simp only [logicalRun,physicalRun,corresponding_step,ih,List.length_cons,Int.natCast_succ]
    rw [show t+1+(fs.length:Int) = t+((fs.length:Int)+1) by omega]

def logicalRead [DecidableEq A] (M : Int) (a : A) (j : Int) (xs : List (Term A)) : Int :=
  (xs.map fun x => if x.label=a ∧ x.site%M=j%M then x.amplitude else 0).sum

def physicalRead [DecidableEq A] (a : A) (x : Int) (xs : List (Term A)) : Int :=
  (xs.map fun w => if w.label=a ∧ w.site=x then w.amplitude else 0).sum

theorem corresponding_read [DecidableEq A] (M t : Int) (a : A) (j : Int) (xs : List (Term A)) :
    physicalRead a (encode M t j) (xs.map (encodeTerm M t)) = logicalRead M a j xs := by
  simp only [physicalRead,logicalRead,List.map_map,Function.comp_def,encodeTerm,injective_modulo]

/-- Finite-history coherence is preserved before squaring. The equality of
any sum of like normalized terminal records follows by summing these cells. -/
theorem finite_schedule_record [DecidableEq A] (M t : Int) (fs : List (Layer A))
    (xs : List (Term A)) (a : A) (j : Int) :
    physicalRead a (encode M (t+(fs.length:Int)) j)
        (physicalRun M t fs (xs.map (encodeTerm M t))) =
      logicalRead M a j (logicalRun M fs xs) := by
  rw [finite_schedule,corresponding_read]

theorem outside_image_dark [DecidableEq A] (M t : Int) (a : A) (x : Int)
    (missing : ∀ j, encode M t j ≠ x) (xs : List (Term A)) :
    physicalRead a x (xs.map (encodeTerm M t)) = 0 := by
  induction xs with
  | nil => rfl
  | cons p ps ih => simpa [physicalRead,encodeTerm,missing] using ih

/-- Fourier exponents in turns of 1/(2M), using the positive character
convention. Conjugating the Fourier convention reverses the common phase. -/
def exponent (M k x : Int) := (k*x)%(2*M)

theorem phase_on_code (M t k j : Int) :
    exponent M k (encode M t j) = (2*(k*j)-k*t)%(2*M) := by
  unfold exponent encode
  rw [Int.mul_emod k ((2*j-t)%(2*M)) (2*M),Int.emod_emod,← Int.mul_emod]
  simp only [Int.mul_sub,← Int.mul_assoc k 2 j,Int.mul_comm k 2,Int.mul_assoc]

theorem alias_exponent (M t k j : Int) :
    exponent M (k+M) (encode M t j) =
      (exponent M k (encode M t j) - M*t)%(2*M) := by
  rw [phase_on_code,phase_on_code,Int.emod_sub_emod]
  have expr : 2*((k+M)*j)-(k+M)*t =
      (2*(k*j)-k*t-M*t) + j*(2*M) := by
    simp only [Int.add_mul,Int.mul_add,Int.mul_assoc,Int.mul_comm,Int.mul_left_comm]
    omega
  rw [expr,Int.add_mul_emod_self]

/-- Fixed forward-frame alternate two-hop wiring: on the first tick both
arms move +1. On the second the hold arm goes −1, the advancing arm goes +1.
No tick has zero physical displacement; both arms return to even sites. -/
theorem static_two_hop (M j : Int) (advance : Bool) :
    (((encode M 0 j + 1)%(2*M)) + physicalDelta advance)%(2*M) =
      encode M 0 ((j+logicalDelta advance)%M) := by
  rw [Int.emod_add_emod]
  have h := encode_congr M 0 ((j+logicalDelta advance)%M) (j+logicalDelta advance)
    (Int.emod_emod ..)
  rw [h]
  unfold encode
  simp only [Int.sub_zero]
  rw [Int.add_assoc,Int.emod_add_emod]
  congr 1
  cases advance <;> dsimp [physicalDelta,logicalDelta] <;> omega

/-- One-site physical translation, read back onto the occupied parity after
two ticks, is exactly one logical unit translation. -/
theorem two_translations (M t j : Int) :
    (encode M t j + 2)%(2*M) = encode M t (j+1) := by
  unfold encode
  rw [Int.emod_add_emod]
  congr 1
  omega

/-- The frozen code occupies the physical parity −t; this condition is
sufficient as well as necessary, including when a coordinate wraps. -/
theorem image_parity (M t x : Int) (hx : 0≤x) (hx' : x<2*M) :
    (∃ j, encode M t j = x) ↔ (x+t)%2=0 := by
  constructor
  · rintro ⟨j,rfl⟩
    have eq := congrArg (fun n : Int => n%2) (encoded_coordinate M t j)
    have dvd : (2:Int) ∣ 2*M := ⟨M,rfl⟩
    dsimp only at eq
    rw [Int.emod_emod_of_dvd _ dvd] at eq
    simpa using eq
  · intro even
    refine ⟨(x+t)/2,?_⟩
    unfold encode
    have back : 2*((x+t)/2)-t=x := by omega
    rw [back,Int.emod_eq_of_lt hx hx']

/-! ## Equal-time gain of a uniform departure field on the line -/

abbrev rightCount (w : List Bool) : Int := (w.count true : Nat)
abbrev leftCount (w : List Bool) : Int := (w.count false : Nat)

private def delta : Bool → Int | true => 1 | false => -1

/-- Actual integer sheet gain of g(x)=x accumulated on departure. -/
def gain (x : Int) : List Bool → Int
  | [] => 0
  | b::bs => x + gain (x+delta b) bs

/-- Count left-before-right pairs, each with a distinct pair of tick indices. -/
def inversions : List Bool → Int
  | [] => 0
  | true::w => inversions w
  | false::w => rightCount w + inversions w

private theorem count_length (w : List Bool) :
    (w.length : Int) = rightCount w + leftCount w := by
  induction w with
  | nil => rfl
  | cons b w ih =>
    cases b <;> simp [rightCount,leftCount,List.count_cons] at * <;> omega

private theorem gain_translates (w : List Bool) (x off : Int) :
    gain (x+off) w = gain x w + (w.length:Int)*off := by
  induction w generalizing x with
  | nil => simp [gain]
  | cons b w ih =>
    simp only [gain,List.length_cons,Int.natCast_succ,Int.add_mul,Int.one_mul]
    rw [show x+off+delta b=x+delta b+off by omega,ih]
    omega

private theorem triangular_formula (w : List Bool) :
    let r := rightCount w
    let l := leftCount w
    2*gain 0 w = r*(r-1)-l*(l-1)+2*(r*l)-4*inversions w := by
  induction w with
  | nil => rfl
  | cons b w ih =>
    have shift := gain_translates w 0 (delta b)
    have len := count_length w
    cases b <;>
      simp [gain,delta,inversions,rightCount,leftCount,List.count_cons,Int.add_mul,Int.mul_add,
        Int.sub_mul,Int.mul_sub,Int.mul_comm] at shift ih len ⊢ <;> omega

private theorem inversions_bounds (w : List Bool) :
    0 ≤ inversions w ∧ inversions w ≤ rightCount w * leftCount w := by
  induction w with
  | nil => exact ⟨by decide,by decide⟩
  | cons b w ih =>
    have rpos : 0 ≤ rightCount w := by unfold rightCount; omega
    have lpos : 0 ≤ leftCount w := by unfold leftCount; omega
    cases b <;> simp [inversions,rightCount,leftCount,List.count_cons,Int.add_mul,Int.mul_add] at * <;> omega

theorem balanced_area (w : List Bool) (a : Int) (hr : rightCount w=a) (hl : leftCount w=a) :
    gain 0 w = a*a-2*inversions w ∧ -(a*a) ≤ gain 0 w ∧ gain 0 w ≤ a*a := by
  have exactGain := triangular_formula w
  have bounds := inversions_bounds w
  simp only [hr,hl] at exactGain bounds
  omega

private theorem end_of_path (x : Int) (w : List Bool) :
    gain x (w ++ [true]) = gain x w + (x+rightCount w-leftCount w) := by
  induction w generalizing x with
  | nil => simp [gain,rightCount,leftCount]
  | cons b w ih =>
    cases b <;> simp [gain,ih,rightCount,leftCount,List.count_cons,delta] <;> omega

private theorem block_inversions (a b : Nat) :
    inversions (List.replicate a true ++ List.replicate b false) = 0 ∧
    inversions (List.replicate a false ++ List.replicate b true) = (a:Int)*b := by
  have allRight (n : Nat) : inversions (List.replicate n true)=0 := by
    induction n with | zero => rfl | succ n ih => simpa [List.replicate_succ,inversions] using ih
  have allLeft (n : Nat) : inversions (List.replicate n false)=0 := by
    induction n with
    | zero => rfl
    | succ n ih => simp [List.replicate_succ,inversions,rightCount,List.count_replicate,ih]
  induction a with
  | zero => simp [allLeft,allRight]
  | succ a ih =>
    simp [List.replicate_succ,inversions,ih.1,ih.2,rightCount,List.count_replicate,Int.add_mul,Int.add_comm]

/-- Both full words have last rail R. Before that tick their balanced
prefixes return to zero and realize both endpoints of the gain interval. -/
theorem extremal_closed_excursions (a : Nat) :
    gain 0 ((List.replicate a true ++ List.replicate a false) ++ [true]) = (a:Int)*a ∧
    gain 0 ((List.replicate a false ++ List.replicate a true) ++ [true]) = -((a:Int)*a) := by
  have h₁ := balanced_area (List.replicate a true ++ List.replicate a false) a
    (by simp [rightCount,List.count_replicate]) (by simp [leftCount,List.count_replicate])
  have h₂ := balanced_area (List.replicate a false ++ List.replicate a true) a
    (by simp [rightCount,List.count_replicate]) (by simp [leftCount,List.count_replicate])
  rw [(block_inversions a a).1] at h₁
  rw [(block_inversions a a).2] at h₂
  simp only [end_of_path,rightCount,leftCount,List.count_append,List.count_replicate]
  simp at *
  omega

theorem all_equal_time_records (w z : List Bool) (a : Int)
    (r₁ : rightCount w=a) (l₁ : leftCount w=a)
    (r₂ : rightCount z=a) (l₂ : leftCount z=a) :
    gain 0 (w++[true]) - gain 0 (z++[true]) ≤ 2*(a*a) := by
  have fw := balanced_area w a r₁ l₁
  have fz := balanced_area z a r₂ l₂
  rw [end_of_path,end_of_path,r₁,l₁,r₂,l₂]
  omega

structure Vertex where
  t : Int
  x : Int
  rail : Bool

private def next (p : Vertex) (edge : Bool) : Vertex := ⟨p.t+1,p.x+delta edge,edge⟩

def finish (p : Vertex) : List Bool → Vertex
  | [] => p
  | e::w => finish (next p e) w

def correctedGain (gauge : Vertex → Int) (p : Vertex) : List Bool → Int
  | [] => 0
  | e::w => p.x + gauge (next p e) - gauge p + correctedGain gauge (next p e) w

theorem telescopes (gauge : Vertex → Int) (p : Vertex) (w : List Bool) :
    correctedGain gauge p w = gain p.x w + gauge (finish p w) - gauge p := by
  induction w generalizing p with
  | nil => simp [gain,correctedGain,finish]
  | cons e w ih => simp [gain,correctedGain,finish,ih,next] <;> omega

theorem matched_end_gauges (gauge : Vertex → Int) (p : Vertex) (w z : List Bool)
    (same : finish p w=finish p z) :
    correctedGain gauge p w-correctedGain gauge p z = gain p.x w - gain p.x z := by
  rw [telescopes,telescopes,same]
  omega

/-- For a cyclic pair separation d no greater than half the circumference,
the representatives cannot be closer than d in the universal cover. -/
theorem bounded_lifts (M d u v B : Int) (half : 2*d≤M)
    (matchResidue : (u-v)%M=d%M) (hi : u≤B) (lo : -B≤v) (hi' : v≤B) (lo' : -B≤u) :
    d≤2*B := by
  apply Classical.byContradiction
  intro hn
  have left : 0<(u-v-d)+M := by omega
  have right : (u-v-d)+M<M := by omega
  have eq := Int.emod_eq_emod_iff_emod_sub_eq_zero.mp matchResidue
  have zero : ((u-v-d)+M)%M=0 := by simpa only [Int.add_emod_self] using eq
  rw [Int.emod_eq_of_lt (by omega) right] at zero
  omega

private theorem finish_append (p : Vertex) (w z : List Bool) :
    finish p (w++z) = finish (finish p w) z := by
  induction w generalizing p with
  | nil => rfl
  | cons e w ih => simpa only [List.cons_append,finish] using ih (next p e)

private theorem finish_coordinates (p : Vertex) (w : List Bool) :
    (finish p w).t=p.t+w.length ∧ (finish p w).x=p.x+rightCount w-leftCount w := by
  induction w generalizing p with
  | nil => simp [finish,rightCount,leftCount]
  | cons e w ih =>
    have h := ih (next p e)
    cases e <;> simp [next,delta,finish,rightCount,leftCount,List.count_cons] at h ⊢ <;> omega

private theorem same_full_endpoint (p : Vertex) (w z : List Bool) (a : Int)
    (rw₁ : rightCount w=a) (lw₁ : leftCount w=a)
    (rz₁ : rightCount z=a) (lz₁ : leftCount z=a) :
    finish p (w++[true])=finish p (z++[true]) := by
  have wp := finish_coordinates p w
  have zp := finish_coordinates p z
  have wl := count_length w
  have zl := count_length z
  simp only [rw₁,lw₁,rz₁,lz₁] at wp zp wl zl
  simp only [finish_append,finish,next]
  congr 1 <;> omega

def edgeSum (shift : Vertex → Bool → Int) (p : Vertex) : List Bool → Int
  | [] => 0
  | e::w => shift p e + edgeSum shift (next p e) w

private theorem edgeSum_budget (shift : Vertex → Bool → Int) (v : Int)
    (edgeBounds : ∀ p e, -(v)≤shift p e ∧ shift p e≤v) (p : Vertex) (w : List Bool) :
    -((w.length:Int)*v) ≤ edgeSum shift p w ∧ edgeSum shift p w ≤ (w.length:Int)*v := by
  induction w generalizing p with
  | nil => simp [edgeSum]
  | cons e w ih =>
    have edge := edgeBounds p e
    have tail := ih (next p e)
    simp only [edgeSum,List.length_cons,Int.natCast_succ,Int.add_mul,Int.one_mul]
    omega

private theorem edgeSum_congruence (M : Int) (shift : Vertex → Bool → Int) (gauge : Vertex → Int)
    (calibrated : ∀ p e, (shift p e)%M=(p.x+gauge (next p e)-gauge p)%M)
    (p : Vertex) (w : List Bool) :
    (edgeSum shift p w)%M = (correctedGain gauge p w)%M := by
  induction w generalizing p with
  | nil => rfl
  | cons e w ih =>
    rw [edgeSum,correctedGain,Int.add_emod,calibrated,ih,← Int.add_emod]

/-- Pointwise integer calibration errors may correlate arbitrarily. The edge
condition applies to every transition; no averaging or random error model
enters. With errorBound = 0 it gives the exact microscopic speed bound. -/
theorem local_holonomy_cost (a : Nat) (M v errorBound : Int) (startRail : Bool)
    (large : 4*((a:Int)*a) ≤ M)
    (shift err : Vertex → Bool → Int) (gauge : Vertex → Int)
    (speed : ∀ p e, -v ≤ shift p e ∧ shift p e ≤ v)
    (accuracy : ∀ p e, -errorBound ≤ err p e ∧ err p e ≤ errorBound)
    (calibrated : ∀ p e, (shift p e - err p e)%M =
                              (p.x+gauge (next p e)-gauge p)%M) :
    (a:Int)*a ≤ (2*(a:Int)+1)*(v+errorBound) := by
  let p : Vertex := ⟨0,0,startRail⟩
  let w := List.replicate a true ++ List.replicate a false
  let z := List.replicate a false ++ List.replicate a true
  let net := fun p e => shift p e - err p e
  have bound (s : Vertex) (e : Bool) : -(v+errorBound) ≤ net s e ∧ net s e ≤ v+errorBound := by
    have y := speed s e
    have h := accuracy s e
    dsimp [net]
    omega
  have same := same_full_endpoint p w z (a:Int)
    (by simp [w,rightCount,List.count_replicate]) (by simp [w,leftCount,List.count_replicate])
    (by simp [z,rightCount,List.count_replicate]) (by simp [z,leftCount,List.count_replicate])
  have differences : correctedGain gauge p (w++[true])-correctedGain gauge p (z++[true])=2*((a:Int)*a) := by
    rw [matched_end_gauges gauge p _ _ same]
    have h := extremal_closed_excursions a
    change gain 0 ((List.replicate a true ++ List.replicate a false) ++ [true]) -
              gain 0 ((List.replicate a false ++ List.replicate a true) ++ [true])=_
    omega
  have eq : (edgeSum net p (w++[true])-edgeSum net p (z++[true]))%M = (2*((a:Int)*a))%M := by
    rw [Int.sub_emod,edgeSum_congruence M net gauge calibrated,edgeSum_congruence M net gauge calibrated,
      ← Int.sub_emod,differences]
  have wb := edgeSum_budget net (v+errorBound) bound p (w++[true])
  have zb := edgeSum_budget net (v+errorBound) bound p (z++[true])
  have wl : ((w++[true]).length:Int)=2*(a:Int)+1 := by simp [w]; omega
  have zl : ((z++[true]).length:Int)=2*(a:Int)+1 := by simp [z]; omega
  rw [wl] at wb
  rw [zl] at zb
  have lim := bounded_lifts M _ _ _ _ (by omega) eq wb.2 zb.1 zb.2 wb.1
  omega

end MovingPhaseClock
