# A mid-circuit mark and a later read in a superconducting qubit

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Independent analysis and computational replay with OpenAI Codex. Kenneth Rudinger and colleagues designed and conducted the experiment and deposited its records.

Can a same-launch diagnostic be treated as harmless to a later science read? In this experiment, giving a nominally ground-state qubit a dispersive measurement before two gates produced a strong delay dependence in the final read. At the shortest delay, the marked circuit returned 211 final ones in 1,024 repetitions, against 988 in the control. At the longest delay, the counts were 981 and 995. A position walk or a binary sensor for its scoring mode was never part of this apparatus. The data test the physical premise that an earlier read can be added without changing subsequent operations. [Primary experiment](https://arxiv.org/pdf/2103.03008) · [Primary data, version 1.0.2](https://zenodo.org/records/5146074) · [Same-launch detector marks](detector_marks.md)

## What the two circuits measure

The authors used a superconducting transmon on a five-qubit device. A 500 µs idle prepared the nominal ground state; $G_x$ is a $\pi/2$ rotation about the $x$ axis. The comparison holds the nominal preparation, gate pair and final $Z$ measurement fixed. One circuit starts with a 1 µs dispersive $Z$ measurement, written **(Iz)** in the deposited circuit label. The other starts with the gates. In an ideal ground-state preparation a projective $Z$ read returns zero and preserves the state, so two ideal $G_x$ gates produce the excited state in either circuit. Keeping both observed intermediate outcomes tests what the complete physical sequence actually did. [Experiment, pp. 2–4](https://arxiv.org/pdf/2103.03008)

For each reported delay $t$, take the **(Iz)GxGx** and **GxGx** rows from the corresponding data column. The former reports the ordered pair (intermediate bit, final bit). The experiment distributes its four counts in the order $(0,0),(0,1),(1,0),(1,1)$. The final-one numerator is the sum of the second and fourth counts. The control supplies only its terminal counts in the order $(0,1)$. Let $\Delta(t)$ be the marked-minus-control final-one count divided by 1,024.

| Run delay | Marked joint counts | Marked final ones | Control final ones | $\Delta(t)$ |
|---:|---|---:|---:|---:|
| 500 ns | 795, 200, 18, 11 | 211 | 988 | $-777/1024$ |
| 2,020 ns | 35, 961, 8, 20 | 981 | 995 | $-14/1024$ |

The difference $\Delta(500)-\Delta(2020)=-763/1024$ is descriptive. The [replay](check_observed_mark_disturbance.rs) emits all 39 delay rows with the four marked counts, both control counts and the signed difference. The series includes an exact tie at 1,180 ns and positive differences of $1,7,3,8$ counts at 1,260, 1,500, 1,900 and 1,980 ns respectively. Every delay is retained, including the late reversals.

The deposit also contains a **no-following-gates** comparison, **(Iz)** against the empty circuit **{}**. Its final-one counts at 500 ns are 45 marked and 30 unmarked, a difference of $+15/1024$. At 2,020 ns the corresponding counts are 44 and 22, a difference of $+22/1024$. Thus the sign and magnitude of the mark comparison depend on which operations follow it. The replay prints this control over all 39 run delays as well.

The delay is the time **after the measurement pulse** and before subsequent operations on marked circuits. It is a run label in the control columns. The no-mark circuit omits the pulse, and the source documents no duration-matched sham. The 92 control circuit histograms, considered together, differ at every pair of distinct run delays. The single **GxGx** control has 23 distinct count pairs across 39 runs. Thus the file does not simply reuse one common control vector. Within-shot pairing of the two bits is retained in the joint histogram. There are no per-shot time stamps or identifiers to pair individual marked and control repetitions or verify randomized pulse omission.

## What the discrepancy can reveal

This comparison measures the final outcome of a sequence containing the mark, two rotations and a terminal detector. It cannot allocate the discrepancy among state change during measurement, subsequent gate errors, elapsed time or drift. The authors' broader analysis attributes much of the short-delay error to residual cavity photons that shift the qubit's frequency during later gates. Their Stark-shift model explains much of the effect, with residual mismatch at the shortest delays. The count difference here uses two observed circuits and is a different quantity from their fitted instrument error or their maximum model discrepancy across circuits. [Primary mechanism analysis, pp. 3–5](https://arxiv.org/pdf/2103.03008)

For a walk detector, an analogous end-to-end comparison would retain all science outcomes after diagnostic-on and duration-matched diagnostic-off controls. A difference would falsify invariance for that exposed preparation and schedule. Agreement of ensemble means still allows opposite changes in unobserved response modes. These transmon counts supply an observed example of sequence dependence. They give no mode channel, half-mass calibration or probability-embedding result for the walk.

## Reproduce the complete curve

Download **2103.03008.zip** from the authors' versioned [Zenodo deposit](https://zenodo.org/records/5146074). Its recorded MD5 is **051eaf6d854425618260796b82f25c98**. Extract the following member directly, preserving its original bytes.

    2103.03008/data/PD192v1_QILGST_Q3_ZeroDrive_200515-final.txt
    SHA-256  2ce200cc68ab65f508429c5ae61ded7233ecf51b4cb2e87ce9a8b7ee110be972

The file includes 128 circuits and 39 groups of six outcome columns, one group for each run delay from 500 to 2,020 ns in 40 ns increments. Thirty-six circuits contain the mid-circuit measurement. The checker verifies the label of every column, the distinction between inapplicable fields and measured zeros, and a denominator of exactly 1,024 for every circuit and delay. Those 4,992 histograms represent 5,111,808 recorded circuit repetitions. Upstream hardware attempts are outside this count.

From this supplement's directory, run the following commands after checking the file digest. The checker reads the supplied count file offline. On Windows use the generated executable with its .exe suffix. Standard output contains the 39 data rows and their CSV header. The diagnostic summary goes to standard error.

    rustc --edition=2021 -D warnings check_observed_mark_disturbance.rs -o mark_replay
    ./mark_replay "path/to/PD192v1_QILGST_Q3_ZeroDrive_200515-final.txt"
