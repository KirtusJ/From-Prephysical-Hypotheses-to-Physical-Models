# Four-phase response

## 1. Inherited observation law and verified reflection bound

The source four-use comparison has ideal single-use rate \(s=131/320\), and the final reported-one probability after the *previously reported* history \(111\) is

\[
q_\star=\frac{81711338569043}{224995905216000}
=0.36316811406233676725\ldots.
\]

The conditional history has probability
\[
\Pr(W=111)=\frac{284760442539}{4096000000000}=0.069521592416\ldots.
\]
These are probabilities in a supplied mathematical population law, not observations.

Fix a rank-one projector \(P\) on a complex Hilbert space \(\mathcal H\) of dimension at least two, a state \(\rho\geq0\) of trace one, and an effect \(0\leq E\leq I\). Set
\[
s=\operatorname{Tr}(P\rho),\quad h=\operatorname{Tr}(EP),\quad
U_\pi=2P-I,\quad q_0=\operatorname{Tr}(E\rho),\quad
q_\pi=\operatorname{Tr}(EU_\pi\rho U_\pi^\dagger).
\]
The Hilbert–Schmidt triangle inequality gives
\[
\sqrt{q_0}+\sqrt{q_\pi}\geq2\sqrt{sh}.
\]
Indeed, writing \(A=\sqrt E\sqrt\rho\) and \(B=\sqrt E U_\pi\sqrt\rho\), their squared Hilbert–Schmidt norms are \(q_0,q_\pi\), and \(A+B=2\sqrt E P\sqrt\rho\) has squared norm \(4sh\).

At \(h=99/100\), this gives
\[
q_\pi\geq\bigl(2\sqrt{sh}-\sqrt{q_\star}\bigr)^2
=0.44970403693542629849\ldots,
\]
which is at least \(0.08653592287308953124\ldots\) greater than the supplied \(q_\star\). This is a sharp *population* inequality under the common-state, common-effect and exact-operation premises.

An equality witness uses a two-dimensional subspace with
\[
|\psi\rangle=\sqrt s\,|0\rangle+\sqrt{1-s}\,|1\rangle,
\quad\rho=|\psi\rangle\langle\psi|,
\quad E=\begin{pmatrix}h&-\sqrt{h e}\\-\sqrt{h e}&e\end{pmatrix},
\]
where
\[
e=\frac{(\sqrt{sh}-\sqrt{q_\star})^2}{1-s}
=0.00195526010392640486\ldots.
\]
The matrix is positive semidefinite with eigenvalues \(0\) and \(h+e=0.9919552601\ldots<1\). The state is pure and positive. Direct substitution gives \(q_0=q_\star\) and \(q_\pi\) equal to the sharp lower bound. It is an algebraic witness, not a claim of a laboratory state.

The ideal unitary–depolarizing mixture \(\rho_0=0.37P+0.63I/16\), and more generally any \(\rho\) block diagonal with respect to \(P\oplus(I-P)\), obey \(\rho\ge sP\), so \(q_0\ge sh\) and \(q_\pi=q_0\). At \(h=0.99\), the target \(q_\star<sh=0.40528125\) already contradicts this block-diagonal null. Allowing coherent off-diagonal blocks evades the single-arm bound, but not the reflected-arm inequality.

## 2. New exact four-phase feasibility criterion

Let \(R=I-P\), and for phases \(\phi\in\{0,\pi/2,\pi,3\pi/2\}\) define
\[
U_\phi=P+e^{i\phi}R,\qquad
q_\phi=\operatorname{Tr}(EU_\phi\rho U_\phi^\dagger).
\]
Here \(0<s<1\), \(0\le h\le1\), and **the same** \(\rho,E\) are used in all four arms. The operation is a relative phase between a specified rank-one *joint match sector* and its full orthogonal complement.

**Proposition (sharp four-phase feasibility).** Four proposed probabilities \(q_0,q_{\pi/2},q_\pi,q_{3\pi/2}\) arise from such a state, effect and phase family if and only if the following hold. Put
\[
a=sh,\quad
\bar q=\frac{q_0+q_\pi}{2},\quad
b=\bar q-a,\quad
c=\frac{q_0-q_\pi}{4}+i\frac{q_{\pi/2}-q_{3\pi/2}}{4}.
\]
Then
\[
\boxed{q_0+q_\pi=q_{\pi/2}+q_{3\pi/2},}\tag{F1}
\]
\[
\boxed{0\le b\le1-s,}\tag{F2}
\]
\[
\boxed{|c|^2\le\min\bigl\{sh\,b,\,s(1-h)[(1-s)-b]\bigr\}.}\tag{F3}
\]
The theorem is unchanged if \(\mathcal H\) has dimension greater than two. The conditions themselves imply that all four probabilities belong to \([0,1]\), because of the constructive realization below.

**Proof of necessity.** Put \(b=\operatorname{Tr}(ER\rho R)\ge0\), and \(c=\operatorname{Tr}(EP\rho R)\). Directly expanding \(U_\phi\rho U_\phi^\dagger\) yields
\[
q_\phi=sh+b+2\operatorname{Re}(e^{-i\phi}c).
\]
Hence (F1) and \(b\le\operatorname{Tr}(R\rho)=1-s\). Hilbert–Schmidt Cauchy–Schwarz applied to the diagonal and cross terms gives \(|c|^2\le (sh)b\). Applying the same argument to \(I-E\), whose off-diagonal trace term equals \(-c\), gives \(|c|^2\le s(1-h)[(1-s)-b]\). Together these prove (F2)–(F3).

**Proof of sufficiency and sharpness.** Take a two-dimensional space spanned by \(|0\rangle,|1\rangle\), set \(P=|0\rangle\langle0|\), and choose the pure state
\[
\rho=|\psi\rangle\langle\psi|,\qquad
|\psi\rangle=\sqrt s\,|0\rangle+\sqrt{1-s}\,|1\rangle.
\]
Define
\[
E=\begin{pmatrix}
 h&\bar c/\sqrt{s(1-s)}\\
 c/\sqrt{s(1-s)}& b/(1-s)
\end{pmatrix}.
\]
The determinant conditions for \(E\ge0\) and \(I-E\ge0\) are exactly the two inequalities in (F3), while the diagonal bounds follow from (F2) and \(0\le h\le1\). Therefore \(0\le E\le I\). Direct evaluation produces all four prescribed \(q_\phi\), using (F1). This constructs a realization for every feasible quartet and proves the criterion is both necessary and sufficient. \(\square\)

This is an elementary finite-dimensional quantum feasibility result derived from standard effect positivity. **No claim of novelty relative to existing quantum-detector tomography and testing-region theory is made.**

**Corollary (sharp phase-contrast ceiling).** Maximizing (F3) over \(b\) gives
\[
|q_0-q_\pi|\le4\sqrt{s(1-s)h(1-h)}.
\]
The bound is attained by a pure two-dimensional state and a rank-one projective effect (at \(b=(1-s)(1-h)\)). At the inherited \(s\) and \(h=0.99\), its numerical value is \(0.19570150261303565\ldots\). It bounds the contrast but does not predict its sign.

**What phase cycling identifies.** The ideal four response probabilities identify only \(\bar q\) and the real and imaginary parts of \(c\), for fixed \(s,h\). They do not identify a unique state or measurement effect. In particular every admissible response admits a two-dimensional *pure-state* explanation, so these data alone cannot force a mixed-state interpretation. Conversely a flat response need not mean \(\rho\) is block diagonal: the effect may be phase-blind, or the accessible interference product \(c\) may vanish.

## 3. Application, feasibility margins, and negative controls

For the sharp two-arm witness in Section 1, \(c\) is negative and real and the four **illustrative witness** probabilities are

| Ideal phase arm | An attaining witness (not a universal prediction) |
|---|---:|
| \(0\) | 0.36316811406233677… |
| \(\pi/2\) | 0.40643607549888153… |
| \(\pi\) | 0.44970403693542630… |
| \(3\pi/2\) | 0.40643607549888153… |

They satisfy (F1) and saturate the first disk constraint (F3). A different compatible coherent model may yield different quarter-phase rates or a higher reflected-arm rate. **The original four-report probability table contains no experimental responses at the added phase settings.**

If an idealized experiment measured \(q_0=q_\pi=q_\star\), while \(s=0.409375\) and \(h=0.99\) remained valid, then the two-arm inequality would be violated. With fixed, perfectly known population rates, a reflected-arm allowance \(\delta+\tau\ge0.08653592287\ldots\) would be needed to erase that particular discrepancy if all of the allowance were applied to the reflected arm. Finite-shot uncertainty in \(q_0,q_\pi,s,h\) and other systematic uncertainties can close the gap sooner. This number is **not** a tolerated hardware error budget by itself.

For a conservative finite-data test, construct simultaneous lower limits \(s_L,h_L\), upper limits \(U_0,U_\pi\), and independently justified bounds \(\delta\) on the reflected state deviation in half-trace distance and \(\tau\) on the difference between arm effects in operator norm. The strict condition
\[
\sqrt{U_0}+\sqrt{\min(1,U_\pi+\delta+\tau)}<2\sqrt{s_Lh_L}
\]
is sufficient to reject the joint calibrated model. It is not a mechanism-specific identification of state coherence, gate error, or detector drift. If more phases are measured, one can test whether any quartet inside their simultaneous confidence intervals and systematic allowances satisfies (F1)–(F3); numerical infeasibility needs an independently justified enclosure when a rigorous decision is required.

Two matched negative controls are especially important:

1. **Pure reference:** \(U_\phi P U_\phi^\dagger=P\) at every phase. Phase-dependent reference click rates therefore reveal a failure of the common-state/effect/operation idealization, although phase-independent rates do not prove it.
2. **Verified block-diagonal mixture:** \(U_\phi\rho_0 U_\phi^\dagger=\rho_0\). Its phase response should be flat. A nonflat response in this control detects some setting-dependent errors or preparation departures, without uniquely assigning their origin.

In a real experiment the phase arm should be chosen only after the preceding reported history has been committed, using a choice isolated from the state source and detector. Each arm needs an adequately populated held-out sample, a declared sampling design, and valid cross-record conditional guarantees. Postselection on history \(111\) does not automatically deliver a fresh ideal bit or erase apparatus memory. The phase operations here are joint operations on the target/reference probe: local one-qubit phase rotations are **not generally equivalent** to \(P+e^{i\phi}(I-P)\).
