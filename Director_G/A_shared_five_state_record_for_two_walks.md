# A shared five-state record for two walks

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two independently launched Hadamard walks can test whether a shared record of their movements preserves interference between two different histories. **A forward position measurement alone separates a coherent shared total from any classical relay that leaves a separable pair of calibrated path qubits, even after the relay announces a successful total.** The signed walk needs at most three ticks per walker. The memory, its coherent coupling, the two independent sources, and ordinary probability weighting are stipulated in this calculation.

## The memory and what is added to the candidate

In *Composition as a Record*, adding the determinant covector for \((e_1,e_2)\) increments its value on \(e_3\) by one in \(\mathbb F_5\). Restrict the blank carrier to that one covector component \(m\). Fire this write only on a walker's rightward first hop and restore the sources and scratch of the writer. Do this once for walker A and once for walker B using the same carrier. After the second write apply a fixed offset of \(-1\) and query the zero/nonzero flag. Define the herald event \(h\) as a recorded zero query on a detected trial. This distinguishes a total of **exactly one rightward hop** among the two. All residues here are interpreted modulo five, with attainable totals zero, one and two. The two local contacts may occur at different times while the paths are held coherently. The apparatus carrying the memory from one contact to the next is a resource. [Original finite writer and its associative simulator](../candidates/composition_record/README.md)

For the coherent hypothesis, promote the classical memory states to orthogonal basis vectors, implement the controlled writes as permutations acting linearly on amplitudes, and use a zero query whose unobserved environment is identical on the two histories giving total one. These assumptions exceed the candidate's deterministic tables. The rival may keep classical data, measure locally, exchange classical messages, apply correlated phases and condition the herald on the data it has amassed. With initially independent walkers, a separable memory and local quantum operations controlled by those messages, each classical transcript gives a product state or a mixture of product states. Summing the transcripts accepted by the same herald keeps the pair separable. This argument requires isolation from other joint interactions, coherent messengers or pre-existing entanglement. Parity-mediated entanglement and the need to preserve coherence inside a parity sector have been demonstrated in a superconducting circuit. The calculation below supplies a forward walk-position read for this particular covector proposal. [Ristè et al., *Nature* 502, 350–354 (2013)](https://doi.org/10.1038/nature12513)

## Two position settings after the herald

Use separate unforced intervals or lines with each source at least three steps from any wall. Both walkers begin at their own origin on the right rail. The real Hadamard followed by the conditional shift gives \((|r\rangle+|l\rangle)/\sqrt2\), with \(|r\rangle=|+1,R\rangle\), \(|l\rangle=|-1,L\rangle\). In the product preparation the four pairs have equal amplitude. The coherent total gives \(p_h=1/2\). On success the common memory has the same value on both paths, giving the normalized state
\[
 |\Psi\rangle=(|r,l\rangle+|l,r\rangle)/\sqrt2.
\]
The two incoming path qubits are now isolated. Choose the read after the herald, independently of that trial's data.

* **Immediate setting.** At each walker record \(+1\) at \(+1\), and \(-1\) at \(-1\), with both rails collected. On the two-path code this is \(Z=\mathrm{diag}(1,-1)\). The ideal pair obeys \(\langle Z\otimes Z\rangle=-1\).
* **Delayed setting.** Each walker takes two more ordinary Hadamard-and-shift ticks. The detector pools the final rails at each site and assigns the signs \((+,-,+,-)\) in order of increasing displacement \((-3,-1,1,3)\). Its signed mean on the incident code is exactly the operator \(X/2\), where \(X\) exchanges \(r,l\).

Indeed the four site effects in the \((r,l)\) basis, in units of \(1/4\), have entries \((rr,rl,ll)\) given by
\[
 (0,0,1),\quad (1,-1,2),\quad (2,1,1),\quad (1,0,0).
\]
They sum to \(4I\) in these units and the signed sum is \(2X\). This reuses the position mask derived for the earlier two-walk contact experiment, here acting on the code after the **shared herald**. The off-diagonal of any bounded site score \(|s_x|\le1\) is \((s_1-s_{-1})/4\), with magnitude at most \(1/2\). The mask attains that value and cancels both diagonal entries. With zero or one further tick every single-site effect on this same code is diagonal, so an earlier position-only setting cannot detect its coherence. These statements fix the scope to this code, unaltered free walk, pooled rails and a bounded position score. [Original analyzer and its site effects](Two_coin_position_read_at_one_contact.md) · [Exact integer path replay](check_two_walk_memory.py)

## A score on all trials

For the immediate and delayed settings let \(C_Z,C_M\) be the mean product of the two local signs **multiplied by the herald indicator**, per initial pair in that setting. The same herald mechanism precedes either choice. A separable pair at the herald satisfies
\[
 C_M-C_Z\le p_h .
\]
For a single product of local density matrices with Bloch components \((x_j,z_j)\), the conditional score is \(x_A x_B/4-z_A z_B\le1\) by Cauchy–Schwarz and \(x_j^2+z_j^2\le1\). Average over products. For the coherent total, \(C_M=p_h/4=1/8\) and \(C_Z=-p_h=-1/2\); the difference is \(5/8\), above the separable bound \(1/2\). Equivalently the two correlators imply a lower bound on the fraction of accepted pairs outside the separable class in any mixture: the operator \(X\otimes X/4-Z\otimes Z\) has largest eigenvalue \(5/4\), so the lower bound on that fraction is \(\max\{0,4[(C_M-C_Z)/p_h-1]\}\) for \(p_h>0\). Pre-herald failures count towards the original trial denominator. A missed local sign, missing herald flag or code leakage in a real test requires an independently bounded effect on these three observed rates. The model predicts complete readout.

| How the apparatus carries the two writes | \(p_h\) | \(C_Z\) | \(C_M\) | \(C_M-C_Z\) |
|---|---:|---:|---:|---:|
| Coherent total, no extra copy | \(1/2\) | \(-1/2\) | \(1/8\) | \(5/8\) |
| Retained total, extra copy of the first path | \(1/2\) | \(-1/2\) | \(0\) | \(1/2\) |
| Erase the first write into an inaccessible register and prepare a fresh blank | \(1/2\) | \(0\) | \(0\) | \(0\) |

For the second row the accepted histories \((r,l),(l,r)\) remain individually legible to the environment. The accepted pair is their incoherent mixture. In the third row only the second path determines the flag. Implementing the same associative permutations coherently with the corresponding registers also gives the entire first row. This leaves the physical origin of the records and the associator unresolved. A relay with arbitrary untrusted sign boxes can also send a random sign to both parties, return opposite local signs for the immediate setting and equal ones for the delayed setting. The separable bound uses the calibrated local position effects, their two-path support and independent measurement choice.

If the two accepted paths leave environment states with overlap \(\gamma\), the conditional delayed correlation is \(\mathrm{Re}(\gamma)/4\), while the immediate anticorrelation remains perfect. Positive real overlap suffices to exceed the separable bound in the ideal lossless model. A complex or negative overlap can escape this particular mask; calibrated phase changes on a path could probe its other quadrature. The protocol does not identify an arbitrary memory channel from two numbers.

## Why the public flag matters

Discarding the shared tally instead gives a mixture of ordinary local phase shifts on the two first hops. In the memory Fourier basis its translations are diagonal. For a blank tally all five Fourier labels are equally weighted, and the same label controls both walkers. Equivalently the factor between computational path pairs of totals \(j,k\) is \(5^{-1}\sum_{n=0}^4\exp(2\pi i n(j-k)/5)=\mathbf1_{j=k\bmod 5}\). The entire unconditioned pair is therefore separable. Inspecting the **real zero flag** after a coherent total exposes an accepted sector which shared classical phases and an input-independent classical random flag cannot produce within the calibrated local model. The local path state of each accepted walker separately is the fair mixture of its two outgoing alternatives. Their joint position counts contain the distinguishing information. No long-flight trajectory limit or empirical detector identification follows from this finite construction. [Full tables for both flags and settings](results/two_walk_memory.json) · [Lean finite sign and path controls](lean/TwoWalkMemory.lean)
