# Independent checks in five paper series

Each calculation below starts from a stated model in a reader copy. Page numbers refer to the PDF file, starting at the cover. These checks cover particular propositions or examples. They contain no empirical observations.

| Paper | Calculation | Result |
|---|---|---|
| [A1, p. 5](../A1%20-%20Program%20Overview%20%E2%80%93%20Questions%2C%20Models%20and%20Physical%20Correspondence.pdf#page=5) | Recompute both endpoints of an identified set with uncertain calibration. | The exact interval is \([2/5,3/5]\). |
| [B4, pp. 2–3](../B4%20-%20Four-Preparation%20Tests%20for%20a%20Conditional%20Quantum%20Operation.pdf#page=2) | Construct a nonlocal diagonal success operator and compute its four probabilities and Choi projection independently. | Both discrepancy terms are nonzero and the bound is attained at \(w=13/15\). |
| [C4, p. 4](../C4%20-%20Clock-Scale%20Ambiguity%2C%20Static%20CAR%20States%2C%20and%20Gibbs%20Modular%20Equivalence.pdf#page=4) | Test the sign of modular evolution on an off-diagonal operator and vary both inverse temperature and energy zero. | A quarter turn distinguishes the two signs. Positive rescaling with a compensating temperature gives exactly the same Gibbs state. |
| [E1, pp. 3–4](../E1%20-%20Positive%20Spectral%20Measures%20Under%20Finite%20Moment%20and%20Laplace%20Constraints.pdf#page=3) | Verify the five contact conditions in the explicit nonsingleton-face counterexample. | The same face admits measures with different support thresholds, 1 and 2. |
| [F5, pp. 3–4](../F5%20-%20Statistical%20Precision%20under%20Weak%20Readout%20Gain.pdf#page=3) | Enumerate a four-trial binary experiment and a coarsened experiment that observes only parity. | The full total variation is \(37/125\), and the parity laws agree exactly. |

### A1. Calibration uncertainty

With \(p=1/2,\ f\in[1/5,3/10],\ s\in[7/10,4/5]\), the attainable readout at a fixed \(\theta\in[0,1]\) is exactly \([1/5+\theta/2,\;3/10+\theta/2]\). The two constraints for this interval to contain \(1/2\) give \(2/5\le\theta\le3/5\). At \(\theta=2/5\) the upper calibration corner attains \(1/2\); at \(3/5\) the lower corner attains it. A reference with exact zero contrast \(f=s=1/2\) instead fits every \(\theta\). This tests the projection calculation, including its behavior at zero gain.

### B4. Four preparations

In the paper's input order, take the single Kraus matrix \(K=\operatorname{diag}(1,1/2,3/4,1/4)\); \(K^\dagger K\le I\). A computational-basis measurement of the first output bit gives \(r_0=(1,0),\ r_1=(1/4,0)\) and \(s_2=9/16,\ s_3=1/16\). The resolved discrepancy and unresolved success term each equal \(1/4\). The projection of \(K\) on the local subspace is \(\operatorname{diag}(3/4,3/4,1/2,1/2)\); its squared norm is \(13/8\), against \(S=\|K\|_F^2=15/8\). Thus \(2(1-w)S=1/2\). These data exclude \(w_0=9/10\), whose right side is \(3/8\). Conditioning on success before computing the two outcome distributions would erase the first discrepancy. The calculation tests the per-attempt convention and sharpness for this input.

### C4. Modular and physical time

Choose \(H=\operatorname{diag}(0,1),\ \beta=\log 2\), so \(\rho=\operatorname{diag}(2/3,1/3)\). Direct multiplication sends \(A=|0\rangle\langle1|\) to \(2^{is}A\) under modular evolution and to \(e^{-it/\hbar}A\) under physical evolution. For \(s=\pi/(2\log2)\), \(t=-\hbar\beta s\) gives \(iA\); reversing the sign gives \(-iA\). The second Hamiltonian \(H'=2H+7I,\ \beta'=\beta/2\) has the same normalized Gibbs matrix, since \(\beta H-\beta'H'=-(7\beta/2)I\). Exchanging the eigenvectors of \(H\) at the same temperature exchanges the unequal populations. This check applies to the finite faithful Gibbs claim.

### E1. Why the supporting face matters

Write \(h=\log 2\), \(d=8h^2-23h+12\). For each energy \(j=1,2,3\), independently substitute \(e^{-hj}=2^{-j}\) in the displayed certificate \(F(j)\), and in its derivative for \(j=2,3\). After multiplication by \(d\), each expression is a polynomial of degree at most three in the formal variable \(h\). Exact rational evaluation at \(0,1,2,3\), holding \(2^{-j}\) fixed, gives zero at all four nodes for each of the five polynomials. This proves the five identities at \(\log2\). The printed moments and Laplace observations are obtained directly from the equally weighted atoms \(1,2,3\) and the single atom \(2\). Both are normalized and supported on zeros of \(F\), so their observation vectors have identical supporting functional \(\beta\cdot y=-c_0\). The cylinder in the paper contains both, yet their lower support endpoints are 1 and 2. This checks the counterexample; the three subsequent numerical extremizers have separate certificates.

### F5. Exact distance and a lossy observation

Set \(N=4,\ h=1,\ \kappa=1/5\). The two source probabilities are \(2/5,3/5\). Summing half the 16 absolute differences of the word probabilities gives \(37/125\). Grouping by count gives the same result: only \(k=3,4\) have positive excess under the second law, and the middle count is tied. With \(95\%\) coverage under both alternatives, (2.3) therefore gives a probability of at least \(151/250\) that the interval or set includes both endpoints under the first law. If only the parity of the count is retained, complementing every bit interchanges the two laws and preserves parity for even \(N\). Their new total variation is zero. This tests the distinction between retaining the sufficient count and applying an arbitrary common coarsening.
