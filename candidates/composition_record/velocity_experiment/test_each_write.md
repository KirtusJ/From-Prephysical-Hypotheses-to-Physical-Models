# Test the probability exponent at each reached position write

The first site write of the original nine-tick walk has only two distinct squared weights. A mixture of two nonordinary powers can reproduce its full distribution and then use the ordinary rule for every later write. One additional phase gate per three-tick flight removes that ambiguity. In the modified circuit, the recorded words can test the exponent at **each reached write**, even when it is drawn again using the preceding history. The proof also allows an unknown fraction of instruments that score the entire word once. [First-write counterexample](joint_and_conditional_powers.md)

## A circuit with enough siblings to compare

Use the sharp R source, the two $S$ pulses, and the same four position codes and write clocks as in the [original circuit](generate.py). Add $T=\operatorname{diag}(1,e^{i\pi/4})$ uniformly to the coin after ticks 2, 5 and 8, before the Hadamard of the next tick. There is no change of measured position address. The ideal first-word marginals, in code order, are

$$
\frac1{512}(64,\ 192+64\sqrt2,\ 192-64\sqrt2,\ 64).
$$

Each of the 64 leaves has positive squared weight. Of the 21 internal nodes (one root, four one-code prefixes, sixteen two-code prefixes), fourteen have three distinct positive child weights and seven have four. Multiplicities and conditioning matter: four positive children of just two different sizes would not suffice. These are circuit calculations. No shots from this modified circuit are reported here. [Exact tree calculation](check_all_writes.py)

A second circuit uses only real coins. The addressed middle tick of each flight applies X on even address parity and H on odd parity. Every reachable prefix has three distinct positive children and one dark child. The same comparison applies on occupied support. The separate dark outcomes provide a direct check on that support. [Exact addressed circuit, field embeddings and limitations](addressed_embedding.md)

## Which models the word table tests

Write $p_w$ for the ordinary probability of leaf $w$, $p_\alpha=\sum_{w\succeq\alpha}p_w$ for a prefix, and $r_j=p_{\alpha j}/p_\alpha$ for its ordinary conditional child probabilities. A launch may belong to either of two classes:

* A whole-word mode draws $Q$ and reports $w$ with probability $p_w^Q/\sum_v p_v^Q$.
* A sequential mode reaches a prefix $\alpha$, draws $q_\alpha$ using any hidden variables and the history so far, then emits $j$ with probability $r_j^{q_\alpha}/\sum_i r_i^{q_\alpha}$. The successive draws may be arbitrarily correlated. This is a conditional law given the drawn exponent and the available hidden history; the draw precedes the next outcome. The normalized state fed to the following gate sequence must be the stipulated projected branch state whenever the corresponding prefix occurred.

This is a finite experiment for specified response mechanisms. Busch derives the density-operator probability rule from probability assignments on the space of quantum effects. Here the observables and post-write states are specified and the competing powers are explicit. [Busch, generalized probability distributions on effects](https://doi.org/10.1103/PhysRevLett.91.120403)

The mixture proportions and exponent laws are unknown. The formulas describe the true stored words. Applying them to reported words requires a calibrated recording channel, or valid error bounds for the observable below. Branch-dependent losses, additional hidden rail scoring, and modified post-write states require their own models. A uniformly independent choice of preparation would still require a per-preparation table or an explicitly modeled pooling rule. [Word reporting and calibration](reporter_calibration.md)

## Observable scores and the population claim

At each internal node $\alpha$ select three distinct **values** among its conditional probabilities: the smallest $l$, an interior $m$, and the largest $h$. Fix in advance which interior value to use if two are available. Write $n_l,n_m,n_h$ for their multiplicities and $\theta=\log(m/l)/\log(h/l)$. For each original launch, score zero unless the word reaches $\alpha$. On that visit assign the score

| Next child's ordinary weight | Score on that launch |
| --- | ---: |
| $l$ | $(1-\theta)/(n_l l)$ |
| $m$ | $-1/(n_m m)$ |
| $h$ | $\theta/(n_h h)$ |
| any other weight | 0 |

Denote this bounded score by $s_\alpha(w)$. Including every child in a tied level makes the test independent of which tied extreme a maximum or minimum rule chooses. For finite $q$, the conditional mean under a local power is

$$
f_\alpha(q)=\frac{(1-\theta)l^{q-1}+\theta h^{q-1}-m^{q-1}}{\sum_j r_j^q}.
$$

Because $m=l^{1-\theta}h^\theta$, weighted arithmetic–geometric mean gives $f_\alpha(q)\ge0$ with equality exactly at $q=1$. This covers $q=0$ and even finite negative powers on this all-positive tree. Pure maximum and minimum selectors have positive scores as well. On a tree with zero-probability edges a convention for those edges must be fixed before extending the result; unreachable ordinary histories yield no conditional test.

**First identify whole-word modes.** Sum $s_\alpha$ over the sixteen parents of leaves, defining $s_*(w)$. Exactly one of those parents is reached on a launch. In a sequential mode the expected contribution there is $f_\alpha(q_\alpha)$ conditional on reaching it and drawing its exponent. In a whole-word mode with finite $Q$, the conditional law on the four sibling leaves, given their parent, equals the local power with exponent $Q$: their common factor $p_\alpha^Q$ cancels. Thus the expected terminal sum $F(Q)=E_Q[s_*]$ is strictly positive unless $Q=1$. For global maximum or minimum scoring, **any** globally extremal leaf is also extremal among its siblings, where the score is positive. This includes arbitrary allocation among globally tied leaves. Using just one terminal prefix could miss such a mode.

**Then test the earlier writes.** Ordinary word frequencies give zero mean for $s_*$ and each $s_\alpha$. By nonnegativity, the terminal equality forces every whole-word exponent to equal one almost surely and every realized last sequential exponent to equal one almost surely. Whole-word modes now contribute precisely zero to every earlier score. In sequential modes the conditional expectation at an earlier visited node is again $f_\alpha(q_\alpha)$: all its later continuations sum to one regardless of subsequent power draws. Thus each earlier equality forces $q_\alpha=1$ almost surely on the sequential visits to that node. Strictly speaking, after the terminal equality, all earlier nodes may be tested in parallel. The conclusion concerns **realized decisions**. It cannot determine a mode's counterfactual exponent off the visited path or the split between the two classes when both behave ordinarily. The individual word frequencies imply these equalities; the prespecified score equalities already suffice.

## What finite counts can certify

Let $U_*$ and $U_\alpha$ be simultaneous upper confidence limits for the population means of $s_*$ and the earlier scores. Use per-launch counts, assigning zero on launches that did not reach the given prefix. For independent launches, with $K$ such comparisons and score range width $R_j$, one valid upper limit is $\widehat E[s_j]+R_j\sqrt{\log(K/\beta)/(2N)}$ for $N$ launches and family error probability $\beta$. A union bound permits reusing the same words in all scores. Account for recording uncertainty before interpreting the limits. [Hoeffding's inequality](https://doi.org/10.1080/01621459.1963.10500830)

Choose a separation $h>0$ and a lower bound $v_h>0$ for $F(Q)$ over $|Q-1|\ge h$. A positive bound exists on this fixed tree: the finite-power expectations are continuous and the limiting extreme-leaf scores are positive. For arbitrary tie breaking at the endpoints, include the **smallest** score on the globally extremal leaves in the bound. The probability per launch of a whole-word mode with $|Q-1|\ge h$ is at most $\min(1,U_*/v_h)$.

An earlier whole-word contribution need not have a positive sign at finite calibration error. Use the full ordinary leaf table to compute $H_\alpha(Q)=E_Q[s_\alpha]$ under whole-word scoring. It vanishes at one. Define $\omega_h=\sup_{|Q-1|<h}|H_\alpha(Q)|$ and $M_\alpha=\max_w|s_\alpha(w)|$. For sequential powers outside a specified tolerance $\delta>0$, let $v_{\alpha,\delta}>0$ be a lower bound for $f_\alpha(q)$ over $|q-1|\ge\delta$, including any allowed endpoint rules. On the joint confidence event,

$$
\Pr(\text{sequential mode, reach }\alpha,\ |q_\alpha-1|\ge\delta)
\le
\frac{U_\alpha+\omega_h+M_\alpha\min(1,U_*/v_h)}
     {v_{\alpha,\delta}} .
$$

Indeed, whole-word modes near one can lower the earlier observed score by at most $\omega_h$. The remaining whole-word modes can lower it by at most $M_\alpha$ times their incidence. All sequential contributions are nonnegative. For a terminal parent, $U_*/v_{\alpha,\delta}$ alone bounds the joint incidence since each contribution to the terminal-sum expectation is nonnegative. Clip probability upper bounds at one; a negative certified upper bound challenges the stipulated model on that confidence event.

These are fractions of *all launches*. A conditional statement about bad sequential decisions among all visits to a node requires a positive lower limit for its visit probability. A statement restricted to sequential visits requires a lower bound on **that** subpopulation, which is generally unobserved. With few or no visits the record can be compatible with large conditional deviations on that branch.
