# How close to an equal launch can the four journal orders reach?

Kirtus Justus directed the research. OpenAI ChatGPT (Director G) derived the launch construction and the conditional calibration bound. 16 November 2026, B.C. Pacific Time (PCT, UTC−07:00).

**The four site orders exclude an exactly equal rail mixture, yet allow a launch arbitrarily close to it.** This statement concerns eight cells in Fig. 7(c) of Lorz et al. A quantitative lower bound on launch polarization would require an independent bound on how strongly the displayed value can respond to a change in optical intensity. The journal figure supplies the four displayed gaps used below. [Journal figure, page 8](https://physik.uni-paderborn.de/fileadmin-nw/physik/Arbeitsgruppen/integrierte-quantenoptik/publications/2019/PhysRevResearch.1.033036.pdf#page=8) · [Palette extraction, numerical-panel control and sensitivity to the color bands](Four_site_orders_in_the_journal_figure.md)

## A family tending to the equal mixture

Use the ten-site ideal balanced walk, localized at site 2, and the outgoing rail convention in the figure calculation. Let $B_{tm}$ carry its two input rails to the two rails at site $m$ in round $t$. For launch density $\rho$ and a time-independent analyzer effect $H_m$ at each site, the latent intensity per unit launch power is $x_{tm}=\operatorname{tr}(H_m B_{tm}\rho B_{tm}^\dagger)$. A common nondecreasing response within each round preserves the direction implied by a strict displayed order. [Walk and order conventions](Four_site_orders_in_the_journal_figure.md)

Take $\rho(z)=(I+z Z)/2$, where $Z=\operatorname{diag}(1,-1)$. Set $H_0=A_0/4$ and $H_4=A_4(z)/4$ with

$$
A_0=\begin{pmatrix}2&0\\0&1\end{pmatrix},\qquad
A_4(z)=\begin{pmatrix}1+z/2&3iz\\-3iz&2+z/2\end{pmatrix}.
$$

For every $0<z<1/134$ these effects lie between $0$ and $I$. The eigenvalues of $A_4$ lie between $1+z/2-3z$ and $2+z/2+3z$ by the Hermitian row-sum bounds. Each candidate uses the same analyzer pair at all four rounds. The analyzer at site 4 varies across candidates.

| Round | Brighter minus dimmer | Four times the latent difference |
|---:|---|---|
| 2 | site 4 minus site 0 | $z/8$ |
| 6 | site 4 minus site 0 | $17z/128-11z^2/32$ |
| 8 | site 0 minus site 4 | $z(1-134z)/512$ |
| 14 | site 4 minus site 0 | $767z/32768+499z^2/16384$ |

All four differences are positive on the stated open interval. At $z=1/134$ round 8 ties and above that point its ordering reverses in this family. As $z$ tends to zero, the trace distance to $I/2$ tends to zero as $z/2$, and the purity tends to $1/2$ as $(1+z^2)/2$. Exactly at zero, the signed identity for the equal mixture excludes the four strict orders for *every* fixed analyzer pair. [Equal-mixture proof](Four_site_orders_in_the_journal_figure.md) · [Polynomial and boundary checks](check_circle_launch_bias.py)

Both latent intensities in each pair are positive because the launch and effects are positive definite and each selected transfer is nonzero. Choose a displayed value in each of the two corresponding bands. Linear interpolation from the origin through the ordered pair of input-output points gives a common increasing response on the sampled interval for that round. The slopes may grow without bound as $z$ decreases. This construction fixes eight displayed values. It leaves the other cells, joint normalization of a full predicted panel, and feasibility with one response function shared across rounds unresolved.

## What an independent response calibration would buy

For general $\rho=(I+\mathbf r\cdot\boldsymbol\sigma)/2$, use the Pauli order $(X,Y,Z)$ and $\|\mathbf r\|\le1$. Write $d_t=x_{t,\mathrm{brighter}}-x_{t,\mathrm{dimmer}}$ in the four directions above and $J=\sum_t w_t d_t$, with $w=(1545,1648,7444,1280)$. Give the brighter site sign $s_{tm}=+1$ and the dimmer site sign $-1$. Direct propagation of both input columns gives

$$
\sum_t s_{t0}w_t B_{t0}\rho B_{t0}^\dagger
=\frac{(M\mathbf r)\cdot\boldsymbol\sigma}{8},\qquad
\sum_t s_{t4}w_t B_{t4}\rho B_{t4}^\dagger
=-\frac{(M\mathbf r)\cdot\boldsymbol\sigma}{8},\qquad
M=\begin{pmatrix}2057&0&0\\0&1826&-3301\\0&1244&1826\end{pmatrix}.
$$

The scalar output coefficient vanishes for every input, and the identity input contributes zero to both sums. The checker verifies each entry using integer rail amplitudes and exact fractions. Each signed site operator has eigenvalues $\pm\|M\mathbf r\|/8$. An effect between $0$ and $I$ collects at most its positive eigenvalue. Choosing the positive spectral projector independently at each site attains both maxima at once.

Consequently the exact maximum of $J$ at fixed launch is $\|M\mathbf r\|/4$. To maximize over directions at a given radius, the lower $2\times2$ block of $M$ has squared singular values with sum $19{,}112{,}689$ and product of singular values $7{,}440{,}720$. Its larger singular value is $(\sqrt{33{,}994{,}129}+2057)/2$, greater than the remaining axial singular value $2057$. Thus

$$
J\le K\|\mathbf r\|,\qquad K=\frac{\sqrt{33{,}994{,}129}+2057}{8}\simeq985.931055 .
$$

Suppose independent calibration places an upper Lipschitz bound $L_t>0$ on the common map from the absolutely normalized $x$ to the displayed value at both sites in round $t$. This bound must cover the intervening intensity interval, launch power, response gain and any display normalization. The smallest gaps from the journal bands at the four-unit maximum-channel allowance are $g=(1,8,7,24)/256$. The two inequalities $g_t\le L_t d_t$ and $J\le K\|\mathbf r\|$ imply

$$
\|\mathbf r\|\ge\frac{1}{K}\sum_t\frac{w_tg_t}{L_t}.
$$

For a common cap $L$, the lower bound is $97557/(256 K L)\simeq0.386520/L$. A measured cap below $97557/(256K)$ would be incompatible with every launch in this model, since the radius cannot exceed one. The maximization of the latent weighted score is sharp. Achieving its maximum need not reproduce the four individual display gaps, much less the full panel. A source specification, an unscaled detector slope or the color legend alone supplies no such effective cap. The figure also leaves open launch preparation, the actual site effects, and whether the two channels shared a response. Stage 1 Initial External Grounding and physical identification remain open.

Run the checker from the repository root with Python, PyMuPDF and Pillow. It reads the pinned journal PDF, recovers the four displayed gaps and tests the open interval, its boundary and the transfer bound. [Checker](check_circle_launch_bias.py) · [Exact output](circle_launch_bias_output.json)

`python -I -B Director_G/persistent_walk/check_circle_launch_bias.py lorz.pdf`
