# Winding weights from one fixed position detector

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Prepare the balanced ring walk at well 0 on rail R. Let it propagate freely, then record a single bit indicating whether its final well lies in the fixed semicircle $W=\{0,\dots,D-1\}$ of the $2D$-well ring. Both rails contribute. Varying only the time between launch and detection identifies the fair-count fraction and all observable conjugate-pair weights in the finite character mixture below. The four-well case needs two more ticks than the rail-resolved comparison when the effective group has at least two elements. [Rail-resolved protocol](Fixed_ring_winding_weights.md) · [Director Z’s pure-character comparison with position masks, Propositions 1 and 2](../Director_Z/computation/Character_Separation/CRITERION.md)

## What the clock bound means

Take gains $(RR,RL,LR,LL)=(1,g,1,zg)$ in $C_2\times C_q$. Each coherent sector has $\chi(z)=-1$ and $\chi(g)=e^{2\pi i s/q}$. The fair sector assigns probability $2^{-t}$ to each length-$t$ word. Each launch uses the same mixture. Define $m=q/\gcd(D,q)$, $K=\lfloor m/2\rfloor$. Group the coherent weights by the effective phase $u_s=\chi(g)^D$, pairing inverse phases. The $K+1$ coherent masses and the fair mass sum to one. Within these premises, the smallest **maximum clock** over collections of final well measurements that identify all these masses is

| Number of wells | Optimal maximum clock | Detector attaining it |
|---|---:|---|
| $2D\ge6$ | $\max(3,KD+1)$ | The fixed semicircle $W$ |
| $2D=4$ | $2K+3$ | The fixed pair $\{0,1\}$ |
| $2D=2$ | No identifying clock | Well parity is deterministic at every tick |

Every rate is unconditional per original launch. There are no intermediate measurements or filters. The minimum concerns the full unknown mixture; a test between two specified pure sectors can finish earlier. Enlarging the ring’s group by labels that map to the same effective conjugate pair cannot distinguish those labels on this apparatus. These are conditional model probabilities, with the probability-law family, sharp preparation, coherence and detector registration all supplied.

## Why a single semicircle suffices on six or more wells

An amplitude at a terminal site and rail has real signed coefficients indexed by the left-step count $l$. Each $LL$ transition contributes a minus sign. At the observed well $x$ all possible $l$ are congruent modulo $D$ since $t-2l=x\pmod{2D}$. After removing a common phase, its coherent square is a linear combination of $\cos(h\arg u_s)$, where $hD$ is a left-count difference. Summing the two rail squares describes the well read exactly. For each rail, left counts belong to an interval of length $t-1$ ($0$ through $t-1$ for R, $1$ through $t$ for L).

At $t=kD+1$ a harmonic of degree $k$ can occur only twice. At $x=t\pmod{2D}$ the two extreme R words are $R^t$ and $L^{t-1}R$, giving signed product $\epsilon=(-1)^{kD-1}$. At $x=t-2\pmod{2D}$ the two extreme L words are $R^{t-1}L$ and $L^t$, giving $-\epsilon$. These wells are distinct for $D\ge2$. The pair is $1,-1$ for even $k$ and $D+1,D-1$ for odd $k$, modulo $2D$. The semicircle contains exactly one of each pair. Thus for known count weight, the original-launch rate, multiplied by $2^t$, gives a triangular linear system in the coherent cosine moments $J_k=\sum_s b_s\cos(k\arg u_s)$. Its new coefficient at $J_k$ is $2\epsilon$ or $-2\epsilon$.

At tick 3 on $D\ge4$, $W$ includes the two reachable positive displacements $1,3$. The coherent and counting probabilities are $6/8$ and $4/8$. For $D=3$ the two extreme displacements coalesce outside $W$, leaving $5/8$ and $3/8$ inside. Both comparisons determine the counting mass. The remaining zero-lag moment is total coherent mass. The first $K$ further moments invert the folded cosine transform on $C_m$. If $m=1$ there are no further moments. These results lower no requirement on reset or clock stability.

The time bound is sharp even for a detector that reports the entire well. Through tick $KD$ only degrees $0,\ldots,K-1$ are accessible when $K\ge1$. Two different unit populations on effective labels $v$ with masses $(1\pm\cos(2\pi Kv/m))/m$ agree on these moments by finite Fourier orthogonality. When $m=1$, every occupied oriented port through tick 2 has at most one word for $D\ge2$, so counting and coherent probabilities agree. A detector covering every even well yields only deterministic parity at every size. Coarse registration must preserve the boundary between the two extreme-harmonic wells for the semicircle argument.

## Four wells and the missing count comparison

At each tick there are only two reachable wells. Let $X_t=2P_t(t\bmod4)-1$. The outcome of $W=\{0,1\}$ determines this bias with a clock-dependent sign. Fair counting gives $X_t=0$ at every $t\ge1$. For a coherent phase $w=\chi(g)$, put $h=\operatorname{Re}(w^2)$ and $a=(1-h)/2$. Then

$$
X_{2j+2}=X_{2j+1},\qquad
\sum_{j\ge0}X_{2j+1}x^j
=\frac{-x[(1-a)+ax+x^2]}{(1+x^2)^2+a x(1-x)^2}. \tag{1}
$$

To derive (1), separate the two wells by even and odd left count. In the two-component rail space use $A=\mathrm{diag}(1,w)H$, $B=\mathrm{diag}(1,-w)H$ and the real Hadamard coin $H$. The two well amplitudes are $(A^tR\pm B^tR)/2$. Hence $X_t=\operatorname{Re}\langle B^tR,A^tR\rangle$. For $T=\overline B\otimes A$ set $s=(w-\bar w)/2$, so $s^2=-a$. Direct multiplication gives $\det T=1$, $\operatorname{tr}T=-s$, $\operatorname{tr}(T^{-1})=s$, $\operatorname{tr}(T^2)=s^2$. The characteristic polynomial is $\lambda^4+s\lambda^3-s\lambda+1$. Multiplying by its conjugate gives $(\lambda^4+1)^2+a\lambda^2(\lambda^2-1)^2$. Both parity subsequences of the real bias therefore have the recurrence with generating denominator $G(x)=(1+x^2)^2+a x(1-x)^2$. Applying $A,B$ at the first eight ticks gives identical odd/even pairs with entries $0,a-1,-a^2,-1+a^3+2(1-a)^2$. Multiplication by $G$ gives the displayed numerator. All generating series below are formal power series.

A signed unit-mass functional $L$ on polynomials in $h$ can be defined uniquely by $L(1)=1$ and $L(X_{2k+1})=0$ for all $k\ge1$. The extreme-word pivot above makes each $X_{2k+1}$ a polynomial of exact degree $k$ in $h$. This functional describes what the coherent moments would have to be to reproduce the fair transcript. Applying it to (1) and writing $y=x(1-x)^2/(1+x^2)^2$ yields

$$
F(y)=L[(1+ay)^{-1}]=\frac{1+x^2}{1+x}
=1-y\frac{(1+x^2)^2}{1-x^2}.
$$

Indeed the vanishing numerator gives $(1+x^2)F=(1-x)(1-F)/y$. The formal inverse $x(y)$ solves $x=y(1+x^2)^2/(1-x)^2$, and has strictly positive coefficients in every positive degree by the recursion. Consequently $L(a)=1$, $L(a^2)=0$, and $(-1)^j L(a^j)<0$ for every $j\ge3$. Expand the Chebyshev polynomial as $T_k(1-2a)=1+\sum_{j=1}^k(-1)^j c_{kj}a^j$, with $c_{kj}=4^j k(k+j-1)!/[(2j)!(k-j)!]$ (equivalently, expand the Chebyshev recurrence). Each positive coefficient increases with $k$ at fixed $j$, and $c_{k1}=2k^2$. Hence $u_k=L(T_k(h))$ strictly decreases. Its first values are $1,-1,-7,-113,-2335$. Signs and cancellation here concern a signed functional. They place no positivity requirement on a hypothetical affine dependence between experimental rates.

Effective phases obey $T_{K+1}(h)=T_{|m-K-1|}(h)$, where $|m-K-1|\le K$ for $m\ge1$. The strict inequality of the corresponding $u$ values excludes any signed unit-mass coherent ensemble matching fair through $k=K+1$. The coherent response columns are affinely independent by the triangular pivots through $k=K$ and the finite cosine transform. Thus the fair column adds an independent mixture coordinate, and the odd clocks $3,5,\ldots,2K+3$ identify all masses. Before that last clock at most $K$ informative binary frequencies exist by (1), whereas the mixture simplex has affine dimension $K+1$. Distinct positive mixtures then give identical reads by perturbing an interior point in a null direction. This proves the four-well optimum also for the collapsed order $m=1$.

## A two-frequency cubic experiment

For $D=2,q=3$ use the same physical pair of wells $W=\{0,1\}$ in both runs. Only well 1 of the pair is reachable at the chosen odd clocks.

| Clock | Trivial winding | Unit winding or conjugate | Fair count |
|---|---:|---:|---:|
| 3 | $1$ | $5/8$ | $1/2$ |
| 5 | $1/2$ | $7/32$ | $1/2$ |

If $p_3,p_5$ are the two original-launch frequencies, the folded unit weight is $b=(16-32p_5)/9$, the trivial weight is $(8p_3-4-b)/4$ and the rest is count. If both rates have absolute error at most $e$, the error bounds are $32e/9$ for the unit weight, $26e/9$ for the trivial weight and $14e/3$ for count (substitute the same two errors before bounding). At this fixed size the pure trivial and unit responses differ by $3/8$ on the first clock. The general optimal-clock theorem establishes exact identifiability and supplies no uniform conditioning bound in $D$ or $q$.

Run `python -B Director_G/check_position_only_winding.py NEW_DIRECTORY` from the repository root. The checker compares both rail contributions against unsigned physical arc propagation, exhausts rank changes in clock order, checks the four-well generating identity on exact rational nodes, and records failing earlier clocks and blind group aliases. The nested challenger derived the four-well kernel and strict monotonicity argument after an initial numerator failed the $h=-1$ endpoint. Independent checks use signed path runs and direct physical arcs. [Checker](check_position_only_winding.py) · [All finite records](results/position_only_winding.json)
