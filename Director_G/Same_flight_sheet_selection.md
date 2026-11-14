# Selecting the unit winding at the end of the same flight

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

A walker starts at site zero on a sharp right rail and a sharp sheet address. Every departure in the signed Hadamard walk on a ring of $4M$ sites adds $\lfloor x/2\rfloor$ to a cyclic sheet of order $M$. Assume the squared-coordinate record law. Read the rail after each pair of ticks, coherently over the base sites and the sheet. Keep a word of $m$ consecutive rail changes, with $m$ even. On its success run the same walk for a further $n$ ticks and read one position bit. On failure report the first failing block. Neither the field nor the coin changes. The final bit and successful preparation word together select the ordinary pair of characters from the complete incident sheet. The position read is part of the selection: the state at release still contains other windings. [Projected two-tick source](Field_on_source_and_release.md) · [Sharp-record selector before release](Native_multiscale_selector.md)

## One pass from a localized sheet

Fix $F,\lambda,T>0$. Put $\delta=(\pi/(MF))^{1/4}$, site pitch $\delta^2$, tick duration $\delta^3$, $m\sim\lambda M^{2/3}$ and $T_n=n\delta^3\to T$. Let $Y=\delta^2x$ on the lift through the launch. Take $d=FT^2/2$ and choose a fixed $0<R<d/2$. The terminal bit accepts the union of the closed intervals of radius $R$ about $\pm d$. Replacing $d,R$ by values converging to them gives the same limits. The entire light cone is unwrapped since $2m+n=o(M)$. For $E$ denoting both the changing-rail word and the terminal bit, the results are

$$
\Pr(E)\sim\Pr(E,\ s=\pm1)
\sim\frac{2}{M\sqrt{\pi m}}\exp(-\pi^2\lambda^3/3),
\qquad \Pr(s=\pm1\mid E)\to1 .
$$

Here the sector joint law can be defined by a commuting terminal Fourier read of the sheet. The proposed apparatus needs only the base records. A sharp sheet address has squared Fourier weight $1/M$ at every label. A classical mixture of Fourier labels with the same weights gives exactly the same base law. Selection does not orient the two conjugates. The preparation consumes $2m$ ticks, or $O(M^{-1/12})$ physical time, on a successful word; the flight consumes $T+o(1)$ physical time. True successes are at most $2/M$ per original localized launch under any sheet-translation-invariant instrument.

## Which windings survive the rail word?

Use $h=\pi s/M$, where $s$ ranges over a centered set of representatives modulo $M$. On the occupied base parity the Fourier component of the native staircase kick is $e^{-ihx}$ up to a clock-dependent scalar. With $U(q)=\mathrm{diag}(e^{-iq},e^{iq})H$ and $H$ the signed Hadamard, the Fourier tick at **output** $q$ acts on the input at $q+h$. At even $m$ the retained scalar at the output of the last block is, up to a constant of modulus one,

$$
 f_{m,h}(q)=\prod_{a=1}^m\sin\big(q+(2a-1)h\big),\qquad
 P_m(h)=\int_{-\pi}^{\pi}|f_{m,h}(q)|^2\frac{dq}{2\pi}.
$$

The product follows by taking the opposite-rail matrix entry of each two-tick propagator. Even $m$ returns to the incident rail and cancels its momentum-dependent linear phase. The norm integral equals the finite ring average since the Fourier polynomial for the norm has degree $2m<4M$. At zero field $p_m=P_m(0)=\binom{2m}{m}/4^m\sim1/\sqrt{\pi m}$. Hölder gives $P_m(h)\le p_m$. Changing $h$ by $\pi/2$ shifts the product by $\pi/2$ in $q$ up to a constant sign. Thus every prefix survival probability, on either rail, has the same half-order ambiguity whenever the sheet has even order. On odd orders the nearby labels have half-integer offsets instead. [Exact block amplitude and scalar phases](Field_reversal_during_preparation.md)

For all charges a uniform estimate holds. Write $x_h=\mathrm{dist}(2h,\pi\mathbb Z)\in[0,\pi/2]$, $r=\mathrm{dist}(s,(M/2)\mathbb Z)$, so $x_h=2\pi r/M$. From $1-u\le e^{-u}$ and the finite cosine sum,

$$
 P_m(h)\le e^{-m/2} I_0(D/2),\qquad
 D=\left|\sum_{j=0}^{m-1}e^{4ijh}\right|
   =\left|\frac{\sin(m x_h)}{\sin x_h}\right|.
$$

Use $D=m$ at $x_h=0$. The modified Bessel function here is simply the circular average of $e^{u\cos v}$; bounding $1-\cos v$ below by a constant times $v^2$ on $[-\pi,\pi]$ gives $I_0(u)\le C e^u/\sqrt{1+u}$. If $m x_h\ge\pi$, then $D\le\pi/(2x_h)\le m/2$. If $m x_h\le\pi$, expand

$$
 1-(D/m)^2=\frac2{m^2}\sum_{j=1}^{m-1}(m-j)(1-\cos(2j x_h)).
$$

Restricting to $m/8\le j\le m/4$ bounds this below by $c m^2 x_h^2$ for large $m$. Therefore $m-D\ge c m\min(1,m^2x_h^2)$. For $D\ge m/2$ the Bessel prefactor is $O(m^{-1/2})$. For $D<m/2$ an exponential in $m$ absorbs the missing square root. Consequently, with positive constants depending at most on the fixed $\lambda$,

$$
 P_m(h)/p_m\le C\exp[-c\min(m,r^2)] .
$$

For fixed distance cut $K$ the omitted intermediate offsets contribute at most a constant times $\sum_{j>2K-1}\exp(-c j^2/4)$ to the sum of these ratios. Offsets with $r^2>m$ contribute at most $CM e^{-cm}$. Both integer and half-integer distances occur with bounded multiplicity. This controls the aggregate of the many sectors for which no weak-field propagation approximation applies.

## Bounded offsets at the weak and strong fields

First keep $s$ fixed while $M$ grows. There are two replicas of the source centered near $q_*=\pm\pi/2$. Set $z=\sqrt{m}(q-q_*+mh)$ and $d_a=(2a-1-m)h$. The cosine factors have offsets $z/\sqrt m+d_a$ with $\sum d_a=0$ and $\sum d_a^2=h^2m(m^2-1)/3$. On compact $z$ their log modulus tends to $-z^2/2-\pi^2\lambda^3s^2/6$ by Taylor expansion. The signs are constant near each center. For $|q-q_*+mh|\le\pi/4$ the bound $\log\cos v\le-v^2/2$ applies for large $M$; outside these intervals all moduli are uniformly bounded below one by a fixed margin. Thus the normalized shapes converge in the scaled $L^2$ coordinates to a Gaussian at each replica, and

$$
 P_m(h)/p_m\longrightarrow e^{-\pi^2\lambda^3s^2/3}.
$$

This is also the half-order result with $s$ replaced by the fixed offset from $\pm M/2$ and with carriers at $q=0,\pi$, by the exact momentum shift above. In particular, on the entire original uniform sheet the successful preparation word alone has limiting unit fraction $e^{-\pi^2\lambda^3/3}/\sum_{j\in\mathbb Z}e^{-\pi^2\lambda^3j^2/3}$ along even orders. Along odd orders the denominator before cancellation of the numerator’s factor two is the sum of one integer and one half-integer Gaussian series. Both include zero-field or near-half-order impostors.

**Weak field flight.** The normalized weak replicas have lattice momentum width $O(m^{-1/2})$ and center offset $-mh$ about $q_*$. Dividing either by $\delta$ gives $O(M^{-1/12})$. To justify a position prediction, replace their scaled profiles by the limiting Gaussians in norm and cut them off smoothly on $|z|\le L$. For fixed $L$, their normalized branchwise spatial scale follows by differentiating the smooth comparison state in $q$: the initial physical position norm is $O_L(\delta^2\sqrt m)=O_L(M^{-1/6})$. Smooth eigenvectors contribute $O(\delta^2)$. The scaled momentum norm tends to zero. The same-site plane is restored by summing the two parity replicas. Each circular curvature eigenspace has squared overlap $1/2$ with the initial sharp rail at its edge. The encoded-band estimate applies on every bounded scaled momentum interval, with force slope $sF$, action $\varepsilon=\delta$ and error tending to zero since $\delta^2/\varepsilon\to0$. The continuum position after time $T$ is $Y+bTp-bsFT^2/2$ for curvature $b=\pm1$. Its two narrow branches therefore converge to $\pm sFT^2/2$ with equal mass (one common point for zero). A characteristic function of physical position shifts microscopic momentum by $O(\delta^2)$, so distinct replicas stay separated and opposite bands in one replica have a vanishing overlap. Remove the fixed $z$ cutoff by sending $L\to\infty$. The conditional probability of the terminal union tends to one at $s=\pm1$ and to zero at every other fixed signed integer. [Forced-band norm estimate](Forced_envelope_and_classical_motion.md) · [Two-curvature detector read](Single_window_in_a_permanent_field.md)

**Half-order field flight.** For a fixed integer or half-integer offset, write $h=h_0+e$ with $h_0=\pm\pi/2$, $e=O(1/M)$. A pair of ticks at output $q$ is the matrix $A_h(q)=U(q)U(q+h)$ on the input $q+2h$. The output factors in the product for $N=\lfloor n/2\rfloor$ pairs have arguments $q+2je$ because $A_h$ is $\pi$-periodic. The extra input translation by $N(2h_0)$ exchanges equal even-parity replicas where necessary. Direct multiplication gives

$$
 \det A_h=1,\qquad 2\cos\theta_h(q)=\operatorname{tr} A_h(q)=\cos(2q+h)+\cos h.
$$

At either source carrier $q=0\bmod\pi$, $h=h_0$, the eigenvalues are $\pm i$ and hence have a uniform local gap. At $q=0$, $\theta'_h(0)=\sin h/\sqrt{1-\cos^2h}$; it tends to $+1$ or $-1$. Implicit differentiation gives $\cos\theta\,(\theta')^2+\sin\theta\,\theta''=2\cos(2q+h)$, so at exact half-order its second derivative at either carrier is zero. Since the original packet occupies $q=0\bmod\pi$ up to $o(1)$ and $n|e|=o(1)$, the two eigenphase derivatives converge uniformly on shrinking arcs containing all but $o(1)$ mass to $+1$ and $-1$ in some order. This yields velocities $+1/2$ and $-1/2$ **per ordinary tick**.

For the position consequence, choose smooth local eigenframes on these gapped arcs and retain their exact phases. Replacing successive frames by a common branch transport costs $O(N|e|)$ in norm by telescoping their overlaps. In the characteristic function of $x/n$ the Fourier shift is $\xi/n$. The initial source changes by at most $2m|\xi|/n=o(1)$ in norm under this shift, since its position support after preparation is within $2m$. The endpoint projectors contribute $O(|\xi|/n)$ cross-band overlap. Each same-band sum of $N$ eigenphases changes by $\pm\xi/2+o(1)$ uniformly on the retained arcs, using the derivative just computed and $N/n\to1/2$. An unpaired last tick changes the characteristic function by $O(|\xi|/n)$, by the one-site shift bound. Thus every subsequential ballistic limit is supported on $\{-1/2,1/2\}$, regardless of the split between them. This argument controls the derivative of the total phase even if an approximation of the total phase itself by its exactly resonant value would accumulate a large error. The bounded physical tubes correspond to $|x|/n=O(\delta)$, so their conditional probability tends to zero throughout this fixed-offset family.

With the weak-core and half-order results in hand, sum first over a finite set of offsets, separately on odd and even orders. Then remove that cutoff by the uniform tail bound. The only surviving terms in $M\Pr(E)/p_m$ are the two physical-unit terms, each tending to $e^{-\pi^2\lambda^3/3}$. This proves the claim without a rate of convergence uniform in all flight propagators.

## Priors, costs and finite counterchecks

All operations above commute with sheet translations. For any other incident folded mixture, the output odds multiply the input odds by the ratio of event likelihoods. The same proof gives asymptotic purity, with yield $b_* p_m e^{-\pi^2\lambda^3/3}$, if $b_*=b_1+b_{M-1}>0$ and every signed Fourier mass obeys $b_s\le C b_*$ uniformly. A persistent fair-count component of mass $b_C$ contributes at most $b_C2^{-m}$: after two underlying independent fair steps, the final rail is opposite the incoming rail with probability $1/2$. Count is negligible if $b_C 2^{-m}=o(b_*p_m)$. A zero unit input cannot be repaired by this sheet-blind instrument. Even positive unit input alone gives no prior-uniform guarantee. At a finite order with another primitive pair, each accepted signed path amplitude from a sharp launch is an integer polynomial evaluated at the sheet root, up to its common positive normalization. If it vanishes on another primitive root, cyclotomic conjugacy forces it to vanish on the unit root too. Summing nonnegative port probabilities preserves this obstruction; arbitrarily small target odds can defeat any finite positive likelihood ratio. [Galois support of signed histories](check_clock_galois_support.py)

The demonstrated one-pass clock spends $2m=O(M^{2/3})$ ticks before release; its unit rate per localized launch is $O(M^{-4/3})$. The subsequent terminal interval test performs real discrimination and consumes the flight. This differs operationally from preparing a selected character with high target completeness before another experiment. There is also an existence-only improvement in one-pass preparation cost. Apply the fixed-$\lambda$ result successively at $\lambda=1/j$. Choose increasing order thresholds beyond which posterior error and relative error in the yield are each at most $1/j$ at that fixed setting, and beyond which $m$ diverges along the schedule. The resulting piecewise constant $\lambda_M\downarrow0$ spends $o(M^{2/3})$ preparation ticks and has joint yield asymptotic to $2M^{-4/3}/\sqrt{\pi\lambda_M}$. This diagonal argument supplies no explicit thresholds or improved exponent; the terminal discriminator still takes order $M^{3/4}$ ticks. Arbitrary retries on a persistent unknown sector change the relative weights of the records and need their own accounting.

The checker fixes $F=T=1$, $\lambda=1/2$, radius $T_n^2/8$, with both $m$ and $n$ rounded to the nearest even clock. It propagates the signed rail amplitudes, applies the actual departure gains, and enumerates every folded label at ten orders from 32 through 513. Exact integer histories from localized sheet addresses on three smaller rings independently check the complete terminal ports and every first-failure total. The first-failure probability at each block appears in each finite row along with both terminal outcomes.

At $M=128,129$ neither interval contains an occupied-parity well. Their exact joint probability is zero. At $M=512$ the unit fraction rises from 0.24143 after the word to 0.28208 after the joint event. At $M=64$ it falls from 0.24368 to 0.15033. In a higher-order selected panel, $M=16384$, unit survival relative to zero is 0.66368 but the unit’s terminal conditional tube probability is only 0.10365. The finite panels give no practical purity threshold; the eventual conclusion uses the asymptotic bounds. [Reproducible checker](check_same_flight_sheet_selection.py) · [All finite rows and controls](results/same_flight_sheet_selection.json)
