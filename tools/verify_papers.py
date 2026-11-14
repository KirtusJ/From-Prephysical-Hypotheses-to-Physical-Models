"""Check the front paper catalog. Requires PyMuPDF. Use --write to refresh its CSV."""

import argparse
import csv
import hashlib
import io
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote, unquote

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "edition"
PAPERS = ROOT / "papers"
ARCHIVE_INDEX = EDITION / "PROGRAM/registers/PAPER_INDEX.csv"
ALIAS = re.compile(r"\b(?:directors?[\s_~–-]+[a-z](?!\w)|iris\b)", re.I)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reader_name(row):
    # Keep every title word; the two subtitle separators below are illegal on Windows.
    title = re.sub(r"[:?]\s+", " – ", row["title"])
    return f"{row['id']} - {title}.pdf"


def check_text(label, content):
    normalized = unicodedata.normalize("NFKC", content).replace(r"\_", "_")
    match = ALIAS.search(normalized)
    if match:
        raise ValueError(f"{label} contains a workflow alias: {match.group()!r}")
    # Text layers can put whitespace or a discretionary hyphen inside a name.
    spelling = re.sub(r"[\s\u00ad\u2010-\u2014-]+", "", normalized.casefold())
    if "deepseek(highflyer)" in spelling:
        raise ValueError(f"{label} should credit DeepSeek by its published name")


def inspect_pdf(path, title):
    with pymupdf.open(path) as document:
        if document.metadata.get("title") != title:
            raise ValueError(f"{path.name} PDF title differs from the paper index")
        cover = " ".join(document[0].get_text().casefold().split())
        for credit in ("kirtus justus", "theoretical physicist", "port coquitlam",
                       "british columbia", "canada"):
            if credit not in cover:
                raise ValueError(f"{path.name} title page is missing {credit!r}")
        check_text(path.name, "\n".join(str(v) for v in document.metadata.values() if v))
        check_text(path.name, document.get_xml_metadata())
        check_text(path.name, "\n".join(row[1] for row in document.get_toc()))
        for number, page in enumerate(document, 1):
            check_text(f"{path.name} p. {number}", page.get_text())
            for annotation in page.annots() or ():
                check_text(f"{path.name} p. {number} annotation", str(annotation.info))
        return len(document)


def verify_catalog(write):
    with ARCHIVE_INDEX.open(encoding="utf-8-sig", newline="") as file:
        entries = list(csv.DictReader(file))
    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate paper ID in edition index")
    expected = {row["id"] for row in entries if row["kind"] != "planned"}
    filenames = {reader_name(row) for row in entries if row["kind"] != "planned"}
    found = {path.name for path in PAPERS.glob("*.pdf")}
    if found != filenames:
        raise ValueError(f"Missing {filenames - found}, unexpected {found - filenames}")
    catalog = (PAPERS / "README.md").read_text(encoding="utf-8")
    contributions = (PAPERS / "contributions.md").read_text(encoding="utf-8")
    anchors = re.findall(r'<a\s+id="([A-G][1-9][0-9]*)"\s*>\s*</a>', contributions)
    if sorted(anchors) != sorted(ids):
        raise ValueError("Expected a unique contribution record for every indexed paper and plan")
    for link in re.findall(r"\]\(([^)]+)\)", catalog):
        if not link.startswith(("https://", "#")):
            if write and link == "catalog.csv":
                continue
            if not (PAPERS / unquote(link.split("#")[0])).exists():
                raise ValueError(f"Catalog link is missing: {link}")
    for source in (PAPERS / "source").rglob("*.tex"):
        check_text(source, source.read_text(encoding="utf-8"))
    buffer = io.StringIO(newline="")
    fields = ["id", "series", "title", "kind", "contributions", "file", "pages", "sha256",
              "issued_file", "issued_pages", "issued_sha256"]
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in entries:
        key = row["id"]
        record = {field: row[field] for field in ("id", "series", "title", "kind")}
        record["contributions"] = f"contributions.md#{key}"
        if catalog.count(f"]({record['contributions']})") != 1:
            raise ValueError(f"Expected exactly one paper-level credit link for {key}")
        if key in expected:
            reader = PAPERS / reader_name(row)
            original = EDITION / row["file"]
            link = quote(reader.name)
            if catalog.count(f"]({link})") != 1:
                raise ValueError(f"Expected exactly one reader link for {key}")
            pages = inspect_pdf(reader, row["title"])
            catalog_row = f"| {key} | [{row['title']}]({link}) | {pages} |"
            if catalog_row not in catalog:
                raise ValueError(f"Catalog title or page count differs for {key}")
            record.update(file=reader.name, pages=pages, sha256=digest(reader),
                          issued_file=original.relative_to(ROOT).as_posix(),
                          issued_pages=int(row["pages"]), issued_sha256=digest(original))
        else:
            plan, = (EDITION / "PAPERS").glob(f"{key}_*/PLANNED.md")
            if f"](../{plan.relative_to(ROOT).as_posix()})" not in catalog:
                raise ValueError(f"Missing plan link for {key}")
            record.update(issued_file=plan.relative_to(ROOT).as_posix())
        writer.writerow(record)
    manifest = PAPERS / "catalog.csv"
    if write:
        manifest.write_bytes(buffer.getvalue().encode("utf-8"))
    elif manifest.read_text(encoding="utf-8") != buffer.getvalue():
        raise ValueError("Paper catalog differs from its PDFs or the issued index")
    print(f"{len(expected)} reader PDFs and {len(entries) - len(expected)} plan(s) verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    verify_catalog(parser.parse_args().write)
