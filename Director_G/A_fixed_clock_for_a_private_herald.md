# A fixed clock for a private herald

An observer can watch every position record in a prescribed sequence of $K$ blocks without learning whether a measured walk has one long-time velocity or two. The [previous construction](How_far_a_herald_record_can_identify_motion.md) drew a private setting from a posterior distribution before each block. Its exact sampling time was unbounded. Here a rotating register supplies the targets on a fixed schedule. A return test on the next block separates the mechanisms by at least **0.66 percentage points**, uniformly in $K$. The price of exact matching is paid in preparing the register.

## Keep the actual herald operation

In the [six-wire preparation](../candidates/composition_record/velocity_experiment/a_private_controller_for_the_walk_herald.md), the held mode has stationary weights $\pi=(55,73)/128$. Its successive private targets $T$ are independent given the mode, with probabilities $a_0=467/880,\ a_1=173/1168$ for target one. The genuine projected walk, comparison with the target, optional reflection and second measurement give final herald rates $b_0=45/1024,\ b_1=925/1024$ conditional on the target. The resulting held-mode herald rates are $p_0=1/2,\ p_1=25/146$. Each independent launch draws its mode before the run.

Use the [four-tick walker](Private_heralds_in_a_measured_walk.md) with distinct fresh auxiliary trials. On a successful herald make the extra site measurement. Let $K_h$ denote the full-site displacement kernel conditional on herald $h$. Conditional on target $t$, the kernel is $L_t=(1-b_t)K_0+b_tK_1$. Thus the probability of return changes from $557/4096$ to $1437/4096$ when the target changes from zero to one. Write $\beta=55/256$ for this difference. Under the right-site probe the mean displacement at herald $h$ is $-h/4$.

## Read a slot before changing it

Fix $K\ge1$. For a particular $K$-bit target word $w$ with $j$ ones define

$$
 \mu(w)=\sum_i\pi_i a_i^j(1-a_i)^{K-j}.
$$

Preload $K$ target bits with this distribution. At each block feed the oldest bit to the genuine herald operation. Update only that used slot, then rotate it to the back. The update reads the other $K-1$ bits $u$. Write $A:B=\mu(0u):\mu(1u)$ in positive coprime integers. Choose one power of two $D\ge 2\max_u(A+B)$ for the apparatus. If the used bit was zero, flip it with probability $B/D$. If it was one, flip it with probability $A/D$. A fixed $\log_2 D$ fair bits and an integer comparison implement either rule. The target register receives no information from the science walk or its outcomes. Pad the two branches of the original herald operation to the same block clock. These are logical clock and randomness budgets for the specified finite apparatus.

Conditional on $u$, the flows $A B/D$ and $B A/D$ balance before normalization. Updating one slot preserves $\mu$, and rotation preserves it by exchangeability. The next $K$ outputs are the $K$ distinct bits already in the register at the start of the window. Later updates to those slots cannot change their earlier reads. Thus every stationary window of $K$ targets has its original held law. The same holds for the actual heralds and recentered displacements through their common conditional operations. Even access to the successive targets in that window preserves the equality. A read of the controller's private state before each update would be a different experiment. Single-coordinate updates preserving a joint distribution are familiar from systematic-scan sampling. Here their read order fixes the entire short observation law. [He et al., *Scan Order in Gibbs Sampling*](https://pmc.ncbi.nlm.nih.gov/articles/PMC5361064/)

In a complete sweep, each slot can flip or stay with strictly positive probability. Every final target word can be reached from every initial word. The finite register in the rotating representation is therefore ergodic. The empirical target fraction tends to $m=5/16$. With fresh native trials the herald fraction tends to $(1-m)b_0+mb_1=5/16$. Conditional on the full exogenous herald sequence, the centered full-site displacement increments are independent, bounded and have average variance tending to $75/16$. The central limit theorem gives $N(0,75/16)$ after dividing the total displacement by $\sqrt n$. Under the right-site probe the bounded conditional noise averages to zero, so the limiting velocity is $-5/64$ per block. The held model has the two Gaussian variances $5-p_i$ or the two velocities $-p_i/4$. This comparison fixes $K$ before taking $n$ to infinity.

## A sharp probability gap at the first distinguishing span

At span $K+1$ condition on the middle $K-1$ targets $u$. They are the other slots present when the first slot is updated. Both endpoint targets have mean $q=E[a\mid u]$ in both models. The covariance of the held endpoints is $\mathrm{Var}(a\mid u)$. For the register, the last endpoint is the very slot used and updated at the first clock. Its conditional covariance with the original value is $(1-(A+B)/D)q(1-q)$. Denote the register covariance minus the held covariance by $g_u$.

The sign is positive for every middle word. Indeed $q\in[1/8,9/16]$ gives $q(1-q)\ge7/64$, while a variable in that interval has variance at most $49/1024$. Since $(A+B)/D\le1/2$, it follows that $g_u\ge7/1024$. In the two endpoint target table the signed differences are $+g_u$ on the diagonal and $-g_u$ elsewhere. Passing through the common displacement channels multiplies the signed endpoint factors by $L_1-L_0$. Its positive part is at return, its negative part at displacements $\pm2$, and its total variation norm as a difference of probabilities is $\beta$. Summing over the middle records cannot reverse these signs. As in the [endpoint factorization](How_far_a_herald_record_can_identify_motion.md), agreement of the two endpoint return indicators attains the entire total variation distance of the full $K+1$ displacement word. The register has the greater agreement probability by $2\beta^2 E g_u$.

For a stronger uniform bound put $V=\mathrm{Var}(a)=144/4015$. Total variance gives

$$
 E g_u\ \ge\ \tfrac12 m(1-m)-V+\tfrac12\mathrm{Var}(q)
 \ \ge\ 147097/2055680 .
$$

Hence the agreement gap is at least $8090335/1224736768$, approximately $0.00660577$. Equality occurs for $K=1$, $A:B=11:5$, $D=32$. A larger choice of $D$ can change the separation. The event is measured from the two block displacements at lag $K$; intervening target bits need only be conditioned on in the proof. No physical sample size or observed frequency is asserted.

## What fits on a clock, including preparation

Only the count of ones in $u$ enters the two thresholds. There are $K$ rows for the $2^K$ possible register configurations. For example $128(16\cdot55\cdot73)^K$ clears all $K$-word denominators, so the integer thresholds and the number of fair bits per update are $O(K)$ and the table uses $O(K^2)$ bits. There are $K$ stored target bits. The [exact replay](check_clocked_herald_register.py) uses the smallest common admissible power of two. At $K=8$ it uses 115 fair bits per update and gives an agreement gap of $0.01548527$.

Exact stationary preparation is a separate physical resource. For $K\ge2$ the held law gives two actual successes with probability $145/1168$ and two actual returns with probability $401/9344$. Both reduced denominators contain $73$. A sharp initial state, bounded fair splits and fixed dyadic branch probabilities can produce only dyadic event probabilities, even with classical feedback. Finite Hadamard-and-sign path sums at fixed clock yield dyadic squared probabilities as well. Thus no exact implementation under those restrictions can match this two-block panel, including the held comparator. A preloaded ensemble or an almost surely terminating prelaunch rejection draw can supply the distribution. A deterministic cycle with a uniform initial phase has a separate [period and preparation cost](The_period_of_a_herald_target_tape.md).

There is also a bounded preparation with an explicit error. Draw the mode from its seven-bit prior. Round each $a_i$ to the nearest multiple of $2^{-b}$ and initialize each of the $K$ slots with an independent $b$-bit comparison at that rounded rate. Coupling each draw to the exact conditional target gives initialization error at most $K\,2^{-(b+1)}$ in total variation. Whenever the queues agree they can share all later update bits and genuine conditional operations. The same bound therefore holds on the entire subsequent register output law relative to its stationary version, regardless of run length. Each $K$-window matches the ideal held experiment within this error. For the endpoint test the guaranteed gap relative to the ideal held law decreases by at most this error. Every initialization still tends to the register's single long-time velocity. At $K=32,\ b=18$ the preload uses 583 fair bits and the error is at most $1/16384$.

This identifies a resource that short position records cannot certify and an additional reading that tests it for a specified memory length. [Opening the herald selector](../candidates/composition_record/velocity_experiment/opening_the_pell_selector.md) enlarges the permitted preparation and read interface. The present equality concerns the common target-conditioned channel on the original preparation. The native conditional probability law, the meaning of a fair split and the availability of the auxiliary apparatus remain assumptions of the walk.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex constructed and independently checked the register, its covariance bound and the preparation obstruction.
