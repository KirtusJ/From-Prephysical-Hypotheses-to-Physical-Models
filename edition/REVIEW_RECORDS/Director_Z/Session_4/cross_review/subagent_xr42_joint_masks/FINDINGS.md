# xr42 findings (append-only)

## Step 0. Target mismatch
The named target Director_G/Joint_residue_masks.md does NOT contain the claims in the pull-request summary
(six ticks, eight-tick panel when 4|M, summed residue, 5,5,4 over 65536). Those are in
Director_G/Independent_walks_and_shared_gains.md (checker check_product_gain_fibers.py, result
results/product_gain_fibers.json, Lean lean/SharedGainPurity.lean). Joint_residue_masks.md is the
"separate residues, larger two-dimensional character family" note (checker check_joint_residue_preparation.py).
Both reviewed; each finding names its file.

## Step 2. Reruns from a copy (scratch/copy, python3 -B <checker> OUTDIR as docstrings say)
- check_joint_residue_preparation.py -> rerunA/joint_residue_preparation.json : byte-identical to stored
  (sha256 66efc1ad...); second run refuses: FileExistsError. MET.
- check_product_gain_fibers.py -> rerunB/product_gain_fibers.json : byte-identical (sha256 6fedaf18...);
  second run refuses: FileExistsError. MET.
- Tick formula (5M+3)K+6+P+N+1 checked by hand against stored ticks (667,1495,84,107,130,176,199): consistent.
- 72+128+200+392+512 = 1304: consistent.
- NOTE: "isolated output rail pair and unrestricted successor signs" were run at M=3, one target (11,1) only;
  crossed-arm control at M=5 only; "every sign and residue pair" at M=3,4 has multiplicity one per bin.

## Step 3. Own program own_check.py -> own_result.json (mode 'x'; second run refused)
Exact integer arithmetic in Z[x]/(Phi_M). M = 3,4,5,6,8,12 (note) and 7,9,16,20 (not reported by note).
- H1 (three settings share one signed joint histogram, one end well, rail R, equal ticks): true in 30/30 (M,panel).
- P1 M=4 six ticks half count + half s=1: 4,4,4 MET.  P2 eight ticks: 5,5,4 over 65536 MET.  P3: 10,10,9 over 4096 MET.
- P4 forced purity under the note's prescribed test: 334023 ordered law pairs, all qualify; 63 pass,
  all 63 are A=B pure; 0 violations either direction. MET at 10/10 orders.
- P5 six-tick alone: MET at M=3,5,6,7,9; FAILED at M=4,8,12,16,20 (23,23,23,14,14 non-pure passes) - as the note says.
- P6 eight-tick alone (no claim in note; measured only): MET at 3,5,6,7,9; FAILED at 4,8,12,16,20
  (s=M/4 and s=M/2 both give response 1).
- P7 BB/BH/HH first row (algebra only, mask preparation not redone): MET 10/10.
- P8 single oriented equality: FAILED at 8/10 orders (met only at M=5,7) - the note states this failure.
Grid: weights multiples of 1/4 (1/3 for M>=16). A grid is a finite sample, not a proof; proof is the note's variance identity.

## Step 4. Lean (4.19.0, commit 6caaee842e94, scratch copies)
SharedGainPurity.lean, MultisetBlock.lean, ResidueControlWords.lean: exit 0, no sorry/axiom;
one_fiber_purity, two_margin_purity, moments_force_center: [propext, Quot.sound].
Formalized: finite list, Nat weights, Int responses, Int means; zero variance + injective response => one label.
NOT formalized: the walk, masks, histogram equality, multiplicativity f(U*V)=f(U)f(V), injectivity of the
response (hypothesis `inj`), real weights, irrational responses (cos 2 pi s/M rational for all s only at M=3,4,6).
Joint_residue_masks.md links no Lean file; MultisetBlock.lean (via Multiset_block_law.md) is Int-valued F,
the note uses real F.

## Step 1. Hypotheses / derivations
Joint_residue_masks.md: all premises (finite nonneg F_v, F_v(0)=0, depends on gain multiset only, additive
over ports, stationary over depth and program, one common k, some positive score, M>=3, accessible parity
component, coherent joint masks) are in section "Walk and score". Steps k=4, strong connectivity (unit shift
RLR/LRR, sign loop RLRLLR x LLLRRR), max principle, 2F(U+V)+2F(U+JV)=4F(U)+4F(V), pair removal, parallelogram,
PSD, Fourier: each FOLLOWS (rechecked by hand). GAPs: (a) "any prescribed signed multiset" for every M rests on
the construction argument plus the single-walker isolation table in another note; checker covers 5 orders,
complete bins only at M=3,4 with multiplicity one; (b) last paragraph's "It also tested each isolated output
rail pair and the unrestricted successor signs" is M=3, one target; (c) real-valued polarization is by hand.
Independent_walks_and_shared_gains.md: "must" is analytic (variance identity + strict monotonic cosine), not the
144-pair run. Premises stated in text: local laws in the single-walk family with fixed weights, product
independence, sufficiency, same M, same clock/port. GAP: the pull-request summary drops the family premise.
Nothing in either note concerns "pointer sectors": no statement to check.

## Step 5. Comparison with the earlier statement
Joint_residue_masks.md: DIFFERENT - it is the classification stage (a|U| + sum b |char sum|^2 on {+-1} x Z_M^2),
no selection; whole convex family survives.
Independent_walks note: same conclusion class (count or one folded class; zero excluded by normalization),
different hypothesis: no joint rule of the family is assumed multiplicative; instead two possibly different
local laws, product independence and a detector that is any function of U*V; three settings at 6/8 ticks
instead of all large lengths. Stronger in hypothesis economy, narrower in group (cyclic only).
No repository change required; no patch written.
