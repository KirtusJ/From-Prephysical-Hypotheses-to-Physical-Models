# Which probability rules fit the stopped walk with a heralded phase reference?

The addressed walk can run with an approximate gate synthesized entirely from uniformly applied Hadamards and signed permutations. In its smallest example with four selector paths, the gate succeeds on $5/16$ of inputs, independently of the rail and address. Dropping the other launches would discard most of the experiment. Here a failed gate is an outcome of the walk. Among the specified competing readers, the complete stopped-record distribution identifies ordinary probability at every realized coarse write. A reader that first scores success separately can hide a nonordinary power at every herald and produce the same complete records. [Gate construction, resource count and two-call phase check](a_phase_reference_from_synchronized_walks.md)

## The experiment

Start on rail R at site zero of the eight-site ring. The two-bit address $y$ counts left shifts modulo four. Physical site after tick $t$ is $t-2y\bmod8$. Each three-tick flight uses global H on its first and last ticks. On its middle tick apply the four-path reference with $X$ on even and $H$ on odd addresses, using fresh selector and path registers. Move after each coin. At the flight boundary record **one coarse outcome**. Its labels are failure, or success at one of the four named addresses. A failed flight ends that launch. Otherwise run the next flight, up to three. Keep the earlier addresses when a later flight fails.

For this experiment the success projector can be measured jointly with the terminal address, after the last shift. The path and rejection registers need no further coupling after the middle call. All unsuccessful path/flag coordinates form one failure effect, including all final positions. The selector choice is unresolved. This coarse instrument is a physical premise of the probability comparison. Classical processing of several separately scored readouts would implement another model.

On success the synthesized channel agrees with the addressed target followed by dephasing between the even and odd arms. Write $P=10$, $C=7$ for the filter pair and $\lambda=\sqrt2 C/P$ for its interference visibility. The ordinary first addresses given success have probabilities

$$
\left(0,\ \frac38+\frac{C}{2P},\ \frac12-\frac{C}{2P},\ \frac18\right)
=\left(0,\frac{29}{40},\frac3{20},\frac18\right).
$$

One way to obtain these numbers is to average the two signed addressed-gate probabilities $(3\pm2\sqrt2)/8$ for code 1 with weights $(1\pm\lambda)/2$. Direct integer propagation gives the same result. Per original launch the first probabilities for failure and codes 1, 2, 3 are $(88,29,6,5)/128$. At every subsequent reached prefix, the three bright successful children have different masses. Failure at that flight is always the unique largest child because its conditional probability is $11/16$.

The [exact checker](check_rational_reference_walk.py) compares a sum over physical direction paths with propagation by the individual filter matrices, summing their unresolved alternatives. It also tests both unknown signs in the nine-tick phase echo. At each flight the two outside Hadamard factors contribute an amplitude factor $1/2$. On success the two integer filters act as Kraus matrices divided by $\sqrt P$. Three successful flights therefore have word probabilities with common denominator $(4P)^3$ on the successful population. For example the reached prefix $(3,3)$ occurs on $25/16384$ of all launches. Its final positive child masses per original launch, in units of $25/2097152$, are 1, 5, 34 and 88 for codes 1, 3, 0 and failure.

| Stopping event | Ordinary probability per original launch |
|---|---:|
| Failure on the first flight | $11/16$ |
| First failure on the second | $55/256$ |
| First failure on the third | $275/4096$ |
| Three successful flights | $125/4096$ |

Including all nominal addresses gives 85 possible stored words, of which 40 carry positive mass and 45 are structurally dark. The unique maximum is immediate failure. The unique minimum positive word is $(3,3,1)$ with probability $25/2097152$. Every value is rational. [Complete conditional and original-launch tables, including all dark outcomes](../../../Director_G/results/rational_reference_walk_64.json)

## Identifiability on the stopped tree

A whole-word reader draws $Q$ before the launch and normalizes the $Q$th powers of all positive stopped-leaf masses together. A sequential reader can choose $q$ at each visited prefix, using its hidden type and the complete past before the next outcome. It raises the stipulated ordinary conditional child masses to that one power and normalizes. The choice can differ across launches and visits, including between the two types of reader. Powers may be any real number, with zero uniform on positive support and $\pm\infty$ selecting a maximum or minimum there. Ties at extrema can be broken arbitrarily. The successful state update is the stated coarse instrument at that address. Admitting an independently chosen disturbance after each successful write changes its later masses.

At a reached parent, choose the smallest positive child mass $l$, one intermediate mass $m$, and the largest $h$. Use conditional masses, set $\theta=\log(m/l)/\log(h/l)$, and score those three outcomes respectively by $(1-\theta)/l,-1/m,\theta/h$. Assign zero to all other outcomes and nonvisitors. The ordinary mean is zero. A visiting sequential reader with finite $q$ contributes a positive multiple of

$$
(1-\theta)l^{q-1}+\theta h^{q-1}-m^{q-1}.
$$

This is nonnegative by weighted arithmetic–geometric mean and vanishes exactly at $q=1$. Either extreme selector gives positive score because its local extremum is unique and has positive coefficient. At a terminal parent the same argument holds for finite whole-word powers. Its children are leaves, so their unconditional masses differ from their conditional masses by the same positive factor. [Related full-depth sibling test](test_each_write.md)

1. At $(3,3)$, exact ordinary probabilities give zero mean. Every finite whole-word mode visits this parent with positive probability and therefore must have $Q=1$ almost surely among those modes. The global minimum word arrives at its smallest child and scores positively, excluding $Q=-\infty$. A global maximum selector always fails at the root and contributes zero here. Visiting sequential modes contribute nonnegatively.
2. At the root the remaining ordinary whole-word modes give zero and the global maximum selector gives positive score on immediate failure. All sequential-root modes again contribute nonnegatively. Thus the whole-word maximum mode is excluded too.
3. At any of the thirteen reached parents each remaining whole-word mode now gives its ordinary zero mean. The sequential contributions can vanish only if every realized choice there has $q=1$ almost surely. A hidden policy’s unvisited branches cannot be inferred. A zero observed count at a rare leaf does not establish an exact population equality.

The separation concerns the recorded probability response to physical coarse outcomes. It leaves the two algebraic embeddings indistinguishable on this rational instrument. The earlier experiment with an independently calibrated controlled Hadamard can distinguish their predictions for the specified algebraic gate. A three-tick comparison also shows why reversing the sign convention of an unknown piece of hardware can preserve the data. [Calibrated-gate witness](selecting_the_real_embedding.md) · [Reciprocal splitter and its phase-transfer control](a_three_tick_phase_transfer.md)

## A reader with the same table and a different rule

Suppose the herald is a binary read in its own right. At every visit choose $q=0$ with probability $55/128$ and $q=2$ with probability $73/128$. The success probabilities for those two choices are $1/2$ and $25/146$, from the binary masses $5/16$ and $11/16$. Their mixture is exactly $5/16$. After success, use the ordinary conditional positions and the same state update. Induction on the reached prefix gives every ordinary stopped-word probability although none of the herald choices used exponent one. This counterfeit also works with the herald result kept hidden until the final report. The physical grouping at which the rule is applied matters.

No hardware data enter these calculations. The instrument specifies synchronized signed propagation, protected relative phases for the auxiliary paths, faithful address readout and a single coarse failure-or-position record per flight. Its survival through $j$ flights has ordinary probability $(5/16)^j$, while the surviving channel preserves a rail and coherent position information. Connecting those stipulated operations and the observed event grouping to a prephysical law remains open.

    python -I -B check_rational_reference_walk.py
    python -I -B check_rational_reference_walk.py --table new_table.json

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the stopped-record comparison and exact replay.
