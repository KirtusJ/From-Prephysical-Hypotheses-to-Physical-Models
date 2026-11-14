# Localizing the response around the selected mass gap

Research supplement for Director G, prepared by OpenAI Codex for Kirtus Justus. Gate OP-27.

On the tick-256 menu the [finite-moment bound](Finite_moment_transfer_between_calibrated_masses.md) gives an attainable square-root coefficient of about 1.230 using a single tent across the lower half. The detector below uses its hidden state to center the tent around the winning gap. It gives a coefficient of about 1.956, with an observable change in the distribution of paired errors.

## Fixed-mass calibration and selected error

Use the [zero-cost attaining law](Hidden_threshold_between_calibrated_masses.md). Write $I$ for its winning lower-half gap, $h_i=b_i-a_i$ for its width, $m_i=(a_i+b_i)/2$ for its center, and $t$ for the joint cutoff. Conditional on winning, the distance $D$ is uniform on $[t,h_i]$. The lower threshold $Z$ lies at distance $D-h_i/2$ from the center. The selected science mass is either $Z$ or $1-Z$. Let $\sigma$ be positive in the first case and negative in the second. The orientation is independently fair given the winning gap and distance.

For each winning gap take the lower-half tent
$$
R_i=\min(4h_i,m_i,1/2-m_i),\qquad f_i(z)=(R_i-|z-m_i|)_+ .
$$
Extend by $f_i(1-z)=-f_i(z)$. These functions vanish at the endpoints and midpoint and have Lipschitz constant one. The factor four is a construction choice. Exploratory integer factors two through eight gave coefficients around 1.265, 1.853, 1.956, 1.937, 1.880, 1.812 and 1.751. There is no claim of optimal tent width.

Use a common mixing weight $0\le\epsilon\le1$ for every type:
$$g_\epsilon(s)=(1-\epsilon)g_0(s)+\epsilon(s+\sigma f_I(s)).$$
Every type remains monotone, complementary and endpoint-faithful. At fixed $s$, conditioning on $I$ cancels the signed tent; averaging $g_0$ over all types gives $s$. A proposed refinement that varies the mixing weight by winning gap fails this argument: generally $\mathbb E[g_0(s)\mid I]\ne s$. The winning threshold in a given gap is confined to its edge strips conditional on that gap winning. A same-family second reader identified this selection dependence when reviewing the proposed formulas. Only the common-weight construction is evaluated below.

Let $p_i=2(1-t/h_i)$ in active gaps and zero elsewhere. For this menu $R_i\ge h_i/2$ in every active gap. On the selected target the tent contributes $R_i+h_i/2-D$, whereas the original error is $D$. The conditional mean increase per unit mixing weight is therefore $G_i=R_i-h_i/2-t$. Using the lower-half paired weights $W_j$ from the finite-moment supplement, define
$$G=\sum_i p_i G_i,\qquad H=\sum_i p_i\sum_j W_j f_i(x_j)^2.$$
The mean signed bias is exactly $B_0+\epsilon G$ and the aggregate paired moment is exactly $\epsilon^2 H$. The two reads independently sample the per-type response conditional on the same hidden state. All trials count. Thus $B_0+(G/\sqrt H)\sqrt M$ is attainable for $0\le M\le H$.

## Numerical consequence and a discriminator

The [rational checker](check_gap_local_response.py) sums over all 11 active gaps and integrates each affine edge strip independently as a cross-check. It gives $H\approx0.000731481676$ and $G/\sqrt H\approx1.956009335$. At $M=10^{-8}$ the selected bias is about **2.001824 percentage points**. The earlier upper bound is about **2.150342 points** at this budget. The sharp coefficient remains open.

Under this construction the centered pair score at node $x_j$ is $M\sum_i p_i f_i(x_j)^2/H$. Exactly 21 of 32 interior lower-half nodes have a positive score. At the routed mass $0.260644776272\ldots$ the score is approximately $3.1642773 M$. At the interior mass $0.000573654881\ldots$ it is zero, whereas the global tent predicts a positive score at every interior node for $M>0$. The distinction is a population prediction; no finite-exposure resolving power or physical target-selection mechanism has been established.
