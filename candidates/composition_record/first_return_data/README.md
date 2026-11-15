# First returns in a monitored three-spin experiment

At a programmed gate angle of π/2, 1,170 shots returned on the first measurement, 1,671 on the second and 35,497 on the third. Another 630 of the 40,000 shots had no return within 20 measurements. This third-tick peak tests whether the click chance after survival can be constant from tick to tick, allowing that chance to vary across trials. The observed schedule conflicts with that premise.

[First-return counts for all 99 settings](first_returns.csv) come from the single-excitation preparation of Quancheng Liu, Sabine Tornow, David A. Kessler and Eli Barkai. They executed a kicked XX chain on IBM Sherbrooke and deposited full 20-bit outcome histograms. In the ideal single-excitation sector, the location of that excitation is a walker on three sites. We use the product preparation called `State_100` in the archive. The authors also released three other product preparations and an ancilla experiment. The table here concerns the single-excitation preparation only. [Paper, §VIII and Materials and Methods](https://arxiv.org/html/2401.09810v2#S8) · [Published article](https://doi.org/10.1073/pnas.2529694123) · [Original dataset](https://doi.org/10.5281/zenodo.18429670)

## What a clock tick means

The archived QASM excites `q[0]` with an X gate. Each tick applies RXX then RYY on sites (1,2), then RXX and RYY on (0,1), then measures site 0. The sequence writes `c[0]` through `c[19]` in that order. The CSV gives both the numerical JSON field `J` and the literal QASM rotation argument. The 99 actual angles range from π/50 to 99π/50 in steps of π/50. The paper uses a simulated sampling interval τ and writes its rotations with argument −τ. Here π/2 refers to the archived positive gate argument, in radians. A measurement index counts completed rounds. Physical time in seconds cannot be reconstructed from these columns. [Authors' data guide](https://zenodo.org/api/records/18429670/files/Readme.txt/content) · [Paper, quantum computer implementation](https://arxiv.org/html/2401.09810v2#Sx1.SSx2)

The first hit is the earliest recorded 1. In a Sampler count string, `c[0]` is the rightmost bit. The measured string `10110110110110110100` occurs 532 times in the π/2 job `cxs874c0v1500080bdv0`. Its suffix `100` puts all 532 counts in tick 3 regardless of the later outcomes. Summing all strings ending in `1`, `10` and `100` gives 1,170, 1,671 and 35,497 respectively. The all-zero string supplies the right-censored count. The paper's windowed mean divides by the number of detected shots. Our per-shot probabilities divide by all 40,000 shots. [IBM's string convention](https://quantum.cloud.ibm.com/docs/en/qiskit/bit-ordering#strings) · [Paper, §VIII](https://arxiv.org/html/2401.09810v2#S8)

## Stationary mixture check

Suppose each shot draws a chance $a\in[0,1]$ and its conditional chance of a click, given survival and $a$, stays equal to $a$ at every round. Then the first-hit masses $f_t=E[a(1-a)^{t-1}]$ decrease weakly. The survival probabilities $s_t=E[(1-a)^t]$, with $s_0=1$, satisfy $s_t^2\leq s_{t-1}s_{t+1}$ by Cauchy–Schwarz.

At π/2, the three empirical survival fractions are 0.97075, 0.928975 and 0.04155. Hence $s_1^2-s_2=0.0133805625$ and $s_2^2-s_1s_3=0.822659888125$ for the empirical fractions. In the ideal circuit the paired π/2 rotations swap an excitation across an occupied link up to phase. A whole round carries site 0 to 1, 1 to 2 and 2 to 0. This accounts for a return at tick 3 with an ideal detector. The same return schedule occurs in a deterministic classical three-cycle.

The CSV retains all 20 first-hit counts, the no-hit count and all 19 signed differences (later count minus earlier count) for every setting. The 3,960,000 device shots give 3,873,150 first hits and 86,850 censored observations. Across 1,881 adjacent comparisons the later count rose 680 times, fell 1,154 times and tied 47 times. Small fluctuations are retained alongside large effects.

Under independent, identically distributed shots within a setting, the count $b$ in the later of two adjacent bins, conditional on their combined count $m=a_0+b$, is binomial. Under the weakly decreasing null its success probability is at most 1/2. For $b>m/2$, a one-sided Chernoff bound after Bonferroni adjustment is $\min(1,1881\exp[-b\log(2b/m)-a_0\log(2a_0/m)])$, using natural logarithms and $0\log0=0$. At π/2 it gives an adjusted bound below $10^{-16}$ for ticks 1–2 and below $10^{-8225}$ for ticks 2–3. The adjustment covers all 99 settings and all 19 adjacent pairs in this file, including comparisons sharing bins. Shot order and inter-shot dependence cannot be diagnosed from the archived word counts. The counts and empirical contrasts do not require the independence assumption.

This record challenges the use of a time-independent conditional click chance for this evolving system. Every finite first-hit histogram admits a time-dependent classical hazard $h_t=f_t/s_{t-1}$ wherever $s_{t-1}>0$. In particular, these times alone cannot select the ordinary probability embedding. A direct-versus-split comparison would require its own physical intervention, resolved output labels and an independent check of the post-survival preparation.

## Reproduce the table

Download the [original State_100 JSON](https://zenodo.org/api/records/18429670/files/Experiment_Data_Heisenberg_State_100.json/content). It is a 57,271,744-byte JSON file and requires no archive extraction. The [Python adapter](extract.py) checks its source digest, verifies the preparation and all 1,980 serial measurement assignments in the QASM text, and extracts the raw word multiplicities. It treats QASM and embedded QPY as inert data. The [Rust reducer](check.rs) decodes each first hit by trailing zero bits, checks it against string indexing, enforces one total per job, and emits the CSV with LF line endings. Both commands require unused output filenames. Use temporary paths for the intermediate and rebuilt files.

```sh
rustc --edition=2021 -O check.rs -o check
python extract.py Experiment_Data_Heisenberg_State_100.json word_counts.tsv
./check word_counts.tsv rebuilt.csv
python -c "from pathlib import Path; assert Path('rebuilt.csv').read_bytes() == Path('first_returns.csv').read_bytes()"
```

On Windows use `-o check.exe` and `.\check.exe`. The original JSON has SHA-256 `2ea7433dc7e4a00ec203af9e84690ce2f915966dbe12ae1079be6d0e071ce3d4`. The authors' `Readme.txt` has SHA-256 `75d133a35f79a77395837467cb0b7f2f0a23517ad641a2a78b6d567a5dff4a59`. The derived CSV has SHA-256 `d2f2d7aca97a70de0c75533dbf9b2c5b59b856af89a7b6b0b63914dd932a74f4`. The dataset is licensed under CC BY 4.0. The first-hit regrouping and adjacent differences are derived from the authors' published histograms. [Dataset and license](https://zenodo.org/records/18429670) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
