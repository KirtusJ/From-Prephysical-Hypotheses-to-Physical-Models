# When a stopping time is used twice

Kirtus Justus, research direction. OpenAI Codex, derivation and computational checks. 15 November 2026.

One duplicated timing assignment among 804 launches takes the [original decision](One_port_randomized_boundary.md) just below its promised 95% ideal power. A change in the decision threshold can protect the same 804-launch budget against **eight arbitrary changes** to the scored record. These statements concern different prespecified rules. Both use a single terminal detector, count every preparation including losses, and have the same maximum duration of 999,996 ticks. The first is an evaluation of the ideal walk. The second also gives a uniform false-rejection guarantee over the fixed homogeneous stochastic models with at most 55 states.

## One duplicated pair

Draw 803 independent accepted settings with the original generator. Use the first for two separately prepared launches and use each of the other 802 once. Keep the two detector outcomes independent conditional on their shared setting. This deliberate duplication differs from two independent draws that happen to produce the same tick. Accidental equality under independent draws is already included in the original calculation.

If $s(T)$ is the ideal probability of a successful signed score at the accepted setting, write $p=E[s(T)]$ and $m=E[s(T)^2]$. The two scores in the repeated block sum to zero, one or two with probabilities $(1-2p+m,2(p-m),m)$. The other 802 scores sum to an independent $B$ with binomial parameters $(802,p)$. For each $j=0,1,2$, evaluate the old decision on $B+j$, then average with these three weights. The old decision rejects above 480 successes and with probability $115/1024$ at 480.

| Timing assignments | Ideal probability of rejecting the stochastic class |
|---|---:|
| 804 independent draws | 0.950013337855 to 0.950013337856 |
| 802 independent single launches and one independent two-launch block | 0.949888445268 to 0.949888445270 |

Direct propagation of the ten rail amplitudes on the finite-bit timing distribution encloses both moments. In particular $0.52966370805656 < m < 0.52966370805658$. An independent numerical check from the two-phase return amplitude $(1+2\cos(l\arg u)+2\cos(l\arg v))/5$ at tick $2l$ gave $p=0.6256637061390$ and $m=0.5296637080566$. The certified intervals in the table use integer arithmetic. [Fresh-setting calculation](check_804_timing.py) · [Pair moments and pair protocol](Paired_stopping_times.md) · [Duplicated-pair calculation](check_timing_faults.py)

## Eight arbitrary score replacements

Prespecify 804 independent settings and preparations under the [fresh-setting protocol](Real_readout_return_test.md). For a stochastic model the success probability is bounded above by $p_0=0.547843$. For the ideal walk it is bounded below by $p_1=0.625662$. Suppose the observed record can be coupled to this fresh record with at most eight score differences in total. The eight indices and their replacements may depend on the entire fresh record. One sufficient physical case is at most eight substitutions of timing assignments, with the other preparations, settings and outcomes isolated from those substitutions. The bound counts affected launches, including any later ones if a fault propagates.

Reject above **472 successes**. At **472**, reject with probability **3/4** from an independent coin. If $X$ is the fresh count and $Y$ the recorded count, then $X-8\le Y\le X+8$. For the increasing decision function $g$, the worst false rejection is bounded by $E_{p_0}g(X+8)<0.049329$. The ideal miss probability is bounded by $1-E_{p_1}g(X-8)<0.045466$. This eight-edit guarantee uses the sharper bound on what a real-valued detector can report under a stochastic model.

## Faults specified by a rate

An alternative specification gives each launch a conditional probability of a fault of at most $r$, after every history. The unfaulted component of the conditional experiment has an independent setting and ordinary preparation, evolution and detection. The fault component can produce any binary score. For example, a controller may independently choose whether to reuse an old assignment before drawing the current setting. A marginal fault frequency alone does not establish this conditional specification.

The conditional success probabilities are at most $p_0+r(1-p_0)$ under the null and at least $(1-r)p_1$ under the ideal walk. To compare counts, construct each next binary score by thresholding a fresh independent uniform variable at its conditional success probability given the previous scores. Thresholding those same uniforms at the respective constant bounds gives ordinary binomial counts above or below the observed count, path by path. Thus a fixed count threshold has the following exact binomial guarantees, allowing history-dependent faults.

| Maximum conditional fault probability | Launches | Reject at or above | False rejection | Ideal miss |
|---:|---:|---:|---:|---:|
| 1% | 586 | 344 | < 0.049574 | < 0.049344 |
| 2% | 833 | 488 | < 0.049512 | < 0.049479 |
| 5% | 4,609 | 2,685 | < 0.049826 | < 0.049662 |

The rates and edit counts are assumptions on the acquisition process. The calculations supply design guarantees for those assumptions. Experimental verification requires an acquisition record and an instrument maintaining the modeled response through the sampled times.

~~~sh
python -I -B -O check_real_readout_bound.py
python -I -B -O check_timing_faults.py
~~~
