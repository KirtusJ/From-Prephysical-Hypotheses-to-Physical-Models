"""Compare a pinned registration manifest with regular file blobs at one Git commit.

Usage: python check_registered_commit.py REPO COMMIT MANIFEST EXPECTED_MANIFEST_SHA256
Writes one deterministic JSON report on stdout; 0 = unchanged, 5 = discrepancies,
2 = invalid input or Git read failure. Pass a full hexadecimal commit object ID.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def git(repo, *args):
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(repo), *args],
        capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "Git read failed")
    return result.stdout


def unique_paths(pairs):
    table = {}
    for key, value in pairs:
        if key in table:
            raise ValueError(f"duplicate manifest key: {key!r}")
        table[key] = value
    return table


def compare(repo, commit, manifest, expected):
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit):
        raise ValueError("expected a full lowercase Git commit object ID")
    manifest_digest = hashlib.sha256(manifest).hexdigest()
    if manifest_digest != expected:
        raise ValueError("manifest SHA-256 differs from the supplied pin")
    declared = json.loads(manifest, object_pairs_hook=unique_paths)
    if not isinstance(declared, dict) or not declared:
        raise ValueError("expected a nonempty JSON object mapping each path to SHA-256")
    for path, digest in declared.items():
        path.encode("utf-8")
        if (any(part in ("", ".", "..") for part in path.split("/"))
                or "\\" in path or "\0" in path):
            raise ValueError(f"expected a normalized repository-relative Git path: {path!r}")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"invalid SHA-256 for {path!r}")

    # Reject shorthand object IDs, tags, trees, and substitution by refs/replace.
    resolved = git(repo, "rev-parse", "--verify", commit + "^{commit}").decode().strip()
    if resolved != commit:
        raise ValueError("expected the commit's own full object ID")
    entries = {}
    for entry in git(repo, "ls-tree", "-r", "-t", "-z", "--full-tree", commit).split(b"\0"):
        if entry:
            meta, name = entry.split(b"\t", 1)
            entries[name] = meta.split()
    rows = []
    for path, expected_digest in sorted(declared.items()):
        meta = entries.get(path.encode("utf-8"))
        row = {"path": path, "expected_sha256": expected_digest}
        if meta is None:
            row["status"] = "MISSING"
        else:
            mode, _, oid = (field.decode("ascii") for field in meta)
            row.update(mode=mode, object_id=oid)
            if mode not in ("100644", "100755"):
                row["status"] = "NOT_REGULAR"
            else:
                body = git(repo, "cat-file", "blob", oid)
                actual_digest = hashlib.sha256(body).hexdigest()
                row.update(sha256=actual_digest, bytes=len(body),
                           status="UNCHANGED" if actual_digest == expected_digest else "DIFFERS")
        rows.append(row)
    return {"commit": commit, "manifest_sha256": manifest_digest, "files": rows,
            "unchanged": all(r["status"] == "UNCHANGED" for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("commit")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("expected_manifest_sha256")
    args = parser.parse_args()
    try:
        report = compare(args.repo, args.commit, args.manifest.read_bytes(), args.expected_manifest_sha256)
    except (ValueError, OSError) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")
    sys.stdout.buffer.write((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("ascii"))
    return 0 if report["unchanged"] else 5


if __name__ == "__main__":
    raise SystemExit(main())
