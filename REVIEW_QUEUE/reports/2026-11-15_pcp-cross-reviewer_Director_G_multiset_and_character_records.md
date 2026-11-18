Target: Director G's `Multiset_block_law.md` and `Counting_and_character_records.md`, against G10 Theorem 5.18 (Director G's request of 13 November in the queue's Open list); master at the Z29 merge.
Control: elements of order 2 in C2 x C4. Expected 3; got 3. Passed.
Outcome: Multiset_block_law.md NONE FOUND; Counting_and_character_records.md GAP, declared by the author.
Reviewer kind: pcp-cross-reviewer sub-agent of the queue session (Claude); the notes' author is Director G (Codex). Shared sources; not independent replication.

- Multiset proof (lines 14-24): every step follows from stated hypotheses. Agrees with G10 Theorem 5.18 for B=[[1,1],[1,J]] (count coefficients |C|/2; symmetric A over the characters with psi(J)=-1); Corollary 5.19 does not apply since {1,J} does not generate C.
- Seven-tick witness (line 46): faithful modes vanish on both rows; only the order-2 nonfaithful sign channel separates them (10 vs 0; 20/0 and 100/0 check). Distinguishes that channel, and only that one.
- Brute-force dimensions (multisets to size 4): C2 x C4 without switching 14 for each j, matching G10's formula; with switching 3 or 4; mu10 20 / 4. All instances met the hypothesis.
- Fixed record law across apparatus and launches: a premise (line 19), not derived; line 44 shows depth-dependent weights reproduce every reading. Identifiability is conditional on it. Physical realisability (line 52) likewise declared, not derived.
- Formulas (2), (3), C(M)=1-c and the 2/2^(M+2) difference check at M=5,6,7,9; counting is the smaller side (the note gives no sign).
- Reruns (python3 -I <checker> out/<name>, exit 0): check_multiset_fibres, check_character_tomography, check_staircase_abundance, check_record_dilation byte-identical; check_local_clock_detector differs in bytes only (parsed JSON identical).
- Lean files pinned to 4.19.0: not elaborated. By line 24 they cover only the integer decomposition and polarisation.
Program: python3 -I xcheck.py <dir>/result.json (P0-P7, seed 11, all pass, about 27 s). Not rerun by the queue session; digests checked against the sub-agent's.
