WOUND. S2 demands far more than any instrument selects, and the surplus is unphysical; but D1 is not killed: on instrument-selectable product events the classification comes out the same at every length computed. S2 must be narrowed and D1 re-proved under the narrowed demand.

Attacker: sub-agent of the model author's family (Claude); not independent review. Target: S2, W1, on Z1-R. Details: FINDINGS.md.

**Method.** Rules mu(S) = sum over end vertices of F_y(multiset of gains), F_y(0) = 0; unknowns are the values on the multisets that occur. Consistency mu(Ext S) = 2 mu(S) is imposed only for S in a family, lengths 0..T. At finite T even the full demand leaves more than two rules, so each family is compared with the full demand at the same T: excess = dim(family rules) minus dim(restriction of all-event rules), also after projecting to multisets of lengths <= L ("interior"). Exact integers. Baseline, all events: interior dimension 2.

**What S2 demands beyond instruments.** On every vertex product event (a set of vertices prescribed at each time; 725808 outcome sequences, t <= 4) the model's weight equals the quantum sequential-measurement value ||P_{A_t} A ... P_{A_1} A e_0||^2 exactly; on 424 product partitions the cells sum to 2^t. Elsewhere the weight is not a probability: at t=4, 1351 of 65535 events exceed the total, maximum 25/16 (W1: 9/8); none of the 4287 product events does. It also disagrees with quantum mechanics where an instrument does select the event: read the vertex at every step (t=3) and keep "anything but R,L,L": quantum 7/8, model 9/8; they differ on 96 of 255 such post-processed sets.

**Does the classification need those events? Not as far as computed.**
- Product events: excess 0 at every depth, T = 3, 4, 5 (315376 events at T=5).
- Two reads: excess 0 through T=5; at T=6 (563535 events) 0 in the interior, 1 at the last length.
- Position product events: 0 in the interior, 1 to 3 at the last length.

**Where D1 fails: demands weaker than product events.** Interior excess, stable as T grows to 8:
- end-vertex events, one step of continuation: 1 at lengths <= 5;
- end-position events: 2 at lengths <= 4;
- single-vertex reads: 1 at lengths <= 4;
- cylinders: 4 at lengths <= 4, 9 at lengths <= 5;
- one read described at all later lengths: 3, 3, 2 at lengths <= 6 for T = 6, 7, 8, though the end-vertex distributions to length 6 are still forced into the model's family.

Explicit rule for end-vertex events: F = square + delta/1152, with delta on multisets (number of +1, number of -1): F_L(3,1) = -288, F_R(4,0) = 288, F_R(2,2) = 288, F_L(2,4) = -288, F_R(3,3) = 288 at lengths <= 5. It is non-negative, gives a single walk weight 1, satisfies all 17267 end-vertex equations to length 7, and still extends at T=8. At t=5 it gives the model's dark vertices (-1,R) and (1,R) 1/128 each. A final read alone does not force the Born distribution; a second read does.

**Conclusion.** (1) S2 as written constrains weights that exceed the total and contradict quantum mechanics; no physical demand does that. (2) That surplus is not what yields the rule: consistency on product events (later steps do not change the statistics of earlier reads) leaves the same two rules to T=5. (3) The proof of Theorem 5.26 uses arbitrary families of multisets; product events reach 70 of the 88 multisets at T=5. Under the narrowed S2 the theorem is unproved.

**Not tried.** Product events beyond T=5; wrapping rings; other carriers; a proof.
