"""Validate the 33 judgments against Z33. Optional PyMuPDF replay uses five component PDFs."""
import argparse
import ast
import csv
import hashlib
import io
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

PIN = "0ca75f60c76af1be7f3c25c2ed8914e82243ff5d"
REGISTRY = "edition/PROGRAM/registers/THEOREM_REGISTRY.csv"
EXTRACTOR = "edition/tools/assemble.py"
PUBLIC_BASE = "https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/" + PIN + "/"
SELECTED = {"PROOF_NOT_ADJACENT", "CONDITIONAL_ON_NAMED_INPUTS"}
REPLAY_IDS = ["D6-05-11", "F2-01-06", "D8-03-04", "D3-01-01", "F1-01-06"]
BLOBS = {
    "edition/PAPERS/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy/parts/01_Finite_Part_of_Wilson_Dirac_Relative_Entropy.pdf": "50e812b4dffffc3e74e2725f975ea6f7f823574e",
    "edition/PAPERS/D6_Concentration_Spectrum_of_the_Half_Filled_Sine_Kernel_Periods_Tails_an/parts/05_Positive_Moment_Bounds_and_Growing_Plunge_Windows.pdf": "2869c938fafb35da97d5ae27358af079446f7fa9",
    "edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/parts/03_Exact_Wilson_Reference_Geometry_and_Two_Bond_Asymptotics.pdf": "e73163e43a6dde68d5dfe9c3c30b73d950011b68",
    "edition/PAPERS/F1_Abstract_Channels_and_Gaussian_Capacity/parts/01_Abstract_Channels_and_Gaussian_Capacity.pdf": "e184a4037a06ea5e54cf0f2b63f157f63fec41ed",
    "edition/PAPERS/F2_Stochastic_Recovery_from_Information_Loss_and_Equality_of_Channel_Capa/parts/01_Stochastic_Recovery_and_Capacity_Equality.pdf": "c70148cdd325115619c4e5d77d908906c5aa15d0",
    "edition/PROGRAM/registers/THEOREM_REGISTRY.csv": "b05ea06aa3079d86fb2b147e641359cefb7c6771",
    "edition/tools/assemble.py": "95017f46bdedab310bc47a26c7a42be545122b7b",
}


def component_path(registry_row, paths):
    prefix = "edition/PAPERS/" + registry_row["paper"] + "_"
    part = "/parts/" + registry_row["id"].split("-")[1] + "_"
    candidates = [p for p in paths if p.startswith(prefix) and part in p and p.endswith(".pdf")]
    if len(candidates) != 1:
        raise ValueError("Expected one original component for " + registry_row["id"])
    return candidates[0]


def pinned_data(path, args):
    if args.source_tree:
        data = (args.source_tree / path).read_bytes()
    else:
        data = subprocess.check_output(["git", "-C", str(args.repo), "show", PIN + ":" + path])
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob != BLOBS[path]:
        raise ValueError("Wrong Z33 source blob for " + path)
    return data


def check_rows(rows):
    source = Path(__file__).with_name("judgments.md").read_text(encoding="utf-8")
    sections = re.split(r"^## ([A-Z]\d+-\d+-\d+) · [^\n]+\n", source, flags=re.M)
    reviewed = {}
    for identifier, body in zip(sections[1::2], sections[2::2]):
        if identifier in reviewed:
            raise ValueError("Duplicate judgment for " + identifier)
        reviewed[identifier] = body
    expected = {r["id"] for r in rows if r["status"] in SELECTED}
    if len(rows) != 456 or len(expected) != 33 or set(reviewed) != expected:
        raise ValueError("The ledger IDs do not match the 33 selected Z33 rows")
    for row in rows:
        if row["id"] not in reviewed:
            continue
        body = reviewed[row["id"]]
        paper = row["paper"]
        page = row["paper_file_page"]
        link_pattern = re.escape(PUBLIC_BASE + "edition/PAPERS/" + paper + "_") + r"[^\s)]+\.pdf#page=" + page + r"\)"
        if "Issued status `" + row["status"] + "`" not in body or not re.search(link_pattern, body):
            raise ValueError("Status or pinned page mismatch for " + row["id"])
    print("33/33 unique IDs, issued labels and pinned page links match the Z33 register.")


def replay(rows, args):
    try:
        import pymupdf
    except ImportError:
        raise SystemExit("--replay requires PyMuPDF (verified with version 1.26.6).")
    tree = ast.parse(pinned_data(EXTRACTOR, args))
    selected = []
    for n in tree.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "ST_RE":
            selected.append(n)
        if isinstance(n, ast.FunctionDef) and n.name == "statements":
            selected.append(n)
    if len(selected) != 2:
        raise ValueError("Expected the issued regular expression and extraction function")
    scope = {"re": re, "unicodedata": unicodedata, "pymupdf": pymupdf}
    exec(compile(ast.Module(body=selected, type_ignores=[]), EXTRACTOR, "exec"), scope)
    by_id = {r["id"]: r for r in rows}
    with tempfile.TemporaryDirectory() as folder:
        for identifier in REPLAY_IDS:
            r = by_id[identifier]
            path = component_path(r, BLOBS)
            pdf = Path(folder) / (identifier + ".pdf")
            pdf.write_bytes(pinned_data(path, args))
            extracted, unused_text = scope["statements"](str(pdf))
            match = [e for e in extracted if (e["kind"], e["number"], e["name"]) == (r["kind"], r["number"], r["name"])]
            if len(match) != 1 or (match[0]["page"], match[0]["status"]) != (int(r["part_page"]), r["status"]):
                raise ValueError("Extractor replay mismatch for " + identifier)
            print(f'{identifier}  component p. {r["part_page"]}  {r["status"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--repo", type=Path, default=Path("."), help="Public repository checkout containing Z33")
    source.add_argument("--source-tree", type=Path, help="Extracted Z33 source tree, checked against pinned blob IDs")
    parser.add_argument("--replay", action="store_true", help="Run the issued extraction function on five source components")
    args = parser.parse_args()
    rows = list(csv.DictReader(io.StringIO(pinned_data(REGISTRY, args).decode("utf-8"))))
    check_rows(rows)
    if args.replay:
        replay(rows, args)


if __name__ == "__main__":
    main()
