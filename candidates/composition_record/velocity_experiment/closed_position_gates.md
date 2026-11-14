# A quantum gate detected by the order of two position records

Two position records can land the walker at the same site with the same frequency and leave its rails pointing in different directions. One more walk tick distinguishes them. Longer records can return the walker to its starting site with a rail gate arbitrarily close to any specified real orthogonal gate. This is a prediction for one ideal instrument under ordinary quantum probabilities.

## A 25-tick position test

Start at site 0 in rail R on the sixteen-site ring. Run the twelve-tick block twice, writing the exact site at each block boundary. Preserve coherence between the two rails at every write. On tick 25 apply H, shift once and record the site again. Group the launches by the two **displacements**, reduced modulo 16. The following orders both end at site 8 before the probe and each has probability $377/4096$ per incident launch. [Block specification and alternative instruments](classical_positions_with_a_retained_qubit.md)

| Displacements | Sites after writes 1 and 2 | Rail just before tick 25, up to sign | Conditional probability of site 9 | Joint probability per launch |
|---|---|---|---:|---:|
| 0, 8 | 0, 8 | $(11,16)/\sqrt{377}$ | $729/754$ | $729/8192$ |
| 8, 0 | 8, 8 | $(11,-16)/\sqrt{377}$ | $25/754$ | $25/8192$ |

The block matrices at 0 and 8 are proportional to the reflections $\left(\begin{smallmatrix}7&3\\3&-7\end{smallmatrix}\right)$ and $\left(\begin{smallmatrix}1&5\\5&-1\end{smallmatrix}\right)$. Their two orders give inverse rotations. H followed by the shift sends the sum of the incoming components, divided by $\sqrt2$, to site 9. A device that prepares its rail using only the final site and the common clock must give the same probe distribution in both rows. A device with a classical memory of the order can reproduce this particular comparison. Report both joint frequencies against all launches, including those outside the two rows. [Exact position-probe calculation](check_record_messages.py)

In the four-qubit circuit the three-bit address $y$ counts left shifts modulo eight. A physical read at tick $t$ decodes as $x=t-2y\bmod16$. In chronological order the triples of absolute address codes for the two site-9 joint counts are $(6,0,0)$ and $(2,0,0)$. The corresponding site-7 outcomes are $(6,0,1)$ and $(2,0,1)$. With other or incomplete records keep the incident counts and flag missing reads. If device frequencies of the two prefixes differ, test equality of the two conditional probe rates separately from agreement with the predicted prefix weights.

Generate the circuit in this directory with the following command. The exporter checks every signed output column against the physical shift for all 512 three-write records, including dark records. [Four-qubit exporter and replay](check_scalar_walk.py)

    python -I -B check_scalar_walk.py --order-probe --qasm fresh.qasm

## Returning to the origin with a chosen gate

Write $O_d$ for the normalized rail matrix conditional on displacement $d$. For a chronological word multiply the matrices with the latest on the left. The displacements $(2,8,14,8)$ trace the sites $0,2,10,8,0$ and give

$$
Q=\frac{1}{65}\begin{pmatrix}63&-16\\16&63\end{pmatrix}.
$$

This word has probability $4225/16777216$ for any localized input rail, including one entangled with another system. The coefficients of $(63+16i)^n$ are $(3,1)$ modulo 5 for every $n\ge1$. Indeed $(3+i)^2\equiv3+i\bmod5$. Thus no positive power of $Q$ is $\pm I$. Its rotation angle is an irrational multiple of $\pi$, and its positive powers are dense among planar rotations. Appending the single zero-displacement reflection gives a dense family of closed records in the other component of $O(2)$. Each real matrix acts complex-linearly on the qubit. Arbitrary complex qubit gates would require additional operations. The construction tracks actual time-ordered measurement outcomes. Even a zero-displacement outcome can change the rail, so a spacetime connection does not follow from the site labels. [Lean proof from signed paths](../../../Director_G/lean/ClosedPositionTransport.lean)

A controller can simply stop at the first recorded return to the origin whose accumulated matrix is within $\epsilon>0$ of a predeclared target, up to global sign in operator norm. It neither resets the rail nor chooses future displacements. To prove termination, from any observed site designate the next increment returning to 0. From there, a finite net of closed words suffices to approximate any residual target by compactness and the density above. With the return included, let $L$ be the longest of these designated continuations. Every needed increment has conditional probability at least $1/64$. Conditional on any live history there is at least $64^{-L}$ probability of stopping within the next $L$ blocks, even if a different acceptable word appears first. Consequently $\Pr(T>kL)\le(1-64^{-L})^k$. The stopping time depends only on the position history and has the same law for every input qubit. A missing record makes the gate uncertain. The proof assumes reliable writes, uninterrupted rail coherence, and control over when the next block starts.

For target H at tolerance $1/32$, no word succeeds within four blocks. The word $(4,8,0,12,8)$ succeeds at five, with reflection first column $(71,69)/\sqrt{9802}$ up to sign. Counting every successful word, the probability of having stopped by five blocks is $14703/268435456$ and by twelve it is $1039325527453239/2305843009213693952$ (about $0.0451\%$). The finite yield matters if rail coherence has a lifetime. A controller at a fixed twelve-block deadline must also report the timeouts. A Hadamard already occurs within the elementary walk. Here the gate is obtained on an unknown input at its starting site while the same block runs at every write. [Integer first-hit calculation and short-word enumeration](check_stopped_gate.py)

To read that five-block gate, prepare $(R+L)/\sqrt2$ or $(R-L)/\sqrt2$ with a fair hidden source label. An I tick followed by the site read resolves the outgoing rails. At the origin, the specified word then gives clockwise probability $4900/4901$ on the plus preparation and $1/4901$ on the minus preparation. It is equally likely to occur on either input. A device that erases all information about the input and has no other access to the hidden source label can guess it only half the time. This is a prospective test of two preparations. General qubit recovery can be tested on a pair. [Recovery with a finite message](recovering_a_qubit_from_position_messages.md)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the calculations and verification. No device outcomes were used.
