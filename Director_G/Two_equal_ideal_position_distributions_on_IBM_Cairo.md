# Two equal ideal position distributions on IBM Cairo

On an eight-site Hadamard cycle, six and eight ticks give exactly the same ideal position distribution for every rail state prepared at site zero. Yet in the published optimized IBM Cairo experiment, the displayed fraction at site four falls from about **45.55% to 35.43%**. The discrepancy sets a scale for interpreting a proposed probability test on this hardware. A classical confusion matrix applied to the ideal sites would predict the same distribution at both clocks. Separate, noisy compiled circuits can produce different terminal states before any bit is read.

Luca Razzoli, Gabriele Cenedese, Maria Bondani and Giuliano Benenti implemented both clocks as terminal position experiments. Their initial coin is cos(π/12)|0⟩ + i sin(π/12)|1⟩, with coin zero moving to the preceding site. They report 100,000 shots per circuit. The walker begins at site zero. The implementation uses a Fourier-basis circuit with a terminal inverse transform. At clock zero the circuit still does more than prepare the input. The paper says its data are available by request. This analysis uses the graphics accompanying the authors’ source release. [Published paper, Fig. 8](https://www.mdpi.com/1099-4300/26/4/313) · [Versioned figure source](https://arxiv.org/src/2402.01854v2)

## Which predictions agree

Let K_t(x) send the two input rail coefficients to the final two coefficients at site x. At four ticks K†K=I/8 at both 0 and 4. Any common function of each site’s ideal weight, followed by normalization, gives those sites equal probability, even for a mixture of such functions conditional on the rail. Their displayed heights are 0.1460 and 0.1986. For a normalized table, moving half their difference between them is the smallest change in total variation which makes them equal, about 0.0263 here. A label-dependent reporter can distinguish these sites at a single clock. Both “null” outcomes of the four-tick rail probe carry positive position weight.

The stronger six/eight comparison uses the entire ordered table. At both clocks the eight effects in site order are (1,0,1,0,5,0,1,0)I/8. One may obtain them by applying the integer Hadamard at each site, shifting its first row to the preceding site and its second row to the next site, and dividing squared norms by 2^t. This proves equality for mixed inputs and even for different localized rail preparations at the two clocks. A common function of the whole site table gives identical predictions. A random reporter requires the same conditional reporting law at the two clocks.

For the authors’ particular coin, the full sixteen computational-basis probabilities also coincide. The transfer matrices have real entries. The relative phase i removes their column cross terms. Every squared entry of the unnormalized eight-tick matrices is four times its six-tick counterpart, precisely the change in the normalization. Thus a fixed classical confusion matrix on all four measured bits, followed by reporting position, still predicts equality on the ideal circuits. A coherent rail-sensitive measurement can distinguish states with the same computational-basis probabilities.

## A local measurement of the coin

The two clocks give the same probability of arriving at site four, but they leave different relative phases between the two coin amplitudes there. Those phases can be compared with one common terminal measurement. Using the paper’s coin and site conventions, the site-four transfer matrices from the input coin are

$
K_6(4)=\frac14\begin{pmatrix}3&1\\-1&3\end{pmatrix},\qquad
K_8(4)=\frac14\begin{pmatrix}3&-1\\1&3\end{pmatrix}.
$

Both satisfy $K^\dagger K=5I/8$. Reading the coin in the $X$ basis adds its two amplitudes for the $+$ outcome and subtracts them for the $-$ outcome. For the published input $(\cos(\pi/12),i\sin(\pi/12))$, the squared norms give the following fractions of **all launches**.

| Ideal joint readout at site four | Six steps | Eight steps |
|---|---:|---:|
| Site four, either coin outcome | $5/8$ | $5/8$ |
| Site four, $+$ | $5/16-3\sqrt3/32$ (15.012%) | $5/16+3\sqrt3/32$ (47.488%) |
| Site four, $-$ | $5/16+3\sqrt3/32$ (47.488%) | $5/16-3\sqrt3/32$ (15.012%) |

Complete dephasing of the terminal coin in its computational basis removes the cross term. It predicts $5/16$ for each joint outcome at both clocks. For an implementation, apply the same terminal Hadamard to the coin in each circuit and read position and coin together. Count the launches that yield site four and coin zero. A reversal of the coin readout labels reverses the signed contrast. Comparing interleaved clocks and tracking the position marginal and all launch outcomes would distinguish some circuit and readout changes from the ideal contrast.

Figure 8(b) reports position. The rotated-coin probabilities above are new predictions for the specified circuits. The observed position discrepancy alone supplies no estimate of this coherence. A run would test the coherence surviving at the chosen clocks and the calibration of this measurement. Many microscopic descriptions can give the same two probabilities.

## What the hardware figure resolves

| Duration | Site 0 | Site 1 | Site 2 | Site 3 | Site 4 | Site 5 | Site 6 | Site 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 6 ticks | .1672 | .0195 | .1751 | .0152 | .4555 | .0188 | .1371 | .0115 |
| 8 ticks | .1915 | .0101 | .1684 | .0082 | .3543 | .0238 | .2294 | .0143 |

Panel (b) gives a total variation distance of about **0.1243** between the displayed rows. For normalized tables p and q, any one prediction r has max(TV(p,r),TV(q,r)) ≥ TV(p,q)/2. The midpoint attains the bound. Even an unrestricted common prediction therefore misses at least one displayed distribution by about **0.0622**. Equivalently, in a different model with the same intact subdistribution plus arbitrary replacements in each arm, the largest shared intact mass is the sum of the componentwise minima. Each arm needs an equal replacement budget of at least about 0.1243. This is an extremal fit to the displayed histograms. Neither bound measures the fraction of hardware shots with a particular fault.

At tick 24 the ideal position returns to site zero with probability one. For a point mass the authors’ squared Hellinger affinity reduces to the reported probability at that site. Panel (a) displays about 0.849 at zero ticks and 0.262 at 24 ticks. Its fidelity marker supplies no allocation among the other seven sites. The experiment provides no readout along the intervening path. To test a proposed probability law with these clocks, independently bound the state preparation, the clock-specific circuit error and the reporting drift to the accuracy required by the contrast.

## Replay and cross-checks

The [transcription](results/cairo_cycle_figure8.json) retains all nine optimized eight-bin histograms, all nine plotted ideal histograms, and all thirty optimized fidelity markers. It includes the wrong-parity bars. The [checker](check_cairo_cycle.py) divides bar heights by the corresponding frame height. It leaves row sums as read, with a maximum residual of 0.000108. An independent extraction using a different PDF library and row-sum scaling gave TV 0.12435. The original integer counts and uncertainty in the underlying frequencies cannot be recovered by rounding the transcription.

As a cross-check, computing the authors’ fidelity from the red bars and exact ideal probabilities gives a value above the panel (a) marker by about 0.0310 at tick five (0.9214 versus 0.8904). Substituting the displayed ideal bars gives a difference about 0.0309. The replay prints the signed residual for every overlapping clock. The panels therefore cannot be interchanged at the precision used here. Their underlying shot records and the reason for the discrepancy have not been established. The six/eight comparison uses panel (b) alone.

Run `python check_cairo_cycle.py` in this directory to replay the deposited coordinates and exact integer effects. To repeat the figure extraction, install PyMuPDF and supply the path to the authors’ `DTQW_n3.pdf` as a positional argument. The script checks its SHA-256 before reading the graphics. The [earlier Quito comparison](What_the_encoded_cycle_histograms_measure.md) involves a different measurement schedule.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility for this research program. OpenAI Codex performed the figure extraction, mathematical analysis and computational cross-checks.
