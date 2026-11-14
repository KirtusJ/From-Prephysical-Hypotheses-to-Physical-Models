# Builder, Product_Events Statement T (written before reading the folder's FINDINGS.md or programs; not compared afterwards)
Same model family as the director. Nothing here passes a gate.

## Reading of the statement
Carrier: vertices (x,R),(x,L), x integer; arcs (x,d)->(x+1,R) gain +, (x,R)->(x-1,L) gain +, (x,L)->(x-1,L) gain -.
Vertex product event of length t: all walks of length t from (0,R) whose s-th vertex is in A_s, A_s ARBITRARY vertex sets.
(Equivalently: all lattice paths inside an arbitrary set of space-time edges; (x,d) at time s is the edge into x.)
Direction-dependent F: two functions F_R,F_L on N^2, F_d(0,0)=0, mu(S)=sum_y F_{d(y)}(m_S(y)). Factor two: mu(Ext S)=2mu(S).
Ambiguity: (A) all lengths, pairs realized at any length [Statement T as worded]; (B) the truncation "events of length <=T,
pairs realized at lengths <=T" [the COMPUTED line]. (A) is proved below. (B) is NOT obtained: the proof uses longer events.

## Theorem (PROVED)
Let F_R,F_L: N^2->R, F_d(0,0)=0, and mu(Ext S)=2mu(S) for all vertex product events S from (0,R) of all lengths.
Then (1) every (p,q)!=(0,0) is realized, alone, at an R vertex and at an L vertex;
(2) F_R=F_L=a(p+q)+c(p-q)^2 on N^2, a=(4F_R(1,0)-F_R(2,0))/2, c=(F_R(2,0)-2F_R(1,0))/2;
(3) conversely these satisfy the condition on every event; n and s^2 are independent ((1,0):1,1; (2,0):2,4). Dimension exactly 2.

Proof. "Gadget for u": product event all of whose walks end at one vertex y, with m(y)=u. P_d = pairs having a gadget ending
at a d-vertex.
Step 0. If H is a gadget for u ending at (x,d), appending A={(x+1,R)} gives a gadget for u at an R vertex; appending {(x-1,L)}
gives u (d=R) or swap u (d=L) at an L vertex. Hence P_L subset P_R, P_R subset P_L, swap P_L subset P_L: P_R=P_L=:P, swap P=P.
Step 1 (joint lemma). Let H1 (length t1, end (x1,d1), pair u) and H2 (length t2>=0, end (x2,d2), pair v; t2=0: empty event,
x2=0, v=(1,0)) be gadgets, a>t1. Define the vertex sets: upper branch (1,R) at time 1; H1 translated by (time+1, x+1) at times
2..t1+1; then k=a+t2-t1>=1 steps R. Lower branch (-s,L) at times s=1..a; (1-a,R) at time a+1; H2 translated by (time+a+1,
x+1-a). At T0=a+1+t2 the branches are at single sites xU=x1+1+k, xL=1-a+x2. Sites: upper at time s<=t1+1 has x>=2-s, later
x>=s-2t1; lower has x=-s for s<=a and x<=s-2a after; since a>t1 the two branches share no site after time 0 and
xU-xL>=2(a-t1)>0, even; D=(xU-xL)/2>=1. Continue upper by L^(D-1), lower by R^(D-1) (sites still distinct), then upper L,
lower R, both to X=xU-D. A walk through the union of the vertex sets cannot change branch (no common site after time 0), so
the event is the disjoint union of {R.w.R^k L^D: w in H1} and {L^a R.w.R^D: w in H2}. The translated w keeps its gain
(it is entered by an R step, as at the start); the suffix multiplies all gains of a branch by one common sign. So the event has
exactly u' in {u,swap u} at (X,L) and v' in {v,swap v} at (X,R).
Step 2. Singles: (mR,mL)=(u,0), u in P: F_R(u)+F_L(u)=2F_R(u), so F_L=F_R=:F on P. (0,u): F_R(u)+F_L(swap u)=2F_L(u), so
F(swap u)=F(u) on P.
Step 3. P=N^2\{0}. (1,0) in P (walk R). If u in P, Step 1 with H2 empty gives e in {(1,0),(0,1)} at (X,R), u' at (X,L); the
continuation has e+u' at (X+1,R) and e+swap u' at (X-1,L), each alone after restriction; with swap P=P this puts both
u+(1,0) and u+(0,1) in P in each of the four sign cases. Induction on p+q.
Step 4. G=F-a n-c s^2 with a,c as in (2): G(1,0)=G(2,0)=0, G symmetric, and by (E) (linear, satisfied by n and s^2) for all
u,v != 0:  G(v'+u')+G(v'+swap u')=2G(u)+2G(v); by symmetry of G the left side is G(u+v)+G(u+swap v) in all four sign cases.
u=v=(1,0): G(2,0)+G(1,1)=0, so G=0 on totals <=2. Suppose G=0 on totals <=N, N>=2; g(p):=G(p,N+1-p).
v=(1,0), |u|=N: g(p+1)=-g(p), p=0..N. v=(2,0), |u|=N-1: g(p+2)=-g(p), p=0..N-1. So g(p)=g(p+2)=-g(p)=0 for p<=N-1, and
g(N)=-g(N-1)=0, g(N+1)=-g(N)=0. QED.

## Claims
- Theorem (1)-(3), reading (A): PROVED (above).
- The |v|=2 joints are needed: with singles and lone-path joints only, nullity 4 at totals <=6: COMPUTED (extra solutions
  on even totals 4 and 6, as the hand count G(p,q)=(-1)^p h_N predicts).
- Construction and rank: COMPUTED, NMAX=6: 102/102 calls satisfy the hypothesis; Q1 0 failures (11 also by brute enumeration,
  0 failures); Q2 no pair missing; 54 unknowns, 136 equations, nullity 2 with span {n, s^2}; longest gadget 67 steps.
- Reading (B) (length <=T events fix pairs of length <=T): not proved here; stays COMPUTED by THEOREM.md.
- Position product events: not treated (the gadgets use vertex sets that split positions).
## Failed / not done
- No sign control in Step 1 was obtained (u' vs swap u' depends on D); avoided by symmetry of G, not solved.
- No Lean: Step 4 is three lines of integer-indexed algebra; not formalized.
Files: joint_gadgets.py (construction + exact rank), result_joint_gadgets.json, rerun/r.json (byte-identical).
