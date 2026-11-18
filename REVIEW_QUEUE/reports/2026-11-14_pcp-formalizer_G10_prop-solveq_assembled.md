Target: edition/PAPERS/G10_*/source/body.tex lines 876-921, Proposition 5.35 (prop:solveq), edition Z26, commit 4ad1dec; and edition/COMPUTATION/Lean/Mathlib/OneGain.lean. Wanted by the director: assemble the proposition from the thirteen checked steps.
Control (known answer, set by the queue session): decide in Lean whether x <= x^2 holds for all real x. Expected: refuted. The sub-agent delivered a checking proof of the negation with x = 1/2. Control passed.
Outcome: NONE FOUND. The proposition is assembled in full as one Lean theorem for every q >= 1; no hypothesis is missing from the paper's statement. The formal proof is shorter than the paper's.
Reviewer kind: pcp-formalizer run as a sub-agent of the queue session; both files rerun by the queue session (exit 0, standard axioms, no sorry / axiom / native_decide), and the definitions compared with the paper's. Same model family as the author. Not independent review.

Lean 4.12.0, Mathlib v4.12.0. Command: `lake env lean FPHPM/<file>`. SolveQAssembled.lean (549 lines): exit 0; axioms of the main theorem: propext, Classical.choice, Quot.sound. Control.lean: exit 0.

Definitions in the file: C is ZMod q written additively, with h = 1; (T W)(g) = W(g - 1), which is the paper's (Tm)(g) = m(g h^-1); size m = |m| as a real number; eps m = sum over g of (-1)^(g.val) m(g), the paper's epsilon; Solves FR FL means both vanish at 0 and the equation holds for all U, V.

Statement proved (copied):

theorem prop_solveq {q : ℕ} [NeZero q] :
    (∀ FR FL : (ZMod q → ℕ) → ℝ, FR 0 = 0 → FL 0 = 0 →
      (∀ U V, FR (U + V) + FL (U + T V) = 2 * FR U + 2 * FL V) →
        FR = FL ∧
        (¬ 2 ∣ q → ∀ m, FR m = FR 1 / q * size m) ∧
        (2 ∣ q → ∀ m, FR m = FR 1 / q * size m
            + (FR (Pi.single 0 1) - FR 1 / q) * (eps m : ℝ) ^ 2)) ∧
    (∀ a : ℝ, Solves (q := q) (fun m => a * size m) (fun m => a * size m)) ∧
    (2 ∣ q → ∀ a c : ℝ, Solves (q := q) (fun m => a * size m + c * (eps m : ℝ) ^ 2)
        (fun m => a * size m + c * (eps m : ℝ) ^ 2)) ∧
    (∀ a a' : ℝ, (∀ m : ZMod q → ℕ, a * size m = a' * size m) → a = a') ∧
    (2 ∣ q → ∀ a c a' c' : ℝ, (∀ m : ZMod q → ℕ, a * size m + c * (eps m : ℝ) ^ 2
        = a' * size m + c' * (eps m : ℝ) ^ 2) → a = a' ∧ c = c')

Deviations from the paper's statement
- The dimension is stated as "the parameters a, respectively (a, c), are determined by the function", not as a dimension of a vector space. With the direct part and the converse this gives dimension 1 and 2.
- The converse for a|m| is proved for every q, not only for odd q.

On the existing file OneGain.lean (rerun unedited: exit 0, output identical to the stored OneGain.out)
- It holds thirteen theorems. Only eleven have a line printing their axioms; sum_T and sign_sub_one are not printed.
- Steps of the paper's proof with no counterpart among the thirteen: Steps 1, 2 and 3; the coset reductions in Steps 5 and 6; Gamma(1,1) = 0 (taken as a hypothesis by one of the thirteen); a = F(1)/q; the independence of |m| and epsilon^2.
- Of the thirteen only A_nat (with A_general), sum_T and sign_sub_one are used by the assembly; B, C, D_size, D_alt are not, and the converse is proved again on multisets with natural counts. Six new lemmas were written (swap, normal, natSolve, chi_eq, eps_T, eps_one).

Shorter argument found by the formal proof: Steps 2 and 3 of the paper (subtracting a|m| and extending to Z^C) are not needed. For q odd, Step 4 on N^C gives F(m) = phi(|m|) with phi additive on N, so F(m) = |m| F(e_1), and a = F(1)/q follows. For q even, Phi(P,Q) = F(P e_1 + Q e_h) satisfies the two-variable equation on N^2, which is solved there directly as a(P+Q) + c(P-Q)^2, and epsilon(1) = 0 identifies a.
The hypothesis F_R(0) = F_L(0) = 0 is needed: the constants F_R = -d, F_L = d satisfy the equation (checked by hand by the sub-agent and by the queue session; not in Lean).

Rechecked by the queue session: both files rerun; the copy of OneGain.lean is byte-identical to the edition's; T, a and c in the Lean statement agree with lines 878 and 894-900 of the paper; the constant counterexample.
Not formalized: Lemma 5.34 (the preparation), Theorem 5.36, anything about walks or events.
Cost reported by the sub-agent: about 9 minutes, 5 tool calls.
