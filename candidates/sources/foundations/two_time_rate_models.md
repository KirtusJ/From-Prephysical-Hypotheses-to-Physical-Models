# A12-C16: two-time model adequacy for the unknown-rate generator benchmark

## Scientific and provenance scope

This is a **conditional, finite four-state classical/diagonal-GKSL** research checkpoint, not a theory of physical Foundations of R. It preserves A12-C15 Unknown-Rate as an immutable historical source. Physical R is **`UNSELECTED`**; the physical ontology and continuum obligations remain `OPEN`. The previously published statistical theory is not overridden. A distinct A12-C15 auxiliary-coherence branch must not be merged into this one.

We fix the C15 model, including the *same preparations* `e0` and `E(e0)` and the same block-sign measurement `H`, and ask whether independent observations at calibrated times can **falsify** that model. We do not claim a passing test proves the model, or that mathematical time is physical time.

### 1. Identifiable rates versus a testable family

Under the time-homogeneous candidate `G_{s,δ}=s G_δ`, with `0.8≤s≤1.2`, `0≤δ≤1/4`, and time input `t`, the parent derivation establishes the restricted mean and contrast

\[
h_s(t)=-1+\frac87(1-e^{-0.7st}),\qquad F_{s,\delta}(t)=\frac{2\delta}{0.3+\delta}\left(e^{-0.7st}-e^{-(1+\delta)st}\right).
\]

The nonrestricted mean is `g(t)=h_s(t)+F_{s,δ}(t)`. The original single-time two-arm experiment fits `s` and `δ` (when model assumptions hold); it leaves no independent scalar overidentification check within those two mean readings.

Take `t1=τ>0`, `t2=2τ`, with specified calibrated ratio 2. Write

\[
q_i=1-\frac78(h(t_i)+1).
\]

**Exact two-time restriction** for the homogeneous family:

\[
\boxed{q_2=q_1^2}\qquad\text{for all permitted }s,\delta.
\]

Indeed `q_i=e^{-0.7 s t_i}`. This identity does not determine the absolute timescale: replacing `(s,τ)` by `(s/c,cτ)` leaves all predicted observations unchanged when only their product is known. The time ratio must be externally specified; it cannot be learned from this identity without circularity.

### 2. Finite-shot test with explicit false-rejection control

At each time make **independent preparations and independent shots** of the restricted input, measuring `H∈{-1,+1}` exactly `m` times per time. Denote the sample means by `\widehat h_i`. Put

\[
\widehat q_i=\Pi_{[0,1]}\left[1-\frac78(\widehat h_i+1)\right],\quad
\widehat T=\widehat q_2-\widehat q_1^2,
\quad R_m=\frac{21}{8}\sqrt{\frac{2\log(4/\alpha)}m}.
\]

**Certified level-α null test**: reject homogeneity within the C15 family if `|\widehat T|>R_m`.

Proof. Hoeffding's bound for each `[-1,+1]` sample mean gives `P(|\widehat h_i-h_i|>r)≤2e^{-mr²/2}`. At `r=\sqrt{2\log(4/\alpha)/m}`, the union probability for the two times is ≤α. On the complementary event, nonexpansiveness of clipping yields `|\widehat q_i-q_i|≤(7/8)r`. For `q_i,\widehat q_i∈[0,1]`,

\[
|\widehat T-(q_2-q_1^2)|≤\frac78r+2\frac78r=R_m.
\]

Under the homogeneous null, `T=0`, so `P_H0(reject)≤α`. Under a specified alternative with true absolute residual `D=|q_2-q_1²|`, **power is at least `1-α` when `D>2R_m`**. This is a conservative sufficient sample budget, not a minimax sample bound or a statement about every alternative.

### 3. Exact piecewise rate-drift counterexample

Retain the valid generator `G_δ` and fixed `δ=0.15`, but apply `s(t)=s1` over `[0,τ]` and `s(t)=s2` over `(τ,2τ]`, with `s1=0.8,s2=1.2,τ=0.9`. At every time the instantaneous `s(t)G_δ` is a valid rate generator of the stipulated scaled type, but the overall evolution is **not homogeneous**. As the generators commute,

\[
U(\tau)=e^{s_1\tau G_\delta},\qquad
U(2\tau)=e^{(s_1+s_2)\tau G_\delta}.
\]

Hence

\[
q_1=e^{-0.7 s_1\tau},\quad q_2=e^{-0.7(s_1+s_2)\tau},\quad
\boxed{T=q_1^2\bigl(e^{-0.7(s_2-s_1)\tau}-1\bigr)}.
\]

For the specified values, 60-digit Decimal evaluation gives

`T = -0.081294119954723351170815494199290227784056213349762383510798`.

At 95% nominal confidence `m=36,552` shots **per restricted-time setting** is sufficient for `D>2R_m` in this example. The sufficient-budget theorem does not presuppose that a high observed statistical rejection rate proves a physical mechanism. Unlike the original C15 confidence intervals, the test can detect this explicit *family misspecification*.

### 4. Full two-time model-membership equations

Write `h_i` and `g_i` for the population means, with contrasts `f_i=g_i-h_i`. Set `w=q_1`, `x=-\log w/0.7=s\tau` (if `0<w<1`). Under the homogeneous null,

\[
q_2=w^2,\qquad f_1=F(x,\delta),\quad f_2=F(2x,\delta).
\]

When `f_1>0`, the factorization

\[
f_2=f_1\left(w+e^{-(1+\delta)x}\right)
\]

provides the exact candidate `v=f_2/f_1-w` and `\delta=-\log(v)/x-1`. The observed four means are **consistent with the stated null family if and only if** all the equations, positivity conditions `w>0,v>0`, bounds on `s` and `δ`, the required amplitude identity `f_1=2\delta(w-v)/(0.3+\delta)`, and the `q_2` equation hold. If `f_1=0`, consistency requires `f_2=0` and `δ=0`. These are population-level algebraic conditions, **not numerically stable finite-shot ratio estimators** near `δ=0`.

For four independently sampled arms (two preparations at each of two times), a conservative confidence-set test is also available: let `r=\sqrt{2\log(8/\alpha)/m}` for `m` shots per arm. Form the set of parameter pairs in the declared compact rectangle whose four predicted means all lie within `r` of the four observed sample means. Reject the whole family **only if this set is provably empty**. Under a correct null, probability of false rejection is ≤α. A mere numerical minimizer failing to find a point is not proof of emptiness; verified interval covering or analytical exclusion is required. Passing merely means **not rejected**.

### 5. A distinct misspecification invisible to the restricted-only test

If the overall rate `s` is fixed but `δ` changes randomly between independent runs, the *restricted* response remains exactly `h_s(t)` for every time and the statistic `T` is always zero. Let `δ` have a nondegenerate distribution supported on `[0,1/4]`. The averaged nonrestricted contrast is `\overline F(x)=\mathbb E[F(x,δ)]`. Its small-`x` expansion is

\[
\overline F(x)=2\overline\delta\,x-
\left(1.7\overline\delta+\mathbb E\delta^2\right)x^2+O(x^3).
\]

Any single fixed `δ_*` agreeing with this averaged contrast **for all x near 0** must have `δ_*=\overline\delta` from its first derivative, but then its second coefficient differs by `\mathrm{Var}(\delta)>0`. Hence no homogeneous single-`δ` family fits all such times. This does not show every chosen finite time pair must distinguish every mixture. For the illustrative equal mixture of `δ=0` and `δ=1/4` with `s=1`, independent SciPy root inversion at `τ=.9` fits `δ_*=0.11831433644848688`, but predicts the `2τ` contrast with residual `-0.003861032773808684` (a numerical diagnostic, not an exact interval-arithmetic certificate).

### 6. Limits / logical disposition

- **Rejecting** the exact homogeneous model is a conclusion about the tested conditional family and sampling model, **not proof** of rate drift, a specific replacement generator, non-Markovianity, or physical R.
- **Non-rejection** does not demonstrate time homogeneity, identify the unrestricted generator, or validate unmeasured preparations or time points.
- The null criterion assumes independent binary shots and calibrated observation-time ratio, well-prepared two inputs, correct block-sign observable, and absence of unaccounted readout bias/drift. A time-dependent bias can imitate a nonzero `T`.
- The homogeneous model's calibrated absolute time remains separate from the purely mathematical semigroup parameter; the latter is *not* emergent physical time.
- Physical R `UNSELECTED`; source theory, covariance, localization, regulators, relative entropy and modular/D3-HSMI topics remain OPEN.

## Mathematical literature / priority caveat

The continuation applies standard exponential semigroup algebra, Hoeffding's inequality and parametric goodness-of-fit inversion. Not a novelty claim. External record checks (2026-10-19): Hoeffding (1963), *Probability inequalities for sums of bounded random variables*, JASA 58:13–30, DOI `10.1080/01621459.1963.10500830`; Kong & Ye (2017), *Goodness-of-fit tests in the multi-state Markov model*, Reliability Engineering & System Safety 166:16–24, DOI `10.1016/j.ress.2017.02.010`; De Stavola (1988), *Testing Departures from Time Homogeneity in Multistate Markov Processes*, JRSS C 37:242–250, DOI `10.2307/2347343`. These works provide context, not peer review of C16.
