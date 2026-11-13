# Reduced-State Sufficiency and Finite-Memory Controls

*Selected sections of an unpublished mathematical note.*

**Original date:** 2026-11-09.  
**Research direction:** Kirtus Justus.  
**Mathematical and editorial assistance:** ChatGPT (OpenAI).

The selected statements, assumptions, arguments, and examples below are drawn from the original note. This editorial excerpt does not claim independent verification. Numerical results are source-reported unless established by the reproduced argument; cited literature is identified from the original note. Original section numbering is retained.


## 3. When does a reduced state support an autonomous process?

Fix finite nonempty sets $X,Z$, a surjection $q:X\to Z$, a specified action set $\mathcal A$, and transition matrices $P_a$ on $X$. The full process is assumed controlled Markov: conditional on the present full state and chosen action, its next-state law is $P_a$. Actions may be chosen by one common policy based on the observed history and private randomization, not on a hidden state unavailable to the reduced model.

Define the next-observation row
\[
M_a(x,z')=\sum_{y:q(y)=z'}P_a(x,y).
\]

**Exact reduction criterion.** There exist kernels $Q_a$ on $Z$ reproducing every finite observed history, for every initial full-state law and every such policy, if and only if
\[
q(x)=q(x')\quad\Longrightarrow\quad M_a(x,\cdot)=M_a(x',\cdot)
\tag{1}
\]
for all actions and all states in the same fiber. When they exist, $Q_a$ are unique on the image of $q$.

**Necessity.** Start from either point mass $x$ or $x'$ in one fiber and perform the same action. Both reduced initial states are $q(x)$. A single reduced next-step law cannot reproduce two different $M_a$ rows.

**Sufficiency.** Set $Q_a(z,\cdot)$ to the common row in the fiber. At an arbitrary observed history, the posterior full state is a probability mixture over that fiber. Every member has the same next-observation row, so the mixture has row $Q_a(z,\cdot)$. This is unchanged by a common observation-based randomized action policy. Induction gives every finite joint history. QED.

This is the standard finite strong-lumpability criterion, applied action by action; it is not a new general theorem (Wolfer and Watanabe, 2024; Buchholz, 1994). It is a more discriminating test than requiring every possible reduction to commute with every possible operation. A reduction can be valid for one chosen action family and invalid for another. Only reachable/preparable states need be included when the scientific contract explicitly restricts them. For one specially fixed initial preparation, weaker forms of reduction can exist; they do not imply the all-initial-law condition above.

The criterion itself requires a mathematical transition model or sufficiently rich preparation evidence. A fit to stationary pairs alone does not verify it.

## 4. Exact stationary counterexample to pair-level process certification

Let the full states be $00,01,10,11$ and let the observation retain only the final bit. Take
\[
P=\begin{pmatrix}
3/4&1/4&0&0\\
0&0&1/4&3/4\\
1/4&3/4&0&0\\
0&0&3/4&1/4
\end{pmatrix}.
\tag{2}
\]
The uniform full-state law is stationary, since the matrix is doubly stochastic. Every binary output word has positive probability. The full-state process is irreducible and aperiodic: any two-bit state is reachable by appending its two bits, all append choices have positive probability, and state 00 has a positive self-loop.

At stationarity, each observed bit is fair and every adjacent observed pair has probability $1/4$. Therefore the fitted one-step matrix on observations is
\[
\widehat Q=\begin{pmatrix}1/2&1/2\\1/2&1/2\end{pmatrix},
\]
exactly the matrix of independent fair bits. Matrix multiplication of this fitted model is perfectly associative. That algebraic fact does not make it the actual reduced process.

The triples are instead
\[
\Pr(Y_0=a,Y_1=b,Y_2=c)
=\frac18\left[1+\frac12(-1)^{a+b+c}\right].
\tag{3}
\]
Even-parity words have probability $3/16$, odd-parity words $1/16$, and their full triple law has total variation $1/4$ from independent fair bits. In particular,
\[
\Pr(Y_2=0\mid Y_0Y_1=00)=3/4,\qquad
\Pr(Y_2=0\mid Y_0Y_1=10)=1/4.
\]
Both histories end in the same observed state, 0. They predict different next observations. This directly violates (1).

For each observation fiber, the hidden-conditioned Bernoulli laws have parameters $1/4$ and $3/4$. Their diameter is $1/2$, so any single approximating row must have worst-case total-variation error at least $1/4$. The fair row attains it. Hence the optimal uniform one-step reduced-kernel error for this model is exactly $1/4$.

**Positive control.** Hidden variables do not automatically defeat reduction. Let the full state be $(z,h)$ and update by
\[
P((z,h),(z',h'))=Q(z,z')\,\mathbf1\{h'=1-h\}.
\]
The hidden bit persists and alternates, but the next observed law is exactly $Q(z,\cdot)$ for either hidden value. The visible process is correctly Markov for every initial law. This gives a positive example of reduced-state sufficiency despite persistent hidden dynamics.

## 5. Finite validation depth cannot uniformly rule out longer memory

Fix $L\ge2$ and $0<|\eta|<1$. Use full states $x=(x_1,\ldots,x_L)\in\{0,1\}^L$. Shift the state and append a bit $b$ with probability
\[
P_\eta\bigl(x,(x_2,\ldots,x_L,b)\bigr)
=\frac12\left[1+\eta(-1)^{x_1+\cdots+x_L+b}\right].
\tag{4}
\]
The uniform law on the $2^L$ full states is stationary. For any target state, summing over the two possible dropped first bits cancels the signed term, proving the stationary column sum. Every append probability is strictly positive; all states communicate in $L$ steps and the all-zero state has a self-loop. This gives a stationary, irreducible, aperiodic finite-state realization with full support on finite output words.

Every contiguous output window of length at most $L$ is exactly distributed as independent fair bits. At length $L+1$,
\[
\Pr_\eta(Y_1=y_1,\ldots,Y_{L+1}=y_{L+1})
=2^{-(L+1)}\left[1+\eta(-1)^{\sum_i y_i}\right].
\tag{5}
\]
Consequently
\[
\operatorname{TV}(\mathcal L_\eta(Y_{1:L+1}),\operatorname{Unif}(\{0,1\}^{L+1}))
=|\eta|/2.
\tag{6}
\]
The next-bit law depends on the oldest of the preceding $L$ bits even when the last $L-1$ are held fixed. Since both such histories have positive probability, the observed Markov order is exactly $L$.

For $\eta=1/2$, the first distinguishing complete window has TV $1/4$, independent of $L$. Thus agreement of every record distribution through an arbitrary fixed length does not certify unrestricted freshness or memorylessness when the comparison class permits larger finite hidden memory.

**Scope guards.** The statement concerns consecutive windows, not every collection of $L$ widely separated indices. The process is stationary, not exchangeable; it is a temporal-record comparison rather than an exchangeable paintbox law. Tests restricted to independently restarted stationary windows of length at most $L$ remain nonidentifying. Keeping correlations between windows or making a longer continuous record changes that experiment. A justified memory bound, state-space bound, or richer intervention family can change identifiability. The formal index is not a derivation of physical time. This elementary higher-order Markov construction is used as a countercontrol without a novelty claim.

## 6. An approximate operational guarantee

Suppose a candidate family $Q_a$ satisfies the uniform row bound
\[
\operatorname{TV}(M_a(x,\cdot),Q_a(q(x),\cdot))\le\delta
\tag{7}
\]
for every permitted full state and action. Match the initial observed distribution. For every common observed-history-based policy and $N$ transitions,
\[
\boxed{\operatorname{TV}(\mathcal L(H_N),\mathcal L(\widehat H_N))
\le1-(1-\delta)^N\le N\delta.}
\tag{8}
\]
Here $H_N$ includes the complete observed sequence and, when relevant, its chosen actions.

**Proof.** Given a common observed history, the true next-observation law is a posterior mixture of the rows $M_a(x,\cdot)$ over the current fiber. Convexity puts that mixture within $\delta$ of $Q_a$. Couple the policy choices identically while histories agree and couple the next observations maximally. Conditional on agreement so far, the probability of another agreement is at least $1-\delta$. Iterating yields agreement probability at least $(1-\delta)^N$, and the coupling inequality proves (8). QED.

The constant cannot be uniformly improved in this unrestricted class. A reference stays at 0; a comparator starting at 0 jumps to absorbing state 1 with probability $\delta$ at every step until it leaves. The reference history is all zeros; the comparator differs with probability exactly $1-(1-\delta)^N$.

A test of false-rejection probability at most $\alpha$ under the reduced model consequently has false-rejection probability at most
\[
\min\{1,\alpha+1-(1-\delta)^N\}
\]
under the true model satisfying (7). This is a conditional error-transfer bound, not a measured calibration guarantee. An averaged stationary mismatch, an estimated mean error, or a comparison on one preparation cannot be substituted for the uniform conditional bound (7). A bound on complete history is also not interchangeable with a claim about only the terminal state.

The coupling argument covers adaptive visible-history policies, and the absorbing-state example attains the bound. The theorem is an elementary application of coupling to the declared controlled process.


## Mathematical sources identified in the original note


- G. Wolfer and S. Watanabe, *Geometric aspects of data-processing of Markov chains*, Transactions of Mathematics and Its Applications 8 (2024), tnae001. DOI: 10.1093/imatrm/tnae001. https://arxiv.org/abs/2203.04575 . Background for the established row-sum characterization of strong lumpability and its distinction from preparation-dependent reduction.

- P. Buchholz, *Exact and ordinary lumpability in finite Markov chains*, Journal of Applied Probability 31 (1994), 59–75. DOI: 10.2307/3215235.
