# Five ticks from a localized sheet test the probability power

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex) and the Codex workers.

Start the walker at a known well, rail and sheet address. Five ordinary Hadamard ticks, two addressed sheet permutations and one joint position-and-sheet read suffice for a population comparison. Three terminal outcomes have squared kinematic masses in the ratio \(1:4:16\), each on a single rail. Their measured frequencies can distinguish the ordinary exponent from every other finite nonnegative exponent in the specified family, even when the power and the decision to resolve rails vary on every launch. The preparation uses neither a complex phase standard nor a coherent difference of two sheet states. The earlier [ten-tick sign experiment](Three_signed_ticks_and_the_probability_power.md) uses a position-only terminal detector. Here distinguishing the sheet at that final read is essential to the stated comparison.

## The addressed permutations and one terminal survey

At position \(0\) initialize rail \(R\) and sheet \(s=0\) sharply. At each tick apply \((r,l)\mapsto(r+l,r-l)/\sqrt2\) on each sheet, and send \(R\) right one well and \(L\) left one well. Immediately **after** that motion at tick 3, exchange sheets 0 and 1 on both rails at well \(-3\). Do the same at tick 4 at well \(+2\). At tick 5 read the pair \((x,s)\). Intermediate passages must remain coherent; no extra passage label is required. The sign in the Hadamard coin is already part of the stipulated walk. The two exchanges are unsigned permutations on named coordinates. Preparing a definite sheet and reading its label are operational premises. The mathematical sharp initialization makes no probability assignment between two simultaneously populated sheets. The conventional coined-walk position amplitudes refer to orthogonal outgoing rails. [Konno on the one-dimensional quantum walk](https://arxiv.org/abs/quant-ph/0206103) · [Earlier local sheet preparations](Native_preparations_and_probability_embeddings.md)

The table gives integer amplitudes divided by \(\sqrt{32}\). The separate counts enumerate all \(2^5=32\) physical outgoing-direction words. Each word toggles its sheet on each addressed visit. The exchange adds no direction alternatives. Multiple words reaching the same output rail interfere under the signed amplitude construction.

| \(x\) | Sheet 0 \((R,L)\) | Sheet 1 \((R,L)\) | Path count, sheet 0 | Path count, sheet 1 |
|---:|---:|---:|---:|---:|
| −5 | (0,0) | (0,1) | 0 | 1 |
| −3 | (0,1) | (−1,1) | 3 | 2 |
| −1 | (−1,−2) | (1,0) | 9 | 1 |
| +1 | (0,0) | (0,2) | 6 | 4 |
| +3 | (0,1) | (4,0) | 1 | 4 |
| +5 | (1,0) | (0,0) | 1 | 0 |

Define \(D=16P(-3,0)-8P(+1,1)+P(+3,1)\) on the incident-launch denominator. All remaining terminal outcomes have coefficient zero. For one powered read, allow the two positive squared rail populations in each \((x,s)\) coordinate to be pooled or kept separate, arbitrarily and independently across coordinates. A positive resulting cell of mass \(m\) receives weight \(m^q\), with one exponent \(q\ge0\) and a common normalizer \(Z\) for the launch. A zero cell always has weight zero, including at \(q=0\). This model permits an arbitrary population of powers and partitions. As a further alternative, permit uniform weighting of complete direction words.

The three scored outcomes have single occupied rails of squared weights \(1,4,16\). Under each powered read,

\[
D(q)=\frac{16-8\,4^q+16^q}{Z}
=\frac{(4^q-4)^2}{Z}
=\frac{16^q}{Z}(1-4^{1-q})^2 .
\]

It vanishes exactly when \(q=1\). At zero it is \(9/Z>0\). The score under full counting is \((16\cdot3-8\cdot4+4)/32=5/8\). A limiting read that selects the largest cell deterministically gives \(D=1\): \((+3,1)\) is the unique largest regardless of partition. There are at most eleven positive cells and every cell has mass at most 16, so for any \(\delta>0\) and every finite \(|q-1|\ge\delta\),

\[
D(q)\ \ge\ (1-4^{-\delta})^2/11.
\]

This follows from \(Z\le11\,16^q\) and \(|1-4^{1-q}|\ge 1-4^{-\delta}\). It also bounds the limiting maximum-cell rule by continuity. Hence an ideal population mean \(D=0\) excludes full counting and selects the ordinary exponent almost surely within the declared family. More quantitatively, for counting fraction \(\alpha\) and powered tail weight \(\beta_\delta\), the population mean is at least \(5\alpha/8+\beta_\delta(1-4^{-\delta})^2/11\). Each launch needs only this one terminal setting. The supplementary dark outcome \((+1,0)\) has six direction words but zero amplitude on both rails. In this family its ideal probability is exactly \(3\alpha/16\), an independent way to identify the full-count fraction. Destructive interference, unread outcomes and physical inefficiency have to be distinguished in such a test.

## Source, detector and negative controls

* **Changing the initial label.** Global interchange of the sheets commutes with the coin, shift and both local exchanges. Starting sharply on sheet 1 reflects every final sheet label. If a source is prepared on a possibly fluctuating sharp sheet, record its actual input label and score the change \(s_{\rm end}\mathbin{\mathrm{xor}}s_{\rm start}\). This gives the same test with either sharp start, even if the chosen power depends on that label. For an unrecorded start on sheet 1, keeping the uncorrected sheet-0 score instead gives \(D=33/32\) under ordinary squared weights. A coherent or otherwise unknown sheet input requires its own analysis; retaining a sharp initial measurement is a different preparation.
* **Switching off the exchanges.** For a sharp sheet-0 source all words then remain on that sheet. The ordinary score with the original target labels is \(5/2\), since the only surviving scored event is \((-3,0)\) of mass \(5/32\). Address swaps and the routing of the terminal labels therefore matter.
* **Ignoring the sheet.** If the detector records only \(x\), the ordinary pooled masses at \(x=-3,+1,+3\) are \(3,4,17\) over 32. Applying the same coefficients directly to these three wells gives \(33/32\). This example gives no impossibility theorem for other position-only scores. For any such addressed-swap schedule the two sheet amplitudes add at each site and rail to the bare, unswapped walk amplitude, by linearity and invariance of the sum under a swap. A site with only one occupied physical rail-and-sheet cell must consequently inherit its nonzero amplitude from a sharp rail of the bare walk. At five ticks the bare sharp-rail sites have just two distinct positive squared masses, 1 and 4. The present construction instead achieves the three pure weights at joint coordinates.
* **Missing detections.** Decode the same initial label, well and final sheet for every incident trial. If a fraction \(\ell\) of terminal records is unclassified, let \(D_{\rm logged}\) assign those records score zero on the incident denominator. The full score then lies in \([D_{\rm logged}-8\ell,\ D_{\rm logged}+16\ell]\). Ordinary systematic errors in the coin, coherent swaps, source or decoding require separate calibration; an unqualified renormalization over detected records could change the comparison. The expected score statements concern population rates and require sampling uncertainty before interpreting measured data.

All amplitudes and squared masses of this finite terminal survey are specified in the prepared coordinate basis. The experiment distinguishes the declared probability powers; it does not select an absolute embedding of a named cyclotomic field, establish these physical operations, or derive the ordinary law for every detector. The [exact replay](check_localized_sheet_power.py) generates all signed and unsigned directed paths from either sheet, compares a separate coordinate propagation, and tests all terminal partitions and controls. The [Lean proof](lean/LocalizedSheetPower.lean) checks the terminal rows and the score numerator equations. [Exact tables and predictions](results/localized_sheet_power.json)

## A stationary exchange at the origin

The timed exchanges can be replaced by one installed permutation. Start again at \((0,R,0)\). On **every** tick apply the Hadamard, shift, then exchange the sheets of both rails arriving at the origin. Read \((x,s)\) once at tick six. The initial preparation at the origin is not an arrival. On a direction word the terminal sheet is the initial label plus the number of returns to the origin modulo two. Thus the physical memory has two states and requires no counter of unbounded size. The unitary step is the same on every tick: the coin and the addressed exchange are on-site, and the shift traverses one edge. This removes the clocked activation of a sign or a swap during flight. A fixed spatial origin, a coherent permutation there, an initial sharp label and a terminal read at a known tick remain premises. The table uses amplitude divisor 8.

| \(x\) | Sheet 0 \((R,L)\) | Sheet 1 \((R,L)\) | Words on 0 | Words on 1 |
|---:|---:|---:|---:|---:|
| −6 | (0,−1) | (0,0) | 1 | 0 |
| −4 | (1,−3) | (0,0) | 4 | 2 |
| −2 | (1,2) | (0,0) | 9 | 6 |
| 0 | (0,−4) | (−2,2) | 8 | 12 |
| +2 | (2,1) | (0,2) | 9 | 6 |
| +4 | (3,1) | (2,0) | 4 | 2 |
| +6 | (1,0) | (0,0) | 1 | 0 |

Use the observed score \(D_{\rm ret}=16P(6,0)-8P(2,1)+P(0,0)+5P(-2,1)\). The first three cells are pure, with weights \(1,4,16\); the fourth is dark in every powered model. Thus \(D_{\rm ret}(q)=(4^q-4)^2/Z\) for every local choice of rail partitions, including at \(q=0\). There are five coordinates with two positive rails and at most 15 positive cells. No cell other than \((0,0)\) exceeds 10, so the maximum-cell score is 1. For \(|q-1|\ge\delta>0\) the normalized score is bounded below by \((1-4^{-\delta})^2/15\). Pure path counting would give \(-24/64\) without the fourth term. The six paths at the dark coordinate add \(30/64\), giving \(3/32>0\). For any mixture in the stated family, the two dark-coordinate rates are separately \(P(-2,1)=6\alpha/64\) and \(P(-4,1)=2\alpha/64\) for count fraction \(\alpha\). Their sum gives \(\alpha/8\). Unknown outcomes have the same incident-score allowance \([-8\ell,16\ell]\) as in the five-tick test.

Switching the origin exchange off gives ordinary score \(3/8\) with the six-tick coefficients. Ignoring the sheet and applying the four coefficients to whole sites gives \(-7/64\) even with the stationary exchange and ordinary read. A sharp initial sheet 1 can again use the relative output label; using the uncorrected sheet-0 labels gives \(-7/64\). Thus the stationary actuator does not remove the terminal label requirement. The [replay](check_localized_sheet_power.py) compares all 64 complete physical words with a site recurrence, including the two dark coordinates and both initial labels.

As a directed walk rule the sheet transport on an edge \(x\to y\) is \(g_{xy}=X^{\mathbf1_{y=0}}\), where \(X\) exchanges the two labels. Consequently the projected two-step return \(0\to1\to0\) carries \(X\). Relabeling sheets separately at each site conjugates this return permutation and cannot make it the identity. In this directed sense the cover has a nontrivial loop permutation. A reciprocal edge connection on an undirected tree instead assigns inverse transports to the two directions, making each immediate retracing trivial; the stationary rule supplies an on-site exchange after transport. Its entire quantum evolution is reversible, with the inverse operations applied in reverse order. In the antisymmetric sheet eigenstate each origin visit would contribute a minus sign, whereas the symmetric eigenstate would see the bare walk. The sharp source and direct joint read used here track the coordinate amplitudes from both sectors and require no independent preparation of a phase eigenstate. [Existing discussion of native preparation and absolute embedding](Native_preparations_and_probability_embeddings.md)
