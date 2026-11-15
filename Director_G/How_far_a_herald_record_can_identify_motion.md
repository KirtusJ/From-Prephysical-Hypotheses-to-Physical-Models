# How far can a herald record identify classical motion?

Two position records can tell whether a hidden setting has persisted beyond a specified memory length. Yet for every fixed observation horizon there is a controller that reproduces the entire held-setting experiment through that horizon and has a different long-time velocity. The controller only reads its own previous heralds. The walker, site detector and two herald preparations can all stay the same.

## What three consecutive returns identify under a two-state law

Use the [four-tick measured walk](Private_heralds_in_a_measured_walk.md). A binary success $H$ causes a full site measurement at tick two. Write $R=1$ if the walker returns to its block origin. The signed path calculation gives $\Pr(R=1\mid H=h)=1/8+h/4$. Each block begins at its recorded origin with a sharp incoming rail. Conditional on exogenous heralds, different blocks have independent displacements. Assume here that a hidden mode persists with probability $\rho\in[0,1]$ and otherwise redraws from its stationary weights. Conditional on the mode path, fresh independent preparations emit successes at rates $p_i$.

Let $q_i=1/8+p_i/4,\ m=ER$, and $d_i=q_i-m$. From stationary population word probabilities write $C_h=E[(R_0-m)(R_h-m)]$, and $T$ for the centered product at three consecutive times. For $V=E d_i^2$ and $\delta=d_0+d_1$, the two support points satisfy $d_i^2=V+\delta d_i$. The conditional expectation of the centered emission $h$ blocks ahead is $\rho^h d_i$. Conditioning successively, using different read times, gives

$$
 C_1=\rho V,\qquad C_2=\rho^2 V,\qquad T=\rho^2 V\delta.
$$

Thus if $C_1>0$, recover $\rho=C_2/C_1,\ V=C_1^2/C_2,\ \delta=T/C_2$. The roots of $z^2-\delta z-V=0$ and their unique zero-mean weights give both $q_i=m+z_i$ and both herald rates, up to exchange. The physical ranges $0<\rho\le1$ and $1/8\le q_i\le3/8$ are testable. A fourth consecutive centered product must equal $C_1^2+T^2/C_1$, by applying the same conditional identities once more. Binary hidden Markov parameter recovery and word constraints have a general algebraic treatment. The walk supplies the physical emission channel needed to convert the recovered numbers into herald rates. [Critch, *Binary hidden Markov models and varieties*](https://arxiv.org/abs/1206.0500)

When $C_1=0$ within this family, either the mode is drawn independently each time or its occupied emission rates coincide. Both give iid Bernoulli return words of every length. When $\rho=1$, independent stationary launches allow the inverse. One arbitrarily long held trajectory samples only its own rate. The inverse uses exact probabilities and becomes ill-conditioned as its denominators vanish.

## A private controller for each finite observation horizon

In the held experiment the two rates are $p_0=1/2,\ p_1=25/146$, with weights $\pi_0=55/128,\ \pi_1=73/128$. Select one mode per launch, then use fresh preparations conditional on it. The [six-wire herald construction](../candidates/composition_record/velocity_experiment/a_private_controller_for_the_walk_herald.md) gives these rates. For a binary word $u$ with $a$ successes and $b$ failures, set $L_i(u)=p_i^a(1-p_i)^b$ and $P(u)=\sum_i\pi_i L_i(u)$, with $P(\varnothing)=1$.

Fix any integer $K\ge1$. Keep the last $K-1$ herald bits. Given memory $u$, select a fresh mode with probability $\pi_i L_i(u)/P(u)$, run one fresh herald with that mode, and shift in its actual bit. For stationary operation preload $u$ from $P$. Equivalently, start empty and use the same posterior on the available prefix until the memory fills. Each mode draw has rational weights and can be made exactly with private fair bits by rejection. For $K=3$ and two stored successes the posterior weight of mode zero is $803/928$. A bounded number of fair draws cannot prepare this weight exactly. Rejection can require unbounded preparation time. The comparison is at completed block counts, and would require a separate timing model for a fixed laboratory clock. The selector can prepare in advance because it does not read the walker. Private modes, auxiliary draws and their timing lie outside the tested record.

The next-bit probability is $P(uh)/P(u)$. Summing $P(hu)$ over the previous bit gives $P(u)$, so the window distribution is stationary. All words covering at most $K$ successive heralds agree exactly with the held experiment. Passing those bits through the common walk also matches every displacement word on such an interval, and any additional common read generated solely from those bits and the same block preparation. For a late window, displacements are relative to its first origin. Absolute position may already contain an older history. The statistical construction is the canonical finite-order Markov approximation. Here it has a realization using the two available herald settings. [Bressaud, Fernández and Galves, §2](https://webspace.science.uu.nl/~ferna107/papers/papers/brefergal99-speed.pdf)

Every transition that appends a bit has positive probability. A specified memory word can therefore be reached from every other, and the all-zero word has a self-loop. The finite stationary memory is ergodic, including the memoryless $K=1$ case. Its empirical success fraction tends to $s=5/16$. In the full-site experiment the displacement conditioned on a herald is centered with variance $5-H$. Given the complete sequence, the increments are independent and bounded. The ergodic average of the variances and the bounded-increment central limit theorem give $X_n/\sqrt n\Rightarrow N(0,5-s)$. The held controller gives a mixture of the two Gaussian laws with variances $5-p_i$. In the right-site experiment the conditional block mean is $-H/4$, so bounded independent centered noise contributes zero to the limiting velocity. The rival has one limiting velocity $-5/64$, while the held controller has velocities $-1/8$ and $-25/584$ with the original weights. These limits fix $K$ first and then let the run length tend to infinity.

## The first separating record uses two endpoint positions

Use the full-site experiment. In a span of $K+1$ blocks let $u$ denote the intervening $K-1$ heralds, $r_u=E[p\mid u]$, and $v_u=\mathrm{Var}(p\mid u)$ under the held law. Given $u$, both endpoint heralds have mean $r_u$ in both models. In the held model their covariance is $v_u$. In the finite-memory model the last herald uses only $u$, giving conditional independence of the endpoints. Thus the held endpoint table minus the rival table has entries $+v_u$ for like bits and $-v_u$ for unlike bits. All $v_u>0$ for these positive, distinct rates and positive weights.

Let $K_h(d)$ be the displacement law given $H=h$, and $\Delta=K_1-K_0$. In order $d=(-4,-2,0,2,4)$ it equals $(0,-2,4,-2,0)/16$. After the physical reads, the difference between the two full displacement-word probabilities at this span is

$$
 \Delta(d_1)\Delta(d_{K+1})
 \sum_u P(u)v_u\prod_{j=1}^{K-1}K_{u_j}(d_{j+1}).
$$

The sum is nonnegative. The positive difference occurs when both endpoint displacements return or both are in the negative part of $\Delta$. Adding the zero-difference cases gives the simple event $R_1=R_{K+1}$. Its probability under the held law exceeds the rival by

$$
 2\,E[v_u]\,\mathrm{TV}(K_1,K_0)^2=\frac{E[v_u]}8 .
$$

This is the entire total variation distance between the full $K+1$ displacement laws. No other event on that word separates the specified pair by more. The test needs the two block displacements, including their block origins, and the public clock. The intermediate outcomes need not be read by the analyst. At $K=1$ the agreement gap is $495/149504$. Strict separation at each finite horizon does not guarantee practical statistical power. There is no finite consecutive panel that certifies the held-mode classical limit against all such memory lengths.

The [exact arithmetic check](check_finite_herald_memory.py) enumerates both herald laws and passes them through the return channel, including both herald outcomes and the degenerate fresh-mode case. The [signed-path replay](check_private_mode_transport.py) verifies the displacement kernels. All conclusions assume the specified ordinary conditional measurement law. How a physical walk obtains that law from prephysical primitives remains open.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex constructed the controller, derived the comparison and independently replayed the word probabilities.
