# Which parts of a written contact survive as an interference phase?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

The [review of Composition as a Record](README.md) recovered ten coefficients from calibrated contacts with values in the field of five elements. Suppose instead that two ways to combine three inputs differ by a complex phase, and the phase convention for each input pair can be changed freely. Seven independent fifth-root values then survive. Three independent field-valued differences can be detected by the original reader while every convention-independent phase experiment gives identical results. This is a distinction between two possible physical implementations of the proposed mathematical record.

## Seven coherent cycles

Keep the input labels and their order fixed in \(V=\mathbb F_5^3\). Use representatives from 0 through 4 and put \(C_j(b,c)=\lfloor(b_j+c_j)/5\rfloor\), with vector sums taken in \(V\). The candidate family in a calibrated scalar convention is
\[
 \omega(a,b,c)=s\det(a,b,c)+\sum_{i,j}M_{ij}a_i C_j(b,c).
\]
Let \(\zeta=e^{2\pi i/5}\). In a coherent extension one reassociation has overlap \(\Omega(a,b,c)=\zeta^{\omega(a,b,c)}\). Rephasing the one-dimensional pair spaces multiplies it by \((\delta u)(a,b,c)=u(b,c)u(a,b+c)/[u(a+b,c)u(a,b)]\), for any normalized \(U(1)\)-valued pair table. This permits arbitrary angles between pair bases. The field-coefficient family and the phase-coefficient classification have different sizes in the primary literature. [Beli, field coefficients](https://arxiv.org/pdf/2005.11868) · [Hu, Wan and Wu, phase coefficients, Eq. 97](https://arxiv.org/pdf/1211.3695) · [Huang, Wan and Ye, associativity and pair bases, §3](https://arxiv.org/pdf/1703.03266)

Define \(T\) as the product of the even permutations of the three ordered basis inputs divided by the product of the odd permutations. Pair rephasings cancel. The carries are symmetric in the final two arguments and the six determinant contributions give \(6s=s\bmod5\). Thus \(T=\zeta^s\). For a single vector \(x\) also measure
\[
 Q(x)=\prod_{j=0}^{4}\Omega(x,jx,x)=\zeta^{x^{\mathsf T} M x}.
\]
Both pair ratios in \(\prod_j\delta u(x,jx,x)\) telescope over the five residues. The summed carry from successively adding \(x\) five times in coordinate \(i\) is the digit \(x_i\), including zero. The determinants all vanish. This cyclic product is the fifth member of the standard cocycle recurrence for powers of a simple label. [Schauenburg, Definition 2.2](https://arxiv.org/pdf/1502.02906)

Read \(Q\) on \(e_1,e_2,e_3,e_1+e_2,e_1+e_3,e_2+e_3\). The first three powers return the diagonal of \(M\). Dividing each pair-sum phase by the corresponding two diagonal phases returns \(M_{ij}+M_{ji}\) in the exponent. Together with \(T\) these values are independent and take every vector in \(\mathbb F_5^7\). In particular a vanishing response on the three coordinate axes alone can conceal every symmetric cross term as well as the determinant.

## A difference that every phase cycle misses

For \(i\ne j\) define a pair phase \(u_{ij}=\exp(2\pi i f_{ij})\), with
\[
 f_{ij}(a,b)=-a_i b_j/25+C_i(a,b)[a_j+b_j]_5/5 \pmod1 .
\]
Here brackets give the canonical digit. Direct subtraction at the four faces gives
\[
 \delta f_{ij}(a,b,c)=[a_i C_j(b,c)-a_j C_i(b,c)]/5\pmod1 .
\]
The [Lean certificate](PhaseGauge.lean) proves the integer identity, including the multiple of 25 removed in passing to a phase. For \((i,j)=(1,2)\) the table uses the value \(-1/25\) at \((e_1,e_2)\). Its phase convention needs 25th roots. If only fifth-root pair changes are admissible, the two field classes remain distinguishable by the earlier crossed contact. The original \(\omega\) still uses fifth roots after exponentiation.

If two seeds in this family have equal seven readings, they have equal \(s\), equal diagonals and equal symmetric cross sums. Their difference is a sum of exactly these three types of skew carry, so the displayed pair tables remove it. Conversely every pure pair change leaves the seven readings invariant. Each fully oriented phase class therefore contains exactly \(5^3=125\) of the submitted family's field-coefficient classes on fixed labels. This completeness follows directly for this family. Testing an unconstrained table for the cocycle identity over all four inputs is a separate obligation.

There is an observable consequence. In the explicit field seed \(a_1 C_2-a_2 C_1\) all seven phase cycles are one, just as for the zero seed. In the original field-valued contact apparatus, holding \(e_1\) as reference and repeating the \(e_2\) lift five times writes **one**. Interchanging reference and lift writes **four**, and the zero seed writes zero on both. In an arbitrary pair phase convention the crossed fivefold slant-product read acquires the fifth power of the chosen lift phase. Indeed the induced two-coboundary on fixed reference \(h\) is \(\delta v_h\), where \(v_h(x)=u(x,h)/u(h,x)\); multiplying five equal lifts gives \(v_h(x)^5\). This explains precisely where a physical fifth-root calibration or an independent scalar register enters. With such a calibration, three upper-triangular crossed reads and the oriented seven phases recover all ten coefficients. With labels or the scalar unit free to transform, there are additional ambiguities.

## Reading the phases with two real rails

Assume one can route two coherent arms through the specified reassociations, their inverses where required, and matched resets of all labels and apparatus except their relative phase. A reference arm or independent balance measurement fixes the dynamical phase of the entire schedule. Concatenation on one arm then multiplies its invariant phases. Recombining the two rails on a real Hadamard gives bright-minus-dark contrast \(\cos(2\pi v/5)\) for a cycle with value \(\zeta^v\), using ordinary squared probabilities. The comparable real toric-code recoupling experiment and its measured phase offset illustrate why coherent control and matched paths have to be verified. [Hai et al., Fig. 4](https://doi.org/10.1093/nsr/nwac264) · [Araújo et al., limitations on controlling a black-box operation](https://arxiv.org/abs/1309.7976)

One real contrast determines \(d(v)=\min([v]_5,[-v]_5)\). Seven separate contrasts leave up to \(2^7\) sign assignments. Choose any nonzero component \(a\) as a reference and adopt its positive folded sign. For each other nonzero component \(b\), measure the two cycles **concatenated before readout**. The result distinguishes the two relative signs, since \(d(a+b)=d(a-b)\) would imply \(2b=0\) or \(2a=0\). Thus at most six additional settings identify the entire seven-component phase class up to simultaneous conjugation. Multiplying two separately measured real contrasts would give \(\cos A\cos B\) and would discard this relative-sign information. For example \(v_1=v_2=1\) and \(v_1=1,v_2=-1\) both give \(0.309017\) on each individual cycle; their joint cycles give \(-0.809017\) and \(1\). With real controls, conjugating the source and every route leaves all real readout probabilities identical. A calibrated imaginary quadrature on one nonzero reference would orient the whole result.

For ideal unit visibility the three contrasts are \(1,(\sqrt5-1)/4,-(\sqrt5+1)/4\). If every measured contrast differs from its ideal value by strictly less than \((5-\sqrt5)/8\simeq0.345492\), nearest-level decoding on each used setting returns the same folded labels as the exact calculation. The number refers to bright-minus-dark contrasts, twice the bright-probability deviation for a binary all-trial read. A calibrated complex overlap error of modulus less than \(\sin(\pi/5)\) likewise suffices for nearest-root decoding of an oriented cycle. These are deterministic total-error criteria. Instrument phase drift, visibility loss, missed trials and sampling error all need to enter an actual error budget. A perfect pentagon closure alone supplies no identification here: every cocycle, including the zero seed, has unit pentagon holonomy.

## What reaches the reader?

At a source, transfer the two-arm phase to a balanced pointer \((|0\rangle+\zeta^v|1\rangle)/\sqrt2\) and disconnect the source. A receiver who gets that pointer can choose its quadrature later. For the zero and unit seeds on the alternating basis test the real bright rates are \(1\) and \((1+\cos(2\pi/5))/2\simeq0.654508\). With an independent phase reference, the optimal binary read for equal priors succeeds with probability \((1+\sin(\pi/5))/2\simeq0.793893\), from the trace distance of the two pure pointer states. Both are model predictions. If a competing detached reader receives a nuisance variable independent of the intervention, its two output distributions coincide. If the variable leaks the intervention by total variation at most \(\ell\), its predicted rate contrast is at most \(\ell\). A physical bound on leakage and a separate intervention on the source are required to apply that test.

A lookup device which receives the inputs and implements these same scalar phase gates reproduces all of the proposed phase records using ordinary associative circuit composition. A dephased pointer gives zero real contrast for both seeds. These controls distinguish what information is carried and what phase convention it uses. They retain the need for an independently characterized physical coupling, a persistent pointer and a probability rule. They do not establish a first record.

Run the [Python replay](check_reassociation_phases.py) with \(\texttt{--check}\). It verifies the boundary coefficients of the seven cycle words, the rank after each type of measurement, every one of the 15,625 skew-carry coordinate triples, and all 78,125 seven-phase vectors under real-only decoding. The [stored result](reassociation_phases.json) retains the entire multiplicity and additional-setting histograms. The [Lean proof](PhaseGauge.lean) checks the coboundary identity for arbitrary integer inputs under the stated digit convention.
