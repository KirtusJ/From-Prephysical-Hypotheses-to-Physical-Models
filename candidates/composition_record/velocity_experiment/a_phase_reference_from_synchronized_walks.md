# How closely can a synchronized walk set a gate’s relative sign?

An addressed walk applies a Hadamard to one arm while the other arm idles. Reversing the Hadamard’s sign changes observed position probabilities, even though the sign of a Hadamard applied everywhere cannot be read. Can a synchronized circuit supply its own phase comparison? In ordinary quantum mechanics it can approximate the required controlled gate to arbitrarily high accuracy on a heralded output. No successful protocol that actually stops after finitely many synchronized operations can implement it exactly, even when it has no deadline.

Here the larger circuit menu includes sharp auxiliary bits, signed permutations, uniform single-qubit Hadamards and coordinate reads. These are resources of the proposed digital apparatus. The elementary two-rail shift alone does not supply arbitrary auxiliary registers or coherent routing. The earlier rational comparison approximates H by a rational orthogonal reflection. The construction below uses two filters with complementary errors. Their combined success probability is independent of the input, and their conditional error has the best possible exponential dependence on the number of Hadamards in this menu. [Earlier rational comparison](../../../Director_G/Rational_references_and_optical_bypass.md) · [Why the addressed gate sign matters](addressed_embedding.md)

## An obstruction that persists under heralding

Use control and rail as four input coordinates. The target $U=I\oplus H$ has two nonzero idle entries equal to one and four nonzero acted entries equal to $\pm1/\sqrt2$. A rational signed permutation on the even arm converts idle $I$ to the exchange $X$ used in the walk. Count one use of a single-qubit uniform H, tensored with identity on the other wires, as one Hadamard. A tensor product on several distinct qubits counts once per qubit. Signed permutations include reversible classical logic with signs. Coherently skipping a single H on one arm would already add the sought capability. [Amy, Glaudell, Li and Ross on scaled dyadic matrices for Toffoli–Hadamard circuits](https://arxiv.org/abs/2305.11305)

Refine every stopped successful history by the coordinates of any discarded quantum registers. Conditional on any independent classical random seed, each fine Kraus operator is $D/2^{j/2}$ for a real integer matrix $D$, where $j$ is the number of Hadamards on that history. A signed step permutes or negates coefficients, a masked read takes a submatrix, and an H adds and subtracts two rows with a common scalar. This induction uses unnormalized branches, including failed earlier attempts in a retry history. If the success channel were a positive multiple of the target unitary channel, its Choi matrix would have rank one. A sum of positive rank-one matrices with that range requires every nonzero contributing Kraus operator to be proportional to $U$. The ratio between an acted and idle entry rules this out. This also covers any countable family of finite successful histories and integrals over independent classical randomness. A protocol may have a positive chance of never halting. Only outputs delivered at a finite time have been analyzed.

**Finite error floor.** Let $F_D$ be the overlap of the normalized fine-branch Choi state with the target Choi state, obtained by feeding half a maximally entangled four-dimensional pair. With the Frobenius inner product,

$$
1-F_D=\frac{\lVert D-\operatorname{proj}_{U}D\rVert_F^2}{\lVert D\rVert_F^2}
       \ \ge\ \frac{1}{16\,4^j}.
$$

To see this, put $S=Z+X=\sqrt2 H$ and let $W$ be the real span of the two matrices supported respectively on the $I$ and $S$ blocks. If $D$ lies outside $W$, either an off-pattern integer is nonzero or two sign-adjusted entries in one block differ by at least one. Their sum of squared deviations from any common value is at least $1/2$. Also $\lVert D\rVert_F^2\le4\,2^j$ because each Kraus operator is a contraction. The claimed bound follows. If $D=aI\oplus bS$, put $E=a^2+2b^2$. Direct projection gives $(a-\sqrt2 b)^2/(2E)$. The nonzero integer $|a^2-2b^2|$ is at least one and $(|a|+\sqrt2|b|)^2\le2E$. Contractivity bounds $E\le2\cdot2^j$. Combining gives the same floor. The [Lean 4.19 certificate](../../../Director_G/lean/RationalControlledHadamard.lean) proves the integer separation by descent, including signed and zero entries. The Choi and channel arguments here are analytic.

For a pooled success the process infidelity is the average of these infidelities weighted by successful probability on that entangled input. If $j\le h$ on successful histories, the floor is $1/(16\,4^h)$. With only a finite mean count $\bar h$ under those same success weights, Jensen’s inequality gives $1/(16\,4^{\bar h})$. Neither inequality requires a lower bound on yield. A herald whose success depends on the input is characterized here by its normalized Choi state. For an input-independent herald the conditional map is a channel, and half its diamond distance from the target is at least the process infidelity by testing the ideal Choi projector. A supplied arbitrary rational rotation with uncharged denominator would invalidate the Hadamard-count bound.

## Two integer filters give a uniform herald

Write $a_n+b_n\sqrt2=(1+\sqrt2)^n$ for $n\ge0$. Choose the adjacent pairs $(a,b)$ and $(c,d)$ with indices $n,n-1$, $n\ge1$. Let $K$ be the smallest power of two at least $\max(a,2b,c,2d)$. Use one fair selector to choose a pair, keep it private, and disregard that label on success. For the selected pair $(a,b)$ the accepted matrix is

$$
L_1=(aI\oplus bS)/K .
$$

Prepare $K$ equal path amplitudes with a Walsh transform. In the idle sector preserve the first $a$ paths. In the acted sector use $Z$ on the first $b$ paths and $X$ on the next $b$. Flag the remaining paths in each sector, undo the Walsh transform and accept only the joint zero path and clear flag. The signed operations act before recombination. The second pair gives $L_2=(cI\oplus dS)/K$ by the same program. All paths experience the same Hadamards. This is a linear combination of signed permutations implemented by heralding. [Childs and Wiebe](https://arxiv.org/abs/1202.5822)

Set $P=a^2+c^2=2(b^2+d^2)$ and $C=ab+cd$. The identity for $P$ follows by adding the opposite Pell norms. The determinant of the two adjacent integer vectors has magnitude one, hence $P^2-2C^2=2$. On every input, including one entangled with another system, success has probability

$$
s=P/(2K^2)=(b^2+d^2)/K^2>1/16 .
$$

Here $K<4b$ since $a\le2b$. The uniform probability holds after pooling the two selectors. Revealing or conditioning on their separate successes changes the instrument.

On success both diagonal control blocks transform exactly as under $U$. The off-diagonal blocks acquire, relative to $U$, a scalar $\lambda=\sqrt2 C/P$. Thus the output is the ideal $U$ followed by an independent sign flip $Z_{\rm control}$ with probability

$$
\delta=\frac{1-\lambda}{2}
       =\frac{1}{P^2(1+\sqrt{1-2/P^2})}.
$$

Both the conditional Choi infidelity and half the diamond distance equal $\delta$. For the latter, the difference of the two unitary channels has diamond norm two because their outputs are orthogonal on a balanced superposition of control arms after undoing $U$. This calculation applies to unknown inputs and arbitrary spectators. The single filters have a small difference in success between arms. Mixing cancels this difference exactly while reducing the residual error to a dephasing probability. [Campbell on gate errors under randomization](https://arxiv.org/abs/1612.02689)

There are $h_0=2\log_2 K$ Walsh Hadamards and one additional H if the circuit generates its own fair selector. Since $P>K^2/8$, the conditional error is below $64/K^4=64\,4^{-h_0}$. Successive eligible $K$ values have a bounded ratio since $b_{n+1}=a_n+b_n\le3b_n$. The finite lower bound and this upper construction therefore match in exponential order as the budget increases. The complexity statement counts individual Hadamards. Reversible routing, available memory, site-clock timing and gate errors carry separate costs. A failed attempt can disturb the input.

| Adjacent pairs | Paths $K$ | Uniform success | Conditional half diamond distance |
|---|---:|---:|---:|
| $(3,2),(1,1)$ | 4 | $5/16$ | 0.00502525 |
| $(7,5),(3,2)$ | 16 | $29/256$ | 0.00014865 approximately |

## A position read of the relative sign

The four-path version can serve as a second addressed operation on the original modulo-four address (physical eight-site ring). At tick 1 apply uniform H and shift. At tick 2 apply the unknown addressed operation $X\oplus\epsilon H$, shift, and coast for ticks 3–5. Four shifts on a fixed rail restore its address. At tick 6 insert the synthetic $X\oplus H$ reference on the same parity and shift. Coast on ticks 7–8. The resulting three shifts undo the first-tick separation after the two addressed coins cancel on each rail. Apply a final H, shift and read at tick 9. The gate program takes auxiliary operations between the declared walk shifts.

In the ideal reference, the two addressed calls compose to $I\oplus\epsilon I$, so the final address is 0 with certainty for the matched sign and 1 for the reversed sign. With the four-path reference, conditional on success the wrong port has probability $\delta$ for either held sign. The complementary herald rate is $11/16$ and counts against incident launches. The comparison presumes the unverified gate acts as one of the two stated lifts and that no other which-path record survives. Swapping the generator and its hardware sign simultaneously still leaves the unknown device’s matrices identical. This experiment fixes its orientation **relative to the built reference**. The reference’s own coordinate channels are rational and the synchronized program has the same predictions in both algebraic descriptions. An absolute embedding has not been observed. [Earlier relative-phase echo](two_address_echoes.md) · [Nine-tick records with the reference in every flight](records_with_a_heralded_reference.md)

The exact [filter and circuit checker](check_heralded_gate_reference.py) reconstructs the accepted and failed maps from individual paths. Its optional Qiskit check reads the exported six-qubit circuit. The four-path sharp-rail control-X probability is $17/20$ on success. All numerical results above are circuit predictions.

    python -I -B check_heralded_gate_reference.py
    python -I -B check_heralded_gate_reference.py --qiskit

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the construction, bounds and checks.
