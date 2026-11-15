# One exact site record changes a ballistic history

**Kirtus Justus**, Theoretical Physicist, Port Coquitlam, British Columbia, Canada. Research supplement by Director G (OpenAI Codex).

Two instruments can report the same first bit with exactly the same probabilities and disagree about the subsequent motion. On the [reflecting Hadamard walk](Reflecting_wells_and_the_classical_limits_of_a_walk.md), an exact site measurement followed by deletion of the site label yields a two-bit event with limiting inferior probability at least **0.06576027**. Preserving coherence across the entire first cell gives limiting probability zero. The walkers start at one sharp site on one sharp rail. Both measurement schedules use ordinary probabilities.

## First and last records

Take \(L=8n\) wells, launch on rail \(R\) at \(x_0=4n\), and use the same uniform signed Hadamard and positive-reflection shift as in the preceding work. All displacements below are from the actual launch site. At tick \(n\) record the bit \(A\) for \(|x-x_0|\le n/6\). At tick \(2n\) record the bit \(B\) for \(|x-x_0|>n/3\). Keep all four joint outcomes per incident population. The light cone through \(2n\) lies strictly inside the interval, so translation on the infinite line computes these two clocks exactly. Boundary reflection is part of the carrier but is inactive in this particular comparison.

For the coherent first bit, apply the projectors onto \(A\) and its complement, preserving both rails and relative phases within each cell. For the finely resolved first bit, measure the exact site at tick \(n\), preserving both rail amplitudes **at that site**, and retain only its membership in \(A\). The latter instrument destroys intersite coherence. Both have first effect \(\sum_{x\in A}|x\rangle\langle x|\otimes I\). Hence their first marginals agree at every finite \(n\). The final instrument and dynamics are the same in both runs.

## A finite symmetry of the second flight

Let \(T_d\) be the real two-by-two coin kernel taking a site-localized input to displacement \(d\) after \(n\) free ticks, including the factor \(2^{-n/2}\). Then for **any** symmetric set \(D=-D\),
\[
 \sum_{d\in D} T_d^\dagger T_d = c_{n,D}I .
\]
In particular the chance of \(|d|>n/2\) is the same for every incoming coin, including mixed coins. Define \(J(r,l)=(l,-r)\). Reflection of position together with \(J\) commutes with the directed shift and takes the coin \(H\) to \(-H\). Thus \(T_{-d}=(-1)^nJT_dJ^{-1}\). For a real symmetric two-by-two effect \(E\), direct multiplication gives \(E+JEJ^{-1}=(\operatorname{tr}E)I\). Pair \(d\) with \(-d\). The singleton \(d=0\), when present, has \(E=JEJ^{-1}\) and is itself scalar. The identity applies even to complex input coin states. The [Lean identity](lean/ExactSiteIntervention.lean) verifies the equal diagonal entries and zero off-diagonal term for any mirrored pair of real integer path kernels after taking out their common divisor.

After the fine first read, every branch starts its second flight at one site, with an arbitrary conditional coin. The probability of a displacement in \(D\) on this flight, jointly with any chosen subset of first sites, equals \(c_{n,D}\) times the first subset probability. For the event \(A\), any displacement of size \(>n/2\) in the second flight guarantees \(B\) because \(n/2-n/6=n/3\). Consequently
\[
  P_{\rm fine}(A,B)\ \ge\ P(A)\,c_{n,\{|d|>n/2\}} .
\]

From a sharp site, the limiting absolute speed of this Hadamard walk is \(|V|=|\cos k|/\sqrt{1+\cos^2 k}\), \(k\) uniform on a full period. The two bands have opposite velocities and their projector weights sum to one at each \(k\), giving the same absolute-speed law for every coin. For \(0\le h\le1/\sqrt2\) its cumulative probability is \(G(h)=2\arcsin(h/\sqrt{1-h^2})/\pi\). The thresholds \(1/6,1/2\) have zero boundary mass. Passage to the limit gives
\[
  \liminf_{n\to\infty}P_{\rm fine}(A,B)\ \ge\
  G(1/6)\,[1-G(1/2)] =
  \frac{4}{\pi^2}\arcsin(1/\sqrt{35})\,\arccos(1/\sqrt3)
  \simeq0.06576027769 .
\]
This bound uses only a subset of the paths into \(B\). It does not assert equality. [Grimmett, Janson and Scudo, ballistic limits from a sharp site](https://doi.org/10.1103/PhysRevE.69.026119)

## Why the coherent bit has no limiting mass on this word

Under a common velocity \(V\), displacements at these two clocks in units of \(n\) are \(V\) and \(2V\). The first bit then requires \(|V|\le1/6\) and the second requires \(|V|>1/6\). Here is a direct justification that this shared velocity gives the limit of the **two actual coarse measurements** on this initial state.

Write \(X\) for displacement on the line and \(U\) for its step. In momentum \(k\) use \(\sum_xe^{ikx}\psi(x)\), so \(U(k)=\operatorname{diag}(e^{ik},e^{-ik})H\). For \(j=1,2\) put \(Y_{n,j}=U^{-jn} X U^{jn}/n\). On any tested initial state, the coarse word probability is the squared norm of \(\mathbf1_{|Y_{n,2}|>1/3}\mathbf1_{|Y_{n,1}|\le1/6}\psi\). For fixed Fourier argument \(\xi\), \(e^{i\xi Y_{n,j}}\) acts on \(\psi(k)\) by multiplication with \(U(k)^{-jn}U(k+\xi/n)^{jn}\) after translating the argument by \(\xi/n\). The translation tends strongly to the identity. Expand the product in spectral projectors. The two eigenvalues stay separated, with smooth periodic projectors \(P_b\) and phases \(\omega_b=\arcsin(\sin k/\sqrt2)\) and \(\pi-\arcsin(\sin k/\sqrt2)\). Cross-band products are \(O(1/n)\) uniformly by orthogonality at equal momenta. The surviving phases tend uniformly to \(e^{i\xi j\omega'_b(k)}\). Thus the exponentials converge strongly to those of \(j\mathcal V\), where \(\mathcal V(k)=\sum_b\omega'_b(k)P_b(k)\).

This gives strong convergence for smooth compactly supported functions of \(Y_{n,j}\) by Fourier inversion and dominated convergence. Approximate the interval projections above by bounded smooth cutoffs, using \(I\) minus an interval cutoff for the exterior event. For each vector the squared approximation error can be bounded by its spectral mass in bands approaching the two thresholds, using continuous majorants there. The limiting mass in the shrinking bands vanishes since all threshold level sets of \(\omega'_b\) here have Lebesgue measure zero. Thus the projections converge strongly. They are contractions, so their ordered product converges strongly to the corresponding product for \(2\mathcal V,\mathcal V\), which is zero. This argument requires ordinary coherent projections with the specified within-cell action. It says nothing about a hidden exact read subsequently binned by a computer.

## Finite replay

The table gives joint probabilities per incident launch. The third column of numbers is the finite lower bound from the symmetric tail.

| Ticks per flight | Coherent \(P(A,B)\) | Fine \(P(A,B)\) | Fine lower bound |
|---:|---:|---:|---:|
| 8 | 0.053284 | 0.053284 | 0.021423 |
| 16 | 0.049728 | 0.090719 | 0.065080 |
| 32 | 0.019920 | 0.075264 | 0.054220 |
| 64 | 0.021011 | 0.087132 | 0.067317 |
| 128 | 0.011615 | 0.082493 | 0.064377 |
| 256 | 0.009279 | 0.083711 | 0.065390 |
| 384 | 0.006753 | 0.084218 | 0.066642 |

At eight ticks only the launch site is occupied inside \(A\), so the two instruments agree on this branch. The thirty-two- and sixty-four-tick rows also illustrate that the approach to zero need not be monotone. The [checker](check_exact_site_intervention.py) tests the symmetric effect at every displacement radius, compares the coherent cell branch with the exact sum over site branches, and independently enumerates all two-flight direction words up to sixteen steps. Its [complete integer tables](results/exact_site_intervention.json) retain all four events, both first marginals and small-clock controls. Run `python -B Director_G/check_exact_site_intervention.py new_file.json`. These are predictions for prescribed measurement operations. Realizing nondisturbing cell readout and establishing its physical provenance remain experimental and ontological obligations.
