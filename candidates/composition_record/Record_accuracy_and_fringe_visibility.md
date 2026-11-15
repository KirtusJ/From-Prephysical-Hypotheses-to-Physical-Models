# How accurately can a covector record be read while its writer preserves interference?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Director G (OpenAI Codex) research supplement to the [Composition as a Record review](README.md).

The submitted writer leaves a covector \(u\) after a source pair disconnects. A late nonzero probe \(q\) reads the scalar \(u(q)\), or produces a flag telling whether it vanishes. Suppose two balanced paths coherently write different covectors into the same memory. How well could the submitted reader still answer arbitrary late probes if the paths showed interference? For the translation model below the error rate of this reader puts a sharp upper bound on mean visibility, and an explicit blank attains it for every path difference at once. The calculation stipulates quantum states, coherent control, and quantum probabilities. It tests this extension of the writer. The finite composition law alone supplies none of those inputs.

## Preparations and observations

Let \(V=\mathbb F_5^3\). Use a Hilbert space with the 125 orthonormal covector labels \(z\in V^*\). Each run starts with the same density operator \(\sigma\), independent of the later choices. A closed write implements \(T_u|z\rangle=|z+u\rangle\), with no extra record of which path was taken. Any source controls used on the paths must recombine into the same final state. Different remnant control states can further reduce a fringe.

* **Record trials.** Choose one write \(u\) uniformly among the 125 covectors and a late probe uniformly among the 31 projective directions, independently. Use one fixed representative \(q\ne0\) per direction. The specified reader acts in the label basis: at \(v=z+u\) it returns \(v(q)\), or the flag \(1_{v(q)\ne0}\). The submitted ordinary-label outputs would be \(v(q)q\) and \(1_{v(q)\ne0}q\); fixed nonzero \(q\) makes the scores equivalent. Compare with the ideal answers for \(z=0\).
* **Fringe trials.** Use the same blank preparation and two balanced, mutually coherent paths writing \(u\) and \(u+d\). Scan a relative phase \(\phi\) before lossless recombination. The port probability is \((1+\operatorname{Re}[e^{i\phi}\operatorname{Tr}(\sigma T_d)])/2\) in a fixed phase convention. Its visibility is \(V_d=|\operatorname{Tr}(\sigma T_d)|\). Average the 124 separately measured contrasts over all \(d\ne0\), obtaining \(\bar V\). Pooling all settings into one phase scan can cancel phases. No trial is conditioned on a memory answer, port or successful erasure.

## The exact upper envelope for the specified reader

Write \(p_z=\langle z|\sigma|z\rangle\) and \(w=1-p_0\). The respective uniform mean errors for flag and scalar reads are

\[
E_{\rm flag}=\frac{10w}{31},\qquad E_{\rm scalar}=\frac{25w}{31}.
\]

Indeed a fixed nonzero offset \(z\) annihilates six of the 31 directions. In each of the other 25 directions it changes the scalar for every \(u\). For the binary flag it changes precisely the inputs \(u(q)=0\) and \(u(q)=-z(q)\), two of five equally likely residues. This argument uses only the diagonal of the state.

At each fixed \(w\in[0,1]\) the greatest attainable mean visibility is

\[
B(w)=2\sqrt{\frac{(1-w)w}{124}}+\frac{123w}{124}.
\]

**Proof.** Positivity of each two-by-two principal minor gives \(|\sigma_{zv}|\le\sqrt{p_zp_v}\). In the sum of \(|\operatorname{Tr}(\sigma T_d)|\) over \(d\ne0\), the triangle inequality counts each ordered pair \(z\ne v\) once. Consequently

\[
124\bar V\le \sum_{z\ne v}\sqrt{p_zp_v}
=\Bigl(\sum_z\sqrt{p_z}\Bigr)^2-1
\le\bigl(\sqrt{1-w}+\sqrt{124w}\bigr)^2-1.
\]

The last step is Cauchy–Schwarz on the 124 nonzero labels. The pure blank

\[
|\psi_w\rangle=\sqrt{1-w}\,|0\rangle+
             \sqrt{w/124}\sum_{z\ne0}|z\rangle
\]

saturates every inequality. Each translate overlaps in two origin-to-nonzero terms and 123 nonzero-to-nonzero terms. Thus \(V_d=B(w)\) for **each** nonzero \(d\). This also gives the greatest achievable *minimum* visibility over those settings, since a minimum cannot exceed their mean. The diagonal mixture with the same \(p_z\) attains zero visibility for every nonzero \(d\) and precisely the same record statistics. Mixing the two blanks realizes any intermediate mean visibility at fixed \(w\).

For an **upper limit** \(E_{\rm flag}\le e\), maximize at \(w=\min(31e/10,124/125)\). The function increases up to \(w=124/125\), where all amplitudes are equal and \(B=1\). This blank has mean flag error \(8/25\). A label-sharp blank has zero record error and zero visibility. A blank with amplitudes proportional to six at the origin and one everywhere else gives mean flag error \(1/4\), worst flag error \(5/8\), and visibility \(27/32\) in each setting.

## Worst input, preparation prior and a selected path difference

For a requirement on **every** \(u,q\), let \(E_{\max}\) be the largest conditional probability of an incorrect flag. Test the zero write and average over directions. A nonzero offset puts that flag up on 25 directions, so \(E_{\max}\ge25w/31\) for any blank. For \(|\psi_w\rangle\), a target zero gives error \(100w/124\), and a target nonzero gives error \(25w/124\). Thus the bound is sharp and the greatest mean visibility consistent with \(E_{\max}\le e\) is \(B(\min(31e/25,124/125))\). No distribution on writes is needed for this version.

Uniform source *pairs* in the submitted writer produce 745 zero writes and 120 of each nonzero covector among 15,625 ordered pairs. For any \(q\), the zero scalar then has weight \(3625/15625\) and each nonzero scalar weight \(3000/15625\). With \(z(q)\ne0\), the two residues that flip the flag now have total probability \(6625/15625\). Averaging over directions gives \(E_{\rm flag}=53w/155\), leaving \(B(w)\) itself unchanged. The scalar error is independent of the write prior. With nonuniform probe choices or correlated preparations, the direction and residue counts in the proof must be weighted by their actual joint law.

A single chosen direction of translation can retain more contrast than the mean suggests. Prepare a uniform positive superposition on the five labels \(0,d,2d,3d,4d\). It has \(w=4/5\) and uniform-write mean flag error \(8/31\). Shifts along this line give unit contrast. The 120 nonzero shifts off the line give zero. This is a counterexample to applying \(B(w)\) as a bound on each separate \(V_d\).

## An arbitrary late measurement

For a different decoder assume a flag can be recovered from the memory alone on each write and each probe with conditional error at most \(e\le1/2\). Fix \(d\ne0\) and choose a probe \(q\) with \(d(q)\ne0\). At this same \(q\) the writes \(0,d\) have opposite ideal flags; their actual binary output distributions differ in total variation by at least \(1-2e\). Hence the trace distance of \(\sigma\) and \(T_d\sigma T_d^\dagger\) is at least \(1-2e\). A purification and its translate have overlap \(\operatorname{Tr}(\sigma T_d)\). Partial trace cannot increase trace distance, and for pure states the distance equals the square root of one minus the squared overlap. It follows that

\[
 V_d\le2\sqrt{e(1-e)} .
\]

This pairwise necessity applies to each nonzero \(d\), including mixed blanks. A uniform mean error across many writes does not supply the two conditional error bounds used here. Sharpness for this arbitrary-decoder problem with all probes simultaneously remains open. For example a decoder that always raises the flag has mean error \(1/5\) under uniform writes even with the translation-invariant blank, but its error on the zero write is one. These distinctions implement the usual path-distinguishability constraint for this finite late-probe family. [Englert, *Fringe Visibility and Which-Way Information*](https://doi.org/10.1103/PhysRevLett.77.2154) · [Fuchs and van de Graaf, trace distance and distinguishability](https://arxiv.org/pdf/quant-ph/9712042)

The fixed-reader statistics alone also admit an ordinary random offset \(z\) with distribution \(p_z\), followed by finite-field addition. The proposed extra observation is a calibrated unconditional phase scan on independent preparations. Exceeding the relevant upper envelope would contradict this joint fixed-reader translation model under its stated calibrations. Agreement would leave the physical origin of the writer and the Born rule open.

From the repository root run `python -B candidates/composition_record/check_visibility.py`. The calculation enumerates the 3,875 write–probe pairs for each tested blank, all 124 nonzero translations and the complete ordered source-pair prior. Five rational amplitude-ratio checks, a dephased control and the one-line counterexample use exact integer and fraction arithmetic. [Checker](check_visibility.py) · [Exact results](visibility_results.json)
