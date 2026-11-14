#!/usr/bin/env python3
"""CHAOS harness, test 1: the edition verifier.  Works on scratch copies only.

Each mutant: fresh `cp -r` of the repository's edition/ into
  <work>/MUTANT_<id>_edition/ , one planted change, then `python3 verify_baseline.py`
run with cwd = the copy (the verifier takes ROOT from dirname(abspath(__file__)),
so it verifies the copy; the harness asserts that the script it runs lives in the copy).
The prediction (which check ought to catch it) is written to PREDICTIONS_edition.md
BEFORE any mutant is run.  Seed 20261113 for every random choice of site.
The planted file is also kept as planted/MUTANT_<id>__<basename>.
Nothing is deleted: a 'deleted' file is moved to planted/.
"""
import csv, hashlib, io, json, os, random, re, shutil, subprocess, sys

SEED = 20261113
REPO = "/home/user/From-Prephysical-Hypotheses-to-Physical-Models"
W = os.path.dirname(os.path.abspath(__file__))
PLANTED = os.path.join(W, "planted")
os.makedirs(PLANTED, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()


def wr(p, b):
    with open(p, "wb") as f:
        f.write(b)


def remanifest(root, rel):
    """Model an error made BEFORE the edition tool computes the manifest:
    the manifest entry of `rel` is brought into agreement with the mutated file."""
    mp = os.path.join(root, "MANIFEST.json")
    m = json.load(open(mp))
    b = rd(os.path.join(root, rel))
    m["files"][rel] = {"sha256": sha(b), "size": len(b)}
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False)


def flip_digit(b, rng, lo=0, hi=None):
    pos = [i for i in range(lo, hi if hi is not None else len(b)) if 48 <= b[i] <= 57]
    i = rng.choice(pos)
    new = 48 + (b[i] - 48 + 1) % 10
    return b[:i] + bytes([new]) + b[i + 1:], i, chr(b[i]), chr(new)


# ---- mutation functions: each returns (rel_path_of_planted_file, one_line_change, made_false) ----

def pick_result_json(root, rng):
    c = sorted(os.path.relpath(os.path.join(dp, f), root) for dp, _, fs in os.walk(os.path.join(root, "COMPUTATION"))
               for f in fs if f.endswith(".json") and "result" in f.lower())
    return rng.choice(c)


def m_json_digit(root, rng, reman=False):
    rel = pick_result_json(root, rng)
    p = os.path.join(root, rel); b = rd(p)
    nb, i, o, n = flip_digit(b, rng)
    wr(p, nb)
    if reman: remanifest(root, rel)
    ctx = nb[max(0, i - 30):i + 30].decode("utf8", "replace").replace("\n", " ")
    return rel, f"digit at byte {i}: {o} -> {n} (context: ...{ctx}...)" + ("; manifest entry re-digested" if reman else ""), "yes (a recorded result value)"


def m_tex_word(root, rng):
    c = sorted(os.path.relpath(os.path.join(dp, f), root) for dp, _, fs in os.walk(os.path.join(root, "PAPERS")) for f in fs if f.endswith(".tex"))
    rng.shuffle(c)
    for rel in c:
        p = os.path.join(root, rel); b = rd(p)
        occ = [m.start() for m in re.finditer(rb" not ", b)]
        if occ:
            i = rng.choice(occ)
            wr(p, b[:i] + b" now " + b[i + 5:])
            ctx = b[max(0, i - 40):i + 45].decode("utf8", "replace").replace("\n", " ")
            return rel, f"word ' not ' -> ' now ' at byte {i} (context: ...{ctx}...)", "yes (a negation removed from a sentence)"
    raise SystemExit("no site")


def m_pdf_byte(root, rng):
    c = sorted(os.path.relpath(os.path.join(dp, f), root) for dp, _, fs in os.walk(os.path.join(root, "PAPERS")) for f in fs if f.endswith(".pdf"))
    rel = rng.choice(c); p = os.path.join(root, rel); b = rd(p)
    i = rng.randrange(len(b))
    wr(p, b[:i] + bytes([b[i] ^ 1]) + b[i + 1:])
    return rel, f"byte {i} of {len(b)}: 0x{b[i]:02x} -> 0x{b[i]^1:02x}", "record altered (PDF bytes)"


def all_files(root):
    return sorted(os.path.relpath(os.path.join(dp, f), root) for dp, _, fs in os.walk(root) for f in fs)


def m_delete(root, rng):
    rel = rng.choice([f for f in all_files(root) if f not in ("MANIFEST.json", "verify_baseline.py")])
    shutil.move(os.path.join(root, rel), os.path.join(PLANTED, "MUTANT_E04__REMOVED__" + os.path.basename(rel)))
    return rel, "file removed from the copy (moved to planted/, not deleted)", "record altered (a file is absent)"


def m_stray(root, rng):
    rel = "COMPUTATION/MUTANT_E05_stray_result.json"
    wr(os.path.join(root, rel), b'{"MUTANT": "E05 stray file", "all_pass": true}\n')
    return rel, "stray file added", "record altered (an unlisted result file)"


def m_stray_pycache(root, rng):
    rel = "PAPERS/__pycache__/MUTANT_E06_stray_paper.tex"
    os.makedirs(os.path.join(root, "PAPERS/__pycache__"), exist_ok=True)
    wr(os.path.join(root, rel), b"% MUTANT E06 stray file in a directory named __pycache__\n\\begin{theorem} 1 = 2. \\end{theorem}\n")
    return rel, "stray .tex added under a directory named __pycache__", "record altered (an unlisted file inside the edition)"


REG = "PROGRAM/registers/THEOREM_REGISTRY.csv"


def reg_rows(root):
    return list(csv.DictReader(open(os.path.join(root, REG), newline="")))


def m_reg_number(root, rng):
    rows = reg_rows(root); r = rng.choice([r for r in rows if r["number"]])
    p = os.path.join(root, REG); b = rd(p)
    old = f'{r["id"]},{r["paper"]},{r["part"]},'.encode()
    i = b.index(old); j = b.index(("," + r["number"] + ",").encode(), i)
    num = r["number"]; new = num[:-1] + str((int(num[-1]) + 1) % 10)
    wr(p, b[:j] + ("," + new + ",").encode() + b[j + len(num) + 2:])
    return REG, f"row {r['id']}: statement number {num} -> {new}", "yes (the registry points to another statement number)"


def m_reg_status(root, rng, reman=False):
    rows = reg_rows(root); r = rng.choice([r for r in rows if r["status"] == "PROOF_NOT_ADJACENT"])
    p = os.path.join(root, REG); lines = rd(p).split(b"\n")
    k = [i for i, l in enumerate(lines) if l.startswith((r["id"] + ",").encode())][0]
    assert b"PROOF_NOT_ADJACENT" in lines[k]
    lines[k] = lines[k].replace(b"PROOF_NOT_ADJACENT", b"PROOF_IN_MANUSCRIPT")
    wr(p, b"\n".join(lines))
    if reman: remanifest(root, REG)
    return REG, f"row {r['id']}: status PROOF_NOT_ADJACENT -> PROOF_IN_MANUSCRIPT" + ("; manifest entry re-digested" if reman else ""), "yes (a proof is declared present in the manuscript)"


def m_reg_delete_row(root, rng):
    rows = reg_rows(root); r = rng.choice([r for r in rows if r["kind"] != "Note"])
    p = os.path.join(root, REG); lines = rd(p).split(b"\n")
    k = [i for i, l in enumerate(lines) if l.startswith((r["id"] + ",").encode())][0]
    wr(os.path.join(PLANTED, "MUTANT_E16__REMOVED_ROW.txt"), lines[k] + b"\n")
    del lines[k]
    wr(p, b"\n".join(lines)); remanifest(root, REG)
    return REG, f"row {r['id']} ({r['kind']} {r['number']}) removed; 412 rows remain; manifest entry re-digested", "yes (README says 413 rows; PAPER_INDEX statements count for the paper is now one too many)"


def m_manifest_digest(root, rng):
    mp = os.path.join(root, "MANIFEST.json"); m = json.load(open(mp))
    rel = rng.choice(sorted(m["files"])); old = m["files"][rel]["sha256"]
    i = rng.randrange(64); c = "0123456789abcdef"; new = old[:i] + c[(c.index(old[i]) + 1) % 16] + old[i + 1:]
    b = rd(mp); assert b.count(old.encode()) >= 1
    wr(mp, b.replace(old.encode(), new.encode(), 1))
    return "MANIFEST.json", f"sha256 of {rel}: hex digit {i} {old[i]} -> {new[i]}", "record altered (a digest in the manifest)"


def m_manifest_pred(root, rng):
    mp = os.path.join(root, "MANIFEST.json"); m = json.load(open(mp))
    old = m["predecessor_manifest_sha256"]; i = rng.randrange(64); c = "0123456789abcdef"
    new = old[:i] + c[(c.index(old[i]) + 1) % 16] + old[i + 1:]
    b = rd(mp); assert b.count(old.encode()) == 1
    wr(mp, b.replace(old.encode(), new.encode()))
    return "MANIFEST.json", f"predecessor_manifest_sha256: hex digit {i} {old[i]} -> {new[i]}", "yes (the edition names a predecessor digest that is not its predecessor's)"


def m_manifest_size(root, rng):
    mp = os.path.join(root, "MANIFEST.json"); m = json.load(open(mp))
    rel = rng.choice(sorted(m["files"])); s = m["files"][rel]["size"]
    b = rd(mp); pat = (json.dumps(rel, ensure_ascii=False)).encode()
    i = b.index(pat); j = b.index(b'"size": ' + str(s).encode(), i)
    wr(mp, b[:j] + b'"size": ' + str(s + 1).encode() + b[j + len(b'"size": ') + len(str(s)):])
    return "MANIFEST.json", f"size of {rel}: {s} -> {s+1}", "yes (the manifest states a wrong size)"


REGCOPY = "REVIEW_RECORDS/Director_Z/Session_4/register/register.jsonl"


def m_register_line(root, rng, reman=False, last=False):
    p = os.path.join(root, REGCOPY); lines = rd(p).split(b"\n")
    n = len([l for l in lines if l])
    k = n - 1 if last else rng.randrange(n - 1)
    l = lines[k]; i = l.index(b'"ts":"') + 6
    nl, j, o, nn = flip_digit(l, rng, i, i + 19)
    lines[k] = nl; wr(p, b"\n".join(lines))
    if reman: remanifest(root, REGCOPY)
    return REGCOPY, f"line seq {k} ({json.loads(l)['kind']}): timestamp digit {o} -> {nn} ({l[i:i+20].decode()} -> {nl[i:i+20].decode()})" + ("; manifest entry re-digested" if reman else ""), "yes (a register record altered)"


def m_readme_count(root, rng, reman=False):
    p = os.path.join(root, "README.md"); b = rd(p)
    assert b.count(b"theorem registry (413 rows)") == 1
    wr(p, b.replace(b"theorem registry (413 rows)", b"theorem registry (431 rows)"))
    if reman: remanifest(root, "README.md")
    return "README.md", "'theorem registry (413 rows)' -> '(431 rows)'" + ("; manifest entry re-digested" if reman else ""), "yes (the registry has 413 rows)"


ADD = "REVIEW_RECORDS/Director_Z/Session_4/ADDENDUM_EDITION_Z23.md"


def m_addendum_count(root, rng):
    p = os.path.join(root, ADD); b = rd(p)
    assert b.count(b"32 labelled statements") == 1
    wr(p, b.replace(b"32 labelled statements", b"33 labelled statements")); remanifest(root, ADD)
    return ADD, "'Paper G10 revised (47 pages, 32 labelled statements' -> '33 labelled statements'; manifest entry re-digested", "yes (G10 has 32 registry rows)"


def m_index_pages(root, rng):
    rel = "PROGRAM/registers/PAPER_INDEX.csv"; p = os.path.join(root, rel); lines = rd(p).split(b"\n")
    k = [i for i, l in enumerate(lines) if l.startswith(b"G10,")][0]
    assert lines[k].count(b".pdf,47,1,32,") == 1
    lines[k] = lines[k].replace(b".pdf,47,1,32,", b".pdf,48,1,32,"); wr(p, b"\n".join(lines)); remanifest(root, rel)
    return rel, "row G10: pages 47 -> 48; manifest entry re-digested", "yes (the assembled G10 PDF has 47 pages)"


def m_swap(root, rng):
    fs = [f for f in all_files(root) if f.startswith("COMPUTATION/") and f.endswith(".json")]
    while True:
        a, b = rng.sample(fs, 2)
        if rd(os.path.join(root, a)) != rd(os.path.join(root, b)): break
    t = os.path.join(root, a + ".swaptmp")
    os.rename(os.path.join(root, a), t); os.rename(os.path.join(root, b), os.path.join(root, a)); os.rename(t, os.path.join(root, b))
    shutil.copy(os.path.join(root, b), os.path.join(PLANTED, "MUTANT_E12__second_of_pair__" + os.path.basename(b)))
    return a, f"file names swapped: {a} <-> {b}", "yes (each name now carries the other's content)"


def m_verifier_itself(root, rng):
    p = os.path.join(root, "verify_baseline.py"); b = rd(p)
    assert b.count(b"if bad:\n") == 1
    wr(p, b.replace(b"if bad:\n", b"if bad and False:  # MUTANT E22\n"))
    # and a second planted error for it to miss: a digit in the README count
    q = os.path.join(root, "README.md"); wr(q, rd(q).replace(b"theorem registry (413 rows)", b"theorem registry (431 rows)"))
    return "verify_baseline.py", "'if bad:' -> 'if bad and False:' in the verifier, together with README '(413 rows)' -> '(431 rows)' (no re-digest)", "yes (the check is disabled and a count is wrong)"


MUTANTS = [
 # id, title, function, kwargs, check that ought to catch it, prediction before the run
 ("E01", "changed digit in a result JSON under COMPUTATION", m_json_digit, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E02", "changed word in a paper's .tex", m_tex_word, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E03", "one byte replaced in a paper PDF", m_pdf_byte, {}, "verify_baseline.py: manifest digest (and crosswalk digest if it is a part)", "CAUGHT (digest)"),
 ("E04", "deleted file", m_delete, {}, "verify_baseline.py: missing file", "CAUGHT (missing)"),
 ("E05", "added stray file", m_stray, {}, "verify_baseline.py: unlisted file", "CAUGHT (unlisted)"),
 ("E06", "added stray file under a directory named __pycache__", m_stray_pycache, {}, "verify_baseline.py: unlisted file", "SURVIVES: the unlisted test skips every path containing '__pycache__'"),
 ("E07", "registry CSV: a statement number changed", m_reg_number, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E08", "registry CSV: a status word changed", m_reg_status, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E09", "a digest changed in the manifest", m_manifest_digest, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E10", "a line changed in the register copy inside the edition", m_register_line, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E11", "README count '413 rows' changed", m_readme_count, {}, "verify_baseline.py: manifest digest", "CAUGHT (digest)"),
 ("E12", "a pair of file names swapped", m_swap, {}, "verify_baseline.py: manifest digest of both", "CAUGHT (digest, two files)"),
 # errors made BEFORE the manifest is computed (the realistic case for a director's slip): the manifest agrees with the mutated file
 ("E13", "result-JSON digit, manifest consistent", m_json_digit, {"reman": True}, "rerun of the program and byte comparison (not the verifier)", "SURVIVES the verifier; only a rerun catches it"),
 ("E14", "README count, manifest consistent", m_readme_count, {"reman": True}, "nothing mechanical ties the README sentence to the registry; a reviewer of the summary", "SURVIVES the verifier (it prints 413 but does not compare)"),
 ("E15", "registry status word, manifest consistent", m_reg_status, {"reman": True}, "a reviewer comparing the registry row with the paper", "SURVIVES the verifier"),
 ("E16", "registry row removed, manifest consistent", m_reg_delete_row, {}, "verify_baseline.py ought to compare PAPER_INDEX.statements and the README count with the registry", "SURVIVES the verifier"),
 ("E17", "addendum '32 labelled statements' -> 33, manifest consistent", m_addendum_count, {}, "summary-sentence review (a reviewer)", "SURVIVES the verifier"),
 ("E18", "manifest: predecessor digest changed", m_manifest_pred, {}, "verify_baseline.py ought to, but has no predecessor to compare with; git history of MANIFEST.json", "SURVIVES the verifier"),
 ("E19", "manifest: a file size changed", m_manifest_size, {}, "verify_baseline.py ought to compare sizes", "SURVIVES: the verifier never reads 'size'"),
 ("E20", "register copy line (interior), manifest consistent", m_register_line, {"reman": True}, "the register's own prev-hash chain; comparison with .pcp/register.jsonl", "SURVIVES the verifier; a chain check would catch it"),
 ("E21", "PAPER_INDEX pages of G10 47 -> 48, manifest consistent", m_index_pages, {}, "verify_baseline.py ought to compare with the PDF page count (it already opens each PDF)", "SURVIVES the verifier"),
 ("E22", "the verifier itself weakened, plus a wrong README count", m_verifier_itself, {}, "nothing inside the edition can; git diff of verify_baseline.py or a trusted copy of the verifier", "SURVIVES"),
 ("E23", "register copy LAST line changed, manifest consistent", m_register_line, {"reman": True, "last": True}, "comparison with the live .pcp/register.jsonl digest", "SURVIVES the verifier and a prev-hash chain check (no successor line)"),
]


def chain_check(root):
    bad = []
    for dp, _, fs in os.walk(os.path.join(root, "REVIEW_RECORDS")):
        for f in fs:
            if f == "register.jsonl":
                r = [l for l in rd(os.path.join(dp, f)).split(b"\n") if l]
                for i in range(len(r) - 1):
                    if json.loads(r[i + 1])["prev"] != sha(r[i]): bad.append((os.path.relpath(os.path.join(dp, f), root), i))
    return bad


def main():
    only = set(sys.argv[1:])
    with open(os.path.join(W, "PREDICTIONS_edition.md"), "w") as f:
        f.write("# Predictions written before any edition mutant was run (seed 20261113)\n\n| id | mutant | check that ought to catch it | prediction |\n|---|---|---|---|\n")
        for i, t, _, _, c, pr in MUTANTS: f.write(f"| {i} | {t} | {c} | {pr} |\n")
    out = []
    for i, title, fn, kw, check, pred in MUTANTS:
        if only and i not in only: continue
        dst = os.path.join(W, f"MUTANT_{i}_edition")
        if os.path.exists(dst): raise SystemExit(f"{dst} exists; refusing to overwrite")
        subprocess.run(["cp", "-r", os.path.join(REPO, "edition"), dst], check=True)
        orig = {rel: sha(rd(os.path.join(dst, rel))) for rel in ("MANIFEST.json", "README.md", "verify_baseline.py", REG, REGCOPY, ADD, "PROGRAM/registers/PAPER_INDEX.csv")}
        rng = random.Random(f"{SEED}-{i[:3] if i not in ('E13','E15','E14','E20') else {'E13':'E01','E15':'E08','E14':'E11','E20':'E10'}[i]}")
        before = None
        rel, change, made_false = fn(dst, rng, **kw)
        src = os.path.join(REPO, "edition", rel)
        odig = sha(rd(src)) if os.path.exists(src) else "(no original: added file)"
        mp = os.path.join(dst, rel)
        if os.path.exists(mp): shutil.copy(mp, os.path.join(PLANTED, f"MUTANT_{i}__" + os.path.basename(rel)))
        script = os.path.join(dst, "verify_baseline.py")
        assert os.path.dirname(os.path.abspath(script)) == dst and not dst.startswith(REPO)
        r = subprocess.run([sys.executable, "verify_baseline.py"], cwd=dst, capture_output=True, text=True)
        o = (r.stdout + r.stderr).strip().split("\n")
        rec = dict(id=i, title=title, file=rel, original_sha256=odig, change=change, made_false=made_false, check=check, prediction=pred,
                   verifier_exit=r.returncode, verifier_output=o[:6], chain_check_failures=len(chain_check(dst)))
        out.append(rec); print(json.dumps(rec, ensure_ascii=False)); sys.stdout.flush()
    rp = os.path.join(W, "edition_mutants_result.json")
    if os.path.exists(rp) and not only: raise SystemExit("result file exists; refusing to overwrite")
    json.dump(out, open(rp if not only else os.path.join(W, "edition_mutants_result_partial.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
