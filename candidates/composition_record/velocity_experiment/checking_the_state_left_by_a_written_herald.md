# Checking the state left by a written herald

The four-path walk gate reports a binary label and returns a quantum state. Measuring only the label misses a reader that makes an extra copy of the logical control. That copy leaves both label frequencies unchanged, while halving each of the two Bell-return probabilities below. One entangled preparation and two choices made **after the science label is written** can verify the entire effective measurement on the gate’s four-dimensional input space. The claim assumes a common completely positive quantum instrument, a protected external reference, and trusted tests of its output. [Walk gate and signed routing](a_phase_reference_from_synchronized_walks.md) · [Three references for testing the probability rule on a specified read](reading_a_herald_with_three_references.md)

## One preparation, two questions

Let $V$ denote the six-wire gate with its four work wires initialized to zero, viewed as an isometry from the logical control and rail. Write $\Pi_G$ for the good sector, $\Pi_B=I-\Pi_G$, and $s_G=5/16$, $s_B=11/16$. The original calculation gives $V^\dagger\Pi_z V=s_z I_4$. In particular $K_z=\Pi_z V/\sqrt{s_z}$ is an isometry for either label. The target instrument on the logical input is $\mathcal L_z(\rho)=s_z K_z\rho K_z^\dagger$.

Prepare two Bell pairs between the two logical wires and two outside reference wires, using balanced Hadamards and controlled bit flips. With $d=4$, this gives $|\Phi\rangle=d^{-1/2}\sum_i |i\rangle|i\rangle$. The preparation after the gate is $|\Psi\rangle=(V\otimes I)|\Phi\rangle$. Apply the **actual** binary writer to the gate wires and save its reported label $z$. It must have no access to the two reference wires. Then use an independent fair bit to choose one terminal test.

* **Sector.** Check the physical good projector $\Pi_G$ with a fresh pointer, and compare the result with the saved $z$. Record both agreements and mismatches.
* **Return.** Apply the inverse of the original six-wire unitary, undo both Bell preparations, and test all eight wires for zero. This is a test of $|\Psi\rangle\langle\Psi|$.

The ideal figures below are per attempted launch assigned to the indicated test. For the balanced random choice, multiply the joint columns by $1/2$ to get their overall incidence.

| Saved label | Label probability | Joint label and sector mismatch | Joint label and successful Bell return |
|---|---:|---:|---:|
| Good | $5/16$ | 0 | $25/256$ |
| Bad | $11/16$ | 0 | $121/256$ |

These tests concern the output **after** the genuine label exists. The ordinary total Bell return after this write is $73/128$. The [earlier unwritten-herald audit](how_a_hidden_herald_changes_the_return.md) instead aims for unit return before any genuine write. The analyzer must retain the label, late choice, outcome, and incident denominator, including unreadable attempts.

## What equality certifies

Assume the gate and actual writer together implement a fixed instrument $\mathcal I_z$ from the four logical input dimensions to the six quantum output wires and a classical label. Each branch is completely positive and their sum preserves trace. A launch-independent distribution over such instruments is covered through its average. Stable preparation and a late choice independent of the output let both tests refer to the same states. Their frequency interpretation uses an ordinary calibrated quantum read. Hypotheses about alternative terminal scoring require a separate check of that read.

Let $p_z$ be the label frequency, $\alpha_z$ the conditional probability of a sector mismatch and $\beta_z$ that of a Bell return. The normalized conditional state $\sigma_z=(\mathcal I_z\otimes I)(|\Phi\rangle\langle\Phi|)/p_z$ is the branch’s normalized Choi state when $p_z>0$. Write $|\phi_z\rangle=(K_z\otimes I)|\Phi\rangle$. The vectors $|\phi_G\rangle$ and $|\phi_B\rangle$ have orthogonal sector support, and their squared coefficients in $|\Psi\rangle$ are $s_G$ and $s_B$.

If $\alpha_z=0$, the state is supported on its named sector. Thus $\beta_z=s_z\langle\phi_z|\sigma_z|\phi_z\rangle\le s_z$. Equality forces $\sigma_z=|\phi_z\rangle\langle\phi_z|$. The label frequencies supply the scale $p_z=s_z$. The two branch Choi matrices now determine $\mathcal I_z=\mathcal L_z$ on every operator on this input space, including off-diagonal and complex operators. Hence the instrument also agrees on arbitrary spectator-entangled science states supported there. A rank-one branch gives only scalar multiples of the same isometry in any Kraus decomposition. A retained environment may encode the authentic label. Given that label its state contains no additional information about the logical input for a dilation of this fixed map with a fresh environment. [Choi’s completely positive map characterization](https://doi.org/10.1016/0024-3795(75)90075-0) · [Process–state correspondence](https://www.sciencedirect.com/science/article/abs/pii/S0003491603002707)

## Bounds from imperfect records

The following bound allows incorrect-sector amplitudes to interfere coherently. Define $F_z=\langle\phi_z|\sigma_z|\phi_z\rangle$. With $s=s_z$, the triangle inequality applied to $\sigma_z^{1/2}|\Psi\rangle$ gives

$$
\sqrt{\beta_z}\le \sqrt{sF_z}+\sqrt{(1-s)\alpha_z},
\qquad
F_z\ge f_z=\frac{[\sqrt{\beta_z}-\sqrt{(1-s)\alpha_z}]_+^2}{s}.
$$

The bound is sharp at all feasible conditional rates. To see physical attainability take $g=\phi_z$ and $b=\phi_{\bar z}$. Composing either branch isometry with a traceless logical Pauli gives states $g',b'$ orthogonal to $g,b$ respectively. If $\beta_z>(1-s)\alpha_z$, put $v=\sqrt{f_z}g+\sqrt{\alpha_z}b$ and use $|v\rangle\langle v|+(1-\alpha_z-f_z)|g'\rangle\langle g'|$. Feasibility gives $f_z\le1-\alpha_z$. Otherwise use a mixture of $g',b,b'$ with weights $1-\alpha_z,\beta_z/(1-s),\alpha_z-\beta_z/(1-s)$. In each case the reference marginal is $I/d$ because the branch maps are isometries into orthogonal sectors. Weighting these states by any normalized label probabilities therefore defines a legitimate instrument. These examples establish sharpness of the conditional fidelity bound.

For the channels carrying the classical label along, a conservative bound on worst-case distinguishability is

$$
\frac12\|\mathcal I-\mathcal L\|_\diamond
\le \min\left\{1,\frac d2\sum_z
\sqrt{(p_z+s_z)^2-4p_zs_z f_z}\right\},\qquad d=4 .
$$

Each square root bounds the trace norm of the difference of the weighted Choi states. Purify the first state to have overlap $\sqrt{F_z}$ with a purification of the pure target, take the trace norm in their two-dimensional span and then trace out the purifying register. The classical label makes the two trace norms additive. The factor $d$ transfers the normalized Choi bound to any input: a purified logical input is obtained from $|\Phi\rangle$ by an operator on its reference with norm at most $\sqrt d$. If $p_z=0$ in the population, its summand is $s_z$, independent of the undefined conditional rates. In finite data, bound the joint label, mismatch and return probabilities with simultaneous coverage and maximize the displayed bound over the compatible populations. Zero observed mismatches alone cannot establish a perfect sector test.

## Three ways to reproduce fewer observations

1. **Keep the label and copy the logical control.** In the original circuit the logical control bit is preserved by $V$ and by the sector checks. Copy it to an inaccessible blank bit. Every logical basis input still passes its own basis-state version of the inverse check at the ideal rate. For the Bell input the two control values now contribute incoherently, each with half the ideal amplitude. Both joint Bell returns fall to $s_z^2/2$ while all sector tests pass.
2. **Leave out the sector test.** Draw $z$ in the right proportions. With probabilities $s_z,1-s_z$, send through the unprojected code isometry $V$ or $VZ$, where $Z$ acts on one logical bit. The two Bell states are orthogonal because $Z$ has trace zero. This instrument gives every ideal label and Bell-return rate in the table. Its conditional sector mismatch is $1-s_z$.
3. **Change the hidden label bias between launches.** A mode can draw good with its own input-independent probability and apply $K_z$ on that label. The scalings $1/2$ and $25/146$ with weights $55/128$ and $73/128$ have the correct mean $5/16$. The resulting averaged instrument equals the target on all logical inputs, so every post-write test passes. This comparison allows arbitrary quantum instruments and does not supply a finite native synthesis of the two normalized isometries as deterministic gates. The data certify the effective instrument. Its internal sampling order and mode-specific biases remain unidentified. Likewise a separate global phase on each reported branch cancels in its map. Coherently erasing the label in a future experiment would require additional phase information. An initial correlation between the instrument environment and the science source or reference can also invalidate the common-channel premise.

The [replay](check_written_herald.py) computes the projections directly from the filter’s signed amplitudes. The eleven-wire OpenQASM circuit includes the actual herald measurement, a separate fair choice made afterwards and a fresh terminal pointer. Its output bits are `herald`, `test` and `answer`. On the sector arm (`test=0`), `answer=1` denotes the physical good sector. On the return arm it denotes successful all-zero return. The optional Qiskit check propagates all eight possible recorded triples including both dark ones. All results here are circuit predictions.

    python -I -B check_written_herald.py
    python -I -B check_written_herald.py --qiskit
    python -I -B check_written_herald.py --qasm fresh.qasm

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the restricted-input verification, sharp conditional bound and control circuit.
