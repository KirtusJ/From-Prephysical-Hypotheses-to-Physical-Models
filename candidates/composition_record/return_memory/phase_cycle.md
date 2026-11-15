# Three phases test a fixed power response at the return detector

Prepare one excitation at site 0, run two monitored rounds, and select the shots in which both site-0 measurements reported zero. At the same gate angle in every arm, give the survivors one of three phase shifts and count their returns on round three. The ordinary binary response predicts that the middle phase gives the mean of the two endpoint return rates. Every fixed, finite, positive power other than one predicts a strict difference under the instrument assumptions below. The proposal uses the three-spin XX circuit of Liu, Tornow, Kessler and Barkai; their archived grid did not include the gate angle \(\pi/4\) or this phase intervention. [Original experiment, §VIII](https://arxiv.org/html/2401.09810v2#S8) · [Archived QASM order and counts](../first_return_data/README.md)

## Survivor and readout

Set the RXX and RYY angles to \(\pi/4\) on link (1,2), then on (0,1), in each round. Measure site 0 after each round. Each link pair acts as \((I-iX)/\sqrt2\) on its two occupied-site alternatives. Assuming ideal projections, the unnormalized surviving \((1,2)\) amplitudes after two rounds are \((-i/(2\sqrt2),-1/2)\), with squared norm \(3/8\). Their normalized column is \((-i/\sqrt3,-\sqrt{2/3})^\mathsf T\). On physical qubit 2, apply \(\mathrm{RZ}(\phi)\) between the second measurement and the third gate round. On these two sites this multiplies the second entry by \(e^{i\phi}\), up to a global phase. The third-round return row is \((-i/2,-1/2)\). The squared return amplitude in the prepared survivor is therefore

$$
p(\phi)=\left|-\frac1{2\sqrt3}+\frac{e^{i\phi}}{\sqrt6}\right|^2
=\frac14-\frac{\sqrt2}{6}\cos\phi.
$$

For \(\phi=0,\pi/2,\pi\), the three values \(p_-,m,p_+\) are approximately 0.014297740, 0.250000000 and 0.485702260. They are equally spaced and strictly below \(1/2\). Here \(p\) is a squared coordinate available from the stipulated unitary and normalized state. Its interpretation as a click probability is precisely what is being compared. Likewise \(3/8\) is the ordinary model's selection probability; the proposed analysis uses the **actual number of selected shots in each arm**. [Three-site transfer calculation](angle_pairs/README.md) · [IBM RZ gate definition](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate)

Let the binary apparatus assign a true click chance

$$
g_q(p)=\frac{p^q}{p^q+(1-p)^q},\qquad 0<q<\infty.
$$

The two cells presented to this response must be “excitation at site 0” and its whole complement. Scoring sites 1 and 2 separately before pooling is a different readout. Suppose the recorded return rate at each phase is \(y(\phi)=a+b\,g_q(p(\phi))\). Here \(a\) is the false-positive probability and \(a+b\) the true-positive probability; both lie in \([0,1]\), with the same \(b\ne0\) across arms. Measure

$$
D_y=y(\pi/2)-\tfrac12[y(0)+y(\pi)]=bD_q,\qquad
D_q=g_q(m)-\tfrac12[g_q(p_-)+g_q(p_+)].
$$

On \(0<p<1/2\), differentiation gives \(g_q'=qg_q(1-g_q)/(p(1-p))>0\). The sign of \(g_q''\) is the sign of \(q(1-2g_q)-(1-2p)\). For \(q>1\), the odds transformation makes \(g_q<p\), so this quantity is strictly positive. For \(0<q<1\), \(g_q>p\) and the quantity is strictly negative. Thus \(D_q<0\) for \(q>1\), \(D_q>0\) for \(q<1\), and \(D_1=0\). The endpoint separation and nonzero gain are essential. A fully dephased survivor or a phase-blind instrument can produce a flat record. Inspect the endpoint contrast \(y(\pi)-y(0)\) as well as the midpoint contrast.

## An explicit mixture that passes the midpoint test

Draw \(q=1/2\) with probability \(w\) and \(q=2\) otherwise, with the same draw distribution in the three survivor arms. The two midpoint contrasts are \(D_{1/2}=0.0658549242900\ldots\) and \(D_2=-0.1358191193971\ldots\). Choose

$$
w=\frac{-D_2}{D_{1/2}-D_2}=0.673458601384\ldots .
$$

This mixture has exactly zero midpoint contrast for any common fixed \(a,b\). With a perfect final reporter its three rates are 0.072459624, 0.279157096 and 0.485854569. They differ from the ordinary probabilities at the same calibrated gain. If the gain and offset are unknown, the *entire triple* also has an ordinary-response explanation. Fit the endpoint line with slope \(b'=(y(\pi)-y(0))/(p_+-p_-)=0.876943107\ldots\) and intercept \(a'=y(\pi/2)-b'm=0.059921320\ldots\). The midpoint identity makes the fit exact, and both \(a'\) and \(a'+b'=0.936864427\ldots\) are valid reporting probabilities. With independent draws per survivor, binary count distributions at these three settings alone cannot distinguish these two models.

## Two calibrated phases identify a mixture of positive powers

Independently calibrate the same binary instrument on certain dark and bright preparations, with settings \(p=0,1\), to measure \(a\) and \(a+b\). The endpoint responses \(g_q(0)=0,\ g_q(1)=1\) hold for every positive finite \(q\). Under a common readout law with \(b\ne0\), the resulting quantity \(z(p)=(y(p)-a)/b\) is the survivor population mean \(E[g_q(p)]\). In the cycle, \(\phi=\pi/2\) gives \(p=1/4\). One extra phase \(\phi=\arccos(9/(10\sqrt2))\) gives \(p=1/10\). The odds against a click are 3 and 9 before scoring. For each \(q\) define

$$
T=\frac{3^q-1}{3^q+1}=1-2g_q(1/4),\qquad
h(T)=\frac{2T}{1+T^2}=1-2g_q(1/10).
$$

The same \(q\)-distribution at the two phases therefore gives \(E[T]=1-2z(1/4)\) and \(E[h(T)]=1-2z(1/10)\). It may arise from a persistent device type or be redrawn independently for each survivor. On \(0<T<1\), \(h''(T)=-4T(3-T^2)/(1+T^2)^3<0\). If the calibrated rates are the ordinary \(1/4,1/10\), their two moments are \(1/2,4/5=h(1/2)\). Equality in strict concavity forces \(T=1/2\) almost surely, hence \(q=1\). The two preparations need not share an individual type draw. They must sample the same distribution among the histories that reach the final measurement.

There is a finite-error bound from the tangent at \(T=1/2\). Define the observable calibrated contrast

$$
S=\frac45+\frac{24}{25}\left(E[T]-\frac12\right)-E[h(T)].
$$

Pointwise the tangent gap is \((T-\tfrac12)^2(24T+32)/(25(1+T^2))\). Its coefficient is at least \(28/25\), since \(24T+32-28(1+T^2)=4(1-T)(7T+1)\ge0\). Thus \(E[(T-1/2)^2]\le25S/28\), with no tail assumption on \(q\). If the two calibrated rates are respectively within \(\epsilon_1,\epsilon_2\) of \(1/4,1/10\), substitute \(S\le(48/25)\epsilon_1+2\epsilon_2\). For any \(d>0\), the fraction with \(|T-1/2|\ge d\) is at most \(25S/(28d^2)\). A negative empirical estimate of \(S\) should be retained with its uncertainty. Calibration errors in both \(a\) and \(b\) and counting errors at both phases must enter any reported upper bound. The test requires a lower bound on \(|b|\) to control division.

This conclusion assumes response at the two whole cells follows the same power family. Preparing site 0 or an unmonitored site at the readout plane can supply the bright/dark controls if the apparatus responds identically on those preparations and on the previously monitored survivors. Calibration must address any dependence on the selected history, phase choice or device population. Common mean endpoint rates alone do not establish that the individual gain is independent of the type. With type-dependent gain of one sign, endpoint normalization instead averages with weights proportional to the gain; zero-gain types are invisible. With mixed signs the normalized weights need not define a probability law. A general response outside the power family may agree on all finitely many settings.

## Counts and controls

Randomize the phase after the recorded \(00\) history, or preassign it independently and conceal the setting from all earlier operations. Interleave the arms, keep their delays and compilation matched, and retain all shots, including failed preparations and every earlier history. For phase \(j\), let \(n_j>0\) be its number of \(00\) histories and \(x_j\) the number ending in \(001\), in chronological order. Substitute \(x_j/n_j\) for \(y(j)\). Under independent shots with a common conditional rate in each arm, a two-sided \(1-\alpha\) interval for \(D_y\) has half-width

$$
\sqrt{\tfrac12\log(2/\alpha)
  \left(\tfrac1{4n_0}+\tfrac1{n_{\pi/2}}+\tfrac1{4n_\pi}\right)}
$$

conditional on the arm sizes. No finite null result establishes exact equality or distinguishes powers arbitrarily close to one. [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)

The three predictions require a shared coherent survivor, the relative phase reference, and a stable binary response. A prior recorded null can misclassify the true projection; an angle error or phase-dependent detector gain can curve the observed record even with an ordinary final response. A separate preparation/readout calibration should check leakage, the phase origin and its quadrature, endpoint contrast and changes in final reporting across arms. Testing a second quadrature at \(3\pi/2\) would check the phase origin. These are controls on an imported quantum-circuit model. The original walk's dynamics and records would still have to supply or independently support these ingredients to select an embedding there. [Evidence on history-dependent recorded outcomes in the original dataset](README.md)
