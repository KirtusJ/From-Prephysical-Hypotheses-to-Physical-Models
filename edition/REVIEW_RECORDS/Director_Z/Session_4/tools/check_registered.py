#!/usr/bin/env python3
"""check_registered: after a call file has been submitted, confirm that every file it registered as an
artifact still has the bytes it had when the call file was written.  Written after the addenda of editions
Z18 and Z22 were edited between registration and issue.
Usage: python3 check_registered.py <repository root> <digests.json>   where digests.json maps path -> sha256
(written by the same step that writes the call file).  Exit 0 if all match; 5 if any file differs or is missing."""
import hashlib, json, os, sys
root, dig = sys.argv[1], json.load(open(sys.argv[2])); bad = 0
for path, want in sorted(dig.items()):
    p = os.path.join(root, path)
    got = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else "MISSING"
    if got != want: bad += 1; print("DIFFERS", path, "registered", want[:16], "now", got[:16])
print(f"{len(dig) - bad} of {len(dig)} registered files unchanged"); sys.exit(5 if bad else 0)
