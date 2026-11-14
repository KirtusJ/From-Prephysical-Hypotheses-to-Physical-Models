"""Verify locally preserved sources in the three early provenance manifests.

Run from any directory. The spelling and digest of the original container and
the member path distinguish provenance; the same member can survive in more
than one archive. A record without retained bytes is a reference only.
"""
import hashlib
import json
import re
import stat
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = (
    "candidates/sources/early",
    "quarantine/fiction/sources",
    "quarantine/mixed/sources",
)
METADATA = {"README.md", "provenance.json"}


def fail(message):
    raise ValueError(message)


def object_fields(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            fail(f"duplicate JSON key {k!r}")
        result[k] = v
    return result


def sha(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", value):
        fail(f"{label} needs a SHA-256 digest")
    return value.lower()


def regular(path):
    if linked(path) or not path.is_file():
        fail(f"expected a regular file at {path}")


def linked(path):
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def retained_name(name, label):
    bad = '<>:"/\\|?*'
    if (not isinstance(name, str) or not name or name in (".", "..")
            or any(c in bad or ord(c) < 32 for c in name)
            or name.endswith((" ", "."))
            or re.fullmatch(r"(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|(?:COM|LPT)[0-9¹²³])",
                            name.split(".", 1)[0].rstrip(" "), re.IGNORECASE)
            or name.casefold() in {k.casefold() for k in METADATA}):
        fail(f"{label}: unsafe or reserved retained basename {name!r}")
    return name


def verify(root):
    identities = {}
    unique_bytes = set()
    retained_files = record_count = 0
    for location in DIRECTORIES:
        folder = root / location
        for part in (folder, *folder.parents):
            if part == root:
                break
            if linked(part):
                fail(f"linked source directory {part}")
        manifest = folder / "provenance.json"
        regular(manifest)
        data = json.loads(manifest.read_bytes(), object_pairs_hook=object_fields)
        if (not isinstance(data, dict) or not isinstance(data.get("scope"), str)
                or not data["scope"].strip() or not isinstance(data.get("records"), list)):
            fail(f"{location}: missing scope or records array")
        retained = {}
        case_spelling = {}
        for index, row in enumerate(data["records"], 1):
            label = f"{location} record {index}"
            if not isinstance(row, dict) or not isinstance(row.get("source"), str) or not row["source"].strip():
                fail(f"{label}: missing source identity")
            artifact = sha(row.get("sha256"), label)
            member = row.get("member")
            if "member" in row:
                if not isinstance(member, str) or not member.strip():
                    fail(f"{label}: empty archive member")
                digest = sha(row.get("member_sha256"), label)
            else:
                if "member_sha256" in row:
                    fail(f"{label}: member digest without a named archive member")
                digest = artifact
            identity = (row["source"], artifact, member)
            if identity in identities:
                fail(f"{label} repeats original source/member identity from {identities[identity]}")
            identities[identity] = label
            record_count += 1
            if "retained" in row:
                name = retained_name(row["retained"], label)
                if case_spelling.setdefault(name.casefold(), name) != name:
                    fail(f"{label}: case-colliding retained names")
                if retained.setdefault(name, digest) != digest:
                    fail(f"{label}: incompatible digests for retained file {name}")
        found = set()
        for path in folder.iterdir():
            regular(path)
            if path.name in METADATA:
                continue
            if path.name not in retained:
                fail(f"{location}: unindexed file {path.name}")
            observed = hashlib.sha256(path.read_bytes()).hexdigest()
            if observed != retained[path.name]:
                fail(f"{location}: {path.name} digest mismatch, expected {retained[path.name]}, got {observed}")
            found.add(path.name)
            unique_bytes.add(observed)
        missing = sorted(retained.keys() - found)
        if missing:
            fail(f"{location}: missing retained files {missing}")
        retained_files += len(found)
    return record_count, retained_files, len(unique_bytes)


def check_target(root, document, link, allow_landing):
    url = urlsplit(link)
    if url.scheme or url.netloc or not url.path:
        return
    path = unquote(url.path)
    base = root if path.startswith("/") else document.parent
    target = (base / path.lstrip("/")).resolve()
    quarantine = root / "quarantine"
    if target.is_relative_to(quarantine):
        if not allow_landing or target not in (quarantine, quarantine / "README.md"):
            fail(f"{document.relative_to(root)}: direct evidence link into quarantine: {link}")
    if target.is_relative_to(root / DIRECTORIES[0]) and not target.exists():
        fail(f"{document.relative_to(root)}: missing early research source: {link}")


def check_indexes(root):
    # Inspect local link destinations in the current catalog, not the words of source documents.
    for document in (root / "README.md", *(root / "candidates").glob("*.md")):
        for match in re.finditer(r"\]\(\s*(?:<([^>]+)>|([^\s)]+))", document.read_text(encoding="utf-8")):
            check_target(root, document, match.group(1) or match.group(2), allow_landing=True)
    document = root / "Director_G/ontology_gate_map.json"
    gate_map = json.loads(document.read_bytes())
    for gate in gate_map["gates"]:
        for update in gate.get("evidence_updates", []):
            for link in update.get("sources", []):
                check_target(root, document, link, allow_landing=False)


if __name__ == "__main__":
    try:
        records, files, contents = verify(ROOT)
        check_indexes(ROOT)
    except (OSError, ValueError, UnicodeError) as error:
        sys.exit(f"Archive check failed: {error}")
    print(f"Verified {records} provenance records, {files} retained files and {contents} distinct byte identities.")
