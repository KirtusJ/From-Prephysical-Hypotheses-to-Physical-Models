# Two partial terminal sheet reads select the ordinary power on six wells

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Consider the [six-well reciprocal ring](A_reciprocal_sheet_connection_on_six_wells.md) at tick eleven after a sharp launch on sheet zero and the right rail. Record the base well on every launch. Choose setting A to record the terminal sheet at wells 1 and 3, or setting B to record it at wells 3 and 5. Either setting alone admits mixtures of nonordinary powers giving its exact ordinary histogram. Together they select ordinary weighting for a common population of powers, even when each setting has different hidden partitions and a different normalization.

## Preparing the two records

Assign a known positive probability to each setting by an independent random choice. For each setting retain the complete conditional histogram of detected outcomes per assigned incident launch. At each reported bin the detector may partition its occupied rail-and-sheet modes arbitrarily, sum the squared kinematic masses inside each cell, apply one power \(q\ge0\), normalize over the whole setting and report the bin. Zero power counts positive cells. Also admit maximizer reads with arbitrary ties and fair counting of all \(2^{11}\) physical direction words. The distribution of \(q\), counting and infinite power must be the same in both assigned populations. Within a type the partitions may depend freely on the setting. The controls or loss must preserve this common distribution at the point of analysis. An external random switch by itself cannot enforce a common exponent inside a context-sensitive detector.

| Well and sheet | Mass numerator | Unsigned words | Settings reporting this pure bin |
|---|---:|---:|---|
| 5, 1 | \(a=81\) | 463 | B |
| 3, 0 | \(b=225\) | 341 | A and B |
| 1, 1 | \(c=576\) | 220 | A |

These are all the pure bins in each setting. The [single-histogram criterion](When_a_position_histogram_identifies_its_probability_power.md) gives the failure of each setting alone. For two settings let \(u=\log(b/a)\), \(v=\log(c/b)\); write \(P_m^k\) for the probability of the designated mass-\(m\) bin in setting \(k\). Form
\[
W=u(P_c^A/c-P_b^A/b)+v(P_a^B/a-P_b^B/b).
\]
Each term uses its own setting's denominator. The ordinary expectations are \(W=0\) and \(P_a^B=81/2048\).

## Bounding what the different normalizers can do

Let \(Z_A,Z_B\) be the sums of the powered cell masses of a particular type in the two settings. Within A the most pooled vector is \(A_0=(761,576,333,225,153)\). Within B the fully split vector is \(B_0=(676,576,324,225,144,81,9,9,4)\). Split every entry of \(A_0\) into two equal halves. \(B_0\) majorizes this doubled-length vector: after padding with zeros, the differences of the sorted prefix sums, multiplied by two, are
\[
591,\ 982,\ 1054,\ 928,\ 883,\ 712,\ 505,\ 298,\ 153,\ 0 .
\]
Combining cells in B increases concentration, and splitting cells in A decreases it. Thus any allowed B vector majorizes the equal-halves duplication of any allowed A vector. The [checker](check_two_partial_sheet_reads.py) also verifies these prefix sums are nonnegative for all 400 pairs of distinct partition vectors. For \(q>1\), convexity of the power function gives \(Z_B\ge2^{1-q}Z_A\). For \(0<q<1\), concavity reverses the bound. At zero power the same reversed inequality follows by continuity from the right, since only positive cells contribute. This is the finite-vector majorization inequality. [Marshall, Olkin and Arnold, Chapter 1](https://doi.org/10.1007/978-0-387-68276-1)

Put \(r=q-1\). The normalized statistic for one finite type is
\[
W=u(c^r-b^r)/Z_A-v(b^r-a^r)/Z_B .
\]
For \(r\ne0\) the ratio \((c^r-b^r)/(b^r-a^r)\) equals \(v/u\) times the ratio of the integrals on \(0\le t\le1\) of \(\exp[r(\log b+tv)]\) and \(\exp[r(\log a+tu)]\), respectively. Their log coordinates differ by \((1-t)u+tv\), strictly greater than \(\log2\), since \(225>2\cdot81\) and \(576>2\cdot225\).
For \(r>0\) the ratio of integrals therefore exceeds \(2^r\), at least \(Z_A/Z_B\). For \(r<0\) it is below \(2^r\), at most \(Z_A/Z_B\). In the second case \(b^r-a^r<0\). In both cases \(W>0\), including \(q=0\). The bounds are uniform in the two hidden partitions. Given a common distribution of \(q\), the conditional partition laws for the two settings can be coupled arbitrarily to average this inequality. No detector has to perform both reads on the same traveler.

For fair counting,
\[
2048W=u(220/576-341/225)+v(463/81-341/225)>0 .
\]
Indeed \(576^2\cdot81>225^3\) gives \(v/u>1/2\), the second bracket is positive, and substituting \(1/2\) for \(v/u\) gives \(31319/32400\) after division by \(u\). The mass 676 inside well 5 belongs to a cell at least this large in both settings. Every scored pure bin is strictly smaller, so maximizer reads give \(W=0\) and \(P_a^B=0\) for every tie rule. Equality of the population score first eliminates fair counting and all finite \(q\ne1\). The ordinary value of \(P_a^B\) then eliminates infinite power.

A setting-dependent mix is an exact counterexample to inference without transfer. In each setting use its own mixture of nearby nonordinary powers as supplied by its two-pure-mass obstruction. Together the two conditional histograms then agree exactly with the ordinary histograms, even if the experimenter independently chooses the setting. No matching of individual launches is required by the positive theorem. It requires the same type law in both populations. The full 2,048-word normalization, both terminal detectors, coherent transport and outcome efficiencies enter this proposed experiment. The conditional result provides no physical data or sample budget. [Exact signed path and partition replay](results/two_partial_sheet_reads.json)
