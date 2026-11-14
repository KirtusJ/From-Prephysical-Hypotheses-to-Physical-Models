# Bounding source error with a binary return record

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Can the walk's records bound preparation asymmetry before its probability law is known? A single return can conceal a fixed source error behind a steep detector response. A circuit that increases the nonblank mass before reading it gives a finite test using only an ordering assumption on two detector ports. This assumes coherent control of the source and a detector that pools the two indicated outcomes. It gives a conditional preparation test. Its physical implementation and its operating rates remain open. [Single-return counterexample and five-slot source](A_random_permutation_echo_for_five_slots.md)

## A detector comparison at half the mass

Prepare five binary slots with a reversible unitary $U$ from a complete blank ray $|0\rangle$, including any inert reference. Draw a slot permutation $g$ independently of the preparation. The echo $W=U^\dagger S_gU$ has nonblank squared mass $\ell=1-|\langle0|W|0\rangle|^2$. Squared masses here describe unitary geometry. Recorded rates enter through a separate premise.

Coherently write a flag distinguishing blank from its entire complement. Keep the residual state in each flag sector. Immediately before detection, use a fresh independent fair bit to choose which of two physical ports represents nonblank, then decode the reported port using that bit. For each hidden type let $F(u)$ be the chance of the first port reporting when it holds total mass $u$ and the other holds $1-u$. The two ports exhaust the ideal reports. The function must be nondecreasing and common to the two assignments of the flag at that type. The curve may otherwise vary between trials and the ports may have unequal gains. This mass-only premise excludes a response to residual labels or to the routing bit itself.

If the nonblank sector has mass $s$, its decoded probability is
$$G(s)=\tfrac12\big[F(s)+1-F(1-s)\big].$$
Hence $G(s)\ge1/2$ for $s\ge1/2$, including equality at the midpoint. An arbitrary monotone curve may give almost no signal just below the midpoint. In an experiment with erasures of otherwise valid two-port reports, count every unresolved read as a possible nonblank. The resulting incident-launch rate upper-bounds the ideal decoded nonblank probability. Losses that change the physical measurement require their own model.

## Turning a small leakage into a port comparison

Set $P_0=|0\rangle\langle0|$, $P_1=I-P_0$, $z=e^{i\pi/3}$, and $D_j=I+(z-1)P_j$. Keep the sampled permutation fixed throughout the audit and apply its inverse on inverse calls. Starting with $V_0=W$, apply the fixed-point search word
$$V_{k+1}=V_kD_0V_k^\dagger D_1V_k.$$
All appearances of a preparation and its inverse in a given audit must use the same realization. If $v=V_k|0\rangle$ has blank mass $b$, the multiplier on its blank component is $1+(z-1)[b+z(1-b)]=-(z-1)^2 b$. Its modulus is $b$. The resulting blank mass is $b^3$, also at $b=0,1$. At depth $k$ it is $(1-\ell)^m$, where $m=3^k$. The circuit uses $m$ forward or inverse echo calls and $m-1$ selective phases. The depth is fixed before the audit, so the choice requires no knowledge of the leakage or the detector curve. [Grover's fixed-point search](https://doi.org/10.1103/PhysRevLett.95.150501)

Put $\delta_m=1-2^{-1/m}$. Whenever $\ell\ge\delta_m$, the final nonblank mass reaches at least one half. If $R$ upper-bounds the decoded nonblank rate across assigned audits, including unresolved reads as above, it follows that
$$\Pr(\ell\ge\delta_m)\le\min(1,2R),\qquad
\mathbb E\ell\le\delta_m+(1-\delta_m)\min(1,2R).$$
Hidden source and detector properties may be arbitrarily correlated. The assignments must preserve the intended launch mixture. A certified absolute error $\eta<1/2$ on the final blank mass replaces the threshold by $1-(1/2-\eta)^{1/m}$. Even a small unaccounted control error can move a borderline type across the midpoint.

For a uniform permutation of the five slots, write $x$ for the squared mass outside their symmetric subspace. The group bound gives $\mathbb E x\le(4/3)\mathbb E\ell$. Uniform even permutations alone give the same *mean kinematic leakage* needed in this bound. The corresponding raw amplified records may differ between samplers. For four uniformly selected adjacent swaps the multiplier is $4/(3\gamma)$, with $\gamma=(3-\sqrt5)/8$. For accepted labels a separate herald bound $h_t\le K Y_t$ and a positive measured pass rate $H$ give mean wrong-ray mass at most $K\mathbb E x/H$, capped at one. [Proofs and herald-bias counterexample](A_random_permutation_echo_for_five_slots.md)

At depth five, $m=243$ and $\delta_m<1/300$. A nonblank rate upper limit of $1/200$ gives $\mathbb E\ell<133/10000$ and, for uniform permutations, $\mathbb E x<133/7500$ (1.774%). For one prespecified audit design, 598 independent identically distributed binary audits with zero nonblank or unresolved reports would give that rate limit at one-sided 95% confidence, since $(199/200)^{598}<0.05$. The five slots in any one audit need not be independent. The example costs 145,314 forward or inverse echo calls over the 598 audits. These are design figures, with no observed launches.

## A phase-free preparation using more slots

Prepare $m$ coherent echo banks in a **product conditional on all launch variables**, with possibly different leakages $\ell_j$. Compute a single reversible flag for “at least one bank is nonblank” and perform the same pooled binary read once. The all-blank mass is $B=\prod_j(1-\ell_j)$. By the arithmetic–geometric mean inequality, $B>1/2$ implies $\bar\ell=m^{-1}\sum_j\ell_j<\delta_m$. The same upper bound holds for $\mathbb E\bar\ell$ with $R$ now measured per block. Uniform sampling of a bank within the block must reproduce the intended audit population. The hidden types may be correlated across banks. The construction trades matched sequential phases for $m$ simultaneous banks and one collective flag operation.

Two controls distinguish this experiment from cheaper alternatives. An entangled joint state $\sqrt{1-a}|0\cdots0\rangle+\sqrt a|1\cdots1\rangle$ has individual nonblank mass $a$ but all-blank mass $1-a$ at every bank count. Also, scoring fine modes before reading the pooled flag can defeat the half-mass comparison. Put half the mass on a single blank mode and distribute the other half equally over $d>1$ nonblank modes. Under a common power score $w^q$, the reported nonblank probability is $1/(1+d^{q-1})$, which tends to zero. A swap of the two output port labels preserves this failure if the detector continues to score the fine modes. Reading every bank separately and OR-ing the classical records also changes the observable.

The [exact computational controls](check_binary_echo.py) and [Lean algebra](lean/BinaryEcho.lean) accompany the [arithmetic record](results/binary_echo.json). The finite bounds use additional source controls and detector ordering. They leave open the emergence of the squared-norm probability law and the realization of those controls on a primitive walk.
