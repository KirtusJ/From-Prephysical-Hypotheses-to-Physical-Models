# Proposed source errata for independent adjudication (not applied to Z2)

## G7 Proposition 4.3 (horizontal-lift proof)

Source wording: recurrence `alpha_{j+1}=alpha_j-arg<a_j|a_{j+1}>`, then `tilde a_k=e^{+i theta}a_0`, and `T=e^{-i theta}U|_{a_0^perp}` with `e^{i theta}=B/|B|`.

**Exact replacement:** `tilde a_k=e^{-i theta}a_0`; consequently `U a_0=e^{-i theta}a_0`, and in the terminal frame `T=e^{+i theta}U|_{a_0^perp}`. Since `det U=1`, `det(U|)=e^{+i theta}`; hence `det_C T=e^{+i(n+1)theta}`, as already stated in the theorem. This is a correction of two mutually offset sign slips in the printed derivation, not a change to the statement.

## G8 Sections 1 and 3 (additive functions)

Keep Lemma 3.1. Where the introduction or commentary says that **no additive function of walks** can depend on transport, qualify explicitly: *no function defined universally by summing a fixed scalar function of each open or closed walk's gain alone, invariant on every gain graph, can depend on that gain.* If an additive term may distinguish returned-to-root paths, `sum_{w:terminal(w)=root}(1+Re chi(gain(w)))` is a positive gauge-invariant, holonomy-sensitive counterexample for `Z_3`.

## G8 Section 5 (projective density)

Add as an explicit example: gain group `Z_n`, base graph `K_4`, gain +1 on oriented edge 2->3, zero on all others. The derived `4n`-cover graph is connected and nonbipartite, hence the counts satisfy `N_k(v,g)=3^k/(4n)+O(rho^k)` for some `rho<3`; for `n>=3`, G8's mathematical event rays are dense in `CP^3`.

## G8 Sections 5, 9 (cross-length meaning)

The fixed-length decoherence kernels need not be projectively consistent under the natural map taking a set of finite paths to all its extensions. For the foregoing `Z_3` graph, `D_1(0->1,0->2)=0` but `D_2(Ext(0->1),Ext(0->2))=1+omega !=0`; total masses `1,3,15` at steps `0,1,2`. A normalized cylinder histories measure or dynamics remains a further obligation. This is **not** a claimed flaw in the fixed-length positive kernel theorem.

**Editorial status:** Suggested changes are a submission from Director A. Source Z2 PDFs and manuscript files remain byte-unmodified.
