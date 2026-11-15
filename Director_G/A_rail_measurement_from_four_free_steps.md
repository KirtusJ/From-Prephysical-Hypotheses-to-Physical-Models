# A rail measurement from four free steps

Four uninterrupted steps on an eight-site ring perform a weak measurement of the Hadamard rail axis. The terminal position supplies two informative outcomes and two nulls. A common pulse on a null restores the input. This implements the corrected [four-route rail instrument](Reading_a_rail_axis_with_four_coherent_routes.md) using the walker's own position as the pointer. The measurement starts at a known site. Its position write is compatible with repeated rail preparation there or at the last reported site. A delocalized wave packet would undergo a spatial measurement as well.

## The four position outcomes

Order the rail as $(R,L)$. Each tick applies $H=(X+Z)/\sqrt2$ and then streams $R$ one site clockwise and $L$ one site counterclockwise. Launch at site zero mod eight. Sum the signed amplitudes over four ticks without an intermediate write. In units of $1/4$, the site matrices are

| Displacement | Outgoing rows, incoming columns | Raw outcome |
|---|---|---|
| $+2$ | $\left(\begin{smallmatrix}3&1\\1&1\end{smallmatrix}\right)$ | plus |
| $-2$ | $\left(\begin{smallmatrix}1&-1\\-1&3\end{smallmatrix}\right)$ | minus |
| $0$ | $\left(\begin{smallmatrix}-1&-1\\1&-1\end{smallmatrix}\right)$ | first null |
| $4$ | $\left(\begin{smallmatrix}1&1\\-1&1\end{smallmatrix}\right)$ | second null |

These entries follow by applying $(r,l)\mapsto(r+l,r-l)$ to each input column and translating the two rows after each tick. The signed weights on the integer line at $+4$ and $-4$ contribute the first and second rows of the antipodal matrix. On the ring both end at one site. The other four sites are dark. Translation of the launch site translates the table.

The informative matrices are $M_\pm=(2I\pm X\pm Z)/4$. Each null has probability $1/8$ on every input. Its rail matrix is $\pm ZH/\sqrt8$. Apply its inverse unitary $HZ$ on either recorded null. The corrected matrix is then $\pm I/\sqrt8$. The four resulting **outcome maps**, including their action on a spectator, coincide with the earlier corrected selector after relabeling its nulls. An implementation needs a coherent ring, a position-only write preserving both arrival rails, and the ability to apply the correction between shifts. The pulse order on the rail is $Z$ followed by $H$.

Starting from $I/2$, each terminal threshold sign $\tau$ is balanced. Measure every four free ticks, count $\pm1$ or zero, and stop at either $\pm m$. The threshold theorem for the selector now applies to these relative displacements. The prepared density is $(I+\tau\eta_m H)/2$, where $u=3-2\sqrt2$ and $\eta_m=(1-u^{2m})/(1+u^{2m})$. The mean cost is $4\sqrt2\,m\eta_m$ free walk ticks, plus the time needed for the reads and corrections. A launch with an unresolved threshold at a deadline remains in the incident count. A new four-tick read on this preparation supplies the full table of the stopped scalar reference in the limit $m\to\infty$, with the two signs tracked separately. The argument uses ordinary probabilities and conditional state updates. The comparison can test the stipulated correspondence between a scalar reference and position data. The coherent phase of a separately addressed gate still needs its own reference.

There is also a preparation with a fixed duration and no rail corrections. Read position every four steps for $m$ blocks. Retain the word with $m$ successive plus signs or the word with $m$ successive minus signs. Each retained word produces the same threshold-tag density from $I/2$ because its rail matrix is $M_\tau^m$. Its per-launch probability is $(\lambda_+^{2m}+\lambda_-^{2m})/2$ where $\lambda_\pm=(2\pm\sqrt2)/4$. Both retained labels together have probability $\lambda_+^{2m}+\lambda_-^{2m}$, which tends to zero. At $m=2$ each retained word occurs with probability $17/64$ and $15/32$ of all launches are outside the two retained words. Short informative words provide a direct experimental check and leave the large-threshold low yield explicit.

The same ring can also implement the null correction using only timed position writes. Six- and eighteen-tick flights generate a feedback procedure that restores the rail with probability one and costs 84 additional walk ticks on average per null. This replaces the separate $HZ$ pulse and changes the expected free-walk cost of the complete threshold preparation to $25\sqrt2\,m\eta_m$. [Position-feedback construction and cost](Restoring_a_rail_with_position_records.md)

## Earliest read in the uniform walk

Four is the first tick at which one terminal site read from a sharp launch, followed by classical randomized relabeling, can reproduce these four raw effects for every rail. This statement fixes the coin and excludes a separate preparation pulse or intermediate measurement. Through tick two all site effects are in the span of $I,X$. At tick three the effects at $+1,-1$ are $(3I\pm(2Z+X))/8$, and those at $+3,-3$ are $(I\pm X)/8$. To obtain the $+2Z/8$ coefficient of the required plus effect, the $+1$ site must always report plus and $-1$ must never do so. The $+1$ site already provides the entire $3I/8$ term. Both outer sites must therefore have zero plus weight, leaving only $X/8$ where $2X/8$ is required.

## A control for coherence at the antipode

On the open line, separately writing $+4$ and $-4$ and combining their classical labels reproduces the ring's antipodal probability on every input. It leaves distinguishable paths. From a sharp $R$ launch, the ring's antipode conditionally has rail $(R-L)/\sqrt2$; the line's merged extreme gives an equal mixture of the two sharp rails. After $HZ$, the next sharp rail read gives $R$ with probability one on the ring and $1/2$ on the line. The joint probabilities per incident launch for this null and $R$ are $1/8$ and $1/16$. This is a proposed two-read control. Intermediate spatial records, imperfect erasure or leakage into a winding label can change its result.

For partial path marking, let the two extremal amplitudes carry normalized environment states with overlap $\gamma$. Tracing over the environment leaves the raw antipode rate at $1/8$; its joint rate with $R$ after $HZ$ becomes $(1+\operatorname{Re}\gamma)/16$. A relative propagation phase enters the same real overlap. A zero contrast can therefore occur for either orthogonal marks or an unmarked coherent relative phase of a quarter turn. This interpolating calculation was supplied by ChatGPT during a source-reading exercise and checked against the two-rail density matrix. [Calculation and provenance](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/issues/270#issuecomment-6887788909)

A second control uses only position writes. Omit the correction after that null, take four more free steps, and ask whether the relative displacement is $+2$. Its conditional probability is $1/8$ on the ring and $3/8$ on the separately recorded line. The joint probabilities for the two successive records are $1/64$ and $3/64$. On the line the analyst can compute the displacement from the stored first site and then pool the two extreme labels.

The construction uses propagation followed by position detection to realize a rail measurement, a principle studied for quantum-walk implementations of generalized measurements. Here the homogeneous coin, eight-cycle and four-tick duration specify the particular instrument. [Kurzyński and Wójcik](https://arxiv.org/abs/1208.1800) · [Exact signed-path replay](check_terminal_site_decision.py)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex derived the four-step implementation and coherence control.
