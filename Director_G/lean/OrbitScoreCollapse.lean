import Std

/-! The two substitutions in the rail score equation, before any lattice
    extension. The explicitly listed additive properties apply in particular
    to real scores. Neither a sign order nor an inverse on the input is used. -/
namespace OrbitScoreCollapse

variable {X A : Type} [Add A] {join : X → X → X} {empty : X} {T : X → X}
  {F : X → A} {zero : A}

def Balanced (join : X → X → X) (T : X → X) (F : X → A) : Prop :=
  ∀ u v, F (join u v) + F (join u (T v)) = (F u + F v) + (F u + F v)

theorem shiftInvariant (balance : Balanced join T F)
    (emptyJoin : ∀ x, join empty x = x) (emptyScore : F empty = zero)
    (zeroAdd : ∀ a : A, zero + a = a)
    (cancel : ∀ a b c : A, a + b = a + c → b = c) (v : X) :
    F (T v) = F v := by
  have h := balance empty v
  simp only [emptyJoin, emptyScore, zeroAdd] at h
  exact cancel _ _ _ h

theorem contextualSquare (balance : Balanced join T F) (invariant : ∀ v, F (T v) = F v)
    (comm : ∀ a b : A, a + b = b + a)
    (cancel : ∀ a b c : A, a + b = a + c → b = c) (u v : X) :
    F (join u v) = F (join u (T (T v))) := by
  have h := balance u (T v)
  rw [invariant v] at h
  apply cancel (F (join u (T v)))
  exact (comm _ _).trans ((balance u v).trans h.symm)

theorem fixedAddition (balance : Balanced join T F)
    (doubleInj : ∀ a b : A, a+a = b+b → a=b) (u c : X) (fixed : T c = c) :
    F (join u c) = F u + F c := by
  have h := balance u c
  rw [fixed] at h
  exact doubleInj _ _ h

end OrbitScoreCollapse
