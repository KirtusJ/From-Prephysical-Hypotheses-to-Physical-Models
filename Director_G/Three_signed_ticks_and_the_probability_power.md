# Selecting the probability power with three signed ticks and a position read

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) with independent path and detector checks by Codex workers.

One terminal histogram gives a population test for the ordinary probability exponent in the following family. Each launch may have its own exponent, and the detector may choose separately at every site whether to resolve its two rails. Three coherent sign changes make the test sensitive even to arbitrarily large powers. The construction assumes a sharp rail, the signed Hadamard dynamics and the ability to address a well at a specified tick. The [passive seven-tick comparison](Seven_free_ticks_and_one_position_read.md) requires only free evolution, with weaker conclusions about detector granularity and large powers.

## The flight and the integer score

Start at site 0 on rail \(R\). Each tick first sends \((r,l)\) to \((r+l,r-l)/\sqrt2\), then shifts \(R\) right and \(L\) left. Immediately after the shift at ticks **2, 7 and 8**, multiply both amplitudes by \(-1\) at sites **−2, +3 and +6**, respectively. Leave all other sites alone. No position or passage record is written during the coherent flight. At tick ten record position. The line can be replaced by any network giving the same paths and terminal bins. A photonic coined-walk experiment has implemented position-dependent phase defects through ten steps. Its reported measurements concern localization. Measuring the histogram for these three specified sign changes remains an experimental task. [Xue, Qin and Tang, experimental setup and phase defects](https://arxiv.org/pdf/1401.6109)

The table suppresses a common amplitude divisor of 32. The last column counts direction words out of 1,024.

| Site | Right | Left | Squared site mass | Words |
|---:|---:|---:|---:|---:|
| −10 | 0 | 1 | 1 | 1 |
| −8 | −1 | 7 | 50 | 10 |
| −6 | −5 | 10 | 125 | 45 |
| −4 | −2 | −2 | 8 | 120 |
| **−2** | **2** | **0** | **4** | **210** |
| **0** | **0** | **−6** | **36** | **252** |
| +2 | 2 | 14 | 200 | 210 |
| **+4** | **−18** | **0** | **324** | **120** |
| +6 | −12 | −9 | 225 | 45 |
| +8 | −7 | 1 | 50 | 10 |
| +10 | 1 | 0 | 1 | 1 |

Score the three bold outcomes by \(81,-18,1\), respectively, and the other sites by zero. Preserve all eleven bins, incident launches and missing detections. Write the population mean as \(D=81P_{-2}-18P_0+P_4\). The ordinary mean vanishes because \(81\cdot4-18\cdot36+324=0\).

## Why one setting suffices

For one detector type, partition the nonzero squared rail masses at each site into one pooled cell or the individual rails. A cell of mass \(m\) receives weight \(m^q\). Normalize over all cells with total \(Z\), then report the site. Take \(q\ge0\) common to the cells on this launch. At \(q=0\) every positive cell weighs one and dark cells remain dark. Any joint law of powers and partitions across launches is allowed. Another admitted type gives equal probability to all microscopic direction words. There is a single terminal measurement in each specification.

**Proposition.** An ideal population with \(D=0\) has zero path-counting fraction and exponent one almost surely among the powered laws. The same conclusion holds for an additional limiting rule that always picks the largest cell.

Indeed, each scored site contains a single occupied rail, so partition choice changes only the denominator of its probability. For every partition,

\[
D(q)=\frac{81\,4^q-18\,36^q+324^q}{Z}
=\frac{4^q(9^q-9)^2}{Z}
=\frac{324^q}{Z}(1-9^{1-q})^2.
\]

Its only finite zero is \(q=1\). At zero it is \(64/Z\). The largest cell is uniquely the one at +4 under all 64 distinct partitions of occupied rails. Thus \(D(q)\to1\) as \(q\to\infty\). Fair path counting gives \(D_{\rm count}=12594/1024=6297/512>0\). Taking a population average of these nonnegative conditional means proves the proposition. A negative measured population mean would challenge at least one specification or calibration assumption.

There are at most 17 positive cells, each of mass at most 324. Hence for every \(\delta>0\) and every partition, on \(|q-1|\ge\delta\),
\[
D(q)\ge d_\delta=\frac{(1-9^{-\delta})^2}{17}.
\]
If \(\alpha\) is the path-counting fraction and \(\beta_\delta\) the population fraction in the indicated power tail, then \(D\ge (6297/512)\alpha+d_\delta\beta_\delta\). This bound allows a new type at every launch and has no upper exponent cutoff. For independent lossless ideal draws at \(q=1\) the single-launch variance is \(4779/128\), from the three squared score coefficients and their actual bin probabilities. A sample mean close to zero requires uncertainty on the score and on the controls before it can bound either fraction.

## A shorter schedule

Six ticks suffice if the readout can use logarithmic score coefficients. Flip the signs after tick 2 at −2 and tick 4 at +2. Sites −2, 0 and +2 have pure-rail masses \(1,16,25\), with 25 the unique maximum. Put \(\lambda=\log(25/16)/\log 25\), so \(1^\lambda25^{1-\lambda}=16\). Score these sites by \(\lambda,-1/16,(1-\lambda)/25\). For either granularity at each site the numerator is
\[
\lambda+(1-\lambda)25^{q-1}-16^{q-1}\ge0
\]
by the weighted arithmetic–geometric mean inequality, with equality only at one. The normalized score tends to \((1-\lambda)/25>0\) at large power. Fair counting yields \([15\lambda +15(1-\lambda)/25-20/16]/64>0\), since \(25^7>16^8\) gives \(\lambda>1/8\). This alternative requires two addressed signs and real-valued score coefficients. The ten-tick version has integer scores and the explicit uniform bound above.

## Preparing a sign, or leaving a record

The phase control can be represented kinematically by a two-sheet exchange. Prepare the sheet difference \((|0\rangle-|1\rangle)/\sqrt2\) independently of site and rail. At the three addresses swap the sheets. The exchange acts by \(-1\) on this state, leaving the sheet factored throughout. Its symmetric partner undergoes the bare walk. This identity specifies the source state and the local controls a native implementation would have to realize. A fixed translation-invariant step alone does not supply them.

There is an exact false indication if the source instead starts on one sheet and the sheet is ignored. Under the ordinary rule the symmetric and antisymmetric sector components each carry half the norm. Since the terminal read is the identity on sheet, the observed site histogram averages the bare and signed histograms. The bare score is \(745/256\), giving \(745/512\) for this localized source even with ordinary readout. In the coordinate-sheet description this register records the parity of visits to the three addresses. A second swap can erase the first change. The positive score therefore detects a preparation failure even though the terminal sheet is ignored. All masses in the signed construction are rational after normalization. Every field embedding fixes those rational masses. The test selects a power in the stipulated readout family and leaves selection of an absolute cyclotomic embedding open. [Native sources and embedding ambiguity](Native_preparations_and_probability_embeddings.md)

## When losses follow the detector choice

A positive efficiency common to the three scored outcomes within each type preserves the sign. A different efficiency at each site can even move the ordinary mean away from zero. The targeted wells carry rails \(R,L,R\). A possible readout control first swaps rails at 0 so all three use \(R\), then uniformly cycles the three whole site pairs among their output ports, recording the chosen cycle to decode the site. Do this after the coherent flight. The three occupied rails remain pure in any port, the spectator sites stay fixed, and permutations preserve their type's normalizer. A random cycle independent of the detector state gives the same mean port efficiency \(\bar\eta_A\) to every term for that type \(A\). This requires equivalent routing for the three targets and losses acting after the power scoring, or an equivalent calibrated implementation. On an incident-launch denominator the routed score is \(\mathbb E[\bar\eta_A D_A]\). Positivity for each type still gives exact selection. A quantitative limit on all incident launches needs a lower bound on those efficiencies. A type with zero efficiency is invisible. Record loss as its own outcome.

A flat reference with the correct three mean efficiencies can miss a correlation between response and efficiency. Take equal numbers of whole-site \(q=1\) and \(q=2\) launches. Give them efficiencies \((e,1-e,e)\) and \((1-e,e,1-e)\) at the three targets. Every port then shows mean efficiency \(1/2\) to a flat reference delivered equally to each type. At \(e=12417/57602\), correcting by these three mean gains gives an exact zero for the science score. The numbers and all six efficiencies are retained in the replay. Likewise an arbitrary per-outcome scoring law can agree on this finite input set. These controls delimit which population the histogram identifies.

If \(\ell\) of incident launches have an unknown terminal position, assigning zero to each missing launch gives a logged mean \(D_{\rm logged}\). With no further loss assumptions the complete mean lies in \([D_{\rm logged}-18\ell,\ D_{\rm logged}+81\ell]\). This counts every missing launch and allows all of them to come from either extreme bin.

The [exact replay](check_addressed_position_score.py) compares a path sum with forward propagation, keeps every terminal row, and enumerates the 64 site partitions including all zero-power controls. The [Lean proof](lean/AddressedPositionScore.lean) checks the three terminal rails directly from the ten-tick recurrence, the integer square factorization and the path-count numerator. [Machine-readable results](results/addressed_position_score.json)
