# Testing the probability rule and the state change of a position detector

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A dark output can reveal that a position measurement preserved interference. In finite data a small count there could also mean that the apparatus systematically suppresses weak outputs. Five forward ticks from a sharp rail provide a calibration of that suppression. Within a family that powers the squared masses, an observed score bounds the error in **every event probability** of the subsequent detector tests. The calibration and interference tests together address both the displayed frequencies and the underlying linear state change in a coherent measurement of either side of a position cut. A classical path-counting component can be tested with the same five ticks. [Three-tick interference test](Certifying_a_position_read_with_three_forward_ticks.md) · [Three distinct masses in a terminal histogram](When_a_position_histogram_identifies_its_probability_power.md)

## One free calibration flight

Use the reflecting Hadamard walk on \(L\ge11\) wells, with a right-rail source at least five wells from either endpoint. Five ticks are then those of the line, even if a final path lands at an endpoint. The coin sends \((r,l)\) to \((r+l,r-l)/\sqrt2\), followed by a shift in the outgoing direction. Read all final sites and rails. Use the same terminal apparatus as in science, with a known fixed value for the bin-label register on these calibration launches. A trusted bypass or independently characterized transparent operation has to supply this blank setting. If the proposed cut instrument has already passed exact sharp-input tests with faithful terminal support, inserting it on the initial sharp source also leaves a single label and the same walk field. An imperfect sharp test cannot be assumed exact to calibrate itself.

A detector type assigns terminal cell \(i\) probability \(h_i^q/\sum_j h_j^q\) on normalized kinematic squared masses \(h_i\). Each launch has one finite \(q\ge0\), possibly drawn afresh. Empty cells stay dark at \(q=0\). The powered cells are the specified joint labels and directed ports, with the whole unobserved environment pooled within each such cell. Any loss or additional output must enter the apparatus model and the incident denominator. An unobserved subdivision before powering or a setting-dependent bank of response curves would change this test. During the three-tick science experiments the unknown linear isometry that writes the label has a reproducible initial apparatus state. The terminal power acts once after the free continuation on the joint labels and visible outputs. A device that powers a live branch at the intermediate time and renormalizes before continuing is a different instrument.

The squared-mass numerators at the fifth tick are four ones, three fours and one sixteen, all over 32. Among the other ports two carry paths that cancel. The table gives the cells used in the score, with displacement measured from the launch. Each of the 32 direction words is counted in the unsigned column before cancellations.

| Port | Signed total | Squared numerator | Unsigned paths | Score |
|---|---:|---:|---:|---:|
| \((-5,L)\) | 1 | 1 | 1 | 16 |
| \((-3,L)\) | 2 | 4 | 4 | −8 |
| \((3,R)\) | 4 | 16 | 4 | 1 |
| \((-1,R)\) | 0 | 0 | 4 | 0 |
| \((1,R)\) | 0 | 0 | 6 | 0 |

Give all unlisted events score zero. Write \(S\) for the population mean on original launches. With \(t=4^q\), its expectation for one powered type is
\[
 s(q)=\frac{16-8t+t^2}{4+3t+t^2}=\frac{(t-4)^2}{t^2+3t+4}.
\]
It vanishes exactly at \(q=1\), is positive at both \(q=0\) and arbitrarily large \(q\), and tends to one as \(q\to\infty\). Thus \(S=0\) forces the ordinary exponent on almost every launch under this model. The five-tick flight uses one terminal read, with neither intermediate signs nor a controlled inverse. Schreiber et al. implemented a five-step optical walk with polarization as the coin and arrival time as the position read. The proposed comparison requires joint rail and position counts on the specified sharp preparation. [Schreiber et al.](https://doi.org/10.1103/PhysRevLett.104.050502)

## What a nonzero score permits in another experiment

Let \(p(q)\) denote the powered law of any *other* terminal mass vector \(h\) on at most \(m\) cells. The score uses only the calibration flight; \(h\) can change completely between experiments. For \(q>0\), differentiate on the occupied support. In total variation,
\[
 \tfrac12\sum_i|p_i'(q)|
 =\tfrac1{2q}\mathbb E_{p(q)}
       |\log p_i(q)-\mathbb E_{p(q)}\log p_i(q)|
 \le H(p(q))/q \le \log(m)/q .
\]
The first inequality uses \(\log p_i\le0\). Integrating from 1 to \(q\) gives \({\rm TV}(p(q),h)\le \log(m)|\log q|\). For \(1/2\le q\le3/2\), the mean-value theorem gives \(|\log q|\le2|q-1|\le |t-4|/\log 4\), and \(t^2+3t+4\le92\). Outside this window \(s(q)\ge4/23\). Indeed its derivative in \(t\) has the sign of \(t-4\) for \(t\ge1\), and the two boundary values are \(2/7,4/23\). The trivial total variation bound one covers both tails, including zero power.

For \(K_m=\max\{\sqrt{23}/2,\sqrt{92}\log(m)/\log 4\}\), these inequalities give \({\rm TV}(p(q),h)\le K_m\sqrt{s(q)}\). Convexity of total variation and Cauchy–Schwarz now give, for a common distribution of powers in calibration and science,
\[
 {\rm TV}\bigl(\mathbb E p(q),h\bigr) \le \delta_m=\min(1,K_m\sqrt S).
\]
Thus every joint event rate differs from its kinematic squared mass by at most \(\delta_m\) in the stipulated model. This sufficient bound can be loose, particularly on a large output bank. It applies to one fixed set of terminal cells per science setting. Calibration under one exponent and science under another can produce \(S=0\) while retaining a finite error. Unresolved detector gains, a change of source with the setting or type-dependent kinematic states require a separate transfer argument.

**Unsigned path counts.** Suppose a fraction \(f\) of launches counts all direction words fairly. Those launches have mean score \(-3/8\) and return a canceled port with probability \(5/16\). Every finite powered type gives zero at both canceled ports. Let \(d\) be their combined observed rate. Then \(f=16d/5\), and \(S_* = S+6d/5\) is the unnormalized contribution of the powered launches to the score. The resulting event-probability error for identical science fields in the powered component is bounded by
\[
 \delta_m=\min\{1,\ f+K_m\sqrt{(1-f)S_*}\}.
\]
The fair component may have any science outputs for this bound provided its fraction transfers. With \(d=S=0\), the ordinary law is selected in the entire stated mixture class. Ignoring \(d\) would allow \(32/101\) fair launches and \(69/101\) at \(q=3/2\) to give \(S=0\). Their canceled rate is \(10/101\). Calibration errors require simultaneous bounds on the rates from the common sample. A set of compatible values of \(f,S_*\) can be propagated through the displayed bound. A negative central estimate of \(S_*\) is not a population certificate.

## Applying the bound to the reflecting trajectory

The localized tests of the cut detector report joint correct-label and correct-mode rates \(a_i^{\rm obs}\). Use \(\max(0,a_i^{\rm obs}-\delta_m)\) as lower bounds on their kinematic squared masses. In the three-forward-tick tests, use \(\min(1,h^{\rm obs}+\delta_m)\) as upper bounds on each same-side dark-port mass. The [column and graph estimates](Certifying_a_position_read_with_three_forward_ticks.md) now bound the distance between the actual linear dilation, up to unobserved tags, and an ideal coherent cut. In ordinary operational units the resulting bound \(\epsilon\) is on half the diamond distance between their classical-label-and-walk channels. Preparing a spectator, putting a phase inside the detector, or choosing a special hidden outcome has not been used to calibrate the probability power.

For a schedule that stores the successive cut labels and powers the complete resolved table once at the end, with freshly initialized instruments, the total variation error of the reported history relative to the ideal squared word law is at most \(\min(1,\delta_{m_{\rm end}}+\sum_j\epsilon_j)\). Replace the devices one at a time in the ordinary kinematic reference calculation, then use the terminal bound and pool the labels. This requires a calibrated final resolved alphabet of size at most \(m_{\rm end}\). If earlier labels are sampled with nonlinear updates, if the same private apparatus carries memory across reads, or if a detector changes resolution with word length, those operations require their own tests. Along a sequence of carriers the error terms must tend to zero for the [reflected classical trajectory theorem](Reflected_position_histories.md) to transfer.

The finite [signed-path replay](check_forward_power_scale.py), [numerical record](results/forward_power_scale.json) and [Lean 4.19 check](lean/ForwardPowerScale.lean) reproduce the calibration table. This is a proposal for a measured probability panel. It has yet to be run on a physical reflecting walk. Full record laws outside this powered and unsigned mixture class, and an absolute cyclotomic interpretation of the sheets, remain open.
