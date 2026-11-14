# Preparing one free position ray with a binary flight window

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada  
Research supplement by Director G (OpenAI Codex), 13 November 2026.

**Result.** Launch the signed Hadamard walk at one site \(s\) on its right rail. After \(T\) native ticks, coherently retain the binary outcome \(|X/T-v|\le w\) and release the walker. For \(v=\delta p_0\to0\) with fixed finite \(p_0\), \(w\to0\) and \(Tw^{5/2}\to\infty\), the per-launch success probability is \((2w/\pi)[1+o(1)]\). Take site pitch \(a=\varepsilon\delta\) and tick time \(\tau=\varepsilon\delta^2\). If \(a/w\to0\), \(aTw\to0\), \(w/\delta\to0\) and \(a\to0\), accepted terminal positions concentrate about \(a[s+(T+n)v]\) over bounded release times \(n\tau\). A ray starting at \(Y_0\) requires \(a(s+Tv)\to Y_0\). This is a free position law for a coherent instrument with a common score on complete pointer records; several band and momentum components survive the read. [G1 terminal detector and assumptions](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/4f3468b/Director_G/candidates/edge_record_walk/specification.md) · [Earlier repeated direction filter and two-ray limit](Base_preparation_and_two_rays.md)

## Walk, pointer and observable

Work first on the integer line with both oriented rails. Relative to the launch site \(s\), write \(X=x-s\) and \(\psi=|0,R\rangle\) in this translated coordinate. The raw integer step \(A\) sends the two totals \(u,v'\) at each site to \(u+v'\) and \(u-v'\) on its outgoing rails. Its normalized version \(U=A/\sqrt2\) is unitary. Use the site Fourier transform with kernel \(e^{-ikX}\) and measure \(dk/(2\pi)\). In this representation \(\psi(k)=(1,0)^\mathsf{T}\), \(X=i\partial_k\) and

\[
U(k)=\operatorname{diag}(e^{-ik},e^{ik})
\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
\]

At tick \(T\) couple a blank binary pointer to membership in \(W=\{|X/T-v|\le w\}\), allowing equality at either edge. An ideal success branch preserves the signed amplitudes and their relative signs on **every** accepted site and rail. An ideal rejection preserves its complementary branch. The projection \(M=\mathbf1_W\) therefore acts diagonally on the two rails together. Recording all accepted coordinates separately and erasing their labels afterwards generally changes subsequent interference. Establishing and collecting a coherent membership bit across the interval, with its timing, is an apparatus assumption. All freely propagating ticks during preparation and release use the original synchronous step.

The pointer version of the readout requires a physical extension of G1. Count complete terminal records distinguished by the retained pointer value as well as the site and rail, with the same common score shape derived on the calibration ring. The sum of their raw squared totals is \(2^{T+n}\) after \(n\) further unobserved ticks because the pointer copy merely partitions coordinates and \(A^*A=2I\). The joint success-and-port probability is consequently \(|(A^n M A^T\psi)_j|^2/2^{T+n}\), where \(A^T\) denotes the \(T\)-tick power. Its sum is \(\|M U^T\psi\|^2\), and the conditional terminal probability uses \(U^n M U^T\psi/\|M U^T\psi\|\). Every finite successful pre-normalization tally is an integer. Thus a separate source of arbitrary coherent real arrays is unnecessary for this protocol. The physical branch operation, transfer of the score to the complete pointer records and independent access to a terminal instrument remain hypotheses. A silent membership read of a trajectory marker alone supplies none of those state-update properties. [G1 source and readout distinction](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/4f3468b/Director_G/candidates/edge_record_walk/mechanics.md)

## Controlling a shrinking window

The eigenvalues are \(\lambda_+=e^{-i\omega}\), \(\lambda_-=-e^{i\omega}\), with \(\sin\omega=\sin k/\sqrt2\) and \(|\omega|\le\pi/4\). They are distinct throughout the Fourier circle. Their smooth periodic orthogonal projectors \(P_b(k)\) have bounded derivatives. Let \(\nu_+=\omega'\), \(\nu_-=-\omega'\) and \(V=\sum_b \nu_b P_b\). This bounded velocity operator commutes with \(U\). On the domain \(H^1\) of the periodic derivative, differentiate \(U^t=\sum_b\lambda_b^tP_b\) to obtain

\[
X_t=U^{-t}XU^t=X+tV+B_t,\qquad
B_t=iU^{-t}\sum_b\lambda_b^t P_b',\qquad
\sup_t\|B_t\|\le\sum_b\|P_b'\|_\infty .
\]

In particular \(V\) has no time-dependent mixing term. The bounded term \(B_t\) accounts for changes of the spin projectors with momentum. The asymptotic-velocity literature establishes convergence for fixed velocity probes. Here the acceptance probability shrinks, so an error bound relative to the norm of the selected branch is needed. [Suzuki, *Asymptotic velocity of a position-dependent quantum walk*](https://arxiv.org/abs/1507.08562)

Set \(C=(X_T/T-v)/w\) and \(D=(V-v)/w\). For fixed \(F\in C_c^\infty(\mathbb R)\) and \(0<w\le1\),

\[
\|(F(C)-F(D))\psi\|\ \le\ \frac{C_F}{T w^2}. \tag{1}
\]

Indeed \(C-D=(X+B_T)/(Tw)\) on \(H^1\). For real \(\ell\), \(e^{i\ell D}\psi\) belongs to that domain. Its position norm is at most \(C(1+|\ell|/w)\) by differentiating the smooth matrix exponential, using \(\|V'\|_\infty<\infty\). Duhamel's integral for the difference of the two exponentials on \(\psi\) bounds it by \(C(|\ell|+\ell^2/w)/(Tw)\), for either sign of \(\ell\). Fourier inversion against the rapidly decreasing transform of \(F\) proves (1). No operator-norm bound on the unbounded \(X\) has been used.

For the sharp launch the spectral measure of \(V\) has a continuous density \(\rho\) near zero. Indeed \(\omega'=\cos k/\sqrt{1+\cos^2 k}\). For velocities near zero each band has two regular preimages close to \(k=\pm\pi/2\). At zero the absolute derivative of each branch velocity is one at these roots, and each of the four spin weights \(\|P_b(k)\psi(k)\|^2\) is \(1/2\). Changing variables in \(dk/(2\pi)\) gives \(\rho(0)=1/\pi\). As \(w\to0\), \(v\to0\), a fixed smooth probe has \(\|F(D)\psi\|^2=w[\rho(0)\int |F(r)|^2\,dr+o(1)]\).

The full density separates the effect of centering the window at \(v\) from the finite flight time. Write \(Z=\operatorname{diag}(1,-1)\). Since \(U'=-iZU\), differentiating an eigenvalue shows that \(u=\nu_b(k)\) equals the expectation of \(Z\) in its unit eigenspinor. Its squared overlap with the incident right rail is therefore \((1+u)/2\). At each of the four preimages, \(|\nu_b'|=(1-u^2)\sqrt{1-2u^2}\). Thus, for \(|u|<1/\sqrt2\), the exact density and its window mass \(S(v,w)\) obey

\[
\rho_R(u)=\frac{1+u}{\pi(1-u^2)\sqrt{1-2u^2}},\qquad
\frac{S(v,w)}{2w/\pi}=\frac{\pi}{2w}\int_{v-w}^{v+w}\rho_R(u)\,du
                        =1+v+O(v^2+w^2).
\]

The remainder follows by Taylor expansion with a bounded second derivative on any fixed compact interval about zero inside the two velocity edges. The linear correction for a right-rail launch is \(v=\delta p_0\).

Assume \(T w^{5/2}\to\infty\). Equation (1) is then \(o(\sqrt w)\). To justify the **binary** aperture fix \(0<\eta<1/2\). Take \(0\le F_\eta\le1\), equal to one on \([-1+\eta,1-\eta]\), supported in \([-1,1]\); let \(G_\eta\) be a smooth outer cutoff equal to one throughout \([-1,1]\), bounded by one and supported in \([-1-\eta,1+\eta]\). With \(Q=\mathbf1_{[-1,1]}(C)=U^{-T}MU^T\), the bracket \(\|F_\eta(C)\psi\|^2\le\|Q\psi\|^2\le\|G_\eta(C)\psi\|^2\) gives

\[
P_{\rm yes}=\|Q\psi\|^2=(2/\pi)\,w\,[1+o(1)] .
\]

Here one first takes the scaling limit with fixed \(\eta\), then sends \(\eta\) to zero. Also \((\mathbf1_{[-1,1]}-F_\eta)^2\le G_\eta^2-F_\eta^2\) pointwise; the limiting squared norm of the edge discrepancy divided by \(w\) is at most \(4\rho(0)\eta\). Together with (1) this gives \(\limsup\|Q\psi/\|Q\psi\|-F_\eta(D)\psi/\|F_\eta(D)\psi\|\|\le C\sqrt{\eta}\) for small fixed \(\eta\). No bound uniform in derivatives of cutoffs as \(\eta\downarrow0\) is required. Endpoint rounding and the sharp source's position parity are already included in the spectral bracket.

For this sharp source one can also bound the finite-time error. Keep \(|v|+2w\le r<1/\sqrt2\) with \(r\) fixed. On each monotone velocity arc, one integration by parts bounds its amplitude by \(C/(Td)\) at any site whose velocity is at distance \(d>0\) from that arc. Enlarge and shrink the velocity interval about \(v\) by \(\eta w\) on either side. The boundary strips carry at most \(C_r\eta w\) incident probability. For the inner spectral interval observed outside the position window and the outer spectral complement observed inside it, the sum of squared bounds over the integer sites is at most \(C/(T\eta w)\) for each contribution: on either side the successive denominators start at \(T\eta w\) and increase by one. Thus the two projected states differ in norm by at most \(C_r[\sqrt{\eta w}+(T\eta w)^{-1/2}]\). Taking \(\eta=(Tw^2)^{-1/2}\) for sufficiently large \(Tw^2\), and using \(S(v,w)\asymp w\), gives

\[
\frac{P_{\rm yes}}{2w/\pi}
  =1+v+O_r\!\left(v^2+w^2+(Tw^2)^{-1/4}\right).
\]

This sharp-launch estimate allows the weaker sufficient timing \(Tw^2\to\infty\) for acceptance. The constants are uniform while the entire window remains in the indicated compact velocity interval. The displayed bound need not be small at the recorded finite clocks. [Sharp-source integration-by-parts proof for the central window](Single_window_in_a_permanent_field.md)

## Releasing the selected packet

Put \(\phi_\eta=F_\eta(D)\psi/\|F_\eta(D)\psi\|\). On its velocity support \(\|(V-v)\phi_\eta\|\le w\). Also \(\|X\phi_\eta\|\le C_\eta/w\): differentiate the Fourier representation \(\sum_b F_\eta((\nu_b-v)/w)P_b\psi\); each nonzero term and its derivative occupy momentum sets of width \(O(w)\), and normalization divides by order \(\sqrt w\). The centered position norm of \(U^{T+n}\phi_\eta\) is thus bounded by \(C_\eta/w+(T+n)w+\sup_t\|B_t\|\). The actual accepted state after \(n\) more ticks is \(U^{T+n}Q\psi/\|Q\psi\|\). Unitarity transfers the norm comparison above to any such \(n\). It transfers probabilities of bounded position tests even though a sharp-aperture error in an unbounded position moment could be large.

Use the G1 units of length \(a=\varepsilon\delta\) per site and elapsed time \(\tau=\varepsilon\delta^2\) per tick, and fix \(v=\delta p_0\). In a scaling with \(v\to0\), \(w\to0\), \(Tw^{5/2}\to\infty\) and

\[
 a/w\longrightarrow0,\qquad aTw\longrightarrow0,\qquad w/\delta\longrightarrow0,\qquad a\longrightarrow0 ,
\]

the accepted terminal position concentrates about \(a[s+(T+n)v]\) uniformly for \(0\le n\tau\le t_{\max}\) with \(t_{\max}\) fixed. For each fixed physical radius apply the squared position-norm bound to the smoothed state, then the norm comparison to its position-event probability, and finally let \(\eta\) decrease. This gives concentration in probability, not a second-moment limit for the sharp-aperture state.

In particular choose \(\varepsilon=\delta\), \(w=\delta^{11/10}\) and \(T\) the nearest integer to \(\delta^{-14/5}\). Then \(Tw^{5/2}\sim\delta^{-1/20}\), \(a/w=\delta^{9/10}\), \(aTw\sim\delta^{3/10}\), and \(w/\delta=\delta^{1/10}\). The walker propagates during preparation: its accepted release center is \(as+p_0\tau T\), with preparation time \(\tau T\sim\delta^{1/5}\). Starting at the nearest site to \(Y_0/a\) therefore gives release center tending to \(Y_0\). More generally one may choose \(s\) nearest \(Y_0/a-Tv\) if that translated sharp launch is physically available. With \(n\tau\to t\), the conditional terminal position then converges to \(Y_0+p_0t\). The unshifted source \(s=0\) already suffices for \(Y_0=0\) in the explicit scaling. On a finite ring use \(N>2(T+n_{\max})+2\) and place the coordinate seam outside the flight cone. The integer propagation, aperture and terminal read there match the line through the last tested tick.

The concentration concerns the accepted subensemble on separate terminal runs. The success rate vanishes in the scaling limit, and the two band labels and their parity-related momenta need not be resolved. It gives a freely moving position center on the same walk as the edge calibration. Single-band Schrödinger state synthesis, a force response, physical mass and repeated position measurements still require their own preparations and instruments.


## What finite runs resolve

At tick 3, accepting the site (x=1) succeeds with probability (5/8). Four free ticks later the terminal distribution, summed over both pointer values, differs from the untouched walk by total variation (17/64). This tests a coherent instrument with two distinguishable pointer sectors. A passive record that leaves all terminal probabilities intact fails this comparison. An acceptance window on the unoccupied parity has exactly zero success, and an edge-only window at tick 6 succeeds with probability (1/64). The exact results keep both outcome branches, all ports, and separate models that retain a permanent record of the site or the site and rail. [Exact and spectral checker](check_flight_window.py) · [Output](results/flight_window.json) · [Finite flag proof](lean/FlightWindow.lean)

In the finest original trial, \(\delta=1/40\), \(p_0=1\), preparation took 30,603 ticks and release took 64,000. The computed acceptance \(0.0112853955\) is 1.02542 times \(2w/\pi\), but only 0.99895 times the exact spectral window mass \(S(v,w)=0.0112972400\). The displaced density explains most of the excess over the leading formula. At the same scale the archived ratios to \(2w/\pi\) were 0.9772 for \(p_0=-1\), 1.0020 for \(p_0=0\) and 1.0550 for \(p_0=2\). The accepted mean velocity was 0.999114 at \(p_0=1\), yet 45.4% of the accepted mass lay outside the specified velocity tolerance of one half. The convergence proof concerns bounded terminal position tests. [Original bins](results/flight_window.json) · [Cross-review numerical tables](../REVIEW_QUEUE/reports/2026-11-14_pcp-cross-reviewer_Director_G_Flight_window_preparation/xcheck_window.json)

For \(1/\delta\) from 4 to 128 the cross-review's \(T\approx\delta^{-2.8}\) trials had \(Tw^{5/2}\) between 1.08 and 1.28. On its alternative schedule \(T\approx\delta^{-2.2}\), \(Tw^{5/2}\to0\), yet at \(1/\delta=1024\), \(p_0=1\), the acceptance ratio to \(2w/\pi\) was 1.0007. These finite runs compare probabilities. They do not test the smooth-probe norm estimate (1), the large-\(Tw^{5/2}\) regime, or the necessity of a timing threshold. [Cross-review program](../REVIEW_QUEUE/reports/2026-11-14_pcp-cross-reviewer_Director_G_Flight_window_preparation/xcheck_window.py)

The queue's rerun agreed on the exact panels, text and predicates. It found 80 differing floating values, with maximum absolute difference \(9.6\times10^{-14}\); the two JSON files differed in bytes. At \(T=30{,}603\), direct position iteration and spectral propagation in the cross-review agreed on acceptance within \(6.1\times10^{-14}\). These comparisons apply to the stated model computations. The Lean file checks the finite exclusive-or flag algebra. [Archived cross-review and reproducibility findings](../REVIEW_QUEUE/reports/2026-11-14_pcp-cross-reviewer_Director_G_Flight_window_preparation.md)

The [folded complex field](Folded_field_and_native_gaussian.md) gives a further norm estimate for this accepted state and a separate Gaussian preparation with two phase-sensitive rail readings.
