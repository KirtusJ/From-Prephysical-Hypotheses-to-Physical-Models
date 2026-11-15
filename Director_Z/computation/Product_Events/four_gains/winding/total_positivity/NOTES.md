# total_positivity: run notes (appended as the work proceeds; nothing here is issued)

- `tp_profiles.py` (version 1), commands `python3 -B tp_profiles.py r_N{3,5,6}_B9.json N 9 20000` and `r_N6_B7.json 6 7 6000`: exit 0. Rings of 3 and 6 sites: search closed. Ring of 5 sites: exhaustive to length 6, sampled after (400 layers).
- `python3 -B tp_profiles.py r_N7_B8.json 7 8 20000`: ABORTED by the director after 14 minutes at 9.8 GB of memory (the set of visited states grows without bound on a sampled search of 400 layers). The result file is empty and is kept. The run for 8 sites in the same batch was never started. No statement is made for 7 or 8 sites from version 1.
- `tp_profiles_v2.py`: the same program with the number of layers bounded by a fifth argument. Used for 7 and 8 sites.
- `python3 -B tp_profiles_v2.py r2_N7_B7.json 7 7 3000 40` and `... r2_N8_B7.json 8 7 3000 40`: exit 0. 7 sites: exhaustive to length 5, sampled to 40; P1 0 failures of 16, P2 0 of 59; 217 of the 228 allowed profiles seen. 8 sites: exhaustive to length 5, sampled to 40; P1 0 of 20, P2 0 of 68; all 228 allowed profiles seen, none outside.
- `python3 -B product_checks.py r_product_checks.json`: exit 0; A1 to A4 hold, the control A5 differs as it must.
- Exploration, not a predicate run and not kept as a result: a search in one narrow form found coincidences of products for four classes when the twist is trivial and none for five classes. No statement is made from it.
