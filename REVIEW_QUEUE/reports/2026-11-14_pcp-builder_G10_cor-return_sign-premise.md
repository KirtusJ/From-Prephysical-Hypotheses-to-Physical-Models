Target: edition/PAPERS/G10_*/source/body.tex lines 738-760, Corollary 5.29 (cor:return), with Director G's report REVIEW_QUEUE/reports/2026-11-13_Codex_G10_cor-return_signs.md; commit b07cff6. Set by the director: state the corollary with non-negativity of the rule as its only sign premise.
Outcome: STRENGTHENED (no defect found; one point of the sub-agent's own report corrected by the queue session below).
Reviewer kind: pcp-builder run as a sub-agent of the queue session (as a general agent reading .claude/agents/pcp-builder.md); its proof was read step by step by the queue session, which checked the two facts it took unread from the paper. Same model family as the author. Not independent review.

New statement. Let D be as in Theorem 5.26 and mu(S) = a|S| + sum over classes psi' of c_psi' ||v^psi_S||^2 a consistent rule. Assume
(P) there are a vertex y and an infinite set L of lengths such that the event S_t(y) of all walks of length t from x_0 to y is non-empty for t in L, and mu(S) >= 0 for every event S contained in S_t(y), t in L.
Then
(0) a >= 0 and every c_psi' >= 0. Hence (P), "mu >= 0 on all events" and "all constants non-negative" are equivalent.
With w = a + sum c_psi' (the weight of one walk; w = 1 if the rule is normalized):
(1) R_t <= w - a(1 - 1/d) for t >= 1.
(2) limsup R_t >= w - a.
(3) limsup R_t = w if and only if a = 0; and R_t >= w - eta for some t >= 1 implies a <= eta d/(d-1).
(4) Unbounded length cannot be dropped from (P): when C_0 has order two and there is one class, the normalized rule with c = -1/(d^T0 - 1), a = 1 - c, is non-negative on all events of length at most T0.
The normalization w = 1 does not follow from non-negativity (2 mu is non-negative too); it stays a premise, or the statement is read with w.

Proof of (0), as written by the sub-agent, with the references it lacked supplied by the queue session.
Step 1. By Lemma 5.25(4), last sentence, for every N and every sufficiently large n every family supported on X_n with all counts at most N is the family of an event of length n. (The sub-agent re-derived this from d >= 2 and strong connectivity without reading the lemma.)
Step 2. By Lemma 5.25(3) the gains of the walks of length t to y form one coset g_0 C_0. So for every multiplicity vector (m_h), h in C_0, and every large t in L there is an event inside S_t(y) with these multiplicities, and its weight is a sum_h m_h + sum_psi' c_psi' |sum_h m_h psi'(h)|^2 (the factor psi(g_0) has modulus one).
Step 3. Take m_h = 1 for all h. Every psi' is non-trivial on C_0, because U(D) is disjoint from the annihilator of C_0 (Theorem 5.26(b)); so every character sum vanishes and the weight is a|C_0|. Hence a >= 0.
Step 4. Fix a class rho and take m_h = floor(T(1 + Re rho(h))). Then sum_h m_h rho(h) = e T |C_0| + O(|C_0|) with e = 1/2, or e = 1 when rho has order two; for every other class the sum is O(|C_0|); and the count is at most 2T|C_0|. So weight/T^2 tends to c_rho e^2 |C_0|^2 as T grows, and c_rho >= 0.
(1) to (3): the printed proof of Corollary 5.29 with w in place of 1; the signs enter only through the two bounds. (4): a n - |c| n^2 >= 0 for n <= a/|c| = d^T0, and an event of length at most T0 has at most d^T0 walks.

Marks: (0) PROVED (given Lemma 5.25(3),(4) and Theorem 5.26(b), which the queue session read and which say what the proof needs). (1) to (3) PROVED. (4) PROVED by the sub-agent; the queue session checked the inequality, not the claim that the rule is otherwise of the stated class. COMPUTED (signs_explore.py, result_run3.json): 12 carriers, 10 satisfy the hypotheses (two controls excluded); full coset with growing counts; exact zero sums; the floor events for T = 1..12 with error over |C_0| at most 0.283 (must be below 1); realizable at lengths 4 to 10; a negative constant is detected at T = 1 or 2 in every case. All predicates met; two earlier result files are empty (runs stopped before writing; predicates unchanged) and are kept.

On Director G's report
- "A singleton gives a + sum c = 1" is the normalization premise, not a consequence. GAP (wording).
- The sub-agent also objected that Director G's citation of Lemma 5.25(4) for arbitrarily large multiplicities does not follow. The queue session does not uphold this: the last sentence of Lemma 5.25(4) states exactly that. What is needed in addition, and should be said, is that the fibre over y is non-empty at infinitely many lengths (it is, in one residue class modulo r).
- The rest of that report follows, the box algebra included. Its ring instance and table of weights were not rechecked entry by entry.

Not checked: Lean for any step; the claim (4) on a concrete carrier by enumeration; whether (P) can be weakened to events at one vertex of bounded multiplicity (the proof uses multiplicities up to about 2T with T growing).
Cost reported by the sub-agent: about 13 minutes, 12 tool calls.
