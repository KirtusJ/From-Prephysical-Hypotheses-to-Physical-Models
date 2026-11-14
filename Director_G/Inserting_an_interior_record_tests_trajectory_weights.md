# Inserting a position record tests how a complete trajectory is weighted

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A sharp right-rail source walks for seven ticks. Record positions at ticks 2, 6 and 7. In a second setting add a position record at tick 4. **The added record changes the ordinary final-position distribution by \(13/64\) in total variation, yet one signed mean of the final position stays at zero.** Within the family that raises each complete recorded trajectory weight to a common finite power, the second setting has this zero mean only at the ordinary exponent. This holds for arbitrary mixtures in that setting, even if the first setting samples different exponents. A second test using seven named position words handles detectors that select any tied maximum. All predictions concern the supplied walk and readout.

## The two schedules

The initial state is \((0,R)\) on the line or at least seven hops from either reflecting boundary. Each tick applies the usual real Hadamard and conditional displacement. A scheduled write copies the current well into a clean persistent register while preserving the coin at that well. Distinct saved words are distinguishable. At the end, sum signed path amplitudes separately for each saved word and outgoing rail, then add the two squared rail amplitudes at the word. The last two positions specify the outgoing rail here. Before normalizing the full table, raise each positive word mass to the one launch-dependent power \(q\ge0\); at \(q=0\) count every positive word once and keep dark words dark. All seven-tick integer masses share denominator 128. The rival at \(q=\infty\) can use any normalized law on the maximum-mass words. The reported scores aggregate these cells *after* that read. Losses, extra copies and conditioning on recorded success would change the test.

Call \((2,6,7)\) the coarse schedule and \((2,4,6,7)\) the fine schedule. This intervention inserts a write before an existing write and can change what happens later. Forgetting the fourth-tick report after it occurred has a different physical effect from omitting that write. Comparisons of inserting and omitting an intermediate measurement have an established formulation in temporal measurement theory. Here it is only a particular signed mean that stays equal at ordinary weight. An earlier walk comparison instead appended a future write after an old word was complete; local forward kernels automatically preserve such old marginals. [Clemente and Kofler, *Phys. Rev. A* 91, 062103 (2015)](https://doi.org/10.1103/PhysRevA.91.062103) · [Five-tick terminal extension and its assumptions](Two_five_tick_records_and_the_probability_power.md)

| Final displacement | −7 | −5 | −3 | −1 | 1 | 3 | 5 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Coarse ordinary mass, units of \(1/128\) | 1 | 17 | 9 | 17 | 17 | 45 | 21 | 1 |
| Fine ordinary mass, same units | 1 | 9 | 15 | 35 | 19 | 35 | 13 | 1 |
| Position score \(G\) | −8 | 48 | −8 | 1 | 15 | 0 | −48 | 0 |

To derive the score, collect the number of positive words of each mass separately at each terminal site. Take a vector on those eight sites orthogonal to each distinct coarse mass row. Of these choose one whose inner products with the fine rows for masses \(1,4,16\) are \(16,-8,1\). An exact integer solution is the displayed \(G\). Its expected value can be measured in units of \(1/48\) by dividing all coefficients by 48 if bounded outcomes in \([-1,1]\) are preferred.

| Schedule and integer word mass | −7 | −5 | −3 | −1 | 1 | 3 | 5 | 7 | Row dotted with \(G\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Coarse 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| Coarse 4 | 0 | 0 | 2 | 4 | 4 | 2 | 1 | 0 | 0 |
| Coarse 16 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Coarse 36 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| Fine 1 | 1 | 1 | 3 | 3 | 3 | 3 | 1 | 1 | 16 |
| Fine 4 | 0 | 2 | 3 | 4 | 4 | 4 | 3 | 0 | −8 |
| Fine 16 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |

The first arm therefore gives \(\mathbb E G=0\) for every finite exponent, and at infinity its unique maximum also scores zero. Put \(y=4^q\). In the fine arm, the positive-word normalizer and the signed mean are
\[
 Z=16+20y+2y^2,\qquad \mathbb E G=\frac{(y-4)^2}{Z}.
\]
Every finite power gives a strictly positive mean except \(q=1\). Thus agreeing coarse and fine means identifies the unit exponent in the **fine** arm of this model with finite powers. The coarse arm alone filters out none of its powers. Comparing to the calculated zero in the fine arm also suffices. In a physical comparison the two arms must realize the specified preparations, grouping and normalized detection. A measured equality of noisy sample means needs an uncertainty analysis.

## Counting paths, maximum ties and a bounded error criterion

The two fine words of mass 16 end at \(-1\) and \(3\). The latter scores zero under \(G\), so a pure maximum rule choosing that word reproduces both position means. To cover arbitrary ties, give seven old words \(h=(x_2,x_6,x_7)\) the coefficients shown below, zero elsewhere. The fine instrument records \(x_4\) in addition; only the statistic ignores it.

| Coefficient \(H(h)\) | Old words | Fine positive masses over the listed words |
|---:|---|---|
| \(+1\) | \((0,0,-1),(0,2,3)\) | \(4,4,16,16\) |
| \(-8\) | \((-2,-4,-5),(2,4,5)\) | \(4,4,4,4\) |
| \(+8\) | \((-2,-2,-3),(2,2,3)\) | \(1,1,1,1,4,4\) |
| \(-2\) | \((-2,-4,-3)\) | \(4\) |

The fine numerator of \(H\) is \(32-16y+2y^2=2(y-4)^2\). At an arbitrary maximum tie both possible outcomes have \(H=1\). Fair counting of all \(128\) direction words contributes respectively \(20,8,12,6\) unsigned paths to the four rows, giving \(\mathbb E H=44/128=11/32\). These means are positive for every named alternative and vanish only for the ordinary power. Thus the seven-word statistic alone tests **all** finite powers, any choice at infinity and fair counting in a single fine schedule. Their expectations in a mixture have no cancellation.

For a population with mean \(\mathbb E H\le e\), the fraction with \(|q-1|\ge\delta\), together with maximum and fair types, is at most \(e/c_\delta\). Here \(c_\delta\) is the least of \(1,11/32\), and the finite expression \(2(y-4)^2/Z\) at \(q=1+\delta\) and, when nonnegative, \(q=1-\delta\). For \(\delta>0\) this is positive. Differentiating the rational expression gives the sign of \(y-4\) since \(2Z-(y-4)Z'=112+36y>0\). If \(e\) is inferred from data, a bound on mean excess must include sampling uncertainty, abstentions and any modeled readout error.

## What consistency does not establish

A reader that normalizes at every write has different statistics even with the same coherent conditional update. In the fine schedule let it sample each well by its local normalized powered mass, keep the projected coin and carry on. At \(q=0,2\) its terminal means of \(G\) are respectively \(5/18,-1/9\). A mixture with probability \(2/7\) on \(q=0\) and \(5/7\) on \(q=2\) reproduces the zero final score exactly while every launch uses a nonordinary exponent. Both types give positive fine means of \(H\), respectively \(1/9\) and \(2/9\), so this second comparison detects this particular cancellation. No claim here characterizes all locally normalized families or their hidden conditional state changes.

More generally two scalar statistics cannot fix the full trajectory law. For the old triple \((-2,-2,-3)\), the fourth-tick well can be \(-4,-2,0\), with positive weight in all three cases. Redistribute a positive amount smaller than the least of their masses between any two of them. The original and altered tables give exactly the same full \((x_2,x_6,x_7)\) distribution, hence the same two scores, while differing as fully recorded four-position laws. Each altered table has consistent earlier marginal laws under ordinary summation and can be generated causally by the chain rule for its finite conditional probabilities. Moreover the named old triple is dark when no fourth-tick record is written and has total mass \(6/128\) when that extra outcome is recorded and then forgotten. Selecting an unrestricted probability rule or identifying an external cyclotomic label requires additional evidence. [All-protocol obstruction for native labels](Native_preparations_and_probability_embeddings.md)

The [replay](check_interior_record_weights.py) computes both instruments by signed paths and by independent transport of the protected position registers. The [record](results/interior_record_weights.json) retains every kinematically reachable word, its two integer amplitudes, destructive cancellations, both score tables and the local-normalization counterexample. The [Lean 4 certificate](lean/InteriorRecordWeights.lean) checks the signed table coefficients and the square identities used to certify the finite-exponent comparison.
