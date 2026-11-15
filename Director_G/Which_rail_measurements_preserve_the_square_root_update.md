# Which rail measurements preserve the square-root state update?

Two instruments can agree on every reported probability and leave different rail states. For the axis $H=(X+Z)/\sqrt2$ this distinction gives an arithmetic constraint on an exact instrument. In the synchronized digital walk menu, every computable strength $0\le\eta<1$ can be realized for the *outcome probabilities* $E_\pm=(I\pm\eta H)/2$. The Lüders state update $\rho\mapsto\sqrt{E_\pm}\rho\sqrt{E_\pm}$ is exactly realizable at the more restricted strengths

$$
 \eta=\frac{2\sqrt2\,t}{1+2t^2},\qquad
 t\in\mathbb Q,\quad 0\le t<1/\sqrt2 .
$$

The menu admits sharp ancillas, signed permutations, synchronized whole-wire Hadamards, coordinate projections that preserve the coherence of unresolved sectors, fresh independent fair records, and almost surely finite classical control. Gates to which only one coherent arm is subjected are charged as extra resources unless compiled from this menu. A trial may take a variable number of steps. The classification is about the complete operation on an arbitrary input, including one half of an entangled pair.

## Necessity

Given the classical randomness and a finite fine record, each rail Kraus matrix is proportional to an integer matrix. A uniform Hadamard on its wire adds or subtracts rows with one common scale. Signed permutations and coordinate masks preserve the form. Include output coordinates of any unused ancillary system as additional Kraus labels. Post-measurement classical choices select the next such operation. This branch property was used in the [synchronized-gate obstruction](../candidates/composition_record/velocity_experiment/a_phase_reference_from_synchronized_walks.md). [Amy et al. on Toffoli–Hadamard synthesis](https://arxiv.org/abs/2305.11305)

The Choi operator of each nonzero Lüders outcome has rank one. Its positive fine-branch summands must therefore have range on the same Choi line. The statement remains true for a classical mixture and an almost surely finite stopping time, by testing the nonnegative mass in the orthogonal complement. Thus any nonzero fine Kraus in that outcome is proportional to its positive square root. Write the positive-outcome square root as a positive scalar times $I+tS$, $S=X+Z$. The off-diagonal entry divided by the half trace equals $t$, which must be rational. Positivity requires $0\le t\le 1/\sqrt2$, and equality would be irrational. Squaring with $S^2=2I$ gives the displayed strength. In particular no strictly positive rational $\eta$ is the strength of an exact Lüders instrument in this menu.

Even if only outcome probabilities are prescribed, $\eta=1$ is impossible. A positive fine effect for the sharp positive outcome would have its range in the corresponding one-dimensional eigenspace. The finite fine effect is proportional to a rational matrix, while the required eigenspace has coordinate ratio $\sqrt2-1$. No nonzero such fine effect exists.

## A circuit for every allowed state update

Let $t=b/a$ with nonnegative coprime integers, $a>0$, and choose the least power of two $L\ge a+2b$. Prepare a label qubit in $|+\rangle$ and prepare $L$ Walsh paths. On $a$ paths apply $I$. On $b$ paths each apply $X$ or $Z$, with the additional sign determined coherently by the label qubit. Flag the other paths. Undo the path Walsh. A single coarse success projector asks for a clear flag and the zero path while preserving the label. The two label components of the successful isometry are $(aI\pm bS)/(\sqrt2 L)$. Its probability $p=(a^2+2b^2)/L^2$ is independent of every input rail state. Keep the label coherent during any recovery.

Let $W$ implement this preparation from blank auxiliary registers. Write $W|0,v\rangle=\sqrt p\,G(v)+\sqrt{1-p}\,B(v)$ for the normalized good and bad branches. After the coarse failure apply $W(I-2P_\mathrm{blank})W^\dagger$, then repeat the same coarse sector measurement. On $B(v)$ this reflection gives $-2\sqrt{p(1-p)}G(v)+(2p-1)B(v)$. It follows from $P_\mathrm{blank}W^\dagger B(v)=\sqrt{1-p}\,|0,v\rangle$ and holds with a spectator. Until the first success the same recovery is available. The eventual success probability is one. For $0<p<1$ the mean number of extra reflections, counting also launches succeeding on the first try, is $1/(4p)$. The elementary $p=1$ case requires no recovery. Cauchy's inequality gives $p>1/12$. A finite deadline must retain the failure outcome. Resolving the individual bad paths would change the recovery. [Earlier reflection construction](Rational_references_and_optical_bypass.md)

Now read the label. Its matrices are $(aI\pm bS)/\sqrt{2(a^2+2b^2)}$. They are positive and give the required instrument. For instance $(a,b)=(3,2)$ gives $\eta=12\sqrt2/17$, with first-try probability $17/64$. Positive solutions $a^2-2b^2=1$ obtained by powers of $3+2\sqrt2$ take this family arbitrarily close to strength one. The [four-route stopped instrument](Reading_a_rail_axis_with_four_coherent_routes.md) also approaches that boundary with unchanged coherent hardware and a growing classical threshold.

On a Bell input the return probability to the same Bell state, pooling the two outcome labels, is

$$
 \tfrac14\sum_\pm|\operatorname{tr}\sqrt{E_\pm}|^2
 =\frac{a^2}{a^2+2b^2}>\tfrac12 .
$$

Every measure-and-prepare channel has a separable output on this input and gives at most $1/2$, since any product state has at most that squared overlap with a two-qubit Bell state. This is a test for surviving entanglement. A single return probability does not determine the entire instrument.

## All strictly unsharp effects

For a specified computable $\eta<1$, choose an allowed strength $\eta_0$ strictly between $\eta$ and one. Use that analyzer with probability $\eta/\eta_0$. Otherwise report a fresh balanced sign. The resulting two effects are exactly $E_\pm$. Independent fair bits can sample the computable mixing probability by comparing the prefixes of a uniform binary real with narrowing rational brackets for the threshold. The comparison terminates almost surely, with a separate time cost for computing the brackets. This construction assumes that the requested strength is specified to the apparatus.

For an explicit example using the [stopped walk reference](A_stopped_walk_reference_for_the_real_embedding.md) itself, take $\eta=1/2$. Use two fair bits for a mask. Two cells enable a basis read, one enables it only when the stopped counter is killed, and one disables it. The enabling probability is $(3-u)/4=1/\sqrt2$, where $u=3-2\sqrt2$ is the counter's hit probability. On enable choose the $X$ or $Z$ basis equally and report its projective sign. On disable report a fair sign. The resulting effects are $(I\pm H/2)/2$. The terminal references here genuinely choose measurements on the input rail. The arithmetic obstruction above shows that the same device cannot have the exact Lüders update at this strength. A variant may discard the rail and prepare a replacement after reporting the same bit.

The tests use ordinary conditional quantum instruments. They establish a difference between observable effects and coherent updates within that theory. They do not select a unique probability embedding across jointly relabeled preparations, operations and detectors.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex derived the classification and its constructive and disturbance controls.
