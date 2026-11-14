# One coherent echo and three terminal records

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch one walker for two ticks. Exactly three quarters of its squared norm reaches a specified set of terminal ports. Can those same preparations test whether the detector reports that value? Compare a longer coherent walk with a Boolean combination of three shorter terminal records. A sequence of such comparisons, together with the measured condition that the hit rates stay between \(1/8\) and \(7/8\), forces the native hit rate to \(3/4\). Twelve levels give a finite interval of width below \(0.004\) if the comparisons agree exactly. This inference applies to the rates of the tested preparations even when the readout depends on the complete pulse history.

## The two ways to get a bit

Launch \(|0,R\rangle\) on a line with the real balanced Hadamard followed by a right/left shift. At two ticks the amplitudes in \((-2,L),(0,L),(0,R),(2,R)\) are \((-1,1,1,1)/2\). Call the single launch ray \(|0,R\rangle\) blank and all other ports a hit. For the forward word \(W\) the kinematic hit mass is \(x_0=3/4\). This calculation uses the signed amplitudes and their norm. The tested hit rate \(p_0\) remains free. A detector pooling both rails at site zero measures a different event.

The earlier fixed-point echo provides two coherent operations on this same binary exit. Given a word \(V\), let \(P_0\) select the complete initial blank and choose \(P\) as \(P_0\) or \(I-P_0\). Replace \(V\) by \(VD_{P_0}V^\dagger D_PV\), with \(D_P=I+(e^{i\pi/3}-1)P\). Choosing the blank sends the kinematic nonblank mass \(x\) to \(D(x)=x^3\). Choosing the nonblank target sends it to \(U(x)=1-(1-x)^3\). The identity follows from the selective-phase interference calculation. The walk's three-address signed memory gives the two conjugate sixty-degree phases on a prepared zero-sum plane; the same real mass transformation holds in both. The controls require a matched inverse, the addressed phase and full pooling of the ancillary memory in each exit. There is no intermediate terminal measurement in the coherent word. [Grover, fixed-point quantum search](https://doi.org/10.1103/PhysRevLett.95.150501) · [Both selectable echoes](Testing_a_binary_probability_with_echo_thresholds.md) · [Signed three-address implementation](A_signed_three_address_echo.md)

Precompute a target path using \(F_j=U\) when \(x_j\le1/2\) and \(F_j=D\) otherwise, with \(x_{j+1}=F_j(x_j)\). To test one edge, interleave independent launches of the coherent child word with launches of the parent word. Denote their hit rates by \(p_{j+1}\) and \(p_j\). A second implementation groups **three independent reports at the parent setting**. Read their AND on a \(D\) edge and their OR on a \(U\) edge. For iid reports the Boolean rate is precisely \(F_j(p_j)\). The hypothesis tested on each edge is

\[
p_{j+1}=F_j(p_j).
\]

One can estimate this numerical residual directly from the two marginal rates. If the Boolean implementation is used instead, also compare its frequency to the polynomial in the parent marginal, or independently establish the triple sampling law. The parent marginal must refer to the same population in both comparisons involving that node. Record all launches; define missed-read scoring in advance and monitor its frequency. Use the same source preparation and the specified coherent controls when assigning kinematic masses. The data can otherwise have a different response at each node of the schedule. In particular this test does not require a scalar response law shared by words, an endpoint calibration, a port-exchange symmetry, or monotonicity of response.

## What the comparisons imply

Let \(I=[1/8,7/8]\). The target schedule keeps \(x_j\in I\): cubing a value in \((1/2,7/8]\) yields a value in \(I\), and the reflected calculation holds below the midpoint. Require as a second observable condition that \(p_j\in I\) at every tested node. For \(\ell(s)=\log(s/(1-s))\) the derivative of \(\ell(D(s))\) with respect to \(\ell(s)\) is \(3/(1+s+s^2)\). For \(U\) replace \(s\) by \(1-s\). Both are at least \(\lambda=192/169>1\) throughout \(I\), independent of which side of \(1/2\) the measured rate occupies.

Set \(\Delta_j=|\ell(p_j)-\ell(x_j)|\) and \(a_j=|\ell(p_{j+1})-\ell(F_j(p_j))|\). The mean-value and triangle inequalities give \(\lambda\Delta_j\le\Delta_{j+1}+a_j\). As both terminal rates lie in \(I\), \(\Delta_n\le2\log 7\). The inverse logit has derivative at most \(1/4\). Thus

\[
|p_0-x_0|\ \le\ \frac14\left(2\lambda^{-n}\log 7+
           \sum_{j=0}^{n-1}\lambda^{-j-1}a_j\right).
\]

Exact agreement and the interior condition at every finite depth force \(p_0=x_0\). The argument is about each measured source separately. For any known interior mass outside \(I\), the same prescribed rule takes it into \(I\) in finitely many steps. Apply the argument on that tail and invert the strictly increasing prefix maps, provided their observed comparisons also hold. At \(x=0,1\) the schedule stays there and this band test does not apply. A family of physically tested preparations gives as many root conclusions as there are verified schedules. An unrestricted law at untested settings remains free.

## Finite schedules, errors and counterexamples

For a probability residual bound \(r_j\) on each edge, start with the terminal interval \(J_n=I\). Work backwards with

\[
J_j=I\cap F_j^{-1}\bigl((J_{j+1}+[-r_j,r_j])\cap[0,1]\bigr).
\]

Then \(p_0\in J_0\). Before outward rounding these are exact feasible intervals for scalar rates subject to only the band and the edge residual limits. Each parent value in the interval has some allowed child in \(J_{j+1}\). Measured confidence intervals for individual nodes may further narrow these sets. The following enclosures use integer arithmetic with outward rounding. The error allowance of \(0.001\) is an example tolerance, independent of the number of shots.

| Coherent target choices | Calls to \(W\) or \(W^\dagger\) in the deepest word | Root interval, exact edge rates | Root interval, each edge residual \(\le0.001\) |
|---|---:|---|---|
| DUDD | 81 | [0.742363, 0.793701] | [0.740466, 0.794936] |
| DUDDUUDU | 6,561 | [0.742363, 0.755658] | [0.740466, 0.757985] |
| DUDDUUDUDDUU | 531,441 | [0.748179, 0.752083] | [0.745740, 0.754543] |

Each extra level triples the base-word calls; controlling their accumulated error may limit the depth. If a physical miss, drift, preparation error or gate error changes a rate or a kinematic label, that change needs its own accounting. The finite table reports consequences of constraints on true probabilities. It contains no statistical evidence that a device meets them.

* The bounded monotone complementary rival \(r(s)=s+\tfrac12s(1-s)(2s-1)\) yields \(p_0=51/64\). On the very first \(D\) edge its coherent-child prediction is \(105597/262144\), and three independent parent hits have rate \(132651/262144\). Their absolute discrepancy is \(13527/131072\).
* Without the interior condition the constant zero and constant one readers satisfy both Boolean identities at every depth. Even exact sharp endpoint calibration leaves a reader returning zero on every strictly interior word as a rival. Every finite echo of an interior mass remains interior.
* For a concrete dependence failure, let every node return a fair bit and use the **same** random bit for all three parent records of each Boolean trial. AND and OR then also return a fair bit. All observed Boolean-versus-child comparisons and band tests would pass. Against the polynomial in the marginal, the first discrepancy is \(1/2-(1/2)^3=3/8\).
* Redrawing a hidden response type independently per launch can mask type differences. Two equally likely types with rates \(x_j\pm x_j(1-x_j)/2\) at node \(j\) give population rate \(x_j\) and pass all marginal comparisons. The certificate establishes the population rate. Source-specific transfer to a different population requires new evidence.

The earlier threshold procedure compared a native rate with a randomized reference built from endpoint decisions. Here one prescribed target itinerary and its interior measured rates replace that reference. A signed shell-return test uses a different quadratic echo and a common monotone complementary law. This experiment targets a single native binary event with coherent inverse access and potentially very deep words. Neither these circuit identities nor a successful population test explains the existence of the coherent walk, the apparatus or a complete probability law for all events. [Threshold comparison](Testing_a_binary_probability_with_echo_thresholds.md) · [Signed shell return](Checking_probability_by_reversing_a_shell_sign.md) · [Independent integer checker](check_three_report_echo.py) · [Complete finite intervals and rivals](results/three_report_echo.json)
