# Three position records between coherent flights

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) and the Codex workers.

A Hadamard walker can generate independent displacements without a rail detector, a new coin, a return to the origin or feedback. Read three consecutive positions where one coherent flight meets the next. The first difference identifies the arriving rail. The next difference is a fair sign independent of the preceding record and identifies the outgoing rail. Varying the interval between these boundaries changes the spread from diffusive to ballistic. In a four-tick version, the frequency of returns to the starting site measures the strength of an optional intervening position measurement. Two consecutive return records can test whether that measurement choice persists.

## A position-only boundary

Start at a known site and in a sharp rail \(R\) or \(L\). At each tick apply \(H=(X+Z)/\sqrt2\) on the two rails and stream them by \(+1,-1\), respectively. Assume an unwrapped line and an ideal nondestructive whole-site write with a fresh persistent record. Its projectors leave both rails at each individual site coherent. We use the ordinary squared path rule and its conditional update. For a block of \(T\ge3\) ticks, write position at ticks \(1,T-1,T\) relative to its start. Repeat on the same walker. Denote the signed displacement between consecutive block boundaries by \(D_T\). All record outcomes are included.

At the start of every block the walker occupies a known site and sharp rail: the positions at the two preceding ticks determine its last displacement and hence its rail. At the very first block this is the launch condition. Conditional on the entire preceding transcript, the first new displacement \(s\in\{-1,1\}\) is fair, and its recorded site projects the walker onto the sharp rail corresponding to \(s\). The intervening spatially homogeneous evolution now depends only on \(s\), relative to the new origin. Reading position one tick before the end cannot change the marginal probability of the final site: for a specified final site **and rail**, the previous site is unique. All paths interfering in that terminal cell therefore gave the same penultimate site. Pool over the terminal rails.

In particular, writing \(Q_j^s(z)\) for the unmonitored position law after \(j\) ticks from a sharp site and rail \(s\), we have exactly

\[
K_T(d)=\Pr(D_T=d\mid\hbox{previous records})
       =\tfrac12\sum_{s=\pm1} Q_{T-1}^s(d-s).
\]

Reflection of position together with the rail transformation \(R\mapsto L,\ L\mapsto-R\) commutes with the stream and reverses the overall sign of the Hadamard. Thus \(Q_j^{-}(z)=Q_j^{+}(-z)\), \(K_T\) is symmetric, and successive displacements have the product law of their \(K_T\)'s for fixed lengths. No assertion about positions between recorded times is necessary. A general incoming coin superposition could bias the first sign. It can be handled by initializing from two consecutive observed positions and starting the clock at the second, where every observed displacement has sharp rail. These extra ticks and their records belong to the preparation.

## A four-tick return measures the diffusion rate

Set \(T=4\), with compulsory writes at \(1,3,4\). At tick two either write its complete site or leave the amplitudes coherent. Choose to write with probability \(p\), independently of the walker and previous outcomes. Define \(r\) as the chance the next block boundary returns to the starting site. Direct signed paths give the following probabilities, all expressed in sixteenths.

| Tick-two choice | \(-4\) | \(-2\) | \(0\) | \(2\) | \(4\) | \(\mathbb E D_4^2\) |
|---|---:|---:|---:|---:|---:|---:|
| Coherent | 1 | 6 | 2 | 6 | 1 | 5 |
| Write the site | 1 | 4 | 6 | 4 | 1 | 4 |

Hence \(r=1/8+p/4\), and position records give the model identities

\[
p=4r-\tfrac12,\qquad
\operatorname{Var}(D_4)=5-p=\tfrac{11}{2}-4r .
\]

For independent block choices the boundary-position variance after \(m\) blocks is \(m(5-p)\). With one tick as the time unit, the variance growth per tick is \((5-p)/4\); the diffusion coefficient in the convention \(\operatorname{Var}X_t\sim2D t\) is \((5-p)/8\). A return frequency outside \([1/8,3/8]\) is incompatible at the population level with this binary intervention and its calibrated reads. Other physical mechanisms could give an in-range rate. For instance a continuous partial dephasing with the same reduced channel can have the same terminal position law. The \(p\) inferred here refers to the stated instrument family.

Suppose instead that an exogenous binary timing sequence \(B_1,B_2,\ldots\), with each \(\Pr(B_j=1)=p\), can have dependencies. Conditional on the entire sequence, blocks still regenerate and each has zero mean. Therefore the full \(m\)-block variance is **still** \(m(5-p)\). With \(I_j=1\) for a return at block \(j\), the position records extract the timing covariance at every distinct pair:

\[
16\,\operatorname{Cov}(I_j,I_k)=\operatorname{Cov}(B_j,B_k),\qquad j\ne k .
\]

More generally, for any distinct indices, the joint expectation of \(\prod_j(4I_j-1/2)\) equals that of \(\prod_j B_j\). Indeed each factor has conditional mean \(B_j\) and the block outcomes factor given the exogenous choices. With population probabilities this reconstructs every finite binary timing law by inclusion–exclusion; finite-sample errors of these products can grow rapidly with order. For one bit held fixed through an entire launch, return covariance is \(p(1-p)/16\) at every nonzero lag. With \(p=1/2\), two returns have probability \(5/64\); fresh fair choices give \(1/16\). The shared-choice displacement divided by \(\sqrt m\) tends to the mixture \((1-p)\mathcal N(0,5)+p\mathcal N(0,4)\). Fresh choices give \(\mathcal N(0,5-p)\). An adaptive switch that reads the walker before deciding is a different experiment.

## Varying the coherent flight time

For \(m\) equal blocks of length \(T\) with only the three compulsory writes, put \(V_T=\sum_d d^2 K_T(d)\). From the same native position records,

\[
\operatorname{Var}(X_{mT}-X_0)=mV_T .
\]

Keeping \(T\) fixed and increasing \(m\) gives the ordinary central limit theorem for the boundary walk. For growing \(T\), the first displacement has size one, and each following sharp-rail flight has the Hadamard weak velocity limit with second moment \(c=1-1/\sqrt2\). Bounded speed permits passage to the second moment, so \(V_T/T^2\to c\). For \(N=mT\) and \(m,T\to\infty\), the variance is asymptotic to \(cNT\). The maximum standardized increment is at most \(T/\sqrt{mV_T}\to0\), giving a standard Gaussian limit after normalization by \(\sqrt{mV_T}\) by the Lindeberg theorem. In contrast, one block of length \(N\) gives the symmetric ballistic Konno velocity distribution after division by \(N\). The first random rail averages the two reflected densities. Even the final pair of position writes is present in this one-block case. [Konno, Theorem 1 and second moment](https://arxiv.org/pdf/quant-ph/0206103)

Measurement-induced diffusion and the crossover exponents have a substantial prior literature. Romanelli et al. connected the diffusion coefficient to the interval variance for simultaneous chirality and position measurements. Chisaki et al. proved limit laws for periodic measurements with a separately prepared coin, explicitly discussing the dependence of an unreset coin on the observed position. The extra consecutive site writes above supply an independent outgoing fair sign on the actual same walker. The four-tick law and its return correlations test this construction on named positions. Earlier program work obtains joint coarse records near a prepared Newtonian ray and a different limit under a sharp record on every tick. Stochastic diffusion here concerns the distribution of this deliberately monitored trajectory. It supplies no Hamiltonian force or microscopic origin of the read. [Romanelli et al.](https://arxiv.org/abs/quant-ph/0403192) · [Chisaki et al., Procedures 2–3 and Sec. 3](https://arxiv.org/pdf/1009.2131) · [Earlier sharp and passive trajectories](Rank_paths_and_classical_flight.md)

Even the average rate of writing a site does not settle the transport exponent. At fixed \(T\ge4\), choose a uniform phase of the periodic three-write schedule independently of the launch. Each tick has write probability \(3/T\). After the first full boundary, the displacements regenerate. At most \(2T+O(1)\) initial and final ticks fall outside full blocks, so the launch-to-terminal mean square is \(O(N)\). Compare an exogenous switch that writes every tick with probability \(3/T\) and otherwise writes none through the flight. Each tick has the same marginal write probability, but the no-write fraction has ballistic mean square \(\sim cN^2\), and the fully written fraction has mean square \(N\) from a sharp launch rail. A common terminal survey is additional to both schedules. For two adjacent scheduled ticks the joint write probability is \(2/T\) in the periodic schedule and \(3/T\) with the shared switch. The timing transcript tests this difference. A site read with unlogged losses, a persistent memory coupled back into the walker, a ring reached by the light cone or an unknown coin changes the premises.

The [exact replay](check_position_record_blocks.py) compares signed histories grouped by the actual site writes with a separately propagated coherent-flight kernel, tests two-block factorization for both input rails, and retains every tested displacement and return pattern. The [archive](results/position_record_blocks.json) gives integer counts and denominators. [Lean 4.19](lean/PositionRecordBlocks.lean) checks the finite calibration and the rank-one terminal-rail identity behind the penultimate write.
