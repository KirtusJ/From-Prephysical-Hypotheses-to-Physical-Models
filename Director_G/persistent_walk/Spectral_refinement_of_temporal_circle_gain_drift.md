# A spectral refinement of the necessary temporal gain change in the optical circle

Kirtus Justus, research direction. OpenAI GPT-6, mathematical derivation and executable control. 15 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

**Result, conditional on a previously digitized figure.** The two-round, three-site optical-circle comparison imposes a larger necessary change in *relative* site gains than the earlier pair-sum calculation. Under the homogeneous ten-site coin, arbitrary (and even different) localized launch-rail density matrices in rounds 11 and 13, positive site gains common to both output rails, and a freely changing overall round normalization, at least one of the ratios `g_7/g_5` or `g_7/g_9` must grow from round 13 to 11 by a factor of **at least 1.9115354124…**. The previous necessary bound was strictly above 1.881069. If each individual site's physical gain is constrained to vary by at most a symmetric multiplicative factor `D`, the necessary factor becomes `D >= 1.3825828772…`, rather than the earlier `D > 1.37152`. These numbers apply to the recorded color-interval *model*, not to observed gain drift of any detector.

## Pinned sources and assumptions

- Primary physical reference: Lorz et al., *Photonic quantum walks with four-dimensional coins* (2019), Eq. (13) and Fig. 7(c), [DOI 10.1103/PhysRevResearch.1.033036](https://doi.org/10.1103/PhysRevResearch.1.033036). The figure is an external publication, but this refinement **does not re-digitize** its pixels or use raw hardware counts.
- Prior scientific work: [three unequal circle detectors, PR #301](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/301), pinned merge `8bffdb4020a2bfa3d2b399bda11a49f9671ceedb` and saved interval file `unequal_circle_gains_output.json` (Git blob `772ed8386297f93e5564f06b7f0c835523b1b9b7`, provenance only); [temporal drift bound, PR #302](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/pull/302), merged head `aef436b19d473cb999b9bf626dc09ebb7f5240bd`. The source intervals were transcribed from a color legend with an eight-level RGB allowance, not statistical confidence intervals.
- Hypotheses: `H'=(I-iX)/sqrt(2)`, nearest-neighbor `R/L` shifts on ten sites, launch at site 2. The site intensity is `q(t,m)=k(t)*g(t,m)*p(t,m)`, with `k(t)>0` arbitrary, `g(t,m)>0` weighting **both outgoing rails equally**, and an arbitrary launch rail state that may vary between the two rounds. Gains and intensities here describe a model of the displayed figure; nonlinear detectors, backgrounds, other source channels and polarization-dependent gain are outside the hypothesis.

## Independent spectral calculation

The exact integer-Gaussian-amplitude recurrence for the specified coin gives the two-rail probability effect at site 5 in round 11,

\[
E_{11,5}=\frac{1}{2048}\begin{pmatrix}505&351i\\-351i&397\end{pmatrix}.
\]

Its reflected partner at site 9 completes a scalar operator. The antipode at site 7 is separately scalar. Consequently, for any launch density matrix, including a mixed state,

\[
S_{11}=p_{11,5}+p_{11,9}=\frac{451}{1024},\quad p_{11,7}=\frac{281}{1024},
\quad S_{13}=p_{13,5}+p_{13,9}=\frac{699}{2048},\quad p_{13,7}=\frac{941}{4096}.
\]

At round 11 let `z=p(11,5)`. By the spectral maximum of `E_(11,5)`,

\[
0<z\le z_{\max}=\frac{451+\sqrt{126117}}{2048}.
\]

Write `w=p(13,5)`, so that the other reflected site has probability `S_13-w`; both are positive for the model. Let `x_t=g(t,7)/g(t,5)` and `y_t=g(t,7)/g(t,9)`. With `K=max(x_11/x_13,y_11/y_13)`, the separately recorded lower and upper bounds on the three displayed intensities imply

\[
K\ge \max\left\{A\frac{z}{w},\;B\frac{S_{11}-z}{S_{13}-w}\right\},
\quad A=\frac{13986083}{9594464},\quad B=\frac{2596219}{1545500},\quad A<B.
\]

The coefficients use the lower bound for `q(11,7)`, upper bound for `q(13,7)`, lower bounds for both round-13 reference sites, upper bounds for both round-11 reference sites, and the exactly calculated ratio `p(13,7)/p(11,7)`. Multiplying the two entries in the maximum by positive weights `w` and `S_13-w`, then taking the weighted mean, gives

\[
K\ge \frac{Az+B(S_{11}-z)}{S_{13}}
\ge K_*:=\frac{451(A+B)+(A-B)\sqrt{126117}}{699}
=1.9115354124759\ldots .
\]

The last inequality uses `A-B<0` and `z<=z_max`. Exact square comparisons `355129^2 < 126117*1000^2 < 355130^2` enclose the radical and certify `1.9115352 < K_* < 1.9115358` without floating-point assumptions. Every choice of round-specific launch state obeys the bound. A symmetric individual-gain drift limit `1/D <= g(11,m)/g(13,m) <= D` gives `K<=D^2`, hence the stated bound on `D`.

**Limit of sharpness.** For these *three independently allowed interval bands only*, the lower bound is attainable: choose the round-11 state to maximize `z`; choose `w=A*z_max/K_*`, approximately `0.3001704432`, for round 13. The allowed spectrum of round-13 site 5 is

\[
\frac{2796-\sqrt{5732480}}{16384}\le w\le\frac{2796+\sqrt{5732480}}{16384},
\]

which contains this witness. Choose the six displayed intensities at the permissive interval endpoints and set positive site gains accordingly. This establishes sharpness of a restricted *interval relaxation*, **not** sharpness after enforcing all other plotted cells, correlations in the image calibration, or physical detector data. The three-site figure data and the states were not independently observed here.

## Executable record and limits

The accompanying [checker](check_spectral_circle_gain_drift.py) reads the pinned saved interval data and independently builds the two-rail effects with integer Gaussian amplitudes. It checks source coefficients, exact spectral identities, the rigorous radical brackets, and the round-13 witness. In a fresh isolated Python directory, with the saved JSON reconstructed byte-identically to the Git blob, `python -I -B check_spectral_circle_gain_drift.py` and `python -I -B -O check_spectral_circle_gain_drift.py` both exited zero with identical output. Three disposable input mutations (a figure band, the round-11 orbit ratio, and the prior constraint) exited nonzero in both modes. These controls test source binding, not the accuracy of the published raster or an instrument.

**Disposition:** a mathematical strengthening within a stipulated source-figure and detector-response model, pending external experimental validation and independent source-reading review. No new observation, hardware calibration, chosen ontology, completed physical-identification gate, or closure of Stage 1 Initial External Grounding or root review G1 follows.
