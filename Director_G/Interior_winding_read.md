# A free ring read with a fixed probability gap

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Launch at one well on the right rail and run the balanced walk freely for one tick per ring well. In a fixed interval of final positions, two windings arrive with signed amplitudes of order $n^{-1/2}$. Their signs vary between neighboring reachable wells. A fixed lookup on the final right-rail record collects enough constructive products to distinguish two winding characters with a probability gap bounded below as the circumference grows. A second frequency from the same records separates an admixture of ordinary fair path counting. These are predictions within a stipulated family of probability embeddings. The preparation and readout supply no measured frequency or independent rule choosing a member. [Four arc gains and winding indices](Four_arc_gains_and_winding_records.md)

## Experiment and exact signals

Take $N=2D$ wells, $D\equiv4\bmod 12$ and $n=N$ ticks. Set the RR, RL, LR, LL gains to $1,g,1,zg$ respectively in $C_2\times C_3$, where $z$ has order two and $g$ order three. Both characters satisfy $\chi(z)=-1$. The first sends $g$ to $1$, the second to $e^{2\pi i/3}$ or its conjugate. The fair counting law assigns mass $2^{-n}$ to each word. All probabilities below use the number of original sharp $(0,R)$ launches as denominator. There is no filtering during propagation.

Let $I=[21/50,11/25]$. The event $E$ accepts final rail R and an integer representative $x\in nI$ with $x\equiv n\bmod2$. Every such well has exactly two allowed displacements, $x$ and $x-N$, since a word reaches only sites of its parity in $[-n,n]$. For each lift let $a$ and $b$ be its real, normalized, line R-to-R amplitudes computed with the ordinary signed Hadamard step. These are the signed word sums with each LL carrying a minus sign, times $2^{-n/2}$. In the gain model the two sums also carry common phases $\chi(g)^{(n-x)/2}$ and $\chi(g)^{(n-x)/2+D}$. For any subset $S$ of these wells write

$$U_S=\sum_S(a^2+b^2),\qquad K_S=\sum_S ab,\qquad C_S=2^{-n}\sum_S\left[\binom{n-1}{(n-x)/2}+\binom{n-1}{(n-x)/2+D}\right].$$

The last step is R, so only the previous $n-1$ steps can be left. The probabilities of $S$ are exactly $U_S+2K_S$, $U_S-K_S$, and $C_S$, respectively. The conjugate characters give identical values. For other circumferences the general signal is $U_S+2\operatorname{Re}(\chi(g)^D)K_S$.

Before the run, form $E_+=\{x\in E:a b>0\}$ from the unfiltered signed line recurrence. This event depends on size, clock and coin, and uses neither the unknown character nor the observed outcomes. Every trial supplies the two indicator values $\mathbf{1}_E,\mathbf{1}_{E_+}$. Failures of both, including other positions and the left rail, have value zero.

**Claim.** Along the stated progression, $U_E$ tends to a positive constant, $K_E\to0$, $C_E\to0$ exponentially, and $\liminf K_{E_+}>0$. In particular the two pure squared laws differ by $3K_{E_+}$ on $E_+$. The fixed numerical interval was chosen to keep the frequencies used below away from lattice resonances. Its endpoints do not tune the experiment to a finite-sample result.

## Stationary amplitudes in native conventions

Use inverse Fourier coefficient $e^{-iky}$ and the momentum matrix

$$M(k)=\begin{pmatrix}e^{ik}&0\\0&e^{-ik}\end{pmatrix}\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad \omega(k)=\arcsin(\sin k/\sqrt2).$$

The eigenvalues are $e^{i\omega}$ and $-e^{-i\omega}$. The RR entry of the first spectral projector is

$$[P_+(k)]_{RR}=\frac{e^{ik}/\sqrt2+e^{-i\omega}}{2\cos\omega}=\frac{1+\omega'(k)}2,\qquad
\omega'(k)=\frac{\cos k}{\sqrt{1+\cos^2 k}}.$$

The imaginary part cancels since $\sin\omega=\sin k/\sqrt2$. The other RR entry is $(1-\omega')/2$. The identity $M(k+\pi)=-M(k)$ exactly doubles the half-zone Fourier integral when $y\equiv n\bmod2$ and annihilates the other parity.

For $0<u<1/\sqrt2$ set

$$\kappa(u)=\arccos\frac{u}{\sqrt{1-u^2}},\qquad
\psi(u)=\omega(\kappa(u))-u\kappa(u),\qquad
c_\pm(u)=\frac{4(1\pm u)/2}{\sqrt{2\pi|\omega''(\kappa(u))|}}.$$

On $(-\pi/2,\pi/2)$ the phase for $y=un$ has its two critical points at $\pm\kappa(u)$ on the **positive** band. The negative band has none. The curvature at $+\kappa$ is $\omega''(k)=-\sin k/(1+\cos^2 k)^{3/2}<0$, giving phase correction $-\pi/4$. The partner point contributes its conjugate. For $y=-un$, the **negative** band contributes $(-1)^n$ times the conjugate phase, with its own weight $(1-u)/2$ at both points. The other band has no critical point there. Including parity doubling, the line amplitudes on matched sites are

$$A_n(un)=n^{-1/2}c_+(u)\cos(n\psi(u)-\pi/4)+O(n^{-1}),$$
$$A_n(-un)=(-1)^n n^{-1/2}c_-(u)\cos(n\psi(u)-\pi/4)+O(n^{-1}).$$

The remainder is uniform for $u$ in the two compact speed intervals $I$ and $1-I$. Indeed the saddles stay separated from one another and from the half-zone boundaries and their second derivatives stay away from zero. Use smooth cutoffs near each saddle and the one-dimensional nondegenerate stationary-phase formula, then integrate the remaining nonstationary pieces by parts once. These formulas retain the odd-clock sign when used for adjacent-clock controls. The theorem uses even $n$. Sunada and Tate treat the ballistic interior of the one-dimensional walk by stationary phase in their coin conventions. [Sunada and Tate, §2](https://arxiv.org/pdf/1108.1878)

## Summing interference without a random-phase assumption

Set $r=x/n$, $s=1-r$, $h=n\psi(r)-\pi/4$ and $j=n\psi(s)-\pi/4$. A matched terminal site advances $r$ by $2/n$. Since $\psi'(u)=-\kappa(u)$, the nonconstant frequencies in $\cos^2 h$, $\cos^2 j$ and $\cos^2 h\cos^2 j$ have limiting phase increments of the forms

$$\pm4\kappa(r),\quad \pm4\kappa(s),\quad 4(\pm\kappa(r)\pm\kappa(s)).$$

For $\cos h\cos j$ the increments are $2(\pm\kappa(r)\pm\kappa(s))$. All stay a fixed distance from $2\pi\mathbb Z$ on $I$. Indeed $0<\kappa(s)<\kappa(r)<\pi/2$, and $\pi/2<\kappa(r)+\kappa(s)<\pi$. For the strict lower bound on the sum, use

$$\cos^2\kappa(r)+\cos^2\kappa(s)
\leq\frac{121}{504}+\frac{841}{1659}<1.$$

Both angles are acute. Their difference therefore lies strictly between 0 and $\pi/2$. Compactness supplies uniform separation. For an actual increment $\Delta_\ell=n(\phi(r+2/n)-\phi(r))$ the discrepancy from $2\phi'(r)$ is $O(1/n)$ and neighboring increments differ by $O(1/n)$. For a fixed smooth weight $w$, sum
$w_\ell(e^{in\phi_\ell}-e^{in\phi_{\ell+1}})/(1-e^{i\Delta_\ell})$ by parts. Its endpoint terms are bounded and the coefficients have bounded total variation. Every such oscillatory sum is $O(1)$, including on the subsequence and rounded interval endpoints used here.

The parity-matched Riemann sums have density $n/2$. The constant Fourier terms of $\cos^2 h$ and $\cos^2 h\cos^2 j$ are $1/2$ and $1/4$. With the preceding uniform remainder this yields

$$U_E\longrightarrow\frac14\int_I[c_+(r)^2+c_-(1-r)^2]\,dr>0,\qquad K_E\longrightarrow0,$$
$$n\sum_E a^2 b^2\longrightarrow L=\frac18\int_I c_+(r)^2 c_-(1-r)^2\,dr>0.$$

There is a constant $M>0$ with $\max_E|ab|\le M/n$ for all sufficiently large $n$. Hence $\liminf\sum_E|ab|\ge L/M$. The identity $2K_{E_+}=\sum_E|ab|+K_E$ proves the lower bound. In the fair model any qualifying word has total displacement of absolute value at least $(21/50)n$. For the fair $\pm1$ sum, $\mathbb E e^{tS_n}=(\cosh t)^n\le e^{nt^2/2}$, so $C_{E_+}\le C_E\le2e^{-n(21/50)^2/2}$. This completes the claim.

## What the two records determine

Let $p_0,p_1,1-p_0-p_1$ be launch-mixture weights for the trivial-winding squared law, conjugate-pair squared law and fair count. Write $\beta=p_0+p_1$, $\eta=p_0-p_1/2$. The predicted rate in any of the two recorded events is

$$P(S)-C_S=(U_S-C_S)\beta+2K_S\eta.$$

For $S=E,E_+$ the determinant is $2[(U_E-C_E)K_{E_+}-(U_{E_+}-C_{E_+})K_E]$. It has positive liminf because $U_{E_+}\le U_E$, $C_{E_+}\le C_E$, and the claimed limits hold. The matrix entries remain bounded, so the inverse is uniformly bounded for sufficiently large $D$. The two unconditional rates then determine $\beta,\eta$ and the three stipulated weights, up to the exact conjugacy ambiguity. For a larger phase family this experiment accesses its weighted cosine moment and coherent fraction, subject to the same two-lift model. Multiple mixtures can share those quantities.

For fixed desired weight accuracy and confidence, sufficiently many independent launches suffice uniformly in large $D$ by concentration for the two bounded indicators. The constants depend on the chosen accuracy, risk and response matrix. Each launch still takes $2D$ ticks. The lookup can be prepared in $O(n^2)$ integer additions on signed path counts of $O(n)$ bits by the elementary recurrence. The apparatus must implement the gain walk coherently, control the clock, and distinguish the accepted right-rail wells on the parity mesh, or implement an equivalent terminal mask. A detector reporting only membership in the entire interval loses the asymptotic character contrast there because $K_E\to0$. The theorem gives no guarantee for imprecisely registered masks, unknown loss, or an unobserved final rail. It does not determine the unrestricted physical probability law.

## Finite records

Selected probabilities for the positive-product right-rail event use all original launches.

| Ring wells and ticks | Reachable wells in $E$ | Trivial winding | Nontrivial winding | Two-rate determinant |
|---:|---:|---:|---:|---:|
| 80 | 1 | 0 | 0 | 0 |
| 152 | 2 | 0.00388212 | 0.00205357 | 0.0000195038 |
| 320 | 3 | 0.00814670 | 0.00286578 | 0.0000368219 |
| 632 | 7 | 0.00436979 | 0.00213445 | 0.0000297318 |
| 1472 | 14 | 0.01097622 | 0.00493026 | 0.0000357856 |
| 2408 | 24 | 0.01012622 | 0.00475401 | 0.0000394382 |

Run `python -B check_interior_winding.py NEW_DIRECTORY` from this directory. Exact per-site signed numerators, fair counts and the positive, negative and zero groups are retained for every panel, including empty windows, size-80's entirely negative window, adjacent odd clocks and trivial winding aliases when $3\mid D$. The small panels use an independent direct physical-ring propagation with three cyclic gain residues on both rails and check all three full normalization sums. The larger panels check the exact line norm. The JSON's leading-amplitude error and displayed probabilities are floating summaries; the integer fields reproduce every rate exactly. [Checker](check_interior_winding.py) · [All finite records](results/interior_winding.json)
