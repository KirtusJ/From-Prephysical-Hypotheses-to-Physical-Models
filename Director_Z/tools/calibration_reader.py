#!/usr/bin/env python3
"""calibration_reader: score a participant's reply against a pinned key, one property at a time.

Why: a reply can be right in value and wrong in the form asked for (or the reverse), and one FOR/AGAINST hides
which.  This reader scores each declared property of each item separately, mechanically, and binds the score to
the digests of the key and of the original reply.  What it cannot score mechanically it marks NEEDS_READER; it
never guesses.

Usage: python3 calibration_reader.py <key.json> <reply file> [<out.json>]
  The out file is opened with mode 'x' (never overwritten).  Exit 0 if every mechanical property is FOR,
  1 if any is AGAINST, 2 on usage or a malformed key.  NEEDS_READER does not change the exit code.

Key format (JSON):
 {"items": [{"id": "1", "section": "<regex that starts this item's part of the reply, optional>",
             "properties": [{"name": "value", "kind": "fraction", "equals": "3/16"},
                            {"name": "format", "kind": "fullmatch", "pattern": "\\s*\\d+/\\d+\\s*"},
                            {"name": "no overclaim", "kind": "absent", "pattern": "gate (is|was) passed"},
                            {"name": "names line 3", "kind": "present", "pattern": "Line 3"},
                            {"name": "argument sound", "kind": "reader", "criterion": "..."}]}]}
 Kinds: fraction (the LAST number or fraction a/b in the item's text equals the key's, exactly, as rationals);
        fullmatch (the whole item text matches); present / absent (regex search, case-insensitive);
        reader (not mechanical).
"""
import hashlib, json, re, sys
from fractions import Fraction

def last_number(text):
    m = re.findall(r"(?<![\w.])([+-]?\d+(?:\.\d+)?)(?:\s*/\s*(\d+))?", text)
    if not m: return None
    num, den = m[-1]
    return Fraction(num) / Fraction(den) if den else Fraction(num)

def sections(reply, items):
    marks = []
    for it in items:
        pat = it.get("section")
        m = re.search(pat, reply, re.I | re.M) if pat else None
        marks.append((m.start() if m else None, it["id"]))
    out = {}
    found = sorted((p, i) for p, i in marks if p is not None)
    for k, (p, i) in enumerate(found):
        out[i] = reply[p: found[k + 1][0] if k + 1 < len(found) else len(reply)]
    for p, i in marks:
        if p is None: out[i] = reply if not any(it.get("section") for it in items) else None
    return out

def score(prop, text):
    kind = prop["kind"]
    if kind == "reader": return "NEEDS_READER", prop.get("criterion", "")
    if text is None: return "AGAINST", "item's section not found in the reply"
    if kind == "fraction":
        got = last_number(text)
        return ("FOR" if got is not None and got == Fraction(prop["equals"]) else "AGAINST"), f"last number read: {got}"
    if kind == "fullmatch":
        return ("FOR" if re.fullmatch(prop["pattern"], text, re.S) else "AGAINST"), "whole item text against the pattern"
    if kind in ("present", "absent"):
        hit = re.search(prop["pattern"], text, re.I | re.S) is not None
        return ("FOR" if hit == (kind == "present") else "AGAINST"), ("pattern found" if hit else "pattern not found")
    raise ValueError("unknown kind " + kind)

def main(a):
    if len(a) not in (3, 4): print(__doc__); return 2
    key_bytes, reply_bytes = open(a[1], "rb").read(), open(a[2], "rb").read()
    try: key = json.loads(key_bytes); items = key["items"]
    except Exception as e: print("malformed key:", e); return 2
    reply = reply_bytes.decode("utf-8", "replace"); sec = sections(reply, items)
    rows, bad = [], 0
    for it in items:
        for p in it["properties"]:
            verdict, note = score(p, sec.get(it["id"]))
            bad += verdict == "AGAINST"
            rows.append(dict(item=it["id"], property=p["name"], kind=p["kind"], verdict=verdict, note=note))
    res = dict(reader="calibration_reader.py", key=a[1], key_sha256=hashlib.sha256(key_bytes).hexdigest(),
               reply=a[2], reply_sha256=hashlib.sha256(reply_bytes).hexdigest(), rows=rows,
               counts={v: sum(r["verdict"] == v for r in rows) for v in ("FOR", "AGAINST", "NEEDS_READER")})
    if len(a) == 4:
        with open(a[3], "x") as f: json.dump(res, f, indent=1)
    for r in rows: print(f'{r["item"]:>4} {r["property"]:<22} {r["verdict"]:<13} {r["note"]}')
    print(res["counts"], "key", res["key_sha256"][:16], "reply", res["reply_sha256"][:16])
    return 1 if bad else 0

if __name__ == "__main__": sys.exit(main(sys.argv))
