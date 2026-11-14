import Std

namespace ExactSiteIntervention

/-- Flattened real two-by-two matrix kernel, with the amplitude divisor omitted. -/
structure Kernel where
  a : Int
  b : Int
  c : Int
  d : Int

/-- X -> J X J^{-1}, J(r,l)=(l,-r). -/
def mirror (t : Kernel) : Kernel := ⟨t.d, -t.c, -t.b, t.a⟩

def effect (t : Kernel) : Int × Int × Int :=
  (t.a*t.a + t.c*t.c, t.b*t.b + t.d*t.d, t.a*t.b + t.c*t.d)

/-- The two mirrored displacement effects sum to a scalar operator. -/
theorem paired_effect (t : Kernel) :
    (effect t).1 + (effect (mirror t)).1 =
       (effect t).2.1 + (effect (mirror t)).2.1 ∧
    (effect t).2.2 + (effect (mirror t)).2.2 = 0 := by
  cases t
  simp only [effect, mirror, Int.neg_mul, Int.mul_neg, Int.neg_neg, Int.mul_comm]
  constructor <;> omega

end ExactSiteIntervention
