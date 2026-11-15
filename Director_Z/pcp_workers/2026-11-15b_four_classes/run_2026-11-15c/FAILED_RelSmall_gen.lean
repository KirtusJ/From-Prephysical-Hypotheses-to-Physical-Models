import Mathlib

theorem rel_s4_m0 (R : Type*) [CommRing R] (x : R) (h : x^4 = -1) :
    (1:R)*((-2+(1)*x)^1*(2+(1)*x)^1*(-5+(6)*x)^1*(5+(6)*x)^1) = (-1:R)*((-8+(13)*x)^1*(8+(13)*x)^1) := by
  linear_combination (36) * h
#print axioms rel_s4_m0

theorem rel_s4_m1 (R : Type*) [CommRing R] (x : R) (h : x^4 = -1) :
    (1:R)*((-3+(1)*x)^1*(2+(3)*x)^1*(-3+(7)*x)^1) = (1:R)*((-1+(1)*x)^1*(1+(1)*x)^1*(2+(1)*x)^1*(-19+(20)*x)^1) := by
  linear_combination (-20) * h
#print axioms rel_s4_m1

theorem rel_s6_m0 (R : Type*) [CommRing R] (x : R) (h : x^6 = -1) :
    (1:R)*((1+(1)*x)^1*(8+(1)*x)^1*(4+(5)*x)^1*(-1+(6)*x)^1*(-15+(11)*x)^1*(-13+(14)*x)^1) = (1:R)*((-1+(1)*x)^1*(6+(1)*x)^1*(-5+(4)*x)^1*(-1+(8)*x)^1*(14+(13)*x)^1*(11+(15)*x)^1) := by
  linear_combination (-1620) * h
#print axioms rel_s6_m0

theorem rel_s6_m1 (R : Type*) [CommRing R] (x : R) (h : x^6 = -1) :
    (1:R)*((1+(1)*x)^1*(1+(2)*x)^1*(-8+(3)*x)^1*(-5+(4)*x)^1*(3+(5)*x)^1*(-26+(23)*x)^1) = (1:R)*((-2+(1)*x)^1*(-1+(1)*x)^1*(-5+(3)*x)^1*(4+(5)*x)^1*(3+(8)*x)^1*(23+(26)*x)^1) := by
  linear_combination (-360) * h
#print axioms rel_s6_m1

theorem rel_s5_m0 (R : Type*) [CommRing R] (x : R) (h : x^5 = -1) :
    (31:R)*((-1+(1)*x)^1*(7+(2)*x)^1*(-2+(3)*x)^1*(3+(5)*x)^1) = (-1:R)*((2+(1)*x)^1*(1+(2)*x)^1*(-7+(3)*x)^1*(-3+(7)*x)^1*(-19+(12)*x)^1) := by
  linear_combination (504) * h
#print axioms rel_s5_m0

theorem rel_s5_m1 (R : Type*) [CommRing R] (x : R) (h : x^5 = -1) :
    (1:R)*((-29+(1)*x)^1*(-3+(2)*x)^1*(4+(3)*x)^1*(-12+(7)*x)^1) = (-1:R)*((2+(1)*x)^1*(-1+(2)*x)^1*(1+(2)*x)^1*(-2+(3)*x)^1*(1+(3)*x)^1*(-1+(4)*x)^1*(-5+(14)*x)^1) := by
  linear_combination (2016*X^2 + 2136*X - 4156) * h
#print axioms rel_s5_m1

