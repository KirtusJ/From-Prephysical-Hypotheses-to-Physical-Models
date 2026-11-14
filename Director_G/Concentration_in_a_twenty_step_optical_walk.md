# Concentration in a twenty-step optical walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

How well does a sharp-source walk select a probability rule at flight lengths already measured? Cheng and colleagues measured the concentration of the position distribution at steps 0 through 20 in a time-multiplexed optical walk. At step four their reported concentration is **0.40854**. Applying any power \(q\ge2\) to the ideal signed walk gives at least **0.79531**, even allowing the detector to pool or resolve its two rails differently at every site and on every launch. The ideal ordinary law gives **0.42969**, also above the authors' upper plotted counting-error cap of **0.41305**. The experiment provides a quantitative discrepancy for strong powers and a measurable calibration requirement for the ordinary law. [Cheng et al., revised primary figure 6(d), page 9](https://arxiv.org/pdf/2503.06460v2#page=9) · [Journal article](https://doi.org/10.1103/7m2n-9vmf) · [Sharp-source velocity law and its different binning limits](Which_probability_powers_preserve_the_classical_velocity_law.md)

## Preparation, apparatus and observable

The source is an attenuated pulsed laser prepared at one time bin with horizontal polarization. A half-wave plate implements the balanced coin. Different fiber delays encode the two shifts. The authors use two avalanche photodiodes, measure polarization projections in the time bins, and normalize their counts. They report that per-step H and V losses initially differed by about 3% and describe an optical compensation for the nominal setting \(\gamma=0\). This is an optical implementation of the walk. Relating its detected light to the ideal amplitudes requires the preparation, relative path transmission, timing and relative detector response. The early and revised preprints give different H/V fiber assignments. The comparison uses the spatial orientation printed in the plots and verifies both polarizations against the signed recurrence. [Experimental section and revised Fig. 6](https://arxiv.org/pdf/2503.06460v2#page=5) · [Earlier experimental section and Fig. 4](https://arxiv.org/pdf/2503.06460v1#page=6)

For the revised figure use \(C_t=\sum_x P_t(x)^2\), computed **after accumulating the observed position histogram**. The early preprint labels the reciprocal quantity IPR. Each blue square in revised Fig. 6(d) is a measured concentration at \(\theta=45^\circ,\gamma=0\). Its blue line is the authors' numerical calculation. All 21 blue squares are retained. No separate horizontal line caps are painted for the blue points at ticks 0 and 7. A full endpoint histogram was located at tick 20 only. These records contain normalized graphical values. Event-level counts, coincidence records and histogram covariance are unavailable in the two source archives. [All concentration markers, visible caps and theory line](results/cheng_concentration.csv) · [Revised figure source](https://arxiv.org/src/2503.06460v2)

## A bound that survives mixtures and local rail choices

Write \(h_{xr}\) for the squared ideal amplitude at site \(x\) on rail \(r\), with \(h_x=\sum_rh_{xr}\). At each site the detector can either raise \(h_x\) to \(q\), or raise the two rail masses separately and add. Normalize the weights over all sites on that launch. The site partition and exponent may vary across launches. The bound permits their mixture, with common ideal kinematics and outcome-independent acceptance on every launch. It does not cover pooling different sites before powering, mixing amplitudes in another rail basis, or unrestricted additional resolved labels.

Suppose a fixed site \(s\) contains a rail of mass \(m\) at least as large as every other site mass. For \(q\ge2\) the weight at \(s\) is at least \(m^q\), while each outside weight is at most \(h_x^q\le m^{q-2}h_x^2\). The same site then has probability at least

\[
L=\frac{m^2}{m^2+\sum_{x\ne s}h_x^2}
\]

on each launch and in the aggregate. For \(n=t+1\) accessible wells, Cauchy–Schwarz gives \(C_t\ge p^2+(1-p)^2/(n-1)\) at \(p=P_t(s)\). This expression increases on \([1/n,1]\), so substitute \(p=\max(L,1/n)\). At ticks without such a rail the table uses the unconditional \(1/n\) floor. At \(q=\infty\) the same statements follow by taking the limit of a finite power on each chosen partition. At \(t=0\) every choice has concentration 1.

| Tick | Plotted center | Plotted caps | Ordinary ideal | Lower bound for every \(q\ge2\) mixture |
|---:|---:|---:|---:|---:|
| 3 | 0.42670 | 0.42553–0.42808 | 0.43750 | 0.71745 |
| 4 | 0.40854 | 0.40455–0.41305 | 0.42969 | 0.79531 |
| 7 | 0.20397 | — | 0.22803 | 0.12500 |
| 20 | 0.09558 | 0.09250–0.09901 | 0.13746 | 0.22775 |

The \(q\ge2\) floor is above the upper painted cap on 15 clocks. Ticks 0, 1, 2, 7, 13 and 19 do not supply that comparison. These cap comparisons are descriptive. The underlying samples and a simultaneous coverage interpretation are unavailable. [All 21 clocks, including weak bounds and missing caps](results/cheng_walk.json)

**The ordinary ideal also misses.** At tick four the two rail masses, in sixteenths and ordered left to right, are \((0,1),(1,1),(1,1),(9,1),(1,0)\). For every \(q\ge1\) the least possible probability at \(+2\) is

\[
\frac{9^q+1}{9^q+1+2\cdot 2^q+2}\ \ge\ \frac58 .
\]

Splitting the peak and pooling the other sites attains the fraction. The inequality follows from \(9^q\ge(9/2)2^q\) and \(2^q\ge2\). Thus even a mixture supported on \([1,\infty]\) has \(C_4\ge109/256=0.42578125\). This exceeds the upper cap. At \(q=1\) the actual prediction is \(55/128\). The measured concentration alone therefore cannot identify the ordinary exponent. An independent reference for experimental broadening is needed to compare more closely.

**Size of a terminal response change.** Suppose relative detection efficiencies lie in a common ratio \(G=\max g/\min g\), with positive efficiencies, and only terminal selection changes the ideal distribution. A peak probability at least \(p\) can have its odds reduced by at most a factor \(G\). This bound holds per launch and under mixing. On \(n\) sites, concentration at most \(c\) requires every site probability to be at most \(u=(1+\sqrt{(n-1)(nc-1)})/n\). Hence \(G\ge[p/(1-p)]/[u/(1-u)]\) when \(p>u\). At tick four the plotted upper cap requires \(G\ge1.053\) for the \(q\ge1\) bound and \(G\ge5.117\) for the \(q\ge2\) bound. At tick twenty \(q\ge2\) requires \(G\ge2.334\). These are necessary ratios for this terminal mechanism. The experiment's precompensation per-step loss is a different quantity. Source errors, changes to propagation and background counts require separate models.

## What the early endpoint graph adds

At tick 20 choose the central half-speed event \(A=\{|x|\le10\}\). Put \(M=\max_{x\in A}h_x\), \(a=\sum_{x\in A}h_x^2\) and \(b=\sum_{x\notin A,r:\ h_{xr}\ge M} h_{xr}^2\). At every \(q\ge2\) the inside weight is at most \(M^{q-2}a\) and the outside weight is at least \(M^{q-2}b\). The resulting upper bound \(a/(a+b)=21691630560/109192894721=0.198654\ldots\) survives any mixture of the allowed local partitions and powers. The ordinary mass is 0.417084.

In v1 Fig. 4(a), the caption describes the black squares as total and gray as V. The legend inside the graph labels black as H. Reading black as total gives a graphical inside sum of 0.432430 and an all-site sum of 1.017144, hence a rescaled share of **0.42514**. Reading black and gray as separate components gives 0.590801 and 1.303839, hence **0.45312**. Both exceed the powered ceiling. At \(x=-20\) the plotted total under the caption reading is about zero while V is 0.00485. Axis clipping and plotted quantization put two marker centers just below zero when reconstructed. All centers and painted caps are retained as read. Neither interpretation supplies a normalized raw count table. [Early Fig. 4(a), page 7](https://arxiv.org/pdf/2503.06460v1#page=7) · [Full digitization of all 21 sites](results/cheng_positions.csv)

Squaring the rescaled site values and summing gives 0.12076 under the caption reading and 0.11018 under the legend reading. Both differ from the revised time-series value of 0.09558. The revised Fig. 4(d) uses H readout for an H input and V readout for a V input. Combining these preparations would change the observable. The time series and early histogram consequently remain separate records from the same paper. [Revised Fig. 4(d)](https://arxiv.org/pdf/2503.06460v2#page=7)

## Replay

From the repository root run `python Director_G/check_cheng_walk.py`. It checks the exact signed-step recursion against a second calculation counting words by their runs of V steps. The largest deviation between exact site weights and early theoretical bar heights is 0.000068. The largest deviation between exact concentrations and the revised theoretical line is 0.000138. These comparisons validate the orientation and axes on the numerical traces.

To regenerate both CSV files, give `python Director_G/read_cheng_figures.py V1.tar.gz V2.tar.gz` the two arXiv source archives. The decoder needs PyMuPDF and checks the SHA-256 digest of each original vector panel. It measures the fixed-size squares from the uncut vertical edge at a clipped boundary, locates error caps by abscissa and uses the axis ticks to convert PDF coordinates. Blank cells indicate an absent cap. Six decimal places preserve the extracted geometry, with fewer significant figures justified by drawing precision. [Version-one source archive](https://arxiv.org/src/2503.06460v1) · [Version-two source archive](https://arxiv.org/src/2503.06460v2) · [Bound and recurrence checker](check_cheng_walk.py) · [Figure decoder](read_cheng_figures.py)
