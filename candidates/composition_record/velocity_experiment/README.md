# A three-qubit test of memory between position records

Run nine Hadamard walk ticks and record position after ticks 3, 6 and 9. Apply a quarter-turn to the coin after each of the first two records. For a fair mixture of sharp right and left launches, equal-sign pulses give the first and third displacements the same sign with probability **1/2**. Opposite-sign pulses give **5/8**. The entire distribution of any two adjacent displacements agrees across the four phase patterns. Independent fair pulse signs give **9/16** for the endpoint sign test. These are ideal circuit predictions. [Two-flight velocity theory](../../../Director_G/Velocity_memory_after_a_position_record.md) · [Three-record phase memory](../../../Director_G/A_phase_kept_between_three_position_records.md)

## Generate and verify

Use Python 3 with the standard library. From this directory:

### Check the circuit laws

    python -I -O generate.py

### Export circuits and exact fixture counts

    python -I generate.py --output circuit_export --ideal-counts ideal_counts.json

The two export options are independent and create new paths. The circuit directory contains eight OpenQASM 3 files and a CSV of all 64 chronological outcomes for each source and phase pair, including zero-weight outcomes. The optional JSON is a histogram fixture with schema **velocity-history-counts-v1**, provenance **ideal** and denominator 512 per circuit. It can be read by the [histogram analyzer](analyze_counts.py). Its numerators are exact path weights. They do not represent acquired shots.

The checker executes the emitted instructions in the eight-dimensional computational basis, starting from each of the two specified launch states. It retains the three intermediate position records. An independent enumeration sums signed paths of the walk on the unbounded line for every block-displacement triple and final coin. A further comparison explicitly dephases R/L after each of the first two blocks, separately for each prepared source. It reproduces every one of the 64 words when the four pulse patterns receive equal weight.

The eight phase circuits also parsed with the OpenQASM reference parser 1.0.2 (ANTLR runtime 4.13.2). A separate syntax-tree check recovered 236 gates, 48 measurements and 48 barriers across the eight files. This check covers the emitted circuit representation. Native device compilation and data acquisition remain open. [OpenQASM reference parser](https://pypi.org/project/openqasm3/1.0.2/)

## Qubits, registers and record order

The coin is q[0]. Initialize it in 0 for R or 1 for L, using an X in the L circuit. Qubits q[1] and q[2] store the low and high bits of the number of left moves modulo 4. Start both at zero. After H on the coin, a left move increments this counter. The controlled carry fires first on the old low bit (CCX coin, low, high), then CX coin, low flips the low bit. R leaves the counter alone. Within a block of three ticks there are only four possible left-move counts, from 0 through 3, so the modulo register identifies each reachable final site relative to the preceding recorded position. An unresolved four-tick block would alias distinct positions.

Each measurement copies the two counter bits to distinct bits of the six-bit register **record**. The circuit includes no counter reset. At each intermediate boundary, S or Sdg on the coin supplies relative left-rail phase +i or −i. Barriers bracket the position writes. A suitable backend must support measurements during the circuit and continued coherent use of the coin, with known compilation, register mapping and timing. A compiler or emulator that postpones all position measurements must independently reproduce the measurement instrument on the reused address qubits. [OpenQASM 3 measurement and barrier instructions](https://openqasm.com/language/insts.html) · [OpenQASM standard gates](https://openqasm.com/language/standard_library.html)

In a **b5 b4 b3 b2 b1 b0** display string (spaces shown only for readability), decode y3 from (b1,b0), y6 from (b3,b2) and y9 from (b5,b4). Beginning at y0=0, for each consecutive pair use

$$
D_i=3-2[(y_{3i}-y_{3i-3})\bmod 4].
$$

For example, the displayed word 100100 gives positions (0,1,2) and displacements (+3,+1,+1). Each displacement is odd, so no tie occurs in this three-tick version. Retain every measured word and every attempted acquisition. Decode backend-specific output once into this explicit bit convention.

## Compare assigned cohorts

Prepare R and L on independent, balanced classical assignments for the maximally mixed initial coin. For each pulse comparison weight sources equally. In the **equal-sign** group give (S,S) and (Sdg,Sdg) equal weights. In the **opposite-sign** group give (S,Sdg) and (Sdg,S) equal weights. The **independent-sign dephasing** comparison is the equal-weight mixture of all four patterns, with both source preparations again weighted equally. Consequently it shares shots with the equal/opposite estimates if all three are computed from the same acquisition. Normalize per assigned cohort before applying the design weights if shot totals differ. Missing records need their own counts. Timing, preparation, readout errors and cohort-dependent losses can affect the contrast.

In the ideal circuit the adjacent same-sign rate is 5/8 in both sign groups. Ideal dephasing is a channel identity: averaging the two conjugations by S and Sdg erases the off-diagonal coin terms. Independent signs at successive boundaries implement the two such averages. A single sign drawn once and reused corresponds to the equal-sign group. The experiment tests a controlled intervention on the encoded walk. It does not independently determine a microscopic record law.

## Analyze a histogram

    python -I analyze_counts.py ideal_counts.json
    python -I analyze_counts.py measured_counts.json --alpha 0.05

The exported ideal fixture is a complete schema example. For a measured file set `schema` to `velocity-history-counts-v1` and `provenance` to `hardware` or `simulator` as appropriate. For each of the eight `arms`, supply `source` (R or L), `phase1`, `phase2` (S or Sdg), `attempts` and a `counts` object mapping six-bit display strings to integer multiplicities. Omitted words have zero recorded multiplicity. Keep the difference between the attempted and recorded totals as missing. Each word must come from one launch. For a backend returning Qiskit Sampler bit arrays, collect the six-bit **record** register from the same circuit result, preserving its bit order. [IBM bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)

The analyzer returns the opposite-minus-equal contrast for all launches and the contributions from the first and middle edge events. Exact fixture values are 1/8, 0 and 0. The [derivation](phase_comparison.md) describes uncertain initial coins and phase offsets. The [reporter calibration bounds](reporter_calibration.md) quantify how large a false contrast can remain after testing deterministic paths.

### Check the recording device on a prescribed route

    python -I -B route_control.py --source L --phases S Sdg --displacements -1 -3 -1 --output control.qasm
    python -I -B -O route_control.py --check

This example has ideal six-bit record 110110. The [route generator](route_control.py) replaces the nine Hadamard coins with identity or exchange coins, choosing right steps before left steps within each three-tick flight. It retains the address updates, three position measurements and both chosen pulse signs. Its independent basis-state interpreter checks all 512 combinations of route, launch rail and pulse settings. Matching the gate timings and the reporter's behavior on naturally occurring paths still requires experimental evidence.

## Calibrating the two writes separately

Suppose write $i$ preserves the two local rail populations and multiplies the off-diagonal coin entry by a real, site-independent factor $\eta_i\in[0,1]$. The pulse is an additional calibrated phase. Both source preparations in this circuit are real. After the first quarter-turn pulse the off-diagonal term is imaginary, hence invisible to every real second-flight position effect. The second real flight sends imaginary coherence to imaginary coherence. The second quarter turn converts that term to a measurable real entry only after both attenuation factors have acted. Any real coherence generated from the diagonal at the middle flight becomes imaginary under the second pulse and is invisible to the final position read. Thus the complete 64-word law of each quarter-turn circuit depends on the two factors only through their product. For example, $(1,1/4)$ and $(1/2,1/2)$ give exactly the same eight histograms.

A reference run at the same clocks replaces both phase pulses by identity. For adjacent three-tick displacements the sign-agreement probability interpolates between $5/8$ at full rail dephasing and $3/4$ at full rail coherence. It is affine in the intervening write factor. The fair R/L mixture has input coin $I/2$ at the first flight and again after averaging over the first position write and all its outcomes, because the summed walk and write channels are unital. The resulting reference rates are

$$
P(D_1D_2>0)=\frac{5+\eta_1}{8},\qquad
P(D_2D_3>0)=\frac{5+\eta_2}{8}.
$$

Both use incident denominators and require no division by the other factor. At $(1/4,3/5)$ the exact rates are $21/32$ and $7/10$. The [reference verifier and exporter](calibrate_writes.py) checks every chronological output against both competing models for each source, the four corners of the bilinear model and the individual reference rates. It exports two additional circuits into their own directory:

    python -I -O calibrate_writes.py
    python -I calibrate_writes.py --output write_reference

Preserve both original measurements, barriers, assignment weights, effective clock times and readout while removing the two rotations. An identity directive can be optimized away by the compiler, so compare the compiled schedules on the intended device. The formulas presume that the reference and phase arms sample the same source and instrument, with common readout calibration. Under a common heterogeneous population of site-independent factors drawn independently of the assigned arm and source, the references give $E[\eta_1]$ and $E[\eta_2]$, while the original interaction gives $E[\eta_1\eta_2]/8$. These three moments can reveal correlation. They leave individual shot factors and their joint distribution unidentified. A complex unknown attenuation, its dependence on the observed site, or population-changing backaction calls for a different calibration.
