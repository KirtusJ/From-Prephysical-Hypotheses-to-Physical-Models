# How large a phase signal could the reporter produce?

The nine-tick proposal compares the fraction of launches reporting that the first and third displacements have the same sign. The ideal coherent walk predicts an increase of $1/8$ with opposite rather than equal pulse signs. Deterministic paths can measure a reporter's susceptibility to the two pulse settings. The bound below uses all four measurements on each path together and states exactly what must transfer to the science runs. There are no hardware results in this note. [Phase comparison and its ideal prediction](phase_comparison.md)

## A sharp bound when both pulse choices leave the true path law unchanged

Let $s=(s_1,s_2)$ be one of $++, +-, -+, --$. Let $W=w$ denote the true chronological triple of three-tick displacements, each in $\{-3,-1,1,3\}$. For each deterministic calibration word, route the walker with $I/X$ coins to visit the prescribed sites at the three read clocks. A phase on a sharp rail has only a global phase. Keep the same two pulse commands, timing, readout and processing in those runs. Let $m_{s,w}$ be the probability that the complete reporter returns **agreement** on that forced word, including all its opportunities to make an error. Other physical degrees of freedom may distinguish the forced path and the science path even if their three positions coincide.

Under the full null, the science word distribution $\pi_w$ is common across all four phase arms. Assume also that the science reporter's conditional agreement probability, given the true word and the arm, equals the measured $m_{s,w}$. Write $Y_s$ for science agreement probability per assigned launch and define

$$
\Delta=\tfrac12 (Y_{+-}+Y_{-+}-Y_{++}-Y_{--}),\qquad
d_w=\tfrac12(m_{+-,w}+m_{-+,w}-m_{++,w}-m_{--,w}).
$$

Then $\Delta=\sum_w\pi_w d_w$. With no further information about $\pi$, the sharp interval of reporter-only effects is $[\min_w d_w,\max_w d_w]$. An endpoint is attained by concentrating the common word law on its extremizing word. With separately established restrictions $\pi\in\mathcal P$, take the minimum and maximum of the **same linear functional** on that set. Restrictions on prefixes, sign frequencies or support give small linear programs. No classifier independence, identical gains, or error sign across the different words is required. Conditioning on a word inferred from the same noisy reports can bias estimates of the true $\pi$.

**Numerical illustration.** For two words A and B let the equal arms both have agreement probabilities $(0.90,0.10)$ and the opposite arms both have $(0.92,0.07)$. The two word contrasts are $+0.02$ and $-0.03$. The largest possible false increase is $0.02$. Choosing the most favorable word separately in every arm would give $0.92-0.10=0.82$ and violate the common-law assumption. If an independent measurement restricts $\pi_A$ to $[0.4,0.6]$, the largest effect is $0.6(0.02)+0.4(-0.03)=0$. If each displayed reporter probability has a simultaneous uncertainty of $\pm0.01$, these upper bounds become 0.04 and 0.02. For example, a lower confidence limit for the science contrast above 0.04 would separate the full null in this illustrative unrestricted-word experiment, subject to transport.

## If only one write is known to erase phase

The other pulse can affect the true word even under this weaker null. If pulse $s_1$ is erased, condition on $t=s_2$. There is one common word law $\pi_{w|t}$ across the erased choices *at fixed $t$*. With equal design weight for both values of $t$, the sharp upper bound using only those two common-law restrictions is

$$
\Delta\le\tfrac12\sum_{t=\pm1}\max_w\big[m_{(-t,t),w}-m_{(t,t),w}\big].
$$

For an erased second pulse interchange the coordinates. If either erasure is possible, use the larger of the two upper bounds. The joint linear program can be tightened using any **independently justified** causal restrictions. For example, when $s_2$ is randomized after the second write, varying $s_2$ cannot change the true prefix already written. The two-law formula allows arbitrary prefixes in each maximization. If an apparatus sometimes erases the first pulse and sometimes the second, combining bounds for separate mechanisms requires calibration responses that apply within those subsets or additional information about their dependence on reporter behavior.

## Randomization, uncertainty and incompleteness

* With independently selected source preparations $r$, compute the four-arm contrast within each preparation, then average with a predeclared common mixture $\tau_r$. When $\pi_r$ may vary by preparation, the sharp upper bound is $\sum_r\tau_r\max_{\pi_r\in\mathcal P_r}\sum_w\pi_{r,w}d_{r,w}$. If the source law changes with the arm, even a perfect reporter can give a false $1/8$. For example, let A always report agreement and B always report disagreement. Taking $\pi_A=9/16$ for opposite arms and $7/16$ for equal arms suffices. Uniform sampling of each phase sign is convenient; unequal randomized arm counts can be standardized to the declared equal arm weights. Adaptive assignment requires valid conditional propensities and positive support.
* Given simultaneous calibration intervals $[l_{s,w},u_{s,w}]$, use $d_w^+=(u_{+-,w}+u_{-+,w}-l_{++,w}-l_{--,w})/2$ for the upper bound. Reverse endpoint choices for the lower bound. This is sharp given just the rectangular intervals and the common law. Additional joint information can shrink the bound. An unmeasured calibration cell has interval $[0,1]$ unless restricted by other evidence. For independent binary launches per arm, one option is simultaneous Hoeffding intervals over the calibration cells and science arms, or allocate separate error budgets whose sum is the desired overall level. Compare an appropriate lower limit for the science $\Delta$ to the reporter-only upper limit. Arbitrary serial drift requires an analysis justified by the randomization and sampling scheme. [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)
* Use original assigned launches for all rates. If a no-report counts as zero agreement, apply this convention in both science and calibration. If agreement is unknown on missing launches, lower and upper counts are the recorded agreements and that count plus the missing launches. Substituting these bounds before propagation retains uncertainty due to losses.

## A transport failure invisible on every forced word

Randomizing the phase signs and calibration words identifies the forced-word responses. It does not by itself identify the response conditional on a naturally occurring science word. Let a balanced hidden mode $Z\in\{-1,1\}$ be independent of both pulse choices. In science runs let $W=\mathrm A$ for $Z=1$ and $W=\mathrm B$ for $Z=-1$. The science word law is common to all arms. Give these words labels $h(\mathrm A)=1$, $h(\mathrm B)=-1$. Suppose the reporter's agreement probability is $1/2+e_s Z h(w)/16$, where $e_s=1$ for opposite pulses and $e_s=-1$ for equal pulses. Every independently forced word averages over balanced $Z$, so every calibration probability equals $1/2$. In science $Zh(W)=1$ on every launch, hence the observed contrast is $9/16-7/16=1/8$, with zero physical phase effect on the word.

If separate evidence bounds the difference between forced and science conditional reporter probabilities by $\eta$ uniformly, enlarge the preceding upper limit by $2\eta$ (and the lower limit downward by $2\eta$), or incorporate per-cell discrepancies directly into the intervals. This factor follows from the total absolute arm weight of two. A hardware test is falsifiable against the stated reporter-and-erasure model when the calibrated bound, including an experimentally warranted transport allowance, falls below the observed effect with the required uncertainty. The forced-word table alone leaves the hidden-mode example open.
