# FINDINGS (builder, same model family as the director; not independent review)

## 1. Before any run (hand results; program build_prod.py written, predicates in its docstring, not yet run at this point)
- Lemma 1 (PROVED, see THEOREM.md): the law for a product event S is the sum of the laws for S restricted to one end position x; each restriction is a product event. So the whole demand is the set of two-vertex equations
  F_{(x+1,R)}(mR+mL) + F_{(x-1,L)}(mR+swap(mL)) = 2 F_{(x,R)}(mR) + 2 F_{(x,L)}(mL)
  over jointly realized (mR at (x,R), mL at (x,L)).
- REFUTED as posed (line, F_y depending on the vertex): F_y(p,q)=x(y)(p+q), i.e. mu(S)=sum over walks of the end position, satisfies mu(Ext S)=2mu(S) on ALL events and is not a|S|+c*sum(p-q)^2 (walk R has weight 1, walk L weight -1). Also F_{(x,R)}=(p-q)phi^x, F_{(x,L)}=(p-q)phi^(x-1), phi golden ratio. So on the infinite line F_y is NOT forced independent of y; independence of position must be assumed (or a finite ring used).
- Factor: does NOT follow in general. F_d(p,q)=(p-q)w_d, w_R=1, w_L=sqrt2-1 is consistent on all events with factor sqrt2. It follows (c=2) if one single walk has nonzero weight and both its continuations have the same weight as it.

## 2. Runs (build_prod.py -> result_T5.json; run2.py -> result_run2.json; exact rational rank; no failed hypothesis test: P1 passes on every equation of every run)
"Excess at L" = dim(solution space projected to unknowns first realized at length <= L) minus 2.
- P2, P3 PASS (line, F independent of vertex / depending on direction only, ALL vertex product events of length <= T): excess 0 at every L <= T, for T = 3..8 (T=8: 46305 one-position states, 769 / 1333 unknowns). At L = T+1 (last layer, unknowns with no later equation) excess > 0, as expected.
- P4 FAILS as predicted (line, F depending on the vertex): excess 3 to 5 in the interior at T=5. Kept. P6 PASS: x*(p+q), golden-ratio rule, and the sqrt2-factor rule satisfy all 272 equations exactly.
- P5 (rings, F depending on the vertex, T<=5): ring 3, 4, 5: excess 0 at L<=5 when T=5; ring 6: excess 1 at T=5 (FAILED predicate at this range, kept; walks have not yet wrapped enough, not followed up).
- P7 subfamilies. Position product events (A_s unions of whole positions): excess 0 at L <= T, T=6,7,8. Reads only at the last k times: k=1 (end-vertex events): excess 1 at L=5 stable for T=7..10 (agrees with the attack report). k=2: direction-dependent F excess 2 at L=6 for T=9,10; vertex-independent F excess 3 at L=7 at T=10 (was 7,5,5). k=3: direction-dependent excess 3 at L=7 (T=9,10); k=4: direction-dependent excess 2 at L=8..9 at T=10. So no fixed window of recent reads was seen to suffice; reads at all times do.
- Realized pairs (p,q) at some vertex, cumulative count by length 1..8: 1, 2, 4, 8, 18, 39, 102, 290 (769 with length 9 from continuations). Lists to length 5 in result_T5.json.
## 3. Proof status
Main classification on product events: NOT PROVED. THEOREM.md gives the proved reduction, the proved one-step relation, and the exact missing step.
