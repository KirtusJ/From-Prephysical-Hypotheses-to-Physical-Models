Target: G10 Theorem 5.26 (thm:periodic) on carriers whose derived digraph is not strongly connected (director's Z21 request): (a) closed-walk gains in a proper subgroup; (b) two terminal classes. Master a8c9608.
Control: is the digraph 0->1, 1->0, 1->2 strongly connected? Expected no; reported no. Control passed.
Outcome: NONE FOUND against the theorem (its hypothesis excludes these carriers); what holds there is stated below.
Reviewer kind: pcp-micro-review run as a sub-agent of the queue session. Same model family as the author.

Method: exact rational solution of the consistency equations on every event from x0 of lengths 0 to 3, each continued to length 4; d = 2; U(D) from A*A = d; dimension counted as functions on those events.
(a) Proper subgroup (the derived digraph splits into copies, one per coset): Z2 with trivial gains, all four arcs: 1 (theorem's formula 1); Z4 with gains in {0,2}, Hadamard step: 2 (formula 2); Z3, three vertices: 1 (formula 1). The conclusion holds: only the component of (x0, 1) is reached, and it behaves as a strongly connected carrier.
(b) Two terminal classes (x0 transient, branching into two closed two-vertex blocks): trivial group: 2 against 1 (a separate count on each class); Z2 with two Hadamard blocks: 4 against 1 (a count and a square on each class; U(D) of the whole carrier is empty because the arcs out of x0 spoil A*A = d); one Hadamard and one trivial block: 3 against 1. With several terminal classes the rules decouple class by class, and U(D) of the whole carrier misses the characters of each block.
Limit: dimensions from events of length at most 3 only; stability at larger lengths not tested.
Rechecked by the queue session: the control; the dimensions in out.txt.
