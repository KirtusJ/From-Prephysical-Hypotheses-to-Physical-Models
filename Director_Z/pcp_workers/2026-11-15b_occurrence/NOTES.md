# Coordinator notes, 2026-11-15b occurrence (appended after every step)

Step 0. Read the two permitted inputs only (draft subsection; body subsections "Four arc gains" and "...winding...").
BLOCK: this agent has no Agent tool (not in its tool list, not among deferred tools; ToolSearch for it returned none).
No child of type pcp-builder / pcp-challenger / pcp-micro-review / pcp-formalizer could be launched. No child controls exist.
Decision: the coordinator does the narrow work itself, in scratch directories, and says so. Everything below is by ONE agent of
the author's model family: not independent review, and without even the reduction of exposure that separate children give.

Coordinator control: Cor. tp(iii): W(Y)=v(Y^2)+Y u(Y^2) has no root with positive real part; for u,v nonzero with non-negative
coefficients, equivalently: g=gcd(u,v) has only real non-positive roots, u/g and v/g have only real, simple, non-positive roots,
and these alternate in decreasing order, the LARGEST root belonging to v/g (the rail L polynomial).

Step 1. Reformulation used by the programs (derived from the proof of thm:tp, unrolled lattice): the state after t masks is
n_t: Z -> N (walk counts by deficit e = number of left steps); a mask is a set E of residues mod M;
n_t(e) = [e mod M in E](n_{t-1}(e)+n_{t-1}(e-1)); profile at a site = (classes c-1, c) of n_{T-1}: v_j=n(c-1+jM), u_j=n(c+jM).
Only M matters, not N.
