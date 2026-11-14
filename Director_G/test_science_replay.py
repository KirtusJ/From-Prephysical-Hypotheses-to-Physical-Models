"""Exercise registration and process/output failures against a dirty synthetic Git tree."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from replay_science import load_manifest, replay


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ScienceReplayTest(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.files = {
            ".gitattributes": b"* -text\n",
            "trial.py": (b"from pathlib import Path\nimport sys\n"
                         b"if Path('archived/out.json').exists(): raise ValueError('exposed reference')\n"
                         b"blob = Path('input').read_bytes()\n"
                         b"folder = Path(sys.argv[1])\nfolder.mkdir()\n"
                         b"(folder/'out.json').write_bytes(blob)\n"),
            "fail.py": (b"from pathlib import Path\nimport sys\n"
                        b"folder=Path(sys.argv[1])\nfolder.mkdir()\n"
                        b"(folder/'out.json').write_bytes(Path('input').read_bytes())\n"
                        b"raise SystemExit(7)\n"),
            "quiet.py": b"pass\n",
            "file.py": (b"from pathlib import Path\nimport sys\n"
                        b"if Path('archived/out.json').exists(): raise ValueError('exposed reference')\n"
                        b"path = Path(sys.argv[1])\n"
                        b"if path.name != 'out.json': raise ValueError('wrong basename')\n"
                        b"with path.open('xb') as f: f.write(Path('input').read_bytes())\n"),
            "input": b"123\n",
            "archived/out.json": b"123\n",
            "other/out.json": b"124\n",
            "longer/out.json": b"123\n\n",
        }
        self.git("init", "-q")
        for name, body in self.files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        self.git("add", ".")
        self.git("-c", "user.name=Tester", "-c", "user.email=test@example.org", "commit", "-qm", "fixture")
        self.commit = self.git("rev-parse", "HEAD")
        (self.repo / "trial.py").write_bytes(b"raise RuntimeError('working tree ran')\n")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args]).decode().strip()

    def manifest(self, program="trial.py", inputs=("input",), reference="archived/out.json", change=None,
                 output_argument=None):
        pins = {key: digest(self.files[key]) for key in (program, *inputs, reference)}
        if change:
            pins.update(change)
        spec = dict(commit=self.commit, program=program, inputs=list(inputs),
                    expected_output=reference, sha256=pins)
        if output_argument is not None:
            spec["output_argument"] = output_argument
        return json.dumps(spec).encode()

    def execute(self, *args, **kwargs):
        raw = self.manifest(*args, **kwargs)
        return replay(self.repo, raw, digest(raw))

    def test_git_bytes_and_failures(self):
        self.assertEqual(self.execute()["status"], "MATCH")
        for path, offset in (("other/out.json", 2), ("longer/out.json", 4)):
            result = self.execute(reference=path)
            self.assertEqual((result["status"], result["output"]["first_differing_byte"]), ("DIFFERS", offset))
        self.assertEqual(self.execute(inputs=())["status"], "PROGRAM_FAILED")
        result = self.execute("fail.py")
        self.assertEqual((result["status"], result["exit_code"], result["output"]["status"]),
                         ("PROGRAM_FAILED", 7, "MATCH"))
        self.assertEqual(self.execute("quiet.py")["status"], "NO_REGULAR_OUTPUT")
        changed = self.execute(change={"input": "0"*64})
        self.assertEqual((changed["status"], changed["ran"]), ("REGISTRATION_DIFFERS", False))
        self.assertEqual(self.git("status", "--porcelain"), "M trial.py")

    def test_output_argument(self):
        self.assertEqual(self.execute(output_argument="directory")["status"], "MATCH")
        self.assertEqual(self.execute("file.py", output_argument="file")["status"], "MATCH")
        self.assertEqual(self.execute("file.py", reference="other/out.json",
                                      output_argument="file")["status"], "DIFFERS")
        self.assertEqual(self.execute("quiet.py", output_argument="file")["status"], "NO_REGULAR_OUTPUT")
        self.assertEqual(self.execute("file.py", inputs=(), output_argument="file")["status"], "PROGRAM_FAILED")
        self.assertEqual(self.execute("trial.py", output_argument="file")["status"], "NO_REGULAR_OUTPUT")

    def test_invalid_setup(self):
        raw = self.manifest()
        with self.assertRaises(ValueError):
            replay(self.repo, raw + b" ", digest(raw))
        for bad in ("../out.json", "C:/out.json", "CON.txt", "a\\b"):
            doc = json.loads(raw)
            doc["expected_output"] = bad
            invalid = json.dumps(doc).encode()
            with self.assertRaisesRegex(ValueError, "portable research path"):
                load_manifest(invalid, digest(invalid))
        for key, value in (("commit", 123), ("inputs", ["INPUT"]), ("inputs", ["input", "INPUT"])):
            doc = json.loads(raw)
            doc[key] = value
            invalid = json.dumps(doc).encode()
            with self.assertRaises(ValueError):
                load_manifest(invalid, digest(invalid))
        for mode in ("stdout", "../escape", None, [], True):
            invalid = json.dumps({**json.loads(raw), "output_argument": mode}).encode()
            with self.assertRaisesRegex(ValueError, "output_argument"):
                load_manifest(invalid,digest(invalid))

    def test_cli_exit_codes(self):
        manifest = Path(self.temp.name) / "registration.json"
        tool = Path(__file__).with_name("replay_science.py")
        for reference, pin_error, status in (("archived/out.json", False, 0), ("other/out.json", False, 5),
                                              ("archived/out.json", True, 2)):
            body = self.manifest(reference=reference)
            manifest.write_bytes(body)
            result = subprocess.run([sys.executable, "-B", str(tool), str(self.repo), str(manifest),
                                     "0"*64 if pin_error else digest(body)], capture_output=True, check=False)
            self.assertEqual(result.returncode, status, result.stderr)


if __name__ == "__main__":
    unittest.main()
