# A finite adaptive panel can hide a held detector response

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical development with OpenAI Codex.

A three-tick Hadamard walk from a sharp right rail has a position well of kinematic mass $m=5/8$. Even the complete ordered records from a bank of $N$ such walks can have exactly the ordinary independent distribution while an unobserved detector response remains fixed throughout each bank and assigns a different probability to that well. The construction below also works when each new preparation is chosen after seeing earlier outcomes. It specifies which marginal of the held response is being tested. [Three-tick preparation and single-read response](spectator_refinements.md) · [What counts from longer banks can identify](held_walk_counts.md)

## A fixed-order response and a dependent bank

Fix in advance a finite maximum number of calls $N\ge1$. A setting specifies a normalized finite table $p=(p_j)$ of terminal cell masses. The ordinary benchmark independently samples the next outcome from the chosen table, conditional on the publicly observed history. A held type $s\in\{-1,+1\}$ is required to give, on **each preassigned slot and setting**, probability $f_s(p_j)/\sum_k f_s(p_k)$. Dependence between different slots conditional on $s$ is allowed.

Choose a smooth function $h$ with compact support in $(1/2,1)$ and $h(5/8)\ne0$. Write $g=h'$, so $\int_0^1g(u)\,du=0$. For $s=\pm1$, set

$$
T_s(x)=x+s\epsilon h(x),\qquad
f_s(x)=(1-x)\frac{T_s(x)}{1-T_s(x)}\quad(0\le x<1),\qquad f_s(1)=1.
$$

Off the support, $f_s(x)=x$. Choose $\epsilon>0$ small enough that both $T_s$ take values in $(0,1)$ on the support and both $f_s$ are strictly increasing. Such a choice exists because the support is compact inside $(1/2,1)$ and the derivatives of $f_s$ converge uniformly to 1 there as $\epsilon\to0$. Also require $\epsilon N\lVert g\rVert_\infty<1$. The two responses differ at the actual $5/8$ mass.

Draw the fair sign **before** the settings. Given $s$, draw a vector of private seeds $U_1,\ldots,U_N$ on $[0,1]^N$ with density

$$
L_s(u_1,\ldots,u_N)=1+s\epsilon\sum_{i=1}^N g(u_i)
$$

relative to uniform product measure. This is a strictly positive probability density since each summand integrates to zero and the perturbation has absolute value less than one. It is invariant under permutations of the slot labels. At any one slot, integrating out the others leaves density $1+s\epsilon g(u)$ and cumulative probability $T_s(x)$. Take auxiliary uniforms $V_1,\ldots,V_N$ independent of these seeds and of the sign.

For a table with a cell of mass $x>1/2$, that cell is unique. Return it exactly when $U_i\le x$. On a miss, use $V_i$ to choose among the remaining cells in proportion to their ordinary masses. If $x=1$ the miss has probability zero. For a table with all masses at most $1/2$, use $V_i$ alone to sample the ordinary table. For a fixed setting at any slot, conditional on the sign the heavy cell has probability $T_s(x)$ and a minor cell of mass $y$ has probability $y(1-T_s(x))/(1-x)$. These agree exactly with normalization by $f_s$, since all minor cells have $f_s(y)=y$. This rule respects a relabeling of the cells in distribution. Randomly permuting the physical read slots also leaves the whole bank law invariant.

## What the observer sees

The two full densities average pointwise to one. Consequently the observer sees independent uniform $U_i$ and $V_i$ across the entire bank, although the $U_i$ are generally dependent conditional on its held sign. For every fixed sequence of tested tables the complete outcome word has its ordinary product law. For the $N$ repeated three-tick walks this includes the entire $\mathrm{Binomial}(N,5/8)$ count law and every ordering of the hits. The two conditional one-slot hit probabilities are $5/8\pm\epsilon h(5/8)$.

The same private bank implements every adaptive policy of length at most $N$ that chooses the next table and whether to continue using only the observed history and independent randomness. At the pooled level the next pair of seeds is independent of that history, so the next conditional distribution is precisely the ordinary chosen table. Induction gives equality of every transcript probability, including its settings and any stopping time within the deadline. The same functions $f_\pm$ work simultaneously over the continuum of choices at this fixed deadline.

There is a stronger condition one could impose on the apparatus. Suppose that even **given the sign and the observed history**, a repeated $5/8$ setting still has its class-specific hit probability $p_s=T_s(5/8)$. Then two successive hits have pooled probability $E[p_s^2]=(5/8)^2+\epsilon^2 h(5/8)^2$. This condition would expose the fluctuation. In the constructed bank, a choice routed specifically to previous hits can select a biased subpopulation of the seeds within a sign. Its sign-conditional success rate need not equal the preassigned-slot marginal. Holding a response throughout a run, or observing that all marginal frequencies agree across distant choices, does not establish the stronger condition.

The simulator describes sequential access to specified tables. If a table combines settings at two stations, its pooled law has the same marginal-invariance properties as the ordinary table. This construction supplies no implementation by separate devices restricted to local information at spacelike separation. Further, $N$ is the number of separately normalized reads, not the three ticks inside each free walk. The allowed perturbation depends on the bank deadline. For the same held-response population at every bank size, the observed variance bound in the [count analysis](held_walk_counts.md) rules out a fixed positive deviation when the ordinary count variance persists as $N\to\infty$.
