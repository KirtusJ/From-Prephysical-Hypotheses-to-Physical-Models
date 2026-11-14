# Three words distinguish ordinary scoring in one nine-tick circuit

The predicted increase of $1/8$ in outer displacement-sign agreement is compatible with a nonordinary probability exponent near 4.665. Three entries from the same full record table give a stronger test. Within the two response models below, one signed count average vanishes precisely at the ordinary exponent, even if the instrument draws a different exponent and scoring order on each launch. This is a prediction for a proposed circuit; the numerical weights come from its two independently computed ideal tables. [Circuit generator and signed-path replay](generate.py) · [Outer-sign measurement](phase_comparison.md)

## A second exponent gives the same outer-sign result

For each sharp source and pulse arm, let $n_w/512$ be the ordinary squared mass of chronological position word $w$. A terminal power model assigns probability $n_w^q/Z(q)$, where $Z(q)=\sum_w n_w^q$ within that same arm. Let $\Delta(q)$ be the opposite-pulse minus equal-pulse fraction of launches with matching outer displacement signs, with the declared equal phase-arm weights. The two sharp sources give identical contrasts. The full tables yield

| $q$ | $\Delta(q)$ |
| --- | ---: |
| 1 | $1/8$ |
| 4 | $142669510080/871237026361>1/8$ |
| 5 | $72526324761481/670822171549928<1/8$ |

Continuity gives an additional exponent in $(4,5)$; numerical bisection gives $q\simeq4.665054739$. A mixture using $q=4$ with probability $(1/8-\Delta(5))/(\Delta(4)-\Delta(5))$ and $q=5$ otherwise also reproduces $1/8$ exactly. This equality concerns the opposite-minus-equal contrast. It does not require that either arm's entire table agree.

### An exact rational comparison for complete-word powers

In the single R, S, S arm, let \(h_n\) be the reported probability of the entire class with ideal numerator \(n\), divided by the number of words in that class. For a whole-word power \(q\) this is \(n^q/Z(q)\). The two computable scores

\[
 R=h_{77}/77+h_9/9-h_{21}/21-h_{33}/33,\qquad
 B=25h_1-10h_5+h_{25}
\]

are both nonnegative. Their numerators are \(9^{q-1}[(7/3)^{q-1}-1][(11/3)^{q-1}-1]\) and \((5^q-5)^2\), respectively. Both vanish at one. The four-level product uses \(77\cdot9=21\cdot33\). The first score stays positive at the maximum selector, and the second stays positive at the minimum selector. Uniformity within finite-\(q\) mass classes follows from the model; for an extreme tie, averaging over the complete class makes the scores insensitive to its tie convention. Thus \(R+B=0\) exposes \(q=1\) in any mixture of complete-word powers, even including both infinite endpoints. These rational scores apply when the reader powers complete-word masses before normalization. [Exact multiplicities, factorization and mixtures](check_joint_power.py)

## A comparison at one common prefix

Use the R source and apply $S$ at each intermediate exact site write. Denote the three saved position codes by $(y_3,y_6,y_9)$. Under prefix $(1,2)$ the four terminal columns are

| $y_9$ | Qiskit bit string | Integer squared weight $n_w$ |
| ---: | --- | ---: |
| 0 | `001001` | 49 |
| 1 | `011001` | 29 |
| 2 | `101001` | 13 |
| 3 | `111001` | 77 |

Let $P_j$ be the probability per **original launch** of prefix $(1,2)$ and $y_9=j$. Set

$$
\theta=\frac{\log(29/13)}{\log(77/13)},\qquad
L=\frac{1-\theta}{13}P_2+\frac{\theta}{77}P_3-\frac{1}{29}P_1 .
$$

The identity $29=13^{1-\theta}77^\theta$ gives a nonnegative quantity for every real finite $q$:

$$
D(q)=(1-\theta)13^{q-1}+\theta77^{q-1}-29^{q-1}\ge 0.
$$

This is weighted arithmetic–geometric mean; it is strict unless $q=1$. Two different physical scoring rules give this same numerator.

* **Score the complete word once.** The mode's contribution to $L$ is $D(q)/Z(q)$, strictly positive for all finite $q\ne1$.
* **Score separately at each write.** At each reached prefix, raise its four ordinary conditional site weights to $q$ and normalize over those four possibilities. Assume the normalized post-write state at the actual site is the stipulated projected coin, and keep the prescribed dynamics thereafter. The mode's contribution is $P_q(y_3=1,y_6=2)D(q)/(49^q+29^q+13^q+77^q)$. The prefix has positive probability for all finite $q$ in this model. No equality between this denominator and the whole-word normalizer is needed.

Thus a mixture of the two scoring orders, with an arbitrary common exponent distribution or an exponent correlated with the order, cannot give $L=0$ unless the exponent is one almost surely on these launches. This conclusion assumes one exponent persists over the three writes in a sequential mode. The uniform-on-positive rule at $q=0$ also has positive $L$. At $q=\infty$, terminal maximum scoring returns the unique word of weight 77. Sequential maximum scoring follows the same word: first-stage weights are $(64,320,64,64)$, next-stage weights after code 1 are $(40,40,168,72)$, and the last split is shown above. Both rules give $L=\theta/77>0$. These endpoints cause no additional zero for \(0\le q\le+\infty\). The three-word test is also strictly positive at each finite negative exponent. A pure minimum selector can avoid this prefix; the all-parent test below handles that endpoint.

**What the counts measure.** Give a launch the coefficient specified in $L$ when it reports one of the three scored words and zero otherwise. Three word counters and the total launch count suffice. For independent launches the per-shot range has width $r=1/29+\max((1-\theta)/13,\theta/77)$. A one-sided confidence bound on $L$ is $\widehat L\pm r\sqrt{\log(1/\alpha)/(2N)}$, choosing the sign for the intended upper or lower limit. Finite counts cannot force exact equality. On any closed exponent range separated from one, lower bounds on the two continuous per-mode gaps give an upper bound on its fraction from a measured upper limit. Word-dependent reporting errors or losses can change the contrast, and scoring individual terminal rails before summing over those rails is another model. Validate or bound the calibrated word probabilities for this observable. [Reporting and missing-word controls](reporter_calibration.md) · [Hoeffding bound](https://doi.org/10.1080/01621459.1963.10500830)

## An exact limitation if the exponent changes between writes

If a sequential model redraws exponents by clock, the comparison constrains the **last** exponent on the reached prefix, weighted by its chance of being reached. There is a counterexample even to identification from the entire 64-word table. The first site write has three light cells of weight one and one cell of weight five after dropping a common factor of 64. The other sharp launch has the same weights in permuted order. Independently draw the first exponent $1/2$ with probability

$$
\pi=\frac{1/8-1/28}{1/(3+\sqrt5)-1/28}\simeq0.575040
$$

and exponent $2$ otherwise. Each light cell then has exactly $(1-\pi)/28+\pi/(3+\sqrt5)=1/8$ probability, and the heavy cell has $5/8$. At the second and third writes use exponent one and the stipulated conditional states. Every complete word in every source and phase arm now has the ordinary probability, although no launch used exponent one at its first write. A persistent response exponent and a calibrated state update are substantive assumptions when interpreting the test.
