#!/usr/bin/env python3
"""Outlier scan of JSON result files. Rules fixed before the first run.

Input: folders given on the command line; every *.json found recursively is read (read-only).
Output: outlier_scan_results.json beside this program; the program refuses to overwrite it.

R1  Any float NaN or +/-infinity, or a string equal (case-insensitive, stripped) to
    nan, inf, -inf, +inf, infinity, -infinity.
R2  Failed predicate. A value is "under a predicate key" if its own key or any ancestor key
    contains pred, pass, check, status, verdict, holds, fail, or has the token ok or met
    (tokens = key split on non-alphanumerics). Flag when such a value is boolean false, or a
    string that matches fail / failed / not met / not_met / false / violated / refuted / no
    (whole string, case-insensitive, or starting with FAIL / NOT MET).
    Polarity exception: if the leaf key itself contains fail, violat or error, then false / 0 /
    empty is the good state; flag instead when it is true, a number > 0, or a non-empty list.
R3  Robust deviation. Numeric columns of length >= 8: (a) a list of numbers, (b) one key across
    a list of records, (c) one index across a list of equal-length numeric rows. Flag any x with
    |x - median| / (1.4826 * MAD) > 10. The cut-off 10 is a conventional screening value, not a
    derived tolerance. Columns with MAD = 0 are skipped and counted.
R4  Residual-like keys (name contains resid, err, defect, dev, diff, max_abs, tol). Groups of
    >= 3 values: the same key across a list of records, a numeric list under such a key, or the
    residual-like scalar siblings in one record. Flag if max|x| > 1000 * median|x| (median > 0),
    or max|x| > 1e-6 while every other |x| < 1e-10.
R5  Self-contradiction. A record with a pass-like flag (key pass, passed, ok, met, holds, status,
    verdict, result) that is true / PASS / met, read mechanically against its own numbers:
    value-like (value, observed, measured, actual, got) vs bound-like (bound, threshold, tol,
    tolerance, limit, max): flag if |value| > bound (bound assumed to be an upper bound on the
    magnitude; this assumption is stated in the flag); value vs expected: flag if
    |value - expected| > tol when a tol-like field is present, else if they differ by more than
    1e-9 * max(1, |expected|).
Booleans are never treated as numbers.
"""
import json, math, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outlier_scan_results.json")
CUT = 10.0
PRED_SUB = ("pred", "pass", "check", "status", "verdict", "holds", "fail")
PRED_TOK = ("ok", "met")
NEG_LEAF = ("fail", "violat", "error")
FAIL_RE = re.compile(r"^\s*(fail(ed|ure)?\b.*|not[ _]met\b.*|false|violated|refuted|no)\s*$", re.I)
RESID = ("resid", "err", "defect", "dev", "diff", "max_abs", "tol")
PASSKEYS = ("pass", "passed", "ok", "met", "holds", "status", "verdict", "result")
VALKEYS = ("value", "observed", "measured", "actual", "got")
BNDKEYS = ("bound", "threshold", "tol", "tolerance", "limit", "max")
flags = []; stats = {"mad0_skipped": 0, "columns_tested": 0, "resid_groups_tested": 0, "r5_records_tested": 0}

def isnum(x): return isinstance(x, (int, float)) and not isinstance(x, bool)
def predkey(k):
    k = str(k).lower(); toks = re.split(r"[^a-z0-9]+", k)
    return any(s in k for s in PRED_SUB) or any(t in toks for t in PRED_TOK)
def residkey(k): return any(s in str(k).lower() for s in RESID)
def add(rule, f, path, **kw): flags.append(dict(rule=rule, file=f, path=path, **kw))

def r3(f, path, col):
    fin = [x for x in col if math.isfinite(x)]
    if len(fin) < 8: return
    a = np.array(fin, float); med = np.median(a); mad = np.median(np.abs(a - med))
    if mad == 0: stats["mad0_skipped"] += 1; return
    stats["columns_tested"] += 1
    z = np.abs(a - med) / (1.4826 * mad)
    for i in np.where(z > CUT)[0]:
        add("R3", f, path, value=float(a[i]), median=float(med), mad=float(mad), robust_dev=float(z[i]), n=len(fin))

def r4(f, path, col):
    a = np.abs(np.array([x for x in col if math.isfinite(x)], float))
    if len(a) < 3: return
    stats["resid_groups_tested"] += 1
    mx = a.max(); med = np.median(a); rest = np.delete(a, a.argmax())
    if med > 0 and mx > 1000 * med:
        add("R4", f, path, max_abs=float(mx), median_abs=float(med), kind="max>1000*median", n=len(a))
    elif mx > 1e-6 and (rest < 1e-10).all():
        add("R4", f, path, max_abs=float(mx), median_abs=float(med), kind="max>1e-6, siblings<1e-10", n=len(a))

def r5(f, path, d):
    low = {str(k).lower(): v for k, v in d.items()}
    flag = None
    for k in PASSKEYS:
        v = low.get(k)
        if v is True or (isinstance(v, str) and re.match(r"^\s*(pass(ed)?|met|ok|true|holds)\s*$", v, re.I)): flag = k
    if flag is None: return
    val = next((low[k] for k in VALKEYS if isnum(low.get(k))), None)
    if val is None: return
    stats["r5_records_tested"] += 1
    bk = next((k for k in BNDKEYS if isnum(low.get(k))), None)
    if isnum(low.get("expected")):
        e = low["expected"]; t = low[bk] if bk else 1e-9 * max(1, abs(e))
        if abs(val - e) > t: add("R5", f, path, value=val, expected=e, tol=t, flag_key=flag)
    elif bk and abs(val) > low[bk]:
        add("R5", f, path, value=val, bound=low[bk], bound_key=bk, flag_key=flag, assumption="bound read as upper bound on |value|")

def walk(f, x, path, under, leaf):
    if isinstance(x, float) and not math.isfinite(x): add("R1", f, path, value=repr(x))
    elif isinstance(x, str) and x.strip().lower() in ("nan", "inf", "-inf", "+inf", "infinity", "-infinity"): add("R1", f, path, value=x)
    if under:
        neg = leaf is not None and any(s in str(leaf).lower() for s in NEG_LEAF)
        if neg:
            if x is True or (isnum(x) and x > 0) or (isinstance(x, list) and len(x) > 0):
                add("R2", f, path, value=x if not isinstance(x, list) else "list of %d" % len(x), polarity="failure-key nonzero")
        elif x is False or (isinstance(x, str) and FAIL_RE.match(x)):
            add("R2", f, path, value=x)
    if isinstance(x, dict):
        r5(f, path, x)
        sib = [(k, v) for k, v in x.items() if residkey(k) and isnum(v)]
        if len(sib) >= 3: r4(f, path + "{resid siblings}", [v for _, v in sib])
        for k, v in x.items():
            walk(f, v, path + "/" + str(k), under or predkey(k), k)
    elif isinstance(x, list):
        if x and all(isnum(v) for v in x):
            r3(f, path, x)
            if leaf is not None and residkey(leaf): r4(f, path, x)
        if x and all(isinstance(v, dict) for v in x):
            keys = []
            for v in x:
                for k in v:
                    if k not in keys: keys.append(k)
            for k in keys:
                col = [v[k] for v in x if isnum(v.get(k))]
                if len(col) >= 8: r3(f, path + "[*]/" + str(k), col)
                if residkey(k) and len(col) >= 3: r4(f, path + "[*]/" + str(k), col)
        if len(x) >= 8 and all(isinstance(v, list) and v and all(isnum(u) for u in v) for v in x) and len({len(v) for v in x}) == 1:
            for j in range(len(x[0])): r3(f, path + "[*][%d]" % j, [v[j] for v in x])
        for i, v in enumerate(x): walk(f, v, path + "[%d]" % i, under, leaf if not isinstance(v, (dict, list)) else None)

def main():
    if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
    files = []; unread = []
    for root in sys.argv[1:]:
        for dp, dn, fn in os.walk(root):
            dn.sort()
            for n in sorted(fn):
                if n.lower().endswith(".json"): files.append(os.path.join(dp, n))
    for f in files:
        try:
            with open(f) as h: data = json.load(h)
        except Exception as e:
            unread.append({"file": f, "error": str(e)[:200]}); continue
        walk(f, data, "", False, None)
    counts = {r: sum(1 for x in flags if x["rule"] == r) for r in ("R1", "R2", "R3", "R4", "R5")}
    res = {"roots": sys.argv[1:], "files_found": len(files), "files_parsed": len(files) - len(unread), "unreadable": unread,
           "cutoff_R3": CUT, "cutoff_note": "10 is a conventional screening cut-off, not a derived tolerance",
           "stats": stats, "counts": counts, "flags": flags}
    with open(OUT, "x") as h: json.dump(res, h, indent=1, default=str)
    print(json.dumps({k: res[k] for k in ("files_found", "files_parsed", "unreadable", "stats", "counts")}, indent=1))
    R = sys.argv[1].rsplit("/", 1)[0] + "/"
    seen = {}
    for x in flags:
        key = (x["rule"], x["file"], re.sub(r"\[\d+\]", "[]", x["path"]))
        seen.setdefault(key, []).append(x)
    for (r, f, p), v in seen.items():
        x = v[0]; extra = {k: (float("%.4g" % w) if isinstance(w, float) else w) for k, w in x.items() if k not in ("rule", "file", "path")}
        print(r, f.replace(R, ""), p, "x%d" % len(v), extra)
main()
