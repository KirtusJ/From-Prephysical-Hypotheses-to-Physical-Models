import Std

namespace SignedSheetEcho

/-- Physical memory amplitudes on addresses zero, one and two. -/
abbrev Sheet := Int × Int × Int

def stroke (x : Sheet) : Sheet := (-x.2.2, -x.1, -x.2.1)
def add (x y : Sheet) : Sheet := (x.1+y.1, x.2.1+y.2.1, x.2.2+y.2.2)
def neg (x : Sheet) : Sheet := (-x.1, -x.2.1, -x.2.2)

/-- On any integer sheet the phase polynomial is exactly the uniform
    direction times the sum of the inputs. -/
theorem phase_residual (a b c : Int) :
    add (stroke (stroke (a,b,c))) (add (neg (stroke (a,b,c))) (a,b,c)) =
      (a+b+c, a+b+c, a+b+c) := by
  apply Prod.ext
  · simp [add, neg, stroke]; omega
  · apply Prod.ext <;> simp [add, neg, stroke] <;> omega

theorem phase_on_plane (a b c : Int) (h : a+b+c=0) :
    add (stroke (stroke (a,b,c))) (add (neg (stroke (a,b,c))) (a,b,c)) = (0,0,0) := by
  rw [phase_residual, h]

theorem sharp_routing (a b c : Int) :
    stroke (stroke (stroke (a,b,c))) = (-a,-b,-c) := by
  simp [stroke]

end SignedSheetEcho
