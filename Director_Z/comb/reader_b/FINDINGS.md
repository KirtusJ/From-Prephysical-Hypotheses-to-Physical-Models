FINDINGS (audit part b, lines 221-568 of body.tex + bibliography). Written progressively.
Computed (chk.py, chk2.py, outputs chk_out.txt, chk2_out.txt):
P1 coefficient 18 OK; two-input sub-predicate FAILED in chk.py (sympy simplify artefact; kept), follow-up chk2.py numeric: two-input hold, three-input fail, invariance OK.
P2 f(5)=625, f(3+4i)=-527, (V) for (1,i,-1,-i) OK on 81x81 box.
P3 U={1,2,4,5} and U={1,3,5} OK.
P4 Hadamard d=2,4, q=4: |a|^2, Re a^2, Im a^2 satisfy BL OK.
P5 local spectra q=1..12 OK.
P6 abundance 4-vertex example: A*A=2, r0=1, Dhat strongly connected, r=2, max 2 gains/vertex/length OK.
P7 M-combination identity OK symbolic.
P8 exponent -1.09 -> -1.1 OK.
P9 phi(q)=2 iff q in {3,4,6} OK.
P10 q=4 Hadamard sigma_2, Re sigma_1^2 satisfy MBL; q=2 all-ones count of gain 1 OK.
P11 normalized real Hadamard d=4 over Z: two-input instances alone give nullity 1 -> contradicts "with two inputs only the conclusion is false for d>=3" (line 380).
P12 thm:multiset dimension formula = exact nullity, 48/48 random matrices (q<=4,d=2,3,sizes<=3); all 48 satisfy d>=2.
P13 displayed d-odd equations hold for |a|^2.

Proof reading (prop:deg34, thm:fourier, thm:vsl, cor:vsl, prop:abund, cor:abund, thm:block, cor:block; also thm:multiset, cor:multiset, cor:multicar, prop:exact, prop:local): every step followed on my reading; NONE FOUND in the proofs. Hypotheses d>=2, q>=2 in cor:vsl/cor:block are automatic.

Findings:
1 DEFECT l.380 "with two inputs only the conclusion is false for $d\ge3$": only shown for d=q=3. False in general: normalized real Hadamard d=4 over Z, two-input instances alone give nullity 1 (P11); even-d Fourier blocks give the parallelogram law from two inputs (thm:fourier's own proof). Fix: "can be false, e.g. d=q=3".
2 DEFECT bib comp4s: no program for the multiset ranks (l.483 "62 matrices ... 216 of 216 \cite{comp4s}"), no Lean file for "Two steps of linear algebra" (l.380) or "Three steps of the proof" (l.483). All 12 cite keys defined, all bibitems cited.
3 GAP l.485 "A rule of first order is the count and is blind to the gains." prop:add needs switching-invariant additive rule, no loops, d out-arcs. B_q (l.126) and the l.328 example have loops; l.483 lists first-order block-law solutions that see gains (sigma_2, number of walks with gain 1).
4 GAP l.483 "...a rule that sees a walk only through its end vertex and its gain, and adds a function of what it sees over end vertices, is a combination of the count and of the squares" - "consistent under continuation with factor d" missing; also d>=2, cyclic group, F(0)=0, full block. Same omission l.380 "a rule that adds over end vertices \emph{any} function of the summed gains, and is unchanged by switching, is a combination...".
5 STALE l.238 "Other blocks, other degrees and gains of higher order are not treated; ... will enter as in Theorem conj" (treated by thm:fourier, cor:vsl). l.265 "Blocks that are not of this form, such as real Hadamard blocks of degree four ... are not treated" (covered by cor:vsl, cor:block, cor:multicar).
6 STALE l.485 paragraph: record-sum summary cites only thm:deg2/thm:power; omits cor:vsl, cor:abund, cor:block. "the form (phi), with the gains taken through a character, is itself a consequence" - conclusion is a combination of squares over several chi^j, j in U, incl. non-coprime j; not one character, not general phi.
7 STALE l.568 "The components are elementary or known: ..." list omits Nullstellensatz argument, block law, multiset law, kernel rules.
8 GAP l.328 "on a finite carrier with \hat D strongly connected the classification needs no hypothesis on events" omits A*A=d, d>=2, faithful character. Same line: "the proposition applies with that subgroup in place of C" needs a switching first (arc gains need not lie in the subgroup).
9 GAP l.528 "in none does a packet follow the ray of the mean field": packet displacement (d) reported for order 4 only; orders 3, 6 have only spread from one vertex.
10 GAP l.492 prop:exact: "exact translation of the quasi-momentum by Phi=2pi/n" not connected to lambda in statement or proof (lambda=e^{i Phi} implicit).
11 TERM: V = vertex set (l.303 "V x C") and R tensor R (l.278, 334-369); R, V used in thm:block statement but V defined only inside proofs. U = orthogonal matrix (l.346), index set (l.386), step (l.489). sigma_j = automorphism of R, j coprime (l.243..374) vs function on M for all j (l.383). M = M(a,b) l.256, symmetric matrix l.348, monoid l.383, M_m l.489. K = exponent l.284, coset l.309. varphi = Euler, gain, linear map (l.437). d = polynomial degree in l.288. "block": pair with common successor (thm:conj), Fourier block, "full block" (never defined; l.331, 373), block without B*B=d (l.476), "18 of them blocks" (l.483), staircase blocks (l.498). "walk" l.483 vs "history" l.485.
12 l.483 "(the multiset of 1 and -1 has sum zero and count two)" presumes even q.
Closest to a derivation claim (both conditional, not a claim that QM/Born rule is derived): l.485 "The second order of the rule of g8 is then a consequence and no longer a separate assumption"; l.483 "That gains with a common end vertex are added ... is then a consequence ... and not an assumption."
Status table: all 24 labelled statements present.
Not checked: g8/g9 lemmas cited, tables' values, counts of carriers, Lean claims, prop:abund beyond the one example.
