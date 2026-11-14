# Can a fixed binary gain explain repeated parity records?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Makihara et al. published 8,447 trajectories with 294 successive reads of the same mechanical mode. Four blocks of these reads violate an equality required of a single fixed binary response with conditionally independent blocks. The original walk uses a persistent choice between count and square to explain a particular repeat-success excess. In the measured apparatus, attributing temporal correlations solely to that sort of binary choice would miss their dependence on the interval between reads. [Original experiment, including apparatus and independent spectroscopy](https://arxiv.org/html/2610.10714v1) · [Deposited trajectories](https://zenodo.org/records/20944616) · [Walk repeat experiment and its assumptions](Repeating_a_position_record.md)

## Which launches and detector are represented

A weak coherent displacement prepares the mechanical mode. A dispersively coupled superconducting qubit interrogates phonon parity and is conditionally reset after readout. A check takes about 12 µs. Six successive excited qubit reports herald a preparation. The archive then keeps 294 further binary qubit reports from each accepted trajectory. In a separate spectroscopic measurement the authors found single-phonon population 0.846 after six excited reports, with reported bounds 0.807–0.885. A one-shot parity assignment has mean fidelity 0.68, so a reported one is an excited **qubit** read, not an independently observed phonon. The authors also report a 649 µs effective energy lifetime under monitoring and about 1.3% demolition per check. [Preparation, spectroscopy and measurement backaction](https://arxiv.org/html/2610.10714v1) · [Spectroscopy (Figure 3) data](https://zenodo.org/records/20944616/files/figure_3_data.csv)

The trajectory CSV begins after the six herald reads. Every one of its 2,483,418 subsequent outcomes is represented in the replay, including the full trajectory extremes of 54 and 224 excited reports. The file supplies no trajectories for failed heralds and no original-attempt denominator. All temporal moments below are for the accepted preparations. An unsuccessful initial preparation cannot be reconstructed by adding a synthetic all-zero row. [Original CSV](https://zenodo.org/records/20944616/files/post_selected_trajectories.csv) · [Per-check and whole-trajectory totals](results/phonon_repeats.json)

## One fixed bit versus four time blocks

Before reading the trajectories, we fixed four 16-read blocks, numbered from the first post-herald check: 1–16, 17–32, 97–112 and 113–128. The two pairs of adjacent blocks are separated by 64 intervening checks (about 768 µs). Each block mean \(Y_i\) is an excited-report fraction on a single trajectory. Let \(C_{ij}\) denote their across-trajectory covariance at distinct times.

In the proposed alternative, each accepted trajectory has a fixed \(H\in\{0,1\}\). Relative to this post-herald population, let \(p=P(H=1)\) and \(d_i=E[Y_i\mid H=1]-E[Y_i\mid H=0]\). The class-conditional block means can change arbitrarily with time, and fluctuations inside each block can be arbitrarily correlated. If distinct blocks have zero conditional covariance given \(H\), total covariance gives \(C_{ij}=p(1-p)d_i d_j\). Thus the following tetrad vanishes:

\[
D=C_{12}C_{34}-C_{13}C_{24}=0 .
\]

The statement covers fresh independent gains by setting all cross-block covariances to zero. Conditioning on an earlier herald can reweight \(p\); the hypotheses about block covariance must still hold in the selected ensemble. This test directly addresses the measured block means and does not assume a particular parity-read confusion matrix. Vanishing tetrads have a long history in one-factor models. The displayed two-state derivation does not require Gaussian observations. [Background on tetrad constraints and singular nulls](https://academic.oup.com/jrsssb/article/86/4/987/7624096)

| Block | Checks | Mean excited fraction |
|---|---|---:|
| 1 | 1–16 | 0.583676 |
| 2 | 17–32 | 0.504321 |
| 3 | 97–112 | 0.366032 |
| 4 | 113–128 | 0.352795 |

With empirical covariance denominator 8,447, the adjacent entries are \(C_{12}=0.020545\) and \(C_{34}=0.021258\). The distant entries in the second product are \(C_{13}=0.003793\) and \(C_{24}=0.006652\). We obtain \(D=0.000411505\). Treating trajectories as independent draws from this cohort, first-order propagation over whole trajectories gives standard error 0.000013187 and an approximate individual 95% interval [0.00038565, 0.00043736], rounded outwards. For example, each covariance influence contribution is \((Y_i-\bar Y_i)(Y_j-\bar Y_j)-\widehat C_{ij}\); the product rule gives the influence of \(D\). This is a local, large-sample interval, with no uniform null tail guarantee near singular covariance models. Contiguous quarters of file order give 0.0003922, 0.0004485, 0.0003853 and 0.0004104. Their consistency does not establish independence across trajectories or reconstruct unavailable wall-clock timestamps. [All six covariances, quarter estimates and counts](results/phonon_repeats.json)

## What remains physically ambiguous

A time-varying mechanical parity can correlate nearby blocks more strongly than distant ones. The authors' transition and measurement model evolves the phonon distribution between checks, and their independently resolved number spectra provide evidence about the physical carrier. A detector state with its own dynamics or several persistent response components can also yield nonzero \(D\). For example, assign independent fair binary values \(A,B\) at launch and set \(Y_1=Y_2=A\), \(Y_3=Y_4=B\). This entirely static four-class model has \(D=1/16\). It illustrates a surviving alternative and does not fit the observed marginals. To localize correlations to the detector, one would need control preparations or an independent probe of the same evolution. [Forward model and measurement assumptions](https://zenodo.org/records/20944616/files/forward_backward.py)

For the walk's sharp-return repeat test the construction gives a specific two-component repeat probability under a stipulated product-event law. A matched physical implementation could measure the four block covariances as a check of the additional fixed-gain, conditionally uncorrelated interpretation. Each block's observed statistic and the treatment of failed continuations must be specified on the same original launches. Intrinsic carryover through the prepared state can itself violate the interpretation. The independent-launch comparison requires newly prepared systems sharing a detector type, whereas these trajectories repeatedly probe one evolving resonator. No probability exponent or mixture weight for the walk can be inferred from this experiment. [Paired-launch site-score predictions](Fluctuating_site_scores_and_paired_launches.md)

Run `python Director_G/check_phonon_repeats.py post_selected_trajectories.csv output.json` with Python 3.11 or newer. The checker verifies the original archive MD5, reports its SHA-256, reads every binary column and holds all finite-sample comparisons at the trajectory level. [Replay checker](check_phonon_repeats.py)
