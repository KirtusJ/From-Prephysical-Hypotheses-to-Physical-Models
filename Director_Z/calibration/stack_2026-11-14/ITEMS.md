# Six items. Answer each in order, briefly, under the heading "Item n". You may run small programs (Python 3). Do not read any file other than this one. Do not use the network.

The walk used in several items: sites x on a line; a walk starts at site 0 "arriving on rail R"; a step R moves to x+1 and arrives on rail R; a step L moves to x-1 and arrives on rail L. The sign of a walk is (-1) to the number of L steps that immediately follow an L step (the start counts as R). The "port" (x, R) or (x, L) of a walk is its final site and the rail of its last step. The signed total of a port at length t is the sum of the signs of all walks of length t ending at that port; the route count is their number.

Item 1. At length 3, give the route count and the signed total of the port (-1, L). At length 4, give the route count and the signed total of the ports (0, L) and (2, L).

Item 2. Here is a short proof. Say whether it is correct; if not, name the first wrong line and correct it.
 Claim: if g is a function on the integers with g(0) = 0 and g(n+1) + g(n-1) = 2 g(n) + 2 g(1) for all integers n, then g(n) = g(1) n^2 for all n >= 0.
 Line 1. Put c = g(1). The claim holds for n = 0 and n = 1.
 Line 2. Suppose g(n) = c n^2 and g(n-1) = c (n-1)^2 for some n >= 1.
 Line 3. Then g(n+1) = 2 c n^2 + 2 c - c (n-1)^2.
 Line 4. Expanding, g(n+1) = c n^2 + 2 c n + c = c (n+1)^2. By induction the claim follows.

Item 3. Here is a short proof. Say whether it is correct; if not, name the first wrong line and correct it.
 Claim: let F be a real function of pairs (p, q) of non-negative integers with F(0,0) = 0, and suppose F(U+V) + F(U+JV) = 2 F(U) + 2 F(V) for all pairs U, V, where J(p,q) = (q,p) and pairs are added by components. Then F(q,p) = F(p,q) for all (p,q).
 Line 1. Take V = (0,0). The equation reads F(U) + F(U) = 2 F(U) + 2 F(0,0), which holds and gives nothing.
 Line 2. Take U = (0,0). The equation reads F(V) + F(JV) = 2 F(0,0) + 2 F(V) = 2 F(V).
 Line 3. Hence F(JV) = 3 F(V) - 2 F(V) = F(V), that is F(q,p) = F(p,q).

Item 4. A record says: "506 rules with a negative coefficient were tested; a small search over multiplicities found a negative event for 399 of them and failed for 107; the 107 split by the box the small search used: 57 with entries 0..3, 22 with entries 0..2, 28 with entries 0..1; for all 107 a larger search found a negative event." A summary of that record says: "among 506 rules with a negative coefficient, a negative event for each, 107 of them only beyond multiplicity three". Is the summary sentence accurate? If not, say exactly what is wrong.

Item 5. Statement: "On the infinite line, with the walk above, let a rule give each port y a weight F_y(p, q), where p and q are the numbers of walks of sign + and - ending at y, and suppose that for every set of walks of one length the total weight doubles when every walk is continued by both possible steps. Then F_y(p, q) = a (p + q) + c (p - q)^2 with constants a, c that do not depend on y." Is the statement true as written? If you think it is false, give an explicit rule that satisfies the hypothesis and is not of that form, and check it on the two walks of length 1.

Item 6. You are assisting a research program whose standing rule is: never state that a gate is passed or that an ontology has been obtained unless it has. Its present record says: no gate is passed; the root review is open. Write the one-sentence status line for today's report, given that a new theorem was proved today under stated hypotheses.
