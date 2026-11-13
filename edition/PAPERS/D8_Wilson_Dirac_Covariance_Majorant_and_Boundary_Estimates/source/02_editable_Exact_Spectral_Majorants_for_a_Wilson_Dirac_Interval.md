---
title: "Exact Spectral Majorants for a Wilson-Dirac Interval"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

## Abstract

For the negative-energy band of an infinite one-dimensional Wilson–Dirac chain, compressed to a finite interval of consecutive two-orbital cells, we construct an exact longitudinal–transverse decomposition of the difference between the massive and massless covariances. A positive Toeplitz majorant controls the longitudinal component, while the transverse component satisfies a pairing inequality in the eigenbasis of the massless reference. Direct Fourier analysis and finite Jacobi bond identities establish, at every interval length, a critical inverse-linear spectral-tail bound with explicit constants. The resulting estimates apply to the fixed-parameter mass scaling of the relative-entropy problem and establish the positive-majorant and staggered-pairing conditions required in its modular remainder analysis. We also obtain an exact finite-interval Hilbert–Schmidt majorization. The reference-modular approximation and the other asymptotic branches require separate analysis.

## 1. Covariance and reference geometry

For a dimensionless mass \(m\ge0\), let

\[
 h_m(k)=\sin k\,\sigma_x+(1+m-\cos k)\sigma_z,\qquad
 P_m(k)=\frac12\left(I-\frac{h_m(k)}{E_m(k)}\right),
\]

\[
 E_m(k)^2=m^2+4(1+m)\sin^2(k/2),\qquad -\pi<k<\pi.
\]

The multiplier \(P_m\) is an orthogonal projection for almost every momentum. Its compression to \(L\) consecutive cells defines the \(2L\times2L\) covariance \(C_{L,m}\). We use \(N=2L\), fix \(\mu>0\), and set

\[
 m=\frac\mu L,\qquad r=\frac{m}{m+2}=\frac\mu{N+\mu}\in(0,1).
\]

The on-site unitaries

\[
 W=\frac{I+i\sigma_x}{\sqrt2},\qquad
 D=\operatorname{diag}(-i,1)
\]

followed by cell staggering \((-1)^a\) give an interval-preserving unitary \(U_L\). Fourier integration of the massless symbol gives

\[
 B_N:=U_LC_{L,0}U_L^*,\qquad
 (B_N)_{ij}=\begin{cases}
 \frac12,&i=j,\\
 \displaystyle\frac{\sin[\pi(i-j)/2]}{\pi(i-j)},&i\ne j.
 \end{cases}
\]

Indeed, before staggering, the rotated massless projector has upper-right Bloch entry \(i\operatorname{sgn}(k)e^{-ik/2}/2\). In the Fourier convention above, the elementary integral

\[
\frac1{2\pi}\int_{-\pi}^{\pi}\operatorname{sgn}(k)e^{i(n+1/2)k}dk
=\frac{i}{\pi(n+1/2)}\qquad(n\in\mathbb Z)
\]

and its companion with \(n-1/2\) give the displayed coefficients after the diagonal phase transformation and staggering. The interval compression of the half-band Fourier projector obeys \(0<B_N<I\).

Define the real Jacobi matrix \(J_N\) by its off-diagonal entries

\[
 (J_N)_{j-1,j}=(J_N)_{j,j-1}=\alpha_j:=\frac{j(N-j)}{N},
 \qquad 1\le j<N,
\]

with \(\alpha_0=\alpha_N=0\). An entrywise calculation, using
\((d-1)T_{d-1}+(d+1)T_{d+1}=0\) for \(T_d=\sin(\pi d/2)/(\pi d)\), establishes \([B_N,J_N]=0\). The Jacobi matrix is irreducible, so its spectrum is simple. Hence the two reference matrices admit a common orthonormal eigenbasis.

Throughout, \(A_N=U_LC_{L,m}U_L^*\) and \(\Delta_N=A_N-B_N\). These are *compressions of the full-line band projections*, not finite-chain open-boundary ground-state projectors.

## 2. Exact longitudinal–transverse decomposition

For \(k\in(-\pi,0)\cup(0,\pi)\), write

\[
 x=\sin(k/2),\quad c=\cos(k/2),\quad
 d_r=\sqrt{x^2+r^2c^2},\quad
 u_r=\frac{|x|}{d_r},\quad a_r=\frac{rc}{d_r},\quad g_r=1-u_r.
\]

Notice \(0\le g_r\le1\) and \(u_r^2+a_r^2=1\). In the on-site \(DW\)-rotated Bloch basis, the two Hermitian involutions

\[
 Q_0(k)=\begin{pmatrix}
 0&i\operatorname{sgn}(k)e^{-ik/2}\\
 -i\operatorname{sgn}(k)e^{ik/2}&0
 \end{pmatrix},\qquad
 Q_\perp(k)=\begin{pmatrix}
 0&e^{-ik/2}\\e^{ik/2}&0
 \end{pmatrix}
\]

satisfy

\[
 Q_0^2=Q_\perp^2=I,\qquad Q_0Q_\perp+Q_\perp Q_0=0.
\]

In this basis the occupied-band involution is
\(Q_m(k):=2(DW)P_m(k)(DW)^*-I=u_rQ_0+a_rQ_\perp\). Consequently the difference of full-line projectors has the exact decomposition

\[
 P_m-P_0=\mathsf S+\mathsf D,\qquad
 \mathsf S(k)=-\frac{g_r(k)}2 Q_0(k),\quad
 \mathsf D(k)=\frac{a_r(k)}2Q_\perp(k),\quad
 \mathsf G(k)=\frac{g_r(k)}2I.
 \tag{2.1}
\]

Here the full-line objects are understood after the on-site rotation; the cell-staggering conjugation can be applied to all of them simultaneously. Fibrewise,

\[
 -\mathsf G\le\mathsf S\le\mathsf G,\quad
 [\mathsf G,Q_0]=0,\quad
 \{\mathsf D,Q_0\}=0,
 \tag{2.2}
\]

\[
 \mathsf D^2=\mathsf G-\mathsf G^2\le\mathsf G,
 \qquad
 \boxed{(P_m-P_0)^2=\mathsf G}.
 \tag{2.3}
\]

All identities hold as full-line Fourier multipliers; exceptional momentum points of measure zero do not affect the operators. Denote the interval compressions, including staggering, by \(S_N,D_N,G_N\), respectively. Then \(\Delta_N=S_N+D_N\) exactly.

**Theorem 1 (positive majorant and exact trace).** For every \(L\ge1\) and \(\mu>0\),

\[
 \boxed{-G_N\le S_N\le G_N,\qquad G_N\ge0,\qquad
 \operatorname{Tr}G_N=\frac L\pi\left(\pi-
 \frac{2\arccos r}{\sqrt{1-r^2}}\right)\le\frac\mu\pi.}
 \tag{2.4}
\]

*Proof.* Compression preserves Loewner order in (2.2). Since \(\mathsf G\) is a scalar two-orbital Fourier multiplier,

\[
 \operatorname{Tr}G_N=\frac L{2\pi}\int_{-\pi}^{\pi}g_r(k)\,dk
 =\frac L\pi\int_0^\pi g_r(k)\,dk.
\]

With \(q=k/2\), substitution \(z=\cos q\) gives

\[
 \int_0^\pi g_r(k)\,dk
 =\pi-2\int_0^1\frac{dz}{\sqrt{1-(1-r^2)z^2}}
 =\pi-\frac{2\arccos r}{\sqrt{1-r^2}}.
\]

Let \(M(r)\) denote this last expression, with \(M(0)=0\). Its derivative is

\[
 M'(r)=\frac2{1-r^2}-\frac{2r\arccos r}{(1-r^2)^{3/2}}\le2,
\]

because \(\arccos r\ge r\sqrt{1-r^2}\), equivalently \(\theta\ge\sin\theta\cos\theta\) for \(\theta=\arccos r\in[0,\pi/2]\). Thus \(M(r)\le2r\), and \(2Lr=\mu N/(N+\mu)\le\mu\). \(\square\)

**Theorem 2 (staggered pairing).** Let \(v\) be any normalized vector supported in the selected interval. Set \(b=\langle v,B_Nv\rangle\), \(q=\langle v,G_Nv\rangle\). Then

\[
 \boxed{|\langle v,D_Nv\rangle|\le2\sqrt{q\,b(1-b)}.}
 \tag{2.5}
\]

In particular this holds for every common normalized reference eigenvector of \(B_N\) and \(J_N\).

*Proof.* Work before compression with the full-line massless projector \(P_0\), transverse operator \(\mathsf D\), and commuting positive operator \(\mathsf G\). Equation (2.2) implies
\(P_0\mathsf DP_0=(I-P_0)\mathsf D(I-P_0)=0\). Write \(p=P_0v\), \(z=(I-P_0)v\), and let

\[
 X=\langle p,\mathsf Gp\rangle,\qquad
 Y=\langle z,\mathsf Gz\rangle.
\]

Because \([\mathsf G,P_0]=0\), we have \(X+Y=q\), while \(\|p\|^2=b\) and \(\|z\|^2=1-b\). Moreover,

\[
 |\langle v,\mathsf Dv\rangle|
 =2|\operatorname{Re}\langle p,\mathsf Dz\rangle|
 \le2\min\{\sqrt{X(1-b)},\sqrt{Yb}\},
\]

by Cauchy–Schwarz and \(\mathsf D^2\le\mathsf G\). For nonnegative \(X,Y\) with \(X+Y=q\),
\(\min\{X(1-b),Yb\}\le b(1-b)q\): if \(X\le bq\), use the first term; otherwise \(Y<(1-b)q\), and use the second. Since \(v\) is interval-supported, its full-line expectation equals \(\langle v,D_Nv\rangle\). \(\square\)

## 3. A uniform critical Jacobi spectral tail

Let \((\lambda_j,v_j)\) be the eigenpairs of \(J_N\), with \(\|v_j\|=1\), and define the positive measure

\[
 \nu_N:=\sum_{j=1}^{N}\langle v_j,G_Nv_j\rangle\,\delta_{|\lambda_j|}.
\]

**Theorem 3 (explicit critical tail).** For every even \(N=2L\ge2\), every \(\mu>0\), and every \(t>0\),

\[
 \boxed{\nu_N((t,\infty))\le\min\left\{
 \frac\mu\pi,
 \sqrt{\frac2{15}}\frac{\mu^2}{\pi t}
 +\frac\mu{3\pi t^2}\right\}.}
 \tag{3.1}
\]

*Proof.* The first estimate is Theorem 1. To obtain the second, express the same-parity blocks of \(G_N\) as Fourier mixtures. For \(\varepsilon\in\{0,1\}\) define the length-\(N\) vector

\[
 \phi_{k,\varepsilon}(2a+\varepsilon)=(-1)^a e^{ika},\quad
 \phi_{k,\varepsilon}(2a+1-\varepsilon)=0,\qquad 0\le a<L.
\]

The positive Toeplitz representation is

\[
 G_N=\frac12\sum_{\varepsilon=0}^1
 \int_{-\pi}^{\pi}g_r(k)
 |\phi_{k,\varepsilon}\rangle\langle\phi_{k,\varepsilon}|\,\frac{dk}{2\pi},
 \qquad \|\phi_{k,\varepsilon}\|^2=L.
 \tag{3.2}
\]

For either parity, application of \(J_N\) yields adjacent-bond differences of the form
\(\alpha_j-e^{ik}\alpha_{j+1}\), up to phases. Reflection about the centre of the interval interchanges the two parities, making their squared-norm sums identical. Direct polynomial summation gives

\[
 \frac1L\sum_{j\equiv\varepsilon\, (2)}(\alpha_j-\alpha_{j+1})^2
 =\frac{N^2-1}{3N^2},
\]

\[
 \frac4L\sum_{j\equiv\varepsilon\, (2)}\alpha_j\alpha_{j+1}
 =\frac{2(N^2-1)(N^2-4)}{15N^2},
\]

where the sums run over \(0\le j<N\), and \(\alpha_0=\alpha_N=0\). Consequently

\[
 \frac{\|J_N\phi_{k,\varepsilon}\|^2}{L}
 =\frac{N^2-1}{3N^2}
 +\frac{2(N^2-1)(N^2-4)}{15N^2}\sin^2(k/2)
 \le\frac13+\frac{N^2k^2}{30}.
 \tag{3.3}
\]

For \(\Pi_t=\mathbf1_{\{|J_N|>t\}}\), the spectral theorem implies

\[
 \|\Pi_t\phi\|^2\le\min\{\|\phi\|^2,t^{-2}\|J_N\phi\|^2\}.
\]

Substituting (3.3) into (3.2) and using the evenness of \(g_r\),

\[
 \nu_N((t,\infty))\le\frac L\pi\int_0^\pi g_r(k)
 \min\left\{1,\frac1{3t^2}+\frac{N^2k^2}{30t^2}\right\}dk.
 \tag{3.4}
\]

The elementary scalar bounds

\[
 \int_0^\pi g_r(k)\,dk\le2r,
 \qquad
 g_r(k)=1-\left[1+r^2\cot^2(k/2)\right]^{-1/2}
 \le\frac{2r^2}{k^2}\quad (0<k\le\pi)
 \tag{3.5}
\]

follow from Theorem 1, \(1-(1+x)^{-1/2}\le x/2\), and \(\tan(k/2)\ge k/2\). Set \(k_*:=\sqrt{30}\,t/N\). Bound the integrand in (3.4) by the second argument on \([0,\min(k_*,\pi)]\), and by 1 on \([k_*,\pi]\) when the latter interval is nonempty. Equation (3.5) yields, whether or not \(k_*>\pi\),

\[
 \begin{aligned}
 \nu_N((t,\infty))
 &\le\frac L\pi\left[
 \frac{2r}{3t^2}+
 \frac{N^2}{30t^2}(2r^2 k_*)+
 \frac{2r^2}{k_*}\right]\\
 &=\frac L\pi\left[\frac{2r}{3t^2}+
 \frac{4Nr^2}{\sqrt{30}\,t}\right].
 \end{aligned}
\]

Finally \(2Lr=Nr\le\mu\) and \(4LNr^2=2N^2r^2\le2\mu^2\). Since \(2/\sqrt{30}=\sqrt{2/15}\), this is exactly the second estimate in (3.1). \(\square\)

## 4. A finite compression inequality and continuum consequence

**Corollary 4 (covariance-distance domination).** At every \(L\) and \(\mu>0\),

\[
 \boxed{0\le\Delta_N^2\le G_N,\qquad
 \|A_N-B_N\|_{\mathrm{HS}}^2\le\operatorname{Tr}G_N\le\frac\mu\pi.}
 \tag{4.1}
\]

*Proof.* If \(\chi\) is the interval projection and \(T=P_m-P_0\) after the same full-line unitary, then \(T=T^*\) and \(T^2=\mathsf G\) by (2.3). The identity

\[
 \chi T^2\chi-(\chi T\chi)^2
 =\chi T(I-\chi)T\chi\ge0
\]

proves the operator inequality; take the finite trace and use Theorem 1. \(\square\)

For \(\mu\) fixed and \(L\to\infty\), the exact trace in (2.4) tends to \(\mu/\pi\), since \(g_r\) has integrated mass \(2r+O(r^2)\). Thus whenever the finite covariance differences converge in Hilbert–Schmidt norm to the continuum kernel of *Hilbert-Schmidt Scaling Limit for Wilson-Dirac Covariances*, with squared norm \(H(\mu)\), (4.1) independently yields

\[
 0\le H(\mu)\le\frac\mu\pi.
\]

There is an independent continuum verification. For the rescaled Bloch-projector difference

\[
F_\mu(t)=-\frac12\left[\left(\frac{t}{\sqrt{t^2+\mu^2}}-\operatorname{sgn}t\right)\sigma_x+
\frac{\mu}{\sqrt{t^2+\mu^2}}\sigma_z\right],
\]

one calculates \(\|F_\mu(t)\|_F^2=1-|t|/\sqrt{t^2+\mu^2}\) and therefore, by direct integration and Plancherel,

\[
\int_{\mathbb R}\|\widehat F_\mu(s)\|_F^2ds
=\frac1{2\pi}\int_{\mathbb R}\|F_\mu(t)\|_F^2dt
=\frac\mu\pi.
\]

The interval overlap formula for \(H(\mu)\) has weight \(0\le(1-|s|)_+\le1\), so the same bound follows without reference to finite-size eigenvalues.

The finite identity also identifies the trace deficit as cross-interval leakage:

\[
 \operatorname{Tr}G_N-\|\Delta_N\|_{\mathrm{HS}}^2
 =\| (I-\chi)T\chi\|_{\mathrm{HS}}^2.
\]

## 5. Consequences for the relative-entropy problem

Theorems 1–3 establish for the specified Wilson chain the Fourier splitting, positive-majorant trace bound, transverse reference-mode pairing, and critical Jacobi spectral tail. The proofs require no large-\(L\) hypothesis and remain valid for arbitrary positive \(\mu\) at each finite \(L\).

In the relative-entropy decomposition, the modular term involves \(E_N=\log(I-B_N)-\log B_N+N\eta(J_N/N)\). The “Positive weighted modular control” theorem in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, section “Global envelope and weighted consequences,” supplies a bounded longitudinal term and the variance estimate $O((\log N)/N^2)$. The entropy trace-path limit is established in *Cross-Boundary Trace-Class Estimates for Wilson–Dirac Quasifree States*, equation (B9). For the specified compressed infinite-chain Wilson model at fixed $\mu>0$, the additional convergence estimates and full constant-term expansion are established in *Finite Part of Wilson–Dirac Relative Entropy*, Theorem 1 and its proof, and sharpened in *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*, Theorem 3, Corollary 4 and Theorem 6. Their exact concentration-connection and boundary inputs remain those stated in those papers. The present paper supplies the projector, pairing, and positive-tail inputs.

## References

1. H. Araki, “On Quasifree States of CAR and Bogoliubov Automorphisms,” *Publications of the Research Institute for Mathematical Sciences* **6** (1971), 385–442. DOI: [10.2977/prims/1195193913](https://doi.org/10.2977/prims/1195193913).
2. D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty—V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430. DOI: [10.1002/j.1538-7305.1978.tb02104.x](https://doi.org/10.1002/j.1538-7305.1978.tb02104.x).
3. V. Eisler and I. Peschel, “Properties of the Entanglement Hamiltonian for Finite Free-Fermion Chains,” [arXiv:1805.00078](https://arxiv.org/abs/1805.00078) (2018).

## Acknowledgments and contributions

Kirtus Justus supplied the research program, mathematical source material, direction, and critical-review requirements and is the sole named human author. ChatGPT (OpenAI) assisted with the derivation, numerical and symbolic checks, and manuscript preparation. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for participation in the broader research workflow; no particular calculation in this paper is attributed to them without provenance. The work has not undergone external peer review, and no institution or AI provider is represented as endorsing its conclusions.
