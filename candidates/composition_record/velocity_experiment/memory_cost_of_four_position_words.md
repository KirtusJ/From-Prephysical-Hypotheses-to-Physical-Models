# Four position words bound the memory needed for rail recovery

Four pairs of position writes in the sixteen-site walk advance the particle to the same site while applying two independent rotations and their inverses to its rail. This forces a passive classical controller to use at least order $(\log N)^2$ working states to preserve any fixed excess over chance in a trusted four-state experiment at write $N$. The same bound holds for a fixed excess over Bell fidelity $1/2$. These are predictions under the ordinary probabilities of the ideal walk. [Twelve-tick block and exact site instrument](classical_positions_with_a_retained_qubit.md) · [Earlier one-angle memory bound](finite_memory_for_position_gates.md)

## Records, resources and scores

Each of the $N$ blocks ends in an exact position write that preserves its two local rails. Its displacement has input-independent probability and applies a specified real orthogonal gate. The stream of displacements is independent across blocks. The controller reads the successive positions and has at most $M$ classical working states at each write. Give it the present site and accumulated determinant sign for free. Its transition tables may depend on the absolute clock, prescribed horizon and independent shared randomness. The receiver may have the entire final working state, site and sign. It applies a trace-preserving recovery to the rail once, at the fixed deadline. Every launch counts. A running transcript, a history-dependent clock or a quantum memory would change these resources.

For the four-state score $A_N$, prepare one of $R,L,+,-$ uniformly at the origin. Keep the preparation private from the controller and the recovery. After recovery, measure in the matching trusted $Z$ or $X$ basis and score a correct sign. For $F_N$, prepare a Bell pair and keep the reference untouched, then score its final overlap with the initial pair. The entanglement-breaking ceilings are $3/4$ for the four-state test and $1/2$ for the Bell test. The $1/2$ appearing below for $A_N$ is the **chance** score. [Four-state calculations](check_four_state_alphabet.py) · [Bell recovery protocol](recovering_a_qubit_from_position_messages.md)

## Two independent rotation angles

Write $R(a,b)=\left(\begin{smallmatrix}a&-b\\b&a\end{smallmatrix}\right)$. Direct multiplication of the two block Kraus matrices, latest on the left, gives the following table. The signs are those of the original walk.

| Chronological displacements mod 16 | Signed Kraus matrix | Incident probability |
| --- | --- | --- |
| $0,2$ | $R(-8,-9)/64$ | $145/4096$ |
| $2,0$ | $R(-8,9)/64$ | $145/4096$ |
| $8,10$ | $R(8,-1)/64$ | $65/4096$ |
| $10,8$ | $R(8,1)/64$ | $65/4096$ |

All four words advance by two modulo 16, with positive determinant. The corresponding rotations up to overall sign are $B,B^{-1},T^{-1},T$, with $B=(8+9i)/\sqrt{145}$ and $T=(8+i)/\sqrt{65}$. No nonzero integer pair $(a,b)$ satisfies $B^aT^b=\pm1$. To prove it, square the putative relation and write

$$
r=B^2=(-17+144i)/145,\qquad t=T^2=(63+16i)/65 .
$$

If $a\ne0$, invert the full relation if necessary to make $a>0$. In $r^a t^b=1$ use $\bar t$ for negative powers of $t$, then clear denominators. Reduce Gaussian integers modulo 29 by $i\mapsto17$ (since $17^2\equiv-1$). The numerator of $r$ maps to 24 and both choices of numerator for $t$ remain nonzero because their product is $65^2$. The right side of the cleared equality is divisible by 29. This excludes $a\ne0$. If $b\ne0$, invert to make $b>0$ and clear denominators in $t^b=1$. Reduction modulo 5 by $i\mapsto3$ sends $63+16i$ to 1 and $65$ to zero.

After $k$ such pairs the exponent vectors are exactly $|a|+|b|\le k$, $a+b\equiv k\pmod2$. Each is realized by the required signed steps along the two axes and enough canceling pairs. The map $(a,b)\mapsto((k+a+b)/2,(k+a-b)/2)$ takes these vectors bijectively onto $\{0,\ldots,k\}^2$. There are therefore $(k+1)^2$ distinct projective angles with common displacement $2k\bmod16$ and unchanged determinant sign.

## The angular information a finite controller loses

Let $\theta$ be the first-column angle of the accumulated orthogonal rail matrix, modulo $\pi$, and let $s$ be its determinant sign. A left step with angle $\phi$ and sign $\sigma$ changes $s\theta$ to $s\theta+(\sigma s)\phi$. For each augmented state $i=(\text{working state},\text{site},s)$ propagate the complex harmonic $h_i=\mathbb E[\mathbf1_i e^{2is\theta}]$. From any starting state the harmonic transition row has absolute sum at most one, since each path contributes its probability times a unit-modulus factor.

Set $k=\lfloor\sqrt M\rfloor$ and choose one word for each of the $(k+1)^2>M$ directions above. Fix the clock, incoming state and independent random tape. Two words end in the same working state, site and sign. Denote their signed Gaussian products by $z,w$, taken from the table before division by $64^k$. Their probabilities are $|z|^2/4096^k$ and $|w|^2/4096^k$. Their harmonic coefficients in this row are $z^2/4096^k,w^2/4096^k$, or their simultaneous conjugates. At their common output the triangle inequality loses at least

$$
\frac{|z|^2+|w|^2-|z^2+w^2|}{4096^k}
=\frac{4\,\operatorname{Im}(z\bar w)^2}{
4096^k\big(|z|^2+|w|^2+|z^2+w^2|\big)}.
$$

The projective directions differ, so $\operatorname{Im}(z\bar w)$ is a nonzero integer. In fact it is divisible by 16. For any two individual letters their real parts are $\pm8$ and their imaginary parts odd, so the cross product of their integer columns is divisible by 16. The imaginary part of a product of Gaussian integers with imaginary parts divisible by 16 remains divisible by 16. Apply this to the $k$ paired factors of $z\bar w$. The parenthesized denominator is at most $4\cdot145^k$. Each $2k$-write transition row thus loses at least $\eta_k=256/(4096\cdot145)^k=256/593920^k$. Other words entering the same row cannot restore this loss, by the triangle inequality. The row estimate is uniform in the incoming state and clock. Composing consecutive blocks, using the single-write estimate on the remainder and then averaging over independent tapes, gives

$$
\sum_i |h_i| \le (1-\eta_k)^{\lfloor N/(2k)\rfloor}.
$$

For a receiver with the shared tape this inequality applies conditionally on each tape. A tape head or lookup key that records past input counts as working memory.

## Converting the loss to a testable score

In a disclosed determinant sector, a real orthogonal correction gives four-state survival $(1+\cos(2\theta-\lambda))/2$ for some chosen angle $\lambda$ when its planar action matches that sector. The opposite sector gives $1/2$. For any trace-preserving qubit channel the $XZ$ Bloch submatrix contracts the Euclidean norm, by applying the channel to pairs of antipodal pure states. The four equiprobable preparations cancel its affine translation. Every real $2\times2$ contraction is a convex combination of orthogonal matrices, by singular value decomposition and a mixture of diagonal sign matrices. All these orthogonal actions on $XZ$ are realized by real rail unitaries. Hence in a cell of mass $p_i$ the optimal incident score is $(p_i+|h_i|)/2$, attained by aligning the correction with its harmonic. For the Bell experiment the two eigenvalues in its corresponding Bell plane are $(p_i\pm|h_i|)/2$, and an inverse real unitary attains the larger. Any coarser terminal report can only reduce either optimum. Consequently

$$
\max(A_N,F_N) \le \frac12+\frac12(1-\eta_k)^{\lfloor N/(2k)\rfloor}.
$$

For either score to reach $1/2+\delta$ for a fixed $0<\delta<1/2$ requires $\lfloor N/(2k)\rfloor\le 593920^k\log(1/(2\delta))/256$. Along any sequence of successful horizons tending to infinity this implies

$$
\liminf_{N\to\infty}\frac{\sqrt{M_N}}{\log N}\ge\frac1{\log 593920}.
$$

Indeed if $k\le (1-\epsilon)\log N/\log 593920$ along a subsequence, the right side of the necessary floor inequality is $O(N^{1-\epsilon})$ whereas its left side is at least of order $N/\log N$. The bound counts **states**. In bits it requires at least $2\log_2\log N-O(1)$ bits. For comparison, rounding the angle on a grid already gives a construction with $O(\sqrt N)$ states. The optimum growth between these bounds is open. [Growing-memory construction](finite_memory_for_position_gates.md)

Run the [integer replay](check_memory_word_angles.py) with `python -I -B check_memory_word_angles.py`. It derives the four signed matrices from the twelve-tick walk, checks the two modular reductions, and verifies the direction counts and pairwise loss bounds through sixteen writes. The algebra proves the bounds at arbitrary horizons. No device outcomes enter the calculation.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex independently checked the argument and wrote the executable verification.
