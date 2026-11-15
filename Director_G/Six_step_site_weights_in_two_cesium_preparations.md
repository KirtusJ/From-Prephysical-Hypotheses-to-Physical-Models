# Six-step site weights from two cesium preparations

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Karski reports seven final wells for each of two six-step walks on individual cesium atoms. At the wells two lattice periods to either side of the launch, the ratio of right-to-left odds for the spin-one preparation to those for a symmetric preparation is **2.52**. With the published ideal dynamics and a spin-blind response at each well, ordinary probabilities give **2.60**. Squaring each site population before normalization gives **6.76**. Squaring the two spin populations separately before pooling gives **7.63**. Unknown spin efficiencies materially weaken this comparison. [Karski, Fig. 6.3 and §§6.2–6.3](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/thesis/phd/michal-karski-phdthesis.pdf#page=200) · [Karski et al., *Science* 325, 174–177](https://doi.org/10.1126/science.1174436)

## The reported sample

Each initial fluorescence image supplies a separate origin for each atom. The source loaded about eight atoms per sequence. Its transport analysis requires sufficiently separated initial atoms for an unambiguous assignment and discards atoms missing from the final image. Positions therefore refer to detected, assignable survivors. Figure 6.3 quotes approximately 800 realizations for each coherent distribution. It supplies normalized heights and statistical bars. It gives neither exact row counts nor a launch-by-launch ledger including discarded atoms. Shared sequence fluctuations can affect several atoms together. [Karski, §§4.5.3 and 6.2.2](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/thesis/phd/michal-karski-phdthesis.pdf#page=155)

Here \(j\) is displacement in units of the lattice period \(\lambda/2\). A walk step moves a spin component by half this distance. The table reads the blue histogram tops as plotted. The archive includes both caps for every bin, the red ideal curves, the dashed dephasing curves, and the green fair-path curve for the delayed run. The last row used a different microwave pulse and inserted 400 μs between each coin and shift. The added delay was intended to dephase the spin between steps. The experiment recorded the terminal position. [Figure coordinates and caps](results/six_step_atom_weights.json)

| Preparation | −3 | −2 | −1 | 0 | +1 | +2 | +3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| (a) Symmetric | .0846 | .2368 | .1570 | .1129 | .1116 | .1926 | .1042 |
| (b) Spin one | .0736 | .1290 | .1093 | .1363 | .1891 | .2641 | .0982 |
| (c) Delayed control | .0068 | .0771 | .2422 | .3423 | .2110 | .1069 | .0135 |

The source’s dashed thermal-dephasing curves give double odds of about 2.30 from the same drawing, compared with the ideal 2.60. This illustrates how changing the modeled dynamics can move the contrast at ordinary readout. Even the coherent outer wells reach .074 to .104, compared with the ideal \(1/64\) at each end. Karski discusses pulse error, inhomogeneous phase, drift and decoherence. The probability curves do not identify their separate contributions. Figure 6.4 gives distributions at 12 and 20 ticks for the symmetric input and widths through 24 ticks. Figure 6.5 gives separate spin projections for the six-tick symmetric input. The author found discrepancies up to 3.0 statistical errors when adding complementary projections and comparing with a separately measured position distribution. These are distinct runs. [Longer walks and spin analysis, Figs. 6.4–6.5](https://quantum-technologies.iap.uni-bonn.de/assets/pdf/thesis/phd/michal-karski-phdthesis.pdf#page=202)

## Which signed walk enters the comparison

In the source spin order \(0,1\) the coin of Eq. (6.9) is \(2^{-1/2}\left(\begin{smallmatrix}1&1\\-1&1\end{smallmatrix}\right)\). The ideal shift sends spin zero right on odd ticks and left on even ticks, with spin one moving the opposite way. This implements Eq. (6.8) at zero differential transport phase. The experimental shift can retain a spin-dependent phase. Substituting the standard fixed-direction Hadamard circuit without checking the signs or source preparation could change the interpretation. The checker propagates both real unit spinors through the six stated steps, then compares their position sums with the ideal curves printed alongside the data.

Let \(a\) be \((|0\rangle+i|1\rangle)/\sqrt2\) and \(b\) be \(|1\rangle\). For each site and spin put \(m_{jr}=|\psi_{jr}|^2\), \(w_j=m_{j0}+m_{j1}\). Since the ideal propagation is real, the two quadratures in \(a\) have no cross term in each mode. In units of \(1/64\), the populations at the two comparison wells are

| Input | Spin populations at −2 | Spin populations at +2 |
|---|---:|---:|
| \(a\) | (17, 1) | (1, 17) |
| \(b\) | (9, 1) | (1, 25) |

For detected frequencies \(f\) write \(D=f_{b,+2}f_{a,-2}/(f_{b,-2}f_{a,+2})\). With preparation-dependent brightness and a positive, spin-blind gain specific to each displacement, all four nuisance factors cancel. For the site law with weights \(w_j^p\), \(D=(26/10)^p\). For the rail law with weights \(\sum_r m_{jr}^p\), \(D=(1+25^p)/(9^p+1)\). Both formulas hold for positive \(p\). These site histograms test fixed alternatives given the stated dynamics and response. If the exponent or rule changes on every launch, frequencies mix the separately normalized rows before the double odds are formed. The displayed power formulas then need not hold. The six-step comparisons do not measure the separately proposed [seven-tick score for fresh powers](Seven_free_ticks_and_one_position_read.md), a pooled binary flag, or a spin-selective read on each incident. The earlier three-tick comparison uses a different experiment with integer count bars. [Robens paired-site comparison](Three_step_site_weights_in_cesium.md)

## Fixed spin gains

Allow arbitrary nonnegative \(e_{jr}\) shared by preparations at each displacement and spin, with positive detected totals at the compared wells. Specify how a site law divides weight inside its site: \(t_{jr}=w_j^{p-1}m_{jr}\). For the rail law take \(t_{jr}=m_{jr}^p\). At fixed \(j\) the ratio of weighted sums for \(b\) and \(a\) is a convex combination of \(t^b_{jr}/t^a_{jr}\), weighted by \(e_{jr}t^a_{jr}\). Taking opposite extremes in the two wells gives attainable sharp bounds. Positive gains approach the boundaries when zero gains are excluded. If gain depends on absolute position, the two preparations also need comparable position-dependent exposures among their origins.

| Model on the ideal walk | \(D\), spin-blind | \(D\), fixed site-and-spin gains |
|---|---:|---:|
| Ordinary | \(13/5\) | \([1,25/9]\) |
| Square each site, ordinary spin split | \(169/25\) | \([13/5,65/9]\) |
| Square each rail | \(313/41\) | \([1,625/81]\) |

The observed 2.52 lies inside the rail-squared range and slightly below the site-squared lower endpoint 2.60. At the scale of the printed statistical bars, this small gap cannot resolve the latter under general fixed spin gains. For perspective, taking the four caps independently gives \(1.84\) to \(3.47\) for the geometric contrast. This sensitivity calculation uses the cap rectangle and has no assigned joint coverage. Fitting \(p\) or computing a count-based significance would require a supported model of incident sampling, dynamics and detector response.

## Replay

The [extractor and rational predictions](check_six_step_atom_weights.py) use Python and pdfplumber (independent replay with 0.11.9). Download the laboratory PDF linked above and run `python -B Director_G/check_six_step_atom_weights.py thesis.pdf fresh.json` from the repository root. The PDF SHA-256 is `6db91b0bc0fd99baeac4b435f97c90fc663d9884a82c5af3e319bd6610ddf7b0`. The extractor reads page 200 and calibrates the vertical scale against its printed major ticks. Each cap belongs to the horizontally centered blue bar. The ideal curve vertices in panels (a) and (b) differ from the signed calculation by at most 0.00011 in probability. The measured bars, which are separate vector paths, sum to between 0.99977 and 0.99979 in each panel before rounding to the table. This comparison checks graphic coordinates and the model convention. Four decimal places in the table describe the drawing and do not imply precision of the measured frequency. The reported ratios use the full extracted heights.
