# A repeated target weight tests two possible detector resolutions

On a nine-site Hadamard walk, the same fixed target mask receives a quarter of the squared norm after either three or five ticks. At three ticks that quarter consists of two light oriented ports. At five ticks it consists of two medium ports. A comparison using this pair and three other launch settings tests whether the probability exponent is one, even if a detector sometimes scores the whole mask and sometimes scores individual oriented ports. The detector resolution and the exponent can be correlated on individual launches.

**Evidence status.** The mask, five launch settings and return frequencies below are an experimental proposal. The signed-path sums and the selection theorem are calculations. The archived three-spin experiment used a different circuit and supplies no frequencies for these five settings. A localized-sheet construction previously obtained a square of a score difference at five ticks by reading three resolved outcomes. Here one binary mask and a second clock give a common test for two scoring orders. [Translated mask, walk specification and executable path check](translated_mask.md) · [Earlier five-tick resolved-outcome test](../../../Director_G/Five_ticks_from_a_localized_sheet.md) · [Published three-spin experiment](https://doi.org/10.1073/pnas.2529694123)

## Five settings

Launch one sharp right-moving rail at site $s$ on the nine-site ring. Run $t$ identical Hadamard-and-shift steps with no intermediate measurement. Count a report in the same mask $\{0,2\}$ on either rail, using every assigned launch as denominator. The middle column lists squared integer amplitudes of the occupied target ports. The ordinary mass divides their sum by $2^t$.

| $(t,s)$ | Target port weights | Ordinary target mass |
| --- | --- | ---: |
| (3,0) | none | 0 |
| (3,5) | 1 | 1/8 |
| (3,3) | 1, 1 | 1/4 |
| (3,1) | 1, 1, 4 | 3/4 |
| (5,1) | 4, 4 | 1/4 |

The full three-tick port weights are four 1s and one 4. At five ticks there are four 1s, three 4s and one 16. Unlisted ports have zero weight. Write $Y_{t,s}$ for the population report rate. Randomize the launch translation and read clock independently of the apparatus mode. A mode has an exponent $0<q<\infty$, a scoring order, and a reporting rule $a+bP$, where $P$ is its target chance before reporting. The joint mode law is common to the five arms. Allow $0\leq a,a+b\leq1$ and $b\geq0$ with some nonzero gain. A consistently inverted report can be relabeled once. A **whole-mask** mode scores the two cell masses by $g_q(p)=p^q/[p^q+(1-p)^q]$. An **oriented-port** mode raises every port weight to $q$, normalizes once over the ring and sums the target ports.

## A contrast shared by both orders

Set $m=(7/12)\log(7)/\log(3)$, $k=m/2-1/4>0$ and define

$$
\begin{aligned}
B&=Y_{3,3}+Y_{3,1}-2Y_{3,0},\\
L_3&=kB-2m(Y_{3,3}-Y_{3,0})+2(Y_{3,5}-Y_{3,0}),\\
C&=Y_{3,3}-Y_{5,1},\qquad L=L_3+16kC .
\end{aligned}
$$

Both orders give $B=E[b]$. On whole-mask modes this follows from $g_q(1/4)+g_q(3/4)=1$. On oriented-port modes the two corresponding target compositions are two light ports and the remaining two light ports plus the heavy port. Offsets cancel in both cases.

**Whole-mask contribution.** For each mode $C$ has conditional expectation zero because the two physical target masses are both $1/4$. Put $T=(3^q-1)/(3^q+1)$ and $h(T)=\tanh[(\log7/\log3)\operatorname{atanh}T]$. The mode's contribution to $L_3$ is $b[3/4+m(T-1/2)-h(T)]$. The bracket is the gap from the tangent to the strictly concave $h$ at $T=1/2$, where $h=3/4$ and $h'=m$. It is positive for $q\ne1$ and zero at $q=1$. [Tangent calculation](translated_mask.md#what-a-common-binary-instrument-implies)

**Oriented-port contribution.** Write $u=4^q$ and $Z=4+3u+u^2$. A light port at tick three has chance $1/(4+u)$ and a medium port at tick five has chance $u/Z$. Dividing the contributions to $L_3$ and $C$ by $b$ for $b>0$ gives

$$
k+\frac{2-4m}{4+u}=k\frac{u-4}{4+u},\qquad
\frac{2}{4+u}-\frac{2u}{Z}=-\frac{2(u-4)}{(4+u)Z}.
$$

Since $Z-32=(u-4)(u+7)$, the contribution to $L$ is exactly

$$
b k\frac{(u-4)^2(u+7)}{(4+u)Z}.
$$

It vanishes precisely at $q=1$ on modes with positive gain. Averaging over both orders therefore yields $L\geq0$. **If $B>0$ and $L=0$, the responsive population has $q=1$ almost surely.** Conversely the ordinary exponent gives zero for any mixture of these orders. The comparison leaves their relative frequencies unidentified at exponent one. The denominator-cleared polynomial factorization is also checked over the integers in Lean. [Polynomial certificate](ReturnRenewal.lean)

## Finite counts and limits

In the table's setting order the exact linear coefficients of $L$ are $w=(-2k+2m-2,\,2,\,17k-2m,\,k,\,-16k)$. Numerically they are $(-0.4667745,2,2.4659659,0.2666128,-4.2658042)$. Estimate $L$ from the separate launch rates. For independent binary shots within each arm and $n_i>0$ assigned launches, take $e_i=\sqrt{\log(10/\alpha)/(2n_i)}$. With probability at least $1-\alpha$ the errors for $L$ and $B$ are simultaneously at most $e_L=\sum_i|w_i|e_i$ and $e_B=e_3+e_4+2e_1$, respectively. A positive lower confidence limit for $L$ separates the ordinary response within the model. A negative upper limit challenges the model or the sampling assumptions. [Hoeffding's inequality](https://doi.org/10.1080/01621459.1963.10500830)

For a prespecified closed exponent range $S$ separated from one, let $v>0$ be the minimum of the two displayed per-gain gaps over that range, using their continuous endpoint limits if needed. For $B>0$, the gain-weighted fraction of responsive modes in $S$ is at most $L/(vB)$. Thus one may use $(\widehat L+e_L)/[v(\widehat B-e_B)]$ when the denominator is positive and the confidence intervals permit the model. An ordinary launch fraction requires information about how gain varies with mode.

The two-clock comparison requires the same readout gain and the same mode distribution at both clock lengths. If only a clock-specific additive mean offset differs, the optional dark launch $(5,0)$ permits $C=(Y_{3,3}-Y_{3,0})-(Y_{5,1}-Y_{5,0})$; use six-arm uncertainty bounds for that design. A gain change or a setting-dependent distribution of mode or exponent can still imitate a signal. A detector which first sums the two rails at each **individual site**, scores sites and then pools the mask is a third resolution. For that mode the denominators are $3+5^q$ and $2+2\,4^q+5^q+17^q$. With unit gain and $q=1.1$, it gives $L\approx-0.001408$. Thus even the sign test needs a physical account of which alternatives the apparatus scores. Agreement at five settings also leaves arbitrary non-power response laws open.
