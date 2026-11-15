# What one terminal site reveals about a rail tag

Prepare one of two opposite rail polarizations with equal probabilities at the same known site. In a homogeneous two-rail reflection walk on the integer line, a decision using just the side of the launch site attains the best probability of guessing the tag from one terminal position at any fixed positive tick. The identity below holds at individual lattice sites, including interference zeros. Long-flight weak limits concern velocity windows and do not by themselves decide this question. [Konno](https://arxiv.org/abs/quant-ph/0206103) · [Grimmett, Janson and Scudo](https://arxiv.org/abs/quant-ph/0309135)

Write the real coin as $C=\left(\begin{smallmatrix}a&b\\ b&-a\end{smallmatrix}\right)$, $a^2+b^2=1$. Stream the top rail one site right after applying $C$ and the bottom rail one site left. Let $K=K_t(x)$ be the real two-column arrival matrix, $t\ge1$. With input $\rho_\pm=(I\pm\eta C)/2$, $0\le\eta\le1$, the ordinary probabilities satisfy, when $a\ne0$,

$$
 P_+(x)-P_-(x)=\eta\,\operatorname{tr}(C K^T K)
 =\frac{\eta x}{a t}\,[\operatorname{tr}K]^2 .
$$

For $a>0$, choosing the positive tag on the right and the negative tag on the left is a maximum-likelihood decision at each site. Reverse the labels for $a<0$. At $x=0$, and at any other tied site, either decision gives the same equal-prior success. For $a=0$, the walk exchanges the rails at each tick. On even ticks it returns to the starting site and on odd ticks the two sharp directions have equal weights for either tag. The site then carries no tag information. These statements assume a single free flight with faithful terminal position and no intermediate read.

**Proof.** Set $U(z)=\operatorname{diag}(z,z^{-1})C$, so $K=[z^x]U(z)^t$. With $Z=\operatorname{diag}(1,-1)$, the trace derivative and cyclicity give
$$
 z\partial_z\operatorname{tr}(U^t)=t\operatorname{tr}(ZU^t),\qquad
 x\operatorname{tr}K=t(K_{11}-K_{22}).
$$
Equivalently, sum signed closed rail words contributing to the trace. Moving the marked final letter cyclically through the $t$ positions leaves the weight unchanged. The sum of its right-minus-left signs is the displacement $x$.

The determinant of $U$ is $-1$. Cayley–Hamilton writes $U^t=A_t U + A_{t-1}I$ with scalar Laurent polynomials, $A_0=0,A_1=1$. Hence for real coefficients $p,q,d$ the arrival matrix has rows $(d+ap,bp)$ and $(bq,d-aq)$. Multiplication gives $\operatorname{tr}(C K^T K)=(p+q)(2d+a(p-q))=(p+q)\operatorname{tr}K$. Since $K_{11}-K_{22}=a(p+q)$, the identity follows.

For the Hadamard coin and the [recorded preparations](A_rail_measurement_from_four_free_steps.md), the all-odd [half-line law](Which_side_a_tagged_rail_reaches.md) gives optimal success $1/2+\eta_m/(2\sqrt2)$ at every odd clock. The sign of the side retains the best equal-prior one-guess score. A site can still carry information about the strength of that guess.

For example, with threshold $m=1$ and five ticks the exact conditional probabilities on sites $(-5,-3,-1,1,3,5)$ are $(1,3,12,12,63,5)/96$ on the positive tag and their reversal on the negative tag. At sites $+1,+3,+5$ the likelihood ratios are $1,21,5$. With a positive-tag prior of $1/10$, the best full-site rule says positive only at $+3$ and scores $15/16$. The best side-only rule always says negative and scores $9/10$. Changing the prior here describes a reweighted decision experiment. The native stopped preparation from the mixed input supplies balanced tags.

The [exact checker](check_terminal_site_decision.py) propagates both columns, retaining zeros and ties, with integer numerators. It checks the trace current, the contrast identity and normalization for all reachable-parity sites through 400 Hadamard ticks and for additional reflection coins, including degenerate cases. The [Lean calculation](lean/SiteTraceDecision.lean) checks the Hadamard matrix factorization and its implication given the trace current. The Laurent-polynomial argument supplies the current identity for all times. These are mathematical checks under ordinary quantum probabilities.

Kirtus Justus, Theoretical Physicist, Port Coquitlam, British Columbia, Canada, holds scholarly responsibility. OpenAI Codex derived and checked the finite-site identity and its decision limits.
