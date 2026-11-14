"""Reproduce seven reader PDFs from the issued edition and the TeX glyph mapping.

Run with Python and PyMuPDF to generate the intermediate readers that preceded
the credit revision. Use a fresh output directory:
    python restore_math_text.py /path/to/pdfx/glyphtounicode-cmr.tex --output ./intermediate
"""
import argparse
import hashlib
import re
from pathlib import Path

import pymupdf


READERS = ("C3", "C5", "C6", "C7", "D3", "D4", "D6")
MAPPING_SHA256 = "4390c8bfb8a6f709b90b7502ae4accb74815a5269d99f18bb97c1dde95c16c2a"


def font_encoding(doc, font):
    reference = int(doc.xref_get_key(font, "Encoding")[1].split()[0])
    differences = doc.xref_get_key(reference, "Differences")[1]
    by_code = {}
    for token in re.findall(r"/[A-Za-z0-9_.]+|\d+", differences):
        if token.isdigit():
            code = int(token)
        else:
            by_code[code] = token[1:]
            code += 1
    return by_code


def repair_pdf(source, destination, mapping):
    with pymupdf.open(source) as doc:
        font_ids = {font[0] for page in doc for font in page.get_fonts()
                    if font[3].split("+")[-1] == "LMMathExtension10-Regular"}
        if not font_ids:
            raise ValueError(f"Missing expected font in {source}")
        for font in sorted(font_ids):
            cmap_ref = int(doc.xref_get_key(font, "ToUnicode")[1].split()[0])
            cmap = doc.xref_stream(cmap_ref)
            block = re.search(rb"(\d+) beginbfchar\s*([\s\S]*?)endbfchar", cmap)
            if not block or b"0 beginbfrange" not in cmap:
                raise ValueError("unexpected embedded character mapping")
            mapped = {int(a, 16) for a in re.findall(rb"<([0-9A-F]{2})>\s+<[0-9A-F]+>", block[2])}
            missing = []
            for code, name in font_encoding(doc, font).items():
                if code not in mapped:
                    value = mapping[name].replace(" ", "")
                    missing.append(f"<{code:02X}> <{value}>".encode("ascii"))
            if not missing:
                raise ValueError("expected missing mappings")
            # A separate bfchar block preserves the existing, including private-use, mappings.
            extra = str(len(missing)).encode() + b" beginbfchar\n" + b"\n".join(missing) + b"\nendbfchar\n"
            doc.update_stream(cmap_ref, cmap.replace(b"endcmap\n", extra + b"endcmap\n"), compress=True)
        # The remaining five arrows consist of a bar and a right arrow. Give their *pair*
        # one text alternative. Mapping the first glyph to a whole arrow would duplicate it.
        for page in doc:
            symbols = [row for row in page.get_fonts()
                       if row[3].split("+")[-1] == "LMMathSymbols10-Regular"]
            for font, _, _, _, resource_name, *_ in symbols:
                by_code = font_encoding(doc, font)
                if by_code.get(55) != "mapsto" or by_code.get(33) != "arrowright":
                    continue
                pattern = rb"(/" + re.escape(resource_name.encode()) + rb" [\d.]+ Tf [^\[\]/]{0,90})(\[\(7!\)\]TJ)"
                for stream_ref in page.get_contents():
                    raw = doc.xref_stream(stream_ref)
                    tagged = re.sub(pattern, rb"\1/Span <</ActualText <FEFF21A6>>> BDC \2 EMC ", raw)
                    if raw != tagged:
                        doc.update_stream(stream_ref, tagged, compress=True)
        doc.save(destination, no_new_id=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_mapping", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = args.tex_mapping.read_bytes()
    if hashlib.sha256(data).hexdigest() != MAPPING_SHA256:
        raise ValueError("The TeX character map has changed; review it before regenerating.")
    definitions = data.decode().split("%% Glyphs from the cmex fonts:")[1]
    mapping = dict(re.findall(r"^\\pdfglyphtounicode\{([^}]+)\}\{([0-9A-F ]+)\}", definitions, re.M))
    papers = Path(__file__).resolve().parents[1]
    args.output.mkdir(exist_ok=False, parents=True)
    for paper_id in READERS:
        source, = (papers.parent / "edition" / "PAPERS").glob(f"{paper_id}_*/*.pdf")
        destination = args.output / f"{paper_id}.pdf"
        repair_pdf(source, destination, mapping)
