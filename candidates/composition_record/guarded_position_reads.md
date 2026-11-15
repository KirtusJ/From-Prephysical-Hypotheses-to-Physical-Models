# A balanced terminal read in the walker's own wells

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development and verification with OpenAI Codex.

A detector calibrated on cells of squared norm at most $1/2$ can read an arbitrarily heavy parent cell if its terminal walk splits that cell into two equal weights. Two free Hadamard ticks suffice with two blank wells per parent. A third tick with controlled coasting and reversal reduces the space cost to one blank well per parent, the minimum for a state-independent guarantee. Both constructions handle arbitrary complex input rails and read position with the rails pooled. [Half-mass response calibration](spectator_refinements.md) · [Coin and shift on a cycle, Aharonov et al.](https://arxiv.org/abs/quant-ph/0012090)

## Two free ticks

Take $N=3m$ wells on a ring, $m\ge1$. At entry only the parent wells $x=3j$ may carry amplitude. Each may hold both rails, and different parents may be coherent. Coins act before the conditional shift, with $R$ stepping clockwise and $L$ counterclockwise. Use $H(R,L)=(R+L,R-L)/\sqrt2$ at both ticks. The first coin may equally be the identity. Write $(a,b)$ for the spinor at one parent just after its first coin, before the first shift. Its mass is $w=|a|^2+|b|^2$. At the first shift the two components go to $x+1$ and $x-1$. Applying $H$ there and shifting again gives

| Final well | $x-2$ | $x$ | $x+2$ |
|---|---:|---:|---:|
| Output $(R,L)$ | $(0,-b)/\sqrt2$ | $(b,a)/\sqrt2$ | $(a,0)/\sqrt2$ |
| Whole-well squared norm | $\lvert b\rvert^2/2$ | $w/2$ | $\lvert a\rvert^2/2$ |

Indices are modulo $N$. The three offsets occupy different residue classes modulo three. Each final well therefore belongs to exactly one parent, also at the wrap and at $N=3$. Reading the center and the union of its two outer wells gives two cells of mass exactly $w/2$ each. Reading all three separately also works, since each is at most $w/2$. Which bins the detector scores is specified before the terminal read. One tick cannot give this guarantee from an arbitrary two-rail input at even a single well. For any chosen first coin $C$, the input $C^\dagger(1,0)$ arrives in one well with unit mass.

## One blank well per parent

Take $N=4m$, $m\ge1$. Parents now occupy $x\equiv0,1\pmod4$. The first two ticks are as above. Different parents' outer wells can coincide at this clock. Even the two outer paths from one parent meet at $N=4$. Incoming rails remain coherent and unmeasured. Apply the identity coin on the parent wells and the swap $X(R,L)=(L,R)$ on the other wells. Then shift once. The outer right-going amplitude $a/\sqrt2$ reverses into $x+1$, and the outer left-going amplitude $-b/\sqrt2$ reverses into $x-1$. The center sends $b/\sqrt2$ to the right and $a/\sqrt2$ to the left. The two resulting spinors of each parent are therefore

$$
x-1:\ (-b,a)/\sqrt2,\qquad x+1:\ (b,a)/\sqrt2 .
$$

The sets $\{x-1,x+1\}$ partition the ring. Each of the two individual wells carries $w/2$ for every parent spinor. The third control is a permutation on rails at each site. It works even where two outer wavefronts have arrived from different parents. The walk model already uses these site-dependent coasting and reversal operations. [Matched-clock native switches](held_split_comparison.md#a-three-tick-walk-supplies-both-settings)

## Why the blank space matters

Let an isometry $U$ carry a $d$-dimensional admissible input space into $D$ orthogonal output modes. Let $\{P_i\}$ be an exhaustive orthogonal partition of those modes. Define $E_i=U^\dagger P_i U$. A uniform bound of $1/2$ on every cell for all normalized complex inputs gives $0\le E_i\le I_d/2$. Since $\sum_i E_i=I_d$,

$$
d=\sum_i\operatorname{tr}E_i
\ \le\ \tfrac12\sum_i\operatorname{rank}E_i
\ \le\ \tfrac12\sum_i\operatorname{rank}P_i=D/2 .
$$

Here $D$ counts the modes available to the terminal projective read. It includes any blank modes supplied to the apparatus. A classical relabeling adds no coherent modes. The three-tick construction attains equality with $d=N$ (two rails on $N/2$ parent wells) and $D=2N$. The bound concerns capacity for every input in the subspace. A specific history can have a much smaller reachable family at that clock.

On an even ring every nearest-neighbor coin-and-shift tick exchanges the even and odd well sectors. Any fixed sequence of such unitary ticks maps the entire input parity sector **onto** its output parity sector. Choose any normalized output basis rail in one measured well and evolve it backwards. Its admissible input produces unit mass at that well. The inverse witness may require support at several wells. Allowing both complex rails at a single localized well does not grant the whole parity sector as a source space. Even if every input well must have nonzero amplitude, a small generic perturbation of the inverse witness still gives mass above one half by continuity.

## Which records can use the read

For an earlier retained history label $h$, each parent spinor can be unnormalized and entangled with unobserved degrees of freedom. The formulas still hold with $a,b$ vectors and squared Hilbert norms. They therefore also apply to joint cells $(h,x)$ when those prefixes are resolved by the detector. If several parents form one physical bin $B$, the disjoint outputs may instead be grouped as the two child cells of $(h,B)$ before scoring. Each receives half the squared norm of $(h,B)$. For any launch whose common scalar response satisfies $f(u)=c_f u$ throughout $[0,1/2]$, with $c_f>0$, the resolved table has normalizer $c_f$. Summing the reported children after that score recovers each original parent weight exactly. This identity alone supplies no value for $f$ above half.

The entry condition requires a prepared sparse position register or a separately justified coherent routing of terminal amplitudes to those parent wells. Relabeling an already dense, fixed-size reflecting walk does not implement that routing. The [terminal refinement for reflected histories](refined_reflecting_histories.md) used the actual walk's positive-time spatial spread. The construction here gives a finite alternative when spare physical wells and the stated controls are provided. Both conclusions concern the specified terminal instrument and its calibration.

The [standalone Rust checker](check_guarded_position_reads.rs) propagates signed Gaussian-integer amplitude numerators. It compares every basis column and coherent complex superpositions against the stated amplitudes for $m=1,\ldots,8$ with both first coins, verifies the half-masses and checks the disjoint terminal bins including the periodic seams. Compile it with rustc in the Rust 2021 edition and run the executable.
