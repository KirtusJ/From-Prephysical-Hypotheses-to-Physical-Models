"""Replay the issued Z26 verifier on a checkout or extracted edition directory."""

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile


# The Z26 manifest hashes the verifier itself. Adapt a private copy so the
# edition stays byte-identical and every original check runs on the real tree.
VERIFIER_SHA256 = "8532cb66ce83a711027400df17c6c5bfa6d5e209c84fc050235f5700d25f21b6"
RELATIVE_PATH = b"rel = os.path.relpath(os.path.join(dp, f), ROOT)"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition", type=Path, nargs="?",
                        default=Path(__file__).resolve().parents[1] / "edition",
                        help="directory containing Z26's MANIFEST.json and verify_baseline.py")
    edition = parser.parse_args().edition.resolve()
    try:
        source = (edition / "verify_baseline.py").read_bytes()
    except OSError as error:
        parser.exit(2, f"Cannot read the issued verifier: {error}\n")
    digest = hashlib.sha256(source).hexdigest()
    if digest != VERIFIER_SHA256:
        parser.exit(2, f"Unrecognized verifier SHA-256 {digest}. Expected Z26's {VERIFIER_SHA256}.\n")

    if os.name == "nt":
        # The manifest stores paths with '/', while Windows relpath uses '\\'.
        if source.count(RELATIVE_PATH) != 1:
            parser.exit(2, "Could not locate the Z26 manifest path comparison.\n")
        source = source.replace(RELATIVE_PATH, RELATIVE_PATH + b'.replace(os.sep, "/")')

    with tempfile.TemporaryDirectory() as scratch:
        verifier = Path(scratch) / "verify_baseline.py"
        verifier.write_bytes(source)
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(verifier), str(edition)]).returncode


if __name__ == "__main__":
    sys.exit(main())
