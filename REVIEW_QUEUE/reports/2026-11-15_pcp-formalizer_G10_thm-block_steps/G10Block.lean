import Mathlib

theorem control_g10 : ∀ n : ℕ, 2 ^ n ≥ n + 1 := by
  intro n; induction n with
  | zero => simp
  | succ n ih => rw [pow_succ]; omega

/-- (a) General form: on any abelian group `G`, a real function whose threefold
differences all vanish is `f 0 + ℓ x + b x x / 2` with `ℓ` additive and `b`
symmetric biadditive. No divisibility on `G` is needed. -/
theorem third_diff_quadratic {G : Type*} [AddCommGroup G] (f : G → ℝ)
    (H : ∀ a h k l : G, f (a+h+k+l) - f (a+h+k) - f (a+h+l) - f (a+k+l)
        + f (a+h) + f (a+k) + f (a+l) - f a = 0) :
    ∃ (ℓ : G → ℝ) (b : G → G → ℝ),
      (∀ x y, ℓ (x+y) = ℓ x + ℓ y) ∧
      (∀ x y z, b (x+y) z = b x z + b y z) ∧
      (∀ x y, b x y = b y x) ∧
      (∀ x, f x = f 0 + ℓ x + b x x / 2) := by
  set b : G → G → ℝ := fun h k => f (h+k) - f h - f k + f 0 with hb
  have bsymm : ∀ x y, b x y = b y x := by intro x y; simp only [hb, add_comm x y]; ring
  have badd : ∀ x y z, b (x+y) z = b x z + b y z := by
    intro x y z; have := H 0 x y z; simp only [zero_add] at this; simp only [hb]; linarith
  have badd2 : ∀ x y z, b z (x+y) = b z x + b z y := by
    intro x y z; rw [bsymm, badd, bsymm x, bsymm y]
  refine ⟨fun x => f x - f 0 - b x x / 2, b, ?_, badd, bsymm, ?_⟩
  · intro x y
    have e1 : b (x+y) (x+y) = b x x + b x y + (b y x + b y y) := by rw [badd, badd2, badd2]
    simp only []; rw [e1, ← bsymm x y]; linarith
  · intro x; ring

/-- (a) on cosets: if threefold differences with steps in `d • G` vanish, then on
each coset `c + d • G` the function is quadratic in the coset parameter. -/
theorem third_diff_coset {G : Type*} [AddCommGroup G] (f : G → ℝ) (d : ℕ)
    (H : ∀ a h k l : G, f (a + d•h + d•k + d•l) - f (a + d•h + d•k) - f (a + d•h + d•l)
        - f (a + d•k + d•l) + f (a + d•h) + f (a + d•k) + f (a + d•l) - f a = 0)
    (c : G) :
    ∃ (ℓ : G → ℝ) (b : G → G → ℝ),
      (∀ x y, ℓ (x+y) = ℓ x + ℓ y) ∧
      (∀ x y z, b (x+y) z = b x z + b y z) ∧
      (∀ x y, b x y = b y x) ∧
      (∀ x, f (c + d•x) = f c + ℓ x + b x x / 2) := by
  have := third_diff_quadratic (fun x => f (c + d•x)) (by
    intro a h k l; simp only [smul_add, ← add_assoc]; exact H _ h k l)
  simpa using this

/-- (b) The maximum argument, general form. -/
theorem max_arg {C : Type*} [Fintype C] (m : C → ℝ) (hm : ∀ c, 0 ≤ m c) (d : ℕ)
    (hd : 2 ≤ d)
    (H : ∀ c, ∃ σ : Fin d → C, (d:ℝ)^2 * m c ≤ ∑ z, m (σ z)) : ∀ c, m c = 0 := by
  intro c0
  obtain ⟨cs, -, hcs⟩ := Finset.exists_max_image Finset.univ m ⟨c0, Finset.mem_univ _⟩
  obtain ⟨σ, hσ⟩ := H cs
  have hle : ∑ z, m (σ z) ≤ d * m cs := by
    calc ∑ z, m (σ z) ≤ ∑ _z : Fin d, m cs :=
          Finset.sum_le_sum (fun z _ => hcs _ (Finset.mem_univ _))
      _ = d * m cs := by simp
  have hd' : (2:ℝ) ≤ d := by exact_mod_cast hd
  have h0 : m cs ≤ 0 := by
    by_contra hpos; push_neg at hpos
    have hp : (0:ℝ) < d * (d - 1) := by nlinarith
    nlinarith [mul_pos hp hpos]
  have := hcs c0 (Finset.mem_univ _); linarith [hm c0]

/-- Degree zero: `∑_z κ(c'_z) = d^2 κ(c)` for the constant vector of cosets. -/
theorem deg_zero {C : Type*} [Fintype C] (κ : C → ℝ) (d : ℕ) (hd : 2 ≤ d)
    (H : ∀ c, ∃ σ : Fin d → C, ∑ z, κ (σ z) = (d:ℝ)^2 * κ c) : κ = 0 := by
  funext c
  have := max_arg (fun c => |κ c|) (fun _ => abs_nonneg _) d hd (by
    intro c; obtain ⟨σ, hσ⟩ := H c; refine ⟨σ, ?_⟩
    calc (d:ℝ)^2 * |κ c| = |∑ z, κ (σ z)| := by rw [hσ, abs_mul]; simp
      _ ≤ ∑ z, |κ (σ z)| := Finset.abs_sum_le_sum_abs _ _) c
  simpa using this

/-- Degree one: `‖ℓ'‖^2 = d ‖ℓ‖^2` (from `Tᵀ ℓ' = d ℓ`, `T = √d U`) with
`ℓ = (ℓ_c,…,ℓ_c)`, i.e. `∑_z ‖ℓ(c'_z)‖^2 = d^2 ‖ℓ_c‖^2`, in any normed group. -/
theorem deg_one {C E : Type*} [Fintype C] [NormedAddCommGroup E] (ℓ : C → E) (d : ℕ)
    (hd : 2 ≤ d)
    (H : ∀ c, ∃ σ : Fin d → C, ∑ z, ‖ℓ (σ z)‖^2 = (d:ℝ)^2 * ‖ℓ c‖^2) : ℓ = 0 := by
  funext c
  have := max_arg (fun c => ‖ℓ c‖^2) (fun _ => sq_nonneg _) d hd
    (fun c => (H c).imp fun σ h => h.ge) c
  simpa using this

#print axioms control_g10
#print axioms third_diff_coset
#print axioms deg_zero
#print axioms deg_one
