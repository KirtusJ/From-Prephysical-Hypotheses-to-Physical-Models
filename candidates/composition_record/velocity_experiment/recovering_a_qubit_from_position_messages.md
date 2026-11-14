# How much of a position record recovers a Bell pair?

In the sixteen-site walk, a receiver who gets only the final position loses all rail–reference entanglement by the seventh position write. A sender who saw the whole path can instead send one of **three classical labels**, enough to recover a Bell fidelity above $0.64$ at write 32. At that same write a binary label gives fidelity below $0.564$, even when the receiver also knows the final position and can choose any local recovery channel. These are exact-model bounds for a fixed read time and a score over **all** incident launches.

## What each party has

Prepare the rail at site 0 maximally entangled with an untouched qubit in $|\Phi\rangle=(|RR\rangle+|LL\rangle)/\sqrt2$. At each twelve-tick block boundary perform the ideal site write, preserving the two local rails. The eight allowed displacements $d$ have state-independent weights $w_d=(58,10,2,10,26,10,2,10)$ in even-site order, divided by 128. Given $d$, the rail undergoes the known real orthogonal matrix $O_d$. The sender observes the position word and computes a single terminal label. The receiver gets the final site, the label, and the rail, then applies a trace-preserving quantum operation to the rail. Score the overlap of the resulting pair with the initial Bell state, averaged over all launches. The receiver has no access to the reference or other path information. The time and the initial entangled state are fixed before the launch. A complete word allows exact conditional unitary recovery. [Walk and position instrument](classical_positions_with_a_retained_qubit.md) · [Gregoratti and Werner on environment-assisted correction](https://arxiv.org/abs/quant-ph/0209025)

## Erasing the path after writing it

For $J_m(s)$ use the joint, subnormalized density matrix of the final pair and site $s$ after $m$ writes. Start with $J_0(0)=|\Phi\rangle\langle\Phi|$, zero elsewhere. With $K_d=\sqrt{w_d/128}\,O_d$ the exact recurrence is

$$
J_{m+1}(s)=\sum_d (K_d\otimes I)J_m(s-d)(K_d^\dagger\otimes I).
$$

Each positive-probability site defines a normalized trace-preserving channel on the arbitrary input rail because its probability is input-independent. Its Choi state is $J_m(s)/\operatorname{tr}J_m(s)$. It breaks entanglement with every reference exactly when this state is separable. For a two-qubit Choi state this is equivalent to a positive partial transpose. The same test applies to the pooled state $\sum_s J_m(s)$. [Horodecki, Shor and Ruskai on entanglement-breaking channels](https://arxiv.org/abs/quant-ph/0302031) · [Horodecki, Horodecki and Horodecki on two-qubit separability](https://arxiv.org/abs/quant-ph/9605038)

| Completed writes | Pooled channel breaks entanglement | Final sites where the conditioned channel still transmits entanglement |
|---:|---|---|
| 1, 2 | No | All eight even sites |
| 3 | No | 0, 2, 6, 8, 10, 14 |
| 4 | No | 0, 8 |
| 5 | Yes | 0, 8 |
| 6 | Yes | 0 |
| 7 and later | Yes | None |

The [integer checker](check_position_memory.py) tests principal minors of each partial transpose and separately tracks the two determinant sectors of the rail matrices. Both calculations give the table. Once all eight states are separable, the recurrence preserves separability at every later write by positive sums of local operations. For the pooled channel the same closure applies from write five. Erasing the records here means losing access to actual writes. Omitting the physical writes allows paths to interfere again and changes the channel.

## The optimum for a fixed alphabet

Describe a planar orthogonal matrix by the angle $\theta$ of its first column and its determinant sign. An overall minus sign has no effect on its channel, so the angle is taken modulo $\pi$. At long times, conditional on **each** final site, both signs become equally likely and the angle becomes uniform on that circle in the sense of weak convergence. The distribution at any finite time is discrete.

To see the convergence, group steps in fours. The words $(0,0,0,0)$ and $(2,8,14,8)$ each return to the origin with positive probability. Their matrices are $I$ and a rotation through $\alpha$, with $\alpha/\pi$ irrational. For any angular harmonic $e^{2in\theta}$ with $n\ne0$, these words leave the site and orientation fixed and multiply the harmonic by 1 and $e^{2in\alpha}$, respectively. Take out the same positive mass $b$ of each word. Their combined operator has norm $2b|\cos(n\alpha)|<2b$. Every remaining left multiplication is an isometry on the space of site, orientation and harmonic coefficients (include both $n$ and $-n$ for reflections). Thus the four-step average strictly contracts each such fixed harmonic. At frequency zero the finite walk on the half-address $s/2\bmod8$ and the determinant sign also mixes. Each finite-group character has scalar mean of modulus less than one unless it is trivial. Indeed displacements 0 and 2 are reflections, so equality of their character values forces the spatial character to be trivial. Displacement 4 is a rotation, then forcing the sign character to be trivial too. Trigonometric approximation gives weak convergence against continuous scores. This argument also gives $J_m(s)\to I_4/32$ at all eight sites. [Irrational closed rotation and its Lean certificate](closed_position_gates.md)

Write $v(0)=0$ and, for $k\ge1$, define

$$
v(k)=\frac12+\frac{k}{2\pi}\sin\!\left(\frac{\pi}{k}\right).
$$

For $t\ge1$ possible terminal labels the optimal limiting fidelity is

$$
F_t=\frac{v(\lfloor t/2\rfloor)+v(\lceil t/2\rceil)}{2}.
$$

For one, two, three and four labels the values are $1/4$, $1/2$, $1/2+1/(2\pi)$ and $1/2+1/\pi$. Three is the smallest alphabet giving a positive **limiting margin** over the separable Bell fidelity bound $1/2$ under this scoring rule.

To derive the formula, the Bell states $(O\otimes I)|\Phi\rangle$ for rotations lie on the unit circle in the real plane spanned by the normalized vectorizations of $I$ and the quarter-turn $J$. Reflections give the orthogonal plane spanned by $Z=\operatorname{diag}(1,-1)$ and the rail swap $X$. For any allowed receiver channel $\mathcal R$, the Bell score on a branch state $\rho$ is $\operatorname{tr}(E\rho)$, where $E=(\mathcal R^\dagger\otimes I)(|\Phi\rangle\langle\Phi|)$ is positive of trace one. Trace one follows from trace preservation and the maximally mixed marginal of $\Phi$. For given recovery choices the sender transmits the label with largest branch score. Independent shared randomness cannot improve the optimum.

For an upper bound relax each $E$ to any density matrix. Dropping the off-diagonal blocks between the two planes and taking real parts preserves every branch score and leaves a positive matrix. This reduced matrix is a mixture of real rank-one projectors, each supported in one plane. The mean maximum over labels is convex separately in each effect. Replacing each effect by a pure component maximizing that objective therefore suffices. Conversely every such real line is the normalized vectorization of an orthogonal matrix, so its score is attainable by the inverse unitary as the decoder.

Place $k$ recovery lines in one plane. Two adjacent lines enclosing a gap $\Delta$ split that gap at its midpoint. Integrating their nearest-line score $\cos^2\theta$ over all gaps on a circle of circumference $\pi$ gives $1/2+\sum_i\sin\Delta_i/(2\pi)$. Equal gaps maximize this expression by concavity of sine on $[0,\pi]$. Successive gains in $v(k)$ decrease because $k\sin(\pi/k)$ is concave for $k\ge1$ and $v(1)-v(0)=1/2\ge v(2)-v(1)=1/\pi$. Balancing the number of lines between the two equally populated planes proves the formula. It covers decoders that change with the time horizon. For fixed $t$ the tuples of effects at the eight sites form a compact set. The maximum-score function is uniformly Lipschitz in those effects, so a finite net transfers weak convergence to convergence of the optimized score.

## A finite comparison

A concrete three-label encoder chooses the nearer of $I,J$ for rotations and always chooses $Z$ for reflections. The receiver applies the inverse indicated by the label. The labels arise from the observed word. The calculation assumes enough working memory to track that word or its gate accurately. It bounds communication to the receiver, with no limit here on encoder memory. Intermediate corrections, a variable stopping time communicated to the receiver, access to ancillary path records, or discarding unsuccessful trials change the experiment.

For the binary upper bound, let $J_{s,\ell}$ be the subnormalized positive Choi state assigned label $\ell$ at $s$. Since $0\le J_{s,\ell}\le J_m(s)$ and each decoder effect has trace one, the total binary score is at most $2\sum_s\lambda_{\max}(J_m(s))$. For either sign sector of mass $p$, its two eigenvalues are $(p\pm|h_2|)/2$, where $h_n$ sums $e^{in\theta}$ weighted by incident probability within that site and sector. The three-label score is $1/2+(\mathbb E[\mathbf1_+|\cos2\theta|]+\mathbb E[\mathbf1_-\cos2\theta])/2$. Bounding the absolute cosine below by its square needs just harmonics 0, 2 and 4. These propagate along the eight-site ring by integer arithmetic after a common denominator is cleared. At write 32 the resulting bounds are strictly below $0.564$ for every binary encoder and strictly above $0.640$ for the specified ternary encoder. All thresholds use the incident denominator and the same final-site access. [Exact finite bounds and direct short-word check](check_record_messages.py)

Bell preparation, controlled recovery and joint Bell readout would require physical validation in addition to recording positions. The record-order position probe offers a shorter test using the walk's own controls. Neither a classical stochastic position chain nor this conditional quantum channel supplies a derivation of ordinary quantum probabilities. [Native position probe](closed_position_gates.md)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the analysis, independent calculation paths and source checks. The predictions have not been tested on this device.
