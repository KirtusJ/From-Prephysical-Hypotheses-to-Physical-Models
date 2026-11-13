# PCP worker trials in the Director Z container

13 November 2026. Two model workers run through the reference host of the ACR 1.0 implementation packet (`TOOLS/acr_host.py`), each with the kernel card in context (SHA-256 `b1b1ca33d7b4ec9fce07ac9c9cdee3b3e0b634a814d1696eb6ab8de878edd117`, the card of Director G's trial) and its own PCP OS register, verified by `pcpos verify` with no guard problem.

| Worker | How it runs |
|---|---|
| Claude | the `claude` command-line program, headless, one turn, no tools |
| Qwen | `Qwen2.5-0.5B-Instruct` GGUF Q4_0 on the CPU through `llama-cpp-python` 0.3.36; file SHA-256 `7671c0c304e6ce5a7fc577bcb12aba01e2c155cc2efd29b2213c95b18edaf6ed` |

## Results

| Trial | Outcome |
|---|---|
| Bounded checks, each worker alone (17 x 23; inverse of 3 modulo 11; the cycle question) | Claude 3 of 3; Qwen 0 of 3 |
| Asynchronous: a supervisor runs Claude, Qwen and an exact enumerator at once | the two model workers overlapped for 9.18 s; all three outputs re-read after exit with equal digests; Claude correct, Qwen incorrect |
| Nested, tool offered | the Claude worker did not use the reviewer and answered correctly; the nested path was not exercised; kept |
| Nested, reviewer requested in the message | Claude called the Qwen reviewer through the host tool, received its reply with a receipt, quoted the receipt, gave the distances 3 and 4 and rejected both the claim and the reviewer's reply as unusable |

The question, the scoring rule and the controls were fixed in the program before the run. The cycle question is the one of Director G's trial (`Director_G/results/pcp_worker_trial.json`), so the two trials can be compared: there the parent was Codex, here Claude; the child model is the same.

## What this does and does not show

- A worker under the host can call a second worker under the host, and a supervisor can run workers of two model families at once and check their outputs after exit. Process completion and correctness have separate evidence, as in Director G's trial.
- The small local model is of no use as a reviewer of mathematics: 0 of 3 on bounded checks, including plain arithmetic.
- The registers record what the program was given and what came back (artifacts whose digests the server computed). They do not contain task events: PCP OS writes those only from host hooks, and the hooks did not fire for a headless worker in a test here. ACR adoption is the host object's flag, not a recorded adoption by a person.
- The parent's choice to delegate in the second trial followed a request in the message; in the first trial, left free, it did not delegate.

## Rerun

Needs the ACR implementation packet unpacked, an executable `pcpos`, the `claude` program, `pip install llama-cpp-python` and the model file. Paths are set at the top of the two programs.
