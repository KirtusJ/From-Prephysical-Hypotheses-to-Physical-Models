# A terminal fringe at the resolution time of the unmodified walk

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Start at $(0,R)$ on a $4M$-site ring. Every streamed tick uses the same balanced signed Hadamard. Both outgoing rails receive the departure sheet gain $\lfloor x/2\rfloor$. Read site and rail only at the terminal tick $t$. For field character zero or one, denote these two conditional laws by $\mathsf P_0,\mathsf P_1$. At $t=o(M^{2/3})$ their total variation tends to zero. Here we show that when $t^3/M^2\to1$, a single bounded statistic of the terminal read has different limiting means. The critical time scale for distinguishing these two sectors at nonvanishing contrast is therefore $M^{2/3}$. The sheet's spatially localized launch gives the uniform prior on all sectors for sheet-blind records. Distinguishing the two specified conditional laws does not isolate the unit from that entire prior. [Centered upper bound](Uninterrupted_sheet_read.md) · [Filter with real routing controls](Routed_sheet_filter.md)

## A statistic computed from the recorded well and rail

On the measured rail R, set $v=x/t$ and keep $1/4\le v\le1/2$ in a lift about the launch. Write

$$
 \kappa=\arccos\frac{v}{\sqrt{1-v^2}},\qquad
 \omega(k)=\arcsin(\sin k/\sqrt2),\qquad
 c=(1-v^2)\sqrt{1-2v^2},\qquad a=(1+v)/2 .
$$

Put $\Phi=2x\kappa-2t\omega(\kappa)+\pi/2$ and $\Delta_M=\pi^2 t(t^2-1)c/(12M^2)$. Assign the recorded outcome the real number $F=\sin(\Phi+\Delta_M/2)$ if it is in the specified window and rail, and assign zero to each other outcome. This is classical processing of a final site-and-rail record, requiring individual well resolution. All expectations here are per launch within the stated sector; there is no condition on landing in the window.

As $M,t\to\infty$ with $t^3/M^2\to1$,

$$
 \mathbb E_1F-\mathbb E_0F\ \longrightarrow\
 -D,\qquad
 D=\frac2\pi\int_{1/4}^{1/2}\frac{a(v)^2}{c(v)}
           \sin\!\left(\frac{\pi^2c(v)}{24}\right)\,dv>0 .
$$

In particular $\liminf\|\mathsf P_1-\mathsf P_0\|_{\rm TV}\ge D/2$. Midpoint quadrature gives $D\approx0.0305733$. For a binary read, accept the terminal record with classically randomized probability $(1+F)/2$. The limiting difference is exactly $-D/2$. Repeated independently prepared samples of one of the two specified sectors distinguish this pair by their average bounded score. A sign reversal of all sheet phases conjugates every amplitude from this real launch and leaves every conditional probability unchanged.

## Centered phases and their two stationary contributions

It suffices to use the line, since the native walk has range $t=o(M)$ about its source. The finite-ring and infinite-line probabilities are identical on that cone. Use $U(k)=\operatorname{diag}(e^{-ik},e^{ik})H$, $P(k)$ for the eigenvalue $e^{-i\omega(k)}$, and $Q=I-P$ for $-e^{i\omega(k)}$. On a fixed occupied parity, the staircase contributes a linear phase of slope $h=\pi/M$, times a scalar. A reversal of its sign merely conjugates the amplitude in this experiment.

In the momentum product center $t$ factors about $k$. The eigenframes at successive arguments differ by $O(h)$ and the two outside frames differ from the center by $O(th)$. Removing all these changes costs $O(th)$ in operator norm, uniformly in $k$, by the unitary telescoping estimate in the upper-bound paper. The sum of the eigenphases equals

$$
 t\omega(k)+\frac{h^2t(t^2-1)}{24}\omega''(k)+O(h^4t^5).
$$

The odd centered moments vanish and $\omega$ has bounded fourth derivative. Here $th\to0$ and $h^4t^5\to0$. Up to a position-diagonal phase, the actual state is therefore $o(1)$ in norm from the inverse Fourier transform of

$$
 \Big[e^{-it\omega(k)-iB\omega''(k)}P(k)
      +(-1)^t e^{it\omega(k)+iB\omega''(k)}Q(k)\Big]e_R ,
 \qquad B=\frac{h^2t(t^2-1)}{24}.
$$

This norm error contributes $o(1)$ to the expectation of every statistic bounded in magnitude by one, including time-dependent $F$. The approximation is invoked for bounded observations; it supplies no relative accuracy for a single rare port.

Since $U(k+\pi)=-U(k)$, $P(k+\pi)=Q(k)$, $\omega(k+\pi)=-\omega(k)$, and likewise for $\omega''$. In the inverse Fourier integral the second term thus gives $(-1)^{x+t}$ times the first. At every occupied well $x\equiv t\bmod2$ the replica doubles the amplitude. The RR entry of $P(k)=(U(k)+e^{i\omega(k)}I)/(2\cos\omega(k))$ equals $(1+\omega'(k))/2$. On the compact velocity window the phase $vk-\omega(k)$ has precisely the two nondegenerate critical points $k=\pm\kappa$. There $\omega'(k)=v$ and $\omega''(\pm\kappa)=\mp c$. Stationary phase gives the R amplitude of the approximating transform as

$$
 \frac{4a}{\sqrt{2\pi t c}}\,
 \cos\!\left(x\kappa-t\omega(\kappa)+\frac\pi4+Bc\right)
 +O(t^{-3/2}).
$$

The expansion is uniform on the specified window because $c$ is bounded away from zero, the critical points stay separated, and the smooth Fourier multipliers have uniform derivative bounds for bounded $B$. The free formula has $B=0$. The free-walk interference in the interior of the ballistic cone has also been derived for general initial spinors. [Sunada and Tate, *Asymptotic behavior of quantum walks on the line*](https://arxiv.org/abs/1108.1878)

Subtracting squared amplitudes and multiplying by $F$ gives the leading contribution per occupied well

$$
 -\frac{8a^2}{\pi t c}\,\sin(\Delta_M/2)\,
             \sin^2(\Phi+\Delta_M/2).
$$

The stationary expansion's summed probability remainder on the window is $O(t^{-1})$. Only half the sites are occupied, and the oscillatory square has limiting average $1/2$ there. To see this last point, write $x=2j+p$ with fixed tick parity $p$. In the exponential contributing to $\cos(2\Phi+\Delta_M)$ the phase derivative in $j$ is $8\kappa(v)+O(1/t)$ because $d[v\kappa(v)-\omega(\kappa(v))]/dv=\kappa(v)$. Throughout this compact window $\pi/4<\kappa(v)<\pi/2$, so the phase increments are uniformly separated from multiples of $2\pi$ and change by $O(1/t)$ per step. Summation by parts using $e^{i\phi_j}=(e^{i\phi_{j+1}}-e^{i\phi_j})/(e^{i(\phi_{j+1}-\phi_j)}-1)$ bounds the oscillatory sum with its smooth weight by a constant. The remaining Riemann sum, including the parity factor, gives the displayed integral under either tick parity.

## Finite records and sharp intermediate reads

The same experiment distinguishes folded one from folded two at the same scale. A fixed signed label $s$ replaces $B$ by $s^2B$. Use $F_{12}=\sin(\Phi+5\Delta_M/2)$ on the same R window and zero elsewhere. The preceding proof gives $\mathbb E_2 F_{12}-\mathbb E_1 F_{12}\to-(2/\pi)\int (a^2/c)\sin(3\pi^2c/24)\,dv$. Its magnitude is strictly positive since $0<c\le1$ and $0<3\pi^2/24<\pi$. Numerically it is $0.0814301$. At $M=32768,t=1024$ the computed contrast is $-0.0812190$, while the full site-and-rail variation for this pair is $0.303673$. A joint classification guarantee for unrestricted labels and the uniform prior would require a separate bound.

At $M=32768$ the full well-and-rail variations at ticks 1023, 1024 and 1025 are $0.112587$, $0.117909$ and $0.114816$. The corresponding measured-statistic mean differences in the model are $-0.030551$, $-0.031009$ and $-0.030679$. At tick 181, near $\sqrt M$, the full variation is $0.000651$. The checker archives all selected ticks, the variation after pooling by position or by rail, probability-normalization residuals and a comparison with independent integer signed sheet-address histograms at short times. The full variation is an optimized distinction between two model distributions; the statistic above is one specified terminal read. A fixed macroscopic position bin generally averages out the oscillation. [Checker](check_uninterrupted_sheet_read.py) · [All finite comparisons](results/uninterrupted_sheet_read.json)

Suppose sharp well-and-rail reads are also allowed between blocks of otherwise free evolution. The clock of the next block may depend on the previous sharp outcomes. Conditional on the sector and an identical transcript so far, both models start the block with the same sharp well and known rail. A maximal coupling of their next outcomes fails with probability at most the one-block bound. The probability of any difference in the full transcripts is at most the largest sum of those block bounds along a common transcript. If the total elapsed time is at most $T$, then $\sum_i n_i\le T$ and $\sum_i n_i^3\le T^3$. The terminal upper bound gives full transcript variation at most $\min(1,\sqrt2 T|h|+h^2T^3/24)$. Adaptive sharp reads therefore cannot achieve constant contrast for this pair in $o(M^{2/3})$ total ticks. Coarse measurements that preserve a spatial superposition, active routing and sheet-sensitive controls require their own comparison.
