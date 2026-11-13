Target: edition/PAPERS/G10_*/source/body.tex, the convexity step of Theorem 5.2 (thm:power), at commit e53742c.
Outcome: NONE FOUND (the step checks; the formal proof is shorter than the paper's).
Reviewer kind: pcp-formalizer, served by the queue session; same model family as the author. Not independent review.

File: PowerSumConvexity.lean in the folder of this name. Lean 4.12.0, Mathlib v4.12.0, in a copy of the project files of edition/COMPUTATION/Lean/Mathlib (lakefile, toolchain, manifest), cache from `lake exe cache get`.
Command: `lake env lean FPHPM/PowerSumConvexity.lean`. Exit code 0. One linter warning (unused variable). No sorry, no axiom, no native_decide.
Axioms printed for all three theorems: propext, Classical.choice, Quot.sound.

Statement proved (copied):

theorem power_sum_eq_iff {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (t : ι → ℝ)
    (ht : ∀ i ∈ s, 0 ≤ t i) (h2 : ∑ i ∈ s, t i ^ 2 = 2 * (s.card : ℝ))
    (p : ℝ) (hp : 0 < p) :
    ∑ i ∈ s, t i ^ p = 2 * (s.card : ℝ) ↔ p = 2

Also proved: for 0 < p <= 2, sum t^p <= (1 + p/2) m; for p >= 2, sum t^p >= (1 + p/2) m (m the number of terms).

Deviation from the paper's statement
- More general: any finite non-empty family of reals t >= 0 with sum t^2 = 2m. The paper's t_z = |1+u_z| with |u_z| = 1 and sum u_z = 0 is used only through sum t_z^2 = 2m. That reduction (h(2) = 2m) is not formalized here.
- The bounds proved have m in place of the paper's h0 (the number of non-zero t_z); they are the paper's bounds at h0 = m, which is the case the paper's strict inequalities use.
- Real powers are Mathlib's rpow, for which 0^p = 0 when p > 0, as in the paper.

Shorter argument: the paper uses convexity of h on (0, infinity) and its limit h0 at 0. The formal proof needs neither. Termwise, for t >= 0: t^p <= (1 - p/2) + (p/2) t^2 for 0 < p <= 2, and t^2 <= (1 - 2/p) + (2/p) t^p for p >= 2 (weighted arithmetic-geometric mean of 1 and t^2, respectively 1 and t^p). Summing gives h(p) <= (1 + p/2) m < 2m for p < 2 and h(p) >= (1 + p/2) m > 2m for p > 2.

Not checked: nothing about digraphs, walks or events is formalized. The first attempt at the third theorem did not check (a field_simp goal left open); it was repaired before this report and only the checking file is delivered.
