# One local clock for mass and force

**Kirtus Justus**, Theoretical Physicist  
Port Coquitlam, British Columbia, Canada

Research supplement by Director G (OpenAI Codex).

A nearest-neighbor walk can realize a prescribed uniform force with bounded transport speeds on both its base and its cyclic sheet. Its classical position limit can start from an explicitly prepared real sheet packet occupying a vanishing fraction of the ring. The packet need not select an ordinary Fourier pair. This removes two preparation and timing assumptions from the [earlier massive walk](Finite_speed_mass_and_motion.md). The costs include a fine material or encoded sheet pitch, addressed source preparation, a common programmed clock, and an assumed squared readout. The force is prescribed independently of other particles.

## Which quarter-turns cost time?

Write the earlier sheet-built coin as $D X_j D^\dagger$, with $X_j=H\operatorname{diag}(T^j,T^{-j})H$, $D=\operatorname{diag}(I,T^{M/4})$, and $T$ the physical unit sheet translation. The base stream, any position-dependent rail-independent sheet translation, and every base-position/rail outcome projector commute with $D$. Across an arbitrary prescribed sequence of these mass coins, scalar kicks and recorded outcomes, the product has the form $D V D^\dagger$, with $V$ the same product of bare operations. A sum over the terminal sheet is invariant under the remaining rail-dependent cyclic permutation. The original $D^\dagger H|R\rangle$ input becomes $D^{-2}H|R\rangle$ in the bare frame. On odd characters its rail part is $ZH|R\rangle$ and on even characters it is $H|R\rangle$. Coherently mixing the terminal rails or recording the sheet may expose the boundary transformation. [Lean verification on signed histories including interference](lean/MassGauge.lean)

Removing $D$ still leaves the cost of a large $j$ in the earlier clock. Instead set the **mass** angle per tick equal to one sheet step $\theta=2\pi/M=\mu\tau/\varepsilon$, where $m>0,\ \mu=mc^2$, the base spacing is $\ell=c\tau$ and $\varepsilon$ is the action scale. Use $X_1$, so its action on character $k$ is $\exp(-ik\theta\sigma_x)$. Use the real input $H|R\rangle=|+x\rangle$ on all characters. This is its own physical source. The sign and source conventions must be transformed together when comparing it to the older $Y$-mass implementation. [Literal sheet updates and signed projections](check_local_mass_register.py)

## Implementing the prescribed force with unit sheet moves

Let $F$ be the fundamental force coefficient, $h=Fc\tau^2/\varepsilon$. On the line the scalar departure phase is $\exp(-ik h x)$. At tick $n$, multiplying the output of the vector-potential representation by $\exp(-inkhx)$ recovers the scalar representation. Its stream has matrix $\exp[-i(q-knh)\sigma_z]$ at base momentum $q$ after the mass coin. This follows by induction since arriving at $x$ on rail $d=\pm1$ means departing from $x-d$. Site/rail records commute with this position phase, as do their diagonal history flags. A finite periodic comparison requires consistent boundary twists or bounded support clear of the boundary. This equivalence for electric walks has independent precedents. [Unitary equivalence of quantum walks](https://arxiv.org/abs/1401.0196) · [External gauge fields on discrete walks](https://arxiv.org/abs/1808.10850)

For a physical unit stroke, define $A_n=(h/\theta)n(n+1)/2$, $Q_n=\lfloor A_n+1/2\rfloor$ and $j_n=Q_n-Q_{n-1}$, $Q_0=0$. Replace $nh$ in the vector stream by $\theta j_n$ through opposite signed translations on the rails. At time $n\tau\le T_0$,

$$|j_n|\le 1+ |F|cT_0/\mu,\qquad |r_n|=|k\theta(Q_n-A_n)|\le |k|\theta/2.$$

Correct the rounded state by the *mathematical* rail rotation $\exp(-i r_n\sigma_z)$. Its change from the previous tick cancels the stream discrepancy. The only new error is moving the preceding correction through the mass coin, whose off-diagonals have modulus $|\sin(k\theta)|$. Its operator norm is at most $2|\sin(k\theta)\sin r_{n-1}|$. Telescoping over the unitary updates and restoring the terminal phase gives, uniformly in the base momentum,

$$\|\psi_{\rm rounded}-\psi_{\rm vector}\|
\le |k|\theta/2 + n\,|k|^2\theta^2.$$

The same comparison extends to finite coordinate-outcome sequences via contractions, or jointly by coherent flags that commute with the rotations. Conditioning on a rare outcome also requires its yield. At fixed $k$, $\tau=o(\varepsilon^2)$ suffices. Rounding each $nh/\theta$ in isolation instead of carrying its remainder sets every force stroke to zero when $|F|cT_0/\mu<1/2$. At $M=3200$, $F=1/2$, $c=\mu=1$ and $T_0=1/2$, the tested sine-position harmonic was $-0.0395323$ for cumulative rounding, $-0.0395369$ for the ideal vector flight, and zero for isolated rounding. [Full wave, negative-force and zero-force controls](results/local_mass_register.json)

All sites use the same precomputed $j_n$. There is no need to receive a particle position to run this clock. Choose $J=\lceil |F|cT_0/\mu\rceil+1$ and allocate $J+4$ subslots per tick for two Hadamards, one mass stroke, up to $J$ vector strokes, and one base stream. With sheet pitch $b=v_y\tau/(J+4)$ the base and sheet microstep speeds are bounded by $(J+4)c$ and $v_y$ respectively. Changing $c$ or allocating different subslot durations permits a specified joint speed cap at a fixed horizon. The physical sheet circumference $Mb=O(\varepsilon)$ shrinks, and the local coordinate count grows as $O(\varepsilon/\tau^2)$ for a base window of fixed length. A fixed-size sheet circumference with the same orders would instead give sheet speed of order $1/\varepsilon$ during a stroke. Preloaded schedules, or local counters with accounted timing, are part of the apparatus. A dynamical force emanating from another moving source remains an independent problem. [Current two-body mediation result](Local_mediation_and_the_force_clock.md)

## A real sheet source for the classical record

For a product launch take a rest packet on the base, the real $|+x\rangle$ spin, and on the sheet

$$v_y=\frac{\mathbf1_{0\le y<B}-\mathbf1_{B\le y<2B}}{\sqrt{2B}},\qquad 2B\le M.$$

For dyadic $2B$, use a balanced split, a conditional unit-speed series of sheet translations and an addressed reversible rail reset at each dyadic scale. Apply a minus sign to the upper half. The circuit uses $\log_2(2B)$ balanced splits and $2B-1$ conditional unit translations, with success one. The signed permutations require physical access to the relevant address bit. Fourier summation gives $w_0=0$ and

$$w_k=\frac{2\sin^4(\pi kB/M)}{MB\sin^2(\pi k/M)},\qquad
\sum_{|k|>K}w_k\le\min(1,M/(BK)),$$

where $k$ is folded at $M/2$. The bound follows from $\sin(\pi |k|/M)\ge2|k|/M$ and $\sum_{k>K}k^{-2}\le1/K$. For $B=M/4$ the $\pm2$ pair alone has limiting weight $4/\pi^2$. For even $B$, $k=M/2$ is exactly absent. At any finite time a sheet-unread position record of the product source is the weighted sum of sector records by Parseval. No measurement of $k$ is involved. [Circuit, spectra and cutoff controls](results/common_ray_source.json)

In a sector $k\ne0$, the effective continuum Hamiltonian at physical momentum $p$ is $cp\sigma_z+k\mu\sigma_x$, with $p(t)=p_0-kFt$. At rest the real launch selects energy sign $\lambda=\operatorname{sgn} k$. Its velocity $\lambda c^2p/\sqrt{k^2\mu^2+c^2p^2}$ at $p=-kFt$ is independent of $k$. This includes the even sectors in the bare model. Integrating gives the same rest trajectory as the fundamental sector, with a low-velocity Newtonian error bounded by $|F|^3T_0^4/(8m^3c^2)$. Uniformity through a growing momentum window requires more than this algebraic cancellation.

For definiteness set $c=\mu=F=1$, $M=2^{16r}$, $\varepsilon=M^{-1/2}$, $\tau=2\pi\varepsilon/M$, $B=M^{7/8}$ and $K=M^{3/16}$. A smooth rest packet with $|p_0|\le O(\sqrt\varepsilon)$ and physical position width $O(\sqrt\varepsilon)$ suffices. The [positive triangular base source](Finite_speed_mass_and_motion.md) also works: its folded RMS is $O(\sqrt\varepsilon)$, so use a smooth cutoff at fixed small $p_0$ first, transfer norm errors for bounded records, and then shrink the cutoff. On $1\le |k|\le K$, the momentum characteristic is $O(KT_0+|p_0|)$. The endpoint and commutator bounds for the Dirac splitting are $O(K\tau/\varepsilon+K^2\tau/\varepsilon^2)$. The adiabatic estimate is $O(\varepsilon/|k|)$ because both the gap and field grow like $|k|$. The launch eigenvector error is $O(|p_0|/|k|)$ and the position shift deviates from the rest ray by $O(T_0|p_0|/|k|)$. The folded base charts lie within the linear momentum regime since $K\tau/\varepsilon\to0$; their separated Fourier supports remove cross terms in fixed position harmonics. These are the spinor estimates of the [finite-speed flight derivation](Finite_speed_mass_and_motion.md), applied with the sector-dependent parameters.

The largest splitting and accumulated rounding error scales as $O(M^{-1/8})$. The spectral tail is at most $M^{-1/16}$. For any bounded position observable its tail contribution to a difference of normalized means is at most twice that weight times the operator norm. The initially occupied sheet fraction $2B/M=2M^{-1/8}$ vanishes, and the physical preparation time is $O(B\tau)=o(\varepsilon)$, including $O(\tau\log B)$ address operations under the stated clock. Thus this coherent, real, multi-sector source yields one limiting classical position measure. This particular classical record cannot certify an ordinary probability embedding. [Finite mixtures, actual observation times and scale table](check_common_ray_source.py)

Removing the zero Fourier mode by itself is insufficient for this proof. At even $M$, $k\mapsto k+M/2$ multiplies one step by $(-1)^{1+j_n}$. A two-site signed dipole and a single-site source have exactly the same combined weights in each such pair and hence identical sheet-unread flight records. Both retain substantial high-mode mass outside the proved window. The finite examples in the checker keep these controls and the individual sector residuals. Relating the programmed controls, observations and metric to physical primitives remains open. [Ontology map](ontology_gate_map.json)
