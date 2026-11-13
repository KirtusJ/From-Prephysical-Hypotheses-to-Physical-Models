# A constant force from one walk to two mechanical limits

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada  
Mathematical development and computational checks by Director G (Codex).

The signed line walk admits a constant-force Schrödinger equation and concentration of its position records on a Newtonian trajectory. The same norm estimate gives both conclusions. A preparation in one oriented sheet sector and one base band, a squared-amplitude readout, and the conversion of lattice variables into scaled coordinates are premises. This supplements the centroid and free-envelope results of the [first construction](Signed_walk_and_weak_field.md). The physical origin of these premises remains open.

## Scales and preparation

Write \(\delta>0\) for a momentum bandwidth scale and \(0<\varepsilon\le1\) for the semiclassical parameter. One step has duration \(\Delta t=\varepsilon\delta^2\), one lattice site represents \(\Delta Y=\varepsilon\delta\), and the phase attached to a departure at site \(x\) is \(\exp(-ihx)\), where \(h=F\varepsilon\delta^3\). Thus the dimensionless momentum \(p=(k-k_*)/\delta\) changes by \(-F\Delta t\) per step. Here \(k_*=-\pi/2\) and \(F\) is the slope of the potential. With this convention the mechanical force is \(-F\). For example, \(F=1\) permits exact realizations with \(h=2\pi/M\) in the character \(r=1\). The signed walk also admits the effective angle \(\pm\pi/M\) on the elementary-holonomy plane of an odd cover. To compare **complex amplitudes** in that representation one must remove the known parity factor from the strong-field walk before demodulating. This output modulation leaves native site probabilities unchanged.

More explicitly, put \(C=(-1)^X\). The identity \(CU_h=-U_hC\) gives \(U_{h+\pi}^n=(-1)^{n(n+1)/2}C^nU_h^n\). Removing that output modulation gives the low-field spinor in the chosen orientation.

Start with an arbitrary normalized scalar envelope \(f(p)\) supported in \(|p|\le P\). Its encoded spinor at \(k=k_*+\delta p\) is \(\delta^{-1/2}f(p)u(k)\), with scalar/Fourier measures chosen consistently for this isometry. Here \(u(k)\) is a smooth normalized plus-band section and \(u_*=u(k_*)\). Along an initial momentum \(p\), put \(p_j=p-Fj\Delta t\), \(k_j=k_*+\delta p_j\). After \(n\) steps let \(t=n\Delta t\), \(L=P+|F|t\), and require \(\delta L\le1\). The support then stays in one chart. The estimates hold on the line and for either sign of \(F\).

## A bound on the complete spinor

After removing the carrier phase \(e^{-in\omega(k_*)}\), the \(L^2\) distance between the exact walk and the envelope encoded at its **final** momentum is at most
\[
 E(t)=2|F|t\delta+
       \frac{t\delta^2L^4}{6\varepsilon}
       +\frac{t|F|L\delta^2}{2}. \tag{1}
\]
The scalar envelope on this characteristic has value
\[
 f_t(p-Ft)=f(p)\exp\!\left[-\frac{i}{\varepsilon}
 \left(\frac{t p^2}{2}-\frac{F t^2 p}{2}+\frac{F^2t^3}{6}\right)\right]. \tag{2}
\]
In the scaled position coordinate \(Y\) this is the evolution for
\[
 i\varepsilon\,\partial_t\psi
   =-\frac{\varepsilon^2}{2}\,\partial_Y^2\psi+FY\psi.
\]
Indeed \(Y=i\varepsilon\partial_p\) in the momentum representation. Equation (2) is obtained by integrating \(p(s)^2/2\) along \(p(s)=p-Fs\). The proof makes the accumulated phase explicit because band populations alone cannot verify this equation.

**Proof.** The plus-band projector \(P_+(k)\) has Bloch vector \((\cos k,\sin k,\cos k)/\sqrt{1+\cos^2 k}\). Use the section \(u(k)=P_+(k)u_*/\|P_+(k)u_*\|\). For \(k=k_*+q,\ |q|\le1\), the dot product of the two Bloch vectors at \(k\) and \(k_*\) equals \(\cos q/\sqrt{1+\sin^2q}\ge0\). The denominator is at least \(1/\sqrt2\). Differentiating the normalized vector in the real norm gives \(\|u'\|\le\sqrt2\|P_+'\|\le2\). The latter projector estimate follows by differentiating its unit Bloch vector, whose numerator has derivative of norm at most \(\sqrt2\) and length at least one.

Each step acts on its characteristic by \(U(k_j)=\mathrm{diag}(e^{-ik_j},e^{ik_j})H\). If its input spinor is replaced by \(u(k_j)\) in place of \(u(k_{j-1})\), the error is bounded by \(2|h|\). The new vector is exactly \(e^{-i\omega(k_j)}u(k_j)\). Unitarity telescopes these errors to at most \(2n|h|\), giving the first term in (1). This estimate is for the spinor itself and includes any phase from transporting the chosen section.

For \(|q|\le1\), the band satisfies \(|\omega(k_*+q)-\omega(k_*)-q^2/2|\le |q|^4/6\), as follows by integrating the derivative \(\sin q/\sqrt{1+\sin^2q}\). Summing at all right endpoints \(q=\delta p_j\) gives the second term. The quadratic phase sum is \(\varepsilon^{-1}\sum_j\Delta t\,p_j^2/2\). The integrand has time derivative bounded by \(|F|L\). Right-endpoint quadrature therefore contributes at most \(t|F|L\Delta t/(2\varepsilon)\), the last term in (1). Using \(|e^{ia}-e^{ib}|\le|a-b|\), multiplying by each initial amplitude and integrating proves (1). The result complements earlier work on quantum-walk envelope equations and continuous limits in external fields. [de Valcárcel, Roldán and Romanelli](https://arxiv.org/abs/1004.0976) · [Di Molfetta, Brachet and Debbasch](https://arxiv.org/abs/1309.4923)

## Which classical records follow?

At \(\varepsilon=1\) and fixed \(t,P,F\), (1) converges to zero with \(\delta\). This gives the forced Schrödinger envelope. A sequence with \(\varepsilon\to0,\ \delta\to0,\ \delta^2/\varepsilon\to0\) gives the same comparison at the action scale of an individual classical packet. One explicit choice is \(\varepsilon=\delta\). For a bounded prescribed time \(T\), take an integer number of steps with \(n\Delta t\to T\) and compare at the attained time \(t=n\Delta t\).

For a point trajectory start with \(g\) smooth with compact support and unit \(L^2\) norm. Set
\[
 f_\varepsilon(p)=\varepsilon^{-1/4}
     g((p-p_0)/\sqrt{\varepsilon})e^{-iY_0 p/\varepsilon}.
\]
The initial momentum has root-mean-square deviation \(\sqrt\varepsilon\,\|s g(s)\|_2\) from \(p_0\). The initial position deviation from \(Y_0\) is \(\sqrt\varepsilon\,\|g'\|_2\). By differentiating (2), the final deviation of the scalar envelope from \(Y_c(t)=Y_0+p_0t-Ft^2/2\) obeys
\[
 \|(i\varepsilon\partial_{p_{\rm final}}-Y_c(t)) f_t\|_2
 \le\sqrt\varepsilon\,(\|g'\|_2+t\|s g\|_2).
\]
The final momentum concentrates at \(p_0-Ft\). These are the trajectories of the Hamiltonian \(p^2/2+FY\).

The conclusion extends to the **lattice position probabilities**. Apply the bounded observable \(e^{i\xi\varepsilon\delta X}\), for any fixed real \(\xi\). Its expectation changes by at most \(2E(t)\) in the spinor comparison. Replacing the encoded end spinor by the constant \(u_*\) costs at most \(2\delta L\) in state norm. In lattice Fourier variables the observable is translation by \(-\xi\varepsilon\delta\) in \(k\), hence by \(-\xi\varepsilon\) in \(p\). With compact momentum support away from the chart boundary, its expectation for the constant spinor equals the continuum position characteristic function for sufficiently small \(\delta\). The deviation estimate above makes that function converge to \(e^{i\xi Y_c(T)}\). The continuity theorem for characteristic functions gives weak convergence of the lattice position distribution to the point mass at \(Y_c(T)\). This argument uses a bounded observable throughout the comparison. It does not imply convergence of lattice position variances or identify outcomes at successive times on one measured path. The momentum marginal of the walk is transported exactly along each characteristic, since every fibre update is unitary. The two marginal conclusions concern separately specified measurements. For context on semiclassical transport of phase-space measures, see [Lions and Paul](https://ems.press/journals/rmi/articles/5283).

At fixed \(\varepsilon\), a packet can spread even when its centre follows the same classical equation. Concentration uses the additional shrinking-action and preparation assumptions. The construction is one-dimensional with a uniform external force and no particle interactions. It does not yet give a limit for the previously demonstrated contact interaction. In particular the band preparation, orienting reference, dimensionful mass and action, observation rule, and physical interpretation of a step have yet to be supplied. An experimental realization of an electric quantum walk tests a prepared quantum system with controlled pulses. It offers an external point of comparison for the walk dynamics. [Genske et al.](https://arxiv.org/abs/1302.2094)

## Reproduction

Run the [fibre checker](check_forced_envelope.py) with a destination directory and NumPy installed. It propagates the two-channel coin exactly up to binary64 arithmetic, compares the spinor including its phase, and records every step for 17 initial momenta, five odd sheet orders, both force signs, the zero-field control, and both scales \(\varepsilon=1,\delta\). For \(\varepsilon=1,\ F=1\), the largest sampled spinor distance was 0.04831 at \(M=65\) and 0.000775 at \(M=16385\). For \(\varepsilon=\delta\) it was 0.05343 and 0.02263 at those orders. The bound holds throughout the compact-support chart by the argument above. The samples cover effective low-field fibres and do not simulate a physical experiment, the full high-order lift, or individual classical trajectories. The 54,774 rows include all residuals. [Summary and predicates](results/forced_envelope.json) · [Numerical trials](results/forced_envelope_trials.csv)

The root review remains G1 OPEN. This conditional link between a lattice update, a forced quantum equation and a limiting classical position record addresses part of P7, P9 and P10. The program's original ontology claim remains unresolved.

A subsequent construction treats smooth position-dependent interaction on two periodic lattices. [Periodic two-body limits](Periodic_interaction_and_two_limits.md)
