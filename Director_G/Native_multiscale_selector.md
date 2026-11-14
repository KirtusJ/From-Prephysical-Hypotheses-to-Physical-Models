# Selecting the unit sheet character with the unmodified walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Start the sheet at one address on the signed staircase of order $M\ge3$. Start the walker at a specified well and rail on the $4M$ ring. Use an ordinary Hadamard and stream on every tick, with sheet increment $\lfloor x/2\rfloor$ at each departure. The controller reads only the base position and rail at preassigned clocks. For $0<\epsilon\le1/4$, it can herald the folded character one with conditional weight at least $1-\epsilon$, in $O(M^{2/3}[1+\log(1/\epsilon)])$ physical ticks per original launch. The herald captures at least $1-\epsilon/4$ of the incident unit pair, whose total prior weight is $2/M$. For fixed small error and fixed target completeness, the power $2/3$ is optimal for this class of sharp-record experiments. The argument assumes the normalized squared-coordinate law, ideal sharp instruments and continued evolution in the same sheet after each read. [One-block resolution bound](Uninterrupted_sheet_read.md) · [Critical fringe for fixed pairs](Uninterrupted_sheet_fringes.md) · [Earlier three-tick and routed selectors](From_a_local_sheet_to_a_flight.md)

## Reusing the original preparation

Every operation commutes with sheet translation. A localized sheet gives a uniform prior, so each sheet-blind transcript $w$ has probability $M^{-1}\sum_s\Pr_s(w)$. Observing $w$ updates the relative Fourier weights according to its sector likelihoods. Conditional on one character and a sharp read, the base is a new known well and rail. A translation of the launch well from $0$ to $h$ changes the gain at tick $u$ by a scalar common to all paths at that clock, since the departure offsets all have parity $u\bmod2$. The factorization holds across the seam, where adding $4M$ to a departure adds $2M$ to its gain.

When the incoming rail is L, reflect the displacement about its starting well and exchange the rail names when scoring the read. This takes a path from an R launch to its complementary path from L. For departure offset $y$ on the R path, the sum $\lfloor(h-y)/2\rfloor+\lfloor y/2\rfloor$ depends only on $h$ and the parity of $y$. The complemented gain thus produces the conjugate of the original relative phase. The ratio of the two path signs is $(-1)^{t+b}$, where $b=1$ for a final L on the R path and $b=0$ otherwise. Indeed the number of direction changes modulo two is $b$, while complementing exchanges RR and LL stays. This factor is common at a fixed terminal port. Consequently the corrected read has the same probability law from either rail and any starting well, for either signed representative of the folded label. Conditional on the sector, successive corrected reads at prescribed block durations are independent. Averaging over the unknown persistent sector generally correlates them. The preparation uses the observed endpoints as successive starting wells with no return-to-home operation. [Lean proof of the word, reflection and seam identities](lean/NativeSheetSelector.lean)

## Comparing a band of labels in one experiment

Fold the sector index to $s\in\{0,\ldots,\lfloor M/2\rfloor\}$. Give label zero its own stage, designated $d=1$. The other stages use $d=2^j$, $j\ge1$, up to $d\le\lfloor M/2\rfloor$, and compare unit against
$S_d=\{d,\ldots,\min(2d-1,\lfloor M/2\rfloor)\}$. Put $N=M/d$. The candidate block duration $t$ is the largest integer with $4d^2t^3\le M^2$.

After the read use the canonical displacement $x$ and rail for an R launch. For R and $v=x/t\in[1/4,1/2]$, set

$$
 \kappa=\arccos\!\frac{v}{\sqrt{1-v^2}},\quad
 \omega(k)=\arcsin(\sin k/\sqrt2),\quad c(v)=(1-v^2)\sqrt{1-2v^2},
 \quad a(v)=(1+v)/2,\quad \Phi=2x\kappa-2t\omega(\kappa)+\pi/2.
$$

Assign $F=-\sin\Phi$ to this outcome and zero elsewhere. The same statistic is used for every band. The compact spatial window supplies a family of rapid oscillations with a relative phase that depends on the charge. It does not require an externally supplied phase on the walker. Summing the wells into a single spatial bin before scoring would remove information needed by the test.

Write $\gamma_s=\pi^2s^2t(t^2-1)/(12M^2)$ and
$J(\gamma)=\pi^{-1}\int_{1/4}^{1/2}(a^2/c)\sin(\gamma c)\,dv$. The mean of the **unrounded** statistic on every $0\le s\le2d$ satisfies

$$
 \mathbb E_sF=J(\gamma_s)+O(N^{-1/3})\qquad(N\to\infty),
$$

where the same error constant works for every $d,M,s$. To see this, center the $t$ momentum queries in the Hadamard eigenframe as in the fixed-pair proof. If $h_s=\pi s/M$, the norm error in replacing the state, up to a position-diagonal phase, by its two dispersive bands carrying curvature multipliers $\exp(\mp i\gamma_s\omega''/2)$ is $O(t|h_s|+t^5h_s^4)$. Here $|h_s|\le2\pi/N$, $t\asymp N^{2/3}$, so this is $O(N^{-1/3})$ uniformly. The model is identified with the line before this approximation by finite propagation.

The approximating R-port probabilities on the occupied parity in the window are

$$
 \frac{4a^2}{\pi t c}\,[1+\cos(\Phi+\gamma_s c)]+O(t^{-2}).
$$

The nondegenerate stationary-phase errors are uniform because $\gamma_s\le\pi^2/12$ and the window is compactly inside the ballistic cone. In multiplying by $-\sin\Phi$, the nonoscillatory term is $\tfrac12\sin(\gamma_s c)$. In the remaining terms the phase increments per occupied parity site tend to $4\kappa$ or $8\kappa$. Both ranges are separated from multiples of $2\pi$ on this window: $\pi/4<\kappa<\pi/2$ there. The smooth amplitudes and correction phases have uniform derivative bounds. Summation by parts on the parity lattice makes these terms $O(t^{-1})$ after normalization. The ordinary Riemann sum has well spacing $2/t$, yielding $J$ with the coefficient shown. Norm error of the original state is used on the expectation of this bounded statistic, rather than as a relative error estimate on rare ports. [Stationary pair, parity replica and summation](Uninterrupted_sheet_fringes.md) · [Free walk oscillations, Sunada and Tate](https://arxiv.org/abs/1108.1878)

In the range $0\le\gamma\le\pi^2/12$ one has $J'(\gamma)\ge25/(512\pi)$, since $a\ge5/8$, the interval length is $1/4$, and $\cos(\gamma c)\ge1/2$. Rounding the clock gives $t(t^2-1)=N^2/4+O(N^{4/3})$. For every $d\ge2$, the difference $\gamma_s-\gamma_1$ on $S_d$ is at least $\pi^2/64-O(N^{-2/3})$. Thus the prospective fringe gap $\min_{s\in S_d}(\mathbb E_sF-\mathbb E_1F)$ has uniform lower limit at least $25\pi/32768$. At $d=1$, the prospective gap in the opposite direction, $\mathbb E_1F-\mathbb E_0F$, has lower limit at least $25\pi/24576$.

## Defining the experiment at every finite order

Small blocks may contain no qualifying well. Use a finite calibration rule, without estimating a crossover from plotted results. Round each $F$ to the nearest multiple of $2^{-15}$, breaking ties toward zero. Let $G=1/2048$. Use that rounded fringe score only if its actual gap, in the indicated direction against every member of the stage, is at least $G$. Each score changes by at most $2^{-16}$ on rounding. The uniform bound above leaves more than $G$ after allowing $2^{-15}$ for a difference of means, so all sufficiently large $N$ pass. The finite criterion uses quantities in the specified model, not acquired observations.

The finite compiler uses standard-library integer and rational arithmetic. For a scored R port, put $b=t^2-x^2$, $u=t^2-2x^2$. Then $e^{2i\kappa}=(3x^2-t^2+2ix\sqrt u)/b$ and $e^{2i\omega(\kappa)}=(x^2+it\sqrt u)/b$. Thus $-\sin\Phi=-\Re(e^{2ix\kappa-2it\omega(\kappa)})$ is rational, and halfway cases round exactly. A signed integer recurrence in physical base and sheet coordinates gives a score polynomial $P(z)$, with the sector-$s$ mean equal to $P(e^{2\pi i s/M})/(2^{15+t})$. For a comparison of means the compiler subtracts the threshold and tests exact zero by division by the $M$th cyclotomic polynomial. For a nonzero comparison it encloses the real part by rational cosine bounds at successively finer precision until its sign is determined. It also returns the nearest competing mean and the threshold as exact root-of-unity expressions. The classical computation can exceed the walk-clock costs. [Finite stage compiler](certify_native_stage.py)

From the supplement directory, run `python -B certify_native_stage.py 17 1` for one stage or `python -B certify_native_stage.py --examples --output REPLAY.json` for the ten archived stages. At $M=17,d=1$ the nonempty fringe uses integer numerator $-14788$ at $(2,R)$ after four ticks and has gap between $0.0223416804$ and $0.0223416805$. At $M=97,d=8$ every candidate fringe comparison fails. Its three-tick replacement has gap above $0.03229$. The archive includes the integer coefficients, signed comparison outcomes and directed enclosures. Fresh ordinary and optimized Python replays agree byte for byte. [Certified stage records](results/native_stage_certificates.json)

If the fringe stage fails that comparison, take **three native ticks** and use the indicator of the canonical output $(-1,L)$. Its probability is $p_s=\tfrac12\sin^2(\pi s/M)$, from two oppositely signed histories differing by one gain. It increases strictly over the folded sector interval. For $d\ge2$ compare $p_1$ with $p_d$, and for the zero stage compare $p_0$ with $p_1$. The replacement gap is positive at every finite order. The set of stages requiring it also has a uniform positive gap. Indeed they have $N\le N_0$ for some fixed $N_0$ by the fringe estimate. For $d\ge2$,

$$
 p_d-p_1\ \ge\ \frac12\left[\sin^2(\pi/N)-\sin^2(\pi/(2N))\right].
$$

The right side has a positive minimum on $2\le N\le N_0$. At a replaced zero stage $M=N\le N_0$, so $p_1\ge\tfrac12\sin^2(\pi/N_0)>0$. These bounds establish a common positive gap without requiring the experimenter to know $N_0$ or its magnitude. The finite scheme above determines the actual gap at each stage. [Exact three-tick probabilities](Refining_the_sheet.md)

## Conditional errors, original yields and clock costs

Let $g_j$ be the actual smallest stage gap used in this calibrated schedule, with $j=0$ for the zero test. Use the midpoint between the unit mean and the closest competing mean as the threshold. The unit side is above it at $j=0$ and below it in every other stage, for either type of score. Set

$$
 h_j=\frac{\epsilon}{8(j+1)^2\,2^j},\qquad
 r_j=\left\lceil\frac{8}{g_j^2}\log(1/h_j)\right\rceil .
$$

Run all $r_j$ blocks in the stage and compare the average with the threshold. Accept the original launch if every stage returns the unit decision. Under each sector the score is independent on repetition, lies in $[-1,1]$, and is separated from the threshold in its assigned stage by at least $g_j/2$. The one-sided Hoeffding bound makes both the target rejection and every assigned competitor's false passage at most $h_j$ in that stage. This bound uses the distribution conditional on the complete previous sharp record. [Hoeffding, Theorem 2](https://doi.org/10.1080/01621459.1963.10500830)

Write $A$ for the final accept flag. The common conditional acceptance of the conjugate unit pair is at least $1-\sum_j h_j\ge1-\epsilon/4$. At most $2\cdot2^j$ signed competitors are assigned to stage $j$, including the single zero at $j=0$. Each must pass its assigned test. Hence $\sum_{s\notin\{\pm1\}}\Pr_s(A)\le2\sum_j 2^j h_j\le\epsilon/2$, using $\sum_{j\ge0}(j+1)^{-2}<2$. With the localized-sheet prior this gives

$$
 \frac{2(1-\epsilon/4)}M\le\Pr(A)\le\frac{2+\epsilon/2}{M},\qquad
 \Pr(s\notin\{\pm1\}\mid A)\le\frac{\epsilon/2}{2(1-\epsilon/4)}<\epsilon .
$$

Every original launch produces an accept or a reject. The reported weights describe the Fourier masses of the conditional state for subsequent compatible sheet-blind evolution. The selected pair's orientation remains unresolved. In an order-three example, a first read at $(1,R)$ after three ticks followed by a read at $(3,R)$ four ticks later has probability $12/128$ with the persistent sheet. Inserting a new localized sheet after the first read gives $6/128$. The independent checker retains all such finite two-record outcomes, its rounded finite comparisons, and fringe settings that fail and use the fallback. The floating-point schedule checks supplement the exact finite definition above. [Independent checker](check_native_multiscale_selector.py) · [Full finite records](results/native_multiscale_selector.json)

The gaps $g_j$ have a positive uniform lower bound. Thus $r_j=O(1+\log(1/\epsilon)+j)$. The longer of the candidate and replacement clocks is at most a constant times $(M/2^j)^{2/3}$. The geometric series weighted by $1+j$ converges, giving the worst-case deterministic tick count per original launch
$O(M^{2/3}[1+\log(1/\epsilon)])$. Requiring every stage to have the same false-passage bound would obscure the geometric saving. The physical protocol places complete measurements at known clocks and uses no active coin or sheet controls. It requires precise endpoint locations and a clock capable of following the blocks across a run. Recording latency is included up to a bounded number of extra clock units per read if the base evolution can be held during it.

For necessity, fix $\epsilon<1/3$ and a sector-one completeness $q>0$ independent of $M$. Any scheme with posterior error at most $\epsilon$ obeys $\sum_{s\notin\{\pm1\}}\Pr_s(A)\le2\epsilon\,\Pr_1(A)/(1-\epsilon)$ under the localized prior and these real controls. In particular, zero and unit must have acceptance probabilities separated by a fixed positive amount. Full transcripts of even adaptively chosen sharp-read blocks of the unmodified walk have vanishing variation between zero and unit in $o(M^{2/3})$ elapsed ticks from one well. The proposed upper and lower powers therefore match at fixed confidence and completeness. This lower bound on elapsed time does not establish optimal dependence on $\epsilon$ or select the probability law of the carrier. [Adaptive sharp-read bound](Uninterrupted_sheet_fringes.md)

The 13-order finite census contains 65 folded-label stages. Eight fringe comparisons reversed sign; 33 more had no qualifying well. The schedule retained all 41 fallbacks. At order 1024 and requested error 0.1, adding the count test and using the actual score ranges gave a sufficient budget of 204,001,782 ticks in the one-pass schedule. Its localized coherent posterior bound was 0.01302. The finite numerical budgets use binary64 means. The [certified stage compiler](certify_native_stage.py) separately decides exact readout choices and thresholds. These sufficient budgets need not minimize the number of ticks.

## Early rejection and the cost per original launch

The uniform incident sheet puts most of its weight on the sectors that can be rejected with short blocks. The following ordering keeps the same worst-case time and reduces the **mean tick count per original launch** to $O(1+\log(1/\epsilon))$, independently of $M$. Use the same calibrated stages, scores and thresholds as above. Let $J=\lfloor\log_2\lfloor M/2\rfloor\rfloor$. At layer $\ell=0,\ldots,J$, the newly opened band is $j=J-\ell$, and the tests in the layer are

$$
 j,j+1,\ldots,j+w_\ell-1,\qquad w_\ell=\min(\ell+1,J-\ell+1).
$$

For each such test of band $i$, take a fresh batch of $\lceil8g_i^{-2}\log(1/b_\ell)\rceil$ blocks, $b_\ell=\epsilon/(64w_\ell^3)$. Stop and report rejection on the first failed test. Report acceptance after the last successful test. Freshness here concerns new sharp base records from the continuing sector, with no reset of the sheet. The per-test false decision bound holds conditional on all earlier decisions within that sector. Put $q=\epsilon/64$.

The target rejection probability is at most $\sum_\ell w_\ell b_\ell\le\epsilon/16$: each positive window size occurs at most twice, and $\sum_{w\ge1}w^{-2}<2$. Band $i$ opens at $k=J-i$. Its test at layer $k+r$ is included precisely when $0\le r\le\lfloor i/2\rfloor$, because $r<w_{k+r}$ amounts to $2r\le i$. A wrong sector in this band must therefore pass $\lfloor i/2\rfloor+1$ assigned tests, each with conditional probability at most $q$. Summing over all signed competitors gives

$$
 \sum_{s\notin\{\pm1\}}\Pr_s(A)\le2\sum_{i\ge0}2^i q^{\lfloor i/2\rfloor+1}=\frac{6q}{1-4q}.
$$

Thus the per-launch herald yield lies between $2(1-\epsilon/16)/M$ and $[2+6q/(1-4q)]/M$. The error conditional on a herald is at most $[6q/(1-4q)]/[2(1-\epsilon/16)]<\epsilon$ over the stipulated error range.

To reach layer $\ell$, a sector in a band opened $r=\ell-k>0$ layers earlier must already have passed $\min(r,\lfloor i/2\rfloor+1)\ge r/2$ assigned tests, since $r\le i$. The prior mass of the band opened at $k$ is at most $2\,2^{J-k}/M\le2^{-k}$. Bands opening at or after $\ell$ have total mass at most $2\,2^{-\ell}$, and the unit prior is at most $2^{-\ell}$. Consequently

$$
 \Pr(\text{reach layer }\ell)\le2^{-\ell}\left[3+\sum_{r=1}^\ell(2\sqrt q)^r\right]=O(2^{-\ell}).
$$

The worst duration of a reached layer is $O(2^{2\ell/3}[1+\log(1/\epsilon)+\log w_\ell])$: the test-duration upper bounds decrease geometrically with the band index, and $2\le M/2^J<4$. Multiplying by the reach bound leaves a summable factor $2^{-\ell/3}$ even with $w_\ell\le\ell+1$. This proves the claimed mean. To bound the worst time for the same stopped schedule, sum the layer durations without the reach factor and use $w_\ell\le J-\ell+1$. This gives $O(M^{2/3}[1+\log(1/\epsilon)])$. An accepted trajectory runs through every scheduled test and uses this full clock.

If rejections trigger **independent fresh localized launches**, the expected number of launches through the first herald is $1/P(A)$, and the expected total walk time is $\mathbb E[T]/P(A)=O(M[1+\log(1/\epsilon)])$. For the latter identity, conditioning on the first launch gives $E=\mathbb E[T]+[1-P(A)]E$; duration and success need not be independent on that launch. A cap of $n$ fresh launches gives timeout probability $[1-P(A)]^n$ and expected total ticks $\mathbb E[T]\{1-[1-P(A)]^n\}/P(A)$. The first herald's conditional target weight is unchanged by the number of preceding failed fresh launches. The latent true-target herald probability per launch is $(2/M)\Pr_1(A)$; an observer with no additional sector measurement can stop only on the herald flag. Source replacement and classical table generation have their own resource costs. Reusing the discarded sheet would produce a different prior.
