Target: edition/PAPERS/G10_*/source/body.tex lines 268-335, four algebraic steps: Step 3 and the Newton step of Theorem 5.12 (thm:vsl); the finite-group fact and the square-matrix fact used in Proposition 5.14 (prop:abund). Edition Z15, commit b84056e.
Outcome: NONE FOUND (all four check in general form).
Reviewer kind: pcp-formalizer run as a sub-agent of the queue session; all four files rerun by the queue session (exit 0 each, axioms as below, no sorry / axiom / native_decide). Same model family as the author. Not independent review.

Lean 4.12.0, Mathlib v4.12.0, project files of edition/COMPUTATION/Lean/Mathlib. Command for each: `lake env lean FPHPM/<file>`. Exit code 0 for all four. Axioms printed for every theorem: propext, Classical.choice, Quot.sound.

1. VslStep3.lean (Step 3 of Theorem 5.12)
theorem MvPolynomial.eq_C_of_pderiv_X_mul_pderiv_eq_zero {R σ : Type*} [CommSemiring R]
    [CharZero R] [NoZeroDivisors R] (g : MvPolynomial σ R)
    (h : ∀ j, pderiv j (X j * pderiv j g) = 0) : g = C (coeff 0 g)
Any set of variables, any commutative semiring of characteristic zero without zero divisors. Proof by coefficients: the coefficient of a monomial m in d_j(t_j d_j g) is (m_j+1)^2 times that of m + e_j in g. Shorter than the paper's "does not depend on t_j and is divisible by t_j". Characteristic zero is needed (t^2 over Z/2 is proved to be a counterexample); the paper works over the reals.

2. VslNewton.lean (Newton step of Step 1)
theorem vsl_newton (m : ℕ) (z : Fin m → ℂ)
    (h : ∀ k, 1 ≤ k → k ≤ m → ∑ i, z i ^ k = (m : ℂ)) : ∀ i, z i = 1
and the general form: two families in a domain of characteristic zero with equal power sums of orders 1..m are equal as multisets. No shorter than the paper's appeal to Newton's identities.

3. SubmonoidFinite.lean (used in 5.14(a))
theorem one_mem_and_inv_mem_of_mul_closed_of_torsion {G : Type*} [Group G] (S : Set G)
    (hne : S.Nonempty) (hmul : ∀ x ∈ S, ∀ y ∈ S, x * y ∈ S)
    (htors : ∀ x ∈ S, IsOfFinOrder x) : (1 : G) ∈ S ∧ ∀ x ∈ S, x⁻¹ ∈ S
with the finite-group corollaries. Finite order of the elements of S suffices. Mathlib has a near-equivalent (subgroupOfIdempotent).

4. SquareIsometry.lean (used in 5.14(a) and in G9 Theorem 4.3)
theorem mul_conjTranspose_eq_smul_one' {n : Type*} [Fintype n] [DecidableEq n]
    (A : Matrix n n ℂ) (d : ℂ) (h : Aᴴ * A = d • (1 : Matrix n n ℂ)) :
    A * Aᴴ = d • (1 : Matrix n n ℂ)
Mathlib has only the unscaled Matrix.mul_eq_one_comm; this is that lemma after scaling. Squareness (finiteness of the vertex set) is essential.

Deviations from what was asked: none. Not formalized: the Nullstellensatz step, Step 2, the reduction of d_x d_xbar on functions of t to the operator of file 1, anything about digraphs.
Cost reported by the sub-agent: about 12 minutes, 8 tool calls.
