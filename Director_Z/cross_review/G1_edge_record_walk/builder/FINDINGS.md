# Builder findings on Edge Record Walk G1 v1.0 (14 November 2026)

Same model family as the director; nothing here is independent review. No gate is passed; nothing is an ontology.
Program `build_b1_b4.py` (exact, predicates in docstring), result `result_b1_b4.json` (mode 'x').
Notation: a port carries route counts a=(p,q)=(n_plus,n_minus); s(p,q)=(q,p); count n=p+q; signed total k=p-q.
Splitter on counts: rails (a,b) at a site go to a+b on the right daughter and a+s(b) on the left daughter.

## B1' Weakest additional premise on a response F(n_plus,n_minus)

### Theorem B1'.1 (PROVED). Premise W: site conservation for every signed-integer source array.
Hypotheses in the form used: F:N^2->R, F(0,0)=0, F(1,0)=1, and
(E) F(a+b)+F(a+s(b)) = 2F(a)+2F(b) for the pairs (i) a=0, b arbitrary; (ii) a arbitrary, b=(1,1); (iii) a=(j,0), b=(1,0), j>=1.
Conclusion: F(p,q) = (1-c)(p+q) + c(p-q)^2 with c = 1 - F(1,1)/2. Conversely every such F satisfies (E) for ALL a,b.
Proof. (i) gives F(b)+F(s b)=2F(b), so F(q,p)=F(p,q). (ii): s(1,1)=(1,1), so F(p+1,q+1)=F(p,q)+m, m=F(1,1);
hence F(p,q)=g(|p-q|)+m*min(p,q), g(j)=F(j,0). (iii): g(j+1)+F(j,1)=2g(j)+2, and F(j,1)=g(j-1)+m, so
g(j+1)-2g(j)+g(j-1)=2-m, g(0)=0, g(1)=1, giving g(j)=(1-c)j+c j^2 with c=(2-m)/2. Then m=2(1-c) and
F=(1-c)(|k|+2min(p,q))+c k^2=(1-c)n+c k^2. Converse: n is additive and n(s b)=n(b); k(a+b)=k_a+k_b, k(a+s b)=k_a-k_b,
parallelogram identity. QED.
Where (E) comes from (PROVED): on a ring N>=8, signed-integer launches at tick 0, conservation read at ticks 0->1 and 1->2.
A remote unit launch gives a site ((1,0),0) at tick 1 with daughters (1,0),(1,0): panel factor 2. Site y with R=(1,0),L=(1,0)
sends (1,1) to (y-1,L); site y-2 with R=(p,0),L=(0,q) [signed integers p and -q] sends (p,q) to (y-1,R): pair (a,(1,1)) at tick 1.
Pairs (0,b): b=(r,s) on (y-1,L) from site y with R=(r,0),L=(s,0), nothing at y-2. Pairs ((j,0),(1,0)): tick 0 directly.
Nonnegativity then requires 0<=c<=1 (F(1,1)=2(1-c)>=0; large k).
COMPUTED check: all pairs in the box [0..6]^2, 533 equations, nullity exactly 2, count and square both in the null space.

### Theorem B1'.2 (PROVED given one exact finite rank computation). Premise Q: F is additive up to a biadditive cross term,
i.e. F = al p + be q + ga p^2 + de pq + ep q^2. Then sharp-launch site conservation alone (the candidate's own stipulation 2,
no extra sources), read through tick 4, leaves exactly span{count, square}: nullity 5,4,3,2 for T=1,2,3,4 and 2 for T=5..10.
Lower bound 2 for all T is the converse of B1'.1; upper bound 2 is the exact rank at T=4 (machine step, 5 unknowns).

### What fixes a=0 (PROVED, arithmetic). With F=a n + c k^2, a+c=1, Z_t=2^t:
tick 3, port (-1,L) has counts (1,1): frequency 2a/8 = a/4; dark iff a=0.
tick 4, ports (0,L),(2,L) have counts (2,1),(1,0): frequencies (1+2a)/16 and 1/16; equal iff a=0.
Either of the candidate's two listed comparisons alone fixes a=0. So "sufficiency of the signed total" can be replaced by
(W or Q) + one of these measurements. a=1 is the fair-marker count law; a in (0,1) is a mixture the candidate does not list.

### Failed / not weaker
- Invariance under adding a cancelling pair, F(p+1,q+1)=F(p,q): this IS stipulation 3 (F depends on k only); no weakening.
  In B1'.1 it is equivalent to m=0, i.e. to a=0. So the tick-3 darkness measurement is exactly the test of this invariance at (0,0).
- Site conservation on the sharp launch alone with free F(p,q): not sufficient (coordinator's dimensions 1,2,3,5,...,37 for T=2..12; not redone).

## B4 General integer splitter [[a,b],[c,d]]: (u,v) -> au+bv right, cu+dv left

- PROVED: f(k)=k^2 satisfies f(au+bv)+f(cu+dv)=lambda(f(u)+f(v)) for all integer (u,v) iff ab+cd=0 and a^2+c^2=b^2+d^2 (=lambda).
  (Expand; compare coefficients of u^2, uv, v^2; pairs (1,0),(0,1),(1,1) suffice.)
- REFUTED as expected-stated ("solutions exist exactly for orthogonal equal-length splitters"):
  counterexample 1: [[1,1],[1,1]] (columns not orthogonal) admits f(k)=|k|: 2|u+v| = 2(|u|+|v|) on its all-positive totals. PROVED.
  COMPUTED: 72 non-orthogonal informative splitters (e.g. [[1,1],[1,1]], [[2,1],[1,2]]; none of the informative orthogonal ones) with entries in [-2,2] admit f=|k| on the sharp launch to T=7.
  counterexample 2: degenerate splitters (e.g. [[1,0],[0,1]], [[1,1],[0,0]]) keep one occupied port; every f with f(1)=1 works,
  so the square is consistent but not forced. 145 square-consistent non-orthogonal splitters, all non-informative. COMPUTED.
- COMPUTED (entries in [-2,2], 625 splitters, 464 informative, T=7): among informative splitters the square is consistent
  with stipulation 2 iff columns orthogonal with equal squared length (48 splitters). P4a pass, P4b fail (kept), P4c fail (kept).
- NOT SETTLED: whether, for an orthogonal splitter, the square is the only solution on the visited totals. It cannot be
  "f(k)=k^2 for every integer" in general: [[2,2],[2,-2]] visits only 1 and even totals, so f(3) is free (PROVED, trivial).
  CONJECTURED: for orthogonal splitters with ac != 0 the square is unique on visited totals.
- Corrected general statement: the square is selected by the splitter's column orthogonality; non-orthogonal splitters can
  select other laws (|k|), so the candidate's map row P3 ("which geometry selects the splitter") carries the Born exponent.

## B2, B3: dropped by the coordinator; not attempted.
