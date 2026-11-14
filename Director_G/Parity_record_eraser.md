# Reading both interference outcomes of a first-direction record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The walk can use its usual two-rail coin to read a stored first direction in a second basis. For a localized rail launch, both outcomes contribute to reconstructing the original terminal position and rail distribution. At one detector the model predicts three distinct frequencies for coherent on-site response, a radius-one response, and an unread copy of the first direction. This is a proposed instrument. Its predictions rely on independently specified preparation and detector laws.

## A physical analyzer with no spare ports

Use the integer line, a sharp launch at zero on rail \(R\) or \(L\), and the homogeneous Hadamard walk \(U=SH\), with rail order \((R,L)\) and the left-to-left sign negative. Store the first direction after the first tick by swapping \((1,R)\) and \((2,R)\). At preparation depth \(t\geq1\), \(x\equiv t\bmod2\) is a logical endpoint. The field at physical \(x\) is the first-left contribution \(D_0(x,c)\), and at \(x+1\) it is the first-right contribution \(D_1(x,c)\). Here \(c=0,1\) denotes the original terminal rail \(R,L\). These \(D\)'s are raw signed word counts and the common amplitude factor is \(2^{-t/2}\). [First-direction encoding and calibration hypotheses](First_direction_in_site_parity.md)

Pair each physical \(x\) of that parity with \(x+1\). Simultaneously transpose \((x,L)\) with \((x+1,R)\) in every pair, then apply one ordinary walk tick. The operation places the two contributions for rail \(c\) in the incoming \(R,L\) ports of \(x+c\). The ordinary splitter sends their sum right and their difference left. The complete terminal decoder is

\[
 (x,c,s)\longmapsto (y,r)=(x+c+1-2s,\ s),\qquad
 A(y,r)=\frac{D_0(x,c)+(-1)^sD_1(x,c)}{\sqrt{2^{t+1}}}.
\]

The physical rail gives \(s\). From \(y-1+2s=x+c\), its known parity determines \(c\), then \(x\). The neighboring pairs do not compete for a port. One cross-rail transposition layer and one ordinary tick suffice for this terminal read. If only same-rail adjacent swaps and local rail exchanges are available, exchange rails at the left endpoint of every pair, swap the paired right ports, and undo the local exchange. This costs three routing layers. In the single-layer convention the clock reads \(t+3\) slots, counting the initial storage swap, analyzer transposition and analyzer tick in addition to the \(t\) preparation ticks. The unit-slot costs and switchable routes are apparatus assumptions. No operation on a surviving hidden copy is implicit in this circuit.

## Using every event

In the \(s=0\) branch the final amplitudes equal the blank walk amplitudes divided by \(\sqrt{2}\). In the \(s=1\) branch the first-right amplitude changes sign. With \(X\) the rail exchange and \(Z=\mathrm{diag}(1,-1)\), one has \((-Z)H=-HX\). Hence for any normalized launch coin vector \(v\) the decoded branch vectors are \(U^t|0,v\rangle/\sqrt2\) and \(-U^t|0,Xv\rangle/\sqrt2\). Each branch has squared norm \(1/2\).

Define \(P\) as reflection about the launch combined with \(J(R,L)=(-L,R)\) on the rail components. It commutes with the conditional shift and anticommutes with the Hadamard, so \(U^tP=(-1)^tPU^t\). For either fixed launch rail, reflection of the measured position and exchange of the measured rail in branch \(s=1\) therefore recovers the blank coordinate distribution; in branch \(s=0\) retain the reported coordinates. The equality holds at every horizon under the squared joint read. Every launch contributes once. This classical decoding restores those terminal frequencies and does not prepare a coherently restored outgoing state. Reflection symmetries of the walk and complementary interference patterns have earlier experimental and mathematical precedents. [Carteret, Ismail and Richmond](https://arxiv.org/abs/quant-ph/0303105) · [Walborn et al., double-slit quantum eraser](https://doi.org/10.1103/PhysRevA.65.033818)

For a general coin density \(\rho\) at the origin, \(J^{-1}X=Z\). The summed, corrected coordinate read therefore equals the blank walk from \((\rho+Z\rho Z)/2\). It works for every rail-diagonal mixture. For a coherent \(|+\rangle=(R+L)/\sqrt2\) launch at one tick the original walk moves right with certainty, whereas the corrected distribution gives each direction \(1/2\). Copying a later direction also changes the identity. With a sharp \(R\) launch and a copy of the **second** direction the same decoding first fails at depth four with total variation \(1/4\).

## A detector that separates three mechanisms

The on-site marker splits according to the two local raw rails \(u,v\), with right probability \(1/2+uv/(u^2+v^2)\). In a second model the denominator also includes the squared rails at the two adjacent sites. Both use a fair default at zero denominator, identical field dynamics, deterministic physical swaps and conservation of one marker. Both agree on all isolated unmodified sharp launches. For the third control suppose the initial record was coherently copied to orthogonal, persistent environmental states. With the ordinary local quantum read, tracing out the extra label replaces \((D_0\pm D_1)^2\) by \(D_0^2+D_1^2\) in that port. A read of the first direction stored in an apparatus can implement this loss of coherence.

For a sharp right-rail launch at \(t=3\), \(x=-1,c=L\), the two counts are \(+1,-1\). After the analyzer transposition they meet at site zero. The squared rail sums at sites \(-1,0,+1\) are \(1,2,2\); the marker mass at zero in each routing model is \(1/4\). Its ordinary right daughter is dark. The radius-one model sends \((1/4)(1/2-1/5)=3/40\) there.

| Complete physical detector | Coherent on-site | Coherent radius-one | Persistent copy with squared read |
|---|---:|---:|---:|
| \((+1,R)\), sum | \(0\) | \(3/40\) | \(1/8\) |
| \((-1,L)\), difference | \(1/4\) | \(7/40\) | \(1/8\) |

At this depth the three models agree on both separate marginals. The branch weights are \(1/2,1/2\), and the uncorrected logical position distribution on \(-3,-1,1,3\) is \((1,3,3,1)/8\). Recording branch and position jointly preserves the contrast. To compare models experimentally one needs the routing and timing controls, a characterized joint detector including background at the dark port, and control over additional records. The completed calculation advances the set of native record tests. It leaves the physical range of the marker response and the unique choice of probability embedding open.

The checker compares the physical compiler with word enumeration at all populated and dark outputs for both sharp initial rails and all eight tested depths. A leaked copy first spoils the corrected sharp-\(R\) endpoint distribution at \(t=3\), with total variation \(1/4\). The case study's eight-site return example likewise distinguishes a final-only record from an intermediate read and from a record at every tick. Here the extra copy is tested as its own instrument. [Checker](check_parity_eraser.py) · [Full terminal panels and adverse controls](results/parity_eraser.json) · [Delegation and scientific review, p. 21](../case_studies/PCP_Delegation_and_Scientific_Review.pdf#page=21)

The [Lean 4.19.0 proof](lean/ParityEraser.lean) checks the unnormalized integer reflection identity by induction at all horizons, the local four-port compiler and the first-arm sign reversal. The density-operator and detector arguments above use additional premises.

## Measuring the response to either neighbor

Consider a stationary marker whose denominator at site \(y\) is \(n_y+\alpha n_{y-1}+\beta n_{y+1}\), where \(n_y=u_y^2+v_y^2\), with unknown finite \(\alpha,\beta\ge0\). The signed field still follows the same walk. All isolated sharp launches continue to agree with on-site calibration because their occupied sites have dark neighbors. The two coefficients describe a proposed dependence of the marker on the local guide. They have no assigned experimental values.

In the sharp-\(R\) setting above, insert three routing slots between the analyzer transposition and its final tick. In the first setting, hold all ports. In the second, swap both rails without mixing them on the successive site pairs \((-1,0),(0,1),(-1,0)\). This permutes the two flanking sites and restores both rails of the central site and its marker mass. Both settings take nine slots from launch through the final split under the one-slot transposition convention. All earlier splits on occupied sites have \(uv=0\); the mass at the central parent is \(1/4\) for every coefficient pair. The earlier controls transport the marker and field by the same permutations. A device that retains intermediate router history can lie outside this comparison.

The two flank norms are \(1,2\) in the hold setting and \(2,1\) after exchange. Thus \(z_1=\alpha+2\beta\) and \(z_2=2\alpha+\beta\) enter as excess denominators over the central norm \(2\). At the same physical daughter pair \(D=(+1,R), B=(-1,L)\) the unconditional detector masses and their odds are

\[
 P_D(z)=\frac{z}{8(2+z)},\qquad P_B(z)=\frac{4+z}{8(2+z)},\qquad
 R(z)=\frac{P_D(z)}{P_B(z)}=\frac{z}{4+z}.
\]

**A directional test needs no relative efficiency calibration.** Suppose the expected counts equal the masses times a positive setting brightness and a stable positive efficiency for each detector. Then the sign of \(C_{D,1}C_{B,2}-C_{B,1}C_{D,2}\) is the sign of \(\beta-\alpha\), since \(R\) is strictly increasing. Both expected dark counts can be zero. The determinant remains defined at this boundary. For \((\alpha,\beta)=(1,0)\) the two dark probabilities are \(1/24\) and \(1/16\); interchanging the coefficients interchanges the results. Sampling uncertainty, background, crosstalk and response changes between schedules require separate treatment.

**For the magnitudes**, prepare one populated incoming rail at the same central splitter with the matched final clock and readout. Since \(uv=0\), both daughter probabilities are equal in this reference for all coefficients. Divide each test setting's dark-to-bright expected count ratio by the corresponding reference ratio. With stable relative efficiencies between each test and its reference this recovers \(R_i\). Setting \(z_i=4R_i/(1-R_i)\) yields

\[
 \alpha=(2z_2-z_1)/3,\qquad \beta=(2z_1-z_2)/3 .
\]

The family predicts \(0\le R_i<1\) and \(z_1\le2z_2,\ z_2\le2z_1\). Invalid values can indicate sampling error or failure of a modeling assumption. The inversion becomes poorly conditioned as \(R_i\) approaches one. In the symmetric subfamily \(\alpha=\beta=\lambda\), even the absolutely calibrated dark probability is one-to-one in \(\lambda\). A hosted PCP worker drafted the exact rational cross-multiplication identity for that last statement, and its parent checked the returned source with Lean 4.19.0. The field equations and measurement model are separate hypotheses. [Lean identity](lean/DarkPort.lean) · [Two-setting checker](check_neighbour_calibration.py) · [All 25 coefficient pairs including zero and large weights](results/neighbour_calibration.json)
