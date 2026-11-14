# Which probability law does a selected walk display?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Suppose the walk initially admits the classified family of stationary scores on signed path multisets. A sequence of ordinary position reads has a joint probability in that family. Its accepted records can select the operational response of one character whenever the input contains that response. The derivation uses the complete recorded histories and does not assume a fresh quantum state or an independent launch after each read. The unit response of a prepared ensemble and the law of the original source are different quantities that can be measured.

## Two recorded wells fix one sharp arrival

Use the balanced signed walk on the $4M$-well ring with staircase gain $\lfloor x/2\rfloor$ on departure. The earlier classification assumes that a position product event has a sum of nonnegative stationary terminal port scores depending on the signed-residue multisets, with a common factor on extension by an unrestricted tick. Preparation of arbitrary signed multisets by whole-position masks gives this factor as two. For a sharp source, the normalized probability for a length-$t$ event ending at one port with multiset $U$ is

$$
2^{-t}\left[c\,|U|+\sum_{d=0}^{\lfloor M/2\rfloor}b_d
\left|\sum_{(\sigma,g)\in U}\sigma\,e^{2\pi i dg/M}\right|^2\right],
\qquad c,b_d\ge0,\quad c+\sum_db_d=1 .
$$

These coefficients are properties of the initial operational law on that family. Equal weights on all signed characters are an additional specification. They follow, for example, from squaring coordinates on the full lifted walk with a spatially localized sheet and tracing that sheet. The identity is finite Parseval: for integer signed endpoint counts $n_y$, $\sum_y n_y^2=M^{-1}\sum_s|\sum_y n_y e^{2\pi i sy/M}|^2$. The position-product classification alone also admits zero unit weight and pure counting. [One-walker classification and its assumptions](Preparing_signed_sheet_residues.md)

A length-$t\ge1$ block ends at $(x,r)$ exactly when its last two wells are $x-\Delta_r,x$, where $\Delta_R=1$, $\Delta_L=-1$. The two predecessor wells are distinct on this ring. Both singleton position filters transmit both incoming rails at their well. For $t=1$ the penultimate position is the known launch. In the ordinary Hilbert realization, with site projector $P_y$, port projector $P_{x,r}$ and tick $U_H$, this is the operator identity

$$P_x U_H P_{x-\Delta_r}=P_{x,r} U_H.$$

It holds on every input, including a coherent superposition. It justifies implementing a sharp block record with two adjacent full position readings, without a separate rail sensor. **It does not permit a penultimate rail read.** From $(0,R)$ the zero-character three-tick record $(1,R)$ retains RLR and LRR. They meet at well zero on different incoming rails with the same sign. The specified branch has probability $4/8$; also recording the penultimate rail gives $2/8$ on pooling those two records. The unwanted record changes a measurable later probability. [Lean proof of the two-well predicate](lean/TwoWellTranscript.lean)

Fix a complete sequence $w$ of sharp block outcomes, including any clock choices determined by earlier outcomes. Along that branch the complete set of allowed paths is one position product event. Split the paths at each identified port. The known incoming rail fixes the next sign convention, and the known starting well fixes every next departure gain. Each prefix can be followed by every word in its next block, with multiplicities preserved. The signed-residue multiset of the whole branch is therefore the convolution of its block multisets. Both its cardinality and its evaluation at a character multiply, including when a signed sum cancels. Denote the normalized one-block probabilities for count and each folded label by $p_i(w_j\mid w_{<j})$ and their initial weights by $a_i$. This proves

$$P(w)=\sum_i a_i\prod_{j=1}^{|w|}p_i(w_j\mid w_{<j}).$$

For each component these sharp records at a chosen clock sum to one by fair path continuation or normalized Hadamard propagation. Treat disjoint, actually registered records as ordinary exclusive outcomes whose probabilities add. Summing the displayed formula over a stopped tree then gives the probability of any pooled flag. A branch need not have the same duration as another branch. The equation concerns measured records or matched product apertures. A device writing an extra internal record or injecting a new sheet on a read needs its own comparison. At $M=3$ a specific two-block record has probabilities $12/128$ and $6/128$ for a retained and a refreshed localized sheet, respectively. [Convolution identity in Lean](lean/TwoWellTranscript.lean) · [Full exact two-record panels](results/native_multiscale_selector.json)

## Selection over the classified family

Conditional weights after the flag $A$ are $a_i P_i(A)/P(A)$ whenever $P(A)>0$. For subsequent recorded product experiments starting at the known sharp port of each accepted transcript, the same convolution proof gives the continued law with these weights, path by path. The starting site and rail can vary. Compare each actual terminal test with its unit-character prediction from that same port and controller history. The total variation discrepancy of the pooled future records is at most the conditional nontarget fraction. This bound holds for the joint law with the accepted history if its marginal is kept fixed in the comparison. It need not bound the error of a diagnostic that multiplies raw probabilities by $M^2$. [Scaled rail diagnostic](Mixed_refinement_records.md) · [Source-dependent accuracy](Addressed_sheet_preparation.md)

The native multiscale filter gives positive uniform gaps against every competing folded label, using the unmodified tick. Add a short comparison against count. The indicator of $(-1,L)$ at tick three has mean $\frac12\sin^2(\pi/M)$ at folded unit and $1/4$ for count. These coincide only at $M=4$ among integer orders $M\ge3$. At that order the **entire** three-tick distributions coincide. At tick four the port $(0,L)$ gives respectively $5/16$ and $3/16$. Use the better of these two settings at each order. The gaps have a positive lower bound independent of $M$, since the three-tick gap tends to $1/4$ and the single exceptional order has the four-tick gap. Both settings use the same two-well instrument. [Exact count alias and finite schedules](check_native_multiscale_selector.py)

In particular fix any lower bound $w>0$ on the original unit mass $b_1$. At dyadic stage $j$ of the one-pass filter grant both decision errors at most $e_j=w\epsilon/[16(j+1)^2]$ and assign the count test error $w\epsilon/16$, for $0<\epsilon\le1/4$. Midpoint tests on independent canonical records within each component need $O(1+\log(1/(w\epsilon))+\log(j+1))$ repetitions, uniformly over the order. Each rival must pass its assigned test; the target must pass them all. Target loss is at most $3w\epsilon/16$, and total accepted wrong mass is at most $(1-b_1)w\epsilon/16$. Thus the conditional error is below $\epsilon$ and the original true-unit herald mass is at least $b_1(1-3w\epsilon/16)$. The deterministic tick bound is $O(M^{2/3}[1+\log(1/(w\epsilon))])$. The sharper localized-prior schedule exploits the number of labels in each band. For a source with $b_1=0$, an acceptance cannot supply genuine unit mass. For unknown tiny $b_1$, there is no uniform posterior guarantee from a fixed bound on false passage alone. [Multiscale schedule and bounds](Native_multiscale_selector.md)

## The early-rejection cost with persistent counting

For the particular source with count fraction $c<1$ and an otherwise localized square-coordinate sheet, the early-rejection schedule can include count economically. Add the count test in each reached layer $\ell$, with the same per-test bound $b_\ell=\epsilon/(64w_\ell^3)$ as that layer's other tests. The additional target loss is at most $\sum_\ell b_\ell<\epsilon/16$, and the square-component reach probabilities can only decrease. A counting launch reaches layer $\ell$ with probability at most $(\epsilon/64)^\ell$ when that test is run first in every layer. Its mean total time is bounded by the sum of these factors times the layer costs $O(2^{2\ell/3}[1+\log(1/\epsilon)+\log(\ell+1)])$. Hence the mean remains $O(1+\log(1/\epsilon))$ per original launch. Its count false passage is at most $(\epsilon/64)^{J+1}$ through all $J+1$ layers. On the original ensemble genuine unit weight is still only $2(1-c)/M$. When $c$ is fixed and $\epsilon\to0$, the per-launch herald probability is asymptotic to that weight. When $c$ is close to one at finite order, include $c(\epsilon/64)^{J+1}$ explicitly in the numerator for wrong heralds.

At fixed small confidence tolerance and fixed $c<1$, this schedule needs order $M$ independent fresh launches on average through its first acceptance. With at least one physical tick per launch, its total expected serial walk-clock cost is $\Theta(M)$, since one trial has bounded mean ticks and success probability $\Theta(1/M)$. On the shrinking-action clock $\tau\asymp M^{-3/4}$ this serial cost is $\Theta(M^{1/4})$ in physical units. On the fixed-action clock $\tau\asymp M^{-2/3}$ it is $\Theta(M^{1/3})$. A vanishing preparation time conditional on a single successful classical launch does not imply vanishing serial time to obtain one. Extra sources in parallel use another physical resource. [Layer ordering and rates](Native_multiscale_selector.md) · [Release clocks](Field_on_source_and_release.md)

## What an observed herald rate could establish

Alternatively preassign all stage errors without specifying an incident unit weight. Suppose the resulting test has $P_1(A)\ge1-\tau$ and $\max_{i\ne1}P_i(A)\le\alpha<1$, including count. Its true herald rate $p=P(A)$ then constrains the unknown source through

$$
\max\{0,(p-\alpha)/(1-\alpha)\}\le b_1\le\min\{1,p/(1-\tau)\}.
$$

The left bound uses $p\le b_1+(1-b_1)\alpha$, and the right uses $p\ge b_1(1-\tau)$ for $\tau<1$. For $p>0$, the unwanted fraction among heralds is at most $\min(1,\alpha(1-p)/[(1-\alpha)p])$. In particular a measured rate well above the maximum false passage would supply evidence of available unit weight even if no lower bound on it had been assumed at design time.

For a fixed number $n$ of independent original preparations using one unchanged source and apparatus, let $k$ of them herald. An exact one-sided lower confidence bound $L$ of level $1-\rho$ is zero when $k=0$, and otherwise solves $\Pr_{\operatorname{Bin}(n,L)}(K\ge k)=\rho$. The tail is monotone in $L$; inverting the test gives the coverage bound. On its coverage event substitute $L$ for $p$ in the lower bound on $b_1$ and the upper bound on the conditional error. The upper bound on $b_1$ instead requires an upper confidence bound for $p$. At $L=0$ the procedure supplies no nontrivial purity bound. This concerns the population of future heralds under the same law. A continued sheet with one persistent sector, inspecting several candidate score tables on the validation data, or stopping that validation when a desired lower limit appears would require a different sampling argument. No physical frequencies are supplied by the numerical walk checks.

To certify unwanted fraction at most $\epsilon$ from this bound one needs $L\ge\alpha/[\alpha+(1-\alpha)\epsilon]$ with $L>0$. The bound is sharp from the rate and these nuisance constraints alone. For $p\ge\alpha$ one can take unit acceptance one and rival acceptance $\alpha$. For $0<p\le\alpha$ one can instead take zero unit mass and rival acceptance $p$. An observed rate does not independently validate the nuisance bounds or the detector model.

These measurements operationally select the ordinary *folded* response relative to the designated cyclic unit. They allow competing initial laws to keep distinct yields. They neither assign the initial coefficients nor break the simultaneous relabeling of preparation, cyclic representation and readout. A primitive warrant for the stationary score or for the apparatus that realizes its product events remains open. [Absolute embedding equivalence](Native_preparations_and_probability_embeddings.md)

## Validating a source when serial launches stop on a herald

The serial waiting cost above ends at the first herald. An experimenter can also choose a positive integer $k$ in advance and record the number $T_k$ of original launches needed for the $k$th herald. Count every miss. Assume independent fresh launches from one unchanged source, using the same apparatus and full within-launch decision rule. Write $p=P(A)$ for the original herald rate and $S_t$ for the number of heralds in the first $t$ launches. The events $T_k\le t$ and $S_t\ge k$ coincide for every sequence of flags. At a completed time $t$, define the one-sided lower limit $L_k(t)$ as the solution of
$$
 \sum_{j=k}^{t}{t\choose j}L_k(t)^j[1-L_k(t)]^{t-j}=\rho.
$$
Under the stated launch model the sum at $p$ is the cumulative probability of $T_k\le t$. It increases with $p$ and with $t$. The times for which $L_k(t)>p$ therefore form an initial segment of probability at most $\rho$. A prespecified deadline can return $L=0$ whenever fewer than $k$ heralds arrive, including when $p=0$. The bound covers over the whole design. [Scholz, negative binomial confidence bounds, §3](https://faculty.washington.edu/fscholz/DATAFILES/ConfidenceBounds.pdf)

On the coverage event the original unit mass and the probability of a **genuine unit herald per original launch** are each at least $\max(0,(L-\alpha)/(1-\alpha))$, where $0\le\alpha<1$ bounds each rival's herald probability. Indeed if $u$ is the genuine herald mass, then $u\le b_1$ and the false mass $p-u\le\alpha(1-b_1)\le\alpha(1-u)$. When $L>0$ the wrong fraction among heralds is at most $\min(1,\alpha(1-L)/[(1-\alpha)L])$.

The launch that triggers release has the ordinary herald's component distribution for every feasible waiting time. For component prior $b_i$ and herald probability $h_i$, independence gives
$$
 \Pr(I_{T_k}=i,T_k=t)=\Pr(S_{t-1}=k-1)b_i h_i,\qquad
 \Pr(I_{T_k}=i\mid T_k=t)=b_i h_i/p .
$$
Waiting gives information about the unknown rate. At a fixed source law and given a herald, waiting supplies no further evidence of that particular launch's component. This assertion also conditions on meeting a deadline measured **in launches**. Conditioning on the internal winning transcript or selecting by its physical run time can reveal additional information.

| Illustrative design | What the timing alone certifies |
|---|---|
| 95% one-sided confidence, rival passage at most 1%, desired purity at least 90% | The required rate lower limit is $10/109$. |
| Stop at the first herald | $L_1(t)=1-(1-\rho)^{1/t}\le\rho=0.05$. Even an immediate herald leaves the wrong-fraction upper bound at $19/99$. |
| Preassign two heralds and the second arrives on launch four | At $p=10/109$, the probability of two or more flags by four is 0.044536. The lower limit is approximately 0.09761146, giving a wrong-fraction upper bound below 9.34%. |
| The second herald arrives on launch five | At the same threshold the tail is 0.069761. Launch four is the last arrival time certifying 90% purity in this design. |

These are prospective numbers under the stipulated false-passage bound. Retaining only successful runs can invalidate the confidence statement. With $p=1/25$, $\rho=1/20$, and a one-launch deadline for the first herald, every completed run reports $L>p$. Such runs have probability $1/25$ across all launches. Choosing the target using the data also changes coverage. At the same $p,\rho$, report the first-herald bound if launch one succeeds and otherwise take the second-herald bound. Exact enumeration gives a probability of overstating $p$ of **7.6621%**, exceeding the nominal 5%. A proof in Lean checks the flag identity at all list lengths and the four-versus-five boundary. The exact checker tests the deadline, the target switch and the component law at each stopping time. [Checker](check_stopped_heralds.py) · [Exact outputs](results/stopped_heralds.json) · [Formal check](lean/StoppedHeralds.lean)
