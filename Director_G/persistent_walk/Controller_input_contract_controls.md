# Input-width controls for the five-site stopping-time sampler

**Research owner:** Kirtus Justus. **Check and draft:** Session A (ChatGPT/OpenAI), 15 November 2026. **Status:** source-bound conditional control, not a physical experiment or independent referee report.

## Question and inspected source

Can a controller produce a well-formed per-launch stopping-time record while its random-input callback violates the independent fair-bit contract assumed by the five-site return test?

- **Research revision:** `34fa3fea5c8fc8b95ed690be370d3eb16ed9dde2`, merged PR #292.
- **Source:** `Director_G/persistent_walk/check_prelaunch_time_sampling.py`, Git blob `e3c60752af6c8a3b97daa6780f952e5c90096be5`, checked by `git hash-object` on a local source copy.
- **Related proof:** `Real_readout_return_test.md`, which requires fresh independent settings and preparations and treats all losses as outcomes. Its 432-launch decision is a calculated guarantee under those premises, not a measured instrument result.

At `N=250000`, `draw_setting` requests `2*18+32=68` bits, parsing 18 bits each for candidate coordinates `J,K` and 32 bits for the acceptance word. A callback that returns 64 uniformly sampled bits *instead* leaves `J,K` unchanged in bit layout but gives the acceptance word only 28 bits. The source function does not attest that the callback honored the request.

## Exact positive and adverse controls

At candidate `J=28, K=0`, the source's 112-bit fixed-point recurrence and a separate 70-/100-digit `decimal` recurrence agree that the positive signed acceptance threshold is `h[28]=95786191`.

Conditional on that **fixed proposed candidate**, both input sources use `accept` iff the acceptance word is less than `h[28]`. Their exact conditional probabilities are:

| Callback premise | Acceptance-word range | Conditional acceptance |
| --- | ---: | ---: |
| Correct 68 independent uniform bits | `0..2^32-1` | `95786191/4294967296` ≈ **0.022301960504** |
| Broken callback supplying 64 independent uniform bits | `0..2^28-1` | `95786191/268435456` ≈ **0.356831368059** |

The second conditional probability is exactly sixteen times the first. This does **not** compute the full accepted-time distribution, and is not an empirical fault rate. Both callbacks can return an accepted candidate with the identical output `(tick=56, click_is_success=True)`. Additional controls confirm rejection at the exact threshold and rejection of an invalid coordinate before accepting a valid candidate.

The 64-bit case is a deliberate **out-of-contract negative control**. It is not a counterexample to the mathematical PR #292 guarantee, whose fair-bit assumptions exclude it. It demonstrates why a correct assigned-tick record alone cannot certify the acquisition law.

## Reproduction and receipts

Run from `Director_G/persistent_walk/` in a checkout containing the named source and the accompanying `check_controller_input_contract.py`:

```sh
python -I -B check_controller_input_contract.py
python -I -B -O check_controller_input_contract.py
```

On a local copy whose original source Git blob matched the repository, both commands exited 0 and produced the five `PASS` lines and one `LIMIT` line shown by the checker. SHA-256 of the new checker: `25991adc2714c3797fd409d47b1f127ddac9ec222b2976bf7836396c2fbd1acc`.

The first test implementation failed under `-I` because ordinary sibling imports are unavailable in Python isolated mode. It was corrected to use `runpy.run_path` on the named sibling file; both ordinary and optimized isolated runs then passed. That correction is a checker implementation detail, not a physical observation.

## What remains open

Whether any experimental controller uses the wrong input width, has nonuniform or dependent draws, changes a preparation when a time is selected, or executes the requested duration physically remains **unmeasured**. Establishing an actual acquisition guarantee requires evidence from the physical controller and its independent input source, including raw candidate and rejected-draw records where available. Finite sample tests alone do not establish universal independence.

No ontology is selected; Stage 1 Initial External Grounding and all 13 physical identification gates remain open. This working supplement changes no issued edition, scientific register, repository release, or PCP OS component.
