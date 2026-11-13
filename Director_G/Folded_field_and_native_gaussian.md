# A complex free field from the two real rails of a signed walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada  
Research supplement by Director G (OpenAI Codex).

A walker released from one sharp site occupies a single site parity at each tick. Its two real rail amplitudes at an occupied site supply the two coordinates of a complex scalar. In a neighborhood of the folded band edge this scalar obeys free Schrödinger evolution in norm, even when the original spinor has comparable populations in both bands. A direction-only preparation produces a specific Gaussian from that same sharp source. Its changing complex phase has a two-time test using ordinary oriented terminal detectors. A different one-bit preparation gives a prescribed moving classical terminal position. The conditional probability law, physical instruments and scaling assumptions appear below.

## The encoding and its error

Use the signed Hadamard and conditional shift of the [Edge Record Walk specification](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/4f3468b/Director_G/candidates/edge_record_walk/specification.md). Rail amplitudes are real, with the common factor \(1/\sqrt2\) per elapsed tick. Set the launch clock to zero, \(s=x_{\rm launch}\bmod 2\); a free evolution of \(t\) ticks has support at \(x\equiv s+t\bmod2\). A real diagonal membership flag preserves that support on either outcome. On occupied sites put

\[
 f_t(x)=i^x e^{-i\pi t/4}\,[R_t(x)+iL_t(x)].
\]

This is an on-site real-linear isometry onto complex fields on the occupied sublattice. Every site probability equals \(|f_t(x)|^2\) under the stipulated squared readout. A change of Fourier convention conjugates or relabels some formulas. The relative \(R,L\) convention and clock phase must remain fixed for the rail measurements below. In particular a global phase of the encoded scalar generally changes the rail populations at a site.

Substitution of the native signed update gives an exact finite-spacing rule on the new occupied parity,

\[
 f_{t+1}(x)=\tfrac12[f_t(x-1)+f_t(x+1)]
 +\tfrac12(-1)^s i^{t+1}
       [\overline{f_t(x-1)}-\overline{f_t(x+1)}].
\]

For a unit \(R\) launch at \(0\), the first two complex values at \(+1,-1\) are \((1+i)/2,(1-i)/2\). The conjugate term rules out exact complex-linearity at finite spacing. The small-momentum result below controls arbitrarily many ticks without summing this term as an independent per-tick error.

Use the site Fourier kernel \(e^{-ikx}\). At \(k_*=-\pi/2\) the Hadamard walk has a positive-curvature eigenvector \((1,-i)/\sqrt2\) with eigenvalue \(e^{i\pi/4}\). Write \(\lambda_+=e^{-i\omega}\), \(\omega=\arcsin(\sin k/\sqrt2)\), \(\lambda_-=-e^{i\omega}\), and \(P_\pm(k)\) for their smooth orthogonal projectors. The eigenvalues are separated by at least \(\sqrt2\). On \(q\in[-\pi/2,\pi/2)\) set \(F_t(q)=\widehat{(R_t,L_t)}(k_*+q)\) and \(\ell=(1,i)\). Then \(Z_t(q)=\widehat f_t(q)=e^{-i\pi t/4}\ell F_t(q)\) is the Fourier transform on the single occupied parity, with measure \(dq/\pi\). This choice uses physical sites in the exponential for either output parity. On a ring, take \(4\mid N\) so \(i^x\) is single-valued under the specified periodic boundary. On the line there is no boundary twist.

There are two identities behind the estimate. First, \(\ell P_-(k_*)=0\), so \(\|\ell P_-(k_*+q)\|\le C|q|\) on \(|q|\le1\). Under \(n\) free ticks the error in replacing \(\ell U(k)^n F_t\) by \(\lambda_+(k)^n\ell F_t\) is \((\lambda_-^n-\lambda_+^n)\ell P_-F_t\). The coefficient is bounded in modulus by two for **every** \(n\). Second, reality and parity give \(F_t(-q)=(-1)^{s+t}\overline{F_t(q)}\), up to the usual endpoint identification. Thus \(|Z_t(q)|^2+|Z_t(-q)|^2=2\|F_t(q)\|^2\). On symmetric frequency regions the spinor and scalar norms coincide exactly. The second equality uses both members of the momentum pair.

For \(0<Q\le1\), let \(e_Q=\|\mathbf1_{|q|>Q} Z_t\|_2\). Free evolution preserves the spinor tail norm and therefore the scalar tail norm on this symmetric region. Combining the first identity with the bound \(|\omega(k_*+q)+\pi/4-q^2/2|\le |q|^4/6\) shows, for normalized input,

\[
 \big\|Z_{t+n}(q)-e^{-inq^2/2} Z_t(q)\big\|_2
 \ \le\ C'Q+nQ^4/6+2e_Q .
\]

The error is for the full encoded scalar field in its own clock and carrier convention. The original complexified spinor can still occupy two eigenbands. The folded parity identifies the duplicate momentum chart, and the two real rails supply the local scalar quadratures. The result also permits arbitrary smooth band-limited scalar inputs if their inverse rail preparations exist. The following instance uses one localized source and an explicitly specified record instrument. [Dispersion estimate](Signed_walk_and_weak_field.md) · [Extended walk states and dispersive wave equations](https://arxiv.org/abs/1004.0976) · [Numerical and exact checks](results/folded_free_field.json)

## A native Gaussian and a phase-sensitive terminal record

Start at \((0,R)\). After every two ticks copy the outgoing direction into a bit without recording the site, and retain the word in which the direction switches in every block. Use an even number \(m\) of blocks. The copy is reversible on rail plus pointer. The bit persists, and different recorded words are mutually exclusive when read. Applying the same calibrated score to **complete** terminal pointer-and-port records gives the probability of each word from its integer signed tallies; ignoring position within one word retains interference. A device that actually measures every site and later erases the labels has a different action. The extension of the detector law to these pointer records is a physical hypothesis.

The off-diagonal entries of \(U(k)^2\) are \(-i e^{\mp ik}\sin k\), with the exponent chosen by the outgoing rail. The alternating switches cancel the cumulative linear phase for even \(m\), return the rail to \(R\), and give Fourier amplitude proportional to \(\sin^m k\). The joint success probability is \(\binom{2m}{m}/4^m\sim1/\sqrt{\pi m}\). In the folded chart the normalized conditional profile is therefore \(Z_0(q)=c_m\cos^m q\), up to a common phase fixed by our release clock. Reset the clock at release. Fix the representative of the real source by multiplying it by \((-1)^{m/2}\), which cancels the raw alternating-word sign. This leaves the two-rail intensity contrast unchanged. Preparation costs \(2m\) native ticks, or two time units in the Gaussian scaling below. Set \(\delta=m^{-1/2}\), \(p=q/\delta\), \(\tau=n\delta^2\), and \(y=\delta x\). As a density amplitude in \(dp\), multiply \(Z_0(\delta p)\) by \(\sqrt{\delta/\pi}\). The resulting normalized wave functions converge in \(L^2(dp)\) to \(G(p)=\pi^{-1/4}e^{-p^2/2}\). This follows by dominated convergence from \(\log\cos q\le-q^2/2\), the near-zero Taylor expansion and exact normalization. For fixed \(P\) use \(Q=P\delta\) in the preceding estimate, take \(m\to\infty\) with \(n/m\to\tau\), and then take \(P\to\infty\). The terminal scalar tends in norm to \(G(p)e^{-i\tau p^2/2}\). This supplies a free Schrödinger state with a specified initial profile; the limiting position density is the Gaussian with variance \((1+\tau^2)/2\). Norm convergence gives weak position convergence. It alone does not control unbounded lattice moments. [Exact direction filter](Base_preparation_and_two_rays.md)

The terminal rail imbalance in a macroscopic block \(B\) is a measured difference of probabilities. Exactly at tick \(n\) it is

\[
 d_n(B)=\sum_{\delta x\in B}(R_n(x)^2-L_n(x)^2)
       =\operatorname{Re}\left[(-i)^n\sum_{\delta x\in B} f_n(x)^2\right]
\]

for this even release parity; an odd release site multiplies the last expression by \(-1\). The identity uses \(R+iL=i^{-x}e^{i\pi n/4}f_n\) and the known parity of \(x\). With the unitary inverse Fourier transform of \(\sqrt{\delta/\pi}Z_n(\delta p)\) denoted by \(g_m(y)\), inversion gives \(f_n(x)=\sqrt{2\delta}\,g_m(\delta x)\) on the occupied parity. The mesh is \(2\delta\), with an offset of at most \(\delta\) between the two clocks. On a fixed momentum cutoff, norm convergence gives uniform convergence of the interpolants. Their Riemann sums on a fixed spatial interval converge to the integral of the **complex square**. Truncation in \(p\) and \(|\int (g^2-h^2)|\le(\|g\|_2+\|h\|_2)\|g-h\|_2\) extend this statement to the convergent Gaussian family. For the whole line the same equality is Parseval pairing of \(Z(q)\) with \(Z(-q)\), without pointwise sampling. Endpoints of a bounded block have zero limiting mass.

Choose \(n\equiv0\bmod4\) with \(n/m\to\tau\). In two freshly prepared ensembles release for \(n\) and \(n+1\) ticks. Their limiting imbalances are the real and imaginary parts of \(\int_B g_\tau(y)^2\,dy\), respectively. For the whole line the integral is
\[
 C(\tau)=\int G(p)G(-p)e^{-i\tau p^2}\,dp=(1+i\tau)^{-1/2},
\]
using the square root continuous from \(C(0)=1\). For \(\tau=1\) the prediction is approximately \(+0.776887\) and \(-0.321797\) at the adjacent reads. Reporting only the total norm or spatial width would miss the sign of the second contrast. The comparison uses the rail readout, preparation phase and clock convention, and does not constitute arbitrary-state tomography. At \(m=512,n=512\), the two simulated full-line imbalances are \(+0.778054\) and \(-0.320574\). Retaining a separate position label at release changes the scaled variance at the first read from \(0.997912\) to \(106.737\). The two measurements occur in separate runs. For a finite realization choose a growing ring with circumference divisible by four and greater than twice the entire \(2m+n+1\)-tick light-cone radius plus two. [Checker](check_folded_gaussian.py) · [All retained runs](results/folded_gaussian.json)

## Connection to the classical flight

Starting from the same sharp site, instead retain one coherent binary window of the position after \(T\) native ticks, targeted at \(v=\delta p_0\). For \(w=\delta^{11/10}\), \(T\sim\delta^{-14/5}\), the [window calculation](Flight_window_preparation.md) shows that the conditional vector is approximable in norm by the velocity-filtered launch propagated to release. In the folded chart the slopes are \(\pm\sin q/\sqrt{1+\sin^2q}\). Their absolute value equals \(|v|+O(w)\) on the smoothed support. For any fixed \(P>|p_0|\), the full spinor outside \(|q|\le P\delta\) therefore has vanishing conditional norm, by the cutoff comparison and then the sharp-window limit. The displayed field estimate applies with \(n=O(\delta^{-3})\). Its \(nQ^4\) term still tends to zero. Moreover the significant scalar support has \(q/\delta\) near \(p_0\): the other velocity branch is suppressed in \(\ell P_-\) by \(O(\delta)\). This proves approximation to the **prepared state's own** free Schrödinger evolution as the state varies with scale. The measured position in units \(Y=\delta^2 x\) then concentrates on \(Y_0+p_0t\) at \(n\delta^3\to t\). Source yield is asymptotic to \(2w/\pi\). The long-time conditional Gaussian construction and the single-window ray are different instruments on the same carrier.

These results leave several operations exposed to attack. The raw signed dynamics, the conserved marker used to calibrate its score, coherent flag copying, and the transfer of that score to a complete recorded word each require physical justification. The exact decoded dynamics is real-linear, while complex-linear evolution is a low-frequency limit. No force, entangling gate, microscopic action unit, noninvasive trajectory, or cosmological dynamics follows from the folding calculation.
