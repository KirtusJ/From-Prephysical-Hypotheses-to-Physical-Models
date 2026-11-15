# Which hidden position records can an absorbing walk detect?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Nitsche and collaborators sent a horizontally polarized coherent pulse through a time-multiplexed Hadamard walk. At each opportunity a switch removed both polarization components reaching the origin. The pulse surviving elsewhere continued to propagate. Their published Figure 4 gives cumulative recurrence probabilities through tick 36. We compare the measured continual-sink curve with two specified alternatives that write hidden positions of the surviving pulse. Both leave the displayed sink outcome unchanged at the moment of each write. The subsequent returns distinguish which spatial coherences matter. [Experimental paper, Fig. 4 and Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6025909/) · [Authors’ version, p. 18](https://arxiv.org/pdf/1803.04712v2#page=18)

| Tick | Plotted continual range with digitization allowance | Coherent survivor | Exact site at even ticks | Exact site every tick |
|---:|---|---:|---:|---:|
| 2 | [0.4895, 0.5607] | 0.500000 | 0.500000 | 0.500000 |
| 6 | [0.6025, 0.6799] | 0.625000 | 0.625000 | 0.687500 |
| 8 | [0.6088, 0.6862] | 0.632812 | 0.664062 | 0.726562 |
| 10 | [0.6088, 0.6862] | 0.632812 | 0.710938 | 0.753906 |
| 36 | [0.6151, 0.6925] | 0.636388 | 0.839157 | 0.867939 |

The coherent survivor lies inside the expanded continual bars at all 18 positive even clocks. The every-tick position record exceeds the upper bar from tick six onward. A hidden site write only at even clocks exceeds it from tick ten onward. These are comparisons with reported systematic-error bars under the ideal Hadamard and origin-removal models. They measure the discrepancy with two complete-dephasing schedules. Partial dephasing, optical errors and other instruments can have different predictions.

## What enters the comparison

For initial rail \(R\) at well zero, apply \(H(r,l)=(r+l,r-l)/\sqrt2\), shift right and left, count intensity arriving at the origin and remove it before the next tick. Under coherent survival the remaining state is the unnormalized projection onto all nonzero sites. Adding the absorbed squared norms across ticks gives the continual recurrence. The complete forward intensities at each clock sum to the incident norm when all earlier absorption is included.

After an exact position read at **every tick**, each retained path has a sharp rail fixed by its successive positions. The remaining probabilities follow a symmetric classical walk with killing at the first positive-time return to zero. By the reflection principle its survival through \(2n\) steps is \(\binom{2n}{n}/4^n\). Equivalently, among walks stepping right first and avoiding zero, the number of remaining nonnegative paths of length \(2n-1\) is \(\binom{2n-1}{n-1}\); stepping left first contributes the same number.

At **even ticks only**, a hidden position read preserves both rails at the measured site. Between two such reads an incoming real coin block \(\begin{pmatrix}r&c\\c&l\end{pmatrix}\) sends unnormalized contributions to three sites. Write \(a=r+2c+l,\ b=r-2c+l\). Four times the contribution at \(x+2\) is \(a|R\rangle\langle R|\), at \(x-2\) it is \(b|L\rangle\langle L|\), and at \(x\) it is \(\begin{pmatrix}b&r-l\\r-l&a\end{pmatrix}\). Sum the independent histories arriving at each site and remove the origin block. The odd clocks have no amplitude at the origin by parity. The resulting even-clock recurrence treats the same conditional sink outcome as the optical schedule.

The authors obtained the first-hit contribution from the continual origin counts divided by the **total unsunk counts at that tick** in the reset run (Methods, Eq. 16). This compensates homogeneous round-trip losses. Dividing by the surviving light alone would instead give a probability conditional on survival. For the separate red reset curve the authors combined independent exposures through \(1-\prod_{t=1}^T[1-p_{\rm free}(0,t)]\). The replay preserves that observable as a control. The ideal reset values fall below the expanded plotted bars at ticks 2 and 4 and lie inside all later bars. The authors used a simulation of their optical settings for the numerical curves and their systematic error estimates, including coin-angle and switch and transmission uncertainties. The first two reset rows and all finite discrepancies remain in the result record. [Definitions and calibration](https://pmc.ncbi.nlm.nih.gov/articles/PMC6025909/#sec-4)

## How much complete recording fits the continual bars?

Suppose a fraction \(f\) of launches writes the exact surviving site on every scheduled tick. The remaining launches retain ideal coherent survival. Each launch keeps its initial choice throughout. Denote the two cumulative predictions at tick \(t\) by \(D_t\) (recorded) and \(C_t\) (coherent). With equal incident intensity and a common calibrated response per launch, Eq. 16 gives \(C_t+f(D_t-C_t)\). The total unsunk reference for a tick is common to the two launch types. Unequal reference brightness would make the fitted fraction intensity-weighted. The experiment combined three initial power and integration settings covering ticks 1–5, 6–21 and 22–36. Comparing all rows with one \(f\) assumes it stays fixed across those settings. [Methods, data acquisition and Eq. 16](https://pmc.ncbi.nlm.nih.gov/articles/PMC6025909/#sec-4)

Intersect \(0\le f\le1\) with the two expanded cap inequalities at each of the 18 positive even clocks. Both intervals below include zero. For each schedule the upper cap at tick 34 is decisive, with \(U_{34}=165/239\) and \(C_{34}=1366504425/2147483648\). Substitution into \((U_{34}-C_{34})/(D_{34}-C_{34})\) gives the exact endpoint. Clocks with equal predictions pass for every fraction. Tick zero also agrees by initialization.

| Eligible write ticks | Clocks with equal predictions among the 18 | Largest compatible launch fraction | Approximate percentage |
|---|---|---:|---:|
| Every tick | 2, 4 | 55480488690/233875096949 | 23.72% |
| Every even tick | 2, 4, 6 | 27740244345/101779613636 | 27.26% |

These fractions describe overlap with the published graphical envelopes under the two ideal mixture models. The bars on cumulative points share earlier measurements. They supply neither a confidence level nor a fit of a common set of apparatus errors across clocks.

Choosing whether to write independently at each eligible tick changes which histories interfere. For a recording probability of one half, summing over all subsets of eligible ticks gives cumulative return \(349/512\) by tick 8 on the every-tick schedule, compared with \(87/128\) when the choice is fixed per launch. On the even-only schedule the corresponding returns by tick 10 are \(171/256\) and \(43/64\). The two launch-fraction endpoints apply only to the fixed choice.

## A hidden record invisible at every continual clock

Allow the survivor to write only the sign of its well, left or right of zero, into an inaccessible register after each tick. After the initial split, a nearest-neighbor path that survives cannot change sides. Incoming components from the negative and positive halves can meet at zero only on opposite rails. Their squared norms add for the polarization-unresolved sink event, and both components are removed there. The two half-lines therefore give the same whole sequence of first-hit probabilities when their relative coherence is eliminated. The retained intensity at every nonzero well is also identical. This holds at arbitrary depth in the stated sink protocol. The first binary tag can destroy coherence immediately even though the published continual-return histogram would have no sensitivity to it.

A proposed control on the same ideal rails is to stop after the first splitting step, before either arm can return to the sink. The two occupied states are \(|+1,R\rangle\) and \(|-1,L\rangle\), each with amplitude \(1/\sqrt2\). Disable the sink for readout, undo the shift and coin, and read **both** rails at the source. Untagged arms give rail probabilities \((1,0)\). A hidden side record makes them \((1/2,1/2)\). A known minus sign on the left arm exchanges the untagged probabilities while leaving the tagged ones unchanged. More generally an environmental-tag overlap \(\gamma\) gives \(((1+\operatorname{Re}\gamma)/2,(1-\operatorname{Re}\gamma)/2)\) with a phase-matched inverse. A phase error or an incoherent phase ensemble can also suppress that contrast. The sum over both return rails is one in all three finite controls. Implementing the inverse and phase reference requires an additional calibrated operation. The published experiment measures the forward sink. [Protected-word return construction](Returning_a_protected_position_word.md)

## Figure reading and reproduction

The [digitized caps and predictions](results/origin_sink_data.json) include both colors for all 18 positive even ticks. The origin at tick zero denotes the initial cumulative value zero. The author PDF contains an 800 by 597 RGB plot on page 18, with the probability axes at rows 537 and 59. At a tick \(t\) the reader finds the upper and lower visible colored bar pixels in columns within four pixels of \(\operatorname{round}(100+16.3t)\). Separate pigment tests exclude the orange and green theory curves. At low ticks the centers overlap, so the bounds use the visible bar extremities instead of a guessed marker center. Allow one pixel of uncertainty for each extracted extremity and each axis line. For upper and lower pixel rows \(h,l\) the conservative probability interval is \([(535-l)/478,(539-h)/478]\) by extremizing the affine map over those displacements. The authors' bars summarize their simulated parameter extremes; the expanded intervals are descriptive and carry no confidence level. The paper's data-availability statement directs additional data requests to the authors. This comparison uses the published raster and reconstructs no individual photon counts or independent trials.

Run the [checker](check_origin_sink_data.py) with a new output name. Supplying the authors’ v2 PDF with the optional argument re-extracts every cap and verifies the embedded RGB digest, which is also stored in the result. The comparisons and microscopic direction-word cross-checks through ten ticks run with standard Python. PDF extraction additionally requires PyMuPDF. The optical input, sink schedule and loss compensation differ from a nondestructive measurement of both live outputs in the [reflecting-walk position histories](Reflected_position_histories.md). Establishing that any specific physical detector preserves coherence inside its bin remains open.

```text
python -B Director_G/check_origin_sink_data.py replay.json
python -B Director_G/check_origin_sink_data.py reread.json --pdf 1803.04712v2.pdf
```
