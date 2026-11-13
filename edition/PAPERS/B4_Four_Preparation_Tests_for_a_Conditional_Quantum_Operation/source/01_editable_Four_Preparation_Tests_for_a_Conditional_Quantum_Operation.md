---
title: "Four-Preparation Tests for a Conditional Quantum Operation"
author: "Kirtus Justus"
date: "Port Coquitlam, British Columbia"
lang: en
---

**Abstract.** Consider a two-qubit operation selected by an observed success event. Two computational-basis preparations have a common binary readout on the first output qubit, and success is recorded for all four basis inputs. We characterize the resulting population data under a lower bound on the local component of the operation's Choi matrix. The discrepancy between the two resolved outcome distributions and the discrepancy between the two remaining success rates share one exact upper bound. A constructive converse holds for a common rank-one projective readout with otherwise unrestricted output states. Randomized assignment after eligibility gives sequential tests with finite-sample control under conditional variation from attempt to attempt.

### Measurement model

Order inputs as \(00,01,10,11\), indexed by \(i=0,1,2,3\). At a given eligible history the four assignments share one nonzero completely positive trace-nonincreasing map with Kraus operators \(K_j\). Write \(s_i=\sum_j\|K_j|i\rangle\|^2\) for its input-specific success probabilities, \(S=\sum_i s_i>0\), and \(p_*=S/4\) for its success probability on \(I_4/4\). On inputs 0 and 1, \(r_{iy}\) is the probability of success and outcome \(y\in\{0,1\}\) of the same binary effect on the first qubit. Thus \(\sum_y r_{iy}=s_i\). All probabilities are per attempted preparation.

Use the Hilbert–Schmidt inner product on Kraus matrices. The normalized Choi state has weight
\[
 w=\frac{\sum_j\|\operatorname{proj}_{\mathcal L} K_j\|_F^2}{S},
 \qquad \mathcal L=\{V\otimes I_2:V\in M_2\}.
\]
The tensor factors, their bases, the prepared inputs and the success event are part of the observation model. The null specifies \(w\ge w_0\), with \(0\le w_0\le1\).

**Proposition 1 (four measured success rates).** Assume the click effect in both arms is \(E\otimes I_2\), with \(0\le E\le I_2\) acting on the first output qubit. Define \(D=\sum_y(\sqrt{r_{0y}}-\sqrt{r_{1y}})^2\). Then
\[
 \boxed{D+(\sqrt{s_2}-\sqrt{s_3})^2\ \le\ 2(1-w_0)S.}
\]
For nonnegative rates with \(0\le s_i\le1\), the stated normalization, and a common rank-one projective first-qubit measurement, this is also sufficient when only these data are fixed. In particular it gives the largest compatible value of \(w\). An independently calibrated nonprojective effect determines the spectral populations described below.

\newpage

# Proof of the four-input bound

In the block structure of the second qubit write each Kraus matrix as \(K_j=\left(\begin{smallmatrix}A_j&B_j\\ C_j&D_j\end{smallmatrix}\right)\), with blocks acting on the first qubit. Orthogonal projection onto \(\mathcal L\) replaces both diagonal blocks by their average and the other blocks by zero. Hence
\[
 S(1-w)=\sum_j\bigl(\tfrac12\|A_j-D_j\|_F^2+\|B_j\|_F^2+\|C_j\|_F^2\bigr).
\]

Let \(u_i=\sum_j K_j|i\rangle\otimes|j\rangle\) be the unnormalized success vectors, and let \(X\) flip only the second output bit. The sum of the squared distances between the aligned columns for the two pairs is
\[
 \sum_{b=0}^1\|u_{2b}-X u_{2b+1}\|^2
 =\sum_j\bigl(\|A_j-D_j\|_F^2+\|C_j-B_j\|_F^2\bigr)
 \le 2S(1-w).
\]
For the first pair, resolve the common measurement using its positive square-root effects. It commutes with \(X\). For each outcome the reverse triangle inequality bounds the difference of the two component norms by the norm of their difference. Summing the squares gives the lower bound \(D\) for the first distance. For the second pair, the same argument without resolving an outcome gives \((\sqrt{s_2}-\sqrt{s_3})^2\). The displayed bound follows.

**Attainment.** In the known projective measurement basis \(\{|y\rangle\}\), choose a dilation whose four input columns are
\[
 u_i=\sum_y\sqrt{r_{iy}}\,|y,i\rangle\,|e_y\rangle\quad(i=0,1),
 \qquad u_{2+b}=\sqrt{s_{2+b}}\,|0,b\rangle\,|e_\perp\rangle\quad(b=0,1).
\]
The three environment vectors are orthonormal. The columns are mutually orthogonal, so the success effect is \(\operatorname{diag}(s_0,s_1,s_2,s_3)\le I\). The first pair reproduces each \(r_{iy}\); the second pair gives the two prescribed successes. The off-diagonal second-bit blocks vanish. Each reverse triangle bound attains equality, giving
\[
 w_{\max}=1-\frac{D+(\sqrt{s_2}-\sqrt{s_3})^2}{2S}.
\]
Zero individual success probabilities are allowed. If the available information on the last pair is only their sum, equality of their two probabilities minimizes the extra term. This explains why resolving them separately can exclude additional operations.

\newpage

# Resolving the output for every preparation

Let the same effect \(E\otimes I_2\) be recorded on successful attempts in all four arms and set \(D_{ij}=\sum_y(\sqrt{r_{iy}}-\sqrt{r_{jy}})^2\). Resolving the second pair by the square roots of the effects in the aligned-column proof gives
\[
 D_{01}+D_{23}\le 2(1-w)S .
\]
For a common rank-one projective first-qubit measurement the upper weight \(1-(D_{01}+D_{23})/(2S)\) is attained. Take four orthonormal environment labels \(e_{by}\) and use the columns
\[
 u_{2b+t}=\sum_y\sqrt{r_{2b+t,y}}\,|y,t\rangle|e_{by}\rangle,\quad b,t=0,1 .
\]
Distinct flags or environment spaces make the columns orthogonal. Their Gram matrix has diagonal \(s_i\le1\), hence defines a contraction. Projecting its Kraus operators onto \(\mathcal L\) attains the stated bound. For a known nonprojective common effect, the exact criterion applies to the success-weighted spectral populations recovered from its eigenvalues.

For nonzero \(s_2,s_3\) the gain in discrepancy is \(2\sqrt{s_2s_3}[1-\sum_y\sqrt{q_{2y}q_{3y}}]\), where \(q_{iy}=r_{iy}/s_i\). If either success vanishes, the gain is zero by continuity. For the four rows \((9,4),(4,9),(16,9),(9,16)\) in hundredths, \(D_{01}=D_{23}=1/50\) and \(S=19/25\). Resolving the second pair reduces the sharp upper weight from \(75/76\) to \(37/38\).

More generally, prescribe the four unnormalized first marginals \(\tau_i\), with \(\operatorname{Tr}\tau_i=s_i\). Write \(F_*(A,B)=\|\sqrt A\sqrt B\|_1\). Then
\[
 w_{\max}=\tfrac12+
 [F_*(\tau_0,\tau_1)+F_*(\tau_2,\tau_3)]/S.
\]
In the first bound replace each classical affinity by the maximal real overlap of the two successful purifications in its pair. Uhlmann's characterization proves necessity. Choose overlap-maximizing purifications in disjoint environment spaces for the two pairs and attach the opposite second-output flags within each pair. The same orthogonality and projection argument attains the maximum. Zero-success columns can be set to zero.

\newpage

# A sequential test using all attempted preparations

Let \(\mathcal H_n\) contain all information before assignment on eligible attempt \(n\). The conditional map, its success probabilities and its readout may vary with \(\mathcal H_n\). Given that history, the same map must describe all four possible assignments and its weight must satisfy \(w_n\ge w_0\). Assign input \(i\) by a private random draw with known positive probabilities \(\pi_{ni}\). Uniform assignment prepares \(I_4/4\) on average. Under unequal assignment the inverse probabilities below recover the unweighted sum of the four conditional success rates.

**Proposition 2 (sequential size).** At each eligible history the two tested inputs share the local click effect \(E_n\otimes I_2\). Set \(\epsilon=1-w_0\). Before assignment choose positive slopes \(t_y\) and \(v\). Suppress \(n\) in the following coefficients:
\[
 d_{0y}=1-t_y,\qquad d_{1y}=1-t_y^{-1},\qquad
 d_2=1-v,\qquad d_3=1-v^{-1}.
\]
On a success with assigned input \(i\), score \(X_n=(d-2\epsilon)/\pi_{ni}\), using the corresponding coefficient. Score every failure by zero. Choose a predictable nonnegative stake \(\eta_n\) such that \(1+\eta_n X_n\ge0\) for every possible outcome. Then \(M_0=1\) and \(M_N=\prod_{n\le N}(1+\eta_n X_n)\) obey
\[
 \Pr_{H_0}\!\left(\sup_N M_N\ge1/\alpha\right)\le\alpha,\qquad 0<\alpha<1 .
\]
Ineligible attempts leave the product unchanged.

**Proof.** For \(x,y\ge0\), \((1-t)x+(1-t^{-1})y\le(\sqrt{x}-\sqrt y)^2\), by arithmetic–geometric mean; maximizing over positive \(t\) gives equality or its limiting value. Assignment weighting gives the conditional expected score
\[
 \sum_y(d_{0y}r_{0y}+d_{1y}r_{1y})+d_2s_2+d_3s_3-2\epsilon S\le0
\]
by Proposition 1. Multiplying nonnegative predictable bets therefore yields a nonnegative supermartingale, and Ville's inequality gives the crossing bound [1]. This reasoning allows dependence between attempts. Setting \(v=1\) gives the test in which inputs 2 and 3 enter only through their combined success probability. Its validity requires only \(D\le2\epsilon S\). If both outcomes are read on the last pair, use one slope \(v_y\) per outcome in place of \(v\). Their support inequality is bounded by \(D_{23}\), and the conditional mean remains nonpositive by the four-outcome theorem. Thus the statistic can be specified before data collection in either form. A prespecified convex mixture also controls size. Searching over completed tests for the first one to cross requires multiplicity control.

\newpage

# Calibrated local readout

Let \(E\otimes I_2\) be the click effect in both tested arms, with \(E=L I_2+(U-L)P\), \(0\le L<U\le1\), and rank-one \(P\). Write \(z_i\) for success and a click per attempt. Its success-weighted spectral populations are
\[
 v_{i+}=\frac{z_i-Ls_i}{U-L},\qquad
 v_{i-}=\frac{Us_i-z_i}{U-L}.
\]
Thus \(Ls_i\le z_i\le Us_i\) is required. Define \(D_E=\sum_{j=\pm}(\sqrt{v_{0j}}-\sqrt{v_{1j}})^2\),
\(R=(\sqrt{s_2}-\sqrt{s_3})^2\), and \(B=2(1-w_0)S-R\). For admissible successes and nonnegative spectral populations, the four-input data are compatible exactly when \(D_E\le B\) in the model that fixes only the four successes, the two click rates, the common effect and \(w\ge w_0\).

**Proof.** Resolve \(P,I-P\) on the first output qubit and apply Proposition 1. Conversely, construct the two tested outputs diagonal in this basis from \(v_{ij}\), using the four columns on the preceding pages. Applying the specified effect then gives exactly \(z_i\). The unknown states need not commute for necessity. Neither the absolute orientation of the eigenbasis nor a choice of phases enters this reduced criterion. The same spectral projectors must apply to both arms. For a scalar effect \(U=L\), require \(z_i=Ls_i\) and use \((\sqrt{s_0}-\sqrt{s_1})^2\) for the minimum tested-pair discrepancy.

**Equal successes.** Suppose \(s_0=s_1=s>0\), \(q_i=z_i/s\). If \(B<0\) even identical outputs are incompatible. Otherwise set \(c=\max(0,1-B/(2s))\). The binary spectral distributions have root fidelity at least \(c\). The fidelity–trace-distance inequality [2] bounds their total variation by \(\sqrt{1-c^2}\). Therefore
\[
 |q_0-q_1|\le (U-L)\sqrt{1-c^2}.
\]
Oppositely ordered spectral probabilities \(((1+d)/2,(1-d)/2)\), with \(d=\sqrt{1-c^2}\), attain the bound. When only \(p_*=S/4\) is known, choose \(s_2=s_3\) if admissible, giving \(c=\max(0,1-4p_*(1-w_0)/s)\). At \(s=p_*=1, w_0=.99, L=.2,U=.8\), the maximum is \(21/125=.168\); the two conditional click rates are .584 and .416.

**Statistical use.** A nonprojective click is a stochastic coarse measurement of the spectral outcome. Its raw squared-root discrepancy can be smaller. The spectral score for each tested success can be implemented on the observed bit \(y\) by replacing \(d_{iy}\) with \(d_{i-}+(y-L)(d_{i+}-d_{i-})/(U-L)\) before applying the penalty and assignment weight in Proposition 2. The score has the required spectral expectation by direct substitution. The stake must ensure nonnegativity for all outcomes. Uncertainty in the spectrum and success rates must be propagated jointly; inversion becomes ill-conditioned as \(U-L\) tends to zero.

\newpage

# Detector transfer across preparations

Two distinct controls delimit the local theorem. For the identity channel \(w=1\). A detector acting on the second qubit distinguishes \(|00\rangle\) from \(|01\rangle\) with certainty: its two binary laws give \(D=2\). Such a measurement falls outside Proposition 1. Alternatively, both first-qubit outputs are \(|0\rangle\), but arm-specific effects \(\mathrm{diag}(.8,.2)\) and \(\mathrm{diag}(.2,.8)\) give clicks .8 and .2. Equal eigenvalues do not establish a common first-qubit effect. Detector tomography provides an experimental means of characterizing quantum measurement effects [4].

**Corollary (known relative orientation).** Two calibrated local effects may share eigenvalues \(L<U\) while their high-eigenvalue projectors have Bloch directions at angle \(\theta\in[0,\pi]\). For equal positive tested successes, with admissible totals and \(B\ge0\) as above, the sharp contrast over otherwise unrestricted first-qubit outputs is
\[
 \max|q_0-q_1|=(U-L)\sin\!\left(\min\{\pi/2,\,\theta/2+\arccos c\}\right).
\]
This is a bound for the calibrated pair of effects. The original common-effect betting statistic assumes \(\theta=0\).

**Proof.** For two specified first-qubit marginals their root fidelity \(F\) is the largest real overlap of two normalized purifications [2]. The first pair of aligned columns then has squared distance at least \(2s(1-F)\). The second pair costs at least \(R\). Both bounds are attained by placing overlap-maximizing purifications on opposite second-bit flags, and the two remaining columns in a common disjoint environment sector with their respective norms. Thus the reduced class is exactly \(F\ge c\).

For qubit Bloch vectors \(r_0,r_1\), form the unit vectors \(u_i=(r_i,\sqrt{1-|r_i|^2})\). The two-dimensional fidelity identity \(F^2=\operatorname{Tr}(\rho_0\rho_1)+2\sqrt{\det\rho_0\det\rho_1}=(1+u_0\cdot u_1)/2\) bounds their angle by \(2\arccos c\). Rotate the second detector axis onto the first through \(\theta\), acting trivially on the fourth coordinate. This changes the angle of \(u_1\) by at most \(\theta\). The triangle inequality on the sphere and projection on the first axis bound the click difference by half the resulting chord length times \(U-L\), as stated.

For equality choose coplanar detector axes \((\cos(\theta/2),\pm\sin(\theta/2))\) and pure-state vectors \((\pm\sin\tau,\cos\tau)\), with \(\tau=\min(\arccos c,(\pi-\theta)/2)\). Their root fidelity is \(\cos\tau\) and their click difference is \((U-L)\sin(\tau+\theta/2)\). These states therefore realize the maximum using a single branch. For a known upper bound on \(\theta\), monotonicity gives the corresponding conservative cap; the actual angle and the local Choi weight are calibration inputs.

\newpage

# Equality, selection and physical interpretation

Set \(r_{0\bullet}=(9/100,4/100)\), \(r_{1\bullet}=(4/100,9/100)\), and \(s_2=s_3=1\). Then \(D=1/50\), \(S=113/50\) and the dilation in Proposition 1 gives \(w=225/226\). With \(t_0=2/3,t_1=3/2,v=1\) and \(\epsilon=1/226\), the conditional mean score is zero. This example attains the population bound and gives a mean-one factor for any admissible stake. It does not establish attainment of Ville's probability bound.

**Selection control.** A single diagonal Kraus matrix with squared entries \((.045,.005,.975,.975)\) has \(p_*=.5\) and \(w=.995\). For fair assignment between inputs 0 and 1, both successful first-qubit outputs are \(|0\rangle\), yet 90% of retained successes are from input 0. To see the statistical consequence, assign all successes a click and score them by \(+1\) on input 0 and \(-1\) on input 1. If \(k\) of \(n\) retained successes came from input 0, a statistic normalized for fair assignment with contrast cap \(.28\) and exponential parameter \(\log2\) is
\[
 M_n=\frac{2^{2k-n}+2^{n-2k}}{2(33/25)^n}.
\]
For the fair-input envelope with score \(Z=(2R-1)Y\), arm 1 has the positive sign. The maximizing corner for the positive exponential is \((p_0,p_1)=(1-\delta,1)\). Reversing the sign exchanges the two arms and leaves the two-sided statistic unchanged.

Under independent repetitions in this example, \(k\sim\operatorname{Bin}(n,.9)\). At \(n=20\) the statistic is at least 20 exactly for \(k\le3\) or \(k\ge17\), of probability \(0.8670466765656734\ldots\). The probability of crossing *by* success 20 is \(0.898600383922\ldots\), obtained by removing paths at the first crossing in the binomial recursion. Through 20 successes the only possible first-hitting times are 9, 13, 16 and 19. The 5% guarantee in Proposition 2 applies to the attempt-level product and its stated null.

**Assignment control.** On the same equality example, take \(\pi=(3/8,3/8,1/8,1/8)\). The expected score with inverse assignment weights is zero. Omitting those weights gives \((3/8)(1/50)-(1/113)[(3/8)(26/100)+1/4]=1/226>0\) on the null. As a separate four-rate example, identical tested rows \((1/4,1/4)\) and remaining successes \((1,1/4)\) give \(S=9/4,D=0,R=1/4\). Proposition 1 gives \(w_{\max}=17/18\).

**Interpretation.** Application requires trusted preparations, commitment of eligibility before assignment, a common conditional operation across assignments, a transferable readout and a justified conditional lower bound on \(w\). Estimated calibration bounds require simultaneous coverage or an appropriate allocation of type-I error. A crossing tests these assumptions jointly. No experimental trial count, power or microscopic cause is determined by the theorem. Experimental multitime tomography provides one framework for studying intervention dependence [3].

**References.** [1] P. Wills, E. Knill, K. Coakley and Y. Zhang, *J. Res. NIST* **125**, 125003 (2020). [DOI](https://doi.org/10.6028/jres.125.003). [2] J. Watrous, *The Theory of Quantum Information*, chapters 2–3 (2018). [Text](https://cs.uwaterloo.ca/~watrous/TQI/). [3] G. A. L. White et al., *PRX Quantum* **3**, 020344 (2022). [DOI](https://doi.org/10.1103/PRXQuantum.3.020344). [4] A. S. Aasen et al., *Commun. Phys.* **7**, 301 (2024). [DOI](https://doi.org/10.1038/s42005-024-01790-8).

**Research direction and responsibility:** Kirtus Justus. Mathematical and computational assistance: ChatGPT (OpenAI).
