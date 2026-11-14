# How much preparation time does one rested position aperture require?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

One displaced position aperture can suppress fair counting, preserve two classical arrivals in the laboratory frame, and take mean serial preparation time $O(\log M\,(\log\log M)^4)$ on supplied unit-character launches. There is a lower bound for the same kind of source: every single position read whose accepted sites satisfy $|x|/t=o(\delta)$ and whose count-to-square pass ratio tends to zero costs $\omega(\log M)$ on supplied square launches. Here $x$ is displacement from the sharp source at tick $t$, and cost is physical time to the first pass on independent sharp restarts. The lower bound allows arbitrary subsets of this velocity interval. It does not require an assumed square success rate or measured outgoing momentum. [Walk, coherent mask and forced flight](Displacing_a_classical_window.md)

Use a $4M$-well ring, sharp launch on R, fixed $F>0$, site pitch $\delta^2$ and tick time $\delta^3$, with $\delta=(\pi/(MF))^{1/4}$. At a physical character $s$ the native staircase acts, on the occupied site parity, by a departure phase of slope $h=sF\delta^4$ up to a clock scalar. For the source construction $s=\pm1$. All clocks before and after the one pass/fail position read use the native walk. The passing branch preserves the relative amplitudes of accepted wells and both rails. Let $Q$ and $C$ denote the per-launch square-character and persistent fair-count probabilities of that same pass.

## The schedule

Write $H=\log M$. Choose $g=g(M)\to\infty$ slowly with $\log g=o(H)$, for example $g=\log H$ for large $M$. Put

$$
w=\delta/g,\qquad v=2w,\qquad
t=\operatorname{round}(DH/w^2),\qquad W=\{x:tw\le x\le3tw\}.
$$

For a known incident unit-weight bound $b_1\ge cM^{-a}$, take a constant $D>2a+1/2$. When the same schedule must work for every fixed $a$, take $D=g$. A walker must move at least $tw$ to pass. The binomial exponential bound gives $C\le\exp[-tw^2/2]=\exp[-DH/2+O(w^2)]$. In both cases $C=o(b_1w)$, since $\delta$ is a fixed multiple of $M^{-1/4}$. In this comparison the exponent \(1/4\) comes from the original-launch square yield.

For the square law $tw^2\sim DH\to\infty$. The translated velocity-window estimate gives $Q_{\rm free}\sim2w/\pi$ and a relative state error $O((DH)^{-1/4})$ against the freely evolved velocity projection. Before applying the position read, the actual field-on state differs from the spatially rephased free state in norm by $O(t|h|+t^3h^2)$. Relative to the passing norm this is $O(\delta^{3/2}(DH)^3g^{13/2})=o(1)$. The phase commutes with the aperture. The normalized field-on branch thus has the same velocity-projection comparison after rephasing and $Q\sim2\delta/(\pi g)$. [Translated sharp-launch bound](Flight_window_preparation.md) · [Field-on comparison](Single_window_in_a_permanent_field.md)

The successful preparation takes physical time $t\delta^3\sim\delta DHg^2\to0$. Its whole window lies within $3\delta^2tw=O(\delta DHg)$ of the launch. In each comparison band the scaled momentum about its slow carrier has magnitude $O(1/g+t|h|/\delta)=o(1)$. For fixed taper fraction $\rho>0$, the smoothed velocity window's physical position norm is $O(\delta^2[1+(\rho w)^{-1}+3tw])=o(1)$; removing this taper costs $O(\sqrt\rho)$ in state norm. The two curvatures each have weight $1/2+o(1)$ from a sharp R launch. The forced band estimate therefore gives the same conditional terminal law at each fixed elapsed release time $T>0$,

$$
\tfrac12\delta_{Y_0-FT^2/2}+\tfrac12\delta_{Y_0+FT^2/2}.
$$

All compared clocks fit on the lifted line because $t+O(\delta^{-3})=o(M)$. The limit concerns a position read at one later clock; different $T$ may use different original launches. [Taper and two-ray proof](Displacing_a_classical_window.md) · [Forced band transport](Forced_envelope_and_classical_motion.md)

For independent sharp unit launches the mean aperture preparation time is

$$
\frac{t\delta^3}{Q}\sim \frac{\pi}{2}DHg^3.
$$

Thus $g=\log H$ gives a cubic power of $\log\log M$ for known $a$ and a fourth power for the universal schedule. Choosing a slower divergent $g$ makes the factor over $\log M$ diverge as slowly as desired. For a fresh unit/count mixture on each original attempt, with unit weight $b_1$ and the remaining mass on count, the mean time to any pass is instead $t\delta^3/[b_1Q+(1-b_1)C]\sim \pi DHg^3/(2b_1)$. The posterior count fraction tends to zero. Repeated draws of the same persistent unknown label need separate accounting. Missing or other coherent sectors require their own calibration. A localized sheet carrying unit mass $2/M$ also has other character components; selecting and resupplying that pair has a separate cost. The physical mean above assumes fresh sharp preparations and ideal pass registration. A constant independent pass efficiency multiplies the mean cost by its reciprocal. A failed window alone does not reset the source.

## A lower bound for any single read inside the rested velocity interval

Consider any nonempty subset $S$ of the occupied parity after $t$ ticks on which $|x|/t\le m$ with $m/\delta\to0$. Use the same set for both records and fix any bounded physical character $s$. Suppose $C/Q\to0$; this is necessary for a vanishing count posterior at fixed positive count and square odds. We prove $t\delta^3/(QH)\to\infty$. If there were a subsequence with $t\delta^3/Q\le KH$, then $t\le KH\delta^{-3}=o(M)$ and $t|h|=O(\delta H)\to0$. Each sharp launch can therefore be treated on the line. Bounded $t$ would give $C\ge2^{-t}$ for every nonempty reachable set, contrary to $C/Q\to0$. Hence $t\to\infty$ on this subsequence.

For this lower bound the centered quadratic approximation need not remain accurate. Retain both *exact* eigenphase sums in the Fourier product $U(k)U(k+h)\cdots U(k+(t-1)h)$. The free projectors $P_b$ are smooth, periodic and gapped. On a real momentum lift carry their frame by a unitary with bounded derivative. Replacing each intervening overlap of adjacent frames by the identity and the final frame by its initial value costs $O(t|h|)$ in operator norm by telescoping unitary factors. On a constant sharp-launch Fourier spinor the resulting inverse transform has two integrals with smooth amplitudes $P_b(k)e_R$, phase $t[(x/t)k\mp\bar\omega(k)]$, and possible scalar signs, where

$$
\bar\omega(k)=t^{-1}\sum_{j=0}^{t-1}\omega(k+jh),\qquad
\omega(k)=\arcsin(\sin k/\sqrt2).
$$

Up to third derivative $\bar\omega$ differs uniformly from $\omega$ by $O(t|h|)$. On fixed neighborhoods of the two zeros of $\omega'$ the absolute second derivative of each phase divided by $t$ stays bounded below. On the complementary arcs the first derivative stays away from zero uniformly for $|x|/t\le m$. The second-derivative oscillatory integral bound on the first arcs and one integration by parts on the rest give an amplitude $O(t^{-1/2})$ per site. The second-derivative bound also follows by cutting where the first derivative has magnitude $\le t^{-1/2}$: monotonicity gives that region length $O(t^{-1/2})$ and one integration by parts gives the same order on the remainder. This argument leaves the global norm error outside the site sum. For $J$ admitted occupied sites,

$$
 Q\le K_1 J/t + K_2(t|h|)^2,\qquad
 \frac{(t|h|)^2}{Q}\le K_3 H t\delta^5=O(\delta^2 H^2)=o(1).
$$

It follows that $Q\le 2K_1J/t$ on the putative cheap subsequence. The constants are uniform in the mask. [Frame-transport proof and sign conventions](Uninterrupted_sheet_read.md)

For counting, set $u=x/t$ and $I(u)=[(1+u)\log(1+u)+(1-u)\log(1-u)]/2$. Uniform Stirling bounds on the two binomial factorials give $\Pr_C(x)\ge c\,t^{-1/2}e^{-tI(u)}$ when $|u|\le1/2$ and $x$ lies on the clock parity. On this interval $I(u)\le u^2$ by $I(0)=I'(0)=0$ and $I''(u)=(1-u^2)^{-1}$. Summing these positive contributions over exactly the same $J$ sites gives

$$
\frac{C}{Q}\ge c'\sqrt t\,e^{-t m^2}.
$$

Hence $tm^2-\tfrac12\log t\to+\infty$. Since $m/\delta\to0$, this forces $t\delta^2/\log t\to\infty$. In particular $t\ge\delta^{-2}$ eventually, so $\log t\ge\tfrac12 H+O(1)$ and $t\delta^2/H\to\infty$. The parity mesh gives $J\le tm+1$, implying $Q=O(m+1/t)=o(\delta)$. Now $(t\delta^2/H)(\delta/Q)\to\infty$, contrary to the assumed cost. [Robbins's explicit Stirling bounds](https://doi.org/10.2307/2308012)

Any individual aperture in this class costs asymptotically more than $\log M$ to reject counting, while the schedules above approach that lower growth rate up to an arbitrarily slowly divergent factor. This argument uses the sharp launch, unchanged homogeneous coin and field, and one diagonal position read at a single clock. A detector that follows a divergent physical velocity or uses intermediate coherent routing has different admissible observations. [Fixed-action moving detector](Moving_window_quantum_flight.md)

## Finite records

The checker propagates both rails at every tick at $M=127,2048,8191,32768$, with $F=1$, $g=\log\log M$, $D=1$ or $g$. It sums the exact binomial integers on the same parity sites and compares them with both analytic probability bounds. The order-2048 records also include the conjugate and zero-field controls. Larger entries in the archive evaluate expressions for scale and error only. [Native walk and exact count checker](check_rested_window_cost.py) · [All 12 trials and parameter estimates](results/rested_window_cost.json)

At $M=32768$ the universal schedule takes $13{,}632$ native ticks. Its actual square pass rate was $0.036042$ and the count pass rate was $3.85\times10^{-7}$. Equal incident weights give posterior count probability $1.07\times10^{-5}$. At the terminal field read the laboratory characteristic at wave number one was $0.01214-0.04998i$, while the rested-ray prediction at the rounded clock was $0.96073$. The computed unit-source mean preparation cost was $366.46$ in physical time. This order separates the passing rates while leaving a large discrepancy in the laboratory position law.
