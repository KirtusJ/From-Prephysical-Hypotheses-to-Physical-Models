# What six measured optical outputs say about a probability power

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Webb and colleagues measured all six terminal modes for four single-photon preparations. Even these 24 numbers cannot distinguish a detector that squares each ideal site population from the ordinary detector if each output has an unknown, stable efficiency. In fact **every finite positive power attains the same smallest worst-row error of 3.258%** on the rescaled published table. This is an exact descriptive result for the specified apparatus model. One exchange of two occupied optical modes before detection would remove the ambiguity for a fixed exponent. [Experimental article, especially Fig. 3 and Appendix B, Table IV](https://doi.org/10.1103/PhysRevResearch.5.023094) · [Full measured rows and printed uncertainties](results/six_port_gains.json)

## A stable gain can absorb the whole exponent

The interferometer prepares four choices of relative sign and implements a six-outcome measurement for state elimination. In its ideal input-output table, a port has either zero weight or a weight that depends only on the **port**. Write \(b=\sqrt2-1\); that positive weight is \(m_j=b\) on A–D and \(m_j=b^2\) on E and F. Each preparation occupies two of the first four and one of the last two, with \(2b+b^2=1\). In order \(++,+-,-+,--\), the bright triples are CDE, BDF, ACF and ABE. A source herald, six photon outputs and a 1 ns coincidence window define the measured signals. The authors report an average interferometer visibility of 97.7%; Table V measures polarization contrast at each port. Contrast compares maximum and minimum response and does not establish relative transmission or detection efficiency across ports. [Apparatus, probabilities and contrast definitions](https://arxiv.org/abs/2207.00019)

For an occupied port the signal yield is proportional to \(g_jm_j^q\), where \(q>0\) is fixed, \(g_j>0\) is constant across preparations and each preparation may have its own exposure or normalizer. The law on the six detected ports is obtained by summing the products over that preparation's occupied ports and dividing. For any \(q'\), taking \(g'_j=g_j m_j^{q-q'}\) produces exactly the same probabilities in all four rows. An overall rescaling of the gains lets every efficiency lie below one. Generalizations that constrain the maximum gain ratio, independently characterize the interferometer, require known absolute efficiencies or measure background have different identifying power.

| Preparation | Printed A–F sum (%) | Printed wrong total (%) | Normalized mass at ideal-dark ports (%) | TV error at attaining gains (%) |
|---|---:|---:|---:|---:|
| ++ | 100.06 | 3.3(2) | 3.25805 | 3.25805 |
| +− | 99.14 | 3.0(2) | 2.15856 | 2.79132 |
| −+ | 100.03 | 2.5(2) | 2.52924 | 3.14751 |
| −− | 99.94 | 2.6(2) | 2.64158 | 2.90328 |

We divide each of the four printed rows by its own printed sum for this comparison. The +− row's dark entries add to 2.14% before rescaling; the independently printed total is 3.0%. The source does not identify a correction. The calculation retains the two numbers and treats only the six reported port entries as its observed distribution. Every ideal powered model predicts exactly zero on the three nominally dark ports. Its total variation from the first measured row must therefore be at least \(326/10006\). Set the products \(g_j m_j^q\) proportional to \((210,190,220,200,94,86)\) in port order. For each input, normalize just the three occupied entries. The four resulting distances are in the table and attain the lower bound on the worst row. The fractions use the reported decimal values; limited counts, drift and rounding affect their physical precision. The authors' uncertainties are three standard deviations under their Poisson model. This calculation uses no inferred integer counts and supplies no confidence interval. [Exact arithmetic replay](check_six_port_gains.py)

## Which additional connection breaks the equivalence?

Retain the ++ preparation and detect C and E. In one setting use the original wiring. In a second, interchange the two outgoing modes *before* the same physical detectors and their unknown gains while keeping the launch and upstream transfer fixed. The ratio \(R\) of the C:E yield odds in the first setting to the same detector odds in the swapped setting is

\[
 R=\left(\frac{b}{b^2}\right)^{2q},\qquad
 q=\frac{\log R}{2\log(1/b)} .
\]

Both setting exposures and both gains cancel. Ordinary and squared weighting predict approximately 5.828 and 33.971, respectively. The port swap was not part of the reported table. A physical permutation with independently calibrated insertion loss is required; relabeling a saved file would also exchange its detector gains. The port masses require independent preparation/transfer calibration, and dark leakage and signal backgrounds must be measured or bounded in both settings. The odds ratio estimates a fixed exponent under these hypotheses. A varying exponent across launches requires a different identification argument.

For a direct coherent *refinement* experiment, leave a reference port of mass \(a>0\) unchanged and use a coherent splitter on another port of mass \(c>0\) to create two distinguishable outgoing cells of mass \(c/2\). With calibrated transmission, both daughter ports collected and corrected for their efficiencies, the ratio of the branch-to-reference odds after and before the split is \(2^{1-q}\). Adding the daughters' observed counts in software occurs after powering; their observation implements a different law from a device that already pools them as one physical cell before powering. The latter predicts an odds ratio of one at every \(q\). Webb et al. identify distinct path and polarization outputs; their four acquisitions use the same six-mode analyzer and do not supply this before/after measurement. [Walk implementation with finer and coarser terminal instruments](Which_probability_powers_preserve_the_classical_velocity_law.md)

## Why a five-path interference bound answers another question

Kauten and colleagues randomized 32 open/closed shutter combinations in five interfering paths. For heralded single photons they reported detector-corrected third-, fourth- and fifth-order Sorkin parameters, in units of \(10^{-3}\), of \(0.0\pm1.6\), \(0.6\pm1.8\) and \(-2.7\pm2.9\), respectively. They treated the dead times of the herald and output detectors together. Their Fig. 2 says extreme outliers were already removed from its classical-light mean powers. The results measure inclusion–exclusion across different coherent aperture settings at a recombined output. The absolute scale and which other cells enter a postulated normalization matter for interpreting them as limits on an exponent. [Kauten et al., Table II and heralded-detector analysis](https://arxiv.org/pdf/1508.03253)

For example, take three equal *aligned* amplitudes and a single unnormalized output proportional to the \(q\)th power of its ideal intensity. At \(k\) open paths the score is proportional to \(k^{2q}\). Its raw third-order difference \(3^{2q}-3\,2^{2q}+3\) vanishes both at \(q=1/2\) and at \(q=1\). At the former value the pairwise differences vanish too, so a normalized Sorkin parameter with those differences as denominator is undefined. Measured pairwise interference supplies information beyond that raw null. These illustrative equal-path numbers do not model Kauten et al.'s measured apparatus. Extracting \(q\) from a real multipath panel would require its phases, gains, acceptance and normalization model.
