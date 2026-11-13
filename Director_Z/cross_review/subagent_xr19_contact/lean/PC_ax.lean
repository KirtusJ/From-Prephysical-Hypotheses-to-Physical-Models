import Std

/-!
# Contact instrument for two real phase planes and its tree record

Real-coordinate coefficients are integers, with the common factor 1/2 of
the H/control/H instrument suppressed. The tree section uses the character
signs of J, not extra physical measurements of individual signs.
-/
namespace PhaseContact

structure PairState where
  a : Int   -- 00
  b : Int   -- 01
  c : Int   -- 10
  d : Int   -- 11
  deriving DecidableEq

def leftJ (p : PairState) : PairState := ⟨-p.c,-p.d,p.a,p.b⟩
def rightJ (p : PairState) : PairState := ⟨-p.b,p.a,-p.d,p.c⟩
def minus (p : PairState) : PairState := ⟨-p.a,-p.b,-p.c,-p.d⟩
def contact (p : PairState) : PairState := minus (leftJ (rightJ p))
def reflectRight (p : PairState) : PairState := ⟨p.a,-p.b,p.c,-p.d⟩
def add (p q : PairState) : PairState := ⟨p.a+q.a,p.b+q.b,p.c+q.c,p.d+q.d⟩
def port (negative : Bool) (p : PairState) : PairState :=
  add p (if negative then minus (contact p) else contact p)

theorem contact_map (p : PairState) : contact p = ⟨-p.d,p.c,p.b,-p.a⟩ := by
  simp [contact,leftJ,rightJ,minus]

theorem contact_involution (p : PairState) : contact (contact p) = p := by
  simp [contact_map]

theorem reverse_child (p : PairState) :
    contact (reflectRight p) = minus (reflectRight (contact p)) := by
  simp [contact_map,reflectRight,minus]

theorem port_eigen (bad : Bool) (p : PairState) :
    contact (port bad p) = if bad then minus (port bad p) else port bad p := by
  cases bad <;> simp [port,contact_map,minus,add] <;>
    congr 1 <;> omega

def corrected (bad : Bool) (p : PairState) :=
  if bad then reflectRight (port bad p) else port bad p

theorem corrected_bright (bad : Bool) (p : PairState) :
    contact (corrected bad p) = corrected bad p := by
  cases bad
  · exact port_eigen false p
  · change contact (reflectRight (port true p)) = reflectRight (port true p)
    rw [reverse_child,port_eigen]
    simp [minus,reflectRight]

def square (p : PairState) := p.a*p.a+p.b*p.b+p.c*p.c+p.d*p.d

theorem energy_ports (p : PairState) :
    square (port false p) + square (port true p) = 4*square p := by
  simp [square,port,minus,add,contact_map,Int.add_mul,Int.mul_add,Int.mul_neg,Int.neg_mul]
  omega

def product (x y z w : Int) : PairState := ⟨x*z,x*w,y*z,y*w⟩

theorem independent_fair (x y z w : Int) :
    square (port false (product x y z w)) = square (port true (product x y z w)) := by
  have cross : (x*z)*(y*w)=(x*w)*(y*z) := by ac_rfl
  have cross' : (y*w)*(x*z)=(y*z)*(x*w) := by ac_rfl
  simp only [product,square,port,Bool.false_eq_true,if_false,if_true,add,minus,contact_map,
    Int.neg_neg,Int.add_mul,Int.mul_add,Int.mul_neg,Int.neg_mul]
  omega

theorem product_read (bad : Bool) (x y z w : Int) :
    square (port bad (product x y z w)) = 2*square (product x y z w) := by
  have s := energy_ports (product x y z w)
  have h := independent_fair x y z w
  cases bad <;> omega

theorem same_localized_output :
    corrected true (product 1 0 1 0) = corrected false (product 1 0 1 0) := by decide

theorem one_side_trace_of_fresh_contact :
    let p := port false (product 1 0 1 0)
    p.a*p.a+p.b*p.b = 1 ∧ p.c*p.c+p.d*p.d = 1 ∧ p.a*p.c+p.b*p.d = 0 := by decide

theorem already_aligned_is_not_fair :
    square (port true (corrected false (product 1 0 1 0))) = 0 := by decide

/-- A tree is presented by unique root paths (lists of edge identifiers);
edge bits are recorded eigenvalues: false=+1, true=-1. -/
def bit (a b : Bool) := Bool.xor a b
def parity : List Bool → Bool
  | [] => false
  | b::bs => bit b (parity bs)

theorem bit_self (a : Bool) : bit a a = false := by cases a <;> rfl
theorem bit_assoc (a b c : Bool) : bit (bit a b) c = bit a (bit b c) := by
  cases a <;> cases b <;> cases c <;> rfl
theorem bit_comm (a b : Bool) : bit a b = bit b a := by cases a <;> cases b <;> rfl
theorem cancel (a b : Bool) : bit a (bit a b) = b := by cases a <;> cases b <;> rfl

def correction (edges : A → Bool) (path : List A) := parity (path.map edges)

theorem append_bit (xs : List Bool) (b : Bool) :
    parity (xs++[b]) = bit (parity xs) b := by
  induction xs with
  | nil => cases b <;> rfl
  | cons a xs ih =>
    simp only [List.cons_append,parity,ih,bit_assoc]

theorem child_frame (edges : A → Bool) (path : List A) (child : A) :
    correction edges (path++[child]) = bit (correction edges path) (edges child) := by
  simp [correction,append_bit]

theorem corrected_edge (edges : A → Bool) (path : List A) (child : A) (u v : Bool)
    (observed : bit u v = edges child) :
    bit u (correction edges path) = bit v (correction edges (path++[child])) := by
  rw [child_frame,← observed]
  cases u <;> cases v <;> cases correction edges path <;> rfl

/-- The signs along any walk telescope; a closed walk has even negative-edge parity. -/
def differences (first : Bool) : List Bool → List Bool
  | [] => []
  | v::vs => bit first v :: differences v vs

def endpoint (first : Bool) : List Bool → Bool
  | [] => first
  | v::vs => endpoint v vs

theorem path_sign (u : Bool) (vs : List Bool) :
    parity (differences u vs) = bit u (endpoint u vs) := by
  induction vs generalizing u with
  | nil => simp [differences,parity,endpoint,bit_self]
  | cons v vs ih =>
    simp only [differences,parity,endpoint,ih]
    rw [bit_assoc,cancel]

theorem loop_sign (u : Bool) (vs : List Bool) (closed : endpoint u vs = u) :
    parity (differences u vs) = false := by rw [path_sign,closed,bit_self]

theorem same_record_under_conjugation (u v : Bool) : bit (!u) (!v) = bit u v := by
  cases u <;> cases v <;> rfl

/-- Finite rooted tree in insertion order. A new leaf chooses the root or
one previously inserted vertex; recursive decoding retains the whole prefix
in reverse order. The bound rules out a reference to a future vertex. -/
def parentBit (root : Bool) (prev : List Bool) (index : Nat) :=
  (prev ++ [root]).getD index root

def decode (root : Bool) : List (Nat × Bool) → List Bool → List Bool
  | [], prev => prev
  | (j,e)::rest, prev => decode root rest (bit (parentBit root prev j) e :: prev)

def encode (root : Bool) : List Nat → List Bool → List Bool → List (Nat × Bool)
  | j::js, v::vs, prev => (j,bit (parentBit root prev j) v)::encode root js vs (v::prev)
  | _, _, _ => []

theorem decode_encode (root : Bool) (js : List Nat) (vs prev : List Bool)
    (lengths : js.length = vs.length) :
    decode root (encode root js vs prev) prev = vs.reverse ++ prev := by
  induction js generalizing vs prev with
  | nil =>
    cases vs <;> simp_all [encode,decode]
  | cons j js ih =>
    cases vs with
    | nil => simp at lengths
    | cons v vs =>
      simp only [List.length_cons,Nat.succ.injEq] at lengths
      simp only [encode,decode,cancel,ih vs _ lengths,List.reverse_cons,List.append_assoc,
        List.singleton_append]

def assigned (root : Bool) : List (Nat × Bool) → List Bool → List Bool
  | [], _ => []
  | (j,e)::rest, prev =>
    let v := bit (parentBit root prev j) e
    v :: assigned root rest (v::prev)

theorem encode_assigned (root : Bool) (es : List (Nat × Bool)) (prev : List Bool) :
    encode root (es.map Prod.fst) (assigned root es prev) prev = es := by
  induction es generalizing prev with
  | nil => rfl
  | cons je es ih =>
    rcases je with ⟨j,e⟩
    simp only [List.map_cons,assigned,encode,cancel,ih]

theorem decode_assigned (root : Bool) (es : List (Nat × Bool)) (prev : List Bool) :
    decode root es prev = (assigned root es prev).reverse ++ prev := by
  induction es generalizing prev with
  | nil => rfl
  | cons je es ih =>
    rcases je with ⟨j,e⟩
    simp only [decode,assigned,ih,List.reverse_cons,List.append_assoc,List.singleton_append]

/-- Any legal parent table defines a rooted tree. Each transcript has exactly
one sign assignment for a specified root (and hence two with root unspecified).
No statistical independence is postulated by this purely combinatorial inverse. -/
theorem unique_fibre (root : Bool) (es : List (Nat × Bool)) (vs : List Bool)
    (len : es.length = vs.length) :
    encode root (es.map Prod.fst) vs [] = es ↔ vs = assigned root es [] := by
  constructor
  · intro observed
    have h := decode_encode root (es.map Prod.fst) vs [] (by simpa using len)
    rw [observed,decode_assigned] at h
    simpa using congrArg List.reverse h.symm
  · intro h
    rw [h,encode_assigned]

/-- Joint equal-weight mass numerator over denominator 2^(number of planes):
the two possible root signs account for the whole fibre. -/
theorem localized_tree_weight (edges : Nat) : 2^(edges+1) = 2*(2^edges) := by
  rw [Nat.pow_succ,Nat.mul_comm]

end PhaseContact

#print axioms PhaseContact.contact_map
#print axioms PhaseContact.contact_involution
#print axioms PhaseContact.reverse_child
#print axioms PhaseContact.port_eigen
#print axioms PhaseContact.corrected_bright
#print axioms PhaseContact.energy_ports
#print axioms PhaseContact.independent_fair
#print axioms PhaseContact.product_read
#print axioms PhaseContact.same_localized_output
#print axioms PhaseContact.one_side_trace_of_fresh_contact
#print axioms PhaseContact.already_aligned_is_not_fair
#print axioms PhaseContact.bit_self
#print axioms PhaseContact.bit_assoc
#print axioms PhaseContact.bit_comm
#print axioms PhaseContact.cancel
#print axioms PhaseContact.append_bit
#print axioms PhaseContact.child_frame
#print axioms PhaseContact.corrected_edge
#print axioms PhaseContact.path_sign
#print axioms PhaseContact.loop_sign
#print axioms PhaseContact.same_record_under_conjugation
#print axioms PhaseContact.decode_encode
#print axioms PhaseContact.encode_assigned
#print axioms PhaseContact.decode_assigned
#print axioms PhaseContact.unique_fibre
#print axioms PhaseContact.localized_tree_weight
