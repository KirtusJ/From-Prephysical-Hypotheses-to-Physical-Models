# Preparing a phase reference by routing on the staircase

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A walker initially localized at one base site, one rail and one sheet address can be given a fixed positive weight on the unit-character pair at **every** order $M\ge3$. We give real controls and an exact amplitude calculation. The preparation has no herald failures. A subsequent sheet-blind test can select the pair with a prescribed error at a yield bounded below independently of $M$. The base moves one well per tick and only its ordinary staircase increments move the sheet. The preparation needs an additional operation that can switch the rail at specified sheet addresses. [Sheet-blind selector](Routed_sheet_filter.md) · [Earlier dyadic square wave prepared by single-address shifts](Preparing_a_phase_clock.md)

## Constructing the source

Let $b=\lfloor\log_2 M\rfloor$, $L=2^b$, and start on R at sheet address zero. At stage $j=0,\ldots,b-1$ the sheet occupies a cyclic interval of $D=2^j$ sites. The base and rail are sharp. Put the balanced real Hadamard in front of two complementary nearest-neighbor paths. They return to the same base well on opposite rails. The path starting right ends on L and acquires $D$ more sheet units than the path starting left, ending on R. To achieve this, use the area construction for a lag $D$ rather than the full ring order. For departures $x+u$ and $x-u$ the difference of staircase gains is exactly $u$, including modulo $M$ at a seam of the base ring. Straight and turn pulses are real rail permutations. Thus one balanced split translates the original interval into two adjacent intervals on opposite rails, preserving all amplitudes within each. The common translation is fixed by the schedule and launch site. [Area construction and signs](Routed_sheet_filter.md)

The new intervals have combined width $2D\le M$ and are disjoint even when they wrap around zero. At their common base well apply a rail swap at every sheet address of the upper interval and the identity elsewhere. At the last stage also apply sign $-1$ on that interval. Each swap acts on the complete two-rail space at a fixed address. The lower and upper halves now occupy the same rail R at *different* sheet addresses. The operation is reversible. Take one R step to begin the next split. Its sheet increment translates both halves equally. After $b$ stages, up to a known translation, the state on that single base port has amplitudes

$$
\psi(y)=L^{-1/2}
\begin{cases}
 +1,&0\le y<L/2,\\
 -1,&L/2\le y<L,\\
 0,&L\le y<M .
\end{cases}
$$

No device reads the route into an outstanding pointer. If it retains a permanent distinguishable word of all the arm choices, tracing that record leaves a uniform *incoherent* distribution over the interval. Its unit-pair weight is $2/M$ at every order. A classical controller can know the pulse schedule without learning which coherent arm the walker took.

The cost of a split is $2a+1$ streamed ticks, with $a$ at most $\max(4,\lceil\sqrt D\rceil)+1$, and one address-dependent rail operation at reunion. Summing $\sqrt{2^j}$ gives $O(\sqrt M)$ streamed ticks and $b$ patterned switching layers. The clock count assumes that switching an interval is parallel or implemented by a preinstalled address comparator. Serial programming of each cell, transport of control instructions and apparatus construction have their own costs. A change of starting address can translate the instructions if that address is known. Extending the alphabet of available gates, applying arbitrary sheet strides in a single tick or initializing a delocalized sheet would describe different resources.

## Weight, yield and precision

At $z=\exp(2\pi i/M)$ the unnormalized Fourier sum equals $(1-z^{L/2})^2/(1-z)$. Using both conjugate frequencies, the target weight is

$$W_M=\frac{8\sin^4(\pi L/(2M))}{ML\sin^2(\pi/M)}.$$

For $x=L/M\in(1/2,1]$, $\sin(\pi/M)<\pi/M$ gives $W_M>(8/\pi^2)\sin^4(\pi x/2)/x$. This last function of $x$ without the factor $8/\pi^2$ has minimum $1/2$ on $[1/2,1]$. Its derivative in the interior has sign $4t-\tan t$, where $t=\pi x/2$; $\tan t/t$ is strictly increasing, so the minimum is at an endpoint. Hence **$W_M>4/\pi^2$ for all $M\ge3$**. This is the best uniform lower bound, approached at $M=2^{j+1}-1$. At dyadic orders $W_M=8/[M^2\sin^2(\pi/M)]$, tending to $8/\pi^2$. Orders 3 and 4 give unit weight exactly. The constant mode has zero weight at every order.

If the subsequent recorded test accepts a target with probability at least $1-\beta$ and each nontarget with probability at most $\beta$, its per-launch accepted fraction is at least $W_M(1-\beta)$. The unwanted fraction among accepted walkers is at most

$$\frac{(1-W_M)\beta}{W_M(1-\beta)+(1-W_M)\beta}.$$

For fixed desired purity and a supplied setting register, $O(\sqrt M)$ ticks now suffice, including source construction. The sheet support bound shows that this scaling in $M$ is necessary for any protocol of the stated type that produces fixed positive unit-pair weight from a single sheet address. The bound applies even to a rare positive-yield herald. At target error $\eta\to0$, a number of probes proportional to $\log(1/\eta)$ gives total routing cost $O(\sqrt M\log(1/\eta))$. The $O(\log M)$ expected coin ticks per probe for internally generating settings fit this bound. A stopped run with a finite deadline must retain sampler timeouts. Positive error at finite order and time generally remains, as the synchronized path amplitudes have integer numerators and their primitive Fourier support is closed under conjugacy of algebraic roots. [Resolution bound](Local_filter_resolution.md) · [Finite-support obstruction](Finite_clock_purity.md) · [Terminal flight from this preparation](From_a_local_sheet_to_a_flight.md)

The independent physical-coordinate replay checks every split, address, sign, final rail and integer norm at 72 orders, each with two launch addresses and base sites. At $M=127$ it used 60 streamed ticks and gave unit-pair weight about 0.412211. At $M=128$ it used 77 ticks and gave 0.810732. These are model probabilities for a squared coordinate readout. The operation that supplies the address pattern and the assignment of its unit to a physical sheet are substantive inputs. [Checker](check_addressed_sheet_source.py) · [All finite profiles](results/addressed_sheet_source.json)

## What precision does a force calibration require?

On fresh copies of the accepted source, begin a matched field-on and field-off three-tick rail comparison from a sharp well and R rail. A known L rail can be reset to R by a directed permutation step. Its common sheet translation preserves the sector weights. For folded weights $b_d$, the scaled rail excess is $C_M=\sum_d b_d v_M(d)^2$, with $v_M(d)=(M/\pi)\sin(\pi d/M)$. The absolute contribution to any ordinary sheet-blind flight event from an unwanted posterior fraction $\eta$ is bounded by $\eta$. The scaled diagnostic magnifies that error. In general $|C_M-v_M(1)^2|\le M^2\eta/\pi^2$. Concentrating a fraction $M^{-2}$ at $d=M/2$ on even orders gives a limiting excess of $1/\pi^2$ above the unit value. Thus $\eta=o(M^{-2})$ suffices for arbitrary contamination and its order cannot be relaxed uniformly. [Three-tick calibration and its coefficient](Mixed_refinement_records.md)

The actual signed source permits a cheaper test. Write $f(y)=\sqrt L\,\psi(y)$ for the translated physical amplitudes. Finite Parseval gives its energy before probing as

$$
C_{\rm pre}=\frac{M^2}{4\pi^2 L}\sum_{y\bmod M}|f(y)-f(y-1)|^2
=\frac{M^2}{4\pi^2 L}
\begin{cases}8,&L=M,\\6,&L<M.\end{cases}
$$

The dyadic profile has two jumps of size two. A profile with an empty interval has one jump of size two and two of size one. In both cases $C_{\rm pre}=O(M)$. The constant mode has zero initial weight, so every nontarget sector with positive weight has $v_M(d)^2\ge v_M(1)^2$. If the selector passes each such sector with probability at most $\beta$ and passes the unit pair with probability at least $1-\beta$, then

$$
0\le C_{\rm accepted}-v_M(1)^2
\le \frac{\beta\,[C_{\rm pre}-W_M v_M(1)^2]}{W_M(1-\beta)}.
$$

For example, $\beta=M^{-1-\gamma}$ for any fixed $\gamma>0$ gives limiting calibrated squared charge one at $O(\sqrt M\log M)$ streamed cost before any sheet reset. The checker compares the three-tick excess computed from the physical one-address overlap with the cyclic difference formula. At order three the prepared source has exact unit-pair weight. A finite family of approximate preparations need not have exactly matching marginals under the cover maps. If the finer and coarser unwanted fractions are $\eta_M,\eta_m$ and $m\mid M$ with $m\ge3$, their folded marginals differ in total variation by at most $\eta_M+\eta_m$, by contraction under folding. Sending the test error to zero at each order gives the compatible folded-unit family. The rail calibration can therefore be realized by a controlled preparation under the squared-coordinate probability law. Deriving that law or fixing an absolute embedding from the apparatus remains a separate obligation. [Compatible folded laws](Refining_the_sheet.md) · [Probability under relabelling](Native_preparations_and_probability_embeddings.md)
