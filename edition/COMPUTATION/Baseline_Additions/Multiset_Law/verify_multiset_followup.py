"""Follow-up to verify_multiset.py (whose result file is kept unchanged).

Reason: the search of P3 found, for d=4 over C_6, six dephased blocks whose core already generates C_6 and for
which the non-faithful j=3 has B^(3)* B^(3) = 4 I; the first program stored as example only the first hit (a core
in a subgroup) and did not run P1 on such a block.

PREDICATES (fixed before the first run).
 F1  For each of the dephased blocks of degree 4 over C_6 found by search(4,6) whose entries generate C_6
     (hypothesis tested per block: is_block and generates; the number qualifying is reported):
     U = {1,3,5}, pred = 1 + 2 (counting, |sigma_1|^2, sigma_3^2), and nullity(B,N) == 3 for N = 2,3,4,
     with rational and two modular ranks agreeing.
 F2  The same blocks: j=3 is not coprime to 6 and B^(3) is a real Hadamard matrix (entries +-1, Gram 4 I).
Result file: verify_multiset_followup_result.json; refuses to overwrite.
"""
import json, os, sys
import verify_multiset as v
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_multiset_followup_result.json")
if os.path.exists(OUT): print("refusing to overwrite", OUT); sys.exit(1)
found, trunc = v.search(4, 6)
res = {"found": len(found), "truncated": trunc, "qualifying": 0, "blocks": [], "failures": []}
for B in found:
    isb = v.gram_ok(B, 6, 1, 5); gen = v.generates(B, 6)
    if not (isb and gen): continue
    res["qualifying"] += 1
    u = v.U(B, 6); lin, quad = v.pred(B, 6)
    rec = {"B": B, "U": u, "pred": [lin, quad], "N": []}
    f1 = (u == [1, 3, 5]) and (lin, quad) == (1, 2)
    for N in (2, 3, 4):
        n, nq, np_, neq = v.nullity(B, 6, N)
        ok = nq == 3 and all(x == 3 for x in np_)
        f1 = f1 and ok
        rec["N"].append({"N": N, "unknowns": n, "equations": neq, "nullity_Q": nq, "nullity_mod_p": np_})
    f2 = all((3*e) % 6 in (0, 3) for r in B for e in r) and v.gram_ok(B, 6, 3, 3)
    rec["F1"] = f1; rec["F2"] = f2
    if not f1: res["failures"].append({"predicate": "F1", "B": B})
    if not f2: res["failures"].append({"predicate": "F2", "B": B})
    res["blocks"].append(rec)
    print(B, u, lin, quad, [x["nullity_Q"] for x in rec["N"]], f1, f2, flush=True)
with open(OUT, "x") as f: json.dump(res, f, indent=1, sort_keys=True)
print("qualifying", res["qualifying"], "failures", res["failures"])
