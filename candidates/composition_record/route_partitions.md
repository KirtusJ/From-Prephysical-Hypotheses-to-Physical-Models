# Which contact words entangle two fixed routes?

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two binary routes keep their labels throughout a sequence of controlled contacts. The contacts act by right multiplication on the regular group register, initially independent of the routes and diagonal in its sheet basis. Discard the entire register at the end. **The largest concurrence that any such sequence can generate from a separable two-qubit input is \(1/2\).** One commutator in the candidate attains it. Subsequent route recombination may use arbitrary local unitaries. Coherent mixing of a route between contacts, a separate coherent work register, a nonregular action, or a coherent initial sheet preparation changes the problem.

## Equality of endpoints

Write \(w_i\) for the chronological group product along route \(i=ab\). For each initial sheet \(s\), the four terminal sheets are \(s w_i\). The reduced matrix element \(\rho'_{ij}\) equals \(\rho_{ij}\) when \(w_i=w_j\), and zero otherwise, by cancellation in the group. This holds for every initial sheet distribution. The entire sequence therefore defines a partition of the four labels. Independent local path phases can be removed by local unitaries. An additional controlled two-party phase would be an independent interaction.

| Block sizes | Number | Reduced action on a product input |
|---|---:|---|
| 4 | 1 | Identity |
| 3, 1 | 4 | A nonzero concurrence is possible |
| 2, 2 | 3 | Mixture of local sign changes |
| 2, 1, 1 | 6 | Separable for every input product |
| 1, 1, 1, 1 | 1 | Diagonal mixture of product states |

For two blocks of two, average the identity with conjugation by \(Z_A\), \(Z_B\), or \(Z_A Z_B\), according to the partition. For one retained pair and two singletons, four choices of the pair share a row or column. The output is block diagonal in the corresponding local bit and hence separable. The other two choices retain a diagonal of the square. Write the input amplitudes as \(x_{ab}=\alpha_a\beta_b\). Partial transposition transfers the sole off-diagonal pair to the other diagonal. Its two-by-two block has nonnegative diagonal entries and determinant zero because \(|x_{00}x_{11}|=|x_{01}x_{10}|\). Thus the partial transpose is positive, which suffices for two-qubit separability. Convexity extends these cases to all separable inputs. [Horodecki, Horodecki and Horodecki, two-qubit separability criterion](https://arxiv.org/abs/quant-ph/9605038)

## Exact concurrence of the remaining four channels

Use local bit flips to place the singleton at \(11\). More generally suppose just that branch acquires a random phase \(\zeta\) of unit modulus with mean \(\gamma\). This multiplies the corresponding off-diagonal entries by \(\gamma\) or its conjugate. A three-plus-one partition gives \(\gamma=0\). For a pure product input the concurrence is

\[
 C=2|x_{00}x_{11}|\,|1-\gamma|.
\]

To see the lower bound, put \(u=(x_{00},x_{01},x_{10},0)\), \(v=(0,0,0,x_{11})\). If any input amplitude vanishes the state stays separable. Otherwise every pure-state decomposition consists of subnormalized vectors \(A_\ell u+B_\ell v\) with \(\sum|A_\ell|^2=1\) and \(\sum\overline{A_\ell}B_\ell=\gamma\). A subnormalized two-qubit vector contributes twice the absolute value of its coefficient determinant to the average concurrence. Since \(x_{00}x_{11}=x_{01}x_{10}\), the sum of those contributions is

\[
 2|x_{00}x_{11}|\sum_\ell |A_\ell|\,|B_\ell-A_\ell|
 \ \ge\ 2|x_{00}x_{11}|
 \left|\sum_\ell\overline{A_\ell}(B_\ell-A_\ell)\right|.
\]

For attainability when \(\gamma\ne1\), extend the ray from 1 through \(\gamma\) to a boundary point \(z\) of the unit disk, so \(\gamma=1-t+tz\) for \(0<t\le1\). The same state is the mixture of phases \(1,z\) with weights \(1-t,t\). Its average concurrence equals the bound since \(t|1-z|=|1-\gamma|\). At \(\gamma=1\) the state is the input product. This argument uses the usual complex two-qubit convex-roof concurrence. [Wootters, entanglement of formation of two qubits](https://arxiv.org/abs/quant-ph/9709029)

Each local product factor obeys \(|\alpha_0\alpha_1|\le1/2\) or \(|\beta_0\beta_1|\le1/2\), respectively. For a blank and \(\gamma=0\), the balanced product \(|++\rangle\) reaches \(C=1/2\). The candidate's word \(g^a h^b g^{-a}h^{-b}\) has identity endpoint for three routes and the nonidentity central commutator for \(11\), realizing this partition. Repeating it \(m\) times gives the same channel for \(m\ne0\bmod p\) and the identity for \(m=0\bmod p\), when this commutator has prime order \(p\). Convexity gives the same upper bound for mixtures of fixed-route programs chosen independently of the input. The proof permits any length and counts every outcome.

## A real local work register raises the exact bound

Now allow each party arbitrary coherent local operations and work space. Use one generator pair \(g,h\), whose central commutator \(c=[g,h]\) has prime order \(p\), and suppose all contact words use this pair. The initial state of the two laboratories is separable across them and independent of a sheet-diagonal regular bus. At every contact the owning laboratory coherently controls a right multiplication on the bus. Local operations can include adaptive measurements and ordinary classical messages between the parties. Every outcome contributes to the unconditional final state. There is no exchange of coherent work systems, direct nonlocal gate, or additional instrument reading or mixing named bus sheets. Within this class the sharp concurrence of a pair of output qubits is **\(1-1/p\)**.

**Upper bound.** All bus operations preserve the eigenspaces of the central translation \(R_c\). A sheet basis vector has equal spectral weight \(1/p\) on each character, since its \(p\) central translates are orthogonal. The same holds for every sheet-diagonal input. The final partial trace removes coherences between different sectors. In the character-zero sector \(R_c=I\), so \(R_g\) and \(R_h\) commute. Choose a simultaneous eigenbasis there. Conditioned on one such basis label, any local controlled word applies only a local phase operator to its controlling laboratory. With local operations, local ancillas and ordinary classical communication, a separable input stays separable on each complete branch. Off-diagonal joint eigenbasis entries disappear on tracing the bus. Summed over all classical outcomes, the zero-sector weight is still \(1/p\), since every operation preserves it and the complete protocol is trace preserving. Convexity of concurrence and its two-qubit maximum 1 give the bound. Conditioning only on successful preparations would change this denominator.

**Protocol attaining it.** Give party B one coherent \(p\)-mode register in the real uniform state \(s=p^{-1/2}\sum_{j=0}^{p-1}|j\rangle\). The route bits are \(a\) at A and \(b\) at B. Apply the four controlled calls

\[
 K(a,j)=g^a h^j g^{-a}h^{-j}=c^{aj}.
\]

Only A controls the \(g\) powers and only B controls the \(h\) powers. On central character \(k\), choose the sign convention \(R_c\mapsto\exp(2\pi i k/p)\). The B work state becomes \(\chi_{ka}=p^{-1/2}\sum_j\exp(2\pi i k a j/p)|j\rangle\). If \(ka=0\), this is \(s\). Otherwise the finite geometric sum gives \(\langle s|\chi_{ka}\rangle=0\). B applies the real reflection \(2|s\rangle\langle s|-I\) when \(b=1\), then both parties undo \(K\) in reverse order. The work register returns exactly to \(s\) and all extra contact displacements cancel. The surviving route phase is \((-1)^{ab\,1_{k\ne0}}\). Complex characters only describe the spectrum here. The physical operations in this model are controlled sheet permutations and a real local reflection. Coherent \(p\)-way control and the calibrated uniform reflection are additional resources. Eigenvalue-based interference and bus-mediated controlled gates have precedents. [Cleve et al., phase estimation](https://arxiv.org/abs/quant-ph/9708016) · [Spiller et al., quantum computation by communication](https://arxiv.org/abs/quant-ph/0509202)

On discarding the bus this realizes identity with probability \(1/p\) and controlled \(Z\) with probability \(1-1/p\). The phase mean is \(\gamma=2/p-1\), so the balanced product has concurrence \(1-1/p\) by the formula above. At field order five the two exact bounds are \(1/2\) for fixed binary routes and \(4/5\) with the extra local work control. The protocol requires neither a central-sector measurement nor the earlier herald. The upper bound concerns one pair of generators, including its inverse and composites. More independent commutators change the weight of the sector in which all allowed contacts commute.

The [integer replay](check_contact_reflection.py) constructs the four chronological calls and their reverse, and checks the reflection on every central sheet and every route input for each requested prime. It keeps the work amplitudes in the sheet basis, so a sign or an uncomputed work label is visible directly.
