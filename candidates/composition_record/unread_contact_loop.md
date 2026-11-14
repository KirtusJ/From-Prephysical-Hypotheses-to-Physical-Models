# Two walkers can entangle through an unread contact record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two walkers, initially independent, visit the same blank register twice each. Each visit couples just one walker to the register. In the stipulated coherent walk, their last visits restore the register's ordinary coordinates. Its center records whether both walkers chose route one. Tracing out this record leaves the walkers entangled. A single terminal position measurement on each walker witnesses that entanglement, with every incident launch counted. The earlier [shared tally](../../Director_G/A_shared_five_state_record_for_two_walks.md) needed a successful flag. The difference is the Boolean function of the routes which the memory records.

## The four visits

Use the candidate's [two determinant contacts](contact_flight.md), \(g\) and \(h\), on the field-five register with multiplication
\[
 (r,l,z)(a,b,c)=(r+a,l+b,z+c+(rb-la)/2).
\]
The controls implement coherent right multiplications and their inverses. Prepare each walker at its origin on the right rail, and give it one free Hadamard-and-shift tick. Name the resulting right and left paths \(0,1\), respectively. On these paths the launch state is \(|+\rangle_A|+\rangle_B\). Hold the alternatives while the bus visits A, B, A, B. With \(a,b\) their local path bits the chronological multipliers are \(g^a,h^b,g^{-a},h^{-b}\). The product is \((0,0,ab)\), including on an arbitrary starting triple. Only the input \(11\) moves the center. Each station must erase the routing scratch coherently. Resetting the bus between visits, or leaving a copy of an individual route at either station, changes the prediction. Space separation requires transport time between visits.

Let \(T\) translate the center by one. For any initial bus density matrix \(\sigma\) independent of the two walkers let \(\gamma=\mathrm{tr}(\sigma T)\). Up to complex conjugation from the row convention, four times the reduced density matrix of the walkers is
\[
 4\rho=
 \begin{pmatrix}1&1&1&\bar\gamma\\1&1&1&\bar\gamma\\1&1&1&\bar\gamma\\
 \gamma&\gamma&\gamma&1\end{pmatrix}.
\]
The first three alternatives have identical final memory. On a named blank \(\gamma=0\), so the memory provides a perfect record of the Boolean conjunction. Ignoring it retains the coherences among \(00,01,10\). The upper-left three-by-three principal minor of \(\rho^{T_B}\) is \(-|1-\gamma|^2/64\). Every \(\gamma\ne1\) therefore gives entanglement. For \(\gamma=1\) the outputs remain the incident product. A positive partial transpose is necessary for separability and sufficient on two qubits. [Horodecki, Horodecki and Horodecki](https://arxiv.org/abs/quant-ph/9605038)

In a resolved central character the same word is a geometric controlled phase. This gate has a finite-dimensional ancillary-qudit precedent. Here a sharp coordinate blank contains all central characters. Tracing the register averages **joint controlled phases**. By contrast, tracing an additive tally \(a+b\) averages products of local phases, which preserve separability. An initially diagonal central-coordinate mixture has \(\gamma=0\) as well. A blank diagonal density matrix does not make the four controlled contacts classical throughout their execution. A classical message relay between independent systems using only local quantum operations leaves the walkers separable. A hidden direct joint gate or suitably pre-existing correlations would evade that inference about the mediator. [Proctor, Dooley and Kendon, Eqs. 21–25](https://arxiv.org/pdf/1402.6674)

## A single fixed pair of position detectors

The [classification by contact endpoints](route_partitions.md) proves that this blank-register protocol attains the maximum concurrence of one half with fixed binary routes. The [Lean certificate](ContactBus.lean) verifies the witness matrix and the blank noise threshold.

After disconnecting the bus, let each walker take two more free ticks. Independently collect both rails at each of the four wells \(x=-3,-1,1,3\), with no walls in the three-tick light cone. In the ordered input code, the three independent entries \(00,01,11\) of the four effects, in units of \(1/4\), are
\[
 (0,0,1),\quad(1,-1,2),\quad(2,1,1),\quad(1,0,0).
\]
This one local measurement spans \(I,X,Z\) over real linear combinations. Give an outcome the two numerical scores \(x_X=(2,-2,2,-2)\) and \(x_Z=(-4,0,0,4)\) in site order. Their expectations are \(\langle X\rangle\) and \(\langle Z\rangle\). They are estimators, not the possible outcomes of projective Pauli measurements. Independent local effects let products of scores estimate products of operators on the same trial.

Put \(P_\pm=(I\pm X)/2\), and use the operator
\[
 W=I-P_+\otimes P_++Z\otimes P_-+P_-\otimes Z+\tfrac12 Z\otimes Z.
\]
In the computational basis take \(v=(3,-1,-1,-1)/2\), \(V=vv^{\mathsf T}\). Expansion gives \(W=(V+V^{T_B})/2\). For a separable state both the state and its partial transpose are positive, so \(\langle W\rangle\ge0\). Direct substitution yields \(\langle W\rangle=-(1-\mathrm{Re}\,\gamma)/8\). Since \(|\gamma|\le1\), this real test detects every nonproduct member of the above family. Each walker needs a stable local phase convention between its source and its free evolution. Neither a shared imaginary-quadrature reference between stations nor an intermediate measurement of the bus is used.

On a blank, the incident-count prediction for the ordered pair of positions is
\[
 \frac1{64}\begin{pmatrix}
 1&3&3&1\\ 3&7&5&1\\ 3&5&19&5\\ 1&1&5&1
 \end{pmatrix}.
\]
Replacing \(X,Z\) in \(W\) by the two numerical scores on each side gives the trial weight. Its mean is **\(-1/8\)**. The replay gives zero with commuting contacts, \(5/8\) with an unread additive tally and \(3/4\) with complete copies of both paths. At each earlier common read clock (zero or one free tick after the bus) the position probabilities agree with the copied-path control. Both extra ticks have a role. The score ranges from \(-57/4\) to \(83/4\), so total variation less than \(1/280\) from the ideal 16-cell distribution guarantees a negative mean. This is a conservative error guarantee. Losses, drift, finite-sample uncertainty and possible support outside the two-path code require calibration when using actual data.

For the specific white-noise model \((1-b)\rho+b I/4\), the displayed witness detects a blank for \(b<1/7\). There is also a sharp limit for *any* analysis of these same complete position counts. Let \(\Sigma\) be the average of \(\rho,\rho^{T_A},\rho^{T_B},\rho^T\). The effects span exactly the local real symmetric matrices, so the counts determine \(\Sigma\). For separable states this average is positive. Conversely if it is positive it is a state equal to its own partial transpose, hence separable in this two-qubit code, with exactly the observed position counts. On a blank,
\[
 8\Sigma=\begin{pmatrix}2&2&2&1\\2&2&1&0\\2&1&2&0\\1&0&0&2\end{pmatrix}.
\]
The antisymmetric eigenvector on \(01,10\) has eigenvalue one in this matrix. Its other three eigenvalues have form \(2-y\) with \(y^3+y^2-9y-1=0\). For the largest root \(y=2.603875\ldots\), the least eigenvalue reaches zero under white-noise mixing at \(b=1-2/y=0.231914\ldots\). Below that value, some real combination of the same 16 counts excludes all separable states. At and above it a separable state reproduces all the counts. This cutoff belongs specifically to the named noise model.

Optical and trapped-ion gates provide physical precedents for creating joint phases using a mediator. In the trapped-ion geometric phase experiment the reported even spin population 0.98 and parity contrast 0.955 give Bell fidelity 0.9675 in the authors' analysis. Those spins and their motional mode do not implement the current detector or the proposed field-five carrier. [Leibfried et al., Fig. 3](https://doi.org/10.1038/nature01492)

## Using the same contacts for a two-body force

With integer exponents the same closed loop writes \(AB\) to the center while restoring the ordinary labels, even when \(A\) depends only on walker A's position and \(B\) only on walker B's. This supplies one concrete local coupling for the earlier [two-body continuum estimate](../../Director_G/Periodic_interaction_and_two_limits.md), which had a gain button taking the two positions as simultaneous inputs. It also changes a symmetry at finite lattice spacing.

On a ring of \(N\) sites divisible by four, write \(Y_x=2\pi x/N\). Fix real \(\kappa\ne0\). Use the extended prime-\(p\) contact family, \(p\ge5\), and the central sector \(k=2\), where a write of \(z\) has phase \(\exp(-4\pi i z/p)\). Choose
\[
 R=\sqrt{p\delta^2|\kappa|/(4\pi)},\qquad C_x=\operatorname{round}(R\cos Y_x),\quad
 S_x=\operatorname{round}(R\sin Y_x).
\]
Run two consecutive commutator loops with the local exponents \((-\mathrm{sgn}(\kappa) C_x,C_y)\) and \((-\mathrm{sgn}(\kappa) S_x,S_y)\). Then release both walkers through their ordinary coins and shifts. The effective kick approximates \(\exp[-i\delta^2 W(Y_x,Y_y)]\) for \(W=-\kappa\cos(Y_x-Y_y)\), equivalent up to a scalar per tick to the previous \(W=\kappa[1-\cos(Y_x-Y_y)]\). Each rounded two-vector lies within \(1/\sqrt2\) of its intended vector of length \(R\). Expanding their dot product gives the uniform angle-error bound
\[
 \theta\le(4\pi/p)(\sqrt2 R+1/2).
\]
Consequently the spinor error over \(n\le T/(\varepsilon\delta^2)\) gains at most \(n\theta\) by unitarity. For fixed bounded \(\kappa,T\), \(p(\varepsilon\delta)^2\to\infty\) suffices for this error to vanish. The number of memory labels must grow. For example one may take \(p\) prime between \(N^3\) and \(2N^3\) along growing \(4\mid N\), with \(2\pi/N=\varepsilon\delta\). A norm estimate on the spinor is needed here because a small potential approximation at one tick can accumulate over the flight.

Under the regularity and prepared-band assumptions of the two-body estimate, fixed \(\varepsilon=1,\ \delta\to0\) gives the two-body Schrödinger evolution. For shrinking localized phase-space packets and \(\delta^2/\varepsilon\to0,\ \varepsilon\to0\), their positions concentrate on the coupled Hamilton trajectories with forces \(-\kappa\sin(Y_A-Y_B)\) and \(+\kappa\sin(Y_A-Y_B)\). For separable prescribed initial packets one can instead [herald the conjugate pair](sector_preparation.md), start with each local packet's real magnitudes, and encode its phase by the nearest central shift. On a fixed character these shifts add the two local phases, with total input norm error at most \(2\pi/p\). The conjugate sector prepares the conjugate spinor and field and gives identical position probabilities at every tick. The herald's residual wrong-sector probability bounds the additional error in the position law. The blank used for the single-run entanglement test does **not** by itself prepare this selected force for a long flight.

Each potential kick needs eight signed runs of at most \(\lceil R+1/2\rceil\) generator slots, including coherent idle slots so the elapsed time leaves no record of the local exponent. The two stations need coherent clocks, local periodic tables and the same spatial origin. If the bus moves between distant stations, travel and inverse visits take time in addition to these slots. The continuum clock counts a fully completed kick and its following two walker steps (one step per walker) as a tick. Deriving that effective duration or a finite-speed instantaneous two-body potential from the hardware remains open. Rounding local sines and cosines separately also breaks exact common lattice-translation symmetry at some finite sizes; exact conservation of total lattice momentum from the earlier relative-coordinate rule does not transfer. For a norm comparison with the earlier shifted potential, restore its global phase \(\exp(-in\kappa\delta^2)\) on the simulated state, or compare directly with the Hamiltonian for the displayed negative cosine. The uniform phase-error estimate suffices for the continuum comparison. At \(N=96,p=1{,}000{,}003,\varepsilon=1\) the measured maximum per-tick angle error in the numerical construction is \(0.000220\), and its analytic bound is \(0.000334\).

Run the [exact count and numerical phase checker](check_unread_loop.py) with `--check`. It retains every finite position count, all four controls, the local readout weights and the force error and symmetry residual at each tested size and action. [Retained results](unread_loop_results.json)
