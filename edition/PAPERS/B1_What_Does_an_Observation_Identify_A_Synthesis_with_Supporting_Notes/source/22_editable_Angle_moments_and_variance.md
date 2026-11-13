# Angle moments and variance

## 2. Verified sharp purity interval with a fully specified detector

Let \(A=Z\otimes I_2\), \(B=X\otimes I_2\). Use normalized output-first Choi vectors

\[
 p=|I_4\rangle,\qquad u=|iA\rangle,\qquad v=|iB\rangle,
 \qquad |M\rangle=(M\otimes I)|\Phi_4\rangle.
\]

These vectors are orthonormal. Define

\[
\begin{aligned}
 k&=\frac{(sh-\sqrt{shq_0})^2}{sh(1-h)}=0.115482549888153\ldots,\\
 d&=s+k=0.524857549888153\ldots,\\
 r&=1-d=0.475142450111847\ldots.
\end{aligned}
\]

\(w=\sqrt{s}\,p-\sqrt{k}\,u\), \(\eta=w/\sqrt d\), and the **fixed** detector

\[
 E=|e\rangle\langle e|,\qquad e=\sqrt h\,p+\sqrt{1-h}\,u.
\]

Let \(F=|v\rangle\langle v|\) be the added, orthogonal outcome, and let \(D=I-P-|u\rangle\langle u|-F\), a rank-13 projector. The model's complete lower-endpoint phase curve, together with the known \(s,h\), fixes the compression of \(\rho\) onto \(\mathrm{span}\{p,u\}\) to \(|w\rangle\langle w|\). This **requires the complete curve**, not merely \(q_0\). Positivity then forces zero support on the orthogonal direction inside that span.

For \(f=\operatorname{Tr}(F\rho)\), \(0\le f\le r\), the sharp purity lower envelope is

\[
 \boxed{J(f)=d^2+f^2+\frac{(r-f)^2}{13}},\qquad
 \boxed{J(f)\le\operatorname{Tr}(\rho^2)\le1}.
\]

The minimum is attained by

\[
 \rho_\star(f)=|w\rangle\langle w|+fF+\frac{r-f}{13}D.
\]

It is a mixture of normalized unitary Choi vectors, hence is CPTP and unital. A pure unitary Choi state also attains the same phase curve, \(f\), and the specified product-input \(Z=+1\) probability

\[
 \boxed{p_0(f)=d+\frac{6(r-f)}{13}}.
\]

The source's construction uses a first-qubit Hermitian unitary and a second-qubit \(X\), with anticommuting Pauli terms. Its unitarity, input and output Choi marginals, and probabilities can be checked by direct \(16\times16\) multiplication. Mixing the pure state with \(\rho_\star(f)\) continuously fills \([J(f),1]\), while preserving the complete phase curve, \(f\), and \(p_0(f)\).

| \(f\) | \(J(f)\), minimum purity | \(p_0(f)\), output first-qubit \(Z=+1\) |
|---|---:|---:|
| \(0\) | 0.292841628282 | 0.744154065324 |
| \(r/14\) | 0.291601186810 | 0.728490028508 |
| \(r/2\) | 0.336257079801 | 0.634505807606 |
| \(r\) | 0.501235795573 | 0.524857549888 |

The two named endpoint Choi states have half-trace distance 0.766538917119 and optimal **state** discrimination success \((1+T)/2=0.883269458559\) at equal priors. That is discrimination of two specified normalized Choi states with a fixed input; unrestricted channel discrimination is a distinct optimization, as explained by Watrous.

## 3. Additional result: an exact purity-excess identity

**Proposition (purity projection identity).** Under the exact phase-curve and \(F\)-population assumptions of §2, every compatible density operator, with or without the Choi marginal constraint, obeys

\[
 \boxed{\operatorname{Tr}(\rho^2)=J(f)+\|\rho-\rho_\star(f)\|_2^2.}\tag{1}
\]

**Proof.** Let \(P_\eta=|\eta\rangle\langle\eta|\). The measured full phase response and positivity give

\[
 \operatorname{Tr}(P_\eta\rho)=d,\quad
 \operatorname{Tr}(F\rho)=f,\quad
 \operatorname{Tr}(D\rho)=r-f.
\]

As \(\rho_\star=dP_\eta+fF+[(r-f)/13]D\), the three fixed populations imply

\[
 \operatorname{Tr}(\rho\rho_\star)
 =d^2+f^2+\frac{(r-f)^2}{13}
 =\operatorname{Tr}(\rho_\star^2)=J(f).
\]

Expand \(\operatorname{Tr}[(\rho-\rho_\star)^2]\) and rearrange. No commutativity between \(\rho\) and \(\rho_\star\) is assumed. Equality \(\operatorname{Tr}\rho^2=J(f)\) holds exactly at \(\rho=\rho_\star\). □

This identity gives a **model-independent-within-the-specified-feasible-class** quantitative interpretation of additional measurements: deviations from the minimum-purity model are controlled by the Hilbert–Schmidt norm.

**Corollary (an additional product-input probability).** Let \(p\) be the first-qubit \(Z=+1\) probability on product input \(|00\rangle\), computed from the **same** trace-preserving channel. Then

\[
 \boxed{\operatorname{Tr}(\rho^2)\ge J(f)+\frac{13}{276}[p-p_0(f)]^2.}\tag{2}
\]

**Proof.** In the output-first normalized Choi convention the probability observable is

\[
 M=4\bigl(|0\rangle\langle0|\otimes I_2\bigr)_{\rm out}
 \otimes |00\rangle\langle00|_{\rm ref}.
\]

Let \(\theta=(\sqrt{k}\,p+\sqrt{s}\,u)/\sqrt d\). The exact phase curve forces \(\rho\theta=0\) and \(\rho_\star\theta=0\). Set \(B_\theta=I-|\theta\rangle\langle\theta|\). The Hilbert–Schmidt projection of \(B_\theta M B_\theta\) orthogonal to the three fixed-population operators \(P_\eta,F,D\) is

\[
 M_\perp=B_\theta M B_\theta-P_\eta-\frac6{13}D.
\]

Direct finite-rank identities give \(\operatorname{Tr}M^2=32\), \(\langle\theta,M\theta\rangle=1\), \(\langle\theta,M^2\theta\rangle=4\), \(\langle\eta,M\eta\rangle=1\), \(\langle v,Mv\rangle=0\), and \(\operatorname{Tr}(DM)=6\). Consequently

\[
 \|M_\perp\|_2^2=(32-8+1)-1-\frac{36}{13}=\frac{276}{13}.
\]

Since \(\rho-\rho_\star\) is orthogonal to the three fixed-population operators and supported in \(B_\theta\), Cauchy–Schwarz yields

\[
 |p-p_0(f)|=|\operatorname{Tr}[M_\perp(\rho-\rho_\star)]|
 \le\sqrt{276/13}\,\|\rho-\rho_\star\|_2.
\]

Insert (1). □

The coefficient in (2) is a **certified, generally non-sharp** lower bound. Trace-preservation and positivity can strengthen it further. When \(p=p_0(f)\), the bound correctly reduces to \(J(f)\); explicit pure and mixed channels show that equality of these rates cannot identify purity.

For finite-data intervals \(f\in F_0\), \(p\in P_0\), with the other input quantities known exactly, a valid population purity bound is obtained by minimizing the right side of (2) over \(F_0\cap[0,r]\) and \(P_0\cap[0,1]\). The input quantities themselves must be jointly calibrated and their uncertainties propagated before applying this to experiment.

## 4. Verified angle-dependent contrast and a variance refinement

The phase-calibration source studies the **general joint-density-operator class**, without imposing a Choi marginal. Its conclusions are sharp in that class. A stronger CPTP or instrument-specific conclusion needs a separate proof.

For a coherent error angle \(\varepsilon\) about the intended reflection, put \(x=\cos\varepsilon\), \(a=sh\), \(t=a-q_0\), \(d_1=s(1-h)\), and define

\[
\begin{gathered}
 b_0=(1-s)(1-h),\quad u_0=a+q_0,\quad R_0=2\sqrt{aq_0},\\
 z_0=\sqrt{4ab_0-(t+b_0)^2}=0.0852578917486220\ldots.
\end{gathered}
\]

The source proves that if the state may depend on \(\varepsilon\) but the **same fixed effect** and exactly the same \(s,h,q_0\) apply in every angle stratum, the sharp minimum contrast at a specified cosine is

\[
 m(x)=\begin{cases}
 (t+b_0)(1+x)-z_0\sqrt{1-x^2},&-1\le x\le x_1,\\
 (t+u_0)(1+x)-R_0\sqrt{2(1+x)},&x_1\le x\le1,
 \end{cases}\tag{3}
\]

where \(x_1=2[(u_0-b_0)/R_0]^2-1=0.9753069372438004\ldots\). Its branches agree with matching first derivatives. In contrast, if a *single conditional response* applies across all realized angles, the strict-increase criterion is \(1+C>\kappa|S|\), with \(\kappa=1.775489004780283\ldots\), \(C=\mathbb E\cos\varepsilon\) and \(S=\mathbb E\sin\varepsilon\).

For states depending on angle, the worst-case average with an **entire specified angle law** is \(\mathbb E m(\cos\varepsilon)\), whereas with only its first sine/cosine moments the worst case is \(m(C)\), by convexity and an attaining two-point angular distribution. The sharp strict-rise condition in this broader class is

\[
 C>\frac{\kappa^2-1}{\kappa^2+1}=0.5183463333912298\ldots.
\]

For equal +60° and −60° offsets, the source's two population calculations reproduce:

\[
 \text{shared response: }+0.064901942155\ldots,\qquad
 \text{angle-dependent states: }-0.001806421221\ldots.
\]

**Further proposition (variance-strengthened guarantee).** If the entire angle law is relevant to the same group-specifically calibrated instrument, put \(X=\cos\varepsilon\), \(C=\mathbb E X\) and \(V=\operatorname{Var}(X)\). Then

\[
 \boxed{\mathbb E[\Delta(\varepsilon)]
 \ge\mathbb E[m(X)]\ge m(C)+\frac{z_0}{2}V.}\tag{4}
\]

The constant \(z_0\) is the **largest valid global strong-convexity constant** for the specific function \(m\) in (3).

**Proof.** In the first branch,

\[
 m''(x)=\frac{z_0}{(1-x^2)^{3/2}}\ge z_0,
\]

and in the second branch,

\[
 m''(x)=\frac{R_0}{2\sqrt2(1+x)^{3/2}}\ge R_0/8
 =0.09591181732043\ldots>z_0.
\]

The first derivatives match at \(x_1\). Hence \(m(x)-(z_0/2)x^2\) is convex on \([-1,1]\). Jensen's inequality applied to that function proves the second inequality in (4); the first holds separately in every calibrated angle stratum. Because \(m''(0)=z_0\), no larger uniform curvature constant holds on the full domain. □

Equation (4) uses a **measured or otherwise independently established** distribution; it does not invent such a distribution. Its variance correction can improve a lower contrast guarantee when full angle information is available. The condition \(m(C)+(z_0/2)V>0\) is sufficient, not generally necessary, for strict positivity. This refinement does not apply if only pooled \(s,h,q_0\) are known or if the angle distribution transfers incorrectly to the gate path.
