import Std

/-!
# Binary electric flux on an infinite ordered two-occupation chain

Link j joins j to j+1. The chosen vacuum sector has zero flux on the
far left. All positions and link labels are integers; lists below enumerate
the finite support exactly. No scalar field dynamics or continuum assumptions.
-/
namespace GaussString

abbrev Field := Int → Bool

def flux (x y j : Int) : Bool := decide (x≤j ∧ j<y)
def occupied (x y i : Int) : Bool := decide (i=x ∨ i=y)
def toggle (b : Int) (f : Field) : Field := fun j => if j=b then !(f j) else f j

theorem gauss (x y i : Int) (ordered : x<y) :
    Bool.xor (flux x y (i-1)) (flux x y i) = occupied x y i := by
  by_cases hL : x≤i-1 ∧ i-1<y <;> by_cases hR : x≤i ∧ i<y <;>
    by_cases q : i=x ∨ i=y <;> simp [flux,occupied,hL,hR,q] <;> omega

def links (x y : Int) : List Int :=
  (List.range (y-x).toNat).map fun (n : Nat) => x+(n:Int)

theorem exact_support (x y j : Int) :
    j ∈ links x y ↔ flux x y j=true := by
  simp only [links,List.mem_map,List.mem_range,flux,decide_eq_true_eq]
  constructor
  · rintro ⟨i,hi,hj⟩
    omega
  · intro inside
    exact ⟨(j-x).toNat,by omega,by omega⟩

theorem support_size (x y : Int) : (links x y).length=(y-x).toNat := by simp [links]

theorem no_duplicates (x y : Int) : (links x y).Nodup := by
  exact List.Pairwise.map _ (fun i j ne eq => ne (by omega)) List.nodup_range

def bit (b : Bool) : Nat := if b then 1 else 0

theorem count_true (f : Field) (js : List Int) (ones : ∀ j ∈ js, f j=true) :
    (js.map fun j => bit (f j)).sum = js.length := by
  induction js with
  | nil => rfl
  | cons j js ih =>
    simp only [List.map_cons,List.sum_cons,List.length_cons,
      ih (fun k hk => ones k (by simp [hk])),ones j (by simp)]
    dsimp [bit]
    omega

theorem electric_energy (x y : Int) :
    ((links x y).map fun j => bit (flux x y j)).sum = (y-x).toNat := by
  rw [count_true,support_size]
  exact fun j mem => (exact_support x y j).mp mem

theorem left_right (x y b : Int) (legal : x+1<y) :
    flux (x+1) y b = toggle x (flux x y) b := by
  by_cases e : b=x <;> by_cases a : x+1≤b ∧ b<y <;> by_cases v : x≤b ∧ b<y <;>
    first | (exfalso; omega) | (simp only [toggle,flux]; simp only [a,v,decide_true,decide_false]; split <;> simp_all <;> omega)

theorem right_right (x y b : Int) (legal : x<y) :
    flux x (y+1) b = toggle y (flux x y) b := by
  by_cases e : b=y <;> by_cases a : x≤b ∧ b<y+1 <;> by_cases v : x≤b ∧ b<y <;>
    first | (exfalso; omega) | (simp only [toggle,flux]; simp only [a,v,decide_true,decide_false]; split <;> simp_all <;> omega)

theorem left_left (x y b : Int) (legal : x<y) :
    flux (x-1) y b = toggle (x-1) (flux x y) b := by
  by_cases e : b=x-1 <;> by_cases a : x-1≤b ∧ b<y <;> by_cases v : x≤b ∧ b<y <;>
    first | (exfalso; omega) | (simp only [toggle,flux]; simp only [a,v,decide_true,decide_false]; split <;> simp_all <;> omega)

theorem right_left (x y b : Int) (legal : x<y-1) :
    flux x (y-1) b = toggle (y-1) (flux x y) b := by
  by_cases e : b=y-1 <;> by_cases a : x≤b ∧ b<y-1 <;> by_cases v : x≤b ∧ b<y <;>
    first | (exfalso; omega) | (simp only [toggle,flux]; simp only [a,v,decide_true,decide_false]; split <;> simp_all <;> omega)

/-- A local directed update either leaves the occupations in place or
crosses the bond with exactly one particle into its vacant neighbour. -/
inductive Edge : Int → Int → Int → Int → Option Int → Prop
  | stay (x y : Int) : Edge x y x y none
  | leftR (x y : Int) (h : x+1<y) : Edge x y (x+1) y (some x)
  | rightR (x y : Int) (h : x<y) : Edge x y x (y+1) (some y)
  | leftL (x y : Int) (h : x<y) : Edge x y (x-1) y (some (x-1))
  | rightL (x y : Int) (h : x<y-1) : Edge x y x (y-1) (some (y-1))

def transport (e : Option Int) (f : Field) :=
  match e with | none => f | some b => toggle b f

theorem edge_intertwiner (x y u v : Int) (e : Option Int) (legal : Edge x y u v e) :
    transport e (flux x y) = flux u v := by
  cases legal with
  | stay => rfl
  | leftR h => funext b; exact (left_right _ _ b h).symm
  | rightR h => funext b; exact (right_right _ _ b h).symm
  | leftL h => funext b; exact (left_left _ _ b h).symm
  | rightL h => funext b; exact (right_left _ _ b h).symm

inductive Path : Int → Int → Int → Int → List (Option Int) → Prop
  | nil (x y : Int) : Path x y x y []
  | cons (step : Edge x y u v e) (rest : Path u v w z es) :
      Path x y w z (e::es)

def traverse : List (Option Int) → Field → Field
  | [], f => f
  | e::es, f => traverse es (transport e f)

theorem path_intertwiner (x y w z : Int) (es : List (Option Int))
    (path : Path x y w z es) : traverse es (flux x y) = flux w z := by
  induction path with
  | nil => rfl
  | cons step rest ih => simp only [traverse,edge_intertwiner _ _ _ _ _ step,ih]

/-- Finite charge lists are interpreted modulo two, including at repeated sites. -/
def prefixFlux (j : Int) : List Int → Bool
  | [] => false
  | z::zs => Bool.xor (decide (z≤j)) (prefixFlux j zs)

def chargeParity (i : Int) : List Int → Bool
  | [] => false
  | z::zs => Bool.xor (decide (z=i)) (chargeParity i zs)

theorem xor_shuffle (a b c d : Bool) :
    Bool.xor (Bool.xor a b) (Bool.xor c d) = Bool.xor (Bool.xor a c) (Bool.xor b d) := by
  cases a <;> cases b <;> cases c <;> cases d <;> rfl

theorem one_jump (z i : Int) :
    Bool.xor (decide (z≤i-1)) (decide (z≤i))=decide (z=i) := by
  by_cases h : z≤i-1 <;> by_cases g : z≤i <;> by_cases eq : z=i <;>
    first | (exfalso; omega) | (simp [h,g,eq] <;> omega)

theorem prefix_gauss (i : Int) (zs : List Int) :
    Bool.xor (prefixFlux (i-1) zs) (prefixFlux i zs) = chargeParity i zs := by
  induction zs with
  | nil => rfl
  | cons z zs ih => rw [prefixFlux,prefixFlux,chargeParity,xor_shuffle,one_jump,ih]

theorem paired_prefix (x y j : Int) (ordered : x<y) :
    prefixFlux j [x,y] = flux x y j := by
  by_cases xj : x≤j <;> by_cases yj : y≤j <;> by_cases inside : x≤j ∧ j<y <;>
    first | (exfalso; omega) | simp [prefixFlux,flux,xj,yj,inside]

theorem spectator_hop (b j : Int) (zs : List Int) :
    prefixFlux j ((b+1)::zs) =
    toggle b (fun z => prefixFlux z (b::zs)) j := by
  by_cases eq : j=b
  · subst j
    simp [prefixFlux,toggle,show ¬b+1≤b by omega]
  · have h : (b+1≤j) = (b≤j) := propext (by omega)
    simp only [toggle,if_neg eq,prefixFlux,h]

theorem complement_same_gauss (f : Field) (i : Int) :
    Bool.xor (!(f (i-1))) (!(f i)) = Bool.xor (f (i-1)) (f i) := by
  cases f (i-1) <;> cases f i <;> rfl

/-- The local-link contribution and scalar separation energy agree at every
sample, hence also as an integrated exponent on any finite history. -/
theorem action (states : List (Int × Int)) (coupling : Int) :
    (states.map fun p => coupling * (((links p.1 p.2).map
      (fun j => bit (flux p.1 p.2 j))).sum:Int)).sum =
    (states.map fun p => coupling * ((p.2-p.1).toNat:Int)).sum := by
  simp only [electric_energy]

end GaussString
