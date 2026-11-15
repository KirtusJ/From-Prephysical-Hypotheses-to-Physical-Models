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
PAPER_INDEX = "edition/PROGRAM/registers/PAPER_INDEX.csv"
EXTRACTOR = "edition/tools/assemble.py"
PUBLIC_BASE = "https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/" + PIN + "/"
SELECTED = {"PROOF_NOT_ADJACENT", "CONDITIONAL_ON_NAMED_INPUTS"}
REPLAY_IDS = ["D6-05-11", "F2-01-06", "D8-03-04", "D3-01-01", "F1-01-06"]
BLOBS = {
    PAPER_INDEX: "8f7d0b9fc2d98b52fe7f54cbfde223c204416af5",
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


def check_judgment(row, paper_path, heading, body):
    # The issued extractor joins these two words in D8-03-04.
    name = row["name"].replace("fixed-μtwo-bond", "fixed-μ two-bond")
    title = " ".join(part for part in (row["kind"], row["number"], name) if part)
    if heading != title:
        raise ValueError("Issued heading mismatch for " + row["id"])
    if re.findall(r"^Issued status `([^`]+)`", body, re.M) != [row["status"]]:
        raise ValueError("Issued status mismatch for " + row["id"])
    paper = row["paper"]
    page = row["paper_file_page"]
    reference = (f"Assembled {paper}, p. {page}", f"{PUBLIC_BASE}edition/{paper_path}#page={page}")
    links = re.findall(r"\[(Assembled [^]\n]+)\]\(([^)\s]+)\)", body)
    if links != [reference]:
        raise ValueError("Assembled paper or page mismatch for " + row["id"])


def check_rows(rows, papers):
    source = Path(__file__).with_name("judgments.md").read_text(encoding="utf-8")
    sections = re.split(r"^## ([A-Z]\d+-\d+-\d+) · ([^\n]+)\n", source, flags=re.M)
    reviewed = {}
    for identifier, heading, body in zip(sections[1::3], sections[2::3], sections[3::3]):
        if identifier in reviewed:
            raise ValueError("Duplicate judgment for " + identifier)
        reviewed[identifier] = (heading, body)
    expected = {r["id"] for r in rows if r["status"] in SELECTED}
    if len(rows) != 456 or len(expected) != 33 or set(reviewed) != expected:
        raise ValueError("The ledger IDs do not match the 33 selected Z33 rows")
    for row in rows:
        if row["id"] not in reviewed:
            continue
        heading, body = reviewed[row["id"]]
        check_judgment(row, papers[row["paper"]], heading, body)
    print("33/33 unique IDs, issued headings and statuses, and assembled-paper page links match Z33.")


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
    index = csv.DictReader(io.StringIO(pinned_data(PAPER_INDEX, args).decode("utf-8-sig")))
    papers = {row["id"]: row["file"] for row in index}
    check_rows(rows, papers)
    if args.replay:
        replay(rows, args)


if __name__ == "__main__":
    main()
