# FINDINGS (challenger working log; G1 v1.0 edge_record_walk theorem)
Reviewer: Claude sub-agent, same model family as the Director Z stack; author is Director G's agent. In-project review, not independent.
Read: specification.md, overview.md only. Checker, JSON, Lean of the author NOT read.

## Item 1. Hypotheses used by theorem + proof, and where stated
H1  update rule D(x+1,R)=u+v, D(x-1,L)=u-v; launch D_0=delta at (0,R)   -- stip 1, sentences 2-3. STATED.
H2  rings of arbitrarily large N (needed: a ring with N>2(t+1) for every t) -- stip 1 sentence 1; proof sentence 1. STATED.
H3  "each output has one parent site" (needed for site conservation)     -- stip 1 sentence 4. STATED.
H4  p_t(j)=f(D_t(j))/Z_t, Z_t over all 2N detectors                      -- stip 3 sentence 1. STATED.
H5  f common across ports (both rails, all sites), times, ring sizes     -- stip 3 sentence 2. STATED.
H6  f(0)=0                                                               -- stip 3 sentence 4 ("unreachable port is dark ... also at exact cancellations"). STATED. Load-bearing (see item 2e).
H7  f(1)>0, units f(1)=1                                                 -- stip 3 sentences 5. STATED.
H8  site conservation p_t(x,R)+p_t(x,L)=p_{t+1}(x+1,R)+p_{t+1}(x-1,L)    -- stip 2 last sentence, as consequence of: one marker; moves to one of the site's two outgoing ports; invariance under planned terminal time; ideal read; plus H3. STATED. The implication itself follows (hand check).
H9  f>=0                                                                 -- stip 3 sentence 2 (codomain [0,inf)). STATED; the proof never uses it (see 2e: needed only if rails may differ).
H10 Z_t>0 (p_t defined)                                                  -- NOT stated as such; follows on unwrapped rings from H6,H7 and the right front (Z_t=2^t); on wrapped rings only after f=k^2. Minor, implicit in H4.
H11 every tick t>=0 is an admissible terminal time on every ring, and conservation is applied between t and t+1 for every t>=0 including t=0,1
                                                                          -- only implicit ("planned terminal time", "common across ... times"). No explicit quantifier "for all t>=0, all N". GAP (minor, surrounding text).
H12 theorem sentence 2 (p_t=D^2/2^t on EVERY ring, wrapped or not) uses the bijection sites x {R-out,L-out} <-> 2N detectors plus the parallelogram identity -- given in the "Conversely" sentence of the proof, not in the forward part. STATED (in proof).
Hypotheses in the theorem sentence itself: only "On these rings, 1-3". Everything above lives in stipulations 1-3, so nothing the proof uses is outside 1-3 except the quantifier H11 and H10.
