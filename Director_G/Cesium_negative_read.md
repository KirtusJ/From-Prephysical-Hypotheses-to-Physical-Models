# What a four-step cesium walk measures about a first-step record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

Robens, Alt, Meschede, Emary and Alberti launched cesium atoms in one spin state at one lattice site. They compared a four-step walk with two runs in which they moved one of the first-step arms five sites aside and counted final positions. Their published histograms supply a test of a passive record that would leave the final distribution invariant. They also show exactly where the experiment stops short of testing the independence of two pointer values at a shared splitter. [Original experiment, Figs. 2–4 and Appendices A–G](https://doi.org/10.1103/PhysRevX.5.011003) · [Authors' PDF used for the counts](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf)

## Which atoms enter each comparison

Let \(j\) denote the terminal well index printed in Fig. 3. The authors' binary read is \(+1\) on \(j>0\) and \(-1\) on \(j\leq0\). Panel (a) measures position with no intermediate probe. In (b) the first positive arm is moved and the negative arm is retained. Panel (c) reverses those roles. Each probed setting starts with 404 counted atoms. For (b) the displaced region is \(j=4,\ldots,8\), and for (c) it is \(j=-8,\ldots,-4\). The figure marks both regions. Positions in these regions are included in the accounting below. [Original Fig. 3 and Eq. (2)](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf)

| Run | \(j=-3\) | \(-2\) | \(-1\) | 0 | \(+1\) | \(+2\) | \(+3\) | Moved aside | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| No probe | 2 | 15 | 131 | 33 | 35 | 14 | 0 | — | 230 |
| Retain negative arm | 0 | 31 | 107 | 32 | 31 | 0 | 0 | 203 | 404 |
| Retain positive arm | 0 | 0 | 27 | 29 | 115 | 25 | 0 | 208 | 404 |

These are counts reconstructed from the vector bars of the published figure. The [checker](check_cesium_negative_read.py) pins the source PDF by digest, reads the five axis ticks in each panel and measures each green bar in units of atoms. The greatest distance to the nearest integer is below 0.070 atom. It saves all seventeen displayed sites for each setting, including zero-height bars and the two blank-run atoms at \(j=-3\), outside the ideal support. The displaced counts by site are \(22,42,111,27,1\) in increasing order for (b), and \(2,22,113,40,31\) for (c). The plot gives no explanation for individual anomalous endpoints. Two readers independently recovered the retained counts. The run order and individual trials are unavailable in these histograms. [Bar geometry, count tables and exact arithmetic](results/cesium_negative_read.json)

Following the authors' equal-exposure pooling, the retained first-arm weights are \(201/397\) and \(196/397\). The observed probability of a positive terminal position changes from \(49/230\) to \(171/397\). For the paper's assignments at the first two times, \(K=1+2[P_{\rm retained}(j>0)-P_{\rm blank}(j>0)]\). These counts give \(K=1.435374\), consistent with the printed \(1.435\pm0.074\). The quoted uncertainty is the authors' bootstrap estimate. Their separate Monte Carlo estimate is 0.068. Neither uncertainty is an error bar for the full distribution distance derived below. [Original Eq. (2), Sec. IV and Appendix C](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf)

## A constraint on terminal records

Write \(p\) for the normalized blank histogram and \(q\) for the normalized pooled retained histogram. Under *any* joint assignment of terminal positions with these two marginals, equal outcomes occupy mass at most \(\sum_j\min(p_j,q_j)\). Matching the common part at each site and coupling the leftover positive and negative excesses attains that bound. Thus the smallest possible terminal mismatch for these empirical distributions is their total variation,

\[
 d_{\rm TV}(p,q)=p(\{-3,-1\})-q(\{-3,-1\})
 =\frac{21981}{91310}\simeq 0.24073 .
\]

The paper's prespecified \(j>0\) read gives a smaller difference of 0.21769. The maximizing event above was selected from the data. The two numbers describe observed histograms; neither measures the proportion of individual atoms that followed one trajectory in both experiments. A lower bound on the fraction of a *population* whose endpoint could have changed requires population distributions, comparable preparation, arm selection and detection, and uncertainty for that bound. The original article discusses a 1% imperfection estimate for the negative probe and a separate position-reconstruction error. Its standard blank walk lacked the extra measurement delay. Its matched-delay control used a Ramsey sequence. A later discrete-event simulation also illustrates the importance of modeling the measuring apparatus. [Robens et al., Sec. VI and Appendices A, E](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/SDT/physrevx-alberti.pdf) · [Willsch et al., *Discrete-Event Simulation of Quantum Walks*](https://doi.org/10.3389/fphy.2020.00145)

There is a sensitivity check for the first-arm weights. Let \(b,c\) be the separately normalized retained histograms. For any putative arm weight \(w\) the distance from \(p\) to \(wb+(1-w)c\) is piecewise linear. It suffices to evaluate the endpoints and all roots of \(p_j=wb_j+(1-w)c_j\) in \((0,1)\). The minimum is \(4937/46230\simeq0.10679\), at \(w=1\). Thus reweighting the two reported arm distributions cannot reproduce the full blank histogram exactly. This is an algebraic result for the plotted central counts. Arbitrary setting-dependent or site-dependent changes in collection can alter the input distributions.

For a positive-cell comparison, use only the two named detectors \(j=\pm1\). The ratio of positive-to-negative odds in the pooled setting divided by the same odds in the blank setting is

\[
 \frac{146\cdot131}{134\cdot35}=\frac{9563}{2345}\simeq4.078 .
\]

Fixed linear efficiencies at these two sites and a common brightness factor per setting cancel. If the two retained settings instead have independently unknown positive brightness factors, their combined odds are between the individual arm odds. Relative to the blank odds the limiting endpoints are \(4061/3745\simeq1.0844\) and \(15065/945\simeq15.942\). This leaves only a small central-value separation in the most adverse weighting. Changing the blank \(+1\) count from 35 to 38, holding the other three arm and blank counts in that endpoint comparison fixed, would put the blank ratio inside the interval. The reported uncertainty on \(K\) cannot establish a significance for this separate nuisance-parameter test.

## The walk and the missing control

Use the reflected logical coordinate: the initially populated right rail in the program represents the left-moving atomic spin. The fair signed update gives \((u+v,u-v)\) on its two outgoing rails. The five occupied terminal sites of the abstract four-tick walk are two coordinate units apart. In the plotted orientation assign each direction word the terminal well \(j=(\#\mathrm{left\ program\ steps}-\#\mathrm{right\ program\ steps})/2\). This is an endpoint convention. The source and both probe operations are specified separately. A fair rotation coin can also be written as the Hadamard followed or preceded by a diagonal sign. For fixed counts of left steps and fixed final rail, the added signs are then common to all contributing paths (incoming counts differ from outgoing counts only by the initial and final rail). They do not affect these squared endpoint sums.

With all 16 words kept, the ideal blank probabilities at the five sites are \((1,10,2,2,1)/16\). Shifting one arm by five plotted wells and using both complementary retained arms gives \((1,6,2,6,1)/16\). The normalized left and right single-arm distributions are \((1,5,1,1,0)/8\) and \((0,1,1,5,1)/8\). The integer panel gives \(K=3/2\), total variation \(1/4\) and two-site odds ratio 5. These are ideal model values. The measured counts and both estimates of statistical uncertainty above are separate data. [All word signs, endpoint ports and displaced masses](results/cesium_negative_read.json)

A marker model that assumes one common undisturbed terminal random variable under the complementary negative reads requires the pooled and blank population laws to agree, given faithful response and matching preparation. A marker coupled to the entire signed field can give different final laws when moving one arm changes the guide in which the other subsequently propagates. In particular the experiment puts the removed arm in a spatially disjoint set of wells. A competing splitter that changes its routing only when **two pointer sectors occupy the same site** can agree with the ordinary law throughout each retained flight. Testing this remaining freedom needs an instrument in which both sectors actually reach the same splitter. The four positive detector readings in the [joint-sector control](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/21) give ratios 1 and \(6/5\) for two such laws. Those are predictions for a different measurement. The empirical comparison constrains transfer from a bare walk to a physically displaced arm; it leaves the physical origin of the marker, the squared detector law, the clock and the full quantum-to-classical map open.
