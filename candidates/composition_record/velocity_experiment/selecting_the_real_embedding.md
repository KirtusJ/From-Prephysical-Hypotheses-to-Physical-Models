# Three recorded words separate the real embeddings for a calibrated gate sign

The first write in the addressed-real circuit leaves an ambiguity between the field embedding and the scoring exponent. Its complete record resolves that ambiguity within the following model. Each launch has one real embedding of $\mathbb Q(\sqrt2)$: the specified one or its conjugate $\sigma:\sqrt2\mapsto-\sqrt2$. A mode can score the complete word with one exponent or score separately at each write using exponents chosen from the preceding history. An ordinary complete table forces the specified embedding on almost all launches. The sign of the odd-address $H$ relative to the even-address $X$ must be independently calibrated. Reversing that sign in the specified embedding gives the conjugate embedding's word probabilities, so records alone cannot resolve an unknown gate sign. This is a calculation on a proposed experiment. [Circuit and root-level ambiguity](addressed_embedding.md) · [Identification of powers at reached writes](test_each_write.md)

## A conjugate maximum on an informative branch

Use the synchronized position codes $(y_3,y_6,y_9)$ from the addressed circuit. At the two-code prefix $(2,3)$ the three occupied final words have specified squared weights

| Word | Six recorded bits, most significant first | Weight before division by 512 |
| --- | --- | ---: |
| $(2,3,1)$ | `011110` | $l=86-60\sqrt2$ |
| $(2,3,3)$ | `111110` | $m=18-8\sqrt2$ |
| $(2,3,0)$ | `001110` | $h=40+4\sqrt2$ |

Here $0<l<m<h$. The conjugated value $l'=86+60\sqrt2$ is the **unique largest leaf weight** among all 27 positive words. The path $(2,3,1)$ also chooses the unique largest conjugate child at *each* of the three writes. At the root the three positive **conjugate** child weights, in the table's units, are $192-128\sqrt2,256+128\sqrt2,64$ in code order 1, 2, 3. At prefix $(2)$ the corresponding conjugate child weights are $64+32\sqrt2,48+32\sqrt2,144+64\sqrt2$ in code order 0, 1, 3. The final choice compares $l'$ with $m'=18+8\sqrt2$ and $h'=40-4\sqrt2$. Both embeddings have the same occupied support. [Exact signed paths, conditional maxima and field inequalities](check_embedding_selection.py)

Let $P_l,P_m,P_h$ be the **unconditional** launch probabilities of these three words. Define

$$
\theta=\frac{\log(m/l)}{\log(h/l)},\quad
A=\frac{1-\theta}{l},\quad M=\frac1m,\quad B=\frac{\theta}{h},
\qquad J=A P_l-M P_m+B P_h .
$$

The observed mean is computed by assigning $+A,-M,+B$ on the three words and zero everywhere else. The ordinary value is zero.

**Specified embedding.** Under complete-word scoring, the contribution to $J$ at a finite exponent $q$ equals a positive normalizer times
$(1-\theta)l^{q-1}+\theta h^{q-1}-m^{q-1}$. This is nonnegative by weighted arithmetic–geometric mean. Under sequential scoring the same expression applies at the parent conditional on the visit and the final exponent; multiply by the probability of that visit and divide by its local power sum. If the visit never occurs the contribution is zero. For $q=\infty$, a complete-word maximum that reaches this prefix or a sequential final maximum here can only select a highest-weight sibling; its score is positive. This proves nonnegativity for either scoring order and every mixture of them.

**Conjugate embedding.** For every $0\le q\le\infty$ the largest positive cell is at least as likely as each other cell. The global maximum word thus has probability at least $1/27$ under complete-word powers. Under sequential powers, the probability of each greedy step, given that history and its drawn exponent, is at least $1/3$. Hence $P_l\ge1/27$ for both classes, even if sequential exponents change with every history. In both classes $P_m\le P_l$ since these words are siblings and $m'<l'$. Mixtures preserve these inequalities. At the relevant choices all maxima are unique; tie breaking elsewhere cannot move the largest word in these bounds. In the limit from positive exponents to zero, positive cells are equiprobable and dark cells keep probability zero. The numerical bound below uses this convention. Assigning equal mass to all 64 complete words at zero power would instead give $J=(A-M+B)/64\simeq0.00493$.

The two field inequalities $m^2<lh$ and $m>2l$ imply $\theta<1/2$ and $A>1/(2l)>M$. Therefore for every conjugate mode

$$
J\ge(A-M)P_l\ge(A-M)/27
>\frac{1/(2l)-1/m}{27}>\frac1{100}.
$$

Every step after the logarithmic threshold can be checked in ordered $\mathbb Q(\sqrt2)$. The [standard-library checker](check_embedding_selection.py) compares the amplitude recurrence with an independent enumeration of signed paths and verifies the strict rational lower bound; run `python -I -B check_embedding_selection.py` in this folder.

The [Lean 4.19 certificate](../../../Director_G/lean/AddressedCoinEmbedding.lean) propagates the two circuits obtained by keeping or reversing the sign of every $H$. It verifies conjugation of all 64 word weights, the occupied support, the maximizing conjugate history and the two field comparisons. Its finite enumerations use Lean’s native evaluator. Changing only the addressed $H$ gives the same weights as changing every $H$, because each of the other two Hadamards in the flight acts at every address and its sign is global. This phase argument, the probability bound $P_l\ge 1/27$, the arithmetic–geometric mean argument, the resulting gap for $J$ and the sampling bounds are derived in prose. The Python checker also verifies the field comparisons used for the numerical gaps.

## Consequences and limits

For a launch mixture with conjugate fraction $\gamma$, $J\ge\gamma(A-M)/27$. Thus **exact ordinary word probabilities force $\gamma=0$**. Once this is established, the sibling-score argument on the remaining single embedding applies to the 13 reached parents with three different positive child weights. With the appropriate full set of terminal and preceding scores, it forces exponent one on each realized sequential decision and on each complete-word mode. The single statistic $J$ establishes the embedding conclusion and by itself tests powers only at the selected parent. Exponents on branches that a sequential mode never reaches remain unobservable.

For finite samples, a valid upper confidence limit $U_J$ yields $\gamma\le\min(1,27U_J/(A-M))$, subject to the scoring, sampling and reporting assumptions. A negative upper confidence limit challenges the model on the confidence event. For $N$ independent launches, a one-sided Hoeffding limit adds $(M+\max(A,B))\sqrt{\log(1/\alpha)/(2N)}$ to the empirical mean. Allow for word-dependent assignment and missing reports. [Reporter calibration](reporter_calibration.md)

The [word-table analyzer](analyze_write_powers.py) constructs the `prefix:23` score from **conditional child weights** $l/P,m/P,h/P$, where $P=l+m+h=144-64\sqrt2=8m$. It still averages contributions over every incident launch. Thus its estimate is for $J_{23}=P J$. Its coefficients are approximately $24.31583,-8,0.56061$. The field comparison $P>43l$ gives $(PA-8)/27>[P/(2l)-8]/27>1/2$. Consequently a joint upper confidence limit $U_{23}$ for the analyzer's score gives the conservative bound $\gamma\le\min(1,2U_{23})$. This scaling requires no estimate of the observed visit probability.

The exact power conclusions do not follow from a small nonzero upper bound on $\gamma$. To reuse the finite-sample inequalities for specified-embedding powers, let $G$ be an upper bound on $\gamma$ and $U_s$ a simultaneous upper bound on any earlier or terminal score $s$. Conjugate launches can contribute as little as $-G\max_w|s(w)|$. Replace $U_s$ by $U_s+G\max_w|s(w)|$ when bounding the specified-embedding contribution per original launch. Then use the signed correction for nonordinary **complete-word** modes before interpreting earlier scores. Confidence limits for rare visited prefixes remain incidence weighted. [Finite-sample corrections](test_each_write.md#what-finite-counts-can-certify)

The comparison assumes a fixed embedding within a launch, nonnegative powers on the occupied support, and a common prescribed normalized state update at each actual branch within its embedding. The exponent may be redrawn before each next outcome and may depend on the entire past. Negative powers, history-dependent embedding switches, unverified relative phases, and arbitrary outcome-reporting maps fall outside the result. The selection is conditional on this experimental model and supplies no claim that an ontological derivation has taken place.
