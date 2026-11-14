# Resolution of a single uninterrupted Hadamard flight

**Kirtus Justus**, Theoretical Physicist
Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Let a walker start at one well $x_0$ of a $4M$ ring with a fixed normalized rail state. Apply the same signed Hadamard on every tick and stream in the two directions. At departure from $x$, the sheet gains $\lfloor x/2\rfloor$. Read the final well and rail at tick $n\ge1$, ignoring the sheet. For a pure sheet character $s$, write $h=\pi s/M$ using a signed representative. Let $\mathsf P_h$ be the complete terminal law, and $\mathsf P_0$ its zero-field counterpart. We obtain

$$
\|\mathsf P_h-\mathsf P_0\|_{\rm TV}
\ \le\ B_n(h):=\min\left\{1,\sqrt2(n-1)|h|+
                   \frac{n(n^2-1)}{24}h^2\right\}.
$$

The same bound applies to $|\sqrt{\mathsf P_h(A)}-\sqrt{\mathsf P_0(A)}|$ for any event $A$ in the well and rail records. In particular, fixed labels 1 and 2 have vanishing terminal contrast for $n=o(M^{2/3})$, including at $n$ proportional to $\sqrt M$. A sheet localized at one address starts with equal weights on all characters. For a proposed high-completeness filter on that prior, even the neighboring fixed label competes at nearly the same rate in this time regime. The conclusion concerns a fixed coin, a sharp launching well and one terminal read. Coherent routing or intermediate records change the product of matrices used below. [Local controls and general tick bounds](Local_filter_resolution.md)

## Momentum translation on a finite ring

In the negative-exponent Fourier convention,
$U(k)=\operatorname{diag}(e^{-ik},e^{ik})H$ is the free tick. On the occupied parity $p_j=(x_0+j)\bmod 2$ the staircase phase is $e^{ihp_j}e^{-ihx}$. Its first factor contributes a global scalar. Multiplication by the second shifts the Fourier input to $k+h$. After $n$ ticks the rail vector is therefore, up to the parity scalar,

$$
U(k)U(k+h)\cdots U(k+(n-1)h)\,
e^{-i(k+nh)x_0}\xi ,
$$

with the common DFT normalization understood. This formula includes both starting parities. It also accounts for a start on the seam, since $e^{-ihx}$ is periodic on the physical ring. The product representation of a linear electric phase is standard for discrete walks. [Cedzich et al., electric walks](https://arxiv.org/abs/1302.2081) · [Staircase-to-linear reduction on each parity](Refinement_and_free_fall.md)

Put $c=k+(n-1)h/2$. The momentum mesh is $\pi/(2M)$, so $c-k$ is exactly $(n-1)s$ mesh steps. Replacing the product by $U(c)^n$ produces the free terminal state multiplied by a site-dependent phase and a common launch phase. Explicitly, insert $e^{-icx_0}$ for the free sharp launch; its ratio to $e^{-i(k+nh)x_0}$ is independent of $k$. The momentum translation $k\mapsto c$ is precisely a diagonal phase in position space. Reading a well and rail, or coarse-graining that read, preserves every free terminal probability after this replacement.

## The centered product estimate

The eigenvalues of $U(k)$ are $\lambda_+=e^{-i\omega(k)}$ and $\lambda_-=-e^{i\omega(k)}$, with $\omega(k)=\arcsin(\sin k/\sqrt2)$. Their separation is at least $\sqrt2$. If $P$ is the first spectral projector and $Q=I-P$, differentiation of $UP=\lambda_+P$ gives $QP'P=QU'P/(\lambda_+-\lambda_-)$. The derivative of an orthogonal projector is off diagonal in $P,Q$. Since $\|U'\|=1$, we have $\|P'\|\le1/\sqrt2$. Transport a unitary eigenframe $V$ on the real momentum lift by $V'=[P',P]V$. It carries a fixed reference projector to $P$ and $\|V'\|\le1/\sqrt2$. A globally periodic eigenframe is unnecessary for an estimate on a lifted interval. [Hadamard spectral conventions](Folded_field_and_native_gaussian.md)

Write each factor $U(k+jh)$ in that frame. Replacing the $n-1$ intervening frame overlaps by identities costs at most $(n-1)|h|/\sqrt2$ in operator norm, since all surrounding factors are unitary. Replacing the two outside frames by $V(c)$ and its adjoint costs at most the same amount, as each endpoint lies $(n-1)|h|/2$ from $c$. The remaining diagonal matrices commute.

The derivative and curvature of the eigenphase satisfy

$$
\omega'(k)=\frac{\cos k}{\sqrt{1+\cos^2k}},\qquad
\omega''(k)=\frac{-\sin k}{(1+\cos^2k)^{3/2}} .
$$

The linear Taylor terms sum to zero about $c$ and $|\omega''|\le1$. Thus the difference between the sum of the phases and $n\omega(c)$ is bounded by

$$
\frac12\sum_{j=0}^{n-1}\left(j-\frac{n-1}{2}\right)^2h^2
=\frac{n(n^2-1)}{24}h^2 .
$$

This controls the error in either diagonal eigenvalue product since $|e^{iu}-e^{iv}|\le |u-v|$. Adding the frame error proves the uniform matrix bound in the first display before taking the minimum with one. Parseval transfers it to the norm of the difference of the actual state and the rephased free state. Trace distance for pure states bounds terminal total variation by this norm. For a terminal event, restriction to the corresponding orthogonal subspace and the reverse triangle inequality bound the difference of square roots.

## Limits of the inference

For fixed $s,r$, a per-launch event with $p_s\ge q>0$ cannot also satisfy $p_r\le\lambda p_s$ for a fixed $\lambda<1$ along $n=o(M^{2/3})$. Its square-root gap would stay at least $(1-\sqrt\lambda)\sqrt q$, whereas the bound for the two labels tends to zero. At $n^3/M^2\to1$ a bounded score using the individually resolved wells has different limiting expectations on sectors zero and one. The total-variation estimate does not determine Fisher information. In dark or very rare bins, a small absolute probability change need not give a small relative change. The two final states compared in momentum space also differ by a spatial phase. A coherent observable that reconnects different terminal wells can detect it. [Terminal interference at the critical scale](Uninterrupted_sheet_fringes.md)
