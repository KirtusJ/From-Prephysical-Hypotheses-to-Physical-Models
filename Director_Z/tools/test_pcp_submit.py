"""Exercise call accounting with the released host. Set PCPOS_BIN if it is not on PATH."""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from pathlib import Path

import pcp_submit

SUBMITTER = Path(__file__).with_name("pcp_submit.py").resolve()


class ReplyFiles(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.request = self.root / "calls.json"
        self.request.write_text('[{"name":"acr_status"}]')
        self.ledger = self.root / "Director_Z" / "tools" / "submitted_calls.jsonl"
        self.started = 0
        host = patch.object(pcp_submit.subprocess, "Popen", side_effect=self.reply)
        host.start()
        self.addCleanup(host.stop)

    def reply(self, *args, **kwargs):
        self.started += 1
        text = f"response {self.started}"
        payload = {"result": {"content": [{"text": text}]}}
        child = unittest.mock.Mock()
        child.stdin = io.StringIO()
        child.stdout = io.StringIO("{}\n" + json.dumps(payload) + "\n")
        child.stderr = io.StringIO()
        return child

    def run_submit(self, *flags):
        return pcp_submit.main(["submit", str(self.root), str(self.request), *flags])

    def entries(self):
        return [json.loads(line) for line in self.ledger.read_text().splitlines()]

    def test_reused_path_and_explicit_replay_keep_each_submission(self):
        self.assertEqual(self.run_submit(), 0)
        self.request.write_text('[{"name":"acr_verify"}]')
        self.assertEqual(self.run_submit(), 0)
        self.assertEqual(self.run_submit("--again"), 0)
        self.assertEqual(self.run_submit(), 4)
        entries = self.entries()
        self.assertEqual(self.started, 3)
        self.assertEqual(len({row["output"] for row in entries}), 3)
        self.assertEqual(entries[1]["sha256"], entries[2]["sha256"])
        self.assertNotEqual(entries[0]["sha256"], entries[1]["sha256"])
        for number, row in enumerate(entries, 1):
            data = Path(row["output"]).read_bytes()
            self.assertIn(f"response {number}".encode(), data)
            self.assertEqual(row["output_sha256"], hashlib.sha256(data).hexdigest())
        latest = self.root / "calls.json.out"
        self.assertEqual(latest.read_bytes(), Path(entries[2]["output"]).read_bytes())

    def test_old_view_paths_are_preserved_including_relative_paths(self):
        for old in ("calls.json.out", "calls.json.latest.out"):
            (self.root / old).write_text("old replies")
        self.ledger.parent.mkdir(parents=True)
        legacy = {"sha256": "legacy", "time": "old", "written": 1, "refused": 0}
        old_entries = [dict(legacy, output=str(self.root / "calls.json.out")),
                       dict(legacy, output="calls.json.latest.out")]
        self.ledger.write_text("".join(json.dumps(row)+"\n" for row in old_entries))
        self.assertEqual(self.run_submit(), 0)
        entries = self.entries()
        self.assertEqual(entries[:2], old_entries)
        for old in ("calls.json.out", "calls.json.latest.out"):
            self.assertEqual((self.root / old).read_text(), "old replies")
        self.assertEqual(Path(entries[-1]["latest_output"]).read_bytes(), Path(entries[-1]["output"]).read_bytes())

    def test_concurrent_identical_requests_send_once(self):
        with ThreadPoolExecutor(max_workers=4) as workers:
            results = list(workers.map(lambda _: self.run_submit(), range(4)))
        self.assertEqual(sorted(results), [0, 4, 4, 4])
        self.assertEqual(self.started, 1)
        self.assertEqual(len(self.entries()), 1)

    def test_view_refresh_failure_does_not_resubmit_completed_calls(self):
        with patch.object(pcp_submit.os, "replace", side_effect=OSError("view unavailable")):
            self.assertEqual(self.run_submit(), 0)
        row, = self.entries()
        self.assertTrue(Path(row["output"]).is_file())
        self.assertEqual(self.run_submit(), 4)
        self.assertEqual(self.started, 1)


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
