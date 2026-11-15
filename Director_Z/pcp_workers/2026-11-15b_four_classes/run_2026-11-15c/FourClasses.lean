import Mathlib
/-- Remark (b) pair as a polynomial identity: X(7+X)(1+X)^2 - (1+3X)^2(1+X) = X^4 - 1. -/
theorem four_pair (R : Type*) [CommRing R] (x : R) :
    x*(7+x)*(1+x)^2 - (1+3*x)^2*(1+x) = x^4 - 1 := by ring
/-- |p+qz|^2 for z*zi = 1 is p^2+q^2+pq(z+zi). -/
theorem absq (R : Type*) [CommRing R] (z zi p q : R) (h : z*zi = 1) :
    (p+q*z)*(p+q*zi) = p^2+q^2+p*q*(z+zi) := by linear_combination q^2*h
/-- h0 of the pair, in w = z + 1/z: -2 (w^3 - 4w). -/
theorem four_h0 (R : Type*) [CommRing R] (w : R) :
    (50+7*w)*(2+w)^2 - (10+3*w)^2*(2+w) = -2*(w^3-4*w) := by ring
/-- the same, from z with z*zi=1 directly. -/
theorem four_h0z (R : Type*) [CommRing R] (z zi : R) (h : z*zi = 1) :
    ((7+z)*(7+zi))*((1+z)*(1+zi))^2 - ((1+3*z)*(1+3*zi))^2*((1+z)*(1+zi))
      = -2*((z+zi)^3-4*(z+zi)) := by
  have h1 := absq R z zi 7 1 h
  have h2 := absq R z zi 1 1 h
  have h3 := absq R z zi 1 3 h
  simp only [one_mul] at h1 h2 h3
  rw [h1, h2, h3]; ring
#print axioms four_pair
#print axioms absq
#print axioms four_h0
#print axioms four_h0z
