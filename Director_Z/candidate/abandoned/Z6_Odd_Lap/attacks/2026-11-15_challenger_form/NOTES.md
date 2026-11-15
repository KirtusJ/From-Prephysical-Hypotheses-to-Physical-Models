# Challenger attack on Z6 "Odd Lap" FORM, 2026-11-15 (same model family as the author; not independent review)
Inputs read: CANDIDATE_PROCESS.md, FORM.md, SPECIFICATION.md, BRAND.md, G10 body.tex (Four arc gains .. Gains of bounded order; cor:composition), Mathematics module sec. 4.
Not read: function/, SPRINT folder.
CONTROL: (eps0,eps1)=(2,-1): (e0+e1)^2=1, (e0-e1)^2=9, e0^2+e1^2=5; the third is not one of the two squares of thm:fgtwo for k even (it is their mean; it is the single square only when k is odd).

## Run (exit 0, 19 s; rerun in a fresh directory byte-identical)
Command (cwd = this folder): `python3 attack_z6.py result_attack_z6_run1.json`  seed 20261115
sha256 attack_z6.py e0987c2f...cfa3f ; result_attack_z6_run1.json 05b28b77...8cc3b9
Qualifying O2 carriers: 140 (N=9: 40 in Z2xZ2, Z2xZ4, Z4xZ4, Z2xZ6; N=16: 30 in Z2xZ16, Z4xZ16, Z2xZ48; N=18: 20; N=20: 30; N=11: 20); tried/qualify per group in the file.
Failures: 0. Dead counters "P10_O2","P10_w" in counts_pass are unused (always 0); P10 data are under "P10".

## Target 1 (D2-D4): HELD
- D2: masks {-1},{-2,0},{-1},{0}: exactly walks LLRR, LRLR at (0,R), gains b+d+c+a and 2(b+c), quotient delta. 140/140: one vertex, 2 walks, class sums (0,0). Weight 2 alpha. Does not need prop:threegroups nor M>=8.
- D3: algebra identity exact on 6237 grid cases (and by hand: c+ + c- = q, 2(c+ - c-) = c). Events with one end vertex, two walks one level apart, of type (1,1) and of type (1,-1): found by own search on each ring (lengths M+1 or M+2), 140/140 carriers.
- D4: product multiset has (E0+-E1) = (e0+-e1)(e0'+-e1') (uses k even); mixtures c+ = 1/4,1/2,3/4 non-multiplicative, c+ = 0,1 multiplicative, 140/140. Hand: 16c+ = 16c+^2, 16c- = 16c-^2, c+ + c- = 1.
- Remark: non-negativity in O5 is not used once O6 is applied (c+,c- in {0,1} already); harmless redundancy.
## Target 2 (O5): HELD on the kill, with a labelling remark
- Under O1-O4 (D1) the third clause of O5 is EXACTLY alpha = 0: any vertex with class sums (0,0) has weight alpha*|m|, and one with |m|=2 exists. O5 excludes exactly the rules with alpha != 0; with the other two clauses it leaves alpha=0, q=1, |c|<=2.
- So D2 is a restatement of O5's third clause, not a derivation with content. FORM labels O5 "rule" stipulation and BRAND says "The count is removed by a stipulation (O5)". Labelled openly: not the Z1 kill.
- Without O5's third clause, O1-O4+O6+normalisation leave three rules: count, even square, odd square.
## Target 3 (symmetry): HELD; one sentence of FORM needs rewording
- Proof: for chi(delta)=-1, the vertex weight is |sum_w chi(beta)^level(w) (-1)^(LL-steps of w)|^2 (lem:fgkappa). So under O7 every allowed carrier gives the same weight to a given mask sequence (P8: 140/140), same for even. Fork at length M+1 has exactly two walks, quotient delta^(M-1) beta, weights odd/even = 0/4 (M odd), 4/0 (M even) (P6: 140/140). Hence no map of allowed carriers can carry odd weights to even weights.
- T1 switching (uniform), T2 rail reflection, T3 inversion, T4 power automorphism: image allowed, original odd character has value -1 on the image's beta, weights same (140/140 each). KILL predicate 0 hits.
- T5 (a,d)->(a+t,d-t), 2Mt an odd multiple of delta (exists for 6 of 140 sampled): image allowed, beta changes to beta+odd*delta, the ORIGINAL character has +1 on the new beta, and all weights under the candidate's rule are unchanged. This meets FORM's literal kill wording "a symmetry that changes beta while fixing every event weight" but is not a kill: it maps (X,odd) to (X',odd). The sentence should read "changes chi(beta)" as SPECIFICATION sec. 1 does. WORDING.
- D6: 120/120 closed-walk checks (N=3,4,5,6,9,16), gains M(b+c), 2M a, quotient beta, invariant under random non-uniform switching.
- P7: 20 random events of length <= M per carrier, odd = even, 140/140.
## Target 4 (O2): HELD; one WOUND-level finding
- O2 holds iff Delta_N = <delta> x Z2 with r even; so A must have non-cyclic 2-part: cyclic groups 0 qualifying (exhaustive Z2..Z16, Z6, Z12; random Z32). On N=16 (M=8) groups of exponent dividing 8 never qualify (beta = 8B = 0): Z2xZ2, Z2xZ4, Z4xZ4, Z2xZ8, Z2^3 all 0. Both sign maps are well defined on every qualifying carrier (proof: Delta/<delta> = Z2).
- The two squares never coincide on the multisets that occur (fork, proof above).
- FINDING: odd weights = weights of the unique square on a ONE-class carrier (s=1, outside O2) with beta an odd power of delta (Z2,(0,1,0,0) for M odd; Z16,(0,1,0,9) for N=16; Z4,(0,1,0,3) for N=20); even weights = plain signed ring Z2,(0,0,0,1). 5/5 rings on 13 events each, and it follows from the formula above. So O7 is weight-equivalent to a choice of carrier in which there is no rule choice. O7 is not empty, but "the sign is the only thing left to choose" is description-dependent.
- O7's "Equivalently" clause fixes the rule by itself; uniqueness under O1-O7 is then trivial; the content is "O1-O6 leave exactly two".
## Target 5 (brand, composites): WOUND (wording), not KILL
- Product formula: E0 = e0e0'+e1e1', E1 = e0e1'+e1e0'; odd x odd gives (E0-E1)^2 with class = parity of total winding. A lap of one part flips; a joint lap has chi(beta)^2 = +1. Consistent if a joint lap counts as two laps. BRAND's first commitment does not assert a composite sign; the one-line is scoped to "a ring" after the colon.
- "a history that has gone once more round is added with a minus": in the fork with M even the two histories one lap apart are ADDED (weight 4), net sign (-1)^M. The sentence is true only of the class sums, which carry their own signs.
