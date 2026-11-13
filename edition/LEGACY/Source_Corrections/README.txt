DOCUMENTED PROSE CORRECTIONS

The five main-volume components listed in Source_Correction_Index.json carry
limited corrections to result-status and scope prose. Their formulas, theorem
premises and page counts are preserved. Available current Markdown and TeX
are in Editable_Articles/ and Typesetting_Source/ respectively.

Text_Article_Corrections.json gives the exact old and replacement source spans
for the three articles with editable sources. The fourth-moment article's
standalone TeX was generated from its supplied Markdown; article_header.tex is
the generation header, already incorporated into that standalone TeX.

Original_PDF_Inputs/ contains only the two exact source PDFs necessary to
reproduce the limited PDF-only corrections. Their earlier scope prose is
preserved solely as a reproduction input. The revised components under
Mathematical_Supplement/ supply the current account. These two source PDFs are
not additional main-volume components and are excluded from its component count.
Complete superseded source editions and other original inputs are preserved
separately.

PDF_Scope_Corrections.json pins the original PDF hashes, component page,
rectangle, original text, font resource and replacement lines. Its source-volume
locators explicitly refer to the preceding 444-page supplement. Current article
ranges are given in the top-level CONTENTS.txt and VOLUME_CONTENTS.json.
The component page and rectangle are the operative coordinates for reproduction.

The portable script reads the source without altering it and refuses existing
output or receipt files. It checks text and pixels outside each declared region
on all pages, plus outlines and links. Original embedded font resources are
reused. Original Content Credentials remain with the source inputs; they do not
attest to the edited derivatives. The inherited attachment entries were removed
from those two derivatives. These are document checks, not mathematical proofs.

From the package root, use new output paths:

  python tools/apply_document_scope_corrections.py --source Source_Corrections/Original_PDF_Inputs/Finite_Part_of_Wilson_Dirac_Relative_Entropy.pdf --output Reproduced_Corrections/Finite_Part_of_Wilson_Dirac_Relative_Entropy.pdf --edits Source_Corrections/PDF_Scope_Corrections.json --entry finite-part --receipt Reproduced_Corrections/Finite_Part_receipt.json

  python tools/apply_document_scope_corrections.py --source Source_Corrections/Original_PDF_Inputs/Uniform_Modular_Control_and_Nonlinear_Convergence_for_Wilson_Dirac_Intervals.pdf --output Reproduced_Corrections/Uniform_Modular_Control_and_Nonlinear_Convergence_for_Wilson_Dirac_Intervals.pdf --edits Source_Corrections/PDF_Scope_Corrections.json --entry uniform-modular --receipt Reproduced_Corrections/Uniform_Modular_receipt.json

PyMuPDF 1.26.6 was used for the recorded byte-identical reproduction. The public
specification changes only the explanatory locator label from the tested
specification; every PDF-operation field is unchanged. Other software versions
can alter PDF serialization. The supplied source and output digests identify
the actual versions delivered.

To compile the three standalone editable articles:

  python tools/build_corrected_articles.py --source-dir Typesetting_Source --output-dir Recompiled_Articles

The wrapper requires a new directory and runs two XeLaTeX passes with
-no-shell-escape. This option was added after the supplied PDF compilations;
no new compilation of the wrapper variant is claimed. The TeX files require
no local input, preamble or image file. Fonts and ordinary TeX package
requirements are stated in the wrapper and the manuscript preambles.
