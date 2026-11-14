# NOTES xr72
CONTROL: resonant pulse area theta from state 0: P(1)=sin^2(theta/2): pi/2 -> 1/2, pi -> 1, 2pi -> 0.
Classical Markov: NO. If T sends 0 to (1/2,1/2), then (T^2)_{00} = 1/2*T00 + 1/2*T(0|1) = 1/4 + T(0|1)/2 <= 3/4 < 1 (convexity; T(0|0)=1/2).
step1: read both notes, checkers, lean file (done)
step2: six source files fetched (HTTP 200), sha256 equal to checker's pins. Checker A rerun from copy with --inputs: exit 0, byte-identical to filed JSON. Checker B rerun: exit 0, byte-identical. Lean 4.19.0 WitnessFlight.lean exit 0; axioms: sumEnvelope [propext], posteriorBound none.
step3: note A numbers vs filed JSON: every table entry, b values, p3, Y-witness values, log tails, 4.257%/17.028% agree with JSON (checked by reading).
 - FINDING A-line: JSON "line" for April rows is not the file's line number (grep -n: Gy(GxGy)^2Gx at 1317, 2037; JSON says 2633, 4073). Probably CR CR LF or lone CR line ends + splitlines(). To confirm.
 - selection rule excludes Gi-padded equivalents (e.g. Gi(GyGx)^1Gi 681/1425) - not stated in note.
 - GitHub API listing of upstream ExperimentalData dir: blocked for this session (repo not enabled) -> cannot verify that only six date files exist / none dropped.
 - derivations A (U matrix, order 3, p_j formula, W0=c+int x^2, classical l3-l2=u(1-u-v)^2) hand-checked: follow.
 - derivations B: W identity, gap bound M>=4, hard alternative moments, kl bound, Hoeffding constants, parity phase, posterior bound: follow by hand. q(1-q)>=1/8 "for sufficiently large M": fails for M=5,6 at small eta; holds all eta for M>=7 (to test).
step4: own program prog/xr72_check.py run 1 -> out1/xr72_result.json, exit 0. Failures kept:
 - A8_impure (my own relaxation, not the note's): 974 fail; my bound 4/27*l0 was wrong (s=u+v ranges to 2); correct elementary bound is l0. Not a note defect.
 - B5 kl bound: 108 fail among qualified -> suspect float cancellation at eta<=1e-3 (kl ~1e-20). Rerun as v2 with series kl; out1 kept.
 - B4: 7 failures (M=5,6 small eta) as predicted by hand.
step5: v2 program aborted on own assert (series radius) exit 1, no result written; v2 file kept; v3 uses series only when |d|/min(p,1-p)<0.05, direct formula otherwise.
step6: v3 run exit 0, result out2/xr72_result_v3.json, rerun in out3 byte-identical, overwrite refused (FileExistsError). B5 passes on qualified; in the 7 unqualified (M=5,6, small eta) the kl bound fails in 3.
step7: patch ion_line_numbers.patch written (line-number provenance for April). arXiv abs reachable; PDF figure 2 / section II D content NOT read (time).
