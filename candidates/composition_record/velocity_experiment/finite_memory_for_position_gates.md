# How much working memory does a position-record encoder need?

Three terminal messages suffice to recover a Bell fidelity approaching $1/2+1/(2\pi)$ when the sender can use the full position record. A sender with a fixed number of classical working states cannot retain any positive limiting margin over $1/2$, even if it sends its entire final state and the receiver knows the final position and determinant sign. A growing memory can retain a margin with the same three messages. The distinction matters when specifying the controller for the [Bell recovery experiment](recovering_a_qubit_from_position_messages.md).

## Experiment and bound

Prepare the rail and an untouched reference in a Bell pair. On the sixteen-site ring repeat the ideal twelve-tick block and perform an exact position write after each block, preserving the local rails. The increments are independent with the stated ordinary probabilities. A classical encoder reads each position once in order. At any write it has at most $M\ge1$ internal states. We can give it the present position and sign as extra inputs. Its transition and its terminal label can depend on the clock and the prespecified horizon $N$. The receiver acts only once, after write $N$, by a trace-preserving channel on the rail, using the available classical output. The fidelity $F_N$ averages over **all** launches. [Instrument and increment law](classical_positions_with_a_retained_qubit.md) · [Environment-assisted recovery, Gregoratti and Werner](https://arxiv.org/abs/quant-ph/0209025)

Put $c=(11+16i)/\sqrt{377}=e^{i\gamma}$, $\beta=377/4096$ and

$$
C_M=\max_{1\le d\le M}|\cos(2d\gamma)|,\qquad
\rho_M=1-2\beta^M(1-C_M).
$$

For every such encoder and decoder,

$$
F_N\ \le\ \frac12+\frac12\rho_M^{\lfloor N/(2M)\rfloor},
\qquad
\rho_M\ \le\ 1-\frac{2}{4096^M}<1 .
$$

For example, $\rho_1=903/1024$ and $\rho_2=4176079/4194304$. These upper bounds can be loose at laboratory horizons. A one-bit encoder that tracks the determinant sign reaches the limiting $1/2$ by choosing a fixed recovery line in the reported sign plane. A particular encoder can approach a smaller value. Even when the encoder is redesigned for each horizon with at most $M_N$ states, the excess vanishes if $N/(M_N4096^{M_N})\to\infty$.

## Two orders with the same endpoint

The two-write words $u=(0,8)$ and $v=(8,0)$ list displacements. Each advances the position by eight, preserves the determinant sign and has probability $\beta$. Their real $2\times2$ matrices rotate the coefficient plane through $\gamma$ and $-\gamma$, respectively, and act complex-linearly on a general rail qubit. Identifying the two real first-column coordinates with one complex number represents those rotations by $c$ and $\bar c$. The square $c^2=(-135+352i)/377$ has infinite order. Indeed a root of unity and its inverse are algebraic integers, so their sum, if rational, must be an integer. Here the sum is $-270/377$. Consequently $|\cos(2d\gamma)|<1$ for every positive integer $d$. Its numerator over $377^d$ is an integer, the real part of $(-135+352i)^d$, giving $1-|\cos(2d\gamma)|\ge377^{-d}$. [Two orders from the rail matrices](closed_position_gates.md) · [Lean certificate for the order pair and its powers](../../../Director_G/lean/ClosedPositionTransport.lean)

Let $\theta$ denote the angle of the first column of the accumulated rail gate, taken modulo $\pi$, and let $s\in\{+1,-1\}$ denote its determinant. A new gate of angle $\phi$ and sign $\sigma$ acts on the left. It gives $\theta'=\phi+\sigma\theta$ and $s'=\sigma s$. In the coordinate $t=s\theta$ this becomes $t'=t+s'\phi$. Track the complex numbers

$$
h_i=\mathbb E[{\bf1}_{i}\exp(2it)]
$$

on the augmented states $i=(\text{encoder state},\text{position},s)$. Their initial absolute sum is one. Each write transports a row vector of these numbers linearly, weighting each transition by its probability times its unit-modulus phase. The sum of the absolute entries in each transition row is at most one. Hence $\sum_i|h_i|$ cannot increase.

Start at any clock and augmented state. In the next $2M$ writes consider the $M+1$ different words $u^jv^{M-j}$ for $j=0,\ldots,M$. They all finish at the same position and sign, and each has probability $\beta^M$. Two must also finish in the same encoder state. If their indices differ by $d$, their body angles differ by $2sd\gamma$, so their contributions to that entry of the harmonic row have combined magnitude $2\beta^M|\cos(2d\gamma)|$. All remaining paths contribute at most their total probability. The absolute row sum is therefore at most $\rho_M$. This holds for every starting state and every consecutive block of $2M$ writes, without any stationarity of the encoder. Multiplication and the single-write bound give $\sum_i|h_i|\le\rho_M^{\lfloor N/(2M)\rfloor}$. For independently randomized transitions or shared random bits, fix the random tape and apply the same uniform bound, then average. Past outputs stored anywhere and available to later updates count as working memory.

## What the receiver can recover

At each augmented state $i$, the Bell pair lies in the two-dimensional plane of its sign. If its incident probability is $p_i$, the two eigenvalues of its subnormalized density matrix are $(p_i\pm|h_i|)/2$. Giving the receiver $i$ allows it to attain the larger eigenvalue by undoing the real orthogonal gate represented by its principal eigenvector. Every local trace-preserving recovery has Bell effect positive of trace one, so cannot improve that bound. Summing over $i$ proves the displayed result. If the receiver sees only a coarser final label, its best fidelity is bounded by the same expression. [Sign planes and Bell effects](recovering_a_qubit_from_position_messages.md)

There is a state-level statement. Replace each conditional block by $p_i/2$ times the projector onto its sign plane. The resulting flagged state is separable across the receiver and reference. Each normalized replacement equals $(I\otimes I-sY\otimes Y)/4$ in the usual Pauli convention, a mixture of product eigenstates of $Y$. The trace distance to this replacement is $\tfrac12\sum_i|h_i|$. A rare final label can retain higher conditional fidelity. For example, recognizing the all-zero displacement word certifies the exact gate $O_0^N$ on an event of mass $(58/128)^N$. For an accepted set of labels of probability $p>0$, its conditional fidelity exceeds $1/2$ by at most $\sum_i|h_i|/(2p)$.

## A growing memory with three terminal messages

A second pair of position words supplies an independent rotation angle. Together the pairs strengthen the necessary number of working states to order $(\log N)^2$ for a positive limiting margin. [Four words and the quantitative lower bound](memory_cost_of_four_position_words.md)

Keep the determinant sign and an estimated body angle on $L$ equally spaced points modulo $\pi$. On each increment add the exact signed angle to the current estimate and round at random to the two adjacent grid points, with probabilities giving the unrounded mean on the lifted line. This wrap-aware rounding has conditional mean error zero and conditional variance at most $\pi^2/(4L^2)$. Since the body coordinate adds increments, successive rounding errors are martingale differences. The cumulative lifted error $e_N$ obeys $\mathbb E|e_N|\le\pi\sqrt N/(2L)$. The encoder uses $2L$ states with displacement inputs. Eight possible preceding sites suffice to convert a stream of absolute positions to displacements.

Use the complete-record three-message rule on this estimated angle. Within the rotation plane choose the better of the identity and quarter-turn recoveries. For the reflection plane send the fixed $Z$ recovery. Each candidate score $\cos^2(\theta-\theta_0)$ is 1-Lipschitz. Choosing the better estimated score costs at most $2|e_N|$ against the choice with the true angle. The expected fidelity loss relative to the prescribed full-record scheme is therefore at most $\pi\sqrt N/L$. With $L=\lceil K\sqrt N\rceil$ and $K>2\pi^2$, the same three messages retain a positive limiting margin. This gives a sufficient memory size. The minimum growth rate between the lower and upper bounds remains open.

These results assume fixed read time and passive classical processing through the interval. Intermediate rail corrections, a quantum memory, transmission of a running transcript, timing a stop from the record, and conditioning on successes give different resources. The calculation predicts ideal frequencies and requires physical tests of the position instrument and the rail recovery.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the proof and finite bounds.
