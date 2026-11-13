import Std

/-!
# The signed Hadamard block on integer multiset counts

For each of finitely many residue classes, a gain multiset counts the two
signs separately. J exchanges all plus and minus counts. The input law is
assumed for every such multiset, with F taking integer values. The factors
of two below avoid dividing a general integer-valued F by two.
-/
namespace MultisetBlock

structure Counts (q : Nat) where
  pos : Fin q → Nat
  neg : Fin q → Nat

def empty : Counts q := ⟨fun _ => 0,fun _ => 0⟩
def join (u v : Counts q) : Counts q := ⟨fun i => u.pos i+v.pos i,fun i => u.neg i+v.neg i⟩
def flip (u : Counts q) : Counts q := ⟨u.neg,u.pos⟩
def sym (u : Counts q) := join u (flip u)
def diag (n : Fin q → Nat) : Counts q := ⟨n,n⟩
def diff (u : Counts q) (i : Fin q) : Int := (u.pos i:Int)-(u.neg i:Int)
def rep (x : Fin q → Int) : Counts q :=
  ⟨fun i => (x i).toNat,fun i => (-(x i)).toNat⟩

def Law (F : Counts q → Int) := ∀ u v,
  F (join u v)+F (join u (flip v)) = 2*F u+2*F v

private theorem count_ext {u v : Counts q} (h : ∀i,u.pos i=v.pos i)
    (g : ∀i,u.neg i=v.neg i) : u=v := by
  cases u; cases v
  congr 1 <;> funext i
  · exact h i
  · exact g i

private theorem sym_fixed (u : Counts q) : flip (sym u)=sym u := by
  apply count_ext <;> intro i <;> simp [flip,sym,join,Nat.add_comm]

private theorem sym_join (u v : Counts q) : sym (join u v)=join (sym u) (sym v) := by
  apply count_ext <;> intro i <;> dsimp [sym,join,flip] <;> omega

private theorem sym_flip (u : Counts q) : sym (flip u)=sym u := by
  apply count_ext <;> intro i <;> simp [sym,join,flip,Nat.add_comm]

private theorem empty_join (u : Counts q) : join empty u=u := by
  apply count_ext <;> intro i <;> simp [join,empty]

theorem zero_value (F : Counts q → Int) (law : Law F) : F empty=0 := by
  have h := law empty empty
  rw [empty_join,empty_join] at h
  change F empty + F empty=2*F empty+2*F empty at h
  omega

theorem symmetric_additivity (F : Counts q → Int) (law : Law F)
    (u c : Counts q) (fixed : flip c=c) : F (join u c)=F u+F c := by
  have h := law u c
  rw [fixed] at h
  omega

theorem sign_invariant (F : Counts q → Int) (law : Law F) (u : Counts q) : F (flip u)=F u := by
  have h := law empty u
  rw [empty_join,empty_join,zero_value F law] at h
  omega

def pairContent (F : Counts q → Int) (u : Counts q) := F (sym u)
def corrected (F : Counts q → Int) (u : Counts q) := 2*F u-pairContent F u

theorem content_additive (F : Counts q → Int) (law : Law F) (u v : Counts q) :
    pairContent F (join u v)=pairContent F u+pairContent F v := by
  unfold pairContent
  rw [sym_join,symmetric_additivity F law (sym u) (sym v) (sym_fixed v)]

theorem corrected_stable (F : Counts q → Int) (law : Law F)
    (u c : Counts q) (fixed : flip c=c) : corrected F (join u c)=corrected F u := by
  have hc : pairContent F c = 2*F c := by
    unfold pairContent sym
    rw [fixed,symmetric_additivity F law c c fixed]
    omega
  unfold corrected
  rw [content_additive F law,symmetric_additivity F law u c fixed,hc]
  omega

/-- u and v with the same signed differences can be made literally equal:
adjoin v's negative counts to both signs of u, and u's to both signs of v. -/
theorem equalized (u v : Counts q) (same : diff u=diff v) :
    join u (diag v.neg)=join v (diag u.neg) := by
  apply count_ext
  · intro i
    have h := congrFun same i
    dsimp [diff] at h
    dsimp [join, diag]
    omega
  · intro i
    dsimp [join,diag]
    omega

theorem depends_on_difference (F : Counts q → Int) (law : Law F)
    (u v : Counts q) (same : diff u = diff v) : corrected F u=corrected F v := by
  calc
    _ = corrected F (join u (diag v.neg)) := (corrected_stable F law _ _ rfl).symm
    _ = corrected F (join v (diag u.neg)) := congrArg (corrected F) (equalized u v same)
    _ = _ := corrected_stable F law _ _ rfl

theorem rep_difference (x : Fin q → Int) : diff (rep x)=x := by
  funext i
  dsimp [diff,rep]
  omega

def lattice (F : Counts q → Int) (x : Fin q → Int) := corrected F (rep x)

theorem descends (F : Counts q → Int) (law : Law F) (u : Counts q) :
    lattice F (diff u)=corrected F u :=
  depends_on_difference F law _ _ (rep_difference _)

theorem scaled_decomposition (F : Counts q → Int) (law : Law F) (u : Counts q) :
    2*F u=pairContent F u+lattice F (diff u) := by
  rw [descends F law]
  unfold corrected
  omega

theorem corrected_law (F : Counts q → Int) (law : Law F) : Law (corrected F) := by
  intro u v
  have original := law u v
  have same : pairContent F (flip v)=pairContent F v := congrArg F (sym_flip v)
  unfold corrected
  rw [content_additive F law,content_additive F law,same]
  omega

private theorem diff_join (u v : Counts q) :
    diff (join u v)=fun i => diff u i+diff v i := by
  funext i
  dsimp [diff,join]
  omega

private theorem diff_flipped_join (u v : Counts q) :
    diff (join u (flip v))=fun i => diff u i-diff v i := by
  funext i
  dsimp [diff,join,flip]
  omega

theorem parallelogram (F : Counts q → Int) (law : Law F) (x y : Fin q → Int) :
    lattice F (fun i => x i+y i)+lattice F (fun i => x i-y i) =
      2*lattice F x+2*lattice F y := by
  have h := corrected_law F law (rep x) (rep y)
  rw [← descends F law (join (rep x) (rep y)),← descends F law (join (rep x) (flip (rep y))),
      diff_join,diff_flipped_join,rep_difference,rep_difference] at h
  exact h

/-! ## Division-free polarization on the signed count lattice -/

abbrev Vec (q : Nat) := Fin q → Int
def plus (x y : Vec q) : Vec q := fun i => x i+y i
def minus (x y : Vec q) : Vec q := fun i => x i-y i
def neg (x : Vec q) : Vec q := fun i => -(x i)
def nilVec : Vec q := fun _ => 0

def para (Q : Vec q → Int) := ∀x y,Q (plus x y)+Q (minus x y)=2*Q x+2*Q y
def polar (Q : Vec q → Int) (x y : Vec q) := Q (plus x y)-Q (minus x y)

private theorem vec_zero (Q : Vec q → Int) (p : para Q) : Q nilVec=0 := by
  have h := p nilVec nilVec
  have a : plus (nilVec : Vec q) nilVec = nilVec := by funext i; rfl
  have b : minus (nilVec : Vec q) nilVec = nilVec := by funext i; rfl
  rw [a,b] at h
  omega

private theorem vec_even (Q : Vec q → Int) (p : para Q) (x : Vec q) : Q (neg x)=Q x := by
  have h := p nilVec x
  have a : plus nilVec x=x := by funext i; simp [plus,nilVec]
  have b : minus nilVec x=neg x := by funext i; simp [minus,neg,nilVec]
  rw [a,b,vec_zero Q p] at h
  omega

theorem polar_symmetric (Q : Vec q → Int) (p : para Q) (x y : Vec q) :
    polar Q x y=polar Q y x := by
  have addxy : plus x y=plus y x := by funext i; simp [plus,Int.add_comm]
  have subxy : minus x y=neg (minus y x) := by funext i; dsimp [minus,neg]; omega
  unfold polar
  rw [addxy,subxy,vec_even Q p]

private theorem polar_odd (Q : Vec q → Int) (p : para Q) (x y : Vec q) :
    polar Q (neg x) y = -polar Q x y := by
  have a : plus (neg x) y = neg (minus x y) := by funext i; dsimp [plus,minus,neg]; omega
  have b : minus (neg x) y = neg (plus x y) := by funext i; dsimp [plus,minus,neg]; omega
  unfold polar
  rw [a,b,vec_even Q p,vec_even Q p]
  omega

private theorem polar_jensen (Q : Vec q → Int) (p : para Q) (x z y : Vec q) :
    polar Q (plus x z) y + polar Q (minus x z) y = 2*polar Q x y := by
  have pp : plus (plus x z) y=plus (plus x y) z := by funext i; dsimp [plus]; omega
  have mp : plus (minus x z) y=minus (plus x y) z := by funext i; dsimp [plus,minus]; omega
  have pm : minus (plus x z) y=plus (minus x y) z := by funext i; dsimp [plus,minus]; omega
  have mm : minus (minus x z) y=minus (minus x y) z := by funext i; dsimp [minus]; omega
  have h₁ := p (plus x y) z
  have h₂ := p (minus x y) z
  unfold polar
  rw [pp,mp,pm,mm]
  omega

theorem polar_additive (Q : Vec q → Int) (p : para Q) (x z y : Vec q) :
    polar Q (plus x z) y = polar Q x y+polar Q z y := by
  have a := polar_jensen Q p x z y
  have b := polar_jensen Q p z x y
  have sw₁ : plus z x=plus x z := by funext i; dsimp [plus]; omega
  have sw₂ : minus z x=neg (minus x z) := by funext i; dsimp [minus,neg]; omega
  rw [sw₁,sw₂,polar_odd Q p] at b
  omega

theorem polar_additive_right (Q : Vec q → Int) (p : para Q) (x y z : Vec q) :
    polar Q x (plus y z) = polar Q x y+polar Q x z := by
  rw [polar_symmetric Q p x (plus y z),polar_additive Q p,polar_symmetric Q p y x,
      polar_symmetric Q p z x]

theorem polar_diagonal (Q : Vec q → Int) (p : para Q) (x : Vec q) :
    polar Q x x = 4*Q x := by
  have z : minus x x=nilVec := by funext i; simp [minus,nilVec]
  have a := p x x
  rw [z,vec_zero Q p] at a
  unfold polar
  rw [z,vec_zero Q p]
  omega

/-- The extracted polar form is symmetric and separately additive. Its
diagonal, divided by four where one works over the rationals, recovers Q. -/
theorem polarized_decomposition (F : Counts q → Int) (law : Law F) (u : Counts q) :
    8*F u = 4*pairContent F u+polar (lattice F) (diff u) (diff u) := by
  have p : para (lattice F) := parallelogram F law
  have splitF := scaled_decomposition F law u
  rw [polar_diagonal _ p]
  omega

theorem converse (F L : Counts q → Int) (Q : Vec q → Int)
    (hL : ∀u v,L (join u v)=L u+L v) (flipL : ∀u,L (flip u)=L u)
    (hQ : para Q) (splitF : ∀u,2*F u=L u+Q (diff u)) : Law F := by
  intro u v
  have a := splitF (join u v)
  have b := splitF (join u (flip v))
  have c := splitF u
  have d := splitF v
  have h := hQ (diff u) (diff v)
  rw [hL,diff_join] at a
  rw [hL,flipL,diff_flipped_join] at b
  change Q (fun i => diff u i+diff v i)+Q (fun i => diff u i-diff v i)=_ at h
  omega

theorem signed_block_iff (F : Counts q → Int) :
    Law F ↔ ∃ (L : Counts q → Int) (Q : Vec q → Int),
      (∀u v, L (join u v)=L u+L v) ∧ (∀u,L (flip u)=L u) ∧ para Q ∧
      (∀u,2*F u=L u+Q (diff u)) := by
  constructor
  · intro law
    exact ⟨pairContent F,lattice F,content_additive F law,
      fun u => congrArg F (sym_flip u),parallelogram F law,scaled_decomposition F law⟩
  · rintro ⟨L,Q,hL,hJ,hQ,hF⟩
    exact converse F L Q hL hJ hQ hF

end MultisetBlock
