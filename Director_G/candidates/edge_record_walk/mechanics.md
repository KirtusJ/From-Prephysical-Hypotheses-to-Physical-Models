# A free particle on the signed line

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The integer walk used to calibrate its detector also has a free Schrödinger envelope and a limit in which its terminal position concentrates on a Newtonian ray. The dynamics uses the same two oriented ports and four signed arcs at each site. The mechanical statements require a family of extended preparations and a detector whose response transfers from the calibration source to those preparations.

### From the sharp source to an extended source

Let \(A\) be the raw signed step. In each block it sends incoming integers \((r,l)\) to \((r+l,r-l)\) on the two outgoing rails. Distinct blocks have distinct oriented outputs. Thus \(A^TA=2I\), and \(U=A/\sqrt2\) is unitary on the complexified line space and orthogonal on its real part. For the sharp launch, the frontier balance theorem fixes the common response \(f(n)=f(1)n^2\) under its stated assumptions. For a finitely supported coherent integer source \(h\ne0\), suppose the **same** response to the absolute signed total applies at every terminal port. Normalization then gives the finite prediction

\[
 \Pr_t(x,c\mid h)=\frac{|(A^t h)(x,c)|^2}{2^t\sum_{y,d}|h(y,d)|^2}.
\]

This formula can fail if the detector distinguishes preparation contexts with the same signed total or if the source keeps distinguishable records of its separate inputs. Sharp-launch measurements do not determine those behaviors. Free waiting after a localized launch preserves the uniform total momentum density because each Fourier fibre evolves unitarily. It therefore cannot prepare the narrow band used below. [Sharp calibration in Lean](EdgeRecords.lean) · [Preparation from localized inputs](../../Base_preparation_and_two_rays.md)

A finite test compares preparations with equal initial oriented-port probabilities. Prepare \(h_+=(1,1)\) or \(h_-=(1,-1)\) at the same site on its two incoming rails. At the next tick their raw outputs are \((2,0)\) and \((0,2)\). An incoherent equal mixture of the two sharp rails gives \((1/2,1/2)\) as terminal probabilities. With verified relative sign, coherent preparation and stable detector settings, a departure from the respective sharp predictions rejects the common source and detector assumptions even if every localized-launch frontier calibration succeeds. An apparatus capable only of preparing localized inputs has yet to implement this test.

### The free Schrödinger envelope

Take the Fourier transform with kernel \(e^{-ikx}\). Then

\[
 U(k)=\operatorname{diag}(e^{-ik},e^{ik})\,2^{-1/2}
 \begin{pmatrix}1&1\\1&-1\end{pmatrix},
 \qquad \lambda_+(k)=e^{-i\omega(k)},\quad
 \sin\omega(k)=\frac{\sin k}{\sqrt2},
 \quad -\pi/4\le\omega\le\pi/4 .
\]

At \(k_*=-\pi/2\), \(\omega_*=-\pi/4\), \(\omega'=0\) and \(\omega''=1\). Select a normalized smooth positive-band eigenvector \(u(k)\) near this point, with \(u(k_*)=(1,-i)/\sqrt2\). Encode a normalized scalar Fourier envelope \(f(p)\), supported in \(|p|\le P\), by \(\widehat\psi(k_*+\delta p)=\delta^{-1/2}f(p)u(k_*+\delta p)\), using compatible Fourier measures. The complex representation labels a band of the real signed update. It introduces no flight phases on the arcs.

Writing \(q=k-k_*\), differentiation gives \(\omega'(k_*+q)=\sin q/\sqrt{1+\sin^2 q}\). For \(|q|\le1\), the difference from \(q\) is at most \(2|q|^3/3\). Integration bounds the difference of the phase from \(\omega_*+q^2/2\) by \(|q|^4/6\). With site scale \(Y=\varepsilon\delta x\), tick duration \(\varepsilon\delta^2\), and attained time \(T=n\varepsilon\delta^2\), the operator-norm error on the selected band between the demodulated walk and the encoded multiplier \(e^{-iTp^2/(2\varepsilon)}\) is at most

\[
 \frac{T\delta^2P^4}{6\varepsilon},\qquad \delta P\le1.
\]

For fixed \(\varepsilon>0\), \(\delta\to0\), this yields \(i\varepsilon\partial_T f=-\varepsilon^2\partial_Y^2 f/2\) in position representation. Smooth vector phases are a choice of section. Rephasing \(u(k)\) requires the inverse phase on its scalar coefficient to represent the same prepared state. The scale choices give dimensionless mass one. Dimensional mass, action, lattice spacing and tick duration require a physical calibration. The leading envelope equation for extended coined walks was previously derived by de Valcárcel, Roldán and Romanelli, Eq. (11). [Program proof and error bound](../../Signed_walk_and_weak_field.md) · [Primary publication](https://doi.org/10.1088/1367-2630/12/12/123022)

### A real preparation and a growing ring

Let \(C\psi(x,c)=\overline{\psi(x,c)}\). The two unit vectors \(\psi\) and \(C\psi\) have disjoint Fourier supports near \(-\pi/2\) and \(+\pi/2\) when \(\delta P\) is sufficiently small. Hence \(r=(\psi+C\psi)/\sqrt2\) is a **normalized real source**. The real walk commutes with \(C\) and preserves each Fourier support. For fixed \(\xi\), the position observable \(M_\xi=e^{i\xi\varepsilon\delta X}\) shifts momentum by \(\xi\varepsilon\delta\) up to sign. When \(2\delta P+|\xi|\varepsilon\delta<\pi\), the two cross terms in \(\langle U^nr,M_\xi U^nr\rangle\) vanish. The diagonal terms agree since conjugation leaves each site intensity unchanged. The real and complex preparations therefore have the same macroscopic position characteristic function at this \(\xi\), throughout flight.

At a single lattice port the real intensity also contains \(\operatorname{Re}[(U^n\psi)(x,c)^2]\). Multiplying the computational \(\psi\) by a global phase changes this quadrature term and can change the microscopic source and detector readings. The macroscopic equality follows from the separated supports for any such fixed quadrature. A sharp source confined to one site parity has corresponding Fourier amplitudes tied under a shift by \(\pi\). Selecting a single complex chart or imposing the real quadrature on an arbitrary packet requires control over the extended source. Subsampling one position parity or resolving alternating-site fringes at the detector can retain the cross terms.

For implementation on a finite signed ring, approximate \(r\) in \(\ell^2\) by truncating its support, approximating its retained real entries by rationals, and normalizing. Clearing a common denominator gives a finite integer vector \(h\) with \(h/\|h\|\) equal to the normalized rational direction. Such directions approximate \(r\) arbitrarily well, also when the initial packet varies with scale. If the support has diameter \(W\), choose an even ring with \(N>W+2n+2\) and place the cut outside its propagation cone. Through tick \(n\) the finite and line evolutions of the truncated source agree exactly in that cone. An initial norm error \(\eta\) contributes at most \(2\eta\) to expectations of operators of norm at most one, by unitarity. This establishes existence along growing rings. It gives no native preparation protocol or uniform bound on register size. A fixed four-site ring has only four momenta.

### The classical terminal record

Choose a smooth compactly supported normalized \(g\) and the scalar initial packet
\[
 f_\varepsilon(p)=\varepsilon^{-1/4}g((p-p_0)/\sqrt\varepsilon)
                         e^{-iY_0p/\varepsilon}.
\]
Take \(\varepsilon\to0\), \(\delta\to0\), \(\delta^2/\varepsilon\to0\) and bounded attained times tending to \(T\). The free multiplier translates the position centre to \(Y_0+p_0T\). At attained time \(s\) its root-mean-square deviation about \(Y_0+p_0s\) is at most \(\sqrt\varepsilon(\|g'\|_2+s\|p g(p)\|_2)\) by differentiating in momentum. The lattice estimate above and smoothness of \(u(k)\) transfer this conclusion for each bounded position characteristic function. Thus **the terminal position law converges weakly to a point mass at \(Y_0+p_0T\)**, also for the integer approximations with \(\eta\to0\). The scalar momentum is the momentum measured relative to the carrier in its selected chart. A momentum analysis of the full real preparation sees both conjugate charts. [Position-limit proof at zero force](../../Forced_envelope_and_classical_motion.md)

Each observation concerns a fresh launch and one terminal time. Repeated observation on a single flight requires an instrument and a state-update rule. The derived motion concerns a free particle in one space dimension. Interactions, higher-dimensional motion and the physical origin of signed propagation, clock, source and detector remain open.
