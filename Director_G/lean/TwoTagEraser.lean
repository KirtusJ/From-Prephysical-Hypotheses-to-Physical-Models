import Std

namespace TwoTagEraser

abbrev TagColumn := Int × Int × Int × Int

def add (v w : TagColumn) : TagColumn :=
  (v.1+w.1,v.2.1+w.2.1,v.2.2.1+w.2.2.1,v.2.2.2+w.2.2.2)

def scale (k : Int) (v : TagColumn) : TagColumn :=
  (k*v.1,k*v.2.1,k*v.2.2.1,k*v.2.2.2)

def swap (v : TagColumn) : TagColumn := (v.1,v.2.2.1,v.2.1,v.2.2.2)

def initial (c d : Int) : TagColumn := (c*c, -(c*d), c*d, -(d*d))

/-- Equal-analyzer outcomes pick out the sum of the I and SWAP coefficients. -/
theorem localRead (c d a b : Int) :
    add (scale a (initial c d)) (scale b (swap (initial c d))) =
      ((a+b)*(c*c), -(a-b)*(c*d), (a-b)*(c*d), -(a+b)*(d*d)) := by
  simp only [initial, add, scale, swap, Int.add_mul, Int.sub_mul,
    Int.neg_mul, Int.mul_neg, Prod.mk.injEq]
  exact ⟨True.intro, by omega, by omega, by omega⟩

end TwoTagEraser
