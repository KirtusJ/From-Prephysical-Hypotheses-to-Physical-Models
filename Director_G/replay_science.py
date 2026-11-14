"""Replay a reviewed Python program from pinned Git blobs and compare its named output.

python replay_science.py REPOSITORY MANIFEST EXPECTED_MANIFEST_SHA256
Emits a JSON receipt. Exit 0 for a match, 5 for failed evidence, 2 for invalid setup.
The program runs with the operator's ordinary permissions. Use only trusted programs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

from check_registered_commit import compare, git, unique_paths


def sha(data):
    return hashlib.sha256(data).hexdigest()


def portable_path(name):
    if not isinstance(name, str) or not name:
        raise ValueError("expected a repository-relative file path")
    for part in name.split("/"):
        reserved = re.fullmatch(r"CON|PRN|AUX|NUL|(?:LPT|COM)[1-9]",
                                part.split(".")[0], re.IGNORECASE)
        if (not re.fullmatch(r"[A-Za-z0-9_.-]+", part) or part in (".", "..")
                or part.endswith(".") or reserved):
            raise ValueError(f"invalid portable research path: {name!r}")
    return name


def load_manifest(raw, pin):
    if sha(raw) != pin:
        raise ValueError("manifest bytes differ from their supplied SHA-256")
    obj = json.loads(raw, object_pairs_hook=unique_paths)
    fields = {"commit", "program", "inputs", "expected_output", "sha256"}
    if not isinstance(obj, dict) or set(obj) != fields:
        raise ValueError(f"expected manifest fields {sorted(fields)}")
    if not isinstance(obj["commit"], str):
        raise ValueError("expected a full Git commit ID")
    if not isinstance(obj["inputs"], list) or not isinstance(obj["sha256"], dict):
        raise ValueError("expected input list and path-to-SHA-256 table")
    names = [portable_path(n) for n in [obj["program"], *obj["inputs"], obj["expected_output"]]]
    if len({n.casefold() for n in names}) != len(names) or set(names) != set(obj["sha256"]):
        raise ValueError("program, inputs and expected output must name distinct, uniquely pinned files")
    if Path(obj["program"]).suffix != ".py":
        raise ValueError("this runner accepts a Python program")
    return obj


def compare_output(file, expected):
    result = {"expected_sha256": sha(expected), "expected_bytes": len(expected)}
    if file.resolve() != file or not file.is_file():
        return dict(result, status="NO_REGULAR_OUTPUT")
    actual = file.read_bytes()
    result.update(observed_sha256=sha(actual), observed_bytes=len(actual))
    if actual == expected:
        return dict(result, status="MATCH")
    offset = next((i for i, (x, y) in enumerate(zip(actual, expected)) if x != y),
                  min(len(expected), len(actual)))
    return dict(result, status="DIFFERS", first_differing_byte=offset)


def replay(repo, raw, pin):
    spec = load_manifest(raw, pin)
    pins = json.dumps(spec["sha256"], sort_keys=True).encode("ascii")
    registration = compare(repo, spec["commit"], pins, sha(pins))
    reference = spec["expected_output"]
    record = {"manifest_sha256": pin, "commit": spec["commit"], "program": spec["program"],
              "inputs": spec["inputs"], "expected_output": reference, "files": registration["files"],
              "ran": False, "exit_code": None}
    if not registration["unchanged"]:
        return dict(record, status="REGISTRATION_DIFFERS")
    with tempfile.TemporaryDirectory(prefix="science-replay-") as tmp:
        root = Path(tmp).resolve()
        source = root / "source"
        for item in registration["files"]:
            body = git(repo, "cat-file", "blob", item["object_id"])
            if sha(body) != item["sha256"]:
                raise ValueError("blob changed between registration and materialization")
            if item["path"] == reference:
                expected = body
            else:
                dest = source / item["path"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("xb") as stream:
                    stream.write(body)

        # Keep the reference bytes outside the temporary program tree.
        output = root / "generated"
        python = Path(sys.executable).resolve()
        flags = ["-E", "-s", "-B"]
        threads = {key: "1" for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}
        child = subprocess.run([str(python), *flags, str(source / spec["program"]), str(output)],
                               cwd=source, env={**os.environ, **threads}, stdin=subprocess.DEVNULL,
                               capture_output=True, check=False)
        runtime = {"python": sys.version, "executable_sha256": sha(python.read_bytes()),
                   "platform": platform.platform(), "flags": flags, "thread_environment": threads}
        record.update(ran=True, exit_code=child.returncode, runtime=runtime,
                      stdout_sha256=sha(child.stdout), stderr_sha256=sha(child.stderr))
        result = compare_output(output / Path(reference).name, expected)
        record["output"] = result
        if child.returncode:
            record["stderr_tail"] = child.stderr[-2000:].decode("utf-8", errors="replace")
            return dict(record, status="PROGRAM_FAILED")
        return dict(record, status=result["status"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("expected_manifest_sha256")
    options = parser.parse_args()
    try:
        report = replay(options.repository, options.manifest.read_bytes(), options.expected_manifest_sha256)
    except (ValueError, OSError) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps(report, indent=2, ensure_ascii=True, allow_nan=False))
    return 0 if report["status"] == "MATCH" else 5


if __name__ == "__main__":
    raise SystemExit(main())
