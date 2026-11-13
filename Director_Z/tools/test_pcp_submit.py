"""Exercise call accounting with the released host. Set PCPOS_BIN if it is not on PATH."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SUBMITTER = Path(__file__).with_name("pcp_submit.py").resolve()


class SubmitAccounting(unittest.TestCase):
    def setUp(self):
        binary = shutil.which(os.environ.get("PCPOS_BIN", "pcpos"))
        if binary is None:
            self.skipTest("requires pcpos on PATH or PCPOS_BIN")
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.register = self.root / ".pcp" / "register.jsonl"
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("PCPOS_", "CLAUDE_PLUGIN_OPTION_"))}
        self.env.update(PCPOS_BIN=str(Path(binary).resolve()), PCPOS_ROOT=str(self.root),
                        PCPOS_REGISTER=".pcp/register.jsonl")
        self.register.parent.mkdir()
        subprocess.run([self.env["PCPOS_BIN"], "init", str(self.register), "--principal", "reader"],
                       env=self.env, cwd=self.root, check=True, capture_output=True)
        self.ledger = self.root / "Director_Z" / "tools" / "submitted_calls.jsonl"

    def submit(self, name, calls):
        request = self.root / (name + ".json")
        request.write_text(json.dumps(calls))
        return subprocess.run([sys.executable, str(SUBMITTER), str(self.root), str(request)],
                              env=self.env, cwd=self.root, capture_output=True, text=True, timeout=20)

    def test_replies_and_register(self):
        result = self.submit("begin", [{"name": "acr_begin"}])
        self.assertEqual(result.returncode, 0, result.stderr)
        before = self.register.read_bytes()
        (self.root / "REFUSE.txt").write_text("ordinary artifact\n")
        artifact = {"path": "REFUSE.txt", "name": "sample"}
        reads = [{"name": "acr_status"}, {"name": "acr_verify"},
                 {"name": "acr_artifact", "arguments": dict(artifact, record=False)}]
        result = self.submit("reads", reads)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("3 succeeded, 0 refused, 0 write receipts", result.stdout)
        self.assertEqual(before, self.register.read_bytes())

        calls = [{"name": "acr_artifact", "arguments": artifact},
                 {"name": "acr_submit", "arguments": {"kind": "GATE_COMMITTED",
                                                      "body": {"review": "absent", "gate": "G1"}}},
                 {"name": "acr_artifact", "arguments": {"name": "no-input"}},
                 {"name": "no-such-tool"}]
        result = self.submit("mixed", calls)
        self.assertEqual(result.returncode, 3, result.stdout)
        after = self.register.read_bytes()
        self.assertEqual(len(after.splitlines()) - len(before.splitlines()), 1)
        row = json.loads(self.ledger.read_text().splitlines()[-1])
        self.assertEqual((row["succeeded"], row["refused"], row["write_receipts"]), (1, 3, 1))
        report = Path(row["output"]).read_text()
        for i, call in enumerate(calls, 1):
            self.assertIn(f"=== [{i}] {call['name']}", report)
        result = self.submit("mixed", calls)
        self.assertEqual(result.returncode, 4)
        self.assertEqual(after, self.register.read_bytes())

    def test_legacy_ledger(self):
        calls = [{"name": "acr_status"}]
        digest = hashlib.sha256(json.dumps(calls).encode()).hexdigest()
        self.ledger.parent.mkdir(parents=True)
        self.ledger.write_text(json.dumps({"sha256": digest, "time": "old", "written": 1,
                                           "refused": 0, "output": "old.out"}) + "\n")
        before = self.register.read_bytes()
        result = self.submit("legacy", calls)
        self.assertEqual(result.returncode, 4)
        self.assertIn("legacy counts", result.stdout)
        self.assertEqual(before, self.register.read_bytes())


if __name__ == "__main__":
    unittest.main()
