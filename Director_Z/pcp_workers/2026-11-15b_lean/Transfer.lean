import Mathlib
/-!
T2. The scalar-transfer step of thm:fgprod(ii).
Two factors. For each factor a point is (n, x): n the count |P|, x in V the vector of the
quadratic monomials of p (V = R^3 in the paper).  The part of g that is under discussion is
  g(n1,x1,n2,x2) = a n1 n2 + n1 * b x2 + n2 * b' x1 + d x1 x2,   b, b' linear, d bilinear.
Transfer by A in M(C_0): (n, x) -> (|A| n, eps_0(A)^2 x) on either factor gives the same value.
Two A with the same s = eps_0(A)^2 and different counts tau, tau' are used.
-/

theorem transfer_core {V : Type*} [AddCommGroup V] [Module ℝ V]
    (a : ℝ) (b b' : V →ₗ[ℝ] ℝ) (d : V →ₗ[ℝ] V →ₗ[ℝ] ℝ)
    (τ τ' s : ℝ) (hτ : τ ≠ τ') (n1 n2 : ℝ) (x1 x2 : V)
    (h : ∀ u ∈ ({τ, τ'} : Set ℝ),
      a * (u * n1) * n2 + (u * n1) * b x2 + n2 * b' (s • x1) + d (s • x1) x2
        = a * n1 * (u * n2) + n1 * b (s • x2) + (u * n2) * b' x1 + d x1 (s • x2)) :
    n1 * b x2 = n2 * b' x1 := by
  have h1 := h τ (by simp)
  have h2 := h τ' (by simp)
  simp only [map_smul, smul_eq_mul, LinearMap.smul_apply] at h1 h2
  have : (τ - τ') * (n1 * b x2 - n2 * b' x1) = 0 := by linear_combination h1 - h2
  rcases mul_eq_zero.mp this with h | h
  · exact absurd (sub_eq_zero.mp h) hτ
  · linarith

/-- With a set S of points (n, x) that occur, containing a point (n0, 0) with n0 ≠ 0:
    b and b' vanish at every x that occurs. -/
theorem transfer_vanish {V : Type*} [AddCommGroup V] [Module ℝ V]
    (a : ℝ) (b b' : V →ₗ[ℝ] ℝ) (d : V →ₗ[ℝ] V →ₗ[ℝ] ℝ)
    (τ τ' s : ℝ) (hτ : τ ≠ τ') (S : Set (ℝ × V)) (n0 : ℝ) (hn0 : n0 ≠ 0) (h0 : (n0, (0:V)) ∈ S)
    (h : ∀ P1 ∈ S, ∀ P2 ∈ S, ∀ u ∈ ({τ, τ'} : Set ℝ),
      a * (u * P1.1) * P2.1 + (u * P1.1) * b P2.2 + P2.1 * b' (s • P1.2) + d (s • P1.2) P2.2
        = a * P1.1 * (u * P2.1) + P1.1 * b (s • P2.2) + (u * P2.1) * b' P1.2
          + d P1.2 (s • P2.2)) :
    ∀ P ∈ S, b P.2 = 0 ∧ b' P.2 = 0 := by
  intro P hP
  have e1 := transfer_core a b b' d τ τ' s hτ n0 P.1 0 P.2 (h _ h0 _ hP)
  have e2 := transfer_core a b b' d τ τ' s hτ P.1 n0 P.2 0 (h _ hP _ h0)
  simp only [map_zero, mul_zero] at e1 e2
  constructor
  · rcases mul_eq_zero.mp e1 with h | h
    · exact absurd h hn0
    · exact h
  · rcases mul_eq_zero.mp e2.symm with h | h
    · exact absurd h hn0
    · exact h

/-- If moreover the x that occur span V, then b = b' = 0. -/
theorem transfer_zero {V : Type*} [AddCommGroup V] [Module ℝ V]
    (a : ℝ) (b b' : V →ₗ[ℝ] ℝ) (d : V →ₗ[ℝ] V →ₗ[ℝ] ℝ)
    (τ τ' s : ℝ) (hτ : τ ≠ τ') (S : Set (ℝ × V)) (n0 : ℝ) (hn0 : n0 ≠ 0) (h0 : (n0, (0:V)) ∈ S)
    (hspan : Submodule.span ℝ (Prod.snd '' S) = ⊤)
    (h : ∀ P1 ∈ S, ∀ P2 ∈ S, ∀ u ∈ ({τ, τ'} : Set ℝ),
      a * (u * P1.1) * P2.1 + (u * P1.1) * b P2.2 + P2.1 * b' (s • P1.2) + d (s • P1.2) P2.2
        = a * P1.1 * (u * P2.1) + P1.1 * b (s • P2.2) + (u * P2.1) * b' P1.2
          + d P1.2 (s • P2.2)) :
    b = 0 ∧ b' = 0 := by
  have key := transfer_vanish a b b' d τ τ' s hτ S n0 hn0 h0 h
  constructor
  · apply LinearMap.ext_on hspan
    rintro _ ⟨P, hP, rfl⟩
    simpa using (key P hP).1
  · apply LinearMap.ext_on hspan
    rintro _ ⟨P, hP, rfl⟩
    simpa using (key P hP).2

#print axioms transfer_core
#print axioms transfer_vanish
#print axioms transfer_zero
