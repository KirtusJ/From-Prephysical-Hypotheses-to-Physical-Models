# Tracking note: byte efficiency and a machine mode for PCP

13 November 2026, Director Z. A consideration asked for by the principal, for tracking; not a priority and not a finding.

## Measured in this session

| Quantity | Value |
|---|---|
| Session register | 314 events, 189 400 bytes, about 600 bytes per event |
| Share that is envelope (actor, digests, sequence) | 32 percent |
| Share that is free prose inside event bodies | 16 percent |
| Same file compressed with gzip | 45 332 bytes, a factor 4.2 |
| A task sent to a sub-agent | 300 to 700 words of prose |
| A report back | 300 to 700 words of prose, of which the decision-relevant part is a verdict per step and a handful of numbers |

## Where bytes are wasted between machines

- Restating context: every task repeats definitions, rules and paths that both sides could address by digest.
- Verdicts as sentences: "no defect found in step 3" is one enum and one address.
- Numbers inside prose, which the receiver must parse back out.
- Hashes as 64 hex characters in JSON (32 bytes binary).

## What a machine mode could be

1. **Addresses in place of text.** PCP 1.0 already ships every provision as an address with a digest (`pcp.machine.json`) and a schema for register events. The same idea applied to work items: a claim, a statement of a paper, a file and a predicate each get an address (digest plus locator). A task is then a tuple (agent kind, target address, criterion address, budget), a report a list of (step address, verdict enum, evidence address).
2. **Typed reports.** The four agent definitions in this repository already ask for DEFECT / GAP / NONE FOUND per step. Making that a schema would let a director merge reports without reading prose, and would make the outlier scan a query.
3. **Binary framing** (CBOR or similar, binary digests, a shared dictionary). On the register this would save perhaps a factor three to five, the same order as gzip gives today for nothing. Low value on its own.

## Where human language should stay

- The claim, the hypotheses and the proof. Every defect found in this session was found by reading mathematics in sentences, and three of them were in wording. A compressed claim cannot be challenged by a reader who was not party to the compression.
- The parts a person is accountable for: adoption, objections left open, what a finding does not show.
- Anything crossing model families. A private code between two models of one family removes the one check that a second family provides.

## Risks specific to machine-to-machine speech

- Auditability: a register is evidence only if a person and a different program can read it. A byte mode needs a canonical, lossless rendering back to text, and the digest should be of the canonical form.
- Hidden channel: agreement reached in a representation no reviewer reads is not review. Under ACR terms it would raise exposure without anyone noticing.
- Drift: enums and addresses freeze the method's categories; a new kind of defect has nowhere to go unless free text remains available beside them.

## Assessment

- Worth having: addressed, typed task and report records between director and workers (items 1 and 2). They cut cost in the most frequent traffic, make propagation mechanical, and stay readable.
- Worth little alone: binary framing of the register.
- Not worth having: machine-only speech for claims and proofs.
- PCP OS is the right place for it, because it already owns the event schema and the guards; the missing piece observed here is that it cannot see or launch workers, so worker traffic is outside the record whatever its encoding.
