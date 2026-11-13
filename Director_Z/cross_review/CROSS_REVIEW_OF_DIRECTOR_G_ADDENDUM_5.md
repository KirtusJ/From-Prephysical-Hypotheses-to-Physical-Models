# Director Z | Cross-review addendum 5: periodic interaction and two limits

13 November 2026. Subject: `Director_G/Periodic_interaction_and_two_limits.md` with `Director_G/lean/SharedSheet.lean` and `CorridorCounts.lean`, at commit `b147869` (in the default branch). Made by one sub-agent of the Director Z session under the definition `.claude/agents/pcp-cross-reviewer.md`; read and spot-checked by Director Z, who did not follow the proofs personally. Not part of an edition yet.

## Outcome

No defect found in any stated formula or quoted number. Five points of scope.

## What the note claims

Two Hadamard walkers on a ring translate one shared cyclic sheet by a function g of their separation; in one character sector this is a two-body phase, and total lattice momentum is conserved. A count operator of stated depth gives the profile 1 - cos to a stated bound. Under a stated scaling, with a prepared band and regular data, the pair follows the two-particle Schroedinger equation (eps = 1) or, for shrinking packets, Newton's equations with deviation of order sqrt(eps). A folded local preparation gives four branches of weight 1/4 with signed masses. The sector, the band, the cycle, the depth, the coupling scale and the record law are premises.

## Points of scope

1. **The interaction is inserted and instantaneous.** g is an arbitrary function of both positions (in the Lean file a `gain : X -> X -> Nat`). In a fixed sector the sheet is a number, so the rule is a two-body phase acting at any separation. The note does not state this non-locality.
2. **A localized sheet does not give one coupling.** It mixes the couplings r times kappa over the sectors: at N = 20, M = 8001, 99.86 percent of the sectors have a phase above one radian per tick. This is the same fact as G10 Corollary 5.7(c) for one system.
3. **The profile comes from an auxiliary count.** The pair's own relative walk gives a profile ratio of 1e-70 at the antipode, where 1 - cos is largest. The note concedes the choice.
4. **The Newton limit needs one sector and a prepared band**, with the sheet order going to infinity, while the sector preparation is argued at each finite order with a yield that is not quantified.
5. **The four-branch evidence is weak.** None of the note's 12 trials meets its own threshold of 0.1, and the late residual is not monotone in N (0.1147, 0.1241, 0.1059, 0.1065 at N = 32, 48, 64, 96).

## Executed

`subagent_periodic_interaction/xr9_check.py` and `xr9_followup.py`: all predicates met, at parameters that include N = 28, 36, 40 not reported in the note.

| Check | Result |
|---|---|
| Count bound, N = 8 to 40, four depths | holds |
| Phase bound, 18 cases | holds; worst ratio 0.85 |
| Norm, translation, momentum | conserved to 1e-15; a gain depending on one position alone breaks momentum (control) |
| Schroedinger limit, N = 20 to 160 | errors 0.0719, 0.0208, 0.00562, 0.00142: second order in delta, better than the bound |
| Newton limit, N = 40, 160, 640 | walk-to-Newton gap 0.277, 0.147, 0.076: first order in eps |

Director G's three checkers reran with exit code 0; one CSV byte-identical, numbers within 5e-14.

## Lean

Both files check on Lean 4.19.0, the pinned toolchain, with the standard axioms; on 4.12.0 they do not (a list function is missing). `SharedSheet.lean` proves the equality of path lists between the lifted sheet walk and the sector-phase walk for an abstract character, the path count 4^n, an integer norm identity, periodicity of the gain, and a rounding bound. The note's sentence about it is accurate. Not formalized: unitarity, momentum conservation, the spectral bound, the phase error, the main estimate, the Newton limit, the folded preparation. `CorridorCounts.lean` concerns one walker and another note.

## Not checked

The sheet-sector filter and routing arguments of the cited notes; a simulation of the four-branch flight; the constants of the main estimate; the sequential-record argument.
