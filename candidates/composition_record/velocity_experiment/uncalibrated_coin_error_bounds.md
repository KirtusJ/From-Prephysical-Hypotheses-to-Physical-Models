# Error bounds for a position write with an unknown incoming coin

Run the eight Hadamard-or-identity ticks $HIHHHHHI$ from a localized position, streaming both rails after every coin. At the next exact site write the individual displacements $-4,+4$ each have squared mass $2/64$, $-2,+2$ each have $8/64$, and 0 has $10/64$. These five masses hold separately for **every** incoming two-rail density matrix, including complex and mixed coins. The four remaining masses, in some mirror order, have numerators $1\pm x$ and $16(1\pm x)$ with $|x|\le1$. Use a geometry where these nine displacements are distinguishable. This note gives finite-data bounds for the corresponding measurement proposal.

A sequential mode can draw its incoming coin and its exponent together, differently on every reached history. Given that pair it scores the next site weights by $w^q/\sum w^q$. The state following a write must be localized for the next leg; its coin is unrestricted. A whole-word mode instead fixes an ordinary tree of complete-word masses and scores those masses once with a launch exponent $Q$. Its leaf table may vary by launch and may correlate with $Q$. At each positive prefix the ordinary tree must have the stated scalar effects. Zero power is uniform on the occupied support. Negative powers, if included, operate on that same support. Allowing $\pm\infty$ means selecting among the positive maximum or minimum weights, with arbitrary tie breaking.

## Two measured quantities

Let $\theta=\log4/\log5$. At one write give a displacement the signed score $s$ and the medium-event indicator $m$ from this table. The coefficients average the two mirror sites, while $m$ counts both.

| Displacement | $s$ | $m$ |
| --- | ---: | ---: |
| $-4,+4$ | $(1-\theta)/4$ | 0 |
| $-2,+2$ | $-1/16$ | 1 |
| $0$ | $\theta/10$ | 0 |
| all others | 0 | 0 |

At a visited node write $g=E[s]$ and $M=E[m]$ conditional on its mode and incoming state. With finite $q$, write $Z$ for the sum of powers of the positive **integer-scale numerators**, including any nonintegral values at the four coin-dependent sites. Then

$$
 g=\frac{(1-\theta)2^{q-1}+\theta10^{q-1}-8^{q-1}}{Z},
 \qquad M=\frac{2\,8^q}{Z},\qquad
 \frac gM=R(q)=\frac{(1-\theta)(1/4)^{q-1}+\theta(5/4)^{q-1}-1}{16}.
$$

The coefficient $1/16$ in $R$ uses the **combined** medium probability. The function is strictly convex with $R(1)=R'(1)=0$, by $8=2^{1-\theta}10^{\theta}$. At ordinary power, $(g,M)=(0,1/4)$. At either extremal power, $M=0$ and $g\ge0$: the largest weight is at least 16, and among the two outermost sites at least one positive weight is at most 2. A minimum-weight tie may include a low scalar site and give a positive score there. Neither extremum can select a medium site.

Fix a scientifically relevant tolerance $\delta>0$. For any $0<h<\min(1,\delta)$ set $r_h=\min(R(1-h),R(1+h))>0$ and $M_h=\min(1,8^h/4)$. The latter bounds $M$ uniformly when $|q-1|<h$: if $q\le1$ the sum of powers of normalized masses is at least one, and if $q\ge1$ it is at least $9^{1-q}$ by convexity. Thus the respective upper bounds are $8^h/4$ and $(9/8)^h/4$. For **every mode on a visit**,

$$
\mathbf1_{|q-1|\ge\delta}
  \le 1-\frac{M}{M_h}+\frac{g}{r_h M_h}. \tag{1}
$$

Inside $|q-1|<h$ the right side is nonnegative. Outside that interval $g\ge r_h M$ for finite $q$, giving a right side of at least one. For either infinite power use $M=0$ and $g\ge0$. No uniform positive lower bound on $g$ near infinite powers is assumed. With precise ordinary means the right side tends to zero as $h\downarrow0$; for finite data $h$ trades the sampling error in $g$ against the slack in $M_h$. The same simultaneous confidence event for $M$ and $g$ justifies optimizing $h$ numerically.

## Bounds from the last write

Pool all original launches at the final write. In a whole-word mode the conditional distribution among terminal sibling leaves, given any visited parent, is the local power of its ordinary children. Their common prefix factor cancels, even if the incoming coin and the parent distribution are associated with the launch exponent. A globally selected extreme leaf is also an extreme among its siblings. Thus (1) controls both whole-word modes with $|Q-1|\ge\delta$ and sequential modes with final $|q-1|\ge\delta$.

Let $U_g$ be a simultaneous upper confidence limit for the final score and $L_M$ a lower limit for the final medium fraction. Their denominator is all assigned launches. A valid upper bound on the combined fraction is

$$
G_\delta=\min\!\left(1,\inf_{0<h<\min(1,\delta)}
\left[1-\frac{L_M}{M_h}+\frac{U_g}{r_h M_h}\right]\right).
$$

The same bound applies to the fraction of whole-word modes at distance at least $\delta$ since these are a subset. A negative upper limit contradicts the model on the confidence event. For a fixed earlier sequential prefix analyzed in isolation, (1) controls the fraction per **visit**, provided the data are actually sampled from those modes. Its per-launch version multiplies the right side by the prefix incidence. A scarce prefix cannot yield a precise conditional estimate just because the full experiment had many launches.

## Earlier writes with an unknown fraction of whole-word modes

At an earlier write, whole-word power need not act locally because later branches can have different normalizers. This makes the correction signed. Let $E$ select a prescribed prefix, or take $E$ to be the whole population for a pooled clock. Define the bounded per-launch observable

$$
T_{h,E}=\mathbf1_E\left[1-\frac{m}{M_h}+\frac{s}{r_h M_h}\right].
$$

Write $W_h$ for the width of its range and $D_h=\max(0,-\min T_{h,E})$; both can be computed directly from the table, including zero off $E$. For sequential modes (1) bounds the probability of the joint event “reach $E$ and draw $|q-1|\ge\delta$” by their contribution to $E[T_{h,E}]$. In an ordinary whole-word mode the mean of $T_{h,E}$ is $P(E)(1-1/(4M_h))\ge0$.

For fixed depth $J$ the complete tree has at most $K=9^J$ leaves. Write $p$ for any ordinary tree law. If $|Q-1|<d<1$, then uniformly on such trees

$$
 d_{\rm TV}(T_Qp,p)\le t_d=\min\!\left(1,\sqrt{d\log K/(1-d)}\right),
 \qquad (T_Qp)_w=\frac{p_w^Q}{\sum_v p_v^Q}.
$$

Indeed with $Z_Q=\sum p_w^Q$ one has $|\log Z_Q|\le d\log K$ and $-E_{T_Qp}\log p=(H(T_Qp)-\log Z_Q)/Q\le(1+d)\log K/(1-d)$ on positive leaves. The identity $D_{\rm KL}(T_Qp\Vert p)=(Q-1)E_{T_Qp}\log p-\log Z_Q$ and Pinsker's inequality give the bound. Consequently a near-ordinary whole-word mode lowers the earlier statistic's mean by at most $W_h t_d$. The incidence of the remaining whole-word modes is at most $G_d$ from the final write. If $U_T$ bounds the full observed mean of $T_{h,E}$, then

$$
 P(\text{sequential mode},E,|q-1|\ge\delta)
 \ \le\ U_T+W_h t_d+D_h G_d . \tag{2}
$$

The last term accounts for the most negative possible contribution from far whole-word modes. Setting that contribution to zero can exclude viable mixtures. $h$ and $d$ serve different purposes and can be chosen separately. The bound is per original launch. A positive lower bound for $P(E)$ permits a statement among all visits to $E$; a lower bound for sequential visits is required to restrict the denominator to that subpopulation. The entropy estimate here depends explicitly on the fixed depth. Increasing the horizon requires a new error budget. [Calibration and increasing resolution](../../../Director_G/Calibration_and_the_log_weights_of_a_flight.md)

For independent launches, simultaneous bounds on the arm means follow from each observable's bounded range and the number of comparisons. To vary $h$ after inspection, first bound the three primitive means of $\mathbf1_E$, $\mathbf1_E m$, and $\mathbf1_E s$ simultaneously, then propagate their intervals with the displayed coefficient signs to obtain $U_T$ for all $h$. Include the terminal statistics in the same family or allocate separate error budgets. Missing launches, mislabeled displacements, and detector gains require measured corrections before treating these as true event scores. This procedure tests the power assigned on realized writes; it does not fix omitted degrees of freedom, counterfactual post-write coins, or an arbitrary rule outside the power family. [Hoeffding's bounded-sum inequality](https://doi.org/10.1080/01621459.1963.10500830) · [Word-level reporting and calibration](reporter_calibration.md)
