# A12-C16 — Exact two-copy invariant calibration and composite confidence theorem

## A. Definitions and prior source

Take the two-level auxiliary space \(\operatorname{span}(|0\rangle,|2\rangle)\) with number charges 0,2, \(P=|2\rangle\langle2|\), and an auxiliary density matrix \(\tau\). Define the basis-fixed coherence
\[
 z(\tau)=2\langle2|\tau|0\rangle,\qquad |z|\le1.
\]
The archived A12-C15 reference model has \(R\) on \(|00\rangle,|01\rangle,|10\rangle,|11\rangle\), \(\gamma=\langle10|R|01\rangle\), outer populations \(a=R_{00,00}, b=R_{11,11}\), and \(d=2|\gamma|\le1\). The target X/Y measurements on product \(\tau_X\otimes R,\tau_Y\otimes R\) yield
\[
 x=\operatorname{Re}(z_X\gamma),\qquad y=\operatorname{Im}(z_Y\gamma).
\]
Their physical realization is **not** established; neither is the availability of coherent auxiliary preparations under strict superselection.

## B. Charge-conserving exchange identity (exact)

On two auxiliary qubits in the ordered basis \(|00\rangle,|02\rangle,|20\rangle,|22\rangle\), define
\[
 W=|02\rangle\langle20|+|20\rangle\langle02|.
\]
This Hermitian observable satisfies \(\|W\|_\infty=1\), \(\operatorname{spec}(W)=\{-1,0,1\}\), and \([W,N_A+N_B]=0\). It preserves each joint charge sector, including the charge-2 sector containing \(|02\rangle,|20\rangle\).

For independent product preparations \(\tau_i\otimes\tau_j\), explicit multiplication gives
\[
 q_{ij}:=\operatorname{Tr}[W(\tau_i\otimes\tau_j)]
 =2\operatorname{Re}(\langle2|\tau_i|0\rangle\langle0|\tau_j|2\rangle)
 =\tfrac12\operatorname{Re}(z_i z_j^*).
\]
Three pair-preparation means therefore determine the **squared relative drift** exactly:
\[
 \boxed{\nu^2:=|z_X-z_Y|^2
 =2(q_{XX}+q_{YY}-2q_{XY}).}
\]
No *absolute* phase reference enters this identity; the common simultaneous \(U(1)\) rotation changes \(z_X,z_Y\) by the same phase and leaves each \(q_{ij}\) invariant. The **existence and reproducibility of the coherent paired preparations remains a substantive assumption**. Measuring \(W\) is assumed operationally available, not derived from number conservation alone.

## C. Finite-shot drift upper confidence bound

Use three independent, predeclared groups of exchange measurements with sizes \(m_{XX},m_{YY},m_{XY}\), bounded outcomes in \([-1,1]\), group means \(\hat q_{ij}\). Let \(0<\beta<1\) and suppose **independent, previously certified deterministic instrumental mean-bias bounds** \(c_{ij}\ge0\) between ideal and apparatus means. Hoeffding and a union bound give simultaneous
\[
 |\hat q_{ij}-q_{ij}|\le s_{ij}
 :=c_{ij}+\sqrt{\frac{2\log(6/\beta)}{m_{ij}}}
\]
with probability at least \(1-\beta\).

Define
\[
 U=2\left(\hat q_{XX}+\hat q_{YY}-2\hat q_{XY}
              +s_{XX}+s_{YY}+2s_{XY}\right),
\quad
 \boxed{\nu_U=\min\{2,\sqrt{[U]_+}\}.}
\]
On the calibration-success event, \(\nu\le\nu_U\) because \(0\le\nu\le2\). A negative \(U\) under ideal assumptions can only occur outside this event or from inconsistent input data. Fail-closed operational handling should also flag such anomalies.

The statistical guarantee pertains to *the same* states \(\tau_X,\tau_Y\) appearing in both calibration and target preparations. Drift between calibration and target phases invalidates that identification unless a separately justified stationarity/transfer bound is added.

## D. Compound finite-sample negativity certification

Independently of the three exchange means, obtain four predeclared groups of target observations of the archived C15 ideal X/Y joint observables and reference populations \(a,b\). Let their means be \(\hat x,\hat y,\hat a,\hat b\), counts \(m_X,m_Y,m_a,m_b\), and deterministic validated systematic-mean bias bounds \(b_X,b_Y,b_a,b_b\). For \(0<\alpha<1\) set
\[
r_X=\sqrt{2\log(8/\alpha)/m_X},\quad r_Y=\sqrt{2\log(8/\alpha)/m_Y},
\quad r_a=\sqrt{\log(8/\alpha)/(2m_a)},\quad r_b=\sqrt{\log(8/\alpha)/(2m_b)}.
\]
Let
\[
 u_X=[|\hat x|-r_X-b_X]_+,\quad u_Y=[|\hat y|-r_Y-b_Y]_+,
\quad a_U=\min(1,\hat a+r_a+b_a),\quad b_U=\min(1,\hat b+r_b+b_b).
\]
By the validated C15 drift inequality, with \(g(v)=\min(1+v,\sqrt2)\),
\[
 \boxed{d_L=\min\left(1,\,2\max\left\{u_X,u_Y,
 \frac{\sqrt{u_X^2+u_Y^2}}{g(\nu_U)}\right\}\right)\le d.}
\]
The inequality uses only \(v_U\ge |z_X-z_Y|\), product preparations, correct joint observables and a common stable reference \(R\) across the four target groups.

Define
\[
 F(d,a,b)=\tfrac12\left[\sqrt{(a-b)^2+d^2}-(a+b)\right]_+.
\]
On simultaneous success, \(\mathcal N(R)\ge F(d_L,a_U,b_U)\). With union bound (independence **between** calibration and target datasets not required if individual conditional bounds remain valid),
\[
 \boxed{\Pr\{\mathcal N(R)\ge F(d_L,a_U,b_U)\}\ge1-\alpha-\beta.}
\]
For any separable \(R\), the rule \(d_L>2\sqrt{a_Ub_U}\) has false-positive probability at most \(\alpha+\beta\) under all assumptions. If bias bounds themselves hold only probabilistically, their total failure probabilities must also be included.

No claim that these observations, resources, or calibrations are actually physically available is made.

## E. Mathematical resource limitation

The calibration uses \(2(m_{XX}+m_{YY}+m_{XY})\) auxiliary copies, *in addition to* one auxiliary for each target X/Y reading. Under equal calibration groups \(m\) and zero instrumental bias, at truly zero drift and ideal mean readouts, the conservative upper bound is
\[
 \nu_U=\min\left\{2,\sqrt{8\sqrt{2\log(6/\beta)/m}}\right\}\quad \text{(ideal mean-readout evaluation).}
\]
Thus the worst-case **certificate magnitude scales as \(m^{-1/4}\)** at this point; this is a limitation of this concentration construction, **not** a minimax lower bound for all protocols. In the actual finite-shot experiment \(\nu_U\) is random and can be larger than this ideal-evaluation quantity. To improve on C15's unconditional coordinate-only fallback using \(g(\nu_U)<\sqrt2\), sufficient calibration strength must certify \(\nu_U<\sqrt2-1\).

## F. Limits and prior art

This is a task-specific combination of finite-dimensional charge-conserving matrix observables, quadratic coherence identities and the established Hoeffding concentration theorem. Claim no novelty or external peer review. The two-copy states \(\tau_i\otimes\tau_j\), instrumental realization of \(W\), reproducible phase relationships, stable \(R\), product auxiliary/reference preparations, fixed shot allocation and independence *within* each group are not consequences of the algebra. The auxiliary charge is an ordinary physical representation label in this benchmark, not a physical frequency or R ontology. Physical R stays `UNSELECTED`.
