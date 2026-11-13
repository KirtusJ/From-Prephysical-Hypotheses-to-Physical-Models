---
title: "All-Degree Jacobi Estimates and Conditional Spectral Localization"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
geometry: margin=1in
fontsize: 11pt
header-includes:
  - \usepackage{amsmath,amssymb,mathtools}
  - \usepackage{microtype}
  - \usepackage{longtable}
  - \usepackage{booktabs}
  - \setlength{\emergencystretch}{3em}
---

**Abstract.** A degree-uniform alternating-walk estimate is proved for a finite Jacobi family, without restricting polynomial degree relative to matrix size. A positive Toeplitz majorant yields a quantitative spectral-tail estimate. We derive the corresponding abstract layer-cake bound and explain the conditional logarithmic modular rate when additional Wilson-specific Coulomb and reference-eigenmode hypotheses hold. The sufficient finite-part route developed here remains conditional on its displayed moving-window hypotheses. Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy* proves the fixed-positive-scaled-mass finite part by a different route. The separate leading law with bounded remainder is established in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*.

## Model and dependency boundaries

Fix \(\mu>0\), \(N=2L\), and \(r=\mu/(N+\mu)\). The reference symmetric Jacobi matrix is \(J_N\) with off-diagonal bonds \(j(N-j)/N\), \(1\le j<N\). Define \(T_N=J_N/N\), and let \(\Delta_N=S_N+D_N\) be the scalarized difference between the compressed infinite-chain massive and massless Wilson covariances. Only the fixed reference matrices \(B_N\) and \(J_N\) commute. The covariance perturbation \(\Delta_N\) is **not** assumed to commute with either reference matrix.

For \(p=2n+1\ge 3\), the series for the comparison function is

\[
\eta(t)=\sum_{n=0}^\infty a_n t^{2n+1},\qquad
 a_n=\frac{\pi\binom{2n}{n}\binom{4n}{2n}}{(2n+1)16^n},\qquad a_0=\pi.
\]

The covariance decomposition, positive Wilson majorant, staggered pairing inequality, and Jacobi spectral-tail estimate are established for this Wilson projector in the companion *Exact Spectral Majorants for a Wilson–Dirac Interval*. The all-degree alternating-walk estimate below supplies a separate finite-Jacobi result. The global reference-mode and moving-window estimates invoked later remain additional assumptions.

## An all-odd-degree alternating-walk estimate

**Theorem (all-degree alternating-walk bound).** For every integer \(N\ge 2\) and every odd integer \(p\ge 1\), let \(T_N\) be the symmetric tridiagonal matrix with bond \(\beta_j=j(N-j)/N^2\), \(j=1,\ldots ,N-1\). Then

\[
\boxed{\displaystyle
\sum_{\substack{1\le a<N\\a\text{ odd}}}
\left|\sum_{i=0}^{N-a-1}(-1)^i(T_N^p)_{i,i+a}\right|
\le \frac{4\sqrt p\,2^{-p}}{N}. }
\tag{S1}
\]

The estimate applies also when the polynomial degree is at least the matrix dimension, and it does not require a parity restriction on the dimension.

**Proof.** For a nearest-neighbor path \(\omega=(\epsilon_1,\ldots ,\epsilon_p)\) with steps \(\epsilon_k \in \{+1,-1\}\) and positive odd net displacement, write its bond offsets as integers \(b_1,\ldots ,b_p\). Its contribution at starting site \(i\) is the zero-extended path weight

\[
 f_\omega(i)=\prod_{\ell=1}^p\beta_+\!\left(\frac{i+b_\ell}{N}\right),\qquad
\beta_+(z)=\max\{z(1-z),0\}.
\]

If the common positive support is empty, the path contributes nothing. Otherwise define the scaled real-variable product \(P(x)=\prod_{\ell=1}^p\beta_+(x+b_\ell/N)\), so that \(f_\omega(i)=P(i/N)\). Its positive support is a bounded interval \((a,b)\); \(P\) is a polynomial of degree \(2p\) on that interval, vanishes at the endpoints, and has all roots real and outside the open support. Let \(a_\ell=4 \beta_+(x+b_\ell/N) \in [0,1]\). As \(|\beta'(z)|=\sqrt{1-4 \beta(z)}\) in \((0,1)\), differentiating the product and applying Cauchy–Schwarz gives

\[
\begin{aligned}
 |P'(x)|
 &\le 4^{1-p}\sum_\ell\sqrt{1-a_\ell}
       \prod_{k\ne\ell}a_k\\
 &\le4^{1-p}\sqrt p\left[
   \sum_\ell(1-a_\ell)\prod_{k\ne\ell}a_k^2\right]^{1/2}
 \le4^{1-p}\sqrt p.
\end{aligned}
\tag{S2}
\]

The last sum is at most one because each \(a_k^2\le a_k\), and the resulting sum is a nonnegative subcollection of terms in \(\prod_k(a_k+(1-a_k))=1\).

The logarithm of \(P\) is strictly concave on its positive support (a sum of logarithms of positive linear distances to the real roots), so \(P'\) has at most one zero there. Real-root interlacing, including repeated-root multiplicities, implies \(P''\) has at most two zeros there. Consequently \(P'\) has at most three monotonic intervals and interior total variation at most \(6 \sup|P'|\). Zero extension across the two endpoints contributes at most two derivative jumps, and therefore

\[
\operatorname{TV}_{\mathbb R}(P')\le 8\sup|P'|
\le32\sqrt p\,4^{-p}.
\tag{S3}
\]

Now let \(g(y)=P(y/N)\) on the support and zero elsewhere. Its distributional second derivative is a finite signed measure, including both possible endpoint atoms. Scaling gives

\[
\|g''\|_{\rm TV}\le \frac{32\sqrt p\,4^{-p}}{N}.
\tag{S4}
\]

For **any** compactly supported continuous function \(g\) whose second distributional derivative is a finite measure, the bilateral discrete second difference obeys

\[
\Delta^2g(i)=g(i+1)-2g(i)+g(i-1)
 =\int_{\mathbb R}(1-|x-i|)_+\,g''(dx).
\tag{S5}
\]

The cardinal hat kernels satisfy the exact partition-of-unity identity \(\sum_{i\in\mathbb Z}(1-|x-i|)_+=1\) for every real \(x\). Thus

\[
\sum_i|\Delta^2g(i)|\le\|g''\|_{\rm TV}.
\]

Because \(\sum_i (-1)^i \Delta^2 g(i)=-4 \sum_i(-1)^i g(i)\), the alternating sum of **one path** is bounded by

\[
\left|\sum_i(-1)^i g(i)\right|
 \le\frac14\|g''\|_{\rm TV}
 \le\frac{8\sqrt p\,4^{-p}}{N}.
\tag{S6}
\]

For odd \(p\), exactly \(2^{p-1}\) unrestricted step sequences have positive net displacement; a step sequence with a displacement \(a\ge N\) has zero weight. Summing (S6) over this superset of contributing paths proves (S1). No operation depends on whether the power exceeds the matrix dimension. \(\square\)

**Coefficient consequence for the stated covariance decomposition.** Here $D_N^{\rm st}=D_N$ is the transverse term of the scalarized Pauli decomposition in *Exact Spectral Majorants for a Wilson–Dirac Interval*, section 2. In the fixed scalar ordering its same-parity entries vanish; for odd $a>0$ write
\[
(D_N)_{i,i+a}=\tfrac12(-1)^i d_a,\qquad d_a=2(D_N)_{0,a}.
\]
These identities follow by Fourier transforming the transverse off-orbital symbol proportional to $a_r(k)e^{\mp ik/2}$ and applying the cell staggering, where $a_r(k)=r\cos(k/2)/\sqrt{\sin^2(k/2)+r^2\cos^2(k/2)}$. In particular
\[
|d_a|\le\frac1{2\pi}\int_{-\pi}^{\pi}a_r(k)\,dk
=d_*(r):=\frac{2r}{\pi\sqrt{1-r^2}}
\operatorname{arsinh}\frac{\sqrt{1-r^2}}r.
\]
Let $a_n=\pi\binom{2n}{n}\binom{4n}{2n}/[(2n+1)16^n]$ be the coefficient of $t^{2n+1}$ in $\eta(t)$. The coefficient bound

\[
 a_n2^{-(2n+1)}\le[2\sqrt2\,n(2n+1)]^{-1}
\]

and the displayed staggered Fourier bound show, using (S1),

\[
\left|\operatorname{Tr}\{D_N^{\rm st}N T_N^{2n+1}\}\right|
\le4d_*(r)\sqrt{2n+1}\,2^{-(2n+1)},
\]

hence

\[
\boxed{\begin{aligned}
 \sum_{n\ge1}a_n\left|\operatorname{Tr}\{D_N^{\rm st}NT_N^{2n+1}\}\right|&\le\zeta(3/2)\,d_*(r),\\
 \sum_{n>K}a_n\left|\operatorname{Tr}\{D_N^{\rm st}NT_N^{2n+1}\}\right|&\le\frac{2d_*(r)}{\sqrt K}.
\end{aligned}}
\tag{S7}
\]

The covariance splitting is imported from the spectral-majorant paper; the scalar Fourier bound and its normalization have been made explicit above. Convergence to the nonlinear finite constant uses a separate all-degree argument, proved in Theorem 7 of *Finite Part of Wilson–Dirac Relative Entropy* and sharpened in Theorem 6 of *Uniform Modular Control and Nonlinear Convergence for Wilson–Dirac Intervals*.

## Positive spectral tail: recalled theorem and its algebraic prerequisite

The tail estimate below is a restatement of the critical spectral-tail theorem in *Exact Spectral Majorants for a Wilson–Dirac Interval*, section 3. The scalar derivation is included to identify the inputs to the conditional localization argument; it is not a separate theorem of priority.

Write \(G_N\) for the positive Toeplitz section of

\[
f_r(q)=\tfrac12\left(1-\frac{|\cos q|}{\sqrt{\cos^2q+r^2\sin^2q}}\right).
\]

Positivity is immediate from \(f_r\ge 0\) and the Fourier rank-one representation. With \(u_q=N^{-1/2}(1,e^{iq},\ldots ,e^{i(N-1)q})\), independent finite-sum reconstruction gives

\[
\|J_Nu_q\|^2=\underbrace{\frac{N^2-1}{3N^2}}_{\beta_N}+
\underbrace{\frac{2(N^2-1)(N^2-4)}{15N^2}}_{c_N^2}\cos^2q.
\]

For the reference spectral projector \(P_R=1_{|J_N|>R}\), use \(P_R\le J_N^2/R^2\) in the quadratic-form sense and \(P_R\le I\). The exact positive nuclear decomposition and the elementary inequality \(\min(1,a+b)\le \min(1,a)+b\) give

\[
\operatorname{Tr}(G_NP_R)\le N\int f_r(q)
 \min\!\left(1,\frac{c_N^2\cos^2q}{R^2}\right)\frac{dq}{2\pi}
 +\frac{\beta_N\operatorname{Tr}G_N}{R^2}.
\]

Rationalization of \(f_r\), the substitution \(x=|\cos q|\), and the bound

\[
H(\rho)=\int_0^1\sqrt{1-x^2}\min\{x^{-2},\rho^{-2}\}\,dx
\le2/\rho
\]

lead to the all-size estimate

\[
\boxed{\operatorname{Tr}(G_NP_R)\le
 \min\left\{\frac\mu\pi,
 \sqrt{\frac2{15}}\frac{\mu^2}{\pi R}
 +\frac\mu{3\pi R^2}\right\}.}
\tag{S8}
\]

The \(N=2\) case is handled directly because \(c_2=0\). Set \(\kappa=\sqrt{2/15}\) and \(D_\mu=(4\mu/3+\kappa \mu^2)/\pi\). Then (S8) proves, for **all** \(R>0\),

\[
\nu_N((R,\infty)):=\operatorname{Tr}(G_NP_R)\le D_\mu/R,
\tag{S9}
\]

by using the mass bound for \(R\le 1\) and the two rational terms for \(R\ge 1\). This is a proof about the **specified positive Toeplitz majorant**. Applying it to the modular correction additionally requires the exact, model-specific inequalities \(|<v_j,S_Nv_j>|\le <v_j,G_Nv_j>\) and \(|<v_j,D_N v_j>|\le 2 \sqrt{q_j b_j(1-b_j)}\), which follow for this Wilson model from the companion spectral-majorant theorem, not from scalar tail algebra alone.

## Uniform finite Coulomb gates and the logarithmic exponent

The finite reference-mode equation and its exact Liouville normal form are

\[
(p_Nu_{\sigma,N}')'=(\sigma c-\alpha_Np_N)u_{\sigma,N},\qquad
 p_N=N\sin(s/N),\quad\alpha_N=(1-N^{-2})/4,\quad c=\lambda/2,
\]

\[
\boxed{w_{\sigma,N}''+
\left(\frac14-\frac{\sigma c}{p_N}+\frac1{4p_N^2}\right)
 w_{\sigma,N}=0,\qquad w=\sqrt{p_N}\,u.}
\tag{S10}
\]

The potentially misleading \(N^{-2}\) terms cancel *exactly*; the symbolic calculation was performed afresh. For \(h=2+\lambda\), assume the uniform forbidden-arc estimate \(\int_0^{512h}u_+^2\le h^{103}\exp(2 I_N)\), whereas the allowed-arc approximation is controlled by two-sided relative errors. The finite one-sided step has the logical form

\[
U_{\sigma,N}\in[1-\delta_N(h),\ 1+\delta_N(h)+C_{\rm in}h^{103}/x],
\quad x=\log N,
\]

with \(\delta_N(h)\le 1/2\). The elementary logarithmic inequality then gives

\[
|e_j|\le \log(1+C_{\rm in}h^{103}/x)+3\delta_N(h)+C_\eta h^3/N^2.
\tag{S11}
\]

**Range restriction.** The term \(C_{\mathrm{in}} h^{103}/x\) need not be small when \(h\) approaches a fixed multiple of \(\sqrt{\log N}\). One must not replace \(\log(1+z)\) by \(O(z)\) under an *unstated smallness assumption* across this full window. The one-sided logarithmic bound is essential to the weighted argument.

For the specified matching constant \(C_0=300000\), let

\[
c_w=(2C_0)^{-1/2}=1/\sqrt{600000},\qquad
 T=\tfrac12c_w\sqrt x.
\]

On the positive-arc window \(h\le c_w \sqrt{x}\), the matching error obeys the **exact deterministic upper inequality** \(\exp(C_0 h^2)/N^2 \le \exp(-3x/2)\); the remaining errors \(h/\sqrt{N}\) and \(h^3/N^2\) also vanish uniformly as \(x\to\infty\). Hence, once model-dependent matching constant \(C_a\) and arc identity are accepted, the \(\delta\le 1/2\) and geometric gates hold eventually, with a starting size independent of the mass. This is a quantifier statement, not a practically reachable numerical cutoff.

The conventional reference-mode envelope \(|e_j|\le 800 \log(2+|\lambda_j|)\) is a **separate global hypothesis**. A finite-element eigenvalue computation cannot establish it uniformly in dimension. The published Coulomb-function and Whittaker asymptotic theories explain the appropriate type of turning-point analysis but do not prove (S11) with these Wilson-specific constants: see NIST DLMF §§13.7, 33.12, and 2.8.

## Derivation of the \(1/103\) modular rate, conditional on the reference identities

**Quantified moving-window hypotheses for this derivation.** Assume there exist finite constants $C_{\log},C_{\rm in}>0$ and an even $N_0$, independent of $N,j$, such that for every even $N\ge N_0$, with $x=\log N$ and $h_j=2+|\lambda_j|$,
\[
|e_j|\le C_{\log}\log(1+C_{\rm in}h_j^{103}/x)
\quad\text{whenever }h_j\le c_w\sqrt{x},
\qquad |e_j|\le800\log h_j\quad\text{for every }j.
\]
These are the direct spectral hypotheses used below. The preceding arc discussion motivates sufficient inputs for them; it does not establish them for this model. In particular, the error terms in (S11) must be bounded and absorbed to obtain the displayed hypothesis before (S13) can be invoked.

For any finite positive measure \(\nu\) with tail \(\nu((t,\infty))\le D/t\), and any \(\alpha>1\), Tonelli and the beta/reflection identity give

\[
\boxed{\int_0^\infty\log(1+(t/\rho)^\alpha)\,d\nu(t)
 \le\frac{\pi D}{\rho\sin(\pi/\alpha)}.}
\tag{S12}
\]

This constant is sharp within the **abstract positive-tail class**, using truncated Pareto-tail measures; it does not imply sharp Wilson asymptotics.

Divide the Wilson positive spectral weights at \(t=2\) and \(t=T=c_w \sqrt{x}/2\). On the middle interval \(2<t\le T\), use \(2+t\le 2t\), (S11), and (S12) with \(\alpha=103\) and \(\rho=x^{1/103}/(2 C_{\mathrm{in}}^{1/103})\). On the high interval, use the global \(800 \log(2+t)\) envelope and the tail bound. The resulting explicit **conditional** estimate is

\[
\begin{split}
 \operatorname{Tr}(G_N|E_N|)\le{}&
  \frac{C_{\log}C_{\rm in}4^{103}Q_\mu}{x}
 +2C_{\log} C_{\rm in}^{1/103}\pi\csc(\pi/103)\,
 D_\mu x^{-1/103}\\
 &+800D_\mu\left[
  \frac{\log(2+T)}{T}+\frac12\log(1+2/T)\right],
\end{split}
\tag{S13}
\]

where \(Q_\mu=\mu/\pi\). Therefore the positive component is \(O_\mu(x^{-1/103})\).

For the staggered part, the required occupation input is stated directly: there exist $C_V<\infty$ and an even $N_V$ such that, for every even $N\ge N_V$,
\[
\sum_j e_j^2b_j(1-b_j)\le C_V/\log N.
\]
This is sufficient together with the diagonal pairing estimate. A bound on $\operatorname{Tr}\sqrt{B_N(I-B_N)}$ alone does not imply it. The stronger $O((\log N)/N^2)$ variance estimate is supplied separately by the “Positive weighted modular control” theorem of *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, section “Global envelope and weighted consequences.” With the stated variance input, Cauchy–Schwarz gives

\[
 \operatorname{Tr}(E_N^2 B_N(I-B_N))=O(x^{-1}),
\quad |\operatorname{Tr}(D_N^{\rm st}E_N)|=O(\sqrt\mu\,x^{-1/2}).
\tag{S14}
\]

The transverse conclusion in (S14) uses precisely the displayed variance input and the model-specific pairing. The longitudinal conclusion (S13) separately requires the uniform reference-mode estimates in (S11), with errors absorbed into its stated moving-window logarithmic bound, and the global modular-error envelope. Slepian's discrete-prolate theorem identifies the common finite-dimensional eigenvectors of \(B_N\) and \(J_N\) and their spectral ordering; it does not establish these Wilson-specific quantitative estimates. Nor do the general special-function references establish them. For \(C_0=300000\), the proof's chosen sufficient gate \(T\ge 1024\) demands \(\log N \ge  2,516,582,400,000\). The formula is a mathematically asymptotic bound, **not a practically sized error certificate**.

The assembled modular correction thus has the conditional rate

\[
\mathcal F_L=\operatorname{Tr}(\Delta_N E_N)
=O_\mu((\log L)^{-1/103}).
\tag{S15}
\]

Here the implied constants are allowed to depend on **fixed** \(\mu\), while the abstract reference-mode constants and sufficiently large starting size for the modal envelope need not.

## Finite-part bounds and order of limits

The elliptic calculation uses the two-bond formula with **elliptic parameter** \(z=1-r^2\), which differs from the DLMF elliptic modulus \(k=\sqrt{z}\) (complementary modulus \(k'=r\)). It checks the expansion

\[
\mathcal P_L=\frac{\mu^2}{6}\log L
 +\mu^2\left(\frac16\log\frac8\mu-\frac14\right)
 +O_\mu\left(\frac{\log L}{L}\right).
\]

The nonlinear scalar limit remains

\[
 c_\eta=\sum_{n=1}^\infty\frac1{2n(4n+1)(4n+2)(4n+3)}
 =\frac{11}{18}-\frac\pi{12}-\frac{\log2}{2}>0,
\]

with analytic tail \(0 < c_\eta - \sum_{n=1}^K \ldots  \le 1/(384 K^3)\). Therefore the finite-part constant simplifies **exactly** to

\[
\boxed{C(\mu)=\mu^2\left(\frac{13}{36}-\frac\pi{12}-\frac{\log\mu}{6}\right).}
\]

These scalar calculations do not establish compact-uniformity of the complete relative-entropy remainder as $\mu\to0$. The conditional assembly below proves its $1/103$ conclusion only under its displayed modular hypotheses. The fixed-$\mu$ finite part also has a direct proof in Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*, with the stronger remainder $O_\mu(1/\log L)$ and without those moving-window hypotheses.

The conditional assembly has the form

\[
D_L(\mu)=\mathcal P_L+\mathcal Q_N+\mathcal F_L-\Delta S_L
\]

with rates \(O_\mu(\log L/L)\), \(O_\mu((\log L/L)^{1/3})\), \(O_\mu((\log L)^{-1/103})\), and the entropy-difference estimate \(O_\mu(1/\log L)\). When **all** separately stated assumptions hold with compatible quantifiers, the modular rate dominates and yields the claimed \(1/103\) expansion. Assembling bounds is not the same as independently proving every antecedent.



## Scope of the conditional result

The all-degree alternating-walk theorem is proved for the specified tridiagonal matrices. The positive spectral tail is proved for the specified Toeplitz majorant and is identified with the Wilson covariance in the companion spectral-majorant theorem. The inverse-logarithmic Wilson modular rate derived here additionally requires global reference-mode, occupation-number and Coulomb turning-point estimates. Neither a finite numerical sample nor a general special-function reference establishes these model-specific hypotheses. The $1/103$ implication established here remains conditional on its stated modal estimates. For the same fixed-positive-scaled-mass Wilson comparison, the finite part and an $O_\mu(1/\log L)$ remainder follow from Theorem 1 of *Finite Part of Wilson–Dirac Relative Entropy*. This does not verify the moving-window or Coulomb-matching hypotheses of the present sufficient route.

## Mathematical references

1. NIST Digital Library of Mathematical Functions, §§5.5, 5.12, 19.12 (reflection, beta and elliptic expansions), https://dlmf.nist.gov/.
2. NIST Digital Library of Mathematical Functions, §§2.8, 13.7, 33.12 (uniform turning-point and Coulomb asymptotic methods), https://dlmf.nist.gov/.
3. V. Eisler and I. Peschel, “Analytical results for the entanglement Hamiltonian of a free-fermion chain,” *Journal of Physics A* **50** (2017), 284003, doi:10.1088/1751-8121/aa76b5 (background only).
4. D. Slepian, “Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty V: The Discrete Case,” *Bell System Technical Journal* **57** (1978), 1371–1430, especially equations (14), (21), and (129)–(131), doi:10.1002/j.1538-7305.1978.tb02104.x (finite common eigenvectors and ordering only).

## AI assistance and acknowledgments

Kirtus Justus is the responsible human author. ChatGPT (OpenAI) assisted with mathematical derivations, verification programs, source comparison and manuscript preparation. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for broader research involvement, without assigning any specific present theorem to those systems absent documentation. No external review or endorsement is implied.
