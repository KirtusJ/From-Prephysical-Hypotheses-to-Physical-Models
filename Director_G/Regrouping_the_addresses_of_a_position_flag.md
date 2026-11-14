# Measuring which paths a detector pools across two launches

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Can a detector tell two preparations apart when the total probability assigned by the ordinary walk is identical? At tick 256, a choice of five shell assignments gives 32 ways to write the same binary flag mass on every input coin. One model pools the two address sectors before reading that mass. Another resolves the address and applies the same nonlinear response to its conditional mass. A pilot-controlled comparison distinguishes these models, even though they give identical singles for every one of the 32 preparations.

## Change the routing while holding the total mass fixed

Use the [balanced-address preparation](Threshold_pilot_and_adaptive_preparation.md). Its endpoint masks $A,B$ have scalar input effects $aI,bI$ with $a=0.239027918813\ldots$, $b=0.260644776272\ldots$. Write $c=(a+b)/2$ and $h=b-a$. Both addresses mark all 36 shared radii; neither marks any radius outside the union. At each of the five remaining radii (82, 158, 170, 188, 190), choose which address sets the flag. In the bit strings below, 1 assigns that radius to address zero. Each launch starts with a fresh fair address independent of the source. The conditional mass on address zero is $m_J$ for design $J$. On address one it is $2c-m_J$. The two masses average to $c$. Each shell effect is a scalar on the two input rails, so even changing the launch coin cannot change this average. Flipping the flag implements the complementary event.

Use design $J$ for the pilot and design $K$ for science. In one policy, choose the direct science flag on a pilot hit and its complement on a miss. In the comparison policy use an independent bit with the same hit frequency. Call the difference in mean science hit rates $D_{JK}$. Both policies have the same mean assigned target. The [randomized feedback protocol](What_pilot_feedback_measures.md) estimates this difference from ordered pilot and science records with both science settings sampled. Randomize designs independently of source and detector, keep both flags and every incident block, and retain bounds for unclassified outcomes. Comparing the reversed ordering $K,J$ is part of the experiment.

## Predictions for a detector with a persistent threshold

Use the [single-gap response](Hidden_threshold_between_calibrated_masses.md) with $U$ uniform on $(0,1)$. For $a<s<b$, the direct hit probability is $g_U(s)=a+h\,\mathbf1\{U<(s-a)/h\}$. The upper-half response is complementary. Elsewhere the probabilities are ordinary. Here all address-conditioned direct masses lie between 0.2116195 and 0.2880532, within the lower half. A pooled read of any design has conditional rate $g_U(c)$. A resolved read has rate $k_J(U)=[g_U(m_J)+g_U(2c-m_J)]/2$. This latter formula requires an unbiased address resolution on each launch. For the joint predictions below, any address draws are independent across launches and the science hit has the stipulated conditional mean after the pilot.

Put $t_J=(1/2-|m_J-c|/h)_+$. Except at finitely many null thresholds, the resolved rate is

$$k_J(U)-c=\tfrac h2[\mathbf1\{U<t_J\}-\mathbf1\{U>1-t_J\}].$$

The pooled rate uses the same expression with $t=1/2$. Both have unconditional mean $c$. The two lower tails are nested across designs, as are the two upper tails. With a shared $U$ the difference in policy values is twice the covariance. Thus the always-resolved model predicts $D_{JK}=h^2\min(t_J,t_K)$, while the always-pooled model gives $h^2/2=0.000233644263\ldots$ throughout. An ordinary calibrated reader with fresh independent noise gives zero throughout.

| Split design (address exchanges give the same prediction) | Resolved $D_{JJ}$ per incident block |
|---|---:|
| 00100 | 0.000158484114 |
| 00101 | 0.000156749790 |
| 00110 | 0.000148084415 |
| 00111 | 0.000146350091 |
| Original endpoint split 01011 and 23 other zero-gain designs | 0 |

The eight positive assignments form four pairs. Their four representative rows have rank four because the matrix of pairwise minima of the distinct positive diagonals factors as cumulative sums of four positive increments. Any stable pooled model whose response depends only on the common $c$ and a shared type gives identical rows and rank at most one, even with a type distribution other than the uniform-threshold example, under the conditional-mean and common-population assumptions.

## Separating threshold retention from address resolution

Allow the pilot and science modes to fluctuate or persist together. Write 0 for pooling, 1 for resolving, and $w_{ij}$ for the probability that the two modes are $i,j$ **and** the science launch retains the pilot threshold. On every other block the science threshold is drawn afresh and independently. The modes and retain/redraw decision may be correlated with one another but are jointly independent of the threshold, settings and measurement noise. All launches have independent address blanks and the same calibrated endpoints. In every mode each reading still has marginal $c$. Conditioning on modes and retention gives
$$
D_{JK}/h^2=w_{00}/2+w_{10}t_J+w_{01}t_K+w_{11}\min(t_J,t_K).
$$
Redrawn blocks contribute zero. Two designs suffice to recover all four weights: an endpoint design of tail 0 and any design with tail $q>0$. Set $f_{uv}=D_{JK}/h^2$ for the ordered tails $u,v\in\{0,q\}$. Then
$$
w_{00}=2f_{00},\quad w_{10}=(f_{q0}-f_{00})/q,\quad
w_{01}=(f_{0q}-f_{00})/q,\quad w_{11}=(f_{qq}-f_{0q}-f_{q0}+f_{00})/q.
$$
Negative inferred weights, a sum above one or a mismatch on the remaining designs contradict this restricted model at the population level. The sum estimates threshold retention **within this model**. The off-diagonal inversion divides rate differences by $h^2q$, amplifying uncertainty when this product is small.

Two controls delimit the inference. A shared address bit can fake full retention on the endpoint design: draw one fair address for both launches, use the corresponding honest endpoint rate $a$ or $b$ twice, and use independent hit draws. Both thresholds can be fresh. Nevertheless $D=2\operatorname{Var}(a\ \text{or}\ b)=h^2/2$. Conversely, divide the unit interval at all thresholds used by this finite family, preserve the interval label, and redraw $U$ independently *inside that interval* on the second launch. Every response on this menu then agrees with retaining $U$ exactly, while the probability of equality of the two continuous thresholds is zero. The effective memory concerns what the tested records can resolve. A detector that stores the pilot design and hit can also reproduce the observed conditional science tables invasively.

## A reversible measurement on the same masks

A separate coherence control writes the address-conditioned flag, allows a possible record to form, unwrites the same XOR flag without undoing any inaccessible copy, and applies a Hadamard to the address. Keep every position and read the minus address port. Under the ordinary readout its mass is zero for a coherent round trip. If the environment copies the flag, the two address arms interfere precisely at sites where the flags agree. At a differing site the orthogonal environmental records leave half the address mass in the minus port. All 32 designs have the same symmetric-difference mass $d=0.076433511304\ldots$, giving **$d/2=0.038216755652\ldots$**. A complete copy of the address gives $1/2$. A relative sign reversal before the final Hadamard exchanges bright and dark ports. A reference using the same mask in both address arms gives $d=0$ and checks which component of the loss of contrast depends on flag disagreement. These predictions require matched gates and readout across the controls. Phase noise or a copied flag followed by coherent erasure changes their interpretation. [Englert on record distinguishability and visibility](https://doi.org/10.1103/PhysRevLett.77.2154) · [Measured quantum-erasure controls](https://arxiv.org/abs/quant-ph/9908072)

The coherent audit and the gain matrix answer different questions. A device can pass the coherent audit and still score the declared address branches separately in a destructive read. Conversely, an inaccessible address copy can suppress the fringe even if the final instrument pools the flag before applying its scalar response. Transferring either conclusion between experiments requires independent evidence about the shared physical instrument. The program has measured neither of these walk panels.

The [exact checker](check_regrouped_address_masks.py) propagates both input rails, integrates each constant-response interval, checks the 1,024 ordered resolved gains against the nested-tail formula, and reconstructs known mixtures including zero retention and each of the four pure retained cases. It sums the unwrite amplitudes by environmental label at each site for all three coherence controls. The [result file](results/regrouped_address_masks.json) retains all assignments, nulls, both address masses, all gains and exact witnesses. From the root run `python -B Director_G/check_regrouped_address_masks.py regrouped-replay.json` with a fresh output name.
