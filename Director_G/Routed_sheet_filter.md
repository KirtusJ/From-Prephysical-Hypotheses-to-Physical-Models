# Selecting one folded sheet character with real routing

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Start with the sheet at a single site, the base at a fixed home, and a known rail. On a cyclic sheet of order $M\ge3$, the initial Fourier weight on the pair $\{1,-1\}$ is $2/M$. We give a real controller that accepts nearly all of this pair and bounds the false acceptance in every other sector. It makes every interference measurement at the same base home and uses the native departure gain on every tick. Its cost per initial launch is $O(\sqrt M\log(M/\epsilon))$ streamed ticks with supplied random settings. The accepted fraction is of order $1/M$. This is a preparation within an assumed squared-coordinate readout and supplies no independent selection of that readout. [Single-walk square and count laws](Counting_and_character_records.md) · [Earlier linear-gain returning loops](Returning_loops_and_one_classical_ray.md)

## What the apparatus does

Use the $4M$-site ring with rails R,L and a sheet translation by $g(x)=\lfloor x/2\rfloor\bmod M$ on departure. The stream advances one well per tick. Supply three possible global real rail settings before the stream: the balanced Hadamard $H$, straight propagation $I$, and interchange $X$. The latter two are coherent routing controls. The terminal analyzer reports which of two outgoing oriented ports fired. Its read is complete, and the sheet remains unmeasured. Every operation commutes with sheet translations. As a consequence the statistics of sheet-blind records equal a mixture over the $M$ Fourier characters with uniform prior. Conditional on a record, the normalized sector weights obey Bayes' rule. This statement concerns the sheet-blind experiments, including subsequent translation-invariant propagation. A definite sheet position is a coherent superposition in Fourier coordinates.

Given a lag $\ell\in\{0,\ldots,M-1\}$, use one $H$ streamed tick to split. Choose a length-$2a$ word $w$ starting on R, ending on L, with $a$ occurrences of each rail. At each later tick continue the direction with $I$ or exchange both directions with $X$, as prescribed by consecutive letters of $w$. Exactly two words propagate, $w$ and its complement. Both return to home $h$ after $2a$ ticks, on opposite rails. No detector identifies the arm. With $z_t$ the displacement on $w$ immediately before the $t$th departure, their register gain difference is exactly

$$
\sum_t\left[\left\lfloor(h+z_t)/2\right\rfloor
                 -\left\lfloor(h-z_t)/2\right\rfloor\right]=\sum_t z_t .
$$

The two arguments of the floors differ by the integer $z_t$. Wrapping a departure by $4M$ changes its gain by $2M$. The return and gain difference therefore work for either launch parity and across the ring seam.

The maximal positive area is $a^2$ for $R^aL^a$. Interchanging an adjacent interior $RL$ to $LR$ subtracts two from the area. All inversion counts $0\le j\le(a-1)^2$ occur among the $a-1$ interior R and $a-1$ interior L letters. One explicit construction moves the first several interior L letters ahead of all interior R letters, then one more L ahead of the required remainder. Let $A=\max(4,\lceil\sqrt{M-1}\rceil)$. Choose $a=A$ or $A+1$ with $a\equiv\ell\bmod2$. Then $a^2-2(a-1)^2\le0\le\ell\le a^2$, and $j=(a^2-\ell)/2$ realizes the specified lag. The area bound $|\sum z_t|\le a^2$ follows from the return light cone $|z_t|\le\min(t,2a-t)$ for departure indices $t=0,\ldots,2a-1$. It concerns two returning paths and an unwrapped gain difference.

Apply a second $H$ streamed tick at the reunion. Let $Y=+1$ if the outgoing rail equals the known initial rail and $Y=-1$ otherwise. If the initial rail is L, the first $H$ changes the relative sign. Exchanging the designation of the two analyzer outcomes corrects it. In character $s$ the two port probabilities are

$$
\Pr_s(Y=y\mid\ell)=\frac{1+y\cos(2\pi s\ell/M)}2,\qquad y=\pm1.
$$

The analyzer moves the walker one well away. Record the port and apply an $X$ streamed tick to bring both possible outcomes back to home. On either outcome the next input rail is known. The return translates the sheet by a known amount on that branch and preserves all sector weights. Starting the next probe immediately gives a total of $2a+2\le2A+4$ streamed ticks per probe. No common accumulated phase or fixed rail between probes is needed.

## A decision using integer arithmetic

Independently choose a uniform $\ell$ for every probe and put

$$
f(\ell)=1-4\min(\ell,M-\ell)/M,\qquad Z=Yf(\ell).
$$

Conditional on $s$, the pairs $(\ell,Y)$ are independent across probes because their laws are the same on every known incoming rail and every completed record. The conditional mean of $Z$ is the real Fourier coefficient $b_t=M^{-1}\sum_\ell f(\ell)\cos(2\pi t\ell/M)$ with $t=\min(s\bmod M,(-s)\bmod M)$. There is a uniform gap between $t=1$ and every competitor.

For $f$ the periodic second difference $2f_j-f_{j-1}-f_{j+1}$ is $8/M$ at zero. For even $M$ its only other nonzero value is $-8/M$ at $M/2$. For odd $M$ the two central wells have $-4/M$ each. The Fourier multiplier is $4\sin^2(\pi t/M)$. Summing $f$ gives $b_0=0$ for even $M$ and $b_0=1/M^2$ for odd $M$. At $t\ge1$ the remaining cases are

$$
\begin{array}{c|cc}
 &t\ \text{odd}&t\ \text{even}\\ \hline
 M\ \text{even} &4/[M^2\sin^2(\pi t/M)]&0\\
 M\ \text{odd} &1/[M^2\sin^2(\pi t/(2M))]&1/[M^2\cos^2(\pi t/(2M))]
\end{array}
$$

Thus $b_1\ge4/\pi^2>2/5$. For odd $t\ge3$ the chord inequality $\sin x\ge2x/\pi$ on $[0,\pi/2]$ gives $b_t\le1/t^2$. For even $t\ge2$ at odd order, $M\ge5$ and $b_t\le2/M^2$. The DC entry is at most $1/9$. Every nonordinary folded sector therefore has $b_t\le1/9$.

After $k$ probes accept if $\sum Z\ge k/4$. Equivalently compare the integer $4\sum_iY_i[M-4\min(\ell_i,M-\ell_i)]$ to $kM$. Each $Z$ lies in $[-1,1]$. The smaller distance of the threshold from the two mean bounds is $5/36$. Hoeffding's inequality bounds the target miss and each other sector's false acceptance by $\beta=\exp(-25k/2592)$. Replacing the rational weight by a classically evaluated exact cosine gives means $1/2$ or zero by cyclic orthogonality and the sharper $\beta=\exp(-k/32)$. The integer test needs no such evaluation. Both implementations use the same real physical pulses. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

The probability of an accepted target on any original launch is at least $2(1-\beta)/M$. The probability of an accepted wrong charge is at most $(1-2/M)\beta$. Hence

$$
\Pr(\text{wrong}\mid\text{accepted})\le
\frac{(M-2)\beta}{2(1-\beta)+(M-2)\beta}.
$$

For $0<\epsilon\le1/2$, $k=\lceil(2592/25)\log(M/\epsilon)\rceil$ suffices. The same bound on false acceptance gives total accepted mass at most $2/M+(1-2/M)\beta$. Rejections retain the complementary mass. With independent localized restarts, the mean number of original launches to one herald is at most $M/[2(1-\beta)]$. Merely observing more records on a copy after rejecting it does not refresh its uniform prior.

Uniform classical settings can also be supplied by the walker. From the known home rail an $H$ stream and sharp outgoing read produce a fair bit in every sector. $X$ streams back to home. Each outcome's conditional operator on the sheet is a signed translation times $1/\sqrt2$. Draw $b=\lceil\log_2 M\rceil$ bits. If their integer is at least $M$, try again. Each batch succeeds with probability $M/2^b>1/2$, independently of the sector. This adds fewer than $4b$ native ticks on average per probe. If the apparatus allows at most $J$ batches per probe, retain a separate timeout flag. A full $k$-probe run completes with probability $[1-(1-M/2^b)^J]^k$, independent of the sheet character. This factor multiplies both accepted yields and leaves the posterior bound unchanged. The deterministic tick budget is then $k(2A+4+2bJ)$.

## What the filter can distinguish

The real pulses and readout give equal likelihoods for $s$ and $-s$ separately on every transcript. At $M=4$, the exact enumeration over 16 probes accepts the target with probability $64839/65536$ and each competing sector with probability $462411533/4294967296$. The overall success probability is $4711700237/8589934592$, and the target posterior is $4249288704/4711700237$. The checker propagates both input rails through the register for every requested lag, including seam homes. It also retains a control in which the first rail is copied and the copy survives recombination. Tracing those orthogonal flags removes the cross-term. A fixed $H$ on every tick with only a successful two-word relative-direction projection has pre-analyzer success $2^{1-2a}$ and requires a distinct instrument. The high-throughput protocol above assumes coherent deterministic turning and straight motion. [Coordinate-level test](check_routed_sheet_filter.py) · [All terminal and failure controls](results/routed_sheet_filter.json)

The order-four checker also compares two fair-rail alternatives. A conditionally fair analyzer passes the 16-probe selector with probability $462411533/4294967296$. A single fair bit retained throughout the trial can choose the sign of each rail relative to the known sign of its lag weight. Each separate lag has the same fair rail marginal, yet the passing probability is $64839/131072$. A calibrated single read therefore leaves a measurable ambiguity about the repeated record. The counting fraction in a same-walker retry has to be carried through those records. [Persistent count and the flight yield](From_a_local_sheet_to_a_flight.md)

Exact purity has a separate finite obstruction. Allow the same global $H,I,X$ ticks with base-coordinate masks or reads and classical control on the completed transcript. The sheet remains unobserved. On any fixed transcript with $h$ Hadamard ticks, each surviving base amplitude in sector $s$ equals $2^{-h/2}$ times an integer polynomial evaluated at $\zeta^s$, with $\zeta=e^{2\pi i/M}$. Green-light outcomes on intermediate coordinate measurements are treated as unnormalized projections. Distinct recorded alternatives add positive probabilities. Primitive roots have the same minimal polynomial over $\mathbb Q$, so a terminal polynomial vanishes on one primitive character exactly when it vanishes on them all. Thus a finite accepted transcript with positive weight on $1$ has positive weight on every primitive character. If $\varphi(M)>2$, none of these controllers heralds *exactly* folded one at positive yield, even with a countable collection of finite stopping transcripts. A label-blind choice among schedules preserves this statement. Replacing the coordinate projectors or the global rail controls by more general phase-sensitive operators can change the coefficient field and the conclusion. [Conrad, Galois group of cyclotomic fields over the rationals](https://math.stanford.edu/~conrad/121Page/handouts/cyclotomic.pdf)

A real routing pulse consumes a stream tick throughout; increasing the lag uses physical separation and elapsed ticks. For a sharp home and one-well streaming, a comparison with the neighboring trivial sector gives an order-$\sqrt M$ lower bound for a uniform constant difference in acceptance, after all failures are counted. The separate locality proof states which controls and elapsed times it covers. The record theorem here applies to the controlled apparatus. Sector selection with comparable throughput under uninterrupted fixed-coin motion remains open. [Local time and filter resolution](Local_filter_resolution.md)
