# What four success records can identify on five sheets

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [five-sheet walk](Native_preparations_and_probability_embeddings.md) predicts two possible success rates for one repeated position-and-direction test after a herald. Four subsequent reads suffice to identify both rates and their proportions from *rational* prefix frequencies, under a stated persistence assumption. The number of possible rates can be unknown, even infinite. Three reads admit an explicit rival with three different rates. This is an inference available from proposed observations. The numbers below come from the walk calculation.

## One fifteen-tick schedule

Launch at site \(0\), right rail, sheet 0. Each tick adds the departure site to the sheet modulo five, applies the real Hadamard coin with a minus on \(L\to L\), and streams along the output rail. On the line, at tick 3 read the site and rail while leaving the sheet coherent. The herald \(H\) is \((-1,L)\). For each heralded launch, at ticks 6, 9, 12 and 15 read the same instrument. On the surviving prefix the constructive output from \((x,L)\) is \((x-1,L)\). Thus the successive targets are sites \(-2,-3,-4,-5\), each on \(L\). At the first failure the prefix ends. There is no need to reset the walker, exchange a rail or measure a sheet between reads. A common schedule retains earlier records even when a later target fails. [Three-tick instrument and output table](Records_and_complex_structure.md)

Let \(S_k=\Pr(\text{first }k\text{ constructive outcomes}\mid H)\), including \(S_0=1\). All four probabilities have the same initial-herald denominator. Report the incident number of launches, the herald frequency and every first failure or unresolved read. An unresolved outcome gives lower and upper bounds on the relevant prefixes. Conditioning instead on survivors of each new test gives the ratios \(S_{k+1}/S_k\).

| Constructive prefix length | Clock | Conditional prefix \(S_k\) | Joint herald and prefix per incident launch |
|---:|---:|---:|---:|
| 0 | 3 | 1 | \(1/4\) |
| 1 | 6 | \(1/8\) | \(1/32\) |
| 2 | 9 | \(1/32\) | \(1/128\) |
| 3 | 12 | \(5/512\) | \(5/2048\) |
| 4 | 15 | \(13/4096\) | \(13/16384\) |

For the kinematic calculation let \(T\) translate the five sheets. Up to a common translation and sign, the unnormalized herald vector has integer coordinates \(d=(T-T^{-1})|0\rangle\). Each successful continuation applies \(B=T+T^{-1}\) with a common translation, sign and denominator \(\sqrt8\). Writing \(C_k=\|B^kd\|^2\), the signed path calculation gives \(C_0,\ldots,C_5=2,2,4,10,26,68\). The ordinary projection probabilities therefore give \(S_k=C_k/(2\,8^k)\). This computes the comparison values while leaving the instrument's observed frequencies free.

## What an observed equality implies

Assume the same heralded population admits a probability measure \(\mu\) on \([0,1]\) with \(S_k=\int x^k\,d\mu(x)\) at every prefix length to which the inference is applied. One sufficient mechanism is a persistent success probability \(x\) within a launch, with conditional chance \(x\) of another success after every successful prefix. Full independence of all outcomes after a failure is unnecessary. A single positive contraction \(A\) with \(S_k=\langle v,A^k v\rangle\) and unit \(v\) also suffices by its spectral measure. For the stipulated walk on the heralded sheet subspace this applies with \(A=B^2/8\). Operationally, extendibility of this moment description to future prefixes is a substantive assumption about the apparatus. The check itself uses records through tick 15. Related results treat repeated nondemolition measurements and finite moment identification. [Bauer and Bernard](https://doi.org/10.1103/PhysRevA.84.044103) · [Curto, Fialkow and Möller](https://arxiv.org/abs/math/0610882)

Set \(P(x)=64x^2-24x+1\). The observable
\[
 R=S_0-48S_1+704S_2-3072S_3+4096S_4=\int P(x)^2\,d\mu(x)
\]
is nonnegative in this class and vanishes at the tabulated probabilities. A single complete heralded run with exactly \(j\) initial successes, capped at four, receives score \(1,-47,657,-2415,1681\) for \(j=0,1,2,3,4\) respectively. Its mean is \(R\). Equivalently, one can score each original launch, assigning zero to every known failed herald, for mean \(\Pr(H)R\). A positive measured herald yield is needed for conditioning.

At exact \(R=0\) the entire measure is supported on the two roots
\[
 q_-=(3-\sqrt5)/16,\qquad q_+=(3+\sqrt5)/16 .
\]
The measured \(S_1=1/8\) puts weight \((\sqrt5-1)/(2\sqrt5)\) at \(q_+\) and the remainder at \(q_-\). These facts fix every subsequent \(S_k\) within the same model. In particular the predicted tick-18 prefix is \(17/16384\) per herald, and the next-success probability after four successes is \(17/52\). Since \(0<q_-<q_+<1\) and both weights are positive, \(S_{k+1}/S_k\to q_+\). No trial needs an exactly pure sector to test the four frequencies. The data distinguish an ordered pair of numerical rates. Simultaneously interchanging the cyclotomic labels assigned to those sectors preserves every native transcript, including this score.

## Which competing mechanisms survive

* **Three prefixes.** Put weights \(41/88,216/407,1/296\) at success probabilities \(0,11/48,1\), respectively. These positive weights sum to one. The resulting \(S_1,S_2,S_3\) equal all three target values. Thus even the full first-failure distribution up to tick 12 agrees. At tick 15 this rival predicts \(119/24576\) per herald, exceeding \(13/4096\) by \(41/24576\). This establishes that four is the shortest sufficient horizon for this success-prefix observation in the unrestricted moment class. Other resolved output channels could carry additional information.
* **An apparatus with memory.** Keep a counter of the successes since the herald. Give the first four steps conditional success chances \(1/8,1/4,5/16,13/40\), then declare failure with certainty at the fifth step. Its whole observed prefix panel through tick 15 agrees, while its fifth joint prefix is zero. One may copy the native conditional distribution over the distinct failure ports until that clock if they are also read. A finite panel does not establish the persistence premise.
* **Finite precision.** For the true moment model and any \(\delta>0\), the measure of rates at distance at least \(\delta\) from both roots is at most \(\min(1,R/(80\delta^2))\). Indeed the farther root is at distance at least \((q_+-q_-)/2=\sqrt5/16\), and \(P(x)^2=4096(x-q_-)^2(x-q_+)^2\). Use a simultaneous upper bound on \(R\) from the joint prefix data. Even a very small nonzero tolerance cannot certify the limiting survivor rate. Adding weight \(\varepsilon\) at \(x=1\) and multiplying the target measure by \(1-\varepsilon\) changes every positive prefix by less than \(\varepsilon\); the limiting next-success probability then becomes one. Its unnormalized contribution to the square residual is \(1681\varepsilon\). Such a tail cannot be discarded.

At finite precision the fifth prefix still has a checkable prediction. In the moment class, Cauchy–Schwarz gives
\[
 |64 S_5-24 S_4+S_3|=|\mathbb E[X^3P(X)]|
 \le\sqrt{S_6 R}\le\sqrt{S_4 R}.
\]
Thus the four observed prefixes bound the next one without assuming a two-point support or excluding rare surviving rates.

There is an algebraic reason rational prefix frequencies can identify irrational persistent rates. Any finite menu using only deterministic relabeling, merging, rational randomization and equalities among otherwise unrestricted record populations defines a rational polytope. Introduce one normalized probability vector for each context and write each comparison as a linear equation with rational coefficients. A uniquely fixed single rate is rational because a nonempty bounded rational polytope has rational vertices. Here multiplicative prefix survival supplies the extra structure that relates those rational observations to latent rates. This establishes an operational consequence of persistence. The physical origin of the record law and the choice of an absolute sheet character remain open.

The [path replay](check_five_sheet_success_spectrum.py) sums every three-direction word on the named site, rail and sheet, retaining all output signed rows and branch probabilities, and checks the moment identity, the fifth prediction and the three rivals. A separate [Lean calculation](lean/FiveSheetSuccessSpectrum.lean) verifies the scaled finite identities. The [result record](results/five_sheet_success_spectrum.json) contains model outputs. No physical outcomes were used.
