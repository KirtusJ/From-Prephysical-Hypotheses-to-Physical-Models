import Mathlib

/-! Vanishing-sum law certificates (valid for every real f on an abelian group with the stated symmetries). -/

/-- Triangle + pair, u = (1, w, w², 1, -1), w³ = 1.  Certificate: 4/5 V(b,-a) - 1/5 V(b,wa) + 2/5 V(b,w²a) - 3/5 V(b,-w²a). -/
theorem vsl_triangle_pair {G : Type*} [AddCommGroup G] (w : G →+ G)
    (hw3 : ∀ x, w (w (w x)) = x) (f : G → ℝ)
    (hfw : ∀ x, f (w x) = f x) (hfneg : ∀ x, f (-x) = f x)
    (hV : ∀ x y, 2 * f (x + y) + f (x + w y) + f (x + w (w y)) + f (x - y) = 5 * f x + 5 * f y) :
    ∀ a b, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have h1 := hV b (-a)
  have h2 := hV b (w a)
  have h3 := hV b (w (w a))
  have h4 := hV b (-(w (w a)))
  simp only [map_neg, hw3, hfw, hfneg, sub_neg_eq_add, ← sub_eq_add_neg] at h1 h2 h3 h4
  have e1 : f (b - a) = f (a - b) := by rw [← hfneg (b - a)]; congr 1; abel
  have e2 : f (b + a) = f (a + b) := by rw [add_comm]
  rw [e1, e2] at h1
  rw [e2] at h2 h3
  rw [e1] at h4
  linarith

/-- u = (1,-1,1,-1,i,-i).  Certificate: 2/3 V(b,-a) - 1/3 V(b,-ia). -/
theorem vsl_pairs_211 {G : Type*} [AddCommGroup G] (J : G →+ G)
    (hJ : ∀ x, J (J x) = -x) (f : G → ℝ)
    (hfJ : ∀ x, f (J x) = f x) (hfneg : ∀ x, f (-x) = f x)
    (hV : ∀ x y, 2 * f (x + y) + 2 * f (x - y) + f (x + J y) + f (x - J y) = 6 * f x + 6 * f y) :
    ∀ a b, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have h1 := hV b (-a)
  have h2 := hV b (-(J a))
  simp only [map_neg, hJ, hfJ, hfneg, sub_neg_eq_add, neg_neg, ← sub_eq_add_neg] at h1 h2
  have e1 : f (b - a) = f (a - b) := by rw [← hfneg (b - a)]; congr 1; abel
  have e2 : f (b + a) = f (a + b) := by rw [add_comm]
  rw [e1, e2] at h1 h2
  linarith

/-- Two pairs u = (1,-1,w,-w), w of order 3.  D(a,b) + D(a,wb) = 0 for all b, three times. -/
theorem vsl_two_pairs_odd {G : Type*} [AddCommGroup G] (w : G →+ G)
    (hw3 : ∀ x, w (w (w x)) = x) (f : G → ℝ)
    (hfw : ∀ x, f (w x) = f x)
    (hV : ∀ x y, f (x + y) + f (x - y) + f (x + w y) + f (x - w y) = 4 * f x + 4 * f y) :
    ∀ a b, f (a + b) + f (a - b) = 2 * f a + 2 * f b := by
  intro a b
  have h1 := hV a b
  have h2 := hV a (w b)
  have h3 := hV a (w (w b))
  simp only [hw3, hfw] at h1 h2 h3
  linarith

#print axioms vsl_triangle_pair
#print axioms vsl_pairs_211
#print axioms vsl_two_pairs_odd
