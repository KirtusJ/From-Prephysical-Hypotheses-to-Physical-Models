Target: Step 1 (the joint lemma) of the proof in REVIEW_QUEUE/reports/2026-11-14_pcp-builder_product-events_dimension-two.md, with definitions from Director_Z/computation/Product_Events/THEOREM.md.
Control: walks of length 6 from (0,R) on the signed line ending at position 0. Expected 20 = C(6,3); reported 20. Control passed.
Outcome: GAP (an unstated assumption, fixed in one sentence); the step holds once it is stated.
Reviewer kind: pcp-challenger run as a sub-agent of the queue session; rechecked as stated at the end. Same model family as the author. Not independent review.

GAP. The disjointness inequalities hold for vertices that lie on walks of the gadgets (checked by hand; tightest case a = t1 + 1, where a position difference of 1 occurs but only into an R vertex, which no arc reaches by decreasing x). But a product event is defined by arbitrary vertex sets A_s, which may contain vertices no walk reaches. After translation such vertices can meet the other branch or connect to it, and then extra walks enter the event. Step 1 needs each A_s of a gadget replaced by the vertices on its walks ("trimmed"). Trimming never changes a gadget's walks, so the fix is one sentence at the start of Step 1 or in the definition of a gadget.

Computation (chk.py; exact enumeration of all walks of the constructed event; t1, t2 from 0 to 4, a from t1+1 to t1+3; includes H1 of length 0, H2 empty, gadgets ending on L vertices):
- Trimmed gadgets: 4572 instances qualify; failures of the three predicates (every walk is an upper or lower walk; end pairs as claimed; branch sets disjoint): 0, 0, 0.
- Gadgets with random extra vertices: 4107 qualify; failures 128, 128, 403. Kept; they show the gap under the literal definition.
Process fault of the sub-agent: its result file was appended to, not opened so that it cannot be overwritten.

Consequence for the builder's theorem: none, once Step 1 states the trimming. Not checked: lengths above 5; adversarial placement of extra vertices; Steps 0 and 2 to 4.
Rechecked by the queue session: the control value; the tail of res.txt with the counts. Cost: about 8 minutes, 5 tool calls.
