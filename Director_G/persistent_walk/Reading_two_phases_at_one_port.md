# Reading two phases at one return port

Research for Kirtus Justus · 15 November 2026 · B.C. Pacific Time (PCT, UTC−07:00)

On the ideal five-site Hadamard ring, eight terminal probabilities at one port determine the two phases of the calibrated even-tick return law. The offsets, in physical ticks from a common even starting time, are **0, 2, 4, 6, 14, 16, 18, 20**. The theorem also holds for arbitrary starting points on the closure of the ideal orbit. It gives a sufficient schedule. The minimum number of settings is open here.

Use one fixed preparation, with an unknown but reproducible even-time phase origin, and fresh launches for the different terminal measurements. Write the phases as $z=e^{ix}, w=e^{iy}$. The calibrated increments $u,v$ are the upper-half-plane roots specified by $u+u^{-1}=(3-\sqrt5)/4$, $v+v^{-1}=(3+\sqrt5)/4$. At offset $2k$ the ideal probability is

$$
 p_k(z,w)=\frac{[1+2\Re(zu^k)+2\Re(wv^k)]^2}{25}.
$$

At starting tick $2n$, the physical walk formula has $(z,w)=(u^n,v^n)$. For the proof the two phases may be anywhere on the torus. The Fourier derivation, integer walk recurrence and proof of density for the actual orbit are supplied in the [one-port return study](Return_at_one_port.md).

## Why squaring the amplitude still allows recovery

Let $X=(z,\bar z,w,\bar w)$ and $r_k=(u^k,u^{-k},v^k,v^{-k})$. For any two phase pairs giving the same eight probabilities, their eight real signed amplitudes have equal magnitudes. At each time either the amplitudes agree, giving $r_k(X-Y)=0$, or their signs differ, giving $(1,r_k)\binom{2}{X+Y}=0$, with $X,Y$ written as columns. A zero amplitude may be assigned to either group.

Every four of the chosen $r_k$ are linearly independent, and every five of the augmented $(1,r_k)$ are linearly independent. If at least four signs agree, the first condition gives $X=Y$. Otherwise at least five signs differ, which would force the vector with first coordinate 2 to vanish. This proves uniqueness including at zero returns.

There is a direct reconstruction. Give each of the first four values $5\sqrt{p_k}$ each possible sign, subtract one, and solve the four linear equations for $X$. Check conjugacy, unit modulus and all eight probabilities. The argument proves that the surviving phase pair is unique for exact model probabilities. Duplicated sign choices at zero can yield the same pair. When eight exact readings give no such pair, they are inconsistent with this calibrated family.

## Exact check of the sampling times

The [checker](check_phase_readings.py) computes 70 four-row and 56 five-row determinants in the prime field of order 1009. It sends $\sqrt5,u,v$ to 244, 667 and 387. These satisfy the three defining equations and both phase images are invertible. The discriminant independence proved in the one-port study gives a degree-eight tower over the rationals, with monic defining equations successively for $\sqrt5,u,v$ over the dyadics. Reduction in each generator leaves a unique polynomial of degree at most one in each. Thus evaluation at these finite-field values is a homomorphism on the ring of coefficients used by the determinants. A nonzero residue certifies a nonzero original determinant. All 126 residues are nonzero. For the first eight consecutive even ticks, this modular test certifies 64 of the 70 four-row minors. Repeating one of the eight selected offsets also breaks the full-minor check. A vanishing residue alone does not establish nonidentifiability.

## Stability and scope

Put $u=e^{i\theta}, v=e^{i\phi}$, $h=(\cos x,\sin x,\cos y,\sin y)$, and let the real row $R_k$ be $(\cos k\theta,-\sin k\theta,\cos k\phi,-\sin k\phi)$. Changing from the complex columns to this real basis is invertible. Let $s_4>0$ be the smallest singular value taken over all four-row matrices $R_I$, and $s_5>0$ the corresponding minimum over five-row matrices $[1,R_J]$. For any two phase vectors $h,g$, the difference of probabilities factors exactly as

$$
 p_k(h)-p_k(g)=\frac{4}{25}\bigl(1+R_k(h+g)\bigr)R_k(h-g).
$$

Take the five smallest absolute first factors. The norm of their vector is at least $s_5\|(1,h+g)\|_2\ge s_5$. At least four of the eight first factors consequently have magnitude at least $s_5/\sqrt5$. On those rows, one second factor has magnitude at least $s_4\|h-g\|_2/2$. In particular

$$
 \|h-g\|_2\le\frac{25\sqrt5}{2s_4s_5}\max_k|p_k(h)-p_k(g)|.
$$

This is a deterministic bound on phase-coordinate error when comparing two candidate traces. A confidence region from counts additionally needs a sampling model. Distinct coherent classical and quantum realizations have identical eight-coordinate records. The closure of the calibrated record is a two-torus: its phase orbit is dense, and the continuous measurement map is injective on a compact torus, hence a homeomorphism onto its image. This identifies a space of distinct predictions under the fixed dynamics and detector. It supplies neither independently controllable internal phases nor a derivation of space, time or the detector law.

Gakhar and Perea derive toroidal sliding-window embeddings for quasiperiodic signals. Gao, Sun, Wang and Xu study recovery from magnitudes of affine measurements. The eight offsets and exact finite-field certificate above specialize these ideas to this port and clock. [Gakhar and Perea](https://arxiv.org/abs/2103.04540) · [Gao et al.](https://arxiv.org/abs/1608.06117)
