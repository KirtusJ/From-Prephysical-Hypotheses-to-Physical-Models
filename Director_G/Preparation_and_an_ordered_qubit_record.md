# How much does the first reported bit tell us about the next?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

In a public experiment on Rigetti's Ankaa-2 processor, the same first hard-read value on qubit 50 predicted very different second-read frequencies depending on the preparation. Among first reads reporting one, the next read reported one in 23 of 328 trials after a nominal zero preparation and in 8,377 of 9,498 after a nominal one. Treating the first bit as a complete description of what the second detector will see loses this dependence. The program's proposal to choose a preparation from earlier hits depends on what persists between reads. These data supply an empirical test of that particular simplification. [Caune et al., Appendix E](https://arxiv.org/pdf/2410.05202) · [Original HDF5 with shot records and reference programs](https://zenodo.org/records/15364358) · [Adaptive preparations from pilot hits](Threshold_pilot_and_adaptive_preparation.md)

## Both preparations and all four outcomes

The two reference programs read qubit 50, wait 500 ns, then read it again. The nominal-one program applies an initial $R_X(\pi)$ pulse. The nominal-zero program starts with the device's baseline preparation. Write $P$ for that preparation label, $X$ for the first hard read and $Y$ for the second. Every stored row enters the table, including both disagreement directions. The file reports two hard read classes. It gives no separate leakage or unlogged-attempt category. The denominators below count archived experimental repetitions.

| Preparation | $X,Y=0,0$ | $0,1$ | $1,0$ | $1,1$ | Repetitions |
|---|---:|---:|---:|---:|---:|
| Nominal zero | 9,310 | 362 | 305 | 23 | 10,000 |
| Nominal one | 440 | 62 | 1,121 | 8,377 | 10,000 |

Consider a common stochastic readout that predicts $T_x=P(Y=1\mid X=x)$ for both preparations. At a given $x$, the smallest possible maximum absolute difference from the two empirical rates is half their separation. The midpoint achieves equality by giving equal errors on the two panels. At $x=1$ this error is $1{,}264{,}601/3{,}115{,}344$, or **40.59 percentage points**. At $x=0$ the rates are $362/9672$ and $62/502$, giving **4.30 points**. Pooling the two preparations yields $8400/9826$ following $x=1$, which conceals how poorly that value describes the nominal-zero panel. A separate single-read reference yielded 328 ones after nominal zero and 9,466 ones after nominal one in 10,000 trials per panel. These separate runs cannot be paired shot by shot.

The empirical bound is an arithmetic property of the stored tables. To infer a population bound, suppose the shot pairs are independent and identically distributed within each reference panel. Conditional on the four observed first-bit denominators, the four second-hit proportions have simultaneous Hoeffding half-widths $r_n=\sqrt{\log(160)/(2n)}$ at coverage at least 95%, by a union bound. Subtracting both half-widths from the measured gap and halving leaves a lower bound of **35.37 percentage points** at $x=1$, rounded down. The corresponding bound at $x=0$ is zero. Drift and serial dependence would require a different sampling analysis. [Hoeffding's probability inequalities](https://doi.org/10.1080/01621459.1963.10500830)

A classical model reproduces every cell. For preparation $p$, draw $X$ with the observed first-hit rate in that panel, retain $(p,X)$, then draw $Y$ with its corresponding conditional rate in the table. The same operation can be realized by drawing a complete pair from the panel frequencies at preparation and revealing its bits in order. Consequently these data alone cannot locate the missing predictive information in a qubit, a detector or a pre-existing record. The experimenters infer post-measurement populations using additional readout-confusion, relaxation and Markov assumptions. [Experimental calibration model, Eqs. E1–E3](https://arxiv.org/pdf/2410.05202)

## A recorded outcome controls an actual later operation

The same archive contains eight further circuits with 1,000 repetitions each. After 2 through 9 rounds of stabilizer measurements, a decoder uses the earlier outcomes to choose an $X$ pulse on qubit 50 (raw decoder code 1) or an equal-duration idle (codes 0 and 2). The last two hard reads on that qubit bracket the feedback step and its associated delays. Writing $L=1$ for a commanded pulse and 0 for idle, the simple prediction $Y=X\mathbin{\mathrm{xor}}L$ matches **5,223/8,000** recorded rows. In order of increasing round count the numerators are 746, 718, 703, 626, 617, 631, 583 and 599. The result file retains each ordered triple and separates all three raw codes at every round count. These are different circuit panels, not eight successive trials on one qubit. [Feedback sequence, Appendix D and Supplementary Fig. 4](https://arxiv.org/pdf/2410.05202) · [All counts](results/caune_feedback.json)

The pulse creates a physical link from earlier records to a subsequent operation. The decoder selected the action using the same trial's syndrome. Comparing these branches therefore does not supply independently randomized pulse and idle interventions at matched histories. The reference counts reject a common first-bit-only prediction under the sampling conditions above. They leave disturbance, detector memory and persistent preparation compatible, as well as the walk's own probability embedding open.

## Reproduce the counts

Download the 5.6 MB `fast_feedback_raw_data.h5` from [Zenodo record 15364358](https://zenodo.org/records/15364358). With Python and `h5py` installed, run `python -B check_caune_feedback.py /path/to/fast_feedback_raw_data.h5 replay.json` from this directory. The checker verifies the file's SHA-256, both double-read programs, read classes and denominators before writing the tables. [Checker](check_caune_feedback.py) · [Archived replay](results/caune_feedback.json)
