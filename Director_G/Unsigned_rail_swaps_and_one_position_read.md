# Testing the probability power with unsigned rail swaps and one position read

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two addressed exchanges of outgoing rail labels replace the applied phase defects in the [six-tick signed protocol](Three_signed_ticks_and_the_probability_power.md#a-shorter-schedule). The walker starts at a single site on rail \(R\). Six ticks suffice for a position histogram with exactly the same rail masses as the signed protocol. Nine ticks give a second design with integer scores and every scored outcome on the same rail. No sheet, intermediate detector or coherent auxiliary source enters either preparation.

## Six ticks with two rail exchanges

On the line, at each tick perform the signed Hadamard \((r,l)\mapsto(r+l,r-l)/\sqrt2\), then shift \(R\) one site right and \(L\) one site left. **After** the shift at tick 3 exchange \(R\) and \(L\) at site \(+1\); after the shift at tick 4 do the same at \(+4\). Each addressed operation is the complete unsigned onsite permutation \(X(r,l)=(l,r)\), including the incoming vacant mode when present. All unaddressed modes keep their rail. Record only position after tick 6. This requires a phase-calibrated site- and time-selective mode exchange in addition to the free tick. Position- and step-dependent coins have been implemented in time-multiplexed photonic walks. A device must also verify the relative phase of its purported unsigned exchange, including its phase relative to other sites. The calculations below are predictions for this setting. [Nitsche et al., experimental dynamic coin control](https://doi.org/10.1088/1367-2630/18/6/063017)

The rail entries have common amplitude denominator \(8\). The last column counts complete six-step direction words.

| Site | \(R\) | \(L\) | Squared mass numerator | Words |
|---:|---:|---:|---:|---:|
| −6 | 0 | −1 | 1 | 1 |
| −4 | 1 | −3 | 10 | 6 |
| **−2** | **1** | **0** | **1** | **15** |
| **0** | **0** | **−4** | **16** | **20** |
| **+2** | **0** | **5** | **25** | **15** |
| +4 | 3 | 1 | 10 | 6 |
| +6 | 1 | 0 | 1 | 1 |

Every individual rail square agrees with the earlier six-tick flight that changes signs at \((2,-2)\) and \((4,+2)\); the signed amplitudes differ. This establishes equivalence for the stipulated terminal readouts only. For a power reader, partition each site on a given launch into one cell or its two rails. Give each positive squared cell mass \(m\) weight \(m^q\) and divide by the common sum \(Z\). Dark cells keep weight zero even at \(q=0\). Report only the site. The nonnegative exponent is common across cells on a launch, and can be arbitrarily correlated with the partition across launches. A second allowed type counts every complete direction word equally. Every word remains available under an unsigned exchange, so its position counts are binomial.

Put \(\theta=\log(4)/\log(5)\). On the three bold sites use scores \(1-\theta,-1/16,\theta/25\), and score every other bin zero. Each scored site has one occupied rail under either granularity. The powered numerator is

\[
  ZD_6(q)=(1-\theta)+\theta\,25^{q-1}-16^{q-1}\ge0.
\]

The weighted arithmetic–geometric mean inequality gives equality exactly when \(25^{q-1}=1\). The pure cell of mass 25 is the unique largest cell for all partitions, so \(D_6(q)\to\theta/25>0\) as \(q\to\infty\). Equal path counting gives \((55/4-72\theta/5)/64>23/1280>0\) since \(4^8<5^7\). Consequently a zero population mean excludes fair counting and places the full powered population at \(q=1\) within the specified class.

## Nine ticks with integer scores, all on rail L

Exchange the rails after tick 2 at \(+2\) and after tick 3 at \(−3\). Read position after tick 9. The scored bins are:

| Site | \(R\) numerator | \(L\) numerator | Direction words | Score |
|---:|---:|---:|---:|---:|
| −9 | 0 | −1 | 1 | 768 |
| −5 | 0 | 2 | 36 | −512 |
| −3 | 0 | −16 | 84 | 1 |
| +3 | 0 | 2 | 84 | 256 |

The squared mass divisor is \(512\). Every powered reader assigns the same probability to sites \(−5,+3\), including when the exponent and the choices at the other sites are fresh each launch. Counting gives the site \(+3\) an excess of \(48/512\) over \(−5\). This lets a single integer statistic retain the power test and assign counting a strictly positive mean. For \(x=4^q\), the complete mean numerator is

\[
 ZD_9(q)=768-512x+x^4+256x
        =(x-4)^2(x^2+8x+48).
\]

Equality is equivalent to \(q=1\). The unique maximum is the single rail at \(−3\) of squared mass 256. Every partition has at most 15 positive cells and \(Z\le15x^4\). In particular \(D_9(q)\to1\) at large power. For \(\delta>0\), if \(|q-1|\ge\delta\), then

\[
 D_9(q)\ge \frac{(1-4^{-\delta})^2}{15}.
\]

Indeed \(ZD_9/x^4=(1-4/x)^2(1+8/x+48/x^2)\). Fair counting gives \(3924/512=981/128\). If \(\alpha\) is the counting fraction and \(\beta_\delta\) the fraction of all launches with such a displaced finite power, the population mean is at least \((981/128)\alpha+\beta_\delta(1-4^{-\delta})^2/15\). A rule always choosing the largest cell contributes mean one. A finite histogram needs a sampling uncertainty model to use this population bound.

All four scored wells already occupy rail \(L\). An efficiency common on that rail across the four sites within each latent type scales its conditional mean by that efficiency. Under type-specific site gains, the earlier [terminal routing control](Three_signed_ticks_and_the_probability_power.md#when-losses-follow-the-detector-choice) can use a fresh, independent uniform cyclic reassignment of these four complete site pairs with decoding. It requires equivalent routes and post-scoring losses. Completely dark types cannot be excluded by detected events. Preserve the incident denominator, unmatched or missing records, and all site bins. For example, if fraction \(\ell\) is missing and each such launch was logged with score zero, its unknown true contribution lies between \(−512\ell\) and \(768\ell\).

## The five-tick false pass

One exchange after tick 3 at \(+3\) gives pure \(L\)-rail masses \(1,4,16\) at \(−5,−1,+1\) at tick 5. Their scores \(16,-8,1\) give numerator \((4^q-4)^2\) for every partition. Counting instead gives \(−27/16\). A mixture of \(9/17\) whole-site \(q=0\) and \(8/17\) fair counting has exactly zero mean for this statistic, with no \(q=1\) launches. The example establishes a failure of this scalar test. The mixture need not match the full ordinary histogram.

These are conditional tests of the probability-rule gate P5. The preparation presupposes coherent signed Hadamards, a sharp launch, the specified unsigned routing without path information leaking, and the terminal detector class. A different rule can agree on this finite set of inputs. Physical correspondence remains an experimental obligation.

The [standard-library replay](check_unsigned_position_score.py) independently sums every signed direction word, propagates amplitudes, and enumerates all distinct terminal rail partitions. The [result record](results/unsigned_position_score.json) retains the full five-, six- and nine-tick tables and the signed control. Reproduce it with `python -B Director_G/check_unsigned_position_score.py NEW_FILE.json`. [Lean 4.19](lean/UnsignedRailScore.lean) checks the scored terminal rails, the nine-tick integer polynomial and the fair-word score numerator; the real-power inequality and the detector interpretation are given above.
