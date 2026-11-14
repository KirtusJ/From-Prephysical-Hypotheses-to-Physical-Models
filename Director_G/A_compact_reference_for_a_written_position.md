# A compact reference for a written position

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex), with construction and challenge by the Codex workers.

At sixteen ticks a signed walk from a localized right rail has squared mass \(50377/65536\) at positions \(x\geq0\), including the origin. How could the walk's own preparations check whether this is the frequency of a bit written at those sites? The earlier comparison used a reference occupying 65,536 equal-amplitude addresses. Here the reference occupies 25 modes. Two reversible operations on the rest of the known flight bring it to the same complete preparation as this reference, with the original bit held throughout. The reference can then be compared with separately assigned sharp preparations. The latter comparison is an experimental premise. [Earlier two-register experiment](Exchanging_a_written_position_flag.md)

## Prepare the reference

Take a complete known column \(n_i/\sqrt S\), with signed integers \(n_i\), \(S=2^t\), and a binary predicate \(B\). Let \(P=\sum_{i:B(i)}n_i^2\). The endpoints \(P=0,S\) have a sharp flag. Test reliability on the actual carrier or match it by the same transport and endpoint-read comparisons as below. At even \(t\) an integer reference may occupy one slot. At odd \(t\), use two equal numerators \(2^{(t-1)/2}\) in the same flag sector, which one addressed Hadamard can collect. The empty bin needs no map. For an interior value, use the \(t\)-digit representation of \(P\), most significant bit first, and prepare a coherent version of the comparison \(j<P\).

At depth \(k=1,\ldots,t\) only one mode still represents equality with the prefix. Apply a balanced Hadamard between it and a fresh empty mode. Park one output as the first differing digit, keeping the other for continued equality. Mark the parked mode exactly when digit \(k\) of \(P\) is 1. The final equality mode is unmarked. Take both outputs with positive signs in this gate convention. A parked mode has amplitude \(2^{-k/2}\), and final equality has amplitude \(2^{-t/2}\). If \(t-k\) is odd, split that parked mode once more into two positive modes with the same mark. Each resulting numerator at scale \(\sqrt S\) is an integer power of two. Both nonempty bins therefore have coordinate gcd with odd part one. The total squared numerator of the marked bin is exactly \(P\), by binary expansion. The circuit has \(t+\lfloor t/2\rfloor\) addressed Hadamards and \(1+t+\lfloor t/2\rfloor\) occupied terminal modes. [Prefix circuit and exact sweep](check_prefix_reference.py) · [Lean identities for all binary words](lean/PrefixReference.lean)

The corresponding classical reference can be made by assigning the \(t+1\) possible stopping histories directly, or by reading independent fair digits until the first difference. History \(k\) has assigned fraction \(2^{-k}\), and equality has fraction \(2^{-t}\). These are design fractions. Exact deterministic stratification may still take \(2^t\) launches per balanced cycle. The literal sequential sampler needs on average \(2-2^{1-t}\) inspected digits. For a reduced interior fraction with odd numerator and denominator \(2^r\), \(r\) digits suffice. In any exact stopping tree fed solely by fresh fair bits, at least one prefix remains unresolved at each level \(k<r\), since termination everywhere by then would make the output a multiple of \(2^{-k}\). Summing the survival bounds proves the reduced tree's mean \(2-2^{1-r}\) optimal in this model. A repeated copy of a single fair bit makes each digit marginally fair but gives \(1/2\) at the four-digit \(9/16\) threshold. [Exact tapes](results/prefix_reference.json) · [Devroye and Gravel on independent-bit sampling](https://arxiv.org/abs/1502.02539)

## Bring the flight to the reference

First write \(B(i)\) coherently into a blank physical flag \(F\). Give each carrier bin a predetermined set of blank slots and designate disjoint output addresses for its reference leaves. When each nonempty source row has odd gcd one, its squared norm and odd gcd agree with the matching reference row. The two-reflection theorem therefore gives a reversible map in each block. Their direct sum acts on the carrier, tensored with the identity on \(F\). A fixed address permutation can place every output in the reference layout. Both routes end at

\[
 S^{-1/2}\sum_\ell y_\ell\lvert\ell,M(\ell)\rangle ,
\]

where \(y_\ell\) is the positive integer numerator of the reference leaf and \(M\) its mark. The direct route writes the same flag from \(M\) after preparing the prefix. All other output slots are empty and any spectator must match on both routes. A retained site copy or a history-dependent apparatus invalidates an inference from the displayed column alone. The construction covers one known coherent column. An unknown family entangled with a spectator would need a common isometry on all relevant columns. [Constructive transport theorem, exact inverses and gate model](Compact_transport_of_a_flight_bin.md) · [General exact circuit synthesis](https://arxiv.org/abs/2305.11305)

## Compare physical rates at the same flag

For a phase control label the \(t+1\) stopping histories by distinct binary words \(j\) of length \(d=\lceil\log_2(t+1)\rceil\). After the flag write apply diagonal signs \((-1)^{a\cdot j}\) with \(a\) uniformly assigned. Give parity-split twins the same sign. Distinct characters average to zero pairwise. Thus the averaged real outer product of the full reference column equals the mixture of normalized stopping-history columns with the programmed fractions above. A twin pair remains the coherent sharp-flag state \((|u,F\rangle+|v,F\rangle)/\sqrt2\). In the classical mixture prepare this whole state on that assigned arm. All these phase operations and preparations require accessible named modes. The identity compares carrier and flag after ignoring the classical controller. A detector able to read its sign or history assignment may distinguish the two ensembles. The measured mixture discrepancy then includes that difference.

On comparable incident populations, bound the following absolute differences of measured hit rates at the same output bit:

| Quantity | Preparations compared |
|---|---|
| \(e_{\rm hold}\) | Original write and the same write followed by the two carrier maps and routing |
| \(e_{\rm route}\) | Transported flight and the directly prepared prefix with its mark written |
| \(e_{\rm sign}\) | Direct prefix and the average over its signed settings |
| \(e_{\rm mix}\) | That signed average and the independently assigned sharp-history preparations |

If each sharp history \(j\) has endpoint error at most \(\eta_j\), its assigned fraction is \(\hat w_j\), and the assignment distribution is within total variation \(\delta\) of the designed fractions, the triangle inequality and ordinary trial counting give

\[
 |r_B-P/S|\ \leq\ e_{\rm hold}+e_{\rm route}+e_{\rm sign}+e_{\rm mix}
               +\sum_j\hat w_j\eta_j+\delta .
\]

Use bounds for the matched assignment and source population, including the sign schedule. Include every incident, carrying unread flags as unknowns. In finite data any population-rate bound must also account for its sampling uncertainty. The outer-product identity supplies a laboratory comparison to perform. Assuming that equal outer products already entail equal rates would silently impose the mixture premise.

For instance a device can return \(G(u)=u^2/[u^2+(1-u)^2]\) on each pure input of pooled squared mass \(u\). At the three-tick half-line the flight, its transported version, and every signed reference all give \(G(3/4)=9/10\). The separately assigned sharp histories give \(3/4\), a difference of \(3/20\). This device passes the first three ideal comparisons and fails the fourth. Existing single-ion fluorescence data pool an electronic rail across the motion. Transferring that control to a spatial predicate still requires a position write and these or equivalent comparisons. [Three-step rail experiment and its calibration limits](Three_steps_and_one_fluorescence_read.md)

## Obstructions and resource costs

The isolated rail \((+2,R)\) at tick four has numerator 3. A dyadic reversible map confined to that bin preserves its odd divisor and cannot reach a prefix row of odd content one. Use the four coherent helper labels from the earlier flag experiment. One always writes 1, one always writes 0 and the other two write \(B\). Each new sector contains one complete copy of the starting column, which has odd content one because its squared norm is a power of two. The new fraction is \(q=(S+2P)/(4S)\). Use the prefix at scale \(t+2\), even if \(q\) reduces as a fraction. To recover the original rate \(r\), compare with an independently assigned classical helper of the same weights. With coherent reference error \(e_q\), coherent-versus-classical difference \(e_c\), honest-arm transfer error \(e_b\), and the endpoint errors \(\eta_0,\eta_1\), the earlier argument gives \(|r-P/S|\le 2(e_c+e_q)+e_b+\max(\eta_0,\eta_1)/2\). This uses the stated assignment weights. The two helper comparisons and any assignment errors require their own measurements. [Helper derivation](Exchanging_a_written_position_flag.md)

| Replayed position or rail | Squared fraction compared | Occupied reference modes | Padded carrier slots, unmarked + marked | Named operations in the two pairs of reflections |
|---|---:|---:|---:|---:|
| \(x\ge0\), tick 3 | \(3/4\) | 5 | 8 + 8 | 38 |
| \(x\ge0\), tick 16 | \(50377/65536\) | 25 | 64 + 64 | 650 |
| \(x\ge0\), tick 32 | \(3262634697/4294967296\) | 49 | 128 + 128 | 2,540 |
| Tick-four \(9/16\) rail, after helper | \(17/32\) | 10 | 64 + 32 | 164 |

The counts omit the position write, prefix preparation, labelling permutation and physical routing. Bank sizes count carrier modes before adjoining the held bit. Deterministic base-four padding gives polynomial synthesis size in the number of listed source entries and in \(t\). A freely propagated line walk has at most \(2(t+1)\) terminal rail entries. A carrier listing a full measurement history can itself grow exponentially.

Locality also matters. For a range-\(R\) layer circuit of depth \(h\), the output squared norm in a site patch \(A\) is at most the initial squared norm within distance \(Rh\) of \(A\), by unitarity and the backward light cone. If both extremes at \(\pm t\) have nonzero amplitude, exact collection into one contiguous \(w\)-site patch therefore needs \(2Rh+w-1\ge2t\). This statement takes positions and blank padding in one common physical line geometry. Uncollected tails of very small squared norm change the lower bound at finite tolerance. Distributed flag measurements have different costs.

The replay includes all five half-line depths tested, the obstructed rail, its repaired helper, and an exact matrix check retaining the twin coherences. The construction reduces the memory cost of a finite discrimination experiment. Physical implementation, its measured rate discrepancies, the origin of the apparatus and the absolute naming of a cyclotomic embedding remain open. [Integrated replay](check_compact_position_reference.py) · [All results](results/compact_position_reference.json)
