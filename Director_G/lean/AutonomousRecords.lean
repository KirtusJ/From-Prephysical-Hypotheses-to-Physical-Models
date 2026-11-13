import Std

/-!
# Calibrating an earlier record in one tagged experiment

The fanout and the final read have different weight tables. At each read,
equal signed entries of that snapshot have equal coordinate masses. Between
reads only the listed protected marginals are equated. Mass arithmetic is
homogeneous and works for real masses with ordinary addition.
-/
namespace AutonomousRecords

structure Additive (R : Type u) [Add R] [OfNat R 0] : Prop where
  assoc : ∀ a b c : R, (a+b)+c = a+(b+c)
  zero_add : ∀ a : R, 0+a=a
  add_zero : ∀ a : R, a+0=a
  cancel_right : ∀ a b c : R, a+c=b+c → a=b

variable {R : Type u} [Add R] [OfNat R 0]

def times (p : R) : Nat → R
  | 0 => 0
  | k+1 => times p k+p

def total (f : I → R) : List I → R
  | [] => 0
  | i::xs => f i+total f xs

private theorem times_add (A : Additive R) (x : R) (k j : Nat) :
    times x (k+j)=times x k+times x j := by
  induction j with
  | zero => simp [times, A.add_zero]
  | succ j ih => change times x (k+j)+x=times x k+(times x j+x)
                 rw [ih,A.assoc]

private theorem times_times (A : Additive R) (x : R) (k j : Nat) :
    times (times x k) j=times x (j*k) := by
  induction j with
  | zero => simp [times]
  | succ j ih => simp [times, ih, Nat.succ_mul, times_add A]

private theorem total_append (A : Additive R) (f : I → R) (xs ys : List I) :
    total f (xs++ys)=total f xs+total f ys := by
  induction xs with
  | nil => simp [total,A.zero_add]
  | cons x xs ih => simp [total,ih,A.assoc]

private theorem total_congr (xs : List I) {f g : I → R}
    (h : ∀ i ∈ xs, f i=g i) : total f xs=total g xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    change f x+total f xs=g x+total g xs
    rw [h x (by simp),ih (fun i hi => h i (by simp [hi]))]

private theorem total_map (f : J → R) (q : I → J) (xs : List I) :
    total f (xs.map q)=total (fun i => f (q i)) xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [total,ih]

private theorem total_constant (A : Additive R) (xs : List I) (p : R) :
    total (fun _ => p) xs=times p xs.length := by
  induction xs with
  | nil => rfl
  | cons i xs ih =>
    change p+total (fun _ => p) xs=times p (xs.length+1)
    rw [ih,Nat.add_comm xs.length 1,times_add A]
    simp [times,A.zero_add]

private theorem total_repeat (A : Additive R) (f : I → R) (x : I) (k : Nat) :
    total f (List.replicate k x)=times (f x) k := by
  have h : total f (List.replicate k x) =
      total (fun _ => f x) (List.replicate k x) := by
    apply total_congr
    intro i hi
    rw [(List.mem_replicate.mp hi).2]
  simpa [total_constant A] using h

private theorem times_zero (A : Additive R) (k : Nat) : times (0:R) k=0 := by
  induction k with
  | zero => rfl
  | succ k ih => simp [times,ih,A.zero_add]

structure Snapshot (I : Type v) (R : Type u) where
  numerator : I → Int
  mass : I → R
  same_entry : ∀ i j, numerator i=numerator j → mass i=mass j

/- This class value is local to one snapshot. Finite orbital histories are
not assigned a single response function across times. -/
private noncomputable def classMass (s : Snapshot I R) (n : Int) : R := by
  classical
  exact if h : ∃ i, s.numerator i=n then s.mass h.choose else 0

omit [Add R] in
private theorem class_at (s : Snapshot I R) (i : I) :
    classMass s (s.numerator i)=s.mass i := by
  classical
  have h : ∃ j, s.numerator j=s.numerator i := ⟨i,rfl⟩
  simp only [classMass,dif_pos h]
  exact s.same_entry _ _ h.choose_spec

private theorem class_row (s : Snapshot (T × C) R) (tag : T) (cells : List C) :
    total (classMass s) (cells.map (fun i => s.numerator (tag,i))) =
    total (fun i => s.mass (tag,i)) cells := by
  rw [total_map]
  exact total_congr cells (fun i _ => class_at s (tag,i))

private theorem scaled_coordinate (A : Additive R) (old whole u p B : R)
    (K S m : Nat) (bound : m ≤ S) (copies : old=times p K)
    (full : whole=times B K) (unit : times u S=B) (cal : p+times u (S-m)=B) :
    times old S=times whole m := by
  have nsum : m+(S-m)=S := by omega
  have one : p=times u m := by
    apply A.cancel_right _ _ (times u (S-m))
    rw [cal,← times_add A,nsum,unit]
  rw [copies,one,full,← unit,times_times A,times_times A,times_times A,times_times A]
  congr 1
  ac_rfl

private theorem uniform_row (A : Additive R) (f : Int → R) (xs : List Int)
    (S k : Nat) (layout : xs=List.replicate S 1++List.replicate k 0)
    (zero : f 0=0) : total f xs=times (f 1) S := by
  rw [layout,total_append A,total_repeat A,total_repeat A,zero,times_zero A,A.add_zero]

private theorem calibrator_row (A : Additive R) (f : Int → R) (xs : List Int)
    (n : Int) (j k : Nat) (layout : xs=n::(List.replicate j 1++List.replicate k 0))
    (zero : f 0=0) : total f xs=f n+times (f 1) j := by
  rw [layout]
  change f n+total f (List.replicate j 1++List.replicate k 0)=_
  rw [total_append A,total_repeat A,total_repeat A,zero,times_zero A,A.add_zero]

/-- The finite tag enumeration and the data enumeration name the tested
register. The reference and calibrator rows are laid out with their unit
entries before their zero padding. K is the actual number of tags.
The original input p enters only via its protected fanout cylinder.
Tag totals start equal as a consequence of replica symmetry. Block
protection carries two tag totals and one frozen target cell to the
final read. A protected blank witnesses zero in that final snapshot.
The output equation multiplies the original target mass by S and the
total input mass by the signed target numerator squared. -/
theorem one_orbit_coordinate
    (A : Additive R) (tags : List T) (cells : List C)
    (target uniform calibrator : T) (i : C)
    (x : C → Int) (S : Nat) (bound : (x i).natAbs^2 ≤ S)
    (fan final : Snapshot (T × C) R) (old whole : R)
    (fanout_entries : ∀ tag cell, fan.numerator (tag,cell)=x cell)
    (old_cylinder : old=total (fun z => fan.mass (z,i)) tags)
    (whole_cylinder : whole=total (fun z => total (fun c => fan.mass (z,c)) cells) tags)
    (hold_target : final.mass (target,i)=fan.mass (target,i))
    (target_entry : final.numerator (target,i)=x i)
    (hold_blocks : ∀ z, z=uniform ∨ z=calibrator →
      total (fun c => final.mass (z,c)) cells=total (fun c => fan.mass (z,c)) cells)
    (blank : T × C) (blank_entry : final.numerator blank=0)
    (blank_start : fan.mass blank=0) (hold_blank : final.mass blank=fan.mass blank)
    (uniform_zeros calibrator_zeros : Nat)
    (uniform_layout : cells.map (fun c => final.numerator (uniform,c)) =
      List.replicate S 1 ++ List.replicate uniform_zeros 0)
    (calibrator_layout : cells.map (fun c => final.numerator (calibrator,c)) =
      x i :: (List.replicate (S-(x i).natAbs^2) 1 ++ List.replicate calibrator_zeros 0)) :
    times old S=times whole ((x i).natAbs^2) := by
  let B := total (fun c => fan.mass (target,c)) cells
  let u := classMass final 1
  let m := (x i).natAbs^2
  have classes (z : T) (c : C) : fan.mass (z,c)=fan.mass (target,c) := by
    apply fan.same_entry
    rw [fanout_entries,fanout_entries]
  have equal_block (z : T) : total (fun c => fan.mass (z,c)) cells=B :=
    total_congr cells (fun c _ => classes z c)
  have full : whole=times B tags.length := by
    rw [whole_cylinder, total_congr tags (fun z _ => equal_block z),total_constant A]
  have copies : old=times (final.mass (target,i)) tags.length := by
    rw [old_cylinder, total_congr tags (fun z _ => classes z i),total_constant A,hold_target]
  have z : classMass final 0=0 := by
    calc
      _ = classMass final (final.numerator blank) := congrArg _ blank_entry.symm
      _ = final.mass blank := class_at ..
      _ = 0 := hold_blank.trans blank_start
  have nc : classMass final (x i)=final.mass (target,i) := by
    rw [← target_entry]; exact class_at ..
  have unit : times u S=B := by
    have q := (class_row final uniform cells).trans
      ((hold_blocks uniform (Or.inl rfl)).trans (equal_block uniform))
    exact (uniform_row A _ _ S _ uniform_layout z).symm.trans q
  have cal : final.mass (target,i)+times u (S-m)=B := by
    have q := (class_row final calibrator cells).trans
      ((hold_blocks calibrator (Or.inr rfl)).trans (equal_block calibrator))
    have result := (calibrator_row A _ _ (x i) _ _ calibrator_layout z).symm.trans q
    simpa only [nc] using result
  exact scaled_coordinate A old whole u _ B tags.length S m bound copies full unit cal

/-- The mass on the cells where a complete-coordinate predicate is true. -/
def restricted (f : I → R) (keep : I → Bool) (xs : List I) : R :=
  total (fun i => if keep i then f i else 0) xs

private theorem total_zeros (A : Additive R) (xs : List I) :
    total (fun _ => (0:R)) xs=0 :=
  (total_constant A xs 0).trans (times_zero A _)

private theorem total_plus (A : Additive R) (comm : ∀ a b : R, a+b=b+a)
    (f g : I → R) (xs : List I) :
    total (fun i => f i+g i) xs=total f xs+total g xs := by
  induction xs with
  | nil => simp [total,A.zero_add]
  | cons i xs ih =>
    change (f i+g i)+total (fun j => f j+g j) xs=(f i+total f xs)+(g i+total g xs)
    rw [ih]
    simp only [A.assoc]
    have swap (a b c : R) : a+(b+c)=b+(a+c) := by
      rw [← A.assoc,comm a b,A.assoc]
    rw [swap (g i) (total f xs)]

private theorem sum_exchange (A : Additive R) (comm : ∀ a b : R, a+b=b+a)
    (xs : List I) (ys : List J) (w : I → J → R) :
    total (fun i => total (w i) ys) xs=total (fun j => total (fun i => w i j) xs) ys := by
  induction xs with
  | nil => simp [total,total_zeros A]
  | cons i xs ih =>
    change total (w i) ys+total (fun i => total (w i) ys) xs =
      total (fun j => w i j+total (fun i => w i j) xs) ys
    rw [ih,total_plus A comm]

private theorem mask_sum (A : Additive R) (f : I → R) (b : Bool) (xs : List I) :
    (if b then total f xs else 0)=total (fun i => if b then f i else 0) xs := by
  cases b <;> simp [total_zeros A]

/-- An edge-supported joint mass with the two prescribed marginals preserves
a moving subset whenever its old and new membership bits agree across every
allowed edge. The identity also holds algebraically for signed weights.
A probabilistic application supplies a nonnegative joint mass at each tick;
the joint mass may depend on the whole preparation and on the tick. -/
theorem supported_coupling (A : Additive R) (comm : ∀ a b : R, a+b=b+a)
    (xs : List I) (ys : List J) (p : I → R) (q : J → R)
    (edge : I → J → Prop) (w : I → J → R) (before : I → Bool) (after : J → Bool)
    (row : ∀ i ∈ xs, p i=total (w i) ys)
    (col : ∀ j ∈ ys, q j=total (fun i => w i j) xs)
    (off : ∀ i ∈ xs, ∀ j ∈ ys, ¬edge i j → w i j=0)
    (transport : ∀ i ∈ xs, ∀ j ∈ ys, edge i j → before i=after j) :
    restricted p before xs=restricted q after ys := by
  have replace (i) (hi : i ∈ xs) (j) (hj : j ∈ ys) :
      (if before i then w i j else 0)=(if after j then w i j else 0) := by
    by_cases e : edge i j
    · rw [transport i hi j hj e]
    · simp [off i hi j hj e]
  calc
    _ = total (fun i => total (fun j => if before i then w i j else 0) ys) xs := by
      apply total_congr
      intro i hi
      rw [row i hi,mask_sum A]
    _ = total (fun i => total (fun j => if after j then w i j else 0) ys) xs := by
      apply total_congr
      intro i hi
      exact total_congr ys (replace i hi)
    _ = total (fun j => total (fun i => if after j then w i j else 0) xs) ys :=
      sum_exchange A comm xs ys _
    _ = _ := by
      apply total_congr
      intro j hj
      rw [col j hj,mask_sum A]

/-- Iterate the coupling identity on a finite directed interval. Vertex
lists, mass tables, membership tests, and support graphs may vary at each
tick. Joint tables exist separately, and are used only for their own tick. -/
theorem directed_interval (A : Additive R) (comm : ∀ a b : R, a+b=b+a)
    (vertices : Nat → List I) (p : Nat → I → R) (mask : Nat → I → Bool)
    (edge : Nat → I → I → Prop) (n : Nat)
    (step : ∀ k, k<n → ∃ w : I → I → R,
      (∀ i ∈ vertices k, p k i=total (w i) (vertices (k+1))) ∧
      (∀ j ∈ vertices (k+1), p (k+1) j=total (fun i => w i j) (vertices k)) ∧
      (∀ i ∈ vertices k, ∀ j ∈ vertices (k+1), ¬edge k i j → w i j=0) ∧
      (∀ i ∈ vertices k, ∀ j ∈ vertices (k+1), edge k i j → mask k i=mask (k+1) j)) :
    restricted (p 0) (mask 0) (vertices 0)=restricted (p n) (mask n) (vertices n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    obtain ⟨w,row,col,off,trans⟩ := step n (by omega)
    exact (ih (fun k h => step k (by omega))).trans
      (supported_coupling A comm _ _ _ _ _ w _ _ row col off trans)

/-- A pair mixer only has support on the diagonal and on the ordered
pair's other endpoint. A mask containing whole pairs meets the support
premise of the coupling theorem. -/
theorem mixer_mask (partner : I → I) (keep : I → Bool)
    (pairs : ∀ i, keep (partner i)=keep i)
    (i j : I) (edge : j=i ∨ j=partner i) : keep i=keep j := by
  rcases edge with eq | eq
  · rw [eq]
  · rw [eq,pairs]

/-- A private rail mixer can choose either rail, while the physical routing
permutation P sends the logical wire to P(wire). The output wire mask is
pulled back along the inverse permutation, so its membership agrees on
every supported edge, including both private rails. -/
theorem routed_wire_mask (P P_inv : I → I) (left_inv : ∀ i, P_inv (P i)=i)
    (keep : I → Bool) (before after : I × Bool) (edge : after.1=P before.1) :
    keep before.1=keep (P_inv after.1) := by
  rw [edge,left_inv]

/-- The integer Hadamard gives one zero port and a doubled bright
numerator for equal or opposite incident entries. The normalized operator
divides these signed numerators by sqrt(2). Both ports vanish at a=0. -/
theorem hadamard_dark_ports (a : Int) :
    (a+a,a-a)=(2*a,0) ∧ (a+(-a),a-(-a))=(0,2*a) := by
  constructor <;> apply Prod.ext <;> dsimp <;> omega

/-- In a closed two-port joint record name the output columns bright and
dark in whichever order the signs require. Positive masses have the
zero-sum property stated below. A sharp dark port forces its entire
column to vanish. The incoming marginals then go to the bright column. -/
theorem dark_column (A : Additive R) (p q ub ud vb vd : R)
    (zero_sum : ∀ a b : R, a+b=0 → a=0 ∧ b=0)
    (row_u : p=ub+ud) (row_v : q=vb+vd) (dark : ud+vd=0) :
    ud=0 ∧ vd=0 ∧ p=ub ∧ q=vb := by
  obtain ⟨a,b⟩ := zero_sum _ _ dark
  exact ⟨a,b,by simpa only [a,A.add_zero] using row_u,
             by simpa only [b,A.add_zero] using row_v⟩

/-- Reverse single-arm fairness concerns the two entries of the *same*
bright column. Its undivided equality applies even at zero mass. -/
theorem reverse_fair_bright_column (A : Additive R) (p q ub ud vb vd : R)
    (zero_sum : ∀ a b : R, a+b=0 → a=0 ∧ b=0)
    (row_u : p=ub+ud) (row_v : q=vb+vd) (dark : ud+vd=0)
    (reverse_fair : ub=vb) : p=q := by
  obtain ⟨_,_,pu,qv⟩ := dark_column A _ _ _ _ _ _ zero_sum row_u row_v dark
  exact pu.trans (reverse_fair.trans qv.symm)

/-- For H followed by H the second joint has a single occupied input.
Forward fairness divides its row equally between the named return ports.
The explicit operational echo hypothesis identifies those returned
marginals with the original p,q. No positive-mass premise is needed. -/
theorem forward_fair_restored_echo (A : Additive R)
    (p q brightU brightV darkU darkV uReturn vReturn : R)
    (zero_sum : ∀ a b : R, a+b=0 → a=0 ∧ b=0)
    (dark_row : darkU+darkV=0) (forward_fair : brightU=brightV)
    (col_u : uReturn=brightU+darkU) (col_v : vReturn=brightV+darkV)
    (restore_u : uReturn=p) (restore_v : vReturn=q) : p=q := by
  obtain ⟨_,_,u,v⟩ := dark_column A _ _ _ _ _ _ zero_sum col_u col_v dark_row
  exact restore_u.symm.trans (u.trans (forward_fair.trans (v.symm.trans restore_v)))

/-- Certify successive edges of an ordered equal-signed class by opposite
child sectors. The Boolean flips on every edge, so edges of a single
sector are disjoint in a list of distinct addresses. The edge equalities
are the conclusions of the chosen local probe (reverse fairness or echo). -/
def alternatingEdges (child : Bool → I → R) : Bool → List I → Prop
  | _, [] => True
  | _, [_] => True
  | sector, i::j::tail =>
    child sector i=child sector j ∧ alternatingEdges child (!sector) (j::tail)

omit [OfNat R 0] in
/-- Equal fair copies make the edge probes transferable to their parent
ports. Iterating the certified edges yields one weight on the whole class
in that actual preparation. No pre-existing equality of equal entries is
used by this implication. -/
theorem probed_class (parent : I → R) (child : Bool → I → R)
    (split : ∀ i, parent i=child false i+child true i)
    (fair : ∀ i, child false i=child true i) (i : I) (tail : List I)
    (s : Bool) (probes : alternatingEdges child s (i::tail)) :
    ∀ j ∈ i::tail, parent j=parent i := by
  have lift_edge (b : Bool) (x y : I) (h : child b x=child b y) : parent x=parent y := by
    cases b
    · rw [split x,split y,← fair x,← fair y,h]
    · rw [split x,split y,fair x,fair y,h]
  induction tail generalizing i s with
  | nil =>
    intro j hj
    exact congrArg parent (List.mem_singleton.mp hj)
  | cons k rest ih =>
    obtain ⟨edge,next⟩ := probes
    have pk := lift_edge s i k edge
    intro j hj
    rcases List.mem_cons.mp hj with same | later
    · rw [same]
    · exact (ih k (!s) next j later).trans pk.symm

end AutonomousRecords
