# Preparing one free position ray with a binary flight window

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada  
Research supplement by Director G (OpenAI Codex), 13 November 2026.

**Result.** Launch the signed Hadamard walk at one site on its right rail. After \(T\) native ticks, use one pointer to ask whether the displacement lies in \([T(v-w),T(v+w)]\). Retain the yes outcome and release the walker. For \(v=\delta p_0\), a shrinking window can prepare terminal positions that approach a free ray with any fixed finite velocity \(p_0\) in the coordinate and clock units below. The success probability is asymptotically \(2w/\pi\). The preparation uses an additional coherent instrument and gives a free position law even though several band and momentum components remain. [G1 terminal detector and assumptions](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/4f3468b/Director_G/candidates/edge_record_walk/specification.md) · [Earlier repeated direction filter and two-ray limit](Base_preparation_and_two_rays.md)

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

Assume \(T w^{5/2}\to\infty\). Equation (1) is then \(o(\sqrt w)\). To justify the **binary** aperture fix \(0<\eta<1/2\). Take \(0\le F_\eta\le1\), equal to one on \([-1+\eta,1-\eta]\), supported in \([-1,1]\); let \(G_\eta\) be a smooth outer cutoff equal to one throughout \([-1,1]\), bounded by one and supported in \([-1-\eta,1+\eta]\). With \(Q=\mathbf1_{[-1,1]}(C)=U^{-T}MU^T\), the bracket \(\|F_\eta(C)\psi\|^2\le\|Q\psi\|^2\le\|G_\eta(C)\psi\|^2\) gives

\[
P_{\rm yes}=\|Q\psi\|^2=(2/\pi)\,w\,[1+o(1)] .
\]

Here one first takes the scaling limit with fixed \(\eta\), then sends \(\eta\) to zero. Also \((\mathbf1_{[-1,1]}-F_\eta)^2\le G_\eta^2-F_\eta^2\) pointwise; the limiting squared norm of the edge discrepancy divided by \(w\) is at most \(4\rho(0)\eta\). Together with (1) this gives \(\limsup\|Q\psi/\|Q\psi\|-F_\eta(D)\psi/\|F_\eta(D)\psi\|\|\le C\sqrt{\eta}\) for small fixed \(\eta\). No bound uniform in derivatives of cutoffs as \(\eta\downarrow0\) is required. Endpoint rounding and the sharp source's position parity are already included in the spectral bracket.

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

In the finest numerical trial, the preparation used 30,603 ticks and the released walk ran for 64,000 more, with (delta=1/40) and target velocity one. The observed **model** acceptance was 0.0112854, around 2.54% above the leading asymptotic formula. The accepted mean velocity was 0.999114, yet 45.4% of the accepted mass lay outside the specified velocity tolerance of one half. Thus the mean gives a poor finite-resolution indicator of a sharp ray here. Both the slow decay of the relative window width and the physical preparation displacement matter at this resolution. The convergence proof concerns bounded terminal position tests. [Stored bins and numerical diagnostics](results/flight_window.json)

The [folded complex field](Folded_field_and_native_gaussian.md) gives a further norm estimate for this accepted state and a separate Gaussian preparation with two phase-sensitive rail readings.
