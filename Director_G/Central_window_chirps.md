# The wave prepared by one central position aperture

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch at a known well on R. The signed Hadamard and the staircase field stay on throughout preparation and flight. At one clock retain the complete interval about the launch in a **single** binary position outcome. In a fixed-action scaling the two slow bands emerging from that aperture have constant modulus on the interval and opposite quadratic phases. Their subsequent position law can be compared with an explicit Fresnel prediction. In a shrinking-action scaling even a narrower velocity window can prepare two rested classical rays. Both preparations have polynomial incident yield. These statements use a fixed bounded physical sheet character, ordinary square probabilities in that sector, and a passing aperture that preserves coherence over its allowed wells. [Position-product scope](Position_transcripts_and_selected_laws.md) · [Sharp launching wells and the scale clock](Field_on_source_and_release.md)

## The two stationary contributions

Work relative to the launch at zero and use physical sheet label $s=\pm1$. Write $h=s\pi/M$ on the $4M$-site ring. On the occupied parity, each departure multiplies by $e^{-ihx}$ up to a time-dependent scalar. Use the negative spatial Fourier exponent and the free tick $U(k)=\operatorname{diag}(e^{-ik},e^{ik})H$. Its two eigenvalues are $e^{-i\omega(k)}$ and $-e^{i\omega(k)}$, where $\omega(k)=\arcsin(\sin k/\sqrt2)$. Let $P(k)$ be the projector for the first. Starting on a sharp well, the Fourier vector is constant $e_R$. In the regimes below the whole cone through preparation and final read fits in a lift of the ring. One may therefore pass to the line before making any continuum approximation.

Put $v=x/t$, $k_b(v)=-b\arccos(v/\sqrt{1-v^2})$, $b=\pm1$, and $k_b^*=-b\pi/2$. For $|v|\le w$ with $w\to0$ these are the two roots of $\omega'(k)=v$, and $\omega''(k_b(v))=b c(v)$ where $c(v)=(1-v^2)\sqrt{1-2v^2}$. In the product $U(k)U(k+h)\cdots U(k+(t-1)h)$ center the arguments at $k+(t-1)h/2$. The inverse Fourier change of variable gives the site phase $e^{-i(t-1)hx/2}$. Uniform transport of the separated eigenframes costs $O(t|h|)$ in norm. The centered Taylor sum of eigenphases includes the quadratic term $B\omega''$ with $B=h^2t(t^2-1)/24$, and the odd centered moments vanish. The remaining operator error is $O(t^5h^4)$. This comparison uses a common phase for the launch and sheet parity. [Centered product estimate](Uninterrupted_sheet_read.md) · [Curvature correction and stationary pair](Uninterrupted_sheet_fringes.md)

For bounded $B$ the inverse transform of the approximating spinor has, on $x\equiv t\bmod2$, one leading contribution for each $b$:

$$
 e^{-i(t-1)hx/2}\frac{2P(k_b(v))e_R}{\sqrt{2\pi t\,c(v)}}\,
 \exp\{i[xk_b(v)-t\omega(k_b(v))-b\pi/4-bBc(v)]\}.
 \tag{1}
$$

Indeed $U(k+\pi)=-U(k)$ and $P(k+\pi)=I-P(k)$. Shifting the second-band inverse transform by $\pi$ gives a second identical first-band integral on the occupied parity and cancellation on the other. The factor two in (1) accounts for that replica; it does not create another independent band. The sign of the stationary-phase Hessian is $-b$. All amplitudes in the approximating integral have uniformly bounded derivatives near these two separated, nondegenerate saddles. The per-site stationary-phase remainder there is $O(t^{-3/2})$ for $v$ in a fixed neighborhood of zero. The field's norm approximation is a separate estimate on the entire state, subsequently projected by contraction. [Free Hadamard stationary asymptotics, Sunada and Tate](https://arxiv.org/abs/1108.1878)

The two endpoint spinors approach the orthogonal circular vectors $P(k_b^*)e_R$. Each limiting vector has norm $1/\sqrt2$. The exact norm squared at either saddle is $(1+v)/2$, and their mutual inner product is $O(w)$. Thus rapidly oscillating saddle phases need not be assumed to cancel. For $L=\lfloor tw\rfloor\to\infty$, restriction of the approximating state to $|x|\le L$ has probability $2w/\pi\,[1+O(w+1/L+1/t)]$. Each branch separately contributes $w/\pi\,[1+O(w+1/L+1/t)]$. There are $L+O(1)$ occupied wells in this interval. All of these are incident probabilities for a sharp launch in the specified sector. To use the estimates for the actual field we require the total norm error across the aperture to be $o(\sqrt w)$.

## Fixed action gives a pair of waves on a finite spatial interval

Fix $A,\kappa,F>0$. Choose $\delta=(\pi/(MF))^{1/3}$, $h=sF\delta^3$, site pitch $\delta$, tick time $\delta^2$, $t\delta^2\to\kappa$ and $L\delta\to A$. The half velocity width is $w=L/t\sim A\delta/\kappa$. Now $B\to F^2\kappa^3/24$. The centered-product norm error is $O(\delta+\delta^2)=o(\sqrt\delta)$. The stationary-phase remainder on the projected window is $O(\sqrt L\,t^{-3/2})=o(\sqrt\delta)$. It is essential to retain $B$: the free-state norm comparison that discards the curvature phase need not be small on this scale.

For $Y=\delta x\in[-A+o(1),A+o(1)]$, the stationary action $S_b(v)=v k_b(v)-\omega(k_b(v))$ has derivative $k_b(v)$, $S_b(0)=b\pi/4$, and $k_b'(0)=b$. Uniformly on the window,

$$
 t S_b(v)=b\pi t/4+k_b^* x+bY^2/(2\kappa)+o(1),\qquad
 (t-1)hx/2=sF\kappa Y/2+o(1).
$$

Writing $u_b=\sqrt2P(k_b^*)e_R$, the normalized accepted waveform on the parity grid is consequently $o(1)$ in norm from

$$
 \sqrt{2\delta}\sum_{b=\pm1}
   \frac{C_b(t)}{\sqrt2}\,e^{ik_b^*x}u_b\, f_b(Y),\qquad
 f_b(Y)=\frac{\mathbf1_{[-A,A]}(Y)}{\sqrt{2A}}\,
   e^{\,ibY^2/(2\kappa)-isF\kappa Y/2},\qquad
 C_b(t)=e^{\,ib\pi(t-1)/4-ibF^2\kappa^3/24}.
 \tag{2}
$$

The displayed formula may use a common global phase. The physical position is relative to the launch. The grid cell has length $2\delta$ on the occupied parity. End-cell and ceiling effects vanish in squared norm even though $f_b$ has jumps. If both carriers are referred to $k_+^*=-\pi/2$, the other gains $(-1)^t$ on these wells. Accordingly their relative phase in a common carrier includes this parity factor and the relative $C_b(t)$; it is not a free setting of the apparatus. Each component has mass $1/2$ after acceptance. The original launch pass probability is $2A\delta/(\pi\kappa)+o(\delta)$, with $2A$ the width of the full physical window.

Start the flight clock at this read. In each curvature branch the continuum Hamiltonian is $H_b=bp^2/2+sFY$, $p=-i\partial_Y$. The native position law after a further $n$ ticks with $n\delta^2\to T>0$ converges weakly to the equal mixture of position laws of $e^{-iTH_b}f_b$. To justify the band transfer for discontinuous $f_b$, approximate each by a Schwartz function with smooth compactly supported Fourier transform in $L^2(\mathbb R)$. On the parity grid the squared-norm error of the sampled approximation converges to its continuum value by Riemann summation, including the tail of the Schwartz function. For that approximant the unfolded lattice has two separated low-momentum replicas and the smoothly varying eigenspinors agree at each carrier with the fixed circular spinor up to $O(\delta)$ on its bounded momentum support. At the shifted replica $U(k+\pi)=-U(k)$ exchanges the branch labels and preserves the curvature. The forced-envelope norm estimate applies on each compact chart. Distinct replicas have disjoint supports after the small momentum shift representing a bounded position characteristic; the opposite curvatures have orthogonal limiting spinors where the charts coincide. Let the initial approximation error tend to zero after the limit, using unitarity for the exact and continuum evolutions. This argument needs no finite position or momentum variance of the released top-hat wave. [Finite-action forced spinor norm estimate](Forced_envelope_and_classical_motion.md)

The complete characteristic function is explicit. Write $\operatorname{sinc}u=\sin(u)/u$ with value one at zero, and $L_T(\xi)=\max(2A-|T\xi|,0)$. The position Heisenberg operator at time $T$ is $Y+bTp-bsFT^2/2$. Its Weyl exponential translates the initial packet by $d=bT\xi$ and contributes the midpoint phase $e^{i\xi(Y+d/2)}$. On the overlap of the shifted intervals the phase in $\overline f_b(Y)f_b(Y+d)$ is $bd(Y+d/2)/\kappa-sF\kappa d/2$. The midpoint coordinate ranges over a symmetric interval of length $L_T(\xi)$. Averaging the two curvatures gives

$$
 \lim \mathbb E[e^{i\xi(Y_{\rm final}-Y_0)}\mid\text{pass},s]
 =\frac{L_T(\xi)}{2A}
    \operatorname{sinc}\!\left(\frac{\xi(1+T/\kappa)L_T(\xi)}2\right)
    \cos\!\left(\frac{sF\xi(\kappa T+T^2)}2\right).
 \tag{3}
$$

At $\xi=0$ this is one. At $|T\xi|\ge2A$ it vanishes. For $T>0$ this provides a bounded position readout of the coherently retained interval. A contrasting apparatus that also records every successful well and later pools the labels makes a mixture of sharp-site sources. At a fixed later $T>0$ the latter has vanishing probability in any fixed bounded physical position interval. To see this, translate each of its starting sites in the aperture to zero and allow any unit rail spinor there. For the further $n$ ticks use the same centered chirped approximation with norm error $O(n|h|+n^5h^4)=O(\delta)$ and bounded $B$. All wells in the target interval have relative $x/n=O(\delta)$ uniformly over these starts. The stationary amplitudes of the approximating propagator have norm $O(n^{-1/2})$ there, so its total probability over $O(\delta^{-1})$ wells is $O(\delta)$. The uniform norm error changes this probability by $o(1)$. This distinction concerns the field at both preparation and flight, with an ideal read of the stated type.

## A narrower regime prepares rested classical rays

Set $\delta=(\pi/(MF))^{1/4}$, $h=sF\delta^4$, physical position $Y=\delta^2 x$ and tick time $\delta^3$. For a unit-conditioned aperture it suffices that

$$
 w/\delta\to0,\qquad L=tw+O(1),\qquad
 \delta L\to\infty,\qquad \delta^2 L\to0,\qquad
 t|h|+t^3h^2=o(\sqrt w),\qquad t|h|/\delta\to0.
$$

Keep the unwrapped cone through flight and count all preparation ticks. When preparation time is asserted negligible, one also needs $t\delta^3\to0$. The conditions permit $tw^2\to0$. For example take $w=\delta^{5/4}$, $t$ an integer nearest $\delta^{-19/8}$ and $L=\lfloor tw\rfloor$. Then $tw^2\asymp\delta^{1/8}$, $\delta L\asymp\delta^{-1/8}$ and $t^3h^2=O(\delta^{7/8})=o(\sqrt w)$. Another choice is $w=\delta/\ell$, $t$ nearest $\ell^2/\delta^2$, $\ell=\log(1/\delta)$, for which $tw^2\to1$.

In this regime replace the field before the aperture by the spatially rephased free state with total norm error $O(t|h|+t^3h^2)=o(\sqrt w)$. The free stationary components (1) have $B=0$. To localize the momentum of their **sharp** restrictions, first taper each outer edge of the position box over $\beta L$ wells, with $\beta\to0$ and $\beta\delta L\to\infty$. A linear taper suffices. Its difference from the hard box has norm $O(\sqrt{\beta+1/L})$ relative to a selected component, by the uniform stationary amplitude bound. After removing $e^{ik_b^*x}$ the bulk phase increments on the parity lattice have size $O(w+1/t)$, because the derivative of the stationary action with respect to $x$ is $k_b(x/t)$. The smooth amplitudes vary by $O(t^{-1})$ relative to their scale; tapered edges add at most $O(1/(\beta L))$ to the normalized two-site finite-difference norm. The common field gauge contributes $O(t|h|)$ more. All these terms are $o(\delta)$.

The Fourier multiplier of this difference has modulus $2|\sin(k-k_b^*)|$ on *both* parity replicas. Consequently the normalized tapered component has vanishing mass outside every fixed multiple of $\delta$ from these carriers, and its scaled momentum tends to zero in probability. The slow-spinor identification can be made branch by branch. Replace $P(k_b(v))e_R$ by $P(k_b^*)e_R$ in (1) at a relative cost $O(w)$ before taking momentum estimates. Use the band for this spinor at one carrier and its complementary band at the other, both of physical curvature $b$. This gives both curvature masses $1/2+o(1)$ without a phase averaging assumption or a rail read at the aperture. In particular the result establishes what is needed about this window's state, without requiring it to be norm close to the free evolution of a sharp *velocity* projection.

For transport, apply smooth momentum cutoffs of scale $\delta$ separately at the two replicas after this normalized-state approximation. Their discarded mass tends to zero. The momentum is bounded in the cutoff variable $p=(k-k_b^*)/\delta$ and concentrates at zero, hence has vanishing second moment there. Each tapered component lies initially in $|Y|\le\delta^2 L$. Commuting its smooth chart cutoff and band projector through $\delta^2 i\partial_k$ costs $O(\delta)$; projection into a smooth band frame has the same bounded derivative control. Thus the final cutoff envelope starts with vanishing position and momentum deviations. With action parameter $\varepsilon=\delta$, the forced-envelope norm bound applies uniformly on bounded flight times. In a curvature branch the position deviation at time $T$ about $-bsFT^2/2$ is bounded by the initial position deviation plus $T$ times the initial momentum deviation, up to the vanishing comparison error for bounded observations. Taking the two curvature contributions gives the weak position limit

$$
  \tfrac12\delta_{\,Y_0-FT^2/2}+\tfrac12\delta_{\,Y_0+FT^2/2}.
$$

The original success rate is $2w/\pi+o(w)$. On an already supplied fixed physical weak sector, independent sharp restarts costing $t$ ticks each take mean time asymptotic to $\pi t\delta^3/(2w)$. This equals $\tfrac\pi2(\delta L)(\delta/w)^2[1+o(1)]$, which diverges under these sufficient conditions. In the logarithmic example it grows as $\tfrac\pi2\ell^3$. A small physical duration of the successful trial and polynomial original-launch yield do not make serial preparation time vanish. If a preceding sheet selector leaves unwanted weight $\eta$ and its success probabilities on those sectors are unknown, the unwanted conditional fraction after this new aperture is bounded by $\eta/[(1-\eta)(2w/\pi+o(w))+\eta]$. Thus $\eta=o(w)$ suffices to retain the claimed limits even for an unspecified contaminant. This calculation uses the unit-sector rate of the subsequent aperture and makes no closure claim for arbitrary physical embeddings. [Complementary velocity-projector window estimate](Single_window_in_a_permanent_field.md)

For fair history counting, the pass probability is the exact binomial sum $2^{-t}\sum_{|2j-t|\le L}\binom tj$. With $u=L/\sqrt t$, it tends to $\operatorname{erf}(u_0/\sqrt2)$ when $u\to u_0>0$, and to one when $u\to\infty$. At fixed action $u_0=A/\sqrt\kappa$; the logarithmic example gives $u_0=1$. If $u\to0$ and $L\to\infty$, the central binomial estimate on the occupied parity gives pass probability $\sim\sqrt{2/\pi}\,u$. The ratio to the coherent pass then grows as $\sqrt{\pi t/2}$, so a count-only contaminant must have incident weight $o(t^{-1/2})$ for its accepted fraction to vanish. In the fixed-action $M=32768$ model with $A=F=\kappa=1$ (rounded clocks), the coherent and counting pass probabilities were $0.02936$ and $0.68622$. At the later time nearest $T=0.75$, the conditional probabilities in $|Y-Y_0|\le2$ were $0.80619$ for the coherent aperture, $0.07923$ after registering each passing well, and $0.95242$ for fair counting. The checker propagates each complex sharp-rail column once per return law, checks pooling against a separate propagation from every retained well at small order, and counts the entire classical joint event in integers. [Finite checker](check_central_window_flight.py) · [All 36 model trials](results/central_window_flight.json)
