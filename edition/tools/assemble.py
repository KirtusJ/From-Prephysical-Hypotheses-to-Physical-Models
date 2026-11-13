#!/usr/bin/env python3
"""Assemble the 12 November 2026 baseline of From Prephysical Hypotheses to Physical Models.

Inputs: the 10 November 2026 review packet (extracted), manuscripts compiled by build_tex.py, the new
Sobolev-bound note, and paper_plan.py.  Outputs: PAPERS/ (one folder and one assembled PDF per paper),
and the registers under PROGRAM/registers/.  Program documents, review records and the manifest are
written by finalize.py.
"""
import csv, hashlib, json, os, re, shutil, subprocess, sys, unicodedata
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_plan import P, STUDIES, SERIES, AUTHOR, AUTHOR_TITLE, AUTHOR_LOCATION, PROGRAM, BASELINE_DATE, BASELINE_ID, check_plan

SRC = "/home/claude/work/Review_Materials"
TEX = "/home/claude/bb/tex"
OUT = "/home/claude/bb/out/FPHPM_Baseline_2026-11-12"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
VC = json.load(open(os.path.join(SRC, "VOLUME_CONTENTS.json")))
COMP = VC["components"]

def sha(path): return hashlib.sha256(open(path, "rb").read()).hexdigest()
def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("\u2013", "-").replace("\u2014", "-")).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
def tex_escape(s):
    s = unicodedata.normalize("NFKC", s)
    s = "".join(ch for ch in s if ch == "\n" or (ord(ch) < 0x2100 and unicodedata.category(ch)[0] != "C") or ch in "\u2013\u2014\u2018\u2019\u201c\u201d")
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
                 ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

# ---------------------------------------------------------------- location normalization
LOC_RE = re.compile(r"Vancouver(?:, British Columbia)?(?:(?: \u00b7|,)? ?(?:Pacific Time|PCT) \(UTC.7\))?")
def normalize_location(src, dst):
    doc = pymupdf.open(src); n = 0
    for page in doc:
        spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]
        todo = [s for s in spans if "Vancouver" in s["text"]]
        if not todo: continue
        pix = page.get_pixmap(dpi=72)
        jobs = []
        for s in todo:
            new = LOC_RE.sub(AUTHOR_LOCATION, s["text"])
            assert "Vancouver" not in new, new
            x0, y0, x1, y1 = s["bbox"]
            px = pix.pixel(max(0, int(x0) - 2), int((y0 + y1) / 2))
            fill = tuple(c / 255 for c in px[:3])
            neighbours = [t["bbox"][0] for t in spans if t is not s and t["bbox"][0] >= x1 - 0.5 and abs(t["bbox"][1] - y0) < 4 and t["text"].strip()]
            limit = (min(neighbours) if neighbours else page.rect.width - x0) - 5
            jobs.append((s, new, fill, limit))
            page.add_redact_annot(pymupdf.Rect(x0, y0 + 0.6, x1, y1 - 0.6), fill=fill)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
        for s, new, fill, limit in jobs:
            ff = SERIF if "Serif" in s["font"] else SANS
            font = pymupdf.Font(fontfile=ff); size = s["size"]
            width = font.text_length(new, fontsize=size)
            if s["origin"][0] + width > limit:
                size *= (limit - s["origin"][0]) / width
                assert size >= 0.8 * s["size"], (src, new, size)
            c = s["color"]; rgb = ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)
            page.insert_text(s["origin"], new, fontsize=size, fontfile=ff, fontname="NormLoc", color=rgb)
            n += 1
    doc.save(dst, garbage=3, deflate=True); doc.close()
    chk = "".join(p.get_text() for p in pymupdf.open(dst))
    assert "Vancouver" not in chk, dst
    return n

# ---------------------------------------------------------------- statement extraction
ST_RE = re.compile(r"^[ \t]*(Theorem|Proposition|Lemma|Corollary)( used here)?(?:\s{1,3}([A-Z]?\d+(?:\.\d+)*))?(?:\s{0,3}\(([^)]{3,160})\))?\.(?=\s)", re.M)
def statements(pdf):
    doc = pymupdf.open(pdf); out = []; texts = [p.get_text() for p in doc]
    full = ""; offs = []
    for t in texts: offs.append(len(full)); full += t + "\n"
    ms = [m for m in ST_RE.finditer(full) if m.group(3) or m.group(4)]
    seen = set()
    for i, m in enumerate(ms):
        key = (m.group(1), m.group(3), (m.group(4) or "")[:40])
        if m.group(3) and (m.group(1), m.group(3)) in seen: continue      # an in-text line that begins with a reference
        if m.group(3): seen.add((m.group(1), m.group(3)))
        end = ms[i + 1].start() if i + 1 < len(ms) else len(full)
        seg = full[m.end():end]
        page = max(k for k, o in enumerate(offs) if o <= m.start()) + 1
        name = re.sub(r"\s+", " ", m.group(4) or "").strip()
        name = unicodedata.normalize("NFKC", name)
        imported = bool(m.group(2)) or "imported" in name.lower()
        has_proof = bool(re.search(r"(^|\n)\s*Proof\b", seg))
        if imported: status = "RESTATEMENT"
        elif "conditional" in name.lower(): status = "CONDITIONAL_ON_NAMED_INPUTS"
        elif has_proof: status = "PROOF_IN_MANUSCRIPT"
        else: status = "PROOF_NOT_ADJACENT"
        out.append(dict(kind=m.group(1), number=m.group(3) or "", name=name, page=page, status=status))
    return out, full

# ---------------------------------------------------------------- parts
def component_sources(pdf_rel):
    stem = os.path.basename(pdf_rel)[:-4]; found = []
    for d in ("Editable_Articles", "Typesetting_Source", "New_Studies"):
        for r, _, fs in os.walk(os.path.join(SRC, d)):
            for f in fs:
                if os.path.splitext(f)[0] == stem and not f.endswith(".pdf"): found.append(os.path.join(r, f))
    return found

def gather_parts(p, pdir):
    parts = []; os.makedirs(os.path.join(pdir, "parts"), exist_ok=True); os.makedirs(os.path.join(pdir, "source"), exist_ok=True)
    for n, (kind, key) in enumerate(p["parts"], 1):
        rec = dict(no=n, kind=kind, key=key, sources=[])
        if kind == "component":
            c = COMP[key]; src = os.path.join(SRC, c["pdf"]); assert sha(src) == c["sha256"]
            rec.update(title=c["title"], legacy_path=c["pdf"], legacy_sha256=c["sha256"], legacy_volume=c["volume"],
                       legacy_pages=f'{c["first_page"]}-{c["last_page"]}')
            dst = os.path.join(pdir, "parts", f"{n:02d}_{os.path.basename(c['pdf'])}")
            if "Vancouver" in "".join(pg.get_text() for pg in pymupdf.open(src)):
                k = normalize_location(src, dst); rec["change"] = f"location line normalized to {AUTHOR_LOCATION} ({k} text spans); all other content unchanged"
            else:
                shutil.copy(src, dst); rec["change"] = "byte-identical"
            for s in component_sources(c["pdf"]):
                tag = "editable" if "Editable_Articles" in s else ("typesetting" if "Typesetting_Source" in s else "study")
                d2 = os.path.join(pdir, "source", f"{n:02d}_{tag}_{os.path.basename(s)}"); shutil.copy(s, d2); rec["sources"].append(os.path.relpath(d2, OUT))
        elif kind in ("study", "split"):
            wd = os.path.join(TEX, p["id"]); name = f"{p['id']}_manuscript"
            rec.update(title=p["title"], legacy_path="Studies/Source/" + STUDIES[key][0] if kind == "study" else
                       "New_Studies/Calibration_and_Uniform_Limits_Source/" + ("Joint_Calibration_and_Sampling.tex" if key == "joint_calibration" else "Wilson_Uniform_Limits.tex"),
                       legacy_sha256="", legacy_volume="", legacy_pages="",
                       change="recompiled standalone from the supplied TeX with a new title page; body edits listed in tex_edits.json")
            dst = os.path.join(pdir, "parts", f"{n:02d}_{name}.pdf"); shutil.copy(os.path.join(wd, name + ".pdf"), dst)
            for f in sorted(os.listdir(wd)):
                if f.endswith(".tex"):
                    d2 = os.path.join(pdir, "source", f); shutil.copy(os.path.join(wd, f), d2); rec["sources"].append(os.path.relpath(d2, OUT))
        elif kind == "new":
            wd = os.path.join(TEX, "D8_new"); name = "D8_Uniform_Sobolev_Bound"
            rec.update(title="A Uniform Sobolev Bound for the Continuum Cross-Block Interpolants", legacy_path="", legacy_sha256="",
                       legacy_volume="", legacy_pages="", change="first issued with this baseline")
            dst = os.path.join(pdir, "parts", f"{n:02d}_{name}.pdf"); shutil.copy(os.path.join(wd, name + ".pdf"), dst)
            d2 = os.path.join(pdir, "source", f"{n:02d}_{name}.tex"); shutil.copy(os.path.join(wd, name + ".tex"), d2); rec["sources"].append(os.path.relpath(d2, OUT))
        elif kind == "figure":
            d = [x for x in VC["diagrams"] if ("Program" in x["title"]) == (key == "program")][0]
            src = os.path.join(SRC, d["pdf"])
            rec.update(title="Figure: " + d["title"], legacy_path=d["pdf"], legacy_sha256=sha(src), legacy_volume="", legacy_pages="", change="byte-identical")
            dst = os.path.join(pdir, "parts", f"{n:02d}_{os.path.basename(d['pdf'])}"); shutil.copy(src, dst)
            for extra in ([d["source"]] + (["Diagram/source/build_program_scope_diagram.py", "Diagram/Program_Questions_Models_and_Physical_Correspondence.svg"] if key == "program" else [])):
                if os.path.exists(os.path.join(SRC, extra)) and not extra.endswith(".pdf"):
                    d2 = os.path.join(pdir, "source", f"{n:02d}_{os.path.basename(extra)}"); shutil.copy(os.path.join(SRC, extra), d2); rec["sources"].append(os.path.relpath(d2, OUT))
        elif kind == "planned":
            rec.update(title=p["title"], note=key); parts.append(rec); continue
        rec["pdf"] = dst; rec["pages"] = pymupdf.open(dst).page_count; rec["sha256"] = sha(dst)
        parts.append(rec)
    return parts

# ---------------------------------------------------------------- cover
ACK = (f"{AUTHOR} directed the research questions, the selection of mathematical models and the publication standards, is the sole named "
       "author, and is responsible for the claims presented here. ChatGPT (OpenAI) assisted with derivations, critical checks and manuscript "
       "preparation. Claude (Anthropic), Gemini (Google), Grok (SpaceXAI) and DeepSeek (High-Flyer) contributed to the wider research process; "
       "attribution of particular arguments is limited to traceable records. Editorial preparation of this edition: Claude (Anthropic). "
       "Assistance does not imply provider endorsement, external peer review or institutional endorsement.")

def cover_tex(p, parts, rows, offset):
    L = [r"\documentclass[11pt,a4paper]{article}", r"\input{Scientific_Preamble.tex}",
         rf"\hypersetup{{pdftitle={{{tex_escape(p['title'])}}},pdfauthor={{{AUTHOR}}}}}", r"\begin{document}", r"\thispagestyle{empty}\pagestyle{empty}",
         rf"{{\small\sffamily \ProgramTitle\hfill Paper {p['id']}\par}}", r"\vspace*{12mm}",
         rf"{{\LARGE\bfseries\raggedright\hyphenpenalty=10000 {tex_escape(p['title'])}\par}}", r"\vspace{9mm}",
         rf"{{\large {AUTHOR}\par}}\vspace{{1mm}}{AUTHOR_TITLE}\par\AuthorLocation\par\vspace{{2mm}}Baseline edition, {BASELINE_DATE}\par\vspace{{8mm}}"]
    if p.get("scope"): L += [r"\textbf{Scope}\par", tex_escape(p["scope"]) + r"\par\vspace{5mm}"]
    L += [r"\textbf{Contents}\par\vspace{1mm}", r"{\small\begin{longtable}{@{}r>{\raggedright\arraybackslash}p{0.72\textwidth}r@{}}", r"\toprule Part & Title & Page\\\midrule\endhead"]
    pg = offset + 1
    for r in parts:
        L.append(rf"{r['no']} & {tex_escape(r['title'])} & {pg}\\"); r["file_page"] = pg; pg += r["pages"]
    L += [r"\bottomrule\end{longtable}}", r"\vspace{2mm}\textbf{Formal statements}\par\vspace{1mm}",
          r"{\footnotesize Identifiers are those of the program theorem registry. Page numbers refer to this file.\par}",
          r"{\footnotesize\begin{longtable}{@{}l>{\raggedright\arraybackslash}p{0.66\textwidth}r@{}}", r"\toprule Identifier & Statement & Page\\\midrule\endhead"]
    for s in rows:
        label = (s["kind"] + (" " + s["number"] if s["number"] else "") + (f" ({s['name']})" if s["name"] else "")) if s["kind"] != "Note" else s["name"]
        fp = next(r for r in parts if r["no"] == s["part"])["file_page"] + s["page"] - 1
        L.append(rf"{s['id']} & {tex_escape(label)} & {fp}\\")
    L += [r"\bottomrule\end{longtable}}", r"\vspace{3mm}\textbf{Acknowledgments and contributions}\par", r"{\small " + ACK + r"\par}", r"\end{document}"]
    return "\n".join(L)

def build_cover(p, parts, rows, pdir):
    wd = os.path.join(pdir, "source", "cover"); os.makedirs(wd, exist_ok=True)
    shutil.copy(os.path.join(SRC, "Studies/Source/Scientific_Preamble.tex"), wd)
    n = 1
    for attempt in range(4):
        open(os.path.join(wd, "cover.tex"), "w").write(cover_tex(p, parts, rows, n))
        for _ in range(2):
            r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "cover.tex"], cwd=wd, capture_output=True, text=True)
            if r.returncode: print(r.stdout[-2500:]); raise SystemExit("cover failed " + p["id"])
        m = pymupdf.open(os.path.join(wd, "cover.pdf")).page_count
        if m == n: break
        n = m
    for f in os.listdir(wd):
        if f.split(".")[-1] in ("aux", "log", "out"): os.remove(os.path.join(wd, f))
    return os.path.join(wd, "cover.pdf"), n

# ---------------------------------------------------------------- main
def main():
    check_plan()
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "PAPERS")); reg = os.path.join(OUT, "PROGRAM", "registers"); os.makedirs(reg)
    registry, crosswalk, index, texts = [], [], [], {}
    for p in P:
        pdir = os.path.join(OUT, "PAPERS", f"{p['id']}_{slug(p['title'])[:70]}")
        parts = gather_parts(p, pdir); p["_dir"] = pdir; p["_parts"] = parts
        if p["kind"] == "planned":
            shutil.rmtree(os.path.join(pdir, "parts")); shutil.rmtree(os.path.join(pdir, "source"))
            open(os.path.join(pdir, "PLANNED.md"), "w").write(f"# Paper {p['id']}: {p['title']}\n\n{AUTHOR}, {AUTHOR_TITLE}\n{AUTHOR_LOCATION}\n\n{parts[0]['note']}\n")
            index.append(dict(id=p["id"], series=SERIES[p["id"][0]], title=p["title"], kind=p["kind"], file="PLANNED.md", pages=0, parts=0, statements=0)); continue
        rows = []
        for r in parts:
            if r["kind"] == "figure": continue
            sts, full = statements(r["pdf"]); texts[(p["id"], r["no"])] = full
            if not sts: sts = [dict(kind="Note", number="", name=r["title"], page=1, status="RESULT_NOTE_WITHOUT_LABELLED_STATEMENT")]
            for k, s in enumerate(sts, 1):
                s.update(id=f"{p['id']}-{r['no']:02d}-{k:02d}", paper=p["id"], part=r["no"], part_title=r["title"]); rows.append(s)
        single_compiled = len([r for r in parts if r["kind"] != "figure"]) == 1 and parts[0]["kind"] in ("study", "split")
        out_pdf = os.path.join(pdir, f"{p['id']}_{slug(p['title'])[:70]}.pdf")
        doc = pymupdf.open(); toc = []
        if single_compiled:
            off = 0
            for r in parts: r["file_page"] = off + 1; off += r["pages"]
        else:
            cov, off = build_cover(p, parts, rows, pdir); doc.insert_pdf(pymupdf.open(cov)); toc.append([1, "Title, contents and formal statements", 1])
        for r in parts:
            doc.insert_pdf(pymupdf.open(r["pdf"])); toc.append([1, r["title"][:120], r["file_page"]])
        doc.set_toc(toc)
        doc.set_metadata(dict(title=p["title"], author=AUTHOR, subject=f"{PROGRAM}; paper {p['id']}; {BASELINE_ID}", keywords=f"{AUTHOR_TITLE}; {AUTHOR_LOCATION}"))
        doc.save(out_pdf, garbage=3, deflate=True); total = doc.page_count; doc.close()
        for s in rows:
            fp = next(r for r in parts if r["no"] == s["part"])["file_page"] + s["page"] - 1
            pk = next(r for r in parts if r["no"] == s["part"])
            ltitle = s["part_title"]; lnum = s["number"]
            if pk["kind"] == "split":
                ltitle = "Calibration, Identified Sets and Uniform Limits (10 November 2026)"
                if pk["key"] == "wilson_uniform": lnum = "7"
            elif pk["kind"] == "study":
                ltitle = "Mathematical Supplement, opening studies (10 November 2026): " + STUDIES[pk["key"]][2]
            legacy = "" if s["kind"] == "Note" or pk["kind"] == "new" else f"{ltitle}, {s['kind']}{' ' + lnum if lnum else ''}{' (' + s['name'] + ')' if s['name'] else ''}"
            registry.append(dict(id=s["id"], paper=p["id"], part=s["part"], part_title=s["part_title"], kind=s["kind"], number=s["number"], name=s["name"],
                                 status=s["status"], paper_file_page=fp, part_page=s["page"], legacy_locator=legacy))
        for r in parts:
            crosswalk.append(dict(paper=p["id"], part=r["no"], title=r["title"], kind=r["kind"], legacy_path=r.get("legacy_path", ""), legacy_volume=r.get("legacy_volume", ""),
                                  legacy_volume_pages=r.get("legacy_pages", ""), legacy_sha256=r.get("legacy_sha256", ""), baseline_path=os.path.relpath(r["pdf"], OUT),
                                  baseline_sha256=r["sha256"], pages=r["pages"], change=r["change"], editable_sources=len(r["sources"])))
        index.append(dict(id=p["id"], series=SERIES[p["id"][0]], title=p["title"], kind=p["kind"], file=os.path.relpath(out_pdf, OUT), pages=total,
                          parts=len(parts), statements=len([s for s in rows if s["kind"] != "Note"])))
        print(p["id"], total, "pages", len(rows), "registry rows")
    # legacy split record for component 10
    c = COMP[10]
    crosswalk.append(dict(paper="D5+F4", part="", title=c["title"] + " (10 November 2026 combined study)", kind="legacy", legacy_path=c["pdf"], legacy_volume=c["volume"],
                          legacy_volume_pages=f'{c["first_page"]}-{c["last_page"]}', legacy_sha256=c["sha256"], baseline_path="LEGACY/" + os.path.basename(c["pdf"]),
                          baseline_sha256=c["sha256"], pages=c["pages"], change="separated into papers F4 (Theorems 1, 3, 6; Propositions 2, 5; Lemma 4) and D5 (legacy Proposition 7); retained byte-identical for citation",
                          editable_sources=3))
    # ---- citations between papers
    def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower().replace("\u2013", "-")).strip()
    titles = []
    for p in P:
        if p["kind"] == "planned": continue
        for r in p["_parts"]:
            if r["kind"] != "figure":
                key = " ".join(norm(r["title"]).split()[:6])
                if len(key.split()) >= 3: titles.append((key, p["id"], r["no"], r["title"]))
    cites = []; loc_re = re.compile(r"(Theorem|Proposition|Lemma|Corollary|[Ee]quation|Section)s?\s+(\(?[A-Z]?\d+(?:\.\d+)?\)?)(?:\s+and\s+(?:[a-z]+\s+)?\(?\d+\)?)?\s+of\s+([A-Z][A-Za-z\u2013\u2019 \-]{8,100})")
    for (pid, no), full in texts.items():
        flat = norm(full)
        for key, tp, tn, tt in titles:
            if (tp, tn) != (pid, no) and key in flat:
                cites.append(dict(citing_paper=pid, citing_part=no, cited_paper=tp, cited_part=tn, cited_title=tt, evidence="title mention", locator=""))
        for m in loc_re.finditer(full.replace("\n", " ")):
            tgt = norm(m.group(3))
            for key, tp, tn, tt in titles:
                if tgt.startswith(" ".join(key.split()[:4])):
                    cites.append(dict(citing_paper=pid, citing_part=no, cited_paper=tp, cited_part=tn, cited_title=tt, evidence="explicit locator", locator=f"{m.group(1)} {m.group(2)}")); break
    seen = set(); cites2 = []
    for c_ in cites:
        k = tuple(c_.values())
        if k not in seen: seen.add(k); cites2.append(c_)
    for p in P:
        p["depends"] = sorted({c_["cited_paper"] for c_ in cites2 if c_["citing_paper"] == p["id"] and c_["cited_paper"] != p["id"]}) or p["depends"]
    for row in index: row["cites_papers"] = " ".join(next(p for p in P if p["id"] == row["id"])["depends"])
    def wcsv(name, rows):
        with open(os.path.join(reg, name), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    wcsv("THEOREM_REGISTRY.csv", registry); wcsv("COMPONENT_CROSSWALK.csv", crosswalk); wcsv("PAPER_INDEX.csv", index); wcsv("CITATIONS_BETWEEN_PAPERS.csv", cites2)
    shutil.copy(os.path.join(TEX, "tex_edits.json"), os.path.join(reg, "TEX_SOURCE_EDITS.json"))
    json.dump(dict(papers=len(P), registry_rows=len(registry), crosswalk_rows=len(crosswalk), citations=len(cites2)), open("/home/claude/bb/assemble_summary.json", "w"))
    print(len(registry), "registry rows;", len(crosswalk), "crosswalk rows;", len(cites2), "citation edges")

if __name__ == "__main__":
    main()
