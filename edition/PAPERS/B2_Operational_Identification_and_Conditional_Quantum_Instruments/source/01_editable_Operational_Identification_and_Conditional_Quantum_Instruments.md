---
title: "Operational Identification and Conditional Quantum Instruments"
author: "Kirtus Justus"
date: "Port Coquitlam, British Columbia"
lang: en
---

**Abstract.** An observation identifies a property when the property is constant on the class of models that predict the same observations. This article studies three examples: resistance reconstruction from labelled spectral measurements, readout probabilities under controlled phase interventions, and purity bounds for an outcome-selected quantum operation. In the last example, the success probabilities of individual preparations determine how a measurement of one output constrains the normalized Choi matrix. A complete set of four basis preparations provides a sequential test that accounts for failure as well as success. The mathematical models specify the state spaces, port labels, units, and measurement effects. A physical interpretation requires independent justification of these inputs.

**Scope.** The claims concern finite-dimensional models and probabilities of specified outcomes. Numerical examples evaluate exact models. Identifying the compatible class places a limit on which properties can be inferred from the observations.

**Research direction and responsibility:** Kirtus Justus. Mathematical and computational assistance: ChatGPT (OpenAI).

\clearpage
\includepdf[pages=1,fitpaper=true,pagecommand={\thispagestyle{empty}}]{Program_Identification_Map.pdf}
\clearpage

# Identification from observations

The program-wide identification map shows how model premises, observations and prospective controls enter the examples below.

For a model parameter \(\theta\) and allowed experiment \(e\), let \(P_\theta^e\) be its outcome law. Two parameter values are observationally equivalent when these laws agree for every allowed experiment. A functional \(h(\theta)\) is identifiable if and only if it is constant on each equivalence class. Otherwise the identified set is the range of \(h\) on that class. The criterion applies to a graph with labelled ports and to a quantum operation with explicitly chosen input and output measurements.

# Premises and notation

| Domain | Inputs required for the statements that follow |
|---|---|
| Finite operator selection | A finite Hilbert space, a supplied self-adjoint operator tuple, its generated unital algebra and the allowed data-preserving symmetries. |
| Graph reconstruction | A connected, real symmetric combinatorial Laplacian, uniform null mode, labelled input ports, unconditional scale statistics, normalized preparations and calibrated detector response. |
| Spectral estimation | A known excited mode, a phase reference, specified gains and noise model, and an explicit list of monitored outputs. |
| Quantum sequences | A state space with a declared tensor-product structure, specified preparations, gates, effects and available interventions. |
| Readout statistics | An ideal reference law, allowed histories and directions of reporting errors, timing, eligibility, missed events and the risk criterion. |
| Channel tomography | A common completely positive map; a trace-preserving marginal when required; calibrated operations transferred between Choi and product preparations. |
| Selected branch | A common nonzero completely positive trace-nonincreasing map. Success and failure are recorded per **attempt**. Input-specific success must be positive to define a conditional output. |

The branch effect is \(H=\mathcal B^\dagger(I)\), its absolute mean success is \(p_*=\operatorname{Tr}H/4\), and \(g_i=p_i/p_*\) is a **relative** success that can exceed one. For input \(i=00\), its share of the normalized Choi trace is \(t=g_0/4\). The capital \(C\) denotes the trace-one Choi state. We use output-first vectorization \(|K\rangle=\mathrm{vec}(K)/2\). The conventional trace distance is \(\|X-Y\|_1/2\); root fidelity is \(\|\sqrt X\sqrt Y\|_1\). A scale parameter is a filter setting unless a physical clock relationship is separately given.

Throughout, CP means completely positive, TP means trace preserving, and CPTP denotes a map with both properties. For a graph, \(K=L^+\) is the Moore–Penrose inverse of the Laplacian. In the phase calculation, \(d=s+k\), \(r=1-d\), and \(\ell=r-f\).

\newpage

# Algebraic selection and graph measurements

**Selection.** Decompose a generated finite algebra into blocks \(M_{n_\alpha}\otimes I_{m_\alpha}\). Data-preserving unitaries in the commutant form a connected group. Its action on an invariant finite unordered set of rank-one projections must fix each one. Thus each projection belongs to the bicommutant, the generated algebra. A full resolution is possible exactly when every \(m_\alpha=1\); it is unique exactly in the maximal abelian case. These are algebraic projectors. Their association with positions or subsystems needs independent evidence. 

**Subsystem measurements.** Two collective quadrature measurements constrain the outcome laws of those observables. Identifying independently acting subsystems requires information about the generated operator algebras. An expected commutator can vanish in one state while the operator commutator is nonzero. For example, in the maximally mixed qubit state every commutator has zero expectation, while the Pauli operators \(X\) and \(Z\) generate the full matrix algebra.

**Resistance.** The continuous effect is \(\Pi(ds)=4sL^2e^{-2sL}\,ds\) and there is a separate zero-mode effect \(P_0=\mathbf1\mathbf1^T/n\). Integrating on each positive eigenspace gives \(P_0+\int\Pi=I,\ \int s\Pi=K,\ \int s^2\Pi=3K^2/2\). Two states on the same port pair with identical diagonal populations have difference \(z|i\rangle\langle j|+\bar z|j\rangle\langle i|\). Hence
\[
 K_{ij}=\frac{\Delta\mu}{n\Delta p_0},\qquad
 R_{ij}=K_{ii}+K_{jj}-2K_{ij},\qquad \Delta p_0\ne0 .
\]
The ratio cancels unknown real coherence. Row sums fix the diagonals and \(L=K^+\). A common truncated window amounts to measuring the entry of a truncated operator. If the omitted positive operator lies between \(0\) and \(BI\), its off-diagonal entries are bounded by \(B/2\), by centering at \(BI/2\). A mean computed only on clicks needs the zero-mode and loss correction. Perturbing either mean or zero-mode probability amplifies the error as \(|\Delta p_0|\) approaches zero.

\newpage

# Spectral identification, detectors and decision rules

**Coherent spectral estimation.** For a known excited mode at positive eigenvalue \(\lambda\), let \(f_u=u\lambda e^{-u\lambda}\) for two calibrated scales \(u=s,t\). A complementary port has amplitude \(h=\sqrt{1-f_s^2-f_t^2}\). Homodyne measurements have independent variance \(1/2\) and mean \(\sqrt2 a\) times the monitored amplitude vector, where the real source amplitude \(a\) is unknown. With all ports observed, the normalized vector \(v=(f_s,f_t,h)\) obeys \(v^\mathsf T v'=0\). The Fisher cross term for amplitude and eigenvalue therefore vanishes, and the information for \(\lambda\) is \(4a^2\|v'\|^2\). At equal scales, \(x e^{-x}\) has two positive inverse images for each amplitude in \((0,e^{-1})\). Thus even a positive local Fisher information leaves two possible eigenvalues.

**Positive measures and graphs.** The normalized edge-difference probe on the rook graph gives \(m_0,\ldots,m_4=(1,5/32,7/256,11/2048,19/16384)\). A rational contraction certificate fixes the first four moments of a weighted graph; its \(m_4\) lies between \(0.006804564875115\) and \(0.006804564875116\). The extension to 16 vertices leaves this entire pair measure invariant. A different pair of abstract positive measures has \(\Delta m_4=27/2945024\). The moment gap and associated sample bounds apply only to those measures.

**Calibrated coupling.** In the reference experiment \(f_c(u)=4c^2u e^{-2cu}\). A fixed event has response \(0\le\eta\le1\). For couplings 1 and 2 the likelihood ratio \(4e^{-2u}\) decreases; a lower-tail threshold therefore maximizes the second response at fixed first response. The upper and lower boundaries are \(F_2(F_1^{-1}(p_1))\) and \(1-F_2(F_1^{-1}(1-p_1))\). At \(p_1=1/2\) they are approximately \(0.848168\) and \(0.151832\). Concavity/convexity extends necessity to stable positive-mode mixtures under a common eigenvalue rescaling. For a finite set of incident laws a single event vector is feasible exactly if \(a\cdot p\le\int(\sum_i a_i f_i)_+\) for all real \(a\). Maximize the integrand pointwise, then use compactness and separation. Multiple outcomes require one normalized kernel. Loss or preparation drift can imitate a stationary detector even at all couplings.

\newpage

# Gate sets, memory and timing

**Gauge.** Consider qubit models in which the preparation/effect radii are \((1/2,3/4)\) and \((3/4,1/2)\). Similarity on Bloch coordinates preserves the accessible sequence probabilities but the preparation purities are \(5/8\) and \(25/32\). The channel \(0.37\,\mathrm{Ad}_{\rm CNOT}+0.63\,\mathcal D\) and its scaled similarity both have positive Choi matrices and can entangle product inputs. Their accessible labelled product output can even differ in separability. The least eigenvalue of the output partial transpose for the labelled product preparation is positive in one model and negative in the other. For a genuinely unitary candidate, unital trace-preserving complete positivity and unit determinant magnitude force Hilbert–Schmidt isometry; the similarity then requires preservation of the one-body Pauli subspace. Its unitary normalizer is local unitaries, optionally with SWAP. This eliminates this scaling gauge for an independently established entangling unitary. It does not eliminate every imaginable gauge.

**Four-use correlations.** With reported prefix \(W\), last ideal bit \(Z\), last reported bit \(Y\), and reference \(s\), the triangle inequality in total variation gives
\[
 \mathrm{TV}(\mathcal L(W,Y),\mathcal L(W)\operatorname{Bern}(s))
 \le \Pr(Y\ne Z)+\mathrm{TV}(\mathcal L(W,Z),\mathcal L(W)\operatorname{Bern}(s)).
\]
For a concrete four-bit law, put \(t=.37, r=1/16, e=.01, s=t+(1-t)r, m=s+(1-2s)e\), and \(A=t^4[(1-r)(1-2e)]^4/4\). Define
\[
 Q(y)=\prod_{i=1}^4m^{y_i}(1-m)^{1-y_i}-A\prod_{i=1}^4(2y_i-1).
\]
This is a normalized nonnegative distribution with the same proper marginals as the Bernoulli product. The left side of the inequality for this law is \(0.02671723099894\ldots\). A 1% final error cap requires a freshness departure of at least \(0.01671723099894\ldots\). An anticipating reporting kernel and an immediate reporting rule have different admissible histories. Retain all attempted records and record when the past becomes irrevocable.

**Directional errors.** With a fresh ideal bit of probability \(s=131/320\), each history-specific reported-one probability lies in \([s(1-\varepsilon),\,s+(1-s)\varepsilon]\). One-sided channels attain both boundaries and interpolation attains the interior. Applying the rule at every tree node is sufficient for the entire word law. For this law the parity-only, full-word fixed-\(s\), and full-word fitted-common-\(s\) thresholds are \(4.41216575\%\), \(11.28717824\%\), \(8.15529323\%\). With a 1% conditional directional-error cap, a randomized-boundary parity test reaches 95% power at 5% size with 6,343 records under the stated population law.

For 30 cells, 459 zero-error observations per cell give one 99% upper bound on the maximum; 797 suffice for simultaneous coverage of 30 distinct limits under the stated binomial design. A prespecified conjunction rule controls erroneous rejection by \(\max(\gamma,\alpha)\) under the respective calibration/testing premises. Gate-test power does not alone determine joint power.

\newpage

# Phase interventions and the observable part of a state

A single conditional state and binary effect are common to the direct and phase arms. \(P\) is a rank-one joint match, \(s=\operatorname{Tr}P\rho\), \(h=\operatorname{Tr}EP\), \(R=I-P\), and \(U_\phi=P+e^{i\phi}R\). Model values \(h=0.99\), \(s=131/320\), \(q=81711338569043/224995905216000\) are population inputs after the reported history \(111\). The reflection is about the joint probe. Local single-qubit phase gates cannot simply be substituted.

**Four-phase feasibility.** Write \(a=sh,\ b=(q_0+q_\pi)/2-a\) and \(c=(q_0-q_\pi+i(q_{\pi/2}-q_{3\pi/2}))/4\). The opposite-arm sums must agree and
\[
 0\le b\le1-s,\qquad |c|^2\le\min\{ab,\ s(1-h)(1-s-b)\}.
\]
Expansion gives the first harmonic; Cauchy–Schwarz for \(E\) and \(I-E\) gives both disks. Conversely a pure state with components \(\sqrt s,\sqrt{1-s}\) and a two-by-two effect with diagonals \(h,b/(1-s)\) and the requisite off-diagonal realizes the quartet when \(0<s<1\). Endpoint cases use positivity directly. On the two reflected arms alone one gets \(q_\pi\in[0.449704036935\ldots,0.551029468634\ldots]\) for these \(s,h,q_0\).

**Angle and group variation.** The sharp zero-rise boundary for general density states with the relevant calibration is \(58.778607958569660\ldots^\circ\). The outward-rounded 30-degree contrast interval is \([4.69764481,18.19990866]\) percentage points. A feasible minimizer by itself only supplies an upper bound on the minimum; the support geometry supplies the global lower bound. For a common response over offsets, the exact sign test is \(1+\mathbb E\cos\varepsilon>1.77548900478\ldots\,|\mathbb E\sin\varepsilon|\). Angle-conditioned states require the appropriate group-specific calibrations. The same symmetric angle histogram can give minima of opposite sign.

**Channel restriction.** The diagonal unitary pair gives \(+0.118207001877\) percentage points at balanced \(\pm60^\circ\), and \(-0.023649426882\) at \(\pm61^\circ\). Its zero is near \(60.832579155406^\circ\); it gives an upper bound on the first failure, not the optimizer. A strict rise holds for general states at \(60^\circ\) if their half-trace-distance cap is below \(0.8309705985874090117\ldots\), and zero is attainable at that cap. Trace-preserving Choi states with maximally entangled match still rise at that cap. Their unrestricted sign at \(60^\circ\) is open.

\newpage

# Purity with a fixed response and incomplete tomography

The complete specified lower-endpoint phase curve with its fixed detector annihilates a Choi direction. Let \(u=|iZ\otimes I\rangle,\ v=|iX\otimes I\rangle,\ p=|I_4\rangle\) and \(k=(\sqrt{sh}-\sqrt q)^2/(1-h)\). A normalized vector \(\eta=(\sqrt s\,p-\sqrt k\,u)/\sqrt d\) has fixed weight \(d=s+k\). The ray \(v\) has weight \(f\); the thirteen-dimensional residual subspace has weight \(\ell=r-f\). Define \(\rho_\star\) with weights \(d,f,\ell/13\) on the corresponding sectors. Its prescribed trace-preserving marginal follows from the maximally entangled basis. For every compatible state the fixed populations give
\[
 J(f)=d^2+f^2+\ell^2/13,\qquad
 \operatorname{Tr}\rho^2=J(f)+\|\rho-\rho_\star\|_2^2 .
\]
The complete interval given just this phase contract and \(f\) is \([J(f),1]\); additional transferred product measurements can reduce it.

**Three axes.** For product input \(|00\rangle\), let \(u_Z=p_Z-d-6\ell/13,\ u_X=p_X-1/2,\ u_Y=p_Y-1/2\). On the interior support, projecting the three probability observables away from the fixed populations and Choi marginal yields the Gram diagonal \((1230/91,97/7,97/7)\). Orthogonal projection gives
\[
 \operatorname{Tr}\rho^2\ge J(f)+(91/1230)u_Z^2+(7/97)(u_X^2+u_Y^2).
\]
The equality candidate adds the minimum-norm tangent with these readings to \(\rho_\star\). It attains equality exactly when it is positive. At \(0<f<r\) sufficiently small simultaneous deviations always do. At \(f=0\) the support has rank 14 and the rotated \(Z,X,Y\) Gram diagonal is \((159/13,25/2,254/21)\). At \(f=r\) it is \((0,0,1/2)\); the only free parameter is the real coherence. At the three reference rates its value is zero, fixing purity to \(0.501235795572884\ldots\).

**Reference triple.** The full interval \([J(f),1]\) occurs throughout \(0\le f\le f_\star\), where \(7f_\star^2+(39d-7)f_\star-6dr=0\) and \(f_\star\approx0.105322985\). A controlled-unitary construction attains the pure endpoint in this range. Some ambiguity survives throughout \(0<f<r\). Purity one requires \(f\le19r/32\): a pure channel is unitary, its off-diagonal second-bit blocks have equal squared norms, and the first marginal's largest eigenvalue must be at least \(1-2\ell\). Its reference value \(d+6\ell/13\) then gives the requirement.

There is no general pure witness asserted for \(f_\star<f\le19r/32\). At \(\ell=0.01\), a distinct two-sign family keeps the same first-qubit output along purities \([0.9802,1]\); its transverse readings differ from the reference triple. A second-qubit \(Y\) test resolves the sign within that family. At the interior reference point, 204 local real dimensions survive first-qubit tomography under trace preservation, 189 with unitality. A nine-dimensional family even shares the complete joint output on this one input.

\newpage

# One prepared input: trace-preserving channels

For a known pure input with full output \(\sigma\), set \(P=\operatorname{Tr}\sigma^2,\ \lambda=\lambda_{\max}(\sigma)\). The exact trace-one Choi purity interval over CPTP channels is
\[
 [(P+3/4)/16,\ (9+6\lambda+P)/16].
\]
For the lower endpoint, dephase the input basis, prepare \(\sigma\) on the tested input and \(I/4\) on the other three. The block Hilbert–Schmidt norm shows minimality. For the upper endpoint, a Stinespring isometry produces environmental states \(\tau_j\) on basis inputs; \(\tau_0\) has the nonzero spectrum of \(\sigma\). Their average has the nonzero spectrum of \(C\). For \(\tau=(\tau_1+\tau_2+\tau_3)/3\), \(16\operatorname{Tr}C^2=P+6\operatorname{Tr}(\tau_0\tau)+9\operatorname{Tr}\tau^2\le P+6\lambda+9\). Choose a Schmidt purification for input 0. Complete the isometry using three **system vectors orthogonal to its top system Schmidt vector**, all with the top environment vector. This attains equality. Continuity on mixtures supplies the rest of the interval.

For local readings only, let \(a\) be the first marginal's larger eigenvalue, \(\beta\) the probability of a calibrated rank-one projective outcome on the second qubit, \(b=\min(\beta,1-\beta)\), \(m=\min(1,a+b)\). In the measured bases, dephasing achieves the minimum joint purity
\[
 L=(a-x)^2+x^2+(1-a-b+x)^2+(b-x)^2,\quad
 x=\operatorname{clip}((a+b)/2-1/4,\max(0,a+b-1),\min(a,b)).
\]
Positivity of the two diagonal second-output blocks gives \(\lambda_{\max}(\sigma)\le a+b\), so \(P\le m^2+(1-m)^2\). For \(a+b<1\), take \(z=\sqrt a\,|00\rangle+\sqrt b\,|11\rangle\), and \(\sigma=|z\rangle\langle z|+(1-a-b)|10\rangle\langle10|\). For \(a+b\ge1\) a rotated Schmidt basis realizes a pure output. Hence the exact local-only interval is
\[
 [(L+3/4)/16,\; (9+6m+m^2+(1-m)^2)/16].
\]
A unitary fits precisely when \(1-a\le\beta\le a\). At \(f=0\) the reference first-qubit data permit purity one, while the complete joint reference output alone bounds it above by \(0.812504\). These two observations have different identifying power.

**Distance.** The sharp minimum normalized Choi half-trace distance to a unitary for fixed local readings is \([1-m+\sqrt{(1-m)^2+12(1-\sqrt m)^2}]/8\). Compress onto the tested input Choi direction and the coherent direction of the other three inputs. Their diagonal bounds are \(m/4,3/4\), and positivity bounds the cross term by \(\sqrt{3m}/4\). The nonnegative top Rayleigh vector gives the displayed lower bound; complementary output eigenvectors give an attaining Kraus construction. With additional detector data the numerical lower bound \(0.173002789690\) remains valid in its **TP** contract. The metric is the trace distance between normalized Choi states.

\newpage

# A selected branch: relative success and flip probability

Let \(\mathcal B\ne0\) be CP and trace-nonincreasing, \(0\le H=\mathcal B^\dagger(I)\le I\). Rescale its Kraus matrices by \(1/\sqrt{p_*}\), \(p_*=\operatorname{Tr}H/4\). The normalized Choi state has reference marginal \(G^T/4\) for \(G=H/p_*\), \(\operatorname{Tr}G=4\). Let \(g_0,g_1\) be the diagonal entries for inputs \(00,01\), \(w\) the Choi population in the operator subspace \(V\otimes I_2\), and \(\beta\) the second-bit flip conditional on success on \(00\). Require \(g_0>0\), \(g_1\ge0\), \(g_0+g_1\le4\).

**Sharp branch flip theorem.**
\[
 4(1-w)\ \ge\ g_0\beta+
 \tfrac12\bigl(\sqrt{g_0(1-\beta)}-\sqrt{g_1}\bigr)^2 .
\]
Split each Kraus operator into \(A_j,B_j,C_j,D_j\) in second-bit order. The squared norm outside the local subspace sums to \(4(1-w)=\sum_j[\|A_j-D_j\|_F^2/2+\|B_j\|_F^2+\|C_j\|_F^2]\). Keep only the relevant first columns and let \(\alpha\) be the reverse flip weight on input 1. A reverse triangle inequality gives \(g_0\beta+\alpha+(\sqrt{g_0(1-\beta)}-\sqrt{g_1-\alpha})^2/2\); this increases with \(\alpha\). Put \(\alpha=0\). Write \(u=(4-g_0-g_1)/2\). The two normalized Kraus operators
\[
 \operatorname{diag}(\sqrt{g_0(1-\beta)},\sqrt{g_1},\sqrt u,\sqrt u),\qquad
 \sqrt{g_0\beta}\,|01\rangle\langle00|
\]
attain equality. A common positive scaling makes a genuine trace-nonincreasing operation. For externally fixed absolute success, the scale must also satisfy the success-effect bound; it cannot be varied freely.

The inversion follows by completing the square in \(x=\sqrt{g_0(1-\beta)}\). For compatible data,
\[
 (x+\sqrt{g_1})^2\ge2(g_0+g_1)-8(1-w_0),\qquad w\ge w_0.
\]
For \(g_0=g_1=1,\ w_0=0.99\), \(\beta\le 1-(\sqrt{3.92}-1)^2<0.039797974645\). This alone gives a CPTP local-output purity ceiling \(0.807826398288\) after using the corresponding first marginal. A branch with other relative successes does not inherit that numerical ceiling.

\newpage

# A selected branch: sharp Choi-purity interval

Let \(t=\langle\psi|H|\psi\rangle/\operatorname{Tr}H>0\) for a known pure input \(\psi\). Write \(\sigma=\mathcal B(\psi)/p_\psi\) for its normalized output. With only \(t,\sigma\) fixed over nonzero CP trace-nonincreasing branches,
\[
 \boxed{t^2 P+(1-t)^2/12\ \le\operatorname{Tr}C^2
 \le t^2P+(1-t)^2+2t(1-t)\lambda.}
\]
Here \(P=\operatorname{Tr}\sigma^2\) and \(\lambda=\lambda_{\max}(\sigma)\). The selected input sector has dimension four, its complement twelve. In block form \(A=t\sigma,\ \operatorname{Tr}D=1-t\), so \(\operatorname{Tr}C^2=t^2P+\operatorname{Tr}D^2+2\|B\|_2^2\). Take \(B=0,D=(1-t)I_{12}/12\) for the minimum. Block positivity gives \(B=A^{1/2}KD^{1/2}\) for a contraction \(K\), and \(\|B\|_2^2\le t\lambda(1-t)\). Couple a top eigenvector of \(\sigma\) coherently to one complementary ray with weights \(t\lambda,1-t\), leaving the other input-block eigenvectors at weights \(t\lambda_j\). This saturates the maximum. Each normalized positive Choi state can be rescaled to a CP trace-nonincreasing operation. Mix endpoint states to cover every intermediate purity.

For local readings only, replace \(P\) at the lower endpoint by \(L\), and replace \(P,\lambda\) at the upper endpoint by \(m^2+(1-m)^2,m\). The same joint extremizers and block argument establish sharpness. At \(t=1\) there is only the tested block; at \(t=1/4\) the numerical endpoints coincide with the CPTP formula. The scalar condition \(t=1/4\) is weaker than the full CPTP marginal. CPTP endpoint attainability uses the separate isometry proof.

**Rank-one operation.** A branch with one Kraus operator produces a pure conditional output from a known pure input on which it succeeds. The local criterion \(1-a\le\beta\le a\) is therefore necessary. A suitable purification and a single Kraus preparation attain it. At fixed positive \(t\), the preceding upper formula reaches one exactly when \(m=1\); that argument supplies sufficiency for the fixed-\(t\) statement as well. A rank-one branch need not be a unitary. If \(t\) can approach zero, a mixed successful output can exclude rank one without a uniform gap below purity one.

**Distance consequence.** The same block inequality gives \(\lambda_{\max}(C)\le t\lambda+1-t\); the constructed upper witness attains equality. The distance of a state to the nearest unconstrained pure state is \(1-\lambda_{\max}(C)\), by the top-eigenvector test and its diagonal realization. Thus the sharp minimum distance to an arbitrary pure normalized branch is \(t(1-\lambda)\), or \(t(1-m)\) for local readings alone. The comparison state need not satisfy those observations. This consequence does not use the CPTP unitary-distance formula. If only raw successful-input probability \(p_\psi>0\) is calibrated, \(t\ge p_\psi/(p_\psi+3)\) because the other three basis successes are at most one; this gives a conservative distance floor.

\newpage

# Two conditional outputs and a shared flip budget

For two successful preparations require \(g_0,g_1>0\). Let \(\rho_i\) be their conditional first-qubit marginals, \(w\ge w_0\) and \(F\) their root fidelity. In the observation class fixing just the relative successes, those two states and \(w\ge w_0\), a branch exists **if and only if**
\[
 g_0+g_1-2\sqrt{g_0g_1}\,F(\rho_0,\rho_1)\le8(1-w_0).
\]
Indeed, the squared distance of the two aligned, unnormalized purification vectors is at most \(8(1-w)\) by the Kraus-block identity. The real overlap of normalized purifications is at most root fidelity. Conversely choose purifications attaining \(F\), carry them on distinct second-bit output flags at weights \(g_0,g_1\), and fill the other two columns using the same vector in a disjoint environment with weight \((4-g_0-g_1)/2\) each. The columns are mutually orthogonal. The deficit is exactly the left side divided by eight. Common rescaling supplies an instrument branch. At fixed \(p_*\) all raw successes, including those of the completing columns, must be admissible.

For a common binary effect record \(r_{iy}=\Pr(\mathrm{success},Y=y\mid i)\) using **all attempts**. Monotonicity of root fidelity under measurement yields
\[
  \sum_y(\sqrt{r_{0y}}-\sqrt{r_{1y}})^2\le8p_*(1-w_0).
\]
The condition is sharp for the stated binary projective-readout-only data with admissible success totals; a general calibrated effect gives a necessary test. For \(p_*=1/2,\ g_0=g_1=0.04\), select orthogonal first outputs. The construction yields raw successes \(0.02,0.02,0.98,0.98\), with \(w=0.99\). Perfect discrimination is possible. Equality of the two tested successes alone cannot justify the equal-to-mean bound.

At \(g_0=g_1=1,\ w_0=0.99\), put \(c=0.96\),
\(G(x)=(c\sqrt x+\sqrt{1-c^2}\sqrt{1-x})^2\) on \(x<c^2\). Binary fidelity gives \(p_1\le G(p_0)\). The largest possible change for the given first marginal \(a=0.529472934503538\ldots\) is \(G(1-a)-(1-a)<0.272954\), attained under the reduced contract. Write \(\alpha,\beta\) for the two flips. The same deficit gives \(\alpha+\beta\le0.04\). The neighbor's largest eigenvalue is bounded by \(\min\{G(a+\beta),G(a)+0.04-\beta\}\); taking the maximum at the crossing gives \(<0.810954608659\). The two successful environmental states have weights \(1/4\) each in the Choi purification. The other weights sum to \(1/2\). Thus
\[
 \lambda_{\max}(C)\le T=(2+a+G(a)+0.04)/4,\quad
 \operatorname{Tr}C^2\le T^2+(1-T)^2<0.732104302723 .
\]
Global sharpness of these two upper bounds under all of the specified constraints is open. The TP distance bound \(0.173002789690\) concerns distance to unitary Choi states.

\newpage

# Sequential evidence and selection

Define eligibility from the preceding record, then privately assign the next input. For a fair comparison, a binary click earns score \(Z=+Y\) on input 0 and \(-Y\) on input 1. If the two conditional click probabilities differ by at most \(\delta\) at each eligible history, put \(A=e^\lambda-1\), \(B=1-e^{-\lambda}\) for fixed \(\lambda>0\). The mean of \(e^{\lambda Z}\) is \(1+(Ap_0-Bp_1)/2\). Its maximum occurs at \((1,1-\delta)\), as the objective increases in \(p_0\) after setting \(p_1=\max(0,p_0-\delta)\). The opposite score has the same upper envelope.

For an independently justified root-fidelity lower bound \(c\), an alternative exact one-step envelope is
\[
 F_c=1+\frac{A-B+\sqrt{(A-B)^2+4AB(1-c^2)}}{4}.
\]
Align two purifications by fidelity. Maximization over effects is bounded by the positive part of their weighted projector difference, which has the displayed two-dimensional eigenvalue expression. Pure states of overlap \(c\) and its top projector attain the bound in this class. At \(c=.96,\lambda=\log 2\), this gives \(1.284452187191\ldots\); the scalar envelope at \(\delta=.28\) is \(33/25\). For either applicable envelope \(F\), average the two one-sided products to obtain \(M_N=\cosh(\lambda\sum_{n\le N} Z_n)/F^N\). Each product has conditional mean at most its previous value. Ville's inequality gives \(\Pr(\sup_N M_N\ge20)\le .05\). This applies to a prespecified test or an appropriately weighted mixture. Choosing whichever test crosses first requires its own error accounting.

**Selection counterexample.** The diagonal single-Kraus branch with squared entries \((.045,.005,.975,.975)\) is trace-nonincreasing, has \(p_*=.5\), and has local weight \(w=1-(.3-.1)^2/8=.995\). Both successful first qubits are in state \(|0\rangle\) and click with certainty for its projector. Under independent repeated attempts and fair assignment, the retained arm-0 probability is \(.9\). Thus the scalar channel statistic applied only to successes has the following probabilities.

| Event for the incorrectly selected statistic | Exact-model probability |
|---|---:|
| Statistic at least 20 at success 20 | 0.867046676566 (rounded) |
| Statistic reached 20 on or before success 20 | 0.898600383922 (rounded) |
| Statistic eventually reaches 20 under indefinite repetition | 1 |

At success 20 the arm-0 count must be at most 3 or at least 17. Through that time, the first crossing can occur only at successes 9, 13, 16 or 19. For the cumulative probability, discard paths at their first crossing and propagate surviving masses with weights \(.9,.1\). The exact cumulative probability is \(449300191961080193/500000000000000000\). The final row follows from the positive limiting log growth \(.8\log 2-\log(33/25)\). These are properties of the constructed selection rule.

\newpage

# Testing conditional outputs per attempt

Let \(r_{iy}\) be the probability, given assignment \(i\), of success and binary outcome \(y\). Write \(s_i=\sum_y r_{iy}\), \(\varepsilon=1-w_0\), and \(D=\sum_y(\sqrt{r_{0y}}-\sqrt{r_{1y}})^2\). All eligible preparations in each arm enter its denominator. For a common branch, \(D\le8\varepsilon p_*\). With fixed absolute success rates, also require \(0\le s_i\le1\) and \(0\le4p_*-s_0-s_1\le2\); these express the existence of two other trace-nonincreasing basis successes. The raw inequality is exact for unrestricted marginal states and a shared projective qubit readout. Choose states diagonal in its basis and use the paired-input purification construction.

For both tested successes positive, put \(c=(s_0+s_1-8p_*\varepsilon)/(2\sqrt{s_0s_1})\). Given first conditional click probability \(x\), define \(\theta=\arccos\sqrt{x}\). When \(0<c\le1\), the second probability spans exactly
\[
 [\cos^2(\min\{\pi/2,\theta+\arccos c\}),\;
  \cos^2(\max\{0,\theta-\arccos c\})].
\]
This follows by writing the two binary square-root probability vectors as unit vectors in the first quadrant. For \(c\le0\) the full unit interval is available; \(c>1\) excludes compatibility. A zero-success arm has no conditional click probability.

**Sequential test with a reference.** Before assignment choose \(t_y>0\), put \(d_{0y}=1-t_y\) and \(d_{1y}=1-1/t_y\). The supremum of \(d_{0y}x+d_{1y}y'\) over \(t_y\) equals \((\sqrt{x}-\sqrt{y'})^2\). Randomize among tested inputs and the maximally mixed reference with known positive probabilities \(\pi_0,\pi_1,\pi_*\). Score tested successes by \(d_{iy}/\pi_i\), reference successes by \(-8\varepsilon/\pi_*\), and failures by zero. The conditional expected score is at most \(D-8\varepsilon p_*\le0\). For a predictable nonnegative stake with \(1+\eta X\ge0\) at every outcome, the product of these factors starts at one and has the same 5% crossing guarantee at 20.

**Two tested inputs only.** Trace nonincrease implies \(D\le 2\varepsilon(s_0+s_1+2)\). The reduced projective model attains this condition by assigning success one to both untested columns and using orthogonal second-output flags. Score a success by \((d_{iy}-2\varepsilon)/\pi_i-4\varepsilon\) and each failure by \(-4\varepsilon\). The conditional mean is again nonpositive. This test can accept rate pairs the reference-arm test would exclude.

**Pooling and uncertainty.** At committed histories the conditional operations may vary. Joint convexity gives \(D(\bar r)\le N^{-1}\sum_n D(r_n)\le8\varepsilon\bar p_*\). A uniform private basis draw gives unbiased scores \(4\mathbf1_{i,\,\mathrm{success},\,y}\) for the four raw rates and \(\mathbf1_{\mathrm{success}}\) for \(p_*\). Conditional Hoeffding bounds and the summable weights \(1/[N(N+1)]\) give simultaneous coverage at all eligible sample sizes. For a total error allocation \(\alpha_r+\alpha_*\), the respective half-widths are \(\sqrt{8\log(8N(N+1)/\alpha_r)/N}\) and \(\sqrt{\log(2N(N+1)/\alpha_*)/(2N)}\). Use a lower bound on discrepancy and upper bound on the right side. A pooled estimate alone cannot justify the history-by-history null of the product test.

\newpage

# When the binary detector is calibrated

**Conditional corollary.** Suppose the common first-qubit click effect has known eigenvalues \(0\le L<U\le1\). Let \(z_i=r_{i1}\) be success with a click per attempt and let \(s_i\) be total success. There are two uniquely determined success-weighted populations in the detector eigenbasis,
\[
 v_{i+}=\frac{z_i-Ls_i}{U-L},\qquad v_{i-}=s_i-v_{i+}.
\]
In the model fixing these rates, \(p_*\) and \(w\ge w_0\), with arbitrary first-qubit states, feasibility is equivalent to admissible absolute successes, \(v_{i\pm}\ge0\), and
\[
   \sum_{j=+,-}(\sqrt{v_{0j}}-\sqrt{v_{1j}})^2\le8p_*(1-w_0).
\]

**Proof.** Write the effect as \(E=L I+(U-L)P_+\). On input \(i\), the success-weighted expectation of \(E\) is therefore \(L s_i+(U-L)v_{i+}\). Measuring the spectral projectors gives the displayed necessary inequality by monotonicity of root fidelity. For the converse, take both states diagonal in those projectors with the indicated success-weighted populations. Their fidelity equals that of their spectral distributions, and the paired-input theorem constructs a single operation. The physical detector with the specified eigenvalues then gives exactly \(z_i\). If an arm has zero success, its spectral weights vanish and its column can be zero in the same construction. If \(U=L\), require \(z_i=L s_i\); the least possible discrepancy is \((\sqrt{s_0}-\sqrt{s_1})^2\), attained with identical successful states. No assumption of commuting unknown laboratory states enters the necessary direction.

**Equal successes.** Put \(s_0=s_1=s>0\), \(q_i=z_i/s\) and \(c=\max(0,1-4p_*(1-w_0)/s)\). With only admissible absolute successes through \(p_*\), the sharp click difference is \((U-L)\sqrt{1-c^2}\). The two spectral distributions can be chosen as the symmetric pair \(((1+d)/2,(1-d)/2)\) and its reverse with \(d=\sqrt{1-c^2}\). For \(s=p_*=1\), \(w_0=.99\) and eigenvalues .2 and .8 this gives .168. A prescribed first-qubit spectrum can further reduce this maximum.

**Implication for an experiment.** A calibrated detector whose eigenvalues lie strictly inside the unit interval can discard a distinguishable part of the response. For a sequential comparison one can score the actually observed bit \(y=0,1\) by
\[
 k_{iy}=d_{i-}+\frac{y-L}{U-L}(d_{i+}-d_{i-}).
\]
Here the \(d_{ij}\) are the predictable coefficients for spectral outcome \(j\) from the preceding page. Direct substitution gives \(\sum_y k_{iy}r_{iy}=\sum_j d_{ij}v_{ij}\). Replacing tested-arm success coefficients by \(k_{iy}\) and retaining the reference score gives another nonpositive conditional mean. The allowed stake must keep every factor nonnegative; small \(U-L\) can make the coefficients large. The detector spectrum and its transfer across histories require independent characterization. Uncertainty in either eigenvalue requires joint propagation.

\newpage

# A complete basis of four preparations

For a common two-qubit branch, a complete trusted computational basis, and the same first-output-qubit click effect \(E\otimes I_2\) on both tested inputs, \(p_*=\sum_i s_i/4\). Write \(S=\sum_i s_i\) and \(\epsilon=1-w_0\). Then the resolved first pair obeys \(D\le2\epsilon S\). Choose the four arm probabilities \(\pi_i>0\) before each draw. For a success on input 0 or 1, score \((d_{iy}-2\epsilon)/\pi_i\) with \(d_{0y}=1-t_y,\;d_{1y}=1-1/t_y\). For a success on input 2 or 3, score \(-2\epsilon/\pi_i\), and score zero on failure. Assignment weighting gives conditional mean at most \(D-2\epsilon S\le0\). Nonnegative stakes that preserve nonnegative factors produce a test supermartingale. A single prespecified product reaches 20 with probability at most .05 under the conditional null, by Ville's inequality.

If the last two success rates are separately resolved, the full necessary condition is
\[
 D+(\sqrt{s_2}-\sqrt{s_3})^2\le2\epsilon S .
\]
The extra term is the minimum cost of unequal norms in the aligned columns for inputs 2 and 3. For a common rank-one projective first-qubit output with otherwise unrestricted marginals, both costs are attained together. This makes the inequality sufficient in that class. For a nonprojective common effect with known eigenvalues, the same statement holds with \(D\) evaluated on the inverted spectral masses. Two different first-qubit effects with matching spectra can yield different probabilities on identical outputs. A shared second-qubit detector can also distinguish the two identity-channel outputs perfectly at \(w=1\). The proof and the sequential score are in *Four-Preparation Tests for a Conditional Quantum Operation*, Propositions 1 and 2.

Recording the same first-qubit outcome on the last two inputs further replaces \((\sqrt{s_2}-\sqrt{s_3})^2\) by \(D_{23}\). The four-row criterion \(D_{01}+D_{23}\le2\epsilon S\) is sharp for a common projective readout and otherwise free outputs. For rows \((9,4),(4,9),(16,9),(9,16)\) in hundredths, the sharp weight changes from \(75/76\) to \(37/38\). With all first marginals prescribed, pairwise purification overlaps give the exact maximum.

**Interpretation.** All four counterfactual assignments at a committed history must share one physical operation. Uniform assignment realizes the maximally mixed input as a basis average. Unequal private assignment probabilities require weighting. A threshold crossing tests the combined preparation, branch, readout and conditional weight assumptions. The proof supplies a size bound. Power depends on the alternative and design.

**References.** D. K. Hammond, P. Vandergheynst and R. Gribonval, *Appl. Comput. Harmon. Anal.* **30**, 129–150 (2011). [DOI](https://doi.org/10.1016/j.acha.2010.04.005). J. Watrous, *The Theory of Quantum Information*, chapters 2–3 (2018). [Text](https://cs.uwaterloo.ca/~watrous/TQI/). A. C. Keith et al., *Phys. Rev. A* **98**, 042318 (2018). [DOI](https://doi.org/10.1103/PhysRevA.98.042318). P. Wills et al., *J. Res. NIST* **125**, 125003 (2020). [DOI](https://doi.org/10.6028/jres.125.003). G. A. L. White et al., *PRX Quantum* **3**, 020344 (2022). [DOI](https://doi.org/10.1103/PRXQuantum.3.020344).
