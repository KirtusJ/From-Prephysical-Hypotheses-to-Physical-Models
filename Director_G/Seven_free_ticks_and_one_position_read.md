# Seven free ticks and one position read select a probability power

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) and the Codex workers.

Launch a walker at one well on the right rail, let it run for seven real Hadamard ticks, then record its well. A single weighted sum of well frequencies has ordinary expectation zero. Its expectation is strictly positive under every other finite nonnegative power in either of two readout families and also under full path counting. The detector may choose a new power and a new family on every launch. This removes the persistence premise of the earlier two-block test. Very large powers can approach zero, which limits what finite precision can establish. [Two successive five-tick position tests](Two_five_tick_records_and_the_probability_power.md)

## The measured wells and the candidate laws

Apply \(H(r,l)=(r+l,r-l)/\sqrt2\), then move the right rail one site right and the left rail one site left. Use the line or an apparatus that realizes the same paths without wraparound. No mask, intermediate write, sign actuator or rail read enters the experiment. The integer amplitudes in the table have a common denominator \(\sqrt{128}\). Each classically counted direction word has weight \(1/128\). The usual coined walk obtains position probability from the sum of squared orthogonal rail amplitudes. A spatially resolved walk has been implemented with trapped atoms; the three-step experimental counts analyzed in this program are a different protocol and supply no seven-step data. [Konno's coined-walk model](https://arxiv.org/abs/quant-ph/0206103) · [Robens et al., single-atom quantum walks](https://doi.org/10.1103/PhysRevX.5.011003) · [The three-step cesium record](Three_step_site_weights_in_cesium.md)

| Well \(x\) | \(R_x\) | \(L_x\) | \(m_x=R_x^2+L_x^2\) | Number of unsigned paths |
|---:|---:|---:|---:|---:|
| \(-7\) | 0 | 1 | 1 | 1 |
| \(-5\) | −1 | 4 | 17 | 7 |
| \(-3\) | −2 | −1 | 5 | 21 |
| \(-1\) | 3 | 0 | 9 | 35 |
| \(+1\) | −4 | −1 | 17 | 35 |
| \(+3\) | 5 | 4 | 41 | 21 |
| \(+5\) | 6 | 1 | 37 | 7 |
| \(+7\) | 1 | 0 | 1 | 1 |

For each launch assume one of the following rules for the complete position survey. A site-power rule samples proportionally to \(m_x^q\). A rail-cell-power rule samples proportionally to \((R_x^2)^q+(L_x^2)^q\), reporting the well. Full path counting gives the last column. The exponent \(q\) is common to the scored cells within a launch and can be any finite \(q\ge0\). At zero, each positive cell counts once and a dark cell scores zero. The choices may have any joint distribution, including a dependence between exponent and rule. Both power families coincide with the ordinary position law at \(q=1\). Exponents act on the squared kinematic masses in this construction.

## One score from the same histogram

Let \(P_x\) denote the population probability of the indicated well. Write \(k_m=m\log m\) with the natural logarithm, and set

\[
\begin{split}
\Delta &= k_5k_{16}-k_{17}k_4,\\
b&=k_9(k_{16}-k_{17})/\Delta,\qquad
c=k_9(k_5-k_4)/\Delta,\qquad a=9-5b-17c.
\end{split}
\]

The fixed observable is

\[
W=aP_{-7}+bP_{-3}+cP_{-5}-P_{-1}
+2(P_{+1}-P_{-5}).
\]

Here \(a\simeq3.826974733,\ b\simeq-0.836548414,\ c\simeq0.550339255\). Use the defining equations or verified coefficient intervals if evaluating a near-zero score. Every reported well, including the three wells with zero coefficient, is part of the normalization. The coefficients and signed scores need not be probabilities.

The final difference in \(W\) vanishes in both power models at **every** exponent: the two sites have identical multisets of squared rail amplitudes, \(\{1,16\}\). It gives \(28/128\) under counting. After omitting this difference, the unnormalized numerators in the site and rail families are respectively

\[
F(q)=a+b5^q+c17^q-9^q,\qquad
G(q)=a+b+c+b4^q+c16^q-9^q.
\]

The defining equations ensure \(F(1)=G(1)=0\) and \(F'(1)=G'(1)=0\). Indeed \(5b+17c+a=9\), \(bk_5+ck_{17}=k_9\) and \(bk_4+ck_{16}=k_9\). Both curves are strictly positive off one. For the first, \(F'(q)/(17^q\log17)\) is the positive constant \(c\) plus \(b(\log5/\log17)(5/17)^q\) and \(-(\log9/\log17)(9/17)^q\). The latter two terms are strictly increasing because \(b<0\). This derivative ratio crosses zero once. Replacing 5 and 17 by 4 and 16 yields the same argument for \(G\). Dividing the numerators by the corresponding positive normalization preserves their signs. At zero the numerators are \(a+b+c-1\) and \(a+2b+2c-1\), both positive.

For counting, the numerator of \(128W\) is \(30+16b-10c>4\), since \(-1<b<0\) and \(0<c<1\). For reproducible signs, in order \(4,5,9,16,17\), the values \(k_m\) lie strictly between \(5.545,8.047,19.775,44.361,48.164\) and these respective lower endpoints plus \(0.001\). The checker encloses every logarithm with rational arithmetic using \(z=(m-1)/(m+1)\) and

\[
0\le \log m-2\sum_{j=0}^{99}\frac{z^{2j+1}}{2j+1}
\le\frac{2z^{201}}{201(1-z^2)} .
\]

The identity follows by integrating the geometric series for \(2/(1-z^2)\). The displayed upper error replaces every remaining denominator by 201. Interval operations verify coefficient signs and positivity of \(\Delta\). Hence a population score \(W=0\) gives zero mass to counting and to every \(q\ne1\) for any probability mixture over the stated laws. This uses nonnegativity and the strict pointwise equality condition; no repetition with a persistent detector or a separately prepared probability reference is required.

## What an approximate zero and a mixed readout permit

An upper population bound \(W\le\epsilon\) bounds the counting fraction by \(128\epsilon/(30+16b-10c)\). For a specified finite cap \(Q\) and separation \(\delta>0\), take the smaller normalized score over the two families on \(0\le q\le Q,\ |q-1|\ge\delta\). When this set is nonempty its minimum is positive by continuity; dividing \(\epsilon\) by it bounds the corresponding population weight. There is **no** positive uniform margin over the entire tail. For \(q\ge0\), positivity and the signs of the dropped terms bound the normalized site score by \((a+c\,17^q)/41^q\) and the normalized rail score by \((a+b+c+c\,16^q)/36^q\). Both tend to zero. The two limiting detector distributions concentrate at \(+3\) and \(+5\), respectively, whose coefficients are zero. If a deterministic maximum-weight read is admitted as an additional rule, it passes this one contrast. The full histogram contains other information about those wells.

The choice between site and rail granularity above is one choice for the whole detector at this launch. Permitting site-specific granularity breaks positivity. For example, with \(q=2\) pool at every well except \(+1\). Its mass changes from \(17^2=289\) to \(16^2+1=257\), reducing the score numerator by 64. The new numerator is \(20b+272c-136<0\), as the same interval calculation verifies. Its normalized value is approximately \(-0.00082038\). Mixing this instrument with positive-score path counting can give zero with no ordinary exponent. A score of zero is a proposed experimental comparison on the predeclared detector family. Unknown position efficiencies, unmeasured losses, a different coin or setting-dependent reads need measured bounds or an expanded model. This result alone supplies no probability law for other preparations, no external phase embedding and no physical origin of the walk.

The [checker](check_seven_tick_position_score.py) independently enumerates all 128 signed and unsigned paths, compares them with the rail recurrence, constructs the log certificates and records interval scores for both rules, full counting and the mixed-granularity counterexample. [Exact results](results/seven_tick_position_score.json) · [Lean check of terminal numerators and cancellation](lean/SevenTickPositionScore.lean) · [Earlier switched-ring tests](Forward_staircase_and_spatial_probability.md)
