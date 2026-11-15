# Detecting a hidden herald with a return to the input subspace

Can a copy of a gate’s success flag be detected when the final reader preserves only the ordering of probabilities, possibly in reverse? A six-outcome read gives a sharp lower bound on detected failures for a completely distinguishable flag. A weak copy can escape it. Varying the number of readout cells after the gate gives a bound on the size of that escape. These are predictions for a proposed walk experiment. [Heralded gate](a_phase_reference_from_synchronized_walks.md) · [Five-cell test for the narrower power family](reading_a_herald_with_three_references.md)

## What an early flag does to the inverse

The filter $W$ acts on four zero ancillas and two logical qubits. Let $V$ be its restriction to that input, $P=VV^\dagger$ the prepared output subspace and $\Pi$ the good sector at release. The gate has input-independent success $V^\dagger\Pi V=sI$, with $s=5/16$. Undoing $W$ on its six qubits and testing its four original ancillas has return mass $w=\operatorname{tr}(P\rho)$, where $\rho$ is their state at release. The inverse has no access to an outside copy.

If an outside record perfectly distinguishes the two sectors, tracing out that record leaves $\rho$ block diagonal in $\Pi,I-\Pi$. The restricted positive operator $\Pi P\Pi=(\Pi V)(\Pi V)^\dagger$ has norm $s$ since $(\Pi V)^\dagger(\Pi V)=sI$. The other block similarly has norm $1-s$. Thus $w\le11/16$, even if the sector populations have changed. A normalized projection of a prepared input into the bad sector attains that bound. Simply copying the flag and leaving both sectors intact gives the more specific return $w=s^2+(1-s)^2=73/128$. The undisturbed input gives $w=1$.

## Six cells suffice to detect a complete copy

Use two fresh fair bits to route a quarter of the returned test’s failures to the pass group. The total pass mass becomes $u=1/4+3w/4$. Divide this group among four equal pass labels. Divide the remaining failure mass among two labels in the ratio $1:15$. Uncompute or leave unmeasured the intermediate routing information and read one terminal label. The six unnormalized path counts are pooled into physical cells *before* applying the unknown response. The masses per launch are

$$
\underbrace{u/4,\ u/4,\ u/4,\ u/4}_{\text{pass}},\qquad (1-u)/16,\quad 15(1-u)/16 .
$$

In each mode, assign each occupied cell the same nonnegative monotone function of its own mass and normalize the resulting nonzero total. Equal masses receive equal weight. Both monotone directions are allowed and can vary with hidden state or setting. Dark outcomes remain dark. A selector of the largest or smallest *raw* positive mass can also choose arbitrarily among tied extrema.

For a complete copy $1/4\le u\le49/64$. The smaller failure is strictly below a pass cell and the larger failure strictly above it. At least one failure receives at least the weight of each pass cell for either direction. The probability of reporting a failure is therefore **at least $1/5$**. A step response retaining exactly the four pass cells and the larger failure attains it. Both extreme selectors necessarily report a failure.

For the special response proportional to a common power $q$, define $x=(1-u)/(4u)$. Failure odds against the four pass cells are $[x^q+(15x)^q]/4$. For $q\ge0$ the minimum at fixed exponent occurs at $x=15/196$. For $q\le0$ it occurs at $x=3/4$. Minimizing at each endpoint gives a global minimum between $0.234157974$ and $0.234157977$. The checker verifies the interval by rational inequalities and independently reconstructs both sector norms. Applying the common response to the binary pass group first can defeat the entire test. For instance, the undisturbed-sector copy gives $u=347/512>1/2$, so a binary maximum selector always passes and can then choose the four pass labels uniformly. [Exact six-cell replay](check_hidden_herald_return.py)

## An imperfect copy can imitate a private flag

Couple the good and bad sectors to two normalized marker states of real overlap $c$. On a prepared input the return becomes $w=s^2+(1-s)^2+2s(1-s)c$. At $c=1/2$ this gives $w=201/256$ and $u=859/1024$. The two distinct marker states carry flag information. Yet every pass cell is larger than either failure, so a single common maximum selector choosing uniformly among the four maxima reproduces the private-flag table exactly. In fact this construction works whenever $w>41/57$, and a favorable tie choice also works at equality. A nondecreasing step response can suppress both failures when there is strict separation. Zero observed failures at this fixed resolution therefore cannot certify privacy against all partial copies.

## Choosing resolution after the cut

Keep the quarter bypass. Choose $m=2^k$ pass labels, $k\ge2$, and make the two failure masses $(1-u)/(4m)$ and $(1-1/(4m))(1-u)$. Each pass cell has mass $u/m$. Fresh fair routing bits suffice at any fixed $k$. For the following probability bound, the choice of $k$ must be independent of the state at release. The reader may learn $k$ and choose its monotone response afterwards.

Put $d=1-w$, so $1-u=3d/4$. For $d>0$ the smaller failure is strictly below each pass cell since $(1-u)/4<u$. The larger one is strictly above each pass cell precisely when

$$
(m+3/4)(1-u)>1,\qquad\text{equivalently}\qquad (4m+3)3d>16 .
$$

At such a resolution at least $1/(m+1)$ of all launches with that state report failure. Let a geometric menu assign probability $2/m$ to each dyadic $m\ge4$. These probabilities sum to one, the mean $k$ is three and the distribution has no finite maximum resolution. For any $d>0$, take the first dyadic satisfying the strict crossing. If it is four then $md\le4$. Otherwise the preceding dyadic $m/2$ failed to cross, giving $md\le8/3-3d/2<4$. In both cases $(m+1)d\le5$. The incidence of reported failures, including the chance of drawing this one resolution, is at least

$$
\frac{2}{m(m+1)}\ \ge\ \frac{d^2}{10}.
$$

For a population the failure rate $e$ thus bounds $E[(1-w)^2]\le10e$. This establishes ideal return at population zero under this hypothetical unbounded menu. It does not identify the reader's scoring function. The [Lean 4.19 certificate](../../../Director_G/lean/HeraldAuditResolution.lean) checks the crossing and cleared-denominator bound for rational defects. It also constructs the least dyadic satisfying the sufficient condition $md\ge2$. The inequalities above give the direct argument for real $d$.

**A finite instrument.** Set a maximum $M=2^K$, $K\ge2$, and assign all probability beyond $M$ to $M$. Each retained setting still has probability at least $2/m$. Define $d_M=16/[3(4M+3)]$. For $d>d_M$ a crossing occurs by $M$, so the previous proof applies unchanged. For $d\le d_M$ the pass cells are maximal at every offered resolution, allowing a maximum selector to reproduce the ordinary undisturbed pass row throughout, including the boundary tie. Consequently

$$
E[(1-w)^2\,{\bf1}_{1-w>d_M}]\le10e,\qquad
E[1-w]\le \sqrt{d_M^2+10e}.
$$

This identifies the blind interval of that finite menu explicitly. The mean $k$ of the idealized menu concerns binary label width. The required number of distinguishable labels at a given resolution is $2^k+2$, and the uncapped mean label count diverges. For independent comparable launches use an upper confidence limit for $e$, retaining missing outcomes as possible failures. With zero failures or missing labels in $N$ independent identically distributed launches, the one-sided level $1-\alpha$ binomial limit is $1-\alpha^{1/N}$. A new record made after the return/science choice, a separately scored earlier flag, a reporter that weights the labels individually or an environment that can undo its own copy falls outside this readout guarantee. [Stopped science tree and its binary rival](records_with_a_heralded_reference.md)

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, retains scholarly responsibility. OpenAI Codex developed the order bounds and counterexamples.
