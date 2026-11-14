# Two calibrated preparations for a three-step walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development, challenge and computational verification with OpenAI Codex.

A three-step walker starting on the right rail puts squared norm $5/8$ in well $+1$. Its own preparations give two controls where every well is within the previously calibrated range through $1/2$. A device that reads one fixed quantum measurement effect must assign $5/8$ to the original well if it agrees on these controls. A freshly fluctuating terminal sampler can pass all three population tests while assigning $2/3$ or $7/12$ on individual launches. The difference matters when using a reversible detector to investigate the sampler. All rates here are predictions. [Half-mass calibration and fluctuating sampler](spectator_refinements.md) · [Operational quantum detector tomography, Lundeen et al.](https://www.nature.com/articles/nphys1133)

## Build the controls in the same walk

Start at the origin on a line. Each tick applies the real Hadamard coin $(R,L)\mapsto (R+L,R-L)/\sqrt2$ and shifts right and left rails one site in their respective directions. For a rail density matrix of trace one write $z=\rho_{RR}-\rho_{LL}$ and $x=2\operatorname{Re}\rho_{RL}$. Three ticks give the following four squared norms, in well order $-3,-1,+1,+3$:

$$\frac18(1-x,\ 3-2z-x,\ 3+2z+x,\ 1+x).$$

The middle two sum to $3/4$. The exterior wells are always at most $1/4$. Thus all four wells are within the half-mass calibration exactly when $|2z+x|\le1$. The [integer replay](check_light_probes.rs) evolves the rails and sums their squares at the wells. The underlying Hadamard walk has a standard signed-amplitude realization. [Ambainis et al., One-Dimensional Quantum Walks](https://cs.uwaterloo.ca/~watrous/Papers/OneDimensionalQuantumWalks.pdf)

Use two balanced label bits, initially coherent, giving four orthogonal labels of equal squared norm. At the origin route the labels to rails according to the table, keep them, and apply the same three ticks. Read position, pooling both rails and all labels **before** the terminal score. No well selection or discarded launch is needed.

| Source | Rails of labels 0 through 3 | Four well masses | Hit at $+1$ under the calibrated linear rule |
|---|---|---|---|
| Plus | R, R, R, L | $(1,2,4,1)/8$ | $1/2$ |
| Minus | R, L, L, L | $(1,4,2,1)/8$ | $1/4$ |
| Target | R, R, R, R | $(1,1,5,1)/8$ | $5/8$ (extrapolated) |

One can remove even the assumption that a proposed fixed effect ignores the retained labels. For each source independently choose uniformly two two-bit masks $s,t$. On label $j$, apply the sign $(-1)^{t\cdot j}$ and the permutation $j\mapsto j\mathbin{\mathrm{xor}}s$. Each of the 16 controls preserves all four well masses on that individual preparation. In the ensemble, averaging over signs kills the off-diagonal label blocks. Averaging over permutations puts the sum of the diagonal blocks, divided by four, at every label. The detector-accessible input is then $(I_4/4)\otimes\rho$ for each family, with $\rho$ respectively $\operatorname{diag}(3/4,1/4)$, $\operatorname{diag}(1/4,3/4)$ and $\operatorname{diag}(1,0)$. Applying a common walk or fixed linear premeasurement preserves the following matrix identity:

$$2\bar\rho_R=3\bar\rho_+-\bar\rho_-.$$

Here the bars include the labels. The random keys must be independent of the responding mode and inaccessible to the reader. Discarded preparation hardware carrying the setting would reopen the same loophole if it could affect the read. Sampling a classical R or L first would present a heavy well on each trial and invalidate the half-mass control.

## What follows from a common detector effect

For each apparatus mode $F$ suppose one fixed effect $0\le E_F\le I$ gives its actual hit probability as $\operatorname{tr}(E_F\rho)$ on these preparations, inclusive of the common walk and any retained labels. Apply it to the identity. Writing $h$ for the mode's hit probability averaged over the independent keys gives $h_R=(3h_+-h_-)/2$. The two control laws then give $h_R=5/8$ in that mode. This uses only affinity on one three-point comparison. An affine pointer tested on different complete inputs or a different destructive detector requires an additional transfer assumption.

Both the conditioning and the numerical stability are sharp within this comparison. Errors at most $\epsilon$ on each control imply at most $2\epsilon$ error on the extrapolation. Any signed representation of the target by preparations with all four cells in range must spend total absolute coefficient weight at least two: apply the affine functional $2z+x$, whose absolute value is at most one on those preparations and equals two on the target. The two controls attain that minimum. This also covers complex rail preparations, since imaginary coherence drops out of the witness. For a single hypothesized mode whose observed or stipulated three rates miss the identity by $\delta=|h_R-(3h_+-h_-)/2|$, the smallest uniform error of an unrestricted affine fit on these three points is $\delta/3$. The triangle inequality gives the lower bound. Moving the target toward the interpolant by $\delta/3$ and the two fit values in opposite directions by $\delta/3$ attains it. At the fair rival's two target rates the gap is $1/24$ for both modes, so either requires a fit error of at least $1/72$. Their pooled rates give a gap of zero.

There is also a pure-state construction where label controls are unavailable. The three real spinors proportional to $(3,-1),(1,1),(1,3)$ give $(z,x)=(4/5,-3/5),(0,1),(-4/5,3/5)$. Every well is in range, and the signed weights $3/4,3/4,-1/2$ reproduce the sharp-right input density matrix. Eight free ticks from sharp R yield $(3,-1)/16$ at well $-4$. The reflected sharp L launch yields $(1,3)/16$ at $+4$. Heralding the named well while preserving its rails supplies either direction at kinematic mass $5/128$. The middle probe needs a balanced pair on the same site. The two-label-bit construction avoids these heralds and their possible selection of apparatus modes. [Lean certificate for the coefficient identities and sharp bounds on rational grids](LightProbeExtrapolation.lean)

## What a reversible comparison can measure

Consider a balanced path control that operates the direct and split read mechanisms coherently on the same prepared launch. Compare their outgoing unit vectors $u_F,v_F$ in one physical output space, after aligning any known routing. Use a common initial purification and include all output modes and environmental records that could distinguish the arms, including those disturbed by the read. An incoherent classical mixture can be included in $F$ if that same refinement applies to both arms. Supply a fresh balanced label or compatible spare walk modes so the terminal read can split each scored port into half-sized leaves. It must resolve these leaves before pooling and retain the incident-trial denominator. With this calibration and the balanced recombiner, the measured minus-port rate is $D=\mathbb E d_F$, where $d_F=\|u_F-v_F\|^2/4$. [Guarded terminal read](guarded_position_reads.md) · [Interference of quantum channels, Oi](https://arxiv.org/abs/quant-ph/0303178)

The comparison bears on an original sampler only if the split and direct outputs actually encode its hit probabilities $q_F,p_F$ in a common pointer event. With an orthogonal hit projector, splitting each vector into hit and miss sectors gives

$$
1-2d_F=\operatorname{Re}\langle u_F,v_F\rangle
\ \le\ \sqrt{p_Fq_F}+\sqrt{(1-p_F)(1-q_F)} .
$$

Nonnegative real amplitudes in a two-dimensional pointer attain equality. More generally, the difference of the pure-state projectors has nonzero eigenvalues $\pm\sqrt{1-|\langle u_F,v_F\rangle|^2}$ when the states differ as rays. Its expectation in any common effect bounds $|p_F-q_F|$ by the positive eigenvalue. Thus $\mathbb E(p_F-q_F)^2\le4D(1-D)$ by concavity. If the actual direct and split rates have independently bounded RMS errors $e_U,e_S$ relative to their encoded probabilities, the RMS error between actual rates is at most $2\sqrt{D(1-D)}+e_U+e_S$. Uncontrolled phases and records can create dark counts even at equal hit probabilities. Equal branch channels measured separately can have different interference through different physical implementations. [Abbott et al., coherent control of quantum channels](https://quantum-journal.org/papers/q-2020-09-24-333/)

Against a split reference of $5/8$, the minimum mean dark rate for the named fair $2/3,7/12$ rival is $0.0004643282733$. This is the average of the two bounds $(1-\sqrt{pq}-\sqrt{(1-p)(1-q)})/2$. In an ideal independent-trial test, zero dark counts in 6,451 incident launches give probability below 0.05 throughout this linked rival family. At 6,450 an attaining implementation still exceeds 0.05. The test would need to count missed trials and bound detection losses before using that figure.

The terminal-only rival gives the decisive control. Let both modes implement identical reversible circuitry and assign their differing scores only at the terminal sampling step. Undo the routed paths before sampling. The two outgoing vectors can coincide exactly and the echo stays dark. On a separate direct heavy-cell read the two modes can still assign $2/3$ and $7/12$ and average to $5/8$. The coherent interface connecting the physical sampler to the pointer is therefore an experimental obligation. A common affine effect reproducing each mode's controls and target would itself settle this particular site before the echo. Recovering the complete probability rule, or transferring it to successive records of a classical trajectory, remains open.
