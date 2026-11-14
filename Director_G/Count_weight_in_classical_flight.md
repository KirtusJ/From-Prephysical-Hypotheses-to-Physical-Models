# Does observing a freely moving ray exclude path counting?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

A moving position aperture can suppress counting in its successful output even if counting contributes most of the input weight. A central aperture has the opposite effect. Counting all launches distinguishes a change in the preparation yield from a change in the trajectory of the selected walkers.

Use the signed line walk from one positive right-moving launch. Let $\alpha$ be its fixed count fraction, with the remaining weight on the squared signed count. On an uninterrupted product of position masks its unconditioned probability is $\alpha P_C+(1-\alpha)P_Q$. No choice of a trajectory coupling at unmeasured intermediate times is necessary. For release, a successful aperture must preserve coherence between all its accepted sites and rails. The following application uses the previously derived shrinking-aperture estimate and free ray on this instrument. The ballistic limit of a homogeneous quantum walk has been studied independently for fixed velocity sets. A shrinking aperture requires an estimate relative to its vanishing success probability. [Position-mask classification](Position_mask_preparation.md) · [Shrinking aperture and free ray](Flight_window_preparation.md) · [Konno](https://arxiv.org/abs/quant-ph/0206103) · [Suzuki](https://arxiv.org/abs/1507.08562)

## Two preparations on the same sharp source

At tick $T$ retain the binary outcome $E_{p_0}$ that $|X_T/T-\delta p_0|\le w$, with displacement measured from the launch. Choose $\delta=T^{-5/14}$ and $w=\delta^{11/10}$. As $T\to\infty$ the square success rate at either fixed $p_0$ is $Q_T\sim2w/\pi$. It comes from the two-band velocity density at velocity zero with $Tw^{5/2}\to\infty$. The counting walk appends left and right with equal weight at each tick, so its $X_T$ is the sum of $T$ fair signs. Write $C_T=P_C(E_{p_0})$. For $p_0\ne0$ and $|\delta p_0|>w$,

$$C_T\le\exp[-T(|\delta p_0|-w)^2/2].$$

For $p_0=0$, $1-C_T\le2\exp[-Tw^2/2]$. Both bounds follow by exponential Markov inequality from $\mathbb E e^{sX_T}=(\cosh s)^T\le e^{Ts^2/2}$ and minimization over $s$. Here $T\delta^2=T^{2/7}$ and $Tw^2=T^{3/14}$. Hence the moving-window bound is $o(w)$, whereas the count probability of the central window approaches one.

| Per-launch quantity | Fixed $p_0\ne0$ | $p_0=0$ |
|---|---:|---:|
| Total acceptance $P(E_{p_0})$ | $(1-\alpha)(2w/\pi)+o(w)$ | $\alpha+o(1)$ |
| Counting fraction among successes, $0<\alpha<1$ | tends to 0 | tends to 1 |

At any finite $T$, the counting fraction among successes is $\alpha C_T/[\alpha C_T+(1-\alpha)Q_T]$, provided the denominator is positive. A source fraction changing with the scale must be inserted in this expression before taking a limit.

## What the released position measures

Choose a site pitch $\delta^2$, a clock interval $\delta^3$, and a launch nearest a fixed $Y_0$. At release the measured position is within $\delta^2T(|\delta p_0|+w)$ of its launch, a distance tending to zero. For the squared term the earlier theorem gives conditional terminal concentration about $Y_0+p_0t$ at subsequent times $n\delta^3\to t$. Fix $p_0\ne0$, $t>0$ and any positive tube radius about that point. With $B$ the event of terminal arrival in the tube, the original sharp launches satisfy

$$\frac{P(E_{p_0}\ \mathrm{and}\ B)}{2w/\pi}\longrightarrow 1-\alpha.$$

The counted joint contribution is at most $C_T=o(w)$ independently of the subsequent motion. For any fixed $\alpha<1$ the moving ray survives when conditioning on acceptance. Under pure counting, conditioned solely on the preparation, later count increments remain independent fair signs. Their physical variance $n\delta^4\to0$ at fixed $t$ and their conditional release position tends to $Y_0$. The count-only flight thus stays at $Y_0$ in this scaling. At $p_0=0$ both pure conditional flights concentrate there, although their preparation yields differ. The limits concern a free terminal position in separate runs. A force law and a joint law of unmeasured trajectories require further premises.

## Finite depths

At $T=1024$ the count probabilities of the apertures for $p_0=0,1,2$ are approximately $0.96377,0.27635,0.00051196$. With equal incident weights the counting fractions among accepted launches are $0.95844,0.85621,0.00988$, respectively. The $p_0=1$ aperture favors counting at all six tested depths from 32 to 1024. At $p_0=2$ the squared success probability at 1024 is about $0.05129$. Replacing an asymptotic yield by a moderate-depth number could reverse the inferred mechanism. All 18 finite results include the exact numerator, common denominator and lattice endpoints. The binomial tally and the signed recurrence are tested separately. [Checker](check_count_flight_windows.py) · [Exact finite apertures](results/count_flight_windows.json)
