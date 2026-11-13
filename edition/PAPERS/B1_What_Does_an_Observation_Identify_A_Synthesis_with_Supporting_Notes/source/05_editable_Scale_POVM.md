# Scale POVM

## 1. Postulates, definitions, and source of each premise

**P1 (supplied graph).** The one-particle input space is \(\mathbb C^n\) with specified orthonormal port labels \(e_i\). Its real symmetric operator \(L\) is the Laplacian of a connected positively weighted graph. Therefore \(L\succeq0\), \(\ker L=\operatorname{span}\{\mathbf1\}\), and \(L_{ij}\leq0\) for \(i\ne j\). Let \(P_0=\mathbf1\mathbf1^T/n\), \(Q=I-P_0\), and \(K=L^+\).

**P2 (supplied measurement).** A one-photon scale-register POVM has a separate zero-mode outcome \(P_0\), and positive-scale POVM density \(\Pi(ds)=4sL^2e^{-2sL}\,ds\), \(s>0\). This is the ideal spectral Calderón analysis measurement. Its abstract passive isometric realization is mathematical; no physical continuous-scale apparatus is claimed to have been constructed.

**P3 (restricted preparations).** For a specified pair of ports \(i\ne j\), two possible input density operators \(\rho_A,\rho_B\) are supported in \(\operatorname{span}\{e_i,e_j\}\) and have identical diagonal populations. Their off-diagonal coherence, phase noise, and purity are not specified. Input relative phase is *not* calibrated. Both preparations are probed with the same normalized POVM and detector calibration.

**P4 (statistics).** For finite-sample statements, preparations are repeated independently, with independently specified bounds on source spectral gap, scale readout, and detector efficiencies. The distinction between calibrated physical time and mathematical filter resolution is retained throughout.

These postulates import Hilbert space, graph, measurement, input basis and quantum preparation. None is derived from prephysical hypotheses.

## 2. Elementary moment lemma

**Lemma 1.** For every integer \(k\geq1\),

\[
P_0+\int_0^\infty\Pi(ds)=I,\qquad
\int_0^\infty s^k\Pi(ds)=\frac{(k+1)!}{2^k}K^k.
\]

**Proof.** For a positive spectral eigenvalue \(\lambda\), the positive-scale measure has density \(4\lambda^2s e^{-2\lambda s}\). The first identity is \(\int_0^\infty4\lambda^2s e^{-2\lambda s}ds=1\). For integer \(k\geq1\),
\[
4\lambda^2\int_0^\infty s^{k+1}e^{-2\lambda s}ds
=\frac{(k+1)!}{2^k\lambda^k}.
\]
The zero eigenvalue contributes zero to the positive-scale integrals. The spectral theorem proves the result. \(\square\)

A reported *unconditional* scale mean is \(\mu(\rho)=\int_0^\infty s\operatorname{Tr}(\rho\Pi(ds))=\operatorname{Tr}(\rho K)\). If a detector instead reports only the conditional mean among positive-scale events, the physically correct conversion is
\[
\mu(\rho)=\bigl(1-\operatorname{Tr}(\rho P_0)\bigr)\,\mathbb E[s\mid s>0].
\]
Failing to apply this factor biases the proposed reconstruction whenever zero-mode clicks occur.

## 3. Self-calibrated off-diagonal pseudoinverse

**Theorem 2 (phase-contrast ratio).** Under P1–P3, define the measured zero-port probabilities \(p_X=\operatorname{Tr}(\rho_XP_0)\) and unconditional first scale moments \(\mu_X=\operatorname{Tr}(\rho_XK)\) for \(X=A,B\). If \(p_A\ne p_B\), then
\[
\boxed{K_{ij}=\frac{\mu_A-\mu_B}{n(p_A-p_B)}.}
\]
No calibration of the relative phase or even of the individual port populations is necessary, provided the populations are the same for the two preparations.

**Proof.** Equal diagonals imply \(\rho_A-\rho_B=z|i\rangle\langle j|+\bar z|j\rangle\langle i|\) for some \(z\in\mathbb C\). Since \(K\) is real symmetric,
\[
\mu_A-\mu_B=2\operatorname{Re}(z)K_{ij}.
\]
Since \((P_0)_{ij}=1/n\),
\[
p_A-p_B=2\operatorname{Re}(z)/n.
\]
The asserted ratio follows when its denominator is nonzero. \(\square\)

**Corollary 3 (electrical resistance and full reconstruction).** Independently prepare the known basis states \(e_i\) and \(e_j\), obtaining \(\mu_i=K_{ii}\) and \(\mu_j=K_{jj}\). The exact electrical resistance is
\[
\boxed{R_{ij}=\mu_i+\mu_j-\frac{2(\mu_A-\mu_B)}{n(p_A-p_B)}.}
\]
If this experiment can be performed for every labeled pair with nonzero contrast, all entries of \(K\) are determined and \(L=K^+\) follows. A direct implementation uses \(n\) single-site preparations and two population-matched pair preparations for each unordered pair, totaling \(n^2\) preparation settings. This is a sufficient, not a proven minimal, count for this calibration-light protocol.

**Concrete coherent/dephased implementation.** Let \(p_i+p_j=1\) and prepare an arbitrarily phase-imperfect pair \(\psi=\sqrt{p_i}e_i+e^{i\phi}\sqrt{p_j}e_j\). Compare it with its fully dephased state \(\rho_D=p_i|i\rangle\langle i|+p_j|j\rangle\langle j|\). These have the same populations, and \(p_D=1/n\) regardless of the unknown populations. Provided \(p_{\rm coh}\ne 1/n\),
\[
K_{ij}=\frac{\mu_{\rm coh}-\mu_D}{np_{\rm coh}-1}.
\]
The same statement holds for an arbitrary phase-drift ensemble, because both outputs depend only on the averaged real coherence.

**Nonidentifiability boundary.** If \(p_A=p_B\), the two corresponding measurement differences vanish in the same real-coherence direction. The ratio is undefined. The two observations alone do not reconstruct \(K_{ij}\). Further independent preparation settings can supply a nonzero contrast.

## 4. Finite scale-window and readout resolution

Suppose a physical register records only \(a\leq s\leq b\), where \(0\leq a<b<\infty\), and assume the independent spectral enclosure \(\lambda_2(L)\geq\underline\lambda>0\) and \(\lambda_{\max}(L)\leq\overline\lambda\).

**Lemma 4 (uniform moment-loss bound).** If \(\widetilde\mu(\rho)=\int_a^b s\operatorname{Tr}(\rho\Pi(ds))\), then for every normalized input state
\[
0\leq\mu(\rho)-\widetilde\mu(\rho)\leq
\boxed{B_{a,b}=\frac43\overline\lambda^{\,2}a^3+
\frac{e^{-2\underline\lambda b}}{\underline\lambda}
\bigl(1+2\underline\lambda b+2\underline\lambda^2b^2\bigr).}
\]
If the observed scale is replaced by a midpoint of a bin of maximum width \(h\), add \(h/2\) to this bound.

**Proof.** For each positive eigenvalue, the missing low-scale first moment is bounded by \(4\lambda^2\int_0^a s^2ds\leq4\overline\lambda^2a^3/3\). The omitted upper tail is exactly
\[
4\lambda^2\int_b^\infty s^2e^{-2\lambda s}ds
=\frac{e^{-2\lambda b}}{\lambda}(1+2\lambda b+2\lambda^2b^2).
\]
The right-hand side decreases with \(\lambda>0\), so it is bounded by its value at \(\underline\lambda\). Spectral weights are nonnegative and sum to at most one on the positive subspace. Binning contributes at most \(h/2\) per photon. \(\square\)

**Corollary 5.** Using the exact zero-mode contrast \(d=p_A-p_B\ne0\) and finite-window scale moments in Theorem 2 gives
\[
|\widetilde K_{ij}-K_{ij}|\leq \frac{2(B_{a,b}+h/2)}{n|d|}.
\]
This is a deterministic approximation bound. It assumes no unmodelled detector loss, and the scale moment must be normalized by *injected* photon number or separately correct for events outside the monitored window.

## 5. Statistical conditioning and explicit finite-sample error

Let each of the four preparations \(e_i,e_j,\rho_A,\rho_B\) have \(M\) independent trials. A scale observation includes an atom at \(s=0\) for the zero port. With \(\lambda_2\geq\underline\lambda\), Lemma 1 gives
\[
\mathbb E[s^2]\leq\frac3{2\underline\lambda^2},\qquad
\operatorname{Var}(s)\leq\frac3{2\underline\lambda^2}.
\]
Hence the union bound, Chebyshev, and Hoeffding imply that all four empirical first moments have absolute error at most \(\eta\) and the two relevant zero-port frequencies have absolute error at most \(\delta\), except with probability at most
\[
\boxed{\frac{6}{M\underline\lambda^2\eta^2}+4e^{-2M\delta^2}.}
\]
These are conservative, not optimal, statistical guarantees.

**Theorem 6 (ratio stability).** On that event, let \(d=|p_A-p_B|>2\delta\). The empirical ratio \(\widehat K_{ij}=(\widehat\mu_A-\widehat\mu_B)/[n(\widehat p_A-\widehat p_B)]\) obeys
\[
\boxed{|\widehat K_{ij}-K_{ij}|\leq
\frac{2\eta/n+2\delta/\underline\lambda}{d-2\delta}.}
\]
The derived effective-resistance estimator obeys
\[
\boxed{|\widehat R_{ij}-R_{ij}|\leq2\eta+
\frac{4\eta/n+4\delta/\underline\lambda}{d-2\delta}.}
\]

**Proof.** Let \(h=\mu_A-\mu_B=ndK_{ij}\) with the sign of \(d\) retained when dividing. Its empirical perturbation is at most \(2\eta\), and the zero-mode contrast perturbation is at most \(2\delta\). Use
\[
\widehat K_{ij}-K_{ij}=\frac{(\widehat h-h)-nK_{ij}(\widehat d-d)}{n\widehat d}
\]
and \(|K_{ij}|\leq\|K\|_{\rm op}\leq1/\underline\lambda\). The resistance bound follows by adding the two diagonal mean errors. \(\square\)

These bounds explain why phase calibration can be replaced by *observable* contrast calibration only if the actual contrast is statistically separated from zero.

## 6. Exact statistical refinement for the rook versus Shrikhande testbench

For the fixed plus-state input on two known ports adjacent in the rook graph and nonadjacent in the Shrikhande graph, the positive-scale densities are
\[
p_E(s)=32s e^{-8s}+96s e^{-16s},\quad
p_N(s)=16s e^{-8s}+160s e^{-16s},
\]
with the same zero-port mass \(1/8\). Their likelihood ratio is
\[
\frac{p_E(s)}{p_N(s)}=\frac{2e^{8s}+6}{e^{8s}+10},
\]
strictly increasing for \(s>0\), and equals one at \(s_*=\log2/4\).

**Proposition 7 (one-bit sufficiency for the single-shot optimal *classical* decision).** The indicator \(X=\mathbf1\{s>s_*\}\), setting \(X=0\) for zero-port outcomes, captures the full single-shot total-variation distance of the ideal classical scale-counting distributions:
\[
\begin{aligned}
p_E&=\Pr_E(X=1)=\frac{19+22\log4}{128},\\
p_N&=\Pr_N(X=1)=\frac{13+18\log4}{128},\\
\operatorname{TV}(P_E,P_N)&=p_E-p_N=\frac{3+2\log4}{64}\simeq0.090196698785.
\end{aligned}
\]

**Proof.** The density difference changes sign exactly once, at \(s_*\). By the classical Neyman–Pearson characterization, its positive region is the optimal single-shot decision set. The gamma(shape 2, rate \(2\lambda\)) survival function is \((1+2\lambda s)e^{-2\lambda s}\); substituting at \(s_*\) yields the displayed probabilities. \(\square\)

For \(M\) independent photons, retain only the binary outcomes, and perform the exact binomial likelihood-ratio test. The smallest integer \(M\) for which this *particular* equal-prior test has error \(\leq0.1\) is **181 photons**; the exact error at 181 is approximately \(0.09947986615\). At 180 photons it is \(0.10012764629\). A direct Hoeffding-based sufficient count is 567 photons. This improves the earlier, much looser 960-photon Chebyshev certificate without asserting optimality among collective quantum measurements of the full scale-register states.

The binary threshold is for the exactly specified *plus* input and calibrated graph pair; it is not an invariance under unknown phase drift. For drift-robust effective-resistance reconstruction, use Theorem 2 and its calibration readouts.
