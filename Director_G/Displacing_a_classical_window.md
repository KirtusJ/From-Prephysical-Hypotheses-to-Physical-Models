# A displaced aperture prepares two rested classical arrivals and suppresses fair counting

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch at a sharp well on R. Keep the native signed Hadamard and the staircase field running. Read the position once at tick $t$, retaining all wells in one displaced interval as a single coherent outcome. On the shrinking-action scales below, that interval leaves the fair count walk's diffusive core while its physical displacement and incident physical velocity both tend to zero. In the physical unit-character sectors the accepted state reaches $Y_0\pm FT^2/2$ at release time $T$, with limiting probability $1/2$ at each location. The observation coordinates stay in the laboratory frame. The count rejection and the predicted motion refer to two hypotheses already allowed in the complete-record score classification. [Score and conditional record laws](Position_transcripts_and_selected_laws.md) · [Centered aperture and its count contamination](Single_window_in_a_permanent_field.md)

## The source and its fixed-clock read

On a ring of $4M$ sites let $X$ denote displacement from the sharp launch and $Y_0$ the limiting physical launch position. Fix $F>0$ and put $\delta=(\pi/(MF))^{1/4}$. The site pitch is $\delta^2$, the tick time is $\delta^3$, and the departure phase slope in sector $s=\pm1$ is $h=sF\delta^4$. Use the nearest integer $t$ to $\delta^{-9/4}$ and set

$$
v=\delta^{33/32},\qquad w=\delta^{17/16},\qquad
W=\{|X-tv|\le tw\}.
$$

The window includes equality at its endpoints and uses its real center $tv$ without rounding. A passing instrument preserves the two rails and the relative amplitudes of all passing sites. A terminal experiment consists of this membership bit and a later position read. All preparation clocks remain in the cost. For $n\delta^3\to T>0$ the full cone through $t+n$ fits on the ring since $t+n=o(M)$.

Write $U$ for the free tick, $\psi$ for the launch, and $V$ for the free band velocity operator. Set $Q=\mathbf1_{\{|V-v|\le w\}}$. The translated sharp-launch integration-by-parts estimate bounds

$$
\frac{\|\mathbf1_W U^t\psi-U^tQ\psi\|}{\sqrt w}
     \le C(tw^2)^{-1/4}.
$$

Its inner and outer velocity intervals sit a distance $\eta w$ from the corresponding position boundary in $X/t$. Their leakage norm is $O((t\eta w)^{-1/2})$, and the two intervening strips carry $O(\eta w)$ spectral probability. The constants are uniform here since $|v|+2w\to0$ lies away from the velocity edges. The sharp-R density gives $\|Q\psi\|^2=(2w/\pi)[1+v+O(v^2+w^2)]$. Here $tw^2\asymp\delta^{-1/8}\to\infty$. [Translated estimate and density](Flight_window_preparation.md)

On the occupied site parity the native staircase is a linear phase up to a scalar at each tick. The field-on full state differs in norm from $e^{-i(t-1)hX/2}U^t\psi$ by $O(t|h|+t^3h^2)=O(\delta^{5/4})=o(\sqrt w)$, up to a global phase. Since this site phase commutes with the aperture, the physical pass has probability $(2/\pi+o(1))w$. The normalized passing state is within $o(1)$ of $e^{-i(t-1)hX/2}U^tQ\psi/\|Q\psi\|$. Thus the preparation is the actual coherent position mask; the velocity projection is its analytical comparison. [Centered field-on estimate](Uninterrupted_sheet_read.md)

## Release in the laboratory

The four small momentum intervals in $Q$ occur on two bands near the carriers $k_*=\pm\pi/2$. Each has length $2w[1+o(1)]$, and the right incident rail has limiting squared eigenvector overlap $1/2$ there. Consequently each chart and band contributes $1/4+o(1)$ to the accepted law, with total $1/2+o(1)$ for each curvature $b=\pm1$. After the site rephasing all these components obey

$$
\left|\frac{k-k_*}{\delta}\right|
 \le C\,\frac{v+w+t|h|}{\delta}=o(1).
$$

The aperture itself lies within $\delta^2t(v+w)=O(\delta^{25/32})$ of the launch and takes physical time $t\delta^3=O(\delta^{3/4})$. For a branchwise transport argument taper the outer fraction $\rho$ of each spectral window, for fixed $0<\rho<1/2$. This changes the normalized state by $O(\sqrt{\rho})$. Differentiating the smooth cutoff, the free eigenvectors and the free flight phase bounds the norm of physical displacement on each normalized comparison branch by $C\delta^2[1+(\rho w)^{-1}+t(v+w)]\to0$. The momentum translation from the site phase leaves this position norm unchanged and shifts the smooth band projectors by $O(t|h|)$ in norm. These estimates avoid a position-moment assumption on the sharp Fourier cut.

The forced-envelope estimate applies uniformly to the bounded scaled momentum charts. Its Hamiltonian $bp^2/2+sFY$ gives the position observable $Y+bTp-bsFT^2/2$ after time $T$. The incident position and momentum deviations just bounded tend to zero in each tapered branch. For a bounded position characteristic, well-separated charts remain disjoint after its $O(\delta^2)$ shift in microscopic momentum; two bands on a common chart have vanishing cross overlap by smooth spectral orthogonality. Removing the taper after passage to the limit gives the conditional terminal law

$$
\tfrac12\,\delta_{Y_0-FT^2/2}+\tfrac12\,\delta_{Y_0+FT^2/2}.
$$

This proves convergence of a final position read for each fixed $T$. Timing, sheet sector, force and a coherent passing instrument enter as specified inputs. Each terminal tube around a single arrival can be queried as one binary event on fresh runs. [Forced band estimate and classical motion](Forced_envelope_and_classical_motion.md)

## Count rejection and incident weights

In the persistent count component each clock adds an independent fair sign. The pass entails $X_t\ge t(v-w)$. For $\lambda>0$, its moment-generating function is $(\cosh\lambda)^t\le e^{t\lambda^2/2}$. Taking $\lambda=v-w$ bounds the count passing rate by

$$
P_C(W)\le e^{-t(v-w)^2/2},\qquad
t(v-w)^2=\delta^{-3/16}(1-\delta^{1/32})^2[1+o(1)].
$$

For every fixed finite $a\ge0$ this gives $P_C(W)=o(w M^{-a})$. If the incident unit-character weight is $b_1\ge c M^{-a}$ for some $c>0$, and the count weight is $b_C\le1$, then $b_C P_C(W)=o(b_1w)$. For a mixture containing only these alternatives the original-launch pass rate is $b_1(2w/\pi)[1+o(1)]$ and the posterior count probability tends to zero. A persistently absent unit sector cannot be created by accepting an outcome. Other coherent sectors require their own control. For example, fixed $s=0$ and $s=2$ also pass at rate $(2/\pi+o(1))w$: in the first the subsequent pair coincides at $Y_0$, while in the second the two accelerated displacements are twice as large. Accrued selector failures and unit completeness must be included in an original-launch accounting.

For independent new sharp unit preparations, the mean serial cost of obtaining a pass is asymptotic to $\pi t\delta^3/(2w)$ in physical time, of order $\delta^{-5/16}$. A failed mask supplies no sharp reset on its own. At fixed action a translating aperture can also reject count, but then the native quantum wave must be followed in its moving frame. [Fixed-action protocol and its single-read laboratory obstruction](Moving_window_quantum_flight.md)

## Finite native trials

The checker propagates the two physical rails with the staircase at every departure and a single membership mask. It compares with the exact fair binomial count of every passing prefix, tests conjugate and nonunit settings, and uses an independent integer signed-history expansion at $M=127$. It records terminal characteristic functions at $\xi=0,1,3$ with the physical laboratory or moving origin prescribed by each protocol. The archive retains all 18 cases without an agreement threshold against either limiting law. [Checker](check_moving_window_flight.py) · [All finite trials](results/moving_window_flight.json)

At $M=524287$, $F=1$, $s=1$, the shrinking-action example gives a coherent pass probability of $0.027874$ and a count pass probability of $0.45402$. An equal incident mixture has posterior count probability $0.94216$. Its coherent laboratory characteristic at $\xi=1$ is $0.48299+0.51786i$, compared with the limiting-law prediction $0.96070$ using the actual rounded release time. At this order the lower edge is only $0.119$ count standard deviations above the launch. The finite observations do not yet demonstrate this asymptotic count rejection or rested classical flight.

In the fixed-action moving-frame example at the same order the coherent pass probability is $0.013692$ and count passes with probability $6.09\times10^{-11}$. With equal incident weights the count posterior is $4.45\times10^{-9}$. The coherent moving-frame characteristic at $\xi=1$ is $0.40966+0.01193i$, compared with the Fresnel prediction $0.40228$. These coordinate choices and rates belong to different preparations.
