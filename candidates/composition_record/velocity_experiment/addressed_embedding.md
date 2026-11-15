# What an addressed rail coin reveals about the real embedding

A walk with a sharp right-rail source can test a change of real algebraic embedding using a position record after only three ticks. The apparatus applies a different coin coherently on even and odd values of its position address. This supplies the relative phase between paths that pass through different numbers of Hadamards. The [synchronized-walk theorem](../../../Director_G/Native_preparations_and_probability_embeddings.md) identifies this extra operation explicitly. In that earlier apparatus every path of a given duration had the same number of Hadamards.

A [reference built from stopped fair direction records](../../../Director_G/A_stopped_walk_reference_for_the_real_embedding.md) produces the entire specified first-address distribution using a classical counter and a finite-error deadline. It provides a separate rate comparison for a labeled gate.

## A register with an observable square root

Use the same two-bit address as the [three-qubit position experiment](README.md). A free shift increments it modulo four on L and holds it on R. In each group of three ticks, use the Hadamard coin \(H\) on the first and third ticks. For the middle tick use \(X\) on an even address and \(H\) on an odd address, before the shift. Apply identity at the intermediate site writes. Start on R at address zero. Immediately after the middle shift of the first flight, the amplitudes are \(1/2\) on (address 1, R), \(1/\sqrt2\) on (address 1, L), and \(-1/2\) on (address 2, L). The last Hadamard mixes the two amplitudes at address 1 before the last shift. Writing the address then gives these probabilities per incident launch.

| First address code | Specified real matrices | Conjugate real matrices |
| --- | ---: | ---: |
| 0 | \(0\) | \(0\) |
| 1 | \((3+2\sqrt2)/8\) | \((3-2\sqrt2)/8\) |
| 2 | \((2-\sqrt2)/4\) | \((2+\sqrt2)/4\) |
| 3 | \(1/8\) | \(1/8\) |

Here conjugation means the nonidentity field map on \(\mathbb Q(\sqrt2)\). It fixes rational numbers and maps each \(\sqrt2\) to \(-\sqrt2\), including in every matrix and the amplitudes they generate. The matrices remain real orthogonal under the map. The recorded probabilities generate \(\mathbb Q(\sqrt2)\) because code 1 alone determines the generator. No odd-order cyclotomic sheet character appears in these operations. Their records leave any embedding that fixes \(\sqrt2\) indistinguishable.

The controlled matrix is \(\Pi_{\rm even}\otimes X+\Pi_{\rm odd}\otimes H\), with the address projectors understood as parity projectors. The field map sends \(H\) to \(-H\) and fixes \(X\). Uniform Hadamards therefore acquire a harmless global sign. The addressed Hadamard instead acquires a sign *relative to the even-address operation*. Reversing that relative phase reproduces the conjugate law for every word. Separate tests of \(X\) or \(H\) alone cannot calibrate it. These two fixed implementations predict different named-address frequencies, and the experiment requires a trusted phase convention for the joint operation to attribute that difference to an embedding.

This ambiguity also applies to a calibration assembled solely from the same unknown apparatus. Let \(\epsilon=\pm1\) be the physical sign on the odd-address Hadamard relative to the even-address exchange. Simultaneously conjugating \(\sqrt2\) and reversing \(\epsilon\) leaves each addressed operation unchanged as a real matrix. Each synchronized unconditional Hadamard changes by a global minus. Rational permutations, coordinate projections and the sharp source are fixed. Hence on every measured branch the two descriptions yield the same normalized probabilities. Feedback based only on these records makes the same choices, so repeated calibration with this menu still identifies only the combined sign convention. A second coherent reference must have an independently established relative phase to break that ambiguity. Araújo and colleagues give the general circuit reason that an undetermined global phase of an isolated operation becomes observable when that operation is coherently controlled. [Araújo, Feix, Costa and Brukner](https://doi.org/10.1088/1367-2630/16/9/093026)

After three such flights there are 27 positive words and 37 dark words. Each of the 13 reached parent nodes has one dark child and three different positive child weights. The [exact replay and circuit exporter](addressed_write_test.py) retains all 64 words. The [per-write identification theorem](test_each_write.md) applies on this occupied support, with maximum, minimum and zero-power choices defined there. A report on a dark word tests support, dynamics and reporting jointly. The logical walk uses real matrices throughout. Implementing a controlled Hadamard on a specific machine can require further gates. [OpenQASM gate controls and phase conventions](https://openqasm.com/language/gates.html)

## Separating the field map from the probability response

If both populations use ordinary squared probabilities and share the calibrated matrices and reporting, their mixture is identifiable from the first record. Let \(\lambda\) denote the fraction with the specified embedding. Code 1 has probability \((3-2\sqrt2)/8+\lambda\sqrt2/2\). This statement concerns a specified pair of models and has no empirical estimate here.

A second interpretation raises the first-write masses to an unknown power \(q\ge0\) and normalizes over occupied cells. Under the conjugate embedding code 1 has the **smallest** positive mass, so its modeled rate is at most \(1/3\), even in a mixture of exponents. A homogeneous conjugate embedding with this local response cannot reach the specified ordinary rate of about 0.72855. More generally, if a measured rate has lower limit \(u>1/3\), the fraction from the specified embedding is at least \((3u-1)/2\) among these two populations. This bound uses only original launches, a faithful or bounded reporter and a local first-write response. Global powers on complete words require a separate marginal calculation.

There is also an exact limitation. Let \(U\) be the uniform law on the three bright codes, realized by \(q=0\) on occupied support. The maximum selector gives a point mass at code 1 in the specified embedding, and at code 2 in the conjugate embedding. The ordinary first-record histogram is exactly

\[
 \frac38 U+\frac{1+\sqrt2}{4}\,\delta_1
             +\frac{3-2\sqrt2}{8}\,\delta_2 .
\]

These three strictly positive weights sum to one. Even restricting powers to finite positive exponents leaves such a counterfeit: the ordinary point lies in the interior of this triangle in the bright three-code simplex. Its barycentric coordinates remain positive if \(U\) is replaced by a sufficiently small positive-power law and each point mass by a sufficiently large finite-power law in its respective embedding. Thus the first record alone cannot select both the embedding and an unrestricted mixture of power responses. This construction matches the first marginal. A [test on the final three words after prefix (2,3)](selecting_the_real_embedding.md) separates the embedding even with unknown nonnegative powers at fixed relative gate phase.

OpenAI Codex developed the calculation in the research program of Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada.
