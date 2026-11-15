# Four more ticks test the probabilities of the recorded flight

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

After the science flight, copy its final well and rail into a blank register. Keep the earlier science labels, let the **same walker** take four more ordinary ticks and then read its position together with the stored labels. Each old directed mode now has a five-site reference distribution of its own. The relative rates of those five sites test the probability weighting on that actual science setting, even when the weighting changes on every other setting. This replaces the separate calibration launches of the [five-tick reference](From_five_forward_ticks_to_a_coherent_position_read.md) with a coherent copy and a longer terminal experiment. The reference selects the ordinary exponent within the readout family below. Agreement by an apparatus that separately normalizes the science and reference outcomes has a different meaning.

## The copied mode and its five sites

Use \(L\ge5\) wells with the reflecting Hadamard shift. An outward proposal at a wall holds for one tick and reverses the rail with sign \(+1\). Let \(i\) include all retained science labels, the final well \(x\) and its directed rail \(r\). A reversible copy sends a sharp input mode and blank pointer to that mode and its named pointer value. Distinct labels previously recorded remain isolated. If several microscopic histories have reached the same \(i\), first add their amplitudes coherently as prescribed by the science instrument. Write \(\xi_i\) for its remaining environment vector and \(h_i=\|\xi_i\|^2\), normalized over the full science bank. The operation can also act on a purification of a mixed state. It need not copy any private environment state. It must preserve the orthogonality and identity of the old labels, give the prescribed forward propagation in every sector, and count every incident launch.

From an old entry \(i\), let \(j=-4,-2,0,2,4\) denote final displacement on the unfolded line relative to the stored travel direction \(r=\pm1\). To decode the final physical well, reduce \(x+rj\) modulo \(2L\) to \(a\in\{0,\ldots,2L-1\}\), and take \(\min(a,2L-1-a)\). The five wells are distinct because \(2L>8\) and the two lifts of any well have opposite parity. For paths to the same lifted endpoint at this depth the signs from crossing a reflecting seam agree up to the endpoint rail gauge. Each crossing in one direction followed by its reverse cancels, and different windings require endpoints at least \(2L\) apart in the lift. This reduces the folded position table to the line table even at the walls. Reversing the incoming rail reflects the line site weights. [Signed unfolding of the reflecting walk](Reflecting_wells_and_the_classical_limits_of_a_walk.md)

| Displacement \(j\) along the old rail | −4 | −2 | 0 | +2 | +4 |
|---|---:|---:|---:|---:|---:|
| Right-rail line launch, signed final \(R,L\) amplitudes in quarters | \(0,-1\) | \(1,-1\) | \(-1,1\) | \(3,1\) | \(1,0\) |
| Squared site mass numerator \(m_j\) | 1 | 2 | 2 | 10 | 1 |
| Unsigned direction words | 1 | 4 | 6 | 4 | 1 |

The projected block for output \((i,j)\) has squared norm \(h_i m_j/16\). The old copy prevents paths from different old modes from interfering. The final rails at a single site are **pooled before scoring**. Thus this is a position read at the final clock, with access to the old rail in the saved register. A four-step discrete walk has been performed with state-dependent transport of cesium atoms and site-resolved endpoint imaging. Implementing the coherent old-mode copy and the joint read remains an additional requirement. [Robens et al., experimental methods](https://doi.org/10.1103/PhysRevX.5.011003)

## Joint probabilities and an observed test

Assume one terminal read on the joint cells. For a launch of type \(q\ge0\), raise every occupied joint squared mass to the same \(q\) and normalize once. Empty cells stay empty even at \(q=0\). The powered joint table then factors as
\[
 {\Pr}_q(i,j)=T_q(h)_i\,\frac{m_j^q}{Z(q)},\qquad
 T_q(h)_i=\frac{h_i^q}{\sum_{h_k>0}h_k^q},\quad
 Z(q)=2+2\,2^q+10^q .
\]
The ambient rail field, old terminal masses and exponent may vary between launches and may be correlated. The suffix on each occupied \(i\) must still have the specified pooled table. An absorbing loss that cannot enter the four-tick continuation does not furnish a matched reference; it needs its own incident accounting and error budget.

Set \(\lambda=\log(5)/\log(10)\). Score \(j=-4,-2,+2\) by \(\lambda,-1/2,(1-\lambda)/10\) respectively, and all other offsets by zero. Let \(S\) be the incident mean. Conditional on a powered type its expectation is
\[
 s(q)=\frac{\lambda-2^{q-1}+(1-\lambda)10^{q-1}}{Z(q)} .
\]
The weighted arithmetic–geometric mean inequality makes \(s(q)\ge0\), with equality precisely at \(q=1\). The numerator uses \(1^\lambda 10^{1-\lambda}=2\). No empirical value for any single science mass \(h_i\) enters. A type choosing a maximal joint cell, under any tie rule, must give \(j=+2\) and pays \(s(\infty)=(1-\lambda)/10>0\). The largest suffix mass is unique within every old cell. This establishes selection even when maximal rules coexist with finite powers.

A fair path-counting type choosing each new direction independently and uniformly instead has mean \(b=(3\lambda/5-8/5)/16\), which is negative. It can cancel a positive powered score. Keep a second observed number \(D=\Pr(j=0)-\Pr(j=-2)\). Every powered type gives zero there, including maximal types, while fair counting gives \(1/8\). For a fair fraction \(f\), therefore, \(f=8D\) and \(S_{\rm pow}=S-fb\) is the unnormalized mean from the other launches. In particular \(D=S=0\) forces the ordinary exponent on that setting. If the science input is type-dependent this yields the population average of its ordinary kinematic tables. The assumptions fix only the suffix of the fair component. Its law on the earlier science flight may be arbitrary.

For uncertainty bounds take \(0<\epsilon<1\) and put \(s_\epsilon=\min_{q\in[0,\infty],\,|q-1|\ge\epsilon}s(q)>0\), including \(q=\infty\). Continuity at infinity follows from the unique mass ten. At most \(S_{\rm pow}/s_\epsilon\) of the original population consists of these outlying powered types. For at most \(m\) scored old labels, a remaining powered type obeys \({\rm TV}(T_q(h),h)\le\log(m)|\log q|\le-\log(m)\log(1-\epsilon)\) by the entropy derivative bound. Taking the mean, the total error in the old-label marginal against the ordinary type-averaged marginal is bounded by
\[
 \min\{1,\ f+S_{\rm pow}/s_\epsilon-(1-f)\log(m)\log(1-\epsilon)\}.
\]
The score uses data from that very marginal's joint measurement. Rates with uncertainty require compatible bounds on \(S,D\). Taking the score of each decorated instrument test on its own removes an equality of latent exponent distributions across tests. Relating those results to a bare flight without the copy or four extra ticks still requires an operational comparison. In the [three-tick cut certificate](Certifying_a_position_read_with_three_forward_ticks.md), stationarity of the tested state transformation, as distinct from the terminal exponent, remains necessary to compare its different input columns.

## Limits that the four ticks expose

* **Too few ticks.** From an interior sharp rail the sorted squared site numerators through one, two and three ticks are \((1,1)\), \((1,1,2)\) and \((1,1,1,5)\). Each has at most two distinct positive masses. With two masses the population weight of the heavier class under \(q<1\) and \(q>1\) brackets its ordinary value, so mixing the two gives the entire ordinary relative histogram. Equal weights give the same histogram for every exponent. Four is the shortest uninterrupted sharp-launch position reference distinguishing every fresh mixture by its relative histogram in this family. At \(L=4\) the five offsets alias; at \(x=0\) on the right rail the site numerators are \((2,2,10,2)\).
* **Rails resolved before powering.** The four-tick field has seven occupied unit rail masses and one mass nine, in sixteenths. Weight \(9/20\) of launches with \(q=0\) and \(11/20\) with \(q=2\). The heavy rail occurs with probability \(1/8\) or \(81/88\), respectively. Their average is \(9/16\), and the other seven rails are individually ordinary by symmetry. The entire relative-site marginal, both scores included, passes. On a science pair \(h=(1/4,3/4)\), however, the first old-label rate is \(7/25\). This control defeats the marginal scores; it does not assert equality of the complete joint tables.
* **Independent normalizers.** An apparatus may choose a science label according to \(T_2(h)\) and then use ordinary \(m_j/16\) conditional on each such label. Every cell-wise conditional reference passes and every relative histogram is ordinary. Under joint powering this combination is excluded by the common exponent and normalization. The conditional reference alone cannot validate those premises. Writing only the old position while leaving both old rails coherent also changes the construction, since the four-tick suffix can then depend on their incoming superposition.

The [integer replay](check_appended_position_read.py) enumerates every four-tick physical direction word on lengths 5 through 48, from both rails of every well. It separately propagates an actual seven-tick walk that stores its third-tick directed mode and checks the full joint table against the product formula, including two exact cancellations. [Complete results](results/appended_position_read.json) · [Lean 4.19 boundary and countermixture checks](lean/AppendedPositionRead.lean)
