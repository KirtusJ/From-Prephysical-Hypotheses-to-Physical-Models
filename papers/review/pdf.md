# Research-paper PDF review

The Z26 paper index contains 41 entries. Forty have an assembled PDF, totaling 692 issued pages. F7 is planned. The 100 component PDFs and 27 PDFs under paper source directories were counted separately. [Issued paper index](../../edition/PROGRAM/PAPER_INDEX.md)

The current reader catalog contains 40 PDFs and 683 pages. All 683 pages were rerendered after the corrections. All contained visible ink and none had visible glyph ID zero or traced text beyond the page. The four re-typeset papers G7–G10 contain 17, 10, 12 and 50 pages respectively. Visual inspection of their opening and final pages confirmed that their author and contribution lines, final references and page numbers fit. Use the catalog hashes to identify the reader copies. [Reader catalog](../catalog.csv) · [Mathematical corrections](math.md)

## Inspection

At source commit `9ba569b1fed1411913438de7c2b58e0ed4ce1837`, the repository held 221 loose PDFs and 201 further PDF occurrences inside its Z3 ZIP. Deduplication by SHA-256 left 210 distinct files. PyMuPDF 2.1 rendered every one of their 1,532 pages in grayscale at 72 dpi. The checks covered empty rasters, text extending beyond the page, glyph ID zero, Unicode replacement characters, nonembedded fonts, and ink touching the trim. The count includes ancillary and quarantined files as inventory only. [Issued edition](../../edition/README.md) · [Z3 archive](../../edition_archives/)

All 1,532 pages opened and rendered without structural repair. Every page had visible ink. No visible glyph had ID zero. None of the 40 issued papers contained traced text outside its page boundary. A second screen flagged 26 pages where adjoining word boxes overlapped, including duplicate component copies. Visual inspection at the flagged locations showed stacked binomial arguments, indices, operators and fractions. The 22 edge marks in B1 are full-width colored header rules. The large lower margins on several title pages separate the summary from the credits. An omitted symbol at typesetting time can leave no glyph to inspect. Source comparison is necessary for that class of error. [B1](../B1%20-%20What%20Does%20an%20Observation%20Identify%20%E2%80%93%20A%20Synthesis%20with%20Supporting%20Notes.pdf) · [D7](../D7%20-%20Reference%20Modular%20and%20Jacobi%20Estimates%20for%20a%20Half-Filled%20Fermion%20Interval.pdf) · [F6](../F6%20-%20Statistical%20Comparisons%20and%20Reference%20Errors.pdf)

## Seven corrected reader text layers

The equation shapes rendered in the issued papers, but a raw character trace returned U+FFFD for 490 glyph instances. In 485 instances the embedded Latin Modern math-extension font specified a glyph name but its PDF lacked the corresponding Unicode entry. The reader copies add the named entries from the TeX `pdfx` mapping, including the size variation selectors. The remaining five are mapsto arrows. TeX draws each as two glyphs. A single PDF `ActualText` span now returns U+21A6 when copied. PyMuPDF’s raw drawing trace still sees the two constituent glyphs in these five cases. [TeX glyph mapping](https://mirrors.ctan.org/macros/latex/contrib/pdfx/glyphtounicode-cmr.tex) · [Reproduction script](restore_math_text.py)

| Reader | Previously unmapped instances | Added Unicode entries, counted by use | Mapsto text spans |
| --- | ---: | ---: | ---: |
| [C3](../C3%20-%20Calibrated%20Dynamical%20Identification%20in%20Fermionic%20Systems.pdf) | 42 | 41 | 1 |
| [C5](../C5%20-%20Continuum%20and%20Finite-Lattice%20Two-Time%20Identification.pdf) | 42 | 42 | 0 |
| [C6](../C6%20-%20Local%20Number-Conserving%20Response%20and%20Inference.pdf) | 69 | 67 | 2 |
| [C7](../C7%20-%20Restricted%20Observables%20and%20CAR-State%20Distinguishability.pdf) | 29 | 28 | 1 |
| [D3](../D3%20-%20Finite%20Part%20of%20Wilson%E2%80%93Dirac%20Relative%20Entropy.pdf) | 103 | 103 | 0 |
| [D4](../D4%20-%20Uniform%20Modular%20Control%20and%20Nonlinear%20Convergence%20for%20Wilson%E2%80%93Dirac%20Intervals.pdf) | 77 | 77 | 0 |
| [D6](../D6%20-%20Concentration%20Spectrum%20of%20the%20Half-Filled%20Sine%20Kernel%20%E2%80%93%20Periods%2C%20Tails%20and%20Plunge%20Windows.pdf) | 128 | 127 | 1 |

At the 14 November math-text revision (commit `c143ec4`), all 90 pages in those seven reader files were pixel-identical to the issued copies under two independent renderers, PyMuPDF at 144 dpi and Poppler at 90 dpi. Object-level comparison confined the differences to the seven Unicode maps and the five text-equivalence spans. The drawing commands inside each span and every other decoded page-content stream matched the originals. All five semantic arrows read back correctly. These checks cover the repaired glyphs. Flattened line extraction can still reorder multidimensional expressions. Use the typeset mathematics or its TeX source for the full expression.

## Contribution revision and filenames

All 40 PDFs now carry their full manuscript titles in the filenames. A comparison with the preceding reader edition covered all 683 pages at 108 dpi. On 87 pages the only changed pixels fell within the declared acknowledgment regions. The other 596 pages matched pixel for pixel. The 27 papers that carried a broader-program roster retain that acknowledgment. The seven repaired math-font mappings were byte-identical, and all five composite arrows still copied correctly. In D6 the credit paragraph on page 15 now says “even-size” where it previously used a typeset $N$. The mathematical text elsewhere retained its glyph positions.

The 36 readings updated by localized replacement reproduced byte for byte from the pinned revision. An independent Tectonic 0.17 build of G7–G10 reproduced the text and rendered page content across their 89 pages. PDF creation metadata can differ on rebuild. [Credit edit specification](reader_credits.json) · [Reproduction script](repair_reader_credits.py) · [Paper contribution records](../contributions.md)

## Ancillary clipping

Two references pages in the retained FAR-1 negative control have visible right-edge clipping. The overview’s page 6 extends up to 69.0 points beyond the page and the specification’s page 11 extends up to 89.3 points. The same bytes occur inside the historical Z3 archive. Both documents are filed under negative controls. [Overview](../../edition/NEGATIVE_CONTROLS/FAR-1/Toy_Universe_Overview.pdf#page=6) · [Specification](../../edition/NEGATIVE_CONTROLS/FAR-1/Toy_Universe_Specification.pdf#page=11)
