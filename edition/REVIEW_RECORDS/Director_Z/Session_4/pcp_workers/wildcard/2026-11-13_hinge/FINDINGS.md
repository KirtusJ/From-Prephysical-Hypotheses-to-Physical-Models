# Wildcard, seed "hinge" — FINDINGS

Chosen: the return premise on which candidate Z1 turned (G10 Cor. 5.29; WHY_ABANDONED.md "Return is late or never exact"), because the director records the attacker's return table as not recomputed.

## Program
ring_return.py (predicates P1-P5 in docstring before first run; exact integers, no tolerance; result opened 'x').
run1/ring_return_result.json (first run, has "seconds"); run2/, run3/ reruns byte-identical
(sha256 18d20f9044c314ff84a630feec81edb73330bd51b157f49d2e9323073d90dedd). All five predicates true; none failed.

- P1: signed ring, N=2..40: U periodic iff N in {2,4,8} (cyclotomic factor test of charpoly(A^2)(2x)).
- P2: least t with A^t = 2^(t/2): 2, 8, 24.
- P3: exact return R_t=1 at x0=(0,R), N=3..12: first at t=8 (N=4), t=24 (N=8), none otherwise
  (N=4,8,9,11 to t=100000; N=3,5,6,7,10,12 to t=20000 only).
- P4: first t with R_t>99/100: 38, 8, 264, 38, 504, 24, 95946, 264 (N=3..10), none to 100000 (N=11), 6416 (N=12). Agrees with the Z1 record in every entry.
- P5: rings 3,4,5,6,8 return above 0.99 below t=4000; rings 9, 11, 12 do not.

## Proof: exact return is periodicity (signed ring)
If |(U^t)_{x0x0}|=1 then U^t e_(0,R) = λ e_(0,R). Translation commutes with U, so U^t = λ on all R-states.
U e_(0,R) = (e_(1,R)+e_(-1,L))/√2 and U^t commutes with U, so U^t e_(-1,L) = λ e_(-1,L); by translation U^t = λ. U is real, so λ=±1 and U^{2t}=1.
Hence "never exact" holds for all t (not only to 100000) for N=3..40, N≠4,8, by P1; for all N by Konno-Shimizu-Takei,
"Periodicity for the Hadamard walk on cycles", Interdiscip. Inform. Sci. 23 (2017), arXiv:1504.06396 (abstract seen via search; paper not opened). Not cited in the repository.

## Consequence for G10 (no file is wrong; no patch)
body.tex line 759: "the coherent part returns above 0.99" at lengths up to 4000 on rings of 3,4,5,6,8 sites is true but depends on the horizon and the selection: rings 9, 11, 12 fail it at 4000.

## Runners-up (not pursued)
- Cor. 5.29(1) generalizes: with at most k<d parallel arcs into x0, R_t <= 1 - a(1-k/d) (same proof, P^t entry <= max entry of P); not checked by program.
- Queue item for Cor. 5.28 with C_0≠C: on ζ[[1,1],[1,-1]] (8th roots) length-2 events with (|S|,||v||²) = (1,1),(2,4),(2,0) already force (a,c) in {(0,0),(1,0),(0,1)}; hand computation only.
