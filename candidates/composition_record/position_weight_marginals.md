# Can a distant choice of read time select the ordinary joint weights?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Mathematical and computational assistance from OpenAI Codex.

Hold the preparation and the near station's instrument fixed. Can switching the distant walker between an immediate read and three free ticks change the near station’s outcome frequencies? In the [heralded contact experiment](heralded_bell.md), this question distinguishes every fixed finite positive power of the modeled joint weights from ordinary weighting, except power one itself. There are two different tests depending on what the detector records before the power is applied. Both use the same signed walk, conditional preparation and two clock settings. This is an identification result within a family of readout laws. The choice of that family, physical isolation, setting independence and faithful local counting are premises.

## If each station records a binary sign

Take the conditional joint cells in the [terminal table](terminal_bell_read.md), raise each to the same power $q>0$, and normalize the four entries *at each setting pair*. Here $q=1$ gives ordinary weighting of the squared masses. With Alice reading immediately, changing Bob's read from immediate to late gives these respective probabilities for Alice’s positive sign:

$$
 m_{00}=\frac{1}{1+2^q},\qquad m_{01}=\frac{3^q+1}{3^q+7^q+2}.
$$

Equality reduces to $7^q+1=6^q+2^q$. For $q>1$ the increment from 6 to 7 is strictly larger than the increment from 1 to 2. For $0<q<1$ it is strictly smaller. Thus equality holds exactly at $q=1$. At $q=2$ the two rates are $1/5$ and $1/6$. Read as a target for a physical test, a fixed-setting local rate changes by $1/30$ under this rival. With ordinary weights it is $1/3$ at both settings.

The [probability projection](bell_projection/README.md) plots each four-cell row at its two local signed means and its signed correlation. For the squared cells the coordinates for settings 00 and 01 differ by $(1,1,1)/15$, so a camera looking along that direction places them at the same point. A second view shows the change in the local means. The exact coordinates in the figure make each overlap checkable.

## If the detectors first resolve whole wells

Now power each joint well-pair weight, normalize at the setting pair, then pool wells if desired. This ordering matters. For Alice's **immediate** read, Bob's late read has row multisets proportional to $(0,1,1,5,1)$ and $(2,10,2,2,0)$. The second multiset is twice the first up to permutation. Alice therefore retains the same marginal at either remote setting for every $q>0$. The binary-sign test above loses its discrimination at this resolution.

Instead have Alice read after three free ticks. Order her wells $-4,-2,0,2,4$. For an immediate Bob read order his wells $-1,+1$. For a late read use the same order as Alice. The paired matrices below count every occupied or dark joint well, pooling the two local rails:

$$
24P_{10}=\begin{pmatrix}2&0\\10&1\\2&1\\2&5\\0&1\end{pmatrix},\qquad
192P_{11}=\begin{pmatrix}
2&10&2&2&0\\10&43&11&23&1\\2&11&3&7&1\\2&23&7&19&5\\0&1&1&5&1
\end{pmatrix}.
$$

Write the near odds as $P_A(0)/P_A(+4)$. Both denominators are positive at finite $q>0$. The remote choices give $1+2^q$ and $(2^q+11^q+3^q+7^q+1)/(3+5^q)$. Equality is precisely equality of the power sums of the following integer vectors:

$$
 (11,7,3,2,1,0,0,0),\qquad (10,5,2,2,2,1,1,1).
$$

There is a direct proof from the detector rows. Set $v=(0,1,1,5,1)$ and $w=(1,5,1,1,0)$. The late zero-well row is $v+2w$, the late $+4$ row is $v$, and $w$ permutes $v$. At each of the three sites where both are positive, $(v_j+2w_j)^q$ strictly exceeds $v_j^q+(2w_j)^q$ for $q>1$ and is strictly smaller for $0<q<1$. The other sites give equality. Thus only $q=1$ preserves the odds, giving 3 under either remote choice. At $q=2$ the odds are 5 and $46/7$. The [Lean certificate](ContactPositionWeights.lean) checks the equivalent finite curvature inequalities. [Raw site and sign replay](check_position_powers.rs)

## What an experiment could establish

Use the same preparation flag before independent setting choices and identify each station’s outcome by a local clock and launch ID. Count all post-herald shots, including a prespecified outcome for a miss. The ideal numbers require the [specified instrument and loss conditions](terminal_bell_read.md). Comparing the near frequencies across remote settings tests marginal independence. The Bell score tests consistency with a shared local hidden variable across *all four* settings. A common probability rule and stable composition of records are additional requirements for interpreting either test. Causality-based restrictions on probability assignments have precedents for different families and quantum instruments. [Han and Choi, quantum probability assignment and relativistic causality](https://doi.org/10.1038/srep22986)

The finite positive exponent is the same for every occupied cell and setting. A support-only limit with zeros kept dark gives equal immediate-sign rates at the two remote settings but different late-well odds, 2 and $5/4$. A rule supported on the largest joint cell gives the same local deterministic result for each local setting regardless of the distant clock in this example. These limiting rules illustrate why the stated range of exponents matters.

There are also smooth, strictly increasing response functions outside the power family that agree on this entire experiment. Let $D$ be the finite set of ordinary normalized cells in the two tests together with 0 and 1. The function $f(p)=p+\epsilon\prod_{d\in D}(p-d)^2$ agrees with the identity at every sampled cell and differs elsewhere for nonzero $\epsilon$. Choose $|\epsilon|$ so that the absolute derivative of the added term stays below 1 on $[0,1]$. This preserves monotonicity and the endpoints. Conditioning, locality, or a finite figure alone cannot select a response on the untested continuum. No experimental frequencies for this apparatus have been supplied.
