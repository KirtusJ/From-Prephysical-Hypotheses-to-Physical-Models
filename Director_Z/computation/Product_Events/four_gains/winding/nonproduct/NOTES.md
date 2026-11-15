# Non-product multisets, three classes (15 November 2026)

- Session B (GPT-6, comment 6897889046 on PR 283): two occurring five-walk non-products m_e, m_o whose rule value is forced by three coincidences m*P = g*(Q1*Q2); value = count + two squares. Director's recheck: all six identities hold in N[C2 x C3]; determinant 8.
- `python3 -B reach.py r_m5_p4_q5.json 5 4 5`: exit 0; control R0 FAILED (Session B's other two factors have size 6 > 4). Kept.
- `python3 -B reach.py r_m5_p6_q6.json 5 6 6`: exit 0; R0 passes. Of 146 three-coset multisets of size <= 5 in C2 x C3: 30 forced (rank 3), all agreeing with count + squares (R2: 0 failures); 116 not forced at these bounds, of which 54 pass the one-rail real-root condition for some cyclic order of levels. Occurrence on a ring is not tested.
- Next: larger factor bounds; occurrence of the 54 (total positivity is necessary, not sufficient).
