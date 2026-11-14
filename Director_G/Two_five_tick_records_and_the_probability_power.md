# Which probability powers pass two five-tick position tests?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) and the Codex workers.

Three position writes per block let a walker supply a repeated test of its own readout. One five-tick event has ordinary probability \(5/8\). Its probability increases strictly with the power applied to the kinematic weights in each of three specified rival rules. A fourth rival that counts every path gives \(3/8\). Two successive blocks can distinguish even a mixture of those rules from the ordinary exponent, if the rule persists and the same instrument is used. The experiment requires no final rail read and its reference can be prepared on the same type of walk.

## A named event with two orientations

On the line, launch one walker at a known site in a sharp \(R\) or \(L\) rail. Each tick applies the real balanced Hadamard and shifts \(R\) right, \(L\) left. Write the complete position into a fresh pointer at ticks \(1,4,5\), and again at \(6,9,10\). Let \(x_0,x_1,x_4,x_5\) be the start and the three writes of any one block, using local clock indices. Define a hit by

\[
E=\{x_4-x_1=x_1-x_0\}.
\]

This tests the inner well on the side indicated by the first step. Reverse the well used for a hit when that first step was left. The last write identifies the ending rail because \(x_5-x_4=\pm1\). The next block starts from that observed sharp rail, on the same carrier. The three boundary writes are at absolute ticks \(4,5,6\). Use the complete original launch ensemble, including the complementary event and any missing writes. [Position regeneration and its operational premises](Diffusion_from_three_position_records.md)

Conditional on a right first step, the signed rail amplitudes at the next write, three coherent ticks later, are as follows. A common amplitude factor \(1/\sqrt8\) is suppressed. The last two columns are integer amplitudes at the following right and left sites, conditional on the indicated position at clock four, before the common factor \(1/4\). The predecessor is recorded, so these last columns specify separate complete records.

| \(x_4-x_1\) | \(R\) at 4 | \(L\) at 4 | right at 5 | left at 5 |
|---:|---:|---:|---:|---:|
| \(-3\) | 0 | 1 | 1 | \(-1\) |
| \(-1\) | \(-1\) | 0 | \(-1\) | \(-1\) |
| \(+1\) | 2 | 1 | 3 | 1 |
| \(+3\) | 1 | 0 | 1 | 1 |

Translation, reflection with a rail-sign change, and the fair first split give the reflected table of squared weights for a left first step. The preceding sharp rail can change the first-step sign of an amplitude, which drops out of every squared weight.

## Where the readout applies the power

Write \(q\ge0\) for a fixed exponent on **squared** kinematic weights. For \(q=0\) each positive cell has weight one and a zero cell has weight zero. The ordinary exponent is one. Consider these closures of the measurement specification.

| Rule within a block | How the event is scored | \(r=\Pr(E)\) |
|---|---|---|
| Complete position transcripts | Sum signed paths with the same written sites and terminal rail, pool terminal rails at the same transcript, take the \(q\) power of each transcript mass, then normalize over the entire experiment. The clock-five site already specifies the final rail. | \((1+9^q)/(7+9^q)\) |
| Local site read | At each write take the \(q\) power of each site's mass and normalize within the current branch; project to the observed site retaining its two rail amplitudes. | \(5^q/(3+5^q)\) |
| Local site and rail cells | At each write take the \(q\) powers of the positive squared rail amplitudes and normalize jointly; report the cell's site. For an explicit instrument, select that sharp rail and continue from it. | \((1+4^q)/(4+4^q)\) |
| Full path counting | Give each microscopic right/left path equal weight and pool paths by the named records. | \(3/8\) |

These compartment choices correspond to different instruments. In the last local power rule, the same event formula also holds if, after sampling a site with the cell-sum law, the apparatus preserves that site's normalized coin. The next site write makes the resulting rail sharp before each new block begins. In these rules fresh normalization is applied only at actual writes. Applying powers separately after every unrecorded microscopic step is another prescription.

The counts in the table of amplitudes give each expression directly. For the complete record the hit comprises two cells of weights \(9,1\) against six other unit cells. At clock four the local site read has weights \(1,1,5,1\), and the local rail read has one weight four and four unit weights, including one unit in the selected site. For path counting, three of the eight direction words have the required one-site displacement. Each power response is strictly increasing and equals \(5/8\) at \(q=1\) only. In particular, the zero-power responses are respectively \(1/4,1/4,2/5\). All three powers give qualitatively different predictions at \(q=2\), respectively \(41/44,25/28,17/20\).

## Why the second read factors and what it can exclude

At fixed local rule and exponent, every conditional incoming sharp rail gives the same one-block hit probability after orientation by its first movement. Thus the second conditional hit probability is \(r\) for every first-block transcript. This also holds for the fair counting rule. For the global power, every signed count in a complete multiblock word is the product of its block counts. The write at the block boundary specifies one site **and** one rail, so there is a one-dimensional channel between consecutive word segments. The sum of positive powered one-block cells, including both first-step orientations, is the same for both incoming rails. Consequently the unrestricted continuation of a prefix multiplies its sum of weights by this same normalizer. Summing the global two-block products gives \(\Pr(E_1,E_2)=r^2\) and both marginals \(r\) even when the normalization is postponed to tick ten. This proof does not posit an independently reset source or a stored hidden rail between the actual writes. Regeneration by itself works for every exponent in the table.

Let \(\mu\) be an arbitrary distribution of persistent choices among all four rules, including a distribution of powers. Define the observable population discrepancy

\[
M=P(E_1,E_2)-r_*\,[P(E_1)+P(E_2)]+r_*^2
=\int(r-r_*)^2\,d\mu,\qquad r_*=\tfrac58 .
\]

Thus \(M=0\) removes the full counting component and selects \(q=1\) almost surely among all three power rules, even if their mixture weights are unknown. This selects the exponent for this family and these readouts. At \(q=1\) a real rail measurement at clock four can still alter later data. For instance, given the right first step, the joint hit and right last step is \(9/16\) with the site projector and \(5/16\) when the rail at clock four is actually measured and then forgotten. The latter value is \(5/8\) times \(1/2\). Equality of a binary test rate does not identify the instrument.

The reference \(r_*\) can itself be tested. From a sharp site and rail, write each of three consecutive positions and flag five prespecified words of the three displacements. Each sign is conditionally fair under each named model, since squared branches from a sharp rail have equal nonzero mass and remain sharp. The full-word global normalization also gives eight equal words. A physical comparison needs calibrated fairness of these fresh signs or agreement of their full measured word frequencies within uncertainty. If an independent matched reference provides Bernoulli outcomes \(R_1,R_2\) of mean \(r_*\), independent of each other and the two science outcomes, the mean of \((1_{E_1}-R_1)(1_{E_2}-R_2)\) is \(M\). Alternatively estimate the rates in separate ensembles with their statistical uncertainty. Shared reference noise, setting-dependent losses or a different apparatus in the second block can change that expectation. The squared kinematic masses and the specified branch update describe the hypothesis being tested; equal preparation frequencies in an external apparatus are empirical premises.

Bounds on \(M\) are useful away from the pure case. The counting fraction is at most \(16M\). For \(\delta>0\), let \(d_\delta\) be the smallest absolute gap from \(5/8\) among the three increasing response curves at \(q=1+\delta\), and also at \(1-\delta\) when nonnegative. This minimum is positive. The total power-model weight with \(|q-1|\ge\delta\) is at most \(M/d_\delta^2\). These are population bounds; finite data require uncertainty on the rates and the reference.

For a control, use the global transcript rule and \(q=2\) with probability \(11/20\), \(q=0\) otherwise. The one-block rate is exactly \(5/8\). If that choice persists, \(M=81/704\). A fresh independent choice at each block gives the ordinary product law on **every sequence of binary hits**. More generally, correlated types with conditionally independent outcomes compare \(E[(r_1-r_*)(r_2-r_*)]\), which can vanish away from the ordinary exponent. A detector with a completely different rule whose two conditional hit rates are always \(5/8\) also passes. Even a model with dependent outcomes can copy two specified binary rates. These limits make persistence, the scored cells, the instrument across writes and record integrity experimentally consequential. The proof selects neither a probability law for all instruments nor an absolute cyclotomic embedding.

## A single launch tests whether a future write changes an old position word

There is a complementary comparison specific to globally powered, whole-site transcripts. Start at \((0,R)\) and write the positions at ticks two and four, leaving the coin at the clock-four site unresolved. Seal these two coordinates in the old record. In one setting end the walk and read that record. In the other, append a tick, write position at five and then marginalize over that last outcome. Assign settings independently of the source and detector type, and use the same old-record reader. Every newly written position is retained. Compare frequencies of the two original words \(S=(2,4)\) and \(L=(0,2)\). Denote the new marginal minus the old rate by \(\Delta_S,\Delta_L\). Ordinary forward refinement of a protected classical record requires both differences to vanish. A final score on all coherent pointer registers is a rival model of this read; physically matching that score to the read of a record already made is exactly what the comparison probes.

Grouping the signed amplitudes by both old sites gives four old words of integer squared mass 1 that each split as \((1,1)\), two of mass 2 that split as \((0,4)\) up to order, two of mass 4 that split as \((4,4)\), and one permanently dark word. Old masses use denominator 16 and new ones denominator 32. The clock-four rail is pooled in the old mass; resolving that rail at clock four changes the model. In particular \(S\) has old mass 1 and \(L\) has old mass 4. Let \(u=2^q\). The global normalization totals before and after are \(A=4+2u+2u^2\) and \(B=8+6u^2\), with common kinematic denominators omitted. For a fixed exponent,

\[
\Delta_S={2\over B}-{1\over A},\qquad
\Delta_L=u^2\Delta_S,\qquad
4\Delta_S-\Delta_L
=\frac{2u(2-u)^2(2+u)}
       {(8+6u^2)(4+2u+2u^2)} .
\]

The last contrast is nonnegative for every \(q\ge0\), equals \(3/56\) at zero, vanishes only at \(q=1\), and tends to \(1/6\) for large powers. The two individual differences can change sign; the fixed contrast prevents cancellation across a common population of exponents. Both old marginals persisting therefore select \(q=1\) within the global whole-site-transcript family, without a persistent detector across two independent event trials. Every locally normalized forward kernel, including a nonordinary one, automatically preserves the old record when the future outcomes are summed. The contrast has zero sensitivity to those alternatives. In a stable mixture of local and global rules it constrains only the global component. A changed detector population, a clock-dependent read of the stored words or setting-dependent loss can spoil the comparison. No empirical equality is assumed for either word. [Earlier protected-record comparisons](Protected_records_and_coordinate_weights.md)

The [exact checker](check_five_tick_record_powers.py) enumerates the full ten-tick record from either incoming rail and tests each global cell against the concatenated kernels. It archives the raw old-word rail amplitudes, their continuations including dark and zero entries, joint signed amplitudes for the five-tick blocks, and the control populations. The [Lean check](lean/FiveTickRecordPowers.lean) verifies integer cross-multiplication for the three hit rates, the paired binary identity and the numerator factorization in the old-word comparison. [Exact results](results/five_tick_record_powers.json) · [Earlier finite tests of local spatial powers](Partial_flag_readout_and_spatial_powers.md) · [Persistent types and two-read moment bounds](Paired_reads_for_a_type_dependent_target.md)
