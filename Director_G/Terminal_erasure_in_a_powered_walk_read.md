# How many terminal records can a competing probability rule retain?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

On the reciprocal six-well ring at tick eleven, the squared-mass rule \(q=2\) cannot reproduce the ordinary \(q=1\) well histogram under lossless readout. If erasure can depend on the final well, the same competitor can reproduce it among the detected launches while retaining exactly \(1142784/1181699\) of the incident launches, about 96.71%. Counting every missing launch gives a sharp test once the overall retention is known. The bound changes when the detector also records a terminal bit. These are predictions for an idealized instrument. [Walk and terminal bits](A_reciprocal_sheet_connection_on_six_wells.md) · [Lossless fixed-power criterion](When_a_position_histogram_identifies_its_probability_power.md#the-full-set-of-histograms-at-one-fixed-exponent)

## A sharp retention bound

Fix the preparation, the terminal bins and a finite common exponent \(q\ge0\) for **all** launches. A bin has positive mode masses \(a_{xi}\) and total mass \(m_x\). On each launch, each bin can be partitioned freely before raising the resulting cell masses to \(q\) and applying one global normalization. Empty modes stay dark. Erasure then either preserves the correct bin or returns a distinct no-click symbol. There are no dark counts or reassigned labels. Keep the incident denominator. Write \(p_x>0\) for any prescribed histogram on the occupied bins, with \(\sum_xp_x=1\). The observed law to be explained is \(\eta p_x\) in bin \(x\) and \(1-\eta\) at no-click.

Let \(L_x,U_x\) be the lesser and greater of \(m_x^q\) and \(\sum_i a_{xi}^q\), using only occupied modes. The earlier normalization argument gives every latent histogram \(r_x=w_x/\sum_yw_y\) with \(L_x\le w_x\le U_x\), and these exhaust the mixtures over partitions at this \(q\). Per-bin acceptance after scoring, allowed to depend on type and bin, can give the target if and only if some such \(r\) satisfies \(r_x\ge\eta p_x\) for every \(x\). Necessity follows from the direction of erasure. For sufficiency use the type-independent acceptances \(\eta p_x/r_x\).

Set \(k=\min_x U_x/p_x\). The greatest feasible retention is

\[
\eta_{\max}(q,p)=\frac{1}{\sum_x\max\{p_x,L_x/k\}}.
\]

For the upper bound take a minimizing bin \(j\). Every normalized partition satisfies \(U_j r_x\ge L_xr_j\), so every mixture does too. Since \(r_j\ge\eta p_j\), all \(r_x\ge\eta\max(p_x,L_x/k)\). Sum over \(x\). For attainment take \(w_x=\max(L_x,kp_x)\), which lies in every interval. The resulting \(r_x\ge\eta_{\max}p_x\). Further uniform erasure attains every smaller value. At \(\eta=1\) this reduces to the lossless box criterion. The fixed-power assumption matters if using the bound to exclude an entire type of instrument. A varying exponent can put some launches above a pointwise exclusion threshold.

## Exact six-well controls

The inputs are the nine nonzero squared amplitudes of the eleven-tick walk. The target \(p_x=m_x/2048\) is ordinary weighting, also on exposures reporting a bit. In the last row \(0R\) marks sheet 0 and the right rail.

| Reported outcomes | Largest retention at \(q=0\) | Largest retention at \(q=1\) | Largest retention at \(q=2\) |
|---|---|---|---|
| Well | \(1\) | \(1\) | \(1142784/1181699\) |
| Well and sheet | \(256/445\) | \(1\) | \(41472/242957\) |
| Well and \(0R\) bit | \(256/357\) | \(1\) | \(2048/242957\) |

For the well-only read at \(q=2\), the latent model can have probabilities proportional to \((406782,311364,463553)\) at wells \(1,3,5\). Pool well 3, split well 5 fully, and mix full pooling and full splitting of well 1 with their computed launch weights. Accept all records at wells 1 and 3, and the fraction \(424638/463553\) at well 5. The incident law is proportional to \((406782,311364,424638,38915)\), in well order followed by no-click. Among the clicks it has the ordinary proportions \(729:558:761\). In the two joint reads the \(q=2\) supremum is already attained at full splitting, with exactly the acceptances in the [rational witnesses](results/terminal_erasure.json).

For any preparation with positive occupied bins, and the ordinary target, \(\eta_{\max}(q,p)\to1\) as \(q\to1\), because all box endpoints are continuous and at one \(\eta_{\max}=1\). Thus for **every** fixed \(0<\eta<1\), some common finite \(q\ne1\) reproduces the entire detected and no-click distribution exactly if terminal erasure is unconstrained by label. Even recording no-click on every incident launch leaves this ambiguity. The ceiling still distinguishes specified exponents at sufficient retention. The [cesium selection calculation](Cesium_negative_read.md) compares two empirical histograms to a common unknown source. Here the source is constrained to the walk's admissible powered responses.

## When lost records still permit exact selection

If post-score acceptance at each bin is a known positive \(e_x\) conditional on that label for the science population, divide each incident click rate by \(e_x\) to recover the latent law. Calibration on another population needs an assumption that these rates carry over. If instead every bin within type \(A\) has the same efficiency \(e(A)\), the histogram conditional on a click is a mixture of the original laws reweighted by \(e(A)\). Positive mean efficiency gives an observable click histogram. If \(e(A)>0\) almost surely, the clicked and incident type distributions assign zero to the same events. Exact ordinary click proportions at an instrument with three distinct masses in single-mode bins thus force the ordinary finite exponent on the incident launches. An entirely blind type can have any exponent. Its incident fraction is at most \(1-\eta\), a bound attained by a fully efficient ordinary type and a fully blind alternative type. These arguments cover exact population probabilities.

One way to produce equal within-type efficiencies is to choose uniformly among the cyclic shifts of all occupied bin labels and decode every click using the assigned shift. The output channels may have type-dependent efficiencies \(e_j(A)\). Assume the shift is fresh and independent of the type and latent output, leaves the powered bin law intact up to permutation, and that the only losses attach to the physical output channel after routing. For **each** original bin and type the mean survival is then \(\sum_j e_j(A)/n\), where \(n\) is the number of routed bins. This extends the earlier three-target routing argument to all bins so that the entire recovered histogram, including the second constraint for maximal-cell types, can be used. A metadata change made after an outcome-dependent loss cannot equalize that loss. Marginally uniform routing can also fail if the assigned shift reveals the detector type. The checker keeps explicit failures of both assumptions and includes a completely blind type. Randomized terminal relabeling has an experimental precedent for qubit readout with a different error channel. [Prior three-site control](Three_signed_ticks_and_the_probability_power.md) · [Smith et al., bit-flip averaging](https://arxiv.org/abs/2106.05800)

The [checker](check_terminal_erasure.py) reconstructs the three instruments from the archived signed terminal amplitudes, checks the upper inequality on every distinct partition vector for the three tabulated powers, and constructs explicit mixtures and acceptances attaining every displayed bound. No terminal efficiency of a physical six-well instrument has been measured here. Interference lost before the terminal operation, additive background, and incorrect labels each require a response model of their own.
