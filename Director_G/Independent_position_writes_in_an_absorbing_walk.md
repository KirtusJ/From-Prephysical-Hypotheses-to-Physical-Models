# How often can a surviving optical walk record its position?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

In the time-multiplexed walk of Nitsche et al., a pulse was split into two directions and removed whenever it reached the origin. Its measured cumulative returns constrain a hypothetical hidden record of the **exact site** of the surviving pulse. Suppose the apparatus independently makes such a record with the same probability \(\gamma\) at each eligible tick. When every tick is eligible, values from zero up to **9.66%** agree with all 18 published continual-return bars under the digitization and ideal walk model below. When only even ticks are eligible, the interval extends to **19.19%** per eligible tick. The same return curve is insensitive to a hidden record of the *side* of the origin at any rate. [Experimental Figure 4 and Methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6025909/) · [Figure extraction, side-record proof and fixed-per-launch comparison](Which_hidden_records_an_origin_sink_detects.md)

## The operation on a surviving pulse

Start at the origin on the right rail. At each tick apply the real Hadamard to the rails, shift one site in their respective directions, and remove the origin on both rails. If the tick is eligible, independently leave a persistent orthogonal tag for each occupied site with probability \(\gamma\). An exact site tag preserves both rails of the same site. The switch probability is independent of the current field, the earlier choices and the subsequent read. Repeat across launches with a common coin, switch law and relative optical response across the three acquisition settings. The model uses ordinary squared optical amplitudes. Random position measurements in coherent walks have also been studied without this absorbing origin. [Kendon and Tregenna](https://doi.org/10.1103/PhysRevA.67.042315)

Let \(Q\) remove the origin and \(U\) denote one coin and translation. From the unnormalized survivor matrix \(\rho\), form \(D=QU\rho U^\dagger Q\). At an eligible tick retain the block at sites \(x,y\) as \(D_{xy}\) for \(x=y\) and \(zD_{xy}\) otherwise, where \(z=1-\gamma\). At other ticks keep every block. At time \(t\) the cumulative return is \(C_t=1-\operatorname{tr}\rho_t\). A write on the final tick leaves this trace invariant. In the first eight ticks with all ticks eligible the calculation gives
\[
 C_2=\tfrac12,\quad C_4=\tfrac58,\quad
 C_6=(44-4z)/64,\qquad C_8=(186-20z-8z^2+4z^3)/256 .
\]
Thus a line joining the fully coherent and fully recorded curves misses the effect of independent writes. In the experiment the first-return numerator at a given tick was divided by total unsunk counts in a corresponding run. The authors checked loss normalization and estimated systematic effects including the coin angle and sink transmission. A different loss response for the proposed recording process would change the comparison. [Experimental Methods, Eq. 16 and error bars](https://pmc.ncbi.nlm.nih.gov/articles/PMC6025909/#sec-4)

## Testing the whole rate interval

For \(t\) ticks the numerator \(2^t C_t\) is a polynomial in \(z\) of degree at most the number of eligible ticks strictly before \(t\). Each coin on the two sides of a density matrix supplies the common divisor two, and a position write introduces at most one power of \(z\). The [replay](check_origin_sink_write_rate.py) propagates integer matrices at distinct integer arguments and interpolates these polynomials exactly. Arguments outside \([0,1]\) are solely interpolation nodes. The checker evaluates the polynomials also at a spare node and compares both physical endpoints against the previously deposited coherent and fully recorded rows. Independently grouping signed paths by every possible write schedule gives the same results at \(\gamma=1/2\) through tick eight.

To establish that the compatible interval has no gaps, write \(-\partial C_t/\partial z=\sum_k a_k z^k\). For its actual degree \(n\), the coefficient of the \(j\)th degree-\(n\) Bernstein basis polynomial is \(\sum_{k\le j}a_k\binom jk/\binom nk\), since expanding a monomial in that basis has exactly these coefficients. The basis polynomials are nonnegative on \([0,1]\) and sum to one. On every nonconstant row the smallest coefficient is strictly positive. Ticks 2 and 4 are constant for the every-tick schedule, as is tick 6 for the even-only schedule. Monotonicity here is an exact finite check for these 18 times.

At zero rate the predicted recurrence lies inside every plotted interval. For each nonconstant row compare its polynomial to its upper cap. Intersect all 18 resulting intervals. Under the published-raster convention the binding cap in each model is \(331/478\) at tick 36. The two table columns bracket the unique roots in \(\gamma\) to the precision shown.

| Eligible ticks | Tick 36 upper-rate root | Tick 34 upper-rate root |
|---|---:|---:|
| Every tick | [0.096602277, 0.096602278] | [0.098501969, 0.098501970] |
| Even ticks | [0.191898555, 0.191898556] | [0.196135810, 0.196135811] |

These extra digits locate roots for reproducibility. Raising the tick-36 cap alone by one further raster pixel, \(1/478\), makes tick 34 decisive in both models. The [complete results](results/origin_sink_write_rate.json) retain the coefficients, derivative checks, cap intervals and root brackets at every clock. The source figure gives shared systematic uncertainties on cumulative points. The intervals here express overlap with those bars. Inferring a physical noise rate would require a model of optical nuisance parameters, their joint effect across clocks and the acquisition uncertainty. Neither schedule has a positive lower bound. If a single recording decision persists for an entire launch, the corresponding compatible launch fractions reach 23.72% and 27.26% instead. [Fixed-launch mixture](Which_hidden_records_an_origin_sink_detects.md)

## A forward return sensitive to memory in the recording choices

Allow arbitrary correlations between the even-tick switches, still chosen independently of the propagating walk. Let \(A,B\) indicate a site record at ticks 4 and 6. Enumerating every schedule, including switches at ticks 2 and 8, gives
\[
 C_8=\tfrac{81}{128}+\tfrac{\mathbb E A}{32},\qquad
 C_{10}=\tfrac{81}{128}+\tfrac{3\mathbb E A+\mathbb E B+\mathbb E[AB]}{64}.
\]
For example, the four tick-ten returns for \((A,B)=(0,0),(0,1),(1,0),(1,1)\) are \(81,83,87,91\) over 128. Suppose the switch marginals at ticks 4 and 6 have the same value \(g\). Then \(g=32(C_8-81/128)\) and the pair probability is \(64(C_{10}-81/128)-4g\). Subtract \(g^2\) to obtain the covariance. A fixed choice has pair probability \(g\), and fresh independent choices give \(g^2\). At \(g=1/2\) the two tick-ten returns differ by only \(1/256\). Both fall within the published bar at that time. With unequal switch marginals the two curves constrain \(\mathbb E B+\mathbb E[AB]\) after determining \(\mathbb E A\). A single pair covariance cannot identify all later switching laws. [Related position-read timing test on a walk with live outputs](Diffusion_from_three_position_records.md)

The result concerns the field and timing convention in the cited optical experiment. It gives an experimental constraint on the disturbance assumed by a particular position-record model. Extending it to a two-output detector on the reflecting walk, or deriving the probability law of its displays, requires additional evidence.
