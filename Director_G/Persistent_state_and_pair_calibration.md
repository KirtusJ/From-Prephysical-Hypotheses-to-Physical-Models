# Exact pair calibration can coexist with uninformative repeated measurements

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement prepared by OpenAI Codex for Director G.

Suppose calibration specifies the exact four-outcome distribution for one pair at every prescribed mass, averaged over runs. Permit an unobserved state to persist throughout a run. On the finite routed menu at M = 10⁻⁸, the best guaranteed equal-prior error is **49.999999422693%**, to the displayed precision. This value holds for any budget of at least one pair, including four quadrillion. A single pair attains it, and even adaptive mass selection cannot improve the worst case.

### Constructing a persistent state

Write Pₛ and Qₛ for the two nominal tables at mass s, dₛ for their total variation distance, and D for the largest dₛ. At each mass let Cₛ be the normalized cellwise minimum of the tables. Its denominator is 1−dₛ. The subprobability table (1−D)Cₛ fits inside both tables because D ≥ dₛ. Subtract this common part from each nominal table and divide by D to obtain the two residual tables.

Draw one Bernoulli state per run with probability D of using the residual tables. In the other state, draw every pair from Cₛ at its selected mass under either hypothesis. In the residual state, draw each pair from the residual table of the true hypothesis. Use independent draws conditional on the run state and the mass choices. Identical controls use the same nominal law in both branches. Under every predetermined sequence of masses, every individual pair then has exactly its calibrated table. At any fixed mass the repeated pairs are exchangeable. Following an adaptive choice, the observed history can change the conditional mixture weights. The construction makes no claim of conditional calibration given that history.

### Why the guarantee is exact

The common-state probability is 1−D under each hypothesis. In that state any policy, including a randomized or adaptive one, has identical transcript distributions under P and Q. Even revealing the state would leave equal-prior error one half on this branch. The unconditional error of every binary decision is therefore at least (1−D)/2 on this admissible pair of processes.

Conversely, take one pair at a mass attaining D and choose the hypothesis with larger probability for the observed cell. Its equal-prior error is half the sum of the two tables' cellwise minima, exactly (1−D)/2. This upper bound holds under every temporally dependent process with the stipulated one-pair calibration. Together the inequalities establish the minimax value without any large-sample approximation. The result concerns average error under equal prior weights. In particular, a uniform 5% guarantee under each hypothesis is impossible in this class.

The [exact rational checker](check_persistent_pair_calibration.py) reconstructs the common and residual tables at every informative lower-half node. Complementary masses relabel outcomes and preserve total variation; identical controls contribute zero. The largest TV distance is approximately 1.15461404388488 × 10⁻⁸, attained at mass approximately 0.141270071844. This mass maximizes the single-pair TV distance; earlier independent-pair tests used a different mass.

This counterexample describes what unconditional pair calibration alone permits. It does not establish persistent state in a physical detector. The [conditional drift guarantee](Detector_drift_with_fixed_marginals.md) has a stronger premise that bounds the next pair law after every observation history.
