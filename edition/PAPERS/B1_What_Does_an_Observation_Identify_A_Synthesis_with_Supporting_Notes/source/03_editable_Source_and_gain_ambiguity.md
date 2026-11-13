# Source and gain ambiguity

## 3. gain-shift ambiguity with arbitrary common source covariance

Let L be a **connected real symmetric weighted graph Laplacian** on n *already labeled* sites, with `P0=J/n`, `Q=I-P0`, `W_s=sLe^{-sL}`. Take distinct **known** scales `0<s<t`, a **single shared** zero-mean random source x with covariance Σ strictly positive on the mean-zero subspace, and positive scalar detector gains `g_s,g_t`:

`y_s=g_s W_s x`, `y_t=g_t W_t x`.

The jointly measured covariances are

`C_st=g_s g_t W_s Σ W_t`, `C_tt=g_t² W_t Σ W_t`.

All operators W_s and W_t vanish on P0 and are invertible on Q. On Q, `C_st C_tt^+ = (g_s/g_t) W_s W_t^{-1}`, independent of the generally **noncommuting** covariance Σ. Thus

`C_st C_tt^+ = (g_s/g_t) (s/t) exp[(t-s)L]Q`.

Consequently the nominal logarithmic reconstruction without calibrated relative gain returns

`\hat L = (1/(t-s)) log[P0+(t/s) C_st C_tt^+] = L+αQ`,

where `α=log(g_s/g_t)/(t-s)`.

This is an **exact one-parameter ambiguity**, not an additive noise approximation. Unknown Σ by itself cancels for paired measurements; unknown relative gain does not. The identity fails if cross-scale observations do not share the same x, if Σ loses rank on Q, or if the readout covariances contain uncorrected independent additive detector noise.

### A conditional self-calibration that weakens the gain premise

A weighted graph Laplacian has offdiagonal entries `L_ij=-w_ij ≤ 0`. If the candidate is independently known to have **at least one absent edge** in the measured site basis, then `max_{i≠j} L_ij=0`. As `Q_ij=-1/n` for `i≠j`,

`\hat L_ij=L_ij-α/n`.

Therefore

`α=-n max_{i≠j}\hat L_ij`,

`L=\hat L-αQ`, and `g_s/g_t=exp[(t-s)α]`.

**The location of the missing edge need not be known.** If an approximate shifted generator has entrywise error at most `δ`, the extracted α has error at most `nδ`, and the final recovered generator has entrywise error at most `nδ`. This controls errors **after** the logarithmic inversion; it is not a uniform stability bound from noisy covariance measurements, whose inversion may be severely ill-conditioned. The existence of the missing edge must, however, be justified independently; otherwise the inference has simply inserted sparsity into the premises. This statement is false as unconditional graph reconstruction: for a fully connected positive-weight graph, adding a small complete-graph term generates alternative valid graph Laplacians.

### Adversarial source-and-gain transformation

For any `c>0`, `L_c=L+cQ` is a valid connected graph Laplacian adding weight `c/n` to *every* distinct pair. With

`T_c=P0 + L(L+cQ)^{-1}_Q Q`, `x'=T_c x`, `g'_s=g_s e^{sc}`,

one has exactly `g'_s W_s(L_c)x'=g_s W_s(L)x` for **all scales** and individual realizations. Hence if the source and gain laws are insufficiently calibrated, sparse and complete graphs can be observationally identical. The conditional sparsity recovery above **rejects** the complete augmentation only because its prior forbids the augmented model.

### Numerical checks

Constructed both 16-vertex rook/Shrikhande Laplacians and a nonwhite, noncommuting positive-definite Σ. Used scales `s=log2/4`, `t=.31`, gains `g_s=1.73`, `g_t=.67`. The recovered `α` is `6.93860535328…`; the exact target is `log(1.73/.67)/(.31-log2/4)`. Reconstructed each L by the independent no-missing-edge-coordinate self-calibration with entrywise errors `1.25e-13` (rook), `2.26e-13` (Shrikhande). With complete-graph augmentation `c=2.3` and transformed sources/gains, four separate filter scales agree to <`2.5e-15` in maximum matrix entry. These are floating-point corroborations of the exact formulas, not formal error bars or physical data. The test script and JSON output are retained. A separate verification program constructs both graphs, enumerates all induced three-port types and four-cliques, compares noncommuting three-port control sequences, and verifies an exact π-flux four-cycle caging identity. All assertions pass locally, with three-port controlled response difference `7.33e-16`, Krylov ranks `7` in both chosen triangle-port experiments, and π-flux opposite-corner transfer below `6.1e-17`.

**Prior art boundary:** blind graph deconvolution, spectrum/graph learning from structured signals, and system-identification similarity classes are established fields (e.g. Hammond et al. 2011; Ramírez et al. 2017; Burgarth and Yuasa 2014). These conditional formulas are a working synthesis and do not establish publication novelty.

## 4. Operational readout of full commutation: a simple robustness calculation

Let A and B be Pauli observables with `A²=B²=I`. After a projective measurement of B, apply `U(θ)=exp(iθA)`, then measure B again. Let b,b' be the consecutive ideal outcomes. For commuting A,B, `E[bb']=1`. For anticommuting A,B, `E[bb']=cos(2θ)`. At θ=π/2 they are +1 and -1, respectively, irrespective of the state. This distinguishes the two models without interpreting a global -I phase as an observable by itself.

Under the **specific** error model in which the two recorded bits are independently flipped with probability `e`, and θ=`π/2+δ`, the observed contrast is

`Δ_corr=2(1-2e)² cos² δ`.

Thus a simple instrument noise model retains a finite discrimination signal whenever `e<1/2` and `|δ|<π/2`. This is not a guarantee for arbitrary invasive/nonprojective measurements, source drift, or pulse crosstalk. For `e=.08`, `δ=.07`, the predicted contrast is `1.40429640693`, checked by full two-qubit matrices. The required B in the dressed model is itself a nonlocal Pauli string under the original site interpretation, so access to its projective measurement is a substantial operational input.

If a faithful state `ρ` on dimension d has known smallest eigenvalue `r>0`, then `Tr[ρ C†C] ≥ r ||C||_op²` for `C=[A,B]`. A measured small commutator *mean-square* controls an operator-norm cross-commutator only with this faithfulness bound. The weaker expected commutator `Tr(ρ[A,B])≈0` does not provide it. If `r=0` or scales to zero with d, no uniform operator-level guarantee follows.
