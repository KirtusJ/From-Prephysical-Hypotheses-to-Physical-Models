# Reading the herald and testing its probability rule on the same launch

A walk can leave a protected record unset until an experiment chooses how to read it. The [previous stopped walk](records_with_a_heralded_reference.md) admits an exact rival if the gate’s success is scored separately from its position. Here three reference outcomes accompany the actual two outcomes of interest. Their frequencies test the probability rule on that very read, even when the returning state is unknown, the exponent depends on the state, and inverse powers or extreme selectors are allowed.

## One pointer with five labels

Let $W$ be the six-qubit coherent four-path filter. Its four logical input coordinates may be in an arbitrary state and entangled with a spectator. Its other four qubits start at zero. Denote the projector onto that input subspace by $B$ and the good path/clear-flag projector by $\Pi$ (the Pell selector stays unresolved). On the input subspace the exact identity is $BW^\dagger\Pi WB=sB$ with $s=5/16$. The protected release cut is immediately after $W$. Neither the selector nor the path and rejection bits have been written there. [Filter, signed paths and six-qubit circuit](a_phase_reference_from_synchronized_walks.md)

At the cut choose the target operation. For a **return**, undo $W$ and test the four zero ancillas, leaving the unknown logical input alone. For a **direct read**, test $\Pi$ itself. These effects define a kinematic mass $w$ and its complement $1-w$. For the return $w=\operatorname{tr}[(WBW^\dagger\otimes I_E)\rho]$, allowing an arbitrary prior joint state $\rho$ and inaccessible or accessible side systems $E$. For the intended prepared state the return mass is one and the direct success mass is $5/16$. A third choice changes the herald coherently, as described [in the amplification experiment](changing_a_herald_before_it_is_written.md).

Prepare three fresh balanced bits coherently. Four of their eight equal paths label the high reference H, two label M and one labels L. On the eighth path label the target result P or F. These are five mutually exclusive projectors, four or five of which may be occupied. Only the final pointer label is read. Equivalently apply the chosen operation to every path, leave its inverse output unmeasured, compute the five-valued label reversibly and read the label once. This comparator uses signed permutations, balanced splits and the specified coarse pointer. Its unnormalized cell masses are

$$
(4,\ 2,\ 1,\ w,\ 1-w).
$$

A reader draws one $q$ for that launch and applies the same power to all five masses, pooling each cell’s internal paths before normalization. The distribution of $q$ may depend on $w$, the test and the prior history. Zero power is uniform on occupied cells. Negative powers act on the same support. At $\pm\infty$ the reader may choose among tied extrema in any way. Dark cells receive zero probability. Without a specified physical grouping these hypotheses need not hold.

## What the three reference counts establish

Write $h,m,l$ for the **reported probabilities** of the three reference outcomes in a mode. Give the outcomes H, M, L, P, F scores $1,-4,4,0,0$. For finite $q$ put $x=2^q$ and let $V$ be the sum of powers of the positive target cells. With $Z=x^2+x+1+V$,

$$
R=h-4m+4l=\frac{(x-2)^2}{Z}\ge0.
$$

It vanishes exactly at $q=1$. The positive infinity selector assigns H unit probability, so scores one. At negative infinity both H and M have zero probability, so $R=4l\ge0$. If the two **population** measurements give $E R=0$ and $E h=1/2$, the only finite modes left use $q=1$. Each of them has $h=1/2$ for every $w$. The remaining possible negative infinity modes have $h=0$, hence they also have zero incidence. This proves $q=1$ almost surely on this read. It uses all launches, including those on which the target has either a dark or a near-dark cell. The scalar square is the geometric-progression form of the earlier sibling test. [Earlier translated masks and resolved-port contrast](../return_memory/translated_mask.md) · [Lean 4.19 scalar certificate](../../../Director_G/lean/HeraldAuditResolution.lean)

On a return, the measured failure rate is then exactly $E[1-w]/8$. A zero population failure rate puts the entire state in the prepared subspace almost surely. This conclusion allows correlations between $q$, $w$ and hidden state. In that subspace every joint state with a spectator can be written as $W\rho_0 W^\dagger$, with $\rho_0$ supported on $B$ and identity action on the spectator understood. Reading $\Pi$ yields unnormalized spectator state $s\rho_E$ on success and $(1-s)\rho_E$ on failure, by $BW^\dagger\Pi WB=sB$. Thus the genuine binary herald is independent of previously held spectator information. The logical input inside that subspace can still differ between launches. For a general $w$, projection onto the subspace and purification give trace distance at most $\sqrt{1-w}$ to a state in it. Contractivity and the triangle inequality give a bound $2\sqrt{1-w}$ on the measured flag–spectator distance from the known binary law times the actual spectator marginal. This last statement uses ordinary quantum trace distance for a specified physical measurement. [Fuchs and van de Graaf](https://arxiv.org/abs/quant-ph/9712042)

On a direct read, the same three reference counts test $q$ independently of the return setting. A correct return on matched cut states then predicts the five direct rates $(1/2,1/4,1/8,5/128,11/128)$. Alternatively one may test any specified binary grouping of the subsequent position record on the target path. The theorem selects the power of the final five-cell read in each tested setting. It cannot transfer that result to an earlier two-cell writer merely because both report the same success bit.

## Finite error and incidence

Here is one bound that still works when a few targets have arbitrarily small bright masses. Bars denote population means. Fix a tolerance $0<\eta<1$, put $x_\pm=2^{1\pm\eta}$ and $h_- =x_-^2/(x_-^2+x_-+2)$. Then

$$
\begin{aligned}
\Pr(q\ge1+\eta)&\le\frac{2\bar R}{(1-2/x_+)^2},\\
\Pr(q\le1-\eta)&\le
\frac{1/2-\bar h+\sqrt{\bar R/2}}{1/2-h_-}.
\end{aligned}
$$

For $q\in[0,1]$ one has $V\ge1$, including a dark target. Thus $h\le x^2/(x^2+x+2)\le1/2$. For $q<0$ H has the smallest weighted probability among at least four occupied cells, hence $h\le1/4$. For $q\ge1$, $V\le1$ and $h\ge1/2$, while convexity gives $V\ge 2/x$. Substitution yields $2h-1\le1-2/x$ since $x^3-x^2-x-2=(x-2)(x^2+x+1)$. Consequently $(h-1/2)_+\le\sqrt{R/2}$ and above $1+\eta$ one has $R\ge(1-2/x_+)^2/2$. The extreme selectors respect the respective inequalities. Taking expectations, subtracting the measured $\bar h$ and applying Cauchy–Schwarz proves the displayed bounds.

Let $b_\eta$ be a valid upper bound on the combined tail incidence. On the remaining modes the probability of F is at least $(1-w)^{1+\eta}/D_\eta$, with $D_\eta=x_+^2+x_++3$. Jensen’s inequality gives

$$
E(1-w)\ \le\ b_\eta+(D_\eta\,\overline{\Pr(F)})^{1/(1+\eta)} .
$$

For a fixed number $N$ of independent comparable launches, insert a jointly valid upper limit for $\bar R$, a lower limit for $\bar h$ and an upper limit for $\overline{\Pr(F)}$. One elementary choice uses $\epsilon=\sqrt{\log(3/\alpha)/(2N)}$ and respective allowances $8\epsilon,\epsilon,\epsilon$. Treat a missing or ambiguous label conservatively as score 4 for the upper score bound, zero for lower H and one for upper F. Include known reporting errors separately. A negative upper limit for a nonnegative model mean challenges the assumed instrument on the confidence event. These are conservative bounds, not measured rates. [Hoeffding’s bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830)

## Can an earlier record imitate all five rates?

Yes, if the final grouping is also changed. Make a complete early good/bad copy, then return using $W^\dagger$ on the six protected qubits alone. With an ordinary early copy and otherwise ideal gates the return mass is $w=s^2+(1-s)^2=73/128$, which is greater than one half. A nested reader can choose the three reference labels or the remaining path with probabilities $4:2:1:1$, then on the remaining path apply a maximum selector to pass versus fail. Every target pass is reported. Its five returned frequencies are exactly $(1/2,1/4,1/8,1/8,0)$ despite the retained copy. Even the reference selection can be generated by a sequence of singly read fair bits. Thus the single physical five-cell read is the consequential assumption.

An audit choice must be fresh at the cut for conclusions about the science population. An instrument could protect the cut until that choice and introduce a separate binary herald **after** it learns the science setting. On the earlier stopped walk its mixture of powers zero and two can reproduce the entire ordinary science table. Putting the references on science launches tests the final scoring on those launches. Identifying every earlier, unexposed subcomparison requires further physical information.

The [matrix and outcome checker](check_anchored_herald.py) compares the direct, coherent-return and hidden-copy cases. [An order-only return test](how_a_hidden_herald_changes_the_return.md) gives a different guarantee when each unknown common response is monotone and need not be a power. No hardware counts enter these predictions.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the measurement design, conditional proof and controls.
