# b17 cor:multicar
CONTROL 20 (prog.py).
1 Realization PROVED, with one hypothesis made explicit: each x_y has out-degree exactly d,
 one arc to each y_z (no parallel arcs). Otherwise B undefined/continuation has extra walks.
 Proof: walks of length n from one start with given end and gain are distinct objects; abundance gives
 >= N per (x_y,h) at a common n, so pick count_h(m_y) of them; S has m_S(x_y)=m_y, empty elsewhere
 (x_y distinct vertices). Each walk ending at x_y with gain h has exactly the d continuations,
 gain B_zy h at y_z; so cont(S) has sum_y B_zy.m_y at y_z, nothing else. F(0)=0 gives (MBL) for all
 (m_y) with counts<=N; N arbitrary => all of M^d. x's overlapping y's harmless (different lengths).
2 Last sentence on infinite carrier PROVED true (events finite sets of walks, every vertex d out-arcs,
 no parallel arcs). v=v^psi_S finitely supported; (Av)_z=sum_y A_zy v_y finite sum (support finite);
 Av finitely supported (out-degree d). (A*A)_{yy'}=sum over common successors z: finite.
 ||Av||^2=sum_{y,y'} conj(v_y) v_y' (A*A)_{yy'} = d||v||^2: all sums finite, no convergence needed.
 Count: |cont S|=d|S|. Line k->k+-1 does NOT satisfy A*A=2 for any gains (k,k+2 share one successor)
 so it is vacuous, not a counterexample; signed arc digraph of the line satisfies it: COMPUTED P3 200/200,
 P4 (A*A!=2) 66/200 consistent, square fails.
