"""Replay the registered-at-commit reader against synthetic Git objects and real addenda."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


READER = Path(__file__).with_name("check_registered_commit.py")
RECOVERY_COMMIT = "cc9c8d57a1e651caf80384d176a4b15c5c8da104"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", str(repo), *args], input=data,
                          capture_output=True, check=True).stdout.strip()


def register(repo, commit, manifest, path, pin=None):
    path.write_bytes(manifest)
    return subprocess.run([sys.executable, "-B", str(READER), str(repo), commit,
                           str(path), pin or sha(manifest)], capture_output=True)


class CommitReaderTest(unittest.TestCase):
    def test_literal_git_tree_and_pinned_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp, "repo")
            repo.mkdir()
            git(repo, "init", "-q")
            body = b"original\r\n"
            blob = git(repo, "hash-object", "-w", "--stdin", data=body)
            target = git(repo, "hash-object", "-w", "--stdin", data=b"file.txt")
            tree = git(repo, "mktree", data=(b"100644 blob "+blob+b"\tfile.txt\n"
                          +b"120000 blob "+target+b"\tlink\n"))
            commit = git(repo, "-c", "user.name=test", "-c", "user.email=test@example.invalid",
                         "commit-tree", tree.decode(), "-m", "fixture").decode()
            (repo / "file.txt").write_bytes(b"dirty\n")
            manifest_path = Path(tmp, "manifest.json")
            good = json.dumps({"file.txt": sha(body)}).encode()
            a = register(repo, commit, good, manifest_path)
            b = register(repo, commit, good, manifest_path)
            self.assertEqual((a.returncode, a.stdout), (0, b.stdout))
            self.assertEqual(b.returncode, 0)
            observed = json.loads(a.stdout)["files"][0]
            self.assertEqual((observed["bytes"], observed["object_id"]), (len(body), blob.decode()))
            bad = json.dumps({p: sha(b"wrong") for p in ("file.txt", "link", "missing")}).encode()
            c = register(repo, commit, bad, manifest_path)
            self.assertEqual(c.returncode, 5)
            self.assertEqual([r["status"] for r in json.loads(c.stdout)["files"]],
                             ["DIFFERS", "NOT_REGULAR", "MISSING"])
            duplicate = b'{"x":"' + sha(body).encode() + b'","x":"' + sha(body).encode() + b'"}'
            for damaged, ref, pin in [(good+b" ", commit, sha(good)), (good, "HEAD", None),
                                      (duplicate, commit, None), (b"{}", commit, None)]:
                with self.subTest(ref=ref, data=damaged):
                    reply = register(repo, ref, damaged, manifest_path, pin)
                    self.assertEqual((reply.returncode, reply.stdout), (2, b""))

    def test_registered_and_issued_addenda(self):
        repo = READER.parent.parent
        probe = subprocess.run(["git", "-C", str(repo), "cat-file", "-e", RECOVERY_COMMIT],
                               capture_output=True)
        if probe.returncode:
            self.skipTest("recovery commit unavailable in this checkout")
        register_bytes = git(repo, "show", RECOVERY_COMMIT + ":.pcp/register.jsonl")
        events = [json.loads(line) for line in register_bytes.splitlines()]
        registered = {e["body"]["filename"]: e["body"]["sha256"] for e in events
                      if e["seq"] in (374, 492) and e["kind"] == "ARTIFACT_ADDED"}
        self.assertEqual(len(registered), 2)
        with tempfile.TemporaryDirectory() as tmp:
            for prefix, expected_exit in [("case_studies/recovered", 0), ("Director_Z/addenda", 5)]:
                manifest = json.dumps({prefix+"/"+p: d for p,d in registered.items()}).encode()
                result = register(repo, RECOVERY_COMMIT, manifest, Path(tmp, "manifest.json"))
                self.assertEqual(result.returncode, expected_exit, result.stderr)
                expected = "DIFFERS" if expected_exit else "UNCHANGED"
                self.assertEqual([r["status"] for r in json.loads(result.stdout)["files"]],
                                 [expected, expected])


if __name__ == "__main__":
    unittest.main()
