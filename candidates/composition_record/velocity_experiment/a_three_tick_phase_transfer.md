# Transferring a relative phase in three ticks of a walk

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex developed the construction and its exact checks.

A site that stays dark when two returning paths use opposite swaps gives a phase reference for a subsequent Hadamard comparison. The same two outer splitters serve both settings. Their splitting ratio and individual entry phases cancel from a ratio of two measured site probabilities. This is a proposed circuit with calculated predictions. No physical counts are available here.

## Paths on the ring

Launch a right-going rail $R$ at site 0 of an eight-site ring. In each tick apply the coin and then translate $R$ by $+1$ and $L$ by $-1$. Write position only after tick 3. An instrument that stores the left-step count $y$ modulo four reads $x=3-2y\bmod 8$ at this clock. Codes 1, 2 and 3 therefore mean physical sites $+1,-1,-3$.

At tick 1 apply a uniform full-support unitary $U=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)$ in the ordered basis $(R,L)$. At tick 3 use $U^{\mathsf T}$ uniformly in the same rail-phase convention. Uniform overall phases on either use cancel from all predictions. A symmetric splitter can be reused without changing its entries. A real orthogonal splitter can use its inverse. A generic complex splitter requires the **transpose** relation between its two physical uses.

After the first shift the amplitudes are $a$ at $(+1,R)$ and $c$ at $(-1,L)$. Tick 2 applies $X$ at $+1$ and a selected payload at $-1$. Let $\eta$ be a complex phase of unit modulus associated with the addressed path. For science use $\sigma\eta H$ with $\sigma=\pm1$ and $H=(Z+X)/\sqrt2$. After the second shift the nonzero rails are $a$ at $(0,L)$, $\sigma\eta c/\sqrt2$ at $(0,R)$ and $-\sigma\eta c/\sqrt2$ at $(-2,L)$. The third coin and shift give the following complete amplitudes.

| Physical site | Rail | Amplitude |
| --- | --- | --- |
| $+1$ | $R$ | $ac(1+\sigma\eta/\sqrt2)$ |
| $-1$ | $L$ | $ad+\sigma\eta bc/\sqrt2$ |
| $-1$ | $R$ | $-\sigma\eta c^2/\sqrt2$ |
| $-3$ | $L$ | $-\sigma\eta cd/\sqrt2$ |

Write $p_j$ for the squared-norm mass at **code** $j$. Unitarity gives $|a|=|d|$. The two single-rail sites satisfy

$$
p_3=\tfrac12|ac|^2,\qquad
\frac{p_1}{p_3}=3+2\sqrt2\,\sigma\operatorname{Re}\eta.
$$

For the calibration setting replace the addressed payload by $-\eta X$. Both paths now return to site 0 at tick 2. At the terminal sites the sole amplitudes are $ac(1-\eta)$ at $(+1,R)$ and $ad-\eta bc$ at $(-1,L)$. At $\eta=1$ the first site is dark and the second amplitude is $\det U$. This equality uses the complex gain product $ac$ on both interfering paths. For example, if $U=\operatorname{diag}(1,i)(3Z+4X)/5$ and the last coin instead uses $U^\dagger$, the calibration mass at $+1$ is $4|ac|^2$ at $\eta=1$.

## What the two settings determine

With a common phase across settings, an exact zero calibration probability forces $\eta=1$. The conclusion survives launch-to-launch changes of $U$ and $\eta$ when $|ac|>0$ almost surely, the recorder assigns positive probability to every occupied cell, and the setting choice samples the same underlying launch population. A nonnegative reported probability can average to zero only by vanishing almost surely. A finite run with no recorded clicks gives an upper confidence limit on their frequency. Turning that limit into a phase bound requires sensitivity information. In particular an arbitrarily weak splitter can conceal a phase error.

At the calibrated phase the two science ratios are $3+2\sqrt2$ and $3-2\sqrt2$, on opposite sides of one. For a fixed sign, any common strictly increasing cell response preserves the predicted ordering of codes 1 and 3, including normalized powers $q>0$ redrawn per launch. Both cells carry one physical rail, so this comparison applies when normalization uses whole sites or when it uses resolved rails subsequently pooled by site. Site-specific detection gains would require their own calibration. A positive common gain preserves the ordering. Contrasts can approach zero as $q\downarrow0$ or $|ac|\downarrow0$. Uniform-on-support and maximum-only responses can erase a strict ordering. More generally, both signs still give their respective orderings at a fixed phase whenever $\operatorname{Re}\eta>1/\sqrt2$.

With ordinary squared-norm reporting the calibration yields more than a zero test. Let $P_1,P_3$ be science probabilities and $\kappa$ the calibration probability of code 1. For fixed $\sigma$, random matching settings and an arbitrary common law of $(U,\eta)$,

$$
P_1-3P_3=\sigma\sqrt2\,(2P_3-\kappa/2).
$$

This follows from $|1-\eta|^2=2-2\operatorname{Re}\eta$. With $\eta=1$ and ordinary reporting, the science ratio likewise gives the $|ac|^2$-weighted mean sign. A fixed splitter, or independence of splitter strength and sign, makes this the population mean sign.

The minus sign of the addressed calibration swap relative to the other swap is a physical premise. The payload change must preserve the addressed path phase. A device with $\eta_X=1$ and $\eta_H=-1$ gives a perfect dark calibration while reversing every science sign. Likewise, changing the real embedding $\sqrt2\mapsto-\sqrt2$ and simultaneously reversing the relative physical phase on every addressed use of $H$ leaves the realized operators unchanged. Finite adaptive sequences made of those same preparations, coins and reads give identical records by composition. Coherently bypassing an operation requires a specified phase for the occupied and bypassed arms. Earlier work identifies this issue for controlled unknown operations, synchronized native preparations and rational bypass gates. [Araújo, Feix, Costa and Brukner](https://arxiv.org/abs/1309.7976) · [Native preparations](../../../Director_G/Native_preparations_and_probability_embeddings.md) · [Rational references and optical bypass](../../../Director_G/Rational_references_and_optical_bypass.md)

## A mixed-sign population that exactly reproduces the ordinary table

Take the real symmetric rational splitter $U=(3Z+4X)/5$ and $\eta=1$. The ordinary whole-site row in code order $(1,2,3)$ is

$$
O_\sigma=\frac1{625}(216+144\sigma\sqrt2,\ 337-144\sigma\sqrt2,\ 72).
$$

The following population reproduces every science and calibration **site** count probability of $O_+$. Choose a minus-sign launch with probability $v$ and independently draw the power from $\{1/2,2\}$. For a probability row $O$, write $E_q(O)_j=O_j^q/\sum_i O_i^q$. Define $L(v)=(1-v)E_{1/2}(O_+)+vE_{1/2}(O_-)$ and $D(v)$ by the same formula using power 2. Put $T=O_+$. Throughout $0\le v\le1/20$ the strict inequality $D_3(v)<T_3<L_3(v)$ follows by affinity from the two endpoints. Choose the half-power probability

$$
w(v)=\frac{T_3-D_3(v)}{L_3(v)-D_3(v)}.
$$

This matches code 3 exactly. The continuous code-1 residual $w(v)L_1(v)+(1-w(v))D_1(v)-T_1$ lies strictly between 0.028 and 0.030 at $v=0$ and between $-0.003$ and $-0.002$ at $v=1/20$. The checker verifies these open intervals by outward rational bounds on square roots. There is therefore an interior $v$ matching code 1 as well. Normalization fixes code 2. The dark calibration has a single occupied site under either power. Hence this two-setting experiment separates the two *pure fixed-sign* hypotheses with any common strictly increasing response, while allowing an exactly matching population with both signs, even with independence between sign and exponent. This construction uses whole-site scoring and does not establish equality of rail-resolved tables. The longer existing record test uses a different panel and a fixed relative gate phase. [Nine-tick embedding test](selecting_the_real_embedding.md) · [Addressed walk](addressed_embedding.md) · [Two-address echoes](two_address_echoes.md)

The Python replay enumerates all three-tick rail paths on the physical ring for three exact complex-integer matrix representatives and certifies the two interpolation signs. Run from this directory. [Replay source](check_three_tick_phase_transfer.py)

~~~sh
python -I -B -O check_three_tick_phase_transfer.py
~~~
