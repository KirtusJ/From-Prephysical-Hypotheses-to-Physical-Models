# Angular contrast and rounding

## 1. Quantum model, notation and sufficient two-dimensional reduction

Let `P=|p><p|` be a rank-one projector and `R=I−P` on the specified joint-probe Hilbert space. Let `ρ` be a normalized state and `0≤E≤I` a *common* binary effect, with

\[
 s=\mathrm{Tr}(P\rho)=\frac{131}{320},\qquad h=\mathrm{Tr}(EP)=\frac{99}{100},\qquad
 q=q(0)=\frac{81711338569043}{224995905216000}.
\]

For the phase family `U_φ=P+e^{iφ}R`, write `q(φ)=Tr(E U_φ ρ U_φ†)`. Put

\[
 a=sh,\quad d=s(1-h),\quad t=a-q>0,\quad
 b=\mathrm{Tr}(E R\rho R),\quad c=\mathrm{Tr}(E P\rho R),\quad z=2\operatorname{Im}c.
\]

The ordinary readout fixes `Re c=−(t+b)/2`. Positivity of `E` and `I−E` gives

\[
 |c|^2\le\min\{ab,\ d(1-s-b)\},\qquad 0\le b\le 1-s.
\]

These conditions are **sufficient**, not just necessary, because every admissible pair `(b,c)` is realized by the pure state `|ψ>=√s|p>+√(1−s)|u>` and the two-dimensional effect

\[
 E_{b,c}=\begin{pmatrix}
 h & \overline c/\sqrt{s(1-s)}\\
 c/\sqrt{s(1-s)} & b/(1-s)
 \end{pmatrix},
\]

embedded in the joint-probe space. Both determinant conditions for `E` and `I−E` are precisely the inequalities above. Their joint feasible set is convex.

Equivalently, the allowed `(b,z)` are the intersection of two disks:

\[
 (b-C_1)^2+z^2\le R_1^2,\quad (b-C_2)^2+z^2\le R_2^2,
\]
\[
 C_1=a+q,\ R_1=2\sqrt{aq},\quad
 C_2=-(t+2d),\ R_2=2\sqrt{d(1-q)}.
\]

They meet at `b₀=(1−s)(1−h)` and `z=±z₀`, with

\[
 z_0=\sqrt{4ab_0-(t+b_0)^2},\qquad
 \kappa=\frac{z_0}{t+b_0}=1.77548900478028319584\ldots.
\]

## 2. Sharp **two-sided** contrast for a deterministic coherent offset

Let the intended relative phase be `π`; assume that its **only** error is a coherent offset `±δ` in the very same family `U_φ`, with the **same** `ρ`, `E` and `P` in both arms. Then, upon choosing the adverse sign of the imaginary interference,

\[
 \Delta(\delta):=q(\pi\pm\delta)-q(0)
 =A(t+b)-Bz,\qquad A=1+\cos\delta,\quad B=\sin\delta
\]

for `0≤δ≤π` (the signs are interchangeable because `z` can take either sign). Set `H=√(A²+B²)=2cos(δ/2)`.

**Sharp minimum.** Let

\[
 \delta_1=2\arccos[(C_1-b_0)/R_1]=12.7591826805379687\ldots^\circ.
\]

For `0≤δ≤δ₁`, the supporting point of the first disk is feasible for both, giving

\[
 \Delta_{\min}(\delta)=A(t+C_1)-R_1H
 =4a\cos^2(\delta/2)-4\sqrt{aq}\cos(\delta/2).
\]

For `δ₁≤δ≤δ_c` the supporting point would leave the disk intersection; the minimum is at its shared upper point `(b₀,z₀)`:

\[
 \Delta_{\min}(\delta)=A(t+b_0)-Bz_0.
\]

Its zero occurs sharply at

\[
 \delta_c=2\arctan(1/\kappa)=58.77860795856966018\ldots^\circ.
\]

Every compatible state/effect yields strictly positive contrast for `|δ|<δ_c`. At `δ_c` an admissible two-dimensional **projective** effect gives zero, so this is an open condition.

**New sharp upper endpoint.** On the same full interval `0≤δ≤δ_c`, maximizing the contrast over the *second* disk gives the simultaneously attainable bound

\[
 \boxed{\displaystyle
 \Delta_{\max}(\delta)=A(t+C_2)+R_2H
 =4\sqrt{d(1-q)}\cos(\delta/2)-4d\cos^2(\delta/2).}
\]

Its supporting point is

\[
 (b,z)=\left(C_2+R_2\frac A H,\ -R_2\frac B H\right).
\]

This point belongs to the first disk whenever `b≥b₀`. For the supplied inputs it remains feasible through `δ=113.20968269065858...°`, well beyond `δ_c`. The upper formula therefore holds throughout the guaranteed-positive interval. The constructed two-dimensional `E_{b,c}` has `0≤E≤I` and attains the rate. The image of the convex disk intersection under the linear contrast is a full interval, so **every intermediate contrast is attainable** as well.

| Offset | Sharp lower increase (percentage points) | Sharp upper increase (percentage points) |
|---:|---:|---:|
| 0° | 8.653592287309 | 18.786135457214 |
| 10° | 8.006123191762 | 18.720856010456 |
| 20° | 6.398293220245 | 18.525231209691 |
| 30° | 4.697644815950 | 18.199908655488 |
| 45° | 2.168778595748 | 17.471285101295 |
| 55° | 0.572299788190 | 16.827620196169 |
| 58° | 0.116299082295 | 16.610292664719 |

These are percentages of theoretical binary *probabilities*, not percentages measured on devices. The decimal entries in this table are rounded descriptions, not lower/upper decimal certificates. The companion verifier emits **downward-rounded lower certificates** for `Δ_min` separately.

## 3. Sharp calibration criterion for an independently varying phase offset

Suppose one fixed pre-phase conditional `ρ` and one fixed `E` apply to all trials in this comparison, and the distribution of actual offsets `ε` is transferable to that same response independently of hidden state/effect changes. Define the *population* moments

\[
 C=\mathbb E\cos\varepsilon,\qquad S=\mathbb E\sin\varepsilon,
\qquad C^2+S^2\le1.
\]

No values of these moments are assumed known from experiment. Averaging the fixed response gives exactly

\[
 \overline\Delta=(1+C)(t+b)-S z.
\]

Put `A=1+C`, `B=|S|`, `H=√(A²+B²)` and `b_* = C₁−R₁ A/H` when `H>0`. The **sharp minimum** over all state/effect pairs compatible with the three supplied population inputs is

\[
 \boxed{\displaystyle
 M(C,S)=\begin{cases}
 A(t+C_1)-R_1H, & b_*\le b_0,\\
 A(t+b_0)-Bz_0, & b_*>b_0.
 \end{cases}}
\]

If `A=B=0` (the phase is reversed relative to the intended reflection with probability one), take `M=0`. The proof is the same supporting-line optimization over the two-disk intersection, and both branches are attainable.

The exact **strict sign criterion** is

\[
 \boxed{1+C>\kappa|S|.}
\]

Necessity as well as sufficiency follows because `max z/(t+b)=κ` at the disk intersection, and `t+b>0` throughout the feasible set. In the symmetric case `S=0` the sharp lower contrast simplifies to

\[
 \boxed{M(C,0)=\frac{1+C}{2}\;4(a-\sqrt{aq}).}
\]

Simultaneous, independently justified confidence bounds `C≥C_L` and `|S|≤S_U` therefore give the sufficient physical sign criterion `1+C_L>κ S_U` *only when* the common-state/effect and transfer hypotheses have been independently established. The rectangular bound can be conservative if it includes moment pairs that no phase distribution can realize.

**Nontransfer control.** Two hidden conditional subpopulations can have the same `s,h,q` but opposite imaginary interference coefficients. If positive and negative angle errors are systematically correlated with these subpopulations, their pooled error histogram can have `S=0` while both arms have the adverse response. At the sign boundary their average contrast can be zero. Thus an unlabelled marginal angle histogram is **not** evidence for the independent-transfer condition, and may not be inserted into `M(C,S)` without justification.
