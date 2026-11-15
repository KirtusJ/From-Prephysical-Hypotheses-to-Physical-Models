# What the encoded cycle histograms measure

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Wadhia, Chancellor and Kendon deposited the programs and measured position distributions of four- and eight-node walks implemented on IBM’s Quito processor, alongside finite-shot simulator results. At tick three of the eight-node walk, the simulator frequencies at sites \(1,3,5,7\) were \(372,125,127,376\) per thousand. Measuring position at each tick predicts \(375,125,125,375\); a coherent terminal-only Hadamard walk predicts \(125,125,125,625\) in the deposited coordinate convention. The hardware also reported 545 of that row’s thousand outcomes at sites with the wrong parity for either ideal walk. This limits what the physical record can establish about a terminal probability power. [Wadhia et al., sections 2–3 and Figs. 3, 6](https://doi.org/10.1140/epjd/s10053-023-00795-2) · [Authors’ data and code](https://doi.org/10.15128/r15x21tf47n)

## The record and the circuit

The article describes restarting the walk at each chosen endpoint and measuring the register. The deposited eight-node program also contains three position measurements **inside** its loop over ticks. Each pass writes the same three classical bits, and none of the intervening operations depends on those bits. The code specifies no conditional reset. Overwriting the classical result leaves only the last position in a returned histogram. It does not restore coherence lost to earlier measurements. The archive provides source code and aggregate tables. It includes no executed circuit job IDs, transpiled circuits or per-shot histories that could establish what a particular hardware run executed. The deposited four-node example measures only at its end and uses its own gate sequence. [Programs and workbooks in the archived ZIP](https://researchdata.durham.ac.uk/downloads/r15x21tf47n)

The two workbooks label separate sheets `Simulator` and `ibmq_quito`. Their entries are normalized frequencies. Both source programs request 1,000 shots. Multiplying each entered frequency by 1,000 recovers an integer to the spreadsheet’s floating-point precision, and every row sums to 1,000. We report these integer equivalents for all sites and steps, including the listed step-zero preparation. They do not identify missing individual jobs, bit-string order within a job, lost physical launches or time correlations. The data are processor readouts from a digital encoding. There is no separately manipulated sheet variable or crossable physical ring edge in this record. [All 4- and 8-node rows](results/encoded_cycle_measurements.json)

## A test of measurement timing

Positions are encoded in three bits, with `qr[2]` the low bit in the reported number. For coin zero the step decrements the position modulo eight, and for coin one it increments it. The ideal update first applies \(H\) to the coin. The source’s multi-controlled gate expansion also needs checking: its recursive branch applies the gates CRZ, CU, a smaller controlled flip, inverse CU, that smaller flip again, and inverse CRZ. Direct multiplication gives the intended position permutation. Relative to a plain shift the extra phase is \(+i\) on the decrements from 2 and 6 and the increments from 1 and 5. All other basis shifts have phase 1. The replay records the complete action on the sixteen basis states. These phases affect terminal-only position probabilities by tick five. This comparison uses the supplied gate definitions and stated qubit ordering. [IBM's controlled-U matrix](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CUGate) · [IBM's controlled-Z-rotation matrix](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CRZGate)

With an ideal position measurement after each shift and a sharp initial position, each next step has two distinct destinations. Given the preceding position history, the newly measured arrival identifies the coin direction. A balanced coin then gives independent fair next directions; the edge phases cancel in the squared branch probabilities. Summing over the unreported intermediate positions gives the binomial coefficients folded modulo eight. This derivation uses the measurement schedule, not a fitted decoherence parameter. [Position records in the monitored Hadamard walk](Diffusion_from_three_position_records.md)

| Step | TV of simulator frequencies from monitored walk | TV from plain coherent walk | TV from coherent source gate expansion | Quito wrong-parity outcomes / 1,000 |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | .017 | .017 | .017 | 379 |
| 2 | .008 | .008 | .008 | 591 |
| 3 | .003 | .249 | .249 | 545 |
| 4 | .025 | .396 | .396 | 607 |
| 5 | .0215 | .435 | .356 | 481 |
| 6 | .018 | .451 | .3875 | 512 |
| 7 | .027 | .407 | .3395 | 452 |
| 8 | .019 | .409 | .3195 | 577 |

The distances use every reported site. The two coherent columns are counterfactual calculations, with zero intermediate measurements and identical input preparation. Agreement of the simulated histograms with the measured-at-each-tick calculation across the six discriminating rows is an empirical check on how the *simulator baseline* should be interpreted. It establishes neither the executed hardware instruction schedule nor which physical error caused an off-parity bit.

## Why the hardware rows cannot select a power here

A nearest-neighbor walk from zero on an even ring has \(x\equiv t\pmod2\) on every path. For any finite nonnegative terminal power that leaves zero cells dark, for any mixtures of those powers, for a maximal-cell read, and for fair path counting, the opposite parity has zero probability. The observed wrong-parity fraction therefore lower-bounds the total variation of the **empirical histogram** from every such ideal prediction at that clock, regardless of rail pooling. A population lower bound on the apparatus discrepancy would also need sampling uncertainty and a model for repeated shots. On the four-node processor circuit the four noninitial wrong-parity counts are \(134,173,137,99\) per thousand. The eight-node values above range from 379 to 607. The corresponding simulator wrong-parity counts are zero at all 12 noninitial clocks across both rings. Removing these hardware outcomes would condition away a directly measured discrepancy. Separating state-preparation, gate, intermediate-measurement and readout contributions requires additional calibration.

The deposit provides useful controls for testing a circuit intended to measure the terminal position alone. Its even rings do not implement the sharp joint sheet-and-site read in the [reciprocal connection experiment](A_reciprocal_sheet_connection_on_six_wells.md). Bian and colleagues reported single-photon walks on three- and four-node circles; the accessible university record establishes the circle sizes, localized preparation and revivals. We did not recover their per-site counts for the present analysis. Lorz and colleagues’ four-dimensional-coin platform gives measured cyclic spatial profiles using pulsed coherent light; its observable is optical intensity. [Bian et al., primary article](https://doi.org/10.1103/PhysRevA.95.052338) · [Macquarie research record](https://researchers.mq.edu.au/en/publications/experimental-implementation-of-a-quantum-walk-on-a-circle-with-si/) · [Four-dimensional-coin experiment](https://doi.org/10.1103/PhysRevResearch.1.033036)

## Replay

Download the authors’ ZIP without unpacking it and run `python -B Director_G/check_encoded_cycle_measurements.py authors.zip fresh.json` with Python and NumPy. The [checker](check_encoded_cycle_measurements.py) reads the workbook XML, checks the shot grid and the eight-node measurement loop, expands the source’s elementary gates on every basis input, and compares all clocks. It does not submit circuits to the processor. The [result](results/encoded_cycle_measurements.json) pins the archive and each member’s SHA-256, stores every integer-equivalent count and keeps the simulated and physical tables separate.
