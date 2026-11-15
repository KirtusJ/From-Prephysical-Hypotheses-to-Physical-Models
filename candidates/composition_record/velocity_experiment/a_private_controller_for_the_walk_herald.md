# Two private herald rates from one finite walk circuit

A stopped walk gate can show the ordinary success rate $5/16$ and leave the predicted quantum state on **every** logical input, even when two private settings fixed before the input arrives have success rates $1/2$ and $25/146$. The [post-write instrument test](checking_the_state_left_by_a_written_herald.md) left the physical realization of this rival open. Here eleven fair bits, a genuine intermediate herald, and at most one reflection implement it exactly. A measurement across the intermediate write distinguishes the circuit from the ordinary single write. All rates below are theoretical population probabilities.

## The two projected branches

Let $V$ be the six-wire walk isometry on its four-dimensional logical input, with the other four wires blank. The known walk computation gives $V^\dagger\Pi_G V=sI$ for $s=5/16$. Write $\Pi_B=I-\Pi_G$, $s_G=s,\ s_B=1-s$ and $K_z=\Pi_zV/\sqrt{s_z}$. The ordinary instrument returns label $z$ with output map $s_zK_z\rho K_z^\dagger$. No deterministic implementation of either normalized $K_z$ is presumed. [Walk circuit](a_phase_reference_from_synchronized_walks.md) · [Signed reflection and recorded-sector transitions](changing_a_herald_before_it_is_written.md)

The native reflection $R=I-2VV^\dagger$ runs the full walk unitary backwards, changes the sign on the four-work-wire blank subspace, and runs the walk forwards. For any logical vector, applying $R$ to $K_G$ gives $(1-2s)K_G-2\sqrt{s(1-s)}K_B$; applying it to $K_B$ gives $-2\sqrt{s(1-s)}K_G+(2s-1)K_B$. Thus a fresh sector read after the reflection changes the label with probability $\tau=4s(1-s)=55/64$ in either direction. On each measured history the output operator is a scalar times its final $K_z$. This operator identity covers arbitrary mixtures and entanglement with an untouched spectator. The reflection uses the same subspace geometry as amplitude amplification. [Brassard, Høyer, Mosca and Tapp](https://arxiv.org/abs/quant-ph/0005055)

## A finite writer for the four-path gate

Before the science system arrives, generate eleven private bits with fresh balanced splits and ordinary reads. Compare the resulting unsigned integer $J$ against the cumulative interval endpoints below. Store a private mode $M$ and a target bit $T$.

| Values of $J$, inclusive | Mode $M$ | Target $T$ | Number of patterns |
|---|---|---|---:|
| 0–466 | Flat | G | 467 |
| 467–879 | Flat | B | 413 |
| 880–1052 | Square | G | 173 |
| 1053–2047 | Square | B | 995 |

Apply $V$ and genuinely read the first sector $X$. If $X\ne T$, reflect once. In both arms measure the actual sector again and report this second label $Z$. This can use two distinct pointers and a reversible control on the saved bit. A new input requires fresh private randomness for the comparison to a memoryless public instrument. The target and first record remain private. Keep the two arms on a common public clock when testing that interface.

For a fixed target, the final success probabilities are $s+(1-s)\tau=925/1024$ for G and $s-s\tau=45/1024$ for B. Thus if $r=\Pr(T=G\mid M)$ the reported success rate is $s+\tau(r-s)$. The counts above solve this linear equation separately in each mode.

| Mode | Incidence | Conditional target G | Conditional reported G |
|---|---:|---:|---:|
| Flat | $55/128$ | $467/880$ | $1/2$ |
| Square | $73/128$ | $173/1168$ | $25/146$ |

On the binary mass table $(5/16,11/16)$, these are exactly the power-zero and power-two probabilities. The internal reads and gates use ordinary quantum mechanics throughout. The calculation constructs two physically recorded conditional populations with those rates. It supplies no independent law changing the probability of a primitive quantum measurement.

The marginal target probability is $640/2048=s$, so the final good probability is $s$. Since every private history ending at $z$ has output proportional to $K_z$, the averaged *branch map* is exactly $s_z K_z\rho K_z^\dagger$. A classical label and the quantum output are the entire public interface. With fresh independent controller draws, composition of these identical maps gives identical records under any finite causal sequence of calls to that interface, including adaptive settings on the logical inputs and intermediate operations on a spectator. The assertion does not grant access between the gates, to the controller bits, to physical timing differences or to coherent superpositions of black-box uses. [Operational composition of quantum instruments](https://arxiv.org/abs/0904.4483)

## Which additional records distinguish it?

* **The earlier sector.** At the gate output, save a trusted copy of the projected sector before feedback, insulated from the controller. Compare it to the final herald. Two ordinary consecutive reads on an undisturbed sector always agree. The finite writer disagrees with probability $2s(1-s)\tau=3025/8192$, equally divided between the two directions. Equivalently, an independently prepared input confined to the good branch flips to bad with probability $(1-s)\tau=605/1024$ when supplied directly to the writer after $V$. The original process test only admits inputs upstream of $V$.
* **The same private mode twice.** Hold $M$ fixed and prepare two independent target draws conditional on that mode, with fresh science trials. The excess double-good probability over $s^2$ is $\mathrm{Var}(\Pr(G\mid M))=495/18688$. Retaining both $M$ and $T$ instead gives the larger excess $166375/1048576$. Reusing independent ordinary preparations alone cannot enforce which part of the controller persists. Conditional target draws can be made by drawing new bit strings until their mode matches the held value; keep such extra draws in the resource account. [Scope of paired-read evidence](../../../Director_G/Paired_reads_for_a_type_dependent_target.md)
* **A second mass.** For any $0<x<1$, a flat/square mixture with fixed flat weight $a$ gives $a/2+(1-a)x^2/[x^2+(1-x)^2]$. Equality with $x$ at $x\ne1/2$ requires $a=2x(1-x)$. Two noncomplementary masses away from one half therefore refute the same held mixture if it claims the ordinary rate on both. The fair point supplies no constraint. The eleven-bit table was chosen for the actual four-path gate.

The same circuit also admits an enlarged input test: the previously blank Pell selector can carry a third logical qubit. This changes the completeness equations for any private writer that must act on that entire space. [Opening the selector and testing the effective instrument in each private mode](opening_the_pell_selector.md)

## An exact extension when the setting may change the mode population

A second writer uses the native gate to choose its own mode distribution. It works for each scalar-success isometry with $0<s<1$ when a copy of the setting, two clean scratch preparations, its sector read and the same reflection are available. Two independent scratch gates are run before the science input arrives. If their labels disagree, use a fresh fair target. If they agree, use their common label. The two cases have probabilities $2s(1-s)$ and $s^2+(1-s)^2$. Their conditional target-good probabilities are $p_D=1/2$ and $p_A=s^2/[s^2+(1-s)^2]$. Thus the unconditional target has good probability $s$ without numerically estimating $s$.

Read the actual science sector. Until the observed label matches the target, reflect and read again. Every mismatch survives another round with probability $1-\tau$, independently of the logical input. With no cap the rule terminates almost surely and implements the two conditional target rates exactly. At a fixed cap of $k$ reflections publish the last actual label even if it misses the target. Given mode $m$, the success probability is
$$
 s+\big[1-(1-\tau)^k\big](p_m-s).
$$
Its average equals $s$ for **every** cap. Each terminal branch still outputs its corresponding $K_z$ on the full logical input. A hard cap generally changes the two conditional rates. The specifically tuned eleven-bit controller above attains the two rates at a fixed cost for $s=5/16$.

Let $N$ be the uncapped number of reflections. The exact tail is $\Pr(N>k)=2s(1-s)(1-\tau)^k$ and $E N=1/2$ for $0<s<1$. At the two sharp endpoints the scratch and science labels coincide and the cost is zero. For masses near either endpoint a rare initial mismatch can lead to a long run. At $s=5/16,\ k=2$ the timeout probability is $4455/524288$; all of those attempts contribute their actual label. A visible timeout, an intermediate record or elapsed time gives an observer a larger interface. The setting-dependent mode incidences also distinguish this extension from a detector whose mode proportions must be common to all settings.

The [finite controller and six-wire replay](check_private_herald_feedback.py) compare every input column and the full private-record probabilities. The optional Qiskit calculation replays the two target-conditioned eight-wire circuits. The [stopped-history calculation](check_repeated_herald_target.py) independently propagates the signed measured branches over nine success masses and five caps, including both dark endpoints. No physical event counts enter either check.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the circuit, proofs, counterexamples and replays.
