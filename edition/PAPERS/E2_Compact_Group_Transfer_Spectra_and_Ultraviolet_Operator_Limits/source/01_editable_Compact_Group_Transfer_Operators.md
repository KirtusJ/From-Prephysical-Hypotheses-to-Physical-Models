---
title: "Compact-Group Transfer Spectra and Ultraviolet Operator Limits"
author: 'Kirtus Justus \textbullet{} Theoretical Physicist \textbullet{} 23 October 2026\tabularnewline Port Coquitlam, British Columbia, Canada'
date: ''
lang: en
header-includes:
 - \usepackage{microtype}
 - \usepackage{booktabs}
 - \usepackage{longtable}
---

**Abstract.** A normalized central positive transfer operator on $SU(2)$ supplies an exactly diagonalizable test of continuum-scale inference. Bessel ratios give its spectrum; Peter–Weyl multiplicities change the ultraviolet Schatten thresholds. We distinguish positive-time convergence, resolvent convergence, generator domains and the short-time trace topology. A representation-theoretic commutant lemma limits which symmetric perturbations may fail to commute. A Schatten–Duhamel estimate and a scalar-shift-invariant unhalved trace-norm bound give stability of unnormalized and normalized heat operators under bounded perturbations, and an explicit diagonal moving-projection model realizes the normalized rate order. Sharp moving-window limits for the Bessel model and a proposed noncommuting construction remain unproved targets. These are mathematical operator results with their Hilbert spaces and scaling parameters fixed, and do not constitute a continuum Yang–Mills construction.

**Keywords:** SU(2); compact groups; heat operators; modified Bessel functions; Schatten ideals.

## 1. The operator and its two inequivalent representation spaces

The decomposition uses the Peter–Weyl theorem and the representation theory of $SU(2)$ [2]. Standard properties and uniform asymptotic methods for modified Bessel functions are documented in the NIST Digital Library of Mathematical Functions [1].

Take normalized Haar measure on $G=SU(2)$ and $\gamma>0$. The central convolution transfer operator is

$$ (T_\gamma f)(U)=\frac{1}{Z_\gamma}\int_G e^{\frac\gamma2\mathrm{Tr}(UV^{-1})}f(V)\,dV,
\quad Z_\gamma=\frac{2I_1(\gamma)}\gamma. $$

On the conjugation-invariant character Hilbert space $\mathcal H_c=L^2(G)^{\mathrm{Ad}}$ each integer $n=2j+1\ge1$ occurs **once**. On the full regular representation $\mathcal H_f=L^2(G)$ it occurs with multiplicity $n^2$:

$$T_\gamma\big|_n=\frac{I_n(\gamma)}{I_1(\gamma)}I,
\qquad A_\gamma=-\gamma\log T_\gamma,\quad a_{\gamma,n}=-\gamma\log\frac{I_n(\gamma)}{I_1(\gamma)},\quad \ell_n=\frac{n^2-1}{2}. $$

Let $L$ denote the diagonal operator with eigenvalues $\ell_n$. Here $s>0$ is an **abstract semigroup parameter**; no physical time units have been identified. The normalized vacuum is the constant representation $n=1$.

**Proposition (fixed-positive-time operator-norm limits).** On either specified representation space,
\[
\|e^{-sA_\gamma}-e^{-sL}\|\longrightarrow0\quad(s>0\text{ fixed}),\qquad
\|(A_\gamma+I)^{-1}-(L+I)^{-1}\|\longrightarrow0.
\]
*Proof.* The positive integral representation of $I_\nu$ [1, §10.32.2], differentiated in $\gamma$ and combined with $I_\nu'=I_{\nu+1}+\nu I_\nu/\gamma$, gives
\[
\frac{I_{\nu+1}(\gamma)}{I_\nu(\gamma)}
=\frac{\int_{-1}^{1}t e^{\gamma t}(1-t^2)^{\nu-1/2}\,dt}
{\int_{-1}^{1}e^{\gamma t}(1-t^2)^{\nu-1/2}\,dt}\in(0,1),\qquad \nu\ge1.
\]
Positivity follows by pairing $t$ and $-t$; the strict upper bound follows from $t<1$ almost everywhere. Thus $a_{\gamma,n}$ increases with $n$ and is nonnegative. The fixed-order large-argument expansion [1, §10.40.1] gives $a_{\gamma,n}\to(n^2-1)/2$ for every fixed $n$. Split each diagonal supremum into $n\le M$ and $n>M$. The finite part tends to zero; the heat tail is bounded by $e^{-s a_{\gamma,M}}+e^{-s\ell_M}$ and the resolvent tail by $(1+a_{\gamma,M})^{-1}+(1+\ell_M)^{-1}$. Taking $\gamma\to\infty$ and then $M\to\infty$ proves both limits. Multiplicities do not affect an operator-norm supremum. $\square$

This proof supplies no trace-ideal rate, convergence of generator domains, or operator-norm convergence uniform down to $s=0$. At fixed $\gamma$, the large-$n$ growth law differs from that of $L$.

## 2. Representation multiplicity and Schatten scale

For $1\le p<\infty$ and $m_n\in\{1,n^2\}$,

$$\|e^{-sA_\gamma}-e^{-sL}\|_p^p
=\sum_{n\ge1}m_n\,|e^{-sa_{\gamma,n}}-e^{-s\ell_n}|^p.$$

A large-order Bessel expansion separates two scales:

$$a_{\gamma,n}-\ell_n\approx \frac{n^2}{4\gamma}-\frac{n^4}{24\gamma^2},$$

on the uniform moving spectral windows for which the remainder is controlled. Both terms contribute if $n\asymp\sqrt\gamma$; neither can be extrapolated to arbitrary $n$ without a tail estimate.

**Asymptotic target 1 (unproved moving-window predictions).** Formal scaling analysis predicts the following transitions; no quantified uniform remainder and tail proof is supplied here. On $\mathcal H_c$, the first order-one discrepancy occurs at $s=u\gamma^{-4p/(2p+1)}$. On $\mathcal H_f$ it occurs at

$$\boxed{s=u\gamma^{-\alpha_p},\qquad
\alpha_p=\begin{cases}2p/3,&1\le p<3/2,\\1,&p=3/2,\\4p/(2p+3),&p>3/2.\end{cases}}$$

These predictions require quantified uniform Bessel expansions and summable spectral tails. They are not a conditional theorem with fully specified sufficient hypotheses. In particular, the proposed full-space $p=1$ limit is

$$\lim_{\gamma\to\infty}\|e^{-u\gamma^{-2/3}A_\gamma}-e^{-u\gamma^{-2/3}L}\|_1
=\frac34\sqrt{\frac\pi2}u^{-3/2}.$$

The same formal calculation predicts that at this scale the corresponding normalized trace-state discrepancy tends to zero and its leading term is of order $\gamma^{-1}$. The coefficient for the full regular representation is $(3\sqrt3/2)\sqrt{2/\pi}\,e^{-3/2}$. The character-space first trace-norm crossover instead occurs at $\gamma^{-4/3}$. The two statements have different multiplicities and cannot be relabeled as a single 'SU(2) trace threshold'.

## 3. A symmetry obstruction to unrestricted noncommuting perturbations

The Peter–Weyl decomposition is

$$ L^2(G)\simeq\bigoplus_{n=1}^\infty V_{(n-1)/2}\otimes V_{(n-1)/2}^*,\qquad \dim=n^2. $$

Each block appears with multiplicity one as an irreducible representation of $G\times G$. Thus a bounded operator commuting with **both** regular left and right actions is block scalar; the full commutant is abelian. Any two such operators commute (Theorem 2, immediate from Schur's lemma). Symmetry only under the *diagonal conjugation action* is weaker. The decomposition into $SU(2)$ conjugation irreducibles has common subrepresentations across neighboring blocks, enabling conjugation-equivariant but noncommuting operators.

These statements do not select which observables or symmetries a physical gauge-invariant vacuum Hilbert space should carry.

## 4. Bounded noncommuting perturbations

**Theorem 3 (Schatten–Duhamel stability).** Let $A$ be self-adjoint and bounded below, with $e^{-sA}$ trace class for $s>0$, and let $V=V^*$ be bounded, $v=\|V\|$. Then for $1\le p<\infty$,

$$\boxed{\|e^{-s(A+V)}-e^{-sA}\|_p\le (e^{sv}-1)\|e^{-sA}\|_p.}$$

*Proof.* Duhamel gives $e^{-s(A+V)}-e^{-sA}=-\int_0^s e^{-(s-t)(A+V)}Ve^{-tA}\,dt$. Apply Schatten Hölder with exponents $ps/(s-t)$ and $ps/t$. The min–max eigenvalue inequality from $A+V\ge A-vI$ bounds the $p$-th trace of the perturbed heat operator by $e^{psv}\operatorname{Tr}(e^{-psA})$. The integrand is consequently bounded by $v e^{(s-t)v}\|e^{-sA}\|_p$; integrate. $\square$

This is a general operator theorem, **not** a requirement that $[A,V]=0$. Its application to a moving ultraviolet scale must additionally control the heat trace uniformly in $\gamma$.

**Construction target 1 (noncommuting moving ultraviolet perturbation; unproved).** One proposed direction is to specify bounded conjugation-equivariant operators $K_\gamma$ and $V_\gamma=c\gamma^{-1/3}K_\gamma$ which vanish on every fixed low representation eventually, preserve the vacuum and fixed-positive-time limits, and modify a moving-scale trace coefficient. No definition of $K_\gamma$ or complete asymptotic construction is supplied here. Accordingly this paragraph asserts no counterexample. A moving-unitary construction would likewise need an explicit operator and a proved change of the relevant trace comparison. The diagonal model in §6 proves only the normalized rate order in its own stated setting.

## 5. A normalized-state perturbation theorem independent of multiplicity

**Theorem 4 (bounded-perturbation stability of normalized Gibbs operators).** Suppose $A=A^*$ is bounded below, $e^{-sA}$ is trace class for the specified $s>0$, and $V=V^*$ is bounded. Define $\rho_A(s)=e^{-sA}/\operatorname{Tr}e^{-sA}$ and

$$\operatorname{osc}(V)=\sup\sigma(V)-\inf\sigma(V).$$

All norms $\|\rho-\sigma\|_1$ in this analysis are **unhalved Schatten trace norms**, with operational trace distance $T(\rho,\sigma)=\frac12\|\rho-\sigma\|_1$. Then, without any commutativity assumption,

$$\boxed{\|\rho_{A+V}(s)-\rho_A(s)\|_1\le\min\{2,s\,\operatorname{osc}(V)\}.}$$

*Proof.* Let $A_r=A+rV$, $X_r=e^{-sA_r}$ and $Z_r=\operatorname{Tr}X_r$. Bounded perturbations preserve trace class at this fixed $s$ by the min–max eigenvalue inequality. The bounded-perturbation Dyson series converges in trace norm: multi-factor Schatten Hölder bounds its $k$th term by $Z_r(s\|V\|)^k/k!$. Thus no trace-class assumption at smaller times is needed. Duhamel differentiation in trace class gives

$$\frac{dX_r}{dr}=-\int_0^s e^{-(s-t)A_r}V e^{-tA_r}\,dt.$$

Schatten–Hölder, with exponents $s/(s-t)$ and $s/t$, implies $\|X'_r\|_1\le s\|V\|Z_r$, including the endpoint limits. Differentiating $Z_r$ under the trace gives $|Z'_r|\le s\|V\|Z_r$. Hence

$$\left\|\frac{d}{dr}(X_r/Z_r)\right\|_1\le2s\|V\|.$$

Normalized Gibbs states are unchanged by adding a scalar to their Hamiltonian. Replace $V$ with $V-cI$, where $c=(\sup\sigma(V)+\inf\sigma(V))/2$, to obtain $2s\|V-cI\|=s\operatorname{osc}(V)$. Integrate $r\in[0,1]$ and combine with the trivial **unhalved trace-norm** ceiling 2. Under the conventional operational convention the resulting bound reads $T(\rho_{A+V}(s),\rho_A(s))\le\min\{1,\tfrac{s}{2}\operatorname{osc}(V)\}$. $\square$

For $V=cI$, the distance is exactly zero, an essential test that a bound phrased solely in terms of $\|V\|$ conceals. For the moving family $V_\gamma=c\gamma^{-1/3}K_\gamma$ with $\sup_\gamma\|K_\gamma\|\le K$, $u>0$, at $s_\gamma=u\gamma^{-2/3}$ the theorem yields

$$\boxed{\|\rho_{A_\gamma+V_\gamma}(s_\gamma)-\rho_{A_\gamma}(s_\gamma)\|_1\le 2u|c|K\,\gamma^{-1}.}$$

An order-one unnormalized perturbation would be compatible with this bound if the relevant heat trace grew as $\Theta(\gamma)$; that moving-scale estimate for $A_\gamma$ is not proved here. For the diagonal reference $L$, the estimate follows by the Riemann sum used in §6. No spectral multiplicity estimate is required for the normalized bound itself.

## 6. Exact normalized ultraviolet sharpness on a moving projection

This independent model theorem shows that the $1/\gamma$ order in Theorem 4 can occur, without using the model-specific $I_n(\gamma)$ expansion. Work on $\mathcal H_f=\bigoplus_{n\ge1}\mathbb C^{n^2}$ with $L|_n=(n^2-1)/2$, and set $\Pi_\gamma=\mathbf1_{\{n\ge\lceil x_0\gamma^{1/3}\rceil\}}$ for a fixed $x_0>0$. For $u,c>0$, put $V_\gamma=c\gamma^{-1/3}\Pi_\gamma$ and $s_\gamma=u\gamma^{-2/3}$. Then $V_\gamma$ is bounded, commutes with $L$, tends to zero in norm, and eventually vanishes on each fixed representation block. Writing
$$ p_\gamma=\frac{\operatorname{Tr}(\Pi_\gamma e^{-s_\gamma L})}{\operatorname{Tr}(e^{-s_\gamma L})},\qquad t_\gamma=e^{-uc/\gamma}, $$
the disjoint spectral supports give the **exact finite-$\gamma$ trace-norm identity**
$$ \boxed{\|\rho_{L+V_\gamma}(s_\gamma)-\rho_L(s_\gamma)\|_1=\frac{2p_\gamma(1-p_\gamma)(1-t_\gamma)}{1-p_\gamma+p_\gamma t_\gamma}.} $$
The Riemann-sum limit is
$$ p_\gamma\to p=\frac{\int_{x_0}^\infty x^2e^{-ux^2/2}\,dx}{\int_0^\infty x^2e^{-ux^2/2}\,dx}\in(0,1),\qquad\boxed{\gamma\|\rho_{L+V_\gamma}-\rho_L\|_1\to2ucp(1-p)>0.} $$
This proves **achievability of the normalized rate order** on a simple diagonal reference model. It neither establishes a sharp universal constant for Theorem 4 nor establishes the unproved noncommuting construction target in §4.

## 7. Positive spectral measures at fixed semigroup time

For fixed $\gamma,s_0>0$ and representation multiplicities $d_n\in\{1,n^2\}$, set $Z_\gamma(s_0)=\sum_{n\ge1}d_ne^{-s_0a_{\gamma,n}}$ and
$$ \mu_{\gamma,s_0}=\sum_{n\ge1}\frac{d_ne^{-s_0a_{\gamma,n}}}{Z_\gamma(s_0)}\,\delta_{a_{\gamma,n}}. $$
The modified-Bessel power series implies $I_n(\gamma)\le I_0(\gamma)(\gamma/2)^n/n!$ for fixed $\gamma$, so $a_{\gamma,n}$ grows faster than linearly in $n$; the normalization and every polynomial moment are finite. This is a positive probability measure with
$$ \int e^{-tE}\,d\mu_{\gamma,s_0}(E)=\frac{Z_\gamma(s_0+t)}{Z_\gamma(s_0)},\quad t\ge0. $$
The $n=1$ contribution has positive mass at zero, so $\inf\operatorname{supp}\mu_{\gamma,s_0}=0$. This establishes a mathematical instance of the class of positive-measure observation problems, **not** equality with its six benchmark observations, nor a nonzero physical mass gap.

## 8. What survives transfer to a different theory?

Transfer between these results and a finite-volume pure-gauge Wilson lattice construction would require, in order: a specified lattice action and reflection, positivity of the **physical** transfer operator, the gauge-invariant vacuum representation, its spectral multiplicities, a physical time conversion, uniform-in-volume and ultraviolet estimates, and a continuum construction. The compact-group central convolution by itself establishes none of these.

The following concepts are mathematically distinct: a positive type class function versus full lattice reflection positivity; class functions versus the full regular representation; bounded perturbation norm versus moving trace norm; strong versus norm-resolvent versus trace-class convergence; unnormalized heat operators versus normalized trace states.

## References

1. National Institute of Standards and Technology, *Digital Library of Mathematical Functions*, §§10.29, 10.32.2, 10.40.1 and 10.41 (modified-Bessel recurrence, positive integral representation, fixed-order large-argument expansion and large-order asymptotics), https://dlmf.nist.gov/10.32 and https://dlmf.nist.gov/10.40.

2. B. C. Hall, *Lie Groups, Lie Algebras, and Representations: An Elementary Introduction*, 2nd ed., Springer, 2015, doi:10.1007/978-3-319-13467-3.

## Acknowledgments and AI-assisted research

Kirtus Justus provided research direction, the scientific questions, the supplied mathematical materials, and requirements for critical evaluation. ChatGPT (OpenAI) assisted with mathematical checking, manuscript preparation, and editorial examination. Additional AI systems used in the research program include Claude (Anthropic), Gemini (Google), Grok (SpaceXAI), and DeepSeek (High-Flyer). No particular proof, numerical calculation, or independent review is attributed to those systems without supporting records. AI systems are not listed as authors; responsibility for the submitted scholarly claims rests with the named author. The acknowledgment does not imply endorsement by any AI provider or independent peer review.
