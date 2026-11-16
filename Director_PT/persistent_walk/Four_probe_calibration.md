# Four calibration inputs for the five-site terminal detector

Kirtus Justus, research direction. OpenAI ChatGPT, derivation and computational checks. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

How could one check the terminal analyzer before committing to the 31-launch walk experiment? Measuring each rail separately leaves its relative phases undetermined. Four specified coherent inputs suffice to bound the analyzer’s contribution to the signed walk score, provided the inputs have an independent phase reference tied to the walk. With ideal references, at most two errors in 5,065 calibration trials certifies the required score at a one-sided 5% error level. A shared input/analyzer phase error can pass every calibration statistic while cutting the 31-launch walk power below 0.345. [Walk proposal and rail convention](Terminal_rail_readouts.md)

## Inputs and observations

Prepare one of these real vectors normalized to unit length, chosen uniformly and independently on each calibration trial. Inject it at the walk’s terminal plane. Use the same fixed binary analyzer for calibration and the walk. Count every input, including losses, and classify loss as a miss. The expected labels below define calibration success.

| Input | Rail amplitudes before normalization | Expected label |
|---|---|---|
| 1 | $(-4,0,1,0,1,0,1,0,1,0)$ | click |
| 2 | $(0,-46,3,6,-26,-6,26,46,-3,0)$ | click |
| 3 | $(0,0,1,0,-1,0,-1,0,1,0)$ | miss |
| 4 | $(0,34,49,98,-32,-98,32,-34,-49,0)$ | miss |

The analysis permits any fixed effect $0\le F\le I$ on the ten input rails. The analyzer must receive the same physical input modes across both experiments, with no side information from the probe label, trial type, timing sign or previous record. The probabilities below assume fresh independent trials. The calibration concerns the terminal effect. The walk’s evolution and stopping law still have their own physical requirements.

## From four click frequencies to walk power

Let $P_i$ be the normalized projector for input $i$, $W=P_1+P_2-P_3-P_4$, and $q$ the probability of a correct calibration label with trusted inputs. Then $4q-2=\mathrm{tr}(FW)$. The signed walk success satisfies $p(F)=p_-+\mathrm{tr}(FM)$ with the signed matrix and negative-setting mass from the [walk calculation](Terminal_rail_readouts.md). Put $\lambda=0.1570796327$ and let $M_g$ be the calculated grid matrix. Direct rational squaring gives

$$
10\sum_{ij}|(M_g-\lambda W)_{ij}|^2 < (0.000000079)^2.
$$

Since $\|F\|_F\le\sqrt{10}$, this bounds the trace residual for every effect, including complex effects. Propagating the walk contributes at most $\epsilon=6(499998)/2^{104}$. Consequently

$$
p(F)\ge p_-+\lambda(4q-2)-0.000000079-\epsilon.
$$

At $q=0.998757285$ the right side already exceeds $0.813378364430$, the sufficient success probability for 95% power in 31 launches. Thus any analyzer falling below the required walk score has $q<0.998757285$. If the *mean* trace distance between the four actual normalized inputs and their specifications is at most $\delta$, the observed calibration pass probability can increase by at most $\delta$. That assertion requires an externally justified reference-state bound at the analyzer input, including a bound on any omitted modes.

## Finite calibration and experiment

Prespecify one row. Proceed with the walk only if calibration passes. False certification means accepting an analyzer whose ideal-state walk score is below $0.813378364430$. Joint ideal power is the probability of both passing calibration and rejecting the bounded stochastic model with the intended analyzer, ideal calibration inputs and ideal walk. The last row allows inaccurate probe inputs when bounding false certification. Its displayed ideal power still assumes ideal probe inputs.

| Permitted mean probe error $\delta$ for soundness | Probe trials | Maximum probe errors | Walk decision | False certification below | Joint ideal power above |
|---:|---:|---:|---|---:|---:|
| 0 | 2,410 | 0 | At least 29 successes in 42 | 0.049947 | 0.951646 |
| 0 | 5,065 | 2 | At least 22 successes in 31 | 0.049956 | 0.951167 |
| 0.0001 | 5,508 | 2 | At least 22 successes in 31 | 0.049974 | 0.951153 |

For $m$ probes and at most $k$ observed errors, the probability to pass calibration is $\sum_{j=0}^k {m\choose j}(1-q)^j q^{m-j}$. Evaluate it at $q=0.998757285+\delta$ for the false-certification bound. For joint ideal power the exact mode overlaps give $q>0.999986292$. Independence of fresh calibration and walk trials gives the product of their pass probabilities. Under the bounded stochastic null each walk rule alone has false-rejection probability below 5%. Requiring the calibration to pass can only reduce that probability. The walk count and the calibration count measure different resource costs.

## A phase-reference failure that the probes cannot detect

Let $D$ reverse the phase of rail 1, leaving all other rails fixed. If the source delivers $DP_iD^*$ and the analyzer implements $DED^*$, their calibration overlaps are exactly the intended overlaps for all four probes. If the walk outputs stay in the original frame, the signed score of this analyzer lies between **0.657918768 and 0.657918770**. Its 31-launch power is below **0.344480**. An independently registered source or measurement of the relative phase at the walk output is a substantive additional requirement. With the same rotation applied to the walk outputs as well, the joint probabilities are invariant.

A linear-optical multiport decomposition supplies a construction for finite unitary mode transformations. Bian and colleagues observed optical walks on three- and four-node circles. Neither result measures the relative frame, stage loss or propagation fidelity of the proposed five-site apparatus. [Reck et al., *Physical Review Letters* 73, 58 (1994)](https://doi.org/10.1103/PhysRevLett.73.58) · [Bian et al., *Physical Review A* 95, 052338 (2017)](https://doi.org/10.1103/PhysRevA.95.052338)

From the repository root, run `python -I -B Director_PT/persistent_walk/check_four_probe_calibration.py`. The checker rebuilds the signed matrix from the integer timing table, checks the residual, computes the binomial tails as rationals and tests the common-phase fault. [Checker](check_four_probe_calibration.py) · [Recorded output](four_probe_output.txt)
