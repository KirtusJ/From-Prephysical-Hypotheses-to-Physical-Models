# Three active contact pairs without an oriented rail phase

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Prepare three pairs of balanced paths, each subjected to the same conditional contact commutator. No local analyzer needs to know the phase between a single walker's two rails. A measurement that mixes *which copy* took a given rail can still witness entanglement produced by the contacts. A sharp central blank gives different raw scores if a fresh register is used for each pair or a single register is retained across all three. The experiment requires mutual coherence among copies prepared in the same laboratory, coherent local filtering, and characterized local analyzers. The candidate's classical multiplication table does not supply those operations. [Candidate register and its contact order](contact_flight.md)

## What is prepared and kept

The two laboratories A and B each launch three local balanced path qubits, initially a product across laboratories. In each pair apply \(g\) conditional on A's 1 rail, \(h\) conditional on B's 1 rail, then the two controlled inverses in the same order. The two control bits survive. Three of the four alternatives act as identity on the register. Alternative \(11\) translates the center by one, denoted \(T\). Coherent controlled permutations, isolation and ordinary quantum probabilities enter this extension. Define \(\gamma=\operatorname{tr}(\sigma T)\) for a blank state \(\sigma\); reversing the unit central shift conjugates \(\gamma\). The fresh protocol uses three independent copies of \(\sigma\). The persistent protocol runs all three contact words on one \(\sigma\) without measurement, reset, or additional dynamics between words.

At each laboratory project onto the subspace in which exactly one of the three path qubits occupies rail 1. Record just success or failure; revealing *which* copy used rail 1 destroys the needed coherence. Keep the trial when both laboratories succeed, before choosing the analyzer settings. The joint success probability is \(9/64\), independent of \(\sigma\). A logical qutrit \(|i\rangle\), \(i=1,2,3\), names the copy occupying rail 1. The two laboratories can have unrelated, unknown rail phases. A common shift of the single-rail phase for all three copies in one laboratory multiplies its entire accepted subspace by one scalar. Independent unknown shifts on the three copies are not removed. An exchange of \(|i\rangle\) and \(|j\rangle\) can be implemented by swapping the corresponding copies; measuring their real superpositions requires a calibrated coherent mixer for these alternatives. The distinction between total local occupation and individually addressable degrees of freedom is also used in operational studies of entanglement subject to local number restrictions. [Wiseman and Vaccaro, accessible entanglement](https://arxiv.org/abs/quant-ph/0210002)

## A three-copy correlation and the role of the register

Let \(|a\rangle=\sum_{i,j}|ij\rangle\), \(|d\rangle=\sum_i|ii\rangle\), and \(D=\sum_i|ii\rangle\langle ii|\). When \(i\ne j\), no pair translates its register. When \(i=j\), exactly one translation acts. Distinct diagonal alternatives therefore have memory overlap \(t=|\gamma|^2\) with independent fresh registers and \(t=1\) with the persistent register. Tracing the registers gives the conditional state

\[
9\rho=|a\rangle\langle a|+(\gamma-1)|d\rangle\langle a|
 +(\bar\gamma-1)|a\rangle\langle d|
 +\xi|d\rangle\langle d|+(1-t)D,\qquad
\xi=1-2\operatorname{Re}\gamma+t.
\]

In particular \(\xi=|1-\gamma|^2\) or \(2(1-\operatorname{Re}\gamma)\), respectively. The difference requires testing the stated reset models on comparable preparations. A correlated ensemble of registers can give another overlap.

Consider the normalized vector

\[
 |w\rangle=(|12\rangle-|21\rangle+|23\rangle-|32\rangle
                    +|31\rangle-|13\rangle)/\sqrt6.
\]

It has zero diagonal and zero row and column sums, and changes sign under swap. Consequently \(\rho w=0\). Partial transpose on B, written \(\Gamma\), sends \(|d\rangle\langle d|\) to the swap operator and leaves \(D\) unchanged. The partial transposes of \(|d\rangle\langle a|\) and its adjoint annihilate \(w\) by its row and column sums. Thus \(\rho^\Gamma w=-(\xi/9)w\). The following witness can be measured with local real symmetric observables:

\[
W=\tfrac12\left(|w\rangle\langle w|+(|w\rangle\langle w|)^\Gamma\right),
\qquad
\langle W\rangle=-\xi/18 .
\]

A separable state and its partial transpose are both positive, so every separable conditional state gives \(\langle W\rangle\ge0\). This applies to a classical relay restricted to local operations and classical messages, even with a probabilistic herald, provided the incident laboratories share no entanglement and the local instruments have the stated action. Other nonlocal operations could also produce a negative score. [Peres, separability criterion for density matrices](https://doi.org/10.1103/PhysRevLett.77.1413)

| Input register and inter-copy use | \(\gamma\) | Mean on joint successes | Mean multiplied by success indicator per launched triple |
|---|---:|---:|---:|
| Sharp field-five central blank, fresh | 0 | \(-1/18\) | \(-1/128\) |
| Same sharp blank, persistent | 0 | \(-1/9\) | \(-1/64\) |
| Signed blank \((|0\rangle-|1\rangle)/\sqrt2\), fresh | \(-1/2\) | \(-1/8\) | \(-9/512\) |
| Uniform central superposition, persistent | 1 | 0 | 0 |

**Why the third active copy matters.** With just two active pairs, project each laboratory onto one excitation across its two copies. For real \(\gamma=c\) the partial transpose, multiplied by four, splits in the logical Bell basis \((\Phi_+,\Psi_+,\Phi_-,\Psi_-)\) into the block \(\left(\begin{smallmatrix}2&2c\\2c&1+t\end{smallmatrix}\right)\) and the two scalars \(0,1-t\). The block is positive for both \(t=c^2\) and \(t=1\), since \(1+t-2c^2\ge0\). Positivity of partial transpose is sufficient for separability in this two-by-two sector. The other local occupation sectors have a one-dimensional factor. Thus for real \(\gamma\), locally twirling the two-active-pair preparation over independent laboratory phases leaves a separable state in these two reset models. In particular the sharp blank evades every occupation-preserving two-copy entanglement test on that input, while the three-copy score detects it. This argument is specific to the equal balanced preparations, the contact word and the two register schedules. [Horodecki, Horodecki and Horodecki, two-by-two separability](https://arxiv.org/abs/quant-ph/9605038)

## Extracting the score at the two laboratories

Use the three local occupation projectors \(L_{ii}=|i\rangle\langle i|\) and the three real pair exchange observables \(L_{ik}=|i\rangle\langle k|+|k\rangle\langle i|\), \(i<k\). An exchange read has outcomes \(+1,-1,0\) on the sum, difference and unused copy. Let \(w_{ij}\) denote the signed normalized entries above, and let \(O_{ik}\) be the one or two distinct orderings of \((i,k)\). Expand \(W=\sum_{i\le k,\,j\le l} C_{ik,jl} L_{ik}\otimes L_{jl}\), with

\[
C_{ik,jl}=\frac{1}{|O_{ik}||O_{jl}|}
 \sum_{(b,c)\in O_{ik}}\sum_{(e,f)\in O_{jl}}w_{be}w_{cf}.
\]

This averages each coefficient over local transpose in both laboratories. Since \(|w\rangle\langle w|\) is real symmetric, averaging over both local transposes gives exactly \(W\). There are 21 nonzero setting weights with \(\sum |C|=11/4\). Estimate each product on independent identically prepared triples, multiply by its coefficient, and sum. Experiments scoring all initial triples give zero to failures of the occupation herald. Local readout loss or any other missing counts need separate calibration. If each per-setting conditional product mean has an absolute error bound \(\epsilon\), their weighted sum changes by at most \(11\epsilon/4\). A fraction \(b\) of white noise \(I_9/9\) in the accepted qutrit state gives a negative ideal score precisely for \(b<\xi/(2+\xi)\). This white-noise example does not describe general decoherence or biased herald losses.

The [exact calculation](check_three_active_copies.py) derives the logical matrices by tracing translated physical field-five wavefunctions and computes all local outcome probabilities from their rank-one projectors. The [complete results](three_active_copies.json) retain all 21 nonzero settings, including zero-probability outcomes. These are calculated predictions. The coherent contacts and copy-exchange analyzers still require a physical implementation.
