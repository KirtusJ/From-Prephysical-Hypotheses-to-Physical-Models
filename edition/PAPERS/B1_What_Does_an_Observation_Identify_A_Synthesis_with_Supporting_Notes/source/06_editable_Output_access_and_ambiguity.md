# Output access and ambiguity

## 2. Postulates and two different observation contracts

**P1.** A scalar positive parameter \(\lambda\) is a *supplied* eigenvalue of a supplied real graph generator. The experimenter can prepare its known input eigenmode. This is not derived from prephysical hypotheses.

**P2.** For calibrated positive scales \(s,t\), the two monitored Ricker signal amplitudes are
\[
 f_s(\lambda)=s\lambda e^{-s\lambda},\qquad f_t(\lambda)=t\lambda e^{-t\lambda}.
\]
Because \(0\le f_u\le e^{-1}\), the two-signal amplitude stack is passive, with a complementary amplitude
\[
 h(\lambda)=\sqrt{1-f_s(\lambda)^2-f_t(\lambda)^2}>0.
\]

**P3.** A real coherent source amplitude \(a\ne0\), with mean input photon number \(E=a^2\), is unknown but common to both signal paths. Phase-calibrated homodyne produces means \(\sqrt2 a f_j\), vacuum variance \(1/2\), independently across distinct canonical output modes. The source and ancillary modes are quantum *inputs*, not derived entities.

**Contract M (monitored-only):** measure the two signal output ports. The third complementary port is discarded.  
**Contract F (full-output):** also measure the complementary canonical port. A physical device must supply the required access, phase reference and sufficiently low excess noise. A mathematical isometric dilation does not independently implement the device.

## 3. Reconfirmation: original two-monitored-port global optimum

Let \(x=s\lambda\), \(y=t\lambda\), \(f(z)=ze^{-z}\), and \(g(z)=z(1-z)e^{-z}\). In Contract M, eliminating the unknown source amplitude by a Schur complement gives
\[
 \mathcal I^{M}_{\lambda\mid a}=\frac E{\lambda^2}\,\mathcal C_M(x,y),\qquad
 \mathcal C_M(x,y)=\frac{4x^2y^2e^{-2(x+y)}(y-x)^2}{x^2e^{-2x}+y^2e^{-2y}}.
\]
The analysis proves global uniqueness up to exchanging the two scales by reducing the stationary equations to the unique root \(u\in(0,1)\) of
\[
 3\log\frac{1+u}{1-u}-\log u-2(u+u^{-1})=0,
\]
whose derivative is strictly positive on the interval. The maximizing scales are
\[
\begin{aligned}
 x_M&=0.4121145890889544\ldots,\\ y_M&=2.7010117642659317\ldots,\\
 \mathcal C_M&=0.4780676701094133\ldots.
\end{aligned}
\]
The reported bracketing and differential-evolution calculations agree. This is a *global statement only within Contract M*, with the known source mode, two scale settings, calibrated phase and unit vacuum noise, not a universal quantum Fisher optimum.

## 4. Theorem 1: full-output amplitude nuisance decouples

**Statement.** Let \(f(\lambda)\in\mathbb R^m\) be a continuously differentiable passive signal vector with \(\|f\|^2<1\). Append \(h(\lambda)=\sqrt{1-\|f(\lambda)\|^2}\), and measure all \(m+1\) output modes through the phase-calibrated homodyne contract P3. Put \(v=(f,h)\). Then
\[
 \boxed{\mathcal I_{a\lambda}=0,\qquad
 \mathcal I^{F}_{\lambda\mid a}=4E\left(\|f'\|^2+
 \frac{(f^Tf')^2}{1-\|f\|^2}\right).}
\]
The right-hand side is also the pure-coherent-state quantum Fisher information for this real-displacement family; complete homodyne achieves it within the specified model.

**Proof.** The homodyne mean vector is \(\sqrt2 a v\) and its covariance is \(I/2\), independent of both parameters. Thus the Fisher matrix is four times the Euclidean Gram matrix of \(v\) and \(a v'\). The identity \(\|v\|^2=1\) implies \(v^Tv'=0\), making the amplitude/parameter cross term vanish. Differentiation of \(h\) gives \(h'=-f^Tf'/h\); substitute in \(\|v'\|^2\). The known formula for QFI of real coherent displacements gives the same \(4E\|v'\|^2\). □

**Numerical design comparison.** For the Ricker case with two signal ports, \(f=(w_s,w_t)\),
\[
 \mathcal I^F_{\lambda\mid a}=\frac E{\lambda^2}\mathcal C_F(x,y),
\quad
\mathcal C_F=4\left[g(x)^2+g(y)^2+\frac{(f(x)g(x)+f(y)g(y))^2}{1-f(x)^2-f(y)^2}\right].
\]
At the original Contract M maximizer, \(\mathcal C_F=0.484225125\ldots\). At equal scaled settings \(x=y\approx2.5212816\), a separate one-dimensional numerical maximization gives \(\mathcal C_F\approx0.827935853\). This numerical maximization is restricted to equal scales. The unrestricted proof is given in the full-output design supplement. For comparison, if Contract M uses equal scales, its nuisance-adjusted Fisher information is exactly zero because both signal means are proportional to the unknown amplitude.

The complement's accessibility fundamentally changes the estimation contract. Its contribution is not an automatic free measurement.

## 5. Theorem 2: high local Fisher information can coexist with exact global aliasing

**Statement.** At equal scales \(s=t\), the full-output model is not globally injective in \(\lambda>0\). Any amplitude \(0<f<e^{-1}\) occurs at exactly two positive scaled eigenvalues
\[
 x_-=-W_0(-f)\in(0,1),\qquad x_+=-W_{-1}(-f)>1.
\]
The full accessible output states coincide exactly for the pair \(\lambda_-=x_-/s\), \(\lambda_+=x_+/s\), with the same coherent input amplitude. At the numerically locally optimized equal scale, the alias pair is
\[
 x_+\approx2.5212815653,\qquad x_-\approx0.2637461880,
\qquad f\approx0.202601510.
\]

**Proof.** The function \(x\mapsto xe^{-x}\) is strictly increasing on \((0,1)\), strictly decreasing on \((1,\infty)\), and equals \(e^{-1}\) at \(x=1\). At the two solutions, the two monitored amplitudes both equal \(f\), while the complement amplitude equals \(\sqrt{1-2f^2}\) in both models. All accessible output coherent-state factors, including their vacuum noise, are thus identical. □

This is global parameter nonidentifiability, not merely a weak statistical signal. A local Fisher matrix alone cannot exclude a disconnected competing parameter value.

## 6. Theorem 3: splitting nearly equal scales restores uniqueness with a quadratic alias cost

Fix an alias pair \(x_+>1>x_-\) satisfying \(f(x_+)=f(x_-)=f\), put \(s\lambda_\pm=x_\pm\), and set \(t=s(1+\delta)\). Let \(g(x)=x(1-x)e^{-x}\).

**Exact uniqueness for \(\delta\ne0\).** For a nonzero common input amplitude and calibrated signal ports,
\[
 \frac{f_s(\lambda)}{f_t(\lambda)}=\frac st e^{(t-s)\lambda},
\]
which is strictly monotone in \(\lambda\) if \(s\ne t\). Thus the two-scale ideal mean vector is injective up to the unknown amplitude, whereas it is not so for equal scales.

**Asymptotic discrimination cost.** Let
\[
 v_\pm(\delta)=\left(f(x_\pm),\ f((1+\delta)x_\pm),\ \sqrt{1-f(x_\pm)^2-f((1+\delta)x_\pm)^2}\right).
\]
Then, as \(\delta\to0\),
\[
 \boxed{\|v_+(\delta)-v_-(\delta)\|^2
 =C_{\mathrm{alias}}\delta^2+O(\delta^3),\quad
 C_{\mathrm{alias}}=[g(x_+)-g(x_-)]^2\frac{1-f^2}{1-2f^2}>0.}
\]
**Proof.** The first amplitude is exactly equal in the two alternatives. The second differs to first order by \(\delta[g(x_+)-g(x_-)]\). Differentiation of the square-root complement produces \(-f/\sqrt{1-2f^2}\) times this first-order difference. Sum the two nonzero squared components. Positivity holds because \(g(x_+)<0<g(x_-)\). □

For a fixed, known coherent amplitude with input energy \(E\), the squared overlap of the two full-output pure coherent states is exactly \(\exp[-E\|v_+-v_-\|^2]\). The equal-prior Helstrom error is at most 10% only if
\[
 E\ge\frac{-\log(0.36)}{\|v_+-v_-\|^2}
 \sim \frac{-\log(0.36)}{C_{\mathrm{alias}}}\delta^{-2}.
\]
At the locally optimized equal-scale point, numerical evaluation yields \(C_{\mathrm{alias}}\approx0.2185515\), giving a leading photon requirement near \(4.67\delta^{-2}\). The exact threshold for \(\delta=0.01\) is about 47,134 photons. This comparison is for two specified alternative devices and fixed input energy; an unknown source amplitude or additional nuisance parameters cannot be assumed to improve the discrimination guarantee.

**Interpretation.** Under Contract F, a pair of very similar scales can be locally efficient yet costly for rejecting a distant Lambert-W alias. Under Contract M, the two distinct scales in the original audited global Fisher optimum avoid this specific alias while estimating an unknown amplitude. The designs optimize different scientific tasks. The mathematical tension is between local statistical curvature and global uniqueness, not between quantum theory and classical probability.
