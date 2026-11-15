import Mathlib
open Finset Matrix

/-- Control: (a+b)^2 = a^2+b^2 fails for a = b = 1. -/
theorem control_refuted : ¬ ∀ a b : ℤ, (a + b) ^ 2 = a ^ 2 + b ^ 2 := by
  intro h; have := h 1 1; norm_num at this

namespace FPHPM.VertexStep3

/-- Core of Step 3 of thm:vertexlaw, abstracted: any field `K`, finite vertex type `V`,
predecessor relation `P z y` (`y ∈ pred z`), weights `u v r` that vanish off arcs and with
`u, v` nonzero on arcs, `d ≠ 0`, the identity (eq:vtri), and the conclusion of
lem:maxp(2)+(b) as hypothesis `hW`. Then `f = 0`. -/
theorem step3_core {K V : Type*} [Field K] [Fintype V] [DecidableEq V]
    (P : V → V → Prop) (u v r : V → V → K) (f : V → K) (d : K) (hd : d ≠ 0)
    (hu : ∀ y z, P z y → u y z ≠ 0) (hv : ∀ y z, P z y → v y z ≠ 0)
    (hvtri : ∀ y y' y'', ∑ z, u y z * v y' z * r y'' z * f z
        = if y = y' ∧ y = y'' then d * f y else 0)
    (hW : f ≠ 0 → ∃ z, f z ≠ 0 ∧ ∃ y y', y ≠ y' ∧ P z y ∧ P z y') :
    f = 0 := by
  by_contra hf
  obtain ⟨z0, hz0, y, y', hyy, hy, hy'⟩ := hW hf
  classical
  let R := {z : V // f z ≠ 0}
  have sumR : ∀ w : V → K, (∀ z, f z = 0 → w z = 0) →
      ∑ z : R, w z.1 = ∑ z, w z := by
    intro w hw
    rw [← Finset.sum_subtype (Finset.univ.filter fun z => f z ≠ 0) (by simp)]
    exact Finset.sum_filter_of_ne (fun z _ h => by by_contra h'; exact h (hw z h'))
  let M : Matrix R R K := fun η z => u η.1 z.1 * v η.1 z.1 * f z.1
  let A : Matrix R R K := fun z w => r w.1 z.1
  have hMA : M * A = d • Matrix.diagonal (fun η : R => f η.1) := by
    ext η w
    simp only [M, A, Matrix.mul_apply, Matrix.smul_apply, Matrix.diagonal_apply, smul_eq_mul]
    have := hvtri η.1 η.1 w.1
    rw [sumR (fun z => u η.1 z * v η.1 z * f z * r w.1 z) (by intro z hz; simp [hz])]
    have e : ∀ z, u η.1 z * v η.1 z * f z * r w.1 z = u η.1 z * v η.1 z * r w.1 z * f z :=
      fun z => by ring
    simp only [e, this, Subtype.ext_iff]
    by_cases h : η = w
    · subst h; simp
    · have h' : ¬ (η.1 = w.1) := fun e => h (Subtype.ext e)
      simp [h, h']
  have hdet : IsUnit A.det := by
    have h1 := congrArg Matrix.det hMA
    rw [det_mul, det_smul, det_diagonal] at h1
    have : M.det * A.det ≠ 0 := by
      rw [h1]; exact mul_ne_zero (pow_ne_zero _ hd) (Finset.prod_ne_zero_iff.2 fun i _ => i.2)
    exact isUnit_iff_ne_zero.2 (right_ne_zero_of_mul this)
  let g : R → K := fun z => u y z.1 * v y' z.1 * f z.1
  have hg : Matrix.vecMul g A = 0 := by
    ext w
    simp only [Matrix.vecMul, Matrix.dotProduct, g, A, Pi.zero_apply]
    rw [sumR (fun z => u y z * v y' z * f z * r w.1 z) (by intro z hz; simp [hz])]
    have := hvtri y y' w.1
    simp only [hyy, false_and, if_false] at this
    calc _ = ∑ z, u y z * v y' z * r w.1 z * f z := Finset.sum_congr rfl fun z _ => by ring
      _ = 0 := this
  have := congrFun (Matrix.eq_zero_of_vecMul_eq_zero hdet.ne_zero hg) ⟨z0, hz0⟩
  simp only [g, Pi.zero_apply] at this
  exact mul_ne_zero (mul_ne_zero (hu y z0 hy) (hv y' z0 hy')) hz0 this

/-- The induction of Step 3, abstracted: `G n` is "the family vanishes on all multisets of
size n". If it holds for n ≤ 2 and the inductive step holds for every N ≥ 3, it holds for all n. -/
theorem step3_induction (G : ℕ → Prop) (h2 : ∀ n ≤ 2, G n)
    (hstep : ∀ N ≥ 3, (∀ n < N, G n) → G N) : ∀ n, G n := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih => by_cases hn : n ≤ 2
              · exact h2 n hn
              · exact hstep n (by omega) ih

/-- Whole Step 3 in abstract form: a family `φ N z p` (value of the linear functional
`φ_z` on spanning element `p` of degree `N`) such that, for each `N ≥ 3` and each `p`, once all
lower degrees vanish the vector `z ↦ φ N z p` satisfies (eq:vtri) for data `u v r d` and
the maxp conclusion; then all `φ` vanish. -/
theorem step3_whole {K V ι : Type*} [Field K] [Fintype V] [DecidableEq V]
    (P : V → V → Prop) (d : K) (hd : d ≠ 0) (φ : ℕ → V → ι → K)
    (h2 : ∀ n ≤ 2, ∀ z p, φ n z p = 0)
    (data : ∀ N ≥ 3, (∀ n < N, ∀ z p, φ n z p = 0) → ∀ p : ι,
      ∃ u v r : V → V → K, (∀ y z, P z y → u y z ≠ 0) ∧ (∀ y z, P z y → v y z ≠ 0) ∧
        (∀ y y' y'', ∑ z, u y z * v y' z * r y'' z * φ N z p
          = if y = y' ∧ y = y'' then d * φ N y p else 0) ∧
        ((fun z => φ N z p) ≠ 0 → ∃ z, φ N z p ≠ 0 ∧ ∃ y y', y ≠ y' ∧ P z y ∧ P z y')) :
    ∀ n z p, φ n z p = 0 := by
  have := step3_induction (fun n => ∀ z p, φ n z p = 0) h2 (by
    intro N hN ih z p
    obtain ⟨u, v, r, hu, hv, ht, hW⟩ := data N hN ih p
    exact congrFun (step3_core P u v r (fun z => φ N z p) d hd hu hv ht hW) z)
  exact fun n z p => this n z p

end FPHPM.VertexStep3
#print axioms control_refuted
#print axioms FPHPM.VertexStep3.step3_core
#print axioms FPHPM.VertexStep3.step3_whole
