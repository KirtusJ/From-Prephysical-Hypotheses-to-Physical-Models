---
title: "Exact Reference Geometry and the Two-Bond Asymptotic of a Wilson–Dirac Covariance"
author: 'Kirtus Justus (Theoretical Physicist) \textbullet{} 31 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
---

**Abstract.** For the specified one-dimensional two-orbital Wilson--Dirac Bloch Hamiltonian, an explicit cellwise, interval-preserving unitary transforms every finite compression of the massless occupied-band projection into the scalar half-filled sine-kernel matrix. The resulting discrete-prolate sine kernel commutes exactly with a tridiagonal Jacobi matrix of simple spectrum. The same unitary gives an exact two-bond reduction of the massive-minus-massless Jacobi trace, its complete-elliptic-integral representation, and its fixed-positive-mass logarithmic expansion. The proofs work for every positive interval length and do not use numerical extrapolation. These identities do not resolve the distinct nonlinear, Coulomb/reference-mode, or entropy estimates needed for a full relative-entropy asymptotic theorem.

## 1. Model and notation

Let \(\sigma_x,\sigma_y,\sigma_z\) denote the Pauli matrices and, for \(m\geq0\), put

\[
 h_m(k)=\sin k\,\sigma_x+(m+1-\cos k)\,\sigma_z,
 \qquad E_m(k)=\bigl[m^2+4(m+1)\sin^2(k/2)\bigr]^{1/2}.
\]

The infinite-chain negative-band spectral projection has symbol
\(P_m(k)=\tfrac12(I-h_m(k)/E_m(k))\), interpreted almost everywhere for \(m=0\). Let

\[
 (C_{L,m})_{ab}=\frac1{2\pi}\int_{-\pi}^{\pi}
 e^{ik(a-b)}P_m(k)\,dk,\qquad 0\le a,b<L,
\]

where each entry is a two-by-two orbital block. Set \(N=2L\). We distinguish this compression of an infinite-volume spectral projection from the negative spectral projection of an open finite-chain Hamiltonian.

## 2. Explicit all-interval scalarization

**Theorem 1 (exact massless reference scalarization).** Define

\[
H_2=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
W=\frac{I-i\sigma_x}{\sqrt2}H_2,\qquad R=\sigma_z,
\]

and let \(U=\bigoplus_{j=0}^{L-1}(-1)^j RW\). Then, for every integer \(L\ge1\),

\[
 \boxed{\ U C_{L,0} U^\dagger=B_N\ },\qquad
(B_N)_{pq}=\begin{cases}
\frac12,&p=q,\\[2pt]
\displaystyle\frac{\sin(\pi(p-q)/2)}{\pi(p-q)},&p\ne q,
\end{cases}
\]

with \(0\le p,q<N\). The unitary is a direct sum over cells, is independent of the interval length except for repetition of its fixed blocks, and does not mix sites inside and outside the interval.

*Proof.* For an integer cell displacement \(d\), direct Fourier integration at \(m=0\) gives

\[
 (C_{L,0})_{ab}=\tfrac12\delta_{d0}I+x_d\sigma_x+z_d\sigma_z,
 \qquad d=a-b,
\]

where

\[
 x_d=-\frac{i}{2\pi}\frac{d}{d^2-1/4},\qquad
 z_d=-\frac1{\pi(1-4d^2)}.
\]

For clarity, these follow from
\(\sin k/E_0(k)=\operatorname{sgn}(k)\cos(k/2)\) and
\((1-\cos k)/E_0(k)=|\sin(k/2)|\), using elementary sine--cosine product integrals on \([0,\pi]\). In particular \(x_0=0\), \(x_{-d}=\overline{x_d}\), and \(z_{-d}=z_d\).

Direct multiplication of the constant two-by-two matrices establishes
\(W\sigma_zW^\dagger=\sigma_x\) and
\(W\sigma_xW^\dagger=-\sigma_y\). Conjugating by \(R=\sigma_z\) therefore produces

\[
 U_a(C_{L,0})_{ab}U_b^\dagger
 =(-1)^d\left(\tfrac12\delta_{d0}I+x_d\sigma_y-z_d\sigma_x\right).
\]

The upper-right and lower-left entries are respectively

\[
 (-1)^d(-z_d-ix_d)=\frac{(-1)^{d+1}}{\pi(2d-1)},\qquad
 (-1)^d(-z_d+ix_d)=\frac{(-1)^d}{\pi(2d+1)}.
\]

These are exactly the sine-kernel entries at scalar index differences \(2d-1\) and \(2d+1\). The like-orbital entries are zero for \(d\ne0\) and equal to \(1/2\) for \(d=0\). Thus every matrix entry agrees, proving the asserted identity for all \(L\). \(\square\)

**Corollary 2 (reference positivity, commuting Jacobi operator, and simple spectrum).** Define

\[
(J_N)_{j-1,j}=(J_N)_{j,j-1}=\frac{j(N-j)}{N},\quad 1\le j<N,
\]

with all remaining entries zero. Then \(0<B_N<I\), \([B_N,J_N]=0\), and \(J_N\) has simple real spectrum.

*Proof.* The sine kernel is the compression of the Fourier projection onto the momentum arc \([-\pi/2,\pi/2]\). For any nonzero vector \(v\in\mathbb C^N\), its associated trigonometric polynomial is nonzero on subsets of positive measure in both this arc and its complement, because a nonzero trigonometric polynomial cannot vanish on an open arc. Hence \(0<\langle v,B_Nv\rangle<\|v\|^2\).

Put \(b_d=\sin(\pi d/2)/(\pi d)\) with \(b_0=1/2\), and \(a_j=j(N-j)/N\), with \(a_0=a_N=0\). Direct evaluation gives

\[
 [J_N,B_N]_{pq}=\frac{N-p-q-1}{N}
 \left[(p-q-1)b_{p-q-1}+(p-q+1)b_{p-q+1}\right]=0.
\]

The last equality follows from the sine addition formula, including the removable zero-index terms. All \(a_j>0\) for \(1\le j<N\). For an eigenvector of the symmetric Jacobi matrix, its first coordinate fixes the others recursively; a zero first coordinate forces the zero vector. Every eigenspace is therefore one-dimensional, and the real symmetric matrix has simple spectrum. \(\square\)

## 3. The exact massive two-bond trace

Let \(A_N=UC_{L,m}U^\dagger\) and \(\Delta_N=A_N-B_N\). The mass-independent unitary of Theorem 1 also scalarizes the massive compression, though \(A_N\) is generally not the sine kernel and need not commute with \(J_N\).

**Theorem 3 (two-bond Fourier and elliptic identities).** Define

\[
 u_m=\frac1{2\pi}\int_0^\pi\frac{m+1-\cos k}{E_m(k)}\,dk,
 \quad
 v_m=\frac1{2\pi}\int_0^\pi\frac{1-(m+1)\cos k}{E_m(k)}\,dk.
\]

Then \(u_m\) and \(v_m\) are the intra-cell and inter-cell nearest-neighbor entries of \(A_N\) in scalar index order, respectively, while \(u_0=v_0=1/\pi\). For every \(L\ge1\),

\[
\boxed{\ \operatorname{Tr}[\Delta_N(-\pi J_N)]
=-\pi\left[\frac{4L^2-1}{6}
 \left(u_m+v_m-\frac2\pi\right)
+\frac12(u_m-v_m)\right].\ }
\]

For \(m>0\) put \(r=m/(m+2)\), \(z=1-r^2\), and define complete elliptic integrals with **parameter** \(z\):

\[
\mathbf K(z)=\int_0^{\pi/2}\frac{d\theta}{\sqrt{1-z\sin^2\theta}},\quad
\mathbf E(z)=\int_0^{\pi/2}\sqrt{1-z\sin^2\theta}\,d\theta.
\]

Then the following identities are exact:

\[
\boxed{\quad
 u_m+v_m=\frac2\pi\frac{\mathbf E(1-r^2)-r^2\mathbf K(1-r^2)}{1-r^2},
 \qquad
 u_m-v_m=\frac{2r}\pi\frac{\mathbf K(1-r^2)-\mathbf E(1-r^2)}{1-r^2}.
\quad}
\]

*Proof.* For general \(m\), write the Fourier coefficient of \(P_m\) as \(\tfrac12\delta_{d0}I+x_d(m)\sigma_x+z_d(m)\sigma_z\). Its coefficients satisfy

\[
 z_d(m)=-\frac1{2\pi}\int_0^\pi\cos(dk)\frac{m+1-\cos k}{E_m(k)}\,dk,
\quad
 x_d(m)=-\frac i{2\pi}\int_0^\pi\sin(dk)\frac{\sin k}{E_m(k)}\,dk.
\]

The same constant orbital rotation and alternating cell gauge show that the intra-cell bond is \(-z_0(m)=u_m\). The inter-cell bond is \(z_1(m)+ix_1(m)\), which simplifies to \(v_m\) because
\(\sin^2k-\cos k(m+1-\cos k)=1-(m+1)\cos k\). At \(m=0\), the formulas in Theorem 1 yield \(u_0=v_0=1/\pi\).

Because \(J_N\) has only first off-diagonal entries, the trace receives only these two bond contributions. Elementary summation gives

\[
\sum_{\substack{1\le j<2L\\j\,\mathrm{odd}}}\frac{j(2L-j)}{2L}=\frac{2L^2+1}{6},\qquad
\sum_{\substack{1\le j<2L\\j\,\mathrm{even}}}\frac{j(2L-j)}{2L}=\frac{L^2-1}{3}.
\]

Thus the trace equals \(-2\pi\bigl[\frac{2L^2+1}{6}(u_m-1/\pi)+\frac{L^2-1}{3}(v_m-1/\pi)\bigr]\), algebraically equivalent to the boxed two-bond formula.

Finally, \(E_m(k)=(m+2)\sqrt{1-z\cos^2(k/2)}\). Taking sums and differences of the original Fourier integrals gives

\[
u_m+v_m=\frac{m+2}{2\pi}\int_0^\pi\frac{1-\cos k}{E_m(k)}\,dk,\qquad
u_m-v_m=\frac{m}{2\pi}\int_0^\pi\frac{1+\cos k}{E_m(k)}\,dk.
\]

Set \(\theta=(\pi-k)/2\). The integrals reduce to the standard identities
\(\int\sin^2\theta/\sqrt{1-z\sin^2\theta}=(\mathbf K-\mathbf E)/z\) and
\(\int\cos^2\theta/\sqrt{1-z\sin^2\theta}=(\mathbf E-(1-z)\mathbf K)/z\), yielding exactly the asserted forms. The \(m=0\) case follows by continuity. \(\square\)

**Corollary 4 (unconditional fixed-\(\mu\) two-bond finite part).** Fix \(\mu>0\), set \(m=\mu/L\), and let \(\mathcal P_L=\operatorname{Tr}[\Delta_N(-\pi J_N)]\). Then

\[
 \boxed{\mathcal P_L=
 \frac{\mu^2}{6}\log L+
 \mu^2\left(\frac16\log\frac8\mu-\frac14\right)
 +\mathcal O_\mu\left(\frac{\log L}{L}\right).}
\]

*Proof.* For \(r\downarrow0\), put \(\ell=\log(4/r)\). The classical complementary-modulus expansions (DLMF §19.12) yield

\[
\mathbf K(1-r^2)=\ell+\mathcal O(r^2\ell),\qquad
\mathbf E(1-r^2)=1+\frac{r^2}{2}(\ell-\tfrac12)+\mathcal O(r^4\ell).
\]

It follows that

\[
 u_m+v_m=\frac2\pi\left[1+r^2\left(\frac34-\frac\ell2\right)+\mathcal O(r^4\ell)\right],
 \quad
 u_m-v_m=\frac{2r}\pi\left[\ell-1+\mathcal O(r^2\ell)\right].
\]

For \(r=\mu/(2L+\mu)\), one has \((4L^2-1)r^2=\mu^2+\mathcal O_\mu(L^{-1})\), \(r\ell=\mathcal O_\mu((\log L)/L)\), and \(\ell=\log L+\log(8/\mu)+\mathcal O_\mu(L^{-1})\). Inserting these in Theorem 3 gives the result. No estimates for the nonlinear, modular, or entropy branches are used. \(\square\)

## 4. Consequences and explicit limits of the derivation

The scalar reference geometry, its Jacobi commutation, and the exact Fourier-to-elliptic reduction of \(\mathcal P_L\) follow unconditionally from the specified infinite-chain Wilson symbol. The finite relative-entropy identity

\[
\mathcal D_L=\mathcal P_L+\mathcal Q_N+\mathcal F_L-\Delta S_L
\]

requires separate analyses of \(\mathcal Q_N\), \(\mathcal F_L\), and \(\Delta S_L\) to yield a full asymptotic theorem. Their boundedness, assembled in *Uniform Bulk Modular Asymptotics and the Leading Wilson Entropy Law*, establishes the leading coefficient at fixed positive mass; convergence to a finite part requires stronger control. In particular, the Coulomb/reference-mode occupancy identities, all-degree comparison hypotheses where applicable, and compatible mass-dependent limiting quantifiers are not established by these results. The logarithmic coefficient of \(\mathcal P_L\) alone must not be identified with a proved coefficient of \(\mathcal D_L\). This paper concerns finite compressions of full-line projectors and makes no equivalence claim for projectors of finite open-chain Hamiltonians.

## References

1. NIST Digital Library of Mathematical Functions, §19.12, *Asymptotic Approximations of Legendre's Integrals*, https://dlmf.nist.gov/19.12 (the DLMF symbol uses the modulus; the manuscript's \(\mathbf K(z),\mathbf E(z)\) use the parameter \(z\)).
2. H. Araki, "On Quasifree States of CAR and Bogoliubov Automorphisms," *Publications of the Research Institute for Mathematical Sciences* **6** (1970/71), 385--442, doi:10.2977/PRIMS/1195193913.
3. D. Slepian, "Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty V: The Discrete Case," *Bell System Technical Journal* **57** (1978), 1371--1430, doi:10.1002/j.1538-7305.1978.tb02104.x.
4. F. A. Grünbaum, "Eigenvectors of a Toeplitz Matrix: Discrete Version of the Prolate Spheroidal Wave Functions," *SIAM Journal on Algebraic Discrete Methods* **2** (1981), 136--141, doi:10.1137/0602017.

## Acknowledgments and AI-assisted research

Kirtus Justus supplied research direction, the model, source materials, and requirements for independent mathematical scrutiny. ChatGPT (OpenAI) assisted in developing and checking the derivations, symbolic and numerical diagnostics, and manuscript drafting. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer) are acknowledged for prior participation in the broader research program; no specific new derivation in this manuscript is attributed to them without supporting provenance. The named human author remains responsible for scientific content. The manuscript has not undergone independent journal peer review and does not imply endorsement by an AI provider.
