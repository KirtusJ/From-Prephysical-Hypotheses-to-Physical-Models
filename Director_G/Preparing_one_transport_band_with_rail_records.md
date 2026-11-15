# Preparing one transport band with rail records

A site-localized walker can supply its own extended packet, and a separate rail tag can select the sign of its velocity. The preparation uses a position-blind rail read after each pair of ordinary Hadamard steps, followed by the [four-route stopped instrument](Reading_a_rail_axis_with_four_coherent_routes.md). At finite preparation depth the wrong band retains nonzero weight. We bound that weight and the root-mean-square error of a terminal position read, first in free flight and then through a finite accumulated field impulse. Both parity-related peaks contribute to the same predicted motion.

This working supplement assumes ordinary squared-coordinate probabilities and the specified conditional operations. Its result concerns transport on a stipulated one-dimensional walk. Earlier work derived envelope equations for extended walk states, and electric quantum walks have been implemented with controlled atoms. Neither supplies data for the preparation proposed here. [Extended walk preparations](https://arxiv.org/abs/1004.0976) · [Electric walk experiment](https://arxiv.org/abs/1302.2094)

## A packet and a recorded tag

Use the Fourier transform with kernel $e^{-ikx}$, $-\pi\le k<\pi$, and normalized measure $dk/(2\pi)$. Position is $i\partial_k$. One tick applies $H=(X+Z)/\sqrt2$ to rails $(R,L)$, then translates $R$ one site right and $L$ one site left. Its fibre is $U(k)=\mathrm{diag}(e^{-ik},e^{ik})H$.

Start at $(0,R)$. Keep the field off during preparation. After each of $B\ge1$ pairs of ticks, read the rail, preserving coherence between all sites with that rail. End the preparation on the first $L$. The all-$R$ word leaves the last rail known. One passing pair multiplies its Fourier amplitude by $(U^2)_{RR}=e^{-ik}\cos k$. The passing word thus has probability and normalized envelope
\[
p_B={\binom{2B}{B}}/{4^B},\qquad g_B(k)=e^{-iBk}\cos^B k/\sqrt{p_B}.
\]
In real space the amplitude at $2j$ is $\binom Bj/\sqrt{\binom{2B}B}$, $0\le j\le B$. The squared amplitudes give a hypergeometric law for $j$ with population $2B$, $B$ marked objects and $B$ draws. Consequently the prepared centre is $B$ and its standard deviation is $s_B=B/\sqrt{2B-1}$. The ratio $p_{B+1}/p_B$ gives $\mathbb E_{|g_B|^2}\sin^2 k=1/(2B+2)$. The complementary [alternating-rail filter](Base_preparation_and_two_rays.md) peaks on a different pair of momenta.

On each passing launch apply $I$ or $X$ according to an independent fair bit, with the same operation at every occupied site. Pool that bit. This gives $|g_B\rangle\langle g_B|\otimes I/2$. From the cited stopped instrument, the two tags $\tau=\pm1$ now occur equally often. Their conditional rail densities are
\[
\rho_\tau=(I+\tau\eta_m H)/2,\qquad
\eta_m=(1-u^{2m})/(1+u^{2m}),\qquad u=3-2\sqrt2,\quad m\ge1.
\]
This application requires every fine selector history (including each corrected null) to act identically at every site, as $I_{\rm pos}\otimes K_{\rm history}$, or to have the same action after a known position correction. A local apparatus that retains information about the site, or moves different parts of the packet during the stopped sequence, requires a different analysis. The physical clock for flight starts at release, the field then acts at every departure. Position, transport time and any sheet orientation have to be registered consistently across launches.

Per original launch the first rail failure at pair $j$ has weight $p_{j-1}-p_j$ ($p_0=1$); completion with either specified tag has weight $p_B/2$. The selector uses a mean $\sqrt2\,m\eta_m$ raw reads per passing packet, including nulls. With a raw-attempt cutoff $D$, its timeout probability $d_{m,D}$ on the mixed input is retained. Sign reversal of the mixed-input sign history makes the two completed tag fractions $p_B(1-d_{m,D})/2$. Each history reaching a given threshold acts by a scalar multiple of the same rail operator, so the conditional completed state is still $\rho_\tau$. Without the independent reset, the input is sharp $R$, the tag weights are $(1+\tau\eta_m/\sqrt2)/2$, and the conditional state is proportional to $\sqrt{E_{m,\tau}}|R\rangle\langle R|\sqrt{E_{m,\tau}}$. Substituting $\rho_\tau$ for that preparation gives the wrong finite-threshold prediction.

## Free flight

Write $P=(I+\boldsymbol n\cdot\boldsymbol\sigma)/2$ for the band with eigenvalue $\lambda_+=e^{-i\omega}$; the other eigenvalue is $\lambda_-=-e^{i\omega}$. Direct diagonalization gives
\[
\sin\omega=\sin k/\sqrt2,\quad
\boldsymbol n=(\cos k,\sin k,\cos k)/\sqrt{1+\cos^2 k},\quad
v(k)=\omega'(k)=\cos k/\sqrt{1+\cos^2 k}.
\]
The velocity observable is $W(k)=v(k)(2P(k)-I)$. At both $0$ and $\pi$, $W=H/\sqrt2$. The analytic band names exchange between the parity-related charts: a tag $\tau$ selects the eigenvalue $\tau\,\mathrm{sgn}(\cos k)$ of $2P-I$ at launch. The two chart boundaries have zero Fourier measure. The mean weight $\ell$ of the opposite branch satisfies
\[
\ell=\tfrac12\mathbb E\!\left[1-\eta_m\sqrt2\,|\cos k|/\sqrt{1+\cos^2k}\right]
\le (1-\eta_m)/2+\eta_m/[4(B+1)] .
\]
Here $1-\sqrt2 |c|/\sqrt{1+c^2}\le 1-c^2$ on $[-1,1]$. This bound controls the initially selected pair of bands on the two charts.

Let $X_N$ be the ordinary position after $N\ge1$ unmonitored free ticks on the tagged packet. With $\|\cdot\|_2$ denoting RMS in this ensemble,
\[
\left\|(X_N-B)/N-\tau/\sqrt2\right\|_2
\le (s_B+\sqrt2)/N+
\sqrt{1-\eta_m+(2\eta_m-1)/[4(B+1)]}. \tag{1}
\]
Indeed $iU^\dagger\partial_k U=X$ (Pauli $X$). The band-diagonal part of $X$ is $W$. In the average of its $N$ Heisenberg conjugates each off-diagonal entry has a geometric sum whose norm before division by $N$ is at most $2/|\lambda_+-\lambda_-|\le\sqrt2$. The envelope derivative contributes $s_B/N$. Finally,
\[
\operatorname{tr}\rho_\tau(W-\tau I/\sqrt2)^2=
1-\eta_m+(2\eta_m-1)\frac{\sin^2 k}{2(1+\cos^2 k)}.
\]
Since $2\eta_m-1>0$, integration gives (1). The same norm argument applies to a purification of the rail density. For example, $m,B\to\infty$ and $\sqrt B/N\to0$ select a single velocity in the conditional terminal position law. The per-launch preparation yield $p_B$ tends to zero as $1/\sqrt{\pi B}$.

## Weak field over a finite impulse

Attach $e^{-ihx}$ at each departure during flight, so the incoming Fourier characteristic $k$ reaches $k_j=k-jh$ after $j$ steps. Use the ordered product $T_j=U(k_j)\cdots U(k_1)$, $T_0=I$. For real $h$ define the predicted mean velocity $\bar v_{N,h}=N^{-1}\sum_{j=1}^N v(-jh)$. Then
\[
\left\|(X_N-B)/N-\tau\bar v_{N,h}\right\|_2
\le \frac{s_B+4}{N}+16|h|+32Nh^2+
\sqrt{2\ell}+\frac{\pi}{2\sqrt{2B+2}}. \tag{2}
\]
The constants below use the global band gap, so the flight may cross a zero of its group velocity.

Here is a finite-step proof. For a Hermitian matrix $Y(k)$ let
\[
L_k(Y)=aP Y(I-P)+\bar a(I-P)YP,\qquad a=(\bar\lambda_+\lambda_- -1)^{-1}.
\]
It solves $U^\dagger L_k(Y)U-L_k(Y)=P Y(I-P)+(I-P)YP$. Define $Q=L_k(P')$ and $C=L_k(X)$. Derivatives use the initial momentum coordinate. The bounds
\[
\|P'\|\le1,\quad \|P''\|\le4,\quad |a|,|a'|\le1,\quad
\|Q\|,\|C\|\le2,\quad \|Q'\|\le14,\quad \|C'\|\le6
\]
follow by differentiating the displayed formulas. In detail $g=(\cos k,\sin k,\cos k)$ has $|g|\ge1$ and $|g'|,|g''|\le\sqrt2$. Differentiating $\boldsymbol n'=(I-\boldsymbol n\boldsymbol n^T)g'/|g|$ gives $|\boldsymbol n'|\le\sqrt2$, $|\boldsymbol n''|\le 4+\sqrt2+2<8$. Also $|\lambda_+-\lambda_-|\ge\sqrt2$ and $|\lambda_\pm'|\le1$. The product rule gives the remaining bounds.

Since $P'$ is off-diagonal relative to $P$, $U^\dagger Q U-Q=P'$. Transport $P+hQ$ by one step from $k_j$ back to $k_{j-1}=k_j+h$. Taylor's theorem bounds the norm defect by $h^2(\|P''\|_\infty/2+\|Q'\|_\infty)\le16h^2$. Telescoping $j-1$ steps and removing $hQ$ at both ends yields
\[
\|T_{j-1}^\dagger P(k_j)T_{j-1}-P(k)\|
\le5|h|+16(j-1)h^2 .
\]
The additional $|h|$ accounts for using $P(k_j)$ one step ahead. Meanwhile $X-W=U^\dagger C U-C$. The derivative $iT_N^\dagger\partial_k T_N$ is the sum of $T_{j-1}^\dagger X T_{j-1}$. In the sum its $X-W$ terms telescope, leaving two end terms of total norm at most 4 and at most $N-1$ differences of successive $C$ of norm $6|h|$. Together with the preceding projector estimate and $2|v|\le2$ this gives
\[
\left\|N^{-1} iT_N^\dagger\partial_k T_N-
 (2P(k)-I)N^{-1}\sum_j v(k_j)\right\|
\le4/N+16|h|+32Nh^2 .
\]
The final Fourier translation leaves the position derivative unchanged. Fold the initial $k$ to $r\in[-\pi/2,\pi/2)$ by a multiple of $\pi$. Since $v(k+\pi)=-v(k)$, $|v'|\le1$ and $|r|\le(\pi/2)|\sin k|$, replacing the fibre speed by its chart-centre value costs at most $\pi/(2\sqrt{2B+2})$ in RMS. Using the selected sign costs at most $2\|v\|_\infty\sqrt\ell=\sqrt{2\ell}$. Adding the initial width proves (2).

For $h=F/n$, $N=\lfloor nt\rfloor$, fixed $t>0$, $m,B\to\infty$ and $\sqrt B/n\to0$, $(X_N-B)/n$ therefore converges in mean square to $\tau\int_0^t v(-Fs)\,ds$. This holds at each prescribed endpoint. Multiple observations on the same launch would specify additional interventions. For $F=0$ the curve is straight; at finite $F$ it uses the actual periodic dispersion. It has zero initial acceleration at $k=0$. A switchable field or a verified preparation compensation, the realization of the phase, the conditional read rule and the units of this curve are explicit premises. A [permanently active field and a different release protocol](Field_on_source_and_release.md) require their own analysis.

## Why the mechanical band edge is different

The [constant-mass Schrödinger and Newtonian limits](Forced_envelope_and_classical_motion.md) use $k_*=-\pi/2$, where the plus-band Bloch vector points along $-Y$; at $+\pi/2$ it points along $Y$. Every real rail density, including either tagged $\rho_\tau$, has exactly half of its mass in each band there. In a packet converging to those two chart centres, this gives half in each curvature branch for this product preparation, uniformly even as $m$ increases. At either centre a homogeneous real propagation step $D(k)H$ is a real matrix times a common phase. More generally a homogeneous finite real stencil with displacements of one parity has the same property there for each fine record. A fixed such filter with nonzero passing probability at the centre preserves reality of its conditional rail there. This centre argument places no uniform bound on filters of increasing depth or success vanishing at the centre. [Two returning gain paths](Returning_loops_and_one_classical_ray.md) supply a verified relative phase for selecting one accelerating mechanical ray. The real stopped tag by itself prepares the ballistic branch proved above.

The [replay](check_tagged_transport_band.py) uses signed coordinate paths for the passing filter, exact finite stopped-tag effects, and direct position-space propagation for both field signs. It also checks the matrix identities in the proof at off-axis momenta. All its numbers are calculations on the stipulated walk. The physical origin of the walk and its record rule remains open.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed the preparation, estimates and computational verification.
