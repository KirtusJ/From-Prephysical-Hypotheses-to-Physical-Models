# Consistency demanded only on vertex product events (signed line, start (0,R))

Builder report; same model family as the director, not independent review. Nothing here passes a gate.

Notation. Vertices (x,R), (x,L). A pair m=(p,q) counts the walks of gain +1 and -1 of an event that end at
a vertex; swap(p,q)=(q,p). mu(S)=sum_y F_y(m_S(y)), F_y(0,0)=0. A product event of length t is given by
vertex sets A_1..A_t. "Realized at y at length t": m=m_S(y) for some product event S of length t.

## Lemma 1 (reduction to one position) -- PROVED
For a product event S of length t and a position x let S|x be the walks of S ending at (x,R) or (x,L).
(a) S|x is a product event (replace A_t by A_t ∩ {(x,R),(x,L)}); so is the restriction to any set of end vertices.
(b) mu(S)=sum_x mu(S|x), since mu is a sum over end vertices.
(c) Ext S is the disjoint union of the Ext(S|x); the walks of Ext(S|x) end at (x+1,R) or (x-1,L), and
    (x+1,R) has predecessors only at position x, (x-1,L) only at position x. So the end vertices of
    Ext(S|x) for different x are different and mu(Ext S)=sum_x mu(Ext(S|x)).
(d) If S|x has mR at (x,R) and mL at (x,L), then Ext(S|x) has mR+mL at (x+1,R) and mR+swap(mL) at (x-1,L)
    (the only arc of gain -1 is (x,L)->(x-1,L)).
Hence: mu(Ext S)=k mu(S) for all product events S  <=>  for every x and every pair (mR,mL) jointly
realized at ((x,R),(x,L)),
   (E)  F_{(x+1,R)}(mR+mL) + F_{(x-1,L)}(mR+swap mL) = k F_{(x,R)}(mR) + k F_{(x,L)}(mL).
Also F_y(m)=mu(S) for the event S restricted to y; so "mu as a function on product events" and
"F_y on realized pairs" carry the same information.

## Proposition 2 (the statement as posed is false on the infinite line) -- PROVED
F_y(p,q)=x(y)(p+q), i.e. mu(S)=sum over the walks of S of the end position, satisfies mu(Ext S)=2mu(S)
for every event: a walk ending at x has continuations ending at x+1 and x-1. It has F_y(0,0)=0 and is
not a|S|+c*sum(p-q)^2: the walks R and L are product events with weights 1 and -1, but both formulas give a+c.
Second family: F_{(x,R)}=(p-q)phi^x, F_{(x,L)}=(p-q)phi^(x-1), phi^2=phi+1: from (x,R): phi^(x+1)+phi^(x-2)
=phi^x(phi+2-phi)=2phi^x; from (x,L): phi^(x+1)-phi^(x-2)=phi^(x-1)(phi^2-phi^(-1))=2phi^(x-1).
So on the line F_y is not forced to be independent of y, even by all events. The hypothesis needed is
that F does not depend on the position (F_y=F or F_y=F_d, d the direction), or a finite ring.
(Checked exactly on all 272 one-position equations to length 5.)

## Proposition 3 (the factor) -- PROVED
(a) The factor does not follow: F_d(p,q)=(p-q)w_d, w_R=1, w_L=sqrt2-1 satisfies (E) with k=sqrt2 for all
events (w_R+w_L=sqrt2 w_R, w_R-w_L=sqrt2 w_L). It takes negative values.
(b) If F does not depend on the vertex and F(1,0)!=0, then k=2: the walk R^t is a product event,
its continuation has (1,0) at two vertices, 2F(1,0)=kF(1,0). (With F_d: F_R(1,0)+F_L(1,0)=kF_R(1,0) only.)

## Lemma 4 (what one step gives) -- PROVED
Let F=F_d or F, k=2, and let G=F-(a(p+q)+c(p-q)^2) vanish on all pairs realized at lengths <= t. If
(mR,mL) is jointly realized at length t, then by (E), linear in F and satisfied by the model,
   G_R(mR+mL) + G_L(mR+swap mL) = 0.
So at length t+1 the deviation is not zero but antisymmetric between the two continuation vertices.
This is why at every finite T the last layer has excess (computed: 2,2,3,6,12 for T=4..8, F vertex-independent).

## Statement T (the target, with the hypothesis in the form that survives) -- COMPUTED, NOT PROVED
Line, start (0,R), F_y=F_d (direction only) or F_y=F, F(0,0)=0, mu(Ext S)=2mu(S) for all vertex product
events S. Then F_d(p,q)=a(p+q)+c(p-q)^2 on every realized pair.
COMPUTED: for product events of lengths <= T, on all pairs realized at lengths <= T the solution space has
dimension exactly 2, for T=3..8 (exact rational rank; at T=8: 46305 one-position states, 769 pairs for F,
1333 for F_d). The same holds for POSITION product events (A_s unions of whole positions), T=6,7,8.
Realized pairs (some vertex), cumulative by length 1..8: 1,2,4,8,18,39,102,290. Length <=3: (1,0),(0,1),(1,1),(2,0);
length 4 adds (0,2),(1,2),(2,1),(3,0); not all pairs with p+q<=number of walks are realized.

The step I cannot prove: closing Lemma 4. One needs, for each pair u realized at length t+1, a second
relation for G(u) from product events of bounded greater length. The computation says length t+1 events
suffice for F independent of the vertex (pairs of length <= T are fixed by events of length <= T), but I
have no description of the jointly realized set (mR,mL) from which to write the induction. The proof of
Theorem 5.26 does not transfer: it uses arbitrary multisets at three vertices with a common successor.

## Where the line is -- COMPUTED
- End-vertex events only (reads at the final time): one extra rule on pairs of length <=5, stable T=7..10.
- Reads only at the last k times, k=2,3,4: extra rules remain for direction-dependent F (2 at length 6;
  3 at length 7; 2 at lengths 8-9, at T=10); for vertex-independent F the excess moves outward with T and
  is not settled.
- Reads at all times, positions only: no extra rule (T<=8).
CONJECTURED: position product events suffice; no family with reads confined to a bounded number of final
times does.
Not done: a further natural condition closing the gap for weaker families; rings beyond T=5
(rings 3,4,5 with vertex-dependent F: dimension 2 at lengths <=5; ring 6: 3 at T=5, not followed up).
