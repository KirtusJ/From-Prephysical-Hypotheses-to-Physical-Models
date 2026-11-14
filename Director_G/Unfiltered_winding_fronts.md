# Reading a winding phase where two unfiltered fronts meet

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

At sufficiently large even $D$ coprime to three, a sharp launch and a calibrated terminal site-and-rail detector at one chosen clock distinguish two specified cubic phase responses that give identical sharp-launch records on the line. Estimating the lone-port contrast at fixed error takes order $t^{2/3}$ independent launches. The first meeting of the ballistic fronts on an even ring gives opposite changes on the two rails. Their sum measures the coherent fraction in a specified mixture, and their difference supplies a winding cosine. A later read in the interior gives a contrast bounded away from zero as the ring grows. These are predictions per original launch. No intermediate path is measured or removed. [Filtered ring comparison and word gains](Four_arc_gains_and_winding_records.md) · [Interior read and proof](Interior_winding_read.md)

## Which probabilities are being compared?

Take a ring of $2D$ sites, with initial rail $R$ at site zero. An outgoing $R$ step advances one site and $L$ retreats one. Let $z,g$ generate $C_2\times C_q$, and assign the four incoming/outgoing arc gains $(RR,RL,LR,LL)=(1,g,1,zg)$. In the coherent models each arc carries its character value divided by $\sqrt 2$. A terminal probability is the squared modulus of the sum over words reaching the named port. The admissible characters under comparison obey $\chi(z)=-1$, so they all have a unitary coin. The alternative fair count assigns $2^{-t}$ to each length-$t$ word. Their convex mixtures refer to single-launch probabilities. Launch independence is an additional assumption in the sampling estimates.

Write $A_t(y,r)$ for the real signed Hadamard amplitude on the **line**. Each step receives the factor $1/\sqrt2$ and each $LL$ arc contributes a minus sign. A word ending at $y$ has $(t-y)/2$ left steps. Its additional phase $\chi(g)^{(t-y)/2}$ is common at that line endpoint. At a ring port where only the two lifts $y,y-2D$ are accessible, put $a_r=A_t(y,r)$, $b_r=A_t(y-2D,r)$ and $u=\chi(g)^D$. Then exactly
$$p_\chi(y,r)=a_r^2+b_r^2+2\operatorname{Re}(u)a_rb_r. \tag{1}$$
Changing $\chi(g)$ is invisible on the line in this preparation. A ring identifies the two endpoints and makes their relative phase accessible. Observing the lifts separately removes this cross term. The terminal rail remains available in the proposed read.

## The first meeting of the ballistic fronts

Let $v=1/\sqrt2$ and choose $t$ nearest to $\sqrt2D$ among the integers with the parity of $D$. Then $|D-vt|\le v$, and near the antipode there are exactly two possible lifts for large $D$. Put $\eta=(D-vt)t^{-1/3}$, $\alpha=(4\sqrt2)^{1/3}$ and $h=\alpha t^{-1/3}\operatorname{Ai}(\alpha\eta)$. Define $\sigma=(-1)^t$. At the antipode the two rail probabilities satisfy
$$p_\chi(D,R)=(3+\sigma\operatorname{Re}u)h^2+O(t^{-1}),\qquad
p_\chi(D,L)=(1-\sigma\operatorname{Re}u)h^2+O(t^{-1}). \tag{2}$$
If the leading $L$ amplitude cancels exactly between the two unit phases, its probability is $O(t^{-4/3})$. The leading sum on the two rails is $4h^2$, independent of winding. Smaller position-only contrasts can survive at finite times. The fair-count probability at this site is exponentially small in $t$. Indeed reaching either lift requires a displacement of magnitude $D=vt+O(1)$ in $t$ independent fair steps. The same exponential bound holds for a window $O(t^{1/3})$ wide by the binomial tail bound.

For the derivation use the inverse transform with $e^{-iky}$ and
$$M(k)=\mathrm{diag}(e^{ik},e^{-ik})\,H,\qquad
H=2^{-1/2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}.$$
Its eigenvalues are $e^{i\omega(k)},-e^{-i\omega(k)}$, where $\omega(k)=\arcsin(v\sin k)$. At zero the projectors are $(I\pm H)/2$. The cubic expansion is $\omega(k)=vk-v(1-v^2)k^3/6+O(k^5)$. At the right front the first eigenvalue is stationary at zero, and at the left front the second eigenvalue contributes the factor $\sigma$. The chart translated by $\pi$ contributes equally on matched parity because $M(k+\pi)=-M(k)$. It cancels on the other parity. Hence, in rail order $(R,L)$, the two line amplitudes have the following leading terms, with uniform absolute error $O(t^{-2/3})$ for bounded scaled offsets:
$$
\begin{aligned}
A_t(y)&=\alpha t^{-1/3}\operatorname{Ai}\!\left(\alpha(y-vt)t^{-1/3}\right)(1+v,v)
   +O(t^{-2/3}) &&(y\simeq vt),\\
A_t(y)&=\sigma\alpha t^{-1/3}\operatorname{Ai}\!\left(\alpha(-y-vt)t^{-1/3}\right)(1-v,-v)
   +O(t^{-2/3}) &&(y\simeq -vt).
\end{aligned}
$$
The rescaling $k=\alpha t^{-1/3}s$ makes the cubic coefficient $1/3$ in absolute value. The uniform Airy expansion applies at these two simple cubic stationary points. Away from them the phase derivative is bounded away from zero and integration by parts controls the remainder. Equation (2) follows from (1), using $2(1+v)(1-v)=2v^2=1$. Sunada and Tate give the uniform amplitude expansion in Proposition 3.1 and the corresponding wall probability in Theorem 1.3. The projector factors above use this walk's rail convention. [Sunada and Tate, *Asymptotic behavior of quantum walks on the line*](https://arxiv.org/pdf/1108.1878)

## What the two rails identify

Suppose a common preparation has fair-count weight $c$ and coherent weights $b_s$ for $\chi_s(g)=e^{2\pi i s/q}$, with $c+\sum_s b_s=1$. Define $\mathcal R,\mathcal L$ as the limiting antipode rates on the respective rails divided by $h^2$ on a sequence of fixed $D\bmod q$ and fixed parity. Both use the original number of launches as their denominator. Set
$$T=(\mathcal R+\mathcal L)/4,\qquad J_D=\sigma(\mathcal R-3\mathcal L)/4.$$
Then $T=1-c$ and $J_D=\sum_s b_s\cos(2\pi Ds/q)$. At $q=3$ with $D\equiv1$ or $2\bmod3$ this reads all three observable weights:
$$c=1-T,\qquad b_0=(T+2J_D)/3,\qquad b_1+b_2=2(T-J_D)/3. \tag{3}$$
For example, with even $D\equiv1\bmod3$, dividing by $h^2$ gives $(4,0)$ for the trivial winding character, $(5/2,3/2)$ for the unit conjugate pair, and $(0,0)$ for fair count in the limit. A conditional tally of the rail only among antipode arrivals loses the overall coherent fraction. If $D\equiv0\bmod3$, the two phases give the same distribution at every ring port at every clock.

For general finite $q$, suppose the same distribution of labels and the same assignment of $g$ can be carried from one circumference to the next. For each residue $j\bmod q$ take $D\to\infty$ in class $j$ with a fixed available parity, and correct the sign by that parity. The moments $J_j$ are the finite Fourier transform of the symmetric weights $\widetilde b_s=(b_s+b_{-s})/2$. Inverting gives $\widetilde b_s=q^{-1}\sum_{j=0}^{q-1}J_j\cos(2\pi js/q)$. Self-conjugate labels have their individual mass, and for every other pair the folded mass is $2\widetilde b_s$. A varying source would give different ensembles to the different rows of this inversion. Even with the stipulated common source, conjugation preserves every distribution here. A finite sequence of read times on one ring also suffices when $D$ is coprime to $q$. [Fixed-ring identification](Fixed_ring_winding_weights.md)

A separate designation of the generator and physical frequency data are needed to give the ordinary embedding empirical meaning. [Compatible mixtures under sheet refinement](Mixed_refinement_records.md)

## How often a launch gives evidence

For $q=3$ and even $D\equiv1\bmod3$, the single $R$ port separates the two coherent responses by order $t^{-2/3}$. Enlarge the read to the final event $(D+k,R)$ for even $k$ with $8|k|^3\le t$. For phases with winding real parts $m_1,m_2$, its probability difference is
$$
\frac{(m_1-m_2)\alpha^2}{2}t^{-1/3}
\int_{-1/2}^{1/2}\operatorname{Ai}(\alpha z)\operatorname{Ai}(-\alpha z)\,dz
+o(t^{-1/3}).
$$
The Airy arguments at the two lifts are $\alpha(\eta+kt^{-1/3})$ and $\alpha(\eta-kt^{-1/3})$. Uniformity permits summation. The parity mesh gives the factor $1/2$ and $\eta\to0$. Both Airy factors are positive throughout the integration interval, which lies above the first real zero. [NIST, DLMF Table 9.9.1](https://dlmf.nist.gov/9.9#T1)

For a fixed error probability below $1/2$ and the two stated coherent alternatives, the window requires $\Theta(t^{1/3})$ independent launches, versus $\Theta(t^{2/3})$ using the lone $R$ port. Each estimate uses the corresponding binary event and all misses. Its success probability and its probability gap have the same order. A threshold halfway between the hypotheses and a binomial variance bound give sufficiency. With $o(1/p)$ launches the all-miss transcript has probability tending to one under both alternatives, giving the lower bound at each scale. Each launch still occupies $\Theta(D)$ ticks. A later, spatially resolved read can do better in number of launches. [Interior detector and its resolution requirements](Interior_winding_read.md)

## Reproduction and physical scope

Run the linked checkers with Python 3, passing a fresh output directory to each. The first folds exact signed line amplitudes, compares against direct evolution on the six-sheet cover on small rings, and records the fair count, both rails, parity misses, blind circumferences and the finite summed-rail residual. The companion tests the interior read. The time dependence and limits are mathematical predictions. There is no observed frequency here that selects either character, and the initial choice of probability-law family remains a premise. [Front checker](check_unfiltered_winding.py) · [Front data](results/unfiltered_winding.json) · [Interior checker](check_interior_winding.py) · [Interior data](results/interior_winding.json)
