# Opening the walk's selector wire tests a private change of herald rate

The [finite feedback writer](a_private_controller_for_the_walk_herald.md) can assign private success rates $1/2$ and $25/146$ while passing every public experiment on the original four logical inputs. On that input space the ideal success probability is the same for every state. The existing six-wire circuit already has an input that removes this degeneracy. Prepare its Pell selector coherently instead of fixing it to zero. Under the quantum-instrument model, an ideal result of the resulting test forces the herald rule even in each pre-existing classical mode of the writer. The argument uses a special case of instrument extremality. [D’Ariano, Perinotti and Sedlák, Theorem 5](https://arxiv.org/abs/1101.4889)

## Change the preparation, keep the writer

Let $V$ be the six-wire walk with its three path and rejection wires initially zero. The two former logical wires (rail and control) and wire $q_5$ (the Pell selector) can now carry any three-qubit input. Let $A_z=\Pi_z V$ for the original good and bad output sectors and $E=A_G^\dagger A_G$. The target branch maps are $\rho\mapsto A_z\rho A_z^\dagger$. The same physical writer must handle all these inputs. It has no classical read of the preparation or access to the outside reference. [Original Pell filter](a_phase_reference_from_synchronized_walks.md)

The first Hadamard on the selector sends its $X$-basis inputs to the two Pell branch labels. The selected good Kraus matrices on the rail are proportional to $I$ in the idle-control arm and to $X+Z$ in the acted arm. Direct projection of the four signed paths gives the following success probabilities on any unit rail input.

| Initial selector | Idle control | Acted control |
|---|---:|---:|
| $\lvert +\rangle$ | $1/16$ | $1/8$ |
| $\lvert -\rangle$ | $9/16$ | $1/2$ |
| Original $\lvert0\rangle$ | $5/16$ | $5/16$ |

Each of the first four eigenvalues occurs twice, once per rail dimension. The effect is diagonal in the joint control and selector eigenbasis because the corresponding output labels are orthogonal. In the computational basis of the selector, both diagonal blocks are $(5/16) I_4$ and the off-diagonal block is $\operatorname{diag}(-1/4,-1/4,-3/16,-3/16)$ in rail-fast order. Merely changing between the two computational input bits would miss the distinction.

## A test with no extra classical setting label

Entangle the three free input qubits with three protected reference qubits. Apply $V$ and let the actual writer produce its science label. Only then choose between checking the sector and undoing the walk and the three Bell preparations. The first test compares the saved label with the actual output sector. The second tests whether all nine gate and reference wires return to zero. This is the [post-write experiment](checking_the_state_left_by_a_written_herald.md) enlarged by one Bell pair on the previously blank selector. It uses twelve wires including the choice and pointer wires. The rates below are per attempted launch in each test arm.

| Saved label | Label rate $s_z=\operatorname{tr}(A_z^\dagger A_z)/8$ | Joint sector mismatch | Joint Bell return |
|---|---:|---:|---:|
| G | $5/16$ | 0 | $25/256$ |
| B | $11/16$ | 0 | $121/256$ |

Although the target rates equal the earlier table numerically, the coherent input and inverse test differ. Let $|\Psi\rangle=(V\otimes I)|\Phi_8\rangle$ and $|\phi_z\rangle=(\Pi_z\otimes I)|\Psi\rangle/\sqrt{s_z}$. At zero mismatch a conditional branch state lies entirely in the reported sector. Its Bell-return probability is at most $s_z$, with equality only for $|\phi_z\rangle\langle\phi_z|$. The measured joint and label rates therefore fix both Choi operators on the entire eight-dimensional input, including their coherences between selector states. [Choi's correspondence](https://doi.org/10.1016/0024-3795(75)90075-0)

Now suppose an unobserved classical mode $h$ exists before the independent preparation, with a common distribution over trace-preserving quantum instruments. Allow arbitrary private feedback and multiple Kraus operators in each branch. Each positive branch Choi operator in the mixture must be supported on its observed one-dimensional range almost surely. Hence its branch map is $a_{h,z} A_z(\cdot) A_z^\dagger$ for nonnegative $a_{h,z}$. Trace preservation *in that mode on all admitted inputs* requires
$$
a_{h,G} E+a_{h,B}(I-E)=I.
$$
Taking expectations in the idle states of success probabilities $1/16$ and $9/16$ and subtracting gives $a_{h,G}=a_{h,B}$. Either equation then gives both equal to one. This proves that each such mode has the original science rate $5/16$ on the selector-blank subspace and the full predicted law on every enlarged input. On the original subspace alone $E=(5/16)I$, which leaves only one scalar equation and admits the earlier two-rate writer. More generally these two linearly independent effects suffice for any binary instrument with rank-one nonzero Choi branches.

## A bound for imperfect returns

Let $p_z$ be the observed label rate, $\alpha_z$ its conditional sector-mismatch rate and $\beta_z$ its conditional Bell-return rate. Set
$$
 f_z=\frac{[\sqrt{\beta_z}-\sqrt{(1-s_z)\alpha_z}]_+^2}{s_z},
 \qquad e=\sum_z p_z(1-f_z).
$$
The split of $|\Psi\rangle$ into its two orthogonal sectors and the triangle inequality give conditional Choi fidelity at least $f_z$. For a zero-incidence branch omit its term. Use simultaneous confidence bounds on the raw joint counts including all timeouts when estimating these quantities. Values inconsistent with a valid state should be tested against the model before interpreting them. [Post-write fidelity inequality](checking_the_state_left_by_a_written_herald.md)

For each private instrument let $t_{h,z}$ be its Choi trace on the normalized maximally entangled input. Put $a_{h,z}=t_{h,z}/s_z$. The trace norm $\delta_{h,z}$ from its unnormalized Choi operator to $t_{h,z}|\phi_z\rangle\langle\phi_z|$ is at most $2\sqrt{t_{h,z}\epsilon_{h,z}}$, where $\epsilon_{h,z}$ is its mass outside $|\phi_z\rangle$. This follows by purification and trace-distance contraction. The traces sum to one for every mode. Summing and applying Cauchy–Schwarz across modes gives $E_h\sum_z\delta_{h,z}\le 2\sqrt e$. [Fuchs and van de Graaf](https://arxiv.org/abs/quant-ph/9712042)

For any input density operator, its branch probability differs from the scaled target by at most $d\delta_{h,z}/2$ with $d=8$. In normalized Choi coordinates this is the expectation of $d(I_{\rm out}\otimes\rho^\mathsf{T})$ on a trace-zero difference. Put $b_h=(d/2)\sum_z\delta_{h,z}$. Completeness tested on a state with good effect $\lambda$ implies $|a_{h,G}\lambda+a_{h,B}(1-\lambda)-1|\le b_h$. Choi trace normalization gives the same expression exactly zero at $s=5/16$. At $\lambda=1/16$ the difference is $|a_{h,G}-a_{h,B}|/4$. For **any original science input** with blank selector this yields
$$
 E_h\,|P_h(G)-5/16|\le \min\{1,(119/8)\sqrt e\}.
$$
Indeed the discrepancy is at most $b_h+s(1-s)|a_{h,G}-a_{h,B}|\le(119/64)b_h$. For the earlier two-mode writer the mean absolute discrepancy is $165/1024$. Any common instrument extending those mode rates to this enlarged experiment must have $e\ge(165/15232)^2$. This bound is conservative. It concerns population errors and permits small sets of badly performing modes.

## Controls and scope

A rival first measures the selector in the $X$ basis and then uses the ideal walk. Every classical test using a definite $+$ or $-$ selector passes, and the sector always agrees with the reported label. With the coherent Bell input the good and bad joint returns instead fall to $149/2048$ and $533/2048$. The good branch has $3/64$ and $17/64$ of its Choi mass in the two selector components; an unread copy removes their interference. The bad branch has $29/64$ and $15/64$. The sums of the corresponding squares give the two altered returns. Ignoring which outputs are bright or dropping one of the reference qubits would test a different instrument.

An arbitrary record generated *after* the outcome can correlate with it even for this extreme instrument. Likewise preparation-dependent hidden sampling, correlated initial reference and apparatus, an instrument chosen after learning the test, or a scoring rule outside the quantum CP model evades the argument. This experiment makes mode-specific rates identifiable within a stated operational theory. It uses the ordinary quantum probability law to interpret its terminal measurements. Establishing that law from prephysical dynamics and connecting those physical records to the classical limit remain open.

The [exact and optional Qiskit replay](check_open_pell_wire.py) tests the complete effect and both twelve-wire circuits. Run the checker with `--qiskit` for dynamic outcome verification. All rates are predictions for the specified circuits.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the preparation, proof, controls and replay.
