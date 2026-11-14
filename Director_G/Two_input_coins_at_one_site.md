# Two input coins at one site

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

One source preparation at a time, a pair of dyadic reflections can match the marked amplitudes of a walk to a reference. An unknown input coin requires a **single fixed circuit** for both input rails and their superpositions. At tick seven there is a whole-site example in which both one-column circuits exist, every input coin gives the same squared flag mass on the two preparations, and exact common transport still fails. This bears on how an experiment could transfer a flag calibration to a changing or entangled source. [One-column comparison](A_compact_reference_for_a_written_position.md) · [Exact dyadic transfer](Compact_transport_of_a_flight_bin.md)

## The two full preparations

Launch at the origin on the R or L rail. At each tick apply the real Hadamard in that order, then move R one step right and L one step left. Write the flag for the entire site \(+3\) after seven ticks. In units \(1/\sqrt{128}\), its marked block \(A\) has two rows for the outgoing rails and two columns for the incoming coin. Give a proposed reference four marked addresses with block \(B\). Keep every unmarked row unchanged.

\[
A=\begin{pmatrix}5&-1\\4&2\end{pmatrix},\qquad
B=\begin{pmatrix}0&2\\3&1\\4&0\\4&0\end{pmatrix},\qquad
A^\mathsf{T}A=B^\mathsf{T}B=\begin{pmatrix}41&3\\3&5\end{pmatrix}.
\]

The unmarked Gram matrix is \(\left(\begin{smallmatrix}87&-3\\-3&123\end{smallmatrix}\right)\); together the blocks have Gram \(128 I\). Thus either complete preparation is an isometric encoding of an arbitrary coin, even when tensored with a spectator. Equality of the whole-site effects gives identical quadratic flag predictions for every coin state. The conditional carrier states inside that flag may differ.

Each corresponding R column has squared norm 41 and odd coordinate content one. The L columns also have odd content one and squared norm 5. The replay actually compiles the two one-column maps from the earlier theorem. Their two-reflection words require respectively 23 + 11 and 17 + 15 addressed operations in its convention. Choosing a circuit after learning which basis state was sent changes the preparation when that information was coherent or unavailable.

## Where the common operation fails

Let \(v=(1,-2)^\mathsf{T}\). Then \(Av=(7,0)^\mathsf{T}\) while \(Bv=(-4,1,4,4)^\mathsf{T}\). Every dyadic matrix maps a vector whose entries are all multiples of seven in \(\mathbb Z[1/2]\) to another such vector. Adding any number of blank addresses preserves the divisibility. The contradiction also survives individually addressed balanced Hadamards: reducing \(\sqrt2\) to 3 modulo 7 defines a ring map \(\mathbb Z[1/2,\sqrt2]\to\mathbb F_7\). The source still vanishes and the target has a unit entry. This argument tests the required linear action without assuming one can prepare \(v/\sqrt5\) in the laboratory. [Gate rings and exact synthesis](https://arxiv.org/abs/2305.11305)

The obstruction can be read directly from the unique real isometry on the span of the two occupied source addresses:

\[
BA^{-1}=\frac17\begin{pmatrix}-4&5\\1&4\\4&2\\4&2\end{pmatrix}.
\]

The integer columns have Gram \(49I\), so an extension to a real orthogonal matrix exists. Exact transport in the displayed coordinates forces, in particular, the matrix entry \(1/7\). The failure concerns one carrier operation after the site flag has been written and held. A separately prepared reference, an apparatus with other gate coefficients, or an approximation requires a distinct test. No positive lower bound on approximation error follows from this divisibility argument.

As a control, pad \(A\) with two zero rows and apply one four-mode Walsh matrix. It transports both inputs at once to rows \((9,1),(1,-3),(9,1),(1,-3)\), with an additional common denominator of two. Its inverse restores both columns. Sharing a Gram matrix and separate column contents permits successful examples as well.

## The first whole-site example and its measurement scope

For a real-rank-two integer source block, reduction modulo an odd prime \(\ell\) loses rank exactly when all \(2\times2\) minors vanish modulo \(\ell\). Their gcd tests all odd primes at once. We enumerated **all nonempty unions of reachable whole sites** at clocks zero through eight, including the full-support mask. Counts of real-rank-two blocks with two individually odd-primitive columns and a rank loss at some odd prime are \(0,0,0,0,0,0,0,2,4\), respectively. The first two are the singleton sites \(-3\) and \(+3\). For \(+3\), the source minor is 14 and the target minors have gcd 2. This is a first occurrence of that particular source-side criterion on this walk. A target chosen specifically to lose rank can obstruct transport in the reverse direction at other clocks.

If \(v/\sqrt5\) can be prepared, both programs assign mass \(49/640\) to the original binary mark. A second mask over the **third and fourth named marked addresses** distinguishes the untouched source padded with zeros from the proposed target. The squared masses are respectively zero and \(32/640=1/20\) per incident. Recording that diagnostic needs named output addresses and a detector with calibrated response. A faithful endpoint alone does not fix the nonzero frequency. This comparison distinguishes two particular preparations; it cannot certify a gate alphabet or exclude every approximate circuit. Any detector depending exclusively on the original pooled mass, including the normalized-square rival, predicts equal rates for the original bit on the two preparations.

The [checker](check_two_coin_site.py) sums the signed path words from both input rails, checks the complete norm at each clock, and calls the independent reflection compiler for the scalar controls. The [full census and endpoints](results/two_coin_site.json) retain all qualifying masks. From the repository, run the following with a fresh output file.

    python -B Director_G/check_two_coin_site.py NEW_RESULT.json
